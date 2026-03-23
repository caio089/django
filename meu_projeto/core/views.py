from django.contrib.auth import logout
from django.shortcuts import redirect
from meu_projeto.redirect_utils import redirect_to_frontend

def index(request):
    """Redireciona para o React (Dashboard em /index)"""
    return redirect_to_frontend('/index')

def logout_view(request):
    logout(request)
    return redirect_to_frontend('/login')