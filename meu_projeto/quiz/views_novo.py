from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from payments.views import verificar_acesso_premium
from .models import ProgressoQuiz
import json

# Create your views here.
def quiz(request):
    # Verificar se usuário está logado
    if not request.user.is_authenticated:
        messages.warning(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login')
    
    # Verificar acesso premium
    tem_acesso, assinatura = verificar_acesso_premium(request.user)
    
    if not tem_acesso:
        messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
        return redirect('payments:planos')
    
    return render(request, 'quiz/quiz.html', {
        'assinatura': assinatura
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def salvar_progresso(request):
    """
    Salva o progresso do quiz no banco de dados
    Sistema de progresso contínuo - usuário pode sair e voltar
    """
    try:
        data = json.loads(request.body)
        dificuldade = data.get('dificuldade', 'easy')
        pergunta_atual = data.get('pergunta_atual', 0)
        acertos = data.get('acertos', 0)
        erros = data.get('erros', 0)
        pontuacao = data.get('pontuacao', 0)
        quiz_completo = data.get('quiz_completo', False)
        
        # Buscar ou criar progresso (todos os níveis liberados)
        progresso = ProgressoQuiz.get_progresso_ou_criar(request.user, dificuldade)
        
        # Atualizar progresso
        progresso.pergunta_atual = pergunta_atual
        progresso.acertos = acertos
        progresso.erros = erros
        progresso.pontuacao = pontuacao
        progresso.quiz_completo = quiz_completo
        
        # Calcular progresso percentual
        progresso.calcular_progresso_percentual()
        
        if quiz_completo:
            progresso.data_fim = timezone.now()
        
        progresso.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Progresso salvo com sucesso',
            'progresso': {
                'pergunta_atual': progresso.pergunta_atual,
                'total_perguntas': progresso.total_perguntas,
                'acertos': progresso.acertos,
                'erros': progresso.erros,
                'pontuacao': progresso.pontuacao,
                'quiz_completo': progresso.quiz_completo,
                'progresso_percentual': progresso.progresso_percentual
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def carregar_progresso(request):
    """
    Carrega o progresso do quiz do banco de dados
    """
    try:
        dificuldade = request.GET.get('dificuldade', 'easy')
        
        # Buscar progresso para esta dificuldade
        progresso = ProgressoQuiz.get_progresso_ou_criar(request.user, dificuldade)
        
        return JsonResponse({
            'success': True,
            'progresso': {
                'pergunta_atual': progresso.pergunta_atual,
                'total_perguntas': progresso.total_perguntas,
                'acertos': progresso.acertos,
                'erros': progresso.erros,
                'pontuacao': progresso.pontuacao,
                'quiz_completo': progresso.quiz_completo,
                'progresso_percentual': progresso.progresso_percentual
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def verificar_niveis_disponiveis(request):
    """
    Verifica quais níveis estão disponíveis para o usuário
    Todos os níveis estão liberados
    """
    try:
        niveis = ['easy', 'medium', 'hard', 'expert']
        progressos = {}
        
        for nivel in niveis:
            progresso = ProgressoQuiz.get_progresso_ou_criar(request.user, nivel)
            progressos[nivel] = {
                'pergunta_atual': progresso.pergunta_atual,
                'total_perguntas': progresso.total_perguntas,
                'acertos': progresso.acertos,
                'erros': progresso.erros,
                'pontuacao': progresso.pontuacao,
                'quiz_completo': progresso.quiz_completo,
                'progresso_percentual': progresso.progresso_percentual,
                'disponivel': True  # Todos os níveis estão liberados
            }
        
        return JsonResponse({
            'success': True,
            'niveis': progressos
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def reiniciar_quiz(request):
    """
    Reinicia o quiz para uma dificuldade específica
    """
    try:
        data = json.loads(request.body)
        dificuldade = data.get('dificuldade', 'easy')
        
        # Buscar progresso e reiniciar
        progresso = ProgressoQuiz.get_progresso_ou_criar(request.user, dificuldade)
        progresso.reiniciar_quiz()
        
        return JsonResponse({
            'success': True,
            'message': 'Quiz reiniciado com sucesso',
            'progresso': {
                'pergunta_atual': progresso.pergunta_atual,
                'total_perguntas': progresso.total_perguntas,
                'acertos': progresso.acertos,
                'erros': progresso.erros,
                'pontuacao': progresso.pontuacao,
                'quiz_completo': progresso.quiz_completo,
                'progresso_percentual': progresso.progresso_percentual
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
