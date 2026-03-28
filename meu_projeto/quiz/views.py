from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from meu_projeto.redirect_utils import redirect_to_frontend
from .models import ProgressoQuiz, QuizRanking, ProgressoUsuario
import json

# Categorias do ranking por nível (10 níveis)
CATEGORIAS_NIVEL = {
    1: 'Kohai',
    2: 'Aprendiz',
    3: 'Ninja',
    4: 'Samurai',
    5: 'Monge',
    6: 'Mestre',
    7: 'Yudansha',
    8: 'Renshi',
    9: 'Kyoshi',
    10: 'Sensei',
}
MAX_NIVEL_QUIZ = 10

# Create your views here.
def quiz(request):
    """Redireciona para o React em /quiz"""
    return redirect_to_frontend('/quiz')

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


# --- API Ranking (público: não exige login) ---

@require_http_methods(["GET"])
def api_ranking(request):
    """
    GET /quiz/api/ranking/
    Retorna o ranking: posição, nome, cidade, xp_total, nivel_quiz, categoria_titulo.
    Limite padrão 50.
    """
    try:
        limit = min(int(request.GET.get('limit', 50)), 100)
        entries = QuizRanking.objects.all().order_by('-xp_total')[:limit]
        result = []
        for i, e in enumerate(entries, start=1):
            nome = e.nickname
            if e.usuario_id:
                try:
                    nome = e.usuario.profile.nome
                except Exception:
                    pass
            result.append({
                'posicao': i,
                'nome': nome,
                'dojo': getattr(e, 'dojo', '') or '',
                'cidade': e.cidade or '',
                'xp_total': e.xp_total,
                'nivel_quiz': e.nivel_quiz,
                'categoria_titulo': e.categoria_titulo,
            })
        return JsonResponse({'success': True, 'ranking': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_submit(request):
    """
    POST /quiz/api/submit/
    Body: { nickname?, cidade?, nivel_quiz, xp_ganho, passou_nivel (bool) }
    Atualiza ou cria entrada no ranking (por session_key ou usuario).
    Se passou_nivel, sobe nivel_quiz e atualiza categoria_titulo.
    """
    try:
        data = json.loads(request.body)
        nickname = (data.get('nickname') or '').strip() or 'Anônimo'
        dojo = (data.get('dojo') or '').strip()
        cidade = (data.get('cidade') or '').strip()
        nivel_quiz = max(1, min(MAX_NIVEL_QUIZ, int(data.get('nivel_quiz', 1))))
        xp_ganho = max(0, int(data.get('xp_ganho', 0)))
        passou_nivel = data.get('passou_nivel', False)

        # Garantir sessão para anônimos
        if not request.session.session_key:
            request.session.create()

        entry = None
        if request.user.is_authenticated:
            entry = QuizRanking.objects.filter(usuario=request.user).first()
            if entry:
                entry.nickname = nickname or (getattr(entry.usuario.profile, 'nome', None) or entry.usuario.username)
            else:
                entry = QuizRanking(
                    usuario=request.user,
                    nickname=nickname or getattr(request.user.profile, 'nome', request.user.username),
                )
        else:
            sk = request.session.session_key
            entry = QuizRanking.objects.filter(session_key=sk).first()
            if not entry:
                entry = QuizRanking(session_key=sk, nickname=nickname)
            else:
                entry.nickname = nickname

        entry.dojo = dojo or getattr(entry, 'dojo', '') or ''
        entry.cidade = cidade or entry.cidade
        entry.xp_total += xp_ganho
        if passou_nivel:
            entry.nivel_quiz = min(MAX_NIVEL_QUIZ, entry.nivel_quiz + 1)
            entry.categoria_titulo = CATEGORIAS_NIVEL.get(entry.nivel_quiz, 'Sensei')
        else:
            entry.categoria_titulo = CATEGORIAS_NIVEL.get(entry.nivel_quiz, 'Kohai')
        entry.save()

        # Sincronizar ProgressoUsuario se logado (tabela existente, não usada antes)
        if request.user.is_authenticated:
            prog, _ = ProgressoUsuario.objects.get_or_create(usuario=request.user)
            prog.experiencia_total = entry.xp_total
            prog.nivel_quiz = entry.nivel_quiz
            prog.categoria_titulo = entry.categoria_titulo
            prog.total_acertos = (prog.total_acertos or 0) + (data.get('acertos', 0) or 0)
            prog.total_quiz_realizados = (prog.total_quiz_realizados or 0) + 1
            prog.save(update_fields=['experiencia_total', 'nivel_quiz', 'categoria_titulo', 'total_acertos', 'total_quiz_realizados', 'data_atualizacao'])

        return JsonResponse({
            'success': True,
            'xp_total': entry.xp_total,
            'nivel_quiz': entry.nivel_quiz,
            'categoria_titulo': entry.categoria_titulo,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
