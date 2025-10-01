"""
Comando para debug de redirecionamento
"""
from django.core.management.base import BaseCommand
from django.urls import reverse
from payments.models import PlanoPremium

class Command(BaseCommand):
    help = 'Debug de redirecionamento'

    def handle(self, *args, **options):
        # Verificar se existem planos
        planos = PlanoPremium.objects.filter(ativo=True)
        self.stdout.write(f'Total de planos ativos: {planos.count()}')
        
        for plano in planos:
            self.stdout.write(f'\n📋 Plano: {plano.nome} (ID: {plano.id})')
            
            # Testar URL de criar pagamento
            try:
                url = reverse('payments:criar_pagamento', kwargs={'plano_id': plano.id})
                self.stdout.write(f'  ✅ URL: {url}')
            except Exception as e:
                self.stdout.write(f'  ❌ Erro na URL: {e}')
            
            # Testar URL de escolher plano
            try:
                url = reverse('payments:escolher_plano', kwargs={'plano_id': plano.id})
                self.stdout.write(f'  ✅ URL escolher: {url}')
            except Exception as e:
                self.stdout.write(f'  ❌ Erro na URL escolher: {e}')
        
        # Testar URL de planos
        try:
            url = reverse('payments:planos')
            self.stdout.write(f'\n📋 URL de planos: {url}')
        except Exception as e:
            self.stdout.write(f'❌ Erro na URL de planos: {e}')






