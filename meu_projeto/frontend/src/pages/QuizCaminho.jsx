import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Lock } from 'lucide-react';
// Imagens do caminho em frontend/public/
// (caminho absoluto a partir da raiz do Vite):
const MAP_IMAGE_DESKTOP = '/montanhas-v2.jpg';
const MAP_IMAGE_MOBILE = '/montanhas-v3.jpg';
import { CATEGORIAS_NIVEL, MAX_NIVEL } from '../data/quizData';

const STORAGE_NIVEL = 'quiz_ranking_nivel';
const ACCENT = 'rgb(59, 130, 246)';

const NIVEL_DESCRICOES = {
  1: 'Entrou no jogo. Zero glamour, só começo.',
  2: 'Já sabe cair, levantar e não desistir.',
  3: 'Aqui o cara escolhe o caminho. Não é mais turista.',
  4: 'Fase divertida e viciante. Agilidade, reflexo, técnica aparecendo.',
  5: 'Controle, honra, cabeça fria. Jogador consistente.',
  6: 'Marco forte. Não é final — é “agora começa”.',
  7: 'Quem vive o judô no dia a dia. Disciplina acima do ego.',
  8: 'Status alto. Saber, transmitir, liderar.',
  9: 'Técnica + filosofia + exemplo.',
  10: 'Nível simbólico máximo. Representar os valores supremos do judô.',
};

function getNivelSalvo() {
  if (typeof window === 'undefined') return 1;
  try {
    const raw = localStorage.getItem(STORAGE_NIVEL);
    const n = Math.max(1, Math.min(MAX_NIVEL, Number(raw) || 1));
    return n;
  } catch {
    return 1;
  }
}

export default function QuizCaminho() {
  const [nivelAtual, setNivelAtual] = useState(1);
  const [isMobile, setIsMobile] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setNivelAtual(getNivelSalvo());
    const updateSize = () => {
      if (typeof window === 'undefined') return;
      setIsMobile(window.innerWidth < 768);
    };
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  const montanhas = Array.from({ length: MAX_NIVEL }, (_, i) => {
    const n = i + 1;
    const status = n < nivelAtual ? 'completo' : n === nivelAtual ? 'atual' : 'bloqueado';
    return {
      nivel: n,
      titulo: CATEGORIAS_NIVEL[n],
      descricao: NIVEL_DESCRICOES[n],
      status,
    };
  });

  // Configuração dinâmica de posições por nível
  // Percentuais afinados para o mapa épico (desktop) e variação para mobile
  const LEVEL_CONFIG = {
    1: {
      key: 'INICIANTE',
      // alinhado bem no topo da montanha + texto "Iniciante" da arte
      // (área clicável vai ser bem grande pra garantir o clique)
      desktop: { left: '20%', top: '82%' },
      mobile: { left: '21%', top: '83%' },
      tier: 'low',
    },
    2: {
      key: 'APRENDIZ',
      desktop: { left: '42%', top: '88%' },
      mobile: { left: '45%', top: '90%' },
      tier: 'low',
    },
    3: {
      key: 'DISCÍPULO',
      desktop: { left: '69%', top: '86%' },
      mobile: { left: '72%', top: '88%' },
      tier: 'low',
    },
    4: {
      key: 'NINJA',
      desktop: { left: '22%', top: '64%' },
      mobile: { left: '24%', top: '63%' },
      tier: 'mid',
    },
    5: {
      key: 'SAMURAI',
      desktop: { left: '51%', top: '64%' },
      mobile: { left: '51%', top: '63%' },
      tier: 'mid',
    },
    6: {
      key: 'FAIXA PRETA',
      desktop: { left: '79%', top: '63%' },
      mobile: { left: '78%', top: '62%' },
      tier: 'mid',
    },
    7: {
      key: 'GUARDIÃO DO CAMINHO',
      desktop: { left: '35%', top: '43%' },
      mobile: { left: '37%', top: '41%' },
      tier: 'high',
    },
    8: {
      key: 'SENSEI',
      desktop: { left: '63%', top: '46%' },
      mobile: { left: '63%', top: '44%' },
      tier: 'high',
    },
    9: {
      key: 'MESTRE DO JUDÔ',
      desktop: { left: '30%', top: '27%' },
      mobile: { left: '32%', top: '25%' },
      tier: 'apex',
    },
    10: {
      key: 'ESPÍRITO DE JIGORO KANO',
      desktop: { left: '69%', top: '20%' },
      mobile: { left: '69%', top: '18%' },
      tier: 'apex',
    },
  };

  return (
    <div className="relative h-screen font-display antialiased overflow-hidden bg-black">

      {/* Botão voltar no canto superior esquerdo */}
      <div className="absolute top-4 left-4 z-30">
        <Link
          to="/quiz"
          className="flex items-center gap-2 text-slate-200 hover:text-white px-3 py-2 rounded-xl bg-black/70 hover:bg-black/90 border border-white/30 text-xs sm:text-sm shadow-lg"
        >
          <ArrowLeft className="w-4 h-4" /> Voltar
        </Link>
      </div>

      {/* Imagem principal ocupando 100% da tela */}
      <div className="absolute inset-0 z-20">
        <motion.img
          src={isMobile ? MAP_IMAGE_MOBILE : MAP_IMAGE_DESKTOP}
          alt="Caminho do mestre do judô"
          className="w-full h-full object-cover"
          initial={false}
        />

        {/* Hotspots clicáveis sobre cada montanha */}
        {montanhas.map((m) => {
          const cfg = LEVEL_CONFIG[m.nivel];
          const pos = cfg ? (isMobile ? cfg.mobile : cfg.desktop) : { left: '50%', top: '50%' };
          const desbloqueado = m.nivel <= nivelAtual;
          const isAtual = m.status === 'atual';
          const tier = cfg?.tier || 'mid';

          const baseLabelClasses =
            tier === 'apex'
              ? 'text-[12px] sm:text-sm md:text-xl px-5 sm:px-7 py-2 sm:py-2.5'
              : tier === 'high'
              ? 'text-[11px] sm:text-sm md:text-lg px-4 sm:px-6 py-1.5 sm:py-2'
              : 'text-[10px] sm:text-xs md:text-base px-3 sm:px-4 py-1.5';

          return (
            <motion.button
              key={m.nivel}
              type="button"
              disabled={!desbloqueado}
              onClick={() => {
                if (!desbloqueado) return;
                navigate('/quiz', { state: { treinoNivel: m.nivel } });
              }}
              whileHover={desbloqueado ? { scale: 1.05 } : {}}
              whileTap={desbloqueado ? { scale: 0.97 } : {}}
              className="absolute -translate-x-1/2 -translate-y-1/2 flex items-center justify-center"
              style={{ left: pos.left, top: pos.top }}
            >
              {/* Área de clique invisível (somente interação) */}
              <div
                className={`rounded-full cursor-pointer ${
                  desbloqueado ? 'border-2 border-transparent hover:border-amber-300/80' : 'cursor-not-allowed'
                }`}
                style={{
                  width:
                    m.nivel === 1
                      ? 220
                      : tier === 'apex'
                      ? 140
                      : tier === 'high'
                      ? 120
                      : 90,
                  height:
                    m.nivel === 1
                      ? 130
                      : tier === 'apex'
                      ? 90
                      : tier === 'high'
                      ? 80
                      : 70,
                }}
              />
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}

