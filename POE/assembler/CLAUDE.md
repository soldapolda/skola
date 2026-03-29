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

This is an **interactive AVR emulator visualization** (`assembler-sim`) for educational purposes (Czech language UI). It dynamically executes a hardcoded AVR program step-by-step with animated SVG connections and a flying-value packet. Navigation is via **Step button**, **→/Space** (advance), **←** (reset).

### Execution model

The emulator runs a 3-phase cycle driven by a single `stepEmulator()` function:

```
fetch  →  execute  →  writeback  →  fetch  →  …
```

- **Fetch**: PC highlights a Flash row; instruction packet flies from Flash → ALU.
- **Execute**: ALU activates; instruction result is computed (not yet applied).
- **Writeback**: Result committed to registers / PORTF / SREG; PC advances.

There is **no IR (Instruction Register)** — the instruction flies directly to the ALU.

### Default program (`src/data.ts`)

Interactive LED scanner controlled by two active-low PINK buttons:

```asm
.org 0
jmp Program           ; 0x00–0x01  (2-word JMP)
Program:
    ldi r16, 0xff     ; 0x02
    out DDRF, r16     ; 0x03
    ldi r17, 0x00     ; 0x04
reset:
    ldi r20, 0x00     ; 0x05
main:
    lds r18, PINK     ; 0x06–0x07  (2-word LDS, PINK = 0x106)
    sbrc r18, 0       ; 0x08  — skip RJMP if B0 pressed (bit=0)
    rjmp inc          ; 0x09
    dec r20           ; 0x0A
    rjmp update       ; 0x0B
inc:
    inc r20           ; 0x0C
update:
    out PORTF, r20    ; 0x0D
    sbrc r18, 1       ; 0x0E  — if B1 pressed, rjmp reset
    rjmp main         ; 0x0F
    rjmp reset        ; 0x10
```

### Supported instructions (`src/logic/emulator.ts`)

`LDI`, `OUT` (PORTF / DDRF), `LDS`, `INC`, `DEC`, `SBRC`, `RJMP`, `JMP`

32-bit (2-word) instructions: **JMP**, **LDS** — PC increments by 2 after these.

**SBRC skip logic**: on writeback, looks ahead at the next instruction's word count to skip the correct number of words.

### Data flow

```
App.tsx (EmulatorState + stepEmulator / resetEmulator)
  → CpuSlide.tsx  (derives all display props from EmulatorState)
      ├── PortPanel        — PORTF LEDs (top-left)
      ├── ButtonPanel      — PINK buttons, active-low (top-left, id=pink-panel)
      ├── Registers (top)  — R16–R19 above ALU
      ├── Alu              — trapezoid, id=alu-shape; lit during execute
      ├── Registers (bot)  — R20–R23 below ALU
      ├── ControlUnit      — PC + SREG only (IR removed)
      ├── Ram              — FLASH panel showing FlashWord[] (second words dimmed)
      ├── Connections      — SVG overlay with color-coded data-flow lines
      └── FlyingValue      — packet from Flash row → alu-shape during fetch
```

### Key types (`src/types.ts`)

- `EmulatorState` — `phase`, `pc`, `registers[32]`, `portF`, `ddrF`, `pink`, `sreg`, `flash`, `currentInstruction`, `flightKey`
- `ExecPhase` — `'fetch' | 'execute' | 'writeback'`
- `Instruction` — discriminated union: `LDI | OUT | LDS | INC | DEC | SBRC | RJMP | JMP | WORD`
- `FlashWord` — `address`, `hex`, `label`, `loopLabel?`, `isSecondWord?`, `instr`
- `DecodedInstruction` — fetched+executed instruction carrying `result`, `newSreg`, `skip`, `jumpTarget`
- `ConnectionType` — SVG bus lines; `reg-RXX-alu | alu-sreg | pc-ram | portf-out | pink-in`

### PINK register

- Data memory address `0x106` (ATmega2560 Port K input)
- **Active-low**: default `0xFF` (all bits 1 = all buttons released)
- Pressing a button in ButtonPanel toggles the corresponding bit to `0`
- Read by `LDS R18, PINK` at runtime; bit tests via `SBRC`

### Connections (`src/components/Connections.tsx`)

Color-coded orthogonal SVG paths via `useElementRects` hook:

| Color  | Route |
|--------|-------|
| Blue   | R16–R19 → ALU top; R20–R23 → ALU bottom |
| Orange | PINK buttons → ALU top (via cpu-outer left edge) |
| Purple | ALU → SREG (via R21/R22 center lane) |
| Green  | PC → FLASH row |
| Red    | CPU → PORTF panel |

`laneX` = midpoint between `reg-R21` right and `reg-R22` left — reserved for SREG line.

### Flying value (`src/components/FlyingValue.tsx`)

- Source: `ram-row-${hexPc}` (the Flash row at the current PC)
- Destination: `alu-shape`
- Triggered by `flightKey` (increments in `resetEmulator` → `commit`)
- Visible only during `phase === 'fetch'`; unmounts when phase advances

### Layout (`src/components/CpuSlide.tsx`)

Left column (`flex-[3]`):
1. Top panels row: `PortPanel` + `ButtonPanel` (side by side)
2. `cpu-outer` flex-col: Registers(top) → ALU → Registers(bot) → ControlUnit(bottom-right)

Right column (`flex-1`): `Ram` (FLASH panel)

Phase badge (top-left) + step label (bottom-centre) + Step/Reset buttons (bottom-right).

### Styling

Tailwind CSS 4 (`@tailwindcss/vite`). Layout in viewport units (`vw`/`vh`). Color palette: beige/brown CPU box, teal register cells, purple FLASH panel.
