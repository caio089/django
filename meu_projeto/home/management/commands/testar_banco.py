"""
Comando para testar conexão e estado do banco de dados
Execute: python manage.py testar_banco
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from home.models import Profile, HistoricoFaixas
from quiz.models import CategoriaQuiz, Pergunta, Alternativa
from payments.models import PlanoPremium, ConfiguracaoPagamento

class Command(BaseCommand):
    help = 'Testa conexão e verifica estado do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("🔍 TESTE COMPLETO DO BANCO DE DADOS")
        self.stdout.write("=" * 70)
        
        # 1. Testar conexão
        self.stdout.write("\n1️⃣  TESTANDO CONEXÃO...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f"   ✅ Conexão OK!"))
                self.stdout.write(f"   📊 PostgreSQL: {version.split(',')[0]}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erro de conexão: {e}"))
            return
        
        # 2. Verificar tabelas principais
        self.stdout.write("\n2️⃣  VERIFICANDO TABELAS...")
        
        tabelas_status = []
        
        try:
            count = User.objects.count()
            tabelas_status.append(("auth_user (Usuários)", count, True))
        except Exception as e:
            tabelas_status.append(("auth_user (Usuários)", 0, False))
        
        try:
            count = Profile.objects.count()
            tabelas_status.append(("home_profile (Perfis)", count, True))
        except Exception as e:
            tabelas_status.append(("home_profile (Perfis)", 0, False))
        
        try:
            count = CategoriaQuiz.objects.count()
            tabelas_status.append(("quiz_categoriaquiz (Categorias)", count, True))
        except Exception as e:
            tabelas_status.append(("quiz_categoriaquiz (Categorias)", 0, False))
        
        try:
            count = Pergunta.objects.count()
            tabelas_status.append(("quiz_pergunta (Perguntas)", count, True))
        except Exception as e:
            tabelas_status.append(("quiz_pergunta (Perguntas)", 0, False))
        
        try:
            count = Alternativa.objects.count()
            tabelas_status.append(("quiz_alternativa (Alternativas)", count, True))
        except Exception as e:
            tabelas_status.append(("quiz_alternativa (Alternativas)", 0, False))
        
        try:
            count = PlanoPremium.objects.count()
            tabelas_status.append(("payments_plano_premium (Planos)", count, True))
        except Exception as e:
            tabelas_status.append(("payments_plano_premium (Planos)", 0, False))
        
        for nome, count, ok in tabelas_status:
            if ok:
                self.stdout.write(f"   ✅ {nome}: {count} registros")
            else:
                self.stdout.write(self.style.ERROR(f"   ❌ {nome}: ERRO"))
        
        # 3. Verificar integridade dos dados
        self.stdout.write("\n3️⃣  VERIFICANDO INTEGRIDADE...")
        
        # Usuários sem profile
        try:
            usuarios_sem_profile = User.objects.filter(profile__isnull=True).count()
            if usuarios_sem_profile == 0:
                self.stdout.write("   ✅ Todos os usuários têm profile")
            else:
                self.stdout.write(self.style.WARNING(
                    f"   ⚠️  {usuarios_sem_profile} usuário(s) sem profile"
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erro ao verificar profiles: {e}"))
        
        # Perguntas sem alternativas
        try:
            perguntas_sem_alternativas = Pergunta.objects.filter(
                alternativas__isnull=True
            ).count()
            if perguntas_sem_alternativas == 0:
                self.stdout.write("   ✅ Todas as perguntas têm alternativas")
            else:
                self.stdout.write(self.style.WARNING(
                    f"   ⚠️  {perguntas_sem_alternativas} pergunta(s) sem alternativas"
                ))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"   ⚠️  Não foi possível verificar perguntas"))
        
        # 4. Resumo final
        self.stdout.write("\n4️⃣  RESUMO:")
        total_usuarios = User.objects.count()
        total_profiles = Profile.objects.count()
        total_quiz = CategoriaQuiz.objects.count()
        
        self.stdout.write(f"   👥 Usuários cadastrados: {total_usuarios}")
        self.stdout.write(f"   📋 Profiles criados: {total_profiles}")
        self.stdout.write(f"   📝 Categorias de quiz: {total_quiz}")
        
        # Verificar configuração de pagamento
        try:
            config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            if config:
                self.stdout.write(f"   💳 Mercado Pago: {'✅ Configurado' if config.access_token and config.public_key else '⚠️  Pendente'}")
            else:
                self.stdout.write("   💳 Mercado Pago: ⚠️  Não configurado")
        except:
            self.stdout.write("   💳 Mercado Pago: ⚠️  Não configurado")
        
        self.stdout.write("\n" + "=" * 70)
        
        # Verificar se tudo está OK
        tabelas_ok = all([status[2] for status in tabelas_status])
        
        if tabelas_ok and total_usuarios >= 0:
            self.stdout.write(self.style.SUCCESS("✅ BANCO DE DADOS FUNCIONANDO PERFEITAMENTE!"))
        else:
            self.stdout.write(self.style.WARNING("⚠️  BANCO DE DADOS COM PROBLEMAS - Verifique os erros acima"))
        
        self.stdout.write("=" * 70)

