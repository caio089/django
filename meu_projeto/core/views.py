from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import Profile

# Create your views here.

@login_required(login_url='login')
def index(request):
    nome = None
    faixa = None
    assinatura = None
    
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(
                user=request.user,
                nome=request.user.get_full_name() or request.user.username,
                idade=18,
                faixa='branca'
            )
        nome = profile.nome
        faixa = profile.get_faixa_display()
        
        # Verificar se tem assinatura ativa
        from payments.views import verificar_acesso_premium
        tem_acesso, assinatura = verificar_acesso_premium(request.user)
        
        # Verificar se tem assinatura cancelada recentemente
        assinatura_cancelada = None
        if not assinatura:
            from payments.models import Assinatura
            assinatura_cancelada = Assinatura.objects.filter(
                usuario=request.user,
                status='cancelada'
            ).order_by('-data_cancelamento').first()
        
        # Verificar se veio do pagamento (parâmetro na URL)
        from_payment = request.GET.get('from_payment', False)
        new_subscription = None
        if from_payment and assinatura:
            # Buscar a assinatura mais recente
            new_subscription = Assinatura.objects.filter(
                usuario=request.user,
                status='ativa'
            ).order_by('-data_inicio').first()
        
    return render(request, 'index.html', {
        'nome': nome, 
        'faixa': faixa,
        'assinatura': assinatura,
        'assinatura_cancelada': assinatura_cancelada,
        'from_payment': from_payment,
        'new_subscription': new_subscription
    })

def logout_view(request):
    logout(request)
    return redirect('login')  # Substitua 'login' pelo nome da sua url de login