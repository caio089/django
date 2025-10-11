# 🧪 Teste do Dashboard - Guia Rápido

## 📋 Checklist de Verificação

### 1️⃣ **Servidor Rodando?**
```bash
python manage.py runserver
```
✅ Deve mostrar: `Starting development server at http://127.0.0.1:8000/`

### 2️⃣ **Você é Superusuário?**
```bash
python manage.py createsuperuser
```
✅ Crie um superusuário se não tiver

### 3️⃣ **Fazer Login no Admin**
1. Acesse: `http://localhost:8000/admin/`
2. Faça login com seu superusuário
3. ✅ Deve aparecer o painel admin do Django

### 4️⃣ **Acessar o Dashboard**
1. Acesse: `http://localhost:8000/dashboard/admin-dashboard/`
2. ✅ Deve aparecer o dashboard com gráficos

## 🔍 Possíveis Problemas

### ❌ Erro 404 - Página não encontrada
**Solução:**
```bash
# Verifique se o app está instalado
python manage.py check
```

### ❌ Acesso Negado
**Causa:** Você não é superusuário

**Solução:**
```bash
# Tornar usuário existente em superusuário
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='SEU_USERNAME')
>>> user.is_superuser = True
>>> user.is_staff = True
>>> user.save()
>>> exit()
```

### ❌ Erro no Template
**Causa:** Problema com os dados

**Solução:** Verifique se existem pagamentos no sistema
```bash
python manage.py shell
>>> from payments.models import Payment
>>> Payment.objects.count()
```

### ❌ Gráficos não aparecem
**Causa:** Chart.js não carregou

**Solução:** Verifique a conexão com internet (Chart.js é carregado via CDN)

## ✅ Teste Rápido

```bash
# 1. Inicie o servidor
python manage.py runserver

# 2. Em outro terminal, teste a URL
curl http://localhost:8000/dashboard/admin-dashboard/
```

## 🎯 URLs Corretas

- ✅ Dashboard: `http://localhost:8000/dashboard/admin-dashboard/`
- ✅ Admin: `http://localhost:8000/admin/`
- ❌ Errado: `http://localhost:8000/dashboard/` (falta o admin-dashboard)

## 📞 Me diga qual erro você está vendo!

1. Erro 404?
2. Acesso negado?
3. Página em branco?
4. Erro no console do navegador?
5. Outro erro?
