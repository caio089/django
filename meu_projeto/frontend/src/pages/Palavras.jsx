import { useState, useCallback, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Volume2, Mic, Trophy, Sparkles } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { BELT_DATA } from '../data/palavrasData';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { pronunciaCorreta, normalizarTexto } from '../utils/pronuncia';
import { apiMe } from '../api';

const ACCENT = 'rgb(124, 58, 237)';

function getAllWords() {
  const seen = new Set();
  const all = [];
  ['gray', 'blue', 'yellow', 'green'].forEach((key) => {
    BELT_DATA[key].words.forEach((w) => {
      const id = `${w.japanese}-${w.meaning}`;
      if (!seen.has(id)) {
        seen.add(id);
        all.push({ ...w });
      }
    });
  });
  return all;
}

const TODAS_PALAVRAS = getAllWords();

const NUMERO_PT = { 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez' };
const NUMERO_ROMAJI_LOWER = { 1: 'ichi', 2: 'ni', 3: 'san', 4: 'shi', 5: 'go', 6: 'roku', 7: 'shichi', 8: 'hachi', 9: 'ku', 10: 'ju' };

const NUMEROS_JUDO = [
  { kanji: '一', romaji: 'Ichi', num: 1, speak: 'いち' },
  { kanji: '二', romaji: 'Ni', num: 2, speak: 'に' },
  { kanji: '三', romaji: 'San', num: 3, speak: 'さん' },
  { kanji: '四', romaji: 'Shi', num: 4, speak: 'し' },
  { kanji: '五', romaji: 'Go', num: 5, speak: 'ご' },
  { kanji: '六', romaji: 'Roku', num: 6, speak: 'ろく' },
  { kanji: '七', romaji: 'Shichi', num: 7, speak: 'しち' },
  { kanji: '八', romaji: 'Hachi', num: 8, speak: 'はち' },
  { kanji: '九', romaji: 'Ku', num: 9, speak: 'く' },
  { kanji: '十', romaji: 'Jū', num: 10, speak: 'じゅう' },
];

let jaVoices = [];

// Partículas estáveis (evita flicker por re-renders)
const PARTICLES = (() => {
  const colors = ['#22c55e', '#34d399', '#86efac', '#4ade80', '#fbbf24', '#f59e0b', '#a78bfa', '#ffffff'];
  return {
    intense: Array.from({ length: 16 }, (_, i) => ({
      id: i,
      angle: (i / 16) * 360,
      color: colors[i % colors.length],
      delay: ((i * 7) % 13) / 13 * 0.1,
      size: 10 + (i % 5) * 1.5,
    })),
    normal: Array.from({ length: 36 }, (_, i) => ({
      id: i,
      angle: (i / 36) * 360,
      color: colors[i % colors.length],
      delay: ((i * 5) % 11) / 11 * 0.1,
      size: 8 + (i % 4) * 1.2,
    })),
  };
})();

function ConfettiBurst({ active, intense }) {
  if (!active) return null;
  const particles = intense ? PARTICLES.intense : PARTICLES.normal;
  const dist = intense ? 320 : 220;
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
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
          transition={{ duration: 0.8, delay: p.delay, ease: 'easeOut' }}
        />
      ))}
    </div>
  );
}

function CelebraçãoAcerto({ onClose, isNumero }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black"
      style={{ isolation: 'isolate', transform: 'translateZ(0)' }}
      onClick={onClose}
    >
      <ConfettiBurst active intense />
      <motion.div
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ type: 'spring', damping: 18, stiffness: 260 }}
        onClick={(e) => e.stopPropagation()}
        className="relative text-center max-w-md"
      >
        <motion.div
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 0.5, repeat: 1 }}
          className="mb-4 inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 shadow-[0_0_40px_rgba(245,158,11,0.6)]"
        >
          <Trophy className="w-10 h-10 text-white" strokeWidth={2.5} />
        </motion.div>
        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-xl sm:text-2xl font-bold text-amber-400 mb-2 drop-shadow-lg"
        >
          O DOJO ESTÁ ORGULHOSO DE VOCÊ!
        </motion.h2>
        <motion.p
          initial={{ y: 10, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-slate-200 text-base mb-4"
        >
          {isNumero ? 'Você pronunciou o número perfeitamente!' : 'Pronúncia correta! Excelente!'}
        </motion.p>
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: 'spring', stiffness: 300 }}
          className="flex justify-center gap-2"
        >
          <Sparkles className="w-6 h-6 text-amber-400/80" />
          <span className="text-amber-300/90 text-sm font-semibold">OSS!</span>
          <Sparkles className="w-6 h-6 text-amber-400/80" />
        </motion.div>
      </motion.div>
    </motion.div>
  );
}

function NumeroCard({ n, cardId, speechProps = {}, onCelebrate }) {
  const [playing, setPlaying] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [debugTexto, setDebugTexto] = useState('');
  const timeoutRef = useRef(null);

  const sp = speechProps ?? { supported: false, listening: false, activeCardId: null, startVoiceForCard: () => {}, stopVoice: () => {}, reset: () => {} };
  const isListening = sp.listening && sp.activeCardId === cardId;
  const { supported = false, startVoiceForCard = () => {}, stopVoice = () => {}, reset = () => {} } = sp;

  const alvoPt = NUMERO_PT[n.num];
  const alvoRomaji = NUMERO_ROMAJI_LOWER[n.num] ?? n.romaji?.toLowerCase().trim();

  const onResult = useCallback(
    (texto) => {
      setDebugTexto(texto);
      const txtNorm = normalizarTexto(texto || '');
      const resPt = alvoPt ? pronunciaCorreta(alvoPt, texto, 0.52) : { ok: false };
      const resRomaji = alvoRomaji ? pronunciaCorreta(alvoRomaji, texto, 0.52) : { ok: false };
      const digitMatch = txtNorm === String(n.num);
      const ok = resPt.ok || resRomaji.ok || digitMatch;
      if (ok && onCelebrate) {
        onCelebrate(true);
      } else if (!ok) {
        setFeedback('erro');
        setTimeout(() => setFeedback(null), 1500);
      }
    },
    [alvoPt, alvoRomaji, onCelebrate, n.num]
  );

  useEffect(() => () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); }, []);

  const handlePlay = useCallback(() => {
    setPlaying(true);
    speakJapanese(n.speak || n.kanji);
    setTimeout(() => setPlaying(false), 800);
  }, [n.speak, n.kanji]);

  return (
    <motion.div
      role="group"
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      whileHover={{ y: -4 }}
      className="relative"
    >
      <div
        className={`flex flex-col items-center justify-center rounded-2xl p-6 sm:p-8 min-w-[140px] sm:min-w-[160px] transition-all ${
          playing || isListening
            ? 'bg-emerald-500/25 ring-2 ring-emerald-400/50'
            : 'bg-white/[0.05] border border-white/10 hover:bg-white/[0.1] hover:border-purple-500/30'
        }`}
      >
        <button
          type="button"
          onClick={handlePlay}
          className="flex flex-col items-center justify-center w-full cursor-pointer text-left"
        >
          <span className="font-jp text-4xl sm:text-5xl font-bold text-white">{n.kanji}</span>
          <span className="text-slate-400 text-sm sm:text-base font-mono mt-1">{n.romaji}</span>
          <span className="text-amber-400/90 text-lg sm:text-xl font-semibold mt-1">{n.num}</span>
          {n.desc && <span className="text-slate-500 text-xs mt-1">{n.desc}</span>}
        </button>
        {supported && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              if (!supported) return;
              if (isListening) {
                if (timeoutRef.current) clearTimeout(timeoutRef.current);
                timeoutRef.current = null;
                stopVoice();
                return;
              }
              setDebugTexto('');
              reset();
              startVoiceForCard(onResult, cardId);
              timeoutRef.current = setTimeout(() => { timeoutRef.current = null; stopVoice(); }, VOICE_TIMEOUT_MS);
            }}
            className={`mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold border transition-all ${
              isListening ? 'border-emerald-400 bg-emerald-500/20 text-emerald-100' : 'border-white/20 bg-white/10 text-slate-300 hover:border-purple-400/50'
            }`}
          >
            <Mic className="w-4 h-4" />
            {isListening ? 'Parar' : 'Falar'}
          </button>
        )}
        {debugTexto && <span className="text-xs text-slate-500 mt-2 truncate max-w-full">Você: {debugTexto}</span>}
        {feedback === 'erro' && (
          <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-[10px] text-red-400 mt-1">Tente novamente</motion.span>
        )}
        {isListening && (
          <motion.div
            className="pointer-events-none absolute inset-0 rounded-xl border-2 border-emerald-400/60"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.3, 0.7, 0.3] }}
            transition={{ duration: 1, repeat: Infinity }}
          />
        )}
      </div>
    </motion.div>
  );
}

function speakJapanese(text) {
  if (typeof window === 'undefined' || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'ja-JP';
  u.rate = 0.85;
  if (jaVoices.length) u.voice = jaVoices[0];
  window.speechSynthesis.speak(u);
}

const VOICE_TIMEOUT_MS = 6000; // 6s para o usuário falar

function WordCard({ w, index, cardId, speechProps = {}, onCelebrate }) {
  const [playing, setPlaying] = useState(false);
  const [feedback, setFeedback] = useState(null); // 'ok' | 'erro' | 'no-support'
  const [debugTexto, setDebugTexto] = useState('');
  const timeoutRef = useRef(null);
  const kanji = w.japanese.replace(/\s*\([^)]*\)/g, '').trim();
  const textToSpeak = w.speak || kanji || w.romaji;
  const alvoPronunciaPt = w.meaning;
  const alvoPronunciaRomaji = w.romaji;

  const sp = speechProps ?? {
    supported: false,
    listening: false,
    activeCardId: null,
    error: null,
    startVoiceForCard: () => {},
    stopVoice: () => {},
    reset: () => {},
  };
  const isListening = sp.listening && sp.activeCardId === cardId;
  const {
    supported = false,
    error = null,
    startVoiceForCard = () => {},
    stopVoice = () => {},
    reset = () => {},
  } = sp;

  const onResult = useCallback(
    (texto) => {
      setDebugTexto(texto);
      if (!alvoPronunciaPt && !alvoPronunciaRomaji) {
        setFeedback('erro');
        setTimeout(() => setFeedback(null), 1500);
        return;
      }
      const resPt = alvoPronunciaPt ? pronunciaCorreta(alvoPronunciaPt, texto, 0.52) : { ok: false };
      const resRomaji = alvoPronunciaRomaji ? pronunciaCorreta(alvoPronunciaRomaji, texto, 0.52) : { ok: false };
      const ok = resPt.ok || resRomaji.ok;
      if (ok) {
        (onCelebrate ?? (() => {}))(false);
      } else {
        setFeedback('erro');
        setTimeout(() => setFeedback(null), 1500);
      }
    },
    [alvoPronunciaPt, alvoPronunciaRomaji, onCelebrate]
  );

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  const handleClick = useCallback(() => {
    setPlaying(true);
    speakJapanese(textToSpeak);
    setTimeout(() => setPlaying(false), 1200);
  }, [textToSpeak]);

  return (
    <motion.div
      role="group"
      tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(); } }}
      initial={{ opacity: 0, y: 24, scale: 0.96 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ delay: Math.min(index * 0.02, 0.4), type: 'spring', stiffness: 280, damping: 22 }}
      whileHover={{ y: -6, scale: 1.02, transition: { duration: 0.2 } }}
      whileTap={{ scale: 0.97 }}
      onClick={handleClick}
      className="relative w-full text-left rounded-2xl overflow-hidden group cursor-pointer"
    >
      <div
        className={`relative rounded-2xl p-5 sm:p-6 transition-all duration-300 group-hover:shadow-[0_0_30px_-5px_rgba(124,58,237,0.25)] ${
          playing
            ? 'bg-gradient-to-br from-purple-500/15 to-emerald-500/10 ring-2 ring-emerald-400/40'
            : 'bg-white/[0.04] border border-white/[0.06] group-hover:bg-white/[0.07] group-hover:border-white/10'
        }`}
      >
        {/* Ripple effect when playing */}
        {playing && (
          <motion.div
            className="absolute inset-0 rounded-2xl pointer-events-none"
            initial={{ opacity: 0.5, scale: 0.95 }}
            animate={{ opacity: 0, scale: 1.1 }}
            transition={{ duration: 0.6 }}
            style={{
              background: 'radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%)',
            }}
          />
        )}

        <div className="relative flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <motion.p
              className="font-jp text-2xl sm:text-3xl font-bold text-white mb-2 drop-shadow-sm"
              initial={false}
              animate={{ scale: playing ? 1.05 : 1 }}
              transition={{ duration: 0.2 }}
            >
              {kanji || w.japanese}
            </motion.p>
            <p className="text-slate-400 text-sm font-mono tracking-wide mb-2">{w.romaji}</p>
            <p
              className="inline-block px-3 py-1 rounded-lg text-amber-400/95 font-semibold text-sm"
              style={{ backgroundColor: 'rgba(245,158,11,0.15)' }}
            >
              {w.meaning}
            </p>
          </div>
          <motion.div
            className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 transition-colors duration-300 ${
              playing ? 'bg-emerald-500/30' : 'bg-white/5 group-hover:bg-purple-500/20'
            }`}
            animate={{
              scale: playing ? [1, 1.15, 1] : 1,
              transition: playing ? { duration: 0.5 } : {},
            }}
          >
            <Volume2
              className={`w-6 h-6 transition-colors ${
                playing ? 'text-emerald-400' : 'text-slate-400 group-hover:text-purple-300'
              }`}
            />
          </motion.div>
        </div>
        <div className="relative mt-3 flex items-center justify-between gap-3 text-xs">
          <p className="text-slate-500/80 font-medium">
            Toque para ouvir · fale a tradução em voz alta para treinar
          </p>
          {isListening && (
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/60 text-emerald-100 text-[10px] font-semibold">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-300" />
              </span>
              Escutando você...
            </div>
          )}
        </div>

        {/* Botão de pronúncia por voz — button real (parent é div, não há nesting) */}
        <div className="mt-4 flex items-center justify-between gap-3 text-xs">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation(); // não disparar o play do card
              if (!supported) {
                setFeedback('no-support');
                setTimeout(() => setFeedback(null), 1500);
                return;
              }
              if (isListening) {
                if (timeoutRef.current) clearTimeout(timeoutRef.current);
                timeoutRef.current = null;
                stopVoice();
                return;
              }
              setDebugTexto('');
              reset();
              startVoiceForCard(onResult, cardId);
              timeoutRef.current = setTimeout(() => {
                timeoutRef.current = null;
                stopVoice();
              }, VOICE_TIMEOUT_MS);
            }}
            className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full border text-xs font-semibold transition-all shadow-sm ${
              !supported
                ? 'border-white/10 text-slate-600 cursor-not-allowed bg-black/20'
                : isListening
                ? 'border-emerald-400 bg-emerald-500/15 text-emerald-100 shadow-[0_0_20px_rgba(16,185,129,0.5)]'
                : 'border-white/20 bg-white/10 text-slate-50 hover:border-purple-400/70 hover:bg-purple-500/30'
            }`}
          >
            <motion.span
              animate={
                isListening
                  ? { scale: [1, 1.2, 1], opacity: [0.8, 1, 0.8] }
                  : { scale: 1, opacity: 1 }
              }
              transition={
                isListening
                  ? { duration: 0.8, repeat: Infinity, ease: 'easeInOut' }
                  : { duration: 0.2 }
              }
              className="flex items-center justify-center"
            >
              <Mic className="w-4 h-4 mr-1" />
            </motion.span>
            {isListening ? 'Parar e ver resultado' : 'Falar'}
          </button>
          {debugTexto && (
            <span className="text-[10px] text-slate-400 truncate max-w-[60%]">
              Você disse: <span className="text-slate-200">{debugTexto}</span>
            </span>
          )}
        </div>

        {/* Overlay visual quando está escutando */}
        {isListening && (
          <motion.div
            className="pointer-events-none absolute inset-0 rounded-2xl border-2 border-emerald-400/60"
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: [0.4, 0.8, 0.4], scale: [0.96, 1, 0.96] }}
            transition={{ duration: 1, repeat: Infinity, ease: 'easeInOut' }}
          />
        )}

        {/* Feedback rápido de erro / no-support */}
        {feedback && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className={`pointer-events-none absolute inset-x-4 bottom-4 rounded-2xl px-4 py-2 text-xs font-semibold text-center ${
              feedback === 'erro'
                ? 'bg-red-500/90 text-white'
                : 'bg-amber-500/95 text-slate-900'
            }`}
          >
            {feedback === 'erro'
              ? 'Tente novamente'
              : 'Seu navegador não suporta reconhecimento de voz'}
          </motion.div>
        )}

        {error && (
          <p className="mt-2 text-[10px] text-red-400/80">
            Erro no microfone/navegador. Verifique permissões.
          </p>
        )}
      </div>
    </motion.div>
  );
}

export default function Palavras() {
  const [search, setSearch] = useState('');
  const [focused, setFocused] = useState(false);
  const [activeCardId, setActiveCardId] = useState(null);
  const [celebration, setCelebration] = useState({ show: false, isNumero: false });
  const [isPremiumUser, setIsPremiumUser] = useState(false);
  const celebrationTimerRef = useRef(null);
  const pendingOnResultRef = useRef(null);

  const handleCelebrate = useCallback((isNumero) => {
    if (celebrationTimerRef.current) clearTimeout(celebrationTimerRef.current);
    // Pequeno delay para a UI estabilizar antes de exibir (evita flicker)
    const showId = setTimeout(() => {
      setCelebration({ show: true, isNumero });
    }, 80);
    celebrationTimerRef.current = setTimeout(() => {
      celebrationTimerRef.current = null;
      clearTimeout(showId);
      setCelebration({ show: false, isNumero: false });
    }, 2580);
  }, []);

  const speech = useSpeechRecognition({
    lang: 'pt-BR',
    onResult: (text) => {
      pendingOnResultRef.current?.(text);
      pendingOnResultRef.current = null;
    },
  });

  const startVoiceForCard = useCallback((onResult, cardId) => {
    setActiveCardId(cardId);
    pendingOnResultRef.current = (text) => {
      onResult(text);
      setActiveCardId(null);
    };
    speech.startListening();
  }, [speech.startListening]);

  const stopVoiceWithClear = useCallback(() => {
    setActiveCardId(null);
    speech.stopListening();
  }, [speech.stopListening]);

  const speechProps = {
    supported: speech.supported,
    listening: speech.listening,
    activeCardId,
    error: speech.error,
    startVoiceForCard,
    stopVoice: stopVoiceWithClear,
    reset: speech.reset,
  };

  useEffect(() => {
    apiMe()
      .then((r) => setIsPremiumUser(!!r?.user?.conta_premium))
      .catch(() => setIsPremiumUser(false));
  }, []);

  useEffect(() => {
    const load = () => {
      jaVoices = window.speechSynthesis.getVoices().filter((v) => v.lang.startsWith('ja'));
    };
    load();
    window.speechSynthesis.onvoiceschanged = load;
  }, []);

  const filtered = search.trim()
    ? TODAS_PALAVRAS.filter(
        (w) =>
          w.japanese.includes(search) ||
          w.romaji.toLowerCase().includes(search.toLowerCase()) ||
          w.meaning.toLowerCase().includes(search.toLowerCase())
      )
    : TODAS_PALAVRAS;

  return (
    <div className="min-h-screen relative font-display antialiased overflow-x-hidden">
      <DojoBackground accentColor={ACCENT} />

      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="sticky top-0 z-40 bg-black/50 backdrop-blur-xl border-b border-white/[0.06]"
      >
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/index"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-widest">語彙</span>
        </div>
      </motion.header>

      {/* Hero */}
      <section className="relative pt-12 sm:pt-16 pb-8 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="relative inline-block"
          >
            <span
              className="font-jp text-6xl sm:text-8xl font-bold block bg-clip-text text-transparent"
              style={{
                backgroundImage: `linear-gradient(135deg, #fff 0%, rgba(167,139,250,0.9) 50%, rgba(124,58,237,0.8) 100%)`,
                textShadow: '0 0 60px rgba(124,58,237,0.3)',
              }}
            >
              語彙
            </span>
            <motion.div
              className="absolute -inset-4 rounded-3xl opacity-20 blur-2xl -z-10"
              animate={{
                opacity: [0.15, 0.25, 0.15],
                scale: [1, 1.05, 1],
              }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              style={{ background: `radial-gradient(circle, ${ACCENT} 0%, transparent 70%)` }}
            />
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-2xl sm:text-3xl font-bold text-white mt-4 mb-2"
          >
            Vocabulário do Judô
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-slate-400 text-sm sm:text-base max-w-md mx-auto"
          >
            Aprenda a pronúncia de cada palavra — clique nos cards para ouvir em japonês
          </motion.p>

          {/* Search - enhanced */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-8 max-w-xl mx-auto relative"
          >
            <div
              className={`absolute inset-0 rounded-2xl blur-xl transition-opacity duration-300 ${
                focused ? 'opacity-40' : 'opacity-0'
              }`}
              style={{
                background: `linear-gradient(135deg, ${ACCENT}40, transparent)`,
              }}
            />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              placeholder="Buscar por palavra, romaji ou tradução..."
              className="relative w-full px-5 py-4 pr-28 rounded-2xl bg-white/[0.05] border border-white/10 text-white placeholder-slate-500 focus:border-purple-500/50 focus:ring-2 focus:ring-purple-500/25 outline-none transition-all duration-300"
            />
            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs sm:text-sm tabular-nums">
              {filtered.length}
            </span>
          </motion.div>
        </div>
      </section>

      {/* Seção Números do Judô */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-5xl mx-auto px-4 mb-12"
      >
        <h2 className="font-jp text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-5 rounded-full bg-purple-500" />
          数字 — Números do Judô
        </h2>
        <p className="text-slate-500 text-sm mb-4">
          Contagem usada nos treinos e competições
        </p>
        <div className="flex flex-wrap gap-3 sm:gap-4">
          {NUMEROS_JUDO.map((n, i) => (
            <motion.div
              key={`${n.kanji}-${n.num}`}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.03 }}
            >
              <NumeroCard n={n} cardId={`num-${n.num}`} speechProps={speechProps} onCelebrate={handleCelebrate} />
            </motion.div>
          ))}
        </div>
      </motion.section>

      {!isPremiumUser && (
        <div className="max-w-5xl mx-auto px-4 mb-8">
          <div className="rounded-2xl border border-amber-400/40 bg-amber-500/10 p-4 text-amber-100">
            Modo gratis: somente a secao de numeros esta liberada. O restante do vocabulario e Premium.
          </div>
        </div>
      )}

      {/* Grid de palavras */}
      <div className="max-w-5xl mx-auto px-4 pb-32">
        <h2 className="font-jp text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-5 rounded-full bg-amber-500/80" />
          用語 — Vocabulário
        </h2>
        {isPremiumUser ? (
          <>
            <motion.div
              className="grid gap-4 sm:gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
              layout
            >
              {filtered.map((w, i) => (
                <WordCard key={`${w.japanese}-${w.meaning}-${i}`} w={w} index={i} cardId={`${w.japanese}-${w.meaning}-${i}`} speechProps={speechProps} onCelebrate={handleCelebrate} />
              ))}
            </motion.div>
            {filtered.length === 0 && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-slate-500 text-center py-20 text-lg"
              >
                Nenhuma palavra encontrada.
              </motion.p>
            )}
          </>
        ) : (
          <div className="rounded-2xl border border-white/15 bg-white/5 p-8 text-center">
            <div className="text-5xl mb-2">🔒</div>
            <p className="text-white text-lg font-semibold mb-2">Vocabulário completo bloqueado</p>
            <p className="text-slate-400 mb-5">Desbloqueie todas as palavras e pronuncias com o plano Premium.</p>
            <Link to="/payments/planos" className="inline-block px-6 py-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-black font-semibold transition-colors">
              Desbloquear Premium
            </Link>
          </div>
        )}
      </div>

      {/* Celebração via portal no body — isolada dos re-renders da página */}
      {typeof document !== 'undefined' &&
        createPortal(
          <AnimatePresence mode="wait">
            {celebration.show && (
              <CelebraçãoAcerto
                key="celebration"
                onClose={() => {
                  if (celebrationTimerRef.current) clearTimeout(celebrationTimerRef.current);
                  celebrationTimerRef.current = null;
                  setCelebration({ show: false, isNumero: false });
                }}
                isNumero={celebration.isNumero}
              />
            )}
          </AnimatePresence>,
          document.body
        )}

      {/* Floating accent orbs - desktop only */}
      <div className="hidden lg:block fixed inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute top-1/4 -right-32 w-96 h-96 rounded-full opacity-20 blur-3xl"
          style={{ background: ACCENT }}
        />
        <div
          className="absolute bottom-1/4 -left-32 w-80 h-80 rounded-full opacity-15 blur-3xl"
          style={{ background: 'rgb(16,185,129)' }}
        />
      </div>
    </div>
  );
}
