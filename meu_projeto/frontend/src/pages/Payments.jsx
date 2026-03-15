import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  ArrowRight,
  Shield,
  Lock,
  Zap,
  CreditCard,
  BadgeCheck,
  ChevronRight,
} from 'lucide-react';
import DojoBackground from '../components/DojoBackground';

const ACCENT = 'rgb(180, 50, 55)';
const GOLD = 'rgb(212, 175, 55)';

export default function Payments() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-black/50 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/index"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition-all"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-widest">
            料金 — Pagamentos
          </span>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-28 pb-12 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <motion.span
            className="font-jp text-5xl sm:text-6xl font-bold block mb-3"
            style={{
              color: 'rgba(255,255,255,0.95)',
              textShadow: `0 0 40px ${ACCENT}40`,
            }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            道場
          </motion.span>
          <motion.h1
            className="text-3xl sm:text-4xl font-bold text-white mb-3"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.06 }}
          >
            Área de pagamentos
          </motion.h1>
          <motion.p
            className="text-slate-400 text-lg max-w-xl mx-auto mb-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.12 }}
          >
            Assinatura simples, segura e com a essência do dojo. Escolha seu plano e libere todo o conteúdo.
          </motion.p>

          {/* CTA principal */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Link to="/payments/planos" className="inline-block">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center gap-3 py-4 px-8 rounded-2xl font-semibold text-white shadow-lg"
                style={{
                  background: `linear-gradient(135deg, ${ACCENT}, rgb(140, 40, 45))`,
                  boxShadow: `0 10px 40px ${ACCENT}40`,
                }}
              >
                Ver planos e preços
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Trust strip */}
      <motion.section
        className="max-w-3xl mx-auto px-4 pb-12"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.28 }}
      >
        <div className="flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-slate-400 text-sm">
          <span className="flex items-center gap-2">
            <Lock className="w-4 h-4" style={{ color: ACCENT }} />
            Pagamento criptografado
          </span>
          <span className="flex items-center gap-2">
            <Shield className="w-4 h-4" style={{ color: ACCENT }} />
            Ambiente seguro
          </span>
          <span className="flex items-center gap-2">
            <BadgeCheck className="w-4 h-4" style={{ color: ACCENT }} />
            Cancele quando quiser
          </span>
        </div>
      </motion.section>

      {/* Blocos: Facilidade + Segurança */}
      <section className="max-w-4xl mx-auto px-4 pb-16 space-y-6">
        <motion.div
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 sm:p-8 flex flex-col sm:flex-row items-center gap-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div
            className="w-14 h-14 rounded-xl flex items-center justify-center shrink-0"
            style={{ backgroundColor: `${GOLD}20` }}
          >
            <Zap className="w-7 h-7" style={{ color: GOLD }} />
          </div>
          <div className="flex-1 text-center sm:text-left">
            <h2 className="text-white font-semibold text-lg mb-1">Simples e rápido</h2>
            <p className="text-slate-400 text-sm">
              Escolha o plano, pague com cartão ou PIX e tenha acesso imediato. Sem complicação.
            </p>
          </div>
          <ChevronRight className="w-5 h-5 text-slate-500 shrink-0 hidden sm:block" />
        </motion.div>

        <motion.div
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 sm:p-8 flex flex-col sm:flex-row items-center gap-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div
            className="w-14 h-14 rounded-xl flex items-center justify-center shrink-0"
            style={{ backgroundColor: `${ACCENT}25` }}
          >
            <Shield className="w-7 h-7" style={{ color: ACCENT }} />
          </div>
          <div className="flex-1 text-center sm:text-left">
            <h2 className="text-white font-semibold text-lg mb-1">100% seguro</h2>
            <p className="text-slate-400 text-sm">
              Dados protegidos e ambiente criptografado. <span className="font-jp text-white/80">安心</span>
            </p>
          </div>
          <CreditCard className="w-5 h-5 text-slate-500 shrink-0 hidden sm:block" />
        </motion.div>
      </section>

      {/* CTA secundário */}
      <section className="max-w-4xl mx-auto px-4 pb-24 text-center">
        <motion.p
          className="text-slate-400 text-sm mb-4"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          Cartão de crédito ou PIX. Cancele quando quiser.
        </motion.p>
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <button
            type="button"
            onClick={() => navigate('/payments/planos')}
            className="text-white/90 hover:text-white font-medium text-sm flex items-center gap-2 justify-center mx-auto"
          >
            Ver planos
            <ChevronRight className="w-4 h-4" />
          </button>
        </motion.div>
      </section>
    </div>
  );
}
