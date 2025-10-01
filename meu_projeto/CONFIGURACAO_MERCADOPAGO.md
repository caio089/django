# Configuração do Mercado Pago para Produção

## Problema
Após o deploy, o sistema retorna "Erro na configuração do pagamento" ao tentar criar pagamentos.

## Solução

### 1. Verificar Configuração Atual
```bash
python manage.py verificar_config_producao
```

### 2. Configurar Mercado Pago para Produção

#### Opção A: Usando Variáveis de Ambiente
```bash
# Definir variáveis de ambiente
export MERCADOPAGO_ACCESS_TOKEN="APP-xxxxxxxxxxxxxxxxxxxxxxxx"
export MERCADOPAGO_PUBLIC_KEY="APP_USR-xxxxxxxxxxxxxxxxxxxxxxxx"
export MERCADOPAGO_WEBHOOK_SECRET="seu_webhook_secret"
export MERCADOPAGO_WEBHOOK_URL="https://dojo-on.onrender.com/payments/webhook/"

# Executar comando
python manage.py configurar_mercadopago_producao
```

#### Opção B: Usando Argumentos
```bash
python manage.py configurar_mercadopago_producao \
  --access-token "APP-xxxxxxxxxxxxxxxxxxxxxxxx" \
  --public-key "APP_USR-xxxxxxxxxxxxxxxxxxxxxxxx" \
  --webhook-secret "seu_webhook_secret" \
  --webhook-url "https://dojo-on.onrender.com/payments/webhook/"
```

### 3. Testar Configuração
```bash
python manage.py testar_pagamento_producao
```

## Credenciais do Mercado Pago

### Sandbox (Desenvolvimento)
- Access Token: `TEST-xxxxxxxxxxxxxxxxxxxxxxxx`
- Public Key: `TEST-xxxxxxxxxxxxxxxxxxxxxxxx`

### Produção
- Access Token: `APP-xxxxxxxxxxxxxxxxxxxxxxxx`
- Public Key: `APP_USR-xxxxxxxxxxxxxxxxxxxxxxxx`

## Onde Obter as Credenciais

1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials
2. Faça login com sua conta do Mercado Pago
3. Selecione o aplicativo desejado
4. Copie as credenciais de **Produção**

## Verificação

Após configurar, verifique se:
- [ ] Configuração está ativa no banco de dados
- [ ] Access Token está válido
- [ ] Public Key está configurada
- [ ] Webhook URL está correta
- [ ] Teste de pagamento funciona

## Logs

Os logs detalhados estão disponíveis em:
- Django logs: `python manage.py runserver` (modo debug)
- Logs de produção: Verificar logs do servidor (Render, Heroku, etc.)

## Troubleshooting

### Erro: "Nenhuma configuração ativa encontrada"
- Execute o comando de configuração
- Verifique se a configuração foi salva no banco

### Erro: "Access Token não pôde ser obtido"
- Verifique se o token está correto
- Verifique se a criptografia está funcionando

### Erro: "SDK do Mercado Pago não pôde ser criado"
- Verifique se o token é válido
- Verifique se a biblioteca mercadopago está instalada
