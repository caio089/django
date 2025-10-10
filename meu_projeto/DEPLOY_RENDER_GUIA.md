# 🚀 GUIA DE DEPLOY NO RENDER

## 📋 CONFIGURAÇÃO NO RENDER

### 1. Build Command:
```bash
chmod +x build_render.sh && ./build_render.sh
```

### 2. Start Command:
```bash
cd meu_projeto && gunicorn meu_projeto.wsgi:application
```

### 3. Variáveis de Ambiente Obrigatórias:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-app.onrender.com,*.onrender.com

# Banco de Dados Supabase
DATABASE_URL=postgresql://usuario:senha@host.supabase.com:5432/postgres

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu-token-aqui
MERCADOPAGO_PUBLIC_KEY=sua-chave-publica-aqui

# Opcional - Webhook
WEBHOOK_URL=https://seu-app.onrender.com/payments/webhook/
```

---

## 🔧 PASSOS PARA DEPLOY

### Passo 1: Criar Web Service no Render
1. Conectar repositório GitHub
2. Escolher branch (main/master)
3. Nome do serviço: `dojo-online`
4. Environment: `Python 3`
5. Build Command: `chmod +x build_render.sh && ./build_render.sh`
6. Start Command: `cd meu_projeto && gunicorn meu_projeto.wsgi:application`

### Passo 2: Configurar Variáveis de Ambiente
Adicionar todas as variáveis listadas acima na seção "Environment"

### Passo 3: Deploy
- Clicar em "Create Web Service"
- Aguardar build completar
- Verificar logs

---

## 🗄️ CONFIGURAÇÃO DO BANCO DE DADOS (SUPABASE)

### 1. Criar Projeto no Supabase
1. Acessar https://supabase.com
2. Criar novo projeto
3. Escolher região (preferencialmente perto do Brasil)
4. Copiar credenciais

### 2. Obter DATABASE_URL
No Supabase, ir em:
```
Settings → Database → Connection String → URI
```

Formato:
```
postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-1-us-east-2.pooler.supabase.com:5432/postgres
```

### 3. Configurar no Render
Cole a URL completa na variável `DATABASE_URL`

---

## 🔍 VERIFICAÇÃO PÓS-DEPLOY

### 1. Aplicar Migrations (Primeira vez):
```bash
# No terminal do Render (Shell):
cd meu_projeto
python manage.py migrate
```

### 2. Criar Superuser:
```bash
python manage.py createsuperuser
```

### 3. Configurar Planos:
```bash
python manage.py setup_producao
```

### 4. Testar Sistema:
1. Acessar: `https://seu-app.onrender.com`
2. Fazer login
3. Tentar acessar faixa (deve bloquear)
4. Ir para planos
5. Testar pagamento

---

## ⚠️ TROUBLESHOOTING

### Erro: "Connection refused" no build
**Causa:** Build tentando conectar ao banco  
**Solução:** Use `build_render.sh` que NÃO executa migrations no build

### Erro: Migrations não aplicadas
**Causa:** Migrations não rodaram  
**Solução:** Executar manualmente no Shell do Render

### Erro: Static files não carregam
**Causa:** STATIC_ROOT não configurado  
**Solução:** Já está configurado em settings.py

### Erro: 404 nas páginas
**Causa:** URLs não configuradas  
**Solução:** Verificar `meu_projeto/urls.py`

---

## 📊 ARQUIVOS IMPORTANTES

### Essenciais para Deploy:
- ✅ `build_render.sh` - Build otimizado
- ✅ `release.sh` - Aplicação de migrations
- ✅ `Procfile` - Comando de start
- ✅ `runtime.txt` - Versão do Python
- ✅ `requirements.txt` - Dependências
- ✅ `settings.py` - Configurações Django

### Comandos Úteis (Production):
- `sync_payment_status.py` - Sincronizar pagamentos
- `sync_subscriptions.py` - Sincronizar assinaturas
- `verificar_sistema.py` - Verificar saúde do sistema
- `configurar_mercadopago_producao.py` - Configurar MP
- `setup_producao.py` - Setup inicial

---

## 🎯 CHECKLIST DE DEPLOY

- [ ] Criar conta no Render
- [ ] Criar projeto no Supabase
- [ ] Configurar variáveis de ambiente
- [ ] Fazer primeiro deploy
- [ ] Aplicar migrations
- [ ] Criar superuser
- [ ] Configurar planos premium
- [ ] Testar fluxo de pagamento
- [ ] Configurar webhook do Mercado Pago
- [ ] Testar bloqueio de conteúdo
- [ ] Verificar logs

---

## ✅ SISTEMA PRONTO PARA PRODUÇÃO!

**Desenvolvido para:** DOJO ONLINE Academia de Judô  
**Última atualização:** 10/10/2025

