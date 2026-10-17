export interface Register {
  name: string;
  value: string; // hex display string e.g. '0xFF'
}

export interface StatusFlags {
  I: number; T: number; H: number; S: number;
  V: number; N: number; Z: number; C: number;
}

export type ExecPhase = 'fetch' | 'execute';

export type Instruction =
  | { op: 'JMP';  target: number }
  | { op: 'LDI';  rd: number; k: number }
  | { op: 'OUT';  port: 'PORTF' | 'DDRF'; rr: number }
  | { op: 'LDS';  rd: number; addr: number }
  | { op: 'INC';  rd: number }
  | { op: 'DEC';  rd: number }
  | { op: 'SBRC'; rr: number; bit: number }
  | { op: 'RJMP'; target: number }
  | { op: 'WORD'; value: number }; // second word of 32-bit instruction

export interface FlashWord {
  address: number;        // word address (0-based)
  hex: string;            // representative opcode hex e.g. '0x940C'
  label: string;          // human-readable e.g. 'JMP Program'
  loopLabel?: string;     // assembly label marker e.g. 'reset:', 'main:'
  isSecondWord?: boolean; // true for second word of JMP / LDS
  instr: Instruction;
}

export type ConnectionType =
  | 'reg-R16-alu' | 'reg-R17-alu' | 'reg-R18-alu' | 'reg-R19-alu'
  | 'reg-R20-alu' | 'reg-R21-alu' | 'reg-R22-alu' | 'reg-R23-alu'
  | 'alu-sreg' | 'pc-ram' | 'portf-out' | 'pink-in';

export interface DecodedInstruction {
  instr: Instruction;
  label: string;          // e.g. 'LDI R16, 0xFF'
  hex: string;            // hex for the flying value packet
  wordAddress: number;    // PC at fetch time
  wordCount: 1 | 2;
  // Filled during execute phase:
  result?: number;
  newSreg?: StatusFlags;
  skip?: boolean;         // SBRC: whether to skip next instruction
  jumpTarget?: number;    // JMP / RJMP: resolved target address
}

export interface EmulatorState {
  phase: ExecPhase;
  pc: number;             // current word address in Flash
  registers: number[];    // R0–R31 (indexed by register number)
  portF: number;          // PORTF output register value (0–255)
  ddrF: number;           // DDRF direction register value
  ddrK: number;           // DDRK direction register value (Port K)
  pink: number;           // PINK input register — active-low, default 0xFF
  sreg: StatusFlags;
  flash: FlashWord[];
  currentInstruction: DecodedInstruction | null;
  flightKey: number;      // increments each new fetch cycle to retrigger FlyingValue
  lastWrittenReg?: number;
  lastWrittenPort?: 'PORTF' | 'DDRF';
  lastWrittenSreg?: boolean;
}
