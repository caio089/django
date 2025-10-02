from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Redefine a senha do usuário principal'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='ccamposs2007@gmail.com', help='Email do usuário')
        parser.add_argument('--senha', type=str, default='123456', help='Nova senha')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔑 REDEFININDO SENHA'))
        self.stdout.write('=' * 50)
        
        email = options['email']
        senha = options['senha']
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'Usuário encontrado: {user.username}')
            
            # Redefinir senha
            user.set_password(senha)
            user.save()
            
            self.stdout.write(f'✅ Senha redefinida para {email}')
            self.stdout.write(f'Nova senha: {senha}')
            
            # Testar a senha
            if user.check_password(senha):
                self.stdout.write('✅ Senha testada com sucesso')
            else:
                self.stdout.write('❌ Erro ao testar a senha')
                
        except User.DoesNotExist:
            self.stdout.write(f'❌ Usuário não encontrado: {email}')
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
        
        self.stdout.write('\n✅ Processo concluído!')
