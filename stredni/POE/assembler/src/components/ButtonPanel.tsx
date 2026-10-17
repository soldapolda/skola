interface Props {
  pink:          number;        // current PINK register value (active-low, default 0xFF)
  onToggle:      (bit: number) => void;
}

function toHex(n: number): string {
  return `0x${n.toString(16).padStart(2, '0').toUpperCase()}`;
}

export default function ButtonPanel({ pink, onToggle }: Props) {
  return (
    <div
      id="pink-panel"
      className="rounded-[0.5vw] shadow-xl"
      style={{
        backgroundColor: '#c48e8e',
        border: '2px solid #8d6e63',
        padding: '0.2vw',
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
          <span>PINK <span style={{ color: '#f97316' }}>(vstup)</span></span>
          <span className="font-mono" style={{ color: '#fb923c' }}>{toHex(pink)}</span>
        </div>

        {/* Buttons bit 7 → 0 */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '0.55vw',
            padding: '0.35vh 0.6vw 0.3vh',
          }}
        >
          {[7, 6, 5, 4, 3, 2, 1, 0].map((bit) => {
            // Active-low: bit=0 means button IS pressed
            const pressed = ((pink >> bit) & 1) === 0;
            return (
              <div
                key={bit}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.15vh' }}
              >
                <button
                  onClick={() => onToggle(bit)}
                  style={{
                    width: '1.5vw',
                    height: '1.5vw',
                    borderRadius: '0.25vw',
                    backgroundColor: pressed ? '#f97316' : '#374151',
                    border: pressed ? '1.5px solid #ea580c' : '1.5px solid #64748b',
                    boxShadow: pressed ? '0 0 5px 2px rgba(249,115,22,0.7)' : 'none',
                    cursor: 'pointer',
                    transition: 'background-color 0.15s, box-shadow 0.15s',
                    padding: 0,
                  }}
                  title={`B${bit}: ${pressed ? 'stisknuto (0)' : 'uvolněno (1)'}`}
                />
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
