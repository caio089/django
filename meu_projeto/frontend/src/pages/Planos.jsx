import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Check, ArrowLeft } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';

const ACCENT = 'rgb(59, 130, 246)';

const PLANOS = [
  {
    nome: 'Mensal',
    preco: 'R$ 29,90',
    popular: false,
    beneficios: ['Acesso completo', 'Todas as faixas', 'Quiz e conteúdo', 'Vídeos de técnicas'],
  },
  {
    nome: 'Anual',
    preco: 'R$ 249,90',
    popular: true,
    economize: '30%',
    beneficios: ['Tudo do mensal', '2 meses grátis', 'Conteúdo exclusivo', 'Suporte prioritário'],
  },
];

export default function Planos() {
  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <header className="fixed top-0 left-0 right-0 z-40 bg-black/40 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/index"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition-all"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-wider">料金 — Planos</span>
        </div>
      </header>

      <section className="pt-24 pb-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.span
            className="font-jp text-5xl sm:text-6xl font-bold block text-white/95 mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            道場
          </motion.span>
          <motion.h1
            className="text-3xl sm:text-4xl font-bold text-white mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            Escolha seu plano
          </motion.h1>
          <motion.p
            className="text-slate-400 text-lg"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            Libere todo o conteúdo da academia de judô
          </motion.p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 pb-24">
        <div className="grid md:grid-cols-2 gap-6">
          {PLANOS.map((plano, i) => (
            <motion.div
              key={plano.nome}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`relative rounded-2xl border p-8 ${
                plano.popular
                  ? 'border-blue-500/50 bg-white/[0.06] ring-1 ring-blue-500/30'
                  : 'border-white/10 bg-white/[0.03]'
              }`}
            >
              {plano.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full text-sm font-semibold text-white bg-blue-600">
                  Mais popular
                </span>
              )}
              <h3 className="text-xl font-bold text-white mb-2">{plano.nome}</h3>
              <p className="text-3xl font-bold text-white mb-1">
                {plano.preco}
                <span className="text-sm font-normal text-slate-400">/mês</span>
              </p>
              {plano.economize && (
                <p className="text-emerald-400 text-sm mb-6">{plano.economize} de economia</p>
              )}
              <ul className="space-y-3 mb-8">
                {plano.beneficios.map((b) => (
                  <li key={b} className="flex items-center gap-2 text-slate-300">
                    <Check className="w-5 h-5 text-emerald-400 shrink-0" /> {b}
                  </li>
                ))}
              </ul>
              <a href="/payments/planos/" className="block">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full py-4 rounded-xl font-semibold ${
                    plano.popular
                      ? 'text-white'
                      : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                  style={plano.popular ? { backgroundColor: ACCENT } : {}}
                >
                  Assinar
                </motion.button>
              </a>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
