import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import DojoBackground from '../components/DojoBackground';

const ACCENT = 'rgb(5, 150, 105)';

// Cole aqui o ID do seu vídeo do YouTube (ex: se o link for youtube.com/watch?v=ABC123, use 'ABC123')
const VIDEO_ID = 'COLOQUE_SEU_VIDEO_ID';

const VIDEO_SRC = `https://www.youtube.com/embed/${VIDEO_ID}?rel=0`;

export default function AmarrarFaixa() {
  return (
    <div className="min-h-screen relative font-display antialiased">
      <DojoBackground accentColor={ACCENT} />

      <header className="fixed top-0 left-0 right-0 z-40">
        <div
          className="bg-black/50 backdrop-blur-xl border-b border-white/10"
          style={{ borderBottomColor: 'rgba(5,150,105,0.15)' }}
        >
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link
              to="/index"
              className="flex items-center gap-2 text-slate-400 hover:text-white px-3 py-2 rounded-xl hover:bg-white/5 transition-all"
            >
              <ArrowLeft className="w-4 h-4" /> Voltar
            </Link>
            <span className="font-jp text-slate-500 text-sm tracking-wider">帯結び — Como amarrar a faixa</span>
          </div>
        </div>
      </header>

      <main className="relative z-10 pt-20 pb-12 px-4 sm:px-6 max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-6"
        >
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">Como amarrar a faixa</h1>
            <p className="text-slate-400 text-base">Aprenda o nó correto do judogi</p>
          </div>

          <div className="relative aspect-video rounded-2xl overflow-hidden bg-black/90 ring-1 ring-white/10 border border-white/10">
            <iframe
              src={VIDEO_SRC}
              title="Como amarrar a faixa do judô"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="absolute inset-0 w-full h-full"
            />
          </div>
        </motion.div>
      </main>
    </div>
  );
}
