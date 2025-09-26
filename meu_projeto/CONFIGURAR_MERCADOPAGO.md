# 🚀 Configuração do Mercado Pago

## 📋 Pré-requisitos

1. **Conta no Mercado Pago** - Crie uma conta em [mercadopago.com.br](https://www.mercadopago.com.br)
2. **Acesso ao painel de desenvolvedores** - Faça login na sua conta

## 🔧 Passo a Passo

### 1. Criar Aplicação no Mercado Pago

1. Acesse: https://www.mercadopago.com.br/developers
2. Clique em **"Suas integrações"**
3. Clique em **"Criar aplicação"**
4. Preencha os dados:
   - **Nome**: Dojo Premium (ou o nome que preferir)
   - **Descrição**: Sistema de pagamentos para academia de judô
   - **Categoria**: E-commerce
   - **Site**: https://dojo-on.onrender.com (ou seu domínio)

### 2. Obter Credenciais

Após criar a aplicação, você verá:

- **Access Token** (chave de acesso)
- **Public Key** (chave pública)

### 3. Configurar Webhook (Opcional)

1. Na sua aplicação, vá em **"Webhooks"**
2. Adicione a URL: `https://dojo-on.onrender.com/payments/webhook/`
3. Selecione os eventos: `payment` e `subscription`
4. Copie o **Webhook Secret** gerado

### 4. Atualizar Arquivo .env

Edite o arquivo `.env` no projeto e substitua:

```env
# Credenciais do Mercado Pago (SUBSTITUA PELAS SUAS)
MERCADOPAGO_ACCESS_TOKEN=TEST-SEU_ACCESS_TOKEN_AQUI
MERCADOPAGO_PUBLIC_KEY=TEST-SUA_PUBLIC_KEY_AQUI
MERCADOPAGO_WEBHOOK_SECRET=seu_webhook_secret_aqui
MERCADOPAGO_WEBHOOK_URL=https://dojo-on.onrender.com/payments/webhook/
```

### 5. Configurar no Sistema

Execute os comandos:

```bash
# Configurar credenciais no banco de dados
python manage.py configurar_mercadopago

# Testar conexão
python manage.py testar_mercadopago
```

## 🧪 Ambiente de Teste vs Produção

### Sandbox (Teste)
- Use credenciais que começam com `TEST-`
- Pagamentos são simulados
- Ideal para desenvolvimento e testes

### Produção
- Use credenciais que começam com `APP-`
- Pagamentos reais
- Use apenas quando estiver pronto para vender

## 🔍 Verificar Configuração

### 1. Verificar Credenciais Salvas
```bash
python manage.py shell
```

```python
from payments.models import ConfiguracaoPagamento
config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
print(f"Access Token: {config.get_access_token()[:20]}...")
print(f"Public Key: {config.get_public_key()[:20]}...")
print(f"Ambiente: {config.ambiente}")
```

### 2. Testar Pagamento
1. Acesse: http://127.0.0.1:8000/payments/planos/
2. Escolha um plano
3. Preencha os dados
4. Teste o pagamento

## 🚨 Troubleshooting

### Erro: "PA_UNAUTHORIZED_RESULT_FROM_POLICIES"
- **Causa**: Credenciais inválidas ou expiradas
- **Solução**: Verifique se as credenciais estão corretas no arquivo `.env`

### Erro: "Webhook não recebido"
- **Causa**: URL do webhook incorreta ou não configurada
- **Solução**: Verifique se a URL está correta e acessível

### Erro: "Access token não encontrado"
- **Causa**: Comando de configuração não foi executado
- **Solução**: Execute `python manage.py configurar_mercadopago`

## 📞 Suporte

Se tiver problemas:

1. Verifique os logs: `python manage.py testar_mercadopago`
2. Consulte a documentação: https://www.mercadopago.com.br/developers
3. Verifique se as credenciais estão corretas

## ✅ Checklist de Configuração

- [ ] Conta criada no Mercado Pago
- [ ] Aplicação criada no painel de desenvolvedores
- [ ] Credenciais copiadas (Access Token e Public Key)
- [ ] Webhook configurado (opcional)
- [ ] Arquivo `.env` atualizado com as credenciais
- [ ] Comando `configurar_mercadopago` executado
- [ ] Comando `testar_mercadopago` executado com sucesso
- [ ] Teste de pagamento realizado

---

**🎉 Pronto! Seu sistema de pagamentos está configurado e funcionando!**
