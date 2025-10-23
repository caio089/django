from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import EmailLoginForm, RegisterForm
import logging

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


def login_google_view(request):
    """
    View para login com Google
    """
    # Se já estiver logado, redirecionar para seleção de faixa
    if request.user.is_authenticated:
        return redirect('selecionar_faixa')
    
    return render(request, 'home/login_google.html')


def selecionar_faixa_view(request):
    """
    View para seleção de faixa após login
    """
    # Se não estiver logado, redirecionar para login
    if not request.user.is_authenticated:
        return redirect('login_google')
    
    return render(request, 'home/selecionar_faixa.html')


def processar_login_google(request):
    """
    Processa o login via Google e cria/atualiza o usuário
    """
    from django.http import JsonResponse
    
    if request.method != 'POST':
        logger.warning("⚠️ Método não permitido para login Google")
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        import json
        
        logger.info("🔐 Iniciando processamento de login Google...")
        
        # Verificar se o corpo da requisição não está vazio
        if not request.body:
            logger.error("❌ Corpo da requisição vazio")
            return JsonResponse({'success': False, 'error': 'Dados não fornecidos'})
        
        # Dados do usuário do Google
        try:
            dados_usuario = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao decodificar JSON: {e}")
            return JsonResponse({'success': False, 'error': 'Dados inválidos'})
        
        email = dados_usuario.get('email')
        nome = dados_usuario.get('name', '')
        picture = dados_usuario.get('picture', '')
        
        logger.info(f"📧 Dados recebidos - Email: {email}, Nome: {nome}")
        
        if not email:
            logger.error("❌ Email não fornecido")
            return JsonResponse({'success': False, 'error': 'Email não fornecido'})
        
        # Buscar ou criar usuário
        from django.contrib.auth.models import User
        from django.contrib.auth import login
        from home.models import Profile
        
        logger.info("👤 Criando/buscando usuário...")
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': nome.split(' ')[0] if nome else '',
                'last_name': ' '.join(nome.split(' ')[1:]) if nome and len(nome.split(' ')) > 1 else '',
            }
        )
        
        if created:
            logger.info("🔑 Configurando senha do usuário...")
            user.set_unusable_password()  # Usuário não precisa de senha
            user.save()
            logger.info(f"✅ Novo usuário criado via Google: {email}")
            
            # Criar perfil automaticamente
            try:
                logger.info("👤 Criando perfil do usuário...")
                profile = Profile.objects.create(
                    user=user,
                    nome=nome or user.first_name or user.username,
                    idade=18,  # Idade padrão
                    faixa='cinza'  # Faixa padrão (primeira faixa)
                )
                logger.info(f"✅ Perfil criado para usuário Google: {email}")
            except Exception as e:
                logger.error(f"❌ Erro ao criar perfil: {e}")
                # Continuar mesmo sem perfil
        else:
            logger.info(f"✅ Usuário existente logado via Google: {email}")
            
            # Verificar se tem perfil, se não tiver, criar
            try:
                profile = Profile.objects.get(user=user)
                logger.info("👤 Perfil existente encontrado")
            except Profile.DoesNotExist:
                logger.info("👤 Criando perfil para usuário existente...")
                profile = Profile.objects.create(
                    user=user,
                    nome=nome or user.first_name or user.username,
                    idade=18,
                    faixa='cinza'
                )
                logger.info(f"✅ Perfil criado para usuário existente: {email}")
        
        # Fazer login do usuário
        logger.info("🔐 Fazendo login do usuário...")
        login(request, user)
        
        logger.info("✅ Login Google processado com sucesso!")
        return JsonResponse({
            'success': True,
            'message': f'Bem-vindo, {nome}!',
            'user': {
                'name': nome,
                'email': email,
                'picture': picture
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no login Google: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'error': str(e)})


def selecionar_faixa_view(request):
    """
    View para processar a seleção de faixa do usuário
    """
    if request.method == 'POST':
        try:
            import json
            
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