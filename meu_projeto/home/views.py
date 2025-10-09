from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import EmailLoginForm, RegisterForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    form = EmailLoginForm()
    register_form = RegisterForm()
    show_register = False
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })

def login_view(request):
    # Se já estiver logado, redirecionar para index
    if request.user.is_authenticated:
        return redirect('index')
    
    form = EmailLoginForm(request.POST or None)
    register_form = RegisterForm()
    show_register = False
    
    if request.method == 'POST':
        logger.info(f"Tentativa de login via POST para: {request.POST.get('email', 'N/A')}")
        
        if form.is_valid():
            user = form.cleaned_data['user']
            logger.info(f"Login bem-sucedido para: {user.email}")
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.email}!')
            return redirect('index')
        else:
            logger.warning(f"Formulário inválido. Erros: {form.errors}")
            # Mostrar erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(f"Erro de validação - {field}: {error}")
                    messages.error(request, error)
    
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })


def register_view(request):
    # Se já estiver logado e tentar acessar página de registro, fazer logout primeiro
    if request.user.is_authenticated:
        from django.contrib.auth import logout
        logout(request)
        messages.info(request, 'Você foi desconectado para criar uma nova conta.')
    
    form = EmailLoginForm()
    register_form = RegisterForm(request.POST or None)
    show_register = True
    
    if request.method == 'POST':
        if register_form.is_valid():
            nome = register_form.cleaned_data['nome']
            idade = register_form.cleaned_data['idade']
            faixa = register_form.cleaned_data['faixa']
            email = register_form.cleaned_data['email']
            senha = register_form.cleaned_data['senha']
            
            # Criar usuário
            user = User.objects.create_user(username=email, email=email, password=senha)
            Profile.objects.create(user=user, nome=nome, idade=idade, faixa=faixa)
            
            # Fazer login automaticamente após registro
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {nome}!')
            return redirect('index')
        else:
            # Mostrar erros do formulário
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })

def teste_login_view(request):
    """
    View de teste para login sem JavaScript
    """
    form = EmailLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f'Login realizado com sucesso! Bem-vindo, {user.email}')
            return redirect('index')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    return render(request, 'home/teste_login.html', {'form': form})  

