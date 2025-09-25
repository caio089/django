"""
Sistema de segurança para webhooks e validações
"""

import hmac
import hashlib
import json
import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import ConfiguracaoPagamento, WebhookEvent
from .encryption import encryption_manager
import requests

logger = logging.getLogger(__name__)

class WebhookSecurity:
    """
    Classe para verificação de segurança de webhooks
    """
    
    @staticmethod
    def verify_mercadopago_signature(payload, signature, secret):
        """
        Verifica assinatura do webhook do Mercado Pago
        
        Args:
            payload (bytes): Dados do webhook
            signature (str): Assinatura recebida
            secret (str): Secret do webhook
            
        Returns:
            bool: True se assinatura for válida
        """
        if not secret or not signature:
            return False
            
        try:
            # Gerar assinatura esperada
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            # Comparar assinaturas de forma segura
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Erro ao verificar assinatura: {e}")
            return False
    
    @staticmethod
    def verify_webhook_origin(request):
        """
        Verifica se o webhook veio do Mercado Pago
        
        Args:
            request: Request do Django
            
        Returns:
            bool: True se origem for válida
        """
        # IPs conhecidos do Mercado Pago
        mercadopago_ips = [
            '54.233.0.0/16',    # Mercado Pago Brasil
            '54.207.0.0/16',    # Mercado Pago Argentina
            '54.94.0.0/16',     # Mercado Pago México
        ]
        
        client_ip = WebhookSecurity.get_client_ip(request)
        
        # Verificar se IP está na lista (simplificado)
        for ip_range in mercadopago_ips:
            if client_ip.startswith(ip_range.split('/')[0].rsplit('.', 1)[0]):
                return True
        
        return False
    
    @staticmethod
    def get_client_ip(request):
        """
        Obtém IP real do cliente
        
        Args:
            request: Request do Django
            
        Returns:
            str: IP do cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RateLimiter:
    """
    Sistema de rate limiting para webhooks
    """
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, ip, limit=10, window=60):
        """
        Verifica se IP pode fazer requisição
        
        Args:
            ip (str): IP do cliente
            limit (int): Limite de requisições
            window (int): Janela de tempo em segundos
            
        Returns:
            bool: True se permitido
        """
        now = timezone.now().timestamp()
        
        if ip not in self.requests:
            self.requests[ip] = []
        
        # Remover requisições antigas
        self.requests[ip] = [
            req_time for req_time in self.requests[ip]
            if now - req_time < window
        ]
        
        # Verificar limite
        if len(self.requests[ip]) >= limit:
            return False
        
        # Adicionar requisição atual
        self.requests[ip].append(now)
        return True

class AuditLogger:
    """
    Sistema de logs de auditoria para segurança
    """
    
    @staticmethod
    def log_webhook_event(request, event_type, status, details=None):
        """
        Registra evento de webhook para auditoria
        
        Args:
            request: Request do Django
            event_type (str): Tipo do evento
            status (str): Status do processamento
            details (dict): Detalhes adicionais
        """
        try:
            client_ip = WebhookSecurity.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            log_data = {
                'timestamp': timezone.now().isoformat(),
                'event_type': event_type,
                'status': status,
                'client_ip': client_ip,
                'user_agent': user_agent,
                'details': details or {}
            }
            
            logger.info(f"WEBHOOK_AUDIT: {json.dumps(log_data)}")
            
        except Exception as e:
            logger.error(f"Erro ao registrar log de auditoria: {e}")
    
    @staticmethod
    def log_payment_attempt(user_id, payment_id, status, details=None):
        """
        Registra tentativa de pagamento para auditoria
        
        Args:
            user_id (int): ID do usuário
            payment_id (str): ID do pagamento
            status (str): Status da tentativa
            details (dict): Detalhes adicionais
        """
        try:
            log_data = {
                'timestamp': timezone.now().isoformat(),
                'event_type': 'payment_attempt',
                'user_id': user_id,
                'payment_id': payment_id,
                'status': status,
                'details': details or {}
            }
            
            logger.info(f"PAYMENT_AUDIT: {json.dumps(log_data)}")
            
        except Exception as e:
            logger.error(f"Erro ao registrar log de pagamento: {e}")
    
    @staticmethod
    def log_security_event(event_type, severity, details=None):
        """
        Registra evento de segurança
        
        Args:
            event_type (str): Tipo do evento
            severity (str): Severidade (low, medium, high, critical)
            details (dict): Detalhes do evento
        """
        try:
            log_data = {
                'timestamp': timezone.now().isoformat(),
                'event_type': event_type,
                'severity': severity,
                'details': details or {}
            }
            
            if severity in ['high', 'critical']:
                logger.error(f"SECURITY_EVENT: {json.dumps(log_data)}")
            else:
                logger.warning(f"SECURITY_EVENT: {json.dumps(log_data)}")
                
        except Exception as e:
            logger.error(f"Erro ao registrar evento de segurança: {e}")

class DataValidator:
    """
    Validador de dados para segurança
    """
    
    @staticmethod
    def validate_email(email):
        """
        Valida formato de email
        
        Args:
            email (str): Email a ser validado
            
        Returns:
            bool: True se válido
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_cpf(cpf):
        """
        Valida CPF brasileiro
        
        Args:
            cpf (str): CPF a ser validado
            
        Returns:
            bool: True se válido
        """
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não são todos iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação do algoritmo do CPF
        def calculate_digit(cpf_digits, multiplier):
            total = sum(int(digit) * mult for digit, mult in zip(cpf_digits, multiplier))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Primeiro dígito verificador
        first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
        if int(cpf[9]) != first_digit:
            return False
        
        # Segundo dígito verificador
        second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
        if int(cpf[10]) != second_digit:
            return False
        
        return True
    
    @staticmethod
    def validate_phone(phone):
        """
        Valida telefone brasileiro
        
        Args:
            phone (str): Telefone a ser validado
            
        Returns:
            bool: True se válido
        """
        # Remove caracteres não numéricos
        phone = ''.join(filter(str.isdigit, phone))
        
        # Verifica se tem 10 ou 11 dígitos
        if len(phone) not in [10, 11]:
            return False
        
        # Verifica se começa com dígito válido
        if len(phone) == 11 and phone[0] not in ['1', '2', '3', '4', '5']:
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(data):
        """
        Sanitiza dados de entrada
        
        Args:
            data (str): Dados a serem sanitizados
            
        Returns:
            str: Dados sanitizados
        """
        if not isinstance(data, str):
            return data
        
        # Remove caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        for char in dangerous_chars:
            data = data.replace(char, '')
        
        # Remove espaços extras
        data = ' '.join(data.split())
        
        return data.strip()

class SecurityMiddleware:
    """
    Middleware de segurança para requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Adicionar headers de segurança
        response = self.get_response(request)
        
        # Headers de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

# Instâncias globais
rate_limiter = RateLimiter()
audit_logger = AuditLogger()
data_validator = DataValidator()
