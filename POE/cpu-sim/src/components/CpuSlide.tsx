import type { CpuState } from '../types';
import Registers from './Registers';
import Alu from './Alu';
import Dekodovani from './Dekodovani';
import ControlUnit from './ControlUnit';
import Ram from './Ram';

interface Props {
  state: CpuState;
}

export default function CpuSlide({ state }: Props) {
  return (
    <div
      className="flex"
      style={{
        width: '100vw',
        height: '100vh',
        padding: '1.2vw',
        gap: '1.2vw',
        backgroundColor: '#f1f5f9',
        boxShadow: '0 40px 120px rgba(0,0,0,0.8), 0 0 0 3px #334155',
        overflow: 'hidden',
      }}
    >
      {/* ── CPU ── */}
      <div className="flex-[3] flex flex-col h-full">
        <div
          className="flex flex-col h-full shadow-2xl"
          style={{
            backgroundColor: '#d1b3b3',
            border: '5px solid #8d6e63',
            borderRadius: '2vw',
            padding: '1.2vw',
            gap: '1vh',
          }}
        >
          <Registers registers={state.registers} />
          <Alu />

          {/* Bottom row */}
          <div className="flex items-end justify-between" style={{ gap: '1vw' }}>
            <Dekodovani decoded={state.decoded} />
            <ControlUnit controlUnit={state.controlUnit} />
          </div>
        </div>
      </div>

      {/* ── RAM ── */}
      <Ram rows={state.ram} />
    </div>
  );
}
