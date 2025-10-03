from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento
from payments.views import checkout_pagamento, criar_pagamento
import time

class Command(BaseCommand):
    help = 'Testa o redirecionamento do cartão de crédito'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando redirecionamento do cartão...'))
        
        # Buscar usuário e plano
        usuario = User.objects.filter(is_active=True).first()
        plano = PlanoPremium.objects.filter(ativo=True).first()
        
        if not usuario or not plano:
            self.stdout.write(self.style.ERROR('❌ Usuário ou plano não encontrado'))
            return
        
        # Criar pagamento de teste
        unique_id = int(time.time() * 1000)
        pagamento = Pagamento.objects.create(
            usuario=usuario,
            valor=plano.preco,
            tipo='assinatura',
            descricao=f"Teste Cartão - {plano.nome}",
            payment_id=f'teste-cartao-{unique_id}'
        )
        
        self.stdout.write(f'✅ Pagamento criado: ID {pagamento.id}')
        
        # Criar preferência no Mercado Pago
        factory = RequestFactory()
        request = factory.post(f'/payments/criar-pagamento/{plano.id}/', {
            'nome': 'Teste Usuario',
            'email': 'teste@exemplo.com',
            'telefone': '11999999999',
            'cpf': '11144477735'
        })
        request.user = usuario
        
        from django.middleware.csrf import get_token
        get_token(request)
        
        try:
            # Criar pagamento real
            response = criar_pagamento(request, plano.id)
            
            if response.status_code == 302:  # Redirect
                # Buscar o pagamento criado
                pagamento_real = Pagamento.objects.filter(usuario=usuario).order_by('-id').first()
                
                if pagamento_real and pagamento_real.get_payment_id():
                    self.stdout.write(self.style.SUCCESS('✅ Pagamento real criado'))
                    self.stdout.write(f'   Payment ID: {pagamento_real.get_payment_id()}')
                    
                    # Testar checkout
                    request_checkout = factory.get(f'/payments/checkout/{pagamento_real.id}/')
                    request_checkout.user = usuario
                    
                    response_checkout = checkout_pagamento(request_checkout, pagamento_real.id)
                    
                    if response_checkout.status_code == 200:
                        self.stdout.write(self.style.SUCCESS('✅ Checkout carregado com sucesso!'))
                        
                        # Analisar contexto
                        context = response_checkout.context_data if hasattr(response_checkout, 'context_data') else {}
                        
                        self.stdout.write(self.style.SUCCESS('📊 Contexto do checkout:'))
                        self.stdout.write(f'   Public Key: {context.get("public_key", "N/A")[:20]}...')
                        self.stdout.write(f'   Preference ID: {context.get("preference_id", "N/A")}')
                        self.stdout.write(f'   Init Point: {context.get("init_point", "N/A")}')
                        self.stdout.write(f'   PIX Available: {context.get("pix_available", "N/A")}')
                        
                        # Verificar se Init Point é válido
                        init_point = context.get("init_point")
                        if init_point:
                            if init_point.startswith('https://www.mercadopago.com.br'):
                                self.stdout.write(self.style.SUCCESS('✅ Init Point válido (produção)'))
                            elif init_point.startswith('https://sandbox.mercadopago.com.br'):
                                self.stdout.write(self.style.WARNING('⚠️ Init Point é sandbox'))
                            else:
                                self.stdout.write(self.style.ERROR('❌ Init Point inválido'))
                            
                            # Testar URL do cartão
                            card_url = init_point
                            self.stdout.write(f'🔗 URL do cartão: {card_url}')
                            
                            # Verificar se URL contém parâmetros corretos
                            if 'pref_id=' in card_url:
                                self.stdout.write(self.style.SUCCESS('✅ URL contém preference_id'))
                            else:
                                self.stdout.write(self.style.ERROR('❌ URL não contém preference_id'))
                                
                        else:
                            self.stdout.write(self.style.ERROR('❌ Init Point não encontrado'))
                        
                        self.stdout.write(self.style.SUCCESS('🎯 URL para testar cartão:'))
                        self.stdout.write(f'   http://localhost:8000/payments/checkout/{pagamento_real.id}/')
                        
                    else:
                        self.stdout.write(self.style.ERROR(f'❌ Erro no checkout: {response_checkout.status_code}'))
                else:
                    self.stdout.write(self.style.ERROR('❌ Pagamento real não foi criado corretamente'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar pagamento: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de cartão concluído!'))






