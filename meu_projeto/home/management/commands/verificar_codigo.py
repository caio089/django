"""
Comando para verificação completa do código
Execute: python manage.py verificar_codigo
"""

from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verifica código, configurações e potenciais problemas'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("VERIFICAÇÃO COMPLETA DO CÓDIGO")
        self.stdout.write("=" * 70)
        
        # 1. Django System Check
        self.stdout.write("\n1. Django System Check...")
        try:
            management.call_command('check', '--verbosity=0')
            self.stdout.write(self.style.SUCCESS("   OK - Sem erros de sistema"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ERRO: {e}"))
        
        # 2. Verificar Settings
        self.stdout.write("\n2. Verificando Settings...")
        checks = [
            ('SECRET_KEY definida', hasattr(settings, 'SECRET_KEY') and len(settings.SECRET_KEY) > 20),
            ('DEBUG configurado', hasattr(settings, 'DEBUG')),
            ('ALLOWED_HOSTS configurado', hasattr(settings, 'ALLOWED_HOSTS') and len(settings.ALLOWED_HOSTS) > 0),
            ('DATABASE configurado', hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES),
            ('STATIC_ROOT definido', hasattr(settings, 'STATIC_ROOT')),
            ('STATIC_URL definido', hasattr(settings, 'STATIC_URL')),
        ]
        
        for nome, status in checks:
            if status:
                self.stdout.write(f"   OK {nome}")
            else:
                self.stdout.write(self.style.WARNING(f"   AVISO {nome}"))
        
        # 3. Verificar Apps instalados
        self.stdout.write("\n3. Apps Instalados...")
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'core',
            'home',
            'payments',
            'quiz',
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                self.stdout.write(f"   OK {app}")
            else:
                self.stdout.write(self.style.ERROR(f"   FALTANDO {app}"))
        
        # 4. Verificar Middleware
        self.stdout.write("\n4. Middleware...")
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ]
        
        for mw in required_middleware:
            if mw in settings.MIDDLEWARE:
                self.stdout.write(f"   OK {mw.split('.')[-1]}")
            else:
                self.stdout.write(self.style.WARNING(f"   FALTANDO {mw}"))
        
        # 5. Verificar configurações de segurança (produção)
        self.stdout.write("\n5. Configurações de Segurança...")
        if not settings.DEBUG:
            security_checks = [
                ('SECURE_SSL_REDIRECT', getattr(settings, 'SECURE_SSL_REDIRECT', False)),
                ('SECURE_HSTS_SECONDS', getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0),
                ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', False)),
                ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', False)),
            ]
            
            for nome, valor in security_checks:
                if valor:
                    self.stdout.write(f"   OK {nome}")
                else:
                    self.stdout.write(self.style.WARNING(f"   DESATIVADO {nome}"))
        else:
            self.stdout.write("   DESENVOLVIMENTO - Verificações de segurança puladas")
        
        # 6. Verificar arquivos críticos
        self.stdout.write("\n6. Arquivos Críticos...")
        critical_files = [
            'manage.py',
            'requirements.txt',
            'build.sh',
            'meu_projeto/settings.py',
            'meu_projeto/urls.py',
            'meu_projeto/wsgi.py',
        ]
        
        for arquivo in critical_files:
            caminho = os.path.join(settings.BASE_DIR, arquivo)
            if os.path.exists(caminho):
                self.stdout.write(f"   OK {arquivo}")
            else:
                self.stdout.write(self.style.ERROR(f"   FALTANDO {arquivo}"))
        
        # 7. Resumo final
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("VERIFICAÇÃO CONCLUÍDA"))
        self.stdout.write("=" * 70)
        
        if settings.DEBUG:
            self.stdout.write("\nMODO: Desenvolvimento (DEBUG=True)")
        else:
            self.stdout.write("\nMODO: Produção (DEBUG=False)")
        
        self.stdout.write(f"BANCO DE DADOS: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")

