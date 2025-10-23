from django.urls import path
from . import views
from . import views_recuperacao

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login-google/', views.login_google_view, name='login_google'),
    path('selecionar-faixa/', views.selecionar_faixa_view, name='selecionar_faixa'),
    path('processar-login-google/', views.processar_login_google, name='processar_login_google'),
    path('register/', views.register_view, name='register'),
    path('teste-login/', views.teste_login_view, name='teste_login'),
    
    # URLs de recuperação de senha
    path('esqueci-senha/', views_recuperacao.esqueci_senha, name='esqueci_senha'),
    path('verificar-codigo/<str:email>/', views_recuperacao.verificar_codigo, name='verificar_codigo'),
    path('redefinir-senha/<str:email>/', views_recuperacao.redefinir_senha, name='redefinir_senha'),
]
