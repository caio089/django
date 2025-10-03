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
        
        # Dados do PIX no formato EMV
        pix_data = {
            "00": "01",  # Payload Format Indicator
            "26": {      # Merchant Account Information
                "00": "br.gov.bcb.pix",  # GUI
                "01": chave_pix,         # Chave PIX
            },
            "52": "0000",  # Merchant Category Code
            "53": "986",   # Transaction Currency (BRL)
            "54": valor_formatado,  # Transaction Amount
            "58": "BR",    # Country Code
            "59": nome_beneficiario,  # Merchant Name
            "60": cidade,  # Merchant City
            "62": {        # Additional Data Field Template
                "05": descricao  # Reference Label
            }
        }
        
        # Converter para string EMV
        emv_string = ""
        for tag, value in pix_data.items():
            if isinstance(value, dict):
                # Construir string do dicionário aninhado
                nested_string = ""
                for sub_tag, sub_value in value.items():
                    sub_value_str = str(sub_value)
                    nested_string += f"{sub_tag}{len(sub_value_str):02d}{sub_value_str}"
                
                # Adicionar tag pai com tamanho do conteúdo aninhado
                emv_string += f"{tag}{len(nested_string):02d}{nested_string}"
            else:
                value_str = str(value)
                emv_string += f"{tag}{len(value_str):02d}{value_str}"
        
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
