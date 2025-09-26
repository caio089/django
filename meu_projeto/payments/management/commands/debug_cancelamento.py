"""
Comando para debug do cancelamento
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura
from django.utils import timezone

class Command(BaseCommand):
    help = 'Debug do cancelamento'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='ccamposs2007@gmail.com')
            self.stdout.write(f'🔍 Usuário: {user.username}')
            
            # Verificar assinaturas
            assinaturas = Assinatura.objects.filter(usuario=user)
            self.stdout.write(f'Total de assinaturas: {assinaturas.count()}')
            
            for assinatura in assinaturas:
                self.stdout.write(f'\n📋 Assinatura {assinatura.id}:')
                self.stdout.write(f'  - Status: {assinatura.status}')
                self.stdout.write(f'  - Plano: {assinatura.plano.nome}')
                self.stdout.write(f'  - Data início: {assinatura.data_inicio}')
                self.stdout.write(f'  - Data vencimento: {assinatura.data_vencimento}')
                self.stdout.write(f'  - Data cancelamento: {assinatura.data_cancelamento}')
                
                if assinatura.data_inicio:
                    dias = (timezone.now() - assinatura.data_inicio).days
                    self.stdout.write(f'  - Dias desde compra: {dias}')
                    self.stdout.write(f'  - Tem direito a reembolso: {dias < 7}')
                
                # Verificar se está ativa
                if assinatura.status == 'ativa' and assinatura.data_vencimento > timezone.now():
                    self.stdout.write(f'  - ✅ ATIVA')
                else:
                    self.stdout.write(f'  - ❌ INATIVA')
            
            # Verificar perfil
            try:
                profile = user.profile
                self.stdout.write(f'\n👤 Perfil:')
                self.stdout.write(f'  - Conta premium: {profile.conta_premium}')
                self.stdout.write(f'  - Data vencimento premium: {profile.data_vencimento_premium}')
            except Exception as e:
                self.stdout.write(f'❌ Erro no perfil: {e}')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro geral: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())


