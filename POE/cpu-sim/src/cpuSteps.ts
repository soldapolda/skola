export type ConnectionType =
  | 'reg-R0-alu' | 'reg-R1-alu' | 'reg-R2-alu' | 'reg-R3-alu'
  | 'dek-alu' | 'dek-ri' | 'alu-sreg' | 'pc-alu' | 'pc-ram';

export interface FlightDef {
  fromId: string;   // source element ID; 'ram-row-pc' = sentinel for current PC row
  toId:   string;   // destination element ID
  value:  string;   // text shown in the flying packet
}

export interface CpuStepDef {
  label: string;
  activeFields:  Array<'ir' | 'pc' | 'sreg'>;
  activeAlu:     boolean;
  activeDek:     boolean;
  activeRamRow:  boolean;
  activeConnections: ConnectionType[];
  // one-shot animations
  animateIr?:    boolean;
  animatePc?:    boolean;
  animateDekod?: boolean;
  animateR0?:    boolean;
  animateR1?:    boolean;
  // flying value transition
  flight?: FlightDef;
  // what each field shows at this step
  displayPc:       string;
  displayIr:       string;
  displayOpcode:   string;
  displayOperands: string;
  displayR0:       string;
  displayR1:       string;
  displayFlags:    boolean;
  // which registers to highlight (amber pulse)
  activeRegisters: string[];
}

export const CPU_STEPS: CpuStepDef[] = [
  // ── 0 — blank slate ────────────────────────────────────────────────────────
  {
    label: '', activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    displayPc: '0x00', displayIr: '—', displayOpcode: '', displayOperands: '',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // ══ Instrukce 1: LDI R0, 0x9F ══════════════════════════════════════════════

  // 1 — PC → RAM (fetch address)
  {
    label: 'LDI R0, 0x9F — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x00', displayIr: '—', displayOpcode: '', displayOperands: '',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // 2 — instruction fetched into IR
  {
    label: 'LDI R0, 0x9F — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE09F' },
    displayPc: '0x00', displayIr: '0xE09F', displayOpcode: '', displayOperands: '',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // 3 — PC++
  {
    label: 'LDI R0, 0x9F — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: '', displayOperands: '',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // 4 — decode
  {
    label: 'LDI R0, 0x9F — dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0xE09F' },
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // 5 — ALU execute
  {
    label: 'LDI R0, 0x9F — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['dek-alu'], activeRegisters: [],
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '—', displayR1: '—', displayFlags: false,
  },

  // 6 — write result to R0
  {
    label: 'LDI R0, 0x9F — výsledek zapsán do R0',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R0'],
    animateR0: true,
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // ══ Instrukce 2: LDI R1, 0xA0 ══════════════════════════════════════════════

  // 7 — PC → RAM
  {
    label: 'LDI R1, 0xA0 — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // 8 — instruction fetched into IR
  {
    label: 'LDI R1, 0xA0 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE1A0' },
    displayPc: '0x01', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // 9 — PC++
  {
    label: 'LDI R1, 0xA0 — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R0, 0x9F',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // 10 — decode
  {
    label: 'LDI R1, 0xA0 — dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0xE1A0' },
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // 11 — ALU execute
  {
    label: 'LDI R1, 0xA0 — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['dek-alu'], activeRegisters: [],
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '—', displayFlags: false,
  },

  // 12 — write result to R1
  {
    label: 'LDI R1, 0xA0 — výsledek zapsán do R1',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R1'],
    animateR1: true,
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // ══ Instrukce 3: ADD R0, R1 ═════════════════════════════════════════════════

  // 13 — PC → RAM
  {
    label: 'ADD R0, R1 — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // 14 — instruction fetched into IR
  {
    label: 'ADD R0, R1 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x0C01' },
    displayPc: '0x02', displayIr: '0x0C01', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // 15 — PC++
  {
    label: 'ADD R0, R1 — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'LDI', displayOperands: 'R1, 0xA0',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // 16 — decode
  {
    label: 'ADD R0, R1 — dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0x0C01' },
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R0, R1',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // 17 — ALU adds R0 + R1
  {
    label: 'ADD R0, R1 — ALU sečte 0x9F + 0xA0 = 0x3F',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['reg-R0-alu', 'reg-R1-alu', 'dek-alu'],
    activeRegisters: ['R0', 'R1'],
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R0, R1',
    displayR0: '0x9F', displayR1: '0xA0', displayFlags: false,
  },

  // 18 — write result 0x3F to R0
  {
    label: 'ADD R0, R1 — výsledek 0x3F zapsán do R0',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R0'],
    animateR0: true,
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R0, R1',
    displayR0: '0x3F', displayR1: '0xA0', displayFlags: false,
  },

  // 19 — update SREG (C=1, V=1, S=1 — signed overflow from 0x9F + 0xA0)
  {
    label: 'ADD R0, R1 — aktualizace příznaků SREG',
    activeFields: ['sreg'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: ['alu-sreg'], activeRegisters: [],
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R0, R1',
    displayR0: '0x3F', displayR1: '0xA0', displayFlags: true,
  },
];

export const MAX_CPU_STEP = CPU_STEPS.length - 1; // 19
