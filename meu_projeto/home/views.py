from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile
from .forms import EmailLoginForm, RegisterForm
import logging
import json

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
            
            try:
                # Verificar se já existe usuário com este email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Já existe uma conta com este email. Use outro email ou faça login.')
                    return render(request, 'home/home.html', {
                        'form': form,
                        'register_form': register_form,
                        'show_register': show_register
                    })
                
                # Criar usuário
                user = User.objects.create_user(username=email, email=email, password=senha)
                
                # Verificar se já existe profile (segurança extra)
                if Profile.objects.filter(user=user).exists():
                    logger.warning(f"Profile já existe para usuário {user.id}, atualizando...")
                    profile = Profile.objects.get(user=user)
                    profile.nome = nome
                    profile.idade = idade
                    profile.faixa = faixa
                    profile.save()
                else:
                    # Criar novo profile
                    profile = Profile.objects.create(
                        user=user,
                        nome=nome,
                        idade=idade,
                        faixa=faixa
                    )
                
                logger.info(f"Usuário criado com sucesso: {email}, Profile ID: {profile.id}")
                
                # Fazer login automaticamente após registro
                login(request, user)
                messages.success(request, f'Conta criada com sucesso! Bem-vindo, {nome}!')
                return redirect('index')
                
            except Exception as e:
                logger.error(f"Erro ao criar usuário/profile: {e}")
                messages.error(request, f'Erro ao criar conta: {str(e)}')
                # Se deu erro, deletar o usuário se foi criado
                try:
                    if 'user' in locals():
                        user.delete()
                except:
                    pass
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




def selecionar_faixa_view(request):
    """
    View para seleção de faixa após login
    """
    # Se não estiver logado, redirecionar para login
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'home/selecionar_faixa.html')




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
            
            # Mapeamento de faixas para URLs
            faixas_urls = {
                'cinza': '/pag1/',
                'azul': '/pag2/',
                'amarela': '/pag3/',
                'laranja': '/pag4/',
                'verde': '/pag5/',
                'roxa': '/pag6/',
                'marrom': '/pag7/'
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

