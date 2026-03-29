import { useRef } from 'react';
import type { EmulatorState, ConnectionType, DecodedInstruction, ExecPhase } from '../types';
import Registers from './Registers';
import Alu from './Alu';
import ControlUnit from './ControlUnit';
import Ram from './Ram';
import PortPanel from './PortPanel';
import DdrPanel from './DdrPanel';
import ButtonPanel from './ButtonPanel';
import Connections from './Connections';
import FlyingValue from './FlyingValue';

// ── display helpers ───────────────────────────────────────────────────────────

function toHex(n: number): string {
  return `0x${n.toString(16).padStart(2, '0').toUpperCase()}`;
}

function fmtAddr(n: number): string {
  return `0x${n.toString(16).padStart(2, '0').toUpperCase()}`;
}

// Derive which SVG bus lines should animate this phase/instruction
function activeConnections(
  phase: ExecPhase,
  decoded: DecodedInstruction | null,
): ConnectionType[] {
  if (phase === 'fetch') return ['pc-ram'];
  if (!decoded) return [];
  const { instr } = decoded;
  switch (instr.op) {
    case 'LDI':             return [`reg-R${instr.rd}-alu` as ConnectionType];
    case 'INC': case 'DEC': return [`reg-R${instr.rd}-alu` as ConnectionType, 'alu-sreg'];
    case 'LDS':             return ['pink-in', `reg-R${instr.rd}-alu` as ConnectionType];
    case 'OUT':
      return instr.port === 'PORTF'
        ? [`reg-R${instr.rr}-alu` as ConnectionType, 'portf-out']
        : [`reg-R${instr.rr}-alu` as ConnectionType];
    case 'SBRC':            return [`reg-R${instr.rr}-alu` as ConnectionType];
    case 'RJMP': case 'JMP': return ['pc-ram'];
    default:                return [];
  }
}

// Which register cells pulse orange
function activeRegNames(phase: ExecPhase, decoded: DecodedInstruction | null): string[] {
  if (phase !== 'execute' || !decoded) return [];
  const { instr } = decoded;
  if (instr.op === 'LDI' || instr.op === 'INC' || instr.op === 'DEC' || instr.op === 'LDS')
    return [`R${instr.rd}`];
  if (instr.op === 'SBRC' || instr.op === 'OUT') return [`R${instr.rr}`];
  return [];
}

// Which register cells play the dataReceive flash animation
function animateRegNames(phase: ExecPhase, decoded: DecodedInstruction | null): string[] {
  if (phase !== 'execute' || !decoded) return [];
  const { instr } = decoded;
  if (instr.op === 'LDI' || instr.op === 'INC' || instr.op === 'DEC' || instr.op === 'LDS')
    return [`R${instr.rd}`];
  return [];
}

// Human-readable step label (Czech)
function stepLabel(phase: ExecPhase, decoded: DecodedInstruction | null, pc: number): string {
  if (phase === 'fetch') return `Fetch — PC = ${fmtAddr(pc)}, načítám instrukci…`;
  if (!decoded) return '';
  const { instr, label: lbl } = decoded;
  switch (instr.op) {
    case 'LDI': case 'LDS':
      return `Execute — ${lbl} → R${instr.rd} = ${toHex(decoded.result ?? 0)}`;
    case 'INC': case 'DEC':
      return `Execute — ${lbl} → R${instr.rd} = ${toHex(decoded.result ?? 0)}, SREG aktualizován`;
    case 'OUT':
      return `Execute — ${lbl} → ${instr.port} = ${toHex(decoded.result ?? 0)}`;
    case 'SBRC':
      return decoded.skip
        ? `Execute — ${lbl}: bit ${instr.bit} = 0 → přeskočení`
        : `Execute — ${lbl}: bit ${instr.bit} = 1 → pokračování`;
    case 'RJMP': case 'JMP':
      return `Execute — ${lbl}: PC ← ${fmtAddr(decoded.jumpTarget ?? instr.target)}`;
    default:
      return `Execute — ${lbl}`;
  }
}

// Which ControlUnit fields to highlight
function cuActiveFields(
  phase: ExecPhase,
  decoded: DecodedInstruction | null,
): Array<'pc' | 'sreg'> {
  if (phase === 'fetch') return ['pc'];
  if (!decoded) return [];
  const { op } = decoded.instr;
  if (op === 'INC' || op === 'DEC') return ['sreg'];
  if (op === 'RJMP' || op === 'JMP' || op === 'SBRC') return ['pc'];
  return [];
}

// Instruction-specific label for the Step button
function nextStepLabel(state: EmulatorState): string {
  if (state.phase === 'fetch') {
    const word = state.flash.find(w => w.address === state.pc && !w.isSecondWord);
    return word ? `Fetch: ${word.label}` : 'Fetch';
  }
  return state.currentInstruction
    ? `Execute: ${state.currentInstruction.label}`
    : 'Execute';
}

// Phase button colors
const PHASE_COLORS: Record<ExecPhase, { bg: string; border: string }> = {
  fetch:   { bg: '#1e40af', border: '#3b82f6' },
  execute: { bg: '#92400e', border: '#f59e0b' },
};

// ── component ─────────────────────────────────────────────────────────────────

interface Props {
  state:          EmulatorState;
  onStep:         () => void;
  onReset:        () => void;
  onToggleButton: (bit: number) => void;
}

export default function CpuSlide({ state, onStep, onReset, onToggleButton }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const { phase, pc, registers, portF, ddrF, ddrK, sreg, flash, currentInstruction, flightKey } = state;

  const hexPc       = fmtAddr(pc);
  const flashAtPc   = flash.find(w => w.address === pc && !w.isSecondWord);

  const activeConns  = activeConnections(phase, currentInstruction);
  const activeRegs   = activeRegNames(phase, currentInstruction);
  const animateRegs  = animateRegNames(phase, currentInstruction);

  const activeAlu   = phase === 'execute';
  const activePortF = phase === 'execute' && currentInstruction?.instr.op === 'OUT' && currentInstruction.instr.port === 'PORTF';
  const activeDdrF  = phase === 'execute' && currentInstruction?.instr.op === 'OUT' && currentInstruction.instr.port === 'DDRF';
  const animatePc   = phase === 'execute' && currentInstruction != null && (
    currentInstruction.instr.op === 'RJMP' || currentInstruction.instr.op === 'JMP' || currentInstruction.instr.op === 'SBRC'
  );

  // Build Register display rows (R16–R23)
  const displayRegs = [16, 17, 18, 19, 20, 21, 22, 23].map(n => ({
    name:  `R${n}`,
    value: toHex(registers[n]),
  }));
  const topRegs    = displayRegs.slice(0, 4);
  const bottomRegs = displayRegs.slice(4, 8);

  // Step key for animation retrigger (combine flightKey + phase for uniqueness)
  const stepKey   = flightKey * 2 + (phase === 'fetch' ? 0 : 1);
  const phaseInfo = PHASE_COLORS[phase];
  const label     = stepLabel(phase, currentInstruction, pc);
  const stepBtn   = nextStepLabel(state);

  return (
    <div
      ref={containerRef}
      className="flex"
      style={{
        position: 'relative',
        width: '100vw',
        height: '100vh',
        padding: '1.2vw',
        gap: '2vw',
        backgroundColor: '#f1f5f9',
        boxShadow: '0 40px 120px rgba(0,0,0,0.8), 0 0 0 3px #334155',
        overflow: 'hidden',
        fontFamily: "'Segoe UI', sans-serif",
      }}
    >
      {/* ── Left column: panels + CPU box ── */}
      <div className="flex-[3] flex flex-col h-full" style={{ gap: '1vh' }}>
        {/* Top panels row: PORTF | DDRF | DDRK | PINK buttons */}
        <div style={{ display: 'flex', gap: '1vw', alignItems: 'flex-start' }}>
          <PortPanel
            portF={toHex(portF)}
            active={activePortF}
            stepKey={stepKey}
          />
          <DdrPanel
            id="ddrf-panel"
            name="DDRF"
            value={ddrF}
            active={activeDdrF}
            stepKey={stepKey}
          />
          <DdrPanel
            id="ddrk-panel"
            name="DDRK"
            value={ddrK}
          />
          <ButtonPanel
            pink={state.pink}
            onToggle={onToggleButton}
          />
        </div>

        {/* CPU box */}
        <div
          id="cpu-outer"
          className="flex flex-col flex-1 shadow-2xl"
          style={{
            backgroundColor: '#d1b3b3',
            border: '5px solid #8d6e63',
            borderRadius: '2vw',
            padding: '1.2vw',
            gap: '1.5vh',
          }}
        >
          {/* R16–R19 above ALU */}
          <Registers
            registers={topRegs}
            activeNames={activeRegs}
            animateNames={animateRegs}
            stepKey={stepKey}
          />

          {/* ALU */}
          <Alu active={activeAlu} />

          {/* R20–R23 below ALU */}
          <Registers
            registers={bottomRegs}
            activeNames={activeRegs}
            animateNames={animateRegs}
            stepKey={stepKey}
          />

          {/* ControlUnit — pinned to bottom-right */}
          <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end' }}>
            <ControlUnit
              sreg={sreg}
              activeFields={cuActiveFields(phase, currentInstruction)}
              animatePc={animatePc}
              stepKey={stepKey}
            />
          </div>
        </div>
      </div>

      {/* ── Right column: FLASH ── */}
      <div className="flex-1 flex flex-col h-full">
        <Ram
          flash={flash}
          activeAddress={pc}
        />
      </div>

      {/* ── SVG connections ── */}
      <Connections
        containerRef={containerRef}
        pcAddress={hexPc}
        activeTypes={activeConns}
      />

      {/* ── Flying value packet: Flash row → ALU (fetch phase only) ── */}
      {phase === 'fetch' && flashAtPc && (
        <FlyingValue
          fromId={`ram-row-${hexPc}`}
          toId="alu-shape"
          value={flashAtPc.hex}
          triggerKey={flightKey}
          containerRef={containerRef}
          onArrived={() => {}}
        />
      )}

      {/* ── Step label (bottom-centre) ── */}
      {label && (
        <div style={{
          position: 'absolute',
          bottom: '2.5vh',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: 'rgba(15,23,42,0.88)',
          color: '#fef3c7',
          padding: '0.7vh 2.2vw',
          borderRadius: '0.8vw',
          fontSize: '1.3vw',
          fontWeight: 700,
          whiteSpace: 'nowrap',
          border: '2px solid #f59e0b',
        }}>
          {label}
        </div>
      )}

      {/* ── Controls (top-right) ── */}
      <div style={{
        position: 'absolute',
        top: '1.5vh',
        right: '2vw',
        display: 'flex',
        gap: '0.8vw',
        alignItems: 'center',
      }}>
        <button
          onClick={onReset}
          style={{
            padding: '0.5vh 1.2vw',
            fontSize: '1vw',
            fontWeight: 700,
            backgroundColor: '#334155',
            color: '#fff',
            border: '2px solid #64748b',
            borderRadius: '0.5vw',
            cursor: 'pointer',
            whiteSpace: 'nowrap',
          }}
          title="Reset (←)"
        >
          ↺ Reset
        </button>
        <button
          onClick={onStep}
          style={{
            padding: '0.5vh 1.2vw',
            fontSize: '1vw',
            fontWeight: 900,
            backgroundColor: phaseInfo.bg,
            color: '#fff',
            border: `2px solid ${phaseInfo.border}`,
            borderRadius: '0.5vw',
            cursor: 'pointer',
            whiteSpace: 'nowrap',
          }}
          title="Step (→ or Space)"
        >
          {stepBtn}
        </button>
      </div>
    </div>
  );
}
