import type { RefObject } from 'react';
import { useElementRects } from '../hooks/useElementRects';
import type { ConnectionType } from '../cpuSteps';

// ── colours ───────────────────────────────────────────────────────────────────

const C = {
  reg:   '#3b82f6', // blue   — R0-R3 → ALU
  dekod: '#f97316', // orange — Dekodovani → ALU, Dekodovani → RI
  alu:   '#a855f7', // purple — ALU → SREG
  pc:    '#22c55e', // green  — PC → ALU, PC → RAM
} as const;

const SW = 4;

// ── routing helpers ───────────────────────────────────────────────────────────

const midY = (r: DOMRect) => r.top  + r.height / 2;
const midX = (r: DOMRect) => r.left + r.width  / 2;

function hv(...pts: number[]): string {
  let d = `M ${pts[0]} ${pts[1]}`;
  for (let i = 2; i < pts.length; i += 2) d += ` H ${pts[i]} V ${pts[i + 1]}`;
  return d;
}

function vh(...pts: number[]): string {
  let d = `M ${pts[0]} ${pts[1]}`;
  for (let i = 2; i < pts.length; i += 2) d += ` V ${pts[i + 1]} H ${pts[i]}`;
  return d;
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
    'reg-R0', 'reg-R1', 'reg-R2', 'reg-R3',
    'alu-shape', 'dekodovani-box', 'cu-box', 'cpu-outer',
    'ri-row', 'pc-row', 'sreg-box',
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

  if (!alu || !dek || !cu || !cpuOuter || !ri || !pc || !sreg) return null;

  const aluTop = alu.top;
  const aluBot = alu.top + alu.height;
  const aluL   = alu.left;
  const aluW   = alu.width;

  const busAboveAlu = aluTop - 10;

  const gapL  = dek.left + dek.width;
  const gapR  = cu.left;
  const laneA = gapL + (gapR - gapL) * 0.28;
  const laneB = gapL + (gapR - gapL) * 0.72;

  const lines: Line[] = [];

  // 1. Registers → ALU top (blue) — one connection type per register
  const regFracs = [0.15, 0.38, 0.62, 0.85];
  (['R0', 'R1', 'R2', 'R3'] as const).forEach((name, i) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx = midX(reg);
    const ry = reg.top + reg.height;
    const tx = aluL + aluW * regFracs[i];
    lines.push({ d: vh(rx, ry, tx, busAboveAlu) + ` V ${aluTop}`, color: C.reg, type: `reg-${name}-alu` as ConnectionType });
  });

  // 2. Dekodovani → ALU bottom-left (orange)
  {
    const ent = aluL + aluW * 0.25;
    lines.push({ d: hv(dek.left + dek.width, dek.top + dek.height * 0.25, ent, aluBot), color: C.dekod, type: 'dek-alu' });
  }

  // 3. Dekodovani → RI (orange)
  {
    const dy = midY(dek);
    const ry = midY(ri);
    lines.push({ d: hv(dek.left + dek.width, dy, laneA, ry, ri.left, ry), color: C.dekod, type: 'dek-ri' });
  }

  // 4. ALU → SREG (purple)
  {
    const sy = midY(sreg);
    lines.push({ d: `M ${laneB} ${aluBot} V ${sy} H ${sreg.left}`, color: C.alu, type: 'alu-sreg' });
  }

  // 5. PC → ALU bottom-center (green)
  {
    const py   = midY(pc);
    const alcx = aluL + aluW * 0.5;
    lines.push({ d: hv(cu.left, py, alcx, aluBot), color: C.pc, type: 'pc-alu' });
  }

  // 6. PC → RAM row (green) — only when the PC-addressed row exists in RAM
  if (pcRow) {
    const py   = midY(pc);
    const rry  = midY(pcRow);
    const cpuR = cpuOuter.left + cpuOuter.width;
    const gapX = cpuR + (pcRow.left - cpuR) / 2;
    lines.push({ d: hv(pc.left + pc.width, py, gapX, rry, pcRow.left, rry), color: C.pc, type: 'pc-ram' });
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
            opacity={active ? 1 : 0.15}
            style={active ? { animation: 'flowDash 0.5s linear infinite' } : undefined}
          />
        );
      })}
    </svg>
  );
}
