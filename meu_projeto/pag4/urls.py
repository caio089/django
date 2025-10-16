from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina4, name='pagina4'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso_pag4'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso_pag4'),
]