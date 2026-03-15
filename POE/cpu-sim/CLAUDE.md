# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev      # Start development server (Vite + HMR)
npm run build    # TypeScript type-check + production build
npm run lint     # ESLint
npm run preview  # Preview production build
```

No test suite is configured.

## Architecture

This is an **interactive CPU simulator visualization** for educational purposes (Czech language UI). It renders a static or step-driven CPU state as a visual diagram with animated SVG connection lines.

### Data flow

```
src/data.ts (initialState: CpuState)
  → App.tsx
    → CpuSlide.tsx  (full-screen layout, passes slices of CpuState to children)
        ├── Registers     — R0–R3 register display
        ├── Alu           — trapezoid shape (decorative)
        ├── Dekodovani    — decoded instruction (opcode + operands)
        ├── ControlUnit   — IR, PC, and 8-bit SREG flags
        ├── Ram           — address/data memory table
        └── Connections   — SVG overlay drawing data-flow lines between the above
```

### Key types (`src/types.ts`)

- `CpuState` — root state: `registers`, `controlUnit`, `decoded`, `ram`
- `ControlUnit` — `ir`, `pc`, `flags: StatusFlags`
- `StatusFlags` — 8 CPU flags: I, T, H, S, V, N, Z, C
- `DecodedInstruction` — `raw`, `opcode`, `operands`
- `RamRow` — `address`, `data`, optional `highlighted`

### Connections component (`src/components/Connections.tsx`)

Draws color-coded SVG paths between components using measured DOM positions:
- Accepts a `containerRef` (the outer div) and `pcAddress` to highlight the active RAM row
- Uses `useElementRects` hook (`src/hooks/useElementRects.ts`) to get live bounding rects
- Paths are orthogonal; helper functions `hv()` / `vh()` produce SVG path `d` strings
- A "lane" system spaces parallel paths in the gap between Dekodovani and ControlUnit

Color coding: blue = registers→ALU, orange = decoded→ALU/IR, purple = ALU→SREG, green = PC→RAM.

### Styling

Tailwind CSS 4 (imported via `@tailwindcss/vite` plugin). Layout uses viewport units (`vw`/`vh`). Color palette: beige/brown CPU box, teal data boxes, purple RAM panel.
