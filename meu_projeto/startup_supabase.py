"""
Script de inicialização para manter Supabase ativo no Render
"""
import os
import time
import threading
import logging

logger = logging.getLogger(__name__)

def start_supabase_keepalive_background():
    """Inicia keep-alive em background"""
    try:
        from meu_projeto.supabase_keepalive import start_supabase_keepalive
        start_supabase_keepalive()
        logger.info("🚀 Keep-alive do Supabase iniciado em background")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar keep-alive: {e}")

def main():
    """Função principal de inicialização"""
    # Verificar se está em produção
    if os.getenv('RENDER'):
        logger.info("🌐 Ambiente de produção detectado - iniciando keep-alive")
        
        # Iniciar keep-alive em thread separada
        keepalive_thread = threading.Thread(
            target=start_supabase_keepalive_background,
            daemon=True
        )
        keepalive_thread.start()
        
        # Aguardar um pouco para garantir que o keep-alive foi iniciado
        time.sleep(2)
        
        logger.info("✅ Sistema anti-hibernação ativado")
    else:
        logger.info("💻 Ambiente de desenvolvimento - keep-alive opcional")

if __name__ == '__main__':
    main()
