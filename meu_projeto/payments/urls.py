from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Páginas de planos e pagamento
    path('planos/', views.listar_planos, name='planos'),
    path('plano/<int:plano_id>/', views.escolher_plano, name='escolher_plano'),
    path('criar-pagamento/<int:plano_id>/', views.criar_pagamento, name='criar_pagamento'),
    path('checkout/<int:payment_id>/', views.checkout_pagamento, name='checkout_pagamento'),
    path('sucesso/', views.pagamento_sucesso, name='sucesso'),
    path('falha/', views.pagamento_falha, name='falha'),
    path('pendente/', views.pagamento_pendente, name='pendente'),
    path('assinaturas/', views.minhas_assinaturas, name='assinaturas'),
    
    # API para verificar status
    path('verificar-status/<int:payment_id>/', views.verificar_status_pagamento, name='verificar_status'),
    path('verificar-assinatura/', views.verificar_assinatura, name='verificar_assinatura'),
    
    # PIX direto
    path('gerar-pix/<int:payment_id>/', views.gerar_pix_direto, name='gerar_pix_direto'),
    path('testar-pix/', views.testar_pix, name='testar_pix'),
    path('verificar-pagamento/<int:payment_id>/', views.verificar_pagamento_manual, name='verificar_pagamento_manual'),
    
    # Webhook do Mercado Pago
    path('webhook/', views.webhook_mercadopago, name='webhook'),
    
    # Cancelar assinatura
    path('cancelar-assinatura/', views.cancelar_assinatura, name='cancelar_assinatura'),
]
