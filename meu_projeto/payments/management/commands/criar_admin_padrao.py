from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile

class Command(BaseCommand):
    help = 'Cria um usuário admin padrão após limpeza do banco'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='admin@dojo.com', help='Email do admin')
        parser.add_argument('--senha', type=str, default='admin123', help='Senha do admin')
        parser.add_argument('--nome', type=str, default='Administrador', help='Nome do admin')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('👤 CRIANDO USUÁRIO ADMIN PADRÃO'))
        self.stdout.write('=' * 50)
        
        email = options['email']
        senha = options['senha']
        nome = options['nome']
        
        # Verificar se já existe usuário admin
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('⚠️  Já existe um usuário admin no sistema')
            return
        
        try:
            # Criar usuário admin
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=senha,
                first_name=nome,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write(f'✅ Usuário admin criado:')
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Senha: {senha}')
            self.stdout.write(f'   Nome: {nome}')
            
            # Criar perfil
            profile = Profile.objects.create(
                user=user,
                nome=nome,
                idade=30,
                faixa='preta'
            )
            
            self.stdout.write(f'✅ Perfil criado para o admin')
            
            # Testar login
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=user.username, password=senha)
            
            if auth_user:
                self.stdout.write('✅ Login do admin testado com sucesso!')
            else:
                self.stdout.write('❌ Erro ao testar login do admin')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao criar admin: {e}')
            return
        
        self.stdout.write(f'\n🎯 ADMIN CRIADO COM SUCESSO!')
        self.stdout.write(f'   Agora você pode fazer login com:')
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Senha: {senha}')
        
        self.stdout.write('\n✅ Script concluído!')
