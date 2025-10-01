from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria superusuário admin para o Render'

    def handle(self, *args, **options):
        self.stdout.write('Criando superusuario admin...')
        
        # Verificar se já existe
        if User.objects.filter(username='admin').exists():
            self.stdout.write('Usuario admin ja existe. Redefinindo senha...')
            user = User.objects.get(username='admin')
        else:
            self.stdout.write('Criando novo usuario admin...')
            user = User.objects.create_user(
                username='admin',
                email='admin@exemplo.com',
                password='admin123'
            )
        
        # Definir como superusuário
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password('admin123')
        user.save()
        
        self.stdout.write(self.style.SUCCESS('Superusuario admin criado/atualizado com sucesso!'))
        self.stdout.write('Credenciais:')
        self.stdout.write('  Username: admin')
        self.stdout.write('  Senha: admin123')
        self.stdout.write('  URL: /admin/')
        
        # Testar login
        from django.contrib.auth import authenticate
        test_user = authenticate(username='admin', password='admin123')
        if test_user:
            self.stdout.write(self.style.SUCCESS('Login testado com sucesso!'))
        else:
            self.stdout.write(self.style.ERROR('Erro no teste de login!'))
