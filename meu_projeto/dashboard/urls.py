from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('give-premium/', views.give_premium, name='give_premium'),
]
