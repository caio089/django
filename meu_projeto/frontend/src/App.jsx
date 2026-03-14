import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import EsqueciSenha from './pages/EsqueciSenha';
import Dashboard from './pages/Dashboard';
import FaixaPage from './pages/FaixaPage';
import Quiz from './pages/Quiz';
import Ukemis from './pages/Ukemis';
import Historia from './pages/Historia';
import Palavras from './pages/Palavras';
import Regras from './pages/Regras';
import Planos from './pages/Planos';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Landing />} />
        <Route path="/register" element={<Landing />} />
        <Route path="/esqueci-senha" element={<EsqueciSenha />} />
        <Route path="/index" element={<Dashboard />} />
        <Route path="/pagina/:id" element={<FaixaPage />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/ukemis" element={<Ukemis />} />
        <Route path="/historia" element={<Historia />} />
        <Route path="/palavras" element={<Palavras />} />
        <Route path="/regras" element={<Regras />} />
        <Route path="/payments/planos" element={<Planos />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
