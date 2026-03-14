import { Component } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
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

class QuizErrorBoundary extends Component {
  state = { hasError: false };
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  componentDidCatch(err, info) {
    console.error('Quiz error:', err, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#0a0c0f] flex flex-col items-center justify-center px-4 text-white">
          <h1 className="text-xl font-bold mb-2">Erro ao carregar o Quiz</h1>
          <p className="text-slate-400 text-sm mb-6">Tente recarregar a página ou voltar ao início.</p>
          <Link to="/index" className="px-6 py-3 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-400 font-medium hover:bg-amber-500/30">
            Voltar ao início
          </Link>
        </div>
      );
    }
    return this.props.children;
  }
}

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
        <Route path="/quiz" element={<QuizErrorBoundary><Quiz /></QuizErrorBoundary>} />
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
