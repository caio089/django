from django.core.management.base import BaseCommand
from payments.views import criar_pagamento, get_mercadopago_config
from payments.models import PlanoPremium
from django.contrib.auth.models import User
from django.test import RequestFactory
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Testa a criação de pagamento em produção'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testando criacao de pagamento...'))
        
        # 1. Verificar configuração
        self.stdout.write('1. Verificando configuração do Mercado Pago...')
        sdk, config = get_mercadopago_config()
        if not sdk or not config:
            self.stdout.write(self.style.ERROR('Configuracao do Mercado Pago nao encontrada!'))
            return
        
        self.stdout.write(f'   Configuracao OK: {config.ambiente}')
        
        # 2. Verificar plano
        self.stdout.write('2. Verificando planos...')
        plano = PlanoPremium.objects.filter(ativo=True).first()
        if not plano:
            self.stdout.write(self.style.ERROR('Nenhum plano ativo encontrado!'))
            return
        
        self.stdout.write(f'   Plano encontrado: {plano.nome} - R$ {plano.preco}')
        
        # 3. Verificar usuário
        self.stdout.write('3. Verificando usuario...')
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('Nenhum usuario encontrado!'))
            return
        
        self.stdout.write(f'   Usuario encontrado: {user.email}')
        
        # 4. Testar criação de pagamento
        self.stdout.write('4. Testando criacao de pagamento...')
        try:
            factory = RequestFactory()
            request = factory.post(f'/payments/criar-pagamento/{plano.id}/', {
                'plano_id': str(plano.id),
                'nome': 'Teste Producao',
                'email': user.email,
                'telefone': '(11) 99999-9999',
                'cpf': '111.444.777-35'
            })
            request.user = user
            
            from django.middleware.csrf import get_token
            get_token(request)
            
            response = criar_pagamento(request, plano.id)
            
            if response.status_code == 200:
                import json
                data = json.loads(response.content.decode())
                if data.get('success'):
                    self.stdout.write(self.style.SUCCESS('Pagamento criado com sucesso!'))
                    self.stdout.write(f'   Preference ID: {data.get("preference_id")}')
                    self.stdout.write(f'   Public Key: {data.get("public_key", "N/A")[:20]}...')
                    self.stdout.write(f'   Payment ID: {data.get("payment_id")}')
                else:
                    self.stdout.write(self.style.ERROR(f'Erro na criacao: {data.get("error")}'))
            else:
                self.stdout.write(self.style.ERROR(f'Status HTTP: {response.status_code}'))
                self.stdout.write(f'   Resposta: {response.content.decode()}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao testar pagamento: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
