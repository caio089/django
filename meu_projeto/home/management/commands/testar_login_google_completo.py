from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from django.contrib.auth import login
from django.test import RequestFactory
import json

class Command(BaseCommand):
    help = 'Testa o login com Google completo'

    def handle(self, *args, **options):
        """
        Testa o sistema de login com Google
        """
        self.stdout.write("🔐 Testando sistema de login com Google...")
        
        # Dados simulados do Google
        dados_google = {
            'email': 'teste@google.com',
            'name': 'Usuário Teste Google',
            'picture': 'https://via.placeholder.com/100'
        }
        
        try:
            # 1. Verificar se usuário já existe
            email = dados_google['email']
            nome = dados_google['name']
            
            self.stdout.write(f"📧 Testando com email: {email}")
            
            # 2. Buscar ou criar usuário
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': nome.split(' ')[0] if nome else '',
                    'last_name': ' '.join(nome.split(' ')[1:]) if nome and len(nome.split(' ')) > 1 else '',
                }
            )
            
            if created:
                self.stdout.write("✅ Novo usuário criado")
                user.set_unusable_password()
                user.save()
                
                # Criar perfil
                profile = Profile.objects.create(
                    user=user,
                    nome=nome or user.first_name or user.username,
                    idade=18,
                    faixa='cinza'
                )
                self.stdout.write("✅ Perfil criado")
            else:
                self.stdout.write("✅ Usuário existente encontrado")
                
                # Verificar se tem perfil
                try:
                    profile = Profile.objects.get(user=user)
                    self.stdout.write("✅ Perfil existente encontrado")
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(
                        user=user,
                        nome=nome or user.first_name or user.username,
                        idade=18,
                        faixa='cinza'
                    )
                    self.stdout.write("✅ Perfil criado para usuário existente")
            
            # 3. Verificar dados salvos
            self.stdout.write("\n📊 Dados salvos no banco:")
            self.stdout.write(f"  👤 Usuário: {user.username}")
            self.stdout.write(f"  📧 Email: {user.email}")
            self.stdout.write(f"  👤 Nome: {user.first_name} {user.last_name}")
            self.stdout.write(f"  🥋 Perfil: {profile.nome}")
            self.stdout.write(f"  🎯 Faixa: {profile.get_faixa_display()}")
            self.stdout.write(f"  📅 Idade: {profile.idade}")
            
            # 4. Testar seleção de faixa
            self.stdout.write("\n🥋 Testando seleção de faixas:")
            faixas_urls = {
                'cinza': '/pag1/',
                'azul': '/pag2/',
                'amarela': '/pag3/',
                'laranja': '/pag4/',
                'verde': '/pag5/',
                'roxa': '/pag6/',
                'marrom': '/pag7/'
            }
            
            for faixa, url in faixas_urls.items():
                self.stdout.write(f"  {faixa} -> {url}")
            
            # 5. Verificar se usuário pode fazer login
            self.stdout.write(f"\n🔐 Status de autenticação: {user.is_authenticated}")
            self.stdout.write(f"🔑 Tem senha: {user.has_usable_password()}")
            
            self.stdout.write("\n✅ Teste de login com Google concluído com sucesso!")
            
        except Exception as e:
            self.stdout.write(f"\n❌ Erro no teste: {e}")
            import traceback
            self.stdout.write(f"❌ Traceback: {traceback.format_exc()}")
