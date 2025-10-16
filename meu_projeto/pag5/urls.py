from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina5, name='pagina5'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso_pag5'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso_pag5'),
]