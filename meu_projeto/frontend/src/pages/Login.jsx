import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock, User } from 'lucide-react';
import TypewriterText from '../components/TypewriterText';
import AnimatedBackground from '../components/AnimatedBackground';
import FloatingOrbs from '../components/FloatingOrbs';
import { fetchCsrf, apiLogin, apiRegister } from '../api';

export default function Login({ isRegister = false }) {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCsrf().catch(() => {});
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <AnimatedBackground />
      <FloatingOrbs />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="relative z-10 w-full max-w-md mx-4"
      >
        <div className="glass rounded-3xl p-8 sm:p-10 shadow-2xl border border-white/10">
          {/* Logo e título com efeito de digitação */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-8"
          >
            <motion.div
              className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 mb-6 shadow-lg shadow-blue-500/30"
              whileHover={{ scale: 1.05, rotate: 5 }}
              transition={{ type: 'spring', stiffness: 400 }}
            >
              <span className="text-3xl">🥋</span>
            </motion.div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2 font-[family-name:var(--font-syne)] tracking-tight">
              <TypewriterText
                text={isRegister ? 'CRIAR CONTA' : 'BEM-VINDO DE VOLTA'}
                className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent"
                speed={60}
                delay={300}
              />
            </h1>
            <p className="text-slate-400 text-sm">
              {isRegister ? 'Preencha os dados para começar' : 'Entre na sua academia de judô'}
            </p>
          </motion.div>

          <form className="space-y-5" onSubmit={async (e) => {
            e.preventDefault();
            setError('');
            setIsLoading(true);
            const form = e.target;
            const email = form.email?.value?.trim();
            const senha = form.senha?.value;
            if (!email || !senha) { setError('Preencha email e senha'); setIsLoading(false); return; }
            try {
              if (isRegister) {
                const nome = form.nome?.value; const idade = form.idade?.value; const faixa = form.faixa?.value;
                if (!nome || !idade || !faixa) { setError('Preencha todos os campos'); setIsLoading(false); return; }
                const r = await apiRegister({ nome, idade, faixa, email, senha });
                navigate(r.redirect || '/index');
              } else {
                const r = await apiLogin(email, senha);
                navigate(r.redirect || '/index');
              }
            } catch (err) {
              setError(err.message || 'Erro');
            }
            setIsLoading(false);
          }}>
            {isRegister && (
              <>
                <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-400" />
                  <input name="nome" type="text" placeholder="Nome completo" className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all" required />
                </motion.div>
                <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.35 }} className="relative">
                  <input name="idade" type="number" placeholder="Idade" min={3} max={120} className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all" required />
                </motion.div>
                <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }} className="relative">
                  <select name="faixa" className="w-full pl-4 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all [&>option]:bg-slate-900">
                    <option value="">Selecione sua faixa</option>
                    <option value="branca">Branca</option>
                    <option value="cinza">Cinza</option>
                    <option value="azul">Azul</option>
                    <option value="amarela">Amarela</option>
                    <option value="laranja">Laranja</option>
                    <option value="verde">Verde</option>
                    <option value="roxa">Roxa</option>
                    <option value="marrom">Marrom</option>
                    <option value="preta">Preta</option>
                  </select>
                </motion.div>
              </>
            )}

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: isRegister ? 0.4 : 0.3 }}
              className="relative"
            >
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-400" />
              <input
                name="email"
                type="email"
                placeholder="seu@email.com"
                className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all duration-300"
                required
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: isRegister ? 0.5 : 0.4 }}
              className="relative"
            >
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-400" />
                <input name="senha"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                className="w-full pl-12 pr-12 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all duration-300"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </motion.div>

            {!isRegister && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="flex items-center justify-between text-sm"
              >
                <label className="flex items-center gap-2 text-slate-400 cursor-pointer hover:text-white transition-colors">
                  <input type="checkbox" className="rounded border-white/20 bg-white/5 text-blue-500 focus:ring-blue-500" />
                  Lembrar de mim
                </label>
                <Link to="/esqueci-senha" className="text-blue-400 hover:text-blue-300 transition-colors font-medium">
                  Esqueceu a senha?
                </Link>
              </motion.div>
            )}

            {error && (
              <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/40 text-red-200 text-sm text-center">
                {error}
              </div>
            )}

            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold shadow-lg shadow-blue-500/30 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70"
              disabled={isLoading}
            >
              {isLoading ? (
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                />
              ) : (
                isRegister ? 'CRIAR CONTA' : 'ENTRAR'
              )}
            </motion.button>
          </form>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="mt-6 text-center text-slate-400 text-sm"
          >
            {isRegister ? (
              <>Já tem conta?{' '}
                <Link to="/login" className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                  Faça login
                </Link>
              </>
            ) : (
              <>Não tem conta?{' '}
                <Link to="/register" className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                  Crie grátis
                </Link>
              </>
            )}
          </motion.p>
        </div>
      </motion.div>

      {/* Logo lateral desktop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="hidden lg:block fixed left-12 top-1/2 -translate-y-1/2 z-0"
      >
        <div className="text-center">
          <motion.h1
            className="text-6xl xl:text-8xl font-bold text-white/10 font-[family-name:var(--font-syne)]"
            animate={{ y: [0, -5, 0] }}
            transition={{ duration: 4, repeat: Infinity }}
          >
            DOJO
          </motion.h1>
          <motion.h1
            className="text-6xl xl:text-8xl font-bold text-blue-500/20 font-[family-name:var(--font-syne)]"
            animate={{ y: [0, 5, 0] }}
            transition={{ duration: 4, repeat: Infinity, delay: 0.5 }}
          >
            ONLINE
          </motion.h1>
        </div>
      </motion.div>
    </div>
  );
}
