import type { RamRow } from '../types';

interface Props {
  rows: RamRow[];
}

export default function Ram({ rows }: Props) {
  return (
    <div className="flex-1 flex flex-col h-full">
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
            RAM
          </div>

          {/* Column headers */}
          <div
            className="grid grid-cols-2 border-b-4 border-black text-white font-black uppercase text-center"
            style={{ fontSize: '1.4vw', padding: '0.5vh 0', backgroundColor: 'rgba(0,0,0,0.5)' }}
          >
            <span>Adresa</span>
            <span>Data</span>
          </div>

          {/* Rows */}
          <div className="flex-1 font-mono text-white" style={{ fontSize: '1.4vw' }}>
            {rows.map((row) => (
              <div
                key={row.address}
                className={`grid grid-cols-2 border-b-2 border-black/20 text-center ${row.highlighted ? 'bg-yellow-500/40' : ''}`}
                style={{ padding: '0.6vh 0' }}
              >
                <span>{row.address}</span>
                <span>{row.data}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
