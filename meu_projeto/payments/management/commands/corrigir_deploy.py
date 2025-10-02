from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import ConfiguracaoPagamento
from home.models import Profile
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Corrige problemas comuns no deploy'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 CORRIGINDO PROBLEMAS DO DEPLOY'))
        self.stdout.write('=' * 50)
        
        # 1. Verificar e corrigir usuários
        self.stdout.write('\n👥 VERIFICANDO USUÁRIOS:')
        
        # Verificar se o usuário principal existe
        try:
            user = User.objects.get(email='ccamposs2007@gmail.com')
            if not user.is_active:
                user.is_active = True
                user.save()
                self.stdout.write('✅ Usuário ccamposs2007@gmail.com ativado')
            else:
                self.stdout.write('✅ Usuário ccamposs2007@gmail.com já está ativo')
        except User.DoesNotExist:
            self.stdout.write('❌ Usuário ccamposs2007@gmail.com não encontrado')
        
        # 2. Verificar e corrigir perfis
        self.stdout.write('\n👤 VERIFICANDO PERFIS:')
        
        for user in User.objects.all():
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f'✅ Perfil já existe para {user.email}')
            except Profile.DoesNotExist:
                # Criar perfil com valores padrão
                profile = Profile.objects.create(
                    user=user,
                    nome=user.first_name or user.email.split('@')[0],
                    idade=25,  # Idade padrão
                    faixa='branca'  # Faixa padrão
                )
                self.stdout.write(f'✅ Perfil criado para {user.email}')
        
        # 3. Verificar configuração do Mercado Pago
        self.stdout.write('\n💳 VERIFICANDO MERCADO PAGO:')
        
        # Verificar se há configuração ativa
        active_config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not active_config:
            self.stdout.write('❌ Nenhuma configuração ativa do Mercado Pago')
            
            # Tentar criar configuração a partir das variáveis de ambiente
            access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
            public_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
            
            if access_token and public_key:
                config = ConfiguracaoPagamento.objects.create(
                    nome='Configuração Deploy',
                    ambiente='production' if not access_token.startswith('TEST-') else 'sandbox',
                    access_token=access_token,
                    public_key=public_key,
                    ativo=True
                )
                self.stdout.write('✅ Configuração do Mercado Pago criada a partir das variáveis de ambiente')
            else:
                self.stdout.write('❌ Variáveis de ambiente do Mercado Pago não encontradas')
        else:
            self.stdout.write('✅ Configuração do Mercado Pago ativa encontrada')
        
        # 4. Verificar configurações do Django
        self.stdout.write('\n⚙️ VERIFICANDO CONFIGURAÇÕES:')
        
        if settings.DEBUG:
            self.stdout.write('⚠️ DEBUG está ativado - desative em produção')
        
        allowed_hosts = settings.ALLOWED_HOSTS
        if 'dojo-on.onrender.com' not in allowed_hosts:
            self.stdout.write('⚠️ dojo-on.onrender.com não está em ALLOWED_HOSTS')
        else:
            self.stdout.write('✅ dojo-on.onrender.com está em ALLOWED_HOSTS')
        
        self.stdout.write('\n✅ Correções concluídas!')
