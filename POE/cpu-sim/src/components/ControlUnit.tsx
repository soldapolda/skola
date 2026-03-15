import type { ControlUnit as ControlUnitType } from '../types';

const FLAG_KEYS = ['I', 'T', 'H', 'S', 'V', 'N', 'Z', 'C'] as const;

interface Props {
  controlUnit: ControlUnitType;
  activeFields?: Array<'ir' | 'pc' | 'sreg'>;
  animateIr?:   boolean;
  animatePc?:   boolean;
  stepKey:      number;
}

const ACTIVE_ROW: React.CSSProperties = {
  backgroundColor: '#fef3c7',
  borderRadius: '0.3vw',
  outline: '2px solid #f59e0b',
  animation: 'activePulse 1.2s ease-in-out infinite',
};

export default function ControlUnit({ controlUnit, activeFields = [], animateIr, animatePc, stepKey }: Props) {
  const { ir, pc, flags } = controlUnit;

  const irValueStyle: React.CSSProperties = {
    fontSize: '1.6vw',
    padding: '0.4vh 0.6vw',
    width: '8vw',
    backgroundColor: '#4fb3bf',
    border: '3px solid #000',
    ...(animateIr ? { animation: 'dataReceive 0.75s ease-out forwards' } : {}),
  };

  const pcValueStyle: React.CSSProperties = {
    fontSize: '1.6vw',
    padding: '0.4vh 0.6vw',
    width: '8vw',
    backgroundColor: '#4fb3bf',
    border: '3px solid #000',
    ...(animatePc ? { animation: 'pcIncrement 0.85s ease-out forwards' } : {}),
  };

  return (
    <div
      id="cu-box"
      className="shadow-2xl rounded-lg"
      style={{ width: '32vw', padding: '0.9vw', backgroundColor: '#c48e8e', border: '4px solid #333' }}
    >
      <h3
        className="text-center font-black uppercase border-b-4 border-black/10"
        style={{ fontSize: '1.5vw', marginBottom: '1vh', paddingBottom: '0.5vh' }}
      >
        Řídicí jednotka
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8vh' }}>
        {/* RI */}
        <div
          id="ri-row"
          className="flex items-center justify-between"
          style={activeFields.includes('ir') ? ACTIVE_ROW : undefined}
        >
          <span className="font-black" style={{ fontSize: '1.1vw' }}>Registr Instrukce (RI):</span>
          <div
            key={animateIr ? `ir-anim-${stepKey}` : 'ir'}
            className="font-mono text-center"
            style={irValueStyle}
          >
            {ir}
          </div>
        </div>

        {/* PC */}
        <div
          id="pc-row"
          className="flex items-center justify-between"
          style={activeFields.includes('pc') ? ACTIVE_ROW : undefined}
        >
          <span className="font-black" style={{ fontSize: '1.1vw' }}>ČÍTAČ PROGRAMU (PC):</span>
          <div
            key={animatePc ? `pc-anim-${stepKey}` : 'pc'}
            className="font-mono text-center"
            style={pcValueStyle}
          >
            {pc}
          </div>
        </div>

        {/* SREG */}
        <div
          id="sreg-box"
          style={{ marginTop: '0.4vh', ...(activeFields.includes('sreg') ? ACTIVE_ROW : {}) }}
        >
          <div className="flex border-4 border-black bg-white">
            {FLAG_KEYS.map((key, i) => (
              <div
                key={key}
                className={`flex-1 text-center font-black ${i < FLAG_KEYS.length - 1 ? 'border-r-2 border-black' : ''} ${key === 'I' ? 'bg-blue-100' : key === 'N' ? 'bg-red-100' : ''}`}
                style={{ fontSize: '1.2vw', padding: '0.3vh 0' }}
              >
                {key}
              </div>
            ))}
          </div>
          <div className="flex border-x-4 border-b-4 border-black bg-gray-200 font-mono text-center">
            {FLAG_KEYS.map((key, i) => (
              <div
                key={key}
                className={`flex-1 ${i < FLAG_KEYS.length - 1 ? 'border-r-2 border-black' : ''}`}
                style={{ fontSize: '1.3vw', padding: '0.25vh 0' }}
              >
                {flags[key]}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
