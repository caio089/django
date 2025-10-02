from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from home.forms import EmailLoginForm

class Command(BaseCommand):
    help = 'Testa login com todos os emails cadastrados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📧 TESTANDO LOGIN COM TODOS OS EMAILS'))
        self.stdout.write('=' * 60)
        
        # Listar todos os usuários
        users = User.objects.all()
        self.stdout.write(f'\n👥 USUÁRIOS CADASTRADOS ({users.count()}):')
        
        for user in users:
            self.stdout.write(f'  - {user.email} (ativo: {user.is_active})')
        
        # Testar login com senhas comuns
        senhas_teste = ['123456', '123', 'admin', 'password', 'senha']
        
        self.stdout.write(f'\n🔐 TESTANDO LOGIN:')
        
        for user in users:
            self.stdout.write(f'\n📧 Testando: {user.email}')
            self.stdout.write(f'   Username: {user.username}')
            self.stdout.write(f'   Ativo: {user.is_active}')
            self.stdout.write(f'   Tem senha: {user.has_usable_password()}')
            
            # Testar autenticação direta
            for senha in senhas_teste:
                auth_user = authenticate(username=user.username, password=senha)
                if auth_user:
                    self.stdout.write(f'   ✅ Senha correta: {senha}')
                    break
            else:
                self.stdout.write(f'   ❌ Nenhuma senha funcionou')
            
            # Testar formulário
            for senha in senhas_teste:
                form_data = {'email': user.email, 'senha': senha}
                form = EmailLoginForm(data=form_data)
                
                if form.is_valid():
                    self.stdout.write(f'   ✅ Formulário válido com senha: {senha}')
                    break
            else:
                self.stdout.write(f'   ❌ Formulário inválido com todas as senhas')
                # Mostrar erros do formulário
                for field, errors in form.errors.items():
                    for error in errors:
                        self.stdout.write(f'      - {field}: {error}')
        
        # Testar emails que não existem
        self.stdout.write(f'\n❌ TESTANDO EMAILS INEXISTENTES:')
        emails_inexistentes = ['teste@teste.com', 'inexistente@email.com']
        
        for email in emails_inexistentes:
            form_data = {'email': email, 'senha': '123456'}
            form = EmailLoginForm(data=form_data)
            
            if form.is_valid():
                self.stdout.write(f'   ✅ {email}: Formulário válido (inesperado)')
            else:
                self.stdout.write(f'   ❌ {email}: {form.errors.get("__all__", ["Erro desconhecido"])[0]}')
        
        self.stdout.write('\n✅ Teste de emails concluído!')
