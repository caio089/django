from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from payments.models import Pagamento, Assinatura
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reset completo: remove todos os usuários e cria admin padrão'

    def add_arguments(self, parser):
        parser.add_argument('--confirmar', action='store_true', help='Confirma o reset completo')
        parser.add_argument('--email-admin', type=str, default='admin@dojo.com', help='Email do admin')
        parser.add_argument('--senha-admin', type=str, default='admin123', help='Senha do admin')
        parser.add_argument('--nome-admin', type=str, default='Administrador', help='Nome do admin')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔄 RESET COMPLETO DO SISTEMA'))
        self.stdout.write('=' * 60)
        
        if not options['confirmar']:
            self.stdout.write('❌ ERRO: Esta operação é irreversível!')
            self.stdout.write('💡 Use --confirmar para executar o reset')
            self.stdout.write('💡 Exemplo: python manage.py reset_completo --confirmar')
            return
        
        # 1. CONTAR DADOS ATUAIS
        total_usuarios = User.objects.count()
        total_perfis = Profile.objects.count()
        total_pagamentos = Pagamento.objects.count()
        total_assinaturas = Assinatura.objects.count()
        
        self.stdout.write(f'\n📊 DADOS ATUAIS:')
        self.stdout.write(f'   Usuários: {total_usuarios}')
        self.stdout.write(f'   Perfis: {total_perfis}')
        self.stdout.write(f'   Pagamentos: {total_pagamentos}')
        self.stdout.write(f'   Assinaturas: {total_assinaturas}')
        
        if total_usuarios == 0:
            self.stdout.write('\n✅ Banco já está vazio')
        else:
            # 2. REMOVER TODOS OS DADOS
            self.stdout.write(f'\n🗑️  REMOVENDO TODOS OS DADOS:')
            
            try:
                with transaction.atomic():
                    # Remover perfis
                    Profile.objects.all().delete()
                    self.stdout.write('   ✅ Perfis removidos')
                    
                    # Remover pagamentos
                    Pagamento.objects.all().delete()
                    self.stdout.write('   ✅ Pagamentos removidos')
                    
                    # Remover assinaturas
                    Assinatura.objects.all().delete()
                    self.stdout.write('   ✅ Assinaturas removidas')
                    
                    # Remover usuários
                    User.objects.all().delete()
                    self.stdout.write('   ✅ Usuários removidos')
                    
            except Exception as e:
                self.stdout.write(f'\n❌ ERRO durante a remoção: {e}')
                return
        
        # 3. CRIAR ADMIN PADRÃO
        self.stdout.write(f'\n👤 CRIANDO ADMIN PADRÃO:')
        
        email_admin = options['email_admin']
        senha_admin = options['senha_admin']
        nome_admin = options['nome_admin']
        
        try:
            # Criar usuário admin
            user = User.objects.create_user(
                username=email_admin.split('@')[0],
                email=email_admin,
                password=senha_admin,
                first_name=nome_admin,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write(f'   ✅ Usuário admin criado')
            self.stdout.write(f'   Email: {email_admin}')
            self.stdout.write(f'   Senha: {senha_admin}')
            self.stdout.write(f'   Nome: {nome_admin}')
            
            # Criar perfil do admin
            profile = Profile.objects.create(
                user=user,
                nome=nome_admin,
                idade=30,
                faixa='preta'
            )
            
            self.stdout.write(f'   ✅ Perfil do admin criado')
            
            # Testar login do admin
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=user.username, password=senha_admin)
            
            if auth_user:
                self.stdout.write(f'   ✅ Login do admin testado com sucesso!')
            else:
                self.stdout.write(f'   ❌ Erro ao testar login do admin')
            
        except Exception as e:
            self.stdout.write(f'\n❌ Erro ao criar admin: {e}')
            return
        
        # 4. VERIFICAR RESULTADO FINAL
        usuarios_finais = User.objects.count()
        perfis_finais = Profile.objects.count()
        
        self.stdout.write(f'\n✅ RESET CONCLUÍDO!')
        self.stdout.write(f'   Usuários finais: {usuarios_finais}')
        self.stdout.write(f'   Perfis finais: {perfis_finais}')
        
        self.stdout.write(f'\n🎯 SISTEMA PRONTO!')
        self.stdout.write(f'   Admin criado: {email_admin}')
        self.stdout.write(f'   Senha: {senha_admin}')
        self.stdout.write(f'   Agora você pode criar novos usuários')
        
        self.stdout.write(f'\n💡 PRÓXIMOS PASSOS:')
        self.stdout.write(f'   1. Faça login com o admin')
        self.stdout.write(f'   2. Crie novos usuários via registro')
        self.stdout.write(f'   3. Teste o sistema')
        
        self.stdout.write('\n✅ Reset completo finalizado!')
