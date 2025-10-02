from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, Pagamento, ConfiguracaoPagamento
from payments.views import gerar_pix_direto
from django.test import RequestFactory
import json
import base64
import qrcode
from io import BytesIO

class Command(BaseCommand):
    help = 'Testa a geração de QR Code PIX e verifica se está válido'

    def add_arguments(self, parser):
        parser.add_argument('--payment-id', type=int, help='ID do pagamento para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando geração de QR Code PIX...'))
        
        # Buscar pagamento
        payment_id = options.get('payment_id')
        if payment_id:
            try:
                pagamento = Pagamento.objects.get(id=payment_id)
            except Pagamento.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Pagamento {payment_id} não encontrado'))
                return
        else:
            # Buscar último pagamento
            pagamento = Pagamento.objects.filter(usuario__is_active=True).last()
            if not pagamento:
                self.stdout.write(self.style.ERROR('❌ Nenhum pagamento encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Testando pagamento ID: {pagamento.id}'))
        self.stdout.write(f'   Valor: R$ {pagamento.valor}')
        self.stdout.write(f'   Descrição: {pagamento.descricao}')
        
        # Criar request simulado
        factory = RequestFactory()
        request = factory.post(f'/payments/gerar-pix/{pagamento.id}/')
        request.user = pagamento.usuario
        
        # Simular CSRF token
        from django.middleware.csrf import get_token
        get_token(request)
        
        try:
            # Chamar a view de geração de PIX
            response = gerar_pix_direto(request, pagamento.id)
            
            if response.status_code == 200:
                data = json.loads(response.content.decode())
                
                if data.get('success'):
                    self.stdout.write(self.style.SUCCESS('✅ PIX gerado com sucesso!'))
                    
                    # Verificar dados do PIX
                    qr_code = data.get('qr_code')
                    qr_code_base64 = data.get('qr_code_base64')
                    payment_id_mp = data.get('payment_id')
                    
                    self.stdout.write(f'📊 Dados do PIX:')
                    self.stdout.write(f'   Payment ID MP: {payment_id_mp}')
                    self.stdout.write(f'   QR Code: {qr_code[:50] if qr_code else "None"}...')
                    self.stdout.write(f'   QR Code Base64: {"Sim" if qr_code_base64 else "Não"}')
                    
                    # Verificar se o QR Code é válido
                    if qr_code:
                        self.stdout.write(self.style.WARNING('🔍 Verificando QR Code...'))
                        
                        try:
                            # Tentar decodificar o QR Code
                            qr = qrcode.QRCode(version=1, box_size=10, border=5)
                            qr.add_data(qr_code)
                            qr.make(fit=True)
                            
                            # Criar imagem do QR Code
                            img = qr.make_image(fill_color="black", back_color="white")
                            
                            # Salvar em buffer
                            buffer = BytesIO()
                            img.save(buffer, format='PNG')
                            buffer.seek(0)
                            
                            # Converter para base64
                            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
                            
                            self.stdout.write(self.style.SUCCESS('✅ QR Code gerado com sucesso!'))
                            self.stdout.write(f'   Tamanho da imagem: {len(buffer.getvalue())} bytes')
                            
                            # Verificar se o QR Code contém dados PIX válidos
                            if 'pix' in qr_code.lower() or '000201' in qr_code:
                                self.stdout.write(self.style.SUCCESS('✅ QR Code contém dados PIX válidos'))
                            else:
                                self.stdout.write(self.style.WARNING('⚠️ QR Code pode não conter dados PIX válidos'))
                                self.stdout.write(f'   Conteúdo: {qr_code[:100]}...')
                            
                            # Salvar QR Code para teste
                            with open('qr_code_test.png', 'wb') as f:
                                f.write(buffer.getvalue())
                            self.stdout.write(self.style.SUCCESS('💾 QR Code salvo como qr_code_test.png'))
                            
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'❌ Erro ao processar QR Code: {e}'))
                    
                    else:
                        self.stdout.write(self.style.ERROR('❌ QR Code não foi gerado'))
                
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Erro ao gerar PIX: {data.get("error")}'))
                    
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro HTTP: {response.status_code}'))
                self.stdout.write(f'Resposta: {response.content.decode()[:200]}...')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de QR Code concluído!'))




