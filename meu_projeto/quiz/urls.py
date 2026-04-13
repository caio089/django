from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso'),
    path('verificar-niveis/', views.verificar_niveis_disponiveis, name='verificar_niveis'),
    path('reiniciar-quiz/', views.reiniciar_quiz, name='reiniciar_quiz'),
    path('api/ranking/', views.api_ranking, name='api_ranking'),
    path('api/submit/', views.api_submit, name='api_submit'),
    path('api/start-attempt/', views.api_start_attempt, name='api_start_attempt'),
    path('api/submit-attempt/', views.api_submit_attempt, name='api_submit_attempt'),
]