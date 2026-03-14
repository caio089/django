import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowLeft, ChevronDown } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import ScrollReveal from '../components/ScrollReveal';

const ACCENT = 'rgb(59, 130, 246)';

const KANO_BIO = [
  { label: 'Nome', value: 'Nasceu "Shinnosuke", posteriormente mudou para Jigoro Kano' },
  { label: 'Nascimento', value: '28.out.1860 — Mikage, Província de Settsu (atual Hyogo), Japão' },
  { label: 'Artes marciais', value: 'Praticou Tenjin Shin\'yo-Ryu e Kito-Ryu (possuía Menkyo — licença para ensinar)' },
  { label: 'Escola de judô', value: 'Em 1882, em Tóquio, criou a Kodokan, primeira escola de judô do mundo' },
  { label: 'Família', value: 'Pai: Jirosaku Mareshiba Kano | Mãe: Sadako | Esposa: Sumako' },
  { label: 'Morte', value: '04.mai.1938, de pneumonia, aos 77 anos, num navio no Oceano Pacífico' },
];

const KODOKAN_SIGNIFICADO = [
  { kanji: '講', romaji: 'Ko', desc: 'Palestra, estudo' },
  { kanji: '道', romaji: 'Do', desc: 'Caminho' },
  { kanji: '館', romaji: 'Kan', desc: 'Instituto, escola' },
];

const TIMELINE = [
  { year: '1882', title: 'Fundação do Judô', text: 'Jigoro Kano funda o Instituto Kodokan em Tóquio, criando o judô baseado em eficiência máxima e benefício mútuo.' },
  { year: '1886', title: 'Primeira Demonstração', text: 'O judô é apresentado ao público. O Kodokan vence 13 de 15 lutas contra escolas de jujutsu, provando sua eficácia.' },
  { year: '1914', title: 'Judô no Brasil', text: 'Mitsuyo Maeda, "Conde Koma", chega a Belém do Pará e funda a primeira escola de judô do país.' },
  { year: '1964', title: 'Primeira aparição olímpica', text: 'O judô faz sua primeira apresentação nos Jogos de Tóquio, como esporte de demonstração.' },
  { year: '1972', title: 'Primeiro torneio olímpico', text: 'Nos Jogos de Munique, o judô entra como esporte oficial pela primeira vez. Chiaki Ishii conquista o bronze.' },
  { year: 'Hoje', title: 'Século XXI', text: 'Milhões de praticantes no mundo. Equilíbrio entre tradição e modernidade.' },
];

const FILOSOFIA = [
  { kanji: '精力善用', nome: 'Seiryoku Zenyo', desc: 'Máxima eficiência com mínimo esforço', emoji: '⚡', text: 'A sabedoria supera a força física. O judô ensina a usar a energia do oponente contra ele.' },
  { kanji: '自他共栄', nome: 'Jita Kyoei', desc: 'Benefício mútuo e prosperidade', emoji: '🤝', text: 'O progresso vem pela cooperação e respeito mútuo. O treino beneficia ambos os parceiros.' },
  { kanji: '武士道', nome: 'Bushido', desc: 'O caminho do guerreiro', emoji: '⚔️', text: 'Honra, lealdade, coragem e respeito. O judô desenvolve o caráter e a integridade moral.' },
];

const TECNICAS = [
  { nome: 'Nage-waza', desc: 'Técnicas de Projeção', emoji: '🔄', text: 'Projeções de quadril, perna, ombro e sacrifício, demonstrando Seiryoku Zenyo.' },
  { nome: 'Katame-waza', desc: 'Técnicas de Controle', emoji: '🔒', text: 'Imobilizações, estrangulamentos e chaves. Kano manteve apenas as técnicas seguras.' },
  { nome: 'Atemi-waza', desc: 'Técnicas de Golpe', emoji: '⚡', text: 'Incluídas no judô tradicional para preservar o aspecto marcial completo.' },
];

const MEDALHAS_OLIMPICAS = [
  { ano: '1972', cidade: 'Munique (GER)', medalhas: [{ peso: '-93kg', nome: 'Chiaki Ishii', tipo: 'bronze' }] },
  { ano: '1984', cidade: 'Los Angeles (USA)', medalhas: [
    { peso: '-95kg', nome: 'Douglas Vieira', tipo: 'prata' },
    { peso: '-86kg', nome: 'Walter Carmona', tipo: 'bronze' },
    { peso: '-71kg', nome: 'Luís Onmura', tipo: 'bronze' },
  ]},
  { ano: '1988', cidade: 'Seul (KOR)', medalhas: [{ peso: '-95kg', nome: 'Aurélio Miguel', tipo: 'ouro' }] },
  { ano: '1992', cidade: 'Barcelona (ESP)', medalhas: [{ peso: '-65kg', nome: 'Rogério Sampaio', tipo: 'ouro' }] },
  { ano: '1996', cidade: 'Atlanta (USA)', medalhas: [
    { peso: '-95kg', nome: 'Aurélio Miguel', tipo: 'bronze' },
    { peso: '-65kg', nome: 'Henrique Guimarães', tipo: 'bronze' },
  ]},
  { ano: '2000', cidade: 'Sydney (AUS)', medalhas: [
    { peso: '-73kg', nome: 'Tiago Camilo', tipo: 'prata' },
    { peso: '-90kg', nome: 'Carlos Honorato', tipo: 'prata' },
  ]},
  { ano: '2004', cidade: 'Atenas (GRE)', medalhas: [
    { peso: '-73kg', nome: 'Leandro Guilheiro', tipo: 'bronze' },
    { peso: '-81kg', nome: 'Flávio Canto', tipo: 'bronze' },
  ]},
  { ano: '2008', cidade: 'Pequim (CHN)', medalhas: [
    { peso: '-57kg', nome: 'Ketleyn Quadros', tipo: 'bronze' },
    { peso: '-73kg', nome: 'Leandro Guilheiro', tipo: 'bronze' },
    { peso: '-81kg', nome: 'Tiago Camilo', tipo: 'bronze' },
  ]},
  { ano: '2012', cidade: 'Londres (GBR)', medalhas: [
    { peso: '-48kg', nome: 'Sarah Menezes', tipo: 'ouro' },
    { peso: '-78kg', nome: 'Mayra Aguiar', tipo: 'bronze' },
    { peso: '-60kg', nome: 'Felipe Kitadai', tipo: 'bronze' },
    { peso: '+100kg', nome: 'Rafael Silva', tipo: 'bronze' },
  ]},
  { ano: '2016', cidade: 'Rio de Janeiro (BRA)', medalhas: [
    { peso: '-57kg', nome: 'Rafaela Silva', tipo: 'ouro' },
    { peso: '-78kg', nome: 'Mayra Aguiar', tipo: 'bronze' },
    { peso: '+100kg', nome: 'Rafael Silva', tipo: 'bronze' },
  ]},
];

function JigoroKanoBio() {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-t border-white/10 pt-4">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 text-amber-400/90 font-semibold text-sm hover:text-amber-400 transition-colors"
      >
        <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
        Biografia
      </button>
      <motion.div
        initial={false}
        animate={{ height: open ? 'auto' : 0, opacity: open ? 1 : 0 }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="grid gap-3 mt-4 sm:grid-cols-2">
          {KANO_BIO.map((item) => (
            <div key={item.label} className="rounded-xl border border-white/10 bg-black/20 p-3">
              <p className="text-xs text-amber-400/90 font-semibold uppercase tracking-wider mb-1">{item.label}</p>
              <p className="text-slate-300 text-sm leading-relaxed">{item.value}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}

export default function Historia() {
  const { scrollYProgress } = useScroll();
  const headerOpacity = useTransform(scrollYProgress, [0, 0.1], [1, 0.9]);

  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <motion.header style={{ opacity: headerOpacity }} className="fixed top-0 left-0 right-0 z-40">
        <div className="bg-black/40 backdrop-blur-xl border-b border-white/10">
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link to="/index" className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition-all">
              <ArrowLeft className="w-4 h-4" /> Voltar
            </Link>
            <span className="font-jp text-slate-500 text-sm tracking-wider">歴史 — História</span>
          </div>
        </div>
      </motion.header>

      <section className="pt-24 pb-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.span className="font-jp text-5xl sm:text-6xl font-bold block text-white/95 mb-4" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            柔道の歴史
          </motion.span>
          <motion.h1 className="text-3xl sm:text-4xl font-bold text-white mb-4" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            História do Judô
          </motion.h1>
          <motion.p className="text-slate-400 text-lg" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
            140 anos de evolução, filosofia e tradição — 道の心
          </motion.p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 pb-24 space-y-16">
        <ScrollReveal direction="up">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-center">
            <p className="text-slate-300 leading-relaxed">
              O judô, &quot;caminho da suavidade&quot;, transcende o combate físico. Jigoro Kano criou em 1882 uma prática
              que une eficiência, respeito e harmonia. Uma filosofia de vida que inspira milhões no mundo.
            </p>
          </div>
        </ScrollReveal>

        {/* JIGORO KANO — Destaque principal */}
        <ScrollReveal direction="up">
          <div className="rounded-2xl border-2 overflow-hidden" style={{ borderColor: `${ACCENT}60`, boxShadow: `0 0 40px ${ACCENT}15` }}>
            <div className="p-6 sm:p-8" style={{ background: `linear-gradient(135deg, ${ACCENT}12 0%, transparent 60%)` }}>
              <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
                <div className="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl shrink-0" style={{ backgroundColor: `${ACCENT}25` }}>
                  🥋
                </div>
                <div>
                  <p className="font-jp text-2xl sm:text-3xl font-bold text-white">嘉納 治五郎</p>
                  <h2 className="text-xl sm:text-2xl font-bold text-white tracking-wide">JIGORO KANO</h2>
                  <p className="text-amber-400/90 font-semibold text-sm sm:text-base mt-1">CRIADOR DO JUDÔ</p>
                </div>
              </div>
              <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
                Educador japonês, poliglota e fundador do judô — uma das primeiras artes marciais japonesas a ganhar
                reconhecimento internacional. O judô foi a primeira a se tornar esporte olímpico oficial. Kano também
                foi o <strong className="text-white">primeiro membro asiático do Comitê Olímpico Internacional</strong>.
              </p>
              <JigoroKanoBio />
            </div>
          </div>
        </ScrollReveal>

        {/* KODOKAN — Destaque principal */}
        <ScrollReveal direction="up">
          <div className="rounded-2xl border-2 overflow-hidden border-amber-500/40 bg-gradient-to-br from-amber-500/5 to-transparent">
            <div className="p-6 sm:p-8">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl bg-amber-500/20">講道館</div>
                <div>
                  <h2 className="text-xl font-bold text-white">KODOKAN</h2>
                  <p className="text-amber-400/90 text-sm">Primeira escola de judô do mundo</p>
                </div>
              </div>
              <p className="text-slate-300 text-sm leading-relaxed mb-6">
                Fundada por Jigoro Kano aos 21 anos, em maio de 1882, em Tóquio, no Japão — e existe até os dias atuais.
              </p>
              <div className="grid grid-cols-3 gap-3 mb-6">
                {KODOKAN_SIGNIFICADO.map((s) => (
                  <div key={s.kanji} className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 text-center">
                    <p className="font-jp text-2xl font-bold text-amber-400/90">{s.kanji}</p>
                    <p className="text-xs text-slate-400 font-mono">{s.romaji}</p>
                    <p className="text-xs text-slate-300 mt-1">{s.desc}</p>
                  </div>
                ))}
              </div>
              <p className="text-amber-400/80 text-sm font-semibold mb-2 font-jp">Escola para estudar o caminho</p>
              <div className="space-y-4">
                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                  <h4 className="text-white font-semibold text-sm mb-2">Símbolo da Kodokan</h4>
                  <p className="text-slate-400 text-xs leading-relaxed">
                    Forma de oito lados — fio de seda, círculo vermelho, núcleo de ferro em chamas. Inspirado no
                    <strong className="text-white"> Yata-no-Kagami</strong> (espelho sagrado do relicário imperial do Japão),
                    que representa sabedoria e honestidade. &quot;O espelho de 8 mãos&quot; — símbolo de pureza, iluminação espiritual e renovação.
                  </p>
                </div>
                <p className="text-slate-400 text-xs leading-relaxed">
                  A sede da Kodokan é um local icônico para praticantes de todo o mundo — centro de ensino e pesquisa
                  dedicado à promoção e preservação do judô, tornando-se um símbolo duradouro da influência global dessa arte marcial.
                </p>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* Linha do Tempo — layout melhorado */}
        <section>
          <h2 className="font-jp text-xl font-bold text-white mb-8 flex items-center gap-2">
            <span className="w-1 h-6 rounded-full" style={{ backgroundColor: ACCENT }} /> Linha do Tempo
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {TIMELINE.map((t, i) => (
              <motion.div
                key={t.year}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                whileHover={{ y: -4 }}
                className="rounded-xl border border-white/10 bg-white/[0.03] p-5 hover:border-white/20 transition-colors cursor-default"
              >
                <span className="text-xs font-bold px-2 py-1 rounded-lg text-white" style={{ backgroundColor: `${ACCENT}50` }}>
                  {t.year}
                </span>
                <h3 className="text-base font-bold text-white mt-3 mb-1">{t.title}</h3>
                <p className="text-slate-500 text-xs leading-relaxed">{t.text}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Filosofia — cards interativos */}
        <section>
          <h2 className="font-jp text-xl font-bold text-white mb-8 flex items-center gap-2">
            <span className="w-1 h-6 rounded-full" style={{ backgroundColor: ACCENT }} /> Filosofia do Judô
          </h2>
          <div className="grid gap-6 sm:grid-cols-3">
            {FILOSOFIA.map((f) => (
              <motion.div
                key={f.nome}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                whileHover={{ y: -6, transition: { duration: 0.2 } }}
                className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 group hover:border-white/20 hover:bg-white/[0.05] transition-all cursor-default"
                style={{ borderTopWidth: '3px', borderTopColor: ACCENT }}
              >
                <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">{f.emoji}</div>
                <p className="font-jp text-xl font-bold text-white mb-1">{f.kanji}</p>
                <h3 className="text-lg font-semibold text-white/90">{f.nome}</h3>
                <p className="text-amber-400/90 text-sm mb-3">{f.desc}</p>
                <p className="text-slate-400 text-sm leading-relaxed">{f.text}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Técnicas — layout em grid */}
        <section>
          <h2 className="font-jp text-xl font-bold text-white mb-8 flex items-center gap-2">
            <span className="w-1 h-6 rounded-full" style={{ backgroundColor: ACCENT }} /> Técnicas Históricas
          </h2>
          <div className="grid gap-6 sm:grid-cols-3">
            {TECNICAS.map((t) => (
              <motion.div
                key={t.nome}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 hover:border-white/15 transition-colors"
              >
                <div className="text-2xl mb-3">{t.emoji}</div>
                <h3 className="font-jp font-bold text-white">{t.nome}</h3>
                <p className="text-amber-400/90 text-sm mb-2">{t.desc}</p>
                <p className="text-slate-400 text-sm">{t.text}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Chegada do Judô no Brasil */}
        <ScrollReveal direction="up">
          <div className="rounded-2xl border-2 overflow-hidden border-emerald-500/40 bg-gradient-to-br from-emerald-500/5 to-transparent">
            <div className="p-6 sm:p-8">
              <h2 className="font-jp text-xl font-bold text-white mb-2 flex items-center gap-2">
                <span className="text-2xl">🇧🇷</span> Chegada do Judô no Brasil
              </h2>
              <p className="text-slate-400 text-sm leading-relaxed mb-4">
                Há quem afirme que o judô veio com a imigração japonesa em 1908. Há também referências vagas sobre
                um certo professor Miura que teria ensinado judô por volta de 1903. Entretanto, foi no início dos anos
                vinte que chegou ao Brasil <strong className="text-white">Mitsuyo Maeda</strong> (ou Eisei Maeda),
                conhecido como <strong className="text-amber-400">Conde Koma</strong>, tendo ele o primeiro registro
                nos anais da história do judô brasileiro.
              </p>
              <p className="text-slate-400 text-sm leading-relaxed mb-4">
                Percorreu várias capitais aceitando desafios e ganhando todos, promovendo assim o esporte.
                Radicou-se em <strong className="text-white">Belém do Pará</strong>, onde montou sua escola. Dentre
                seus alunos constava a <strong className="text-white">família Gracie</strong>, que deu continuidade ao
                trabalho, progredindo e fundando novas escolas em algumas capitais e se projetando no cenário esportivo
                brasileiro através do Jiu-Jitsu. (Gama, 1986)
              </p>
              <div className="flex items-center gap-2 text-amber-400/80 text-xs">
                <span className="font-jp">柔道</span> Judô no Brasil — Conde Koma
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* Principais Títulos — Medalhas Olímpicas */}
        <ScrollReveal direction="up">
          <div className="rounded-2xl border-2 overflow-hidden" style={{ borderColor: 'rgba(234,179,8,0.4)', background: 'linear-gradient(135deg, rgba(234,179,8,0.05) 0%, transparent 50%)' }}>
            <div className="p-6 sm:p-8">
              <h2 className="font-jp text-xl font-bold text-white mb-2 flex items-center gap-2">
                <span className="text-2xl">🏅</span> Principais Títulos do Brasil em Jogos Olímpicos
              </h2>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">
                O judô é um esporte de combate individual que no Brasil tem bom prestígio e popularidade, produzindo
                bons resultados em nível internacional — um dos que mais trouxeram medalhas olímpicas ao país.
              </p>
              <div className="flex flex-wrap gap-3 mb-6">
                <span className="px-4 py-2 rounded-xl bg-amber-500/20 text-amber-400 font-bold">22 medalhas</span>
                <span className="px-4 py-2 rounded-xl bg-amber-400/30 text-amber-300 font-semibold">4 ouros</span>
                <span className="px-4 py-2 rounded-xl bg-slate-400/30 text-slate-300 font-semibold">3 pratas</span>
                <span className="px-4 py-2 rounded-xl bg-amber-700/40 text-amber-200 font-semibold">15 bronzes</span>
              </div>
              <div className="space-y-4 max-h-[420px] overflow-y-auto pr-1">
                {MEDALHAS_OLIMPICAS.map((edicao) => (
                  <motion.div
                    key={edicao.ano}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="rounded-xl border border-white/10 bg-white/[0.03] p-4"
                  >
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-bold px-2 py-1 rounded-lg text-white" style={{ backgroundColor: `${ACCENT}50` }}>
                        {edicao.ano}
                      </span>
                      <span className="text-slate-500 text-xs">{edicao.cidade}</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {edicao.medalhas.map((m) => (
                        <span
                          key={`${m.nome}-${m.peso}`}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium ${
                            m.tipo === 'ouro'
                              ? 'bg-amber-500/25 text-amber-300 border border-amber-500/40'
                              : m.tipo === 'prata'
                              ? 'bg-slate-400/20 text-slate-300 border border-slate-400/30'
                              : 'bg-amber-700/25 text-amber-200 border border-amber-700/40'
                          }`}
                        >
                          <span>{m.tipo === 'ouro' ? '🥇' : m.tipo === 'prata' ? '🥈' : '🥉'}</span>
                          <span>{m.nome}</span>
                          <span className="text-slate-500">({m.peso})</span>
                        </span>
                      ))}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* Graduação */}
        <ScrollReveal direction="up">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <h3 className="font-jp text-lg font-bold text-white mb-4">Sistema de Graduação</h3>
            <p className="text-slate-400 text-sm mb-4">
              Cada faixa representa uma etapa no desenvolvimento. A faixa branca simboliza pureza e mente aberta;
              as cores subsequentes representam o crescimento técnico e filosófico.
            </p>
            <p className="text-slate-500 text-xs">
              段位 — Dan | 級位 — Kyu — O sistema garante progressão gradual respeitando o desenvolvimento técnico e mental.
            </p>
          </div>
        </ScrollReveal>
      </div>
    </div>
  );
}
