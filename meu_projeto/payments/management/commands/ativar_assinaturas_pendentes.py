from django.core.management.base import BaseCommand
from payments.models import Pagamento, Assinatura
from payments.views import get_mercadopago_config, ativar_assinatura
import mercadopago

class Command(BaseCommand):
    help = 'Ativa assinaturas pendentes verificando status no Mercado Pago'

    def handle(self, *args, **options):
        self.stdout.write('VERIFICANDO ASSINATURAS PENDENTES\n')
        
        # Buscar pagamentos aprovados sem assinatura
        pagamentos_pendentes = Pagamento.objects.filter(
            status='approved'
        ).exclude(
            assinatura__isnull=False
        )
        
        self.stdout.write(f'Encontrados {pagamentos_pendentes.count()} pagamentos aprovados sem assinatura')
        
        if pagamentos_pendentes.count() == 0:
            self.stdout.write(self.style.SUCCESS('Nenhuma assinatura pendente encontrada'))
            return
        
        # Configurar SDK
        sdk, config = get_mercadopago_config()
        if not sdk:
            self.stdout.write(self.style.ERROR('Erro ao configurar SDK do Mercado Pago'))
            return
        
        ativadas = 0
        
        for pagamento in pagamentos_pendentes:
            try:
                self.stdout.write(f'\nProcessando pagamento {pagamento.id}...')
                self.stdout.write(f'  Usuario: {pagamento.usuario.username}')
                self.stdout.write(f'  Valor: R$ {pagamento.valor}')
                self.stdout.write(f'  Status: {pagamento.status}')
                
                # Verificar se já tem assinatura
                assinatura_existente = Assinatura.objects.filter(
                    external_reference=pagamento.external_reference
                ).first()
                
                if assinatura_existente:
                    self.stdout.write(f'  Assinatura já existe: {assinatura_existente.id}')
                    continue
                
                # Verificar status no Mercado Pago
                payment_id_mp = pagamento.get_payment_id()
                if not payment_id_mp:
                    self.stdout.write(self.style.WARNING('  Sem payment_id do MP'))
                    continue
                
                # Remover prefixo se existir
                if payment_id_mp.startswith('pref_'):
                    payment_id_mp = payment_id_mp.replace('pref_', '')
                
                # Buscar no Mercado Pago
                payment_info = sdk.payment().get(payment_id_mp)
                
                if payment_info["status"] == 200:
                    payment_data = payment_info["response"]
                    self.stdout.write(f'  Status no MP: {payment_data["status"]}')
                    
                    if payment_data["status"] == "approved":
                        # Ativar assinatura
                        ativar_assinatura(pagamento, payment_data)
                        ativadas += 1
                        self.stdout.write(self.style.SUCCESS('  Assinatura ativada com sucesso!'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  Status não aprovado no MP: {payment_data["status"]}'))
                else:
                    self.stdout.write(self.style.ERROR(f'  Erro ao buscar no MP: {payment_info["status"]}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Erro ao processar: {e}'))
        
        self.stdout.write(f'\nRESUMO:')
        self.stdout.write(f'  Assinaturas ativadas: {ativadas}')
        self.stdout.write(f'  Total processadas: {pagamentos_pendentes.count()}')
        
        if ativadas > 0:
            self.stdout.write(self.style.SUCCESS('\nAssinaturas ativadas com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('\nNenhuma assinatura foi ativada'))
