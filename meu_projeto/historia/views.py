from django.shortcuts import redirect
from meu_projeto.redirect_utils import redirect_to_frontend

def historia(request):
    """Redireciona para o React em /historia"""
    return redirect_to_frontend('/historia')  

