from django.shortcuts import render, redirect
from django.contrib.auth import login
from meu_projeto.redirect_utils import redirect_to_frontend
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile
from .forms import EmailLoginForm, RegisterForm
import logging
import json

logger = logging.getLogger(__name__)

def home(request):
    """Redireciona para o React (Landing em /)"""
    return redirect_to_frontend('/')

def login_view(request):
    """Redireciona para o React (Landing em /login)"""
    return redirect_to_frontend('/login')


def register_view(request):
    """Redireciona para o React (Landing em /register)"""
    return redirect_to_frontend('/register')

def teste_login_view(request):
    """Redireciona para o React (Landing em /login)"""
    return redirect_to_frontend('/login')




def selecionar_faixa_view(request):
    """Redireciona para o React (Dashboard em /index)"""
    return redirect_to_frontend('/index')




def processar_selecao_faixa(request):
    """
    View para processar a seleção de faixa do usuário
    """
    if request.method == 'POST':
        try:
            # Dados da faixa selecionada
            dados_faixa = json.loads(request.body)
            faixa = dados_faixa.get('faixa')
            
            if not faixa:
                return JsonResponse({'success': False, 'error': 'Faixa não fornecida'})
            
            # Salvar faixa na sessão
            request.session['faixa_selecionada'] = faixa
            
            # Mapeamento de faixas para URLs (React)
            faixas_urls = {
                'cinza': '/pagina/1',
                'azul': '/pagina/2',
                'amarela': '/pagina/3',
                'laranja': '/pagina/4',
                'verde': '/pagina/5',
                'roxa': '/pagina/6',
                'marrom': '/pagina/7'
            }
            
            url_destino = faixas_urls.get(faixa.lower())
            if url_destino:
                logger.info(f"🥋 Faixa selecionada: {faixa} -> {url_destino}")
                return JsonResponse({
                    'success': True,
                    'message': f'Faixa {faixa} selecionada com sucesso!',
                    'redirect_url': url_destino
                })
            else:
                return JsonResponse({'success': False, 'error': 'Faixa não reconhecida'})
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar seleção de faixa: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


def processar_cadastro_completo(request):
    """
    Processa o cadastro completo do usuário com dados do Google + formulário
    """
    if request.method != 'POST':
        logger.warning("⚠️ Método não permitido para cadastro completo")
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        logger.info("📝 Iniciando processamento de cadastro completo...")
        
        # Dados do usuário
        dados_usuario = json.loads(request.body)
        nome = dados_usuario.get('nome')
        idade = dados_usuario.get('idade')
        email = dados_usuario.get('email')
        senha = dados_usuario.get('senha')
        faixa = dados_usuario.get('faixa')
        
        logger.info(f"📧 Dados recebidos - Nome: {nome}, Email: {email}, Idade: {idade}, Faixa: {faixa}")
        
        # Validar dados obrigatórios
        if not all([nome, idade, email, senha, faixa]):
            return JsonResponse({'success': False, 'error': 'Todos os campos são obrigatórios'})
        
        # Verificar se email já existe
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Este email já está em uso'})
        
        # Criar usuário
        logger.info("👤 Criando usuário...")
        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome.split(' ')[0] if nome else '',
            last_name=' '.join(nome.split(' ')[1:]) if nome and len(nome.split(' ')) > 1 else ''
        )
        
        logger.info(f"✅ Usuário criado: {email}")
        
        # Criar perfil (verificar se já existe devido ao signal)
        logger.info("👤 Criando/atualizando perfil...")
        try:
            profile = Profile.objects.get(user=user)
            # Atualizar perfil existente
            profile.nome = nome
            profile.idade = idade
            profile.faixa = faixa
            profile.save()
            logger.info("✅ Perfil atualizado")
        except Profile.DoesNotExist:
            # Criar novo perfil
            profile = Profile.objects.create(
                user=user,
                nome=nome,
                idade=idade,
                faixa=faixa
            )
            logger.info("✅ Perfil criado")
        
        logger.info(f"✅ Perfil criado: {nome}, Idade: {idade}, Faixa: {faixa}")
        
        # Fazer login
        logger.info("🔐 Fazendo login...")
        login(request, user)
        
        logger.info("✅ Cadastro completo processado com sucesso!")
        
        return JsonResponse({
            'success': True,
            'message': f'Cadastro realizado com sucesso! Bem-vindo, {nome}!',
            'redirect_url': '/dashboard/'
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no cadastro completo: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'error': str(e)})

