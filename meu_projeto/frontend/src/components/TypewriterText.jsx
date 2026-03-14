import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function TypewriterText({ text, className = '', speed = 80, delay = 0, cursorColor = 'rgb(251, 191, 36)' }) {
  const [displayText, setDisplayText] = useState('');
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    let timeout;
    const start = () => {
      let i = 0;
      const type = () => {
        if (i < text.length) {
          setDisplayText(text.slice(0, i + 1));
          i++;
          timeout = setTimeout(type, speed + Math.random() * 30);
        } else {
          setIsComplete(true);
        }
      };
      timeout = setTimeout(type, delay);
    };
    start();
    return () => clearTimeout(timeout);
  }, [text, speed, delay]);

  return (
    <span className={className}>
      {displayText}
      {!isComplete && (
        <motion.span
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.5, repeat: Infinity }}
          className="inline-block w-0.5 h-[1em] ml-0.5 align-middle"
          style={{ backgroundColor: cursorColor }}
        />
      )}
    </span>
  );
}
