/**
 * Cliente API para o backend Django.
 * Usa proxy em dev (Vite) e URL base em produção.
 */

const getBaseUrl = () => {
  if (import.meta.env.DEV) return ''; // Vite proxy encaminha para Django
  return import.meta.env.VITE_API_URL || '';
};

const DEFAULT_TIMEOUT_MS = 10000;

async function fetchWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } catch (err) {
    if (err?.name === 'AbortError') {
      throw new Error('Tempo de resposta do backend esgotado. Verifique o servidor/API.');
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

const getCsrfToken = () => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : null;
};

const headers = (contentType = 'application/json') => {
  const h = {
    'Content-Type': contentType,
    Accept: 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  };
  const csrf = getCsrfToken();
  if (csrf) h['X-CSRFToken'] = csrf;
  return h;
};

export async function fetchCsrf() {
  const res = await fetchWithTimeout(`${getBaseUrl()}/api/csrf/`, { credentials: 'include' });
  if (!res.ok) {
    if (res.status === 502 || res.status === 503) throw new Error('Backend offline. Rode: npm run dev');
    throw new Error('Falha ao obter CSRF');
  }
  return res.json();
}

export async function apiLogin(email, senha) {
  try {
    const res = await fetch(`${getBaseUrl()}/api/login/`, {
      method: 'POST',
      credentials: 'include',
      headers: headers(),
      body: JSON.stringify({ email, senha }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      if (res.status === 502 || res.status === 503) return Promise.reject(new Error('Backend offline. Certifique-se que o Django está rodando (npm run dev).'));
      return Promise.reject(new Error(typeof data?.error === 'string' ? data.error : 'Erro ao fazer login. Verifique email e senha.'));
    }
    return data;
  } catch (err) {
    if (err instanceof Error) return Promise.reject(err);
    return Promise.reject(new Error('Falha de conexão. Verifique se o backend está rodando.'));
  }
}

export async function apiRegister({ nome, idade, faixa, email, senha }) {
  const res = await fetch(`${getBaseUrl()}/api/register/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ nome, idade: parseInt(idade, 10), faixa, email, senha }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status === 500 || res.status === 503) throw new Error(data.error || 'Erro no servidor. Tente novamente.');
    throw new Error(data.error || 'Erro ao cadastrar');
  }
  return data;
}

export async function apiLogout() {
  const res = await fetch(`${getBaseUrl()}/api/logout/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Erro ao sair');
  return data;
}

export async function apiMe() {
  const res = await fetch(`${getBaseUrl()}/api/me/`, { credentials: 'include' });
  const data = await res.json();
  if (!res.ok) throw new Error('Erro ao buscar usuário');
  return data;
}

/** GET ranking do quiz (público). */
export async function getQuizRanking(limit = 50) {
  const res = await fetch(`${getBaseUrl()}/quiz/api/ranking/?limit=${limit}`, { credentials: 'include' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Erro ao carregar ranking');
  return data;
}

/** POST iniciar tentativa do quiz (server-side timing). */
export async function startQuizAttempt({ nivel_quiz, question_keys }) {
  const res = await fetch(`${getBaseUrl()}/quiz/api/start-attempt/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ nivel_quiz, question_keys }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao iniciar tentativa');
  return data;
}

/** POST finalizar tentativa do quiz (XP calculado no servidor). */
export async function submitQuizAttempt({ attempt_id, correct_keys, nickname, dojo, cidade }) {
  const res = await fetch(`${getBaseUrl()}/quiz/api/submit-attempt/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ attempt_id, correct_keys, nickname, dojo, cidade }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao enviar resultado');
  return data;
}

/** POST resultado do quiz (LEGADO). Mantido para compatibilidade. */
export async function submitQuizResult(payload) {
  const res = await fetch(`${getBaseUrl()}/quiz/api/submit/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao enviar resultado');
  return data;
}

// ——— Pagamentos (payments) ———

/** GET detalhes do plano por ID (usa /api para o mesmo proxy do login/me) */
export async function getPlanoDetail(planoId) {
  const res = await fetch(`${getBaseUrl()}/api/payments/plano/${planoId}/`, { credentials: 'include' });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Plano não encontrado');
  return data;
}

/** POST criar pagamento (retorna payment_id e preference_id para checkout) — usa /api */
export async function criarPagamento(planoId, { nome, email, telefone = '', cpf = '' }) {
  const body = new URLSearchParams({
    nome: nome || '',
    email: email || '',
    telefone: telefone || '',
    cpf: cpf || '',
  });
  const res = await fetch(`${getBaseUrl()}/api/payments/criar-pagamento/${planoId}/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': getCsrfToken() || '',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: body.toString(),
  });
  const contentType = res.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    const text = await res.text();
    if (res.status === 302 || res.status === 401 || res.status === 403 || (res.status === 200 && text.includes('<!DOCTYPE'))) {
      throw new Error('Faça login novamente e tente de novo.');
    }
    throw new Error('Resposta inválida do servidor.');
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao criar pagamento');
  return data;
}

/** GET URL do Mercado Pago para redirecionar a partir de payment_id (quando cai em /payments/checkout/:id) */
export async function getCheckoutRedirectUrl(paymentId) {
  const res = await fetch(`${getBaseUrl()}/api/payments/checkout-redirect/${paymentId}/`, { credentials: 'include' });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.init_point) throw new Error(data.error || 'Não foi possível obter o link de pagamento');
  return data.init_point;
}

// ——— Admin Panel API ———
const adminBase = () => getBaseUrl() + '/api/admin';

/** GET verificar se está logado como admin */
export async function adminMe() {
  const res = await fetchWithTimeout(`${adminBase()}/me/`, { credentials: 'include' });
  return res.json();
}

/** POST login admin: { username, password } */
export async function adminLogin(username, password) {
  await fetchCsrf();
  const res = await fetchWithTimeout(`${adminBase()}/login/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao fazer login');
  return data;
}

/** POST logout admin */
export async function adminLogout() {
  const res = await fetch(`${adminBase()}/logout/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao sair');
  return data;
}

/** GET dashboard completo */
export async function adminDashboard() {
  // Dashboard faz muitas agregações no banco; em produção pode levar mais tempo.
  const res = await fetchWithTimeout(`${adminBase()}/dashboard/`, { credentials: 'include' }, 45000);
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 || res.status === 403) throw new Error('Acesso negado');
  if (!res.ok) throw new Error(data.error || 'Erro ao carregar');
  return data;
}

/** GET dashboard (paginado para all_users) */
export async function adminDashboardPage({ page = 1, page_size = 50 } = {}) {
  const qs = new URLSearchParams({ page: String(page), page_size: String(page_size) });
  const res = await fetchWithTimeout(`${adminBase()}/dashboard/?${qs.toString()}`, { credentials: 'include' }, 45000);
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 || res.status === 403) throw new Error('Acesso negado');
  if (!res.ok) throw new Error(data.error || 'Erro ao carregar');
  return data;
}

/** POST dar premium: { user_id ou user_email, plan_id } */
export async function adminGivePremium(payload) {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/give-premium/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro');
  return data;
}

/** POST remover premium: { user_id } */
export async function adminRemovePremium(userId) {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/remove-premium/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ user_id: userId }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro');
  return data;
}

/** POST excluir usuário: { user_id, confirm: "excluir" } */
export async function adminDeleteUser(userId) {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/delete-user/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ user_id: userId, confirm: 'excluir' }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro');
  return data;
}

/** POST refresh cache */
export async function adminRefreshCache() {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/refresh-cache/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro');
  return data;
}

/** GET/POST configurações financeiras do dashboard (custos). */
export async function adminFinanceSettings(payload = null) {
  if (!payload) {
    const res = await fetchWithTimeout(`${adminBase()}/finance-settings/`, { credentials: 'include' }, 15000);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || 'Erro ao carregar configurações financeiras');
    return data;
  }
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/finance-settings/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao salvar configurações financeiras');
  return data;
}

/** POST zerar receita total exibida (offset). */
export async function adminResetTotalRevenue() {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/finance-reset-revenue/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao zerar receita total');
  return data;
}

/** POST corrigir assinaturas */
export async function adminCorrigirAssinaturas() {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/corrigir-assinaturas/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro');
  return data;
}

/** POST envio de email remarketing */
export async function adminSendMarketingEmail(payload) {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/send-marketing-email/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao enviar e-mail');
  return data;
}

/** GET pagamentos (admin) paginado */
export async function adminPayments({ page = 1, page_size = 50 } = {}) {
  const qs = new URLSearchParams({ page: String(page), page_size: String(page_size) });
  const res = await fetchWithTimeout(`${adminBase()}/payments/?${qs.toString()}`, { credentials: 'include' }, 45000);
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 || res.status === 403) throw new Error('Acesso negado');
  if (!res.ok) throw new Error(data.error || 'Erro ao carregar pagamentos');
  return data;
}

/** GET webhooks (admin) paginado */
export async function adminWebhooks({ page = 1, page_size = 50 } = {}) {
  const qs = new URLSearchParams({ page: String(page), page_size: String(page_size) });
  const res = await fetchWithTimeout(`${adminBase()}/webhooks/?${qs.toString()}`, { credentials: 'include' }, 45000);
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 || res.status === 403) throw new Error('Acesso negado');
  if (!res.ok) throw new Error(data.error || 'Erro ao carregar webhooks');
  return data;
}

/** POST reprocessar pagamento (admin) */
export async function adminReprocessPayment(payment_id_mp) {
  await fetchCsrf();
  const res = await fetch(`${adminBase()}/reprocess-payment/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ payment_id_mp }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao reprocessar pagamento');
  return data;
}

/** POST gerar PIX (retorna qr_code e qr_code_base64) — usa /api */
export async function gerarPix(paymentId) {
  const res = await fetch(`${getBaseUrl()}/api/payments/gerar-pix/${paymentId}/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': getCsrfToken() || '',
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao gerar PIX');
  return data;
}

/** GET status atual do pagamento e assinatura */
export async function verificarStatusPagamento(paymentId) {
  const res = await fetch(`${getBaseUrl()}/api/payments/verificar-status/${paymentId}/`, {
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Erro ao verificar status do pagamento');
  return data;
}
