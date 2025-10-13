# 🥋 Dojo On - Academia de Judô Online

Sistema completo de ensino de Judô online com gestão de assinaturas premium.

## 🚀 Deploy no Render

### Variáveis de Ambiente Necessárias:

```bash
# Django
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,www.dojoon.com.br,dojoon.com.br,dojoon.onrender.com

# Database (PostgreSQL fornecido pelo Render)
DATABASE_URL=postgresql://...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
DEFAULT_FROM_EMAIL=noreply@dojoon.com.br

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu_token_aqui
MERCADOPAGO_PUBLIC_KEY=sua_public_key_aqui
```

## 📦 Instalação Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Migrar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Rodar servidor
python manage.py runserver
```

## 🌐 URLs

- **Site:** https://www.dojoon.com.br
- **Dashboard Admin:** https://www.dojoon.com.br/dashboard/login/
- **Admin Django:** https://www.dojoon.com.br/admin/

## 🔐 Credenciais do Dashboard

- **Usuário:** admin
- **Senha:** limueiro

## 📋 Funcionalidades

- ✅ Sistema de faixas (Branca a Marrom)
- ✅ Vídeos e técnicas de Judô
- ✅ Quiz interativo
- ✅ Sistema de pagamentos (Mercado Pago)
- ✅ Assinaturas Premium
- ✅ Dashboard administrativo
- ✅ Gestão de usuários
- ✅ Recuperação de senha via email

## 🛠️ Tecnologias

- Django 5.2.5
- PostgreSQL
- Tailwind CSS
- Mercado Pago API
- Render (Deploy)

## 📞 Suporte

Desenvolvido por Caio Campos

---

© 2024 Dojo On - Todos os direitos reservados

