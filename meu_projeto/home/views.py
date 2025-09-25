from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import EmailLoginForm, RegisterForm

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
    form = EmailLoginForm(request.POST or None)
    register_form = RegisterForm()
    show_register = False
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.email}! Login realizado com sucesso.')
            return redirect('index')  # Redireciona para o core (index)
        else:
            messages.error(request, 'Email ou senha inválidos.')
    
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })


def register_view(request):
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
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            Profile.objects.create(user=user, nome=nome, idade=idade, faixa=faixa)
            login(request, user)  # Login automático após registro
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {nome}!')
            return redirect('index')  # Redireciona para o core (index)
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })  

