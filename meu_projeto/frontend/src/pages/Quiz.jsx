import { useState } from 'react';
import ContentPage from './ContentPage';
import { motion } from 'framer-motion';

export default function Quiz() {
  const [selected, setSelected] = useState(null);
  const perguntas = [
    { pergunta: 'O que significa "judô"?', opcoes: ['Caminho suave', 'Arte marcial', 'Luta corpo a corpo'], certa: 0 },
    { pergunta: 'Quem fundou o judô?', opcoes: ['Miyamoto Musashi', 'Jigoro Kano', 'Morihei Ueshiba'], certa: 1 },
  ];

  return (
    <ContentPage title="Quiz de Judô" description="Teste seus conhecimentos sobre judô.">
      <div className="space-y-6">
        {perguntas.map((q, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-4 rounded-xl bg-white/5 border border-white/10"
          >
            <p className="font-semibold text-white mb-3">{q.pergunta}</p>
            <div className="space-y-2">
              {q.opcoes.map((op, j) => (
                <motion.button
                  key={j}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSelected(j)}
                  className={`w-full p-3 rounded-lg text-left transition-colors ${
                    selected === j ? 'bg-blue-600/30 border-blue-500' : 'bg-white/5 border-transparent hover:bg-white/10'
                  } border`}
                >
                  {op}
                </motion.button>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </ContentPage>
  );
}
