import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Users,
  CreditCard,
  TrendingUp,
  DollarSign,
  LogOut,
  RefreshCw,
  Crown,
  UserMinus,
  Trash2,
  Wrench,
  ChevronRight,
  AlertCircle,
  Loader2,
  BarChart3,
  Zap,
  Mail,
  Send,
} from 'lucide-react';
import {
  adminMe,
  adminLogin,
  adminLogout,
  adminDashboard,
  adminGivePremium,
  adminRemovePremium,
  adminDeleteUser,
  adminRefreshCache,
  adminCorrigirAssinaturas,
  adminSendMarketingEmail,
  fetchCsrf,
} from '../api';

function formatBRL(value) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value || 0);
}

function AdminLogin({ onSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await adminLogin(username, password);
      onSuccess();
    } catch (err) {
      setError(err?.message || 'Usuário ou senha incorretos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0d1117] flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-amber-500/20 border border-amber-500/30 mb-4">
            <Zap className="w-8 h-8 text-amber-400" />
          </div>
          <h1 className="text-2xl font-bold text-white">Painel Admin</h1>
          <p className="text-slate-400 text-sm mt-1">Dojo Online</p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                {error}
              </div>
            )}
            <div>
              <label className="block text-slate-400 text-sm mb-2">Usuário ou e-mail</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50"
                placeholder="Digite seu usuário ou e-mail"
                required
                autoComplete="username"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-2">Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50"
                placeholder="Digite sua senha"
                required
                autoComplete="current-password"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-black font-semibold transition-colors flex items-center justify-center gap-2 disabled:opacity-60"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Entrar'}
            </button>
          </form>
        </div>

        <p className="text-center text-slate-500 text-sm mt-6">
          <Link to="/" className="hover:text-slate-400 transition-colors">← Voltar ao site</Link>
        </p>
      </motion.div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, sub, trend }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-6 hover:bg-white/[0.07] transition-colors"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm">{label}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {sub && <p className="text-slate-500 text-xs mt-1">{sub}</p>}
        </div>
        <div className="w-12 h-12 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center">
          <Icon className="w-6 h-6 text-amber-400" />
        </div>
      </div>
      {trend !== undefined && (
        <p className={`text-xs mt-2 ${trend >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
          {trend >= 0 ? '+' : ''}{trend}% vs mês anterior
        </p>
      )}
    </motion.div>
  );
}

function AdminDashboard({ user, onLogout }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState(null);
  const [modal, setModal] = useState(null);
  const [lastUpdatedAt, setLastUpdatedAt] = useState(null);
  const [sendTo, setSendTo] = useState('selected');
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [marketingSubject, setMarketingSubject] = useState('Convite para ativar seu acesso Premium no Dojo Online');
  const [marketingBody, setMarketingBody] = useState(
    'Ola!\\n\\nEstamos com novidades no Dojo Online e queremos te convidar para ativar o Premium.\\n\\nAcesse: https://www.dojoon.com.br/payments/planos/\\n\\nBons treinos!'
  );
  const [marketingResult, setMarketingResult] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const d = await adminDashboard();
      setData(d);
      setLastUpdatedAt(new Date());
    } catch (err) {
      setError(err?.message || 'Erro ao carregar');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    let intervalId;
    let cancelled = false;

    const start = () => {
      if (intervalId) window.clearInterval(intervalId);
      intervalId = window.setInterval(() => {
        if (cancelled) return;
        if (document.visibilityState !== 'visible') return;
        // atualiza sem bloquear a UI (mantém loading atual apenas na primeira carga)
        adminDashboard()
          .then((d) => {
            if (!cancelled) {
              setData(d);
              setLastUpdatedAt(new Date());
            }
          })
          .catch(() => {});
      }, 15000);
    };

    start();
    return () => {
      cancelled = true;
      if (intervalId) window.clearInterval(intervalId);
    };
  }, []);

  const doAction = async (key, fn) => {
    setActionLoading(key);
    try {
      await fn();
      await load();
      setModal(null);
    } catch (err) {
      setError(err?.message || 'Erro');
    } finally {
      setActionLoading(null);
    }
  };

  const handleGivePremium = (u) => {
    const planId = data?.plans?.[0]?.id;
    if (!planId) {
      setError('Nenhum plano disponível');
      return;
    }
    setModal({
      type: 'give',
      user: u,
      planId,
    });
  };

  const toggleSelectedUser = (id) => {
    setSelectedUsers((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
  };

  const handleSendMarketing = async () => {
    setActionLoading('marketing');
    setMarketingResult('');
    try {
      const resp = await adminSendMarketingEmail({
        subject: marketingSubject,
        body: marketingBody,
        send_to: sendTo,
        user_ids: selectedUsers,
      });
      setMarketingResult(resp?.message || 'E-mail enviado com sucesso');
    } catch (err) {
      setError(err?.message || 'Erro ao enviar e-mail');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-[#0d1117] flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-amber-500 animate-spin" />
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="min-h-screen bg-[#0d1117] flex flex-col items-center justify-center gap-4">
        <p className="text-red-400">{error}</p>
        <button onClick={load} className="px-4 py-2 rounded-lg bg-amber-500/20 text-amber-400 hover:bg-amber-500/30">
          Tentar novamente
        </button>
      </div>
    );
  }

  const s = data?.stats || {};
  const maxRevenue = Math.max(...(data?.monthly_data || []).map((m) => m.revenue), 1);

  return (
    <div className="min-h-screen bg-[#0d1117]">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#0d1117]/90 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-amber-500" />
            <div>
              <h1 className="text-lg font-bold text-white">Painel Admin</h1>
              <p className="text-slate-500 text-xs">Olá, {user?.username}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {lastUpdatedAt && (
              <span className="hidden sm:inline text-xs text-slate-500 mr-1">
                Atualizado {lastUpdatedAt.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
              </span>
            )}
            <a
              href="/django-admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-400 text-sm flex items-center gap-2"
            >
              <Wrench className="w-4 h-4" />
              Django Admin
            </a>
            <button
              onClick={async () => {
                setActionLoading('refresh');
                try {
                  await adminRefreshCache();
                  await load();
                } finally {
                  setActionLoading(null);
                }
              }}
              disabled={actionLoading === 'refresh'}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-400 disabled:opacity-50"
              title="Atualizar cache"
            >
              <RefreshCw className={`w-4 h-4 ${actionLoading === 'refresh' ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={async () => {
                if (!confirm('Confirmar logout?')) return;
                await adminLogout();
                onLogout();
              }}
              className="px-4 py-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-red-400 flex items-center gap-2"
            >
              <LogOut className="w-4 h-4" />
              Sair
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-between">
            <span>{error}</span>
            <button onClick={() => setError('')}>×</button>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard icon={CreditCard} label="Assinaturas ativas" value={s.active_subscriptions ?? 0} />
          <StatCard icon={Users} label="Usuários premium" value={s.unique_premium_users ?? 0} />
          <StatCard
            icon={DollarSign}
            label="Receita total"
            value={formatBRL(s.total_revenue)}
            sub={`Este mês: ${formatBRL(s.current_month_revenue)}`}
          />
          <StatCard
            icon={TrendingUp}
            label="Crescimento"
            value={`${s.growth_percentage ?? 0}%`}
            trend={s.growth_percentage}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <StatCard icon={Users} label="Total de usuários" value={s.total_users ?? 0} sub={`+${s.users_this_month ?? 0} este mês`} />
          <StatCard icon={BarChart3} label="Taxa de conversão" value={`${s.conversion_rate ?? 0}%`} sub="Pagamentos aprovados / total" />
          <StatCard icon={AlertCircle} label="Pagamentos pendentes" value={data?.pending_payments?.length ?? 0} sub="Últimos 7 dias" />
        </div>

        {/* Gráfico receita */}
        {data?.monthly_data?.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 mb-8"
          >
            <h2 className="text-lg font-semibold text-white mb-4">Receita (12 meses)</h2>
            <div className="flex items-end gap-1 h-32">
              {data.monthly_data.map((m, i) => (
                <div key={m.month} className="flex-1 flex flex-col items-center gap-1">
                  <div
                    className="w-full rounded-t bg-amber-500/60 hover:bg-amber-500/80 transition-colors min-h-[4px]"
                    style={{ height: `${Math.max(4, (m.revenue / maxRevenue) * 100)}%` }}
                    title={`${m.month_name}: ${formatBRL(m.revenue)}`}
                  />
                  <span className="text-[10px] text-slate-500 truncate w-full text-center">{m.month_name}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Assinaturas recentes */}
          <div className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
            <h2 className="px-6 py-4 text-lg font-semibold text-white border-b border-white/10">
              Assinaturas recentes
            </h2>
            <div className="divide-y divide-white/5 max-h-80 overflow-y-auto">
              {(data?.recent_subscriptions || []).slice(0, 10).map((a) => (
                <div key={a.id} className="px-6 py-3 flex items-center justify-between hover:bg-white/5">
                  <div>
                    <p className="text-white font-medium">{a.usuario}</p>
                    <p className="text-slate-500 text-sm">{a.plano} · vence {a.data_vencimento}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-500" />
                </div>
              ))}
              {(!data?.recent_subscriptions || data.recent_subscriptions.length === 0) && (
                <p className="px-6 py-8 text-slate-500 text-center">Nenhuma assinatura recente</p>
              )}
            </div>
          </div>

          {/* Usuários recentes + ações */}
          <div className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
            <h2 className="px-6 py-4 text-lg font-semibold text-white border-b border-white/10">
              Usuários recentes
            </h2>
            <div className="divide-y divide-white/5 max-h-80 overflow-y-auto">
              {(data?.recent_users || []).map((u) => (
                <div key={u.id} className="px-6 py-3 flex items-center justify-between gap-2 hover:bg-white/5 group">
                  <div className="min-w-0">
                    <p className="text-white font-medium truncate">{u.nome || u.email}</p>
                    <p className="text-slate-500 text-sm truncate">{u.email}</p>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    {u.premium ? (
                      <span className="px-2 py-0.5 rounded text-xs bg-amber-500/20 text-amber-400">Premium</span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-xs bg-slate-500/20 text-slate-400">Gratuito</span>
                    )}
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                      {!u.premium && data?.plans?.length > 0 && (
                        <button
                          onClick={() => handleGivePremium(u)}
                          className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30"
                          title="Dar premium"
                        >
                          <Crown className="w-4 h-4" />
                        </button>
                      )}
                      {u.premium && (
                        <button
                          onClick={() => {
                            if (confirm(`Remover premium de ${u.email}?`)) {
                              doAction(`rm-${u.id}`, () => adminRemovePremium(u.id));
                            }
                          }}
                          disabled={actionLoading === `rm-${u.id}`}
                          className="p-1.5 rounded-lg bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 disabled:opacity-50"
                          title="Remover premium"
                        >
                          <UserMinus className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={() => {
                          if (confirm(`Excluir usuário ${u.email}? Digite "excluir" na próxima tela.`)) {
                            const c = prompt('Digite "excluir" para confirmar:');
                            if (c?.toLowerCase() === 'excluir') {
                              doAction(`del-${u.id}`, () => adminDeleteUser(u.id));
                            }
                          }
                        }}
                        disabled={actionLoading === `del-${u.id}`}
                        className="p-1.5 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 disabled:opacity-50"
                        title="Excluir usuário"
                      >
                        {actionLoading === `del-${u.id}` ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Lista completa de cadastrados */}
        <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
          <div className="px-6 py-4 border-b border-white/10 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Lista de cadastrados</h2>
            <span className="text-xs text-slate-400">{(data?.all_users || []).length} usuarios</span>
          </div>
          <div className="max-h-96 overflow-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10 text-slate-400">
                  <th className="py-2 px-3 text-left">Sel.</th>
                  <th className="py-2 px-3 text-left">Nome</th>
                  <th className="py-2 px-3 text-left">Email</th>
                  <th className="py-2 px-3 text-left">Cadastro</th>
                  <th className="py-2 px-3 text-left">Ultimo acesso</th>
                  <th className="py-2 px-3 text-center">Status</th>
                  <th className="py-2 px-3 text-right">Acoes</th>
                </tr>
              </thead>
              <tbody>
                {(data?.all_users || []).map((u) => (
                  <tr key={u.id} className="border-b border-white/5 hover:bg-white/5">
                    <td className="py-2 px-3">
                      <input
                        type="checkbox"
                        checked={selectedUsers.includes(u.id)}
                        onChange={() => toggleSelectedUser(u.id)}
                        className="accent-amber-400"
                      />
                    </td>
                    <td className="py-2 px-3 text-white">{u.nome || u.username}</td>
                    <td className="py-2 px-3 text-slate-300">{u.email}</td>
                    <td className="py-2 px-3 text-slate-400">{u.date_joined}</td>
                    <td className="py-2 px-3 text-slate-400">{u.last_login || '-'}</td>
                    <td className="py-2 px-3 text-center">
                      {u.premium ? (
                        <span className="px-2 py-0.5 rounded text-xs bg-amber-500/20 text-amber-400">Premium</span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-xs bg-slate-500/20 text-slate-400">Gratis</span>
                      )}
                    </td>
                    <td className="py-2 px-3">
                      <div className="flex justify-end gap-1">
                        {!u.premium && data?.plans?.length > 0 && (
                          <button
                            onClick={() => handleGivePremium(u)}
                            className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30"
                            title="Dar premium"
                          >
                            <Crown className="w-4 h-4" />
                          </button>
                        )}
                        {u.premium && (
                          <button
                            onClick={() => doAction(`rm-all-${u.id}`, () => adminRemovePremium(u.id))}
                            disabled={actionLoading === `rm-all-${u.id}`}
                            className="p-1.5 rounded-lg bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 disabled:opacity-50"
                            title="Remover premium"
                          >
                            <UserMinus className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Últimos atualizados */}
        <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
          <div className="px-6 py-4 border-b border-white/10">
            <h2 className="text-lg font-semibold text-white">Ultimos atualizados</h2>
            <p className="text-xs text-slate-400 mt-1">Baseado no ultimo login/acesso</p>
          </div>
          <div className="divide-y divide-white/5">
            {(data?.latest_updated_users || []).map((u) => (
              <div key={u.id} className="px-6 py-3 flex items-center justify-between">
                <div>
                  <p className="text-white font-medium">{u.nome}</p>
                  <p className="text-slate-400 text-sm">{u.email}</p>
                </div>
                <div className="text-right">
                  <p className="text-slate-300 text-sm">{u.last_login || 'Nunca logou'}</p>
                  <p className="text-slate-500 text-xs">Cadastro: {u.date_joined}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Remarketing por e-mail */}
        <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
            <Mail className="w-5 h-5 text-amber-400" />
            Remarketing por e-mail
          </h2>
          <div className="grid grid-cols-1 gap-4">
            <div className="flex flex-wrap gap-3">
              <label className="text-sm text-slate-300 flex items-center gap-2">
                <input type="radio" name="sendTo" value="selected" checked={sendTo === 'selected'} onChange={(e) => setSendTo(e.target.value)} />
                Selecionados ({selectedUsers.length})
              </label>
              <label className="text-sm text-slate-300 flex items-center gap-2">
                <input type="radio" name="sendTo" value="all" checked={sendTo === 'all'} onChange={(e) => setSendTo(e.target.value)} />
                Todos cadastrados
              </label>
            </div>
            <input
              value={marketingSubject}
              onChange={(e) => setMarketingSubject(e.target.value)}
              placeholder="Assunto do e-mail"
              className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500"
            />
            <textarea
              value={marketingBody}
              onChange={(e) => setMarketingBody(e.target.value)}
              placeholder="Mensagem"
              rows={6}
              className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500"
            />
            <div className="flex items-center gap-3">
              <button
                onClick={handleSendMarketing}
                disabled={actionLoading === 'marketing' || !marketingSubject.trim() || !marketingBody.trim() || (sendTo === 'selected' && selectedUsers.length === 0)}
                className="px-4 py-2 rounded-lg bg-amber-500 text-black font-semibold hover:bg-amber-400 disabled:opacity-50 flex items-center gap-2"
              >
                {actionLoading === 'marketing' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                Enviar e-mail
              </button>
              {marketingResult && <span className="text-emerald-400 text-sm">{marketingResult}</span>}
            </div>
          </div>
        </div>

        {/* Status assinaturas + Corrigir */}
        <div className="mt-8 flex flex-wrap gap-4 items-center">
          <div className="flex flex-wrap gap-2">
            {Object.entries(data?.status_counts || {}).map(([status, count]) => (
              <span key={status} className="px-3 py-1 rounded-lg bg-white/5 text-slate-400 text-sm">
                {status}: {count}
              </span>
            ))}
          </div>
          <button
            onClick={() => {
              if (confirm('Corrigir assinaturas com ativo=False?')) {
                doAction('corrigir', adminCorrigirAssinaturas);
              }
            }}
            disabled={actionLoading === 'corrigir'}
            className="px-4 py-2 rounded-lg bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 flex items-center gap-2 disabled:opacity-50"
          >
            {actionLoading === 'corrigir' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wrench className="w-4 h-4" />}
            Corrigir assinaturas
          </button>
        </div>
      </main>

      {/* Modal Dar Premium */}
      <AnimatePresence>
        {modal?.type === 'give' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60"
            onClick={() => setModal(null)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="rounded-2xl border border-white/10 bg-[#161b22] p-6 max-w-md w-full"
            >
              <h3 className="text-lg font-semibold text-white mb-2">Dar premium</h3>
              <p className="text-slate-400 text-sm mb-4">
                Para: {modal.user?.nome || modal.user?.email}
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setModal(null)}
                  className="flex-1 py-2 rounded-lg bg-white/10 text-slate-400 hover:bg-white/15"
                >
                  Cancelar
                </button>
                <button
                  onClick={() =>
                    doAction('give', () =>
                      adminGivePremium({
                        user_id: modal.user?.id,
                        user_email: modal.user?.email,
                        plan_id: modal.planId,
                      })
                    )
                  }
                  disabled={actionLoading === 'give'}
                  className="flex-1 py-2 rounded-lg bg-amber-500 text-black font-semibold hover:bg-amber-400 disabled:opacity-50"
                >
                  {actionLoading === 'give' ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : 'Confirmar'}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function AdminPanel() {
  const [auth, setAuth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        await fetchCsrf();
        const me = await adminMe();
        if (mounted) {
          setAuth(me);
        }
      } catch {
        if (mounted) setAuth({ authenticated: false, admin: false });
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0d1117] flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-amber-500 animate-spin" />
      </div>
    );
  }

  if (auth?.authenticated && auth?.admin) {
    return (
      <AdminDashboard
        user={auth}
        onLogout={() => {
          setAuth({ authenticated: false, admin: false });
        }}
      />
    );
  }

  return (
    <AdminLogin
      onSuccess={async () => {
        const me = await adminMe();
        setAuth(me);
      }}
    />
  );
}
