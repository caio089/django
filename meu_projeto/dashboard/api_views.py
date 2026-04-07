"""
API JSON para o painel admin React.
Usa sessão Django + CSRF (igual ao login normal do app).
"""
import json
import uuid
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings

from payments.models import Pagamento, Assinatura, PlanoPremium
from home.models import Profile
from .views import clear_dashboard_cache


def _require_superuser(view_func):
    """Decorator que retorna 403 JSON se não for superuser."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autenticado'}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Acesso negado'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


@ensure_csrf_cookie
@require_http_methods(['GET'])
def api_admin_me(request):
    """Verifica se está logado como admin."""
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({'authenticated': False, 'admin': False})
    return JsonResponse({
        'authenticated': True,
        'admin': True,
        'username': request.user.username,
    })


@require_http_methods(['POST'])
def api_admin_login(request):
    """Login admin via JSON: { username|email, password }."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password', '')

    login_value = username or email
    if not login_value or not password:
        return JsonResponse({'success': False, 'error': 'Usuário/e-mail e senha são obrigatórios'}, status=400)

    # Permite login admin usando e-mail sem quebrar o backend padrão do Django.
    auth_username = login_value
    if '@' in login_value:
        user_by_email = User.objects.filter(email__iexact=login_value).only('username').first()
        if not user_by_email:
            return JsonResponse({'success': False, 'error': 'Usuário ou senha incorretos'}, status=400)
        auth_username = user_by_email.username

    user = authenticate(request, username=auth_username, password=password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Usuário ou senha incorretos'}, status=400)

    if not user.is_active:
        return JsonResponse({'success': False, 'error': 'Conta desativada'}, status=403)

    if not user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Usuário ou senha incorretos'}, status=400)

    login(request, user)
    return JsonResponse({
        'success': True,
        'user': {'username': user.username},
    })


@require_http_methods(['POST'])
def api_admin_logout(request):
    """Logout admin."""
    logout(request)
    return JsonResponse({'success': True})


@_require_superuser
@require_http_methods(['GET'])
def api_admin_dashboard(request):
    """Retorna todas as métricas do dashboard em JSON."""
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    last_month = now - timedelta(days=30)

    # Assinaturas ativas
    active_subscriptions = Assinatura.objects.filter(status='ativa', ativo=True)
    if not active_subscriptions.exists():
        active_subscriptions = Assinatura.objects.filter(status='ativa')
    if not active_subscriptions.exists():
        active_subscriptions = Assinatura.objects.filter(ativo=True)

    active_count = active_subscriptions.count()
    unique_premium = active_subscriptions.values('usuario').distinct().count()

    # Receitas
    total_revenue = Pagamento.objects.filter(status='approved').aggregate(total=Sum('valor'))['total'] or 0
    current_month_revenue = Pagamento.objects.filter(
        status='approved',
        data_criacao__year=current_year,
        data_criacao__month=current_month
    ).aggregate(total=Sum('valor'))['total'] or 0
    last_month_revenue = Pagamento.objects.filter(
        status='approved',
        data_criacao__gte=last_month.replace(day=1),
        data_criacao__lt=now.replace(day=1)
    ).aggregate(total=Sum('valor'))['total'] or 0

    # Crescimento
    new_premium_this_month = Assinatura.objects.filter(
        data_criacao__year=current_year,
        data_criacao__month=current_month
    ).count()
    new_premium_last_month = Assinatura.objects.filter(
        data_criacao__gte=last_month.replace(day=1),
        data_criacao__lt=now.replace(day=1)
    ).count()
    growth = ((new_premium_this_month - new_premium_last_month) / new_premium_last_month * 100) if new_premium_last_month > 0 else (100 if new_premium_this_month > 0 else 0)

    # Histórico 12 meses
    monthly_data = []
    for i in range(12):
        month_date = now - timedelta(days=30 * i)
        month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i == 0:
            month_end = now
        else:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        month_revenue = Pagamento.objects.filter(
            status='approved',
            data_criacao__gte=month_start,
            data_criacao__lte=month_end
        ).aggregate(total=Sum('valor'))['total'] or 0
        month_subs = Assinatura.objects.filter(
            data_criacao__gte=month_start,
            data_criacao__lte=month_end
        ).count()
        monthly_data.append({
            'month': month_start.strftime('%Y-%m'),
            'month_name': month_start.strftime('%b/%Y'),
            'revenue': float(month_revenue),
            'subscriptions': month_subs,
        })
    monthly_data.reverse()

    # Usuários
    total_users = User.objects.count()
    users_this_month = User.objects.filter(
        date_joined__year=current_year,
        date_joined__month=current_month
    ).count()

    # Assinaturas recentes
    recent_subs = Assinatura.objects.select_related('usuario', 'plano').filter(status='ativa').order_by('-data_criacao')[:15]
    recent_subscriptions = []
    for s in recent_subs:
        try:
            nome = s.usuario.profile.nome if hasattr(s.usuario, 'profile') else s.usuario.username
        except Profile.DoesNotExist:
            nome = s.usuario.username
        recent_subscriptions.append({
            'id': s.id,
            'usuario': nome,
            'email': s.usuario.email,
            'plano': s.plano.nome,
            'data_criacao': s.data_criacao.strftime('%d/%m/%Y %H:%M'),
            'data_vencimento': s.data_vencimento.strftime('%d/%m/%Y'),
        })

    # Status das assinaturas
    status_counts = dict(Assinatura.objects.values('status').annotate(count=Count('id')).values_list('status', 'count'))

    # Usuários recentes (últimos 25)
    active_user_ids = set(Assinatura.objects.filter(status='ativa', ativo=True).values_list('usuario_id', flat=True))
    if not active_user_ids:
        active_user_ids = set(Assinatura.objects.filter(status='ativa').values_list('usuario_id', flat=True))
    recent_users = User.objects.order_by('-date_joined')[:25]
    recent_users_list = []
    for u in recent_users:
        try:
            nome = u.profile.nome
            faixa = u.profile.get_faixa_display()
        except Profile.DoesNotExist:
            nome = u.username
            faixa = '-'
        recent_users_list.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'nome': nome,
            'faixa': faixa,
            'date_joined': u.date_joined.strftime('%d/%m/%Y'),
            'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else None,
            'premium': u.id in active_user_ids,
        })

    # Lista completa de cadastrados para gestão no painel
    all_users = User.objects.order_by('-date_joined')
    all_users_list = []
    for u in all_users:
        try:
            profile = u.profile
            nome = profile.nome
            faixa = profile.get_faixa_display()
            premium_profile = bool(profile.conta_premium)
        except Profile.DoesNotExist:
            nome = u.username
            faixa = '-'
            premium_profile = False
        premium_flag = (u.id in active_user_ids) or premium_profile
        all_users_list.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'nome': nome,
            'faixa': faixa,
            'premium': premium_flag,
            'is_active': u.is_active,
            'is_superuser': u.is_superuser,
            'date_joined': u.date_joined.strftime('%d/%m/%Y %H:%M'),
            'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else None,
        })

    # Últimos atualizados (proxy por último login)
    latest_updated_users = User.objects.order_by('-last_login', '-date_joined')[:20]
    latest_updated_list = []
    for u in latest_updated_users:
        try:
            nome = u.profile.nome
        except Profile.DoesNotExist:
            nome = u.username
        latest_updated_list.append({
            'id': u.id,
            'nome': nome,
            'email': u.email,
            'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else None,
            'date_joined': u.date_joined.strftime('%d/%m/%Y %H:%M'),
        })

    # Planos disponíveis
    plans = list(PlanoPremium.objects.filter(ativo=True).values('id', 'nome', 'preco', 'duracao_dias'))

    # Métricas adicionais: pagamentos por status, taxa de conversão
    payments_by_status = dict(Pagamento.objects.values('status').annotate(count=Count('id')).values_list('status', 'count'))
    total_payments = Pagamento.objects.count()
    approved_payments = Pagamento.objects.filter(status='approved').count()
    conversion_rate = (approved_payments / total_payments * 100) if total_payments > 0 else 0

    # Pagamentos pendentes recentes
    pending_payments = Pagamento.objects.filter(
        status__in=['pending', 'in_process'],
        data_criacao__gte=now - timedelta(days=7)
    ).order_by('-data_criacao')[:10]
    pending_list = [{
        'id': p.id,
        'email': p.usuario.email if p.usuario else '-',
        'valor': float(p.valor),
        'status': p.status,
        'data': p.data_criacao.strftime('%d/%m/%Y %H:%M'),
    } for p in pending_payments]

    return JsonResponse({
        'stats': {
            'active_subscriptions': active_count,
            'unique_premium_users': unique_premium,
            'total_revenue': float(total_revenue),
            'current_month_revenue': float(current_month_revenue),
            'last_month_revenue': float(last_month_revenue),
            'new_premium_this_month': new_premium_this_month,
            'new_premium_last_month': new_premium_last_month,
            'growth_percentage': round(growth, 1),
            'total_users': total_users,
            'users_this_month': users_this_month,
            'conversion_rate': round(conversion_rate, 1),
            'payments_by_status': payments_by_status,
            'approved_payments': approved_payments,
            'total_payments': total_payments,
        },
        'monthly_data': monthly_data,
        'recent_subscriptions': recent_subscriptions,
        'recent_users': recent_users_list,
        'all_users': all_users_list,
        'latest_updated_users': latest_updated_list,
        'status_counts': status_counts,
        'plans': plans,
        'pending_payments': pending_list,
        'current_date': now.strftime('%d/%m/%Y'),
    })


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_give_premium(request):
    """Atribuir plano premium. JSON: { user_id ou user_email, plan_id }."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id')
    user_email = data.get('user_email', '').strip()
    plan_id = data.get('plan_id')

    if not user_id and not user_email:
        return JsonResponse({'success': False, 'error': 'Informe user_id ou user_email'}, status=400)
    if not plan_id:
        return JsonResponse({'success': False, 'error': 'Informe plan_id'}, status=400)

    try:
        user = User.objects.get(id=user_id) if user_id else User.objects.get(email=user_email)
        plan = PlanoPremium.objects.get(id=plan_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'}, status=404)
    except PlanoPremium.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Plano não encontrado'}, status=404)

    existing = Assinatura.objects.filter(usuario=user, status='ativa').first()
    if existing:
        return JsonResponse({'success': False, 'error': f'{user.username} já possui assinatura ativa'}, status=400)

    data_inicio = timezone.now()
    data_vencimento = data_inicio + timedelta(days=plan.duracao_dias)
    Assinatura.objects.create(
        usuario=user,
        plano=plan,
        status='ativa',
        data_inicio=data_inicio,
        data_vencimento=data_vencimento,
        ativo=True,
    )
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={'nome': user.get_full_name() or user.username, 'idade': 18, 'faixa': 'branca'}
    )
    profile.conta_premium = True
    profile.data_vencimento_premium = data_vencimento
    profile.save(update_fields=['conta_premium', 'data_vencimento_premium'])
    clear_dashboard_cache()
    return JsonResponse({'success': True, 'message': f'Plano {plan.nome} atribuído para {user.username}'})


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_remove_premium(request):
    """Remover premium. JSON: { user_id }."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Informe user_id'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'}, status=404)

    ativas = Assinatura.objects.filter(usuario=user, status='ativa')
    if not ativas.exists():
        return JsonResponse({'success': False, 'error': f'{user.username} não possui assinatura ativa'}, status=400)

    count = 0
    for a in ativas:
        a.status = 'cancelada'
        a.ativo = False
        a.data_cancelamento = timezone.now()
        a.save()
        count += 1
    try:
        profile = user.profile
        profile.conta_premium = False
        profile.data_vencimento_premium = None
        profile.save(update_fields=['conta_premium', 'data_vencimento_premium'])
    except Profile.DoesNotExist:
        pass
    clear_dashboard_cache()
    return JsonResponse({'success': True, 'message': f'{count} assinatura(s) cancelada(s)'})


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_delete_user(request):
    """Excluir usuário. JSON: { user_id, confirm: "excluir" }."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id')
    confirm = (data.get('confirm') or '').lower().strip()

    if not user_id:
        return JsonResponse({'success': False, 'error': 'Informe user_id'}, status=400)
    if confirm != 'excluir':
        return JsonResponse({'success': False, 'error': 'Confirme digitando "excluir"'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'}, status=404)

    if user.id == request.user.id:
        return JsonResponse({'success': False, 'error': 'Você não pode excluir sua própria conta'}, status=400)
    if user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Não pode excluir outros administradores'}, status=400)

    with transaction.atomic():
        Assinatura.objects.filter(usuario=user).update(status='cancelada', ativo=False, data_cancelamento=timezone.now())
        user.delete()
    clear_dashboard_cache()
    return JsonResponse({'success': True, 'message': 'Usuário excluído'})


@login_required
@_require_superuser
@require_http_methods(['GET'])
def api_admin_user_detail(request, user_id):
    """Detalhes de um usuário."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'}, status=404)

    try:
        profile = user.profile
        nome = profile.nome
        faixa = profile.get_faixa_display()
    except Profile.DoesNotExist:
        nome = user.username
        faixa = '-'

    assinaturas = Assinatura.objects.filter(usuario=user).select_related('plano')
    pagamentos = Pagamento.objects.filter(usuario=user)
    total_pago = pagamentos.filter(status='approved').aggregate(t=Sum('valor'))['t'] or 0

    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'nome': nome,
            'faixa': faixa,
            'date_joined': user.date_joined.isoformat(),
            'premium': assinaturas.filter(status='ativa', ativo=True).exists(),
        },
        'assinaturas': [{
            'id': a.id,
            'plano': a.plano.nome,
            'status': a.status,
            'data_inicio': a.data_inicio.strftime('%d/%m/%Y'),
            'data_vencimento': a.data_vencimento.strftime('%d/%m/%Y'),
        } for a in assinaturas],
        'total_pagamentos': pagamentos.count(),
        'valor_total_pago': float(total_pago),
    })


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_refresh_cache(request):
    """Limpar cache do dashboard."""
    ok = clear_dashboard_cache()
    return JsonResponse({'success': ok})


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_ativar_manual(request):
    """Ativar assinatura manualmente. Query: email=xxx"""
    email = request.GET.get('email', '').strip()
    if not email:
        return JsonResponse({'success': False, 'error': 'Informe email'}, status=400)

    try:
        usuario = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado'}, status=404)

    plano = PlanoPremium.objects.filter(ativo=True).order_by('-preco').first()
    if not plano:
        return JsonResponse({'success': False, 'error': 'Nenhum plano ativo'}, status=400)

    data_inicio = timezone.now()
    data_vencimento = data_inicio + timedelta(days=plano.duracao_dias)
    Assinatura.objects.create(
        usuario=usuario,
        plano=plano,
        status='ativa',
        ativo=True,
        data_inicio=data_inicio,
        data_vencimento=data_vencimento,
        external_reference=uuid.uuid4(),
        subscription_id=f'manual_{usuario.id}_{int(timezone.now().timestamp())}',
    )
    try:
        p = usuario.profile
        p.conta_premium = True
        p.data_vencimento_premium = data_vencimento
        p.save()
    except Profile.DoesNotExist:
        pass
    clear_dashboard_cache()
    return JsonResponse({'success': True, 'message': f'Assinatura ativada para {usuario.email}'})


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_corrigir_assinaturas(request):
    """Corrigir assinaturas com ativo=False."""
    problematicas = Assinatura.objects.filter(status='ativa').filter(Q(ativo=False) | Q(ativo__isnull=True))
    corrigidas = 0
    for a in problematicas:
        a.ativo = True
        a.save()
        try:
            p = a.usuario.profile
            p.conta_premium = True
            p.data_vencimento_premium = a.data_vencimento
            p.save()
        except Profile.DoesNotExist:
            pass
        corrigidas += 1
    clear_dashboard_cache()
    return JsonResponse({'success': True, 'message': f'{corrigidas} assinaturas corrigidas', 'count': corrigidas})


@login_required
@_require_superuser
@require_http_methods(['POST'])
def api_admin_send_marketing_email(request):
    """
    Envia e-mail de remarketing para usuários selecionados ou todos.
    JSON: { subject, body, send_to: 'all'|'selected', user_ids?: [] }
    """
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    subject = (data.get('subject') or '').strip()
    body = (data.get('body') or '').strip()
    send_to = (data.get('send_to') or 'selected').strip()
    user_ids = data.get('user_ids') or []

    if not subject or not body:
        return JsonResponse({'success': False, 'error': 'Informe assunto e mensagem'}, status=400)

    users_qs = User.objects.filter(is_active=True).exclude(email__isnull=True).exclude(email='')
    if send_to != 'all':
        users_qs = users_qs.filter(id__in=user_ids)

    emails = sorted(set([u.email.strip().lower() for u in users_qs if '@' in u.email]))
    if not emails:
        return JsonResponse({'success': False, 'error': 'Nenhum destinatário válido'}, status=400)

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
    if not from_email:
        return JsonResponse({'success': False, 'error': 'DEFAULT_FROM_EMAIL não configurado'}, status=500)

    sent = 0
    batch_size = 100
    for i in range(0, len(emails), batch_size):
        batch = emails[i:i + batch_size]
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[from_email],
            bcc=batch,
        )
        msg.send(fail_silently=False)
        sent += len(batch)

    return JsonResponse({'success': True, 'sent': sent, 'message': f'E-mail enviado para {sent} destinatário(s)'})
