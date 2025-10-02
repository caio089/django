from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from home.models import Profile
from home.forms import EmailLoginForm
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Corrige login para todos os usuários existentes'

    def add_arguments(self, parser):
        parser.add_argument('--senha', type=str, default='123456', help='Senha padrão para todos os usuários')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 CORRIGINDO LOGIN PARA USUÁRIOS EXISTENTES'))
        self.stdout.write('=' * 60)
        
        senha = options['senha']
        
        # 1. LISTAR TODOS OS USUÁRIOS
        users = User.objects.all()
        self.stdout.write(f'\n👥 USUÁRIOS EXISTENTES ({users.count()}):')
        
        for user in users:
            self.stdout.write(f'  - {user.email} (ativo: {user.is_active})')
        
        # 2. CORRIGIR CADA USUÁRIO
        self.stdout.write(f'\n🔧 CORRIGINDO USUÁRIOS:')
        
        for user in users:
            self.stdout.write(f'\n📧 Processando: {user.email}')
            
            # Ativar usuário se estiver inativo
            if not user.is_active:
                user.is_active = True
                self.stdout.write('   ✅ Usuário ativado')
            
            # Redefinir senha
            user.set_password(senha)
            user.save()
            self.stdout.write('   ✅ Senha redefinida')
            
            # Verificar/criar perfil
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write('   ✅ Perfil já existe')
            except Profile.DoesNotExist:
                profile = Profile.objects.create(
                    user=user,
                    nome=user.first_name or user.email.split('@')[0],
                    idade=25,
                    faixa='branca'
                )
                self.stdout.write('   ✅ Perfil criado')
            
            # Testar login
            self.testar_login_usuario(user.email, senha)
        
        # 3. TESTE GERAL
        self.stdout.write(f'\n🧪 TESTE GERAL:')
        self.testar_todos_usuarios(senha)
        
        self.stdout.write(f'\n✅ CORREÇÃO CONCLUÍDA!')
        self.stdout.write(f'🎯 Todos os usuários podem fazer login com senha: {senha}')
    
    def testar_login_usuario(self, email, senha):
        """Testa login de um usuário específico"""
        try:
            # Teste 1: Autenticação direta
            user = User.objects.get(email=email)
            auth_user = authenticate(username=user.username, password=senha)
            
            if auth_user:
                self.stdout.write('   ✅ Autenticação direta: OK')
            else:
                self.stdout.write('   ❌ Autenticação direta: FALHOU')
                return False
            
            # Teste 2: Formulário
            form_data = {'email': email, 'senha': senha}
            form = EmailLoginForm(data=form_data)
            
            if form.is_valid():
                self.stdout.write('   ✅ Formulário: OK')
                return True
            else:
                self.stdout.write('   ❌ Formulário: FALHOU')
                for field, errors in form.errors.items():
                    for error in errors:
                        self.stdout.write(f'      - {field}: {error}')
                return False
                
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
            return False
    
    def testar_todos_usuarios(self, senha):
        """Testa login de todos os usuários"""
        users = User.objects.all()
        sucessos = 0
        falhas = 0
        
        for user in users:
            if self.testar_login_usuario(user.email, senha):
                sucessos += 1
            else:
                falhas += 1
        
        self.stdout.write(f'\n📊 RESULTADO:')
        self.stdout.write(f'   ✅ Sucessos: {sucessos}')
        self.stdout.write(f'   ❌ Falhas: {falhas}')
        
        if falhas == 0:
            self.stdout.write('   🎉 TODOS OS USUÁRIOS FUNCIONAM!')
        else:
            self.stdout.write('   ⚠️ Alguns usuários ainda têm problemas')
