import { useState, useCallback, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ChevronRight, XCircle } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { FAIXAS_SIMULADO, getQuestionsForFaixa, NOTA_MINIMA_APROVACAO } from '../data/simuladoData';

const TIPO_LABEL = {
  teoria: 'Teoria',
  tecnica: 'Projeção',
  imobilizacao: 'Imobilização',
  chave_braco: 'Chave de Braço',
  estrangulamento: 'Estrangulamento',
  atemi: 'Atemi',
  combinado: 'Combinado',
  contra_ataque: 'Contra-ataque',
};

const ACCENT = 'rgb(5, 150, 105)';

const CONFETTI_COLORS = ['#22c55e', '#34d399', '#10b981', '#fbbf24', '#ffffff', '#a7f3d0', '#6ee7b7'];

function ConfettiCelebration() {
  const particles = useMemo(
    () =>
      Array.from({ length: 80 }, (_, i) => ({
        left: Math.random() * 100,
        delay: Math.random() * 0.5,
        duration: 3 + Math.random() * 2,
        color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
      })),
    []
  );
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {particles.map((p, i) => (
        <motion.div
          key={i}
          className="absolute w-3 h-3 rounded-sm"
          style={{ left: `${p.left}%`, top: -20, backgroundColor: p.color }}
          initial={{ y: 0, rotate: 0, opacity: 1 }}
          animate={{ y: '100vh', rotate: 360 * 3, opacity: 0 }}
          transition={{ duration: p.duration, delay: p.delay, ease: 'easeIn' }}
        />
      ))}
    </div>
  );
}

export default function Simulados() {
  const [faixaSelecionada, setFaixaSelecionada] = useState(null);
  const [questoes, setQuestoes] = useState([]);
  const [notas, setNotas] = useState({});
  const [finalizado, setFinalizado] = useState(false);

  const handleSelecionarFaixa = useCallback((faixa) => {
    setFaixaSelecionada(faixa);
    const q = getQuestionsForFaixa(faixa.id);
    setQuestoes(q);
    setNotas(Object.fromEntries(q.map((qu) => [qu.id, ''])));
    setFinalizado(false);
  }, []);

  const handleVoltar = useCallback(() => {
    setFaixaSelecionada(null);
    setQuestoes([]);
    setNotas({});
    setFinalizado(false);
  }, []);

  const setNota = (id, valor) => {
    const n = parseFloat(String(valor).replace(',', '.')) || '';
    setNotas((prev) => ({ ...prev, [id]: n }));
  };

  const handleFinalizar = () => {
    const valores = Object.entries(notas)
      .map(([, v]) => (typeof v === 'number' ? v : parseFloat(String(v).replace(',', '.'))))
      .filter((n) => !Number.isNaN(n) && n >= 0 && n <= 10);
    if (valores.length !== questoes.length) return;
    setFinalizado(true);
  };

  const media = (() => {
    const valores = Object.entries(notas)
      .map(([, v]) => (typeof v === 'number' ? v : parseFloat(String(v).replace(',', '.'))))
      .filter((n) => !Number.isNaN(n) && n >= 0 && n <= 10);
    if (valores.length === 0) return null;
    return valores.reduce((a, b) => a + b, 0) / valores.length;
  })();

  const todasPreenchidas = questoes.length > 0 && questoes.every((q) => {
    const v = notas[q.id];
    const n = typeof v === 'number' ? v : parseFloat(String(v || '').replace(',', '.'));
    return !Number.isNaN(n) && n >= 0 && n <= 10;
  });

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <header className="fixed top-0 left-0 right-0 z-40">
        <div
          className="bg-black/50 backdrop-blur-xl border-b border-white/10"
          style={{ borderBottomColor: 'rgba(5,150,105,0.15)' }}
        >
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
            {faixaSelecionada ? (
              <button
                type="button"
                onClick={handleVoltar}
                className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all"
              >
                <ArrowLeft className="w-4 h-4" /> Voltar
              </button>
            ) : (
              <Link
                to="/index"
                className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all"
              >
                <ArrowLeft className="w-4 h-4" /> Voltar
              </Link>
            )}
            <span className="font-jp text-slate-500 text-sm tracking-wider">
              {faixaSelecionada ? `Simulado — ${faixaSelecionada.nome}` : 'Simulados de Graduação'}
            </span>
          </div>
        </div>
      </header>

      <main className="relative z-10 pt-20 pb-12 px-4 sm:px-6 max-w-4xl mx-auto">
        <AnimatePresence mode="wait">
          {!faixaSelecionada ? (
            <motion.div
              key="faixas"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-8"
            >
              <div className="text-center">
                <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2">Simulados de Graduação</h1>
                <p className="text-slate-400 text-lg">
                  Selecione a faixa para gerar um simulado de exame. O avaliador dará nota de 0 a 10 em cada questão.
                </p>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                {FAIXAS_SIMULADO.map((f, i) => (
                  <motion.button
                    key={f.id}
                    type="button"
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.06 }}
                    onClick={() => handleSelecionarFaixa(f)}
                    className={`rounded-2xl p-5 flex flex-col items-center justify-center text-white shadow-lg border border-white/20
                      bg-gradient-to-br ${f.cor} hover:opacity-95 hover:scale-[1.02] transition-all duration-200`}
                  >
                    <img
                      src={f.img}
                      alt={f.nome}
                      className="h-10 w-auto mb-2 drop-shadow object-contain"
                      onError={(e) => (e.target.style.display = 'none')}
                    />
                    <span className="font-bold text-sm text-center leading-tight">{f.nome}</span>
                    <ChevronRight className="w-5 h-5 mt-2 opacity-80" />
                  </motion.button>
                ))}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="simulado"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-6"
            >
              {!finalizado ? (
                <>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                    <p className="text-white font-medium">
                      Simulado — {faixaSelecionada.nome}
                    </p>
                    <p className="text-slate-400 text-sm mt-1">
                      Preencha a nota (0 a 10) de cada questão. O exame tem 3 fases: Teoria → Em pé → Chão.
                    </p>
                  </div>

                  {[1, 2, 3].map((faseNum) => {
                    const quests = questoes.filter((q) => q.fase === faseNum);
                    if (quests.length === 0) return null;
                    const titulos = {
                      1: 'Fase 1 — Teoria (10 perguntas)',
                      2: 'Fase 2 — Em pé (projeções, combinados, contra-ataques)',
                      3: 'Fase 3 — Chão (imobilização, chave, estrangulamento)',
                    };
                    return (
                      <div key={faseNum} className="space-y-4">
                        <h2 className="text-lg font-semibold text-white border-b border-white/20 pb-2" style={{ borderColor: 'rgba(5,150,105,0.4)' }}>
                          {titulos[faseNum]}
                        </h2>
                        {quests.map((q, i) => (
                          <motion.div
                            key={q.id}
                            initial={{ opacity: 0, x: -12 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="p-5 rounded-2xl border border-white/10 bg-white/[0.04] backdrop-blur-sm"
                            style={{ borderLeftWidth: '4px', borderLeftColor: 'rgba(5,150,105,0.5)' }}
                          >
                            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                              <div className="flex-1">
                                <span className="text-xs font-medium text-emerald-400/90 uppercase tracking-wider">
                                  {TIPO_LABEL[q.tipo] || q.tipo}
                                </span>
                                <p className="text-white mt-1 font-medium leading-relaxed">{q.pergunta}</p>
                              </div>
                              <div className="shrink-0 flex items-center gap-2">
                                <label htmlFor={`nota-${q.id}`} className="text-slate-400 text-sm">
                                  Nota:
                                </label>
                                <input
                                  id={`nota-${q.id}`}
                                  type="number"
                                  min={0}
                                  max={10}
                                  step={0.5}
                                  placeholder="0–10"
                                  value={notas[q.id] ?? ''}
                                  onChange={(e) => setNota(q.id, e.target.value)}
                                  className="w-20 px-3 py-2 rounded-xl bg-white/5 border border-white/20 text-white text-center
                                    focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50"
                                />
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    );
                  })}

                  <div className="flex justify-center pt-4">
                    <motion.button
                      type="button"
                      onClick={handleFinalizar}
                      disabled={!todasPreenchidas}
                      whileHover={todasPreenchidas ? { scale: 1.03 } : {}}
                      whileTap={todasPreenchidas ? { scale: 0.98 } : {}}
                      className={`px-8 py-4 rounded-2xl font-semibold text-lg transition-all ${
                        todasPreenchidas
                          ? 'bg-emerald-500/30 border-2 border-emerald-500/60 text-white hover:bg-emerald-500/40'
                          : 'bg-white/5 border border-white/10 text-slate-500 cursor-not-allowed'
                      }`}
                    >
                      Finalizar e ver resultado
                    </motion.button>
                  </div>
                </>
              ) : media >= NOTA_MINIMA_APROVACAO ? (
                /* ——— APROVADO ——— Tela de celebração especial */
                <motion.div
                  key="aprovado"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.6 }}
                  className="relative text-center max-w-2xl mx-auto overflow-visible"
                >
                  {/* Chuva de confetti */}
                  <ConfettiCelebration />
                  {/* Judoka em pose de vitória */}
                  <motion.div
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
                    className="relative w-40 h-40 mx-auto mb-6"
                  >
                    <motion.svg
                      viewBox="0 0 120 180"
                      className="w-full h-full drop-shadow-[0_0_30px_rgba(34,197,94,0.5)]"
                      animate={{ y: [0, -8, 0], rotate: [0, 2, -2, 0] }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                    >
                      <rect x="45" y="60" width="30" height="50" rx="4" fill="currentColor" className="text-emerald-900/90" />
                      <rect x="42" y="55" width="36" height="25" rx="3" fill="currentColor" className="text-emerald-800/90" />
                      <circle cx="60" cy="40" r="18" fill="currentColor" className="text-emerald-200/95" />
                      <circle cx="60" cy="38" r="14" fill="currentColor" className="text-emerald-100" />
                      <path d="M 35 50 Q 20 20 25 5" stroke="currentColor" strokeWidth="6" fill="none" strokeLinecap="round" className="text-emerald-800/90" />
                      <path d="M 85 50 Q 100 20 95 5" stroke="currentColor" strokeWidth="6" fill="none" strokeLinecap="round" className="text-emerald-800/90" />
                      <rect x="48" y="108" width="14" height="55" rx="3" fill="currentColor" className="text-emerald-900/90" />
                      <rect x="58" y="108" width="14" height="55" rx="3" fill="currentColor" className="text-emerald-900/90" />
                      <rect x="42" y="75" width="36" height="8" rx="2" fill="#22c55e" />
                    </motion.svg>
                    <motion.div
                      className="absolute -inset-4 rounded-full border-4 border-emerald-400/50"
                      animate={{ scale: [1, 1.3, 1], opacity: [0.6, 0, 0.6] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    />
                  </motion.div>
                  <motion.div initial={{ scale: 0, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.3, type: 'spring', stiffness: 200, damping: 15 }} className="relative z-10">
                    {/* Emojis flutuantes — celebrando a conquista */}
                    <div className="flex justify-center gap-6 mb-3">
                      {['🎉', '🏆', '⭐'].map((emoji, i) => (
                        <motion.span
                          key={emoji}
                          className="text-4xl sm:text-5xl"
                          initial={{ scale: 0, rotate: -20 }}
                          animate={{ scale: 1, rotate: 0, y: [0, -6, 0] }}
                          transition={{
                            scale: { delay: 0.2 + i * 0.1, type: 'spring', stiffness: 260, damping: 12 },
                            y: { duration: 1.2, repeat: Infinity, delay: i * 0.2, ease: 'easeInOut' },
                          }}
                          style={{ display: 'inline-block' }}
                        >
                          {emoji}
                        </motion.span>
                      ))}
                    </div>
                    {/* Selo vermelho 合格 — estilo hanko japonês */}
                    <motion.div
                      className="inline-flex items-center justify-center w-24 h-24 sm:w-28 sm:h-28 rounded-full border-4 border-red-600 bg-red-600/90 mx-auto mb-4"
                      initial={{ scale: 2, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ delay: 0.5, type: 'spring', stiffness: 400, damping: 15 }}
                      style={{ boxShadow: '0 0 0 4px rgba(185,28,28,0.3)' }}
                    >
                      <span className="font-jp text-3xl sm:text-4xl font-black text-white">合格</span>
                    </motion.div>
                    <motion.span
                      className="font-jp text-5xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 via-green-400 to-emerald-500 block mb-2"
                      style={{ textShadow: '0 0 60px rgba(34,197,94,0.5)' }}
                      animate={{ scale: [1, 1.08, 1] }}
                      transition={{ duration: 1, repeat: Infinity }}
                    >
                      祝！ 合格！
                    </motion.span>
                    <motion.h2
                      className="text-3xl sm:text-5xl font-black text-white mb-2 drop-shadow-[0_0_30px_rgba(34,197,94,0.6)]"
                      initial={{ y: 30, opacity: 0 }}
                      animate={{ y: 0, opacity: 1 }}
                      transition={{ delay: 0.4, duration: 0.6 }}
                    >
                      VOCÊ PASSOU!
                    </motion.h2>
                    <motion.p
                      className="text-xl sm:text-2xl text-emerald-300 font-bold mb-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.6 }}
                    >
                      Parabéns pelo simulado de {faixaSelecionada.nome}
                    </motion.p>
                    <motion.p
                      className="text-base text-emerald-400/90 font-medium mb-2"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.75 }}
                    >
                      Você merece! O seu esforço valeu a pena.
                    </motion.p>
                    <motion.p
                      className="text-2xl font-bold text-emerald-400 mb-4"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.8, type: 'spring', stiffness: 300 }}
                    >
                      Média: {media.toFixed(1)} / 10
                    </motion.p>
                    <motion.p
                      className="text-slate-400 text-sm italic max-w-md mx-auto mb-8"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1 }}
                    >
                      「努力は裏切らない」
                      <br />
                      <span className="text-slate-500 not-italic">O esforço nunca trai.</span>
                    </motion.p>
                  </motion.div>
                  <motion.button
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.2 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleVoltar}
                    className="relative z-10 px-8 py-4 rounded-2xl font-bold text-white text-lg border-2 border-emerald-500/60"
                    style={{ backgroundColor: 'rgba(34,197,94,0.3)', boxShadow: '0 0 40px rgba(34,197,94,0.3)' }}
                  >
                    Voltar ao início
                  </motion.button>
                </motion.div>
              ) : (
                /* ——— REPROVADO ——— */
                <motion.div
                  initial={{ opacity: 0, scale: 0.96 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="text-center py-12 px-6 rounded-3xl border-2 border-white/10 bg-white/[0.04] backdrop-blur-sm"
                  style={{ borderColor: 'rgba(239,68,68,0.5)' }}
                >
                  <XCircle className="w-20 h-20 mx-auto text-red-500 mb-4" />
                  <h2 className="text-2xl font-bold text-white mb-2">Reprovado</h2>
                  <p className="text-slate-400 text-lg mb-2">
                    Média: <span className="font-bold text-white">{media.toFixed(1)}</span> / 10
                  </p>
                  <p className="text-slate-500 text-sm mb-6">
                    Nota mínima para aprovação: {NOTA_MINIMA_APROVACAO}
                  </p>
                  <p className="text-slate-400 text-sm italic mb-6">「七転び八起き」 — Cair sete vezes, levantar oito.</p>
                  <button
                    type="button"
                    onClick={handleVoltar}
                    className="px-6 py-3 rounded-xl bg-white/10 border border-white/20 text-white hover:bg-white/15 transition-colors"
                  >
                    Voltar ao início
                  </button>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
