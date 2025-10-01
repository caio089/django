#!/bin/bash

# Script para configurar Mercado Pago após deploy
echo "Configurando Mercado Pago para producao..."

# Verificar se as variaveis de ambiente estao definidas
if [ -z "$MERCADOPAGO_ACCESS_TOKEN" ]; then
    echo "ERRO: MERCADOPAGO_ACCESS_TOKEN nao definida"
    exit 1
fi

if [ -z "$MERCADOPAGO_PUBLIC_KEY" ]; then
    echo "ERRO: MERCADOPAGO_PUBLIC_KEY nao definida"
    exit 1
fi

# Executar migracoes
echo "Executando migracoes..."
python manage.py migrate

# Configurar Mercado Pago
echo "Configurando Mercado Pago..."
python manage.py configurar_mercadopago_producao

# Verificar configuracao
echo "Verificando configuracao..."
python manage.py verificar_config_producao

# Testar pagamento
echo "Testando pagamento..."
python manage.py testar_pagamento_producao

echo "Configuracao concluida!"
