from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Testa o login de usuários'

    def handle(self, *args, **options):
        self.stdout.write('Testando login de usuarios...')
        
        # Listar usuários
        users = User.objects.all()
        for user in users:
            self.stdout.write(f'Usuario: {user.username} | Email: {user.email} | Ativo: {user.is_active}')
        
        # Testar login com diferentes combinações
        test_cases = [
            ('ccamposs2007@gmail.com', 'admin123'),
            ('admin', 'admin123'),
            ('ccamposs2007@gmail.com', 'senha_errada'),
        ]
        
        for email, senha in test_cases:
            self.stdout.write(f'\nTestando: {email} / {senha}')
            
            # Buscar usuário por email
            try:
                user = User.objects.get(email=email)
                self.stdout.write(f'  Usuario encontrado: {user.username}')
                
                # Testar autenticação
                auth_user = authenticate(username=user.username, password=senha)
                if auth_user:
                    self.stdout.write(f'  Login: SUCESSO')
                else:
                    self.stdout.write(f'  Login: FALHOU')
                    
            except User.DoesNotExist:
                self.stdout.write(f'  Usuario nao encontrado por email')
                
                # Tentar por username
                try:
                    user = User.objects.get(username=email)
                    self.stdout.write(f'  Usuario encontrado por username: {user.username}')
                    
                    auth_user = authenticate(username=user.username, password=senha)
                    if auth_user:
                        self.stdout.write(f'  Login: SUCESSO')
                    else:
                        self.stdout.write(f'  Login: FALHOU')
                        
                except User.DoesNotExist:
                    self.stdout.write(f'  Usuario nao encontrado por username')

