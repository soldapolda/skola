import type { CpuState } from './types';

export const initialState: CpuState = {
  registers: [
    { name: 'R16', value: '—' },
    { name: 'R17', value: '—' },
    { name: 'R18', value: '—' },
    { name: 'R19', value: '—' },
    { name: 'R20', value: '—' },
    { name: 'R21', value: '—' },
    { name: 'R22', value: '—' },
    { name: 'R23', value: '—' },
  ],
  controlUnit: {
    ir: '—',
    pc: '0x00',
    flags: { I: 0, T: 0, H: 0, S: 0, V: 0, N: 0, Z: 0, C: 0 },
  },
  ram: [
    { address: '0x00', data: '0x940C', label: 'JMP Program' },
    { address: '0x01', data: '0xEF0F', label: 'LDI R16, 0xFF' },
    { address: '0x02', data: '0x9300', label: 'STS DDRF, R16' },
    { address: '0x03', data: '0xE001', label: 'LDI R17, 0x01' },
    { address: '0x04', data: '0x9310', label: 'STS PORTF, R17',  loopLabel: 'loop:' },
    { address: '0x05', data: '0xEF2F', label: 'LDI R18, 0xFF' },
    { address: '0x06', data: '0x952A', label: 'DEC R18',          loopLabel: 'for_loop:' },
    { address: '0x07', data: '0xF7E1', label: 'BRNE for_loop' },
    { address: '0x08', data: '0x0F11', label: 'LSL R17' },
    { address: '0x09', data: '0x2011', label: 'TST R17' },
    { address: '0x0A', data: '0xF411', label: 'BRNE skip_reset' },
    { address: '0x0B', data: '0xE001', label: 'LDI R17, 0x01' },
    { address: '0x0C', data: '0xCFF3', label: 'RJMP loop',        loopLabel: 'skip_reset:' },
  ],
  portF: '0x00',
};
