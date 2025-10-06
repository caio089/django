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
    Sistema sequencial: só pode avançar após completar o nível anterior
    """
    try:
        data = json.loads(request.body)
        dificuldade = data.get('dificuldade', 'easy')
        pergunta_atual = data.get('pergunta_atual', 0)
        total_perguntas = data.get('total_perguntas', 0)
        acertos = data.get('acertos', 0)
        erros = data.get('erros', 0)
        pontuacao = data.get('pontuacao', 0)
        quiz_completo = data.get('quiz_completo', False)
        
        # Verificar se pode acessar este nível
        if not ProgressoQuiz.pode_acessar_nivel(request.user, dificuldade):
            return JsonResponse({
                'success': False,
                'error': 'Você deve completar o nível anterior primeiro'
            }, status=403)
        
        # Buscar ou criar progresso
        progresso, created = ProgressoQuiz.objects.get_or_create(
            usuario=request.user,
            dificuldade=dificuldade,
            defaults={
                'pergunta_atual': pergunta_atual,
                'total_perguntas': total_perguntas,
                'acertos': acertos,
                'erros': erros,
                'pontuacao': pontuacao,
                'quiz_completo': quiz_completo,
                'nivel_desbloqueado': True,
                'data_fim': timezone.now() if quiz_completo else None
            }
        )
        
        # Se já existe, atualizar
        if not created:
            progresso.pergunta_atual = pergunta_atual
            progresso.total_perguntas = total_perguntas
            progresso.acertos = acertos
            progresso.erros = erros
            progresso.pontuacao = pontuacao
            progresso.quiz_completo = quiz_completo
            if quiz_completo and not progresso.data_fim:
                progresso.data_fim = timezone.now()
            progresso.save()
        
        # Se completou o quiz, desbloquear próximo nível
        if quiz_completo:
            niveis = ['easy', 'medium', 'hard', 'expert']
            nivel_index = niveis.index(dificuldade)
            if nivel_index < len(niveis) - 1:  # Não é o último nível
                proximo_nivel = niveis[nivel_index + 1]
                # Criar progresso para o próximo nível (desbloqueado mas não iniciado)
                ProgressoQuiz.objects.get_or_create(
                    usuario=request.user,
                    dificuldade=proximo_nivel,
                    defaults={
                        'pergunta_atual': 0,
                        'total_perguntas': 0,
                        'acertos': 0,
                        'erros': 0,
                        'pontuacao': 0,
                        'quiz_completo': False,
                        'nivel_desbloqueado': True
                    }
                )
        
        return JsonResponse({
            'success': True,
            'message': f'Progresso do quiz salvo: {pergunta_atual}/{total_perguntas} perguntas',
            'progresso': {
                'pergunta_atual': progresso.pergunta_atual,
                'total_perguntas': progresso.total_perguntas,
                'acertos': progresso.acertos,
                'erros': progresso.erros,
                'pontuacao': progresso.pontuacao,
                'quiz_completo': progresso.quiz_completo,
                'nivel_desbloqueado': progresso.nivel_desbloqueado
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
        
        # Verificar se pode acessar este nível
        if not ProgressoQuiz.pode_acessar_nivel(request.user, dificuldade):
            return JsonResponse({
                'success': False,
                'error': 'Você deve completar o nível anterior primeiro'
            }, status=403)
        
        # Buscar progresso para esta dificuldade
        try:
            progresso = ProgressoQuiz.objects.get(
                usuario=request.user,
                dificuldade=dificuldade
            )
            
            return JsonResponse({
                'success': True,
                'progresso': {
                    'pergunta_atual': progresso.pergunta_atual,
                    'total_perguntas': progresso.total_perguntas,
                    'acertos': progresso.acertos,
                    'erros': progresso.erros,
                    'pontuacao': progresso.pontuacao,
                    'quiz_completo': progresso.quiz_completo,
                    'nivel_desbloqueado': progresso.nivel_desbloqueado
                }
            })
        except ProgressoQuiz.DoesNotExist:
            return JsonResponse({
                'success': True,
                'progresso': None
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
    """
    try:
        niveis = ['easy', 'medium', 'hard', 'expert']
        niveis_disponiveis = []
        
        for nivel in niveis:
            pode_acessar = ProgressoQuiz.pode_acessar_nivel(request.user, nivel)
            niveis_disponiveis.append({
                'nivel': nivel,
                'disponivel': pode_acessar,
                'nome': dict(ProgressoQuiz.DIFICULDADE_CHOICES)[nivel]
            })
        
        return JsonResponse({
            'success': True,
            'niveis': niveis_disponiveis,
            'nivel_atual': ProgressoQuiz.get_nivel_atual(request.user)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)