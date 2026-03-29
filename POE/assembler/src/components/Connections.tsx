import type { RefObject } from 'react';
import { useElementRects } from '../hooks/useElementRects';
import type { ConnectionType } from '../types';

// ── colours ───────────────────────────────────────────────────────────────────

const C = {
  reg:   '#3b82f6', // blue   — registers ↔ ALU
  alu:   '#a855f7', // purple — ALU → SREG
  pc:    '#22c55e', // green  — PC → FLASH
  portf: '#ef4444', // red    — CPU → PORTF
  pink:  '#f97316', // orange — PINK buttons → ALU
} as const;

const SW = 4;

// ── routing helpers ───────────────────────────────────────────────────────────

const midY = (r: DOMRect) => r.top  + r.height / 2;
const midX = (r: DOMRect) => r.left + r.width  / 2;
const botY = (r: DOMRect) => r.top  + r.height;
const topY = (r: DOMRect) => r.top;

function hv(x1: number, y1: number, x2: number, y2: number): string {
  return `M ${x1} ${y1} H ${x2} V ${y2}`;
}

// ── component ─────────────────────────────────────────────────────────────────

interface Props {
  containerRef: RefObject<HTMLDivElement | null>;
  pcAddress:    string;
  activeTypes:  ConnectionType[];
}

interface Line { d: string; color: string; type: ConnectionType }

export default function Connections({ containerRef, pcAddress, activeTypes }: Props) {
  const IDS = [
    'reg-R16', 'reg-R17', 'reg-R18', 'reg-R19',
    'reg-R20', 'reg-R21', 'reg-R22', 'reg-R23',
    'alu-shape', 'cu-box', 'cpu-outer',
    'pc-row', 'sreg-box',
    `ram-row-${pcAddress}`,
    'portf-panel',
    'pink-panel',
  ];

  const r = useElementRects(IDS, containerRef);

  const alu        = r['alu-shape'];
  const cu         = r['cu-box'];
  const cpuOuter   = r['cpu-outer'];
  const pc         = r['pc-row'];
  const sreg       = r['sreg-box'];
  const pcRow      = r[`ram-row-${pcAddress}`];
  const r21        = r['reg-R21'];
  const r22        = r['reg-R22'];
  const portfPanel = r['portf-panel'];
  const pinkPanel  = r['pink-panel'];

  if (!alu || !cu || !cpuOuter || !pc || !sreg) return null;

  const aluTop = alu.top;
  const aluBot = botY(alu);
  const aluL   = alu.left;
  const aluW   = alu.width;

  // Vertical lane between R21 and R22 — reserved channel for SREG lines
  const laneX = (r21 && r22)
    ? (r21.left + r21.width + r22.left) / 2
    : aluL + aluW * 0.5;

  const busTopRail    = aluTop - 10;
  const busBottomRail = aluBot  + 10;

  const lines: Line[] = [];

  // ── 1. Top registers (R16–R19) → ALU top (blue) ──────────────────────────
  const topFracs: Record<string, number> = {
    'R16': 0.13, 'R17': 0.35, 'R18': 0.65, 'R19': 0.87,
  };
  (['R16', 'R17', 'R18', 'R19'] as const).forEach((name) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx = midX(reg);
    const ry = botY(reg);
    const tx = aluL + aluW * topFracs[name];
    lines.push({
      d: `M ${rx} ${ry} V ${busTopRail} H ${tx} V ${aluTop}`,
      color: C.reg,
      type: `reg-${name}-alu` as ConnectionType,
    });
  });

  // ── 2. Bottom registers (R20–R23) → ALU bottom (blue) ────────────────────
  const botFracs: Record<string, number> = {
    'R20': 0.28, 'R21': 0.38, 'R22': 0.62, 'R23': 0.72,
  };
  (['R20', 'R21', 'R22', 'R23'] as const).forEach((name) => {
    const reg = r[`reg-${name}`];
    if (!reg) return;
    const rx = midX(reg);
    const ry = topY(reg);
    const tx = aluL + aluW * botFracs[name];
    lines.push({
      d: `M ${rx} ${ry} V ${busBottomRail} H ${tx} V ${aluBot}`,
      color: C.reg,
      type: `reg-${name}-alu` as ConnectionType,
    });
  });

  // ── 3. ALU → SREG (purple) — through R21/R22 lane ─────────────────────────
  {
    const sregY = midY(sreg);
    lines.push({
      d: `M ${laneX} ${aluBot} V ${sregY} H ${sreg.left}`,
      color: C.alu,
      type: 'alu-sreg',
    });
  }

  // ── 4. PC → FLASH row (green) ─────────────────────────────────────────────
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

  // ── 5. CPU → PORTF panel (red) ────────────────────────────────────────────
  if (portfPanel) {
    const r20   = r['reg-R20'];
    const srcY  = r20 ? midY(r20) : midY(alu);
    const dstY  = midY(portfPanel);
    const cpuR  = cpuOuter.left + cpuOuter.width;
    const gapX  = cpuR + (portfPanel.left - cpuR) / 2;
    lines.push({
      d: `M ${cpuR} ${srcY} H ${gapX} V ${dstY} H ${portfPanel.left}`,
      color: C.portf,
      type: 'portf-out',
    });
  }

  // ── 6. PINK buttons → ALU (orange) ────────────────────────────────────────
  if (pinkPanel) {
    const srcY  = midY(pinkPanel);
    const dstX  = aluL + aluW * 0.5; // centre of ALU top
    const cpuL  = cpuOuter.left;
    const gapX  = pinkPanel.left + pinkPanel.width + (cpuL - (pinkPanel.left + pinkPanel.width)) / 2;
    lines.push({
      d: `M ${pinkPanel.left + pinkPanel.width} ${srcY} H ${gapX} V ${busTopRail} H ${dstX} V ${aluTop}`,
      color: C.pink,
      type: 'pink-in',
    });
  }

  return (
    <svg style={{
      position: 'absolute', inset: 0,
      width: '100%', height: '100%',
      pointerEvents: 'none', overflow: 'visible',
    }}>
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
