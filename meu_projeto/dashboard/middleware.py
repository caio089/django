"""
Middleware para otimizar performance do dashboard
"""
import time
from django.core.cache import cache
from django.db import connection
from django.conf import settings


class DashboardPerformanceMiddleware:
    """
    Middleware para monitorar e otimizar performance do dashboard
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Monitorar tempo de resposta apenas para dashboard
        if '/dashboard/' in request.path:
            start_time = time.time()
            
            # Limitar conexões simultâneas para Supabase Session mode
            if hasattr(settings, 'SUPABASE_SESSION_MODE') and settings.SUPABASE_SESSION_MODE:
                if connection.queries:
                    # Se há muitas consultas, limpar cache para liberar recursos
                    if len(connection.queries) > 50:
                        cache.clear()
            
            response = self.get_response(request)
            
            # Log de performance (apenas em desenvolvimento)
            if settings.DEBUG:
                end_time = time.time()
                response_time = end_time - start_time
                if response_time > 2.0:  # Mais de 2 segundos
                    print(f"⚠️ SLOW RESPONSE: {request.path} took {response_time:.2f}s")
            
            return response
        
        return self.get_response(request)
