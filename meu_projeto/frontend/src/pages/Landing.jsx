import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock, User, Calendar, Award, BookOpen, ChevronRight } from 'lucide-react';
import { fetchCsrf, apiLogin, apiRegister } from '../api';

const FAIXAS = [
  { value: 'branca', label: 'Branca' },
  { value: 'cinza', label: 'Cinza' },
  { value: 'azul', label: 'Azul' },
  { value: 'amarela', label: 'Amarela' },
  { value: 'laranja', label: 'Laranja' },
  { value: 'verde', label: 'Verde' },
  { value: 'roxa', label: 'Roxa' },
  { value: 'marrom', label: 'Marrom' },
  { value: 'preta', label: 'Preta' },
];

export default function Landing() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showRegister, setShowRegister] = useState(location.pathname === '/register');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCsrf().catch(() => {});
  }, []);

  useEffect(() => {
    setShowRegister(location.pathname === '/register');
  }, [location.pathname]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    const form = e.target;
    const email = form.email?.value?.trim();
    const senha = form.senha?.value;
    if (!email || !senha) {
      setError('Preencha email e senha');
      setIsLoading(false);
      return;
    }
    try {
      await fetchCsrf().catch(() => {});
      if (showRegister) {
        const nome = form.nome?.value;
        const idade = form.idade?.value;
        const faixa = form.faixa?.value;
        if (!nome || !idade || !faixa) {
          setError('Preencha todos os campos');
          setIsLoading(false);
          return;
        }
        const r = await apiRegister({ nome, idade, faixa, email, senha });
        navigate(r.redirect === '/selecionar-faixa' ? '/index' : r.redirect || '/index');
      } else {
        const r = await apiLogin(email, senha);
        navigate(r?.redirect || '/index');
      }
    } catch (err) {
      const msg = err && typeof err === 'object' && typeof err.message === 'string' ? err.message : 'Não foi possível fazer login. Verifique o email, a senha e se o backend está rodando.';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row items-center justify-center md:justify-between gap-8 md:gap-16 px-4 md:px-12 lg:px-20 py-12 md:py-0 relative overflow-hidden font-display">
      {/* Fundo — dojo escuro, tatami, atmosfera zen */}
      <div className="fixed inset-0 -z-10 bg-[#0a0b0d]" />
      <div
        className="fixed inset-0 -z-10 opacity-[0.04]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.8) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.8) 1px, transparent 1px)
          `,
          backgroundSize: '48px 48px',
        }}
      />
      <div
        className="fixed inset-0 -z-10"
        style={{
          background: `
            radial-gradient(ellipse 120% 80% at 20% 50%, rgba(30, 64, 175, 0.12) 0%, transparent 55%),
            radial-gradient(ellipse 80% 60% at 80% 80%, rgba(124, 58, 237, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 60% 40% at 50% 10%, rgba(245, 158, 11, 0.05) 0%, transparent 45%)
          `,
        }}
      />

      {/* Lado esquerdo — identidade judô */}
      <motion.div
        initial={{ opacity: 0, x: -24 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        className="relative z-10 flex flex-col items-center md:items-start text-center md:text-left md:flex-1 md:max-w-xl"
      >
        <span className="font-jp text-amber-500/80 text-sm tracking-[0.3em] uppercase mb-4">
          道場オンライン
        </span>
        <p className="font-display text-white/90 text-2xl sm:text-3xl font-light tracking-[0.25em] mb-6">
          DOJO ONLINE
        </p>
        <h1
          className="font-jp text-7xl sm:text-8xl md:text-9xl font-bold text-white/95 leading-none tracking-tight select-none"
          style={{
            textShadow: '0 0 80px rgba(30, 64, 175, 0.15), 0 0 40px rgba(245, 158, 11, 0.08)',
          }}
        >
          柔道
        </h1>
        <p className="font-display text-slate-400 text-lg sm:text-xl mt-4 tracking-widest">
          JUDÔ
        </p>
        <div
          className="h-px w-24 mt-8 mb-8"
          style={{ background: 'linear-gradient(90deg, transparent, rgba(245,158,11,0.6), transparent)' }}
        />
        <p className="font-jp text-slate-400/90 text-xl sm:text-2xl leading-relaxed max-w-sm">
          「精力善用、自他共栄」
        </p>
        <p className="text-slate-500 text-sm mt-2 max-w-sm">
          Máxima eficiência, prosperidade mútua — O caminho do judô.
        </p>
      </motion.div>

      {/* Coluna direita: Quiz + Login */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
        className="relative z-20 w-full max-w-md flex flex-col gap-6"
      >
        {/* Card do Quiz */}
        <Link
          to="/quiz"
          className="group relative flex items-center gap-5 p-6 rounded-2xl overflow-hidden border border-white/10 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/40 active:scale-[0.99]"
          style={{
            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(30, 64, 175, 0.12) 50%, rgba(124, 58, 237, 0.1) 100%)',
            boxShadow: '0 8px 32px -8px rgba(245, 158, 11, 0.2)',
          }}
        >
          <div
            className="flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center"
            style={{ backgroundColor: 'rgba(245, 158, 11, 0.25)', border: '1px solid rgba(245, 158, 11, 0.4)' }}
          >
            <BookOpen className="w-7 h-7 text-amber-400" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-display font-semibold text-white text-lg tracking-wide">Quiz de Judô</h3>
            <p className="text-slate-400 text-sm mt-0.5">Teste seus conhecimentos sobre teoria do judô</p>
          </div>
          <ChevronRight className="w-6 h-6 text-amber-500/80 group-hover:translate-x-1 transition-transform flex-shrink-0" />
        </Link>

        {/* Card de Login/Registro — papel washi + moldura */}
        <div
          className="relative rounded-2xl overflow-hidden"
          style={{
            background: 'linear-gradient(145deg, rgba(255,255,255,0.97) 0%, rgba(248,250,252,0.95) 100%)',
            boxShadow: `
              0 25px 50px -12px rgba(0,0,0,0.4),
              0 0 0 1px rgba(255,255,255,0.5),
              inset 0 1px 0 rgba(255,255,255,0.8)
            `,
          }}
        >
          {/* Moldura estilo shodo — borda sutil */}
          <div
            className="absolute inset-0 rounded-2xl pointer-events-none border-2"
            style={{ borderColor: 'rgba(30, 64, 175, 0.25)' }}
          />
          <div
            className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-px"
            style={{ background: 'linear-gradient(90deg, transparent, rgba(30,64,175,0.5), transparent)' }}
          />

          <div className="relative px-6 sm:px-8 py-8 sm:py-10">
            <div className="text-center mb-8">
              <span className="font-jp text-lg text-slate-500 block">道場オンライン</span>
              <span className="font-display text-slate-800 text-xl font-semibold tracking-[0.2em] mt-1">DOJO ONLINE</span>
            </div>

            <AnimatePresence mode="wait">
              <motion.h2
                key={showRegister ? 'register' : 'login'}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="text-lg font-display font-medium text-slate-700 text-center mb-6 tracking-wide"
              >
                {showRegister ? 'CRIAR CONTA' : 'ENTRAR'}
              </motion.h2>
            </AnimatePresence>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <AnimatePresence mode="wait">
                {showRegister && (
                  <>
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="relative"
                    >
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                      <input
                        name="nome"
                        type="text"
                        placeholder=" "
                        required
                        className="peer w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 focus:border-amber-600/60 focus:ring-2 focus:ring-amber-500/20 outline-none bg-white/80 text-slate-800 transition-all"
                      />
                      <label className="absolute left-12 top-1/2 -translate-y-1/2 text-slate-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-amber-700 peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90 peer-[:not(:placeholder-shown)]:text-slate-700">
                        NOME DO ALUNO
                      </label>
                    </motion.div>
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0 }}
                      className="relative"
                    >
                      <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                      <input
                        name="idade"
                        type="number"
                        placeholder=" "
                        min={3}
                        max={120}
                        required
                        className="peer w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 focus:border-amber-600/60 focus:ring-2 focus:ring-amber-500/20 outline-none bg-white/80 text-slate-800 transition-all"
                      />
                      <label className="absolute left-12 top-1/2 -translate-y-1/2 text-slate-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-amber-700 peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                        IDADE DO ALUNO
                      </label>
                    </motion.div>
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="relative">
                      <Award className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 z-10" />
                      <select
                        name="faixa"
                        required
                        className="w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 focus:border-amber-600/60 focus:ring-2 focus:ring-amber-500/20 outline-none bg-white/80 text-slate-800 transition-all appearance-none"
                      >
                        <option value="">Selecione sua faixa</option>
                        {FAIXAS.map((f) => (
                          <option key={f.value} value={f.value}>{f.label}</option>
                        ))}
                      </select>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>

              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input
                  name="email"
                  type="email"
                  placeholder=" "
                  required
                  className="peer w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 focus:border-amber-600/60 focus:ring-2 focus:ring-amber-500/20 outline-none bg-white/80 text-slate-800 transition-all"
                />
                <label className="absolute left-12 top-1/2 -translate-y-1/2 text-slate-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-amber-700 peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                  EMAIL
                </label>
              </div>

              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input
                  name="senha"
                  type={showPassword ? 'text' : 'password'}
                  placeholder=" "
                  required
                  className="peer w-full pl-12 pr-12 py-3.5 rounded-xl border border-slate-200 focus:border-amber-600/60 focus:ring-2 focus:ring-amber-500/20 outline-none bg-white/80 text-slate-800 transition-all"
                />
                <label className="absolute left-12 top-1/2 -translate-y-1/2 text-slate-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-amber-700 peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                  SENHA
                </label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-amber-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              {!showRegister && (
                <div className="flex items-center justify-between text-sm text-slate-600">
                  <label className="flex items-center gap-2 cursor-pointer hover:text-amber-600 transition-colors">
                    <input type="checkbox" className="accent-amber-600 rounded" />
                    <span>Lembrar de mim</span>
                  </label>
                  <Link to="/esqueci-senha" className="hover:text-amber-600 font-medium transition-colors">
                    Esqueceu a senha?
                  </Link>
                </div>
              )}

              {error && (
                <div className="p-3 rounded-xl bg-red-50 text-red-700 border border-red-100 text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoading}
                className="mt-2 w-full py-4 rounded-xl font-display font-semibold text-white transition-all duration-300 hover:opacity-95 active:scale-[0.99] disabled:opacity-70"
                style={{
                  background: 'linear-gradient(135deg, #1E40AF 0%, #7C3AED 100%)',
                  boxShadow: '0 4px 20px -4px rgba(30, 64, 175, 0.4)',
                }}
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Entrando...
                  </span>
                ) : (
                  showRegister ? 'CRIAR CONTA' : 'ENTRAR'
                )}
              </button>
            </form>

            <p className="mt-5 text-center text-sm text-slate-500">
              {showRegister ? (
                <>
                  Já tem conta?{' '}
                  <Link to="/login" className="text-amber-600 hover:text-amber-700 font-semibold transition-colors">
                    FAÇA LOGIN
                  </Link>
                </>
              ) : (
                <>
                  Não possui conta?{' '}
                  <Link to="/register" className="text-amber-600 hover:text-amber-700 font-semibold transition-colors">
                    CRIE UMA CONTA GRÁTIS
                  </Link>
                </>
              )}
            </p>

            <p className="mt-6 text-center text-xs text-slate-400 font-display">
              © 2025 Dojo Online — Judô & Modernidade
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
