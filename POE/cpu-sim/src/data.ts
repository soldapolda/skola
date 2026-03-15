import type { CpuState } from './types';

export const initialState: CpuState = {
  registers: [
    { name: 'R0', value: '0x17' },
    { name: 'R1', value: '0x00' },
    { name: 'R2', value: '0x00' },
    { name: 'R3', value: '0x00' },
  ],
  controlUnit: {
    ir: '0x2017',
    pc: '0x0042',
    flags: { I: 0, T: 0, H: 0, S: 0, V: 0, N: 1, Z: 0, C: 0 },
  },
  decoded: {
    raw: 'LD R0, 0x09',
  },
  ram: [
    { address: '0x00', data: '0x2017' },
    { address: '0x01', data: '0x21FF', highlighted: true },
    { address: '0x02', data: '0x9508' },
    { address: '0x03', data: '0x0000' },
    { address: '0x04', data: '0x0000' },
  ],
};
