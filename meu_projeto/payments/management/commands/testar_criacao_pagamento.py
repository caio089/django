from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, ConfiguracaoPagamento
from payments.views import criar_pagamento
from django.test import RequestFactory
import json

class Command(BaseCommand):
    help = 'Testa a criação de pagamentos para verificar se o erro foi corrigido'

    def add_arguments(self, parser):
        parser.add_argument('--plano-id', type=int, help='ID do plano para testar')
        parser.add_argument('--usuario-id', type=int, help='ID do usuário para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Iniciando teste de criação de pagamento...'))
        
        # Verificar se há configuração do Mercado Pago
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            self.stdout.write('Execute: python manage.py configurar_mercadopago')
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração encontrada: {config.ambiente}'))
        
        # Buscar plano
        plano_id = options.get('plano_id')
        if not plano_id:
            plano = PlanoPremium.objects.filter(ativo=True).first()
            if not plano:
                self.stdout.write(self.style.ERROR('❌ Nenhum plano ativo encontrado'))
                return
        else:
            try:
                plano = PlanoPremium.objects.get(id=plano_id, ativo=True)
            except PlanoPremium.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Plano {plano_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Plano selecionado: {plano.nome} - R$ {plano.preco}'))
        
        # Buscar usuário
        usuario_id = options.get('usuario_id')
        if not usuario_id:
            usuario = User.objects.filter(is_active=True).first()
            if not usuario:
                self.stdout.write(self.style.ERROR('❌ Nenhum usuário ativo encontrado'))
                return
        else:
            try:
                usuario = User.objects.get(id=usuario_id, is_active=True)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Usuário {usuario_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Usuário selecionado: {usuario.username}'))
        
        # Criar request simulado
        factory = RequestFactory()
        request = factory.post(f'/payments/criar-pagamento/{plano.id}/', {
            'nome': 'Teste Usuario',
            'email': 'teste@exemplo.com',
            'telefone': '11999999999',
            'cpf': '11144477735'  # CPF válido para teste
        })
        request.user = usuario
        
        # Simular CSRF token
        from django.middleware.csrf import get_token
        get_token(request)
        
        self.stdout.write(self.style.WARNING('🔄 Testando criação de pagamento...'))
        
        try:
            # Chamar a view de criação de pagamento
            response = criar_pagamento(request, plano.id)
            
            if response.status_code == 200:
                data = json.loads(response.content)
                if data.get('success'):
                    self.stdout.write(self.style.SUCCESS('✅ Pagamento criado com sucesso!'))
                    self.stdout.write(f'   Preference ID: {data.get("preference_id")}')
                    self.stdout.write(f'   Payment ID: {data.get("payment_id")}')
                    self.stdout.write(f'   External Reference: {data.get("external_reference")}')
                    self.stdout.write(f'   Init Point: {data.get("init_point")}')
                    self.stdout.write(f'   Public Key: {data.get("public_key")[:20]}...')
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Erro na criação: {data.get("error")}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro HTTP {response.status_code}'))
                self.stdout.write(f'Resposta: {response.content.decode()}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste concluído!'))
