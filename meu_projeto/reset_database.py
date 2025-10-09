#!/usr/bin/env python
"""
Script para limpar o banco de dados PostgreSQL no Supabase
Execute APENAS se você quiser APAGAR TODOS OS DADOS!
"""

import os
import psycopg2
from urllib.parse import urlparse

def reset_database():
    """Limpa todas as tabelas do banco de dados"""
    
    # Pegar a URL do banco
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada!")
        print("Execute: export DATABASE_URL='sua-url-aqui'")
        return
    
    print("🔥 ATENÇÃO: Este script vai APAGAR TODOS OS DADOS!")
    print(f"📍 Banco: {database_url.split('@')[1].split('/')[0]}")
    print()
    
    # Parse da URL
    result = urlparse(database_url)
    
    try:
        # Conectar ao banco
        print("🔌 Conectando ao banco...")
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Desabilitar foreign keys temporariamente
        print("🔓 Desabilitando constraints...")
        cursor.execute("SET session_replication_role = 'replica';")
        
        # Buscar todas as tabelas (exceto system tables)
        print("🔍 Buscando tabelas...")
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        
        tables = cursor.fetchall()
        
        if not tables:
            print("✅ Nenhuma tabela encontrada. Banco já está limpo!")
        else:
            print(f"📋 Encontradas {len(tables)} tabelas")
            
            # Apagar cada tabela
            for table in tables:
                table_name = table[0]
                print(f"   🗑️  Apagando {table_name}...")
                cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
            
            print("✅ Todas as tabelas foram apagadas!")
        
        # Re-habilitar foreign keys
        cursor.execute("SET session_replication_role = 'origin';")
        
        cursor.close()
        conn.close()
        
        print()
        print("🎉 Banco de dados limpo com sucesso!")
        print("🚀 Agora você pode fazer deploy no Render")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 SCRIPT DE RESET DO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    resposta = input("⚠️  ISSO VAI APAGAR TODOS OS DADOS! Continuar? (sim/não): ")
    
    if resposta.lower() == 'sim':
        reset_database()
    else:
        print("❌ Operação cancelada.")

