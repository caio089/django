import { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Menu,
  X,
  LogOut,
  BookOpen,
  History,
  Languages,
  FileText,
  Award,
  Trophy,
  MapPin,
  ChevronRight,
  Sparkles,
  ArrowLeft,
} from 'lucide-react';
import DashboardBackground from '../components/DashboardBackground';
import { apiMe, apiLogout, getQuizRanking } from '../api';

import { FAIXA_TO_COLOR } from '../data/faixaColors';

const MENU_ITENS = [
  { icon: BookOpen, label: 'Quiz', href: '/quiz', desc: 'Teste seus conhecimentos', emoji: '📝' },
  { icon: Trophy, label: 'Ranking', href: '/ranking', desc: 'Ranking completo do quiz', emoji: '🏆' },
  { icon: Award, label: 'Rolamentos', href: '/ukemis', desc: 'Todos os ukemis', emoji: '🔄' },
  { icon: History, label: 'História', href: '/historia', desc: 'Origens e evolução', emoji: '📚' },
  { icon: Languages, label: 'Japonês', href: '/palavras', desc: 'Vocabulário', emoji: '🇯🇵' },
  { icon: FileText, label: 'Regras', href: '/regras', desc: 'Regulamentos', emoji: '📋' },
];

const TYPING_TEXT = 'Bem-vindo ao quiz do Dojo Online!';
const TYPING_SPEED_MS = 70;
const FONT_ELECTRIC = "'Orbitron', sans-serif";
const FONT_JP = "'Noto Sans JP', sans-serif";

/** Intro impactante: fonte elétrica + kanji judô + animação de digitação */
function JudokaRankingIntro({ onComplete }) {
  const [visibleLength, setVisibleLength] = useState(0);

  useEffect(() => {
    if (visibleLength < TYPING_TEXT.length) {
      const t = setTimeout(() => setVisibleLength((n) => n + 1), TYPING_SPEED_MS);
      return () => clearTimeout(t);
    }
    const t = setTimeout(onComplete, 1500);
    return () => clearTimeout(t);
  }, [visibleLength, onComplete]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
      className="fixed inset-0 z-30 flex flex-col items-center justify-center px-4 bg-[#050608]"
    >
      {/* Kanji judô — remate em japonês */}
      <motion.p
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="text-6xl sm:text-7xl md:text-8xl font-black tracking-widest mb-6 sm:mb-8"
        style={{
          fontFamily: FONT_JP,
          background: 'linear-gradient(180deg, #fef3c7 0%, #f59e0b 50%, #b45309 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          textShadow: '0 0 60px rgba(245,158,11,0.5)',
          filter: 'drop-shadow(0 0 20px rgba(251,191,36,0.4))',
        }}
      >
        道場
      </motion.p>
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.6 }}
        transition={{ delay: 0.3 }}
        className="text-amber-500/60 text-sm sm:text-base tracking-[0.4em] uppercase mb-4"
        style={{ fontFamily: FONT_ELECTRIC }}
      >
        Dojo Online
      </motion.span>
      {/* Frase com efeito de digitação — fonte elétrica + brilho */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="max-w-[420px] text-center"
      >
        <p
          className="text-xl sm:text-2xl md:text-3xl font-bold min-h-[3rem] flex flex-wrap items-center justify-center gap-0.5 tracking-wide"
          style={{
            fontFamily: FONT_ELECTRIC,
            color: '#fef3c7',
            textShadow: '0 0 20px rgba(251,191,36,0.8), 0 0 40px rgba(245,158,11,0.4), 0 2px 4px rgba(0,0,0,0.5)',
          }}
        >
          {TYPING_TEXT.slice(0, visibleLength)}
          {visibleLength < TYPING_TEXT.length && (
            <span
              className="animate-pulse inline-block w-0.5 h-6 sm:h-8 bg-amber-400 ml-0.5 align-middle"
              style={{ boxShadow: '0 0 12px rgba(251,191,36,0.9)' }}
            />
          )}
        </p>
      </motion.div>
      {/* Linha de luz sutil */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 0.5, duration: 1.2 }}
        className="absolute bottom-20 left-1/2 -translate-x-1/2 w-64 h-px bg-gradient-to-r from-transparent via-amber-400/60 to-transparent"
        style={{ boxShadow: '0 0 20px rgba(245,158,11,0.5)' }}
      />
    </motion.div>
  );
}

export default function Ranking() {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [quizRanking, setQuizRanking] = useState([]);
  const [loadingRanking, setLoadingRanking] = useState(true);
  const [showJudokaIntro, setShowJudokaIntro] = useState(true);

  useEffect(() => {
    setLoadingRanking(true);
    getQuizRanking(100)
      .then((data) => setQuizRanking(data.ranking || []))
      .catch(() => setQuizRanking([]))
      .finally(() => setLoadingRanking(false));
  }, []);

  useEffect(() => {
    apiMe()
      .then((r) => {
        if (!r.authenticated) navigate('/login');
        else setUser(r.user);
      })
      .catch(() => navigate('/login'));
  }, [navigate]);

  const handleLogout = async () => {
    try {
      const r = await apiLogout();
      navigate(r.redirect || '/');
    } catch {
      navigate('/');
    }
  };

  const hideJudokaIntro = useCallback(() => setShowJudokaIntro(false), []);

  const faixa = user?.faixa || 'Branca';
  const themeColor = FAIXA_TO_COLOR[faixa] || FAIXA_TO_COLOR.Branca;

  if (!user) {
    return (
      <div className="min-h-screen bg-[#0a0c0f] flex flex-col items-center justify-center text-slate-500">
        <div className="w-12 h-12 border-2 border-amber-500/30 border-t-amber-400 rounded-full animate-spin" />
        <span className="mt-4">Carregando...</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-x-hidden font-display antialiased">
      <DashboardBackground accentColor={themeColor} />

      <AnimatePresence>
        {showJudokaIntro && (
          <JudokaRankingIntro key="judoka-intro" onComplete={hideJudokaIntro} />
        )}
      </AnimatePresence>

      <motion.button
        onClick={() => setSidebarOpen(true)}
        className="fixed top-6 right-6 z-50 p-3.5 rounded-2xl glass text-white"
        whileHover={{ scale: 1.08, rotate: 5 }}
        whileTap={{ scale: 0.95 }}
      >
        <Menu className="w-6 h-6" />
      </motion.button>

      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40"
            />
            <motion.aside
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 28, stiffness: 280 }}
              className="fixed top-0 right-0 w-full max-w-sm h-full z-50 glass-dark border-l border-white/10 overflow-hidden flex flex-col"
            >
              <div className="p-6 overflow-y-auto flex-1">
                <div className="flex items-center justify-between mb-10">
                  <div>
                    <span className="font-jp text-3xl text-white/95 block">道場</span>
                    <span className="text-base text-slate-500">Dojo Online — Menu</span>
                  </div>
                  <motion.button
                    onClick={() => setSidebarOpen(false)}
                    className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/10"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <X className="w-5 h-5" />
                  </motion.button>
                </div>
                <nav className="space-y-1">
                  {MENU_ITENS.map((item, i) => (
                    <motion.div key={item.href} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
                      <Link
                        to={item.href}
                        className={`flex items-center gap-5 p-5 rounded-2xl transition-colors group border ${
                          item.href === '/ranking' ? 'bg-white/10 border-white/20' : 'border-transparent hover:border-white/20 hover:bg-white/10'
                        }`}
                        onClick={() => {
                          setSidebarOpen(false);
                          if (item.href === '/ranking') setShowJudokaIntro(true);
                        }}
                      >
                        <span className="text-3xl">{item.emoji}</span>
                        <div className="flex-1 min-w-0 text-left">
                          <p className="font-semibold text-lg text-white">{item.label}</p>
                          <p className="text-base text-slate-500">{item.desc}</p>
                        </div>
                        <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-all" style={{ color: themeColor }} />
                      </Link>
                    </motion.div>
                  ))}
                </nav>
                <div className="mt-8 pt-6 border-t border-white/10 space-y-3">
                  <Link
                    to="/index"
                    className="flex items-center justify-center gap-2 py-3.5 rounded-xl text-slate-400 hover:bg-white/5 hover:text-white transition-colors border border-white/10"
                    onClick={() => setSidebarOpen(false)}
                  >
                    <ArrowLeft className="w-5 h-5" /> Voltar ao início
                  </Link>
                  <Link
                    to="/payments/planos"
                    className="flex items-center justify-center gap-3 py-4 rounded-2xl font-semibold transition-all text-lg"
                    style={{
                      backgroundColor: `${themeColor}20`,
                      borderColor: `${themeColor}50`,
                      borderWidth: '1px',
                      color: themeColor,
                    }}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Sparkles className="w-6 h-6" /> Assinar Premium
                  </Link>
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-slate-500 hover:bg-white/5 hover:text-white transition-colors"
                  >
                    <LogOut className="w-4 h-4" /> Sair
                  </button>
                </div>
              </div>
              <div className="p-5 border-t border-white/5">
                <p className="font-jp text-slate-500 text-sm text-center">柔道 — Judô</p>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <div className="relative z-10 pt-20 md:pt-24 pb-12 px-4 sm:px-6 max-w-5xl mx-auto">
        <Link
          to="/index"
          className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-5 h-5" /> Voltar ao início
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-amber-500/20 border border-amber-500/30">
              <Trophy className="w-8 h-8 text-amber-400" />
            </div>
            Ranking completo
          </h1>
          <p className="mt-2 text-slate-400">Teoria do Judô — todos os colocados por XP</p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-sm overflow-hidden">
          <div className="px-4 sm:px-6 py-4 border-b border-white/10 flex items-center justify-between flex-wrap gap-2">
            <span className="text-slate-400 text-sm">Quiz Ranking — até 100 primeiros</span>
            <Link
              to="/quiz"
              className="text-sm font-medium px-4 py-2 rounded-xl transition-colors"
              style={{ color: themeColor, backgroundColor: `${themeColor}20` }}
            >
              Jogar quiz
            </Link>
          </div>
          <div className="overflow-x-auto">
            {loadingRanking ? (
              <div className="py-16 text-center text-slate-500 text-sm">Carregando ranking...</div>
            ) : quizRanking.length === 0 ? (
              <div className="py-16 text-center text-slate-500 text-sm">Nenhum resultado ainda. Seja o primeiro!</div>
            ) : (
              <table className="w-full min-w-[520px] text-sm">
                <thead>
                  <tr className="border-b border-white/10 text-slate-400 text-left">
                    <th className="py-3 px-3 font-medium">#</th>
                    <th className="py-3 px-3 font-medium">Nome</th>
                    <th className="py-3 px-3 font-medium hidden sm:table-cell">Dojo</th>
                    <th className="py-3 px-3 font-medium hidden md:table-cell">Cidade</th>
                    <th className="py-3 px-3 text-right font-medium">XP</th>
                    <th className="py-3 px-3 text-center font-medium">Nível</th>
                  </tr>
                </thead>
                <tbody>
                  {quizRanking.map((e) => (
                    <tr key={e.posicao} className="border-b border-white/5 hover:bg-white/[0.03] transition-colors">
                      <td className="py-3 px-3 font-medium text-slate-400">{e.posicao}</td>
                      <td className="py-3 px-3 text-white font-medium">{e.nome}</td>
                      <td className="py-3 px-3 text-slate-500 hidden sm:table-cell">{e.dojo || '—'}</td>
                      <td className="py-3 px-3 text-slate-500 hidden md:table-cell">
                        {e.cidade ? (
                          <span className="inline-flex items-center gap-1">
                            <MapPin className="w-3.5 h-3.5" /> {e.cidade}
                          </span>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td className="py-3 px-3 text-right font-semibold" style={{ color: themeColor }}>
                        {e.xp_total}
                      </td>
                      <td className="py-3 px-3 text-center">
                        <span className="px-2 py-1 rounded-lg bg-white/10 text-slate-300 text-xs">
                          {e.nivel_quiz} · {e.categoria_titulo}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
