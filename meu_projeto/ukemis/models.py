from django.db import models
from django.contrib.auth.models import User

class TipoUkemi(models.Model):
    """
    Modelo para definir os tipos de ukemi (técnicas de queda) do judô
    Organiza as técnicas por categoria e nível de dificuldade
    """
    nome = models.CharField(max_length=100, verbose_name="Nome do ukemi")
    descricao = models.TextField(verbose_name="Descrição da técnica")
    categoria = models.CharField(max_length=50, choices=[
        ('mae', 'Mae Ukemi'),
        ('ushiro', 'Ushiro Ukemi'),
        ('yoko', 'Yoko Ukemi'),
        ('zenpo', 'Zenpo Kaiten Ukemi'),
    ], verbose_name="Categoria")
    
    # Dificuldade e requisitos
    nivel_dificuldade = models.PositiveIntegerField(default=1, verbose_name="Nível de dificuldade")
    faixa_minima = models.CharField(max_length=10, choices=[
        ('branca', 'Branca'),
        ('cinza', 'Cinza'),
        ('azul', 'Azul'),
        ('amarela', 'Amarela'),
        ('laranja', 'Laranja'),
        ('verde', 'Verde'),
        ('roxa', 'Roxa'),
        ('marrom', 'Marrom'),
        ('preta', 'Preta'),
    ], default='branca', verbose_name="Faixa mínima")
    
    # Recursos multimídia
    video_url = models.URLField(blank=True, null=True, verbose_name="URL do vídeo")
    imagem_demonstracao = models.ImageField(upload_to='ukemis/', blank=True, null=True, verbose_name="Imagem de demonstração")
    
    # Configurações
    ativo = models.BooleanField(default=True, verbose_name="Tipo ativo")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de exibição")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"
    
    class Meta:
        verbose_name = "Tipo de Ukemi"
        verbose_name_plural = "Tipos de Ukemi"
        ordering = ['categoria', 'nivel_dificuldade', 'ordem']


class ProgressoUkemi(models.Model):
    """
    Modelo para acompanhar o progresso do usuário em cada tipo de ukemi
    Registra tentativas, sucessos e melhorias
    """
    STATUS_CHOICES = [
        ('nao_iniciado', 'Não Iniciado'),
        ('aprendendo', 'Aprendendo'),
        ('praticando', 'Praticando'),
        ('dominado', 'Dominado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresso_ukemis')
    tipo_ukemi = models.ForeignKey(TipoUkemi, on_delete=models.CASCADE, related_name='progressos')
    
    # Status do progresso
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciado')
    
    # Estatísticas
    total_tentativas = models.PositiveIntegerField(default=0, verbose_name="Total de tentativas")
    tentativas_sucesso = models.PositiveIntegerField(default=0, verbose_name="Tentativas com sucesso")
    melhor_tempo = models.PositiveIntegerField(null=True, blank=True, verbose_name="Melhor tempo (segundos)")
    
    # Pontuação e experiência
    pontos_conquistados = models.PositiveIntegerField(default=0, verbose_name="Pontos conquistados")
    experiencia_ganha = models.PositiveIntegerField(default=0, verbose_name="Experiência ganha")
    
    # Timestamps
    data_primeira_tentativa = models.DateTimeField(null=True, blank=True, verbose_name="Primeira tentativa")
    data_ultima_tentativa = models.DateTimeField(null=True, blank=True, verbose_name="Última tentativa")
    data_dominio = models.DateTimeField(null=True, blank=True, verbose_name="Data de domínio")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def calcular_taxa_sucesso(self):
        """Calcula a taxa de sucesso do usuário neste ukemi"""
        if self.total_tentativas == 0:
            return 0
        return round((self.tentativas_sucesso / self.total_tentativas) * 100, 2)
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.tipo_ukemi.nome} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Progresso de Ukemi"
        verbose_name_plural = "Progressos de Ukemi"
        unique_together = ['usuario', 'tipo_ukemi']


class SessaoPratica(models.Model):
    """
    Modelo para registrar sessões de prática de ukemi
    Permite acompanhar o progresso detalhado de cada sessão
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessoes_pratica_ukemi')
    tipo_ukemi = models.ForeignKey(TipoUkemi, on_delete=models.CASCADE, related_name='sessoes_pratica')
    
    # Configurações da sessão
    duracao_minutos = models.PositiveIntegerField(verbose_name="Duração da sessão (minutos)")
    total_repeticoes = models.PositiveIntegerField(verbose_name="Total de repetições")
    
    # Resultados da sessão
    repeticoes_sucesso = models.PositiveIntegerField(verbose_name="Repetições com sucesso")
    melhor_tempo = models.PositiveIntegerField(null=True, blank=True, verbose_name="Melhor tempo (segundos)")
    tempo_medio = models.FloatField(null=True, blank=True, verbose_name="Tempo médio (segundos)")
    
    # Observações e notas
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    dificuldades = models.TextField(blank=True, null=True, verbose_name="Dificuldades encontradas")
    melhorias = models.TextField(blank=True, null=True, verbose_name="Melhorias observadas")
    
    # Experiência e pontos
    experiencia_ganha = models.PositiveIntegerField(default=0, verbose_name="Experiência ganha")
    pontos_conquistados = models.PositiveIntegerField(default=0, verbose_name="Pontos conquistados")
    
    # Timestamps
    data_inicio = models.DateTimeField(verbose_name="Data de início")
    data_fim = models.DateTimeField(verbose_name="Data de fim")
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def calcular_taxa_sucesso(self):
        """Calcula a taxa de sucesso da sessão"""
        if self.total_repeticoes == 0:
            return 0
        return round((self.repeticoes_sucesso / self.total_repeticoes) * 100, 2)
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.tipo_ukemi.nome} - {self.data_inicio.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = "Sessão de Prática de Ukemi"
        verbose_name_plural = "Sessões de Prática de Ukemi"
        ordering = ['-data_inicio']


class DesafioUkemi(models.Model):
    """
    Modelo para criar desafios específicos de ukemi
    Sistema de gamificação para motivar a prática
    """
    TIPO_CHOICES = [
        ('tempo', 'Desafio de Tempo'),
        ('precisao', 'Desafio de Precisão'),
        ('resistencia', 'Desafio de Resistência'),
        ('tecnica', 'Desafio Técnico'),
    ]
    
    DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
        ('expert', 'Expert'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome do desafio")
    descricao = models.TextField(verbose_name="Descrição")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de desafio")
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE_CHOICES, verbose_name="Dificuldade")
    
    # Configurações do desafio
    tipo_ukemi = models.ForeignKey(TipoUkemi, on_delete=models.CASCADE, related_name='desafios')
    objetivo = models.TextField(verbose_name="Objetivo do desafio")
    criterios_sucesso = models.JSONField(default=dict, verbose_name="Critérios de sucesso")
    
    # Recompensas
    pontos_experiencia = models.PositiveIntegerField(default=0, verbose_name="Pontos de experiência")
    bonus_pontuacao = models.PositiveIntegerField(default=0, verbose_name="Bônus de pontuação")
    
    # Status
    ativo = models.BooleanField(default=True, verbose_name="Desafio ativo")
    disponivel_premium = models.BooleanField(default=False, verbose_name="Disponível apenas para Premium")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True, verbose_name="Data de expiração")
    
    def __str__(self):
        return f"{self.nome} - {self.get_dificuldade_display()}"
    
    class Meta:
        verbose_name = "Desafio de Ukemi"
        verbose_name_plural = "Desafios de Ukemi"
        ordering = ['dificuldade', 'nome']


class ConquistaUkemi(models.Model):
    """
    Modelo para registrar conquistas específicas de ukemi
    Relaciona usuários com conquistas desbloqueadas
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conquistas_ukemi')
    desafio = models.ForeignKey(DesafioUkemi, on_delete=models.CASCADE, related_name='conquistas')
    
    # Resultados da conquista
    pontuacao_final = models.PositiveIntegerField(verbose_name="Pontuação final")
    tempo_realizacao = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tempo de realização (segundos)")
    criterios_atendidos = models.JSONField(default=dict, verbose_name="Critérios atendidos")
    
    # Status
    conquistada = models.BooleanField(default=False, verbose_name="Conquista desbloqueada")
    nivel_conquista = models.CharField(max_length=20, choices=[
        ('bronze', 'Bronze'),
        ('prata', 'Prata'),
        ('ouro', 'Ouro'),
        ('diamante', 'Diamante'),
    ], null=True, blank=True, verbose_name="Nível da conquista")
    
    # Timestamps
    data_tentativa = models.DateTimeField(auto_now_add=True, verbose_name="Data da tentativa")
    data_conquista = models.DateTimeField(null=True, blank=True, verbose_name="Data da conquista")
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.desafio.nome}"
    
    class Meta:
        verbose_name = "Conquista de Ukemi"
        verbose_name_plural = "Conquistas de Ukemi"
        unique_together = ['usuario', 'desafio']
        ordering = ['-data_tentativa']
