import { useRef, useState, useEffect } from 'react';
import type { CpuState } from '../types';
import { CPU_STEPS, MAX_CPU_STEP } from '../cpuSteps';
import Registers from './Registers';
import Alu from './Alu';
import ControlUnit from './ControlUnit';
import Ram from './Ram';
import PortPanel from './PortPanel';
import Connections from './Connections';
import FlyingValue from './FlyingValue';

const BLANK_FLAGS = { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 0, C: 0 };
const Z_FLAGS     = { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 1, C: 0 };

interface Props {
  state: CpuState;
  step?: number;
}

export default function CpuSlide({ state, step = 0 }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const def = CPU_STEPS[Math.min(step, MAX_CPU_STEP)];

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

  const resolvedFlight = def.flight ? {
    ...def.flight,
    fromId: def.flight.fromId === 'ram-row-pc'
      ? `ram-row-${def.displayPc}`
      : def.flight.fromId,
  } : undefined;

  const displayIr = (resolvedFlight?.toId === 'ri-row' && !flightDone) ? '—' : def.displayIr;

  const animateRegNames = [
    ...(def.animateR16 ? ['R16'] : []),
    ...(def.animateR17 ? ['R17'] : []),
    ...(def.animateR18 ? ['R18'] : []),
  ];

  const displayState: CpuState = {
    registers: state.registers.map(r => {
      if (r.name === 'R16') return { ...r, value: def.displayR16 };
      if (r.name === 'R17') return { ...r, value: def.displayR17 };
      if (r.name === 'R18') return { ...r, value: def.displayR18 };
      return r;
    }),
    controlUnit: {
      ir:    displayIr,
      pc:    def.displayPc,
      flags: def.displayFlagZ ? Z_FLAGS : BLANK_FLAGS,
    },
    ram: state.ram,
    portF: def.displayPortF,
  };

  const activeRamAddresses = def.activeRamRow ? [def.displayPc] : [];

  const topRegs    = displayState.registers.slice(0, 4);
  const bottomRegs = displayState.registers.slice(4, 8);

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
      {/* ── CPU + PORTF above ── */}
      <div className="flex-[3] flex flex-col h-full" style={{ gap: '1.5vh' }}>
        <PortPanel
          portF={displayState.portF}
          active={def.activePortF}
          stepKey={step}
        />
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
            activeNames={def.activeRegisters}
            animateNames={animateRegNames}
            stepKey={step}
          />

          {/* ALU */}
          <Alu active={def.activeAlu} />

          {/* R20–R23 below ALU */}
          <Registers
            registers={bottomRegs}
            activeNames={def.activeRegisters}
            animateNames={animateRegNames}
            stepKey={step}
          />

          {/* ControlUnit — pushed to bottom-right of card */}
          <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end' }}>
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

      {/* ── Right column: FLASH ── */}
      <div className="flex-1 flex flex-col h-full">
        <Ram rows={displayState.ram} activeAddresses={activeRamAddresses} />
      </div>

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
          fontSize: '1.3vw',
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
