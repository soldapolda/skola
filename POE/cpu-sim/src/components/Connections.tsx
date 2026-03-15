import type { RefObject } from 'react';
import { useElementRects } from '../hooks/useElementRects';

// ── colours ───────────────────────────────────────────────────────────────────

const C = {
  reg:   '#3b82f6', // blue   — R0-R3 → ALU
  dekod: '#f97316', // orange — Dekodovani → ALU, Dekodovani → RI
  alu:   '#a855f7', // purple — ALU → SREG
  pc:    '#22c55e', // green  — PC → ALU, PC → RAM
} as const;

const SW = 4; // stroke-width (px)

// ── routing helpers ───────────────────────────────────────────────────────────

/** Absolute mid-y of a rect. */
const midY = (r: DOMRect) => r.top  + r.height / 2;
/** Absolute mid-x of a rect. */
const midX = (r: DOMRect) => r.left + r.width  / 2;

/**
 * Orthogonal path that goes HORIZONTAL first, then VERTICAL.
 * Usage: hv(x0,y0, x1,y1) → "M x0 y0 H x1 V y1"
 * Chain more waypoints: hv(x0,y0, x1,y1, x2,y2) uses H-V alternation.
 */
function hv(...pts: number[]): string {
  // pts = [x0,y0, x1,y1, x2,y2, ...]
  let d = `M ${pts[0]} ${pts[1]}`;
  for (let i = 2; i < pts.length; i += 2) {
    d += ` H ${pts[i]} V ${pts[i + 1]}`;
  }
  return d;
}

/**
 * Orthogonal path that goes VERTICAL first, then HORIZONTAL.
 * Usage: vh(x0,y0, x1,y1) → "M x0 y0 V y1 H x1"
 */
function vh(...pts: number[]): string {
  let d = `M ${pts[0]} ${pts[1]}`;
  for (let i = 2; i < pts.length; i += 2) {
    d += ` V ${pts[i + 1]} H ${pts[i]}`;
  }
  return d;
}

// ── component ─────────────────────────────────────────────────────────────────

interface Props {
  containerRef: RefObject<HTMLDivElement | null>;
  /** PC value string, e.g. "0x01" — used to find the matching RAM row. */
  pcAddress: string;
}

export default function Connections({ containerRef, pcAddress }: Props) {
  const IDS = [
    'reg-R0', 'reg-R1', 'reg-R2', 'reg-R3',
    'alu-shape',
    'dekodovani-box',
    'cu-box',
    'cpu-outer',
    'ri-row',
    'pc-row',
    'sreg-box',
    `ram-row-${pcAddress}`,
  ];

  const r = useElementRects(IDS, containerRef);

  const alu      = r['alu-shape'];
  const dek      = r['dekodovani-box'];
  const cu       = r['cu-box'];
  const cpuOuter = r['cpu-outer'];
  const ri       = r['ri-row'];
  const pc       = r['pc-row'];
  const sreg     = r['sreg-box'];
  const pcRow    = r[`ram-row-${pcAddress}`];

  if (!alu || !dek || !cu || !cpuOuter || !ri || !pc || !sreg || !pcRow) return null;

  // ── layout measurements ───────────────────────────────────────────────────

  const aluTop  = alu.top;
  const aluBot  = alu.top + alu.height;
  const aluL    = alu.left;
  const aluW    = alu.width;

  // Horizontal bus just above ALU — register lines meet here before fanning in.
  const busAboveAlu = aluTop - 8;

  // Gap between Dekodovani right edge and ControlUnit left edge.
  const gapL = dek.left + dek.width;  // = dek.right
  const gapR = cu.left;
  // Two vertical lanes inside this gap (well separated).
  const laneA = gapL + (gapR - gapL) * 0.28; // Dek→RI
  const laneB = gapL + (gapR - gapL) * 0.72; // ALU→SREG

  const lines: { d: string; color: string }[] = [];

  // ── 1. Registers → ALU top (blue) ────────────────────────────────────────
  // Each register drops to the shared bus just above the ALU, then fans in
  // horizontally to an evenly-spaced entry point on the ALU top edge.
  const regFracs = [0.15, 0.38, 0.62, 0.85];

  (['R0', 'R1', 'R2', 'R3'] as const).forEach((name, i) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx = midX(reg);
    const ry = reg.top + reg.height;   // register bottom
    const tx = aluL + aluW * regFracs[i]; // target on ALU top
    // Down to bus → horizontal to target → down into ALU
    lines.push({ d: vh(rx, ry, tx, busAboveAlu) + ` V ${aluTop}`, color: C.reg });
  });

  // ── 2. Dekodovani → ALU bottom-left 25 % (orange) ───────────────────────
  // Exits Dek right side at 25 % height → goes right through the open gap to
  // the ALU entry x → rises straight up into ALU bottom.
  {
    const ent = aluL + aluW * 0.25;
    lines.push({ d: hv(dek.left + dek.width, dek.top + dek.height * 0.25, ent, aluBot), color: C.dekod });
  }

  // ── 3. Dekodovani → RI (orange) ──────────────────────────────────────────
  // Exits Dek right side, jogs right into laneA, rises to RI height, enters RI.
  {
    const dy  = midY(dek);
    const ry  = midY(ri);
    lines.push({ d: hv(dek.left + dek.width, dy, laneA, ry, ri.left, ry), color: C.dekod });
  }

  // ── 4. ALU → SREG (purple) ───────────────────────────────────────────────
  // Exits ALU bottom at laneB x (within trapezoid 25–75 % range, in the open
  // gap between Dek and CU) → drops straight down → enters SREG from the left.
  {
    const sy = midY(sreg);
    lines.push({ d: `M ${laneB} ${aluBot} V ${sy} H ${sreg.left}`, color: C.alu });
  }

  // ── 5. PC → ALU bottom-center (green) ────────────────────────────────────
  // Exits CU left edge at PC height, goes left to ALU center-x, rises into ALU.
  {
    const py   = midY(pc);
    const alcx = aluL + aluW * 0.5; // ALU center bottom
    lines.push({ d: hv(cu.left, py, alcx, aluBot), color: C.pc });
  }

  // ── 6. PC → RAM row matching the PC address (green) ──────────────────────
  // Exit PC right → go right to the gap between CPU outer box and RAM →
  // drop/rise vertically in that gap to the target row height → enter RAM.
  {
    const py   = midY(pc);
    const rry  = midY(pcRow);
    const cpuR = cpuOuter.left + cpuOuter.width;
    // Midpoint of the gap between CPU outer box and RAM panel.
    const gapX = cpuR + (pcRow.left - cpuR) / 2;
    lines.push({ d: hv(pc.left + pc.width, py, gapX, rry, pcRow.left, rry), color: C.pc });
  }

  return (
    <svg
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        overflow: 'visible',
      }}
    >
      {lines.map(({ d, color }, i) => (
        <path
          key={i}
          d={d}
          fill="none"
          stroke={color}
          strokeWidth={SW}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
    </svg>
  );
}
