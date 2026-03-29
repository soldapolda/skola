import type { FlashWord } from '../types';

interface Props {
  flash:           FlashWord[];
  activeAddress?:  number; // word address currently pointed to by PC
}

const COLS = '3fr 5fr';

function fmtAddr(n: number): string {
  return `0x${n.toString(16).padStart(2, '0').toUpperCase()}`;
}

export default function Ram({ flash, activeAddress }: Props) {
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
              gridTemplateColumns: COLS,
              fontSize: '1.1vw',
              padding: '0.5vh 0',
              backgroundColor: 'rgba(0,0,0,0.5)',
            }}
          >
            <span style={{ color: '#fbbf24' }}>Návěstí</span>
            <span>Instrukce</span>
          </div>

          {/* Rows — second words are hidden; their ID is placed on the first word's row */}
          <div className="flex-1 text-white overflow-auto" style={{ fontSize: '1.2vw' }}>
            {flash.filter(w => !w.isSecondWord).map((word) => {
              const isActive = word.address === activeAddress;
              // For 2-word instructions the PC lands on the first word; also accept second-word address
              const secondWord = flash.find(w => w.address === word.address + 1 && w.isSecondWord);
              const secondActive = secondWord != null && secondWord.address === activeAddress;
              const active = isActive || secondActive;
              return (
                <div
                  key={word.address}
                  // Expose both IDs so connections/flying-value can target either address
                  id={`ram-row-${fmtAddr(word.address)}`}
                  className="grid border-b-2 border-black/20 text-center"
                  style={{
                    gridTemplateColumns: COLS,
                    padding: '0.55vh 0',
                    backgroundColor: active ? '#f59e0b' : undefined,
                    animation: active ? 'activePulse 1.2s ease-in-out infinite' : undefined,
                    transition: 'background-color 0.3s',
                  }}
                >
                  <span
                    className="font-mono font-black"
                    style={{
                      color: active ? '#7c3aed' : '#fbbf24',
                      fontSize: '1vw',
                      alignSelf: 'center',
                    }}
                  >
                    {word.loopLabel ?? ''}
                  </span>
                  <span
                    className="font-bold"
                    style={{ fontFamily: "'Segoe UI', sans-serif", textAlign: 'left', paddingLeft: '0.4vw' }}
                  >
                    {word.label}
                    {secondWord && (
                      <span style={{ fontSize: '0.8em', color: active ? '#7c3aed' : '#c4b5fd', marginLeft: '0.4em' }}>
                        (32b)
                      </span>
                    )}
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
