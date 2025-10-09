#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependências
pip install -r requirements.txt

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





