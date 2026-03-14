
/**
 * Fundo inspirado em dojo: tatami, atmosfera japonesa, essência do judô
 */
export default function DojoBackground({ accentColor = 'rgb(59, 130, 246)' }) {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      {/* Base escura – ambiente do dojo */}
      <div className="absolute inset-0 bg-[#0a0c0f]" />

      {/* Gradiente sutil com cor da faixa */}
      <div
        className="absolute inset-0 opacity-40"
        style={{
          background: `radial-gradient(ellipse 80% 50% at 50% 0%, ${accentColor}15 0%, transparent 60%),
                      radial-gradient(ellipse 60% 40% at 80% 100%, ${accentColor}08 0%, transparent 50%)`,
        }}
      />

      {/* Padrão tatami – grid sutil */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)
          `,
          backgroundSize: '48px 48px',
        }}
      />

      {/* Textura papel japonês sutil */}
      <div
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Brilho estático */}
      <div
        className="absolute inset-0 opacity-80"
        style={{
          background: `radial-gradient(circle at 30% 20%, ${accentColor}12 0%, transparent 40%)`,
        }}
      />
    </div>
  );
}
