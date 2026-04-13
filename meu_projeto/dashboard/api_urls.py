from django.urls import path
from . import api_views

urlpatterns = [
    path('me/', api_views.api_admin_me),
    path('login/', api_views.api_admin_login),
    path('logout/', api_views.api_admin_logout),
    path('dashboard/', api_views.api_admin_dashboard),
    path('finance-settings/', api_views.api_admin_finance_settings),
    path('finance-reset-revenue/', api_views.api_admin_reset_total_revenue),
    path('give-premium/', api_views.api_admin_give_premium),
    path('remove-premium/', api_views.api_admin_remove_premium),
    path('delete-user/', api_views.api_admin_delete_user),
    path('refresh-cache/', api_views.api_admin_refresh_cache),
    path('ativar-manual/', api_views.api_admin_ativar_manual),
    path('corrigir-assinaturas/', api_views.api_admin_corrigir_assinaturas),
    path('send-marketing-email/', api_views.api_admin_send_marketing_email),
    path('user/<int:user_id>/', api_views.api_admin_user_detail),
    path('payments/', api_views.api_admin_payments),
    path('webhooks/', api_views.api_admin_webhooks),
    path('reprocess-payment/', api_views.api_admin_reprocess_payment),
]
