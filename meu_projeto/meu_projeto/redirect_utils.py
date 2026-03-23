"""Utilitários para redirecionar ao frontend React."""
from django.shortcuts import redirect
from django.conf import settings


def redirect_to_frontend(path=''):
    """Redireciona para o frontend React. path deve começar com / (ex: /index, /quiz)."""
    base = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    path = path if path.startswith('/') else f'/{path}'
    return redirect(f'{base}{path}', permanent=False)
