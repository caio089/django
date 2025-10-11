# Configuração do Domínio - www.dojoon.com.br

## ✅ Configurações Atualizadas

### 1. ALLOWED_HOSTS
```python
ALLOWED_HOSTS = [
    'www.dojoon.com.br',
    'dojoon.com.br',
    'localhost',
    '127.0.0.1',
    'testserver'
]
```

### 2. CSRF_TRUSTED_ORIGINS
```python
CSRF_TRUSTED_ORIGINS = [
    'https://www.dojoon.com.br',
    'https://dojoon.com.br',
    'https://dojo-on.onrender.com',
    'https://*.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

### 3. Email Padrão
```python
DEFAULT_FROM_EMAIL = 'noreply@dojoon.com.br'
```

## 🔧 Próximos Passos

1. **Configurar DNS**: Apontar o domínio para o servidor
2. **SSL**: Configurar certificado HTTPS
3. **Deploy**: Fazer deploy com as novas configurações
4. **Teste**: Verificar se o site funciona no novo domínio

## 📝 Variáveis de Ambiente

Para produção, configure estas variáveis:

```bash
ALLOWED_HOSTS=www.dojoon.com.br,dojoon.com.br
DEFAULT_FROM_EMAIL=noreply@dojoon.com.br
```

## 🌐 URLs do Site

- **Principal**: https://www.dojoon.com.br
- **Sem www**: https://dojoon.com.br
- **Desenvolvimento**: http://localhost:8000
