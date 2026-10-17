import type { Register } from '../types';

interface Props {
  registers: Register[];
  activeNames?:  string[];  // amber pulse
  animateNames?: string[];  // dataReceive one-shot
  stepKey:       number;
}

export default function Registers({ registers, activeNames = [], animateNames = [], stepKey }: Props) {
  return (
    <div className="grid grid-cols-4" style={{ gap: '1.4vw' }}>
      {registers.map((reg) => {
        const active  = activeNames.includes(reg.name);
        const animate = animateNames.includes(reg.name);

        let style: React.CSSProperties = {
          fontSize: '1.7vw',
          padding: '0.3vh 0',
          backgroundColor: '#4fb3bf',
          border: '3px solid #000',
          transition: 'background-color 0.3s, border-color 0.3s',
        };

        if (animate) {
          style = { ...style, animation: 'dataReceive 0.75s ease-out forwards' };
        } else if (active) {
          style = {
            ...style,
            backgroundColor: '#fffbeb',
            border: '3px solid #f59e0b',
            animation: 'activePulse 1.2s ease-in-out infinite',
          };
        }

        return (
          <div key={reg.name} className="text-center">
            <span className="block font-black" style={{ fontSize: '0.9vw', marginBottom: '0.2vh' }}>
              {reg.name}
            </span>
            <div
              id={`reg-${reg.name}`}
              key={animate ? `${reg.name}-anim-${stepKey}` : reg.name}
              className="font-mono text-center shadow-inner"
              style={style}
            >
              {reg.value}
            </div>
          </div>
        );
      })}
    </div>
  );
}
