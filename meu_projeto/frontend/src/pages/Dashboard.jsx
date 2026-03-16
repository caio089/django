import { useState, useEffect } from 'react';
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
  Clock,
  Megaphone,
  Sparkles,
  ChevronRight,
  Trophy,
  MapPin,
} from 'lucide-react';
import DashboardBackground from '../components/DashboardBackground';
import ScrollReveal from '../components/ScrollReveal';
import { apiMe, apiLogout, getQuizRanking } from '../api';

const FAIXAS = [
  { id: 1, nome: 'Faixa Cinza', sub: 'Ponteira Cinza', cor: 'from-gray-600 to-gray-700', img: '/static/faixa-cinza.png', href: '/pagina/1' },
  { id: 2, nome: 'Faixa Azul', sub: 'Ponteira Azul', cor: 'from-blue-600 to-blue-800', img: '/static/faixa-azul.png', href: '/pagina/2' },
  { id: 3, nome: 'Faixa Amarela', sub: 'Ponteira Amarela', cor: 'from-amber-500 to-amber-600', img: '/static/faixa-amarela.png', href: '/pagina/3' },
  { id: 4, nome: 'Faixa Laranja', sub: 'Ponteira Laranja', cor: 'from-orange-500 to-orange-600', img: '/static/faixa-laranja.png', href: '/pagina/4' },
  { id: 5, nome: 'Faixa Verde', sub: '', cor: 'from-emerald-600 to-emerald-700', img: '/static/faixa-verde.png', href: '/pagina/5' },
  { id: 6, nome: 'Faixa Roxa', sub: '', cor: 'from-purple-600 to-purple-700', img: '/static/faixa-roxa.png', href: '/pagina/6' },
  { id: 7, nome: 'Faixa Marrom', sub: '', cor: 'from-amber-800 to-amber-900', img: '/static/faixa-marrom.png', href: '/pagina/7' },
];

const MENU_ITENS = [
  { icon: BookOpen, label: 'Quiz', href: '/quiz', desc: 'Teste seus conhecimentos', emoji: '📝' },
  { icon: Award, label: 'Simulados', href: '/simulados', desc: 'Simulados de graduação', emoji: '📋' },
  { icon: Trophy, label: 'Ranking', href: '/ranking', desc: 'Ranking completo do quiz', emoji: '🏆' },
  { icon: Award, label: 'Rolamentos', href: '/ukemis', desc: 'Todos os ukemis', emoji: '🔄' },
  { icon: Award, label: 'Amarrar faixa', href: '/amarrar-faixa', desc: 'Como amarrar a faixa', emoji: '🎗️' },
  { icon: History, label: 'História', href: '/historia', desc: 'Origens e evolução', emoji: '📚' },
  { icon: Languages, label: 'Japonês', href: '/palavras', desc: 'Vocabulário', emoji: '🇯🇵' },
  { icon: FileText, label: 'Regras', href: '/regras', desc: 'Regulamentos', emoji: '📋' },
];

// Cor RGB por faixa do usuário — define o tema da página
const FAIXA_TO_COLOR = {
  Branca: 'rgb(203, 213, 225)', // slate-300 — visível no dark
  Cinza: 'rgb(107, 114, 128)',
  Azul: 'rgb(37, 99, 235)',
  Amarela: 'rgb(245, 158, 11)',
  Laranja: 'rgb(234, 88, 12)',
  Verde: 'rgb(5, 150, 105)',
  Roxa: 'rgb(124, 58, 237)',
  Marrom: 'rgb(146, 64, 14)',
};

const QUOTES = [
  { jp: '「柔よく剛を制す」', pt: 'O suave domina o rígido' },
  { jp: '「精力善用、自他共栄」', pt: 'Máxima eficiência, prosperidade mútua' },
  { jp: '「形を正し、心を鍛える」', pt: 'Corrija a forma, tempere a mente' },
  { jp: '「心・技・体」', pt: 'Mente, técnica e corpo' },
];

function formatTrialRemaining(trialFim) {
  if (!trialFim) return '--:--:--';
  const end = new Date(trialFim);
  const now = new Date();
  const ms = end - now;
  if (ms <= 0) return '00:00:00';
  const totalSec = Math.floor(ms / 1000);
  const d = Math.floor(totalSec / 86400);
  const h = Math.floor((totalSec % 86400) / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  const s = totalSec % 60;
  const pad = (n) => (n < 10 ? '0' : '') + n;
  return d > 0 ? `${d}d ${pad(h)}:${pad(m)}:${pad(s)}` : `${pad(h)}:${pad(m)}:${pad(s)}`;
}

function FaixaCard({ f, locked, navigate, index }) {
  const isCenter = index === 6;
  const shapeClass = isCenter ? 'rounded-3xl' : index % 3 === 0 ? 'rounded-2xl' : 'rounded-[1.5rem]';

  const content = (
    <>
      <img
        src={f.img}
        alt={f.nome}
        className="h-10 w-auto mx-auto mb-2 drop-shadow object-contain"
        onError={(e) => (e.target.style.display = 'none')}
      />
      <p className="text-base font-bold leading-tight line-clamp-1 relative z-10">{f.nome}</p>
      {f.sub ? <p className="text-xs opacity-90 mt-1 line-clamp-1 relative z-10">{f.sub}</p> : <span className="h-4" />}
    </>
  );

  const baseClass = `h-full w-full ${shapeClass} p-3 flex flex-col items-center justify-center text-center relative overflow-hidden bg-gradient-to-br text-white shadow-lg
    border border-white/20`;

  if (locked) {
    return (
      <div className="w-full h-full min-w-0 min-h-0">
        <div
          onClick={() => navigate('/payments/planos')}
          className={`${baseClass} ${f.cor} cursor-pointer`}
        >
          {content}
          <span className="absolute top-3 right-3 text-white/80 text-xl">🔒</span>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full min-w-0 min-h-0">
      <div>
        <Link
          to={f.href}
          className={`block ${baseClass} ${f.cor} hover:opacity-95 transition-opacity duration-200`}
        >
          {content}
        </Link>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [trialCountdown, setTrialCountdown] = useState('--:--:--');
  const [trialProgress, setTrialProgress] = useState(0);
  const [showTrialWelcome, setShowTrialWelcome] = useState(false);
  const [trialExpirado, setTrialExpirado] = useState(false);
  const [quizRanking, setQuizRanking] = useState([]);
  const [loadingRanking, setLoadingRanking] = useState(false);

  useEffect(() => {
    if (!user) return;
    setLoadingRanking(true);
    getQuizRanking(15)
      .then((data) => setQuizRanking(data.ranking || []))
      .catch(() => setQuizRanking([]))
      .finally(() => setLoadingRanking(false));
  }, [user]);

  useEffect(() => {
    if (false && trialExpirado) {
      const t = setTimeout(() => navigate('/payments/planos'), 5000);
      return () => clearTimeout(t);
    }
  }, [trialExpirado, navigate]);

  useEffect(() => {
    apiMe()
      .then((r) => {
        if (!r.authenticated) navigate('/login');
        else {
          setUser(r.user);
          if (false && r.user?.trial_ativo && r.user?.trial_fim) {
            const key = 'trial_welcome_shown_' + r.user.id;
            if (!localStorage.getItem(key)) setShowTrialWelcome(true);
          }
          if (false && r.user?.trial_expirado) setTrialExpirado(true);
        }
      })
      .catch(() => navigate('/login'));
  }, [navigate]);

  useEffect(() => {
    if (!user?.trial_ativo || !user?.trial_fim) return;
    const tick = () => {
      const end = new Date(user.trial_fim);
      const now = new Date();
      const start = user?.trial_inicio ? new Date(user.trial_inicio) : new Date(end.getTime() - 3 * 24 * 60 * 60 * 1000);
      const totalMs = end - start;
      const used = now - start;
      const pct = totalMs > 0 ? Math.min(100, Math.max(0, (used / totalMs) * 100)) : 0;
      setTrialProgress(pct);
      setTrialCountdown(formatTrialRemaining(user.trial_fim));
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [user]);

  const handleLogout = async () => {
    try {
      const r = await apiLogout();
      navigate(r.redirect || '/');
    } catch {
      navigate('/');
    }
  };

  const nome = user?.nome || 'Visitante';
  const faixa = user?.faixa || 'Branca';
  const trialAtivo = false;
  const temAcesso = user?.conta_premium || false;
  const themeColor = FAIXA_TO_COLOR[faixa] || FAIXA_TO_COLOR.Branca;
  const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];

  return (
    <div className="min-h-screen relative overflow-x-hidden font-display antialiased">
      <DashboardBackground accentColor={themeColor} />

      {/* Trial Bar removida */}

      <motion.button
        onClick={() => setSidebarOpen(true)}
        className="fixed top-6 right-6 z-50 p-3.5 rounded-2xl glass text-white"
        whileHover={{ scale: 1.08, rotate: 5 }}
        whileTap={{ scale: 0.95 }}
      >
        <Menu className="w-6 h-6" />
      </motion.button>

      {/* Sidebar */}
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
                    <motion.div
                      key={item.href}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.04 }}
                    >
                      <Link
                        to={item.href}
                        className="flex items-center gap-5 p-5 rounded-2xl hover:bg-white/10 transition-colors group border border-transparent hover:border-white/20"
                        onClick={() => setSidebarOpen(false)}
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

      {/* Trial modais removidos */}

      {/* Main */}
      <div className="relative z-10 pt-20 md:pt-24 pb-12 px-4 sm:px-6 max-w-6xl mx-auto">
        {!user && (
          <div className="flex flex-col items-center justify-center min-h-[60vh] text-slate-500">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1.2, repeat: Infinity, ease: 'linear' }}
              className="w-12 h-12 border-2 border-amber-500/30 border-t-amber-400 rounded-full"
            />
            <span className="mt-4 font-jp text-base">読み込み中... — Carregando</span>
          </div>
        )}

        {user && (
          <>
            <div className="text-center mb-6 md:mb-8">
              <span className="font-jp text-4xl sm:text-5xl font-bold text-white/95 block mb-4">柔道</span>
              <p className="font-jp text-xl sm:text-2xl font-medium text-white/90">{quote.jp}</p>
              <p className="text-sm sm:text-base mt-1 opacity-80" style={{ color: themeColor }}>{quote.pt}</p>
            </div>

            {/* Desktop */}
            <div className="hidden lg:grid lg:grid-cols-2 gap-14 items-start">
              <ScrollReveal direction="left" delay={0.1}>
                <div className="space-y-8">
                  <div className="p-5 rounded-3xl bg-white/5 border border-white/10">
                    <h2 className="text-2xl md:text-3xl font-semibold text-white leading-tight">
                      {nome}, você está no caminho.
                    </h2>
                    <p className="mt-3 text-slate-400 text-lg">
                      Faixa <span className="font-semibold" style={{ color: themeColor }}>{faixa}</span> é só o começo.
                      Escolha sua faixa e evolua no judô.
                    </p>
                  </div>
                  {/* Card Quiz — destaque para jogar */}
                  <Link
                    to="/quiz"
                    className="group block p-5 rounded-2xl border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 transition-all duration-300 hover:scale-[1.02]"
                  >
                    <div className="flex items-center gap-4">
                      <div className="p-3 rounded-xl bg-amber-500/20 border border-amber-500/30">
                        <BookOpen className="w-8 h-8 text-amber-400" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-white">Quiz de Judô</h3>
                        <p className="text-slate-400 text-sm mt-0.5">Teste seus conhecimentos sobre teoria do judô</p>
                      </div>
                      <ChevronRight className="w-6 h-6 text-amber-400 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </Link>
                  <ScrollReveal direction="up" delay={0.4}>
                    <div
                      className="rounded-2xl border backdrop-blur p-5 dojo-frame"
                      style={{ backgroundColor: `${themeColor}08`, borderColor: `${themeColor}30` }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <Megaphone className="w-6 h-6" style={{ color: themeColor }} />
                          <span className="text-white/95 font-semibold text-lg">Anúncios</span>
                        </div>
                        <div className="flex gap-2">
                          <span className="px-3 py-1.5 rounded-xl text-sm font-medium" style={{ backgroundColor: `${themeColor}25`, color: themeColor }}>PROMO</span>
                          <span className="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 text-sm font-medium">NOVO</span>
                        </div>
                      </div>
                    </div>
                  </ScrollReveal>
                </div>
              </ScrollReveal>

              <ScrollReveal direction="right" delay={0.1}>
                <div className="grid grid-cols-3 gap-3 grid-rows-[140px_140px_140px]">
                  {FAIXAS.slice(0, 6).map((f, i) => (
                    <div key={f.id} className="overflow-hidden">
                      <FaixaCard f={f} index={i} locked={!temAcesso} navigate={navigate} />
                    </div>
                  ))}
                  <div className="col-start-2 overflow-hidden">
                    <FaixaCard f={FAIXAS[6]} index={6} locked={!temAcesso} navigate={navigate} />
                  </div>
                </div>
              </ScrollReveal>
            </div>

            {/* Mobile */}
            <div className="lg:hidden space-y-6">
              <ScrollReveal direction="up" delay={0.05}>
                <div className="text-center space-y-6">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                    <h2 className="text-xl md:text-2xl font-semibold text-white">
                      {nome}, você está no caminho.
                    </h2>
                    <p className="mt-4 text-slate-400 text-lg">
                      Faixa <span className="font-semibold" style={{ color: themeColor }}>{faixa}</span>. Escolha sua faixa e comece.
                    </p>
                  </div>
                  <Link
                    to="/quiz"
                    className="group flex items-center gap-4 p-4 rounded-2xl border border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 transition-all mx-auto max-w-sm"
                  >
                    <div className="p-2.5 rounded-xl bg-amber-500/20 border border-amber-500/30">
                      <BookOpen className="w-6 h-6 text-amber-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white">Quiz de Judô</h3>
                      <p className="text-slate-400 text-sm">Teste seus conhecimentos</p>
                    </div>
                    <ChevronRight className="w-5 h-5 text-amber-400 group-hover:translate-x-1 transition-transform" />
                  </Link>
                  <div
                    className="rounded-2xl border p-4 mx-auto max-w-sm"
                    style={{ backgroundColor: `${themeColor}08`, borderColor: `${themeColor}30` }}
                  >
                    <div className="flex items-center justify-between">
                      <Megaphone className="w-5 h-5" style={{ color: themeColor }} />
                      <span className="text-white/95 font-medium">Anúncios</span>
                      <span className="px-2.5 py-1 rounded-lg text-sm font-medium" style={{ backgroundColor: `${themeColor}25`, color: themeColor }}>PROMO</span>
                    </div>
                  </div>
                </div>
              </ScrollReveal>

              <ScrollReveal direction="up" delay={0.15}>
                <div className="grid grid-cols-2 gap-3 grid-rows-[130px_130px_130px_130px] max-w-lg mx-auto">
                  {FAIXAS.slice(0, 6).map((f, i) => (
                    <div key={f.id} className="overflow-hidden">
                      <FaixaCard f={f} index={i} locked={!temAcesso} navigate={navigate} />
                    </div>
                  ))}
                  <div key={FAIXAS[6].id} className="overflow-hidden">
                    <FaixaCard f={FAIXAS[6]} index={6} locked={!temAcesso} navigate={navigate} />
                  </div>
                </div>
              </ScrollReveal>
            </div>

            {/* Ranking do Quiz — seção própria, sem sobrepor */}
            <ScrollReveal direction="up" delay={0.2}>
              <section className="mt-12 md:mt-16 w-full max-w-4xl mx-auto">
                <div className="rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-sm overflow-hidden">
                  <div className="px-4 sm:px-6 py-4 border-b border-white/10 flex items-center justify-between flex-wrap gap-2">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-amber-500/15 border border-amber-500/25">
                        <Trophy className="w-5 h-5 text-amber-400" />
                      </div>
                      <div>
                        <h2 className="text-lg font-semibold text-white">Top 3 — Ranking do Quiz</h2>
                        <p className="text-xs text-slate-500">Teoria do Judô — XP por nível</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Link
                        to="/ranking"
                        className="text-sm font-medium px-4 py-2 rounded-xl transition-colors border border-white/20 text-slate-300 hover:bg-white/10 hover:text-white"
                      >
                        Ver ranking completo
                      </Link>
                      <Link
                        to="/quiz"
                        className="text-sm font-medium px-4 py-2 rounded-xl transition-colors"
                        style={{ color: themeColor, backgroundColor: `${themeColor}20` }}
                      >
                        Jogar quiz
                      </Link>
                    </div>
                  </div>
                  <div className="overflow-x-auto">
                    {loadingRanking ? (
                      <div className="py-12 text-center text-slate-500 text-sm">Carregando ranking...</div>
                    ) : quizRanking.length === 0 ? (
                      <div className="py-12 text-center text-slate-500 text-sm">Nenhum resultado ainda. Seja o primeiro!</div>
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
                          {quizRanking.slice(0, 3).map((e, idx) => {
                            const medalStyles = [
                              { rowBg: 'rgba(245,158,11,0.18)', borderColor: '#f59e0b', trophyColor: '#fbbf24', label: '1º' },
                              { rowBg: 'rgba(148,163,184,0.2)', borderColor: '#94a3b8', trophyColor: '#cbd5e1', label: '2º' },
                              { rowBg: 'rgba(180,83,9,0.25)', borderColor: '#b45309', trophyColor: '#d97706', label: '3º' },
                            ][idx];
                            return (
                              <tr
                                key={e.posicao}
                                className="border-b border-white/10 transition-colors"
                                style={{
                                  backgroundColor: medalStyles.rowBg,
                                  borderLeft: `4px solid ${medalStyles.borderColor}`,
                                }}
                              >
                                <td className="py-4 px-3">
                                  <span className="inline-flex items-center gap-2 font-bold">
                                    <span
                                      className="p-1.5 rounded-xl border inline-flex"
                                      style={{ backgroundColor: medalStyles.rowBg, borderColor: medalStyles.borderColor, color: medalStyles.trophyColor }}
                                    >
                                      <Trophy className="w-5 h-5" style={{ color: medalStyles.trophyColor }} />
                                    </span>
                                    <span className="text-white">{medalStyles.label}</span>
                                  </span>
                                </td>
                                <td className="py-4 px-3 text-white font-semibold">{e.nome}</td>
                                <td className="py-4 px-3 text-slate-400 hidden sm:table-cell">{e.dojo || '—'}</td>
                                <td className="py-4 px-3 text-slate-400 hidden md:table-cell">{e.cidade ? <span className="inline-flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> {e.cidade}</span> : '—'}</td>
                                <td className="py-4 px-3 text-right font-bold" style={{ color: themeColor }}>{e.xp_total}</td>
                                <td className="py-4 px-3 text-center">
                                  <span className="px-2 py-1 rounded-lg bg-white/10 text-slate-300 text-xs font-medium">{e.nivel_quiz} · {e.categoria_titulo}</span>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>
              </section>
            </ScrollReveal>
          </>
        )}
      </div>
    </div>
  );
}
