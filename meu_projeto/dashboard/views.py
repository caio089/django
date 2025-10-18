from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from payments.models import Pagamento, Assinatura, PlanoPremium
from django.contrib.auth.models import User
from django.contrib import messages
import json


def clear_dashboard_cache():
    """Limpa o cache do dashboard quando há mudanças importantes"""
    cache.delete('dashboard_stats')
    cache.delete('dashboard_recent_users')


def admin_login(request):
    """
    Página de login exclusiva para o dashboard administrativo
    Credenciais: admin / limueiro
    """
    # Se já está logado como admin, redireciona para o dashboard
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard_admin')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar se é superusuário
            if user.is_superuser:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}! 🎉')
                
                # Redirecionar para o dashboard ou para a página solicitada
                next_url = request.GET.get('next', 'dashboard_admin')
                return redirect(next_url)
            else:
                messages.error(request, '❌ Acesso negado! Apenas administradores podem acessar.')
        else:
            messages.error(request, '❌ Usuário ou senha incorretos!')
    
    return render(request, 'dashboard/admin_login.html')


def admin_logout(request):
    """
    Logout do dashboard administrativo
    """
    logout(request)
    messages.success(request, '✅ Logout realizado com sucesso!')
    return redirect('admin_login')




@login_required(login_url='/dashboard/login/')
def dashboard_admin(request):
    """
    Dashboard administrativo para visualizar assinaturas premium e receitas
    Requer login de superusuário
    """
    
    # Verificar se o usuário é admin ou tem permissão
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar o dashboard administrativo.')
        return render(request, 'dashboard/access_denied.html')
    
    # Data atual
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    # === ESTATÍSTICAS GERAIS ===
    
    # Cache das estatísticas por 5 minutos
    cache_key_stats = 'dashboard_stats'
    stats = cache.get(cache_key_stats)
    
    if not stats:
        # Total de assinaturas ativas
        active_subscriptions = Assinatura.objects.filter(
            status='ativa'
        ).count()
        
        # Total de usuários premium únicos
        unique_premium_users = Assinatura.objects.filter(
            status='ativa'
        ).values('usuario').distinct().count()
        
        stats = {
            'active_subscriptions': active_subscriptions,
            'unique_premium_users': unique_premium_users
        }
        cache.set(cache_key_stats, stats, 300)  # Cache por 5 minutos
    else:
        active_subscriptions = stats['active_subscriptions']
        unique_premium_users = stats['unique_premium_users']
    
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
    
    recent_subscriptions = Assinatura.objects.select_related('usuario', 'plano').filter(
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
    
    # Cache dos usuários recentes por 2 minutos
    cache_key_users = 'dashboard_recent_users'
    recent_users_data = cache.get(cache_key_users)
    
    if not recent_users_data:
        # Últimos usuários cadastrados com informação de assinatura ativa
        # OTIMIZAÇÃO: Usar select_related e prefetch_related para evitar N+1 queries
        recent_users = User.objects.select_related().prefetch_related('assinaturas').order_by('-date_joined')[:20]
        
        # OTIMIZAÇÃO: Buscar todas as assinaturas ativas de uma vez usando bulk operations
        active_subscription_user_ids = set(Assinatura.objects.filter(
            status='ativa',
            ativo=True
        ).values_list('usuario_id', flat=True))
        
        # Adicionar informação de assinatura ativa para cada usuário (sem consultas extras)
        for user in recent_users:
            user.has_active_subscription = user.id in active_subscription_user_ids
        
        recent_users_data = recent_users
        cache.set(cache_key_users, recent_users_data, 120)  # Cache por 2 minutos
    else:
        recent_users = recent_users_data
    
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


@login_required(login_url='/dashboard/login/')
def give_premium(request):
    """
    Função para atribuir plano premium a um usuário
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('dashboard_admin')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_email = request.POST.get('user_email')
        plan_id = request.POST.get('plan_id')
        
        # Validar se pelo menos um método foi fornecido
        if not user_id and not user_email:
            messages.error(request, 'Você deve fornecer um email ou selecionar um usuário da lista.')
            return redirect('dashboard_admin')
        
        if not plan_id:
            messages.error(request, 'Você deve selecionar um plano.')
            return redirect('dashboard_admin')
        
        try:
            # Buscar usuário por ID ou email
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(email=user_email.strip())
            
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
                
                # Limpar cache após mudanças
                clear_dashboard_cache()
        
        except User.DoesNotExist:
            if user_email:
                messages.error(request, f'Usuário com email "{user_email}" não encontrado.')
            else:
                messages.error(request, 'Usuário não encontrado.')
        except PlanoPremium.DoesNotExist:
            messages.error(request, 'Plano não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao atribuir plano: {str(e)}')
    
    return redirect('dashboard_admin')


@login_required(login_url='/dashboard/login/')
def remove_premium(request):
    """
    Função para remover plano premium de um usuário
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('dashboard_admin')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if not user_id:
            messages.error(request, 'ID do usuário não fornecido.')
            return redirect('dashboard_admin')
        
        try:
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                
                # Buscar assinaturas ativas do usuário
                assinaturas_ativas = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa'
                )
                
            if not assinaturas_ativas.exists():
                messages.warning(request, f'{user.username} não possui assinatura ativa.')
            else:
                # Cancelar todas as assinaturas ativas
                count = 0
                for assinatura in assinaturas_ativas:
                    assinatura.status = 'cancelada'
                    assinatura.ativo = False
                    assinatura.data_cancelamento = timezone.now()
                    assinatura.save()
                    count += 1
                
                messages.success(request, f'{count} assinatura(s) cancelada(s) para {user.username}!')
                
                # Limpar cache após mudanças
                clear_dashboard_cache()
        
        except User.DoesNotExist:
            messages.error(request, f'Usuário com ID {user_id} não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao remover premium: {str(e)}')
    
    return redirect('dashboard_admin')


@login_required(login_url='/dashboard/login/')
def delete_user(request):
    """
    Função para excluir um usuário com otimizações de performance
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('dashboard_admin')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        confirm = request.POST.get('confirm', '').lower()
        
        try:
            with transaction.atomic():
                # Buscar usuário com select_related para otimizar
                user = User.objects.select_related().get(id=user_id)
                
                # Proteção: não permitir excluir a si mesmo
                if user.id == request.user.id:
                    messages.error(request, 'Você não pode excluir sua própria conta!')
                    return redirect('dashboard_admin')
                
                # Proteção: não permitir excluir outros superusuários
                if user.is_superuser:
                    messages.error(request, 'Você não pode excluir outros administradores!')
                    return redirect('dashboard_admin')
                
                # Verificar confirmação (case-insensitive)
                if confirm.lower() != 'excluir':
                    messages.error(request, 'Confirmação inválida. Digite "excluir" para confirmar.')
                    return redirect('dashboard_admin')
                
                username = user.username
                email = user.email
                
                # Cancelar assinaturas ativas antes de excluir
                assinaturas_ativas = Assinatura.objects.filter(
                    usuario=user,
                    status='ativa'
                )
                
                if assinaturas_ativas.exists():
                    assinaturas_ativas.update(
                        status='cancelada',
                        ativo=False,
                        data_cancelamento=timezone.now()
                    )
                
                # Excluir usuário (isso também exclui assinaturas e perfil por cascade)
                user.delete()
                
                # Limpar cache imediatamente após exclusão
                clear_dashboard_cache()
                
                messages.success(request, f'✅ Usuário {username} ({email}) excluído com sucesso!')
        
        except User.DoesNotExist:
            messages.error(request, '❌ Usuário não encontrado.')
        except Exception as e:
            messages.error(request, f'❌ Erro ao excluir usuário: {str(e)}')
    
    return redirect('dashboard_admin')