# Dojo Online - Frontend React

Frontend moderno do Dojo Online - Academia de Judô, desenvolvido com **React + Vite + Tailwind CSS**.

## Tecnologias

- **React 19** + Vite 8
- **Tailwind CSS 3** - estilização
- **Framer Motion** - animações fluidas
- **React Router** - navegação
- **Lucide React** - ícones
- **Typewriter Effect** (custom) - efeito de digitação

## Recursos de UX

- Efeito de digitação (typewriter) em títulos
- Glassmorphism nos cards
- Orbs flutuantes no background
- Animações de entrada (fade, slide)
- Sidebar com transição spring
- Scroll reveal em elementos
- Design responsivo

## Rodar o projeto

```bash
npm install
npm run dev
```

Acesse http://localhost:5173

## Build para produção

```bash
npm run build
```

Os arquivos serão gerados em `dist/`.

## Integração com Django

O frontend foi pensado para ser hospedado como SPA. Para integrar com o backend Django:

1. Configure o Django para servir o build estático em produção
2. Adicione um proxy para as APIs ou configure CORS
3. Use variáveis de ambiente para a URL base da API
