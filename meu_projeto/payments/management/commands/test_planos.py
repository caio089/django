"""
Comando para testar acesso à página de planos
"""
from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

class Command(BaseCommand):
    help = 'Testa acesso à página de planos'

    def handle(self, *args, **options):
        client = Client()
        
        # Testar sem autenticação
        self.stdout.write('🔍 Testando sem autenticação:')
        response = client.get('/payments/planos/')
        self.stdout.write(f'  Status: {response.status_code}')
        if response.status_code == 302:
            self.stdout.write(f'  Redirecionando para: {response.url}')
        
        # Testar com usuário logado
        self.stdout.write('\n🔍 Testando com usuário logado:')
        try:
            user = User.objects.get(username='ccamposs2007@gmail.com')
            client.force_login(user)
            
            response = client.get('/payments/planos/')
            self.stdout.write(f'  Status: {response.status_code}')
            
            if response.status_code == 200:
                self.stdout.write('  ✅ Página carregada com sucesso!')
                # Verificar se contém informações de assinatura ativa
                content = response.content.decode('utf-8')
                if 'Você já tem acesso premium' in content:
                    self.stdout.write('  ✅ Usuário tem assinatura ativa!')
                else:
                    self.stdout.write('  ❌ Usuário não tem assinatura ativa')
            elif response.status_code == 302:
                self.stdout.write(f'  Redirecionando para: {response.url}')
            else:
                self.stdout.write(f'  ❌ Erro: {response.status_code}')
                
        except User.DoesNotExist:
            self.stdout.write('  ❌ Usuário não encontrado')









