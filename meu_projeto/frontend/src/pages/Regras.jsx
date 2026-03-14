import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { ArrowLeft, X, ChevronRight } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import ScrollReveal from '../components/ScrollReveal';

const ACCENT = 'rgb(245, 158, 11)'; // amber

const SECTIONS = [
  { id: 'kimono', label: 'Kimono', emoji: '🥋', color: 'rgb(5, 150, 105)' },
  { id: 'regras', label: 'Regras da Luta', emoji: '⚔️', color: 'rgb(245, 158, 11)' },
  { id: 'pontuacoes', label: 'Pontuações', emoji: '🏆', color: 'rgb(34, 197, 94)' },
  { id: 'punicoes', label: 'Punições', emoji: '⚠️', color: 'rgb(239, 68, 68)' },
  { id: 'tecnicas', label: 'Técnicas', emoji: '🥋', color: 'rgb(124, 58, 237)' },
  { id: 'dicas', label: 'Dicas', emoji: '💡', color: 'rgb(59, 130, 246)' },
];

function RuleCard({ title, icon, children, onClick, borderColor }) {
  return (
    <motion.div
      whileHover={{ y: -3, transition: { duration: 0.2 } }}
      onClick={onClick}
      className="relative rounded-xl border border-white/[0.06] bg-white/[0.03] backdrop-blur-sm p-5 cursor-pointer overflow-hidden group transition-colors min-h-[100px] flex flex-col justify-center"
      style={{ borderLeftWidth: '3px', borderLeftColor: borderColor }}
    >
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity" style={{ background: `linear-gradient(135deg, ${borderColor}06 0%, transparent 60%)` }} />
      <div className="relative flex items-center gap-4">
        <div className="w-11 h-11 rounded-lg flex items-center justify-center shrink-0 text-xl" style={{ backgroundColor: `${borderColor}18` }}>
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-white text-base mb-1">{title}</h4>
          <div className="text-slate-500 text-[13px] leading-relaxed">{children}</div>
        </div>
        <ChevronRight className="w-4 h-4 text-slate-600 group-hover:translate-x-0.5 transition-transform shrink-0" />
      </div>
    </motion.div>
  );
}

function Modal({ open, onClose, title, children }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
            className="fixed top-[5vh] left-3 right-3 bottom-[5vh] sm:inset-6 md:inset-auto md:left-1/2 md:top-1/2 md:right-auto md:bottom-auto md:-translate-x-1/2 md:-translate-y-1/2 md:max-w-2xl md:w-full md:max-h-[85vh] overflow-y-auto z-50 rounded-2xl border border-white/10 bg-[#0f1115] shadow-2xl"
          >
            <div className="sticky top-0 bg-[#0f1115]/95 backdrop-blur border-b border-white/10 px-4 sm:px-6 py-3 sm:py-4 flex items-center justify-between shrink-0">
              <h3 className="text-lg sm:text-xl font-bold text-white pr-2">{title}</h3>
              <button onClick={onClose} className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-4 sm:p-6 text-slate-300 text-sm sm:text-base">{children}</div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

export default function Regras() {
  const [modal, setModal] = useState(null);
  const [activeSection, setActiveSection] = useState('kimono');
  const { scrollYProgress } = useScroll();
  const headerOpacity = useTransform(scrollYProgress, [0, 0.1], [1, 0.9]);

  useEffect(() => {
    const onEscape = (e) => { if (e.key === 'Escape') setModal(null); };
    window.addEventListener('keydown', onEscape);
    return () => window.removeEventListener('keydown', onEscape);
  }, []);

  useEffect(() => {
    const handler = () => {
      const sections = SECTIONS.map((s) => ({ id: s.id, el: document.getElementById(s.id) })).filter((s) => s.el);
      const scrollY = window.scrollY + 120;
      for (let i = sections.length - 1; i >= 0; i--) {
        const top = sections[i].el?.offsetTop ?? 0;
        if (scrollY >= top) {
          setActiveSection(sections[i].id);
          break;
        }
      }
    };
    handler();
    window.addEventListener('scroll', handler);
    return () => window.removeEventListener('scroll', handler);
  }, []);

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      {/* Header */}
      <motion.header style={{ opacity: headerOpacity }} className="fixed top-0 left-0 right-0 z-40">
        <div className="bg-black/40 backdrop-blur-xl border-b border-white/10">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link
              to="/index"
              className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition-all"
            >
              <ArrowLeft className="w-4 h-4" /> Voltar
            </Link>
            <span className="font-jp text-slate-500 text-sm tracking-wider">規則 — Regras</span>
          </div>
        </div>
      </motion.header>

      {/* Hero */}
      <section className="pt-24 pb-16 px-4">
        <div className="max-w-5xl mx-auto text-center">
          <motion.span
            className="font-jp text-5xl sm:text-6xl font-bold block text-white/95 mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            規則
          </motion.span>
          <motion.h1
            className="text-3xl sm:text-4xl font-bold text-white mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.6 }}
          >
            Regras de Competição
          </motion.h1>
          <motion.p
            className="text-slate-400 text-lg max-w-xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            Conheça as regras essenciais da IJF para competições de judô.
          </motion.p>
        </div>
      </section>

      {/* Spacer para o nav fixo no mobile */}
      <div className="h-16 sm:h-14 md:hidden" aria-hidden />
      <div className="fixed md:sticky top-[57px] left-0 right-0 z-30 py-3 px-4 bg-black/40 backdrop-blur-xl border-b border-white/5 md:bg-black/30 md:backdrop-blur-lg">
        <div className="max-w-5xl mx-auto flex flex-wrap justify-center gap-2">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              onClick={() => scrollTo(s.id)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                activeSection === s.id ? 'text-white' : 'text-slate-500 hover:text-slate-300'
              }`}
              style={{
                backgroundColor: activeSection === s.id ? `${s.color}25` : 'transparent',
                borderColor: activeSection === s.id ? `${s.color}50` : 'transparent',
                borderWidth: '1px',
              }}
            >
              <span className="mr-1.5">{s.emoji}</span>
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-24 pt-8 space-y-16">
        {/* Intro */}
        <ScrollReveal direction="up" delay={0.1}>
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-center">
            <p className="text-slate-400 leading-relaxed">
              As competições de judô seguem regras rigorosas da <strong className="text-white">Federação Internacional de Judô (IJF)</strong>.
              Conheça kimono, técnicas permitidas, punições e mais.
            </p>
          </div>
        </ScrollReveal>

        {/* Kimono */}
        <section id="kimono">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(5,150,105,0.2)' }}>🥋</span>
              袴 — Regras do Kimono
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              <RuleCard title="Tamanhos" icon="📏" borderColor="rgb(5, 150, 105)" onClick={() => setModal('kimono-tamanhos')}>
                <p>Masculino: 1–5 • Feminino: F1–F4 • Infantil: I1–I4</p>
              </RuleCard>
              <RuleCard title="Material" icon="🧵" borderColor="rgb(5, 150, 105)" onClick={() => setModal('kimono-material')}>
                <p>100% algodão, mínimo 700g. Cor branca ou azul</p>
              </RuleCard>
              <RuleCard title="Medidas" icon="📐" borderColor="rgb(5, 150, 105)" onClick={() => setModal('kimono-medidas')}>
                <p>Manga 5–7 cm do pulso • Calça 5–7 cm do tornozelo</p>
              </RuleCard>
            </div>
            <div className="grid gap-4 mt-5 sm:grid-cols-2">
              <RuleCard title="Permitido" icon="✓" borderColor="rgb(34, 197, 94)" onClick={() => setModal('kimono-permitido')}>
                <p>Kimono limpo e bem passado</p>
                <p>Faixa 4–5 cm • Camiseta branca por baixo</p>
              </RuleCard>
              <RuleCard title="Proibido" icon="✕" borderColor="rgb(239, 68, 68)" onClick={() => setModal('kimono-proibido')}>
                <p>Kimono rasgado ou sujo</p>
                <p>Faixa incorreta • Roupas coloridas por baixo</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Regras da Luta */}
        <section id="regras">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(245,158,11,0.2)' }}>⚔️</span>
              試合 — Regras da Luta
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <RuleCard title="Área de Combate" icon="⬜" borderColor={ACCENT} onClick={() => setModal('regras-area')}>
                <p>Tatame 8×8 m • Área segura 3 m • Verde ou azul</p>
              </RuleCard>
              <RuleCard title="Duração" icon="⏱" borderColor={ACCENT} onClick={() => setModal('regras-duracao')}>
                <p>Sênior/Júnior: 4 min • Cadete: 3 • Infantil: 2 min</p>
              </RuleCard>
              <RuleCard title="Golden Score" icon="⭐" borderColor={ACCENT} onClick={() => setModal('regras-golden')}>
                <p>Empate → primeiro ponto vence. Sem limite de tempo</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Pontuações em Tachi-waza */}
        <section id="pontuacoes">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(34,197,94,0.2)' }}>🏆</span>
              立技 — Pontuações em Tachi-waza
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <RuleCard title="Ippon" icon="🥇" borderColor="rgb(34, 197, 94)" onClick={() => setModal('pont-ippon')}>
                <p>Velocidade, força, de costas, controle. Ponte = ippon</p>
              </RuleCard>
              <RuleCard title="Waza-ari" icon="🥈" borderColor="rgb(234, 179, 8)" onClick={() => setModal('pont-wazaari')}>
                <p>Queda &gt;90° do ombro. 2 waza-ari = ippon</p>
              </RuleCard>
              <RuleCard title="Yuko" icon="🥉" borderColor="rgb(148, 163, 184)" onClick={() => setModal('pont-yuko')}>
                <p>Contados (1, 2, 3...). Infinitos yuko &lt; 1 waza-ari</p>
              </RuleCard>
            </div>
            <div className="grid gap-4 mt-5 sm:grid-cols-2">
              <RuleCard title="Kumikata (Romper)" icon="✋" borderColor="rgb(59, 130, 246)" onClick={() => setModal('pont-kumikata')}>
                <p>1 mão sem manter = ok • 2 mãos sem manter = shido</p>
              </RuleCard>
              <RuleCard title="Kumikata (Zonas)" icon="✋" borderColor="rgb(59, 130, 246)" onClick={() => setModal('pont-kumikata-zonas')}>
                <p>Wagi, manga, calças — permitido/proibido por situação</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Punições */}
        <section id="punicoes">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(239,68,68,0.2)' }}>⚠️</span>
              罰則 — Punições
            </h2>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 xl:grid-cols-4">
              <RuleCard title="Shido (Leves)" icon="🟡" borderColor="rgb(234, 179, 8)" onClick={() => setModal('shido')}>
                <p>Passividade, sair da área, agarrar perna. 3 shidos = desqualificação</p>
              </RuleCard>
              <RuleCard title="Perda de Tempo" icon="⏱" borderColor="rgb(234, 179, 8)" onClick={() => setModal('perda-tempo')}>
                <p>1ª vez: advertência. 2ª vez: shido</p>
              </RuleCard>
              <RuleCard title="Abraço de Urso" icon="🐻" borderColor="rgb(234, 179, 8)" onClick={() => setModal('abraco-urso')}>
                <p>Sem kumikata + mãos em círculo = shido</p>
              </RuleCard>
              <RuleCard title="Hansoku-make (Graves)" icon="🔴" borderColor="rgb(239, 68, 68)" onClick={() => setModal('hansoku')}>
                <p>Golpes, chutes, morder. Desqualificação imediata</p>
              </RuleCard>
            </div>
            <div className="grid gap-4 mt-5 sm:grid-cols-2 lg:grid-cols-3">
              <RuleCard title="Saída de Área" icon="🚪" borderColor="rgb(234, 179, 8)" onClick={() => setModal('saida-area')}>
                <p>Tachi-waza ou ne-waza: sair intencionalmente = shido</p>
              </RuleCard>
              <RuleCard title="Gestos Religiosos" icon="⛔" borderColor="rgb(239, 68, 68)" onClick={() => setModal('gestos-religiosos')}>
                <p>Religioso, político, pessoal ou comercial = proibido</p>
              </RuleCard>
              <RuleCard title="Atendimento Médico" icon="🏥" borderColor="rgb(59, 130, 246)" onClick={() => setModal('atendimento-medico')}>
                <p>2 ocasiões • 3ª vez = kiken-gachi</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Técnicas */}
        <section id="tecnicas">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(124,58,237,0.2)' }}>🥋</span>
              技 — Técnicas
            </h2>
            <div className="grid gap-4 sm:grid-cols-2">
              <RuleCard title="Permitidas" icon="✓" borderColor="rgb(34, 197, 94)" onClick={() => setModal('tecnicas-permitidas')}>
                <p>Nage-waza, Katame-waza. Te, Ashi, Koshi, Sutemi-waza</p>
              </RuleCard>
              <RuleCard title="Proibidas" icon="✕" borderColor="rgb(239, 68, 68)" onClick={() => setModal('tecnicas-proibidas')}>
                <p>Golpes mão fechada, chutes, Kawazu-gake, pescoço perigoso</p>
              </RuleCard>
            </div>
            <div className="grid gap-4 mt-5 sm:grid-cols-2">
              <RuleCard title="Osae-waza" icon="📌" borderColor="rgb(124, 58, 237)" onClick={() => setModal('osae-waza')}>
                <p>Controle só em cabeça/pescoço sem braço = Mate! ou Shido!</p>
              </RuleCard>
              <RuleCard title="Por Categoria de Idade" icon="👥" borderColor="rgb(124, 58, 237)" onClick={() => setModal('tecnicas-categorias')}>
                <p>Infantis: proibido finalização • Adultos: todas</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Dicas */}
        <section id="dicas">
          <ScrollReveal direction="up">
            <h2 className="font-jp text-xl sm:text-2xl font-bold text-white mb-5 flex items-center gap-3">
              <span className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ backgroundColor: 'rgba(59,130,246,0.2)' }}>💡</span>
              ポイント — Dicas
            </h2>
            <div className="grid gap-4 sm:grid-cols-3">
              <RuleCard title="Mental" icon="🧠" borderColor="rgb(59, 130, 246)" onClick={() => setModal('dica-mental')}>
                <p>Calma, respire, confie no treino</p>
              </RuleCard>
              <RuleCard title="Físico" icon="💪" borderColor="rgb(59, 130, 246)" onClick={() => setModal('dica-fisico')}>
                <p>Condicionamento, força, resistência</p>
              </RuleCard>
              <RuleCard title="Técnica" icon="📖" borderColor="rgb(59, 130, 246)" onClick={() => setModal('dica-tecnica')}>
                <p>Domine 2–3 técnicas perfeitamente</p>
              </RuleCard>
            </div>
          </ScrollReveal>
        </section>

        {/* Fonte */}
        <ScrollReveal direction="up">
          <div className="mt-12 pt-8 border-t border-white/5 text-center">
            <p className="text-slate-500 text-sm">Fonte: Seminário Técnico Nacional de Judô</p>
            <p className="text-slate-600 text-xs mt-1">01 e 02 de fevereiro de 2026</p>
          </div>
        </ScrollReveal>
      </div>

      {/* Modais */}
      <Modal open={modal === 'kimono-tamanhos'} onClose={() => setModal(null)} title="Tamanhos do Kimono">
        <ul className="space-y-2">
          <li><strong className="text-white">Masculino:</strong> 1, 2, 3, 4, 5</li>
          <li><strong className="text-white">Feminino:</strong> F1, F2, F3, F4</li>
          <li><strong className="text-white">Infantil:</strong> I1, I2, I3, I4</li>
        </ul>
      </Modal>
      <Modal open={modal === 'kimono-material'} onClose={() => setModal(null)} title="Material do Judogi">
        <ul className="space-y-2">
          <li>• 100% algodão</li>
          <li>• Peso mínimo: 700g</li>
          <li>• Cor: branca ou azul</li>
        </ul>
      </Modal>
      <Modal open={modal === 'kimono-medidas'} onClose={() => setModal(null)} title="Medidas do Kimono">
        <ul className="space-y-2">
          <li>• <strong className="text-white">Manga:</strong> 5–7 cm do pulso</li>
          <li>• <strong className="text-white">Calça:</strong> 5–7 cm do tornozelo</li>
          <li>• <strong className="text-white">Largura:</strong> 10–15 cm do corpo</li>
        </ul>
      </Modal>
      <Modal open={modal === 'kimono-permitido'} onClose={() => setModal(null)} title="O que é Permitido">
        <ul className="space-y-2 text-green-300/90">
          <li>• Kimono limpo e bem passado</li>
          <li>• Faixa (obi) de 4–5 cm de largura</li>
          <li>• Camiseta branca por baixo (opcional)</li>
          <li>• Calcinha/short branco por baixo</li>
        </ul>
      </Modal>
      <Modal open={modal === 'kimono-proibido'} onClose={() => setModal(null)} title="O que é Proibido">
        <ul className="space-y-2 text-red-300/90">
          <li>• Kimono rasgado ou sujo</li>
          <li>• Faixa muito longa ou curta</li>
          <li>• Camiseta colorida por baixo</li>
          <li>• Calcinha/short colorido</li>
        </ul>
      </Modal>
      <Modal open={modal === 'regras-area'} onClose={() => setModal(null)} title="Área de Combate">
        <ul className="space-y-2">
          <li>• <strong className="text-white">Tatame:</strong> 8×8 metros</li>
          <li>• <strong className="text-white">Área segura:</strong> 3 metros</li>
          <li>• <strong className="text-white">Cor:</strong> verde ou azul</li>
        </ul>
      </Modal>
      <Modal open={modal === 'regras-duracao'} onClose={() => setModal(null)} title="Duração das Lutas">
        <ul className="space-y-2">
          <li>• <strong className="text-white">Sênior e Júnior:</strong> 4 minutos</li>
          <li>• <strong className="text-white">Cadete:</strong> 3 minutos</li>
          <li>• <strong className="text-white">Infantil:</strong> 2 minutos</li>
        </ul>
      </Modal>
      <Modal open={modal === 'regras-golden'} onClose={() => setModal(null)} title="Golden Score">
        <p className="mb-4">Em caso de empate ao final do tempo regulamentar:</p>
        <ul className="space-y-2">
          <li>• O primeiro ponto vence a luta</li>
          <li>• Não há limite de tempo no Golden Score</li>
        </ul>
      </Modal>
      <Modal open={modal === 'pont-ippon'} onClose={() => setModal(null)} title="Ippon — Tachi-waza">
        <p className="mb-4 text-emerald-300/90 font-medium">Critérios para ippon:</p>
        <ul className="space-y-2 mb-6">
          <li>• <strong className="text-white">Velocidade</strong> na execução</li>
          <li>• <strong className="text-white">Força</strong> no arremesso</li>
          <li>• Adversário cai <strong className="text-white">de costas</strong></li>
          <li>• <strong className="text-white">Controle habilidoso</strong> até o fim da aterrissagem</li>
        </ul>
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <p className="text-emerald-300 font-semibold">🌉 Ponte = Ippon</p>
          <p className="text-sm mt-2 text-slate-400">
            Sempre que o atleta fizer ponte (cabeça e um pé ou dois pés no tatami) será declarado ippon.
          </p>
        </div>
      </Modal>
      <Modal open={modal === 'pont-wazaari'} onClose={() => setModal(null)} title="Waza-ari — Tachi-waza">
        <p className="mb-4 text-amber-300/90">Queda que vale waza-ari:</p>
        <ul className="space-y-2 mb-6">
          <li>• Aterrissagem a <strong className="text-white">mais de 90°</strong> do eixo do ombro</li>
          <li>• Mas <strong className="text-white">não totalmente de costas</strong></li>
        </ul>
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
          <p className="text-amber-300 font-semibold">🥇 Waza-ari-awasete-ippon</p>
          <p className="text-sm mt-2 text-slate-400">
            Dois waza-ari somam e equivalem a um ippon — fim da luta.
          </p>
        </div>
      </Modal>
      <Modal open={modal === 'pont-yuko'} onClose={() => setModal(null)} title="Yuko — Tachi-waza">
        <p className="mb-4 text-slate-300">Situações que valem yuko:</p>
        <ul className="space-y-2 mb-4">
          <li>• Queda <strong className="text-white">lateral</strong> em 90° ou mais em relação à queda frontal</li>
          <li>• Queda na <strong className="text-white">parte superior das costas</strong></li>
          <li>• Queda sobre a <strong className="text-white">nuca</strong></li>
          <li>• Queda lateral no eixo do ombro + um cotovelo ou uma mão no tatami</li>
          <li>• Queda com uma das nádegas (com ou sem cotovelos/braços no tatami)</li>
        </ul>
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 mb-4">
          <p className="text-red-300 font-semibold">✕ Não será yuko</p>
          <p className="text-sm mt-2 text-slate-400">
            Se o abdômen, quadril ou joelhos tocarem o tatami <strong className="text-white">antes</strong> da lateral das costas.
          </p>
        </div>
        <div className="p-4 rounded-xl bg-slate-500/10 border border-slate-500/20 space-y-2">
          <p className="text-slate-300"><strong>Regra:</strong> Yukos são contados (1, 2, 3...)</p>
          <p className="text-slate-300"><strong>Mas não somam</strong> para waza-ari</p>
          <p className="text-amber-400 font-semibold mt-2">⚠️ Infinitos yuko são inferiores a um waza-ari</p>
        </div>
      </Modal>
      <Modal open={modal === 'pont-kumikata'} onClose={() => setModal(null)} title="Kumikata — Romper a Pegada">
        <ul className="space-y-3">
          <li className="flex gap-3">
            <span className="text-emerald-400 font-bold">a)</span>
            <span>Romper com uma ou duas mãos, mantendo <strong className="text-white">pelo menos uma pegada</strong> — permitido.</span>
          </li>
          <li className="flex gap-3">
            <span className="text-emerald-400 font-bold">b)</span>
            <span>Romper com <strong className="text-white">uma mão</strong> e NÃO manter a pegada — permitido.</span>
          </li>
          <li className="flex gap-3">
            <span className="text-amber-400 font-bold">c)</span>
            <span>Romper com <strong className="text-white">duas mãos</strong> e NÃO manter a pegada = <span className="text-amber-400 font-semibold">shido</span>.</span>
          </li>
        </ul>
      </Modal>
      <Modal open={modal === 'pont-kumikata-zonas'} onClose={() => setModal(null)} title="Kumikata — Zonas da Pegada">
        <p className="mb-3 text-emerald-300/90 font-medium">Permitido:</p>
        <p className="text-slate-400 text-sm mb-4">Pegadas no wagi e abaixo da faixa até o nível da parte superior da coxa.</p>
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mb-4">
          <p className="text-amber-300 font-semibold">Shido:</p>
          <p className="text-sm mt-2 text-slate-400">Kumikata negativo abaixo da faixa e na parte superior interna das coxas.</p>
        </div>
        <div className="space-y-4">
          <div>
            <p className="text-white font-medium mb-2">Tachi-waza:</p>
            <ul className="text-sm space-y-1 text-slate-400">
              <li>• <span className="text-emerald-400">Permitido</span> agarrar dentro da manga (tori e uke)</li>
              <li>• <span className="text-red-400">Proibido</span> agarrar por dentro das calças (parte inferior) = shido</li>
            </ul>
          </div>
          <div>
            <p className="text-white font-medium mb-2">Ne-waza:</p>
            <ul className="text-sm space-y-1 text-slate-400">
              <li>• <span className="text-emerald-400">Permitido</span> agarrar dentro da manga</li>
              <li>• <span className="text-emerald-400">Permitido</span> agarrar por dentro das calças</li>
            </ul>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'saida-area'} onClose={() => setModal(null)} title="Saída de Área">
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <p className="text-amber-300 font-semibold mb-2">Tachi-waza</p>
            <p className="text-sm text-slate-400">Quem sair intencionalmente da área (com ou sem kumikata) = <strong className="text-white">shido</strong> (recomendação IJF).</p>
          </div>
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <p className="text-amber-300 font-semibold mb-2">Ne-waza</p>
            <p className="text-sm text-slate-400">Quem sair intencionalmente da área = <strong className="text-white">shido</strong>.</p>
          </div>
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <p className="text-emerald-300 font-semibold mb-2">Validação</p>
            <p className="text-sm text-slate-400">Ações que iniciarem dentro da área (um atleta em contato com a área) devem ser validadas. Se ne-waza começar dentro e sair com ação contínua, pode ser válido.</p>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'gestos-religiosos'} onClose={() => setModal(null)} title="Gestos Religiosos e Proibidos">
        <p className="text-slate-400 mb-4">Qualquer manifestação ou conotação de caráter religioso, político, pessoal ou comercial é <strong className="text-red-400">proibida</strong> para todos dentro do shiai-jo (área de competição).</p>
      </Modal>
      <Modal open={modal === 'osae-waza'} onClose={() => setModal(null)} title="Osae-waza — Recomendação">
        <p className="mb-4 text-slate-400">Não é permitido manter osae-waza apenas ao redor da cabeça/pescoço sem o controle de pelo menos um dos braços do adversário.</p>
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <p className="text-amber-300 font-medium">Braços ao redor do pescoço</p>
            <p className="text-sm mt-2 text-slate-400">Controle em ne-waza com braços ao redor do pescoço, sem o braço do adversário por dentro = <strong className="text-white">&quot;Mate!&quot;</strong>.</p>
          </div>
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <p className="text-amber-300 font-medium">Pernas ao redor do pescoço</p>
            <p className="text-sm mt-2 text-slate-400">Controle em ne-waza com pernas ao redor do pescoço, sem o braço do adversário por dentro = <strong className="text-white">&quot;Mate!&quot;</strong> e <strong className="text-amber-400">&quot;Shido!&quot;</strong>.</p>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'shido'} onClose={() => setModal(null)} title="Shido (Penalidades Leves)">
        <p className="mb-3 text-amber-300/90 font-medium">Shido por falta de combatividade:</p>
        <p className="text-slate-400 text-sm mb-4">Serão considerados ataques em <strong className="text-white">tachi-waza</strong> e ataques em <strong className="text-white">ne-waza</strong>.</p>
        <ul className="space-y-2 mb-4">
          <li>• Na posição em pé, após &quot;hajime!&quot; e kumikata estabelecido, <strong className="text-white">não realizar nenhum ataque</strong></li>
          <li>• Tempo entre kumikata e ataque: <strong className="text-white">30–45 segundos</strong> com progressão positiva</li>
          <li>• Penalizar atleta que não fizer kumikata convencional ou evitar kumikata do oponente</li>
          <li>• Passividade excessiva, sair da área, agarrar perna sem técnica, técnicas perigosas</li>
          <li>• Não seguir comandos do árbitro</li>
        </ul>
        <p className="text-amber-400 font-semibold">⚠️ 3 shidos = hansoku-make (desqualificação)</p>
      </Modal>
      <Modal open={modal === 'perda-tempo'} onClose={() => setModal(null)} title="Perda de Tempo">
        <p className="mb-4 text-slate-400">Perder o tempo entre &quot;mate!&quot; e &quot;hajime!&quot; por:</p>
        <ul className="space-y-2 mb-4">
          <li>• Não se levantar após a ação ne-waza</li>
          <li>• Não retornar imediatamente à posição inicial</li>
          <li>• Arrumar o cabelo, judogi ou amarrar a faixa</li>
          <li>• Ou combinação destes pontos</li>
        </ul>
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
          <p className="text-amber-300"><strong>1ª vez:</strong> advertência</p>
          <p className="text-amber-400 font-semibold mt-1"><strong>2ª vez e seguintes:</strong> shido</p>
        </div>
      </Modal>
      <Modal open={modal === 'abraco-urso'} onClose={() => setModal(null)} title="Abraço de Urso">
        <p className="mb-4 text-red-300/90 font-medium">Shido quando:</p>
        <ul className="space-y-2 mb-4">
          <li>• Sem kumikata (de uke e/ou tori), tori junta as duas mãos formando um círculo</li>
          <li>• Ou tori agarra o(s) braço(s) do oponente formando um círculo</li>
        </ul>
        <p className="mb-3 text-emerald-300/90 font-medium">Permitido:</p>
        <ul className="space-y-2 mb-4">
          <li>• Abraço direto em tachi-waza se as mãos do tori <strong className="text-white">NÃO</strong> estiverem entrelaçadas</li>
          <li>• Tori segura a própria manga com a mão oposta</li>
          <li>• Mãos entrelaçadas se tori e/ou uke <strong className="text-white">já tiverem kumikata</strong> — nenhum shido</li>
        </ul>
      </Modal>
      <Modal open={modal === 'atendimento-medico'} onClose={() => setModal(null)} title="Atendimento Médico">
        <p className="mb-4 text-slate-400">O atleta pode receber tratamento médico (sangramento leve ou grave) em <strong className="text-white">apenas duas ocasiões</strong>.</p>
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mb-4">
          <p className="text-amber-400 font-semibold">3ª vez = kiken-gachi</p>
          <p className="text-sm mt-1 text-slate-400">Oponente vence por desistência/incapacidade.</p>
        </div>
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
          <p className="text-blue-300 font-semibold text-sm">Cadetes — shime-waza</p>
          <p className="text-sm mt-2 text-slate-400">Se perder a consciência durante shime-waza, <strong className="text-red-400">NÃO poderá continuar</strong>. Se desistir (&quot;maitta!&quot;) antes de perder a consciência (com ou sem mate/ippon), poderá continuar se aplicável.</p>
        </div>
      </Modal>
      <Modal open={modal === 'hansoku'} onClose={() => setModal(null)} title="Hansoku-make (Desqualificação)">
        <p className="mb-4 text-red-300/90">Infrações graves:</p>
        <ul className="space-y-1 mb-4">
          <li>• Golpes com mão fechada</li>
          <li>• Chutes ou joelhadas</li>
          <li>• Morder, arranhar ou beliscar</li>
          <li>• Comportamento antidesportivo</li>
          <li>• Desrespeito ao árbitro</li>
          <li>• Substâncias proibidas</li>
        </ul>
        <p className="text-red-400 font-semibold">🚫 Desqualificação imediata da luta</p>
      </Modal>
      <Modal open={modal === 'tecnicas-permitidas'} onClose={() => setModal(null)} title="Técnicas Permitidas">
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-green-400 mb-2">Nage-waza (Projeções)</h4>
            <ul className="text-sm space-y-1">
              <li>• Te-waza, Ashi-waza, Koshi-waza, Sutemi-waza</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-blue-400 mb-2">Katame-waza (Controle)</h4>
            <ul className="text-sm space-y-1">
              <li>• Osae-komi (imobilizações)</li>
              <li>• Shime-waza (estrangulamentos)</li>
              <li>• Kansetsu-waza (chaves de articulação)</li>
            </ul>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'tecnicas-proibidas'} onClose={() => setModal(null)} title="Técnicas Proibidas">
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-red-400 mb-2">Golpes proibidos</h4>
            <ul className="text-sm space-y-1">
              <li>• Golpes com mão fechada, chutes, joelhadas</li>
              <li>• Cotoveladas ou cabeçadas, morder ou arranhar</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-amber-400 mb-2">Técnicas perigosas</h4>
            <ul className="text-sm space-y-1">
              <li>• Kawazu-gake, técnicas de pescoço perigosas</li>
              <li>• Chaves em articulações pequenas</li>
            </ul>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'tecnicas-categorias'} onClose={() => setModal(null)} title="Regras por Categoria">
        <div className="grid gap-6 sm:grid-cols-2">
          <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
            <h4 className="font-semibold text-purple-300 mb-2">Infantis (5–12 anos)</h4>
            <ul className="text-sm space-y-1">
              <li>• Proibidas finalizações</li>
              <li>• Foco em projeções</li>
              <li>• Tatame reduzido • 1–2,5 min</li>
            </ul>
          </div>
          <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
            <h4 className="font-semibold text-blue-300 mb-2">Adultos (13+ anos)</h4>
            <ul className="text-sm space-y-1">
              <li>• Todas as técnicas permitidas</li>
              <li>• Golden Score em empate</li>
              <li>• Duração: 3–4 min</li>
            </ul>
          </div>
        </div>
      </Modal>
      <Modal open={modal === 'dica-mental'} onClose={() => setModal(null)} title="Dica Mental">
        <p>Mantenha a calma, respire fundo e confie no seu treino. A mentalidade é fundamental para vencer!</p>
      </Modal>
      <Modal open={modal === 'dica-fisico'} onClose={() => setModal(null)} title="Dica Físico">
        <p>Treine condicionamento, força e resistência. O físico faz diferença na luta, especialmente no final!</p>
      </Modal>
      <Modal open={modal === 'dica-tecnica'} onClose={() => setModal(null)} title="Dica Técnica">
        <p>Domine 2–3 técnicas perfeitamente. É melhor ser especialista que generalista em competição!</p>
      </Modal>
    </div>
  );
}
