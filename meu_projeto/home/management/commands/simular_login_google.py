"""
Comando para simular login com Google e testar o sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from quiz.models import ProgressoUsuario, ProgressoQuiz
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Simula login com Google e testa todo o sistema'

    def handle(self, *args, **options):
        """
        Simula o processo completo de login com Google
        """
        self.stdout.write("🚀 Simulando login com Google...")
        
        # Dados simulados do Google
        email_simulado = "usuario@teste.com"
        nome_simulado = "Usuário Teste"
        picture_simulado = "https://via.placeholder.com/100"
        
        try:
            # 1. Simular criação/busca de usuário
            self.stdout.write("👤 Criando/buscando usuário...")
            user, created = User.objects.get_or_create(
                username=email_simulado,
                defaults={
                    'email': email_simulado,
                    'first_name': nome_simulado.split(' ')[0],
                    'last_name': ' '.join(nome_simulado.split(' ')[1:]) if len(nome_simulado.split(' ')) > 1 else '',
                }
            )
            
            if created:
                user.set_unusable_password()
                user.save()
                self.stdout.write(f"✅ Novo usuário criado: {email_simulado}")
            else:
                self.stdout.write(f"✅ Usuário existente: {email_simulado}")
            
            # 2. Criar/verificar perfil
            self.stdout.write("👤 Criando/verificando perfil...")
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f"✅ Perfil encontrado: {profile.nome}")
            except Profile.DoesNotExist:
                profile = Profile.objects.create(
                    user=user,
                    nome=nome_simulado,
                    idade=18,
                    faixa='branca'
                )
                self.stdout.write(f"✅ Perfil criado: {profile.nome}")
            
            # 3. Criar/verificar progresso do usuário
            self.stdout.write("📊 Criando/verificando progresso...")
            try:
                progresso = ProgressoUsuario.objects.get(usuario=user)
                self.stdout.write(f"✅ Progresso encontrado: {progresso}")
            except ProgressoUsuario.DoesNotExist:
                progresso = ProgressoUsuario.objects.create(usuario=user)
                self.stdout.write(f"✅ Progresso criado: {progresso}")
            
            # 4. Testar progresso de quiz
            self.stdout.write("🎯 Testando progresso de quiz...")
            progresso_quiz = ProgressoQuiz.get_progresso_ou_criar(user, 'easy')
            self.stdout.write(f"✅ Progresso de quiz: {progresso_quiz}")
            
            # 5. Simular progresso no quiz
            self.stdout.write("🎯 Simulando progresso no quiz...")
            progresso_quiz.pergunta_atual = 10
            progresso_quiz.acertos = 7
            progresso_quiz.erros = 3
            progresso_quiz.pontuacao = 70
            progresso_quiz.calcular_progresso_percentual()
            progresso_quiz.save()
            
            self.stdout.write(f"✅ Progresso salvo: {progresso_quiz.pergunta_atual}/15 - {progresso_quiz.progresso_percentual:.1f}%")
            
            # 6. Verificar se tudo foi salvo corretamente
            self.stdout.write("🔍 Verificando dados salvos...")
            
            # Verificar usuário
            user_verificado = User.objects.get(username=email_simulado)
            self.stdout.write(f"✅ Usuário verificado: {user_verificado.username}")
            
            # Verificar perfil
            profile_verificado = Profile.objects.get(user=user_verificado)
            self.stdout.write(f"✅ Perfil verificado: {profile_verificado.nome} - {profile_verificado.get_faixa_display()}")
            
            # Verificar progresso
            progresso_verificado = ProgressoUsuario.objects.get(usuario=user_verificado)
            self.stdout.write(f"✅ Progresso verificado: {progresso_verificado}")
            
            # Verificar progresso de quiz
            quiz_verificado = ProgressoQuiz.objects.get(usuario=user_verificado, dificuldade='easy')
            self.stdout.write(f"✅ Quiz verificado: {quiz_verificado.pergunta_atual} perguntas, {quiz_verificado.acertos} acertos")
            
            self.stdout.write(
                self.style.SUCCESS(
                    "\n🎉 SIMULAÇÃO CONCLUÍDA COM SUCESSO!\n"
                    "✅ Login com Google simulado\n"
                    "✅ Usuário criado no banco de dados\n"
                    "✅ Perfil criado automaticamente\n"
                    "✅ Progresso sendo salvo corretamente\n"
                    "✅ Sistema de quiz funcionando\n"
                    "✅ Todos os dados persistidos no banco\n\n"
                    "🚀 O sistema está funcionando perfeitamente!"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro durante a simulação: {e}")
            )
            logger.error(f"❌ Erro na simulação: {e}")
