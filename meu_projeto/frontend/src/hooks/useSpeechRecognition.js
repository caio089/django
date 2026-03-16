import { useCallback, useEffect, useRef, useState } from 'react';

export function useSpeechRecognition({ lang = 'pt-BR', onResult, onEnd } = {}) {
  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);
  const startingRef = useRef(false);
  const accumulatedRef = useRef('');
  const deliveredRef = useRef(false);
  const onResultRef = useRef(onResult);
  const onEndRef = useRef(onEnd);

  onResultRef.current = onResult;
  onEndRef.current = onEnd;

  useEffect(() => {
    let recog = null;
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          recog = new SpeechRecognition();
          recog.lang = lang || 'pt-BR';
          recog.interimResults = true;
          recog.maxAlternatives = 3;
          recog.continuous = true;

          const deliverResult = (finalText) => {
            if (deliveredRef.current) return;
            deliveredRef.current = true;
            setTranscript(finalText);
            if (onResultRef.current) onResultRef.current(finalText);
            if (onEndRef.current) onEndRef.current(finalText);
          };

          recog.onstart = () => {
            startingRef.current = false;
            deliveredRef.current = false;
            accumulatedRef.current = '';
            setListening(true);
            setError(null);
            setTranscript('');
          };

          recog.onend = () => {
            setListening(false);
            const finalText = accumulatedRef.current.trim();
            deliverResult(finalText);
          };

          recog.onerror = (e) => {
            setListening(false);
            setError(e.error || 'speech-error');
            const finalText = accumulatedRef.current.trim();
            deliverResult(finalText);
          };

          recog.onresult = (e) => {
            let full = '';
            for (let i = 0; i < e.results.length; i++) {
              const r = e.results[i];
              const t = r[0]?.transcript || '';
              full += t;
              if (r.isFinal) full += ' ';
            }
            const newAccumulated = full.trim();
            accumulatedRef.current = newAccumulated;
            setTranscript(newAccumulated);
          };

          recognitionRef.current = recog;
          setSupported(true);
        } catch {
          setSupported(false);
        }
      } else {
        setSupported(false);
      }
    } else {
      setSupported(false);
    }

    return () => {
      if (recog) {
        recog.onresult = null;
        recog.onend = null;
        recog.onerror = null;
        recog.onstart = null;
        try {
          recog.abort();
        } catch {
          /* ignore */
        }
        if (recognitionRef.current === recog) recognitionRef.current = null;
      }
    };
  }, [lang]);

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

