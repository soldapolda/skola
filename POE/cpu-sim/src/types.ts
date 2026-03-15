export interface Register {
  name: string;
  value: string;
}

export interface StatusFlags {
  I: number; T: number; H: number; S: number;
  V: number; N: number; Z: number; C: number;
}

export interface ControlUnit {
  ir: string;   // instruction register
  pc: string;   // program counter
  flags: StatusFlags;
}

export interface DecodedInstruction {
  raw: string;      // e.g. "LD R0, 0x09"
  opcode: string;   // e.g. "LD"
  operands: string; // e.g. "R0, 0x09"
}

export interface RamRow {
  address: string;
  data: string;
  highlighted?: boolean;
}

export interface CpuState {
  registers: Register[];
  controlUnit: ControlUnit;
  decoded: DecodedInstruction;
  ram: RamRow[];
}
