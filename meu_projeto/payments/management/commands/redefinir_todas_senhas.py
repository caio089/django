from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Redefine senhas de todos os usuários para uma senha padrão'

    def add_arguments(self, parser):
        parser.add_argument('--senha', type=str, default='123456', help='Senha padrão para todos os usuários')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔑 REDEFININDO TODAS AS SENHAS'))
        self.stdout.write('=' * 50)
        
        senha = options['senha']
        
        users = User.objects.all()
        self.stdout.write(f'Usuários encontrados: {users.count()}')
        
        for user in users:
            try:
                user.set_password(senha)
                user.is_active = True
                user.save()
                self.stdout.write(f'✅ {user.email} - Senha redefinida')
            except Exception as e:
                self.stdout.write(f'❌ {user.email} - Erro: {e}')
        
        self.stdout.write(f'\n🎯 Todas as senhas foram redefinidas para: {senha}')
        self.stdout.write('✅ Agora todos os usuários podem fazer login!')
