/**
 * Dados para Simulados de Graduação — 3 fases por faixa
 * Fase 1: 10 perguntas teóricas (exige mais conforme a faixa)
 * Fase 2: Projeções, ataques combinados e contra-ataques (em pé)
 * Fase 3: Imobilização, chave de braço, estrangulamento (chão)
 */

import {
  PERGUNTAS_NIVEL_1_2,
  PERGUNTAS_NIVEL_3_4,
  PERGUNTAS_NIVEL_5_6,
  PERGUNTAS_NIVEL_7_8,
  PERGUNTAS_NIVEL_9_10,
  PERGUNTAS_NIVEL_6,
  PERGUNTAS_NIVEL_7,
  PERGUNTAS_NIVEL_8,
  PERGUNTAS_NIVEL_9,
  PERGUNTAS_NIVEL_10,
} from './quizData';

export const FAIXAS_SIMULADO = [
  { id: 1, nome: 'Faixa Cinza', cor: 'from-gray-600 to-gray-700', img: '/static/faixa-cinza.png' },
  { id: 2, nome: 'Faixa Azul', cor: 'from-blue-600 to-blue-800', img: '/static/faixa-azul.png' },
  { id: 3, nome: 'Faixa Amarela', cor: 'from-amber-500 to-amber-600', img: '/static/faixa-amarela.png' },
  { id: 4, nome: 'Faixa Laranja', cor: 'from-orange-500 to-orange-600', img: '/static/faixa-laranja.png' },
  { id: 5, nome: 'Faixa Verde', cor: 'from-emerald-600 to-emerald-700', img: '/static/faixa-verde.png' },
  { id: 6, nome: 'Faixa Roxa', cor: 'from-purple-600 to-purple-700', img: '/static/faixa-roxa.png' },
  { id: 7, nome: 'Faixa Marrom', cor: 'from-amber-800 to-amber-900', img: '/static/faixa-marrom.png' },
];

// Quantidades por faixa — Fase 2 (em pé): projeção, combinado, contra-ataque
const FASE2_POR_FAIXA = {
  1: { tecnica: 2, combinado: 0, contra_ataque: 0 },
  2: { tecnica: 2, combinado: 1, contra_ataque: 1 },
  3: { tecnica: 3, combinado: 2, contra_ataque: 2 },
  4: { tecnica: 3, combinado: 2, contra_ataque: 2 },
  5: { tecnica: 3, combinado: 2, contra_ataque: 2 },
  6: { tecnica: 3, combinado: 2, contra_ataque: 2 },
  7: { tecnica: 3, combinado: 2, contra_ataque: 2 },
};

// Quantidades por faixa — Fase 3 (chão): imobilização, chave, estrangulamento, atemi
const FASE3_POR_FAIXA = {
  1: { imobilizacao: 2, chave_braco: 0, estrangulamento: 0, atemi: 0 },
  2: { imobilizacao: 3, chave_braco: 0, estrangulamento: 0, atemi: 0 },
  3: { imobilizacao: 3, chave_braco: 0, estrangulamento: 0, atemi: 0 },
  4: { imobilizacao: 2, chave_braco: 1, estrangulamento: 1, atemi: 0 },
  5: { imobilizacao: 2, chave_braco: 2, estrangulamento: 2, atemi: 0 },
  6: { imobilizacao: 2, chave_braco: 2, estrangulamento: 2, atemi: 0 },
  7: { imobilizacao: 2, chave_braco: 1, estrangulamento: 1, atemi: 1 },
};

// Pool de teoria por faixa (nível de complexidade — exige mais conforme a faixa)
const TEORIA_POR_FAIXA = {
  1: PERGUNTAS_NIVEL_1_2,
  2: PERGUNTAS_NIVEL_1_2,
  3: [...PERGUNTAS_NIVEL_1_2, ...PERGUNTAS_NIVEL_3_4],
  4: [...PERGUNTAS_NIVEL_3_4, ...PERGUNTAS_NIVEL_5_6],
  5: [...PERGUNTAS_NIVEL_5_6, ...PERGUNTAS_NIVEL_7_8],
  6: [...PERGUNTAS_NIVEL_7_8, ...PERGUNTAS_NIVEL_6, ...PERGUNTAS_NIVEL_7],
  7: [...PERGUNTAS_NIVEL_8, ...PERGUNTAS_NIVEL_9, ...PERGUNTAS_NIVEL_10],
};

// Perguntas práticas (avaliador dá nota 0-10)
const PERGUNTAS_TECNICA = [
  { pergunta: 'Demonstre Osoto-gari (projeção)', faixaMin: 1 },
  { pergunta: 'Demonstre Ippon-seoi-nage', faixaMin: 1 },
  { pergunta: 'Demonstre O-goshi ou Koshi-guruma', faixaMin: 2 },
  { pergunta: 'Demonstre O-uchi-gari ou Ko-uchi-gari', faixaMin: 3 },
  { pergunta: 'Demonstre Tai-otoshi', faixaMin: 3 },
  { pergunta: 'Demonstre Uchi-mata', faixaMin: 4 },
  { pergunta: 'Demonstre Harai-goshi', faixaMin: 4 },
  { pergunta: 'Demonstre De-ashi-harai', faixaMin: 4 },
  { pergunta: 'Demonstre Kata-guruma', faixaMin: 5 },
  { pergunta: 'Demonstre Tani-otoshi', faixaMin: 5 },
  { pergunta: 'Demonstre Sumi-gaeshi ou Tomoe-nage', faixaMin: 6 },
  { pergunta: 'Demonstre Ushiro-goshi', faixaMin: 6 },
  { pergunta: 'Demonstre Yoko-wakare ou Yoko-gake', faixaMin: 7 },
];

const PERGUNTAS_IMOBILIZACAO = [
  { pergunta: 'Demonstre Hon-kesa-gatame', faixaMin: 1 },
  { pergunta: 'Demonstre Yoko-shiho-gatame', faixaMin: 2 },
  { pergunta: 'Demonstre Kami-shiho-gatame', faixaMin: 2 },
  { pergunta: 'Demonstre Kuzure-kesa-gatame', faixaMin: 3 },
  { pergunta: 'Demonstre Kata-gatame', faixaMin: 4 },
  { pergunta: 'Demonstre Mune-gatame ou Ura-shiho-gatame', faixaMin: 5 },
  { pergunta: 'Demonstre Sankaku-gatame (controle)', faixaMin: 6 },
  { pergunta: 'Demonstre variações de Tate-shiho-gatame', faixaMin: 7 },
];

const PERGUNTAS_CHAVE = [
  { pergunta: 'Demonstre Ude-hishigi-juji-gatame', faixaMin: 4 },
  { pergunta: 'Demonstre Ude-garami (uma variação)', faixaMin: 5 },
  { pergunta: 'Demonstre Ude-hishigi-hiza-gatame', faixaMin: 5 },
  { pergunta: 'Demonstre Sankaku-gatame (chave)', faixaMin: 6 },
  { pergunta: 'Demonstre Waki-gatame ou Hara-gatame', faixaMin: 7 },
];

const PERGUNTAS_ESTRANGULAMENTO = [
  { pergunta: 'Demonstre Hadaka-jime', faixaMin: 4 },
  { pergunta: 'Demonstre Okuri-eri-jime', faixaMin: 4 },
  { pergunta: 'Demonstre Nami-juji-jime ou Kata-juji-jime', faixaMin: 5 },
  { pergunta: 'Demonstre Sankaku-jime', faixaMin: 6 },
  { pergunta: 'Demonstre Kata-ha-jime', faixaMin: 6 },
  { pergunta: 'Demonstre Sode-guruma-jime ou Ashi-jime', faixaMin: 7 },
];

const PERGUNTAS_ATEMI = [
  { pergunta: 'Explique os pontos de atemi permitidos em defesa pessoal', faixaMin: 7 },
  { pergunta: 'Demonstre bloqueio básico contra atemi', faixaMin: 7 },
];

const PERGUNTAS_COMBINADO = [
  { pergunta: 'Execute uma sequência Renraku-waza (ataque combinado)', faixaMin: 3 },
  { pergunta: 'Execute O-soto-gari → O-soto-guruma ou similar', faixaMin: 4 },
  { pergunta: 'Execute duas técnicas de ataque combinado', faixaMin: 5 },
  { pergunta: 'Execute sequência de 3 ataques combinados', faixaMin: 7 },
];

const PERGUNTAS_CONTRA_ATAQUE = [
  { pergunta: 'Execute um Kaeshi-waza (contra-ataque)', faixaMin: 3 },
  { pergunta: 'Contra O-soto-gari com técnica adequada', faixaMin: 4 },
  { pergunta: 'Execute Seoi-nage → Tani-otoshi (contra)', faixaMin: 5 },
  { pergunta: 'Execute dois contra-ataques diferentes', faixaMin: 6 },
  { pergunta: 'Execute três Kaeshi-waza', faixaMin: 7 },
];

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function pickByFaixa(pool, faixa, count) {
  const filtered = pool.filter((p) => p.faixaMin <= faixa);
  return shuffle(filtered).slice(0, count);
}

function teoriaToSimulado(q) {
  return { tipo: 'teoria', pergunta: q.question, nota: null, fase: 1 };
}

/**
 * Gera questões para o simulado da faixa em 3 fases:
 * Fase 1: 10 teoria | Fase 2: projeções + combinado + contra-ataque | Fase 3: chão
 */
export function getQuestionsForFaixa(faixaId) {
  const faixa = Math.max(1, Math.min(7, Number(faixaId) || 1));
  const f2 = FASE2_POR_FAIXA[faixa] || FASE2_POR_FAIXA[1];
  const f3 = FASE3_POR_FAIXA[faixa] || FASE3_POR_FAIXA[1];
  const result = [];
  let id = 1;

  // ——— FASE 1: 10 perguntas teóricas ———
  const poolTeoria = TEORIA_POR_FAIXA[faixa] || TEORIA_POR_FAIXA[1];
  shuffle(poolTeoria).slice(0, 10).forEach((q) => {
    result.push({ ...teoriaToSimulado(q), id: id++ });
  });

  // ——— FASE 2: Em pé (projeções, combinado, contra-ataque) ———
  pickByFaixa(PERGUNTAS_TECNICA, faixa, f2.tecnica).forEach((p) => {
    result.push({ tipo: 'tecnica', pergunta: p.pergunta, nota: null, fase: 2, id: id++ });
  });
  pickByFaixa(PERGUNTAS_COMBINADO, faixa, f2.combinado).forEach((p) => {
    result.push({ tipo: 'combinado', pergunta: p.pergunta, nota: null, fase: 2, id: id++ });
  });
  pickByFaixa(PERGUNTAS_CONTRA_ATAQUE, faixa, f2.contra_ataque).forEach((p) => {
    result.push({ tipo: 'contra_ataque', pergunta: p.pergunta, nota: null, fase: 2, id: id++ });
  });

  // ——— FASE 3: Chão (imobilização, chave, estrangulamento, atemi) ———
  pickByFaixa(PERGUNTAS_IMOBILIZACAO, faixa, f3.imobilizacao).forEach((p) => {
    result.push({ tipo: 'imobilizacao', pergunta: p.pergunta, nota: null, fase: 3, id: id++ });
  });
  pickByFaixa(PERGUNTAS_CHAVE, faixa, f3.chave_braco).forEach((p) => {
    result.push({ tipo: 'chave_braco', pergunta: p.pergunta, nota: null, fase: 3, id: id++ });
  });
  pickByFaixa(PERGUNTAS_ESTRANGULAMENTO, faixa, f3.estrangulamento).forEach((p) => {
    result.push({ tipo: 'estrangulamento', pergunta: p.pergunta, nota: null, fase: 3, id: id++ });
  });
  pickByFaixa(PERGUNTAS_ATEMI, faixa, f3.atemi).forEach((p) => {
    result.push({ tipo: 'atemi', pergunta: p.pergunta, nota: null, fase: 3, id: id++ });
  });

  return result;
}

export const NOTA_MINIMA_APROVACAO = 7;
