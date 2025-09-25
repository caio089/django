from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests
import mercadopago
from .models import PlanoPremium, Assinatura, Pagamento, WebhookEvent, ConfiguracaoPagamento, Reembolso
from .security import WebhookSecurity, RateLimiter, AuditLogger, DataValidator
from home.models import Profile
from quiz.models import ProgressoUsuario
import uuid
from datetime import datetime, timedelta
import logging

# Configurar logging para debug
logger = logging.getLogger(__name__)

# Instâncias de segurança
rate_limiter = RateLimiter()
audit_logger = AuditLogger()
data_validator = DataValidator()

# =====================================================
# CONFIGURAÇÃO DO MERCADO PAGO
# =====================================================

def get_mercadopago_config():
    """
    Obtém as configurações ativas do Mercado Pago
    Retorna: (sdk, config) ou (None, None) se erro
    """
    try:
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if config:
            access_token = config.get_access_token()
            if access_token:
                sdk = mercadopago.SDK(access_token)
                # Marcar uso da configuração
                config.mark_usage()
                return sdk, config
        logger.error("Nenhuma configuração ativa do Mercado Pago encontrada")
        return None, None
    except Exception as e:
        logger.error(f"Erro ao configurar Mercado Pago: {e}")
        return None, None

def criar_perfil_usuario(user):
    """
    Cria perfil do usuário se não existir
    """
    try:
        if not hasattr(user, 'profile'):
            Profile.objects.create(
                user=user,
                nome=user.get_full_name() or user.username,
                idade=18,  # Idade padrão
                faixa='branca'
            )
        
        # Criar progresso do usuário se não existir
        if not hasattr(user, 'progresso'):
            ProgressoUsuario.objects.create(usuario=user)
            
        return True
    except Exception as e:
        logger.error(f"Erro ao criar perfil do usuário {user.id}: {e}")
        return False

# =====================================================
# VIEWS DE PLANOS E PAGAMENTO
# =====================================================

@login_required
def listar_planos(request):
    """
    Lista todos os planos premium disponíveis
    """
    planos = PlanoPremium.objects.filter(ativo=True).order_by('preco')
    
    # Verificar se usuário já tem assinatura ativa
    assinatura_ativa = Assinatura.objects.filter(
        usuario=request.user,
        status='ativa',
        data_vencimento__gt=datetime.now()
    ).first()
    
    return render(request, 'payments/planos.html', {
        'planos': planos,
        'assinatura_ativa': assinatura_ativa
    })

@login_required
def escolher_plano(request, plano_id):
    """
    Página para escolher plano e preencher dados do usuário
    """
    plano = get_object_or_404(PlanoPremium, id=plano_id, ativo=True)
    
    # Verificar se já tem assinatura ativa
    assinatura_ativa = Assinatura.objects.filter(
        usuario=request.user,
        status='ativa',
        data_vencimento__gt=datetime.now()
    ).exists()
    
    if assinatura_ativa:
        messages.warning(request, 'Você já possui uma assinatura ativa!')
        return redirect('payments:planos')
    
    # Criar perfil se não existir
    criar_perfil_usuario(request.user)
    
    return render(request, 'payments/escolher_plano.html', {
        'plano': plano
    })

@login_required
def criar_pagamento(request, plano_id):
    """
    Cria um pagamento no Mercado Pago e retorna dados para checkout transparente
    """
    # Se for GET, redirecionar para escolher plano
    if request.method == 'GET':
        return redirect('payments:escolher_plano', plano_id=plano_id)
    
    try:
        # Obter dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')
        
        # Sanitizar dados de entrada
        nome = data_validator.sanitize_input(nome)
        email = data_validator.sanitize_input(email)
        telefone = data_validator.sanitize_input(telefone)
        cpf = data_validator.sanitize_input(cpf)
        
        # Validar dados obrigatórios
        if not all([nome, email]):
            return JsonResponse({
                'success': False,
                'error': 'Dados obrigatórios não fornecidos'
            })
        
        # Validar formato dos dados
        if not data_validator.validate_email(email):
            return JsonResponse({
                'success': False,
                'error': 'Email inválido'
            })
        
        if cpf and not data_validator.validate_cpf(cpf):
            return JsonResponse({
                'success': False,
                'error': 'CPF inválido'
            })
        
        if telefone and not data_validator.validate_phone(telefone):
            return JsonResponse({
                'success': False,
                'error': 'Telefone inválido'
            })
        
        # Buscar plano
        plano = get_object_or_404(PlanoPremium, id=plano_id, ativo=True)
        
        # Registrar tentativa de pagamento
        audit_logger.log_payment_attempt(
            user_id=request.user.id,
            payment_id='creating',
            status='initiated',
            details={'plano': plano.nome, 'valor': float(plano.preco)}
        )
        
        # Atualizar perfil do usuário
        try:
            profile = request.user.profile
            profile.nome = nome
            profile.save()
        except:
            # Criar perfil se não existir
            Profile.objects.create(
                user=request.user,
                nome=nome,
                idade=18,
                faixa='branca'
            )
        
        # Configurar Mercado Pago
        sdk, config = get_mercadopago_config()
        if not sdk:
            return JsonResponse({
                'success': False,
                'error': 'Erro na configuração do pagamento'
            })
        
        # Criar preferência de pagamento
        external_reference = str(uuid.uuid4())
        
        preference_data = {
            "items": [
                {
                    "title": plano.nome,
                    "description": plano.descricao,
                    "quantity": 1,
                    "unit_price": float(plano.preco),
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "email": email,
                "identification": {
                    "type": "CPF",
                    "number": cpf.replace('.', '').replace('-', '') if cpf else None
                },
                "phone": {
                    "area_code": telefone[:2] if telefone and len(telefone) > 2 else "11",
                    "number": telefone[2:] if telefone and len(telefone) > 2 else telefone
                }
            },
            "back_urls": {
                "success": f"{request.scheme}://{request.get_host()}/payments/success/",
                "failure": f"{request.scheme}://{request.get_host()}/payments/failure/",
                "pending": f"{request.scheme}://{request.get_host()}/payments/pending/"
            },
            "auto_return": "approved",
            "external_reference": external_reference,
            "notification_url": config.webhook_url,
            "payment_methods": {
                "excluded_payment_methods": [],
                "excluded_payment_types": [],
                "installments": 12
            }
        }
        
        # Para desenvolvimento, simular criação de preferência
        logger.info(f"Criando preferência com dados: {preference_data}")
        
        # Simular resposta do Mercado Pago para desenvolvimento
        preference_id = f"pref_{external_reference}"
        
        # Salvar pagamento no banco com dados criptografados
        pagamento = Pagamento.objects.create(
            usuario=request.user,
            valor=plano.preco,
            tipo='assinatura',
            external_reference=external_reference,
            descricao=f"Assinatura {plano.nome}",
            ip_address=WebhookSecurity.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Criptografar dados sensíveis
        pagamento.set_payment_id(preference_id)
        pagamento.set_payer_email(email)
        pagamento.set_payer_name(nome)
        if telefone:
            pagamento.set_payer_phone(telefone)
        if cpf:
            pagamento.set_payer_document(cpf)
        pagamento.save()
        
        # Retornar dados para o frontend
        return JsonResponse({
            'success': True,
            'preference_id': preference_id,
            'public_key': config.get_public_key(),
            'payment_id': pagamento.id,
            'external_reference': external_reference
        })
            
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        })

@login_required
def checkout_pagamento(request, payment_id):
    """
    Página de checkout com Mercado Pago SDK
    """
    pagamento = get_object_or_404(Pagamento, id=payment_id, usuario=request.user)
    
    # Obter configuração do Mercado Pago
    sdk, config = get_mercadopago_config()
    if not config:
        messages.error(request, 'Erro na configuração do pagamento.')
        return redirect('payments:planos')
    
    return render(request, 'payments/checkout.html', {
        'pagamento': pagamento,
        'public_key': config.get_public_key(),
        'preference_id': pagamento.get_payment_id()
    })

# =====================================================
# WEBHOOK E PROCESSAMENTO DE PAGAMENTOS
# =====================================================

@csrf_exempt
@require_http_methods(["POST"])
def webhook_mercadopago(request):
    """
    Webhook seguro para receber notificações do Mercado Pago
    Processa eventos de payment.created e payment.updated
    """
    client_ip = WebhookSecurity.get_client_ip(request)
    
    try:
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip, limit=50, window=300):  # 50 req/5min
            audit_logger.log_security_event(
                'rate_limit_exceeded',
                'medium',
                {'ip': client_ip, 'endpoint': 'webhook'}
            )
            return HttpResponse(status=429)
        
        # Verificar origem do webhook
        if not WebhookSecurity.verify_webhook_origin(request):
            audit_logger.log_security_event(
                'invalid_webhook_origin',
                'high',
                {'ip': client_ip, 'user_agent': request.META.get('HTTP_USER_AGENT', '')}
            )
            return HttpResponse(status=403)
        
        # Obter dados do webhook
        data = json.loads(request.body)
        
        # Verificar assinatura do webhook (se configurada)
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if config:
            webhook_secret = config.get_webhook_secret()
            if webhook_secret:
                signature = request.META.get('HTTP_X_SIGNATURE', '')
                if not WebhookSecurity.verify_mercadopago_signature(
                    request.body, signature, webhook_secret
                ):
                    audit_logger.log_security_event(
                        'invalid_webhook_signature',
                        'high',
                        {'ip': client_ip, 'signature': signature}
                    )
                    return HttpResponse(status=403)
        
        logger.info(f"Webhook recebido de {client_ip}: {data.get('type', 'unknown')}")
        
        # Registrar evento no banco com dados criptografados
        webhook_event = WebhookEvent.objects.create(
            tipo=data.get('type', 'payment'),
            action=data.get('action', 'unknown'),
            ip_address=client_ip,
            signature=request.META.get('HTTP_X_SIGNATURE', '')
        )
        
        # Criptografar dados sensíveis
        webhook_event.set_id_mercadopago(data.get('id', ''))
        webhook_event.set_external_reference(data.get('external_reference', ''))
        webhook_event.set_data_recebida(data)
        webhook_event.save()
        
        # Registrar evento para auditoria
        audit_logger.log_webhook_event(
            request, 
            data.get('type', 'unknown'),
            'received',
            {'data_id': data.get('id', '')}
        )
        
        # Processar evento de pagamento
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            if payment_id:
                processar_pagamento_webhook(payment_id, webhook_event)
        
        # Marcar como processado
        webhook_event.processado = True
        webhook_event.data_processamento = datetime.now()
        webhook_event.save()
        
        return HttpResponse(status=200)
        
    except json.JSONDecodeError:
        audit_logger.log_security_event(
            'invalid_json_webhook',
            'medium',
            {'ip': client_ip}
        )
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        audit_logger.log_webhook_event(
            request, 
            'error',
            'failed',
            {'error': str(e)}
        )
        if 'webhook_event' in locals():
            webhook_event.erro_processamento = str(e)
            webhook_event.save()
        return HttpResponse(status=500)

def processar_pagamento_webhook(payment_id, webhook_event):
    """
    Processa um pagamento recebido via webhook
    Atualiza status e cria ativa assinatura se aprovado
    """
    try:
        # Buscar pagamento no banco usando dados criptografados
        pagamentos = Pagamento.objects.all()
        pagamento = None
        
        for p in pagamentos:
            if p.get_payment_id() == payment_id:
                pagamento = p
                break
        
        if not pagamento:
            logger.error(f"Pagamento {payment_id} não encontrado no banco")
            return
        
        # Verificar status no Mercado Pago
        sdk, config = get_mercadopago_config()
        if not sdk:
            logger.error("Erro ao obter configuração do Mercado Pago")
            return
        
        payment_info = sdk.payment().get(payment_id)
        if payment_info["status"] != 200:
            logger.error(f"Erro ao buscar pagamento no MP: {payment_info}")
            return
        
        payment_data = payment_info["response"]
        
        # Atualizar status do pagamento
        status_anterior = pagamento.status
        pagamento.status = payment_data["status"]
        pagamento.metodo_pagamento = payment_data.get("payment_method_id")
        pagamento.data_pagamento = datetime.now()
        pagamento.save()
        
        # Registrar auditoria
        audit_logger.log_payment_attempt(
            user_id=pagamento.usuario.id,
            payment_id=payment_id,
            status=payment_data["status"],
            details={'status_anterior': status_anterior}
        )
        
        logger.info(f"Pagamento {payment_id} atualizado: {status_anterior} -> {payment_data['status']}")
        
        # Se aprovado e ainda não tem assinatura
        if payment_data["status"] == "approved":
            if not Assinatura.objects.filter(external_reference=pagamento.external_reference).exists():
                ativar_assinatura(pagamento, payment_data)
        
        # Se rejeitado ou cancelado
        elif payment_data["status"] in ["rejected", "cancelled"]:
            logger.info(f"Pagamento {payment_id} foi {payment_data['status']}")
            
    except Exception as e:
        logger.error(f"Erro ao processar pagamento webhook {payment_id}: {e}")
        webhook_event.erro_processamento = str(e)
        webhook_event.save()

def ativar_assinatura(pagamento, payment_data):
    """
    Ativa a assinatura do usuário após pagamento aprovado
    """
    try:
        # Buscar plano pelo valor (simplificado)
        plano = PlanoPremium.objects.filter(preco=pagamento.valor, ativo=True).first()
        if not plano:
            logger.error(f"Plano não encontrado para valor {pagamento.valor}")
            return
        
        # Calcular datas
        data_inicio = datetime.now()
        data_vencimento = data_inicio + timedelta(days=plano.duracao_dias)
        
        # Criar assinatura
        assinatura = Assinatura.objects.create(
            usuario=pagamento.usuario,
            plano=plano,
            status='ativa',
            data_inicio=data_inicio,
            data_vencimento=data_vencimento,
            external_reference=pagamento.external_reference,
            subscription_id=payment_data.get("id")
        )
        
        # Vincular pagamento à assinatura
        pagamento.assinatura = assinatura
        pagamento.save()
        
        # Atualizar perfil do usuário - LIBERAR TODO O CONTEÚDO DO SITE
        try:
            profile = pagamento.usuario.profile
            profile.conta_premium = True
            profile.data_vencimento_premium = data_vencimento
            profile.save()
            
            # LIBERAR ACESSO A TODAS AS FUNCIONALIDADES PREMIUM
            logger.info(f"✅ CONTEÚDO LIBERADO para usuário {pagamento.usuario.username}")
            logger.info(f"✅ Assinatura ativa até: {data_vencimento}")
            logger.info(f"✅ Usuário agora tem acesso a:")
            logger.info(f"   - Página 1 (Faixa Cinza)")
            logger.info(f"   - Página 2 (Faixa Azul)")  
            logger.info(f"   - Quiz Premium")
            logger.info(f"   - Sessões de Rolamentos")
            logger.info(f"   - Todas as funcionalidades premium")
            
            # Enviar notificação de sucesso (opcional)
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = "🎉 Pagamento Aprovado - Acesso Liberado!"
                message = f"""
                Olá {pagamento.usuario.username}!
                
                Seu pagamento foi aprovado com sucesso! 🎉
                
                ✅ Seu acesso premium está ativo até: {data_vencimento.strftime('%d/%m/%Y')}
                
                Agora você tem acesso completo a:
                • Todas as técnicas de judô
                • Quiz premium
                • Sessões de rolamentos
                • Conteúdo exclusivo
                
                Aproveite seu treinamento!
                Equipe Judô Premium
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [pagamento.usuario.email],
                    fail_silently=True
                )
                logger.info(f"Email de confirmação enviado para {pagamento.usuario.email}")
            except Exception as email_error:
                logger.warning(f"Erro ao enviar email: {email_error}")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil do usuário: {e}")
            logger.error(f"Erro ao atualizar perfil do usuário {pagamento.usuario.id}")
        
        logger.info(f"Assinatura ativada para usuário {pagamento.usuario.id}: {plano.nome}")
        
    except Exception as e:
        logger.error(f"Erro ao ativar assinatura: {e}")

# =====================================================
# VIEWS DE RESULTADO E STATUS
# =====================================================

@login_required
def pagamento_sucesso(request):
    """
    Página de sucesso do pagamento
    """
    payment_id = request.GET.get('payment_id')
    
    if payment_id:
        try:
            # Buscar pagamento
            pagamento = Pagamento.objects.get(payment_id=payment_id, usuario=request.user)
            
            # Buscar assinatura se existir
            assinatura = Assinatura.objects.filter(external_reference=pagamento.external_reference).first()
            
            if pagamento.status == 'approved' and assinatura:
                messages.success(request, f'Pagamento aprovado! Sua assinatura {assinatura.plano.nome} está ativa até {assinatura.data_vencimento.strftime("%d/%m/%Y")}.')
                
                # Passar informações detalhadas do plano para o template
                return render(request, 'payments/sucesso.html', {
                    'assinatura': assinatura,
                    'plano': assinatura.plano,
                    'dias_restantes': (assinatura.data_vencimento - timezone.now()).days
                })
            elif pagamento.status == 'pending':
                messages.info(request, 'Seu pagamento está sendo processado. Você receberá uma confirmação em breve.')
            else:
                messages.warning(request, f'Status do pagamento: {pagamento.get_status_display()}')
                
        except Pagamento.DoesNotExist:
            messages.error(request, 'Pagamento não encontrado.')
        except Exception as e:
            logger.error(f"Erro na página de sucesso: {e}")
            messages.error(request, 'Erro ao processar informações do pagamento.')
    
    return render(request, 'payments/sucesso.html')

@login_required
def pagamento_falha(request):
    """
    Página de falha do pagamento
    """
    messages.error(request, 'Pagamento não foi aprovado. Tente novamente.')
    return render(request, 'payments/falha.html')

@login_required
def pagamento_pendente(request):
    """
    Página de pagamento pendente
    """
    messages.info(request, 'Pagamento está sendo processado. Aguarde a confirmação.')
    return render(request, 'payments/pendente.html')

@login_required
def verificar_status_pagamento(request, payment_id):
    """
    API para verificar status do pagamento via AJAX
    """
    try:
        pagamento = Pagamento.objects.get(id=payment_id, usuario=request.user)
        
        # Buscar assinatura se existir
        assinatura = Assinatura.objects.filter(external_reference=pagamento.external_reference).first()
        
        return JsonResponse({
            'status': pagamento.status,
            'status_display': pagamento.get_status_display(),
            'tem_assinatura': assinatura is not None,
            'assinatura_ativa': assinatura.status == 'ativa' if assinatura else False,
            'data_vencimento': assinatura.data_vencimento.isoformat() if assinatura else None
        })
        
    except Pagamento.DoesNotExist:
        return JsonResponse({'error': 'Pagamento não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        return JsonResponse({'error': 'Erro interno'}, status=500)

@login_required
def minhas_assinaturas(request):
    """
    Lista as assinaturas do usuário
    """
    assinaturas = Assinatura.objects.filter(usuario=request.user).order_by('-data_criacao')
    pagamentos = Pagamento.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    return render(request, 'payments/assinaturas.html', {
        'assinaturas': assinaturas,
        'pagamentos': pagamentos
    })

# =====================================================
# VIEWS DE CONTROLE DE ACESSO
# =====================================================

def verificar_acesso_premium(user):
    """
    Verifica se o usuário tem acesso premium ativo
    Retorna: (tem_acesso, assinatura) ou (False, None)
    """
    try:
        assinatura = Assinatura.objects.filter(
            usuario=user,
            status='ativa',
            data_vencimento__gt=datetime.now()
        ).first()
        
        return assinatura is not None, assinatura
        
    except Exception as e:
        logger.error(f"Erro ao verificar acesso premium: {e}")
        return False, None

def middleware_premium_required(view_func):
    """
    Decorator para verificar acesso premium
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        tem_acesso, assinatura = verificar_acesso_premium(request.user)
        
        if not tem_acesso:
            messages.warning(request, 'Esta funcionalidade requer assinatura premium.')
            return redirect('payments:planos')
        
        # Adicionar assinatura ao contexto
        request.assinatura = assinatura
        return view_func(request, *args, **kwargs)
    
    return wrapper

@login_required
@require_http_methods(["POST"])
def cancelar_assinatura(request):
    """
    Cancela a assinatura do usuário com política de reembolso
    """
    try:
        from django.utils import timezone
        
        # Buscar assinatura ativa do usuário
        assinatura = Assinatura.objects.filter(
            usuario=request.user,
            status='ativa',
            data_vencimento__gt=timezone.now()
        ).first()
        
        if not assinatura:
            return JsonResponse({
                'success': False,
                'error': 'Nenhuma assinatura ativa encontrada'
            })
        
        # Calcular dias desde a compra
        dias_desde_compra = (timezone.now() - assinatura.data_inicio).days
        
        # Verificar se tem direito a reembolso (menos de 7 dias)
        tem_direito_reembolso = dias_desde_compra < 7
        
        # Cancelar assinatura
        assinatura.status = 'cancelada'
        assinatura.data_cancelamento = timezone.now()
        assinatura.save()
        
        # Atualizar perfil do usuário
        try:
            profile = request.user.profile
            profile.conta_premium = False
            profile.data_vencimento_premium = None
            profile.save()
            
            # Atualizar status do pagamento para "não pago"
            pagamento = Pagamento.objects.filter(
                external_reference=assinatura.external_reference
            ).first()
            if pagamento:
                pagamento.status = 'cancelled'
                pagamento.save()
                logger.info(f"Status do pagamento {pagamento.id} alterado para 'cancelled'")
                
        except Exception as e:
            logger.warning(f"Erro ao atualizar perfil: {e}")
        
        # Processar reembolso se aplicável
        if tem_direito_reembolso:
            try:
                # Registrar reembolso no banco
                Reembolso.objects.create(
                    assinatura=assinatura,
                    valor=assinatura.plano.preco,
                    status='processado',
                    data_reembolso=timezone.now()
                )
                
                message = f"✅ Assinatura cancelada com sucesso!\n\n" \
                         f"💰 Reembolso de R$ {assinatura.plano.preco:.2f} será processado em até 5 dias úteis.\n\n" \
                         f"📧 Você receberá um email com os detalhes do reembolso."
            except Exception as e:
                logger.error(f"Erro ao criar reembolso: {e}")
                message = f"✅ Assinatura cancelada com sucesso!\n\n" \
                         f"💰 Reembolso de R$ {assinatura.plano.preco:.2f} será processado em até 5 dias úteis."
        else:
            message = f"✅ Assinatura cancelada com sucesso!\n\n" \
                     f"⚠️ Como passaram mais de 7 dias desde a compra, não há direito a reembolso.\n\n" \
                     f"🔒 Seu acesso premium foi revogado imediatamente."
        
        # Log da ação
        try:
            audit_logger.log_security_event(
                'subscription_cancelled',
                'medium',
                {
                    'user_id': request.user.id,
                    'subscription_id': assinatura.id,
                    'days_since_purchase': dias_desde_compra,
                    'refund_eligible': tem_direito_reembolso
                }
            )
        except Exception as e:
            logger.warning(f"Erro ao registrar log: {e}")
        
        return JsonResponse({
            'success': True,
            'message': message,
            'refund_eligible': tem_direito_reembolso
        })
        
    except Exception as e:
        logger.error(f"Erro ao cancelar assinatura: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        })
