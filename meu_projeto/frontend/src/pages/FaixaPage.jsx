import { useParams, Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowLeft, ChevronUp, Target, Zap } from 'lucide-react';
import { useState } from 'react';
import DojoBackground from '../components/DojoBackground';
import { FAIXA_DATA } from '../data/faixaData';

// Cor RGB de destaque por faixa (para o DojoBackground)
const BELT_ACCENT = {
  1: 'rgb(107, 114, 128)',  // cinza
  2: 'rgb(37, 99, 235)',    // azul
  3: 'rgb(245, 158, 11)',   // amarelo
  4: 'rgb(234, 88, 12)',    // laranja
  5: 'rgb(5, 150, 105)',    // verde
  6: 'rgb(124, 58, 237)',   // roxo
  7: 'rgb(146, 64, 14)',    // marrom
};

const QUOTES = [
  '「柔よく剛を制す」 — O suave domina o rígido',
  '「精力善用」 — Máxima eficiência',
  '「自他共栄」 — Prosperidade mútua',
  '「形を正し、心を鍛え、技を磨く」 — Corrija a forma, tempere a mente',
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.06, delayChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0 },
};

function VideoCard({ v, beltColor }) {
  const src = `https://www.youtube.com/embed/${v.id}?rel=0`;

  return (
    <motion.div variants={item} className="group">
      <div
        className="relative overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.03] backdrop-blur-sm transition-shadow duration-200"
        style={{ borderLeftWidth: '3px', borderLeftColor: beltColor }}
      >
        <div className="p-6 sm:p-7">
          <div className="flex items-start gap-4 mb-4">
            <div
              className="w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 border"
              style={{ borderColor: `${beltColor}60`, backgroundColor: `${beltColor}15` }}
            >
              <span className="text-2xl">🥋</span>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-xl font-bold text-white tracking-tight">{v.titulo}</h3>
              <p className="text-slate-500 text-sm mt-1 font-medium">{v.desc}</p>
            </div>
          </div>

          <div className="relative aspect-video rounded-xl overflow-hidden bg-black/80 ring-1 ring-white/10">
            <iframe
              src={src}
              title={v.titulo}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
              className="absolute inset-0 w-full h-full"
            />
          </div>

          {v.dica && (
            <div className="mt-4 p-4 rounded-xl bg-amber-500/5 border border-amber-500/20">
              <h4 className="text-amber-400/90 font-semibold text-sm flex items-center gap-2 mb-1.5 font-jp">
                <span className="font-sans">💡</span> ポイント — Dica
              </h4>
              <p className="text-slate-400 text-sm leading-relaxed">{v.dica}</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export default function FaixaPage() {
  const { id } = useParams();
  const data = FAIXA_DATA[Number(id)] || FAIXA_DATA[1];
  const [activeSection, setActiveSection] = useState('nage-waza');
  const accentRgb = BELT_ACCENT[Number(id)] || BELT_ACCENT[1];
  const quote = QUOTES[(Number(id) || 1) % QUOTES.length];

  const { scrollYProgress } = useScroll();
  const headerOpacity = useTransform(scrollYProgress, [0, 0.12], [1, 0.92]);
  const heroY = useTransform(scrollYProgress, [0, 0.3], [0, 80]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.25], [1, 0.4]);

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={accentRgb} />

      {/* Header fixo */}
      <motion.header
        style={{ opacity: headerOpacity }}
        className="fixed top-0 left-0 right-0 z-50"
      >
        <div
          className="bg-black/40 backdrop-blur-xl border-b"
          style={{ borderBottomColor: `${accentRgb}40` }}
        >
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link
              to="/index"
              className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition-all duration-300"
            >
              <ArrowLeft className="w-4 h-4" /> Voltar
            </Link>
            <span className="font-jp text-slate-500 text-sm tracking-wider">柔道 — JUDÔ</span>
            <h1 className="text-base font-bold truncate max-w-[140px]" style={{ color: accentRgb }}>
              {data.nome}
            </h1>
          </div>
        </div>
      </motion.header>

      <div className="pt-14">
        {/* Hero — essência do dojo */}
        <motion.section
          style={{ y: heroY, opacity: heroOpacity }}
          className="relative overflow-hidden pt-20 pb-24 sm:pt-28 sm:pb-32 px-4"
        >
          <div
            className="absolute inset-0"
            style={{
              background: `linear-gradient(to bottom, ${accentRgb}15 0%, transparent 40%), linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, transparent 100%)`,
            }}
          />
          <div className="relative max-w-4xl mx-auto text-center">
            <motion.span
              className="font-jp text-5xl sm:text-6xl font-bold block mb-4 text-white/90"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              柔道
            </motion.span>
            <motion.h1
              className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white mb-4 tracking-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
            >
              {data.nome}
            </motion.h1>
            <motion.p
              className="text-slate-400 text-lg sm:text-xl max-w-xl mx-auto mb-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              {data.subtitulo}
            </motion.p>
            <motion.p
              className="text-slate-500/90 text-sm sm:text-base italic max-w-2xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
            >
              {quote}
            </motion.p>
            {/* Linha decorativa — faixa */}
            <motion.div
              className="mt-10 h-1 rounded-full max-w-[200px] mx-auto"
              style={{ background: `linear-gradient(90deg, transparent, ${accentRgb}, transparent)` }}
              initial={{ scaleX: 0, opacity: 0 }}
              animate={{ scaleX: 1, opacity: 1 }}
              transition={{ delay: 1, duration: 0.8 }}
            />
          </div>
        </motion.section>

        <div className="max-w-4xl mx-auto px-4 pb-24 space-y-20">
          {/* Condições */}
          <motion.section
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h2 className="text-xl font-bold flex items-center justify-center gap-2 mb-6" style={{ color: `${accentRgb}` }}>
              <Target className="w-5 h-5 opacity-90" />
              <span className="font-jp tracking-wide">条件</span> — Condições
            </h2>
            <motion.div
              variants={container}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true }}
              className="flex flex-wrap justify-center gap-3"
            >
              {data.condicoes.map((c, i) => (
                <motion.div
                  key={i}
                  variants={item}
                  className="px-5 py-3 rounded-xl bg-white/[0.04] border text-slate-300 font-medium
                    hover:bg-white/[0.06] transition-all duration-300"
                  style={{ borderColor: `${accentRgb}40` }}
                >
                  {c}
                </motion.div>
              ))}
            </motion.div>
          </motion.section>

          {/* Habilidades */}
          <motion.section
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h2 className="text-xl font-bold flex items-center justify-center gap-2 mb-6" style={{ color: `${accentRgb}` }}>
              <Zap className="w-5 h-5 opacity-90" />
              <span className="font-jp tracking-wide">技能</span> — Habilidades
            </h2>
            <motion.div
              variants={container}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true }}
              className="grid sm:grid-cols-2 gap-3 max-w-2xl mx-auto"
            >
              {data.habilidades.map((h, i) => (
                <motion.div
                  key={i}
                  variants={item}
                  className="px-4 py-3.5 rounded-xl bg-white/[0.03] border text-slate-400 text-sm text-left
                    hover:bg-white/[0.05] transition-all duration-300"
                  style={{ borderColor: `${accentRgb}25`, borderLeftWidth: '3px', borderLeftColor: accentRgb }}
                >
                  {h}
                </motion.div>
              ))}
            </motion.div>
          </motion.section>

          {/* Navegação de Seções */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="flex flex-wrap justify-center gap-2"
          >
            {data.secoes.map((sec) => (
              <motion.button
                key={sec.id}
                onClick={() => setActiveSection(sec.id)}
                className="px-5 py-3 rounded-xl font-semibold text-sm transition-all duration-300"
                style={
                  activeSection === sec.id
                    ? { backgroundColor: accentRgb, color: '#0f172a', boxShadow: `0 10px 25px -5px ${accentRgb}50` }
                    : {
                        backgroundColor: 'rgba(255,255,255,0.05)',
                        color: 'rgb(148, 163, 184)',
                        borderColor: `${accentRgb}30`,
                        borderWidth: '1px',
                      }
                }
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {sec.titulo}
              </motion.button>
            ))}
          </motion.div>

          {/* Seções de Vídeos */}
          {data.secoes.map((sec) =>
            activeSection === sec.id ? (
              <motion.section
                key={sec.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                <h2 className="text-2xl font-bold mb-10 text-center font-jp tracking-wide" style={{ color: accentRgb }}>
                  {sec.titulo}
                </h2>
                <motion.div
                  variants={container}
                  initial="hidden"
                  animate="show"
                  className="grid gap-10"
                >
                  {sec.videos.map((v, i) => (
                    <VideoCard
                      key={`${sec.id}-${v.titulo}-${i}`}
                      v={v}
                      beltColor={accentRgb}
                    />
                  ))}
                </motion.div>
              </motion.section>
            ) : null
          )}
        </div>

        {/* Botão Voltar ao Topo */}
        <motion.button
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: false }}
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="fixed bottom-8 right-8 w-12 h-12 rounded-full backdrop-blur-md flex items-center justify-center shadow-xl z-40 transition-all duration-300 hover:scale-105"
          style={{
            backgroundColor: `${accentRgb}20`,
            borderColor: `${accentRgb}50`,
            borderWidth: '1px',
            color: accentRgb,
          }}
        >
          <ChevronUp className="w-5 h-5" />
        </motion.button>
      </div>
    </div>
  );
}
