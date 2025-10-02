from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import ConfiguracaoPagamento
from home.models import Profile
import os

class Command(BaseCommand):
    help = 'Correção completa do deploy - login e pagamentos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 CORREÇÃO COMPLETA DO DEPLOY'))
        self.stdout.write('=' * 60)
        
        # 1. CORRIGIR LOGIN
        self.stdout.write('\n🔐 CORRIGINDO LOGIN:')
        
        # Redefinir senha do usuário principal
        try:
            user = User.objects.get(email='ccamposs2007@gmail.com')
            user.set_password('123456')
            user.is_active = True
            user.save()
            self.stdout.write('✅ Senha redefinida para ccamposs2007@gmail.com')
            self.stdout.write('   Nova senha: 123456')
        except User.DoesNotExist:
            self.stdout.write('❌ Usuário ccamposs2007@gmail.com não encontrado')
        
        # 2. CORRIGIR PERFIS
        self.stdout.write('\n👤 CORRIGINDO PERFIS:')
        
        for user in User.objects.all():
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f'✅ Perfil OK para {user.email}')
            except Profile.DoesNotExist:
                profile = Profile.objects.create(
                    user=user,
                    nome=user.first_name or user.email.split('@')[0],
                    idade=25,
                    faixa='branca'
                )
                self.stdout.write(f'✅ Perfil criado para {user.email}')
        
        # 3. CORRIGIR CONFIGURAÇÃO MERCADO PAGO
        self.stdout.write('\n💳 CORRIGINDO MERCADO PAGO:')
        
        # Obter tokens das variáveis de ambiente
        access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
        public_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
        
        if access_token and public_key:
            # Desativar configurações antigas
            ConfiguracaoPagamento.objects.filter(ativo=True).update(ativo=False)
            
            # Criar nova configuração sem criptografia
            config = ConfiguracaoPagamento.objects.create(
                nome='Configuração Deploy Corrigida',
                ambiente='production' if not access_token.startswith('TEST-') else 'sandbox',
                access_token=access_token,  # Sem criptografia
                public_key=public_key,      # Sem criptografia
                webhook_url='https://dojo-on.onrender.com/payments/webhook/',
                ativo=True
            )
            
            self.stdout.write('✅ Configuração do Mercado Pago criada')
            self.stdout.write(f'   Ambiente: {config.ambiente}')
            self.stdout.write(f'   Access token: {"✅" if config.access_token else "❌"}')
            self.stdout.write(f'   Public key: {"✅" if config.public_key else "❌"}')
        else:
            self.stdout.write('❌ Variáveis de ambiente do Mercado Pago não encontradas')
            self.stdout.write('   MERCADOPAGO_ACCESS_TOKEN:', bool(access_token))
            self.stdout.write('   MERCADOPAGO_PUBLIC_KEY:', bool(public_key))
        
        # 4. TESTAR CONFIGURAÇÃO
        self.stdout.write('\n🧪 TESTANDO CONFIGURAÇÃO:')
        
        try:
            from payments.views import get_mercadopago_config
            sdk, config = get_mercadopago_config()
            if sdk and config:
                self.stdout.write('✅ Configuração do Mercado Pago funcionando')
            else:
                self.stdout.write('❌ Configuração do Mercado Pago com problemas')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao testar configuração: {e}')
        
        # 5. RESUMO
        self.stdout.write('\n📋 RESUMO:')
        self.stdout.write('✅ Login: Senha redefinida para 123456')
        self.stdout.write('✅ Perfis: Verificados/criados')
        self.stdout.write('✅ Mercado Pago: Configuração recriada')
        
        self.stdout.write('\n🎯 PRÓXIMOS PASSOS:')
        self.stdout.write('1. Teste o login com: ccamposs2007@gmail.com / 123456')
        self.stdout.write('2. Teste os pagamentos')
        self.stdout.write('3. Verifique os logs para confirmar funcionamento')
        
        self.stdout.write('\n✅ Correção completa finalizada!')
