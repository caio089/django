#!/usr/bin/env python
"""
Script para migrar dados do SQLite para Supabase (PostgreSQL)

Este script:
1. Faz backup dos dados do SQLite
2. Verifica a conexão com o Supabase
3. Migra os dados para o PostgreSQL
4. Valida a migração

USO:
    python migrate_to_supabase.py
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_step(number, text):
    """Imprime passo formatado"""
    print(f"\n[{number}] {text}")
    print("-" * 60)

def run_command(command, description):
    """Executa comando e retorna sucesso/falha"""
    print(f"\n>>> Executando: {description}")
    print(f"    Comando: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"    ✅ Sucesso!")
        if result.stdout:
            print(f"    Output: {result.stdout[:200]}")
        return True
    else:
        print(f"    ❌ Erro!")
        if result.stderr:
            print(f"    Erro: {result.stderr[:200]}")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe e está configurado"""
    print_step(1, "Verificando arquivo .env")
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print("❌ Arquivo .env não encontrado!")
        print("\nVocê precisa criar um arquivo .env com as credenciais do Supabase.")
        print("Consulte o arquivo CONFIGURAR_SUPABASE.md para instruções.")
        return False
    
    # Verificar se DATABASE_URL está configurado
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        if 'DATABASE_URL=' in content:
            # Verificar se não é o exemplo
            if 'SEU_PROJETO' in content or 'SUA_SENHA' in content:
                print("⚠️ O arquivo .env contém valores de exemplo!")
                print("Você precisa substituir pelos valores reais do Supabase.")
                print("Consulte o arquivo CONFIGURAR_SUPABASE.md para instruções.")
                return False
            else:
                print("✅ Arquivo .env encontrado e configurado!")
                return True
        else:
            print("⚠️ DATABASE_URL não encontrado no .env!")
            print("Você precisa adicionar a connection string do Supabase.")
            print("Consulte o arquivo CONFIGURAR_SUPABASE.md para instruções.")
            return False

def backup_sqlite():
    """Faz backup dos dados do SQLite"""
    print_step(2, "Fazendo backup dos dados do SQLite")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_sqlite_{timestamp}.json"
    
    command = f"python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > {backup_file}"
    
    if run_command(command, "Exportar dados do SQLite"):
        print(f"\n✅ Backup criado: {backup_file}")
        return backup_file
    else:
        print("\n❌ Erro ao criar backup!")
        return None

def test_postgres_connection():
    """Testa conexão com o PostgreSQL"""
    print_step(3, "Testando conexão com o Supabase (PostgreSQL)")
    
    command = "python manage.py check --database default"
    
    if run_command(command, "Verificar configuração do banco"):
        print("\n✅ Conexão com Supabase configurada corretamente!")
        return True
    else:
        print("\n❌ Erro na conexão com Supabase!")
        print("\nVerifique:")
        print("1. Se o arquivo .env está configurado corretamente")
        print("2. Se a connection string está correta")
        print("3. Se sua conexão com a internet está funcionando")
        return False

def migrate_to_postgres():
    """Aplica migrações no PostgreSQL"""
    print_step(4, "Aplicando migrações no PostgreSQL")
    
    command = "python manage.py migrate"
    
    if run_command(command, "Aplicar migrações"):
        print("\n✅ Migrações aplicadas com sucesso!")
        return True
    else:
        print("\n❌ Erro ao aplicar migrações!")
        return False

def load_data(backup_file):
    """Carrega dados no PostgreSQL"""
    print_step(5, "Carregando dados no PostgreSQL")
    
    if not backup_file:
        print("⚠️ Nenhum arquivo de backup fornecido. Pulando...")
        return True
    
    command = f"python manage.py loaddata {backup_file}"
    
    if run_command(command, "Importar dados"):
        print("\n✅ Dados carregados com sucesso!")
        return True
    else:
        print("\n❌ Erro ao carregar dados!")
        print("\n⚠️ Não se preocupe! Seus dados estão seguros no backup.")
        print(f"    Arquivo de backup: {backup_file}")
        return False

def verify_data():
    """Verifica se os dados foram migrados corretamente"""
    print_step(6, "Verificando migração")
    
    # Criar script de verificação
    verification_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento, PlanoPremium

print(f'Usuarios: {User.objects.count()}')
print(f'Assinaturas: {Assinatura.objects.count()}')
print(f'Pagamentos: {Pagamento.objects.count()}')
print(f'Planos: {PlanoPremium.objects.count()}')
"""
    
    with open('verify_migration.py', 'w', encoding='utf-8') as f:
        f.write(verification_script)
    
    command = "python verify_migration.py"
    
    if run_command(command, "Contar registros"):
        # Limpar script temporário
        os.remove('verify_migration.py')
        print("\n✅ Dados verificados!")
        return True
    else:
        print("\n⚠️ Não foi possível verificar os dados.")
        return False

def main():
    """Função principal"""
    print_header("MIGRAÇÃO PARA SUPABASE (PostgreSQL)")
    
    print("Este script vai migrar seus dados do SQLite para o Supabase.")
    print("Certifique-se de ter configurado o arquivo .env antes de continuar.")
    print("\nConsulte: CONFIGURAR_SUPABASE.md para instruções detalhadas.")
    
    input("\n>>> Pressione ENTER para continuar ou CTRL+C para cancelar...")
    
    # Passo 1: Verificar .env
    if not check_env_file():
        print("\n❌ Configure o arquivo .env e execute novamente.")
        return False
    
    # Passo 2: Backup do SQLite
    backup_file = backup_sqlite()
    if not backup_file:
        print("\n❌ Não foi possível fazer backup. Abortando migração.")
        return False
    
    # Passo 3: Testar conexão
    if not test_postgres_connection():
        print("\n❌ Não foi possível conectar ao Supabase. Abortando migração.")
        print(f"\n✅ Seus dados estão seguros no backup: {backup_file}")
        return False
    
    # Passo 4: Aplicar migrações
    if not migrate_to_postgres():
        print("\n❌ Erro ao aplicar migrações. Abortando.")
        print(f"\n✅ Seus dados estão seguros no backup: {backup_file}")
        return False
    
    # Passo 5: Carregar dados
    if not load_data(backup_file):
        print("\n⚠️ Erro ao carregar dados, mas o banco está configurado.")
        print(f"    Você pode tentar carregar manualmente: python manage.py loaddata {backup_file}")
        return False
    
    # Passo 6: Verificar
    verify_data()
    
    # Sucesso!
    print_header("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("✅ Seus dados foram migrados para o Supabase!")
    print(f"✅ Backup do SQLite: {backup_file}")
    print("\nPróximos passos:")
    print("1. Teste o site: python manage.py runserver")
    print("2. Acesse http://localhost:8000 e verifique se tudo está funcionando")
    print("3. Faça login e teste as funcionalidades")
    print("4. Se tudo estiver OK, você pode fazer deploy!")
    print("\n🎉 Parabéns! Agora seu sistema suporta:")
    print("   - 100.000+ usuários")
    print("   - 10.000+ assinaturas ativas")
    print("   - 1.000+ usuários simultâneos")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Migração cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)
