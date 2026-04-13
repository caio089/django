"""
Middleware personalizado para lidar com redirecionamentos de domínio
"""
from django.http import HttpResponsePermanentRedirect


class WWWRedirectMiddleware:
    """
    Middleware para redirecionar aliases do domínio para dojoon.com.br.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Usa o host bruto para evitar DisallowedHost antes do redirecionamento.
        raw_host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST', '')
        host = raw_host.split(':', 1)[0].lower().strip()

        redirect_hosts = {
            'www.dojoon.com.br',
            'www.dojoon.com',
            'dojoon.com',
        }

        if host in redirect_hosts:
            # Preservar o protocolo (http/https)
            protocol = 'https' if request.is_secure() else 'http'
            # Preservar a URL completa
            redirect_url = f"{protocol}://dojoon.com.br{request.get_full_path()}"
            return HttpResponsePermanentRedirect(redirect_url)
        
        response = self.get_response(request)
        return response
