import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      // Apenas as rotas de API de quiz vão para o Django;
      // as páginas React em /quiz e /quiz/caminho ficam no frontend.
      '/quiz/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/static': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/admin': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      // Só encaminha ao Django as rotas de API/checkout; /payments, /payments/planos e /payments/plano/:id ficam no React
      '/payments/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/criar-pagamento': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/gerar-pix': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/criar-pagamento-cartao': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      // /payments/checkout NÃO é proxy: fica no React para redirecionar direto ao Mercado Pago
      '/payments/verificar-status': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/sucesso': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/falha': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/pendente': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/bem-vindo': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/assinaturas': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/cancelar-assinatura': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/payments/webhook': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
})
