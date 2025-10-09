"""
Views para recuperação de senha
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import CodigoRecuperacao
import logging
import traceback

logger = logging.getLogger(__name__)

def esqueci_senha(request):
    """Página inicial para solicitar recuperação de senha"""
    try:
        if request.method == 'POST':
            email = request.POST.get('email', '').strip()
            
            if not email:
                messages.error(request, 'Por favor, digite seu email.')
                return render(request, 'home/esqueci_senha.html')
            
            # Verificar se o email existe
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'Email não encontrado em nosso sistema.')
                return render(request, 'home/esqueci_senha.html')
            
            try:
                # Gerar código de recuperação
                codigo_obj = CodigoRecuperacao.gerar_codigo(email)
                logger.info(f"Código gerado para {email}: {codigo_obj.codigo}")
                
                # Enviar email com o código (em ambiente de desenvolvimento, apenas loga)
                try:
                    enviar_email_codigo(email, codigo_obj.codigo)
                    logger.info(f"Email enviado para {email}")
                except Exception as email_error:
                    logger.warning(f"Erro ao enviar email: {email_error}")
                    # Mesmo se o email falhar, continua (para desenvolvimento)
                    logger.info(f"CÓDIGO DE RECUPERAÇÃO (desenvolvimento): {codigo_obj.codigo}")
                
                messages.success(request, f'Código enviado para {email}! Verifique sua caixa de entrada.')
                
                # Redirecionar para página de verificação
                return redirect('verificar_codigo', email=email)
                
            except Exception as e:
                logger.error(f"Erro ao gerar código de recuperação: {e}")
                traceback.print_exc()
                messages.error(request, f'Erro ao processar solicitação: {str(e)}')
        
        return render(request, 'home/esqueci_senha.html')
        
    except Exception as e:
        logger.error(f"Erro geral em esqueci_senha: {e}")
        traceback.print_exc()
        messages.error(request, 'Erro ao carregar página. Tente novamente.')
        return render(request, 'home/esqueci_senha.html')


def verificar_codigo(request, email):
    """Página para verificar o código de 6 dígitos"""
    if request.method == 'POST':
        codigo_digitado = request.POST.get('codigo')
        
        if not codigo_digitado:
            messages.error(request, 'Por favor, digite o código.')
            return render(request, 'home/verificar_codigo.html', {'email': email})
        
        try:
            # Buscar código válido
            codigo_obj = CodigoRecuperacao.objects.filter(
                email=email,
                codigo=codigo_digitado,
                usado=False
            ).first()
            
            if codigo_obj and codigo_obj.is_valido():
                # Código válido - redirecionar para redefinir senha
                codigo_obj.marcar_como_usado()
                return redirect('redefinir_senha', email=email)
            else:
                messages.error(request, 'Código inválido ou expirado. Tente novamente.')
                
        except Exception as e:
            logger.error(f"Erro ao verificar código: {e}")
            messages.error(request, 'Erro ao verificar código. Tente novamente.')
    
    return render(request, 'home/verificar_codigo.html', {'email': email})


def redefinir_senha(request, email):
    """Página para redefinir a nova senha"""
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not nova_senha or not confirmar_senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'home/redefinir_senha.html', {'email': email})
        
        if nova_senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'home/redefinir_senha.html', {'email': email})
        
        if len(nova_senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'home/redefinir_senha.html', {'email': email})
        
        try:
            # Atualizar senha do usuário
            user = User.objects.get(email=email)
            user.set_password(nova_senha)
            user.save()
            
            messages.success(request, 'Senha alterada com sucesso! Faça login com sua nova senha.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        except Exception as e:
            logger.error(f"Erro ao redefinir senha: {e}")
            messages.error(request, 'Erro ao alterar senha. Tente novamente.')
    
    return render(request, 'home/redefinir_senha.html', {'email': email})


def enviar_email_codigo(email, codigo):
    """Envia email com o código de recuperação"""
    try:
        # Verificar se o email está configurado
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
        
        if not email_host_user:
            # Modo desenvolvimento - apenas loga o código
            logger.warning(f"Email não configurado. Código para {email}: {codigo}")
            print(f"\n{'='*50}")
            print(f"CÓDIGO DE RECUPERAÇÃO PARA {email}")
            print(f"CÓDIGO: {codigo}")
            print(f"{'='*50}\n")
            return
        
        assunto = 'Código de Recuperação de Senha - Dojo Online'
        
        mensagem = f"""
Olá!

Você solicitou a recuperação de senha para sua conta no Dojo Online.

Seu código de verificação é: {codigo}

Este código expira em 15 minutos.

Se você não solicitou esta recuperação de senha, ignore este email.

Atenciosamente,
Equipe Dojo Online
        """
        
        remetente = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dojo-online.com')
        
        send_mail(
            assunto,
            mensagem,
            remetente,
            [email],
            fail_silently=False,
        )
        
        logger.info(f"Email de recuperação enviado para {email}")
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {email}: {e}")
        # Em desenvolvimento, não falha se o email não funcionar
        if settings.DEBUG:
            logger.warning(f"Modo DEBUG: Continuando apesar do erro de email")
            print(f"\n{'='*50}")
            print(f"ERRO AO ENVIAR EMAIL, MAS CÓDIGO GERADO:")
            print(f"Email: {email}")
            print(f"Código: {codigo}")
            print(f"{'='*50}\n")
        else:
            raise
