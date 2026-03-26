interface Props {
  portF:    string;
  active?:  boolean;
  stepKey?: number;
}

export default function PortPanel({ portF, active, stepKey }: Props) {
  const value = parseInt(portF, 16) || 0;

  return (
    <div
      id="portf-panel"
      className="rounded-[0.5vw] shadow-xl"
      style={{
        backgroundColor: '#c48e8e',
        border: active ? '2px solid #ef4444' : '2px solid #8d6e63',
        padding: '0.2vw',
        transition: 'border-color 0.3s',
        alignSelf: 'flex-start',
      }}
    >
      <div
        className="rounded-[0.3vw] overflow-hidden"
        style={{ backgroundColor: '#1e293b', border: '2px solid #000' }}
      >
        {/* Title row: PORTF + hex value */}
        <div
          className="flex items-center justify-between text-white font-black uppercase"
          style={{
            fontSize: '0.65vw',
            padding: '0.15vh 0.5vw',
            backgroundColor: 'rgba(0,0,0,0.6)',
          }}
        >
          <span>PORTF</span>
          <span
            key={active ? `portf-hex-${stepKey}` : 'portf-hex'}
            className="font-mono"
            style={{
              color: '#fbbf24',
              animation: active ? 'dataReceive 0.75s ease-out forwards' : undefined,
            }}
          >
            {portF}
          </span>
        </div>

        {/* LEDs */}
        <div
          key={active ? `portf-active-${stepKey}` : 'portf'}
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '0.4vw',
            padding: '0.25vh 0.5vw 0.2vh',
            animation: active ? 'dataReceive 0.75s ease-out forwards' : undefined,
          }}
        >
          {[7, 6, 5, 4, 3, 2, 1, 0].map((bit) => {
            const lit = Boolean((value >> bit) & 1);
            return (
              <div key={bit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.1vh' }}>
                <div
                  style={{
                    width: '0.8vw',
                    height: '0.8vw',
                    borderRadius: '50%',
                    backgroundColor: lit ? '#fbbf24' : '#374151',
                    border: lit ? '1px solid #f59e0b' : '1px solid #64748b',
                    boxShadow: lit ? '0 0 5px 2px rgba(251,191,36,0.7)' : 'none',
                    transition: 'background-color 0.3s, box-shadow 0.3s',
                  }}
                />
                <span style={{ fontSize: '0.4vw', color: '#94a3b8', fontFamily: 'monospace' }}>
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
