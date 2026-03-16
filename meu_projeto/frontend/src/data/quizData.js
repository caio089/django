/**
 * Banco de perguntas do Quiz — Teoria do Judô
 * Baseado em conteúdo de significado, etiqueta, fundamentos e história.
 * 8 perguntas por nível, 10 níveis.
 */

// Perguntas organizadas por nível de complexidade (para distribuição nos 10 níveis)
const PERGUNTAS_NIVEL_1_2 = [
  { question: 'O que significa "JU" em judô?', answers: ['Caminho', 'Suave', 'Força', 'Arte'], correct: 1, explanation: 'Ju (柔) significa suave, flexível.' },
  { question: 'O que significa "DÔ" em judô?', answers: ['Suave', 'Caminho', 'Técnica', 'Respeito'], correct: 1, explanation: 'Dô (道) significa caminho, via.' },
  { question: 'Qual o significado de "Judô"?', answers: ['Arte da guerra', 'Caminho suave', 'Caminho da força', 'Arte marcial'], correct: 1, explanation: 'Judô significa "caminho suave" — Ju (suave) + Dô (caminho).' },
  { question: 'Como são chamados os praticantes de judô?', answers: ['alunos de judô', 'Senseis', 'Judocas', 'Faixas-pretas'], correct: 2, explanation: 'Aqueles que praticam o judô são chamados de judocas.' },
  { question: 'De qual país o judô é originário?', answers: ['China', 'Coreia', 'Japão', 'Brasil'], correct: 2, explanation: 'O judô é uma arte marcial japonesa.' },
  { question: 'Em qual cidade o judô foi criado?', answers: ['Osaka', 'Kyoto', 'Tóquio', 'Yokohama'], correct: 2, explanation: 'O judô foi criado em Tóquio, capital do Japão.' },
  { question: 'Qual é o nome do uniforme usado no judô?', answers: ['Kimono', 'Gi', 'Judogi', 'Hakama'], correct: 2, explanation: 'Judogi é o nome correto do uniforme usado no judô.' },
  { question: 'Qual é o nome do local onde se pratica judô?', answers: ['Tatame', 'Dojo', 'Academia', 'Ginásio'], correct: 1, explanation: 'Dojo é o local sagrado onde se pratica judô.' },
];

const PERGUNTAS_NIVEL_3_4 = [
  { question: 'Em que ano Jigoro Kano fundou a primeira escola de judô?', answers: ['1872', '1882', '1892', '1902'], correct: 1, explanation: 'Em maio de 1882, Jigoro Kano fundou a primeira escola de judô do mundo.' },
  { question: 'Quem foi o primeiro aluno de Jigoro Kano?', answers: ['Mitsuyo Maeda', 'Tsunejirô Tomita', 'Kyuzo Mifune', 'Masahiko Kimura'], correct: 1, explanation: 'Tsunejirô Tomita foi o primeiro aluno de Kano, matriculou-se em 5 de junho de 1882.' },
  { question: 'O que significa "Jita-kyoei"?', answers: ['Melhor uso da energia', 'Caminho suave', 'Bem estar e benefícios mútuos', 'Respeito'], correct: 2, explanation: 'Jita-kyoei significa bem estar e benefícios mútuos.' },
  { question: 'O que significa "Seiryoku Zen\'yo"?', answers: ['Benefícios mútuos', 'Melhor uso da energia', 'Caminho suave', 'Técnica perfeita'], correct: 1, explanation: 'Seiryoku Zen\'yo significa melhor uso da energia (máxima eficiência).' },
  { question: 'Qual era o nome de nascimento de Jigoro Kano?', answers: ['Jigoro', 'Kano', 'Shinnosuke', 'Tomita'], correct: 2, explanation: 'Quando nasceu chamava-se "Shinnosuke"; posteriormente mudou para Jigoro Kano.' },
  { question: 'Onde Jigoro Kano nasceu?', answers: ['Tóquio', 'Mikage, província de Settsu', 'Osaka', 'Kyoto'], correct: 1, explanation: 'Nasceu em 28.out.1860 em Mikage, província de Settsu (atual Hyogo), Japão.' },
  { question: 'Qual arte marcial além do judô que Kano praticou possuía Menkyo?', answers: ['Tenjin Shin\'yo-ryu', 'Kito-ryu', 'Aikido', 'Karate'], correct: 1, explanation: 'Kano praticou Kito-ryu, onde possuía Menkyo — licença para ensinar.' },
  { question: 'O que é "Menkyo" no judô/jujutsu?', answers: ['Uniforme', 'Faixa', 'Licença para ensinar', 'Competição'], correct: 2, explanation: 'Menkyo é uma licença/certificado para ensinar a arte.' },
];

const PERGUNTAS_NIVEL_5_6 = [
  { question: 'Como se chama a primeira escola de judô fundada por Kano?', answers: ['Dojo Central', 'Kodokan', 'Kano-ryu', 'Nihon Judo'], correct: 1, explanation: 'Em 1882, em Tóquio, Kano criou o Kodokan, primeira escola de judô do mundo.' },
  { question: 'O que significa "KAN" em Kodokan?', answers: ['Caminho', 'Instituto ou escola', 'Suave', 'Judô'], correct: 1, explanation: 'KAN significa instituto/escola. O Kodokan é a escola para estudar o caminho.' },
  { question: 'O que significa "DO" em Kodokan?', answers: ['Escola', 'Caminho', 'Judô', 'Instituto'], correct: 1, explanation: 'DO significa caminho. Kodokan = escola para estudar o caminho.' },
  { question: 'Qual o nome da esposa de Jigoro Kano?', answers: ['Sadako', 'Sumako', 'Tomiko', 'Yuki'], correct: 1, explanation: 'Esposa: Sumako. Pai: Jirosaku Mareshiba Kano. Mãe: Sadako.' },
  { question: 'O que significa "Ritsu-rei"?', answers: ['Saudação ajoelhado', 'Saudação em pé', 'Início da luta', 'Fim da luta'], correct: 1, explanation: 'Ritsu-rei é a saudação em pé.' },
  { question: 'O que significa "Za-rei"?', answers: ['Saudação em pé', 'Saudação ajoelhado', 'Comando de começar', 'Comando de parar'], correct: 1, explanation: 'Za-rei é a saudação ajoelhado.' },
  { question: 'O que é "Kumi-kata" no judô?', answers: ['Técnica de projeção', 'Formas de pegar no judogi', 'Tipo de queda', 'Saudação'], correct: 1, explanation: 'Kumi-kata refere-se às formas de pegar no judogi.' },
  { question: 'O que significa "Hiki-te"?', answers: ['Mão de puxar', 'Mão de elevação', 'Perna de apoio', 'Braço de controle'], correct: 1, explanation: 'Hiki-te é a mão de elevação no kumi-kata.' },
];

const PERGUNTAS_NIVEL_7_8 = [
  { question: 'O que é "Ai-yotsu"?', answers: ['Pegadas de lados opostos', 'Pegadas do mesmo lado', 'Movimento para frente', 'Saudação'], correct: 1, explanation: 'Ai-yotsu: destro x destro ou canhoto x canhoto — pegadas do mesmo lado.' },
  { question: 'O que é "Kenka-yotsu"?', answers: ['Pegadas do mesmo lado', 'Pegadas de lados opostos', 'Passadas normais', 'Repetições em movimento'], correct: 1, explanation: 'Kenka-yotsu: destro x canhoto — pegadas de lados opostos.' },
  { question: 'O que é "Mae-sabaki"?', answers: ['Movimento para trás', 'Movimento para frente', 'Movimento com giro', 'Passadas sucessivas'], correct: 1, explanation: 'Mae-sabaki é o movimento para frente.' },
  { question: 'O que é "Ushiro-sabaki"?', answers: ['Movimento para frente', 'Movimento para trás', 'Movimento com giro', 'Passadas normais'], correct: 1, explanation: 'Ushiro-sabaki é o movimento para trás.' },
  { question: 'Para que o "Otae-sabaki" é muito usado?', answers: ['Saudação', 'Kaeshi-waza (técnicas de contra-ataque)', 'Aquecimento', 'Competição'], correct: 1, explanation: 'Otae-sabaki é usado para esquivar de um ataque e realizar outro (kaeshi-waza).' },
  { question: 'O que significa "Ayumi-ashi"?', answers: ['Passadas sucessivas', 'Passadas normais', 'Movimento com giro', 'Saudação'], correct: 1, explanation: 'Ayumi-ashi são as passadas normais.' },
  { question: 'O que significa "Tsugi-ashi"?', answers: ['Passadas normais', 'Passadas sucessivas', 'Movimento para trás', 'Repetições'], correct: 1, explanation: 'Tsugi-ashi são as passadas sucessivas.' },
  { question: 'O que é "Ido Uchi-komi"?', answers: ['Repetições sem deslocamento', 'Repetições em movimento', 'Repetições alternadas', 'Treino livre'], correct: 1, explanation: 'Ido Uchi-komi: repetições em movimento, com deslocamento (shintai).' },
];

const PERGUNTAS_NIVEL_9_10 = [
  { question: 'O que é "Koge Uchi-komi" ou repetições alternadas?', answers: ['Um faz técnicas sem parar', 'Um faz a técnica, em seguida o outro', 'Apenas em movimento', 'Só em competição'], correct: 1, explanation: 'Koge Uchi-komi: alternando, onde um faz a técnica e em seguida o outro.' },
  { question: 'O que significa "Senpai"?', answers: ['Iniciante', 'Veterano ou mentor', 'Árbitro', 'Professor'], correct: 1, explanation: 'Senpai significa veterano — aluno mais velho e experiente que orienta o kohai.' },
  { question: 'O que significa "Kohai"?', answers: ['Veterano', 'Júnior ou iniciante', 'Árbitro', 'Faixa-preta'], correct: 1, explanation: 'Kohai significa júnior — aluno mais novo, tendo o senpai como exemplo.' },
  { question: 'O que significa "Uke" no judô?', answers: ['Quem aplica a técnica', 'Quem recebe a técnica', 'Árbitro', 'Professor'], correct: 1, explanation: 'Uke é o judoca passivo que recebe a técnica e se defende.' },
  { question: 'O que significa "Tori" no judô?', answers: ['Quem recebe a técnica', 'Quem aplica a técnica', 'Árbitro', 'Iniciante'], correct: 1, explanation: 'Tori é o judoca ativo que aplica a técnica e ataca.' },
  { question: 'Qual a primeira fase de uma projeção no judô?', answers: ['Kuzushi', 'Kumi-kata', 'Kake', 'Kime'], correct: 1, explanation: 'Fases: 1.Kumi-kata (pegada), 2.Kuzushi (desequilíbrio), 3.Tsukuri (preparação), 4.Kake (execução), 5.Kime (conclusão).' },
  { question: 'O que significa "Kuzushi" nas fases da projeção?', answers: ['Pegada', 'Desequilíbrio', 'Execução', 'Conclusão'], correct: 1, explanation: 'Kuzushi é o desequilíbrio do oponente antes da técnica.' },
  { question: 'O que significa "Kake" nas fases da projeção?', answers: ['Pegada no judogi', 'Desequilíbrio', 'Execução da técnica', 'Conclusão'], correct: 2, explanation: 'Kake é a execução da técnica de projeção.' },
];

// Perguntas adicionais para níveis 6–10 (cada nível com pool exclusivo)
const PERGUNTAS_NIVEL_6 = [
  { question: 'Qual o nome do pai de Jigoro Kano?', answers: ['Kano Jirosaku', 'Jirosaku Mareshiba Kano', 'Mareshiba Kano', 'Kano Sadako'], correct: 1, explanation: 'Pai: Jirosaku Mareshiba Kano. Mãe: Sadako.' },
  { question: 'Em que data Tsunejirô Tomita se matriculou no Kodokan?', answers: ['5.jun.1882', '28.out.1860', 'maio 1882', '1.jan.1883'], correct: 0, explanation: 'Tsunejirô Tomita matriculou-se em 5 de junho de 1882.' },
  { question: 'O que significa "Migi-ashi Mae-sabaki"?', answers: ['Movimento para trás à direita', 'Movimento para frente à direita', 'Movimento com giro', 'Passadas normais'], correct: 1, explanation: 'Migi-ashi Mae-sabaki: movimento para frente à direita.' },
  { question: 'O que significa "Hidari-ashi Ushiro-sabaki"?', answers: ['Frente à esquerda', 'Trás à esquerda', 'Trás à direita', 'Frente à direita'], correct: 1, explanation: 'Hidari-ashi Ushiro-sabaki: movimento para trás à esquerda.' },
  { question: 'O que é "Mae-mawari-sabaki"?', answers: ['Movimento para trás', 'Movimento para frente com giro', 'Passadas normais', 'Saudação'], correct: 1, explanation: 'Mae-mawari-sabaki é o movimento para frente com giro.' },
  { question: 'O que é "Ushiro-mawari-sabaki"?', answers: ['Movimento para frente', 'Movimento para trás com giro', 'Passadas sucessivas', 'Repetições'], correct: 1, explanation: 'Ushiro-mawari-sabaki é o movimento para trás com giro.' },
  { question: 'Qual é a segunda fase de uma projeção?', answers: ['Kumi-kata', 'Kuzushi (desequilíbrio)', 'Kake', 'Kime'], correct: 1, explanation: 'Fases: 1.Kumi-kata, 2.Kuzushi, 3.Tsukuri, 4.Kake, 5.Kime.' },
  { question: 'O que significa "Tsukuri" nas fases da projeção?', answers: ['Pegada', 'Desequilíbrio', 'Preparação da técnica', 'Execução'], correct: 2, explanation: 'Tsukuri é a preparação da técnica.' },
];

const PERGUNTAS_NIVEL_7 = [
  { question: 'O que significa "Kime" nas fases da projeção?', answers: ['Pegada', 'Desequilíbrio', 'Execução', 'Conclusão da técnica'], correct: 3, explanation: 'Kime é a conclusão da técnica de projeção.' },
  { question: 'Qual o nome da mãe de Jigoro Kano?', answers: ['Sumako', 'Sadako', 'Tomiko', 'Yuki'], correct: 1, explanation: 'Mãe: Sadako. Esposa: Sumako.' },
  { question: 'Em que dia e mês Jigoro Kano nasceu?', answers: ['5.jun.1860', '28.out.1860', 'maio.1882', '1.jan.1860'], correct: 1, explanation: 'Nasceu em 28 de outubro de 1860 em Mikage.' },
  { question: 'O que é "Hidari-ashi Mae-mawari-sabaki"?', answers: ['Trás à esquerda com giro', 'Frente à esquerda com giro', 'Frente à direita', 'Trás à direita'], correct: 1, explanation: 'Hidari-ashi Mae-mawari-sabaki: frente à esquerda com giro.' },
  { question: 'O que é "Migi-ashi Ushiro-mawari-sabaki"?', answers: ['Trás à esquerda com giro', 'Frente à direita com giro', 'Trás à direita com giro', 'Frente à esquerda'], correct: 2, explanation: 'Migi-ashi Ushiro-mawari-sabaki: trás à direita com giro.' },
  { question: 'Qual a função do Senpai em relação ao Kohai?', answers: ['Competir', 'Passar experiência e aconselhar', 'Aplicar penalidades', 'Árbitrar'], correct: 1, explanation: 'O Senpai passa experiência, adverte e aconselha para o Kohai progredir.' },
  { question: 'No Ido Uchi-komi, como é o deslocamento?', answers: ['Sem deslocamento', 'Com deslocamento (shintai)', 'Apenas alternado', 'Só em competição'], correct: 1, explanation: 'Ido Uchi-komi: repetições em movimento, com deslocamento (shintai).' },
  { question: 'No Uchi-komi tradicional sem deslocamento, quantos fazem a técnica?', answers: ['Os dois alternando', 'Apenas um', 'Ninguém', 'O professor'], correct: 1, explanation: 'Tradicional: apenas um faz as técnicas repetidamente, sem deslocamento.' },
];

const PERGUNTAS_NIVEL_8 = [
  { question: 'Em que província atual fica Mikage (onde Kano nasceu)?', answers: ['Tóquio', 'Osaka', 'Hyogo', 'Kyoto'], correct: 2, explanation: 'Mikage ficava na província de Settsu, atual Hyogo.' },
  { question: 'Qual arte marcial Kano praticou além de Kito-ryu?', answers: ['Aikido', 'Tenjin Shin\'yo-ryu', 'Karate', 'Kempo'], correct: 1, explanation: 'Kano praticou Tenjin Shin\'yo-ryu e Kito-ryu.' },
  { question: 'O que é "Kaeshi-waza"?', answers: ['Técnicas de projeção', 'Técnicas de contra-ataque', 'Técnicas de imobilização', 'Técnicas de estrangulamento'], correct: 1, explanation: 'Kaeshi-waza são técnicas de contra-ataque.' },
  { question: 'Qual a ordem correta das fases de uma projeção?', answers: ['Kake, Kuzushi, Kime', 'Kumi-kata, Kuzushi, Tsukuri, Kake, Kime', 'Kime, Kake, Kuzushi', 'Kuzushi, Kake, Tsukuri'], correct: 1, explanation: 'Ordem: 1.Kumi-kata, 2.Kuzushi, 3.Tsukuri, 4.Kake, 5.Kime.' },
  { question: 'O Kodokan foi criado em que cidade?', answers: ['Osaka', 'Kyoto', 'Tóquio', 'Yokohama'], correct: 2, explanation: 'Em 1882, em Tóquio, Kano criou o Kodokan.' },
  { question: 'Qual a visão do Kohai em relação ao Senpai?', answers: ['Rival', 'Exemplo e referência', 'Adversário', 'Árbitro'], correct: 1, explanation: 'O Kohai tem o Senpai como exemplo, com mais experiência.' },
  { question: 'O Uke no randori é o judoca que:', answers: ['Aplica a técnica', 'Recebe a técnica e se defende', 'Árbitra', 'Anota pontos'], correct: 1, explanation: 'Uke é o judoca passivo que recebe a técnica.' },
  { question: 'O Tori no randori é o judoca que:', answers: ['Recebe a técnica', 'Aplica/ataca com a técnica', 'Observa', 'Coaching'], correct: 1, explanation: 'Tori é o judoca ativo que aplica a técnica.' },
];

const PERGUNTAS_NIVEL_9 = [
  { question: 'Quantas fases tem uma projeção no judô?', answers: ['3', '4', '5', '6'], correct: 2, explanation: 'Fases: Kumi-kata, Kuzushi, Tsukuri, Kake, Kime.' },
  { question: 'Em que ano o judô foi fundado?', answers: ['1860', '1882', '1890', '1900'], correct: 1, explanation: 'Maio de 1882 — fundação do Kodokan.' },
  { question: 'O princípio "melhor uso da energia" corresponde a:', answers: ['Jita-kyoei', 'Seiryoku Zen\'yo', 'Ritsu-rei', 'Kumi-kata'], correct: 1, explanation: 'Seiryoku Zen\'yo = melhor uso da energia.' },
  { question: 'O princípio "bem estar e benefícios mútuos" corresponde a:', answers: ['Seiryoku Zen\'yo', 'Jita-kyoei', 'Za-rei', 'Tsukuri'], correct: 1, explanation: 'Jita-kyoei = bem estar e benefícios mútuos.' },
  { question: 'Qual a terceira fase da projeção?', answers: ['Kuzushi', 'Tsukuri (preparação)', 'Kake', 'Kime'], correct: 1, explanation: 'Tsukuri = preparação da técnica.' },
  { question: 'Qual a quarta fase da projeção?', answers: ['Tsukuri', 'Kake (execução)', 'Kime', 'Kuzushi'], correct: 1, explanation: 'Kake = execução da técnica.' },
  { question: 'Onde fica o Kodokan até hoje?', answers: ['Osaka', 'Tóquio', 'Kyoto', 'Yokohama'], correct: 1, explanation: 'O Kodokan foi criado em Tóquio em 1882.' },
  { question: 'O judô é classificado como:', answers: ['Esporte apenas', 'Arte marcial japonesa', 'Luta livre', 'Defesa pessoal'], correct: 1, explanation: 'O judô é uma arte marcial japonesa criada em Tóquio.' },
];

const PERGUNTAS_NIVEL_10 = [
  { question: 'O que o Otae-sabaki permite fazer?', answers: ['Saudar', 'Esquivar de um ataque para realizar outro', 'Aquecer', 'Competir'], correct: 1, explanation: 'Otae-sabaki é usado em Kaeshi-waza para esquiva e contra-ataque.' },
  { question: 'Qual a diferença entre Ayumi-ashi e Tsugi-ashi?', answers: ['São iguais', 'Normais vs sucessivas', 'Frente vs trás', 'Rápidas vs lentas'], correct: 1, explanation: 'Ayumi-ashi = passadas normais. Tsugi-ashi = passadas sucessivas.' },
  { question: 'No Koge Uchi-komi, quantos fazem a técnica?', answers: ['Apenas um', 'Os dois, alternando', 'Ninguém', 'Apenas o sensei'], correct: 1, explanation: 'Koge Uchi-komi: um faz a técnica, em seguida o outro.' },
  { question: 'O Menkyo em Kito-ryu permitia a Kano:', answers: ['Competir', 'Ensinar a arte', 'Lutar', 'Fundar escola'], correct: 1, explanation: 'Menkyo é licença para ensinar.' },
  { question: 'Qual a quinta e última fase da projeção?', answers: ['Kuzushi', 'Tsukuri', 'Kake', 'Kime'], correct: 3, explanation: 'Kime = conclusão da técnica.' },
  { question: 'Qual o papel do Hiki-te no kumi-kata?', answers: ['Puxar', 'Elevar', 'Girar', 'Imobilizar'], correct: 1, explanation: 'Hiki-te = mão de elevação.' },
  { question: 'Ai-yotsu ocorre quando:', answers: ['Destro enfrenta canhoto', 'Ambos usam a mesma pegada (destro x destro)', 'Há movimento de giro', 'É competição'], correct: 1, explanation: 'Ai-yotsu: destro x destro ou canhoto x canhoto.' },
  { question: 'Kenka-yotsu ocorre quando:', answers: ['Ambos destros', 'Destro x canhoto (lados opostos)', 'Ambos canhotos', 'Em Kata'], correct: 1, explanation: 'Kenka-yotsu: destro x canhoto ou canhoto x destro.' },
];

// Export para uso em simulados
export {
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
};

// Cada nível tem pool EXCLUSIVO — perguntas diferentes por nível
const POOL_POR_NIVEL = {
  1: PERGUNTAS_NIVEL_1_2,
  2: PERGUNTAS_NIVEL_3_4,
  3: PERGUNTAS_NIVEL_5_6,
  4: PERGUNTAS_NIVEL_7_8,
  5: PERGUNTAS_NIVEL_9_10,
  6: PERGUNTAS_NIVEL_6,
  7: PERGUNTAS_NIVEL_7,
  8: PERGUNTAS_NIVEL_8,
  9: PERGUNTAS_NIVEL_9,
  10: PERGUNTAS_NIVEL_10,
};

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shuffleAnswersInQuestions(questions) {
  return questions.map((q) => {
    const order = shuffle(q.answers.map((_, i) => i));
    const answers = order.map((i) => q.answers[i]);
    const correct = order.indexOf(q.correct);
    return { ...q, answers, correct };
  });
}

/** 8 perguntas por nível em todos os 10 níveis. */
export const PERGUNTAS_POR_NIVEL_MAP = {
  1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8,
};

export function getPerguntasPorNivel(nivel) {
  return PERGUNTAS_POR_NIVEL_MAP[Math.max(1, Math.min(10, Number(nivel) || 1))] ?? 8;
}

export const XP_POR_ACERTO = 10;

/** Categorias por nível (10 níveis para manter a pessoa presa ao sistema). */
export const CATEGORIAS_NIVEL = {
  1: 'Iniciante',
  2: 'Aprendiz',
  3: 'Discípulo',
  4: 'Ninja',
  5: 'Samurai',
  6: 'Faixa Preta',
  7: 'Guardião do Caminho',
  8: 'Sensei',
  9: 'Mestre do Judô',
  10: 'Espírito de Jigoro Kano',
};

export const MAX_NIVEL = 10;

function getPoolForLevel(n) {
  return POOL_POR_NIVEL[n] ?? POOL_POR_NIVEL[1];
}

/**
 * Retorna as perguntas para o nível (8 por nível, de 1 a 10).
 */
export function getQuestionsForLevel(nivel) {
  const n = Math.max(1, Math.min(10, Number(nivel) || 1));
  const total = getPerguntasPorNivel(n);
  const pool = getPoolForLevel(n);
  const chosen = shuffle([...pool]).slice(0, total);
  return shuffleAnswersInQuestions(chosen);
}

// Compatibilidade com modo não-ranking (se existir)
export const QUESTIONS_BY_DIFFICULTY = {
  easy: POOL_POR_NIVEL[1],
  medium: [...POOL_POR_NIVEL[1], ...POOL_POR_NIVEL[2], ...POOL_POR_NIVEL[3]].slice(0, 24),
  hard: POOL_POR_NIVEL[10],
};

export function getQuestions(difficulty) {
  const all = Object.values(POOL_POR_NIVEL).flat();
  const list = shuffle(all).slice(0, difficulty === 'all' ? 45 : 15);
  return shuffleAnswersInQuestions(list);
}
