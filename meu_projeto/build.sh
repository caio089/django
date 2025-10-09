#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependências
pip install -r requirements.txt

# Executar migrações (--fake-initial ignora tabelas que já existem)
python manage.py migrate --fake-initial

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Executar script de configuração inicial (apenas se necessário)
python setup_render.py





