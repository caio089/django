from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from payments.models import Pagamento, Assinatura, PlanoPremium
from django.contrib.auth.models import User
from django.contrib import messages
import json

@login_required(login_url='/admin/login/')
def dashboard_admin(request):
    """
    Dashboard administrativo para visualizar assinaturas premium e receitas
    """
    
    # Verificar se o usuário é admin ou tem permissão
    if not request.user.is_superuser:
        return render(request, 'dashboard/access_denied.html')
    
    # Data atual
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    # === ESTATÍSTICAS GERAIS ===
    
    # Total de assinaturas ativas
    active_subscriptions = Assinatura.objects.filter(
        status='ativa'
    ).count()
    
    # Total de usuários premium únicos
    unique_premium_users = Assinatura.objects.filter(
        status='ativa'
    ).values('usuario').distinct().count()
    
    # === RECEITAS ===
    
    # Receita total (todos os tempos)
    total_revenue = Pagamento.objects.filter(
        status='approved'
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Receita do mês atual
    current_month_revenue = Pagamento.objects.filter(
        status='approved',
        data_criacao__year=current_year,
        data_criacao__month=current_month
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Receita do mês passado
    last_month = now - timedelta(days=30)
    last_month_revenue = Pagamento.objects.filter(
        status='approved',
        data_criacao__gte=last_month.replace(day=1),
        data_criacao__lt=now.replace(day=1)
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # === CRESCIMENTO ===
    
    # Novos usuários premium este mês
    new_premium_this_month = Assinatura.objects.filter(
        data_criacao__year=current_year,
        data_criacao__month=current_month
    ).count()
    
    # Novos usuários premium mês passado
    new_premium_last_month = Assinatura.objects.filter(
        data_criacao__gte=last_month.replace(day=1),
        data_criacao__lt=now.replace(day=1)
    ).count()
    
    # Calcular crescimento percentual
    if new_premium_last_month > 0:
        growth_percentage = ((new_premium_this_month - new_premium_last_month) / new_premium_last_month) * 100
    else:
        growth_percentage = 100 if new_premium_this_month > 0 else 0
    
    # === HISTÓRICO DOS ÚLTIMOS 12 MESES ===
    
    monthly_data = []
    for i in range(12):
        month_date = now - timedelta(days=30*i)
        month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if i == 0:
            month_end = now
        else:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        
        month_revenue = Pagamento.objects.filter(
            status='approved',
            data_criacao__gte=month_start,
            data_criacao__lte=month_end
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        month_subscriptions = Assinatura.objects.filter(
            data_criacao__gte=month_start,
            data_criacao__lte=month_end
        ).count()
        
        monthly_data.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%b/%Y'),
            'revenue': float(month_revenue),
            'subscriptions': month_subscriptions
        })
    
    # Inverter para mostrar do mais antigo ao mais recente
    monthly_data.reverse()
    
    # === ASSINATURAS RECENTES ===
    
    recent_subscriptions = Assinatura.objects.filter(
        status='ativa'
    ).order_by('-data_criacao')[:10]
    
    # === STATUS DAS ASSINATURAS ===
    
    status_counts = Assinatura.objects.values('status').annotate(count=Count('id'))
    
    # === ESTATÍSTICAS DE USUÁRIOS ===
    
    # Total de usuários cadastrados
    total_users = User.objects.count()
    
    # Usuários cadastrados este mês
    users_this_month = User.objects.filter(
        date_joined__year=current_year,
        date_joined__month=current_month
    ).count()
    
    # Últimos usuários cadastrados
    recent_users = User.objects.order_by('-date_joined')[:20]
    
    # Planos disponíveis para atribuir
    available_plans = PlanoPremium.objects.filter(ativo=True)
    
    # === CONTEXTO ===
    
    context = {
        'active_subscriptions': active_subscriptions,
        'unique_premium_users': unique_premium_users,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
        'last_month_revenue': last_month_revenue,
        'new_premium_this_month': new_premium_this_month,
        'new_premium_last_month': new_premium_last_month,
        'growth_percentage': round(growth_percentage, 1),
        'monthly_data_json': json.dumps(monthly_data),
        'recent_subscriptions': recent_subscriptions,
        'status_counts': status_counts,
        'current_date': now.strftime('%d/%m/%Y'),
        'total_users': total_users,
        'users_this_month': users_this_month,
        'recent_users': recent_users,
        'available_plans': available_plans,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='/admin/login/')
def give_premium(request):
    """
    Função para atribuir plano premium a um usuário
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('dashboard_admin')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        plan_id = request.POST.get('plan_id')
        
        try:
            user = User.objects.get(id=user_id)
            plan = PlanoPremium.objects.get(id=plan_id)
            
            # Verificar se já tem assinatura ativa
            existing = Assinatura.objects.filter(
                usuario=user,
                status='ativa'
            ).first()
            
            if existing:
                messages.warning(request, f'{user.username} já possui uma assinatura ativa!')
            else:
                # Criar nova assinatura
                now = timezone.now()
                data_vencimento = now + timedelta(days=plan.duracao_dias)
                
                assinatura = Assinatura.objects.create(
                    usuario=user,
                    plano=plan,
                    status='ativa',
                    data_inicio=now,
                    data_vencimento=data_vencimento,
                    ativo=True
                )
                
                messages.success(request, f'Plano {plan.nome} atribuído com sucesso para {user.username}!')
        
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        except PlanoPremium.DoesNotExist:
            messages.error(request, 'Plano não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao atribuir plano: {str(e)}')
    
    return redirect('dashboard_admin')