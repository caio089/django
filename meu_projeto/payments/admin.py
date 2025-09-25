from django.contrib import admin
from .models import (
    PlanoPremium, Assinatura, Pagamento, WebhookEvent, ConfiguracaoPagamento
)

@admin.register(PlanoPremium)
class PlanoPremiumAdmin(admin.ModelAdmin):
    """
    Administração dos planos premium
    """
    list_display = ['nome', 'preco', 'duracao_dias', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    ordering = ['preco']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'preco', 'duracao_dias')
        }),
        ('Recursos', {
            'fields': ('acesso_ilimitado_quiz', 'relatorios_detalhados', 'suporte_prioritario')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    """
    Administração das assinaturas dos usuários
    """
    list_display = ['usuario', 'plano', 'status', 'data_inicio', 'data_vencimento']
    list_filter = ['status', 'plano', 'data_inicio', 'ativo']
    search_fields = ['usuario__username', 'usuario__email', 'subscription_id']
    readonly_fields = ['external_reference', 'data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Usuário e Plano', {
            'fields': ('usuario', 'plano')
        }),
        ('Status', {
            'fields': ('status', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_vencimento', 'data_cancelamento')
        }),
        ('Identificadores Mercado Pago', {
            'fields': ('subscription_id', 'external_reference')
        }),
        ('Timestamps', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    """
    Administração dos pagamentos (DADOS CRIPTOGRAFADOS)
    """
    list_display = ['usuario', 'valor', 'status', 'tipo', 'data_pagamento', 'get_payment_id_display']
    list_filter = ['status', 'tipo', 'data_criacao', 'data_pagamento']
    search_fields = ['usuario__username', 'external_reference']
    readonly_fields = ['external_reference', 'data_criacao', 'data_atualizacao', 'get_payment_id_display']
    
    def get_payment_id_display(self, obj):
        """Exibe ID do pagamento de forma segura"""
        payment_id = obj.get_payment_id()
        if payment_id:
            return f"{payment_id[:8]}...{payment_id[-4:]}"
        return "N/A"
    get_payment_id_display.short_description = "Payment ID"
    
    fieldsets = (
        ('Usuário e Assinatura', {
            'fields': ('usuario', 'assinatura')
        }),
        ('Informações do Pagamento', {
            'fields': ('valor', 'status', 'tipo', 'descricao', 'metodo_pagamento')
        }),
        ('Identificadores Mercado Pago (Criptografados)', {
            'fields': ('get_payment_id_display', 'external_reference'),
            'description': 'Dados sensíveis estão criptografados no banco'
        }),
        ('Dados do Pagador (Criptografados)', {
            'fields': ('payer_email_encrypted', 'payer_name_encrypted', 'payer_phone_encrypted', 'payer_document_encrypted'),
            'classes': ('collapse',),
            'description': 'Dados pessoais criptografados - use métodos get_* para acessar'
        }),
        ('Dados de Auditoria', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_pagamento', 'data_criacao', 'data_atualizacao')
        }),
    )

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    """
    Administração dos eventos de webhook (DADOS CRIPTOGRAFADOS)
    """
    list_display = ['tipo', 'action', 'get_id_mercadopago_display', 'processado', 'data_recebimento']
    list_filter = ['tipo', 'action', 'processado', 'data_recebimento']
    search_fields = ['external_reference']
    readonly_fields = ['data_recebimento', 'data_processamento', 'get_id_mercadopago_display']
    
    def get_id_mercadopago_display(self, obj):
        """Exibe ID do Mercado Pago de forma segura"""
        mp_id = obj.get_id_mercadopago()
        if mp_id:
            return f"{mp_id[:8]}...{mp_id[-4:]}"
        return "N/A"
    get_id_mercadopago_display.short_description = "ID Mercado Pago"
    
    fieldsets = (
        ('Evento', {
            'fields': ('tipo', 'action', 'get_id_mercadopago_display')
        }),
        ('Processamento', {
            'fields': ('processado', 'erro_processamento', 'data_processamento')
        }),
        ('Dados de Segurança', {
            'fields': ('ip_address', 'signature'),
            'classes': ('collapse',)
        }),
        ('Dados Criptografados', {
            'fields': ('id_mercadopago_encrypted', 'external_reference_encrypted', 'data_recebida_encrypted'),
            'classes': ('collapse',),
            'description': 'Dados sensíveis criptografados - use métodos get_* para acessar'
        }),
        ('Timestamp', {
            'fields': ('data_recebimento',)
        }),
    )

@admin.register(ConfiguracaoPagamento)
class ConfiguracaoPagamentoAdmin(admin.ModelAdmin):
    """
    Administração das configurações de pagamento (TOKENS CRIPTOGRAFADOS)
    """
    list_display = ['ambiente', 'ativo', 'usage_count', 'last_used', 'data_atualizacao']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'usage_count', 'last_used']
    
    fieldsets = (
        ('Configurações Mercado Pago (Criptografadas)', {
            'fields': ('access_token_encrypted', 'public_key_encrypted'),
            'description': 'Tokens criptografados - use métodos get_* para acessar'
        }),
        ('Webhook', {
            'fields': ('webhook_url', 'webhook_secret_encrypted'),
            'description': 'Secret do webhook está criptografado'
        }),
        ('Ambiente e Status', {
            'fields': ('ambiente', 'ativo')
        }),
        ('Estatísticas de Uso', {
            'fields': ('usage_count', 'last_used'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
