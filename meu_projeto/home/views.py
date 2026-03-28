from django.contrib.auth import login
from meu_projeto.redirect_utils import redirect_to_frontend
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile
import logging
import json

logger = logging.getLogger(__name__)


def home(request):
    return redirect_to_frontend('/')


def login_view(request):
    return redirect_to_frontend('/login')


def register_view(request):
    return redirect_to_frontend('/register')


def selecionar_faixa_view(request):
    return redirect_to_frontend('/index')


def processar_selecao_faixa(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})

    try:
        dados_faixa = json.loads(request.body)
        faixa = dados_faixa.get('faixa')

        if not faixa:
            return JsonResponse({'success': False, 'error': 'Faixa não fornecida'})

        request.session['faixa_selecionada'] = faixa

        faixas_urls = {
            'cinza': '/pagina/1', 'azul': '/pagina/2', 'amarela': '/pagina/3',
            'laranja': '/pagina/4', 'verde': '/pagina/5', 'roxa': '/pagina/6',
            'marrom': '/pagina/7',
        }

        url_destino = faixas_urls.get(faixa.lower())
        if url_destino:
            return JsonResponse({
                'success': True,
                'message': f'Faixa {faixa} selecionada com sucesso!',
                'redirect_url': url_destino,
            })
        return JsonResponse({'success': False, 'error': 'Faixa não reconhecida'})
    except Exception as e:
        logger.error(f"Erro ao processar seleção de faixa: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def processar_cadastro_completo(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})

    try:
        dados_usuario = json.loads(request.body)
        nome = dados_usuario.get('nome')
        idade = dados_usuario.get('idade')
        email = dados_usuario.get('email')
        senha = dados_usuario.get('senha')
        faixa = dados_usuario.get('faixa')

        if not all([nome, idade, email, senha, faixa]):
            return JsonResponse({'success': False, 'error': 'Todos os campos são obrigatórios'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Este email já está em uso'})

        user = User.objects.create_user(
            username=email, email=email, password=senha,
            first_name=nome.split(' ')[0] if nome else '',
            last_name=' '.join(nome.split(' ')[1:]) if nome and len(nome.split(' ')) > 1 else '',
        )

        try:
            profile = Profile.objects.get(user=user)
            profile.nome = nome
            profile.idade = idade
            profile.faixa = faixa
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, nome=nome, idade=idade, faixa=faixa)

        login(request, user)

        return JsonResponse({
            'success': True,
            'message': f'Cadastro realizado com sucesso! Bem-vindo, {nome}!',
            'redirect_url': '/dashboard/',
        })
    except Exception as e:
        logger.error(f"Erro no cadastro completo: {e}")
        return JsonResponse({'success': False, 'error': str(e)})
