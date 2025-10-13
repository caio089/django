from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),  # /dashboard/login/
    path('logout/', views.admin_logout, name='admin_logout'),  # /dashboard/logout/
    path('', views.dashboard_admin, name='dashboard_admin'),  # /dashboard/
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin_alt'),  # /dashboard/admin-dashboard/
    path('give-premium/', views.give_premium, name='give_premium'),
    path('remove-premium/', views.remove_premium, name='remove_premium'),
    path('delete-user/', views.delete_user, name='delete_user'),
]
