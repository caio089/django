import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowLeft, Sparkles } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import ScrollReveal from '../components/ScrollReveal';

const ACCENT = 'rgb(5, 150, 105)';

const UKEMIS = [
  { nome: 'Ushiro-ukemi', desc: 'Rolamento para trás', emoji: '🔄', video: '_g7rvsxTkz8', dica: 'Mantenha o queixo encostado no peito e bata as mãos no tatame.' },
  { nome: 'Zenpo-kaiten', desc: 'Rolamento para frente com giro', emoji: '🔄', video: 'kbiLot6laks', dica: 'Gire o corpo mantendo a linha reta e controle a queda.' },
  { nome: 'Mae-ukemi', desc: 'Rolamento para frente', emoji: '⬇️', video: 'veM5RFdjo0U', dica: 'Proteja a cabeça e role suavemente para frente.' },
  { nome: 'Yoko-ukemi', desc: 'Rolamento lateral', emoji: '↔️', video: 'JCwK1Ia4jsc', dica: 'Relaxe o corpo e role lateralmente, batendo o braço no tatame.' },
];

const CONDICOES = ['Qualquer nível de faixa', 'Idade mínima: 6 anos'];
const HABILIDADES = ['Ushiro-ukemi', 'Yoko-ukemi', 'Mae-ukemi', 'Zenpo-kaiten-ukemi'];

const QUOTE = '「受身は心」 — Ukemi é a base: quem cai bem, levanta mais forte.';

function UkemiCard({ u, index }) {
  const src = `https://www.youtube.com/embed/${u.video}?rel=0`;
  return (
    <motion.article
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.5, delay: index * 0.08 }}
      className="group relative rounded-2xl overflow-hidden border border-white/[0.06] bg-gradient-to-br from-white/[0.06] to-white/[0.02] backdrop-blur-sm transition-all duration-300 hover:border-emerald-500/30 hover:shadow-[0_0_40px_-8px_rgba(5,150,105,0.25)]"
      style={{ borderLeftWidth: '4px', borderLeftColor: 'rgba(5,150,105,0.5)' }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      <div className="relative p-5 sm:p-6">
        <div className="flex items-center gap-4 mb-4">
          <motion.div
            className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-lg shrink-0"
            style={{ backgroundColor: 'rgba(5,150,105,0.2)', border: '1px solid rgba(5,150,105,0.3)' }}
            whileHover={{ scale: 1.05, rotate: 5 }}
          >
            {u.emoji}
          </motion.div>
          <div>
            <h3 className="font-jp font-bold text-white text-lg tracking-tight">{u.nome}</h3>
            <p className="text-slate-400 text-sm mt-0.5">{u.desc}</p>
          </div>
        </div>
        <div className="relative aspect-video rounded-xl overflow-hidden bg-black/90 ring-1 ring-white/10 group-hover:ring-emerald-500/20 transition-all duration-300">
          <iframe src={src} title={u.nome} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen className="absolute inset-0 w-full h-full" />
        </div>
        {u.dica && (
          <div className="mt-4 p-4 rounded-xl bg-amber-500/5 border border-amber-500/20">
            <p className="text-amber-400/90 font-semibold text-sm font-jp mb-1 flex items-center gap-2">
              <Sparkles className="w-4 h-4" /> ポイント — Dica
            </p>
            <p className="text-slate-400 text-sm leading-relaxed">{u.dica}</p>
          </div>
        )}
      </div>
    </motion.article>
  );
}

export default function Ukemis() {
  const { scrollYProgress } = useScroll();
  const headerOpacity = useTransform(scrollYProgress, [0, 0.1], [1, 0.9]);

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <motion.header style={{ opacity: headerOpacity }} className="fixed top-0 left-0 right-0 z-40">
        <div className="bg-black/50 backdrop-blur-xl border-b border-white/10" style={{ borderBottomColor: 'rgba(5,150,105,0.15)' }}>
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link to="/index" className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200">
              <ArrowLeft className="w-4 h-4" /> Voltar
            </Link>
            <span className="font-jp text-slate-500 text-sm tracking-wider">受身 — Ukemi</span>
          </div>
        </div>
      </motion.header>

      <section className="relative pt-28 pb-16 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/10 via-transparent to-transparent pointer-events-none" />
        <div className="max-w-4xl mx-auto text-center relative">
          <motion.span
            className="font-jp text-6xl sm:text-7xl font-bold block text-white/95 mb-4 drop-shadow-lg"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            受身
          </motion.span>
          <motion.h1
            className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.12, duration: 0.5 }}
          >
            Rolamentos do Judô
          </motion.h1>
          <motion.p
            className="text-slate-400 text-lg sm:text-xl mb-6"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.25 }}
          >
            A base da segurança e evolução no tatame
          </motion.p>
          <motion.div
            className="h-1 rounded-full max-w-[180px] mx-auto mb-8"
            style={{ background: `linear-gradient(90deg, transparent, ${ACCENT}, transparent)` }}
            initial={{ scaleX: 0, opacity: 0 }}
            animate={{ scaleX: 1, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.7 }}
          />
          <motion.p
            className="text-slate-500 text-sm sm:text-base italic max-w-xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {QUOTE}
          </motion.p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 pb-24 space-y-12">
        <ScrollReveal direction="up">
          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 sm:p-6 backdrop-blur-sm">
            <h3 className="font-jp text-lg font-bold text-white mb-3 flex items-center gap-2" style={{ color: ACCENT }}>
              条件 — Condições
            </h3>
            <div className="flex flex-wrap gap-2">
              {CONDICOES.map((c) => (
                <span key={c} className="px-4 py-2.5 rounded-xl bg-white/5 text-slate-300 text-sm border border-white/5 hover:border-emerald-500/20 transition-colors">
                  {c}
                </span>
              ))}
            </div>
          </div>
        </ScrollReveal>

        <ScrollReveal direction="up">
          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 sm:p-6 backdrop-blur-sm">
            <h3 className="font-jp text-lg font-bold text-white mb-3 flex items-center gap-2" style={{ color: ACCENT }}>
              技能 — Habilidades
            </h3>
            <div className="flex flex-wrap gap-2">
              {HABILIDADES.map((h) => (
                <span key={h} className="px-4 py-2.5 rounded-xl bg-emerald-500/10 text-emerald-300/90 text-sm border border-emerald-500/20">
                  {h}
                </span>
              ))}
            </div>
          </div>
        </ScrollReveal>

        <section>
          <motion.h2
            className="font-jp text-2xl font-bold text-white mb-8"
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            style={{ color: ACCENT }}
          >
            基本の受身 — Rolamentos Fundamentais
          </motion.h2>
          <div className="grid gap-8 sm:grid-cols-2">
            {UKEMIS.map((u, i) => (
              <UkemiCard key={u.nome} u={u} index={i} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

