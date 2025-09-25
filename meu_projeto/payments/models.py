from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class PaymentPlan(models.Model):
    """Modelo para os planos de pagamento"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    """Modelo para assinaturas dos usuários"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, default='pix')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    def is_valid(self):
        """Verifica se a assinatura ainda é válida"""
        return self.is_active and timezone.now() < self.end_date
    
    def extend_subscription(self, months):
        """Estende a assinatura por X meses"""
        if self.is_valid():
            self.end_date += timedelta(days=months * 30)
        else:
            self.end_date = timezone.now() + timedelta(days=months * 30)
        self.is_active = True
        self.save()
    
    @classmethod
    def create_subscription(cls, user, plan):
        """Cria uma nova assinatura"""
        end_date = timezone.now() + timedelta(days=plan.duration_months * 30)
        subscription, created = cls.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'end_date': end_date,
                'is_active': True
            }
        )
        return subscription

class Payment(models.Model):
    """Modelo para registrar pagamentos"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - R$ {self.amount}"

class UserProgress(models.Model):
    """Modelo para armazenar progresso geral do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_time_spent = models.IntegerField(default=0)  # em minutos
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Progresso"

class FaixaProgress(models.Model):
    """Modelo para progresso em cada faixa"""
    FAIXA_CHOICES = [
        ('cinza', 'Faixa Cinza'),
        ('azul', 'Faixa Azul'),
        ('amarela', 'Faixa Amarela'),
        ('laranja', 'Faixa Laranja'),
        ('verde', 'Faixa Verde'),
        ('roxa', 'Faixa Roxa'),
        ('marrom', 'Faixa Marrom'),
        ('preta', 'Faixa Preta'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faixa = models.CharField(max_length=20, choices=FAIXA_CHOICES)
    progress_percentage = models.IntegerField(default=0)  # 0-100
    time_spent = models.IntegerField(default=0)  # em minutos
    lessons_completed = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=10)
    last_accessed = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'faixa']
    
    def __str__(self):
        return f"{self.user.username} - {self.faixa} - {self.progress_percentage}%"

class QuizProgress(models.Model):
    """Modelo para progresso no quiz"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    progress_percentage = models.IntegerField(default=0)  # 0-100
    current_level = models.IntegerField(default=1)
    total_time_spent = models.IntegerField(default=0)  # em minutos
    last_quiz_date = models.DateTimeField(auto_now=True)
    best_score = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - Quiz - {self.progress_percentage}%"

class RolamentosProgress(models.Model):
    """Modelo para progresso nos rolamentos"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_rolamentos = models.IntegerField(default=0)
    completed_rolamentos = models.IntegerField(default=0)
    progress_percentage = models.IntegerField(default=0)  # 0-100
    time_spent = models.IntegerField(default=0)  # em minutos
    last_accessed = models.DateTimeField(auto_now=True)
    current_rolamento = models.CharField(max_length=50, default='')
    
    def __str__(self):
        return f"{self.user.username} - Rolamentos - {self.progress_percentage}%"

class UserSession(models.Model):
    """Modelo para armazenar sessões de login"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"