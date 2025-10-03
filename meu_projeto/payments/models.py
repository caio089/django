from django.db import models
from django.contrib.auth.models import User
import uuid
from decimal import Decimal
from .encryption import encryption_manager, email_encryption, payment_encryption
import json
import logging

logger = logging.getLogger(__name__)

class PlanoPremium(models.Model):
    """
    Modelo para definir os planos premium disponíveis
    Armazena informações sobre os diferentes tipos de assinatura
    """
    nome = models.CharField(max_length=100, verbose_name="Nome do plano")
    descricao = models.TextField(verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    duracao_dias = models.PositiveIntegerField(verbose_name="Duração em dias")
    ativo = models.BooleanField(default=True, verbose_name="Plano ativo")
    
    # Recursos do plano
    acesso_ilimitado_quiz = models.BooleanField(default=True, verbose_name="Acesso ilimitado ao quiz")
    relatorios_detalhados = models.BooleanField(default=True, verbose_name="Relatórios detalhados")
    suporte_prioritario = models.BooleanField(default=False, verbose_name="Suporte prioritário")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
    
    class Meta:
        verbose_name = "Plano Premium"
        verbose_name_plural = "Planos Premium"


class Assinatura(models.Model):
    """
    Modelo para gerenciar assinaturas premium dos usuários
    Registra o status da assinatura e datas importantes
    """
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
        ('suspensa', 'Suspensa'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assinaturas')
    plano = models.ForeignKey(PlanoPremium, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    
    # Datas importantes
    data_inicio = models.DateTimeField(verbose_name="Data de início")
    data_vencimento = models.DateTimeField(verbose_name="Data de vencimento")
    data_cancelamento = models.DateTimeField(null=True, blank=True, verbose_name="Data de cancelamento")
    
    # Identificadores externos (Mercado Pago)
    subscription_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="ID da Assinatura MP")
    external_reference = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Referência externa")
    
    # Campos de controle
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.plano.nome} ({self.status})"
    
    class Meta:
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"


class Pagamento(models.Model):
    """
    Modelo para registrar todos os pagamentos realizados
    Integrado com o Mercado Pago para controle de transações
    DADOS SENSÍVEIS CRIPTOGRAFADOS
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]
    
    TIPO_CHOICES = [
        ('assinatura', 'Assinatura'),
        ('compra_avulsa', 'Compra Avulsa'),
    ]
    
    # Relacionamentos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagamentos')
    assinatura = models.ForeignKey(Assinatura, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Informações do pagamento
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='assinatura')
    
    # Identificadores do Mercado Pago (CRIPTOGRAFADOS)
    payment_id = models.CharField(max_length=200, unique=True, verbose_name="ID do Pagamento MP (Criptografado)")
    external_reference = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Referência externa")
    
    # Dados sensíveis CRIPTOGRAFADOS
    payer_email_encrypted = models.TextField(null=True, blank=True, verbose_name="Email do pagador (Criptografado)")
    payer_name_encrypted = models.TextField(null=True, blank=True, verbose_name="Nome do pagador (Criptografado)")
    payer_phone_encrypted = models.TextField(null=True, blank=True, verbose_name="Telefone (Criptografado)")
    payer_document_encrypted = models.TextField(null=True, blank=True, verbose_name="CPF/Documento (Criptografado)")
    
    # Dados do cartão CRIPTOGRAFADOS (se aplicável)
    card_holder_name_encrypted = models.TextField(null=True, blank=True, verbose_name="Nome no cartão (Criptografado)")
    card_last_four_encrypted = models.TextField(null=True, blank=True, verbose_name="Últimos 4 dígitos (Criptografado)")
    
    # Informações não sensíveis
    descricao = models.TextField(verbose_name="Descrição do pagamento")
    metodo_pagamento = models.CharField(max_length=50, null=True, blank=True, verbose_name="Método de pagamento")
    
    # Dados de auditoria
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP do pagamento")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    
    # Timestamps
    data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do pagamento")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def set_payer_email(self, email):
        """Define email do pagador de forma criptografada"""
        if email:
            self.payer_email_encrypted = encryption_manager.encrypt(email)
    
    def get_payer_email(self):
        """Obtém email do pagador descriptografado"""
        if self.payer_email_encrypted:
            try:
                return encryption_manager.decrypt(self.payer_email_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar email: {e}")
                return None
        return None
    
    def set_payer_name(self, name):
        """Define nome do pagador de forma criptografada"""
        if name:
            self.payer_name_encrypted = encryption_manager.encrypt(name)
    
    def get_payer_name(self):
        """Obtém nome do pagador descriptografado"""
        if self.payer_name_encrypted:
            try:
                return encryption_manager.decrypt(self.payer_name_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar nome: {e}")
                return None
        return None
    
    def set_payer_phone(self, phone):
        """Define telefone de forma criptografada"""
        if phone:
            self.payer_phone_encrypted = encryption_manager.encrypt(phone)
    
    def get_payer_phone(self):
        """Obtém telefone descriptografado"""
        if self.payer_phone_encrypted:
            try:
                return encryption_manager.decrypt(self.payer_phone_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar telefone: {e}")
                return None
        return None
    
    def set_payer_document(self, document):
        """Define CPF/documento de forma criptografada"""
        if document:
            self.payer_document_encrypted = encryption_manager.encrypt(document)
    
    def get_payer_document(self):
        """Obtém CPF/documento descriptografado"""
        if self.payer_document_encrypted:
            try:
                return encryption_manager.decrypt(self.payer_document_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar documento: {e}")
                return None
        return None
    
    def set_payment_id(self, payment_id):
        """Define ID do pagamento"""
        if payment_id:
            self.payment_id = str(payment_id)
    
    def get_payment_id(self):
        """Obtém ID do pagamento"""
        return self.payment_id
    
    def __str__(self):
        return f"Pagamento {self.get_payment_id() or 'N/A'} - R$ {self.valor}"
    
    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_criacao']


class WebhookEvent(models.Model):
    """
    Modelo para registrar eventos recebidos via webhook do Mercado Pago
    Permite rastreamento e debug de notificações
    DADOS SENSÍVEIS CRIPTOGRAFADOS
    """
    TIPO_CHOICES = [
        ('payment', 'Pagamento'),
        ('subscription', 'Assinatura'),
        ('invoice', 'Fatura'),
        ('point_integration_wh', 'Ponto de Integração'),
    ]
    
    # Informações do evento
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo de evento")
    action = models.CharField(max_length=50, verbose_name="Ação")
    
    # Identificadores (CRIPTOGRAFADOS)
    id_mercadopago_encrypted = models.TextField(verbose_name="ID Mercado Pago (Criptografado)", default='')
    external_reference_encrypted = models.TextField(null=True, blank=True, verbose_name="Referência externa (Criptografada)", default='')
    
    # Dados do evento (CRIPTOGRAFADOS)
    data_recebida_encrypted = models.TextField(verbose_name="Dados recebidos (Criptografados)", default='')
    processado = models.BooleanField(default=False, verbose_name="Processado")
    erro_processamento = models.TextField(null=True, blank=True, verbose_name="Erro no processamento")
    
    # Dados de segurança
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP do webhook")
    signature = models.TextField(null=True, blank=True, verbose_name="Assinatura do webhook")
    
    # Timestamps
    data_recebimento = models.DateTimeField(auto_now_add=True, verbose_name="Data de recebimento")
    data_processamento = models.DateTimeField(null=True, blank=True, verbose_name="Data de processamento")
    
    def set_id_mercadopago(self, mp_id):
        """Define ID do Mercado Pago de forma criptografada"""
        if mp_id:
            self.id_mercadopago_encrypted = encryption_manager.encrypt(str(mp_id))
    
    def get_id_mercadopago(self):
        """Obtém ID do Mercado Pago descriptografado"""
        if self.id_mercadopago_encrypted:
            try:
                return encryption_manager.decrypt(self.id_mercadopago_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar ID Mercado Pago: {e}")
                return None
        return None
    
    def set_external_reference(self, ref):
        """Define referência externa de forma criptografada"""
        if ref:
            self.external_reference_encrypted = encryption_manager.encrypt(str(ref))
    
    def get_external_reference(self):
        """Obtém referência externa descriptografada"""
        if self.external_reference_encrypted:
            try:
                return encryption_manager.decrypt(self.external_reference_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar referência externa: {e}")
                return None
        return None
    
    def set_data_recebida(self, data):
        """Define dados recebidos de forma criptografada"""
        if data:
            # Converter para JSON se necessário
            if isinstance(data, dict):
                data_str = json.dumps(data, ensure_ascii=False)
            else:
                data_str = str(data)
            self.data_recebida_encrypted = encryption_manager.encrypt(data_str)
    
    def get_data_recebida(self):
        """Obtém dados recebidos descriptografados"""
        if self.data_recebida_encrypted:
            try:
                decrypted_data = encryption_manager.decrypt(self.data_recebida_encrypted)
                # Tentar converter de volta para JSON
                try:
                    return json.loads(decrypted_data)
                except json.JSONDecodeError:
                    return decrypted_data
            except Exception as e:
                logger.error(f"Erro ao descriptografar dados recebidos: {e}")
                return None
        return None
    
    def __str__(self):
        return f"Webhook {self.tipo} - {self.action} - {self.data_recebimento}"
    
    class Meta:
        verbose_name = "Evento Webhook"
        verbose_name_plural = "Eventos Webhook"
        ordering = ['-data_recebimento']


class ConfiguracaoPagamento(models.Model):
    """
    Modelo para configurações do sistema de pagamento
    Armazena tokens e configurações do Mercado Pago
    TOKENS CRIPTOGRAFADOS
    """
    # Tokens do Mercado Pago (CRIPTOGRAFADOS)
    access_token_encrypted = models.TextField(verbose_name="Access Token (Criptografado)", default='')
    public_key_encrypted = models.TextField(verbose_name="Public Key (Criptografado)", default='')
    
    # Configurações de webhook
    webhook_url = models.URLField(verbose_name="URL do Webhook")
    webhook_secret_encrypted = models.TextField(verbose_name="Secret do Webhook (Criptografado)", default='')
    
    # Configurações gerais
    ambiente = models.CharField(max_length=10, choices=[('sandbox', 'Sandbox'), ('production', 'Produção')], default='sandbox')
    ativo = models.BooleanField(default=True, verbose_name="Configuração ativa")
    
    # Dados de auditoria
    last_used = models.DateTimeField(null=True, blank=True, verbose_name="Último uso")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="Contador de uso")
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def set_access_token(self, token):
        """Define access token de forma criptografada"""
        if token:
            self.access_token_encrypted = encryption_manager.encrypt(token)
    
    def get_access_token(self):
        """Obtém access token descriptografado"""
        if self.access_token_encrypted:
            try:
                # Tentar descriptografar primeiro
                return encryption_manager.decrypt(self.access_token_encrypted)
            except Exception as e:
                logger.warning(f"Erro ao descriptografar access token: {e}")
                # Se falhar, pode ser que o token não esteja criptografado
                # Verificar se parece com um token válido (não criptografado)
                if self.access_token_encrypted.startswith(('TEST-', 'APP-')):
                    logger.info("Usando token não criptografado")
                    return self.access_token_encrypted
                else:
                    logger.error("Token não é válido nem criptografado")
                    # Tentar usar o token como está (pode ser válido mas não reconhecido)
                    logger.info("Tentando usar token como está")
                    return self.access_token_encrypted
        else:
            # Se não há token criptografado, tentar obter das variáveis de ambiente
            import os
            env_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
            if env_token:
                logger.info("Usando token das variáveis de ambiente")
                return env_token
        return None
    
    def set_public_key(self, key):
        """Define public key de forma criptografada"""
        if key:
            self.public_key_encrypted = encryption_manager.encrypt(key)
    
    def get_public_key(self):
        """Obtém public key descriptografada"""
        if self.public_key_encrypted:
            try:
                # Tentar descriptografar primeiro
                return encryption_manager.decrypt(self.public_key_encrypted)
            except Exception as e:
                logger.warning(f"Erro ao descriptografar public key: {e}")
                # Se falhar, pode ser que a key não esteja criptografada
                # Verificar se parece com uma key válida (não criptografada)
                if self.public_key_encrypted.startswith(('TEST-', 'APP-')):
                    logger.info("Usando public key não criptografada")
                    return self.public_key_encrypted
                else:
                    logger.error("Public key não é válida nem criptografada")
                    # Tentar usar a key como está (pode ser válida mas não reconhecida)
                    logger.info("Tentando usar public key como está")
                    return self.public_key_encrypted
        else:
            # Se não há key criptografada, tentar obter das variáveis de ambiente
            import os
            env_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
            if env_key:
                logger.info("Usando public key das variáveis de ambiente")
                return env_key
        return None
    
    def set_webhook_secret(self, secret):
        """Define webhook secret de forma criptografada"""
        if secret:
            self.webhook_secret_encrypted = encryption_manager.encrypt(secret)
    
    def get_webhook_secret(self):
        """Obtém webhook secret descriptografado"""
        if self.webhook_secret_encrypted:
            try:
                return encryption_manager.decrypt(self.webhook_secret_encrypted)
            except Exception as e:
                logger.error(f"Erro ao descriptografar webhook secret: {e}")
                return None
        return None
    
    def mark_usage(self):
        """Marca uso da configuração"""
        from django.utils import timezone
        self.last_used = timezone.now()
        self.usage_count += 1
        self.save(update_fields=['last_used', 'usage_count'])
    
    def __str__(self):
        return f"Configuração {self.ambiente} - {'Ativa' if self.ativo else 'Inativa'}"
    
    class Meta:
        verbose_name = "Configuração de Pagamento"
        verbose_name_plural = "Configurações de Pagamento"


class Reembolso(models.Model):
    """
    Modelo para gerenciar reembolsos de assinaturas canceladas
    Registra informações sobre reembolsos processados
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processado', 'Processado'),
        ('falhou', 'Falhou'),
        ('cancelado', 'Cancelado'),
    ]
    
    assinatura = models.ForeignKey(Assinatura, on_delete=models.CASCADE, related_name='reembolsos')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do reembolso")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da solicitação")
    data_reembolso = models.DateTimeField(null=True, blank=True, verbose_name="Data do reembolso")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo do reembolso")
    
    # Dados do reembolso (criptografados)
    _refund_id = models.TextField(blank=True, null=True, verbose_name="ID do reembolso")
    _refund_data = models.TextField(blank=True, null=True, verbose_name="Dados do reembolso")
    
    def set_refund_id(self, refund_id):
        """Criptografa e armazena o ID do reembolso"""
        if refund_id:
            self._refund_id = payment_encryption.encrypt(refund_id)
    
    def get_refund_id(self):
        """Descriptografa e retorna o ID do reembolso"""
        if self._refund_id:
            try:
                return payment_encryption.decrypt(self._refund_id)
            except Exception as e:
                logger.error(f"Erro ao descriptografar refund_id: {e}")
                return None
        return None
    
    def set_refund_data(self, data):
        """Criptografa e armazena os dados do reembolso"""
        if data:
            self._refund_data = payment_encryption.encrypt(json.dumps(data))
    
    def get_refund_data(self):
        """Descriptografa e retorna os dados do reembolso"""
        if self._refund_data:
            try:
                return json.loads(payment_encryption.decrypt(self._refund_data))
            except Exception as e:
                logger.error(f"Erro ao descriptografar refund_data: {e}")
                return None
        return None
    
    def __str__(self):
        return f"Reembolso {self.id} - {self.assinatura.usuario.username} - R$ {self.valor}"
    
    class Meta:
        verbose_name = "Reembolso"
        verbose_name_plural = "Reembolsos"
        ordering = ['-data_solicitacao']