"""
Comando para testar cancelamento de assinatura
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Assinatura, Reembolso
from payments.views import cancelar_assinatura
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone

class Command(BaseCommand):
    help = 'Testa cancelamento de assinatura'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username do usuário')

    def handle(self, *args, **options):
        username = options.get('username', 'ccamposs2007@gmail.com')
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'🔍 Testando cancelamento para: {user.username}')
            
            # Verificar assinaturas ativas
            assinaturas = Assinatura.objects.filter(
                usuario=user,
                status='ativa',
                data_vencimento__gt=timezone.now()
            )
            
            self.stdout.write(f'Assinaturas ativas encontradas: {assinaturas.count()}')
            
            for assinatura in assinaturas:
                self.stdout.write(f'  - ID: {assinatura.id}')
                self.stdout.write(f'  - Plano: {assinatura.plano.nome}')
                self.stdout.write(f'  - Data início: {assinatura.data_inicio}')
                self.stdout.write(f'  - Data vencimento: {assinatura.data_vencimento}')
                
                # Calcular dias desde a compra
                dias_desde_compra = (timezone.now() - assinatura.data_inicio).days
                self.stdout.write(f'  - Dias desde compra: {dias_desde_compra}')
                self.stdout.write(f'  - Tem direito a reembolso: {dias_desde_compra < 7}')
            
            # Simular requisição
            factory = RequestFactory()
            request = factory.post('/payments/cancelar-assinatura/')
            request.user = user
            
            # Testar função
            response = cancelar_assinatura(request)
            self.stdout.write(f'Status da resposta: {response.status_code}')
            
            if hasattr(response, 'content'):
                import json
                try:
                    data = json.loads(response.content)
                    self.stdout.write(f'Resposta: {data}')
                except:
                    self.stdout.write(f'Conteúdo: {response.content}')
            
        except User.DoesNotExist:
            self.stdout.write(f'❌ Usuário {username} não encontrado')
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
