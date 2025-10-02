from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from home.forms import EmailLoginForm
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Testa o processo de login'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email para testar')
        parser.add_argument('--senha', type=str, help='Senha para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔐 TESTANDO PROCESSO DE LOGIN'))
        self.stdout.write('=' * 50)
        
        email = options.get('email') or 'ccamposs2007@gmail.com'
        senha = options.get('senha') or '123456'
        
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Senha: {"*" * len(senha)}')
        
        # 1. Verificar se usuário existe
        self.stdout.write('\n1️⃣ VERIFICANDO USUÁRIO:')
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'✅ Usuário encontrado: {user.username}')
            self.stdout.write(f'   - Ativo: {user.is_active}')
            self.stdout.write(f'   - Staff: {user.is_staff}')
            self.stdout.write(f'   - Superuser: {user.is_superuser}')
            self.stdout.write(f'   - Tem senha: {user.has_usable_password()}')
        except User.DoesNotExist:
            self.stdout.write(f'❌ Usuário não encontrado: {email}')
            return
        
        # 2. Testar autenticação direta
        self.stdout.write('\n2️⃣ TESTANDO AUTENTICAÇÃO DIRETA:')
        auth_user = authenticate(username=user.username, password=senha)
        if auth_user:
            self.stdout.write('✅ Autenticação direta funcionou')
        else:
            self.stdout.write('❌ Autenticação direta falhou')
        
        # 3. Testar formulário
        self.stdout.write('\n3️⃣ TESTANDO FORMULÁRIO:')
        form_data = {'email': email, 'senha': senha}
        form = EmailLoginForm(data=form_data)
        
        if form.is_valid():
            self.stdout.write('✅ Formulário válido')
            self.stdout.write(f'   - Usuário: {form.cleaned_data.get("user")}')
        else:
            self.stdout.write('❌ Formulário inválido')
            for field, errors in form.errors.items():
                for error in errors:
                    self.stdout.write(f'   - {field}: {error}')
        
        # 4. Verificar senha
        self.stdout.write('\n4️⃣ VERIFICANDO SENHA:')
        if user.check_password(senha):
            self.stdout.write('✅ Senha correta')
        else:
            self.stdout.write('❌ Senha incorreta')
        
        # 5. Listar todos os usuários
        self.stdout.write('\n5️⃣ TODOS OS USUÁRIOS:')
        for u in User.objects.all():
            self.stdout.write(f'   - {u.email} (ativo: {u.is_active})')
        
        self.stdout.write('\n✅ Teste de login concluído!')
