from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, ConfiguracaoPagamento
from payments.views import checkout_pagamento, criar_pagamento
import time

class Command(BaseCommand):
    help = 'Testa o checkout com dados detalhados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando checkout detalhado...'))
        
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
            descricao=f"Teste Checkout - {plano.nome}",
            payment_id=f'teste-checkout-{unique_id}'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Pagamento criado: ID {pagamento.id}'))
        self.stdout.write(f'   Payment ID: {pagamento.get_payment_id()}')
        
        # Criar preferência no Mercado Pago
        factory = RequestFactory()
        request = factory.post(f'/payments/criar-pagamento/{plano.id}/', {
            'nome': 'Teste Usuario',
            'email': 'teste@exemplo.com',
            'telefone': '11999999999',
            'cpf': '11144477735'
        })
        request.user = usuario
        
        # Simular CSRF token
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
                        
                        # Verificar se é sandbox
                        if 'sandbox' in str(context.get("init_point", "")):
                            self.stdout.write(self.style.SUCCESS('✅ Usando URL do sandbox'))
                        else:
                            self.stdout.write(self.style.WARNING('⚠️ Usando URL de produção'))
                        
                        self.stdout.write(self.style.SUCCESS('🎯 URL para testar:'))
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
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste detalhado concluído!'))
