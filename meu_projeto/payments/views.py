from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import json
from .models import PaymentPlan, UserSubscription, Payment

# Planos disponíveis
PLANS = {
    'monthly': {
        'name': 'Plano Mensal',
        'price': 29.00,
        'discount': 0,
        'duration': 1,  # meses
        'features': [
            'Acesso a todas as faixas',
            'Quiz interativo completo',
            'Rolamentos do Judô',
            'História do Judô',
            'Palavras em Japonês',
            'Regras do Judô',
            'Suporte por email'
        ]
    },
    'semester': {
        'name': 'Plano Semestral',
        'price': 149.00,
        'original_price': 174.00,
        'discount': 14,
        'duration': 6,  # meses
        'features': [
            'Acesso a todas as faixas',
            'Quiz interativo completo',
            'Rolamentos do Judô',
            'História do Judô',
            'Palavras em Japonês',
            'Regras do Judô',
            'Conteúdo exclusivo',
            'Suporte prioritário',
            'Certificado digital'
        ]
    },
    'annual': {
        'name': 'Plano Anual',
        'price': 249.00,
        'original_price': 348.00,
        'discount': 28,
        'duration': 12,  # meses
        'features': [
            'Acesso a todas as faixas',
            'Quiz interativo completo',
            'Rolamentos do Judô',
            'História do Judô',
            'Palavras em Japonês',
            'Regras do Judô',
            'Conteúdo exclusivo',
            'Suporte prioritário',
            'Certificado digital',
            'Mentoria personalizada',
            'Acesso vitalício'
        ]
    }
}

def pricing_view(request):
    """Página de preços"""
    return render(request, 'payments/pricing.html', {
        'plans': PLANS
    })

@login_required
def checkout_view(request, plan_id):
    """Página de checkout para um plano específico"""
    if plan_id not in PLANS:
        messages.error(request, 'Plano inválido.')
        return redirect('pricing')
    
    plan = PLANS[plan_id]
    return render(request, 'payments/checkout.html', {
        'plan': plan,
        'plan_id': plan_id
    })

@login_required
def simulate_payment_view(request, plan_id):
    """Simula um pagamento para teste"""
    if plan_id not in PLANS:
        messages.error(request, 'Plano inválido.')
        return redirect('pricing')
    
    plan_data = PLANS[plan_id]
    
    # Criar plano no banco se não existir
    plan, created = PaymentPlan.objects.get_or_create(
        name=plan_data['name'],
        defaults={
            'price': plan_data['price'],
            'duration_months': plan_data['duration'],
            'features': plan_data['features']
        }
    )
    
    # Criar assinatura para o usuário
    subscription = UserSubscription.create_subscription(request.user, plan)
    
    # Criar registro de pagamento
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=plan.price,
        status='completed',
        payment_method='simulado',
        payment_id=f'sim_{request.user.id}_{timezone.now().timestamp()}',
        completed_at=timezone.now()
    )
    
    messages.success(request, f'Pagamento simulado realizado com sucesso! Acesso liberado por {plan.duration_months} meses.')
    return redirect('index')

@login_required
def payment_success_view(request):
    """Página de sucesso do pagamento"""
    return render(request, 'payments/success.html')

@login_required
def payment_cancel_view(request):
    """Página de cancelamento do pagamento"""
    return render(request, 'payments/cancel.html')

@csrf_exempt
def webhook_view(request):
    """Webhook para receber notificações de pagamento"""
    if request.method == 'POST':
        # Aqui será implementada a lógica do webhook
        # para processar notificações dos gateways de pagamento
        pass
    
    return JsonResponse({'status': 'ok'})

def access_denied_view(request):
    """Página de acesso negado para usuários não pagantes"""
    return render(request, 'payments/access_denied.html')

def progress_example_view(request):
    """Página de exemplo do sistema de progresso"""
    return render(request, 'payments/progress_example.html')

def simple_usage_guide_view(request):
    """Guia de uso simplificado do sistema de progresso"""
    return render(request, 'payments/simple_usage_guide.html')