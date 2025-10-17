"""
Views para monitoramento do Supabase
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from meu_projeto.supabase_keepalive import get_supabase_status, start_supabase_keepalive, stop_supabase_keepalive
from django.db import connection
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def supabase_status(request):
    """Endpoint para verificar status do Supabase"""
    try:
        # Obter status do keep-alive
        status = get_supabase_status()
        
        # Testar conexão atual
        connection_ok = False
        response_time = None
        
        try:
            import time
            start_time = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            response_time = time.time() - start_time
            connection_ok = result is not None
        except Exception as e:
            logger.warning(f"Erro ao testar conexão: {e}")
        
        return JsonResponse({
            'success': True,
            'data': {
                'keep_alive': status['keep_alive'],
                'connection_health': status['connection_health'],
                'current_connection': {
                    'active': connection_ok,
                    'response_time': response_time
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no endpoint de status: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def start_keepalive(request):
    """Endpoint para iniciar keep-alive manualmente"""
    try:
        start_supabase_keepalive()
        return JsonResponse({
            'success': True,
            'message': 'Keep-alive iniciado com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao iniciar keep-alive: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def stop_keepalive(request):
    """Endpoint para parar keep-alive"""
    try:
        stop_supabase_keepalive()
        return JsonResponse({
            'success': True,
            'message': 'Keep-alive parado com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao parar keep-alive: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def test_connection(request):
    """Endpoint para testar conexão com Supabase"""
    try:
        import time
        start_time = time.time()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test, NOW() as timestamp")
            result = cursor.fetchone()
        
        response_time = time.time() - start_time
        
        return JsonResponse({
            'success': True,
            'data': {
                'connection_active': True,
                'response_time': round(response_time, 3),
                'timestamp': str(result[1]) if result else None
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no teste de conexão: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'connection_active': False
        }, status=500)
