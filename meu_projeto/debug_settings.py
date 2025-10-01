"""
Configurações de debug para produção
Execute: python manage.py check --deploy
"""
import os
from django.core.management import execute_from_command_line

def debug_deploy():
    """Verifica configurações de deploy"""
    print("🔍 Verificando configurações de deploy...")
    
    # Verificar variáveis de ambiente críticas
    critical_vars = [
        'SECRET_KEY',
        'DEBUG', 
        'ALLOWED_HOSTS',
        'DB_HOST',
        'DB_PASSWORD'
    ]
    
    missing_vars = []
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis faltando: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Todas as variáveis críticas estão configuradas")
    
    # Verificar configurações Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ SECRET_KEY configurada: {'Sim' if settings.SECRET_KEY else 'Não'}")
        
        # Verificar banco de dados
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

if __name__ == '__main__':
    debug_deploy()


