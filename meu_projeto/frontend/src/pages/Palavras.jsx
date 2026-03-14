import { useState, useCallback, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Volume2 } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { BELT_DATA } from '../data/palavrasData';

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

function NumeroCard({ n }) {
  const [playing, setPlaying] = useState(false);
  const handleClick = useCallback(() => {
    setPlaying(true);
    speakJapanese(n.speak || n.kanji);
    setTimeout(() => setPlaying(false), 800);
  }, [n.speak, n.kanji]);

  return (
    <motion.button
      onClick={handleClick}
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.95 }}
      className={`flex flex-col items-center justify-center rounded-xl p-4 min-w-[72px] transition-all ${
        playing
          ? 'bg-emerald-500/25 ring-2 ring-emerald-400/50'
          : 'bg-white/[0.05] border border-white/10 hover:bg-white/[0.1] hover:border-purple-500/30'
      }`}
    >
      <span className="font-jp text-2xl font-bold text-white">{n.kanji}</span>
      <span className="text-slate-400 text-xs font-mono mt-0.5">{n.romaji}</span>
      <span className="text-amber-400/90 text-sm font-semibold mt-0.5">{n.num}</span>
      {n.desc && <span className="text-slate-500 text-[10px] mt-0.5">{n.desc}</span>}
    </motion.button>
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

function WordCard({ w, index }) {
  const [playing, setPlaying] = useState(false);
  const kanji = w.japanese.replace(/\s*\([^)]*\)/g, '').trim();
  const textToSpeak = w.speak || kanji || w.romaji;

  const handleClick = useCallback(() => {
    setPlaying(true);
    speakJapanese(textToSpeak);
    setTimeout(() => setPlaying(false), 1200);
  }, [textToSpeak]);

  return (
    <motion.button
      initial={{ opacity: 0, y: 24, scale: 0.96 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ delay: Math.min(index * 0.02, 0.4), type: 'spring', stiffness: 280, damping: 22 }}
      whileHover={{ y: -6, scale: 1.02, transition: { duration: 0.2 } }}
      whileTap={{ scale: 0.97 }}
      onClick={handleClick}
      className="relative w-full text-left rounded-2xl overflow-hidden group"
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
        <p className="relative text-slate-500/80 text-xs mt-3 font-medium">Toque para ouvir</p>
      </div>
    </motion.button>
  );
}

export default function Palavras() {
  const [search, setSearch] = useState('');
  const [focused, setFocused] = useState(false);

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
              <NumeroCard n={n} />
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Grid de palavras */}
      <div className="max-w-5xl mx-auto px-4 pb-32">
        <h2 className="font-jp text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-5 rounded-full bg-amber-500/80" />
          用語 — Vocabulário
        </h2>
        <motion.div
          className="grid gap-4 sm:gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
          layout
        >
          {filtered.map((w, i) => (
            <WordCard key={`${w.japanese}-${w.meaning}-${i}`} w={w} index={i} />
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
      </div>

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
