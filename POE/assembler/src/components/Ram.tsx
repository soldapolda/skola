import type { RamRow } from '../types';

interface Props {
  rows: RamRow[];
  activeAddresses?: string[];
}

export default function Ram({ rows, activeAddresses = [] }: Props) {
  return (
    <div id="ram-panel" className="flex-1 flex flex-col h-full">
      <div
        className="rounded-[1.5vw] flex flex-col h-full shadow-2xl"
        style={{ backgroundColor: '#c48e8e', border: '5px solid #8d6e63', padding: '0.8vw' }}
      >
        <div
          className="rounded-[1vw] overflow-hidden flex flex-col h-full"
          style={{ backgroundColor: '#7b1fa2', border: '4px solid #000' }}
        >
          {/* Title */}
          <div
            className="text-white text-center font-black uppercase"
            style={{ fontSize: '1.6vw', padding: '0.6vh 0', backgroundColor: 'rgba(0,0,0,0.6)' }}
          >
            FLASH
          </div>

          {/* Column headers */}
          <div
            className="grid border-b-4 border-black text-white font-black uppercase text-center"
            style={{
              gridTemplateColumns: '2fr 5fr',
              fontSize: '1.2vw',
              padding: '0.5vh 0',
              backgroundColor: 'rgba(0,0,0,0.5)',
            }}
          >
            <span>Adr.</span>
            <span>Instrukce</span>
          </div>

          {/* Rows */}
          <div className="flex-1 text-white" style={{ fontSize: '1.3vw' }}>
            {rows.map((row) => {
              const stepActive = activeAddresses.includes(row.address);
              return (
                <div
                  key={row.address}
                  id={`ram-row-${row.address}`}
                  className="grid border-b-2 border-black/20 text-center"
                  style={{
                    gridTemplateColumns: '2fr 5fr',
                    padding: '0.7vh 0',
                    backgroundColor: stepActive
                      ? '#f59e0b'
                      : row.highlighted
                        ? 'rgba(234,179,8,0.4)'
                        : undefined,
                    animation: stepActive ? 'activePulse 1.2s ease-in-out infinite' : undefined,
                    transition: 'background-color 0.3s',
                  }}
                >
                  <span className="font-mono">{row.address}</span>
                  <span className="font-bold" style={{ fontFamily: "'Segoe UI', sans-serif" }}>
                    {row.label ?? row.data}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
