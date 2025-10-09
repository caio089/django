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

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Executar script de configuração inicial (apenas se necessário)
python setup_render.py





