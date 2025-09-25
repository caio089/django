"""
Sistema de criptografia para dados sensíveis
Protege dados de pagamento, emails e informações pessoais
"""

import base64
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

class EncryptionManager:
    """
    Gerenciador de criptografia para dados sensíveis
    Usa AES-256 com chaves derivadas de senha (PBKDF2)
    """
    
    def __init__(self):
        self.key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.key)
    
    def _get_or_create_encryption_key(self):
        """
        Obtém ou cria chave de criptografia baseada em senha do Django
        """
        # Usar SECRET_KEY do Django como base para derivar chave
        password = settings.SECRET_KEY.encode()
        salt = b'judo_online_secure_salt_2024'  # Salt fixo para consistência
        
        # Derivar chave usando PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # 100k iterações para segurança
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, data):
        """
        Criptografa dados sensíveis
        
        Args:
            data (str): Dados a serem criptografados
            
        Returns:
            str: Dados criptografados em base64
        """
        if not data:
            return None
            
        try:
            # Converter para bytes se necessário
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Criptografar
            encrypted_data = self.cipher_suite.encrypt(data)
            
            # Converter para string base64
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Erro ao criptografar dados: {e}")
            raise EncryptionError(f"Falha na criptografia: {e}")
    
    def decrypt(self, encrypted_data):
        """
        Descriptografa dados sensíveis
        
        Args:
            encrypted_data (str): Dados criptografados em base64
            
        Returns:
            str: Dados descriptografados
        """
        if not encrypted_data:
            return None
            
        try:
            # Converter de base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # Descriptografar
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            
            # Converter para string
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Erro ao descriptografar dados: {e}")
            raise DecryptionError(f"Falha na descriptografia: {e}")
    
    def hash_sensitive_data(self, data):
        """
        Gera hash irreversível para dados sensíveis
        Usado para buscas sem expor dados originais
        
        Args:
            data (str): Dados a serem hasheados
            
        Returns:
            str: Hash SHA-256 dos dados
        """
        if not data:
            return None
            
        # Normalizar dados (lowercase, remover espaços)
        normalized_data = data.lower().strip()
        
        # Adicionar salt
        salted_data = f"judo_secure_{normalized_data}_2024"
        
        # Gerar hash SHA-256
        hash_object = hashlib.sha256(salted_data.encode('utf-8'))
        return hash_object.hexdigest()
    
    def verify_hash(self, data, hash_value):
        """
        Verifica se dados correspondem ao hash
        
        Args:
            data (str): Dados originais
            hash_value (str): Hash a ser verificado
            
        Returns:
            bool: True se corresponder
        """
        return self.hash_sensitive_data(data) == hash_value

class EmailEncryption:
    """
    Criptografia específica para emails
    Permite busca parcial sem expor email completo
    """
    
    def __init__(self):
        self.encryption = EncryptionManager()
    
    def encrypt_email(self, email):
        """
        Criptografa email completo
        
        Args:
            email (str): Email a ser criptografado
            
        Returns:
            dict: {
                'encrypted': str,  # Email criptografado
                'domain_hash': str,  # Hash do domínio para busca
                'partial': str  # Primeira parte do email para busca
            }
        """
        if not email:
            return None
            
        email_lower = email.lower().strip()
        
        # Criptografar email completo
        encrypted_email = self.encryption.encrypt(email_lower)
        
        # Extrair domínio e fazer hash
        domain = email_lower.split('@')[-1] if '@' in email_lower else ''
        domain_hash = self.encryption.hash_sensitive_data(domain)
        
        # Primeira parte do email para busca (sem criptografar)
        local_part = email_lower.split('@')[0] if '@' in email_lower else email_lower
        partial_email = local_part[:3] + '*' * (len(local_part) - 3) if len(local_part) > 3 else local_part
        
        return {
            'encrypted': encrypted_email,
            'domain_hash': domain_hash,
            'partial': partial_email
        }
    
    def decrypt_email(self, encrypted_data):
        """
        Descriptografa email
        
        Args:
            encrypted_data (str): Email criptografado
            
        Returns:
            str: Email descriptografado
        """
        return self.encryption.decrypt(encrypted_data)
    
    def search_by_domain(self, domain):
        """
        Busca emails por domínio sem descriptografar
        
        Args:
            domain (str): Domínio para busca
            
        Returns:
            str: Hash do domínio para query no banco
        """
        return self.encryption.hash_sensitive_data(domain.lower())

class PaymentDataEncryption:
    """
    Criptografia específica para dados de pagamento
    """
    
    def __init__(self):
        self.encryption = EncryptionManager()
    
    def encrypt_payment_data(self, data):
        """
        Criptografa dados sensíveis de pagamento
        
        Args:
            data (dict): Dados do pagamento
            
        Returns:
            dict: Dados com campos sensíveis criptografados
        """
        encrypted_data = data.copy()
        
        # Campos sensíveis a serem criptografados
        sensitive_fields = [
            'payer_email',
            'payer_name',
            'payer_phone',
            'payer_document',
            'card_holder_name',
            'card_number',
            'external_reference'
        ]
        
        for field in sensitive_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[f"{field}_encrypted"] = self.encryption.encrypt(str(encrypted_data[field]))
                # Remover campo original
                del encrypted_data[field]
        
        return encrypted_data
    
    def decrypt_payment_data(self, encrypted_data):
        """
        Descriptografa dados de pagamento
        
        Args:
            encrypted_data (dict): Dados criptografados
            
        Returns:
            dict: Dados descriptografados
        """
        decrypted_data = encrypted_data.copy()
        
        # Campos criptografados
        encrypted_fields = [
            'payer_email_encrypted',
            'payer_name_encrypted',
            'payer_phone_encrypted',
            'payer_document_encrypted',
            'card_holder_name_encrypted',
            'card_number_encrypted',
            'external_reference_encrypted'
        ]
        
        for field in encrypted_fields:
            if field in decrypted_data and decrypted_data[field]:
                # Nome do campo original
                original_field = field.replace('_encrypted', '')
                
                # Descriptografar
                decrypted_data[original_field] = self.encryption.decrypt(decrypted_data[field])
                
                # Remover campo criptografado
                del decrypted_data[field]
        
        return decrypted_data

class SecurePasswordManager:
    """
    Gerenciador seguro de senhas
    """
    
    @staticmethod
    def hash_password(password):
        """
        Gera hash seguro da senha usando PBKDF2
        
        Args:
            password (str): Senha em texto plano
            
        Returns:
            str: Hash da senha
        """
        # Usar hash SHA-256 com salt
        salt = os.urandom(32)
        
        # Derivar chave usando PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return f"{base64.urlsafe_b64encode(salt).decode()}:{key.decode()}"
    
    @staticmethod
    def verify_password(password, stored_hash):
        """
        Verifica senha contra hash armazenado
        
        Args:
            password (str): Senha em texto plano
            stored_hash (str): Hash armazenado
            
        Returns:
            bool: True se senha estiver correta
        """
        try:
            # Extrair salt e hash
            salt_b64, stored_key = stored_hash.split(':')
            salt = base64.urlsafe_b64decode(salt_b64.encode())
            
            # Derivar chave da senha fornecida
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
            
            # Comparar hashes
            return key.decode() == stored_key
            
        except Exception:
            return False

class EncryptionError(Exception):
    """Erro de criptografia"""
    pass

class DecryptionError(Exception):
    """Erro de descriptografia"""
    pass

# Instâncias globais para uso no sistema
encryption_manager = EncryptionManager()
email_encryption = EmailEncryption()
payment_encryption = PaymentDataEncryption()
password_manager = SecurePasswordManager()
