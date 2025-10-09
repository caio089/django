"""
Comando para limpar usuários e profiles duplicados
Execute: python manage.py limpar_duplicados
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile

class Command(BaseCommand):
    help = 'Limpa usuários e profiles duplicados ou órfãos'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("🧹 LIMPEZA DE USUÁRIOS DUPLICADOS/ÓRFÃOS")
        self.stdout.write("=" * 60)
        
        # 1. Encontrar profiles órfãos (sem usuário)
        self.stdout.write("\n1️⃣  Verificando profiles órfãos...")
        orfaos = Profile.objects.filter(user__isnull=True)
        if orfaos.exists():
            self.stdout.write(f"   Encontrados {orfaos.count()} profiles órfãos")
            for profile in orfaos:
                self.stdout.write(f"   - Profile ID {profile.id} (sem usuário)")
            # Deletar órfãos
            orfaos.delete()
            self.stdout.write("   ✅ Profiles órfãos removidos")
        else:
            self.stdout.write("   ✅ Nenhum profile órfão encontrado")
        
        # 2. Encontrar usuários sem profile
        self.stdout.write("\n2️⃣  Verificando usuários sem profile...")
        usuarios_sem_profile = User.objects.filter(profile__isnull=True)
        if usuarios_sem_profile.exists():
            self.stdout.write(f"   Encontrados {usuarios_sem_profile.count()} usuários sem profile")
            for user in usuarios_sem_profile:
                self.stdout.write(f"   - Usuário ID {user.id} ({user.email})")
                # Criar profile padrão
                Profile.objects.create(
                    user=user,
                    nome=user.username,
                    idade=18,
                    faixa='branca'
                )
                self.stdout.write(f"     ✅ Profile criado para {user.email}")
            self.stdout.write("   ✅ Profiles criados para todos os usuários")
        else:
            self.stdout.write("   ✅ Todos os usuários têm profile")
        
        # 3. Verificar duplicatas de email
        self.stdout.write("\n3️⃣  Verificando emails duplicados...")
        from django.db.models import Count
        emails_duplicados = User.objects.values('email').annotate(
            count=Count('email')
        ).filter(count__gt=1)
        
        if emails_duplicados.exists():
            self.stdout.write("   ⚠️  Emails duplicados encontrados:")
            for item in emails_duplicados:
                email = item['email']
                count = item['count']
                self.stdout.write(f"   - {email}: {count} usuários")
                # Manter apenas o mais antigo
                usuarios = User.objects.filter(email=email).order_by('date_joined')
                manter = usuarios.first()
                deletar = usuarios.exclude(id=manter.id)
                self.stdout.write(f"     ✅ Mantendo: {manter.email} (ID {manter.id})")
                for user in deletar:
                    self.stdout.write(f"     🗑️  Removendo: {user.email} (ID {user.id})")
                    user.delete()
        else:
            self.stdout.write("   ✅ Nenhum email duplicado encontrado")
        
        # 4. Resumo final
        self.stdout.write("\n4️⃣  Resumo final:")
        total_usuarios = User.objects.count()
        total_profiles = Profile.objects.count()
        self.stdout.write(f"   👥 Usuários: {total_usuarios}")
        self.stdout.write(f"   📋 Profiles: {total_profiles}")
        
        if total_usuarios == total_profiles:
            self.stdout.write("   ✅ Sincronização perfeita!")
        else:
            self.stdout.write("   ⚠️  Ainda há diferença entre usuários e profiles")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ LIMPEZA CONCLUÍDA!")
        self.stdout.write("=" * 60)
