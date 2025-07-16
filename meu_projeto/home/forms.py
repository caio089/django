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
                user = User.objects.get(email=email)
            except Exception:
                raise forms.ValidationError('Email ou senha inválidos.')
            user = authenticate(username=user.username, password=senha)
            if user is None:
                raise forms.ValidationError('Email ou senha inválidos.')
            cleaned_data['user'] = user
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