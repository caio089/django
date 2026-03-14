export const QUESTIONS_BY_DIFFICULTY = {
  easy: [
    { question: 'Quem criou o judô?', answers: ['Jigoro Kano', 'Mitsuyo Maeda', 'Kyuzo Mifune', 'Masahiko Kimura'], correct: 0, explanation: 'Jigoro Kano criou o judô em 1882, fundando o Instituto Kodokan em Tóquio.' },
    { question: 'Qual é o significado da palavra "judô"?', answers: ['Caminho da força', 'Arte da guerra', 'Caminho suave', 'Arte marcial'], correct: 2, explanation: '"Ju" significa suave e "do" significa caminho, formando "caminho suave".' },
    { question: 'Qual é o nome do uniforme usado no judô?', answers: ['Kimono', 'Gi', 'Judogi', 'Hakama'], correct: 2, explanation: 'Judogi é o nome correto do uniforme usado no judô.' },
    { question: 'Qual é o nome do local onde se pratica judô?', answers: ['Dojo', 'Tatame', 'Academia', 'Ginásio'], correct: 0, explanation: 'Dojo é o local sagrado onde se pratica judô e outras artes marciais.' },
    { question: 'O que significa "Rei" no judô?', answers: ['Respeito', 'Força', 'Técnica', 'Vitória'], correct: 0, explanation: '"Rei" significa respeito e é fundamental na etiqueta do judô.' },
    { question: 'Qual é a cor da faixa mais alta no judô?', answers: ['Vermelha', 'Preta', 'Branca', 'Dourada'], correct: 0, explanation: 'A faixa vermelha é a mais alta, seguida da branca e vermelha, e depois da preta.' },
    { question: 'Quantas faixas coloridas existem antes da faixa preta no judô?', answers: ['4', '5', '6', '8'], correct: 3, explanation: 'Existem 8 faixas coloridas antes da faixa preta no judô.' },
    { question: 'O que significa "Ukemi" no judô?', answers: ['Técnica de projeção', 'Técnica de rolamentos', 'Técnica de queda', 'Técnica de estrangulamento'], correct: 1, explanation: 'Ukemi são as técnicas de rolamentos que protegem o praticante durante as projeções.' },
    { question: 'Qual é o objetivo principal do judô?', answers: ['Derrotar o oponente', 'Desenvolver corpo e mente', 'Ganhar competições', 'Aprender autodefesa'], correct: 1, explanation: 'O judô visa o desenvolvimento físico, mental e moral através da prática.' },
    { question: 'Em que ano o judô se tornou esporte olímpico?', answers: ['1964', '1972', '1980', '1988'], correct: 0, explanation: 'O judô se tornou esporte olímpico em 1964, nos Jogos de Tóquio.' },
    { question: 'Qual é a duração de uma luta de judô em competição?', answers: ['3 minutos', '4 minutos', '5 minutos', '6 minutos'], correct: 1, explanation: 'Uma luta de judô em competição dura 4 minutos para adultos.' },
    { question: 'O que significa "Ippon" no judô?', answers: ['Ponto completo', 'Ponto parcial', 'Penalidade', 'Empate'], correct: 0, explanation: 'Ippon é o ponto completo que encerra imediatamente a luta.' },
    { question: 'O que significa "Waza-ari" no judô?', answers: ['Ponto completo', 'Ponto parcial', 'Penalidade', 'Aviso'], correct: 1, explanation: 'Waza-ari é um ponto parcial, dois waza-ari equivalem a um ippon.' },
    { question: 'O que significa "Shido" no judô?', answers: ['Ponto', 'Penalidade leve', 'Penalidade grave', 'Desqualificação'], correct: 1, explanation: 'Shido é uma penalidade leve por infrações menores durante a luta.' },
    { question: 'Qual é a idade mínima para obter a faixa preta no judô?', answers: ['14 anos', '16 anos', '18 anos', 'Não há idade mínima'], correct: 1, explanation: 'A idade mínima para obter a faixa preta (1º dan) é 16 anos.' },
  ],
  medium: [
    { question: 'Qual é o princípio fundamental do judô?', answers: ['Máxima eficiência com mínimo esforço', 'Força bruta', 'Velocidade máxima', 'Técnica perfeita'], correct: 0, explanation: 'O princípio fundamental é "Seiryoku Zenyo" - máxima eficiência com mínimo esforço.' },
    { question: 'Qual é uma das técnicas mais fundamentais do judô?', answers: ['Uke-goshi', 'Seoi-nage', 'O-goshi', 'Tai-otoshi'], correct: 2, explanation: 'Seoi-nage é uma das primeiras técnicas ensinadas no judô.' },
    { question: 'O que significa "Kata" no judô?', answers: ['Luta livre', 'Forma ou padrão', 'Competição', 'Treino físico'], correct: 1, explanation: 'Kata são sequências formais de técnicas executadas em padrões específicos.' },
    { question: 'Qual é o nome da técnica de imobilização mais básica?', answers: ['Kesa-gatame', 'Kami-shiho-gatame', 'Yoko-shiho-gatame', 'Tate-shiho-gatame'], correct: 0, explanation: 'Kesa-gatame (imobilização em diagonal) é considerada a mais básica.' },
    { question: 'O que significa "Randori" no judô?', answers: ['Treino livre', 'Competição', 'Kata', 'Aquecimento'], correct: 0, explanation: 'Randori é o treino livre onde os praticantes aplicam técnicas.' },
    { question: 'Qual é o nome da técnica de projeção com quadril?', answers: ['Seoi-nage', 'Tai-otoshi', 'O-goshi', 'O-soto-gari'], correct: 2, explanation: 'O-goshi utiliza o quadril como ponto de apoio principal.' },
    { question: 'O que significa "Osae-komi" no judô?', answers: ['Imobilização', 'Projeção', 'Estrangulamento', 'Chave de braço'], correct: 0, explanation: 'Osae-komi é o anúncio de que uma imobilização está sendo aplicada.' },
    { question: 'O que significa "Toketa" no judô?', answers: ['Imobilização', 'Imobilização quebrada', 'Projeção', 'Estrangulamento'], correct: 1, explanation: 'Toketa é o anúncio de que uma imobilização foi quebrada.' },
    { question: 'O que significa "Hajime" no judô?', answers: ['Pare', 'Continue', 'Comece', 'Descanso'], correct: 2, explanation: 'Hajime é o comando para começar a luta.' },
    { question: 'Quem introduziu o judô no Brasil?', answers: ['Jigoro Kano', 'Mitsuyo Maeda', 'Carlos Gracie', 'Helio Gracie'], correct: 1, explanation: 'Mitsuyo Maeda, "Conde Koma", introduziu o judô no Brasil em 1914.' },
    { question: 'Em que cidade o judô foi primeiro ensinado no Brasil?', answers: ['São Paulo', 'Rio de Janeiro', 'Belém do Pará', 'Brasília'], correct: 2, explanation: 'Mitsuyo Maeda estabeleceu-se em Belém do Pará.' },
    { question: 'Qual família brasileira foi influenciada pelo judô de Maeda?', answers: ['Família Gracie', 'Família Machado', 'Família Vieira', 'Família Santos'], correct: 0, explanation: 'A família Gracie foi influenciada pelo judô de Mitsuyo Maeda.' },
    { question: 'O que significa "Mate" no judô?', answers: ['Continue', 'Pare', 'Lute', 'Descanso'], correct: 1, explanation: 'Mate é o comando para parar a luta temporariamente.' },
    { question: 'O que significa "Sonomama" no judô?', answers: ['Interrupção temporária', 'Continue', 'Lute', 'Descanso'], correct: 0, explanation: 'Sonomama é o comando para manter a posição atual.' },
    { question: 'O que significa "Yoshi" no judô?', answers: ['Pare', 'Lute', 'Continue', 'Descanso'], correct: 2, explanation: 'Yoshi é o comando para continuar a luta.' },
  ],
  hard: [
    { question: 'Qual é o nome da técnica de estrangulamento mais conhecida?', answers: ['Hadaka-jime', 'Okuri-eri-jime', 'Kata-juji-jime', 'Sankaku-jime'], correct: 0, explanation: 'Hadaka-jime (estrangulamento nu) é uma das mais fundamentais.' },
    { question: 'Qual é o nome da técnica de projeção com sacrifício?', answers: ['Tomoe-nage', 'Seoi-nage', 'O-goshi', 'Tai-otoshi'], correct: 0, explanation: 'Tomoe-nage é uma técnica de projeção com sacrifício.' },
    { question: 'O que significa "Hansoku-make" no judô?', answers: ['Ponto completo', 'Penalidade leve', 'Penalidade grave', 'Desqualificação'], correct: 3, explanation: 'Hansoku-make é a desqualificação por infrações graves.' },
    { question: 'O que significa "Sore-made" no judô?', answers: ['Continue', 'Pare', 'Lute', 'Fim da luta'], correct: 3, explanation: 'Sore-made indica o fim da luta.' },
    { question: 'Qual é o nome da imobilização lateral de quatro pontos?', answers: ['Kesa-gatame', 'Kami-shiho-gatame', 'Yoko-shiho-gatame', 'Tate-shiho-gatame'], correct: 2, explanation: 'Yoko-shiho-gatame utiliza quatro pontos de contato.' },
    { question: 'Qual é o nome da imobilização superior de quatro pontos?', answers: ['Kesa-gatame', 'Kami-shiho-gatame', 'Yoko-shiho-gatame', 'Tate-shiho-gatame'], correct: 1, explanation: 'Kami-shiho-gatame é a imobilização superior.' },
    { question: 'Qual é o nome da técnica de projeção com joelho?', answers: ['Hiza-guruma', 'Seoi-nage', 'O-goshi', 'Tai-otoshi'], correct: 0, explanation: 'Hiza-guruma utiliza o joelho como ponto de apoio.' },
    { question: 'Qual técnica utiliza a gola do judogi para estrangulamento?', answers: ['Hadaka-jime', 'Okuri-eri-jime', 'Kata-juji-jime', 'Sankaku-jime'], correct: 1, explanation: 'Okuri-eri-jime utiliza a gola do judogi.' },
    { question: 'Qual técnica de estrangulamento usa os braços em cruz?', answers: ['Hadaka-jime', 'Okuri-eri-jime', 'Kata-juji-jime', 'Sankaku-jime'], correct: 2, explanation: 'Kata-juji-jime utiliza os braços em formato de cruz.' },
    { question: 'Qual técnica de projeção usa quadril em movimento diagonal?', answers: ['Koshi-guruma', 'Seoi-nage', 'O-goshi', 'Tai-otoshi'], correct: 0, explanation: 'Koshi-guruma utiliza o quadril em movimento diagonal.' },
    { question: 'Qual é a imobilização vertical de quatro pontos?', answers: ['Kesa-gatame', 'Kami-shiho-gatame', 'Yoko-shiho-gatame', 'Tate-shiho-gatame'], correct: 3, explanation: 'Tate-shiho-gatame é a imobilização vertical.' },
    { question: 'Qual técnica de projeção usa as pernas em triângulo?', answers: ['Hadaka-jime', 'Okuri-eri-jime', 'Kata-juji-jime', 'Sankaku-jime'], correct: 3, explanation: 'Sankaku-jime usa as pernas em formato de triângulo.' },
    { question: 'Qual técnica de projeção usa tornozelo como apoio?', answers: ['Ashi-guruma', 'Seoi-nage', 'O-goshi', 'Tai-otoshi'], correct: 0, explanation: 'Ashi-guruma utiliza o tornozelo como ponto de apoio.' },
    { question: 'Uke-goshi usa o quadril como ponto de apoio?', answers: ['Dinâmico', 'Estático', 'Rotativo', 'Nenhum'], correct: 1, explanation: 'Uke-goshi utiliza o quadril como ponto de apoio estático.' },
    { question: 'Qual é o nome da técnica de projeção com corpo como alavanca?', answers: ['O-goshi', 'Seoi-nage', 'Tai-otoshi', 'Uke-goshi'], correct: 2, explanation: 'Tai-otoshi utiliza o corpo como alavanca.' },
  ],
};

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Embaralha as alternativas de cada pergunta e atualiza o índice da resposta correta. */
function shuffleAnswersInQuestions(questions) {
  return questions.map((q) => {
    const order = shuffle(q.answers.map((_, i) => i));
    const answers = order.map((i) => q.answers[i]);
    const correct = order.indexOf(q.correct);
    return { ...q, answers, correct };
  });
}

/** Número de perguntas por nível: 1–3 = 7, 4–6 = 10. */
export const PERGUNTAS_POR_NIVEL_MAP = { 1: 7, 2: 7, 3: 7, 4: 10, 5: 10, 6: 10 };

export function getPerguntasPorNivel(nivel) {
  return PERGUNTAS_POR_NIVEL_MAP[Math.max(1, Math.min(6, Number(nivel) || 1))] ?? 7;
}

/** XP por acerto no modo ranking. */
export const XP_POR_ACERTO = 10;

/** Categorias/títulos por nível (apenas 6 níveis). */
export const CATEGORIAS_NIVEL = {
  1: 'Kohai',
  2: 'Aprendiz',
  3: 'Ninja',
  4: 'Samurai',
  5: 'Monge',
  6: 'Sensei',
};

/** Último nível do quiz. */
export const MAX_NIVEL = 6;

/**
 * Retorna o número correto de perguntas para o nível (7 para 1–3, 10 para 4–6).
 */
export function getQuestionsForLevel(nivel) {
  const n = Math.max(1, Math.min(6, Number(nivel) || 1));
  const total = getPerguntasPorNivel(n);
  let pool = [];
  if (n <= 2) pool = [...QUESTIONS_BY_DIFFICULTY.easy];
  else if (n <= 4) pool = [...QUESTIONS_BY_DIFFICULTY.easy, ...QUESTIONS_BY_DIFFICULTY.medium];
  else pool = [...QUESTIONS_BY_DIFFICULTY.easy, ...QUESTIONS_BY_DIFFICULTY.medium, ...QUESTIONS_BY_DIFFICULTY.hard];
  const chosen = shuffle([...pool]).slice(0, total);
  return shuffleAnswersInQuestions(chosen);
}

export function getQuestions(difficulty) {
  let list;
  if (difficulty === 'all') {
    const all = [...QUESTIONS_BY_DIFFICULTY.easy, ...QUESTIONS_BY_DIFFICULTY.medium, ...QUESTIONS_BY_DIFFICULTY.hard];
    list = shuffle(all).slice(0, 45);
  } else {
    const base = QUESTIONS_BY_DIFFICULTY[difficulty] || QUESTIONS_BY_DIFFICULTY.easy;
    list = shuffle([...base]).slice(0, 15);
  }
  return shuffleAnswersInQuestions(list);
}
