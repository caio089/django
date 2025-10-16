from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina7, name='pagina7'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso_pag7'),
    path('carregar_progresso/', views.carregar_progresso, name='carregar_progresso_pag7'),
]