from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile

class Command(BaseCommand):
    help = 'Corrige nomes de perfil que estão como "Teste Usuario"'

    def handle(self, *args, **options):
        # Buscar todos os perfis com nome "Teste Usuario"
        perfis_problema = Profile.objects.filter(nome='Teste Usuario')
        
        self.stdout.write(f'Encontrados {perfis_problema.count()} perfis com nome "Teste Usuario"')
        
        for perfil in perfis_problema:
            user = perfil.user
            nome_anterior = perfil.nome
            
            # Definir novo nome baseado no usuário
            if user.get_full_name():
                novo_nome = user.get_full_name()
            else:
                # Se não tem nome completo, usar email sem o domínio
                email_parts = user.email.split('@')
                if len(email_parts) > 0:
                    novo_nome = email_parts[0].replace('.', ' ').title()
                else:
                    novo_nome = user.username
            
            perfil.nome = novo_nome
            perfil.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Perfil do usuário {user.email} atualizado: "{nome_anterior}" → "{novo_nome}"'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'SUCCESS: {perfis_problema.count()} perfis corrigidos com sucesso!')
        )
