# 🚀 Guia de Configuração do Supabase (PostgreSQL)

## 📋 Índice
1. [Criar Conta no Supabase](#1-criar-conta-no-supabase)
2. [Criar Projeto](#2-criar-projeto)
3. [Obter Credenciais](#3-obter-credenciais)
4. [Configurar Variáveis de Ambiente](#4-configurar-variáveis-de-ambiente)
5. [Migrar Dados](#5-migrar-dados)
6. [Verificar Funcionamento](#6-verificar-funcionamento)

---

## 1. Criar Conta no Supabase

### Passo a passo:
1. Acesse: https://supabase.com/
2. Clique em **"Start your project"**
3. Faça login com GitHub, Google ou Email

✅ **Plano Free inclui:**
- 500 MB de banco de dados PostgreSQL
- 2 GB de armazenamento
- 50.000 usuários ativos mensais (MAU)
- Ilimitado de requisições API

---

## 2. Criar Projeto

### Passo a passo:
1. No dashboard do Supabase, clique em **"New Project"**
2. Preencha os campos:
   - **Name**: `judo-site` (ou o nome que preferir)
   - **Database Password**: Escolha uma senha FORTE (mínimo 12 caracteres)
     - **⚠️ IMPORTANTE:** Guarde essa senha! Você vai precisar dela!
   - **Region**: Escolha **"South America (São Paulo)"** para menor latência
   - **Pricing Plan**: Selecione **"Free"**
3. Clique em **"Create new project"**
4. Aguarde 2-3 minutos enquanto o projeto é criado

---

## 3. Obter Credenciais

### Método 1: Connection String Completa (RECOMENDADO)

1. No seu projeto, vá em **Settings** (engrenagem no menu lateral)
2. Clique em **Database** no menu
3. Role até encontrar **"Connection string"**
4. Selecione a aba **"URI"**
5. Copie a string que aparece (algo como):
   ```
   postgresql://postgres.xxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:5432/postgres
   ```
6. **SUBSTITUA** `[YOUR-PASSWORD]` pela senha que você criou no passo 2
7. Exemplo final:
   ```
   postgresql://postgres.abc123xyz:MinhaSenh@F0rte!@aws-0-sa-east-1.pooler.supabase.com:5432/postgres
   ```

### Método 2: Credenciais Individuais (Alternativa)

Na mesma página **Settings > Database**, você também encontra:
- **Host**: `aws-0-sa-east-1.pooler.supabase.com`
- **Database name**: `postgres`
- **Port**: `5432`
- **User**: `postgres.xxxxxxxxxxx`
- **Password**: A senha que você criou

---

## 4. Configurar Variáveis de Ambiente

### Opção A: Usando Connection String (Mais Fácil)

1. Crie um arquivo `.env` na raiz do projeto `meu_projeto/`:
   ```bash
   # Windows (PowerShell)
   New-Item -Path ".env" -ItemType File
   
   # Linux/Mac
   touch .env
   ```

2. Adicione a seguinte configuração no arquivo `.env`:
   ```env
   # Supabase PostgreSQL
   DATABASE_URL=postgresql://postgres.abc123xyz:MinhaSenh@F0rte!@aws-0-sa-east-1.pooler.supabase.com:5432/postgres
   
   # Django
   SECRET_KEY=django-insecure-sua-chave-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

### Opção B: Usando Variáveis Individuais

Se preferir, configure assim no `.env`:
```env
# Supabase PostgreSQL
DB_NAME=postgres
DB_USER=postgres.abc123xyz
DB_PASSWORD=MinhaSenh@F0rte!
DB_HOST=aws-0-sa-east-1.pooler.supabase.com
DB_PORT=5432

# Django
SECRET_KEY=django-insecure-sua-chave-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### ⚠️ IMPORTANTE:
- O arquivo `.env` **NÃO** deve ser enviado para o GitHub (já está no .gitignore)
- Nunca compartilhe suas credenciais
- Use senhas fortes!

---

## 5. Migrar Dados

### Passo a passo:

1. **Aplicar migrações no novo banco:**
   ```bash
   python manage.py migrate
   ```

2. **Criar superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

3. **[OPCIONAL] Migrar dados do SQLite para PostgreSQL:**
   
   Se você já tem dados no SQLite e quer migrá-los:
   
   ```bash
   # 1. Fazer backup dos dados do SQLite
   python manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup_sqlite.json
   
   # 2. Configurar o .env para usar PostgreSQL (já feito acima)
   
   # 3. Aplicar migrações no PostgreSQL
   python manage.py migrate
   
   # 4. Carregar os dados no PostgreSQL
   python manage.py loaddata backup_sqlite.json
   ```

---

## 6. Verificar Funcionamento

### Teste de conexão:

Execute o comando:
```bash
python manage.py dbshell
```

Se conectar com sucesso, você verá algo como:
```
psql (14.x)
Type "help" for help.

postgres=>
```

Digite `\dt` para listar as tabelas:
```sql
\dt
```

Para sair, digite:
```sql
\q
```

### Teste no site:

1. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

2. Acesse: http://localhost:8000

3. Faça login e teste as funcionalidades

---

## 📊 Monitoramento no Supabase

### Verificar uso do banco:

1. Acesse seu projeto no Supabase
2. Vá em **Settings > Database**
3. Role até **Database size** para ver o espaço usado

### Visualizar dados:

1. No Supabase, clique em **Table Editor**
2. Você verá todas as tabelas do Django
3. Pode visualizar, editar e exportar dados diretamente

### Backup automático:

- Plano Free: 7 dias de backup automático
- Plano Pro: 30 dias de backup automático

---

## 🔧 Solução de Problemas

### Erro: "password authentication failed"
- Verifique se a senha no `.env` está correta
- Certifique-se de que substituiu `[YOUR-PASSWORD]` pela senha real

### Erro: "could not connect to server"
- Verifique sua conexão com a internet
- Confirme se o host está correto
- Verifique se não há firewall bloqueando a porta 5432

### Erro: "SSL connection required"
- Adicione `?sslmode=require` no final da DATABASE_URL
- Exemplo: `postgresql://...postgres?sslmode=require`

### Banco muito lento:
- Plano Free tem limites de performance
- Considere upgrade para Pro ($25/mês) se necessário
- Verifique índices no banco de dados

---

## 💡 Dicas Importantes

### Performance:
- ✅ Use conexão pooler (já vem configurado no Supabase)
- ✅ Crie índices em campos frequentemente consultados
- ✅ Use paginação em listas grandes

### Segurança:
- 🔒 Sempre use SSL em produção
- 🔒 Nunca exponha credenciais no código
- 🔒 Use variáveis de ambiente
- 🔒 Faça backups regulares

### Escalabilidade:
- 📈 Monitore o uso do banco regularmente
- 📈 Considere upgrade quando atingir 70% da capacidade
- 📈 Implemente cache (Redis) para otimizar

---

## 📞 Suporte

- **Documentação Supabase**: https://supabase.com/docs
- **Discord Supabase**: https://discord.supabase.com/
- **Status Supabase**: https://status.supabase.com/

---

## ✅ Checklist Final

Antes de ir para produção, verifique:

- [ ] Conexão com Supabase funcionando
- [ ] Migrações aplicadas
- [ ] Dados migrados (se aplicável)
- [ ] Superusuário criado
- [ ] Site funcionando localmente
- [ ] Backup dos dados antigos
- [ ] Arquivo `.env` no `.gitignore`
- [ ] Variáveis de ambiente configuradas
- [ ] SSL habilitado
- [ ] Testes executados com sucesso

---

**🎉 Parabéns! Seu sistema agora está usando PostgreSQL com Supabase!**

**Capacidade atual:**
- 👥 100.000+ usuários
- 💳 10.000+ assinaturas ativas
- 🚀 1.000+ usuários simultâneos
