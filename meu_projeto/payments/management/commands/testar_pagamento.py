from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento, PlanoPremium, Pagamento
from django.contrib.auth.models import User
import mercadopago
import uuid
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Testa o fluxo completo de pagamento'

    def handle(self, *args, **options):
        """
        Testa o fluxo completo de pagamento
        """
        try:
            # Obter configuração ativa
            config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            
            if not config:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Nenhuma configuração ativa do Mercado Pago encontrada.\n'
                        'Execute: python manage.py configurar_mercadopago'
                    )
                )
                return

            # Obter credenciais
            access_token = config.get_access_token()
            public_key = config.get_public_key()
            
            if not access_token:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Access token não encontrado ou não pode ser descriptografado.'
                    )
                )
                return

            # Obter primeiro plano
            plano = PlanoPremium.objects.filter(ativo=True).first()
            if not plano:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Nenhum plano ativo encontrado.'
                    )
                )
                return

            self.stdout.write('🔄 Testando fluxo de pagamento...')
            
            try:
                # Inicializar SDK
                sdk = mercadopago.SDK(access_token)
                
                # Gerar external_reference único
                external_reference = str(uuid.uuid4())
                
                # Criar preferência de teste
                preference_data = {
                    "items": [
                        {
                            "title": f"Teste - {plano.nome}",
                            "description": f"Teste de pagamento - {plano.descricao}",
                            "quantity": 1,
                            "unit_price": float(plano.preco),
                            "currency_id": "BRL"
                        }
                    ],
                    "payer": {
                        "email": "teste@exemplo.com",
                        "identification": {
                            "type": "CPF",
                            "number": "12345678901"
                        }
                    },
                    "back_urls": {
                        "success": f"http://127.0.0.1:8000/payments/success/?external_reference={external_reference}",
                        "failure": f"http://127.0.0.1:8000/payments/failure/?external_reference={external_reference}",
                        "pending": f"http://127.0.0.1:8000/payments/pending/?external_reference={external_reference}"
                    },
                    "auto_return": "approved",
                    "external_reference": external_reference,
                    "notification_url": config.webhook_url,
                    "payment_methods": {
                        "excluded_payment_methods": [],
                        "excluded_payment_types": [],
                        "installments": 12
                    }
                }
                
                # Criar preferência
                preference_result = sdk.preference().create(preference_data)
                
                if preference_result["status"] == 201:
                    preference = preference_result["response"]
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Preferência de teste criada com sucesso!\n'
                            f'   ID: {preference.get("id")}\n'
                            f'   External Reference: {external_reference}\n'
                            f'   Valor: R$ {plano.preco}\n'
                            f'   URL de pagamento: {preference.get("init_point")}'
                        )
                    )
                    
                    # Simular criação de pagamento no banco
                    try:
                        # Buscar usuário de teste ou criar um
                        user, created = User.objects.get_or_create(
                            username='teste_pagamento',
                            defaults={
                                'email': 'teste@exemplo.com',
                                'first_name': 'Usuário',
                                'last_name': 'Teste'
                            }
                        )
                        
                        # Criar pagamento no banco
                        pagamento = Pagamento.objects.create(
                            usuario=user,
                            valor=plano.preco,
                            tipo='assinatura',
                            external_reference=external_reference,
                            descricao=f"Teste - {plano.nome}",
                            status='pending'
                        )
                        
                        # Criptografar dados
                        pagamento.set_payment_id(preference.get("id"))
                        pagamento.set_payer_email("teste@exemplo.com")
                        pagamento.set_payer_name("Usuário Teste")
                        pagamento.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Pagamento criado no banco de dados!\n'
                                f'   ID: {pagamento.id}\n'
                                f'   Status: {pagamento.status}\n'
                                f'   External Reference: {pagamento.external_reference}'
                            )
                        )
                        
                        # Testar busca de pagamento
                        self.stdout.write('\n🔄 Testando busca de pagamento...')
                        
                        # Simular busca por external_reference
                        pagamento_encontrado = Pagamento.objects.filter(
                            usuario=user,
                            external_reference=external_reference
                        ).first()
                        
                        if pagamento_encontrado:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'✅ Pagamento encontrado por external_reference!\n'
                                    f'   ID: {pagamento_encontrado.id}\n'
                                    f'   Status: {pagamento_encontrado.status}\n'
                                    f'   Valor: R$ {pagamento_encontrado.valor}'
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    '❌ Pagamento não encontrado por external_reference!'
                                )
                            )
                        
                        # Testar URLs de retorno
                        self.stdout.write('\n🔗 URLs de retorno:')
                        print(f"   Sucesso: http://127.0.0.1:8000/payments/success/?external_reference={external_reference}")
                        print(f"   Falha: http://127.0.0.1:8000/payments/failure/?external_reference={external_reference}")
                        print(f"   Pendente: http://127.0.0.1:8000/payments/pending/?external_reference={external_reference}")
                        
                        self.stdout.write(
                            self.style.WARNING(
                                '\n📱 PRÓXIMOS PASSOS PARA TESTAR:\n'
                                '1. Acesse a URL de pagamento acima\n'
                                '2. Faça um pagamento de teste (PIX, cartão, etc.)\n'
                                '3. Após o pagamento, você será redirecionado para a página de sucesso\n'
                                '4. O sistema deve encontrar o pagamento pelo external_reference\n'
                                '5. A assinatura será ativada automaticamente'
                            )
                        )
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'❌ Erro ao criar pagamento no banco: {e}'
                            )
                        )
                        
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Erro ao criar preferência: {preference_result}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Erro ao testar pagamento: {e}'
                    )
                )
                logger.error(f"Erro ao testar pagamento: {e}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro geral: {e}')
            )
            logger.error(f"Erro geral ao testar pagamento: {e}")



