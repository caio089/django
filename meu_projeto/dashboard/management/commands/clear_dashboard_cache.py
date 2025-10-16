"""
Comando para limpar cache do dashboard manualmente
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Limpa o cache do dashboard'

    def handle(self, *args, **options):
        cache_keys = [
            'dashboard_stats',
            'dashboard_recent_users',
        ]
        
        for key in cache_keys:
            cache.delete(key)
        
        self.stdout.write(
            self.style.SUCCESS('Cache do dashboard limpo com sucesso!')
        )
