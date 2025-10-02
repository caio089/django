from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from home.forms import EmailLoginForm
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Diagnóstico específico do problema de login'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email específico para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 DIAGNÓSTICO DE LOGIN'))
        self.stdout.write('=' * 50)
        
        email_teste = options.get('email')
        
        if email_teste:
            self.testar_email_especifico(email_teste)
        else:
            self.testar_todos_usuarios()
    
    def testar_email_especifico(self, email):
        self.stdout.write(f'\n📧 TESTANDO EMAIL ESPECÍFICO: {email}')
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'✅ Usuário encontrado: {user.username}')
            self.stdout.write(f'   - Ativo: {user.is_active}')
            self.stdout.write(f'   - Staff: {user.is_staff}')
            self.stdout.write(f'   - Superuser: {user.is_superuser}')
            self.stdout.write(f'   - Tem senha: {user.has_usable_password()}')
            
            # Testar senhas comuns
            senhas = ['123456', '123', 'admin', 'password', 'senha']
            
            for senha in senhas:
                self.stdout.write(f'\n🔐 Testando senha: {senha}')
                
                # Teste 1: Autenticação direta
                auth_user = authenticate(username=user.username, password=senha)
                self.stdout.write(f'   Autenticação direta: {"✅" if auth_user else "❌"}')
                
                # Teste 2: Formulário
                form_data = {'email': email, 'senha': senha}
                form = EmailLoginForm(data=form_data)
                
                if form.is_valid():
                    self.stdout.write(f'   Formulário: ✅ Válido')
                    self.stdout.write(f'   Usuário retornado: {form.cleaned_data.get("user")}')
                    break
                else:
                    self.stdout.write(f'   Formulário: ❌ Inválido')
                    for field, errors in form.errors.items():
                        for error in errors:
                            self.stdout.write(f'      - {field}: {error}')
            
        except User.DoesNotExist:
            self.stdout.write(f'❌ Usuário não encontrado: {email}')
    
    def testar_todos_usuarios(self):
        self.stdout.write(f'\n👥 TESTANDO TODOS OS USUÁRIOS:')
        
        users = User.objects.all()
        self.stdout.write(f'Total de usuários: {users.count()}')
        
        for user in users:
            self.stdout.write(f'\n📧 {user.email}:')
            self.stdout.write(f'   - Ativo: {user.is_active}')
            self.stdout.write(f'   - Tem senha: {user.has_usable_password()}')
            
            # Testar com senha padrão
            form_data = {'email': user.email, 'senha': '123456'}
            form = EmailLoginForm(data=form_data)
            
            if form.is_valid():
                self.stdout.write(f'   - Login: ✅ Funciona com 123456')
            else:
                self.stdout.write(f'   - Login: ❌ Não funciona')
                for field, errors in form.errors.items():
                    for error in errors:
                        self.stdout.write(f'      - {field}: {error}')
        
        self.stdout.write('\n✅ Diagnóstico concluído!')
