from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'input'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')
        
        if email and senha:
            try:
                # Buscar usuário por email
                user = User.objects.get(email=email)
                
                # Verificar se o usuário está ativo
                if not user.is_active:
                    raise forms.ValidationError('Esta conta está desativada.')
                
                # Verificar se tem senha definida
                if not user.has_usable_password():
                    raise forms.ValidationError('Esta conta não possui senha definida.')
                
                # Tentar autenticar
                auth_user = authenticate(username=user.username, password=senha)
                if auth_user is None:
                    raise forms.ValidationError('Email ou senha inválidos.')
                
                # Verificar se é um usuário real (não de teste)
                if user.email in ['teste@exemplo.com', 'admin@exemplo.com']:
                    raise forms.ValidationError('Acesso negado para contas de teste.')
                
                cleaned_data['user'] = auth_user
                
            except User.DoesNotExist:
                raise forms.ValidationError('Email não cadastrado.')
            except Exception as e:
                raise forms.ValidationError('Erro na autenticação.')
        
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