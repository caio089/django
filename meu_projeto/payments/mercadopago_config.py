"""
Configurações centralizadas do Mercado Pago
"""
import os
import logging

logger = logging.getLogger(__name__)

def get_mercadopago_credentials():
    """
    Obtém as credenciais do Mercado Pago das variáveis de ambiente
    Retorna: (access_token, public_key, webhook_url, ambiente)
    """
    access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
    public_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
    webhook_url = os.getenv('MERCADOPAGO_WEBHOOK_URL', 'https://dojo-on.onrender.com/payments/webhook/')
    
    if not access_token or not public_key:
        logger.error("ERRO: Variaveis de ambiente MERCADOPAGO_ACCESS_TOKEN ou MERCADOPAGO_PUBLIC_KEY nao encontradas")
        return None, None, None, None
    
    # Detectar ambiente baseado no token
    if access_token.startswith('TEST-'):
        ambiente = 'sandbox'
        logger.info("Ambiente detectado: SANDBOX")
    elif access_token.startswith('APP-') or access_token.startswith('APP_USR-'):
        ambiente = 'production'
        logger.info("Ambiente detectado: PRODUCAO")
    else:
        ambiente = 'unknown'
        logger.warning("Ambiente desconhecido - Token nao reconhecido")
    
    logger.info(f"Credenciais carregadas - Ambiente: {ambiente}")
    logger.info(f"   Access Token: {access_token[:20]}...")
    logger.info(f"   Public Key: {public_key[:20]}...")
    logger.info(f"   Webhook URL: {webhook_url}")
    
    return access_token, public_key, webhook_url, ambiente

def is_sandbox():
    """
    Verifica se estamos em ambiente sandbox
    """
    access_token, _, _, ambiente = get_mercadopago_credentials()
    return ambiente == 'sandbox'

def get_webhook_url():
    """
    Retorna a URL do webhook configurada
    """
    _, _, webhook_url, _ = get_mercadopago_credentials()
    return webhook_url

def get_back_urls():
    """
    Retorna as URLs de retorno configuradas
    """
    base_url = "https://dojo-on.onrender.com"
    
    return {
        "success": f"{base_url}/payments/sucesso/",
        "failure": f"{base_url}/payments/falha/",
        "pending": f"{base_url}/payments/pendente/"
    }

def validate_credentials():
    """
    Valida se as credenciais estão configuradas corretamente
    """
    access_token, public_key, webhook_url, ambiente = get_mercadopago_credentials()
    
    if not access_token:
        return False, "Access Token não configurado"
    
    if not public_key:
        return False, "Public Key não configurada"
    
    if ambiente == 'unknown':
        return False, "Token inválido - deve começar com TEST- ou APP-"
    
    return True, f"Credenciais válidas - Ambiente: {ambiente}"

# Configurações específicas por ambiente
SANDBOX_CONFIG = {
    'enable_recaptcha': False,
    'advanced_fraud_prevention': False,
    'test_cards': {
        'visa': '5031 7557 3453 0604',
        'mastercard': '5031 7557 3453 0604',
        'amex': '3753 651535 56885'
    }
}

PRODUCTION_CONFIG = {
    'enable_recaptcha': True,
    'advanced_fraud_prevention': True,
    'require_verification': True
}

def get_environment_config():
    """
    Retorna configurações específicas do ambiente atual
    """
    if is_sandbox():
        return SANDBOX_CONFIG
    else:
        return PRODUCTION_CONFIG
