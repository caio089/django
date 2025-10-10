#!/usr/bin/env bash
# SCRIPT DE RELEASE - Executado ANTES do servidor iniciar
# Aqui SIM podemos conectar ao banco de dados
set -o errexit

echo "🔄 Executando release commands..."

cd meu_projeto

# Aplicar migrações
echo "📊 Aplicando migrations..."
python manage.py migrate --noinput

echo "✅ Migrations aplicadas!"

# Criar superuser se não existir (opcional)
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

echo "🎉 Release concluído com sucesso!"

