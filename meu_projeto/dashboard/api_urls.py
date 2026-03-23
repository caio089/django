from django.urls import path
from . import api_views

urlpatterns = [
    path('me/', api_views.api_admin_me),
    path('login/', api_views.api_admin_login),
    path('logout/', api_views.api_admin_logout),
    path('dashboard/', api_views.api_admin_dashboard),
    path('give-premium/', api_views.api_admin_give_premium),
    path('remove-premium/', api_views.api_admin_remove_premium),
    path('delete-user/', api_views.api_admin_delete_user),
    path('refresh-cache/', api_views.api_admin_refresh_cache),
    path('ativar-manual/', api_views.api_admin_ativar_manual),
    path('corrigir-assinaturas/', api_views.api_admin_corrigir_assinaturas),
    path('user/<int:user_id>/', api_views.api_admin_user_detail),
]
