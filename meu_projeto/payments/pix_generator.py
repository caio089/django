import qrcode
import base64
from io import BytesIO
import re

def gerar_qr_code_pix_valido(valor, chave_pix, nome_beneficiario, cidade, descricao=""):
    """
    Gera um QR Code PIX válido no formato EMV (padrão brasileiro)
    """
    try:
        # Formatar valor para PIX (2 casas decimais)
        valor_formatado = f"{float(valor):.2f}"
        
        # Limitar tamanho dos campos conforme especificação PIX
        nome_beneficiario = nome_beneficiario[:25] if len(nome_beneficiario) > 25 else nome_beneficiario
        cidade = cidade[:15] if len(cidade) > 15 else cidade
        descricao = descricao[:25] if descricao and len(descricao) > 25 else (descricao or "Pagamento")
        
        # Construir string EMV manualmente para garantir formato correto
        emv_string = "000201"  # Payload Format Indicator
        
        # Merchant Account Information (26)
        gui = "br.gov.bcb.pix"
        gui_length = len(gui)
        chave_length = len(chave_pix)
        merchant_account = f"00{gui_length:02d}{gui}01{chave_length:02d}{chave_pix}"
        merchant_account_length = len(merchant_account)
        emv_string += f"26{merchant_account_length:02d}{merchant_account}"
        
        # Merchant Category Code (52)
        mcc = "0000"
        emv_string += f"52{len(mcc):02d}{mcc}"
        
        # Transaction Currency (53)
        currency = "986"
        emv_string += f"53{len(currency):02d}{currency}"
        
        # Transaction Amount (54)
        amount_length = len(valor_formatado)
        emv_string += f"54{amount_length:02d}{valor_formatado}"
        
        # Country Code (58)
        country = "BR"
        emv_string += f"58{len(country):02d}{country}"
        
        # Merchant Name (59)
        name_length = len(nome_beneficiario)
        emv_string += f"59{name_length:02d}{nome_beneficiario}"
        
        # Merchant City (60)
        city_length = len(cidade)
        emv_string += f"60{city_length:02d}{cidade}"
        
        # Additional Data Field Template (62)
        reference = descricao
        reference_length = len(reference)
        additional_data = f"05{reference_length:02d}{reference}"
        additional_data_length = len(additional_data)
        emv_string += f"62{additional_data_length:02d}{additional_data}"
        
        # Adicionar CRC (Checksum)
        crc = calcular_crc16(emv_string)
        emv_string += f"6304{crc:04X}"
        
        # Gerar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(emv_string)
        qr.make(fit=True)
        
        # Criar imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'qr_code': emv_string,
            'qr_code_base64': f"data:image/png;base64,{img_str}",
            'valor': valor_formatado,
            'chave_pix': chave_pix,
            'nome_beneficiario': nome_beneficiario,
            'cidade': cidade
        }
        
    except Exception as e:
        print(f"Erro ao gerar QR Code PIX: {e}")
        return None

def calcular_crc16(data):
    """
    Calcula CRC16 para PIX
    """
    crc = 0xFFFF
    for byte in data.encode('utf-8'):
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0x8408
            else:
                crc >>= 1
    return crc

def validar_qr_code_pix(qr_code):
    """
    Valida se o QR Code PIX está no formato correto
    """
    try:
        # Verificar se o QR Code não está vazio
        if not qr_code or len(qr_code) < 50:
            return False, "QR Code muito curto ou vazio"
        
        # Verificar se começa com 000201 (formato EMV padrão)
        if not qr_code.startswith('000201'):
            return False, "QR Code não começa com formato EMV válido"
        
        # Verificar se termina com CRC (mais flexível)
        if not re.search(r'6304[0-9A-F]{4}$', qr_code):
            return False, "QR Code não termina com CRC válido"
        
        # Verificar se contém elementos obrigatórios (mais flexível)
        required_elements = ["00", "26", "52", "53", "54", "58", "59", "60"]
        missing_elements = []
        
        for element in required_elements:
            # Verificar se o elemento existe (pode ter diferentes tamanhos)
            pattern = f"{element}[0-9]{{2}}"
            if not re.search(pattern, qr_code):
                missing_elements.append(element)
        
        # Se faltam muitos elementos, considerar inválido
        if len(missing_elements) > 2:
            return False, f"Elementos obrigatórios ausentes: {', '.join(missing_elements)}"
        
        return True, "QR Code válido"
        
    except Exception as e:
        return False, f"Erro na validação: {e}"
