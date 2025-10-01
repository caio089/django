from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

class Command(BaseCommand):
    help = 'Debug do login'

    def handle(self, *args, **options):
        self.stdout.write('Debug do login...')
        
        # Criar cliente de teste
        client = Client()
        
        # Dados de teste
        email = 'ccamposs2007@gmail.com'
        senha = 'admin123'
        
        # Testar login via POST
        self.stdout.write(f'Testando login: {email} / {senha}')
        
        response = client.post('/login/', {
            'email': email,
            'senha': senha,
            'csrfmiddlewaretoken': 'test'
        })
        
        self.stdout.write(f'Status da resposta: {response.status_code}')
        self.stdout.write(f'Redirecionamento: {response.get("Location", "Nenhum")}')
        
        # Verificar se há erros no formulário
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                self.stdout.write(f'Erros no formulário: {form.errors}')
            else:
                self.stdout.write('Formulário sem erros')
        else:
            self.stdout.write('Contexto não disponível')
        
        # Testar autenticação manual
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'Usuário encontrado: {user.username}')
            
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=user.username, password=senha)
            if auth_user:
                self.stdout.write('Autenticação manual: SUCESSO')
            else:
                self.stdout.write('Autenticação manual: FALHOU')
                
        except User.DoesNotExist:
            self.stdout.write('Usuário não encontrado')
