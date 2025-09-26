from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Pagamento, PlanoPremium

class Command(BaseCommand):
    help = 'Cria um pagamento de teste'

    def handle(self, *args, **options):
        # Criar usuário de teste se não existir
        user, created = User.objects.get_or_create(
            username='teste',
            defaults={'email': 'teste@exemplo.com', 'first_name': 'Teste'}
        )
        
        # Criar plano de teste se não existir
        plano, created = PlanoPremium.objects.get_or_create(
            nome='Plano Teste',
            defaults={'descricao': 'Plano de teste', 'preco': 29.90, 'duracao_dias': 30}
        )
        
        # Criar pagamento de teste
        pagamento = Pagamento.objects.create(
            usuario=user,
            valor=plano.preco,
            descricao=f'Assinatura {plano.nome}',
            status='pending'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Pagamento de teste criado com ID: {pagamento.id}')
        )
        self.stdout.write(f'URL: http://127.0.0.1:8000/payments/checkout/{pagamento.id}/')
