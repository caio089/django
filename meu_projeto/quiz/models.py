from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CategoriaQuiz(models.Model):
    """
    Modelo para categorizar as perguntas do quiz
    Organiza as perguntas por temas como técnica, história, regras, etc.
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da categoria")
    descricao = models.TextField(verbose_name="Descrição")
    cor = models.CharField(max_length=7, default='#007bff', verbose_name="Cor (hex)")
    icone = models.CharField(max_length=50, default='fas fa-question-circle', verbose_name="Ícone (Font Awesome)")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de exibição")
    ativo = models.BooleanField(default=True, verbose_name="Categoria ativa")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Categoria do Quiz"
        verbose_name_plural = "Categorias do Quiz"
        ordering = ['ordem', 'nome']


class Pergunta(models.Model):
    """
    Modelo para armazenar as perguntas do quiz
    Contém a pergunta, categoria e nível de dificuldade
    """
    NIVEL_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    ]
    
    categoria = models.ForeignKey(CategoriaQuiz, on_delete=models.CASCADE, related_name='perguntas')
    pergunta = models.TextField(verbose_name="Texto da pergunta")
    nivel_dificuldade = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='medio', verbose_name="Nível de dificuldade")
    pontos = models.PositiveIntegerField(default=10, verbose_name="Pontos por resposta correta")
    
    # Configurações da pergunta
    tempo_limite_segundos = models.PositiveIntegerField(default=30, verbose_name="Tempo limite (segundos)")
    explicacao = models.TextField(blank=True, null=True, verbose_name="Explicação da resposta")
    
    # Status e ordem
    ativa = models.BooleanField(default=True, verbose_name="Pergunta ativa")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.categoria.nome} - {self.pergunta[:50]}..."
    
    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        ordering = ['categoria', 'ordem']


class Alternativa(models.Model):
    """
    Modelo para as alternativas de cada pergunta
    Define as opções de resposta e qual é a correta
    """
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.TextField(verbose_name="Texto da alternativa")
    correta = models.BooleanField(default=False, verbose_name="Alternativa correta")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem da alternativa")
    
    def __str__(self):
        return f"{self.pergunta} - {self.texto[:30]}..."
    
    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        ordering = ['pergunta', 'ordem']


class SessaoQuiz(models.Model):
    """
    Modelo para registrar uma sessão de quiz realizada pelo usuário
    Armazena informações sobre o quiz completo
    """
    STATUS_CHOICES = [
        ('iniciada', 'Iniciada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('abandonada', 'Abandonada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessoes_quiz')
    categoria = models.ForeignKey(CategoriaQuiz, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status da sessão
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='iniciada')
    
    # Configurações da sessão
    total_perguntas = models.PositiveIntegerField(default=10, verbose_name="Total de perguntas")
    perguntas_respondidas = models.PositiveIntegerField(default=0, verbose_name="Perguntas respondidas")
    
    # Resultados
    pontuacao_total = models.PositiveIntegerField(default=0, verbose_name="Pontuação total")
    acertos = models.PositiveIntegerField(default=0, verbose_name="Número de acertos")
    erros = models.PositiveIntegerField(default=0, verbose_name="Número de erros")
    
    # Tempo
    tempo_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Tempo de início")
    tempo_fim = models.DateTimeField(null=True, blank=True, verbose_name="Tempo de fim")
    tempo_total_segundos = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tempo total (segundos)")
    
    # Experiência ganha
    experiencia_ganha = models.PositiveIntegerField(default=0, verbose_name="Experiência ganha")
    
    def __str__(self):
        return f"{self.usuario.profile.nome} - {self.categoria.nome if self.categoria else 'Quiz Geral'} - {self.status}"
    
    class Meta:
        verbose_name = "Sessão de Quiz"
        verbose_name_plural = "Sessões de Quiz"
        ordering = ['-tempo_inicio']


class RespostaUsuario(models.Model):
    """
    Modelo para armazenar as respostas individuais do usuário
    Registra cada resposta dada durante uma sessão de quiz
    """
    sessao = models.ForeignKey(SessaoQuiz, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    alternativa_escolhida = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    
    # Resultado da resposta
    correta = models.BooleanField(verbose_name="Resposta correta")
    pontos_ganhos = models.PositiveIntegerField(default=0, verbose_name="Pontos ganhos")
    
    # Tempo de resposta
    tempo_resposta_segundos = models.PositiveIntegerField(verbose_name="Tempo de resposta (segundos)")
    
    # Timestamp
    data_resposta = models.DateTimeField(auto_now_add=True, verbose_name="Data da resposta")
    
    def __str__(self):
        return f"{self.sessao.usuario.profile.nome} - {self.pergunta} - {'Correta' if self.correta else 'Incorreta'}"
    
    class Meta:
        verbose_name = "Resposta do Usuário"
        verbose_name_plural = "Respostas dos Usuários"
        ordering = ['-data_resposta']


class ProgressoUsuario(models.Model):
    """
    Modelo para acompanhar o progresso geral do usuário no sistema
    Armazena estatísticas e conquistas
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progresso')
    
    # Estatísticas gerais
    total_quiz_realizados = models.PositiveIntegerField(default=0, verbose_name="Total de quiz realizados")
    total_perguntas_respondidas = models.PositiveIntegerField(default=0, verbose_name="Total de perguntas respondidas")
    total_acertos = models.PositiveIntegerField(default=0, verbose_name="Total de acertos")
    total_erros = models.PositiveIntegerField(default=0, verbose_name="Total de erros")
    
    # Pontuação e experiência
    pontuacao_total = models.PositiveIntegerField(default=0, verbose_name="Pontuação total acumulada")
    experiencia_total = models.PositiveIntegerField(default=0, verbose_name="Experiência total")
    
    # Sequências
    sequencia_acertos = models.PositiveIntegerField(default=0, verbose_name="Sequência atual de acertos")
    melhor_sequencia_acertos = models.PositiveIntegerField(default=0, verbose_name="Melhor sequência de acertos")
    
    # Tempo
    tempo_total_quiz_segundos = models.PositiveIntegerField(default=0, verbose_name="Tempo total em quiz (segundos)")
    
    # Conquistas
    conquistas_desbloqueadas = models.JSONField(default=list, verbose_name="Conquistas desbloqueadas")
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def calcular_taxa_acerto(self):
        """Calcula a taxa de acerto do usuário"""
        if self.total_perguntas_respondidas == 0:
            return 0
        return round((self.total_acertos / self.total_perguntas_respondidas) * 100, 2)
    
    def __str__(self):
        return f"Progresso de {self.usuario.profile.nome}"
    
    class Meta:
        verbose_name = "Progresso do Usuário"
        verbose_name_plural = "Progressos dos Usuários"


class Conquista(models.Model):
    """
    Modelo para definir conquistas que os usuários podem desbloquear
    Sistema de gamificação para motivar o aprendizado
    """
    TIPO_CHOICES = [
        ('acertos', 'Acertos'),
        ('sequencia', 'Sequência'),
        ('tempo', 'Tempo'),
        ('quiz_completos', 'Quiz Completos'),
        ('categoria', 'Categoria'),
        ('especial', 'Especial'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome da conquista")
    descricao = models.TextField(verbose_name="Descrição")
    icone = models.CharField(max_length=50, default='fas fa-trophy', verbose_name="Ícone")
    cor = models.CharField(max_length=7, default='#FFD700', verbose_name="Cor")
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de conquista")
    requisito_valor = models.PositiveIntegerField(verbose_name="Valor do requisito")
    requisito_extra = models.JSONField(default=dict, blank=True, verbose_name="Requisitos extras")
    
    # Recompensas
    pontos_experiencia = models.PositiveIntegerField(default=0, verbose_name="Pontos de experiência")
    bonus_pontuacao = models.PositiveIntegerField(default=0, verbose_name="Bônus de pontuação")
    
    ativa = models.BooleanField(default=True, verbose_name="Conquista ativa")
    rara = models.BooleanField(default=False, verbose_name="Conquista rara")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Conquista"
        verbose_name_plural = "Conquistas"


class ProgressoQuiz(models.Model):
    """
    Modelo para salvar o progresso do quiz no banco de dados
    Sistema sequencial: só pode avançar após completar o nível anterior
    """
    DIFICULDADE_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Médio'),
        ('hard', 'Difícil'),
        ('expert', 'Expert'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresso_quiz')
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE_CHOICES, verbose_name="Dificuldade")
    pergunta_atual = models.PositiveIntegerField(default=0, verbose_name="Pergunta Atual")
    total_perguntas = models.PositiveIntegerField(default=0, verbose_name="Total de Perguntas")
    acertos = models.PositiveIntegerField(default=0, verbose_name="Acertos")
    erros = models.PositiveIntegerField(default=0, verbose_name="Erros")
    pontuacao = models.PositiveIntegerField(default=0, verbose_name="Pontuação")
    quiz_completo = models.BooleanField(default=False, verbose_name="Quiz Completo")
    nivel_desbloqueado = models.BooleanField(default=False, verbose_name="Nível Desbloqueado")
    data_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Início")
    data_fim = models.DateTimeField(null=True, blank=True, verbose_name="Data de Fim")
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['usuario', 'dificuldade']
        verbose_name = "Progresso do Quiz"
        verbose_name_plural = "Progressos do Quiz"
        ordering = ['usuario', 'dificuldade']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_dificuldade_display()} - {self.pergunta_atual}/{self.total_perguntas}"
    
    @classmethod
    def get_nivel_atual(cls, usuario):
        """
        Retorna o nível atual que o usuário pode acessar
        """
        # Verificar se completou o nível anterior
        niveis = ['easy', 'medium', 'hard', 'expert']
        
        for i, nivel in enumerate(niveis):
            try:
                progresso = cls.objects.get(usuario=usuario, dificuldade=nivel)
                if not progresso.quiz_completo:
                    return nivel  # Nível atual (não completado)
            except cls.DoesNotExist:
                # Se não existe progresso para este nível, verificar se o anterior foi completado
                if i == 0:  # Primeiro nível (easy) sempre disponível
                    return nivel
                else:
                    # Verificar se o nível anterior foi completado
                    try:
                        nivel_anterior = cls.objects.get(usuario=usuario, dificuldade=niveis[i-1])
                        if nivel_anterior.quiz_completo:
                            return nivel  # Pode acessar este nível
                        else:
                            return niveis[i-1]  # Deve completar o anterior primeiro
                    except cls.DoesNotExist:
                        return niveis[i-1]  # Deve completar o anterior primeiro
        
        return 'expert'  # Se completou todos os níveis
    
    @classmethod
    def pode_acessar_nivel(cls, usuario, nivel):
        """
        Verifica se o usuário pode acessar um determinado nível
        """
        niveis = ['easy', 'medium', 'hard', 'expert']
        
        if nivel not in niveis:
            return False
        
        nivel_index = niveis.index(nivel)
        
        # Primeiro nível sempre disponível
        if nivel_index == 0:
            return True
        
        # Verificar se o nível anterior foi completado
        nivel_anterior = niveis[nivel_index - 1]
        try:
            progresso_anterior = cls.objects.get(usuario=usuario, dificuldade=nivel_anterior)
            return progresso_anterior.quiz_completo
        except cls.DoesNotExist:
            return False