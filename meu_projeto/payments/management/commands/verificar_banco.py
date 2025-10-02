from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from payments.models import ConfiguracaoPagamento
from home.models import Profile

class Command(BaseCommand):
    help = 'Verifica o estado do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🗄️ VERIFICANDO BANCO DE DADOS'))
        self.stdout.write('=' * 50)
        
        # 1. Verificar conexão
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com banco de dados OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão: {e}')
            return
        
        # 2. Verificar tabelas
        self.stdout.write('\n📋 VERIFICANDO TABELAS:')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            expected_tables = [
                'auth_user',
                'home_profile', 
                'payments_configuracaopagamento',
                'payments_pagamento',
                'payments_assinatura'
            ]
            
            for table in expected_tables:
                if any(table in str(t) for t in tables):
                    self.stdout.write(f'✅ {table}')
                else:
                    self.stdout.write(f'❌ {table} - TABELA NÃO ENCONTRADA')
        
        # 3. Verificar dados críticos
        self.stdout.write('\n📊 VERIFICANDO DADOS:')
        
        # Usuários
        user_count = User.objects.count()
        self.stdout.write(f'Usuários: {user_count}')
        
        # Perfis
        profile_count = Profile.objects.count()
        self.stdout.write(f'Perfis: {profile_count}')
        
        # Configurações
        config_count = ConfiguracaoPagamento.objects.count()
        self.stdout.write(f'Configurações: {config_count}')
        
        # 4. Verificar usuário específico
        try:
            user = User.objects.get(email='ccamposs2007@gmail.com')
            self.stdout.write(f'✅ Usuário ccamposs2007@gmail.com encontrado')
            self.stdout.write(f'   - Ativo: {user.is_active}')
            self.stdout.write(f'   - Staff: {user.is_staff}')
            self.stdout.write(f'   - Superuser: {user.is_superuser}')
            
            # Verificar perfil
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f'   - Perfil: {profile.nome}')
            except Profile.DoesNotExist:
                self.stdout.write('   - ❌ Perfil não encontrado')
                
        except User.DoesNotExist:
            self.stdout.write('❌ Usuário ccamposs2007@gmail.com não encontrado')
        
        self.stdout.write('\n✅ Verificação do banco concluída!')
