"""
Comando para verificar todos os usuários e seus profiles no banco
Execute: python manage.py verificar_usuarios
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile

class Command(BaseCommand):
    help = 'Verifica todos os usuários e seus dados de profile'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("📊 VERIFICAÇÃO DE USUÁRIOS NO BANCO DE DADOS")
        self.stdout.write("=" * 60)
        
        usuarios = User.objects.all()
        
        if not usuarios.exists():
            self.stdout.write(self.style.WARNING("⚠️  Nenhum usuário encontrado no banco!"))
            return
        
        self.stdout.write(f"\n📈 Total de usuários: {usuarios.count()}\n")
        
        for user in usuarios:
            self.stdout.write("-" * 60)
            self.stdout.write(f"👤 USUÁRIO #{user.id}")
            self.stdout.write(f"   Username: {user.username}")
            self.stdout.write(f"   Email: {user.email}")
            self.stdout.write(f"   Ativo: {'✅ Sim' if user.is_active else '❌ Não'}")
            self.stdout.write(f"   Superusuário: {'✅ Sim' if user.is_superuser else '❌ Não'}")
            self.stdout.write(f"   Data de criação: {user.date_joined}")
            
            # Verificar se tem profile
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f"\n   📋 PROFILE:")
                self.stdout.write(f"      Nome: {profile.nome}")
                self.stdout.write(f"      Idade: {profile.idade}")
                self.stdout.write(f"      Faixa: {profile.faixa} ({profile.get_faixa_display()})")
                self.stdout.write(f"      Pontos XP: {profile.pontos_experiencia}")
                self.stdout.write(f"      Nível: {profile.nivel}")
                self.stdout.write(f"      Premium: {'✅ Sim' if profile.conta_premium else '❌ Não'}")
                
                if profile.conta_premium and profile.data_vencimento_premium:
                    self.stdout.write(f"      Vencimento Premium: {profile.data_vencimento_premium}")
                
            except Profile.DoesNotExist:
                self.stdout.write(self.style.ERROR("\n   ❌ PROFILE NÃO ENCONTRADO!"))
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ Verificação concluída!")
        self.stdout.write("=" * 60)

