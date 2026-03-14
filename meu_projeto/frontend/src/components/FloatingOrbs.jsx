import { motion } from 'framer-motion';

export default function FloatingOrbs() {
  const orbs = [
    { size: 400, color: 'from-blue-500/20 to-transparent', delay: 0, x: '10%', y: '20%' },
    { size: 300, color: 'from-purple-500/15 to-transparent', delay: 0.5, x: '70%', y: '60%' },
    { size: 250, color: 'from-cyan-500/10 to-transparent', delay: 1, x: '85%', y: '15%' },
    { size: 200, color: 'from-amber-500/10 to-transparent', delay: 1.5, x: '5%', y: '70%' },
  ];

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
      {orbs.map((orb, i) => (
        <motion.div
          key={i}
          className={`absolute rounded-full bg-gradient-to-br ${orb.color} blur-3xl`}
          style={{
            width: orb.size,
            height: orb.size,
            left: orb.x,
            top: orb.y,
            transform: 'translate(-50%, -50%)',
          }}
          animate={{
            x: [0, 30, 0],
            y: [0, -20, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 8 + i * 2,
            repeat: Infinity,
            delay: orb.delay,
          }}
        />
      ))}
    </div>
  );
}
