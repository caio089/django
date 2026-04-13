from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.cache import cache
from django.utils import timezone
from meu_projeto.redirect_utils import redirect_to_frontend
from .models import ProgressoQuiz, QuizRanking, ProgressoUsuario
from home.models import Profile
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

def _has_premium_access(user):
    """Usuário premium tem acesso aos níveis 2+ do quiz."""
    if not user or not user.is_authenticated:
        return False
    try:
        profile = Profile.objects.get(user=user)
        return bool(profile.conta_premium)
    except Profile.DoesNotExist:
        return False


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
        # Ranking do desafio: somente usuários premium (evita multi-contas anônimas)
        entries = QuizRanking.objects.filter(usuario__isnull=False).order_by('-xp_total')[:limit]
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
        # Segurança: XP não pode vir do cliente.
        # Esse endpoint é legado (frontend antigo). Mantemos, mas zeramos XP.
        xp_ganho = 0
        passou_nivel = data.get('passou_nivel', False)
        premium_access = _has_premium_access(request.user)

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
        # Modo freemium: sem premium, apenas nível 1 permanece liberado.
        if not premium_access:
            entry.nivel_quiz = 1
            entry.categoria_titulo = CATEGORIAS_NIVEL.get(1, 'Kohai')
        elif passou_nivel:
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


def _is_premium_user(user):
    try:
        return bool(user.is_authenticated and getattr(user, "profile", None) and user.profile.conta_premium)
    except Exception:
        return False


@login_required
@require_http_methods(["POST"])
def api_start_attempt(request):
    """
    Inicia uma tentativa de quiz com tempo server-side.
    Body: { nivel_quiz, question_keys: [] }
    Retorna: { attempt_id }
    """
    try:
        if not _is_premium_user(request.user):
            return JsonResponse({"success": False, "error": "Apenas Premium participa do ranking."}, status=403)

        data = json.loads(request.body) if request.body else {}
        nivel_quiz = max(1, min(MAX_NIVEL_QUIZ, int(data.get("nivel_quiz", 1))))
        question_keys = data.get("question_keys") or []
        if not isinstance(question_keys, list) or len(question_keys) == 0:
            return JsonResponse({"success": False, "error": "question_keys obrigatório"}, status=400)
        if len(question_keys) > 20:
            return JsonResponse({"success": False, "error": "question_keys inválido"}, status=400)

        from .models import QuizAttempt
        attempt = QuizAttempt.objects.create(
            usuario=request.user,
            nivel_quiz=nivel_quiz,
            total_perguntas=len(question_keys),
            question_keys=question_keys,
        )
        return JsonResponse({"success": True, "attempt_id": attempt.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def api_submit_attempt(request):
    """
    Finaliza tentativa e calcula XP no servidor.
    Body: { attempt_id, correct_keys: [], nickname?, dojo?, cidade? }
    """
    try:
        if not _is_premium_user(request.user):
            return JsonResponse({"success": False, "error": "Apenas Premium participa do ranking."}, status=403)

        # Rate limit simples por usuário (anti-spam)
        rl_key = f"quiz_submit_rl:{request.user.id}"
        if cache.get(rl_key):
            return JsonResponse({"success": False, "error": "Aguarde alguns segundos e tente novamente."}, status=429)
        cache.set(rl_key, 1, 8)

        data = json.loads(request.body) if request.body else {}
        attempt_id = int(data.get("attempt_id") or 0)
        correct_keys = data.get("correct_keys") or []
        nickname = (data.get("nickname") or "").strip() or "Anônimo"
        dojo = (data.get("dojo") or "").strip()
        cidade = (data.get("cidade") or "").strip()

        if attempt_id <= 0:
            return JsonResponse({"success": False, "error": "attempt_id inválido"}, status=400)
        if not isinstance(correct_keys, list):
            return JsonResponse({"success": False, "error": "correct_keys inválido"}, status=400)

        from .models import QuizAttempt, QuizQuestionProgress, QuizRanking, ProgressoUsuario
        attempt = QuizAttempt.objects.select_for_update().get(id=attempt_id, usuario=request.user)
        if attempt.finished_at:
            return JsonResponse({"success": False, "error": "Tentativa já finalizada"}, status=400)

        now = timezone.now()
        elapsed = max(0, int((now - attempt.started_at).total_seconds()))
        attempt.finished_at = now
        attempt.elapsed_seconds = elapsed

        # Validar chaves (não permite inventar perguntas fora da tentativa)
        keys_set = set(attempt.question_keys or [])
        correct_set = set([k for k in correct_keys if isinstance(k, str)])
        correct_set = correct_set.intersection(keys_set)
        correct_count = len(correct_set)
        attempt.correct_count = correct_count

        total = max(1, int(attempt.total_perguntas or len(keys_set) or 1))
        accuracy = correct_count / total

        # Anti-burla: tempo mínimo plausível
        min_per_q = 2.5
        min_elapsed = int(total * min_per_q)
        suspicious = False
        reason = ""
        if elapsed < min_elapsed:
            suspicious = True
            reason = f"Tempo muito baixo ({elapsed}s < {min_elapsed}s)"

        # XP base: primeira vez 10, refazer 3 (por questão correta)
        base_xp = 0
        for qk in correct_set:
            prog, created = QuizQuestionProgress.objects.get_or_create(usuario=request.user, question_key=qk)
            prog.times_seen = (prog.times_seen or 0) + 1
            already_correct = (prog.times_correct or 0) > 0
            base_xp += 3 if already_correct else 10
            prog.times_correct = (prog.times_correct or 0) + 1
            if not prog.first_correct_at:
                prog.first_correct_at = now
            prog.save(update_fields=["times_seen", "times_correct", "first_correct_at", "data_atualizacao"])

        # Bonus por tempo (somente se acurácia mínima e não suspeito)
        bonus = 0
        if (not suspicious) and accuracy >= 0.8:
            target = int(total * 30)  # 30s por pergunta
            bonus = max(0, (target - elapsed) // 10)  # +1 a cada 10s abaixo do alvo
            bonus = min(20, bonus)  # teto por tentativa

        # Cap diário para evitar farm infinito
        cap_daily = 400
        day_key = f"quiz_xp_day:{request.user.id}:{now.strftime('%Y-%m-%d')}"
        earned_today = int(cache.get(day_key) or 0)
        xp_total_attempt = base_xp + bonus
        remaining = max(0, cap_daily - earned_today)
        if xp_total_attempt > remaining:
            xp_total_attempt = remaining
            if remaining == 0:
                bonus = 0

        # Se suspeito, zera bônus (mantém base, mas ainda respeita cap)
        if suspicious:
            xp_total_attempt = min(xp_total_attempt, base_xp)  # remove bônus
            bonus = 0

        cache.set(day_key, earned_today + xp_total_attempt, 60 * 60 * 30)  # 30h

        attempt.xp_awarded = xp_total_attempt
        attempt.bonus_time_xp = bonus
        attempt.suspicious = suspicious
        attempt.suspicious_reason = reason
        attempt.save(update_fields=[
            "finished_at", "elapsed_seconds", "correct_count",
            "xp_awarded", "bonus_time_xp", "suspicious", "suspicious_reason"
        ])

        # Atualizar ranking (somente premium)
        entry = QuizRanking.objects.filter(usuario=request.user).first()
        if entry:
            entry.nickname = nickname or entry.nickname
        else:
            entry = QuizRanking(usuario=request.user, nickname=nickname)
        entry.dojo = dojo or getattr(entry, "dojo", "") or ""
        entry.cidade = cidade or entry.cidade
        entry.xp_total += xp_total_attempt
        # Subir nível apenas se acertar tudo (ou defina regra)
        passou_nivel = (correct_count == total)
        if passou_nivel:
            entry.nivel_quiz = min(MAX_NIVEL_QUIZ, max(entry.nivel_quiz, attempt.nivel_quiz) + 1)
            entry.categoria_titulo = CATEGORIAS_NIVEL.get(entry.nivel_quiz, "Sensei")
        else:
            entry.nivel_quiz = max(entry.nivel_quiz, attempt.nivel_quiz)
            entry.categoria_titulo = CATEGORIAS_NIVEL.get(entry.nivel_quiz, "Kohai")
        entry.save()

        # Sincronizar ProgressoUsuario
        prog, _ = ProgressoUsuario.objects.get_or_create(usuario=request.user)
        prog.experiencia_total = entry.xp_total
        prog.nivel_quiz = entry.nivel_quiz
        prog.categoria_titulo = entry.categoria_titulo
        prog.total_acertos = (prog.total_acertos or 0) + correct_count
        prog.total_quiz_realizados = (prog.total_quiz_realizados or 0) + 1
        prog.save(update_fields=["experiencia_total", "nivel_quiz", "categoria_titulo", "total_acertos", "total_quiz_realizados", "data_atualizacao"])

        return JsonResponse({
            "success": True,
            "xp_ganho": xp_total_attempt,
            "bonus_tempo": bonus,
            "elapsed_seconds": elapsed,
            "accuracy": round(accuracy * 100, 1),
            "suspicious": suspicious,
            "xp_total": entry.xp_total,
            "nivel_quiz": entry.nivel_quiz,
            "categoria_titulo": entry.categoria_titulo,
        })
    except QuizAttempt.DoesNotExist:
        return JsonResponse({"success": False, "error": "Tentativa não encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
