from django.db import models
from django.contrib.auth.models import User

class ProgressoElemento(models.Model):
    """
    Modelo para salvar o progresso dos elementos "Aprendi" em cada página
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresso_elementos_pag2')
    pagina = models.CharField(max_length=50, verbose_name="Página")
    elemento_id = models.CharField(max_length=100, verbose_name="ID do Elemento")
    elemento_tipo = models.CharField(max_length=50, verbose_name="Tipo do Elemento")  # proj-checkbox, imob-checkbox, etc.
    aprendido = models.BooleanField(default=False, verbose_name="Aprendido")
    data_aprendizado = models.DateTimeField(null=True, blank=True, verbose_name="Data do Aprendizado")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['usuario', 'pagina', 'elemento_id']
        verbose_name = "Progresso de Elemento"
        verbose_name_plural = "Progressos de Elementos"
        ordering = ['-data_atualizacao']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pagina} - {self.elemento_id} - {'Aprendido' if self.aprendido else 'Não Aprendido'}"