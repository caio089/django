import ContentPage from './ContentPage';
import { motion } from 'framer-motion';

const UKEMIS = [
  { nome: 'Mae Ukemi', desc: 'Queda para frente' },
  { nome: 'Ushiro Ukemi', desc: 'Queda para trás' },
  { nome: 'Yoko Ukemi', desc: 'Queda lateral' },
  { nome: 'Zempo Kaiten', desc: 'Rolamento para frente' },
];

export default function Ukemis() {
  return (
    <ContentPage title="Rolamentos do Judô" description="Conheça todos os ukemis e técnicas de queda.">
      <div className="grid gap-4">
        {UKEMIS.map((u, i) => (
          <motion.div
            key={u.nome}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors"
          >
            <h3 className="font-semibold text-white">{u.nome}</h3>
            <p className="text-slate-400 text-sm">{u.desc}</p>
          </motion.div>
        ))}
      </div>
    </ContentPage>
  );
}
