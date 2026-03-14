import ContentPage from './ContentPage';
import { motion } from 'framer-motion';

export default function Regras() {
  return (
    <ContentPage title="Regras do Judô" description="Regulamentos oficiais do judô.">
      <motion.ul
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="space-y-3 text-slate-300"
      >
        <li>• A luta ocorre em área delimitada (tatame)</li>
        <li>• Vitória por ippon (ponto completo) ou waza-ari</li>
        <li>• Imobilização por 20 segundos = ippon</li>
        <li>• Projeção com força e controle = pontuação</li>
        <li>• Proibições: golpes em articulações, estrangulamento irregular</li>
      </motion.ul>
    </ContentPage>
  );
}
