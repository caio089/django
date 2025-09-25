# 🔧 Configuração Final - Credenciais

## ✅ **Sistema Pronto! Só Falta Configurar as Credenciais**

### 🎯 **O que você precisa fazer:**

---

## 1️⃣ **CONFIGURAR SUPABASE**

### **Onde encontrar as credenciais:**
1. Acesse [supabase.com](https://supabase.com)
2. Entre no seu projeto
3. Vá em **Settings** → **Database**
4. Copie as credenciais

### **Credenciais necessárias:**
- 🌍 **Host**: `seu-projeto.supabase.co`
- 🔌 **Porta**: `5432`
- 🗄️ **Database**: `postgres`
- 👤 **User**: `postgres`
- 🔑 **Password**: `sua-senha`

---

## 2️⃣ **CONFIGURAR MERCADO PAGO**

### **Onde encontrar as credenciais:**
1. Acesse [mercadopago.com.br](https://mercadopago.com.br)
2. Vá em **Desenvolvedores** → **Suas integrações**
3. Copie as credenciais

### **Credenciais necessárias:**
- 🔑 **Access Token**: `APP_USR-1234567890-abcdef`
- 🔑 **Public Key**: `APP_USR-1234567890-abcdef`

---

## 🚀 **COMO CONFIGURAR (Escolha uma opção):**

### **Opção A: Script Automático**
```bash
python setup_credentials.py
```

### **Opção B: Manual**
1. **Crie arquivo `.env`** na raiz do projeto:
```env
# Supabase
DB_HOST=seu-projeto.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua-senha

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=TEST-seu-access-token
MERCADOPAGO_PUBLIC_KEY=TEST-sua-public-key
SITE_URL=https://seu-dominio.com
```

2. **Configure Mercado Pago no Django:**
```python
# No Django shell
python manage.py shell

from payments.models import ConfiguracaoPagamento

ConfiguracaoPagamento.objects.create(
    access_token='TEST-seu-access-token',
    public_key='TEST-sua-public-key',
    webhook_url='https://seu-dominio.com/payments/webhook/',
    ambiente='sandbox',
    ativo=True
)
```

---

## 🔗 **CONFIGURAR WEBHOOK DO MERCADO PAGO**

1. **Acesse o painel do Mercado Pago**
2. **Vá em Webhooks**
3. **Adicione nova URL:**
   ```
   URL: https://seu-dominio.com/payments/webhook/
   Eventos: payment
   Método: POST
   ```

---

## ✅ **TESTAR O SISTEMA**

### **1. Iniciar servidor:**
```bash
python manage.py runserver
```

### **2. Acessar planos:**
```
http://localhost:8000/payments/planos/
```

### **3. Testar pagamento:**
- Escolha um plano
- Preencha os dados
- Teste PIX ou cartão

---

## 🎯 **STATUS ATUAL:**

✅ **Django configurado**  
✅ **Banco de dados funcionando**  
✅ **Modelos criados**  
✅ **Views implementadas**  
✅ **Templates prontos**  
✅ **URLs configuradas**  
✅ **Dependências instaladas**  
✅ **Dados iniciais criados**  

### **Falta apenas:**
🔧 **Credenciais do Supabase**  
🔧 **Credenciais do Mercado Pago**  
🔧 **Webhook configurado**  

---

## 🚀 **APÓS CONFIGURAR:**

O sistema estará **100% funcional** com:
- 💳 **PIX** funcionando
- 💳 **Cartão de crédito** funcionando
- 🔔 **Webhooks** automáticos
- 📊 **Relatórios** de pagamento
- 🎯 **Assinaturas** automáticas

**Tudo pronto para produção!** 🎉💪
