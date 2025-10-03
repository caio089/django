from django.core.management.base import BaseCommand
from payments.models import Pagamento, Assinatura, WebhookEvent
from payments.views import get_mercadopago_config
import mercadopago
import json

class Command(BaseCommand):
    help = 'Testa se os webhooks estão funcionando corretamente'

    def handle(self, *args, **options):
        self.stdout.write('TESTANDO WEBHOOKS E SISTEMA DE PAGAMENTO\n')
        
        # 1. Verificar configuração
        self.stdout.write('1. Verificando configuração do Mercado Pago...')
        sdk, config = get_mercadopago_config()
        if not sdk:
            self.stdout.write(self.style.ERROR('   ERRO: SDK não configurado'))
            return
        self.stdout.write(self.style.SUCCESS('   OK: SDK configurado'))
        self.stdout.write(f'   Ambiente: {config.ambiente}')
        self.stdout.write(f'   Webhook URL: {config.webhook_url}')
        
        # 2. Verificar webhooks recebidos
        self.stdout.write('\n2. Verificando webhooks recebidos...')
        webhooks = WebhookEvent.objects.all().order_by('-data_recebimento')[:10]
        self.stdout.write(f'   Total de webhooks: {WebhookEvent.objects.count()}')
        self.stdout.write(f'   Últimos 10 webhooks:')
        
        for webhook in webhooks:
            status = 'PROCESSADO' if webhook.processado else 'PENDENTE'
            erro = f' - ERRO: {webhook.erro_processamento}' if webhook.erro_processamento else ''
            self.stdout.write(f'     {webhook.data_recebimento} - {webhook.tipo} - {status}{erro}')
        
        # 3. Verificar pagamentos
        self.stdout.write('\n3. Verificando pagamentos...')
        pagamentos = Pagamento.objects.all().order_by('-data_criacao')[:10]
        self.stdout.write(f'   Total de pagamentos: {Pagamento.objects.count()}')
        
        for pagamento in pagamentos:
            self.stdout.write(f'     ID: {pagamento.id}, Status: {pagamento.status}, Usuario: {pagamento.usuario.username}, Valor: R${pagamento.valor}')
        
        # 4. Verificar assinaturas
        self.stdout.write('\n4. Verificando assinaturas...')
        assinaturas = Assinatura.objects.all().order_by('-data_criacao')[:10]
        self.stdout.write(f'   Total de assinaturas: {Assinatura.objects.count()}')
        
        for assinatura in assinaturas:
            self.stdout.write(f'     ID: {assinatura.id}, Usuario: {assinatura.usuario.username}, Status: {assinatura.status}, Plano: {assinatura.plano.nome}')
        
        # 5. Testar criação de pagamento PIX
        self.stdout.write('\n5. Testando criação de pagamento PIX...')
        try:
            payment_data = {
                "transaction_amount": 1.00,
                "description": "Teste de webhook",
                "payment_method_id": "pix",
                "payer": {
                    "email": "test@example.com",
                    "identification": {
                        "type": "CPF",
                        "number": "12345678901"
                    }
                },
                "external_reference": "test_webhook_123"
            }
            
            payment_result = sdk.payment().create(payment_data)
            
            if payment_result["status"] == 201:
                payment_info = payment_result["response"]
                self.stdout.write(self.style.SUCCESS(f'   OK: PIX criado - ID: {payment_info["id"]}'))
                self.stdout.write(f'   Status: {payment_info["status"]}')
                
                # Verificar se tem QR Code
                point_of_interaction = payment_info.get("point_of_interaction", {})
                transaction_data = point_of_interaction.get("transaction_data", {})
                qr_code = transaction_data.get("qr_code")
                
                if qr_code:
                    self.stdout.write(self.style.SUCCESS('   OK: QR Code gerado'))
                else:
                    self.stdout.write(self.style.WARNING('   AVISO: Sem QR Code'))
                    
            else:
                self.stdout.write(self.style.ERROR(f'   ERRO: {payment_result}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ERRO ao criar PIX: {e}'))
        
        # 6. Verificar função de ativação de assinatura
        self.stdout.write('\n6. Verificando função de ativação...')
        try:
            from payments.views import ativar_assinatura
            self.stdout.write(self.style.SUCCESS('   OK: Função ativar_assinatura importada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ERRO: {e}'))
        
        # 7. Verificar URLs do webhook
        self.stdout.write('\n7. Verificando URLs...')
        self.stdout.write(f'   Webhook URL configurada: {config.webhook_url}')
        
        # Verificar se a URL é acessível (simulação)
        if config.webhook_url:
            if 'render.com' in config.webhook_url:
                self.stdout.write(self.style.SUCCESS('   OK: URL aponta para Render (produção)'))
            else:
                self.stdout.write(self.style.WARNING('   AVISO: URL pode não estar em produção'))
        
        # 8. Resumo final
        self.stdout.write('\nRESUMO DO SISTEMA:')
        
        # Verificar se há pagamentos aprovados sem assinatura
        pagamentos_aprovados_sem_assinatura = Pagamento.objects.filter(
            status='approved'
        ).exclude(
            assinatura__isnull=False
        )
        
        if pagamentos_aprovados_sem_assinatura.count() > 0:
            self.stdout.write(self.style.WARNING(f'   ATENÇÃO: {pagamentos_aprovados_sem_assinatura.count()} pagamentos aprovados sem assinatura'))
        else:
            self.stdout.write(self.style.SUCCESS('   OK: Todos os pagamentos aprovados têm assinatura'))
        
        # Verificar webhooks com erro
        webhooks_com_erro = WebhookEvent.objects.filter(
            erro_processamento__isnull=False
        ).count()
        
        if webhooks_com_erro > 0:
            self.stdout.write(self.style.WARNING(f'   ATENÇÃO: {webhooks_com_erro} webhooks com erro'))
        else:
            self.stdout.write(self.style.SUCCESS('   OK: Nenhum webhook com erro'))
        
        self.stdout.write('\nTESTE CONCLUÍDO!')
        
        # Instruções finais
        self.stdout.write('\nINSTRUÇÕES:')
        self.stdout.write('1. Configure o webhook no painel do Mercado Pago:')
        self.stdout.write(f'   URL: {config.webhook_url}')
        self.stdout.write('   Eventos: payment.created, payment.updated')
        self.stdout.write('2. Teste um pagamento PIX real')
        self.stdout.write('3. Monitore os logs para verificar processamento')
        self.stdout.write('4. O sistema deve detectar automaticamente e ativar a assinatura')
