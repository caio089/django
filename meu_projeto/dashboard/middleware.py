"""
Middleware para monitorar performance do dashboard
"""
import time
from django.conf import settings


class DashboardPerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG or '/dashboard/' not in request.path:
            return self.get_response(request)

        start_time = time.time()
        response = self.get_response(request)
        elapsed = time.time() - start_time
        if elapsed > 2.0:
            print(f"SLOW RESPONSE: {request.path} took {elapsed:.2f}s")
        return response
