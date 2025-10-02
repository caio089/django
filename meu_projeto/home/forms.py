from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'input'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')
        
        logger.info(f"Tentativa de login para email: {email}")
        
        if email and senha:
            try:
                # Buscar usuário por email
                logger.info(f"Buscando usuário com email: {email}")
                user = User.objects.get(email=email)
                logger.info(f"Usuário encontrado: {user.username}, ativo: {user.is_active}")
                
                # Verificar se o usuário está ativo
                if not user.is_active:
                    logger.warning(f"Usuário {email} está desativado")
                    raise forms.ValidationError('Esta conta está desativada.')
                
                # Verificar se tem senha definida
                if not user.has_usable_password():
                    logger.warning(f"Usuário {email} não possui senha definida")
                    raise forms.ValidationError('Esta conta não possui senha definida.')
                
                # Tentar autenticar
                logger.info(f"Tentando autenticar usuário: {user.username}")
                auth_user = authenticate(username=user.username, password=senha)
                logger.info(f"Resultado da autenticação: {auth_user is not None}")
                
                if auth_user is None:
                    logger.warning(f"Falha na autenticação para {email}")
                    raise forms.ValidationError('Email ou senha inválidos.')
                
                # Verificar se é um usuário real (não de teste)
                if user.email in ['teste@exemplo.com', 'admin@exemplo.com']:
                    logger.warning(f"Acesso negado para conta de teste: {email}")
                    raise forms.ValidationError('Acesso negado para contas de teste.')
                
                logger.info(f"Login bem-sucedido para {email}")
                cleaned_data['user'] = auth_user
                
            except User.DoesNotExist:
                logger.warning(f"Email não cadastrado: {email}")
                raise forms.ValidationError('Email não cadastrado.')
            except forms.ValidationError:
                # Re-raise validation errors
                raise
            except Exception as e:
                logger.error(f"Erro inesperado na autenticação para {email}: {e}", exc_info=True)
                raise forms.ValidationError(f'Erro na autenticação: {str(e)}')
        
        return cleaned_data 

class RegisterForm(forms.Form):
    nome = forms.CharField(label='Nome completo', max_length=150)
    idade = forms.IntegerField(label='Idade', min_value=1, max_value=120)
    faixa = forms.ChoiceField(label='Faixa', choices=[
        ('branca', 'Branca'),
        ('cinza', 'Cinza'),
        ('azul', 'Azul'),
        ('amarela', 'Amarela'),
        ('laranja', 'Laranja'),
        ('verde', 'Verde'),
        ('roxa', 'Roxa'),
        ('marrom', 'Marrom'),
        ('preta', 'Preta'),
    ])
    email = forms.EmailField(label='Email', max_length=254)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com este email.')
        return email 