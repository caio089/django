/**
 * Cliente API para o backend Django.
 * Usa proxy em dev (Vite) e URL base em produção.
 */

const getBaseUrl = () => {
  if (import.meta.env.DEV) return ''; // Vite proxy encaminha para Django
  return import.meta.env.VITE_API_URL || '';
};

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
  const res = await fetch(`${getBaseUrl()}/api/csrf/`, { credentials: 'include' });
  if (!res.ok) {
    if (res.status === 502 || res.status === 503) throw new Error('Backend offline. Rode: npm run dev');
    throw new Error('Falha ao obter CSRF');
  }
  return res.json();
}

export async function apiLogin(email, senha) {
  const res = await fetch(`${getBaseUrl()}/api/login/`, {
    method: 'POST',
    credentials: 'include',
    headers: headers(),
    body: JSON.stringify({ email, senha }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status === 502 || res.status === 503) throw new Error('Backend offline. Certifique-se que o Django está rodando (npm run dev)');
    throw new Error(data.error || 'Erro ao fazer login');
  }
  return data;
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
