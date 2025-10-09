from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import random
import string
from datetime import datetime, timedelta

# Create your models here.

class Profile(models.Model):
    """
    Modelo de perfil do usuário que estende o User padrão do Django
    Armazena informações específicas do judoca como nome, idade e faixa atual
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nome = models.CharField(max_length=150, verbose_name="Nome completo")
    idade = models.PositiveIntegerField(verbose_name="Idade")
    
    # Opções de faixas do judô
    FAIXAS = [
        ('branca', 'Branca'),
        ('cinza', 'Cinza'),
        ('azul', 'Azul'),
        ('amarela', 'Amarela'),
        ('laranja', 'Laranja'),
        ('verde', 'Verde'),
        ('roxa', 'Roxa'),
        ('marrom', 'Marrom'),
        ('preta', 'Preta'),
    ]
    faixa = models.CharField(max_length=10, choices=FAIXAS, default='branca', verbose_name="Faixa atual")
    
    # Campos de progresso
    pontos_experiencia = models.PositiveIntegerField(default=0, verbose_name="Pontos de experiência")
    nivel = models.PositiveIntegerField(default=1, verbose_name="Nível")
    
    # Campos de status da conta
    conta_premium = models.BooleanField(default=False, verbose_name="Conta Premium")
    data_vencimento_premium = models.DateTimeField(null=True, blank=True, verbose_name="Data de vencimento Premium")
    
    # Campos de configuração
    notificacoes_ativadas = models.BooleanField(default=True, verbose_name="Notificações ativadas")
    tema_preferido = models.CharField(max_length=20, default='claro', choices=[('claro', 'Claro'), ('escuro', 'Escuro')])
    
    # Timestamps (comentados para evitar conflito com dados existentes)
    # data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    # data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última atualização")

    def __str__(self):
        return f"{self.nome} - {self.get_faixa_display()}"

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"


class HistoricoFaixas(models.Model):
    """
    Modelo para armazenar o histórico de progressão de faixas do usuário
    Registra quando o usuário mudou de faixa e por qual motivo
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_faixas')
    faixa_anterior = models.CharField(max_length=10, verbose_name="Faixa anterior")
    faixa_atual = models.CharField(max_length=10, verbose_name="Faixa atual")
    data_mudanca = models.DateTimeField(auto_now_add=True, verbose_name="Data da mudança")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo da mudança")
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.faixa_anterior} → {self.faixa_atual}"
    
    class Meta:
        verbose_name = "Histórico de Faixas"
        verbose_name_plural = "Históricos de Faixas"
        ordering = ['-data_mudanca']


class CodigoRecuperacao(models.Model):
    """
    Modelo para armazenar códigos de recuperação de senha
    """
    email = models.EmailField(verbose_name="Email do usuário")
    codigo = models.CharField(max_length=6, verbose_name="Código de 6 dígitos")
    usado = models.BooleanField(default=False, verbose_name="Código já foi usado")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    data_expiracao = models.DateTimeField(verbose_name="Data de expiração")
    
    @classmethod
    def gerar_codigo(cls, email):
        """Gera um novo código de recuperação para o email"""
        # Deletar códigos antigos para este email
        cls.objects.filter(email=email).delete()
        
        # Gerar código de 6 dígitos
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Criar novo código (expira em 15 minutos)
        data_expiracao = datetime.now() + timedelta(minutes=15)
        
        return cls.objects.create(
            email=email,
            codigo=codigo,
            data_expiracao=data_expiracao
        )
    
    def is_valido(self):
        """Verifica se o código ainda é válido"""
        return not self.usado and datetime.now() < self.data_expiracao
    
    def marcar_como_usado(self):
        """Marca o código como usado"""
        self.usado = True
        self.save()
    
    def __str__(self):
        return f"Código {self.codigo} para {self.email}"
    
    class Meta:
        verbose_name = "Código de Recuperação"
        verbose_name_plural = "Códigos de Recuperação"
        ordering = ['-data_criacao']