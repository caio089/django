# Deploy no Render - Dojo Online

## Configuração do Render

### 1. Configurar Variáveis de Ambiente

No painel do Render, adicione as seguintes variáveis de ambiente:

```
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=dojo-on.onrender.com,localhost,127.0.0.1

# Banco de Dados (Supabase)
DB_NAME=postgres
DB_USER=seu_usuario_supabase
DB_PASSWORD=sua_senha_supabase
DB_HOST=seu_host_supabase
DB_PORT=5432

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=seu_access_token_mercadopago
MERCADO_PAGO_PUBLIC_KEY=sua_public_key_mercadopago
MERCADO_PAGO_WEBHOOK_URL=https://dojo-on.onrender.com/payments/webhook/

# Configurações de Ambiente
USE_SQLITE_FALLBACK=False
```

### 2. Configurações do Serviço

- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn meu_projeto.wsgi:application`
- **Python Version**: 3.11.0

### 3. Configurar Banco de Dados

1. Crie um banco PostgreSQL no Supabase
2. Configure as variáveis de ambiente do banco
3. Execute as migrações localmente ou via comando no Render

### 4. Configurar Mercado Pago

1. Crie uma conta no Mercado Pago
2. Obtenha as chaves de API (Access Token e Public Key)
3. Configure o webhook URL no Mercado Pago
4. Adicione as variáveis de ambiente

### 5. Arquivos de Configuração

- `requirements.txt` - Dependências Python
- `Procfile` - Comando de inicialização
- `build.sh` - Script de build
- `runtime.txt` - Versão do Python
- `env.example` - Exemplo de variáveis de ambiente

### 6. Comandos Úteis

```bash
# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar superusuário
python manage.py createsuperuser

# Testar configuração
python manage.py check --deploy
```

### 7. Troubleshooting

- Verifique se todas as variáveis de ambiente estão configuradas
- Confirme se o banco de dados está acessível
- Verifique os logs do Render para erros
- Teste as URLs de webhook do Mercado Pago

### 8. URLs Importantes

- **Aplicação**: https://dojo-on.onrender.com
- **Admin**: https://dojo-on.onrender.com/admin/
- **Webhook Mercado Pago**: https://dojo-on.onrender.com/payments/webhook/
