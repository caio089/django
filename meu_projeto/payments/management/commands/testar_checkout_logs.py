from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, ConfiguracaoPagamento
from payments.views import criar_pagamento, checkout_pagamento
from django.test import RequestFactory
import json

class Command(BaseCommand):
    help = 'Testa o checkout com logs detalhados para diagnosticar PIX'

    def add_arguments(self, parser):
        parser.add_argument('--plano-id', type=int, help='ID do plano para testar')
        parser.add_argument('--usuario-id', type=int, help='ID do usuário para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando checkout com logs detalhados...'))
        
        # Verificar configuração
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração: {config.ambiente}'))
        
        # Buscar plano
        plano_id = options.get('plano_id')
        if not plano_id:
            plano = PlanoPremium.objects.filter(ativo=True).first()
        else:
            try:
                plano = PlanoPremium.objects.get(id=plano_id, ativo=True)
            except PlanoPremium.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Plano {plano_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Plano: {plano.nome} - R$ {plano.preco}'))
        
        # Buscar usuário
        usuario_id = options.get('usuario_id')
        if not usuario_id:
            usuario = User.objects.filter(is_active=True).first()
        else:
            try:
                usuario = User.objects.get(id=usuario_id, is_active=True)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Usuário {usuario_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Usuário: {usuario.username}'))
        
        # Criar pagamento de teste
        self.stdout.write(self.style.WARNING('🔄 Criando pagamento de teste...'))
        
        try:
            # Criar pagamento
            import time
            unique_id = int(time.time() * 1000)  # Timestamp único
            pagamento = Pagamento.objects.create(
                usuario=usuario,
                valor=plano.preco,
                tipo='assinatura',
                descricao=f"Teste Checkout - {plano.nome}",
                payment_id=f'teste-checkout-{unique_id}'
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Pagamento criado: ID {pagamento.id}'))
            
            # Criar request simulado para checkout
            factory = RequestFactory()
            request = factory.get(f'/payments/checkout/{pagamento.id}/')
            request.user = usuario
            
            # Simular CSRF token
            from django.middleware.csrf import get_token
            get_token(request)
            
            self.stdout.write(self.style.WARNING('🔄 Testando página de checkout...'))
            
            # Chamar a view de checkout
            response = checkout_pagamento(request, pagamento.id)
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ Página de checkout carregada com sucesso!'))
                
                # Analisar contexto da resposta
                context = response.context_data if hasattr(response, 'context_data') else {}
                
                self.stdout.write(self.style.SUCCESS('📊 Contexto da página:'))
                self.stdout.write(f'   Pagamento: {context.get("pagamento")}')
                self.stdout.write(f'   Public Key: {context.get("public_key", "N/A")[:20]}...')
                self.stdout.write(f'   Preference ID: {context.get("preference_id", "N/A")}')
                self.stdout.write(f'   Init Point: {context.get("init_point", "N/A")}')
                self.stdout.write(f'   PIX Available: {context.get("pix_available", "N/A")}')
                
                # Verificar se PIX está disponível
                pix_available = context.get('pix_available', False)
                if pix_available:
                    self.stdout.write(self.style.SUCCESS('✅ PIX está disponível na página de checkout'))
                else:
                    self.stdout.write(self.style.WARNING('⚠️ PIX NÃO está disponível na página de checkout'))
                
                # Mostrar instruções para testar
                self.stdout.write(self.style.SUCCESS('🎯 Para testar o checkout:'))
                self.stdout.write('1. Acesse a página de checkout no navegador')
                self.stdout.write('2. Abra o console do navegador (F12)')
                self.stdout.write('3. Procure pelos logs detalhados que foram adicionados')
                self.stdout.write('4. Clique na opção PIX e observe os logs')
                self.stdout.write('5. Verifique se o QR Code é gerado')
                
                # Mostrar URL do checkout
                self.stdout.write(self.style.SUCCESS('🔗 URL do checkout:'))
                self.stdout.write(f'   http://localhost:8000/payments/checkout/{pagamento.id}/')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao carregar checkout: {response.status_code}'))
                self.stdout.write(f'Resposta: {response.content.decode()[:200]}...')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Resumo dos logs adicionados
        self.stdout.write(self.style.SUCCESS('📋 Logs adicionados ao console:'))
        self.stdout.write('✅ Inicialização do checkout')
        self.stdout.write('✅ Configurações carregadas')
        self.stdout.write('✅ Elementos do DOM verificados')
        self.stdout.write('✅ Opções de pagamento listadas')
        self.stdout.write('✅ Event listeners configurados')
        self.stdout.write('✅ Configuração do PIX')
        self.stdout.write('✅ Geração de PIX com logs detalhados')
        self.stdout.write('✅ Modal PIX com logs completos')
        self.stdout.write('✅ Verificação de status')
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de checkout com logs concluído!'))
        self.stdout.write(self.style.WARNING('💡 Agora acesse o checkout no navegador e verifique os logs no console!'))
