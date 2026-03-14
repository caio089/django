import { useState, useCallback, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Trophy, ChevronRight, Lightbulb, Check, X, Sparkles, Award, MapPin } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { getQuestionsForLevel, XP_POR_ACERTO, CATEGORIAS_NIVEL, MAX_NIVEL } from '../data/quizData';
import { getQuizRanking, submitQuizResult, apiMe } from '../api';

const STORAGE_NICKNAME = 'quiz_ranking_nickname';
const STORAGE_CIDADE = 'quiz_ranking_cidade';
const STORAGE_DOJO = 'quiz_ranking_dojo';

const ACCENT = 'rgb(59, 130, 246)';
const CORRECT_COLOR = 'rgb(34, 197, 94)';
const WRONG_COLOR = 'rgb(239, 68, 68)';

const RANKING_MODE = { id: 'ranking', label: 'Quiz Ranking', desc: 'Níveis 1–3: 7 perguntas · Níveis 4–6: 10 perguntas — suba até Sensei', emoji: '🏆', color: 'rgb(234, 179, 8)', glow: 'rgba(234,179,8,0.4)' };

const LETTERS = ['A', 'B', 'C', 'D'];

function ConfettiBurst({ active }) {
  if (!active) return null;
  const particles = Array.from({ length: 24 }, (_, i) => ({
    id: i,
    angle: (i / 24) * 360,
    color: ['#22c55e', '#34d399', '#86efac', '#4ade80'][i % 4],
    delay: Math.random() * 0.1,
  }));
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden rounded-2xl">
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute left-1/2 top-1/2 w-2 h-2 rounded-full"
          style={{ backgroundColor: p.color }}
          initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
          animate={{
            x: Math.cos((p.angle * Math.PI) / 180) * 120,
            y: Math.sin((p.angle * Math.PI) / 180) * 120,
            opacity: 0,
            scale: 0,
          }}
          transition={{ duration: 0.6, delay: p.delay, ease: 'easeOut' }}
        />
      ))}
    </div>
  );
}

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.15 } } };
const item = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0 } };

export default function Quiz() {
  const [phase, setPhase] = useState('select');
  const [difficulty, setDifficulty] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  // Modo ranking
  const [isRankingMode, setIsRankingMode] = useState(false);
  const [nivelAtual, setNivelAtual] = useState(1);
  const [xpNivel, setXpNivel] = useState(0);
  const [nickname, setNickname] = useState('');
  const [dojo, setDojo] = useState('');
  const [cidade, setCidade] = useState('');
  const [ranking, setRanking] = useState([]);
  const [loadingRanking, setLoadingRanking] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [lastSubmitResult, setLastSubmitResult] = useState(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted || typeof window === 'undefined') return;
    setNickname(localStorage.getItem(STORAGE_NICKNAME) || '');
    setDojo(localStorage.getItem(STORAGE_DOJO) || '');
    setCidade(localStorage.getItem(STORAGE_CIDADE) || '');
  }, [mounted]);

  const loadRanking = useCallback(async () => {
    setLoadingRanking(true);
    try {
      const { ranking: r } = await getQuizRanking();
      setRanking(r || []);
    } catch {
      setRanking([]);
    } finally {
      setLoadingRanking(false);
    }
  }, []);

  useEffect(() => {
    if (phase === 'select') loadRanking();
  }, [phase, loadRanking]);

  useEffect(() => {
    if (phase === 'nickname') {
      if (typeof window !== 'undefined' && localStorage.getItem(STORAGE_NICKNAME)) {
        setNickname(localStorage.getItem(STORAGE_NICKNAME) || '');
        setDojo(localStorage.getItem(STORAGE_DOJO) || '');
        setCidade(localStorage.getItem(STORAGE_CIDADE) || '');
      } else {
        apiMe().then((r) => {
          if (r?.user?.nome) setNickname(r.user.nome);
        }).catch(() => {});
      }
    }
  }, [phase]);

  const hasDadosRanking = useCallback(() => {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem(STORAGE_NICKNAME);
  }, []);

  const startQuiz = useCallback(() => {
    setDifficulty('ranking');
    if (hasDadosRanking()) {
      setNickname(localStorage.getItem(STORAGE_NICKNAME) || '');
      setDojo(localStorage.getItem(STORAGE_DOJO) || '');
      setCidade(localStorage.getItem(STORAGE_CIDADE) || '');
      startRankingQuizFromStorage();
    } else {
      setPhase('nickname');
    }
  }, [hasDadosRanking, startRankingQuizFromStorage]);

  const startRankingQuizFromStorage = useCallback(async () => {
    const nome = (typeof window !== 'undefined' ? localStorage.getItem(STORAGE_NICKNAME) : null) || (nickname || '').trim() || 'Anônimo';
    const d = (typeof window !== 'undefined' ? localStorage.getItem(STORAGE_DOJO) : null) || (dojo || '').trim();
    const cid = (typeof window !== 'undefined' ? localStorage.getItem(STORAGE_CIDADE) : null) || (cidade || '').trim();
    try {
      await submitQuizResult({ nickname: nome, dojo: d, cidade: cid, nivel_quiz: 1, xp_ganho: 0, passou_nivel: false, acertos: 0 });
    } catch {}
    setIsRankingMode(true);
    setNivelAtual(1);
    setXpNivel(0);
    setDifficulty('ranking');
    setQuestions(getQuestionsForLevel(1));
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setAnswered(false);
    setLastSubmitResult(null);
    setPhase('quiz');
  }, [nickname, dojo, cidade]);

  const startRankingQuiz = useCallback(() => {
    const nome = (nickname || '').trim() || 'Anônimo';
    const d = (dojo || '').trim();
    const cid = (cidade || '').trim();
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_NICKNAME, nome);
      localStorage.setItem(STORAGE_DOJO, d);
      localStorage.setItem(STORAGE_CIDADE, cid);
    }
    submitQuizResult({ nickname: nome, dojo: d, cidade: cid, nivel_quiz: 1, xp_ganho: 0, passou_nivel: false, acertos: 0 })
      .catch(() => {});
    setIsRankingMode(true);
    setNivelAtual(1);
    setXpNivel(0);
    setDifficulty('ranking');
    setQuestions(getQuestionsForLevel(1));
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setAnswered(false);
    setLastSubmitResult(null);
    setPhase('quiz');
  }, [nickname, dojo, cidade]);

  const submitAndGoResult = useCallback(async (passou) => {
    const nome = (nickname || '').trim() || 'Anônimo';
    const d = (dojo || '').trim();
    const cid = (cidade || '').trim();
    setSubmitting(true);
    try {
      const res = await submitQuizResult({
        nickname: nome,
        dojo: d,
        cidade: cid,
        nivel_quiz: nivelAtual,
        xp_ganho: xpNivel,
        passou_nivel: passou,
        acertos: score,
      });
      setLastSubmitResult(res);
      await loadRanking();
      if (passou && nivelAtual < MAX_NIVEL) {
        setPhase('levelUp');
      } else {
        setPhase('result');
      }
    } catch {
      setPhase('result');
    } finally {
      setSubmitting(false);
    }
  }, [nickname, dojo, cidade, nivelAtual, xpNivel, score, loadRanking]);

  const handleAnswer = useCallback((idx) => {
    if (answered) return;
    setSelected(idx);
    setAnswered(true);
    const q = questions[current];
    if (idx === q.correct) {
      setScore((s) => s + 1);
      if (isRankingMode) setXpNivel((x) => x + XP_POR_ACERTO);
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 700);
    } else if (isRankingMode) {
      submitAndGoResult(false);
    }
  }, [answered, questions, current, isRankingMode, submitAndGoResult]);

  const nextQuestion = useCallback(() => {
    const totalNivel = questions.length;
    if (isRankingMode && totalNivel > 0) {
      const completedLevel = current + 1 >= totalNivel;
      if (completedLevel && score === totalNivel) {
        submitAndGoResult(true);
        return;
      }
      if (completedLevel) {
        submitAndGoResult(false);
        return;
      }
    }
    if (current + 1 >= questions.length) {
      setPhase('result');
    } else {
      setCurrent((c) => c + 1);
      setSelected(null);
      setAnswered(false);
    }
  }, [current, questions.length, score, isRankingMode, submitAndGoResult]);

  const goNextLevel = useCallback(() => {
    const next = Math.min(MAX_NIVEL, nivelAtual + 1);
    setNivelAtual(next);
    setQuestions(getQuestionsForLevel(next));
    setCurrent(0);
    setScore(0);
    setXpNivel(0);
    setSelected(null);
    setAnswered(false);
    setPhase('quiz');
  }, [nivelAtual]);

  const restart = useCallback(() => {
    setPhase('select');
    setDifficulty(null);
    setQuestions([]);
    setIsRankingMode(false);
    setLastSubmitResult(null);
  }, []);

  const q = questions[current];
  const total = questions.length;
  const progress = total ? ((current + (answered ? 1 : 0)) / total) * 100 : 0;

  if (!mounted) {
    return (
      <div className="min-h-screen bg-[#0a0c0f] flex flex-col items-center justify-center">
        <div className="text-white/80 font-jp text-lg">読み込み中...</div>
        <div className="text-slate-500 text-sm mt-2">Carregando Quiz</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative font-display antialiased overflow-x-hidden bg-[#0a0c0f]">
      <DojoBackground accentColor={ACCENT} />
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="absolute top-1/2 -left-32 w-64 h-64 rounded-full bg-indigo-500/5 blur-3xl" />
      </div>

      <header className="fixed top-0 left-0 right-0 z-40 bg-black/60 backdrop-blur-xl border-b-2" style={{ borderBottomColor: `${ACCENT}30`, boxShadow: `0 4px 24px -8px ${ACCENT}30` }}>
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/index"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-wider">クイズ — Quiz</span>
        </div>
      </header>

      <main className="relative z-10 pt-20 pb-16 px-4 min-h-screen flex flex-col items-center justify-center">
        <div className="w-full max-w-4xl text-white">

          {/* ——— SELECÇÃO ——— */}
          <AnimatePresence mode="wait">
            {phase === 'select' && (
              <motion.section
                key="select"
                initial={{ opacity: 1 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, scale: 0.96, y: -20 }}
                transition={{ duration: 0.4 }}
                className="text-center max-w-4xl mx-auto"
              >
                <motion.span
                  className="font-jp text-6xl sm:text-7xl font-bold block text-white/95 mb-4 drop-shadow-[0_0_30px_rgba(59,130,246,0.3)]"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1, duration: 0.5 }}
                >
                  試合
                </motion.span>
                <motion.h1
                  className="text-3xl sm:text-4xl font-bold text-white mb-3 tracking-tight"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.18, duration: 0.5 }}
                >
                  Quiz — Teoria do Judô
                </motion.h1>
                <motion.p
                  className="text-slate-400 text-lg mb-6 max-w-lg mx-auto"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  Níveis 1–3: 7 perguntas · Níveis 4–6: 10 perguntas. Acerte todas seguidas para subir.
                </motion.p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-10">
                  <motion.button
                    variants={item}
                    initial="hidden"
                    animate="show"
                    whileHover={{ y: -6, scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={startQuiz}
                    className="py-5 px-10 rounded-2xl font-bold text-white text-lg flex items-center justify-center gap-3"
                    style={{ backgroundColor: RANKING_MODE.color, boxShadow: `0 8px 28px -4px ${RANKING_MODE.glow}` }}
                  >
                    <Trophy className="w-6 h-6" /> Jogar
                  </motion.button>
                  {hasDadosRanking() && (
                    <motion.button
                      variants={item}
                      initial="hidden"
                      animate="show"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setPhase('nickname')}
                      className="py-3 px-6 rounded-xl text-slate-400 hover:text-white text-sm font-medium border border-white/10 hover:border-white/20"
                    >
                      Alterar nome / dojo
                    </motion.button>
                  )}
                </div>
                <motion.div variants={container} initial="hidden" animate="show" className="w-full max-w-3xl mx-auto">
                  <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                    <Award className="w-5 h-5 text-amber-400" /> Ranking
                  </h3>
                  <div className="rounded-2xl border-2 border-white/10 bg-white/[0.04] overflow-hidden max-h-80 overflow-y-auto">
                    {loadingRanking ? (
                      <div className="p-6 text-slate-400 text-center">Carregando ranking...</div>
                    ) : ranking.length === 0 ? (
                      <div className="p-6 text-slate-500 text-center">Nenhum resultado no ranking ainda. Seja o primeiro!</div>
                    ) : (
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-white/10 text-slate-400">
                            <th className="py-3 px-3 text-left font-medium">#</th>
                            <th className="py-3 px-3 text-left font-medium">Nome</th>
                            <th className="py-3 px-3 text-left font-medium hidden sm:table-cell">Dojo</th>
                            <th className="py-3 px-3 text-left font-medium hidden md:table-cell">Cidade</th>
                            <th className="py-3 px-3 text-right font-medium">XP</th>
                            <th className="py-3 px-3 text-center font-medium">Nível</th>
                          </tr>
                        </thead>
                        <tbody>
                          {ranking.slice(0, 25).map((e) => (
                            <tr key={e.posicao} className="border-b border-white/5 hover:bg-white/5">
                              <td className="py-2.5 px-3 font-medium text-slate-300">{e.posicao}</td>
                              <td className="py-2.5 px-3 text-white font-medium">{e.nome}</td>
                              <td className="py-2.5 px-3 text-slate-400 hidden sm:table-cell">{e.dojo || '—'}</td>
                              <td className="py-2.5 px-3 text-slate-400 hidden md:table-cell">{e.cidade || '—'}</td>
                              <td className="py-2.5 px-3 text-right text-amber-400 font-semibold">{e.xp_total}</td>
                              <td className="py-2.5 px-3 text-center">
                                <span className="px-2 py-0.5 rounded-lg bg-white/10 text-slate-300 text-xs">{e.nivel_quiz} · {e.categoria_titulo}</span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </motion.div>
              </motion.section>
            )}

            {/* ——— NICKNAME (Modo Ranking) ——— */}
            {phase === 'nickname' && (
              <motion.section
                key="nickname"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="max-w-md mx-auto"
              >
                <h2 className="text-xl font-bold text-white mb-2">Seus dados no ranking</h2>
                <p className="text-slate-400 text-sm mb-6">Nome e dojo aparecem no ranking. Cidade é opcional.</p>
                <div className="space-y-4 mb-6">
                  <input
                    type="text"
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                    placeholder="Seu nome"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border-2 border-white/10 text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-0 transition-colors"
                  />
                  <input
                    type="text"
                    value={dojo}
                    onChange={(e) => setDojo(e.target.value)}
                    placeholder="Dojo onde treina"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border-2 border-white/10 text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-0 transition-colors"
                  />
                  <input
                    type="text"
                    value={cidade}
                    onChange={(e) => setCidade(e.target.value)}
                    placeholder="Cidade (opcional)"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border-2 border-white/10 text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-0 transition-colors"
                  />
                </div>
                <div className="flex gap-4">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={startRankingQuiz}
                    className="flex-1 py-4 rounded-2xl font-bold text-white flex items-center justify-center gap-2"
                    style={{ backgroundColor: RANKING_MODE.color, boxShadow: `0 8px 24px -4px ${RANKING_MODE.glow}` }}
                  >
                    <Trophy className="w-5 h-5" /> Jogar
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setPhase('select')}
                    className="py-4 px-6 rounded-2xl bg-white/10 text-white font-semibold hover:bg-white/20 border border-white/10"
                  >
                    Voltar
                  </motion.button>
                </div>
              </motion.section>
            )}

            {/* ——— SUBIU DE NÍVEL ——— */}
            {phase === 'levelUp' && (
              <motion.section
                key="levelUp"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                className="text-center max-w-lg mx-auto"
              >
                <motion.div
                  className="w-24 h-24 rounded-3xl flex items-center justify-center mx-auto mb-6 border-2 border-amber-400/50 bg-amber-500/20"
                  animate={{ scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] }}
                  transition={{ duration: 0.6, repeat: 1 }}
                >
                  <Award className="w-12 h-12 text-amber-400" />
                </motion.div>
                <h2 className="font-jp text-2xl sm:text-3xl font-bold text-white mb-2">Subiu de nível!</h2>
                <p className="text-amber-400/95 text-lg font-medium mb-2">
                  Próximo: Nível {nivelAtual + 1} — {CATEGORIAS_NIVEL[nivelAtual + 1] || 'Sensei'}
                </p>
                {lastSubmitResult && (
                  <p className="text-slate-400 text-sm mb-8">Total: {lastSubmitResult.xp_total} XP</p>
                )}
                <motion.button
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={goNextLevel}
                  className="py-4 px-8 rounded-2xl font-bold text-white"
                  style={{ backgroundColor: RANKING_MODE.color, boxShadow: `0 12px 32px -8px ${RANKING_MODE.glow}` }}
                >
                  Próximo nível →
                </motion.button>
              </motion.section>
            )}

            {/* ——— QUIZ ——— */}
            {phase === 'quiz' && total > 0 && q && (
              <motion.section
                key={`quiz-${current}`}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.35, ease: [0.25, 0.46, 0.45, 0.94] }}
                className="space-y-8 max-w-3xl mx-auto relative"
              >
                {/* Progresso elegante */}
                <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
                  <span className="text-slate-500 font-jp tracking-wide">Pergunta {current + 1} / {total}</span>
                  <div className="flex items-center gap-3">
                    {isRankingMode && (
                      <span className="text-amber-400 font-medium px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20">
                        Nível {nivelAtual} — {CATEGORIAS_NIVEL[nivelAtual]}
                      </span>
                    )}
                    <span className="text-emerald-400 font-semibold flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                      <Check className="w-4 h-4" /> {score} acertos
                      {isRankingMode && <span className="text-emerald-300/80">(+{xpNivel} XP)</span>}
                    </span>
                  </div>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden border border-white/5">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: `linear-gradient(90deg, ${ACCENT}, rgba(99,102,241,0.9))`, boxShadow: `0 0 12px ${ACCENT}60` }}
                    initial={false}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5, ease: 'easeOut' }}
                  />
                </div>

                {/* Card da pergunta */}
                <motion.div
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="relative rounded-3xl overflow-hidden border-2 border-white/10 bg-gradient-to-br from-white/[0.09] to-white/[0.02] backdrop-blur-sm p-8 sm:p-10"
                  style={{ boxShadow: '0 8px 32px -8px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08)' }}
                >
                  <ConfettiBurst active={showConfetti} />
                  <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
                  <h2 className="text-xl sm:text-2xl font-bold text-white leading-relaxed mb-8 relative">
                    {q.question}
                  </h2>
                  <div className="space-y-4">
                    {q.answers.map((ans, i) => {
                      const isCorrect = i === q.correct;
                      const isChosen = selected === i;
                      const isWrong = isChosen && !isCorrect;
                      const showAsCorrect = answered && isCorrect;
                      const showAsWrong = answered && isWrong;
                      return (
                        <motion.button
                          key={i}
                          type="button"
                          onClick={() => handleAnswer(i)}
                          disabled={answered}
                          initial={false}
                          animate={
                            showAsCorrect
                              ? { scale: [1, 1.02, 1], boxShadow: [`0 0 0 0 ${CORRECT_COLOR}00`, `0 0 32px 8px ${CORRECT_COLOR}50`, `0 0 0 0 ${CORRECT_COLOR}00`], transition: { duration: 0.5 } }
                              : showAsWrong
                                ? { x: [0, -8, 8, -6, 6, 0], transition: { duration: 0.5 } }
                                : {}
                          }
                          whileHover={!answered ? { scale: 1.01, x: 4 } : {}}
                          whileTap={!answered ? { scale: 0.995 } : {}}
                          className={`w-full text-left py-5 px-6 rounded-2xl border-2 flex items-center gap-4 transition-all duration-300 ${
                            showAsCorrect
                              ? 'bg-emerald-500/25 border-emerald-400 text-white shadow-[0_0_24px_-4px_rgba(34,197,94,0.4)]'
                              : showAsWrong
                                ? 'bg-red-500/20 border-red-400 text-white'
                                : answered
                                  ? 'border-white/5 bg-white/[0.02] text-slate-500 cursor-default'
                                  : 'border-white/10 bg-white/[0.04] text-white hover:border-white/30 hover:bg-white/[0.08]'
                          }`}
                        >
                          <span className="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg border-2" style={{
                            borderColor: showAsCorrect ? 'rgba(34,197,94,0.6)' : showAsWrong ? 'rgba(239,68,68,0.6)' : 'rgba(255,255,255,0.15)',
                            backgroundColor: showAsCorrect ? 'rgba(34,197,94,0.2)' : showAsWrong ? 'rgba(239,68,68,0.2)' : 'rgba(255,255,255,0.05)',
                          }}>
                            {LETTERS[i]}
                          </span>
                          <span className="font-medium text-base sm:text-lg flex-1">{ans}</span>
                          {showAsCorrect && (
                            <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 500, damping: 15 }} className="flex-shrink-0">
                              <Check className="w-7 h-7 text-emerald-400 drop-shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                            </motion.span>
                          )}
                          {showAsWrong && (
                            <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 400 }}>
                              <X className="w-7 h-7 text-red-400" />
                            </motion.span>
                          )}
                        </motion.button>
                      );
                    })}
                  </div>

                  {/* Explicação */}
                  <AnimatePresence>
                    {answered && (
                      <motion.div
                        initial={{ opacity: 0, height: 0, marginTop: 0 }}
                        animate={{ opacity: 1, height: 'auto', marginTop: 32 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.4, ease: 'easeOut' }}
                        className="overflow-hidden"
                      >
                        <motion.div
                          initial={{ opacity: 0, y: 16 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.15 }}
                          className="p-6 sm:p-7 rounded-2xl bg-gradient-to-br from-amber-500/15 to-amber-500/5 border-2 border-amber-500/30 flex gap-5"
                          style={{ boxShadow: '0 4px 24px -4px rgba(245,158,11,0.2), inset 0 1px 0 rgba(255,255,255,0.1)' }}
                        >
                          <div className="shrink-0 w-14 h-14 rounded-2xl bg-amber-500/25 flex items-center justify-center border border-amber-500/30">
                            <Lightbulb className="w-7 h-7 text-amber-400" />
                          </div>
                          <div>
                            <p className="text-amber-400/95 font-bold text-sm font-jp mb-2 flex items-center gap-2">
                              <Sparkles className="w-4 h-4" /> 解説 — Explicação
                            </p>
                            <p className="text-slate-300 text-base leading-relaxed">{q.explanation}</p>
                          </div>
                        </motion.div>
                        <motion.button
                          initial={{ opacity: 0, y: 12 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.25 }}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={nextQuestion}
                          disabled={submitting}
                          className="mt-6 w-full py-5 rounded-2xl font-bold text-white flex items-center justify-center gap-3 text-lg transition-all disabled:opacity-70"
                          style={{ backgroundColor: isRankingMode ? RANKING_MODE.color : ACCENT, boxShadow: `0 12px 32px -8px ${isRankingMode ? RANKING_MODE.glow : ACCENT}60` }}
                        >
                          {submitting ? 'Enviando...' : current + 1 >= total ? (isRankingMode ? 'Finalizar nível' : 'Ver resultado') : 'Próxima pergunta'}
                          {!submitting && <ChevronRight className="w-6 h-6" />}
                        </motion.button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              </motion.section>
            )}

            {/* ——— RESULTADO ——— */}
            {phase === 'result' && (
              <motion.section
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                transition={{ type: 'spring', damping: 20, stiffness: 280 }}
                className="text-center max-w-2xl mx-auto"
              >
                <motion.div
                  className="w-28 h-28 sm:w-32 sm:h-32 rounded-3xl flex items-center justify-center mx-auto mb-8 border-2"
                  style={{
                    backgroundColor: isRankingMode ? `${RANKING_MODE.color}20` : `${ACCENT}20`,
                    borderColor: isRankingMode ? `${RANKING_MODE.color}50` : `${ACCENT}50`,
                    boxShadow: isRankingMode ? `0 0 40px -8px ${RANKING_MODE.glow}` : `0 0 40px -8px ${ACCENT}50`,
                  }}
                  animate={{ scale: [1, 1.08, 1] }}
                  transition={{ repeat: Infinity, duration: 2.5, ease: 'easeInOut' }}
                >
                  <Trophy className="w-14 h-14 sm:w-16 sm:h-16" style={{ color: isRankingMode ? RANKING_MODE.color : ACCENT }} />
                </motion.div>
                <h2 className="font-jp text-3xl sm:text-4xl font-bold text-white mb-2 drop-shadow-[0_0_20px_rgba(59,130,246,0.3)]">
                  {isRankingMode && lastSubmitResult?.nivel_quiz === MAX_NIVEL ? 'Sensei!' : '完了'}
                </h2>
                <p className="text-slate-400 text-lg mb-2">
                  {isRankingMode && lastSubmitResult ? `Nível ${lastSubmitResult.nivel_quiz} — ${lastSubmitResult.categoria_titulo} · ${lastSubmitResult.xp_total} XP` : 'Quiz finalizado'}
                </p>
                {isRankingMode && total > 0 && score < total && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-6 p-4 rounded-2xl bg-amber-500/15 border-2 border-amber-500/30 text-left"
                  >
                    <p className="text-amber-200 font-medium">
                      Para passar de nível é preciso acertar todas as perguntas sem errar. Seu progresso ({score} acertos) foi salvo no ranking. Tente novamente!
                    </p>
                  </motion.div>
                )}
                <motion.p
                  className="text-slate-300 text-base sm:text-lg mb-8 font-medium"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  {total ? (score / total >= 0.8 ? 'Excelente! Você domina a teoria do judô.' : score / total >= 0.5 ? 'Bom trabalho! Continue estudando e evoluindo.' : isRankingMode ? 'Revise o conteúdo e tente de novo para passar de nível.' : 'Siga treinando e revise o conteúdo para melhorar.') : ''}
                </motion.p>
                <div className="grid grid-cols-2 gap-6 mb-8">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-white/[0.1] to-white/[0.02] border-2 border-white/10"
                    style={{ boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1)' }}
                  >
                    <div className="text-4xl sm:text-5xl font-bold text-white">{score} / {total}</div>
                    <div className="text-slate-500 text-sm mt-2 font-medium">Acertos</div>
                  </motion.div>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-white/[0.1] to-white/[0.02] border-2 border-white/10"
                    style={{ boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1)' }}
                  >
                    <div className="text-4xl sm:text-5xl font-bold text-white">
                      {total ? Math.round((score / total) * 100) : 0}%
                    </div>
                    <div className="text-slate-500 text-sm mt-2 font-medium">Percentual</div>
                  </motion.div>
                </div>

                {/* Ranking (modo ranking) */}
                {isRankingMode && (
                  <motion.div
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="mb-10 text-left"
                  >
                    <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                      <Award className="w-5 h-5 text-amber-400" /> Ranking
                    </h3>
                    <div className="rounded-2xl border-2 border-white/10 bg-white/[0.04] overflow-hidden max-h-64 overflow-y-auto">
                      {loadingRanking ? (
                        <div className="p-6 text-slate-400 text-center">Carregando ranking...</div>
                      ) : ranking.length === 0 ? (
                        <div className="p-6 text-slate-500 text-center">Nenhum resultado no ranking ainda.</div>
                      ) : (
                        <table className="w-full text-sm">
                          <thead>
                            <tr className="border-b border-white/10 text-slate-400">
                              <th className="py-3 px-4 text-left font-medium">#</th>
                              <th className="py-3 px-4 text-left font-medium">Nome</th>
                              <th className="py-3 px-4 text-left font-medium hidden sm:table-cell">Dojo</th>
                              <th className="py-3 px-4 text-left font-medium hidden md:table-cell">Cidade</th>
                              <th className="py-3 px-4 text-right font-medium">XP</th>
                              <th className="py-3 px-4 text-center font-medium">Nível</th>
                            </tr>
                          </thead>
                          <tbody>
                            {ranking.slice(0, 20).map((e) => (
                              <tr key={e.posicao} className="border-b border-white/5 hover:bg-white/5">
                                <td className="py-2.5 px-4 font-medium text-slate-300">{e.posicao}</td>
                                <td className="py-2.5 px-4 text-white font-medium">{e.nome}</td>
                                <td className="py-2.5 px-4 text-slate-400 hidden sm:table-cell">{e.dojo || '—'}</td>
                                <td className="py-2.5 px-4 text-slate-400 hidden md:table-cell">
                                  {e.cidade ? <span className="inline-flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> {e.cidade}</span> : '—'}
                                </td>
                                <td className="py-2.5 px-4 text-right text-amber-400 font-semibold">{e.xp_total}</td>
                                <td className="py-2.5 px-4 text-center">
                                  <span className="px-2 py-0.5 rounded-lg bg-white/10 text-slate-300 text-xs">{e.nivel_quiz} · {e.categoria_titulo}</span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      )}
                    </div>
                  </motion.div>
                )}

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <motion.button
                    whileHover={{ scale: 1.04 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={restart}
                    className="py-4 px-8 rounded-2xl font-bold text-white text-lg"
                    style={{ backgroundColor: isRankingMode ? RANKING_MODE.color : ACCENT, boxShadow: `0 12px 32px -8px ${isRankingMode ? RANKING_MODE.glow : ACCENT}60` }}
                  >
                    {isRankingMode ? 'Jogar de novo' : 'Refazer quiz'}
                  </motion.button>
                  <Link
                    to="/index"
                    className="py-4 px-8 rounded-2xl bg-white/10 text-white font-semibold hover:bg-white/20 border-2 border-white/10 transition-all text-lg"
                  >
                    Voltar ao início
                  </Link>
                </div>
              </motion.section>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
