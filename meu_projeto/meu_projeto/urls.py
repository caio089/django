"""
URL configuration for meu_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static
from dashboard import views as dashboard_views
from meu_projeto import views_supabase
from payments import views as payments_views

def redirect_to_admin_panel(request):
    """Redireciona para o painel admin no frontend React."""
    base = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    return redirect(f'{base}/admin-panel', permanent=False)

urlpatterns = [
    path('admin/', redirect_to_admin_panel),
    path('admin-panel/', redirect_to_admin_panel),
    path('django-admin/', admin.site.urls),
    path('', include('home.urls')),
    path('index/', include('core.urls')),
    path('pagina1/', include('pag1.urls')),
    path('pagina2/', include('pag2.urls')),
    path('pagina3/', include('pag3.urls')),
    path('pagina4/', include('pag4.urls')),
    path('pagina5/', include('pag5.urls')),
    path('pagina6/', include('pag6.urls')),
    path('pagina7/', include('pag7.urls')),
    path('ukemis/', include('ukemis.urls')),
    path('quiz/', include('quiz.urls')),
    path('historia/', include('historia.urls')),
    path('palavras/', include('palavras.urls')),  
    path('regras/', include('regras.urls')),
    path('payments/', include('payments.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/admin/', include('dashboard.api_urls')),
    path('admin-dashboard/', dashboard_views.dashboard_admin, name='admin_dashboard_direct'),  # Atalho direto
    
    # API de pagamentos para o frontend React (mesmo prefixo /api do proxy)
    path('api/payments/plano/<int:plano_id>/', payments_views.api_plano_detail, name='api_payments_plano_detail'),
    path('api/payments/criar-pagamento/<int:plano_id>/', payments_views.criar_pagamento, name='api_payments_criar'),
    path('api/payments/gerar-pix/<int:payment_id>/', payments_views.gerar_pix_direto, name='api_payments_gerar_pix'),
    path('api/payments/checkout-redirect/<int:payment_id>/', payments_views.api_checkout_redirect, name='api_payments_checkout_redirect'),
    path('api/payments/verificar-status/<int:payment_id>/', payments_views.verificar_status_pagamento, name='api_payments_verificar_status'),
    # Endpoints de monitoramento do Supabase
    path('api/supabase/status/', views_supabase.supabase_status, name='supabase_status'),
    path('api/supabase/start/', views_supabase.start_keepalive, name='supabase_start'),
    path('api/supabase/stop/', views_supabase.stop_keepalive, name='supabase_stop'),
    path('api/supabase/test/', views_supabase.test_connection, name='supabase_test'),
]

# Configuração para servir arquivos estáticos durante o desenvolvimento
# Esta configuração permite que o Django sirva arquivos estáticos (CSS, JS, imagens)
# diretamente durante o desenvolvimento local
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

