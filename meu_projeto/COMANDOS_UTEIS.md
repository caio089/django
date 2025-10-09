# 🛠️ Comandos Úteis - Supabase & Django

## 🚀 Migração para Supabase

### Migração Automática (Recomendado)
```bash
python migrate_to_supabase.py
```

### Migração Manual (Passo a Passo)

#### 1. Backup dos dados do SQLite
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > backup_sqlite.json
```

#### 2. Aplicar migrações no PostgreSQL
```bash
# Certifique-se de que o .env está configurado
python manage.py migrate
```

#### 3. Carregar dados no PostgreSQL
```bash
python manage.py loaddata backup_sqlite.json
```

#### 4. Criar superusuário
```bash
python manage.py createsuperuser
```

---

## 🔍 Verificação e Testes

### Testar conexão com banco
```bash
python manage.py check --database default
```

### Acessar shell do banco
```bash
# PostgreSQL
python manage.py dbshell

# Comandos úteis dentro do psql:
\dt                 # Listar tabelas
\d nome_tabela      # Descrever tabela
\l                  # Listar bancos
\q                  # Sair
```

### Ver estatísticas do banco
```python
python manage.py shell

from django.contrib.auth.models import User
from payments.models import Assinatura, Pagamento

print(f"Usuários: {User.objects.count()}")
print(f"Assinaturas: {Assinatura.objects.count()}")
print(f"Pagamentos: {Pagamento.objects.count()}")
```

---

## 💾 Backup e Restore

### Backup Completo
```bash
# Exportar tudo
python manage.py dumpdata --indent 2 > backup_completo.json

# Exportar apenas app específico
python manage.py dumpdata payments --indent 2 > backup_payments.json

# Exportar sem permissões
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > backup_limpo.json
```

### Restore (Restaurar)
```bash
# Restaurar tudo
python manage.py loaddata backup_completo.json

# Restaurar app específico
python manage.py loaddata backup_payments.json
```

### Backup direto do PostgreSQL (Avançado)
```bash
# Usando pg_dump (requer PostgreSQL instalado localmente)
pg_dump -h SEU_HOST -U SEU_USER -d postgres > backup.sql

# Restaurar
psql -h SEU_HOST -U SEU_USER -d postgres < backup.sql
```

---

## 🔄 Sincronização de Assinaturas

### Sincronizar pagamentos pendentes
```bash
# Modo dry-run (não faz alterações)
python manage.py sync_subscriptions --dry-run

# Sincronizar de verdade
python manage.py sync_subscriptions
```

---

## 🗄️ Gerenciamento de Migrações

### Ver status das migrações
```bash
python manage.py showmigrations
```

### Criar nova migração
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Reverter migração
```bash
# Reverter para migração específica
python manage.py migrate nome_app 0001

# Reverter todas do app
python manage.py migrate nome_app zero
```

---

## 🧹 Limpeza e Manutenção

### Limpar sessões expiradas
```bash
python manage.py clearsessions
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Verificar problemas
```bash
python manage.py check
```

---

## 📊 Monitoramento

### Ver queries SQL executadas
```python
python manage.py shell

from django.db import connection
from django.db import reset_queries

# Habilitar debug
from django.conf import settings
settings.DEBUG = True

# Executar queries
from payments.models import Assinatura
assinaturas = list(Assinatura.objects.filter(status='ativa'))

# Ver queries
for query in connection.queries:
    print(query['sql'])
```

### Analisar performance de query
```python
python manage.py shell

from django.db import connection
import time

start = time.time()
from payments.models import Assinatura
assinaturas = list(Assinatura.objects.select_related('usuario', 'plano'))
end = time.time()

print(f"Tempo: {end - start:.3f}s")
print(f"Queries: {len(connection.queries)}")
```

---

## 🔐 Segurança

### Gerar nova SECRET_KEY
```python
python manage.py shell

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Criar hash de senha
```python
python manage.py shell

from django.contrib.auth.hashers import make_password
print(make_password('sua_senha'))
```

---

## 🌐 Deploy

### Coletar estáticos para produção
```bash
python manage.py collectstatic --noinput --clear
```

### Verificar configurações de produção
```bash
python manage.py check --deploy
```

### Comprimir arquivos estáticos
```bash
python manage.py compress
```

---

## 🐛 Debug

### Shell interativo do Django
```bash
python manage.py shell
```

### Shell plus (se instalado django-extensions)
```bash
pip install django-extensions ipython
python manage.py shell_plus
```

### Ver configurações atuais
```python
python manage.py shell

from django.conf import settings

print(f"DEBUG: {settings.DEBUG}")
print(f"DATABASES: {settings.DATABASES}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
```

---

## 📝 Logs

### Ver logs em tempo real (Linux/Mac)
```bash
tail -f logs/django.log
```

### Ver logs (Windows PowerShell)
```powershell
Get-Content logs/django.log -Wait
```

### Limpar logs
```bash
# Windows
del logs\django.log

# Linux/Mac
rm logs/django.log
```

---

## 🧪 Testes

### Executar todos os testes
```bash
python manage.py test
```

### Executar testes de um app
```bash
python manage.py test payments
```

### Executar teste específico
```bash
python manage.py test payments.tests.test_models
```

### Coverage (cobertura de testes)
```bash
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Gera relatório HTML
```

---

## 🔄 Utilitários de Banco

### Resetar banco (⚠️ CUIDADO!)
```bash
# ISSO APAGA TUDO!
python manage.py flush

# Ou resetar migrações
python manage.py migrate payments zero
python manage.py migrate payments
```

### Criar dados de teste
```python
python manage.py shell

from django.contrib.auth.models import User
from payments.models import PlanoPremium

# Criar usuários de teste
for i in range(10):
    User.objects.create_user(
        username=f'user{i}',
        email=f'user{i}@example.com',
        password='senha123'
    )

print("10 usuários criados!")
```

---

## 📊 Análise de Dados

### Exportar para CSV
```python
python manage.py shell

import csv
from payments.models import Pagamento

with open('pagamentos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Usuario', 'Valor', 'Status', 'Data'])
    
    for p in Pagamento.objects.all():
        writer.writerow([p.id, p.usuario.username, p.valor, p.status, p.data_criacao])

print("Exportado: pagamentos.csv")
```

---

## 🎯 Comandos Rápidos do Dia a Dia

```bash
# Iniciar servidor
python manage.py runserver

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Sincronizar assinaturas
python manage.py sync_subscriptions

# Backup rápido
python manage.py dumpdata > backup.json

# Shell Django
python manage.py shell
```

---

## 💡 Dicas

### Criar alias (Linux/Mac)
```bash
# Adicionar no ~/.bashrc ou ~/.zshrc
alias djrun="python manage.py runserver"
alias djmigrate="python manage.py migrate"
alias djshell="python manage.py shell"
```

### Criar funções PowerShell (Windows)
```powershell
# Adicionar no $PROFILE
function djrun { python manage.py runserver }
function djmigrate { python manage.py migrate }
function djshell { python manage.py shell }
```

---

**📚 Para mais comandos, consulte:**
- Django Docs: https://docs.djangoproject.com/
- Supabase Docs: https://supabase.com/docs
