from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, ConfiguracaoPagamento
from payments.views import criar_pagamento
from django.test import RequestFactory
import requests
import time

class Command(BaseCommand):
    help = 'Testa a URL do Mercado Pago diretamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando URL do Mercado Pago...'))
        
        # Buscar usuário e plano
        usuario = User.objects.filter(is_active=True).first()
        plano = PlanoPremium.objects.filter(ativo=True).first()
        
        if not usuario or not plano:
            self.stdout.write(self.style.ERROR('❌ Usuário ou plano não encontrado'))
            return
        
        # Criar pagamento real
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
            # Criar pagamento
            response = criar_pagamento(request, plano.id)
            
            if response.status_code == 302:  # Redirect
                # Buscar o pagamento criado
                pagamento = Pagamento.objects.filter(usuario=usuario).order_by('-id').first()
                
                if pagamento and pagamento.get_payment_id():
                    self.stdout.write(self.style.SUCCESS('✅ Pagamento criado com sucesso'))
                    self.stdout.write(f'   Payment ID: {pagamento.get_payment_id()}')
                    
                    # Testar URLs do Mercado Pago
                    urls_para_testar = [
                        f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={pagamento.get_payment_id()}&payment_method_id=pix",
                        f"https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id={pagamento.get_payment_id()}&payment_method_id=pix",
                        f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={pagamento.get_payment_id()}",
                        f"https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id={pagamento.get_payment_id()}"
                    ]
                    
                    for i, url in enumerate(urls_para_testar, 1):
                        self.stdout.write(f'\n🔗 Testando URL {i}:')
                        self.stdout.write(f'   {url}')
                        
                        try:
                            # Fazer requisição HEAD para verificar se a URL existe
                            response = requests.head(url, timeout=10, allow_redirects=True)
                            
                            self.stdout.write(f'   Status: {response.status_code}')
                            self.stdout.write(f'   Final URL: {response.url}')
                            
                            if response.status_code == 200:
                                self.stdout.write(self.style.SUCCESS('   ✅ URL funcionando!'))
                            elif response.status_code == 404:
                                self.stdout.write(self.style.ERROR('   ❌ URL não encontrada (404)'))
                            elif response.status_code == 302:
                                self.stdout.write(self.style.WARNING('   ⚠️ Redirecionamento (302)'))
                            else:
                                self.stdout.write(self.style.WARNING(f'   ⚠️ Status inesperado: {response.status_code}'))
                                
                        except requests.exceptions.RequestException as e:
                            self.stdout.write(self.style.ERROR(f'   ❌ Erro na requisição: {e}'))
                    
                    # Verificar se a preferência ainda existe no Mercado Pago
                    self.stdout.write(f'\n🔍 Verificando preferência no Mercado Pago...')
                    
                    from payments.views import get_mercadopago_config
                    sdk, config = get_mercadopago_config()
                    
                    if sdk:
                        try:
                            preference_info = sdk.preference().get(pagamento.get_payment_id())
                            
                            if preference_info["status"] == 200:
                                preference_data = preference_info["response"]
                                self.stdout.write(self.style.SUCCESS('✅ Preferência encontrada no Mercado Pago'))
                                
                                # Mostrar URLs disponíveis
                                init_point = preference_data.get("init_point")
                                sandbox_init_point = preference_data.get("sandbox_init_point")
                                
                                self.stdout.write(f'   Init Point: {init_point}')
                                self.stdout.write(f'   Sandbox Init Point: {sandbox_init_point}')
                                
                                # Verificar se a preferência expirou
                                expires = preference_data.get("expires", False)
                                if expires:
                                    self.stdout.write(self.style.WARNING('⚠️ Preferência expirada!'))
                                else:
                                    self.stdout.write(self.style.SUCCESS('✅ Preferência válida'))
                                    
                            else:
                                self.stdout.write(self.style.ERROR(f'❌ Preferência não encontrada: {preference_info["status"]}'))
                                
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'❌ Erro ao verificar preferência: {e}'))
                    else:
                        self.stdout.write(self.style.ERROR('❌ SDK do Mercado Pago não disponível'))
                        
                else:
                    self.stdout.write(self.style.ERROR('❌ Pagamento não foi criado corretamente'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar pagamento: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('\n🏁 Teste de URL concluído!'))

