# 📊 Dashboard Administrativo - Dojoon

## 🎯 Funcionalidades

### 📈 Métricas Principais
- **Assinaturas Ativas**: Total de assinaturas premium ativas
- **Usuários Premium**: Número único de usuários com premium
- **Receita Total**: Soma de todas as receitas aprovadas
- **Receita Mensal**: Receita do mês atual
- **Total de Usuários**: Todos os usuários cadastrados no site
- **Novos Usuários**: Usuários cadastrados este mês

### ⭐ Gestão de Usuários
- **Atribuir Premium**: Dar plano premium manualmente para qualquer usuário
- **Lista de Usuários**: Visualizar todos os usuários cadastrados
- **Status Premium**: Ver quais usuários têm premium ativo

### 📊 Gráficos e Relatórios
- **Receita Mensal**: Gráfico de linha com 12 meses de histórico
- **Novas Assinaturas**: Gráfico de barras com crescimento mensal
- **Comparação Mensal**: Comparativo entre mês atual e anterior
- **Status das Assinaturas**: Distribuição por status

### 📋 Tabelas
- **Assinaturas Recentes**: Últimas 10 assinaturas aprovadas
- **Detalhes por Usuário**: Informações completas de cada pagamento

## 🔐 Acesso

### URL
```
https://www.dojoon.com.br/dashboard/admin-dashboard/
```

### Permissões
- Apenas **superusuários** podem acessar
- Requer login no Django Admin

## 🎨 Interface

### Design
- **Responsivo**: Funciona em desktop e mobile
- **Moderno**: Interface limpa com gradientes
- **Interativo**: Gráficos com Chart.js
- **Intuitivo**: Cards com métricas principais

### Cores
- **Azul/Roxo**: Header principal
- **Verde**: Usuários premium
- **Azul Claro**: Receitas
- **Rosa**: Crescimento
- **Roxo**: Assinaturas

## 📊 Dados Exibidos

### Estatísticas em Tempo Real
```python
# Exemplos de métricas
active_subscriptions = 150        # Assinaturas ativas
unique_premium_users = 120        # Usuários únicos
total_revenue = 15000.00          # Receita total (R$)
current_month_revenue = 2500.00   # Receita deste mês (R$)
growth_percentage = 15.5          # Crescimento (%)
```

### Histórico de 12 Meses
- Receita mensal detalhada
- Novos usuários premium por mês
- Tendências de crescimento
- Comparativos mensais

## 🛠️ Implementação Técnica

### Tecnologias
- **Backend**: Django + Python
- **Frontend**: HTML5 + Tailwind CSS
- **Gráficos**: Chart.js
- **Dados**: PostgreSQL (Supabase)

### Estrutura
```
dashboard/
├── views.py          # Lógica do dashboard
├── urls.py           # Rotas
├── models.py         # Modelos (usa payments)
├── templates/
│   └── dashboard/
│       ├── dashboard.html
│       └── access_denied.html
└── README.md
```

## 🚀 Como Usar

1. **Acesse**: `https://www.dojoon.com.br/dashboard/admin-dashboard/`
2. **Login**: Use suas credenciais de admin
3. **Visualize**: Métricas e gráficos em tempo real
4. **Analise**: Tendências e crescimento

## 📱 Responsividade

### Desktop
- Layout em grid 4 colunas
- Gráficos lado a lado
- Tabelas completas

### Mobile
- Layout em coluna única
- Gráficos empilhados
- Tabelas com scroll horizontal

## 🔄 Atualização

Os dados são atualizados em tempo real a cada acesso, mostrando:
- Status atual das assinaturas
- Receitas mais recentes
- Histórico completo

## 🎯 Benefícios

- **Visão Geral**: Métricas importantes em um local
- **Tomada de Decisão**: Dados para estratégias
- **Monitoramento**: Acompanhamento de crescimento
- **Relatórios**: Histórico detalhado
