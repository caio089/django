import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, ArrowLeft } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';

const ACCENT = 'rgb(245, 158, 11)';

export default function EsqueciSenha() {
  const [email, setEmail] = useState('');
  const [enviado, setEnviado] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setEnviado(true);
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-10 w-full max-w-md mx-4"
      >
        <div className="rounded-2xl border border-white/10 bg-black/40 backdrop-blur-xl p-8 sm:p-10 shadow-2xl">
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="text-center mb-8"
          >
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-6" style={{ backgroundColor: 'rgba(245,158,11,0.2)' }}>
              <Mail className="w-8 h-8 text-amber-400" />
            </div>
            <span className="font-jp text-2xl font-bold text-white block mb-2">忘れた — Recuperar Senha</span>
            <p className="text-slate-400 text-sm">
              Digite seu email para receber o código de recuperação
            </p>
          </motion.div>

          {!enviado ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-amber-400/80" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="seu@email.com"
                  className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-2 focus:ring-amber-500/20 outline-none transition-all"
                  required
                />
              </div>
              <motion.button
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-4 rounded-xl font-semibold text-white"
                style={{ backgroundColor: ACCENT }}
              >
                Enviar código
              </motion.button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-4"
            >
              <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl text-emerald-400">✓</span>
              </div>
              <p className="text-emerald-400 font-medium mb-2">Email enviado!</p>
              <p className="text-slate-400 text-sm mb-6">
                Verifique sua caixa de entrada. O código expira em 15 minutos.
              </p>
            </motion.div>
          )}

          <Link
            to="/login"
            className="flex items-center justify-center gap-2 text-slate-400 hover:text-white mt-6 text-sm transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Voltar ao login
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
