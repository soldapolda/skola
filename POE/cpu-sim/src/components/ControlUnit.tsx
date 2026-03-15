import type { ControlUnit as ControlUnitType } from '../types';

const FLAG_KEYS = ['I', 'T', 'H', 'S', 'V', 'N', 'Z', 'C'] as const;

interface Props {
  controlUnit: ControlUnitType;
}

export default function ControlUnit({ controlUnit }: Props) {
  const { ir, pc, flags } = controlUnit;

  return (
    <div
      className="shadow-2xl rounded-lg"
      style={{
        width: '32vw',
        padding: '0.9vw',
        backgroundColor: '#c48e8e',
        border: '4px solid #333',
      }}
    >
      <h3
        className="text-center font-black uppercase border-b-4 border-black/10"
        style={{ fontSize: '1.5vw', marginBottom: '1vh', paddingBottom: '0.5vh' }}
      >
        Řídicí jednotka
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8vh' }}>
        {/* IR */}
        <div className="flex items-center justify-between">
          <span className="font-black" style={{ fontSize: '1.1vw' }}>
            INSTRUKČNÍ REGISTR:
          </span>
          <div
            className="font-mono text-center"
            style={{
              fontSize: '1.6vw',
              padding: '0.4vh 0.6vw',
              width: '8vw',
              backgroundColor: '#4fb3bf',
              border: '3px solid #000',
            }}
          >
            {ir}
          </div>
        </div>

        {/* PC */}
        <div className="flex items-center justify-between">
          <span className="font-black" style={{ fontSize: '1.1vw' }}>
            ČÍTAČ PROGRAMU (PC):
          </span>
          <div
            className="font-mono text-center"
            style={{
              fontSize: '1.6vw',
              padding: '0.4vh 0.6vw',
              width: '8vw',
              backgroundColor: '#4fb3bf',
              border: '3px solid #000',
            }}
          >
            {pc}
          </div>
        </div>

        {/* Status register */}
        <div style={{ marginTop: '0.4vh' }}>
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
