from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento
import time

class Command(BaseCommand):
    help = 'Testa se a URL de checkout está funcionando'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando URL de checkout...'))
        
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
            descricao=f"Teste URL - {plano.nome}",
            payment_id=f'teste-url-{unique_id}'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Pagamento criado: ID {pagamento.id}'))
        
        # Testar com cliente Django
        client = Client()
        
        # Fazer login
        client.force_login(usuario)
        
        # Testar URL de checkout
        url = f'/payments/checkout/{pagamento.id}/'
        self.stdout.write(f'🔗 Testando URL: {url}')
        
        try:
            response = client.get(url)
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ URL funcionando!'))
                self.stdout.write(f'   Status: {response.status_code}')
                self.stdout.write(f'   Content-Type: {response.get("Content-Type", "N/A")}')
                
                # Verificar se o template está sendo renderizado
                content = response.content.decode()
                if 'Checkout - Pagamento' in content:
                    self.stdout.write(self.style.SUCCESS('✅ Template renderizado corretamente'))
                else:
                    self.stdout.write(self.style.WARNING('⚠️ Template pode não estar sendo renderizado'))
                
                # Verificar se PIX está disponível
                if 'PIX' in content:
                    self.stdout.write(self.style.SUCCESS('✅ Opção PIX encontrada no template'))
                else:
                    self.stdout.write(self.style.WARNING('⚠️ Opção PIX não encontrada'))
                
            elif response.status_code == 404:
                self.stdout.write(self.style.ERROR('❌ Erro 404 - Página não encontrada'))
                self.stdout.write('   Verifique se as URLs estão configuradas corretamente')
                
            elif response.status_code == 500:
                self.stdout.write(self.style.ERROR('❌ Erro 500 - Erro interno do servidor'))
                self.stdout.write(f'   Resposta: {response.content.decode()[:200]}...')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro HTTP: {response.status_code}'))
                self.stdout.write(f'   Resposta: {response.content.decode()[:200]}...')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao testar URL: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de URL concluído!'))
        self.stdout.write(f'💡 Acesse: http://localhost:8000{url}')



