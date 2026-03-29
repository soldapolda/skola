import type {
  EmulatorState, DecodedInstruction, StatusFlags, FlashWord, Instruction,
} from '../types';

// ATmega2560 data-memory addresses
export const ADDR_PINK  = 0x106;
export const ADDR_PORTF = 0x111;
export const ADDR_DDRF  = 0x110;

const BLANK_SREG: StatusFlags = { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 0, C: 0 };

function instrWordCount(instr: Instruction): 1 | 2 {
  return (instr.op === 'JMP' || instr.op === 'LDS') ? 2 : 1;
}

// ── Fetch: find and decode the instruction at pc ──────────────────────────────

function decode(flash: FlashWord[], pc: number): DecodedInstruction | null {
  const word = flash.find(w => w.address === pc && !w.isSecondWord);
  if (!word) return null;
  return {
    instr:       word.instr,
    label:       word.label,
    hex:         word.hex,
    wordAddress: pc,
    wordCount:   instrWordCount(word.instr),
  };
}

// ── Execute: compute result without writing back ──────────────────────────────

function executeStep(
  state: EmulatorState,
  decoded: DecodedInstruction,
): DecodedInstruction {
  const { instr } = decoded;
  const regs = state.registers;

  switch (instr.op) {
    case 'LDI':
      return { ...decoded, result: instr.k };

    case 'INC': {
      const val = (regs[instr.rd] + 1) & 0xFF;
      const v   = regs[instr.rd] === 0x7F ? 1 : 0;
      const n   = (val >> 7) & 1;
      return {
        ...decoded,
        result:   val,
        newSreg: { ...state.sreg, V: v, N: n, S: n ^ v, Z: val === 0 ? 1 : 0 },
      };
    }

    case 'DEC': {
      const val = (regs[instr.rd] - 1 + 256) & 0xFF;
      const v   = regs[instr.rd] === 0x80 ? 1 : 0;
      const n   = (val >> 7) & 1;
      return {
        ...decoded,
        result:   val,
        newSreg: { ...state.sreg, V: v, N: n, S: n ^ v, Z: val === 0 ? 1 : 0 },
      };
    }

    case 'LDS': {
      const val = instr.addr === ADDR_PINK ? state.pink : 0xFF;
      return { ...decoded, result: val };
    }

    case 'OUT':
      return { ...decoded, result: regs[instr.rr] };

    case 'SBRC':
      return { ...decoded, skip: ((regs[instr.rr] >> instr.bit) & 1) === 0 };

    case 'RJMP':
    case 'JMP':
      return { ...decoded, jumpTarget: instr.target };

    default:
      return decoded;
  }
}

// ── Writeback: commit result, advance PC, return next state ───────────────────

function commit(state: EmulatorState, decoded: DecodedInstruction): EmulatorState {
  const regs = [...state.registers];
  let portF = state.portF;
  let ddrF  = state.ddrF;
  let sreg  = decoded.newSreg ?? state.sreg;
  let newPc = state.pc + decoded.wordCount;
  let lastWrittenReg: number | undefined;
  let lastWrittenPort: 'PORTF' | 'DDRF' | undefined;
  const lastWrittenSreg = decoded.newSreg != null;

  const { instr } = decoded;

  if (instr.op === 'LDI' || instr.op === 'INC' || instr.op === 'DEC' || instr.op === 'LDS') {
    regs[instr.rd] = decoded.result!;
    lastWrittenReg = instr.rd;
  } else if (instr.op === 'OUT') {
    if (instr.port === 'PORTF') {
      portF = decoded.result!;
      lastWrittenPort = 'PORTF';
    } else {
      ddrF = decoded.result!;
      lastWrittenPort = 'DDRF';
    }
  } else if (instr.op === 'SBRC' && decoded.skip) {
    // Skip the next instruction; determine its word count to skip correctly
    const nextPc   = state.pc + decoded.wordCount;
    const nextWord = state.flash.find(w => w.address === nextPc && !w.isSecondWord);
    const nextCount = nextWord ? instrWordCount(nextWord.instr) : 1;
    newPc = nextPc + nextCount;
  } else if (instr.op === 'RJMP' || instr.op === 'JMP') {
    newPc = decoded.jumpTarget!;
  }

  return {
    ...state,
    phase:            'fetch',
    pc:               newPc,
    registers:        regs,
    portF,
    ddrF,
    sreg,
    currentInstruction: null,
    flightKey:        state.flightKey + 1,
    lastWrittenReg,
    lastWrittenPort,
    lastWrittenSreg,
  };
}

// ── Public API ────────────────────────────────────────────────────────────────

/** Advance the emulator by one sub-step (fetch → execute → fetch …). */
export function stepEmulator(state: EmulatorState): EmulatorState {
  switch (state.phase) {
    case 'fetch': {
      const decoded = decode(state.flash, state.pc);
      if (!decoded) return state;
      return {
        ...state,
        phase:              'execute',
        currentInstruction: decoded,
        lastWrittenReg:     undefined,
        lastWrittenPort:    undefined,
        lastWrittenSreg:    undefined,
      };
    }

    case 'execute': {
      if (!state.currentInstruction) return { ...state, phase: 'fetch' };
      // Compute result then immediately commit (single execute phase)
      return commit(state, executeStep(state, state.currentInstruction));
    }
  }
}

/** Create a fresh emulator state from a flash image. */
export function resetEmulator(flash: FlashWord[], pink = 0xFF): EmulatorState {
  return {
    phase:              'fetch',
    pc:                 0,
    registers:          new Array(32).fill(0),
    portF:              0,
    ddrF:               0,
    ddrK:               0,
    pink,
    sreg:               { ...BLANK_SREG },
    flash,
    currentInstruction: null,
    flightKey:          0,
  };
}
