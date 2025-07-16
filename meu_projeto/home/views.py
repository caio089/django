from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import EmailLoginForm, RegisterForm

def home(request):
    return render(request, 'home/home.html')


def login_view(request):
    form = EmailLoginForm(request.POST or None)
    register_form = RegisterForm()
    show_register = False
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('index')
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
            user = User.objects.create_user(username=email, email=email, password=senha)
            Profile.objects.create(user=user, nome=nome, idade=idade, faixa=faixa)
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    return render(request, 'home/home.html', {
        'form': form,
        'register_form': register_form,
        'show_register': show_register
    })  

