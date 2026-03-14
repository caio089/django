"""
API JSON para o frontend React (login, register, user info).
"""
import json
import logging
from django.http import JsonResponse
from django.db import OperationalError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import EmailLoginForm, RegisterForm
from .models import Profile
from .trial import trial_delta

logger = logging.getLogger(__name__)


def _get_user_data(user):
    """Retorna dados do usuário para o frontend."""
    if not user or not user.is_authenticated:
        return None
    try:
        profile = Profile.objects.get(user=user)
        trial_ativo = bool(profile.trial_inicio) and profile.is_trial_ativo()
        trial_expirado = bool(profile.trial_inicio) and not profile.is_trial_ativo()
        return {
            'id': user.id,
            'email': user.email,
            'nome': profile.nome,
            'faixa': profile.get_faixa_display(),
            'faixa_value': profile.faixa,
            'idade': profile.idade,
            'trial_ativo': trial_ativo,
            'trial_expirado': trial_expirado,
            'trial_fim': profile.trial_fim.isoformat() if profile.trial_fim else None,
            'trial_inicio': profile.trial_inicio.isoformat() if profile.trial_inicio else None,
            'conta_premium': profile.conta_premium,
        }
    except Profile.DoesNotExist:
        return {
            'id': user.id,
            'email': user.email,
            'nome': user.username or user.email,
            'faixa': 'Branca',
            'faixa_value': 'branca',
            'idade': 18,
            'trial_ativo': False,
            'trial_expirado': False,
            'trial_fim': None,
            'trial_inicio': None,
            'conta_premium': False,
        }


@ensure_csrf_cookie
@require_http_methods(['GET'])
def api_csrf(request):
    """Retorna token CSRF para uso em requisições POST."""
    return JsonResponse({'csrf': 'ok'})


@csrf_exempt
@require_http_methods(['POST'])
def api_login(request):
    """Login via JSON. Espera JSON: { email, senha }."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    try:
        form = EmailLoginForm(data)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                if not profile.trial_inicio:
                    now = timezone.now()
                    profile.trial_inicio = now
                    profile.trial_fim = now + trial_delta()
                    profile.save()
            except Exception as e:
                logger.error(f"Erro ao iniciar trial: {e}")

            return JsonResponse({
                'success': True,
                'redirect': '/index',
                'user': _get_user_data(user),
            })
        errors = dict(form.errors)
        first_error = list(errors.values())[0][0] if errors else 'Erro ao fazer login'
        return JsonResponse({'success': False, 'error': first_error}, status=400)
    except OperationalError:
        logger.exception('Erro de conexão com banco em api_login')
        return JsonResponse({
            'success': False,
            'error': 'Banco de dados indisponível. Verifique a conexão com o Supabase.'
        }, status=503)


@csrf_exempt
@require_http_methods(['POST'])
def api_register(request):
    """Registro via JSON."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    try:
        form = RegisterForm(data)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            idade = form.cleaned_data['idade']
            faixa = form.cleaned_data['faixa']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'error': 'Já existe conta com este email'}, status=400)

            user = User.objects.create_user(username=email, email=email, password=senha)
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={'nome': nome, 'idade': idade, 'faixa': faixa}
            )
            if not _:
                profile.nome = nome
                profile.idade = idade
                profile.faixa = faixa
                profile.save(update_fields=['nome', 'idade', 'faixa'])

            now = timezone.now()
            profile.trial_inicio = now
            profile.trial_fim = now + trial_delta()
            profile.save()

            login(request, user)
            return JsonResponse({
                'success': True,
                'redirect': '/selecionar-faixa',
                'user': _get_user_data(user),
            })

        errors = dict(form.errors)
        first_error = list(errors.values())[0][0] if errors else 'Erro ao cadastrar'
        return JsonResponse({'success': False, 'error': first_error}, status=400)
    except OperationalError:
        logger.exception('Erro de conexão com banco em api_register')
        return JsonResponse({
            'success': False,
            'error': 'Banco de dados indisponível. Verifique a conexão com o Supabase.'
        }, status=503)


@csrf_exempt
@require_http_methods(['POST'])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect': '/'})


@require_http_methods(['GET'])
def api_me(request):
    """Retorna dados do usuário logado."""
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False})
    return JsonResponse({
        'authenticated': True,
        'user': _get_user_data(request.user),
    })
