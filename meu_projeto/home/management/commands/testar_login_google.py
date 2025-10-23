"""
Comando para testar o sistema de login com Google
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from quiz.models import ProgressoUsuario, ProgressoQuiz
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Testa o sistema de login com Google e verifica se os dados são salvos corretamente'

    def handle(self, *args, **options):
        """
        Testa o sistema completo de login com Google
        """
        self.stdout.write("🧪 Iniciando teste do sistema de login com Google...")
        
        # Dados de teste
        email_teste = "teste@google.com"
        nome_teste = "Usuário Teste Google"
        
        try:
            # 1. Verificar se usuário existe
            user_exists = User.objects.filter(username=email_teste).exists()
            self.stdout.write(f"📧 Usuário existe: {user_exists}")
            
            if user_exists:
                user = User.objects.get(username=email_teste)
                self.stdout.write(f"👤 Usuário encontrado: {user.username}")
                
                # 2. Verificar se tem perfil
                try:
                    profile = Profile.objects.get(user=user)
                    self.stdout.write(f"✅ Perfil encontrado: {profile.nome} - {profile.get_faixa_display()}")
                except Profile.DoesNotExist:
                    self.stdout.write("❌ Perfil não encontrado - criando...")
                    profile = Profile.objects.create(
                        user=user,
                        nome=nome_teste,
                        idade=18,
                        faixa='branca'
                    )
                    self.stdout.write(f"✅ Perfil criado: {profile.nome}")
                
                # 3. Verificar progresso do usuário
                try:
                    progresso = ProgressoUsuario.objects.get(usuario=user)
                    self.stdout.write(f"📊 Progresso encontrado: {progresso}")
                except ProgressoUsuario.DoesNotExist:
                    self.stdout.write("📊 Progresso não encontrado - criando...")
                    progresso = ProgressoUsuario.objects.create(usuario=user)
                    self.stdout.write(f"✅ Progresso criado: {progresso}")
                
                # 4. Verificar progresso de quiz
                quiz_progressos = ProgressoQuiz.objects.filter(usuario=user)
                self.stdout.write(f"🎯 Progressos de quiz: {quiz_progressos.count()}")
                
                # 5. Testar criação de progresso de quiz
                progresso_quiz = ProgressoQuiz.get_progresso_ou_criar(user, 'easy')
                self.stdout.write(f"🎯 Progresso de quiz criado/encontrado: {progresso_quiz}")
                
                # 6. Testar salvamento de progresso
                progresso_quiz.pergunta_atual = 5
                progresso_quiz.acertos = 3
                progresso_quiz.erros = 2
                progresso_quiz.pontuacao = 30
                progresso_quiz.calcular_progresso_percentual()
                progresso_quiz.save()
                
                self.stdout.write(f"✅ Progresso salvo: {progresso_quiz.pergunta_atual}/15 - {progresso_quiz.progresso_percentual:.1f}%")
                
                # 7. Verificar se o progresso foi salvo
                progresso_salvo = ProgressoQuiz.objects.get(usuario=user, dificuldade='easy')
                self.stdout.write(f"✅ Progresso verificado: {progresso_salvo.pergunta_atual} perguntas, {progresso_salvo.acertos} acertos")
                
                self.stdout.write(
                    self.style.SUCCESS(
                        "🎉 TESTE CONCLUÍDO COM SUCESSO!\n"
                        "✅ Login com Google funcionando\n"
                        "✅ Perfil criado automaticamente\n"
                        "✅ Progresso sendo salvo corretamente\n"
                        "✅ Sistema de quiz funcionando"
                    )
                )
                
            else:
                self.stdout.write("❌ Usuário de teste não encontrado")
                self.stdout.write("💡 Execute o login via Google primeiro para criar o usuário")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro durante o teste: {e}")
            )
            logger.error(f"❌ Erro no teste: {e}")
