from django.contrib import admin
from .models import QuizRanking, ProgressoUsuario

@admin.register(QuizRanking)
class QuizRankingAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'dojo', 'xp_total', 'nivel_quiz', 'categoria_titulo', 'cidade', 'usuario', 'data_atualizacao')
    list_filter = ('nivel_quiz', 'categoria_titulo')
    search_fields = ('nickname', 'cidade')
    ordering = ('-xp_total',)
    readonly_fields = ('data_criacao', 'data_atualizacao')
