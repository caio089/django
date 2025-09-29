from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso'),
    path('verificar-niveis/', views.verificar_niveis_disponiveis, name='verificar_niveis'),
]