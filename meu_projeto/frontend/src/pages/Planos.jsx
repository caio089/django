import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Check,
  ArrowLeft,
  Shield,
  Lock,
  Zap,
  CreditCard,
  BadgeCheck,
  Sparkles,
} from 'lucide-react';
import DojoBackground from '../components/DojoBackground';

const ACCENT = 'rgb(180, 50, 55)';
const GOLD = 'rgb(212, 175, 55)';

// planoId = ID do PlanoPremium no backend (Django). Mensal=1/30d, Trimestral=2/90d, Semestral=3/180d.
const PLANOS = [
  {
    nome: 'Mensal',
    preco: 'R$ 47,90',
    popular: false,
    planoId: 1,
    beneficios: [
      'Acesso completo ao conteúdo',
      'Todas as faixas e técnicas',
      'Quiz e vídeos de técnicas',
      'Suporte por e-mail',
    ],
  },
  {
    nome: 'Trimestral',
    preco: 'R$ 119,90',
    popular: true,
    economize: '3 meses',
    planoId: 2,
    beneficios: [
      'Tudo do plano mensal',
      'Melhor custo-benefício',
      'Conteúdo exclusivo',
      'Suporte prioritário',
    ],
  },
  {
    nome: 'Anual',
    preco: 'R$ 249,90',
    popular: false,
    economize: '30%',
    planoId: 3,
    beneficios: [
      'Tudo do plano mensal',
      '2 meses grátis',
      'Conteúdo exclusivo',
      'Suporte prioritário',
    ],
  },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0 },
};

export default function Planos() {
  return (
    <div className="min-h-screen relative font-display antialiased overflow-x-hidden">
      <DojoBackground accentColor={ACCENT} />

      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-black/60 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/payments"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-widest">
            料金 — Planos
          </span>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-32 pb-8 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <motion.span
            className="font-jp text-5xl sm:text-6xl font-bold block mb-4"
            style={{
              color: 'rgba(255,255,255,0.96)',
              textShadow: `0 0 50px ${ACCENT}50, 0 2px 20px rgba(0,0,0,0.3)`,
            }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            道場
          </motion.span>
          <motion.h1
            className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white mb-4"
            style={{ fontFamily: "'Orbitron', sans-serif" }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.06 }}
          >
            Escolha seu plano
          </motion.h1>
          <motion.p
            className="text-slate-400 text-lg max-w-xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.12 }}
          >
            Libere todo o conteúdo da academia de judô. Simples, rápido e seguro.
          </motion.p>
          {/* Linha decorativa */}
          <motion.div
            className="mt-8 h-px max-w-xs mx-auto rounded-full opacity-60"
            style={{
              background: `linear-gradient(90deg, transparent, ${ACCENT}, ${GOLD}, transparent)`,
            }}
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          />
        </div>
      </section>

      {/* Trust strip */}
      <motion.section
        className="max-w-2xl mx-auto px-4 pb-10"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
      >
        <div
          className="flex flex-wrap items-center justify-center gap-6 sm:gap-8 py-4 px-6 rounded-2xl border border-white/10 bg-white/[0.02]"
          style={{ boxShadow: `inset 0 1px 0 rgba(255,255,255,0.03)` }}
        >
          <span className="flex items-center gap-2 text-slate-400 text-sm">
            <Lock className="w-4 h-4 shrink-0" style={{ color: ACCENT }} />
            Criptografado
          </span>
          <span className="flex items-center gap-2 text-slate-400 text-sm">
            <Shield className="w-4 h-4 shrink-0" style={{ color: ACCENT }} />
            Ambiente seguro
          </span>
          <span className="flex items-center gap-2 text-slate-400 text-sm">
            <BadgeCheck className="w-4 h-4 shrink-0" style={{ color: ACCENT }} />
            Cancele quando quiser
          </span>
        </div>
      </motion.section>

      {/* Cards de planos */}
      <div className="max-w-5xl mx-auto px-4 pb-20">
        <motion.div
          className="grid md:grid-cols-3 gap-8"
          variants={container}
          initial="hidden"
          animate="show"
        >
          {PLANOS.map((plano) => (
            <Link
              key={plano.nome}
              to={`/payments/plano/${plano.planoId}`}
              className="block"
            >
              <motion.div
                variants={item}
                className={`relative rounded-3xl overflow-hidden transition-all duration-300 cursor-pointer hover:border-[rgb(180,50,55)]/40 hover:ring-2 hover:ring-[rgb(180,50,55)]/30 ${
                  plano.popular
                    ? 'ring-2 ring-[rgb(180,50,55)]/50 shadow-2xl'
                    : ''
                }`}
                style={{
                  background: plano.popular
                    ? 'linear-gradient(180deg, rgba(180,50,55,0.12) 0%, rgba(0,0,0,0.4) 100%)'
                    : 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  boxShadow: plano.popular
                    ? `0 25px 50px -12px rgba(0,0,0,0.5), 0 0 60px -15px ${ACCENT}40`
                    : '0 25px 50px -12px rgba(0,0,0,0.3)',
                }}
              >
                {/* Barra superior */}
                <div
                className="h-1.5 w-full"
                style={{
                  background: plano.popular
                    ? `linear-gradient(90deg, ${ACCENT}, ${GOLD})`
                    : 'rgba(255,255,255,0.06)',
                }}
              />
              <div className="p-8 sm:p-10">
                {plano.popular && (
                  <div
                    className="absolute top-6 right-6 flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold text-white"
                    style={{
                      backgroundColor: ACCENT,
                      boxShadow: `0 4px 14px ${ACCENT}50`,
                    }}
                  >
                    <Sparkles className="w-3.5 h-3.5" /> Mais popular
                  </div>
                )}
                <h3
                  className="text-xl font-bold text-white mb-1"
                  style={plano.popular ? { fontFamily: "'Orbitron', sans-serif" } : {}}
                >
                  {plano.nome}
                </h3>
                <div className="flex items-baseline gap-1 mb-2">
                  <span className="text-4xl sm:text-5xl font-black text-white tracking-tight">
                    {plano.preco}
                  </span>
                  <span className="text-slate-400 text-base font-medium">/mês</span>
                </div>
                {plano.economize && (
                  <p
                    className="inline-flex items-center text-sm font-semibold mb-6 px-2.5 py-1 rounded-lg"
                    style={{
                      color: GOLD,
                      backgroundColor: 'rgba(212, 175, 55, 0.15)',
                    }}
                  >
                    {plano.economize} de economia
                  </p>
                )}
                {!plano.economize && <div className="mb-6" />}
                <ul className="space-y-4 mb-10">
                  {plano.beneficios.map((b) => (
                    <li
                      key={b}
                      className="flex items-center gap-3 text-slate-300 text-sm sm:text-base"
                    >
                      <span
                        className="w-6 h-6 rounded-full flex items-center justify-center shrink-0"
                        style={{
                          backgroundColor: plano.popular ? `${GOLD}25` : `${ACCENT}20`,
                        }}
                      >
                        <Check
                          className="w-3.5 h-3.5"
                          style={{ color: plano.popular ? GOLD : ACCENT }}
                        />
                      </span>
                      {b}
                    </li>
                  ))}
                </ul>
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-4 rounded-2xl font-bold text-white text-base transition-all duration-200"
                  style={{
                    backgroundColor: plano.popular ? ACCENT : 'rgba(255,255,255,0.12)',
                    boxShadow: plano.popular ? `0 10px 30px ${ACCENT}40` : 'none',
                  }}
                >
                  Assinar com segurança
                </motion.button>
              </div>
              </motion.div>
            </Link>
          ))}
        </motion.div>
      </div>

      {/* Facilidade — 3 passos */}
      <section className="max-w-4xl mx-auto px-4 pb-16">
        <motion.div
          className="rounded-3xl border border-white/10 bg-white/[0.02] p-8 sm:p-12"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          style={{ boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.03)' }}
        >
          <div className="flex items-center justify-center gap-3 mb-10">
            <Zap className="w-6 h-6" style={{ color: GOLD }} />
            <h2
              className="text-xl font-bold text-white"
              style={{ fontFamily: "'Orbitron', sans-serif" }}
            >
              Simples e rápido
            </h2>
          </div>
          <div className="grid sm:grid-cols-3 gap-10 relative">
            {/* Linha conectora (desktop) */}
            <div
              className="hidden sm:block absolute top-8 left-1/4 right-1/4 h-px opacity-30"
              style={{
                background: `linear-gradient(90deg, transparent, ${ACCENT}, ${GOLD}, transparent)`,
              }}
            />
            {[
              { step: 1, title: 'Escolha o plano', desc: 'Mensal ou anual.' },
              { step: 2, title: 'Pague com segurança', desc: 'Cartão ou PIX.' },
              { step: 3, title: 'Aproveite o dojo', desc: 'Acesso imediato.' },
            ].map(({ step, title, desc }) => (
              <div key={step} className="text-center relative">
                <div
                  className="w-14 h-14 rounded-2xl mx-auto mb-5 flex items-center justify-center text-xl font-black text-white"
                  style={{
                    backgroundColor: ACCENT,
                    boxShadow: `0 8px 24px ${ACCENT}40`,
                  }}
                >
                  {step}
                </div>
                <h3 className="text-white font-semibold mb-1">{title}</h3>
                <p className="text-slate-400 text-sm">{desc}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Segurança — bloco final */}
      <section className="max-w-4xl mx-auto px-4 pb-28">
        <motion.div
          className="rounded-3xl border border-white/10 overflow-hidden flex flex-col sm:flex-row items-center justify-between gap-6 p-8 sm:p-10"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          style={{
            background: 'linear-gradient(135deg, rgba(180,50,55,0.08) 0%, rgba(255,255,255,0.02) 100%)',
            boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)',
          }}
        >
          <div className="flex items-center gap-5">
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center shrink-0"
              style={{
                backgroundColor: `${ACCENT}30`,
                boxShadow: `0 8px 24px ${ACCENT}30`,
              }}
            >
              <Shield className="w-8 h-8" style={{ color: ACCENT }} />
            </div>
            <div>
              <h2
                className="text-white font-bold text-lg mb-1"
                style={{ fontFamily: "'Orbitron', sans-serif" }}
              >
                Pagamento 100% seguro
              </h2>
              <p className="text-slate-400 text-sm">
                Dados criptografados. Ambiente protegido.{' '}
                <span className="font-jp text-white/90">安心</span>
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-slate-400 px-4 py-2 rounded-xl bg-white/5 border border-white/5">
            <CreditCard className="w-5 h-5" />
            <span className="text-sm font-medium">Cartão • PIX</span>
          </div>
        </motion.div>
      </section>
    </div>
  );
}
