import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Eye,
  EyeOff,
  Mail,
  Lock,
  User,
  Calendar,
  Award,
} from 'lucide-react';
import { fetchCsrf, apiLogin, apiRegister } from '../api';
import AnimatedBackground from '../components/AnimatedBackground';

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
        navigate(r.redirect || '/index');
      }
    } catch (err) {
      setError(err.message || 'Erro ao processar');
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row items-center justify-center md:justify-between md:px-12 lg:px-20 relative overflow-x-hidden overflow-y-auto font-display py-8 md:py-0">
      {/* Fundo temático */}
      <div className="fixed inset-0 z-0 bg-gradient-to-br from-judo-black via-slate-900 to-judo-blue" />
      <AnimatedBackground variant="particles" />

      {/* Padrão de faixas */}
      <div
        className="fixed inset-0 z-[5] opacity-20 pointer-events-none"
        style={{
          backgroundImage: `
            repeating-linear-gradient(45deg, rgba(30,64,175,0.15) 0 4px, transparent 4px 40px),
            repeating-linear-gradient(-45deg, rgba(245,158,11,0.1) 0 4px, transparent 4px 40px)
          `,
        }}
      />

      {/* Blur lateral esquerdo */}
      <div className="fixed inset-y-0 left-0 z-10 w-[30vw] md:w-[40vw] max-w-md bg-gradient-to-r from-white/10 to-transparent blur-3xl pointer-events-none saturate-150" />
      {/* Blur lateral direito */}
      <div className="fixed inset-y-0 right-0 z-10 w-[30vw] md:w-[40vw] max-w-md bg-gradient-to-l from-white/10 to-transparent blur-3xl pointer-events-none saturate-150" />

      {/* Brand - esquerda no desktop, topo no mobile */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        className="relative z-20 text-center mb-8 md:mb-0 md:flex-1 md:max-w-xl"
      >
        {/* Anéis decorativos rotativos */}
        <motion.div
          className="absolute -top-6 left-1/2 -translate-x-1/2 w-20 h-20 border-4 border-judo-blue/40 rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        />
        <motion.div
          className="absolute -top-4 left-1/2 -translate-x-1/2 w-16 h-16 border-[3px] border-judo-yellow/40 rounded-full"
          animate={{ rotate: -360 }}
          transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
        />
        <motion.div
          className="absolute -top-2 left-1/2 -translate-x-1/2 w-12 h-12 border-2 border-judo-white/60 rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
        />

        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-display font-light text-white leading-none tracking-wide">
          DOJO
        </h1>
        <motion.h1
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-display font-light text-judo-blue leading-none tracking-wide"
          initial={{ opacity: 0.8 }}
          animate={{
            opacity: [0.9, 1, 0.9],
            textShadow: [
              '0 0 30px rgba(30,64,175,0.3)',
              '0 0 50px rgba(30,64,175,0.5)',
              '0 0 30px rgba(30,64,175,0.3)',
            ],
          }}
          transition={{ duration: 4, repeat: Infinity }}
        >
          ONLINE
        </motion.h1>

        {/* Linha decorativa com gradiente das faixas */}
        <motion.div
          className="mt-3 h-2 mx-auto max-w-xs md:max-w-sm bg-gradient-to-r from-judo-blue via-judo-yellow to-judo-green rounded-full shadow-lg"
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.5, repeat: Infinity }}
        />

        <div className="mt-6 text-center">
          <p className="text-white/80 text-lg md:text-xl font-light tracking-wide">
            ACADEMIA DE JUDÔ
          </p>
          <div className="flex justify-center mt-3 gap-4">
            {['judo-blue', 'judo-yellow', 'judo-green'].map((color, i) => (
              <motion.div
                key={color}
                className={`w-3 h-3 rounded-full bg-${color} shadow-lg`}
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.7, 1, 0.7],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.3,
                }}
                style={{
                  backgroundColor:
                    color === 'judo-blue'
                      ? '#1E40AF'
                      : color === 'judo-yellow'
                        ? '#F59E0B'
                        : '#059669',
                }}
              />
            ))}
          </div>
        </div>

        {/* Elementos flutuantes */}
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="absolute rounded-full"
            style={{
              top: `${20 + i * 15}px`,
              left: '50%',
              transform: 'translateX(-50%)',
              width: 12 + i * 2,
              height: 12 + i * 2,
              backgroundColor:
                i === 0
                  ? 'rgba(30,64,175,0.6)'
                  : i === 1
                    ? 'rgba(245,158,11,0.6)'
                    : 'rgba(5,150,105,0.6)',
            }}
            animate={{ y: [0, -12, 0] }}
            transition={{
              duration: 4 + i,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: i * 0.5,
            }}
          />
        ))}
      </motion.div>

      {/* Card de Login/Registro */}
      <motion.div
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.7, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
        className="relative z-30 w-full max-w-md mx-4 md:mx-0 md:flex-shrink-0"
      >
        <div className="bg-white/95 backdrop-blur-xl rounded-2xl sm:rounded-3xl shadow-2xl px-6 sm:px-8 py-6 sm:py-8 border-2 border-judo-blue/20 overflow-hidden">
          {/* Decoração interna */}
          <div className="absolute inset-0 bg-gradient-to-br from-judo-blue/5 via-transparent to-judo-yellow/5 pointer-events-none" />
          <div className="absolute top-0 right-0 w-20 h-20 bg-judo-blue/10 rounded-full -translate-y-10 translate-x-10" />
          <div className="absolute bottom-0 left-0 w-16 h-16 bg-judo-yellow/10 rounded-full translate-y-8 -translate-x-8" />

          <div className="relative z-10">
            {/* Título */}
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">🥋</span>
              <span className="font-display font-bold text-xl text-judo-black tracking-widest">
                DOJO ONLINE
              </span>
            </div>

            <motion.h2
              key={showRegister ? 'register' : 'login'}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-xl sm:text-2xl font-display font-light mb-6 text-judo-black text-center tracking-wide"
            >
              {showRegister ? 'CRIAR NOVA CONTA' : 'ACESSAR SUA CONTA'}
            </motion.h2>

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
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-judo-blue" />
                      <input
                        name="nome"
                        type="text"
                        placeholder=" "
                        required
                        className="peer w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-judo-blue focus:ring-4 focus:ring-judo-blue/20 outline-none bg-white/95 text-judo-black placeholder-transparent text-sm transition-all shadow-lg hover:shadow-xl"
                      />
                      <label className="absolute left-12 top-1/2 -translate-y-1/2 text-gray-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-judo-blue peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90 peer-[:not(:placeholder-shown)]:text-judo-blue">
                        NOME DO ALUNO
                      </label>
                    </motion.div>

                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0 }}
                      className="relative"
                    >
                      <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-judo-blue" />
                      <input
                        name="idade"
                        type="number"
                        placeholder=" "
                        min={3}
                        max={120}
                        required
                        className="peer w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-judo-blue focus:ring-4 focus:ring-judo-blue/20 outline-none bg-white/95 text-judo-black placeholder-transparent text-sm transition-all shadow-lg hover:shadow-xl"
                      />
                      <label className="absolute left-12 top-1/2 -translate-y-1/2 text-gray-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-judo-blue peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                        IDADE DO ALUNO
                      </label>
                    </motion.div>

                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="relative"
                    >
                      <Award className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-judo-blue z-10" />
                      <select
                        name="faixa"
                        required
                        className="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-judo-blue focus:ring-4 focus:ring-judo-blue/20 outline-none bg-white/95 text-judo-black text-sm transition-all shadow-lg hover:shadow-xl appearance-none"
                      >
                        <option value="">Selecione sua faixa</option>
                        {FAIXAS.map((f) => (
                          <option key={f.value} value={f.value}>
                            {f.label}
                          </option>
                        ))}
                      </select>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>

              {/* Email */}
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-judo-blue" />
                <input
                  name="email"
                  type="email"
                  placeholder=" "
                  required
                  className="peer w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-judo-blue focus:ring-4 focus:ring-judo-blue/20 outline-none bg-white/95 text-judo-black placeholder-transparent text-sm transition-all shadow-lg hover:shadow-xl"
                />
                <label className="absolute left-12 top-1/2 -translate-y-1/2 text-gray-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-judo-blue peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                  EMAIL
                </label>
              </div>

              {/* Senha */}
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-judo-blue" />
                <input
                  name="senha"
                  type={showPassword ? 'text' : 'password'}
                  placeholder=" "
                  required
                  className="peer w-full pl-12 pr-12 py-3 rounded-xl border-2 border-gray-200 focus:border-judo-blue focus:ring-4 focus:ring-judo-blue/20 outline-none bg-white/95 text-judo-black placeholder-transparent text-sm transition-all shadow-lg hover:shadow-xl"
                />
                <label className="absolute left-12 top-1/2 -translate-y-1/2 text-gray-500 bg-white px-2 text-xs font-medium transition-all pointer-events-none peer-focus:top-0 peer-focus:-translate-y-1/2 peer-focus:scale-90 peer-focus:text-judo-blue peer-[:not(:placeholder-shown)]:top-0 peer-[:not(:placeholder-shown)]:-translate-y-1/2 peer-[:not(:placeholder-shown)]:scale-90">
                  SENHA
                </label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-judo-blue transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              {!showRegister && (
                <div className="flex items-center justify-between text-sm text-gray-600">
                  <label className="flex items-center gap-2 cursor-pointer hover:text-judo-blue transition-colors">
                    <input
                      type="checkbox"
                      className="accent-judo-blue rounded"
                    />
                    <span>Lembrar de mim</span>
                  </label>
                  <Link
                    to="/esqueci-senha"
                    className="hover:text-judo-blue font-medium transition-colors"
                  >
                    Esqueceu a senha?
                  </Link>
                </div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-3 rounded-lg bg-red-100 text-red-800 border border-red-200 text-sm"
                >
                  {error}
                </motion.div>
              )}

              <motion.button
                type="submit"
                disabled={isLoading}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                className="relative mt-2 w-full py-4 rounded-xl bg-gradient-to-r from-judo-blue to-blue-600 hover:from-blue-700 hover:to-blue-700 text-white font-display font-medium text-base shadow-xl overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
                <span className="relative z-10 flex items-center justify-center gap-2">
                  {isLoading ? (
                    <motion.span
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                    />
                  ) : (
                    showRegister ? 'CRIAR CONTA' : 'ENTRAR'
                  )}
                </span>
              </motion.button>
            </form>

            {/* Toggle login/registro */}
            <p className="mt-4 text-center text-sm text-gray-600">
              {showRegister ? (
                <>
                  Já tem conta?{' '}
                  <Link
                    to="/login"
                    className="text-judo-blue hover:text-blue-700 font-bold transition-colors"
                  >
                    FAÇA LOGIN
                  </Link>
                </>
              ) : (
                <>
                  Não possui conta?{' '}
                  <Link
                    to="/register"
                    className="text-judo-blue hover:text-blue-700 font-bold transition-colors"
                  >
                    CRIE UMA CONTA GRÁTIS
                  </Link>
                </>
              )}
            </p>

            {/* Footer */}
            <p className="mt-6 text-center text-xs text-gray-500 font-display tracking-wide">
              © 2025 Academia de Judô — Desenvolvido por Caio Campos
            </p>
          </div>
        </div>
      </motion.div>

    </div>
  );
}
