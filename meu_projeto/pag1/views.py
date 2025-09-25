from django.shortcuts import render, redirect
from django.contrib import messages
from payments.views import verificar_acesso_premium

# Create your views here.

def pagina1(request):
    # Verificar se usuário está logado
    if not request.user.is_authenticated:
        messages.warning(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login')
    
    # Verificar acesso premium
    tem_acesso, assinatura = verificar_acesso_premium(request.user)
    
    if not tem_acesso:
        messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
        return redirect('payments:planos')
    
    return render(request, 'pag1/pagina1.html', {
        'assinatura': assinatura
    })  

