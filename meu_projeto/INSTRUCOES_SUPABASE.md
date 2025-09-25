# 🔧 Configuração do Supabase e Mercado Pago

## 📋 Passo a Passo para Configurar

### 1️⃣ **Configurar Supabase**

1. **Acesse o Supabase**: [supabase.com](https://supabase.com)
2. **Faça login** na sua conta
3. **Selecione seu projeto** ou crie um novo
4. **Vá para Settings → Database**
5. **Copie as informações** da "Connection string"

### 2️⃣ **Criar arquivo .env**

1. **Copie o arquivo `env_exemplo.txt`** e renomeie para `.env`
2. **Preencha as informações** do Supabase:

```env
# Substitua pelos seus valores reais do Supabase
DB_HOST=seu-projeto.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua-senha-real-aqui
```

### 3️⃣ **Configurar Mercado Pago (Opcional)**

1. **Acesse**: [mercadopago.com.br](https://mercadopago.com.br)
2. **Vá para**: Desenvolvedores → Suas integrações
3. **Copie** o Access Token e Public Key
4. **Adicione no arquivo .env**:

```env
MERCADOPAGO_ACCESS_TOKEN=TEST-seu-token-real-aqui
MERCADOPAGO_PUBLIC_KEY=TEST-sua-chave-real-aqui
```

### 4️⃣ **Executar o Servidor**

```bash
python manage.py runserver
```

## 🔍 **Onde Encontrar as Informações**

### **Supabase:**
- **Host**: `seu-projeto.supabase.co` (encontre em Settings → Database)
- **Senha**: Na seção "Connection string" do Supabase
- **Porta**: Geralmente `5432`
- **Banco**: Geralmente `postgres`
- **Usuário**: Geralmente `postgres`

### **Mercado Pago:**
- **Access Token**: Em Desenvolvedores → Suas integrações
- **Public Key**: Na mesma seção do Mercado Pago

## ⚠️ **Importante**

- **Nunca compartilhe** o arquivo `.env`
- **Use TEST-** para desenvolvimento
- **Use PROD-** para produção
- **Mantenha as credenciais seguras**

## 🚀 **Testando a Configuração**

Após configurar o `.env`, execute:

```bash
python manage.py runserver
```

Se aparecer "System check identified no issues", está funcionando! 🎉
