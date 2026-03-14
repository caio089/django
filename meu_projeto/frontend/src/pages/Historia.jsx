import ContentPage from './ContentPage';
import { motion } from 'framer-motion';

export default function Historia() {
  return (
    <ContentPage title="História do Judô" description="Origens e evolução do judô no mundo.">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="prose prose-invert max-w-none"
      >
        <p className="text-slate-300 leading-relaxed">
          O Judô foi criado em 1882 por <strong className="text-white">Jigoro Kano</strong> no Japão.
          Ele fundou o Instituto Kodokan em Tóquio, criando uma arte marcial baseada no jiu-jitsu tradicional,
          mas com foco em projeções e técnicas de imobilização. O nome significa &quot;Caminho Suave&quot;.
        </p>
        <p className="text-slate-300 leading-relaxed mt-4">
          O judô se tornou esporte olímpico em 1964 nos Jogos de Tóquio e é praticado em todo o mundo.
        </p>
      </motion.div>
    </ContentPage>
  );
}
