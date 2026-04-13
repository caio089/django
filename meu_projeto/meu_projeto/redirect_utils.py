"""Utilitários para redirecionar ao frontend React."""
from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import redirect, render


def serve_frontend_app(request):
    """Renderiza a SPA do React quando ela é servida pelo Django."""
    return render(request, 'index.html')


def _frontend_is_local_to_current_host(request):
    base = getattr(settings, 'FRONTEND_URL', '').strip()
    if not base or settings.DEBUG:
        return False

    parsed = urlparse(base if '://' in base else f'https://{base}')
    return parsed.netloc == request.get_host()


def redirect_to_frontend(path=''):
    """Redireciona para o frontend React. path deve começar com / (ex: /index, /quiz)."""
    base = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    path = path if path.startswith('/') else f'/{path}'
    return redirect(f'{base}{path}', permanent=False)


def frontend_route(request, path=''):
    """Serve a SPA localmente ou redireciona para um frontend externo."""
    if _frontend_is_local_to_current_host(request):
        return serve_frontend_app(request)
    return redirect_to_frontend(path)
