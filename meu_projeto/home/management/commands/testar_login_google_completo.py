from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from django.test import Client
from django.urls import reverse
import json

class Command(BaseCommand):
    help = 'Testa o sistema completo de login com Google'

    def handle(self, *args, **options):
        """
        Testa o sistema completo de login com Google
        """
        self.stdout.write("🔐 Testando sistema completo de login com Google...")
        
        # 1. Testar view principal
        self.stdout.write("\n1️⃣ Testando view principal...")
        try:
            client = Client()
            
            # Dados de teste
            dados_teste = {
                'email': 'teste@google.com',
                'name': 'Usuário Teste Google',
                'picture': 'https://via.placeholder.com/100'
            }
            
            # Testar processar_login_google
            response = client.post(
                reverse('processar_login_google'),
                data=json.dumps(dados_teste),
                content_type='application/json'
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.stdout.write("✅ View principal funcionando")
                else:
                    self.stdout.write(f"❌ View principal com erro: {data.get('error')}")
            else:
                self.stdout.write(f"❌ View principal retornou status {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro na view principal: {e}")
        
        # 2. Testar view de fallback
        self.stdout.write("\n2️⃣ Testando view de fallback...")
        try:
            client = Client()
            
            # Testar login_google_fallback
            response = client.post(reverse('login_google_fallback'))
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.stdout.write("✅ View de fallback funcionando")
                else:
                    self.stdout.write(f"❌ View de fallback com erro: {data.get('error')}")
            else:
                self.stdout.write(f"❌ View de fallback retornou status {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro na view de fallback: {e}")
        
        # 3. Testar URLs
        self.stdout.write("\n3️⃣ Testando URLs...")
        try:
            client = Client()
            
            # Testar login_google_view
            response = client.get(reverse('login_google'))
            if response.status_code == 200:
                self.stdout.write("✅ URL login_google funcionando")
            else:
                self.stdout.write(f"❌ URL login_google retornou status {response.status_code}")
            
            # Testar selecionar_faixa
            response = client.get(reverse('selecionar_faixa'))
            if response.status_code == 302:  # Redirecionamento para login
                self.stdout.write("✅ URL selecionar_faixa funcionando (redireciona corretamente)")
            else:
                self.stdout.write(f"❌ URL selecionar_faixa retornou status {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro nas URLs: {e}")
        
        # 4. Testar banco de dados
        self.stdout.write("\n4️⃣ Testando banco de dados...")
        try:
            # Contar usuários
            total_usuarios = User.objects.count()
            self.stdout.write(f"👥 Total de usuários: {total_usuarios}")
            
            # Contar perfis
            total_perfis = Profile.objects.count()
            self.stdout.write(f"👤 Total de perfis: {total_perfis}")
            
            # Verificar se há usuários de teste
            usuarios_teste = User.objects.filter(email__contains='google.com')
            self.stdout.write(f"🔍 Usuários Google: {usuarios_teste.count()}")
            
            for user in usuarios_teste[:3]:
                try:
                    profile = user.profile
                    self.stdout.write(f"  👤 {user.username} - {profile.nome} ({profile.get_faixa_display()})")
                except:
                    self.stdout.write(f"  👤 {user.username} - Sem perfil")
            
            self.stdout.write("✅ Banco de dados funcionando")
            
        except Exception as e:
            self.stdout.write(f"❌ Erro no banco de dados: {e}")
        
        # 5. Testar templates
        self.stdout.write("\n5️⃣ Testando templates...")
        try:
            client = Client()
            
            # Testar se o template carrega
            response = client.get(reverse('login_google'))
            if 'Continuar com Google' in response.content.decode():
                self.stdout.write("✅ Template login_google carregando corretamente")
            else:
                self.stdout.write("❌ Template login_google com problemas")
            
            # Testar se o CSRF token está presente
            if 'csrfmiddlewaretoken' in response.content.decode():
                self.stdout.write("✅ CSRF token presente no template")
            else:
                self.stdout.write("❌ CSRF token não encontrado no template")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro nos templates: {e}")
        
        self.stdout.write("\n🎯 Teste completo finalizado!")
        self.stdout.write("📋 Verifique os resultados acima para identificar problemas.")