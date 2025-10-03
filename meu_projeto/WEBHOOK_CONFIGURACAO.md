# Configuração do Webhook Mercado Pago

## ✅ STATUS DO SISTEMA

### SDK Mercado Pago
- ✅ **Configurado:** SDK funcionando corretamente
- ✅ **Ambiente:** PRODUCAO (credenciais reais)
- ✅ **Access Token:** APP_USR-551979324356...
- ✅ **Public Key:** APP_USR-0d73e94d-eab...

### Webhook
- ✅ **URL Configurada:** https://dojo-on.onrender.com/payments/webhook/
- ✅ **Ambiente:** Produção (Render)
- ⚠️ **Webhooks Recebidos:** 0 (ainda não recebeu webhooks)

### Sistema de Pagamento
- ✅ **Função de Ativação:** ativar_assinatura() funcionando
- ✅ **Detecção Automática:** A cada 2 segundos por até 5 minutos
- ✅ **Processamento:** Webhook processa pagamentos e preferências

## 🔧 CONFIGURAR WEBHOOK NO MERCADO PAGO

### Passo 1: Acessar o Painel do Mercado Pago
1. Acesse: https://www.mercadopago.com.br/developers/panel
2. Faça login com sua conta
3. Selecione sua aplicação

### Passo 2: Configurar Notificações
1. No menu lateral, clique em **"Notificações"** ou **"Webhooks"**
2. Clique em **"Configurar notificações"**
3. Preencha os campos:

#### URL do Webhook:
```
https://dojo-on.onrender.com/payments/webhook/
```

#### Eventos para Notificar:
Marque as seguintes opções:
- ✅ `payment` (Pagamento)
  - payment.created
  - payment.updated
- ✅ Modo de produção

### Passo 3: Testar Webhook
1. No painel do Mercado Pago, use a opção **"Testar webhook"**
2. Envie uma notificação de teste
3. Verifique se retorna **200 OK**

## 🔍 COMO O SISTEMA FUNCIONA

### Fluxo de Pagamento PIX:

1. **Usuário escolhe PIX**
   - Sistema cria pagamento no banco de dados
   - Gera QR Code via API do Mercado Pago
   - Exibe QR Code na tela

2. **Usuário faz o PIX**
   - Pagamento chega na conta do Mercado Pago
   - Mercado Pago envia webhook para: `https://dojo-on.onrender.com/payments/webhook/`

3. **Sistema Recebe Webhook**
   - Webhook é processado automaticamente
   - Sistema busca o pagamento no Mercado Pago
   - Verifica se status é "approved"
   - Atualiza status no banco de dados

4. **Ativação Automática**
   - Função `ativar_assinatura()` é chamada
   - Cria registro de assinatura no banco
   - Define data de vencimento
   - Status: "ativa"

5. **Detecção pelo Frontend**
   - JavaScript verifica status a cada 2 segundos
   - Quando detecta `status=approved` e `assinatura_ativa=true`:
     - Para verificação
     - Redireciona para página de bem-vindo
     - Após 5 segundos, redireciona para dashboard

6. **Usuário no Dashboard**
   - Acesso premium liberado
   - Todos os recursos desbloqueados

## 🧪 TESTAR O SISTEMA

### Teste Local (desenvolvimento):
```bash
# Simular webhook
curl -X POST http://localhost:8000/payments/webhook/ \
  -H "Content-Type: application/json" \
  -d '{"type":"payment","data":{"id":"123456"}}'
```

### Teste em Produção:
1. Faça um pagamento PIX real (valor mínimo: R$ 1,00)
2. Monitore os logs do Render
3. Verifique se webhook foi recebido
4. Confirme se assinatura foi ativada

### Verificar Logs no Render:
1. Acesse: https://dashboard.render.com/
2. Selecione seu projeto
3. Clique em **"Logs"**
4. Procure por:
   - `Webhook recebido`
   - `Processando webhook de pagamento`
   - `Assinatura ativada`

## 🔐 SEGURANÇA

### O Sistema Verifica:
- ✅ Pagamento é real (consulta API do Mercado Pago)
- ✅ Status é "approved"
- ✅ Não cria assinatura duplicada
- ✅ Botão "Já Paguei" só funciona se pagamento for real

### Não é Possível:
- ❌ Ativar plano sem pagar
- ❌ Duplicar assinatura
- ❌ Burlar verificação com botão "Já Paguei"

## 📊 MONITORAMENTO

### Comandos Úteis:
```bash
# Verificar ambiente
python manage.py verificar_ambiente

# Testar webhook
python manage.py testar_webhook

# Ativar assinaturas pendentes (caso webhook falhe)
python manage.py ativar_assinaturas_pendentes

# Ver logs
tail -f logs/mercadopago.log
```

### Verificar no Admin Django:
1. Acesse: `/admin/`
2. Confira:
   - **Pagamentos:** Status dos pagamentos
   - **Assinaturas:** Assinaturas ativas
   - **WebhookEvents:** Webhooks recebidos

## ⚠️ PROBLEMAS COMUNS

### Webhook não está sendo recebido:
1. Verifique se URL está correta no painel do Mercado Pago
2. Confirme que aplicação está rodando no Render
3. Teste a URL manualmente

### Pagamento não ativa assinatura:
1. Execute: `python manage.py ativar_assinaturas_pendentes`
2. Verifique logs para ver o erro
3. Confirme que webhook foi processado

### QR Code inválido:
1. Confirme que está usando credenciais de PRODUCAO
2. Verifique se access token começa com `APP_USR-`
3. Teste no ambiente de sandbox primeiro

## ✅ CHECKLIST FINAL

Antes de fazer deploy:
- [x] Credenciais de produção configuradas
- [x] Webhook URL configurada no Mercado Pago
- [x] Sistema de detecção automática funcionando
- [x] Função de ativação testada
- [x] Página de bem-vindo criada
- [x] Redirecionamento correto implementado
- [ ] **Webhook configurado no painel do Mercado Pago** ⚠️ FAZER ISSO!
- [ ] Teste real com PIX

## 🚀 PRÓXIMOS PASSOS

1. **URGENTE:** Configure o webhook no painel do Mercado Pago
   - URL: `https://dojo-on.onrender.com/payments/webhook/`
   - Eventos: `payment.created`, `payment.updated`

2. Faça um teste real com PIX (R$ 1,00)

3. Monitore os logs no Render

4. Confirme que assinatura foi ativada

5. Teste o redirecionamento para dashboard

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique logs no Render
2. Execute comandos de diagnóstico
3. Consulte documentação do Mercado Pago: https://www.mercadopago.com.br/developers/

