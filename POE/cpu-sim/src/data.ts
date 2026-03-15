import type { CpuState } from './types';

export const initialState: CpuState = {
  registers: [
    { name: 'R0', value: '—' },
    { name: 'R1', value: '—' },
    { name: 'R2', value: '—' },
    { name: 'R3', value: '—' },
  ],
  controlUnit: {
    ir: '—',
    pc: '0x00',
    flags: { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 0, C: 0 },
  },
  decoded: {
    raw: '',
    opcode: '',
    operands: '',
  },
  ram: [
    { address: '0x00', data: '0xE09F' },   // LDI R0, 0x9F
    { address: '0x01', data: '0xE1A0' },   // LDI R1, 0xA0
    { address: '0x02', data: '0x0C01' },   // ADD R0, R1
  ],
};
