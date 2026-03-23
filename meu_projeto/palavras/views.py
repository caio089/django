from django.shortcuts import redirect
from meu_projeto.redirect_utils import redirect_to_frontend

def palavras(request):
    """Redireciona para o React em /palavras"""
    return redirect_to_frontend('/palavras')