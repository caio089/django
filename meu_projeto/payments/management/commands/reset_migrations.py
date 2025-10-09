"""
Comando para resetar o estado das migrations no banco
Execute: python manage.py reset_migrations
"""

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reseta o estado das migrations (marca todas como aplicadas sem recriar tabelas)'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Resetando estado das migrations...")
        
        try:
            with connection.cursor() as cursor:
                # Limpar a tabela de migrations
                self.stdout.write("🗑️  Limpando tabela django_migrations...")
                cursor.execute("TRUNCATE TABLE django_migrations;")
                
            self.stdout.write(self.style.SUCCESS("✅ Tabela django_migrations limpa!"))
            self.stdout.write("")
            self.stdout.write("🚀 Agora execute:")
            self.stdout.write("   python manage.py migrate --fake")
            self.stdout.write("")
            self.stdout.write("Isso vai marcar todas as migrations como aplicadas sem recriar as tabelas.")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro: {e}"))

