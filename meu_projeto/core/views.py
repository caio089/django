from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import Profile

# Create your views here.

@login_required(login_url='login')
def index(request):
    nome = None
    faixa = None
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
    return render(request, 'index.html', {'nome': nome, 'faixa': faixa})

def logout_view(request):
    logout(request)
    return redirect('login')  # Substitua 'login' pelo nome da sua url de login