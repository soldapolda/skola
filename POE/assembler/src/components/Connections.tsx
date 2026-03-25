import type { RefObject } from 'react';
import { useElementRects } from '../hooks/useElementRects';
import type { ConnectionType } from '../cpuSteps';

// ── colours ───────────────────────────────────────────────────────────────────

const C = {
  reg:  '#3b82f6', // blue   — registers → ALU
  ri:   '#f97316', // orange — RI → ALU
  alu:  '#a855f7', // purple — ALU → SREG
  pc:   '#22c55e', // green  — PC → FLASH
} as const;

const SW = 4;

// ── routing helpers ───────────────────────────────────────────────────────────

const midY = (r: DOMRect) => r.top  + r.height / 2;
const midX = (r: DOMRect) => r.left + r.width  / 2;
const botY = (r: DOMRect) => r.top  + r.height;
const topY = (r: DOMRect) => r.top;

// Move horizontally then vertically
function hv(x1: number, y1: number, x2: number, y2: number): string {
  return `M ${x1} ${y1} H ${x2} V ${y2}`;
}

// Move vertically then horizontally
function vh(x1: number, y1: number, x2: number, y2: number): string {
  return `M ${x1} ${y1} V ${y2} H ${x2}`;
}

// ── component ─────────────────────────────────────────────────────────────────

interface Props {
  containerRef: RefObject<HTMLDivElement | null>;
  pcAddress: string;
  activeTypes: ConnectionType[];
}

interface Line { d: string; color: string; type: ConnectionType }

export default function Connections({ containerRef, pcAddress, activeTypes }: Props) {
  const IDS = [
    'reg-R16', 'reg-R17', 'reg-R18', 'reg-R19',
    'reg-R20', 'reg-R21', 'reg-R22', 'reg-R23',
    'alu-shape', 'cu-box', 'cpu-outer',
    'ri-row', 'pc-row', 'sreg-box',
    `ram-row-${pcAddress}`,
  ];

  const r = useElementRects(IDS, containerRef);

  const alu      = r['alu-shape'];
  const cu       = r['cu-box'];
  const cpuOuter = r['cpu-outer'];
  const ri       = r['ri-row'];
  const pc       = r['pc-row'];
  const sreg     = r['sreg-box'];
  const pcRow    = r[`ram-row-${pcAddress}`];
  const r21      = r['reg-R21'];
  const r22      = r['reg-R22'];

  if (!alu || !cu || !cpuOuter || !ri || !pc || !sreg) return null;

  const aluTop = alu.top;
  const aluBot = botY(alu);
  const aluL   = alu.left;
  const aluW   = alu.width;

  // Vertical lane between R21 and R22 — used by RI→ALU and ALU→SREG
  // Falls back to ALU center if rects not yet measured
  const laneX = (r21 && r22)
    ? (r21.left + r21.width + r22.left) / 2
    : aluL + aluW * 0.5;

  // Bus rails just outside the ALU edges (for clean L-shaped register wires)
  const busTopRail    = aluTop - 10;
  const busBottomRail = aluBot  + 10;

  const lines: Line[] = [];

  // ── 1. Top registers (R16–R19) → ALU top (blue) ──────────────────────────
  // Fracs avoid the center lane. Top 4: left pair and right pair, spaced outward.
  const topFracs: Record<string, number> = {
    'R16': 0.13, 'R17': 0.35, 'R18': 0.65, 'R19': 0.87,
  };
  (['R16', 'R17', 'R18', 'R19'] as const).forEach((name) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx  = midX(reg);
    const ry  = botY(reg);
    const tx  = aluL + aluW * topFracs[name];
    // Go down to rail, then across to target X, then down into ALU top
    lines.push({
      d: `M ${rx} ${ry} V ${busTopRail} H ${tx} V ${aluTop}`,
      color: C.reg,
      type: `reg-${name}-alu` as ConnectionType,
    });
  });

  // ── 2. Bottom registers (R20–R23) → ALU bottom (blue) ────────────────────
  // Same fracs as top. Avoid center lane (laneX is at ~0.5 of ALU width).
  // ALU bottom edge spans only 25%–75% (trapezoid clip-path), so fracs must stay within that range
  const botFracs: Record<string, number> = {
    'R20': 0.28, 'R21': 0.38, 'R22': 0.62, 'R23': 0.72,
  };
  (['R20', 'R21', 'R22', 'R23'] as const).forEach((name) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx = midX(reg);
    const ry = topY(reg);
    const tx = aluL + aluW * botFracs[name];
    // Go up to rail, then across to target X, then up into ALU bottom
    lines.push({
      d: `M ${rx} ${ry} V ${busBottomRail} H ${tx} V ${aluBot}`,
      color: C.reg,
      type: `reg-${name}-alu` as ConnectionType,
    });
  });

  // ── 3. RI → ALU bottom (orange) — through R21/R22 lane ───────────────────
  {
    const riY = midY(ri);
    // Exit RI right edge → go right to laneX → go up through bottom-regs → enter ALU bottom
    const riRight = ri.left + ri.width;
    lines.push({
      d: `M ${riRight} ${riY} H ${laneX} V ${aluBot}`,
      color: C.ri,
      type: 'ri-alu',
    });
  }

  // ── 4. ALU → SREG (purple) — through R21/R22 lane ─────────────────────────
  {
    const sregY = midY(sreg);
    // Exit ALU bottom at laneX → go down through bottom-regs → enter SREG left
    lines.push({
      d: `M ${laneX} ${aluBot} V ${sregY} H ${sreg.left}`,
      color: C.alu,
      type: 'alu-sreg',
    });
  }

  // ── 5. PC → FLASH row (green) ─────────────────────────────────────────────
  if (pcRow) {
    const py   = midY(pc);
    const rry  = midY(pcRow);
    const cpuR = cpuOuter.left + cpuOuter.width;
    const gapX = cpuR + (pcRow.left - cpuR) / 2;
    lines.push({
      d: hv(pc.left + pc.width, py, gapX, py) + ` V ${rry} H ${pcRow.left}`,
      color: C.pc,
      type: 'pc-ram',
    });
  }

  return (
    <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none', overflow: 'visible' }}>
      {lines.map(({ d, color, type }, i) => {
        const active = activeTypes.includes(type);
        return (
          <path
            key={i}
            d={d}
            fill="none"
            stroke={color}
            strokeWidth={active ? SW + 1 : SW}
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray={active ? '10 6' : undefined}
            opacity={active ? 1 : 0.10}
            style={active ? { animation: 'flowDash 0.5s linear infinite' } : undefined}
          />
        );
      })}
    </svg>
  );
}
