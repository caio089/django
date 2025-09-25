from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from .models import (
    UserProgress, FaixaProgress, QuizProgress, 
    RolamentosProgress, UserSession
)

@login_required
@csrf_exempt
def save_faixa_progress(request):
    """Salva o progresso de uma faixa específica"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            faixa = data.get('faixa')
            progress_percentage = data.get('progress_percentage', 0)
            time_spent = data.get('time_spent', 0)
            lessons_completed = data.get('lessons_completed', 0)
            total_lessons = data.get('total_lessons', 10)
            
            # Criar ou atualizar progresso da faixa
            faixa_progress, created = FaixaProgress.objects.get_or_create(
                user=request.user,
                faixa=faixa,
                defaults={
                    'progress_percentage': progress_percentage,
                    'time_spent': time_spent,
                    'lessons_completed': lessons_completed,
                    'total_lessons': total_lessons,
                    'is_completed': progress_percentage >= 100
                }
            )
            
            if not created:
                faixa_progress.progress_percentage = progress_percentage
                faixa_progress.time_spent += time_spent
                faixa_progress.lessons_completed = lessons_completed
                faixa_progress.total_lessons = total_lessons
                faixa_progress.is_completed = progress_percentage >= 100
                faixa_progress.save()
            
            # Atualizar progresso geral do usuário
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                defaults={'total_time_spent': time_spent}
            )
            if not created:
                user_progress.total_time_spent += time_spent
                user_progress.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Progresso salvo com sucesso!',
                'progress': {
                    'faixa': faixa,
                    'percentage': faixa_progress.progress_percentage,
                    'time_spent': faixa_progress.time_spent,
                    'lessons_completed': faixa_progress.lessons_completed,
                    'is_completed': faixa_progress.is_completed
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar progresso: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

@login_required
@csrf_exempt
def save_quiz_progress(request):
    """Salva o progresso do quiz"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_questions = data.get('total_questions', 0)
            correct_answers = data.get('correct_answers', 0)
            wrong_answers = data.get('wrong_answers', 0)
            current_level = data.get('current_level', 1)
            time_spent = data.get('time_spent', 0)
            
            # Calcular porcentagem
            if total_questions > 0:
                progress_percentage = int((correct_answers / total_questions) * 100)
            else:
                progress_percentage = 0
            
            # Criar ou atualizar progresso do quiz
            quiz_progress, created = QuizProgress.objects.get_or_create(
                user=request.user,
                defaults={
                    'total_questions': total_questions,
                    'correct_answers': correct_answers,
                    'wrong_answers': wrong_answers,
                    'progress_percentage': progress_percentage,
                    'current_level': current_level,
                    'total_time_spent': time_spent,
                    'best_score': progress_percentage
                }
            )
            
            if not created:
                quiz_progress.total_questions += total_questions
                quiz_progress.correct_answers += correct_answers
                quiz_progress.wrong_answers += wrong_answers
                quiz_progress.current_level = current_level
                quiz_progress.total_time_spent += time_spent
                
                # Recalcular porcentagem total
                if quiz_progress.total_questions > 0:
                    quiz_progress.progress_percentage = int(
                        (quiz_progress.correct_answers / quiz_progress.total_questions) * 100
                    )
                
                # Atualizar melhor pontuação
                if progress_percentage > quiz_progress.best_score:
                    quiz_progress.best_score = progress_percentage
                
                quiz_progress.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Progresso do quiz salvo com sucesso!',
                'progress': {
                    'total_questions': quiz_progress.total_questions,
                    'correct_answers': quiz_progress.correct_answers,
                    'wrong_answers': quiz_progress.wrong_answers,
                    'percentage': quiz_progress.progress_percentage,
                    'current_level': quiz_progress.current_level,
                    'best_score': quiz_progress.best_score
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar progresso do quiz: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

@login_required
@csrf_exempt
def save_rolamentos_progress(request):
    """Salva o progresso dos rolamentos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_rolamentos = data.get('total_rolamentos', 0)
            completed_rolamentos = data.get('completed_rolamentos', 0)
            time_spent = data.get('time_spent', 0)
            current_rolamento = data.get('current_rolamento', '')
            
            # Calcular porcentagem
            if total_rolamentos > 0:
                progress_percentage = int((completed_rolamentos / total_rolamentos) * 100)
            else:
                progress_percentage = 0
            
            # Criar ou atualizar progresso dos rolamentos
            rolamentos_progress, created = RolamentosProgress.objects.get_or_create(
                user=request.user,
                defaults={
                    'total_rolamentos': total_rolamentos,
                    'completed_rolamentos': completed_rolamentos,
                    'progress_percentage': progress_percentage,
                    'time_spent': time_spent,
                    'current_rolamento': current_rolamento
                }
            )
            
            if not created:
                rolamentos_progress.total_rolamentos = total_rolamentos
                rolamentos_progress.completed_rolamentos = completed_rolamentos
                rolamentos_progress.progress_percentage = progress_percentage
                rolamentos_progress.time_spent += time_spent
                rolamentos_progress.current_rolamento = current_rolamento
                rolamentos_progress.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Progresso dos rolamentos salvo com sucesso!',
                'progress': {
                    'total_rolamentos': rolamentos_progress.total_rolamentos,
                    'completed_rolamentos': rolamentos_progress.completed_rolamentos,
                    'percentage': rolamentos_progress.progress_percentage,
                    'current_rolamento': rolamentos_progress.current_rolamento
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar progresso dos rolamentos: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

@login_required
def get_user_progress(request):
    """Retorna todo o progresso do usuário"""
    try:
        # Progresso geral
        user_progress, created = UserProgress.objects.get_or_create(user=request.user)
        
        # Progresso das faixas
        faixas_progress = FaixaProgress.objects.filter(user=request.user)
        faixas_data = []
        for fp in faixas_progress:
            faixas_data.append({
                'faixa': fp.faixa,
                'progress_percentage': fp.progress_percentage,
                'time_spent': fp.time_spent,
                'lessons_completed': fp.lessons_completed,
                'total_lessons': fp.total_lessons,
                'is_completed': fp.is_completed,
                'last_accessed': fp.last_accessed.isoformat()
            })
        
        # Progresso do quiz
        quiz_progress = None
        try:
            qp = QuizProgress.objects.get(user=request.user)
            quiz_progress = {
                'total_questions': qp.total_questions,
                'correct_answers': qp.correct_answers,
                'wrong_answers': qp.wrong_answers,
                'progress_percentage': qp.progress_percentage,
                'current_level': qp.current_level,
                'best_score': qp.best_score,
                'last_quiz_date': qp.last_quiz_date.isoformat()
            }
        except QuizProgress.DoesNotExist:
            quiz_progress = None
        
        # Progresso dos rolamentos
        rolamentos_progress = None
        try:
            rp = RolamentosProgress.objects.get(user=request.user)
            rolamentos_progress = {
                'total_rolamentos': rp.total_rolamentos,
                'completed_rolamentos': rp.completed_rolamentos,
                'progress_percentage': rp.progress_percentage,
                'current_rolamento': rp.current_rolamento,
                'last_accessed': rp.last_accessed.isoformat()
            }
        except RolamentosProgress.DoesNotExist:
            rolamentos_progress = None
        
        return JsonResponse({
            'success': True,
            'user_progress': {
                'total_time_spent': user_progress.total_time_spent,
                'last_activity': user_progress.last_activity.isoformat()
            },
            'faixas_progress': faixas_data,
            'quiz_progress': quiz_progress,
            'rolamentos_progress': rolamentos_progress
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao carregar progresso: {str(e)}'
        })

@login_required
@csrf_exempt
def create_user_session(request):
    """Cria uma nova sessão de login"""
    try:
        # Obter IP e User Agent
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Criar sessão
        session = UserSession.objects.create(
            user=request.user,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'login_time': session.login_time.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao criar sessão: {str(e)}'
        })
