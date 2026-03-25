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

export interface RamRow {
  address: string;
  data: string;
  label?: string;       // human-readable instruction, e.g. "LDI R16, 0x9F"
  highlighted?: boolean;
}

export interface CpuState {
  registers: Register[];
  controlUnit: ControlUnit;
  ram: RamRow[];
}
