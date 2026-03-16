// Normaliza texto: minúsculas, sem acento, sem pontuação, trim
export function normalizarTexto(texto) {
  if (!texto) return '';
  let t = String(texto).toLowerCase();
  t = t.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  t = t.replace(/[^a-z0-9\s]/g, '');
  return t.trim();
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

export function pronunciaCorreta(alvo, falado, threshold = 0.85) {
  const score = similaridade(alvo, falado);
  return { ok: score >= threshold, score };
}

