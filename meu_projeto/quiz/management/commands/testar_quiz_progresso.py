from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import ProgressoQuiz
from django.utils import timezone

class Command(BaseCommand):
    help = 'Testa o sistema de progresso do quiz'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testando sistema de progresso do quiz...')
        
        # Verificar se há usuários
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING('⚠️ Nenhum usuário encontrado no banco de dados'))
            return
        
        user = users.first()
        self.stdout.write(f'👤 Usando usuário: {user.username}')
        
        # Verificar progressos existentes
        progressos = ProgressoQuiz.objects.filter(usuario=user)
        self.stdout.write(f'📊 Progressos encontrados: {progressos.count()}')
        
        for progresso in progressos:
            self.stdout.write(f'   - {progresso.dificuldade}: {progresso.pergunta_atual}/{progresso.total_perguntas} (Progresso: {progresso.progresso_percentual:.1f}%)')
        
        # Testar criação de novo progresso
        self.stdout.write('\n🔧 Testando criação de novo progresso...')
        
        # Limpar progresso de teste se existir
        ProgressoQuiz.objects.filter(usuario=user, dificuldade='easy').delete()
        
        # Criar novo progresso
        progresso = ProgressoQuiz.get_progresso_ou_criar(user, 'easy')
        self.stdout.write(f'✅ Progresso criado: {progresso.dificuldade} - {progresso.pergunta_atual}/{progresso.total_perguntas}')
        
        # Simular avanço de pergunta
        progresso.avancar_pergunta(acertou=True)
        self.stdout.write(f'📈 Após 1 pergunta: {progresso.pergunta_atual}/{progresso.total_perguntas} (Progresso: {progresso.progresso_percentual:.1f}%)')
        
        # Simular mais algumas perguntas
        for i in range(5):
            progresso.avancar_pergunta(acertou=(i % 2 == 0))
        
        self.stdout.write(f'📈 Após 6 perguntas: {progresso.pergunta_atual}/{progresso.total_perguntas} (Progresso: {progresso.progresso_percentual:.1f}%)')
        self.stdout.write(f'   Acertos: {progresso.acertos}, Erros: {progresso.erros}, Pontuação: {progresso.pontuacao}')
        
        # Testar reinicialização
        self.stdout.write('\n🔄 Testando reinicialização...')
        progresso.reiniciar_quiz()
        self.stdout.write(f'🔄 Após reiniciar: {progresso.pergunta_atual}/{progresso.total_perguntas} (Progresso: {progresso.progresso_percentual:.1f}%)')
        
        self.stdout.write(self.style.SUCCESS('✅ Teste de progresso concluído com sucesso!'))
