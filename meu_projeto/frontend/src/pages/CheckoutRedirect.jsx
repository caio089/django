import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import { getCheckoutRedirectUrl } from '../api';

/**
 * Quando o usuário cai em /payments/checkout/:paymentId (ex.: por link antigo ou redirect),
 * busca a URL do Mercado Pago e redireciona para lá. Assim nunca fica na página HTML do backend.
 */
export default function CheckoutRedirect() {
  const { paymentId } = useParams();
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!paymentId) return;
    let cancelled = false;
    getCheckoutRedirectUrl(Number(paymentId))
      .then((url) => {
        if (cancelled) return;
        if (url && url.includes('mercadopago.com.br')) {
          window.location.href = url;
        } else {
          setError('URL de pagamento inválida');
        }
      })
      .catch((e) => {
        if (!cancelled) setError(e?.message || 'Erro ao carregar pagamento');
      });
    return () => { cancelled = true; };
  }, [paymentId]);

  if (error) {
    return (
      <div className="min-h-screen bg-[#0a0c0f] flex flex-col items-center justify-center px-4 text-white">
        <p className="text-red-400 mb-4">{error}</p>
        <Link to="/payments/planos" className="text-amber-400 hover:underline">
          Voltar aos planos
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0c0f] flex flex-col items-center justify-center px-4 text-white">
      <Loader2 className="w-10 h-10 animate-spin text-amber-500 mb-4" />
      <p className="text-slate-400">Redirecionando para o Mercado Pago...</p>
    </div>
  );
}
