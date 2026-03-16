import { useCallback, useEffect, useRef, useState } from 'react';

export function useSpeechRecognition({ lang = 'pt-BR', onResult } = {}) {
  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);
  const startingRef = useRef(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    const recog = new SpeechRecognition();
    recog.lang = lang || 'pt-BR';
    recog.interimResults = false;
    recog.maxAlternatives = 1;
    recog.continuous = false;

    recog.onstart = () => {
      startingRef.current = false;
      setListening(true);
      setError(null);
      setTranscript('');
    };
    recog.onend = () => {
      setListening(false);
    };
    recog.onerror = (e) => {
      setListening(false);
      setError(e.error || 'speech-error');
    };
    recog.onresult = (e) => {
      const text = Array.from(e.results)
        .map((r) => r[0]?.transcript || '')
        .join(' ')
        .trim();
      setTranscript(text);
      if (onResult && text) onResult(text);
    };

    recognitionRef.current = recog;
    setSupported(true);

    return () => {
      recog.onresult = null;
      recog.onend = null;
      recog.onerror = null;
      recog.onstart = null;
      try {
        recog.abort();
      } catch {
        // ignore
      }
    };
  }, [lang, onResult]);

  const startListening = useCallback(() => {
    const recog = recognitionRef.current;
    if (!recog) return;
    if (startingRef.current || listening) return;
    try {
      startingRef.current = true;
      setListening(true);
      setError(null);
      recog.lang = lang || 'pt-BR';
      recog.start();
    } catch (e) {
      // start pode lançar se já estiver rodando
      startingRef.current = false;
    }
  }, [lang, listening]);

  const stopListening = useCallback(() => {
    const recog = recognitionRef.current;
    if (!recog) return;
    try {
      recog.stop();
    } catch {
      // ignore
    }
  }, []);

  const reset = useCallback(() => {
    setTranscript('');
    setError(null);
  }, []);

  return {
    supported,
    listening,
    transcript,
    error,
    startListening,
    stopListening,
    reset,
  };
}

