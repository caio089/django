// Normaliza texto: minúsculas, sem acento, sem pontuação, trim
export function normalizarTexto(texto) {
  if (!texto) return '';
  let t = String(texto).toLowerCase();
  t = t.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  t = t.replace(/[^a-z0-9\s]/g, '');
  return t.trim();
}

// Variantes de números (PT e romaji) — API de voz ouve diferente
const NUMERO_VARIANTES = {
  um: ['hum', 'umm'],
  dois: ['doiz'],
  três: ['tres', 'trez'],
  tres: ['trez'],
  quatro: ['cuatro', 'cuantro', 'quatru'],
  cinco: ['sinco', 'sinko', 'cinko'],
  seis: ['seix', 'ceiz'],
  sete: ['seti'],
  oito: ['oit', 'oitu'],
  nove: ['novi'],
  dez: ['des', 'deiz'],
  ichi: ['itxi', 'ixi', 'itchi', 'iti'],
  ni: ['nii'],
  san: ['sã', 'sam', 'saan', 'sann'],
  shi: ['xi', 'chi', 'si', 'yon'],
  go: ['gou', 'gô'],
  roku: ['rocu', 'roco', 'rocou'],
  shichi: ['xichi', 'shiti', 'nana'],
  hachi: ['hati', 'hatchi'],
  ku: ['cu', 'kuu', 'kyuu', 'kyu'],
  ju: ['jyu', 'juu', 'jyuu'],
};

// Aplica variantes comuns de transcrição errada do reconhecimento de voz
function variantesTranscricao(texto) {
  if (!texto) return [''];
  const n = normalizarTexto(texto);
  const variantes = new Set([n]);
  // Variantes específicas para números (PT e romaji)
  if (NUMERO_VARIANTES[n]) {
    NUMERO_VARIANTES[n].forEach((v) => variantes.add(v));
  }
  // Duplicatas de consoantes (API pode ouvir "rr" como "r", "ss" como "s")
  if (n.includes('rr')) variantes.add(n.replace(/rr/g, 'r'));
  if (n.includes('ss')) variantes.add(n.replace(/ss/g, 's'));
  if (n.includes('ll')) variantes.add(n.replace(/ll/g, 'l'));
  // "ch" e "x" soam parecido em português
  if (n.includes('ch')) variantes.add(n.replace(/ch/g, 'x'));
  if (n.includes('x')) variantes.add(n.replace(/x/g, 'ch'));
  // "g" e "j" confusão comum
  if (n.includes('g')) variantes.add(n.replace(/g/g, 'j'));
  if (n.includes('j')) variantes.add(n.replace(/j/g, 'g'));
  // "ão" às vezes vira "am" ou "om"
  if (n.includes('ao')) {
    variantes.add(n.replace(/ao/g, 'am'));
    variantes.add(n.replace(/ao/g, 'om'));
  }
  // "c" e "qu" antes de e/i
  if (n.includes('qu')) variantes.add(n.replace(/qu/g, 'c'));
  if (n.includes('c') && (n.includes('ce') || n.includes('ci'))) variantes.add(n.replace(/ce/g, 'que').replace(/ci/g, 'qui'));
  return Array.from(variantes);
}

// Distância de Levenshtein simples
export function distanciaLevenshtein(a, b) {
  const s = normalizarTexto(a);
  const t = normalizarTexto(b);
  const m = s.length;
  const n = t.length;
  if (m === 0) return n;
  if (n === 0) return m;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = s[i - 1] === t[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1, // remoção
        dp[i][j - 1] + 1, // inserção
        dp[i - 1][j - 1] + cost // substituição
      );
    }
  }
  return dp[m][n];
}

export function similaridade(a, b) {
  const s = normalizarTexto(a);
  const t = normalizarTexto(b);
  if (!s || !t) return 0;
  const dist = distanciaLevenshtein(s, t);
  const maxLen = Math.max(s.length, t.length) || 1;
  return 1 - dist / maxLen;
}

// Verifica se alvo está contido em falado (ex: "puxar" em "puxar o adversário")
function contido(alvo, falado) {
  const a = normalizarTexto(alvo);
  const f = normalizarTexto(falado);
  if (!a) return true;
  const palavras = f.split(/\s+/);
  return palavras.some((p) => p === a || p.includes(a) || similaridade(p, a) >= 0.8);
}

export function pronunciaCorreta(alvo, falado, threshold = 0.62) {
  if (!falado || !falado.trim()) return { ok: false, score: 0 };
  const varAlvo = variantesTranscricao(alvo);
  const f = normalizarTexto(falado);
  let best = 0;
  for (const v of varAlvo) {
    const score = similaridade(v, f);
    if (score > best) best = score;
    if (score >= threshold) return { ok: true, score };
  }
  if (best >= threshold) return { ok: true, score: best };
  if (contido(alvo, falado)) return { ok: true, score: best };
  return { ok: best >= threshold, score: best };
}
