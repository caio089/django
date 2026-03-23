from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from meu_projeto.redirect_utils import redirect_to_frontend
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
from home.models import Profile
from django.core.mail import EmailMessage
from django.conf import settings
import json


def clear_dashboard_cache():
    """Limpa o cache do dashboard quando há mudanças importantes"""
    try:
        # Lista de todas as chaves de cache do dashboard
        cache_keys = [
            'dashboard_stats',
            'dashboard_recent_users',
            'dashboard_recent_subscriptions', 
            'dashboard_status_counts',
            'dashboard_monthly_data',
            'dashboard_growth_data'
        ]
        
        # Limpar caches individuais
        for key in cache_keys:
            cache.delete(key)
        
        # Limpar cache em lote (mais eficiente)
        cache.delete_many(cache_keys)
        
        # Forçar limpeza de todos os caches relacionados a usuários
        try:
            cache.delete_pattern('*user*')
            cache.delete_pattern('*subscription*')
            cache.delete_pattern('*premium*')
        except:
            pass  # delete_pattern pode não estar disponível em todos os backends
        
        print("✅ Cache do dashboard limpo com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao limpar cache do dashboard: {e}")
        return False


def admin_login(request):
    """Redireciona para o React AdminPanel"""
    return redirect_to_frontend('/admin-panel')


def admin_logout(request):
    """Logout e redireciona para o React AdminPanel"""
    logout(request)
    return redirect_to_frontend('/admin-panel')




def dashboard_admin(request):
    """Redireciona para o React AdminPanel"""
    return redirect_to_frontend('/admin-panel')


@login_required(login_url='/dashboard/login/')
def give_premium(request):
    """Legado: redireciona ao React. O AdminPanel usa api/admin/give-premium/."""
    from meu_projeto.redirect_utils import redirect_to_frontend
    if not request.user.is_superuser:
        logout(request)
        return redirect_to_frontend('/admin-panel')
    return redirect_to_frontend('/admin-panel')


@login_required(login_url='/dashboard/login/')
def give_premium(request):
    """
    Função para atribuir plano premium a um usuário
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect_to_frontend('/admin-panel')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_email = request.POST.get('user_email')
        plan_id = request.POST.get('plan_id')
        
        # Validar se pelo menos um método foi fornecido
        if not user_id and not user_email:
            messages.error(request, 'Você deve fornecer um email ou selecionar um usuário da lista.')
            return redirect_to_frontend('/admin-panel')
        
        if not plan_id:
            messages.error(request, 'Você deve selecionar um plano.')
            return redirect_to_frontend('/admin-panel')
        
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
    
    return redirect_to_frontend('/admin-panel')


@login_required(login_url='/dashboard/login/')
def remove_premium(request):
    """
    Função para remover plano premium de um usuário
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect_to_frontend('/admin-panel')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if not user_id:
            messages.error(request, 'ID do usuário não fornecido.')
            return redirect_to_frontend('/admin-panel')
        
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
    
    return redirect_to_frontend('/admin-panel')


@login_required(login_url='/dashboard/login/')
def delete_user(request):
    """
    Função para excluir um usuário com otimizações de performance
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect_to_frontend('/admin-panel')
    
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
                    return redirect_to_frontend('/admin-panel')
                
                # Proteção: não permitir excluir outros superusuários
                if user.is_superuser:
                    messages.error(request, 'Você não pode excluir outros administradores!')
                    return redirect_to_frontend('/admin-panel')
                
                # Debug completo dos dados recebidos
                print(f"DEBUG: Dados POST completos: {request.POST}")
                print(f"DEBUG: Campo 'confirm': '{confirm}'")
                print(f"DEBUG: Tipo: {type(confirm)}")
                print(f"DEBUG: É None: {confirm is None}")
                print(f"DEBUG: É string vazia: {confirm == ''}")
                
                # Verificar se o campo existe
                if not confirm:
                    messages.error(request, 'Campo de confirmação não foi preenchido.')
                    return redirect_to_frontend('/admin-panel')
                
                # Verificar confirmação (case-insensitive e sem espaços/caracteres especiais)
                import re
                confirm_clean = re.sub(r'[^\w]', '', confirm.lower())
                print(f"DEBUG: Valor limpo: '{confirm_clean}' | Tamanho: {len(confirm_clean)}")
                
                if confirm_clean != 'excluir':
                    messages.error(request, f'Confirmação inválida. Recebido: "{confirm_clean}" | Esperado: "excluir"')
                    return redirect_to_frontend('/admin-panel')
                
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
    
    return redirect_to_frontend('/admin-panel')


@login_required(login_url='/dashboard/login/')
def refresh_dashboard_cache(request):
    """
    View para forçar atualização do cache do dashboard
    Útil para atualizar dados em tempo real
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    try:
        # Limpar cache
        success = clear_dashboard_cache()
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Cache do dashboard atualizado com sucesso',
                'timestamp': timezone.now().isoformat()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao atualizar cache do dashboard'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=500)


@login_required(login_url='/dashboard/login/')
def debug_subscriptions(request):
    """
    View para debug das assinaturas - mostra todas as assinaturas no banco
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    try:
        # Buscar todas as assinaturas
        all_subscriptions = Assinatura.objects.select_related('usuario', 'plano').all()
        
        subscriptions_data = []
        for assinatura in all_subscriptions:
            subscriptions_data.append({
                'id': assinatura.id,
                'usuario_id': assinatura.usuario_id,
                'usuario_username': assinatura.usuario.username,
                'plano_nome': assinatura.plano.nome,
                'status': assinatura.status,
                'ativo': assinatura.ativo,
                'data_criacao': assinatura.data_criacao.strftime('%d/%m/%Y %H:%M:%S'),
                'data_inicio': assinatura.data_inicio.strftime('%d/%m/%Y %H:%M:%S'),
                'data_vencimento': assinatura.data_vencimento.strftime('%d/%m/%Y %H:%M:%S'),
            })
        
        # Debug específico para usuários premium
        print("🔍 DEBUG COMPLETO DAS ASSINATURAS:")
        print(f"Total de assinaturas no banco: {all_subscriptions.count()}")
        
        # Contar por status
        status_counts = {}
        for assinatura in all_subscriptions:
            status = assinatura.status
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        print("Contagem por status:", status_counts)
        
        # Contar por ativo
        ativo_counts = {}
        for assinatura in all_subscriptions:
            ativo = assinatura.ativo
            if ativo not in ativo_counts:
                ativo_counts[ativo] = 0
            ativo_counts[ativo] += 1
        
        print("Contagem por ativo:", ativo_counts)
        
        # Usuários únicos premium
        usuarios_premium = set()
        for assinatura in all_subscriptions:
            if assinatura.status == 'ativa' and assinatura.ativo and assinatura.usuario:
                usuarios_premium.add(assinatura.usuario.id)
        
        print(f"Usuários premium únicos (status='ativa' e ativo=True): {len(usuarios_premium)}")
        print(f"IDs dos usuários premium: {list(usuarios_premium)}")
        
        # Debug: mostrar assinaturas canceladas para ver se há o 5º usuário
        assinaturas_canceladas = Assinatura.objects.filter(
            status='cancelada'
        ).select_related('usuario').values('usuario__id', 'usuario__username', 'status', 'ativo', 'data_criacao', 'data_vencimento')
        
        print("🔍 DEBUG: Assinaturas canceladas:")
        for assinatura in assinaturas_canceladas:
            print(f"  - ID: {assinatura['usuario__id']}, Username: {assinatura['usuario__username']}, Status: {assinatura['status']}, Ativo: {assinatura['ativo']}, Criada: {assinatura['data_criacao']}, Vencimento: {assinatura['data_vencimento']}")
        
        # Verificar se há usuários que tiveram assinatura ativa mas agora estão cancelados
        usuarios_cancelados_ids = [a['usuario__id'] for a in assinaturas_canceladas]
        print(f"IDs dos usuários com assinaturas canceladas: {usuarios_cancelados_ids}")
        
        # Verificar se algum desses usuários cancelados já foi premium
        usuarios_que_ja_foram_premium = set(usuarios_premium) & set(usuarios_cancelados_ids)
        if usuarios_que_ja_foram_premium:
            print(f"Usuários que já foram premium mas agora estão cancelados: {usuarios_que_ja_foram_premium}")
        else:
            print("Nenhum usuário cancelado já foi premium anteriormente")
        
        # Debug: verificar webhooks falhados
        from payments.models import WebhookEvent
        webhooks_falhados = WebhookEvent.objects.filter(
            processado=False,
            data_criacao__gte=timezone.now() - timedelta(days=7)
        ).order_by('-data_criacao')
        
        print(f"\n🔍 DEBUG: Webhooks falhados nos últimos 7 dias: {webhooks_falhados.count()}")
        for webhook in webhooks_falhados[:5]:  # Mostrar apenas os 5 mais recentes
            print(f"  - ID: {webhook.id}, Tipo: {webhook.tipo}, Status: {webhook.status}, Data: {webhook.data_criacao}")
            if webhook.erro_processamento:
                print(f"    Erro: {webhook.erro_processamento}")
        
        # Debug: verificar pagamentos pendentes
        pagamentos_pendentes = Pagamento.objects.filter(
            status__in=['pending', 'in_process'],
            data_criacao__gte=timezone.now() - timedelta(days=7)
        ).order_by('-data_criacao')
        
        print(f"\n🔍 DEBUG: Pagamentos pendentes nos últimos 7 dias: {pagamentos_pendentes.count()}")
        for pagamento in pagamentos_pendentes[:5]:  # Mostrar apenas os 5 mais recentes
            print(f"  - ID: {pagamento.id}, Usuário: {pagamento.usuario.email}, Status: {pagamento.status}, Data: {pagamento.data_criacao}")
            print(f"    External Ref: {pagamento.external_reference}, Payment ID: {pagamento.get_payment_id()}")
        
        return JsonResponse({
            'success': True,
            'total_subscriptions': all_subscriptions.count(),
            'status_counts': status_counts,
            'ativo_counts': ativo_counts,
            'usuarios_premium_unicos': len(usuarios_premium),
            'usuarios_premium_ids': list(usuarios_premium),
            'subscriptions': subscriptions_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao buscar assinaturas: {str(e)}'})

def debug_usuario_especifico(request):
    """
    Debug específico para um usuário - verificar pagamentos e assinaturas
    """
    print("🔍 DEBUG: Função debug_usuario_especifico chamada")
    
    if not request.user.is_superuser:
        print("❌ DEBUG: Usuário não é superuser")
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    try:
        print("🔍 DEBUG: Iniciando debug do usuário específico")
        
        # Buscar usuário por email
        email = request.GET.get('email', 'gregoriobaldocs@gmail.com')
        print(f"🔍 DEBUG: Buscando usuário com email: {email}")
        
        try:
            usuario = User.objects.get(email=email)
            print(f"🔍 DEBUG: Usuário encontrado: {usuario.username} (ID: {usuario.id})")
        except User.DoesNotExist:
            print(f"❌ DEBUG: Usuário com email {email} não encontrado")
            return JsonResponse({'error': f'Usuário com email {email} não encontrado'})
        except Exception as e:
            print(f"❌ DEBUG: Erro ao buscar usuário: {e}")
            return JsonResponse({'error': f'Erro ao buscar usuário: {str(e)}'})
        
        # Buscar pagamentos do usuário
        print("🔍 DEBUG: Buscando pagamentos do usuário")
        pagamentos = Pagamento.objects.filter(usuario=usuario).order_by('-data_criacao')
        print(f"🔍 DEBUG: Encontrados {pagamentos.count()} pagamentos")
        
        # Buscar assinaturas do usuário
        print("🔍 DEBUG: Buscando assinaturas do usuário")
        assinaturas = Assinatura.objects.filter(usuario=usuario).order_by('-data_criacao')
        print(f"🔍 DEBUG: Encontradas {assinaturas.count()} assinaturas")
        
        # Verificar perfil do usuário
        try:
            profile = usuario.profile
            conta_premium = profile.conta_premium
            data_vencimento_premium = profile.data_vencimento_premium
        except:
            conta_premium = False
            data_vencimento_premium = None
        
        # Debug detalhado
        print(f"🔍 DEBUG USUÁRIO: {usuario.username} ({usuario.email})")
        print(f"ID do usuário: {usuario.id}")
        print(f"Conta premium no perfil: {conta_premium}")
        print(f"Data vencimento premium: {data_vencimento_premium}")
        
        print(f"\n📊 PAGAMENTOS ({pagamentos.count()}):")
        for pagamento in pagamentos:
            print(f"  - ID: {pagamento.id}, Status: {pagamento.status}, Valor: {pagamento.valor}, Data: {pagamento.data_criacao}")
            print(f"    External Reference: {pagamento.external_reference}")
            print(f"    Payment ID: {pagamento.get_payment_id()}")
        
        print(f"\n📊 ASSINATURAS ({assinaturas.count()}):")
        for assinatura in assinaturas:
            print(f"  - ID: {assinatura.id}, Status: {assinatura.status}, Ativo: {assinatura.ativo}")
            print(f"    Plano: {assinatura.plano.nome if assinatura.plano else 'N/A'}")
            print(f"    Data Início: {assinatura.data_inicio}")
            print(f"    Data Vencimento: {assinatura.data_vencimento}")
            print(f"    External Reference: {assinatura.external_reference}")
        
        # Verificar se há pagamentos aprovados sem assinatura
        pagamentos_aprovados = pagamentos.filter(status='approved')
        assinaturas_ativas = assinaturas.filter(status='ativa', ativo=True)
        
        print(f"\n🔍 ANÁLISE:")
        print(f"Pagamentos aprovados: {pagamentos_aprovados.count()}")
        print(f"Assinaturas ativas: {assinaturas_ativas.count()}")
        
        if pagamentos_aprovados.exists() and not assinaturas_ativas.exists():
            print("❌ PROBLEMA: Usuário tem pagamento aprovado mas não tem assinatura ativa!")
            
            # Tentar ativar assinatura manualmente
            pagamento_aprovado = pagamentos_aprovados.first()
            print(f"Tentando ativar assinatura para pagamento {pagamento_aprovado.id}...")
            
            # Simular dados de pagamento para ativar assinatura
            payment_data = {
                'id': pagamento_aprovado.get_payment_id() or str(pagamento_aprovado.id),
                'status': 'approved'
            }
            
            try:
                # Importar a função ativar_assinatura
                from payments.views import ativar_assinatura
                ativar_assinatura(pagamento_aprovado, payment_data)
                print("✅ Assinatura ativada com sucesso!")
                
                # Atualizar dados após ativação
                assinaturas = Assinatura.objects.filter(usuario=usuario).order_by('-data_criacao')
                assinaturas_ativas = assinaturas.filter(status='ativa', ativo=True)
                print(f"Assinaturas ativas após correção: {assinaturas_ativas.count()}")
                
            except Exception as e:
                print(f"❌ Erro ao ativar assinatura: {e}")
                import traceback
                traceback.print_exc()
        
        print("🔍 DEBUG: Preparando resposta JSON")
        
        # Preparar dados do usuário
        usuario_data = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'conta_premium': conta_premium,
            'data_vencimento_premium': data_vencimento_premium.isoformat() if data_vencimento_premium else None
        }
        
        # Preparar dados dos pagamentos
        pagamentos_data = []
        for p in pagamentos:
            try:
                pagamentos_data.append({
                    'id': p.id,
                    'status': p.status,
                    'valor': float(p.valor),
                    'data_criacao': p.data_criacao.isoformat(),
                    'external_reference': p.external_reference,
                    'payment_id': p.get_payment_id()
                })
            except Exception as e:
                print(f"❌ DEBUG: Erro ao processar pagamento {p.id}: {e}")
        
        # Preparar dados das assinaturas
        assinaturas_data = []
        for a in assinaturas:
            try:
                assinaturas_data.append({
                    'id': a.id,
                    'status': a.status,
                    'ativo': a.ativo,
                    'plano': a.plano.nome if a.plano else None,
                    'data_inicio': a.data_inicio.isoformat(),
                    'data_vencimento': a.data_vencimento.isoformat(),
                    'external_reference': a.external_reference
                })
            except Exception as e:
                print(f"❌ DEBUG: Erro ao processar assinatura {a.id}: {e}")
        
        print("🔍 DEBUG: Enviando resposta JSON")
        
        # Versão simplificada para teste
        return JsonResponse({
            'success': True,
            'message': 'Debug executado com sucesso',
            'usuario': usuario_data,
            'total_pagamentos': len(pagamentos_data),
            'total_assinaturas': len(assinaturas_data)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao buscar dados do usuário: {str(e)}'})

def ativar_assinatura_manual(request):
    """
    Ativar assinatura manualmente para um usuário específico
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    try:
        email = request.GET.get('email', 'gregoriobaldocs@gmail.com')
        print(f"🔍 DEBUG: Ativando assinatura manual para: {email}")
        
        # Buscar usuário
        try:
            usuario = User.objects.get(email=email)
            print(f"🔍 DEBUG: Usuário encontrado: {usuario.username} (ID: {usuario.id})")
        except User.DoesNotExist:
            return JsonResponse({'error': f'Usuário com email {email} não encontrado'})
        
        # Buscar plano Pro (assumindo que é o mais caro)
        plano_pro = PlanoPremium.objects.filter(ativo=True).order_by('-preco').first()
        if not plano_pro:
            return JsonResponse({'error': 'Nenhum plano ativo encontrado'})
        
        print(f"🔍 DEBUG: Plano encontrado: {plano_pro.nome} (R$ {plano_pro.preco})")
        
        # Calcular datas
        data_inicio = timezone.now()
        data_vencimento = data_inicio + timedelta(days=plano_pro.duracao_dias)
        
        # Criar assinatura manual
        assinatura = Assinatura.objects.create(
            usuario=usuario,
            plano=plano_pro,
            status='ativa',
            ativo=True,
            data_inicio=data_inicio,
            data_vencimento=data_vencimento,
            external_reference=f'manual_{usuario.id}_{int(timezone.now().timestamp())}',
            subscription_id=f'manual_{usuario.id}_{int(timezone.now().timestamp())}'
        )
        
        print(f"✅ DEBUG: Assinatura criada com ID: {assinatura.id}")
        
        # Atualizar perfil do usuário
        try:
            profile = usuario.profile
            profile.conta_premium = True
            profile.data_vencimento_premium = data_vencimento
            profile.save()
            print(f"✅ DEBUG: Perfil do usuário atualizado")
        except Exception as e:
            print(f"⚠️ DEBUG: Erro ao atualizar perfil: {e}")
        
        # Limpar cache do dashboard
        try:
            clear_dashboard_cache()
            print(f"✅ DEBUG: Cache do dashboard limpo")
        except Exception as e:
            print(f"⚠️ DEBUG: Erro ao limpar cache: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Assinatura ativada com sucesso para {usuario.email}',
            'assinatura_id': assinatura.id,
            'plano': plano_pro.nome,
            'data_vencimento': data_vencimento.isoformat()
        })
        
    except Exception as e:
        print(f"❌ DEBUG: Erro ao ativar assinatura manual: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': f'Erro ao ativar assinatura: {str(e)}'})

def corrigir_assinaturas_inativas(request):
    """
    Corrigir assinaturas que foram criadas sem ativo=True
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    try:
        print("🔍 CORRIGIR ASSINATURAS: Iniciando correção de assinaturas inativas")
        
        # Buscar assinaturas com status='ativa' mas ativo=False ou None
        assinaturas_problema = Assinatura.objects.filter(
            status='ativa'
        ).filter(
            Q(ativo=False) | Q(ativo__isnull=True)
        )
        
        print(f"🔍 CORRIGIR ASSINATURAS: Encontradas {assinaturas_problema.count()} assinaturas com problema")
        
        corrigidas = 0
        for assinatura in assinaturas_problema:
            print(f"🔍 CORRIGIR ASSINATURAS: Corrigindo assinatura {assinatura.id} - Usuário: {assinatura.usuario.email}")
            
            # Corrigir assinatura
            assinatura.ativo = True
            assinatura.save()
            
            # Atualizar perfil do usuário
            try:
                profile = assinatura.usuario.profile
                profile.conta_premium = True
                profile.data_vencimento_premium = assinatura.data_vencimento
                profile.save()
                print(f"✅ CORRIGIR ASSINATURAS: Perfil atualizado para {assinatura.usuario.email}")
            except Exception as e:
                print(f"❌ CORRIGIR ASSINATURAS: Erro ao atualizar perfil de {assinatura.usuario.email}: {e}")
            
            corrigidas += 1
        
        # Limpar cache
        try:
            clear_dashboard_cache()
            print(f"✅ CORRIGIR ASSINATURAS: Cache limpo")
        except Exception as e:
            print(f"⚠️ CORRIGIR ASSINATURAS: Erro ao limpar cache: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Correção concluída! {corrigidas} assinaturas foram corrigidas.',
            'assinaturas_corrigidas': corrigidas
        })
        
    except Exception as e:
        print(f"❌ CORRIGIR ASSINATURAS: Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': f'Erro ao corrigir assinaturas: {str(e)}'})


@login_required
def dados_usuario(request, user_id):
    """
    View para buscar dados completos de um usuário específico
    """
    try:
        # Buscar usuário
        user = User.objects.get(id=user_id)
        
        # Buscar perfil
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None
        
        # Buscar assinaturas
        assinaturas = Assinatura.objects.filter(usuario=user)
        total_assinaturas = assinaturas.count()
        
        # Buscar pagamentos
        pagamentos = Pagamento.objects.filter(usuario=user)
        total_pagamentos = pagamentos.count()
        valor_total_pago = pagamentos.aggregate(total=Sum('valor'))['total'] or 0
        
        # Preparar dados do usuário
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'has_active_subscription': hasattr(user, 'has_active_subscription') and user.has_active_subscription
        }
        
        # Preparar dados do perfil
        profile_data = {}
        if profile:
            profile_data = {
                'nome': profile.nome,
                'idade': profile.idade,
                'faixa': profile.faixa,
                'faixa_display': profile.get_faixa_display(),
                'pontos_experiencia': profile.pontos_experiencia,
                'nivel': profile.nivel,
                'conta_premium': profile.conta_premium,
                'data_vencimento_premium': profile.data_vencimento_premium.isoformat() if profile.data_vencimento_premium else None,
                'notificacoes_ativadas': profile.notificacoes_ativadas,
                'tema_preferido': profile.tema_preferido
            }
        
        return JsonResponse({
            'success': True,
            'usuario': user_data,
            'perfil': profile_data,
            'total_assinaturas': total_assinaturas,
            'total_pagamentos': total_pagamentos,
            'valor_total_pago': f"{valor_total_pago:.2f}"
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao obter dados do usuário: {str(e)}'
        }, status=500)


@login_required(login_url='/dashboard/login/')
def email_marketing(request):
    """
    Envio de email (remarketing) para usuários selecionados ou para todos.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect_to_frontend('/admin-panel')
    
    # Apenas usuários no plano grátis (sem assinatura ativa)
    users = User.objects.filter(is_active=True)\
        .exclude(assinaturas__status='ativa', assinaturas__ativo=True)\
        .distinct()\
        .order_by('-date_joined')
    
    # Mensagem padrão (formal e direta) e assunto padrão
    default_subject = 'Convite para ativar seu acesso Premium no Dojo Online'
    default_body = (
        'Olá!\n\n'
        'Aqui é do Dojo Online. Vimos que você está aproveitando seu acesso gratuito e gostaríamos de '
        'te convidar para ativar o plano Premium e liberar todos os conteúdos.\n\n'
        'Ao assinar, você terá acesso a:\n'
        '- Aulas e técnicas organizadas por faixa\n'
        '- Vídeos, dicas práticas e imobilizações\n'
        '- Quiz interativo e acompanhamento do seu progresso\n'
        '- Atualizações frequentes e suporte\n\n'
        'Para entrar e concluir sua assinatura agora, acesse:\n'
        'Login: https://www.dojoon.com.br/login/\n'
        'Planos: https://www.dojoon.com.br/payments/planos/\n\n'
        'Qualquer dúvida, é só responder este email.\n\n'
        'Bons treinos!\n'
        'Equipe Dojo Online'
    )
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        send_to = request.POST.get('send_to', 'selected')
        selected_ids = request.POST.getlist('user_ids')
        
        if not subject or not body:
            messages.error(request, 'Informe assunto e mensagem.')
            return render(request, 'dashboard/email_marketing.html', {
                'users': users,
                'default_subject': default_subject,
                'default_body': default_body,
            })
        
        if send_to == 'all':
            recipients_qs = users
        else:
            recipients_qs = users.filter(id__in=selected_ids)
        
        emails = list(recipients_qs.exclude(email__isnull=True).exclude(email='').values_list('email', flat=True))
        emails = [e.strip().lower() for e in emails if '@' in e]
        emails = sorted(list(set(emails)))
        
        if not emails:
            messages.error(request, 'Nenhum destinatário válido.')
            return render(request, 'dashboard/email_marketing.html', {
                'users': users,
                'default_subject': default_subject,
                'default_body': default_body,
            })
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
        if not from_email:
            messages.error(request, 'DEFAULT_FROM_EMAIL não configurado.')
            return render(request, 'dashboard/email_marketing.html', {
                'users': users,
                'default_subject': default_subject,
                'default_body': default_body,
            })
        
        sent = 0
        batch_size = 100
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i+batch_size]
            msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[from_email],
                bcc=batch
            )
            msg.send(fail_silently=False)
            sent += len(batch)
        
        messages.success(request, f'Email enviado para {sent} destinatário(s).')
        return redirect('email_marketing')
    
    return render(request, 'dashboard/email_marketing.html', {
        'users': users,
        'default_subject': default_subject,
        'default_body': default_body,
    })