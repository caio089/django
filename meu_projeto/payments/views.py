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
import os
from .models import PlanoPremium, Assinatura, Pagamento, WebhookEvent, ConfiguracaoPagamento
from .security import WebhookSecurity, RateLimiter, AuditLogger, DataValidator
from home.models import Profile
from quiz.models import ProgressoUsuario
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
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
    Obtém as configurações do Mercado Pago usando configuração centralizada
    Retorna: (sdk, config) ou (None, None) se erro
    """
    try:
        from .mercadopago_config import get_mercadopago_credentials, validate_credentials
        
        # Validar credenciais
        is_valid, message = validate_credentials()
        if not is_valid:
            logger.error(f"❌ Credenciais inválidas: {message}")
            return None, None
        
        # Obter credenciais
        access_token, public_key, webhook_url, ambiente = get_mercadopago_credentials()
        
        if not access_token or not public_key:
            logger.error("❌ Credenciais não encontradas após validação")
            return None, None
        
        logger.info(f"✅ Configurando SDK Mercado Pago - Ambiente: {ambiente}")
        sdk = mercadopago.SDK(access_token)
        
        # Criar um objeto config simples
        class SimpleConfig:
            def __init__(self, access_token, public_key, webhook_url, ambiente):
                self.access_token = access_token
                self.public_key = public_key
                self.webhook_url = webhook_url
                self.ambiente = ambiente
            
            def get_public_key(self):
                return self.public_key
            
            def mark_usage(self):
                pass
        
        config = SimpleConfig(access_token, public_key, webhook_url, ambiente)
        logger.info(f"✅ SDK criado com sucesso - Ambiente: {ambiente}")
        return sdk, config
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar Mercado Pago: {e}", exc_info=True)
        return None, None

def is_sandbox_environment():
    """
    Detecta se estamos em ambiente sandbox baseado no access token
    """
    try:
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if config:
            access_token = config.get_access_token()
            # Tokens de sandbox geralmente começam com TEST-
            return access_token.startswith('TEST-') if access_token else True
        return True  # Assume sandbox por padrão
    except:
        return True

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
        data_vencimento__gt=timezone.now()
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
        data_vencimento__gt=timezone.now()
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
@require_http_methods(["POST"])
def criar_pagamento(request, plano_id):
    """
    Cria um pagamento no Mercado Pago e retorna dados para checkout transparente
    """
    try:
        # Obter dados do formulário
        plano_id = plano_id or request.POST.get('plano_id')
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
        if not all([plano_id, nome, email]):
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
                "success": "https://dojo-on.onrender.com/payments/sucesso/",
                "failure": "https://dojo-on.onrender.com/payments/falha/",
                "pending": "https://dojo-on.onrender.com/payments/pendente/"
            },
            "external_reference": external_reference,
            "notification_url": config.webhook_url,
            "payment_methods": {
                "excluded_payment_methods": [],
                "excluded_payment_types": [],
                "installments": 12
            },
            "auto_return": "approved",
            "binary_mode": False,
            "statement_descriptor": "DOJO-ON",
            "metadata": {
                "plano_id": str(plano.id),
                "user_id": str(request.user.id),
                "external_reference": external_reference
            },
            "differential_pricing": {
                "id": 1
            }
        }
        
        # Criar preferência no Mercado Pago
        logger.info(f"Criando preferência com dados: {preference_data}")
        preference = sdk.preference().create(preference_data)
        logger.info(f"Resposta da preferência: {preference}")
        
        if preference["status"] == 201:
            preference_data = preference["response"]
            
            # Salvar pagamento no banco com dados criptografados
            pagamento = Pagamento.objects.create(
                usuario=request.user,
                valor=plano.preco,
                tipo='assinatura',
                payment_id=f"temp_{external_reference}",  # ID temporário único
                external_reference=external_reference,
                descricao=f"Assinatura {plano.nome}",
                ip_address=WebhookSecurity.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Criptografar dados sensíveis
            # O preference_id não é o payment_id - será definido quando o pagamento for processado
            pagamento.set_payment_id(f"pref_{preference_data['id']}")
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
                'preference_id': preference_data["id"],
                'public_key': config.get_public_key(),
                'payment_id': pagamento.id,
                'external_reference': external_reference
            })
        else:
            logger.error(f"Erro ao criar preferência: {preference}")
            return JsonResponse({
                'success': False,
                'error': 'Erro ao criar pagamento no Mercado Pago'
            })
            
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {e}", exc_info=True)
        import traceback
        logger.error(f"Traceback completo: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        })

@login_required
@require_http_methods(["POST"])
def criar_pagamento_cartao(request, payment_id):
    """
    Cria um pagamento com cartão de crédito no Mercado Pago
    """
    try:
        pagamento = get_object_or_404(Pagamento, id=payment_id, usuario=request.user)
        
        # Obter configuração do Mercado Pago
        sdk, config = get_mercadopago_config()
        if not sdk:
            return JsonResponse({
                'success': False,
                'error': 'Erro na configuração do pagamento'
            })
        
        # Buscar plano pelo valor
        plano = PlanoPremium.objects.filter(preco=pagamento.valor, ativo=True).first()
        if not plano:
            return JsonResponse({
                'success': False,
                'error': 'Plano não encontrado'
            })
        
        # Criar preferência de pagamento para cartão
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
                "email": pagamento.get_payer_email() or pagamento.usuario.email,
                "identification": {
                    "type": "CPF",
                    "number": pagamento.get_payer_document() or "00000000000"
                }
            },
            "back_urls": {
                "success": "https://dojo-on.onrender.com/payments/sucesso/",
                "failure": "https://dojo-on.onrender.com/payments/falha/",
                "pending": "https://dojo-on.onrender.com/payments/pendente/"
            },
            "external_reference": str(pagamento.external_reference),
            "notification_url": config.webhook_url,
            "payment_methods": {
                "excluded_payment_methods": [
                    {"id": "pix"}  # Excluir PIX para forçar cartão
                ],
                "excluded_payment_types": [],
                "installments": 12
            },
            "auto_return": "approved",
            "binary_mode": False,
            "statement_descriptor": "DOJO-ON",
            "metadata": {
                "plano_id": str(plano.id),
                "user_id": str(request.user.id),
                "external_reference": str(pagamento.external_reference),
                "payment_type": "cartao"
            }
        }
        
        # Criar preferência no Mercado Pago
        logger.info(f"Criando preferência para cartão com dados: {preference_data}")
        preference = sdk.preference().create(preference_data)
        logger.info(f"Resposta da preferência cartão: {preference}")
        
        if preference["status"] == 201:
            preference_data = preference["response"]
            
            # Atualizar pagamento com o ID da preferência
            pagamento.set_payment_id(f"pref_{preference_data['id']}")
            pagamento.save()
            
            return JsonResponse({
                'success': True,
                'preference_id': preference_data["id"],
                'init_point': preference_data["init_point"],
                'public_key': config.get_public_key(),
                'payment_id': pagamento.id,
                'external_reference': str(pagamento.external_reference)
            })
        else:
            logger.error(f"Erro ao criar preferência cartão: {preference}")
            return JsonResponse({
                'success': False,
                'error': 'Erro ao criar pagamento com cartão no Mercado Pago'
            })
            
    except Exception as e:
        logger.error(f"Erro ao criar pagamento cartão: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        })

@login_required
@require_http_methods(["POST"])
def gerar_pix_direto(request, payment_id):
    """
    Gera QR Code PIX diretamente para um pagamento
    """
    try:
        pagamento = get_object_or_404(Pagamento, id=payment_id, usuario=request.user)
        
        # Obter configuração do Mercado Pago
        sdk, config = get_mercadopago_config()
        if not sdk:
            return JsonResponse({
                'success': False,
                'error': 'Erro na configuração do pagamento'
            })
        
        # Criar um pagamento PIX no Mercado Pago
        payment_data = {
            "transaction_amount": float(pagamento.valor),
            "description": pagamento.descricao,
            "payment_method_id": "pix",
            "payer": {
                "email": pagamento.get_payer_email() or pagamento.usuario.email,
                "identification": {
                    "type": "CPF",
                    "number": pagamento.get_payer_document() or "00000000000"
                }
            },
            "external_reference": str(pagamento.external_reference)
        }
        
        # Criar pagamento no Mercado Pago
        payment_result = sdk.payment().create(payment_data)
        
        if payment_result["status"] == 201:
            payment_info = payment_result["response"]
            payment_id_mp = payment_info["id"]
            
            # Atualizar pagamento com o ID real do Mercado Pago
            pagamento.set_payment_id(str(payment_id_mp))
            pagamento.status = 'pending'
            pagamento.save()
            
            # Verificar se o pagamento PIX foi criado com sucesso
            if payment_info.get("status") == "pending":
                # Buscar informações do PIX no Mercado Pago
                point_of_interaction = payment_info.get("point_of_interaction", {})
                transaction_details = payment_info.get("transaction_details", {})
            
                # Extrair dados do PIX do Mercado Pago
                qr_code = point_of_interaction.get("transaction_data", {}).get("qr_code")
                qr_code_base64 = point_of_interaction.get("transaction_data", {}).get("qr_code_base64")
                
                if qr_code:
                    logger.info(f"PIX gerado com sucesso - Payment ID: {payment_id_mp}")
                    logger.info(f"QR Code: {qr_code[:50]}...")
                    
                    return JsonResponse({
                        'success': True,
                        'qr_code': qr_code,
                        'qr_code_base64': qr_code_base64,
                        'payment_id': payment_id_mp,
                        'amount': payment_info.get("transaction_amount"),
                        'currency': payment_info.get("currency_id"),
                        'status': payment_info.get("status"),
                        'validation': {
                            'is_valid': True,
                            'message': 'QR Code PIX válido do Mercado Pago'
                        },
                        'pix_info': {
                            'chave_pix': 'Chave PIX do Mercado Pago',
                            'nome_beneficiario': 'Mercado Pago',
                            'cidade': 'Brasil'
                        }
                    })
                else:
                    logger.error(f"PIX criado mas sem QR Code - Payment: {payment_info}")
                    return JsonResponse({
                        'success': False,
                        'error': 'PIX criado mas QR Code não disponível'
                    })
            else:
                logger.error(f"PIX não foi criado corretamente - Status: {payment_info.get('status')}")
                return JsonResponse({
                    'success': False,
                    'error': f'Erro ao criar PIX - Status: {payment_info.get("status")}'
                })
        else:
            logger.error(f"Erro ao criar pagamento PIX: {payment_result}")
            return JsonResponse({
                'success': False,
                'error': f'Erro ao criar pagamento PIX: {payment_result.get("response", {}).get("message", "Erro desconhecido")}'
            })
            
    except Exception as e:
        logger.error(f"Erro ao gerar PIX: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        })

@login_required
def checkout_pagamento(request, payment_id):
    """
    Página de checkout com Mercado Pago
    """
    pagamento = get_object_or_404(Pagamento, id=payment_id, usuario=request.user)
    
    # Obter configuração do Mercado Pago
    sdk, config = get_mercadopago_config()
    if not config:
        messages.error(request, 'Erro na configuração do pagamento.')
        return redirect('payments:planos')
    
    # Debug: verificar dados do pagamento
    payment_id_mp = pagamento.get_payment_id()
    logger.info(f"Checkout - Payment ID: {payment_id_mp}")
    logger.info(f"Checkout - Payment status: {pagamento.status}")
    logger.info(f"Checkout - External reference: {pagamento.external_reference}")
    
    # Se o payment_id começa com "pref_", é uma preferência
    if payment_id_mp and payment_id_mp.startswith('pref_'):
        preference_id = payment_id_mp.replace('pref_', '')
        init_point = f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={preference_id}"
        logger.info(f"Checkout - Init Point: {init_point}")
        
        return render(request, 'payments/checkout.html', {
            'pagamento': pagamento,
            'public_key': config.get_public_key(),
            'preference_id': preference_id,
            'init_point': init_point
        })
    else:
        # Se não é uma preferência, criar uma nova
        logger.info("Criando nova preferência para checkout...")
        
        # Buscar plano pelo valor
        plano = PlanoPremium.objects.filter(preco=pagamento.valor, ativo=True).first()
        if not plano:
            messages.error(request, 'Plano não encontrado.')
            return redirect('payments:planos')
        
        # Criar preferência
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
                "email": pagamento.get_payer_email() or pagamento.usuario.email,
                "identification": {
                    "type": "CPF",
                    "number": pagamento.get_payer_document() or "00000000000"
                }
            },
            "back_urls": {
                "success": "https://dojo-on.onrender.com/payments/sucesso/",
                "failure": "https://dojo-on.onrender.com/payments/falha/",
                "pending": "https://dojo-on.onrender.com/payments/pendente/"
            },
            "external_reference": str(pagamento.external_reference),
            "notification_url": config.webhook_url,
            "payment_methods": {
                "excluded_payment_methods": [],
                "excluded_payment_types": [],
                "installments": 12
            },
            "auto_return": "approved",
            "binary_mode": False,
            "statement_descriptor": "DOJO-ON"
        }
        
        try:
            preference = sdk.preference().create(preference_data)
            if preference["status"] == 201:
                preference_data = preference["response"]
                init_point = preference_data["init_point"]
                preference_id = preference_data["id"]
                
                # Atualizar pagamento com o ID da preferência
                pagamento.set_payment_id(f"pref_{preference_id}")
                pagamento.save()
                
                logger.info(f"Preferência criada: {preference_id}")
                
                return render(request, 'payments/checkout.html', {
                    'pagamento': pagamento,
                    'public_key': config.get_public_key(),
                    'preference_id': preference_id,
                    'init_point': init_point
                })
            else:
                logger.error(f"Erro ao criar preferência: {preference}")
                messages.error(request, 'Erro ao criar checkout.')
                return redirect('payments:planos')
        except Exception as e:
            logger.error(f"Erro ao criar preferência: {e}")
            messages.error(request, 'Erro ao criar checkout.')
            return redirect('payments:planos')

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
        
        # Verificar origem do webhook (mais permissivo para Mercado Pago)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if not WebhookSecurity.verify_webhook_origin(request) and 'MercadoPago' not in user_agent:
            audit_logger.log_security_event(
                'invalid_webhook_origin',
                'high',
                {'ip': client_ip, 'user_agent': user_agent}
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
        webhook_event.data_processamento = timezone.now()
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
        pagamento.data_pagamento = timezone.now()
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
        data_inicio = timezone.now()
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
        
        # Atualizar perfil do usuário
        try:
            profile = pagamento.usuario.profile
            profile.conta_premium = True
            profile.data_vencimento_premium = data_vencimento
            profile.save()
        except:
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
    from django.utils import timezone
    
    assinaturas = Assinatura.objects.filter(usuario=request.user).order_by('-data_criacao')
    pagamentos = Pagamento.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    return render(request, 'payments/assinaturas.html', {
        'assinaturas': assinaturas,
        'pagamentos': pagamentos,
        'now': timezone.now()
    })

@login_required
@require_http_methods(["POST"])
def cancelar_assinatura(request, assinatura_id):
    """
    Cancela uma assinatura ativa do usuário
    """
    try:
        assinatura = get_object_or_404(Assinatura, id=assinatura_id, usuario=request.user)
        
        # Verificar se a assinatura pode ser cancelada
        if assinatura.status != 'ativa':
            messages.error(request, 'Esta assinatura não pode ser cancelada.')
            return redirect('payments:assinaturas')
        
        # Cancelar assinatura
        assinatura.status = 'cancelada'
        assinatura.data_cancelamento = timezone.now()
        assinatura.save()
        
        # Atualizar perfil do usuário
        try:
            profile = request.user.profile
            profile.conta_premium = False
            profile.save()
        except:
            logger.error(f"Erro ao atualizar perfil do usuário {request.user.id}")
        
        # Registrar auditoria
        audit_logger.log_payment_attempt(
            user_id=request.user.id,
            payment_id=f'cancel_{assinatura.id}',
            status='cancelled',
            details={'assinatura_id': assinatura.id, 'plano': assinatura.plano.nome}
        )
        
        messages.success(request, f'Assinatura {assinatura.plano.nome} cancelada com sucesso!')
        logger.info(f"Assinatura {assinatura.id} cancelada pelo usuário {request.user.id}")
        
    except Exception as e:
        logger.error(f"Erro ao cancelar assinatura {assinatura_id}: {e}")
        messages.error(request, 'Erro ao cancelar assinatura. Tente novamente.')
    
    return redirect('payments:assinaturas')

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
            data_vencimento__gt=timezone.now()
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
