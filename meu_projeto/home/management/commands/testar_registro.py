"""
Comando para testar criação de usuário e profile
Execute: python manage.py testar_registro
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile

class Command(BaseCommand):
    help = 'Testa criação de usuário e profile'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("🧪 TESTE DE CRIAÇÃO DE USUÁRIO")
        self.stdout.write("=" * 60)
        
        # Email de teste
        email_teste = "teste_registro@example.com"
        
        # Limpar usuário de teste se existir
        try:
            user_existente = User.objects.filter(email=email_teste).first()
            if user_existente:
                self.stdout.write(f"🗑️  Removendo usuário de teste existente...")
                user_existente.delete()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️  Erro ao limpar: {e}"))
        
        # Tentar criar usuário
        self.stdout.write("\n1️⃣  Criando usuário...")
        try:
            user = User.objects.create_user(
                username=email_teste,
                email=email_teste,
                password='senha123'
            )
            self.stdout.write(self.style.SUCCESS(f"   ✅ Usuário criado! ID: {user.id}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erro ao criar usuário: {e}"))
            return
        
        # Tentar criar profile
        self.stdout.write("\n2️⃣  Criando profile...")
        try:
            profile = Profile.objects.create(
                user=user,
                nome="Usuário de Teste",
                idade=25,
                faixa='azul'
            )
            self.stdout.write(self.style.SUCCESS(f"   ✅ Profile criado! ID: {profile.id}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erro ao criar profile: {e}"))
            self.stdout.write(f"   Detalhes do erro:")
            import traceback
            self.stdout.write(traceback.format_exc())
            return
        
        # Verificar dados
        self.stdout.write("\n3️⃣  Verificando dados...")
        try:
            user_check = User.objects.get(email=email_teste)
            profile_check = Profile.objects.get(user=user_check)
            
            self.stdout.write(f"   👤 Usuário:")
            self.stdout.write(f"      Username: {user_check.username}")
            self.stdout.write(f"      Email: {user_check.email}")
            
            self.stdout.write(f"   📋 Profile:")
            self.stdout.write(f"      Nome: {profile_check.nome}")
            self.stdout.write(f"      Idade: {profile_check.idade}")
            self.stdout.write(f"      Faixa: {profile_check.faixa} ({profile_check.get_faixa_display()})")
            
            self.stdout.write(self.style.SUCCESS("\n✅ TESTE BEM-SUCEDIDO!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erro ao verificar dados: {e}"))
            return
        
        # Limpar
        self.stdout.write("\n4️⃣  Limpando dados de teste...")
        try:
            user.delete()
            self.stdout.write("   ✅ Dados removidos")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"   ⚠️  Erro ao limpar: {e}"))
        
        self.stdout.write("\n" + "=" * 60)

