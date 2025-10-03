"""
Comando para testar URLs do sistema de pagamentos
"""
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Testa URLs do sistema de pagamentos'

    def handle(self, *args, **options):
        client = Client()
        
        # Testar URLs sem autenticação
        self.stdout.write('🔍 Testando URLs sem autenticação:')
        
        urls_to_test = [
            ('payments:planos', 'Página de planos'),
            ('payments:escolher_plano', 'Escolher plano (ID 1)', {'plano_id': 1}),
            ('payments:criar_pagamento', 'Criar pagamento (ID 1)', {'plano_id': 1}),
        ]
        
        for url_name, description, *args in urls_to_test:
            try:
                if args:
                    url = reverse(url_name, kwargs=args[0])
                else:
                    url = reverse(url_name)
                
                response = client.get(url)
                self.stdout.write(f'  ✅ {description}: {url} - Status: {response.status_code}')
                
                if response.status_code == 302:
                    self.stdout.write(f'    ↳ Redirecionando para: {response.url}')
                    
            except Exception as e:
                self.stdout.write(f'  ❌ {description}: {url} - Erro: {e}')
        
        # Testar com usuário logado
        self.stdout.write('\n🔍 Testando URLs com usuário logado:')
        
        try:
            user = User.objects.get(username='ccamposs2007@gmail.com')
            client.force_login(user)
            
            for url_name, description, *args in urls_to_test:
                try:
                    if args:
                        url = reverse(url_name, kwargs=args[0])
                    else:
                        url = reverse(url_name)
                    
                    response = client.get(url)
                    self.stdout.write(f'  ✅ {description}: {url} - Status: {response.status_code}')
                    
                    if response.status_code == 302:
                        self.stdout.write(f'    ↳ Redirecionando para: {response.url}')
                        
                except Exception as e:
                    self.stdout.write(f'  ❌ {description}: {url} - Erro: {e}')
                    
        except User.DoesNotExist:
            self.stdout.write('  ❌ Usuário ccamposs2007@gmail.com não encontrado')









