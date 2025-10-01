from django.core.management.base import BaseCommand
from payments.pix_generator import gerar_qr_code_pix_valido, validar_qr_code_pix
import re

class Command(BaseCommand):
    help = 'Testa detalhadamente a geração de QR Code PIX'

    def handle(self, *args, **options):
        self.stdout.write('Testando geracao detalhada de QR Code PIX...')
        
        # Dados de teste
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
            
            qr_code = pix_data['qr_code']
            self.stdout.write(f'\nQR Code completo: {qr_code}')
            self.stdout.write(f'Tamanho do QR Code: {len(qr_code)} caracteres')
            
            # Análise detalhada
            self.stdout.write('\n=== ANÁLISE DETALHADA ===')
            
            # Verificar estrutura básica
            if qr_code.startswith('000201'):
                self.stdout.write('OK: Inicia com 000201 (correto)')
            else:
                self.stdout.write('ERRO: Nao inicia com 000201')
            
            # Verificar se termina com CRC
            if re.search(r'6304[0-9A-F]{4}$', qr_code):
                crc_match = re.search(r'6304([0-9A-F]{4})$', qr_code)
                crc_value = crc_match.group(1) if crc_match else "N/A"
                self.stdout.write(f'OK: Termina com CRC: {crc_value}')
            else:
                self.stdout.write('ERRO: Nao termina com CRC valido')
            
            # Verificar elementos obrigatórios
            elementos = {
                '00': 'Payload Format Indicator',
                '26': 'Merchant Account Information',
                '52': 'Merchant Category Code',
                '53': 'Transaction Currency',
                '54': 'Transaction Amount',
                '58': 'Country Code',
                '59': 'Merchant Name',
                '60': 'Merchant City',
                '62': 'Additional Data Field Template'
            }
            
            self.stdout.write('\n=== ELEMENTOS OBRIGATORIOS ===')
            for tag, descricao in elementos.items():
                pattern = f"{tag}[0-9]{{2}}"
                if re.search(pattern, qr_code):
                    self.stdout.write(f'OK {tag}: {descricao}')
                else:
                    self.stdout.write(f'ERRO {tag}: {descricao} - NAO ENCONTRADO')
            
            # Validar QR Code
            is_valid, message = validar_qr_code_pix(qr_code)
            
            if is_valid:
                self.stdout.write(self.style.SUCCESS(f'\nOK VALIDACAO: {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'\nERRO VALIDACAO: {message}'))
                
        else:
            self.stdout.write(self.style.ERROR('Erro ao gerar QR Code PIX!'))
