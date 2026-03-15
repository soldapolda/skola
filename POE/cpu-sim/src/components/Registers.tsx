import type { Register } from '../types';

interface Props {
  registers: Register[];
}

export default function Registers({ registers }: Props) {
  return (
    <div className="grid grid-cols-4" style={{ gap: '1.2vw' }}>
      {registers.map((reg) => (
        <div key={reg.name} className="text-center">
          <span
            className="block font-black"
            style={{ fontSize: '1.2vw', marginBottom: '0.3vh' }}
          >
            {reg.name}
          </span>
          <div
            className="font-mono text-center shadow-inner"
            style={{
              fontSize: '2.2vw',
              padding: '0.6vh 0',
              backgroundColor: '#4fb3bf',
              border: '3px solid #000',
            }}
          >
            {reg.value}
          </div>
        </div>
      ))}
    </div>
  );
}
