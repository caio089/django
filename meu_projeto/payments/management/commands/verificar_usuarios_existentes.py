from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from home.models import Profile
from home.forms import EmailLoginForm
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verifica e corrige apenas problemas reais dos usuários existentes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 VERIFICANDO USUÁRIOS EXISTENTES'))
        self.stdout.write('=' * 60)
        
        # 1. LISTAR TODOS OS USUÁRIOS
        users = User.objects.all()
        self.stdout.write(f'\n👥 USUÁRIOS EXISTENTES ({users.count()}):')
        
        for user in users:
            self.stdout.write(f'  - {user.email} (ativo: {user.is_active})')
        
        # 2. VERIFICAR PROBLEMAS REAIS
        self.stdout.write(f'\n🔍 VERIFICANDO PROBLEMAS:')
        
        problemas_encontrados = 0
        
        for user in users:
            self.stdout.write(f'\n📧 Verificando: {user.email}')
            
            # Verificar se está ativo
            if not user.is_active:
                self.stdout.write('   ⚠️ Usuário inativo - ativando')
                user.is_active = True
                user.save()
                problemas_encontrados += 1
            
            # Verificar se tem senha
            if not user.has_usable_password():
                self.stdout.write('   ⚠️ Usuário sem senha - precisa definir senha')
                problemas_encontrados += 1
            
            # Verificar se tem perfil
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write('   ✅ Perfil OK')
            except Profile.DoesNotExist:
                self.stdout.write('   ⚠️ Sem perfil - criando')
                profile = Profile.objects.create(
                    user=user,
                    nome=user.first_name or user.email.split('@')[0],
                    idade=25,
                    faixa='branca'
                )
                problemas_encontrados += 1
        
        # 3. TESTAR LOGIN COM SENHAS CONHECIDAS
        self.stdout.write(f'\n🧪 TESTANDO LOGIN:')
        
        senhas_teste = ['123456', '123', 'admin', 'password', 'senha', 'teste']
        
        for user in users:
            self.stdout.write(f'\n📧 Testando login: {user.email}')
            
            # Testar com senhas comuns
            senha_funcionando = None
            for senha in senhas_teste:
                auth_user = authenticate(username=user.username, password=senha)
                if auth_user:
                    senha_funcionando = senha
                    break
            
            if senha_funcionando:
                self.stdout.write(f'   ✅ Login funciona com senha: {senha_funcionando}')
            else:
                self.stdout.write(f'   ❌ Login não funciona com senhas comuns')
                self.stdout.write(f'   💡 Usuário precisa redefinir senha')
        
        # 4. RESUMO
        self.stdout.write(f'\n📊 RESUMO:')
        self.stdout.write(f'   Problemas corrigidos: {problemas_encontrados}')
        
        if problemas_encontrados == 0:
            self.stdout.write('   ✅ Todos os usuários estão OK!')
        else:
            self.stdout.write('   ⚠️ Alguns problemas foram corrigidos')
        
        self.stdout.write(f'\n💡 PRÓXIMOS PASSOS:')
        self.stdout.write(f'   1. Usuários com senhas desconhecidas precisam redefinir')
        self.stdout.write(f'   2. Use o admin do Django para redefinir senhas')
        self.stdout.write(f'   3. Ou crie um comando específico para redefinir senhas individuais')
        
        self.stdout.write('\n✅ Verificação concluída!')
