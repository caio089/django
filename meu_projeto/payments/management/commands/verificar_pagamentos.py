from django.core.management.base import BaseCommand
from payments.models import Pagamento

class Command(BaseCommand):
    help = 'Verifica pagamentos existentes'

    def handle(self, *args, **options):
        pagamentos = Pagamento.objects.all()[:10]
        
        if not pagamentos:
            self.stdout.write(self.style.WARNING('Nenhum pagamento encontrado'))
            return
            
        self.stdout.write('Pagamentos existentes:')
        for p in pagamentos:
            self.stdout.write(f'ID: {p.id}, Status: {p.status}, Usuario: {p.usuario}')




