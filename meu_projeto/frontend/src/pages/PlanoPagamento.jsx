import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowLeft,
  Shield,
  Lock,
  CreditCard,
  Copy,
  Check,
  X,
  Loader2,
  QrCode,
} from 'lucide-react';
import DojoBackground from '../components/DojoBackground';
import { fetchCsrf, apiMe, getPlanoDetail, criarPagamento, gerarPix, verificarStatusPagamento } from '../api';

const ACCENT = 'rgb(180, 50, 55)';
const GOLD = 'rgb(212, 175, 55)';

export default function PlanoPagamento() {
  const { planoId } = useParams();
  const [plano, setPlano] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [cpf, setCpf] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState(null);
  const [paymentLoading, setPaymentLoading] = useState(false);
  const [paymentError, setPaymentError] = useState(null);
  const [pixData, setPixData] = useState(null);
  const [copied, setCopied] = useState(false);
  const [pixLocalPaymentId, setPixLocalPaymentId] = useState(null);
  const [pixStatus, setPixStatus] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      await fetchCsrf().catch(() => {});
      try {
        const [planoRes, userRes] = await Promise.all([
          getPlanoDetail(planoId),
          apiMe().catch(() => null),
        ]);
        if (cancelled) return;
        setPlano(planoRes);
        if (userRes) {
          setNome(userRes.nome || '');
          setEmail(userRes.email || '');
        }
      } catch (e) {
        setError(e?.message || 'Erro ao carregar plano');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [planoId]);

  const handlePix = async () => {
    if (!plano || !nome?.trim() || !email?.trim()) {
      setPaymentError('Preencha nome e e-mail.');
      return;
    }
    setPaymentError(null);
    setPaymentLoading(true);
    try {
      const created = await criarPagamento(plano.id, {
        nome: nome.trim(),
        email: email.trim(),
        telefone: telefone.trim(),
        cpf: cpf.trim(),
      });
      if (!created.payment_id) throw new Error('Resposta inválida');
      const pix = await gerarPix(created.payment_id);
      if (!pix.qr_code_base64 && !pix.qr_code) throw new Error(pix.error || 'PIX não gerado');
      setPixLocalPaymentId(created.payment_id);
      setPixStatus('pending');
      setPixData({
        qr_code_base64: pix.qr_code_base64,
        qr_code: pix.qr_code,
        amount: pix.amount,
        currency: pix.currency_id || 'BRL',
      });
      setModalMode('pix');
      setModalOpen(true);
    } catch (e) {
      setPaymentError(e?.message || 'Erro ao gerar PIX');
    } finally {
      setPaymentLoading(false);
    }
  };

  const handleCartao = async () => {
    if (!plano || !nome?.trim() || !email?.trim()) {
      setPaymentError('Preencha nome e e-mail.');
      return;
    }
    setPaymentError(null);
    setPaymentLoading(true);
    try {
      const created = await criarPagamento(plano.id, {
        nome: nome.trim(),
        email: email.trim(),
        telefone: telefone.trim(),
        cpf: cpf.trim(),
      });
      // Sempre ir direto para o checkout do Mercado Pago
      const prefId = created.preference_id != null ? String(created.preference_id) : null;
      const urlFromApi =
        (typeof created.init_point === 'string' && created.init_point.includes('mercadopago.com.br')
          ? created.init_point
          : null) ||
        (prefId ? `https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=${prefId}` : null);
      if (urlFromApi) {
        setPaymentError(null);
        // Redireciona imediatamente para o Mercado Pago
        window.location.href = urlFromApi;
        return;
      }
      throw new Error('Resposta inválida do servidor. Tente novamente.');
    } catch (e) {
      setPaymentError(e?.message || 'Erro ao criar pagamento');
      setPaymentLoading(false);
    }
  };

  const copyPixCode = () => {
    if (pixData?.qr_code) {
      navigator.clipboard.writeText(pixData.qr_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const closeModal = () => {
    setModalOpen(false);
    setModalMode(null);
    setPixData(null);
    setPixStatus(null);
    setPixLocalPaymentId(null);
  };

  useEffect(() => {
    if (!modalOpen || modalMode !== 'pix' || !pixLocalPaymentId) return;
    let cancelled = false;
    let intervalId;

    const pollStatus = async () => {
      try {
        const status = await verificarStatusPagamento(pixLocalPaymentId);
        if (cancelled) return;
        setPixStatus(status?.status || null);
        if (status?.status === 'approved' && status?.assinatura_ativa) {
          setPaymentError(null);
          setModalOpen(false);
          alert('Pagamento aprovado! Seu acesso premium foi liberado.');
          window.location.reload();
        }
      } catch (_e) {
        // Mantém polling silencioso para não atrapalhar o fluxo do usuário.
      }
    };

    pollStatus();
    intervalId = window.setInterval(pollStatus, 5000);
    return () => {
      cancelled = true;
      if (intervalId) window.clearInterval(intervalId);
    };
  }, [modalOpen, modalMode, pixLocalPaymentId]);

  if (loading) {
    return (
      <div className="min-h-screen relative font-display antialiased flex items-center justify-center">
        <DojoBackground accentColor={ACCENT} />
        <div className="flex flex-col items-center gap-4 text-white">
          <Loader2 className="w-10 h-10 animate-spin" style={{ color: ACCENT }} />
          <p className="text-slate-400">Carregando plano...</p>
        </div>
      </div>
    );
  }

  if (error || !plano) {
    return (
      <div className="min-h-screen relative font-display antialiased flex items-center justify-center px-4">
        <DojoBackground accentColor={ACCENT} />
        <div className="text-center">
          <p className="text-red-400 mb-4">{error || 'Plano não encontrado'}</p>
          <Link
            to="/payments/planos"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-white"
            style={{ backgroundColor: ACCENT }}
          >
            <ArrowLeft className="w-4 h-4" /> Voltar aos planos
          </Link>
        </div>
      </div>
    );
  }

  const precoFormatado = Number(plano.preco).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });

  return (
    <div className="min-h-screen relative font-display antialiased overflow-x-hidden">
      <DojoBackground accentColor={ACCENT} />

      <header className="fixed top-0 left-0 right-0 z-40 bg-black/60 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link
            to="/payments/planos"
            className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <span className="font-jp text-slate-500 text-sm tracking-widest">支払い — Pagamento</span>
        </div>
      </header>

      <section className="pt-28 pb-8 px-4 max-w-xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-3xl border border-white/10 overflow-hidden"
          style={{
            background: 'linear-gradient(180deg, rgba(180,50,55,0.1) 0%, rgba(0,0,0,0.35) 100%)',
            boxShadow: `0 25px 50px -12px rgba(0,0,0,0.4), 0 0 40px -10px ${ACCENT}30`,
          }}
        >
          <div className="h-1.5 w-full" style={{ background: `linear-gradient(90deg, ${ACCENT}, ${GOLD})` }} />
          <div className="p-8">
            <h1
              className="text-2xl font-bold text-white mb-1"
              style={{ fontFamily: "'Orbitron', sans-serif" }}
            >
              {plano.nome}
            </h1>
            <p className="text-4xl font-black text-white tracking-tight mb-2">
              {precoFormatado}
              <span className="text-slate-400 text-base font-normal ml-1">/ {plano.duracao_dias} dias</span>
            </p>
            <p className="text-slate-400 text-sm">{plano.descricao}</p>
          </div>
        </motion.div>
      </section>

      <section className="max-w-xl mx-auto px-4 pb-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
        >
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <Lock className="w-4 h-4" style={{ color: ACCENT }} />
            Dados para pagamento seguro
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-slate-400 text-sm mb-1">Nome *</label>
              <input
                type="text"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-[rgb(180,50,55)]/50 focus:ring-1 focus:ring-[rgb(180,50,55)]/30 outline-none transition"
                placeholder="Seu nome"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">E-mail *</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-[rgb(180,50,55)]/50 focus:ring-1 focus:ring-[rgb(180,50,55)]/30 outline-none transition"
                placeholder="seu@email.com"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">Telefone</label>
              <input
                type="tel"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-white/20 outline-none transition"
                placeholder="(11) 99999-9999"
              />
            </div>
            <div>
              <label className="block text-slate-400 text-sm mb-1">CPF</label>
              <input
                type="text"
                value={cpf}
                onChange={(e) => setCpf(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-white/20 outline-none transition"
                placeholder="000.000.000-00"
              />
            </div>
          </div>
          {paymentError && (
            <p className="mt-4 text-red-400 text-sm">{paymentError}</p>
          )}
        </motion.div>
      </section>

      <section className="max-w-xl mx-auto px-4 pb-6">
        <p className="text-slate-500 text-sm text-center mb-4">Escolha a forma de pagamento</p>
        <div className="grid grid-cols-2 gap-4">
          <motion.button
            type="button"
            onClick={handlePix}
            disabled={paymentLoading}
            className="flex flex-col items-center gap-3 p-6 rounded-2xl border border-white/10 bg-white/[0.04] hover:bg-white/[0.07] hover:border-[rgb(180,50,55)]/40 transition-all disabled:opacity-60"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {paymentLoading ? (
              <Loader2 className="w-10 h-10 animate-spin text-white" />
            ) : (
              <QrCode className="w-10 h-10" style={{ color: ACCENT }} />
            )}
            <span className="text-white font-semibold">PIX</span>
            <span className="text-slate-400 text-xs text-center">QR Code ou copia e cola</span>
          </motion.button>
          <motion.button
            type="button"
            onClick={handleCartao}
            disabled={paymentLoading}
            className="flex flex-col items-center gap-3 p-6 rounded-2xl border border-white/10 bg-white/[0.04] hover:bg-white/[0.07] hover:border-[rgb(180,50,55)]/40 transition-all disabled:opacity-60"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <CreditCard className="w-10 h-10" style={{ color: ACCENT }} />
            <span className="text-white font-semibold">Cartão</span>
            <span className="text-slate-400 text-xs text-center">Crédito ou débito</span>
          </motion.button>
        </div>
      </section>

      <section className="max-w-xl mx-auto px-4 pb-24 flex items-center justify-center gap-6 text-slate-400 text-sm">
        <span className="flex items-center gap-2">
          <Shield className="w-4 h-4" style={{ color: ACCENT }} />
          Ambiente seguro
        </span>
        <span className="flex items-center gap-2">
          <Lock className="w-4 h-4" style={{ color: ACCENT }} />
          Dados criptografados
        </span>
      </section>

      <AnimatePresence>
        {modalOpen && modalMode === 'pix' && pixData && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeModal}
          >
            <motion.div
              className="rounded-3xl border border-white/10 bg-[#0f1115] p-8 max-w-md w-full shadow-2xl"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              style={{ boxShadow: `0 0 60px ${ACCENT}20` }}
            >
              <div className="flex items-center justify-between mb-6">
                <h3
                  className="text-lg font-bold text-white"
                  style={{ fontFamily: "'Orbitron', sans-serif" }}
                >
                  Pague com PIX
                </h3>
                <button
                  type="button"
                  onClick={closeModal}
                  className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-slate-400 text-sm mb-4">
                Valor: <span className="text-white font-semibold">
                  {Number(pixData.amount).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                </span>
              </p>
              {pixData.qr_code_base64 ? (
                <div className="flex justify-center mb-6 p-4 rounded-2xl bg-white">
                  <img
                    src={pixData.qr_code_base64}
                    alt="QR Code PIX"
                    className="w-48 h-48 object-contain"
                  />
                </div>
              ) : null}
              {pixData.qr_code && (
                <div className="space-y-2">
                  <label className="text-slate-400 text-xs block">Código PIX (copiar e colar)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      readOnly
                      value={pixData.qr_code}
                      className="flex-1 px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs font-mono truncate"
                    />
                    <button
                      type="button"
                      onClick={copyPixCode}
                      className="px-4 py-2 rounded-xl text-white flex items-center gap-2 shrink-0"
                      style={{ backgroundColor: ACCENT }}
                    >
                      {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      {copied ? 'Copiado' : 'Copiar'}
                    </button>
                  </div>
                </div>
              )}
              <p className="text-slate-500 text-xs mt-6 text-center">
                Abra o app do seu banco, escaneie o QR Code ou cole o código. O pagamento será confirmado em instantes.
              </p>
              <p className="text-slate-400 text-xs mt-2 text-center">
                Status: {pixStatus === 'approved' ? 'Aprovado' : pixStatus === 'pending' ? 'Aguardando pagamento' : 'Verificando...'}
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
