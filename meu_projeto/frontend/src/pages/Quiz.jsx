import { useState, useCallback, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Trophy, ChevronRight, Lightbulb, Check, X, Sparkles, Award, MapPin } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { getQuestionsForLevel, CATEGORIAS_NIVEL, MAX_NIVEL } from '../data/quizData';
import { getQuizRanking, startQuizAttempt, submitQuizAttempt, apiMe } from '../api';

const STORAGE_NICKNAME = 'quiz_ranking_nickname';
const STORAGE_CIDADE = 'quiz_ranking_cidade';
const STORAGE_DOJO = 'quiz_ranking_dojo';
const STORAGE_NIVEL = 'quiz_ranking_nivel';

const ACCENT = 'rgb(59, 130, 246)';
const CORRECT_COLOR = 'rgb(34, 197, 94)';
const WRONG_COLOR = 'rgb(239, 68, 68)';

const RANKING_MODE = { id: 'ranking', label: 'Quiz Ranking', desc: '8 perguntas por nível · 10 níveis — suba até Sensei', emoji: '🏆', color: 'rgb(234, 179, 8)', glow: 'rgba(234,179,8,0.4)' };

const LETTERS = ['A', 'B', 'C', 'D'];

function djb2(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i += 1) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return String(hash >>> 0);
}

function getQuestionKey(q) {
  const base = `${q?.question || ''}|${Array.isArray(q?.answers) ? q.answers.join('|') : ''}`;
  return djb2(base);
}

function ConfettiBurst({ active, intense }) {
  if (!active) return null;
  const count = intense ? 48 : 24;
  const colors = intense ? ['#22c55e', '#34d399', '#86efac', '#4ade80', '#fbbf24', '#f59e0b', '#ffffff'] : ['#22c55e', '#34d399', '#86efac', '#4ade80'];
  const dist = intense ? 180 : 120;
  const particles = Array.from({ length: count }, (_, i) => ({
    id: i,
    angle: (i / count) * 360,
    color: colors[i % colors.length],
    delay: Math.random() * 0.15,
    size: intense ? (8 + Math.random() * 8) : 8,
  }));
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden rounded-2xl">
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute left-1/2 top-1/2 rounded-full"
          style={{ width: p.size, height: p.size, backgroundColor: p.color, transform: 'translate(-50%, -50%)' }}
          initial={{ x: 0, y: 0, opacity: 1, scale: 1, rotate: 0 }}
          animate={{
            x: Math.cos((p.angle * Math.PI) / 180) * dist,
            y: Math.sin((p.angle * Math.PI) / 180) * dist,
            opacity: 0,
            scale: 0,
            rotate: 360,
          }}
          transition={{ duration: intense ? 0.9 : 0.6, delay: p.delay, ease: 'easeOut' }}
        />
      ))}
    </div>
  );
}

function ModalUltimaPergunta({ onClose }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0 }}
        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
        onClick={(e) => e.stopPropagation()}
        className="max-w-md w-full rounded-3xl border-2 border-amber-500/50 bg-gradient-to-br from-amber-500/20 to-amber-900/30 p-8 text-center shadow-2xl"
        style={{ boxShadow: '0 0 60px -10px rgba(245,158,11,0.4)' }}
      >
        <motion.span
          className="font-jp text-4xl font-bold text-amber-400 block mb-4"
          animate={{ scale: [1, 1.05, 1], opacity: [0.9, 1, 0.9] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          最後
        </motion.span>
        <h3 className="text-2xl font-bold text-white mb-2">Esta é a última pergunta!</h3>
        <p className="text-slate-300 mb-6">Concentre-se. Respire. Você está preparado. Dê o seu melhor!</p>
        <motion.button
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.98 }}
          onClick={onClose}
          className="py-4 px-8 rounded-2xl font-bold text-white bg-amber-500 hover:bg-amber-600 transition-colors"
        >
          Estou pronto!
        </motion.button>
      </motion.div>
    </motion.div>
  );
}

function JudokaCelebration() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="relative w-48 h-48 mx-auto mb-6"
    >
      <motion.svg
        viewBox="0 0 120 180"
        className="w-full h-full"
        animate={{
          y: [0, -8, 0],
          rotate: [0, 2, -2, 0],
        }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
      >
        {/* Judoka em pose de vitória — torso e gi */}
        <rect x="45" y="60" width="30" height="50" rx="4" fill="currentColor" className="text-amber-900/90" />
        <rect x="42" y="55" width="36" height="25" rx="3" fill="currentColor" className="text-amber-800/90" />
        {/* Cabeça */}
        <circle cx="60" cy="40" r="18" fill="currentColor" className="text-amber-200/95" />
        <circle cx="60" cy="38" r="14" fill="currentColor" className="text-amber-100" />
        {/* Braços levantados */}
        <path d="M 35 50 Q 20 20 25 5" stroke="currentColor" strokeWidth="6" fill="none" strokeLinecap="round" className="text-amber-800/90" />
        <path d="M 85 50 Q 100 20 95 5" stroke="currentColor" strokeWidth="6" fill="none" strokeLinecap="round" className="text-amber-800/90" />
        {/* Pernas */}
        <rect x="48" y="108" width="14" height="55" rx="3" fill="currentColor" className="text-amber-900/90" />
        <rect x="58" y="108" width="14" height="55" rx="3" fill="currentColor" className="text-amber-900/90" />
        {/* Faixa */}
        <rect x="42" y="75" width="36" height="8" rx="2" fill="#f59e0b" />
      </motion.svg>
      <motion.div
        className="absolute -inset-4 rounded-full border-4 border-amber-400/40"
        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      />
    </motion.div>
  );
}

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.15 } } };
const item = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0 } };

export default function Quiz() {
  const [phase, setPhase] = useState('select');
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  // Modo ranking
  const [isRankingMode, setIsRankingMode] = useState(false);
  const [nivelAtual, setNivelAtual] = useState(1);
  const [attemptId, setAttemptId] = useState(null);
  const [questionKeys, setQuestionKeys] = useState([]);
  const [correctKeys, setCorrectKeys] = useState([]);
  const [nickname, setNickname] = useState('');
  const [dojo, setDojo] = useState('');
  const [cidade, setCidade] = useState('');
  const [ranking, setRanking] = useState([]);
  const [loadingRanking, setLoadingRanking] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [lastSubmitResult, setLastSubmitResult] = useState(null);
  const [mounted, setMounted] = useState(false);
  const [maxStreak, setMaxStreak] = useState(0);
  const [streakAtual, setStreakAtual] = useState(0);
  const [showLastQuestionModal, setShowLastQuestionModal] = useState(false);
  const [isTreinoNivelAnterior, setIsTreinoNivelAnterior] = useState(false);
  const [nivelSalvo, setNivelSalvo] = useState(1);
  const [showTreinoSelector, setShowTreinoSelector] = useState(false);
  const [nivelTreinoEscolhido, setNivelTreinoEscolhido] = useState(1);
  const [isPremiumUser, setIsPremiumUser] = useState(false);
  const maxNivelDisponivel = isPremiumUser ? MAX_NIVEL : 1;

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    apiMe()
      .then((r) => setIsPremiumUser(!!r?.user?.conta_premium))
      .catch(() => setIsPremiumUser(false));
  }, []);

  useEffect(() => {
    if (!mounted || typeof window === 'undefined') return;
    try {
      setNickname(localStorage.getItem(STORAGE_NICKNAME) || '');
      setDojo(localStorage.getItem(STORAGE_DOJO) || '');
      setCidade(localStorage.getItem(STORAGE_CIDADE) || '');
      const n = parseInt(localStorage.getItem(STORAGE_NIVEL) || '1', 10);
      setNivelSalvo(Math.max(1, Math.min(maxNivelDisponivel, n)) || 1);
    } catch {
      // localStorage pode estar bloqueado (ex.: modo privado)
    }
  }, [mounted, maxNivelDisponivel]);


  const loadRanking = useCallback(async () => {
    setLoadingRanking(true);
    try {
      const { ranking: r } = await getQuizRanking();
      const arr = Array.isArray(r) ? r : [];
      setRanking(arr);
      try {
        const nick = localStorage.getItem(STORAGE_NICKNAME) || '';
        if (nick) {
          const entry = arr.find((e) => (e?.nome || '').trim().toLowerCase() === nick.trim().toLowerCase());
          if (entry?.nivel_quiz) {
            const n = Math.max(1, Math.min(maxNivelDisponivel, Number(entry.nivel_quiz) || 1));
            setNivelSalvo(n);
            localStorage.setItem(STORAGE_NIVEL, String(n));
          }
        }
      } catch {
        // ignorar erro ao sincronizar nivel
      }
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
    const len = questions.length;
    if (phase === 'quiz' && len > 0 && current === len - 1) {
      setShowLastQuestionModal(true);
    }
  }, [phase, questions.length, current]);

  useEffect(() => {
    // Iniciar tentativa (server-side timing) quando entra no quiz ranking
    if (phase !== 'quiz') return;
    if (!isRankingMode || isTreinoNivelAnterior) return;
    if (!isPremiumUser) return;
    if (!questions || questions.length === 0) return;
    let cancelled = false;
    const keys = questions.map(getQuestionKey);
    setQuestionKeys(keys);
    setCorrectKeys([]);
    setAttemptId(null);
    startQuizAttempt({ nivel_quiz: nivelAtual, question_keys: keys })
      .then((r) => {
        if (!cancelled) setAttemptId(r?.attempt_id ?? r?.attemptId ?? r?.attempt_id ?? r?.attempt_id);
        if (!cancelled && r?.attempt_id != null) setAttemptId(r.attempt_id);
        if (!cancelled && r?.attemptId != null) setAttemptId(r.attemptId);
      })
      .catch(() => {
        // Se falhar (ex.: não premium), só não pontua.
        if (!cancelled) setAttemptId(null);
      });
    return () => { cancelled = true; };
  }, [phase, isRankingMode, isTreinoNivelAnterior, isPremiumUser, questions, nivelAtual]);

  useEffect(() => {
    if (phase === 'nickname') {
      try {
        if (typeof window !== 'undefined' && localStorage.getItem(STORAGE_NICKNAME)) {
          setNickname(localStorage.getItem(STORAGE_NICKNAME) || '');
          setDojo(localStorage.getItem(STORAGE_DOJO) || '');
          setCidade(localStorage.getItem(STORAGE_CIDADE) || '');
        } else {
          apiMe().then((r) => {
            if (r?.user?.nome) setNickname(r.user.nome);
          }).catch(() => {});
        }
      } catch {
        // localStorage bloqueado
      }
    }
  }, [phase]);

  const hasDadosRanking = useCallback(() => {
    try {
      if (typeof window === 'undefined') return false;
      return !!localStorage.getItem(STORAGE_NICKNAME);
    } catch {
      return false;
    }
  }, []);

  const _initRankingQuiz = useCallback((nome, d, cid) => {
    const nivelInicial = Math.max(1, Math.min(MAX_NIVEL, nivelSalvo));
    setIsRankingMode(true);
    setIsTreinoNivelAnterior(false);
    setNivelAtual(nivelInicial);
    setAttemptId(null);
    setQuestionKeys([]);
    setCorrectKeys([]);
    setMaxStreak(0);
    setStreakAtual(0);
    setQuestions(getQuestionsForLevel(nivelInicial));
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setAnswered(false);
    setLastSubmitResult(null);
    setShowLastQuestionModal(false);
    setPhase('quiz');
  }, [nivelSalvo, maxNivelDisponivel]);

  const startQuiz = useCallback(() => {
    if (hasDadosRanking()) {
      try {
        const n = localStorage.getItem(STORAGE_NICKNAME) || '';
        const d = localStorage.getItem(STORAGE_DOJO) || '';
        const c = localStorage.getItem(STORAGE_CIDADE) || '';
        setNickname(n);
        setDojo(d);
        setCidade(c);
        _initRankingQuiz(n || 'Anônimo', d, c);
      } catch {
        setPhase('nickname');
      }
    } else {
      setPhase('nickname');
    }
  }, [hasDadosRanking, _initRankingQuiz]);

  const startRankingQuiz = useCallback(() => {
    const nome = (nickname || '').trim() || 'Anônimo';
    const d = (dojo || '').trim();
    const cid = (cidade || '').trim();
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_NICKNAME, nome);
      localStorage.setItem(STORAGE_DOJO, d);
      localStorage.setItem(STORAGE_CIDADE, cid);
    }
    _initRankingQuiz(nome, d, cid);
  }, [nickname, dojo, cidade, _initRankingQuiz]);

  const submitAndGoResult = useCallback(async (passou) => {
    const nome = (nickname || '').trim() || 'Anônimo';
    const d = (dojo || '').trim();
    const cid = (cidade || '').trim();
    setSubmitting(true);
    try {
      const res = await submitQuizAttempt({
        attempt_id: attemptId,
        correct_keys: correctKeys,
        nickname: nome,
        dojo: d,
        cidade: cid,
      });
      setLastSubmitResult(res);
      if (typeof window !== 'undefined' && res?.nivel_quiz) {
        try {
          localStorage.setItem(STORAGE_NIVEL, String(Math.max(1, Math.min(maxNivelDisponivel, res.nivel_quiz))));
        } catch {}
      }
      setNivelSalvo((prev) => (res?.nivel_quiz ? Math.max(1, Math.min(maxNivelDisponivel, res.nivel_quiz)) : prev));
      await loadRanking();
      if (isPremiumUser && passou && nivelAtual < MAX_NIVEL) {
        setPhase('levelUp');
      } else {
        setPhase('result');
      }
    } catch {
      setPhase('result');
    } finally {
      setSubmitting(false);
    }
  }, [nickname, dojo, cidade, attemptId, correctKeys, loadRanking, isPremiumUser, maxNivelDisponivel, nivelAtual]);

  const handleAnswer = useCallback((idx) => {
    if (answered) return;
    setSelected(idx);
    setAnswered(true);
    const q = questions[current];
    if (idx === q.correct) {
      setScore((s) => s + 1);
      const nextStreak = streakAtual + 1;
      setStreakAtual(nextStreak);
      setMaxStreak((m) => Math.max(m, nextStreak));
      if (isRankingMode && !isTreinoNivelAnterior) {
        const key = questionKeys[current] || getQuestionKey(q);
        setCorrectKeys((prev) => (prev.includes(key) ? prev : [...prev, key]));
      }
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 1200);
    } else {
      setStreakAtual(0);
      if (isRankingMode && !isTreinoNivelAnterior) submitAndGoResult(false);
      // em treino: continua mostrando explicação, depois vai pra result sem subir ranking
    }
  }, [answered, questions, current, streakAtual, isRankingMode, isTreinoNivelAnterior, submitAndGoResult, questionKeys]);

  const nextQuestion = useCallback(() => {
    const totalNivel = questions.length;
    if (isRankingMode && totalNivel > 0) {
      const completedLevel = current + 1 >= totalNivel;
      if (completedLevel) {
        if (isTreinoNivelAnterior) {
          setPhase('result');
          return;
        }
        if (score === totalNivel) {
          submitAndGoResult(true);
          return;
        }
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
  }, [current, questions.length, score, isRankingMode, isTreinoNivelAnterior, submitAndGoResult]);

  const goNextLevel = useCallback(() => {
    if (!isPremiumUser) {
      setPhase('result');
      return;
    }
    const next = Math.min(MAX_NIVEL, nivelAtual + 1);
    setNivelAtual(next);
    setNivelSalvo(next);
    try {
      if (typeof window !== 'undefined') localStorage.setItem(STORAGE_NIVEL, String(next));
    } catch {}
    setQuestions(getQuestionsForLevel(next));
    setCurrent(0);
    setScore(0);
    setAttemptId(null);
    setQuestionKeys([]);
    setCorrectKeys([]);
    setStreakAtual(0);
    setShowLastQuestionModal(false);
    setSelected(null);
    setAnswered(false);
    setPhase('quiz');
  }, [nivelAtual, isPremiumUser]);

  const startTreinoEmNivel = useCallback((nivel) => {
    if (!isPremiumUser) return;
    const n = Math.max(1, Math.min(MAX_NIVEL, nivel));
    setIsTreinoNivelAnterior(true);
    setIsRankingMode(true);
    setNivelAtual(n);
    setQuestions(getQuestionsForLevel(n));
    setCurrent(0);
    setScore(0);
    setAttemptId(null);
    setQuestionKeys([]);
    setCorrectKeys([]);
    setMaxStreak(0);
    setStreakAtual(0);
    setSelected(null);
    setAnswered(false);
    setShowLastQuestionModal(false);
    setPhase('quiz');
  }, [isPremiumUser]);

  const startTreinoNivelAnterior = useCallback(() => {
    if (nivelAtual <= 1) return;
    const nivelAnterior = nivelAtual - 1;
    startTreinoEmNivel(nivelAnterior);
  }, [nivelAtual, startTreinoEmNivel]);

  const restart = useCallback(() => {
    setPhase('select');
    setQuestions([]);
    setIsRankingMode(false);
    setIsTreinoNivelAnterior(false);
    setLastSubmitResult(null);
    setShowLastQuestionModal(false);
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
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
          <Link
            to="/index"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <div className="flex items-center gap-3">
            <span className="font-jp text-slate-500 text-sm tracking-wider">クイズ — Quiz</span>
          </div>
        </div>
      </header>

      <main className="relative z-10 pt-20 pb-16 px-4 min-h-screen flex flex-col items-center justify-center">
        <AnimatePresence>
          {phase === 'quiz' && total > 0 && current === total - 1 && showLastQuestionModal && (
            <ModalUltimaPergunta key="modal-ultima" onClose={() => setShowLastQuestionModal(false)} />
          )}
        </AnimatePresence>
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
                  className="text-slate-400 text-lg mb-4 max-w-lg mx-auto"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  8 perguntas por nível · 10 níveis. Acerte todas seguidas para subir.
                </motion.p>
                {!isPremiumUser && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mb-4 px-4 py-2 rounded-xl inline-block bg-blue-500/10 border border-blue-400/30 text-blue-200 text-sm"
                  >
                    Gratis: Quiz Nivel 1 liberado. Niveis 2+ apenas no Premium.
                  </motion.p>
                )}
                {hasDadosRanking() && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-6 px-6 py-3 rounded-2xl inline-flex items-center gap-3 border-2 border-amber-500/30 bg-amber-500/10"
                    style={{ boxShadow: '0 0 20px -4px rgba(245,158,11,0.2)' }}
                  >
                    <span className="text-amber-400 font-jp text-sm tracking-wider">SEU NÍVEL</span>
                    <span className="text-2xl font-bold text-white">{nivelSalvo}</span>
                    <span className="text-amber-300 font-medium">{CATEGORIAS_NIVEL[nivelSalvo]}</span>
                    <span className="text-slate-500 text-sm">— continue de onde parou</span>
                  </motion.div>
                )}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
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
                    <Trophy className="w-6 h-6" /> {hasDadosRanking() && nivelSalvo > 1 ? 'Continuar' : 'Jogar'}
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
                {isPremiumUser && nivelSalvo > 1 && (
                  <motion.button
                    variants={item}
                    initial="hidden"
                    animate="show"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => {
                      const base = Math.max(1, Math.min(MAX_NIVEL - 1, nivelSalvo - 1));
                      setNivelTreinoEscolhido(base);
                      setShowTreinoSelector(true);
                    }}
                    className="mt-2 py-2.5 px-4 rounded-xl text-slate-300 hover:text-white text-xs sm:text-sm font-medium border border-white/10 hover:border-white/30 bg-white/5 inline-flex items-center gap-2"
                  >
                    <MapPin className="w-4 h-4" /> Treinar níveis anteriores (sem XP)
                  </motion.button>
                )}
                <motion.div variants={container} initial="hidden" animate="show" className="w-full max-w-3xl mx-auto">
                  <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                    <Award className="w-5 h-5 text-amber-400" /> Ranking
                  </h3>
                  <div className="rounded-2xl border-2 border-white/10 bg-white/[0.04] overflow-hidden max-h-80 overflow-y-auto">
                    {loadingRanking ? (
                      <div className="p-6 text-slate-400 text-center">Carregando ranking...</div>
                    ) : !Array.isArray(ranking) || ranking.length === 0 ? (
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
                          {(Array.isArray(ranking) ? ranking : []).slice(0, 25).map((e, idx) => {
                            const isTop3 = idx < 3;
                            const medalStyles = isTop3 ? [
                              { rowBg: 'rgba(245,158,11,0.18)', borderColor: '#f59e0b', trophyColor: '#fbbf24', label: '1º' },
                              { rowBg: 'rgba(148,163,184,0.2)', borderColor: '#94a3b8', trophyColor: '#cbd5e1', label: '2º' },
                              { rowBg: 'rgba(180,83,9,0.25)', borderColor: '#b45309', trophyColor: '#d97706', label: '3º' },
                            ][idx] : null;
                            return (
                              <tr
                                key={e?.posicao ?? idx}
                                className="border-b border-white/5 hover:bg-white/5"
                                style={isTop3 ? { backgroundColor: medalStyles.rowBg, borderLeft: `4px solid ${medalStyles.borderColor}` } : undefined}
                              >
                                <td className="py-2.5 px-3">
                                  {isTop3 ? (
                                    <span className="inline-flex items-center gap-1.5 font-bold">
                                      <span
                                        className="p-1 rounded-lg border inline-flex"
                                        style={{ backgroundColor: medalStyles.rowBg, borderColor: medalStyles.borderColor }}
                                      >
                                        <Trophy className="w-4 h-4" style={{ color: medalStyles.trophyColor }} />
                                      </span>
                                      <span className="text-white">{medalStyles.label}</span>
                                    </span>
                                  ) : (
                                    <span className="font-medium text-slate-300">{e?.posicao ?? '—'}</span>
                                  )}
                                </td>
                                <td className="py-2.5 px-3 text-white font-medium">{e?.nome ?? '—'}</td>
                                <td className="py-2.5 px-3 text-slate-400 hidden sm:table-cell">{e?.dojo || '—'}</td>
                                <td className="py-2.5 px-3 text-slate-400 hidden md:table-cell">{e?.cidade || '—'}</td>
                                <td className="py-2.5 px-3 text-right text-amber-400 font-semibold">{e?.xp_total ?? '—'}</td>
                                <td className="py-2.5 px-3 text-center">
                                  <span className="px-2 py-0.5 rounded-lg bg-white/10 text-slate-300 text-xs">{e?.nivel_quiz ?? '—'} · {e?.categoria_titulo || '—'}</span>
                                </td>
                              </tr>
                            );
                          })}
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
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.6 }}
                className="relative text-center max-w-2xl mx-auto overflow-visible"
              >
                {/* Chuva de confetti */}
                <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
                  {Array.from({ length: 60 }).map((_, i) => (
                    <motion.div
                      key={i}
                      className="absolute w-3 h-3 rounded-sm"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: -20,
                        backgroundColor: ['#fbbf24', '#f59e0b', '#22c55e', '#34d399', '#ffffff', '#fef3c7'][i % 6],
                      }}
                      initial={{ y: 0, rotate: 0, opacity: 1 }}
                      animate={{ y: '100vh', rotate: 360 * 3, opacity: 0 }}
                      transition={{ duration: 3 + Math.random() * 2, delay: Math.random() * 0.5, ease: 'easeIn' }}
                    />
                  ))}
                </div>
                <JudokaCelebration />
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.3, type: 'spring', stiffness: 200, damping: 15 }}
                  className="relative z-10"
                >
                  <motion.h2
                    className="font-jp text-4xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-500 mb-4"
                    style={{ textShadow: '0 0 60px rgba(251,191,36,0.6)' }}
                    animate={{ scale: [1, 1.05, 1] }}
                    transition={{ duration: 0.8, repeat: Infinity }}
                  >
                    祝！
                  </motion.h2>
                  <motion.h2
                    className="text-4xl sm:text-6xl md:text-7xl font-black text-white mb-2 drop-shadow-[0_0_30px_rgba(251,191,36,0.8)]"
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4, duration: 0.6 }}
                  >
                    PARABÉNS GIGANTE!
                  </motion.h2>
                  <motion.p
                    className="text-xl sm:text-2xl text-amber-300 font-bold mb-2"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.7 }}
                  >
                    Vem comigo para o próximo nível
                  </motion.p>
                  <motion.p
                    className="text-3xl sm:text-4xl font-bold text-amber-400 mb-6"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.9, type: 'spring', stiffness: 300 }}
                  >
                    Nível {nivelAtual + 1} — {CATEGORIAS_NIVEL[nivelAtual + 1] ?? 'Sensei'}
                  </motion.p>
                  {lastSubmitResult && (
                    <p className="text-slate-400 text-sm mb-6">Total: {lastSubmitResult.xp_total} XP</p>
                  )}
                </motion.div>
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8 relative z-10">
                  <motion.button
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.2 }}
                    whileHover={{ scale: 1.06 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={goNextLevel}
                    className="py-5 px-10 rounded-2xl font-bold text-white text-lg"
                    style={{ backgroundColor: RANKING_MODE.color, boxShadow: `0 16px 40px -8px ${RANKING_MODE.glow}` }}
                  >
                    Próximo nível →
                  </motion.button>
                  {nivelAtual > 1 && (
                    <motion.button
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1.4 }}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={startTreinoNivelAnterior}
                      className="py-3 px-6 rounded-xl text-slate-400 hover:text-white text-sm font-medium border border-white/20 hover:border-white/40"
                    >
                      Treinar nível anterior (sem XP)
                    </motion.button>
                  )}
                </div>
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
                {/* Nível em destaque + streak máximo */}
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-4">
                  {isRankingMode && (
                    <div className="flex items-center justify-center gap-3 mb-4 flex-wrap">
                      <motion.div
                        className="px-6 py-3 rounded-2xl border-2 bg-gradient-to-r from-amber-500/25 to-amber-600/15"
                        style={{ borderColor: 'rgba(245,158,11,0.6)', boxShadow: '0 0 24px -4px rgba(245,158,11,0.3)' }}
                        animate={{ scale: [1, 1.02, 1] }}
                        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                      >
                        <span className="text-amber-400 font-jp text-xs tracking-widest block">NÍVEL</span>
                        <span className="text-3xl font-bold text-white">{nivelAtual}</span>
                        <span className="text-amber-400 font-bold block text-lg">{CATEGORIAS_NIVEL[nivelAtual]}</span>
                      </motion.div>
                      {!isPremiumUser && (
                        <div className="px-4 py-2 rounded-xl bg-blue-500/15 border border-blue-400/40">
                          <span className="text-blue-200 text-xs font-semibold">Modo Gratis: somente Nivel 1</span>
                        </div>
                      )}
                      {maxStreak > 0 && (
                        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="px-4 py-2 rounded-xl bg-emerald-500/20 border-2 border-emerald-400/40">
                          <span className="text-emerald-400 font-bold text-lg">{maxStreak}</span>
                          <span className="text-emerald-300/90 text-sm block">máx. seguidos</span>
                        </motion.div>
                      )}
                    </div>
                  )}
                </motion.div>
                <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
                  <span className="text-slate-500 font-jp tracking-wide">Pergunta {current + 1} / {total}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-emerald-400 font-semibold flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                      <Check className="w-4 h-4" /> {score} acertos
                      {isRankingMode && !isTreinoNivelAnterior && <span className="text-emerald-300/80">(+{correctKeys.length} certas)</span>}
                    </span>
                    {streakAtual > 0 && (
                      <span className="text-amber-300 font-bold px-3 py-1.5 rounded-full bg-amber-500/20 border border-amber-400/40">{streakAtual} seguidos 🔥</span>
                    )}
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
                  <ConfettiBurst active={showConfetti} intense={streakAtual >= 3 || score >= total - 1} />
                  {showConfetti && (
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ type: 'spring', stiffness: 500, damping: 15 }}
                      className="absolute top-6 right-6 px-4 py-2 rounded-xl bg-emerald-500/30 border-2 border-emerald-400/60 text-emerald-300 font-bold text-lg"
                    >
                      ACERTOU!
                    </motion.div>
                  )}
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
                              ? { scale: [1, 1.05, 1.02], boxShadow: [`0 0 0 0 ${CORRECT_COLOR}00`, `0 0 48px 12px ${CORRECT_COLOR}60`, `0 0 24px 6px ${CORRECT_COLOR}40`], transition: { duration: 0.6 } }
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
                  {isTreinoNivelAnterior ? 'Treino concluído!' : isRankingMode && lastSubmitResult?.nivel_quiz === MAX_NIVEL ? 'Sensei!' : '完了'}
                </h2>
                <p className="text-slate-400 text-lg mb-2">
                  {isTreinoNivelAnterior
                    ? `Nível ${nivelAtual} — ${CATEGORIAS_NIVEL[nivelAtual]} · Sem XP (apenas treino)`
                    : isRankingMode && lastSubmitResult ? `Nível ${lastSubmitResult.nivel_quiz} — ${lastSubmitResult.categoria_titulo} · ${lastSubmitResult.xp_total} XP` : 'Quiz finalizado'}
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
                {!isPremiumUser && (
                  <div className="mb-8 p-4 rounded-2xl bg-amber-500/10 border border-amber-400/30 text-amber-200">
                    Voce concluiu o Nivel 1 gratis. Para desbloquear niveis 2 a 10, assine o Premium.
                  </div>
                )}
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

                <div className="flex flex-col sm:flex-row gap-4 justify-center flex-wrap">
                  {!isPremiumUser && (
                    <Link
                      to="/payments/planos"
                      className="py-4 px-8 rounded-2xl font-bold text-black bg-amber-400 hover:bg-amber-300 transition-colors text-lg"
                    >
                      Desbloquear niveis Premium
                    </Link>
                  )}
                  <motion.button
                    whileHover={{ scale: 1.04 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={restart}
                    className="py-4 px-8 rounded-2xl font-bold text-white text-lg"
                    style={{ backgroundColor: isRankingMode ? RANKING_MODE.color : ACCENT, boxShadow: `0 12px 32px -8px ${isRankingMode ? RANKING_MODE.glow : ACCENT}60` }}
                  >
                    {isTreinoNivelAnterior ? 'Voltar ao quiz' : isRankingMode ? 'Jogar de novo' : 'Refazer quiz'}
                  </motion.button>
                  {isRankingMode && nivelAtual > 1 && (
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={startTreinoNivelAnterior}
                      className="py-4 px-8 rounded-2xl bg-white/10 text-white font-semibold hover:bg-white/20 border-2 border-white/20"
                    >
                      Treinar nível anterior (sem XP)
                    </motion.button>
                  )}
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

      {/* Seletor de treino de nível anterior (fase select) */}
      <AnimatePresence>
        {phase === 'select' && showTreinoSelector && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md px-4"
            onClick={() => setShowTreinoSelector(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0, y: 16 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 18, stiffness: 260 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-md rounded-3xl border border-white/15 bg-[#020617]/95 p-6 sm:p-7"
            >
              <h3 className="text-lg sm:text-xl font-bold text-white mb-2 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-amber-400" /> Treinar níveis anteriores
              </h3>
              <p className="text-slate-400 text-sm mb-4">
                Escolha um nível que você já alcançou para refazer as perguntas <span className="font-semibold text-amber-300">sem ganhar XP</span>.
              </p>
              <div className="grid grid-cols-2 gap-3 max-h-64 overflow-y-auto py-1">
                {Array.from({ length: Math.max(0, nivelSalvo - 1) }, (_, i) => i + 1).map((n) => (
                  <button
                    key={n}
                    type="button"
                    onClick={() => {
                      setShowTreinoSelector(false);
                      startTreinoEmNivel(n);
                    }}
                    className={`flex flex-col items-start px-4 py-3 rounded-2xl border text-left transition-all ${
                      n === nivelTreinoEscolhido
                        ? 'border-amber-400 bg-amber-500/15 text-white shadow-[0_0_24px_rgba(251,191,36,0.4)]'
                        : 'border-white/10 bg-white/5 text-slate-200 hover:border-amber-400/70 hover:bg-amber-500/10'
                    }`}
                  >
                    <span className="text-xs uppercase tracking-widest text-slate-400">Nível {n}</span>
                    <span className="font-semibold text-sm">{CATEGORIAS_NIVEL[n]}</span>
                  </button>
                ))}
              </div>
              <div className="mt-5 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowTreinoSelector(false)}
                  className="px-4 py-2.5 rounded-xl text-slate-300 hover:text-white bg-white/5 border border-white/15 text-sm font-medium"
                >
                  Cancelar
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
