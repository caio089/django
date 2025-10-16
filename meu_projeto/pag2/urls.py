from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina2, name='pagina2'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar_progresso_pag2'),
    path('carregar-progresso/', views.carregar_progresso, name='carregar_progresso_pag2'),
]