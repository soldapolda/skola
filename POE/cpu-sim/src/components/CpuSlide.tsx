import { useRef, useState, useEffect } from 'react';
import type { CpuState } from '../types';
import { CPU_STEPS, MAX_CPU_STEP } from '../cpuSteps';
import Registers from './Registers';
import Alu from './Alu';
import Dekodovani from './Dekodovani';
import ControlUnit from './ControlUnit';
import Ram from './Ram';
import Connections from './Connections';
import FlyingValue from './FlyingValue';

const BLANK_FLAGS = { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 0, C: 0 };
// SREG after ADD 0x9F + 0xA0: carry=1, signed overflow=1, S=N^V=1
const ADD_FLAGS   = { I: 0, T: 0, H: 0, S: 1, V: 1, N: 0, Z: 0, C: 1 };

interface Props {
  state: CpuState;
  step?: number;
}

export default function CpuSlide({ state, step = 0 }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const def = CPU_STEPS[Math.min(step, MAX_CPU_STEP)];

  // Track which steps have completed their flight animation
  const [arrivedSteps, setArrivedSteps] = useState<Set<number>>(new Set());
  const prevStepRef = useRef(step);
  useEffect(() => {
    if (step < prevStepRef.current) {
      setArrivedSteps(prev => {
        const next = new Set(prev);
        [...next].filter(s => s > step).forEach(s => next.delete(s));
        return next;
      });
    }
    prevStepRef.current = step;
  }, [step]);

  const flightDone = arrivedSteps.has(step);

  // Resolve 'ram-row-pc' sentinel to the actual step-relative PC row ID
  const resolvedFlight = def.flight ? {
    ...def.flight,
    fromId: def.flight.fromId === 'ram-row-pc'
      ? `ram-row-${def.displayPc}`
      : def.flight.fromId,
  } : undefined;

  // Suppress destination value while packet is in-flight
  const displayIr       = (resolvedFlight?.toId === 'ri-row'         && !flightDone) ? '—'  : def.displayIr;
  const displayOpcode   = (resolvedFlight?.toId === 'dekodovani-box'  && !flightDone) ? ''   : def.displayOpcode;
  const displayOperands = (resolvedFlight?.toId === 'dekodovani-box'  && !flightDone) ? ''   : def.displayOperands;

  // Registers whose write animation fires this step
  const animateRegNames = [
    ...(def.animateR0 ? ['R0'] : []),
    ...(def.animateR1 ? ['R1'] : []),
  ];

  const displayState: CpuState = {
    registers: state.registers.map(r => {
      if (r.name === 'R0') return { ...r, value: def.displayR0 };
      if (r.name === 'R1') return { ...r, value: def.displayR1 };
      return r;
    }),
    controlUnit: {
      ir:    displayIr,
      pc:    def.displayPc,
      flags: def.displayFlags ? ADD_FLAGS : BLANK_FLAGS,
    },
    decoded: {
      raw:      displayOpcode ? `${displayOpcode} ${displayOperands}` : '',
      opcode:   displayOpcode,
      operands: displayOperands,
    },
    ram: state.ram,
  };

  // Use step-relative PC to highlight the correct RAM row and draw the connection
  const activeRamAddresses = def.activeRamRow ? [def.displayPc] : [];

  return (
    <div
      ref={containerRef}
      className="flex"
      style={{
        position: 'relative',
        width: '100vw',
        height: '100vh',
        padding: '1.2vw',
        gap: '4vw',
        backgroundColor: '#f1f5f9',
        boxShadow: '0 40px 120px rgba(0,0,0,0.8), 0 0 0 3px #334155',
        overflow: 'hidden',
        fontFamily: "'Segoe UI', sans-serif",
      }}
    >
      {/* ── CPU ── */}
      <div className="flex-[3] flex flex-col h-full">
        <div
          id="cpu-outer"
          className="flex flex-col h-full shadow-2xl"
          style={{
            backgroundColor: '#d1b3b3',
            border: '5px solid #8d6e63',
            borderRadius: '2vw',
            padding: '1.2vw',
            gap: '1vh',
          }}
        >
          <Registers
            registers={displayState.registers}
            activeNames={def.activeRegisters}
            animateNames={animateRegNames}
            stepKey={step}
          />
          <Alu active={def.activeAlu} />

          <div className="flex items-start justify-between" style={{ gap: '1vw' }}>
            <Dekodovani
              decoded={displayState.decoded}
              active={def.activeDek}
              animateDekod={def.animateDekod && (resolvedFlight?.toId !== 'dekodovani-box' || flightDone)}
              stepKey={step}
            />
            <ControlUnit
              controlUnit={displayState.controlUnit}
              activeFields={def.activeFields}
              animateIr={def.animateIr && (resolvedFlight?.toId !== 'ri-row' || flightDone)}
              animatePc={def.animatePc}
              stepKey={step}
            />
          </div>
        </div>
      </div>

      {/* ── RAM ── */}
      <Ram rows={displayState.ram} activeAddresses={activeRamAddresses} />

      {/* ── SVG connections ── */}
      <Connections
        containerRef={containerRef}
        pcAddress={def.displayPc}
        activeTypes={def.activeConnections}
      />

      {/* ── Flying value packet ── */}
      {resolvedFlight && !flightDone && (
        <FlyingValue
          fromId={resolvedFlight.fromId}
          toId={resolvedFlight.toId}
          value={resolvedFlight.value}
          triggerKey={step}
          containerRef={containerRef}
          onArrived={() => setArrivedSteps(prev => new Set([...prev, step]))}
        />
      )}

      {/* ── Step label ── */}
      {def.label && (
        <div style={{
          position: 'absolute',
          bottom: '2.5vh',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: 'rgba(15,23,42,0.88)',
          color: '#fef3c7',
          padding: '0.7vh 2.2vw',
          borderRadius: '0.8vw',
          fontSize: '1.4vw',
          fontWeight: 700,
          whiteSpace: 'nowrap',
          border: '2px solid #f59e0b',
        }}>
          {def.label}
        </div>
      )}

      {/* ── Progress dots ── */}
      <div style={{
        position: 'absolute',
        top: '1.5vh',
        right: '2vw',
        display: 'flex',
        gap: '0.4vw',
        alignItems: 'center',
      }}>
        {Array.from({ length: MAX_CPU_STEP }, (_, i) => (
          <div
            key={i}
            style={{
              width: '0.6vw',
              height: '0.6vw',
              borderRadius: '50%',
              backgroundColor: step > i ? '#f59e0b' : '#cbd5e1',
              transition: 'background-color 0.3s',
            }}
          />
        ))}
      </div>
    </div>
  );
}
