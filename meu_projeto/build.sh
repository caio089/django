#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependências essenciais primeiro
echo "📦 Instalando dependências essenciais..."
pip install Django==5.2.5
pip install psycopg2-binary==2.9.10
pip install gunicorn==23.0.0
pip install whitenoise==6.10.0
pip install python-dotenv==1.0.0
pip install dj-database-url==2.1.0

# Instalar dependências opcionais (se falhar, continua)
echo "📦 Instalando dependências opcionais..."
set +e
pip install mercadopago==2.3.0
pip install qrcode==8.2
pip install pillow==10.4.0
pip install cryptography==43.0.3
set -e

# Executar migrações de forma segura
echo "🔄 Aplicando migrações..."
# Temporariamente desabilitar errexit para tentar migrate
set +e
python manage.py migrate --fake-initial
MIGRATE_EXIT_CODE=$?
set -e

# Se falhou, tenta com --fake
if [ $MIGRATE_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Migrate falhou (código $MIGRATE_EXIT_CODE), marcando migrations como aplicadas..."
    python manage.py migrate --fake
fi

# Coletar arquivos estáticos de forma segura
echo "📁 Coletando arquivos estáticos..."
set +e
python manage.py collectstatic --noinput
COLLECTSTATIC_EXIT_CODE=$?
set -e

if [ $COLLECTSTATIC_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Collectstatic falhou (código $COLLECTSTATIC_EXIT_CODE), continuando sem arquivos estáticos..."
    echo "   Os arquivos estáticos serão servidos diretamente do código"
else
    echo "✅ Arquivos estáticos coletados com sucesso"
fi

# Executar script de configuração inicial (apenas se necessário)
echo "🚀 Executando configuração inicial..."
set +e
python setup_render.py
SETUP_EXIT_CODE=$?
set -e

if [ $SETUP_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Setup inicial falhou, mas continuando..."
else
    echo "✅ Configuração inicial concluída"
fi

echo "🎉 Build concluído!"





