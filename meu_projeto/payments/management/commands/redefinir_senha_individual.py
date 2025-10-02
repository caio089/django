from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Redefine senha de um usuário específico'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Email do usuário')
        parser.add_argument('--senha', type=str, required=True, help='Nova senha')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔑 REDEFININDO SENHA INDIVIDUAL'))
        self.stdout.write('=' * 50)
        
        email = options['email']
        senha = options['senha']
        
        try:
            user = User.objects.get(email__iexact=email)
            self.stdout.write(f'Usuário encontrado: {user.email}')
            
            # Redefinir senha
            user.set_password(senha)
            user.is_active = True
            user.save()
            
            self.stdout.write(f'✅ Senha redefinida para {email}')
            self.stdout.write(f'Nova senha: {senha}')
            
            # Testar login
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=user.username, password=senha)
            
            if auth_user:
                self.stdout.write('✅ Login testado com sucesso!')
            else:
                self.stdout.write('❌ Erro ao testar login')
                
        except User.DoesNotExist:
            self.stdout.write(f'❌ Usuário não encontrado: {email}')
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
        
        self.stdout.write('\n✅ Processo concluído!')
