from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    idade = models.PositiveIntegerField()
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
    faixa = models.CharField(max_length=10, choices=FAIXAS)

    def __str__(self):
        return self.nome
