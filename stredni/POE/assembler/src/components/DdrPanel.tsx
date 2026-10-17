interface Props {
  id:     string;   // DOM id for connection routing
  name:   string;   // e.g. 'DDRF' or 'DDRK'
  value:  number;   // 0–255
  active?: boolean;
  stepKey?: number;
}

function toHex(n: number): string {
  return `0x${n.toString(16).padStart(2, '0').toUpperCase()}`;
}

export default function DdrPanel({ id, name, value, active, stepKey }: Props) {
  return (
    <div
      id={id}
      className="rounded-[0.5vw] shadow-xl"
      style={{
        backgroundColor: '#c48e8e',
        border: active ? '2px solid #3b82f6' : '2px solid #8d6e63',
        padding: '0.2vw',
        transition: 'border-color 0.3s',
        alignSelf: 'flex-start',
      }}
    >
      <div
        className="rounded-[0.3vw] overflow-hidden"
        style={{ backgroundColor: '#1e293b', border: '2px solid #000' }}
      >
        {/* Title row */}
        <div
          className="flex items-center justify-between text-white font-black uppercase"
          style={{
            fontSize: '0.8vw',
            padding: '0.2vh 0.6vw',
            backgroundColor: 'rgba(0,0,0,0.6)',
          }}
        >
          <span>{name}</span>
          <span
            key={active ? `${id}-hex-${stepKey}` : `${id}-hex`}
            className="font-mono"
            style={{
              color: '#93c5fd',
              animation: active ? 'dataReceive 0.75s ease-out forwards' : undefined,
            }}
          >
            {toHex(value)}
          </span>
        </div>

        {/* Direction bit indicators */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '0.55vw',
            padding: '0.35vh 0.6vw 0.3vh',
          }}
        >
          {[7, 6, 5, 4, 3, 2, 1, 0].map((bit) => {
            const isOutput = Boolean((value >> bit) & 1);
            return (
              <div key={bit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.1vh' }}>
                <div
                  style={{
                    width: '1.2vw',
                    height: '1.2vw',
                    borderRadius: '0.2vw',
                    backgroundColor: isOutput ? '#3b82f6' : '#374151',
                    border: isOutput ? '1px solid #2563eb' : '1px solid #64748b',
                    boxShadow: isOutput ? '0 0 4px 1px rgba(59,130,246,0.6)' : 'none',
                    transition: 'background-color 0.3s, box-shadow 0.3s',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <span style={{ fontSize: '0.5vw', color: '#fff', fontFamily: 'monospace', fontWeight: 700 }}>
                    {isOutput ? 'O' : 'I'}
                  </span>
                </div>
                <span style={{ fontSize: '0.55vw', color: '#94a3b8', fontFamily: 'monospace' }}>
                  {bit}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
