from django.core.management.base import BaseCommand
from payments.pix_generator import gerar_qr_code_pix_valido, validar_qr_code_pix

class Command(BaseCommand):
    help = 'Testa a geração de QR Code PIX'

    def handle(self, *args, **options):
        self.stdout.write('Testando geracao de QR Code PIX...')
        
        # Dados de teste (mesmos dados configurados na view)
        valor = 1.00
        chave_pix = "ccamposs2007@gmail.com"
        nome_beneficiario = "Dojo On"
        cidade = "Teresina"
        descricao = "Teste de pagamento"
        
        # Gerar QR Code
        pix_data = gerar_qr_code_pix_valido(
            valor=valor,
            chave_pix=chave_pix,
            nome_beneficiario=nome_beneficiario,
            cidade=cidade,
            descricao=descricao
        )
        
        if pix_data:
            self.stdout.write(self.style.SUCCESS('QR Code gerado com sucesso!'))
            self.stdout.write(f'Valor: R$ {pix_data["valor"]}')
            self.stdout.write(f'Chave PIX: {pix_data["chave_pix"]}')
            self.stdout.write(f'Beneficiario: {pix_data["nome_beneficiario"]}')
            self.stdout.write(f'Cidade: {pix_data["cidade"]}')
            self.stdout.write(f'QR Code (primeiros 100 chars): {pix_data["qr_code"][:100]}...')
            
            # Validar QR Code
            is_valid, message = validar_qr_code_pix(pix_data['qr_code'])
            
            if is_valid:
                self.stdout.write(self.style.SUCCESS(f'Validacao: {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'Validacao: {message}'))
        else:
            self.stdout.write(self.style.ERROR('Erro ao gerar QR Code PIX!'))
