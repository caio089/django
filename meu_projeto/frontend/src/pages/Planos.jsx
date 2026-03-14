import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import AnimatedBackground from '../components/AnimatedBackground';

const PLANOS = [
  { nome: 'Mensal', preco: 'R$ 29,90', popular: false, beneficios: ['Acesso completo', 'Todas as faixas', 'Quiz e conteúdo'] },
  { nome: 'Anual', preco: 'R$ 249,90', popular: true, economize: '30%', beneficios: ['Tudo do mensal', '2 meses grátis', 'Conteúdo exclusivo'] },
];

export default function Planos() {
  return (
    <div className="min-h-screen py-20 relative">
      <AnimatedBackground />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 max-w-4xl mx-auto px-4"
      >
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4 font-display">Escolha seu plano</h1>
          <p className="text-slate-400">Libere todo o conteúdo da academia de judô</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {PLANOS.map((plano, i) => (
            <motion.div
              key={plano.nome}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`relative rounded-3xl p-8 glass ${
                plano.popular ? 'ring-2 ring-blue-500 scale-105' : ''
              }`}
            >
              {plano.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-blue-600 text-white text-sm font-semibold">
                  Mais popular
                </span>
              )}
              <h3 className="text-xl font-bold text-white mb-2">{plano.nome}</h3>
              <p className="text-3xl font-bold text-white mb-1">{plano.preco}<span className="text-sm font-normal text-slate-400">/mês</span></p>
              {plano.economize && <p className="text-green-400 text-sm mb-6">{plano.economize} de economia</p>}
              <ul className="space-y-3 mb-8">
                {plano.beneficios.map((b) => (
                  <li key={b} className="flex items-center gap-2 text-slate-300">
                    <Check className="w-5 h-5 text-green-400 flex-shrink-0" /> {b}
                  </li>
                ))}
              </ul>
              <a href="/payments/planos/">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full py-4 rounded-xl font-semibold ${
                    plano.popular
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white'
                      : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                >
                  Assinar
                </motion.button>
              </a>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
