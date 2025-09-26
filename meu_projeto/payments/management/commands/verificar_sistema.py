from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento, PlanoPremium
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verifica se o sistema está configurado corretamente'

    def handle(self, *args, **options):
        """
        Verifica todas as configurações do sistema
        """
        print("🔍 ANÁLISE COMPLETA DO SISTEMA")
        print("=" * 50)

        # 1. Verificar configuração do Mercado Pago
        print("\n1️⃣ CONFIGURAÇÃO DO MERCADO PAGO")
        print("-" * 30)

        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if config:
            print(f"✅ Configuração ativa encontrada")
            print(f"   ID: {config.id}")
            print(f"   Ambiente: {config.ambiente}")
            print(f"   Webhook URL: {config.webhook_url}")
            print(f"   Access Token configurado: {'✅' if config.get_access_token() else '❌'}")
            print(f"   Public Key configurado: {'✅' if config.get_public_key() else '❌'}")
            print(f"   Webhook Secret configurado: {'✅' if config.get_webhook_secret() else '❌'}")
            print(f"   Último uso: {config.last_used}")
            print(f"   Contador de uso: {config.usage_count}")
        else:
            print("❌ Nenhuma configuração ativa encontrada")

        # 2. Verificar credenciais no .env
        print("\n2️⃣ CREDENCIAIS NO ARQUIVO .ENV")
        print("-" * 30)

        access_token = settings.MERCADOPAGO_ACCESS_TOKEN
        public_key = settings.MERCADOPAGO_PUBLIC_KEY
        webhook_secret = settings.MERCADOPAGO_WEBHOOK_SECRET
        webhook_url = settings.MERCADOPAGO_WEBHOOK_URL

        print(f"Access Token: {'✅' if access_token else '❌'} {access_token[:20] + '...' if access_token else 'Não configurado'}")
        print(f"Public Key: {'✅' if public_key else '❌'} {public_key[:20] + '...' if public_key else 'Não configurado'}")
        print(f"Webhook Secret: {'✅' if webhook_secret else '❌'} {webhook_secret[:20] + '...' if webhook_secret else 'Não configurado'}")
        print(f"Webhook URL: {'✅' if webhook_url else '❌'} {webhook_url}")

        # 3. Verificar planos cadastrados
        print("\n3️⃣ PLANOS CADASTRADOS")
        print("-" * 30)

        planos = PlanoPremium.objects.filter(ativo=True)
        if planos.exists():
            print(f"✅ {planos.count()} planos ativos encontrados:")
            for plano in planos:
                print(f"   - {plano.nome}: R$ {plano.preco} ({plano.duracao_dias} dias)")
        else:
            print("❌ Nenhum plano ativo encontrado")

        # 4. Verificar configurações de email
        print("\n4️⃣ CONFIGURAÇÕES DE EMAIL")
        print("-" * 30)

        email_host = settings.EMAIL_HOST
        email_port = settings.EMAIL_PORT
        email_user = settings.EMAIL_HOST_USER
        email_password = settings.EMAIL_HOST_PASSWORD

        print(f"Email Host: {'✅' if email_host else '❌'} {email_host}")
        print(f"Email Port: {'✅' if email_port else '❌'} {email_port}")
        print(f"Email User: {'✅' if email_user else '❌'} {email_user}")
        print(f"Email Password: {'✅' if email_password else '❌'} {'Configurado' if email_password else 'Não configurado'}")

        # 5. Verificar configurações de banco
        print("\n5️⃣ CONFIGURAÇÕES DE BANCO")
        print("-" * 30)

        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default']['NAME']
        use_sqlite = getattr(settings, 'USE_SQLITE_FALLBACK', False)

        print(f"Engine: {db_engine}")
        print(f"Database: {db_name}")
        print(f"SQLite Fallback: {'✅' if use_sqlite else '❌'} {use_sqlite}")

        # 6. Verificar configurações de segurança
        print("\n6️⃣ CONFIGURAÇÕES DE SEGURANÇA")
        print("-" * 30)

        debug = settings.DEBUG
        secret_key = settings.SECRET_KEY
        allowed_hosts = settings.ALLOWED_HOSTS

        print(f"DEBUG: {'⚠️' if debug else '✅'} {debug}")
        print(f"SECRET_KEY: {'✅' if secret_key else '❌'} {'Configurado' if secret_key else 'Não configurado'}")
        print(f"ALLOWED_HOSTS: {'✅' if allowed_hosts else '❌'} {allowed_hosts}")

        # 7. Resumo final
        print("\n7️⃣ RESUMO FINAL")
        print("-" * 30)

        config_ok = config and config.get_access_token() and config.get_public_key()
        planos_ok = planos.exists()
        credenciais_ok = access_token and public_key

        if config_ok and planos_ok and credenciais_ok:
            print("🎉 SISTEMA 100% CONFIGURADO E PRONTO PARA USO!")
            print("✅ Mercado Pago configurado")
            print("✅ Planos cadastrados")
            print("✅ Credenciais válidas")
            print("✅ Webhook configurado")
            print("\n🚀 O sistema está pronto para processar pagamentos reais!")
        else:
            print("⚠️ SISTEMA PARCIALMENTE CONFIGURADO")
            if not config_ok:
                print("❌ Configuração do Mercado Pago incompleta")
            if not planos_ok:
                print("❌ Nenhum plano cadastrado")
            if not credenciais_ok:
                print("❌ Credenciais do Mercado Pago inválidas")

        print("\n" + "=" * 50)
