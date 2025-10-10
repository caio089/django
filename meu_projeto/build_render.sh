#!/usr/bin/env bash
# BUILD OTIMIZADO PARA RENDER - SEM CONEXÃO COM BANCO
set -o errexit

echo "🚀 Iniciando build para Render..."

# Instalar dependências do requirements.txt
echo "📦 Instalando dependências..."
pip install -r ./meu_projeto/requirements.txt

echo "✅ Dependências instaladas!"

# Coletar arquivos estáticos (não precisa de banco)
echo "📁 Coletando arquivos estáticos..."
cd meu_projeto
python manage.py collectstatic --noinput --clear

echo "✅ Arquivos estáticos coletados!"

# NÃO executar migrações aqui - elas rodam automaticamente no startup
echo "ℹ️  Migrations serão aplicadas automaticamente no primeiro acesso"

echo ""
echo "🎉 BUILD CONCLUÍDO COM SUCESSO!"
echo "✅ Próximos passos:"
echo "   1. Servidor vai iniciar"
echo "   2. Migrations aplicadas automaticamente"
echo "   3. Sistema pronto para uso!"
echo ""
echo "🎯 DEPLOY PRONTO!"

