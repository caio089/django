from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from home.models import Profile
from home.trial import trial_delta

from datetime import timedelta

# Create your views here.

@login_required(login_url='login')
def index(request):
    nome = None
    faixa = None
    assinatura = None
    assinatura_cancelada = None
    from_payment = False
    new_subscription = None
    trial_expirado = False
    trial_dias_restantes = 0
    trial_ativo = False
    
    try:
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                # Se não existir profile, criar com valores padrão
                # O nome será definido durante o registro
                profile = Profile.objects.create(
                    user=request.user,
                    nome=request.user.username,  # Temporário, será atualizado no registro
                    idade=18,
                    faixa='branca'
                )
            
            # Usar sempre o nome do profile (que foi definido no registro)
            nome = profile.nome
            faixa = profile.get_faixa_display()
            
            # Verificar se tem assinatura ativa
            try:
                from payments.views import verificar_acesso_premium
                tem_acesso, assinatura = verificar_acesso_premium(request.user)
            except Exception as e:
                # Se houver erro ao verificar assinatura, continuar sem ela
                print(f"Erro ao verificar assinatura: {e}")
                assinatura = None
                
            # Garantir inicialização do trial se ainda não existir (boas-vindas)
            try:
                if not getattr(profile, "trial_inicio", None):
                    now = timezone.now()
                    profile.trial_inicio = now
                    profile.trial_fim = now + trial_delta()
                    profile.save(update_fields=["trial_inicio", "trial_fim"])
            except Exception:
                pass

            # Calcular status do trial (ativo/expirado e dias restantes)
            try:
                trial_dias_restantes = profile.dias_trial_restantes()
                trial_ativo = bool(profile.trial_inicio) and profile.is_trial_ativo() and not assinatura
                trial_expirado = bool(profile.trial_inicio) and not profile.is_trial_ativo() and not assinatura
                trial_fim_iso = profile.trial_fim.isoformat() if profile.trial_fim else None
                trial_inicio_iso = profile.trial_inicio.isoformat() if profile.trial_inicio else None
            except Exception as e:
                trial_expirado = False
                trial_dias_restantes = 0
                trial_ativo = False
                trial_fim_iso = None
                trial_inicio_iso = None
            
            # Verificar se tem assinatura cancelada recentemente
            if not assinatura:
                try:
                    from payments.models import Assinatura
                    assinatura_cancelada = Assinatura.objects.filter(
                        usuario=request.user,
                        status='cancelada'
                    ).order_by('-data_cancelamento').first()
                except Exception as e:
                    print(f"Erro ao verificar assinatura cancelada: {e}")
                    assinatura_cancelada = None
            
            # Verificar se veio do pagamento (parâmetro na URL)
            from_payment = request.GET.get('from_payment', False)
            if from_payment and assinatura:
                try:
                    from payments.models import Assinatura
                    # Buscar a assinatura mais recente
                    new_subscription = Assinatura.objects.filter(
                        usuario=request.user,
                        status='ativa'
                    ).order_by('-data_inicio').first()
                except Exception as e:
                    print(f"Erro ao buscar nova assinatura: {e}")
                    new_subscription = None
    except Exception as e:
        # Log do erro para debug
        print(f"Erro geral na view index: {e}")
        import traceback
        traceback.print_exc()
        
    return render(request, 'index.html', {
        'nome': nome, 
        'faixa': faixa,
        'assinatura': assinatura,
        'assinatura_cancelada': assinatura_cancelada,
        'from_payment': from_payment,
        'new_subscription': new_subscription,
        'trial_expirado': trial_expirado,
        'trial_dias_restantes': trial_dias_restantes,
        'trial_ativo': trial_ativo,
        'trial_fim_iso': trial_fim_iso,
        'trial_inicio_iso': trial_inicio_iso
    })

def logout_view(request):
    logout(request)
    return redirect('login')  # Substitua 'login' pelo nome da sua url de login