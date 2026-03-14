/**
 * Background leve do Dashboard — sem efeitos pesados
 */
export default function DashboardBackground({ accentColor = 'rgb(251, 191, 36)' }) {
  const accentRgba = accentColor.replace('rgb', 'rgba').replace(')', ', 0.25)');

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <div className="absolute inset-0 bg-[#08090c]" />
      <div
        className="absolute inset-0 opacity-50"
        style={{
          background: `
            radial-gradient(ellipse 80% 60% at 30% 10%, ${accentRgba} 0%, transparent 50%),
            radial-gradient(ellipse 60% 50% at 70% 90%, ${accentColor.replace('rgb', 'rgba').replace(')', ', 0.15)')} 0%, transparent 50%)
          `,
        }}
      />
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
    </div>
  );
}
