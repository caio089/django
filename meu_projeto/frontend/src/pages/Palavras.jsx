import ContentPage from './ContentPage';
import { motion } from 'framer-motion';

const PALAVRAS = [
  { japones: 'Judô', portugues: 'Caminho suave' },
  { japones: 'Sensei', portugues: 'Professor' },
  { japones: 'Dojo', portugues: 'Local de treino' },
  { japones: 'Tatame', portugues: 'Esteira de treino' },
  { japones: 'Randori', portugues: 'Treino livre' },
  { japones: 'Osoto-gari', portugues: 'Grande varredura externa' },
];

export default function Palavras() {
  return (
    <ContentPage title="Palavras em Japonês" description="Vocabulário essencial do judô.">
      <div className="grid gap-4">
        {PALAVRAS.map((p, i) => (
          <motion.div
            key={p.japones}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex justify-between items-center p-4 rounded-xl bg-white/5 border border-white/10"
          >
            <span className="font-semibold text-white">{p.japones}</span>
            <span className="text-slate-400">{p.portugues}</span>
          </motion.div>
        ))}
      </div>
    </ContentPage>
  );
}
