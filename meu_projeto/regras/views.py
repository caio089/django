from django.shortcuts import redirect
from meu_projeto.redirect_utils import redirect_to_frontend

def regras(request):
    """Redireciona para o React em /regras"""
    return redirect_to_frontend('/regras')