# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev      # Start development server (Vite + HMR)
npm run build    # TypeScript type-check + production build
npm run lint     # ESLint
npm run preview  # Preview production build
npm run deploy   # Build + publish to GitHub Pages at POE/assembler-sim
```

No test suite is configured.

## Architecture

This is an **interactive AVR assembler simulator visualization** (`assembler-sim`) for educational purposes (Czech language UI). It renders a step-driven CPU state as a visual diagram with animated SVG connection lines. Navigation is via ← → arrow keys (17 steps total, 0–16).

### Data flow

```
src/data.ts (initialState: CpuState)
  → App.tsx  (keyboard nav: ←/→ controls cpuStep 0–16)
    → CpuSlide.tsx  (full-screen layout, derives display state from cpuStep)
        ├── Registers (top)  — R16–R19 above ALU
        ├── Alu              — trapezoid, 22vh, clip-path bottom spans only 25%–75%
        ├── Registers (bot)  — R20–R23 below ALU
        ├── ControlUnit      — RI (instruction text), PC, SREG flags — 32vw, bottom-right
        ├── Ram              — FLASH panel: address + human-readable instruction
        ├── Connections      — SVG overlay with color-coded data-flow lines
        └── FlyingValue      — animated packet flying between DOM elements
```

### Key types (`src/types.ts`)

- `CpuState` — `registers: Register[]`, `controlUnit: ControlUnit`, `ram: RamRow[]`
- `ControlUnit` — `ir: string`, `pc: string`, `flags: StatusFlags`
- `StatusFlags` — 8 AVR flags: I, T, H, S, V, N, Z, C
- `RamRow` — `address`, `data`, optional `label` (e.g. `"LDI R16, 0x9F"`), optional `highlighted`

### Step definitions (`src/cpuSteps.ts`)

`CPU_STEPS: CpuStepDef[]` — 17 entries (index 0 = blank slate, then 5 steps × 3 instructions).

Each instruction cycle: **Fetch → Load RI → PC++ → ALU execute → Write register** (+ SREG update on ADD).

Key `CpuStepDef` fields:
- `displayIr` — human-readable instruction string shown in RI (e.g. `'LDI R16, 0x9F'`) or `'—'`
- `displayPc`, `displayR16`, `displayR17`, `displayFlags`
- `activeConnections: ConnectionType[]` — which SVG lines animate as active
- `flight?: FlightDef` — triggers a flying value packet (carries raw hex opcode)
- `activeRegisters`, `activeFields`, `activeAlu`, `activeRamRow`

`ConnectionType` values: `reg-R16-alu` … `reg-R23-alu` | `ri-alu` | `alu-sreg` | `pc-ram`

### Flying value transitions (`src/components/FlyingValue.tsx`)

- Triggered by steps with a `flight` field; `'ram-row-pc'` sentinel resolves to `ram-row-${pc}` at runtime
- Packet carries the raw hex opcode (e.g. `0xE09F`); destination shows `'—'` while in-flight
- On arrival (`onTransitionEnd`): `dataReceive` animation plays on RI, which then shows the decoded instruction text
- `CpuSlide` tracks `arrivedSteps: Set<number>`; backward navigation clears future arrivals

### Connections (`src/components/Connections.tsx`)

Color-coded orthogonal SVG paths via `useElementRects` hook:

| Color  | Route |
|--------|-------|
| Blue   | R16–R19 → ALU top; R20–R23 → ALU bottom |
| Orange | RI → ALU bottom (via R21/R22 center lane) |
| Purple | ALU → SREG (via same R21/R22 center lane) |
| Green  | PC → FLASH row |

**Key routing rules:**
- Top fracs for R16–R19 on ALU top: `[0.13, 0.35, 0.65, 0.87]`
- Bottom fracs for R20–R23 on ALU bottom: `[0.28, 0.38, 0.62, 0.72]` — must stay within the 25%–75% trapezoid bottom edge
- `laneX` = midpoint between `reg-R21` right edge and `reg-R22` left edge — reserved vertical channel for RI and SREG lines
- Inactive connections render at `opacity: 0.10`

### Layout (`src/components/CpuSlide.tsx`)

`cpu-outer` is a `flex flex-col h-full` box. Children in order:
1. `Registers` — `registers.slice(0, 4)` (R16–R19)
2. `Alu`
3. `Registers` — `registers.slice(4, 8)` (R20–R23)
4. `ControlUnit` — wrapped in `{ marginTop: 'auto', justifyContent: 'flex-end' }` to pin to bottom-right

### Styling

Tailwind CSS 4 (`@tailwindcss/vite`). Layout in viewport units (`vw`/`vh`). Color palette: beige/brown CPU box, teal register cells, purple FLASH panel.
