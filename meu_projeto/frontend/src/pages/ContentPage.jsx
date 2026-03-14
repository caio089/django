import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import AnimatedBackground from '../components/AnimatedBackground';

export default function ContentPage({ title, description, children }) {
  return (
    <div className="min-h-screen relative">
      <AnimatedBackground />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="relative z-10 p-6 max-w-4xl mx-auto"
      >
        <Link to="/index" className="inline-flex items-center gap-2 text-slate-400 hover:text-white mb-8 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Voltar
        </Link>

        <motion.article
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="glass rounded-3xl p-8 sm:p-12"
        >
          <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4">{title}</h1>
          <p className="text-slate-400 mb-8">{description}</p>
          {children}
        </motion.article>
      </motion.div>
    </div>
  );
}
