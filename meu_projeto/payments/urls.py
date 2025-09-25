from django.urls import path
from . import views
from . import progress_views

urlpatterns = [
    path('', views.pricing_view, name='pricing'),
    path('checkout/<str:plan_id>/', views.checkout_view, name='checkout'),
    path('simulate/<str:plan_id>/', views.simulate_payment_view, name='simulate_payment'),
    path('success/', views.payment_success_view, name='payment_success'),
    path('cancel/', views.payment_cancel_view, name='payment_cancel'),
    path('webhook/', views.webhook_view, name='payment_webhook'),
    path('access-denied/', views.access_denied_view, name='access_denied'),
    
    # URLs para progresso do usuário
    path('progress/save-faixa/', progress_views.save_faixa_progress, name='save_faixa_progress'),
    path('progress/save-quiz/', progress_views.save_quiz_progress, name='save_quiz_progress'),
    path('progress/save-rolamentos/', progress_views.save_rolamentos_progress, name='save_rolamentos_progress'),
    path('progress/get/', progress_views.get_user_progress, name='get_user_progress'),
    path('progress/create-session/', progress_views.create_user_session, name='create_user_session'),
    path('progress/example/', views.progress_example_view, name='progress_example'),
    path('progress/guide/', views.simple_usage_guide_view, name='simple_usage_guide'),
]
