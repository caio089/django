from django.db import models
from django.contrib.auth.models import User
import uuid
from decimal import Decimal
# Removido: from .encryption import encryption_manager, email_encryption, payment_encryption
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
    
    # Imagens do plano para mostrar o que o usuário terá acesso (3 fotos principais)
    imagem_1 = models.ImageField(upload_to='planos/imagens/', null=True, blank=True, verbose_name="Imagem 1 - Quiz e Aprendizado")
    imagem_2 = models.ImageField(upload_to='planos/imagens/', null=True, blank=True, verbose_name="Imagem 2 - Vídeos de Técnicas")
    imagem_3 = models.ImageField(upload_to='planos/imagens/', null=True, blank=True, verbose_name="Imagem 3 - Organização e Estrutura")
    
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
    
    # Identificadores do Mercado Pago
    payment_id = models.CharField(max_length=200, unique=True, verbose_name="ID do Pagamento MP")
    external_reference = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Referência externa")
    
    # Dados do pagador
    payer_email = models.EmailField(null=True, blank=True, verbose_name="Email do pagador")
    payer_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nome do pagador")
    payer_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    payer_document = models.CharField(max_length=20, null=True, blank=True, verbose_name="CPF/Documento")
    
    # Dados do cartão (se aplicável)
    card_holder_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nome no cartão")
    card_last_four = models.CharField(max_length=4, null=True, blank=True, verbose_name="Últimos 4 dígitos")
    
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
        """Define email do pagador"""
        if email:
            self.payer_email = email
    
    def get_payer_email(self):
        """Obtém email do pagador"""
        return self.payer_email
    
    def set_payer_name(self, name):
        """Define nome do pagador"""
        if name:
            self.payer_name = name
    
    def get_payer_name(self):
        """Obtém nome do pagador"""
        return self.payer_name
    
    def set_payer_phone(self, phone):
        """Define telefone"""
        if phone:
            self.payer_phone = phone
    
    def get_payer_phone(self):
        """Obtém telefone"""
        return self.payer_phone
    
    def set_payer_document(self, document):
        """Define CPF/documento"""
        if document:
            self.payer_document = document
    
    def get_payer_document(self):
        """Obtém CPF/documento"""
        return self.payer_document
    
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
    
    # Identificadores
    id_mercadopago = models.CharField(max_length=100, verbose_name="ID Mercado Pago", default='')
    external_reference = models.CharField(max_length=100, null=True, blank=True, verbose_name="Referência externa", default='')
    
    # Dados do evento
    data_recebida = models.JSONField(verbose_name="Dados recebidos", default=dict)
    processado = models.BooleanField(default=False, verbose_name="Processado")
    erro_processamento = models.TextField(null=True, blank=True, verbose_name="Erro no processamento")
    
    # Dados de segurança
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP do webhook")
    signature = models.TextField(null=True, blank=True, verbose_name="Assinatura do webhook")
    
    # Timestamps
    data_recebimento = models.DateTimeField(auto_now_add=True, verbose_name="Data de recebimento")
    data_processamento = models.DateTimeField(null=True, blank=True, verbose_name="Data de processamento")
    
    def set_id_mercadopago(self, mp_id):
        """Define ID do Mercado Pago"""
        if mp_id:
            self.id_mercadopago = str(mp_id)
    
    def get_id_mercadopago(self):
        """Obtém ID do Mercado Pago"""
        return self.id_mercadopago
    
    def set_external_reference(self, ref):
        """Define referência externa"""
        if ref:
            self.external_reference = str(ref)
    
    def get_external_reference(self):
        """Obtém referência externa"""
        return self.external_reference
    
    def set_data_recebida(self, data):
        """Define dados recebidos"""
        if data:
            self.data_recebida = data if isinstance(data, dict) else {}
    
    def get_data_recebida(self):
        """Obtém dados recebidos"""
        return self.data_recebida
    
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
    """
    # Tokens do Mercado Pago (SEM CRIPTOGRAFIA)
    access_token = models.TextField(verbose_name="Access Token", default='')
    public_key = models.TextField(verbose_name="Public Key", default='')
    
    # Configurações de webhook
    webhook_url = models.URLField(verbose_name="URL do Webhook")
    webhook_secret = models.TextField(verbose_name="Secret do Webhook", default='')
    
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
        """Define access token"""
        if token:
            self.access_token = token
    
    def get_access_token(self):
        """Obtém access token"""
        return self.access_token
    
    def set_public_key(self, key):
        """Define public key"""
        if key:
            self.public_key = key
    
    def get_public_key(self):
        """Obtém public key"""
        return self.public_key
    
    def set_webhook_secret(self, secret):
        """Define webhook secret"""
        if secret:
            self.webhook_secret = secret
    
    def get_webhook_secret(self):
        """Obtém webhook secret"""
        return self.webhook_secret
    
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