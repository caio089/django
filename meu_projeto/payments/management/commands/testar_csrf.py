from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, ConfiguracaoPagamento
from payments.views import checkout_pagamento
import time

class Command(BaseCommand):
    help = 'Testa se o CSRF token está sendo incluído no template'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando CSRF token no template...'))
        
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
            descricao=f"Teste CSRF - {plano.nome}",
            payment_id=f'teste-csrf-{unique_id}'
        )
        
        # Criar request simulado
        factory = RequestFactory()
        request = factory.get(f'/payments/checkout/{pagamento.id}/')
        request.user = usuario
        
        # Simular CSRF token
        from django.middleware.csrf import get_token
        get_token(request)
        
        # Chamar a view de checkout
        response = checkout_pagamento(request, pagamento.id)
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS('✅ Página de checkout carregada'))
            
            # Verificar se o CSRF token está no HTML
            content = response.content.decode()
            
            if 'csrfmiddlewaretoken' in content:
                self.stdout.write(self.style.SUCCESS('✅ CSRF token encontrado no HTML'))
                
                # Extrair o token
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
                if csrf_match:
                    token = csrf_match.group(1)
                    self.stdout.write(f'   Token: {token[:20]}...')
                else:
                    self.stdout.write(self.style.WARNING('⚠️ Token CSRF não encontrado no formato esperado'))
            else:
                self.stdout.write(self.style.ERROR('❌ CSRF token NÃO encontrado no HTML'))
                
        else:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao carregar checkout: {response.status_code}'))
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de CSRF concluído!'))
