# 📚 Página de Regras de Competição - Judô

## 🎯 Descrição

Esta é uma página web completa e interativa sobre as **regras de competição e luta** do judô atual (2025), criada com HTML, CSS, JavaScript e Tailwind CSS. A página foi projetada para ser educativa e acessível para judocas de todas as idades, seguindo o padrão visual do seu site.

## ✨ Características Principais

### 🎨 Design e Interface
- **Design elegante e minimalista** seguindo o padrão visual do seu site
- **Cores personalizadas** (judo-blue, judo-green, judo-orange, etc.)
- **Fontes consistentes** (Montserrat, Poppins, Inter) como nas outras páginas
- **Interface responsiva** que funciona em todos os dispositivos
- **Animações suaves** sem elementos obstrutivos
- **Navegação intuitiva** com menu fixo no topo

### 📱 Funcionalidades Interativas
- **Navegação por seções** com scroll suave
- **Menu responsivo** para dispositivos móveis
- **Botão "voltar ao topo"** que aparece ao rolar
- **Animações de entrada** para elementos da página
- **Efeitos hover** nos cards e botões
- **Highlight** de seção ativa no menu

### 📚 Conteúdo Focado em Competição
- **Regras do Kimono**: Tamanhos, materiais, medidas e especificações
- **Regras da Luta**: Área de combate, duração, Golden Score
- **Punições e Infrações**: Shido (leves) e Hansoku-make (graves)
- **Técnicas Permitidas/Proibidas**: O que pode e o que não pode fazer
- **Regras por Categoria**: Infantil vs. Adulto
- **Dicas para Competição**: Mental, físico e técnica

## 🚀 Como Usar

### 1. Acessar a Página
- Navegue para `/regras/` no seu projeto Django
- A página carregará automaticamente com todas as funcionalidades

### 2. Navegação
- **Menu superior**: Links para cada seção da página
- **Scroll suave**: Clique nos links do menu para navegar
- **Menu mobile**: Botão hambúrguer em dispositivos pequenos

### 3. Seções Disponíveis
- **Kimono**: Regras e especificações do judogi
- **Regras**: Regras fundamentais da luta
- **Punições**: Infrações e suas consequências
- **Técnicas**: O que é permitido e proibido
- **Dicas**: Conselhos para competição

## 🛠️ Tecnologias Utilizadas

### Frontend
- **HTML5**: Estrutura semântica e acessível
- **Tailwind CSS**: Framework CSS utilitário com cores personalizadas
- **JavaScript**: Interatividade e animações
- **Font Awesome**: Ícones para melhor experiência visual

### Recursos Externos
- **Google Fonts**: Fontes Montserrat, Poppins e Inter
- **CDN**: Tailwind CSS e Font Awesome via CDN

## 🎨 Padrão Visual do Site

### Cores Personalizadas
```javascript
judo: {
    gray: '#6B7280',
    blue: '#3B82F6',      // Azul principal
    yellow: '#FBBF24',    // Amarelo
    orange: '#F97316',    // Laranja
    green: '#10B981',     // Verde
    purple: '#8B5CF6',    // Roxo
    brown: '#92400E'      // Marrom
}
```

### Fontes
- **font-title**: Montserrat (títulos principais)
- **font-subtitle**: Poppins (subtítulos)
- **font-desc**: Inter (texto descritivo)

### Estilos
- **Gradientes**: Bordas com gradiente cinza
- **Sombras**: Cards com sombras suaves
- **Animações**: Transições e efeitos hover

## 📱 Responsividade

A página é totalmente responsiva e se adapta a:
- **Desktop**: Layout em colunas múltiplas
- **Tablet**: Layout intermediário
- **Mobile**: Layout em coluna única com menu hambúrguer

## 🔧 Manutenção

### Atualizar Conteúdo
Para atualizar as regras ou adicionar novas seções:
1. Edite o arquivo `regras.html`
2. Mantenha a estrutura de seções com IDs únicos
3. Adicione novos links no menu de navegação
4. Use as classes de fonte apropriadas (font-title, font-subtitle, font-desc)

### Adicionar Novas Funcionalidades
- **Novas seções**: Adicione `<section id="novo-id">`
- **Novos estilos**: Use classes Tailwind ou CSS customizado
- **Novas animações**: Defina no bloco `<style>` ou JavaScript

## 🌟 Recursos Avançados

### JavaScript
- **Scroll suave** entre seções
- **Animações on-scroll** para elementos
- **Menu mobile** responsivo
- **Highlight** de seção ativa no menu
- **Efeitos hover** nos cards

### CSS
- **Gradientes** para bordas dos cards
- **Transições** suaves para interações
- **Sombras** dinâmicas nos cards
- **Animações keyframe** personalizadas

## 📊 Performance

- **Carregamento otimizado** com CDNs
- **Animações CSS** para melhor performance
- **Lazy loading** de elementos visuais
- **Código JavaScript** eficiente e organizado

## 🎯 Público-Alvo

- **Judocas iniciantes** que querem aprender as regras de competição
- **Competidores** que precisam revisar as regras antes de lutar
- **Treinadores** que ensinam as regras aos alunos
- **Pais** que acompanham seus filhos em competições
- **Arbitros** que precisam de referência rápida

## 📝 Conteúdo Específico

### Regras do Kimono
- **Tamanhos**: Masculino (1-5), Feminino (F1-F4), Infantil (I1-I4)
- **Material**: 100% algodão, peso mínimo 700g
- **Medidas**: Manga 5-7cm do pulso, calça 5-7cm do tornozelo
- **Permitido**: Kimono limpo, faixa 4-5cm, roupas brancas por baixo
- **Proibido**: Kimono sujo/rasgado, faixa inadequada, roupas coloridas

### Regras da Luta
- **Área**: Tatame 8x8 metros, área segura 3 metros
- **Duração**: Sênior/Júnior 4min, Cadete 3min, Infantil 2min
- **Golden Score**: Em caso de empate, primeiro ponto vence

### Punições
- **Shido**: Passividade, sair da área, técnicas perigosas (3 = desqualificação)
- **Hansoku-make**: Golpes proibidos, comportamento antidesportivo (desqualificação imediata)

### Técnicas
- **Permitidas**: Nage-waza (projeções), Katame-waza (controle)
- **Proibidas**: Golpes com mão fechada, chutes, técnicas perigosas
- **Categorias**: Infantis (sem finalizações), Adultos (todas permitidas)

## 📝 Notas Importantes

- Todas as regras estão baseadas na **Federação Internacional de Judô (IJF)**
- O conteúdo é **atualizado para 2025**
- A página é **educativa** e não substitui o conhecimento oficial
- **Sempre consulte** as regras oficiais para competições
- **Design consistente** com o padrão visual do seu site

---

**Desenvolvido com ❤️ para a comunidade do judô, seguindo o padrão visual do seu site**
