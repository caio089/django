"""
Middleware personalizado para lidar com redirecionamentos de domínio
"""
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class WWWRedirectMiddleware:
    """
    Middleware para redirecionar www.dojoon.com.br para dojoon.com.br
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se é www.dojoon.com.br e redirecionar para dojoon.com.br
        host = request.get_host().lower()
        
        # Lista de hosts que devem redirecionar para o domínio principal
        www_hosts = ['www.dojoon.com.br']
        
        if host in www_hosts:
            # Preservar o protocolo (http/https)
            protocol = 'https' if request.is_secure() else 'http'
            # Preservar a URL completa
            redirect_url = f"{protocol}://dojoon.com.br{request.get_full_path()}"
            return HttpResponsePermanentRedirect(redirect_url)
        
        response = self.get_response(request)
        return response
