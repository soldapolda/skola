import type { DecodedInstruction } from '../types';

interface Props {
  decoded:      DecodedInstruction;
  active?:      boolean;
  animateDekod?: boolean;
  stepKey:      number;
}

export default function Dekodovani({ decoded, active = false, animateDekod, stepKey }: Props) {
  return (
    <div
      id="dekodovani-box"
      className="shadow-2xl rounded-lg"
      style={{
        width: '21vw',
        padding: '0.9vw',
        backgroundColor: active ? '#fef3c7' : '#c48e8e',
        border: active ? '4px solid #f59e0b' : '4px solid #333',
        animation: active ? 'activePulse 1.2s ease-in-out infinite' : undefined,
        transition: 'background-color 0.3s, border-color 0.3s',
      }}
    >
      <h3
        className="text-center font-black uppercase border-b-4 border-black/10"
        style={{ fontSize: '1.5vw', marginBottom: '1vh', paddingBottom: '0.5vh' }}
      >
        Dekódování
      </h3>

      {/* Instruction bar — plays decodingReveal when content is first decoded */}
      <div
        key={animateDekod ? `dekod-anim-${stepKey}` : 'dekod'}
        style={{
          display: 'flex',
          backgroundColor: '#1d4ed8',
          borderRadius: '0.3vw',
          overflow: 'hidden',
          animation: animateDekod ? 'decodingReveal 0.7s ease-out forwards' : undefined,
        }}
      >
        <span
          id="instr-opcode"
          className="font-mono font-black text-white text-center"
          style={{
            flex: '0 0 30%',
            fontSize: '1.8vw',
            padding: '0.8vh 0',
            borderRight: '2px solid rgba(255,255,255,0.35)',
          }}
        >
          {decoded.opcode}
        </span>
        <span
          id="instr-operands"
          className="font-mono font-black text-white text-center"
          style={{ flex: 1, fontSize: '1.8vw', padding: '0.8vh 0' }}
        >
          {decoded.operands}
        </span>
      </div>

      <div style={{ display: 'flex', marginTop: '0.5vh' }}>
        <div className="text-center font-black" style={{ flex: '0 0 30%', fontSize: '0.9vw', lineHeight: 1.2 }}>
          <div style={{ fontSize: '1.1vw' }}>↑</div>
          OPERACE
        </div>
        <div className="text-center font-black" style={{ flex: 1, fontSize: '0.9vw', lineHeight: 1.2 }}>
          <div style={{ fontSize: '1.1vw' }}>↑</div>
          OPERANDY
        </div>
      </div>
    </div>
  );
}
