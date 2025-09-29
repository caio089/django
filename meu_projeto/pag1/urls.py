from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina1, name='pagina1'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso'),
]