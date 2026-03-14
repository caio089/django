import { motion } from 'framer-motion';

/**
 * Logo Dojo Online — usa o favicon com efeitos premium
 * @param size 'sm' | 'md' | 'lg' | 'xl' | number (px)
 * @param glow — brilho animado
 * @param tint — cor para filtro (opcional)
 */
export default function DojoLogo({ size = 'md', glow = false, tint, className = '' }) {
  const sizes = { sm: 32, md: 48, lg: 64, xl: 96 };
  const w = typeof size === 'number' ? size : sizes[size] || 48;

  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${className}`}
      initial={glow ? { scale: 0.95, opacity: 0.9 } : {}}
      animate={
        glow
          ? {
              scale: [1, 1.05, 1],
              opacity: [0.95, 1, 0.95],
            }
          : {}
      }
      transition={glow ? { duration: 3, repeat: Infinity, ease: 'easeInOut' } : {}}
    >
      {glow && (
        <motion.div
          className="absolute inset-0 rounded-full blur-xl opacity-50"
          style={{
            width: w * 1.8,
            height: w * 1.8,
            background: tint
              ? `radial-gradient(circle, ${tint.replace('rgb', 'rgba').replace(')', ', 0.5)')} 0%, transparent 70%`
              : 'radial-gradient(circle, rgba(124, 58, 237, 0.5) 0%, transparent 70%)',
            margin: `-${w * 0.4}px`,
          }}
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 2.5, repeat: Infinity }}
        />
      )}
      <img
        src="/favicon.svg"
        alt="Dojo Online"
        width={w}
        height={w}
        className="relative z-10 drop-shadow-lg"
        style={{
          filter: tint
            ? `drop-shadow(0 0 12px ${tint.replace('rgb', 'rgba').replace(')', ', 0.5)')})`
            : undefined,
        }}
      />
    </motion.div>
  );
}
