@echo off
REM Script para configurar Mercado Pago após deploy no Windows

echo Configurando Mercado Pago para producao...

REM Verificar se as variaveis de ambiente estao definidas
if "%MERCADOPAGO_ACCESS_TOKEN%"=="" (
    echo ERRO: MERCADOPAGO_ACCESS_TOKEN nao definida
    exit /b 1
)

if "%MERCADOPAGO_PUBLIC_KEY%"=="" (
    echo ERRO: MERCADOPAGO_PUBLIC_KEY nao definida
    exit /b 1
)

REM Executar migracoes
echo Executando migracoes...
python manage.py migrate

REM Configurar Mercado Pago
echo Configurando Mercado Pago...
python manage.py configurar_mercadopago_producao

REM Verificar configuracao
echo Verificando configuracao...
python manage.py verificar_config_producao

REM Testar pagamento
echo Testando pagamento...
python manage.py testar_pagamento_producao

echo Configuracao concluida!
pause
