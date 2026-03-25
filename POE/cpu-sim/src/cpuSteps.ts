export type ConnectionType =
  | 'reg-R16-alu' | 'reg-R17-alu' | 'reg-R18-alu' | 'reg-R19-alu'
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
  animateR16?:   boolean;
  animateR17?:   boolean;
  // flying value transition
  flight?: FlightDef;
  // what each field shows at this step
  displayPc:       string;
  displayIr:       string;
  displayOpcode:   string;
  displayOperands: string;
  displayR16:      string;
  displayR17:      string;
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
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // ══ Instrukce 1: LDI R16, 0x9F ══════════════════════════════════════════════

  // 1 — PC → RAM (fetch address)
  {
    label: 'PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x00', displayIr: '—', displayOpcode: '', displayOperands: '',
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 2 — instruction fetched into IR
  {
    label: 'instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE09F' },
    displayPc: '0x00', displayIr: '0xE09F', displayOpcode: '', displayOperands: '',
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 3 — PC++
  {
    label: 'čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: '', displayOperands: '',
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 4 — decode
  {
    label: 'dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0xE09F' },
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 5 — ALU execute
  {
    label: 'ALU zpracuje instrukci',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['dek-alu'], activeRegisters: [],
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 6 — write result to R16
  {
    label: 'výsledek zapsán do R16',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R16'],
    animateR16: true,
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // ══ Instrukce 2: LDI R17, 0xA0 ══════════════════════════════════════════════

  // 7 — PC → RAM
  {
    label: 'PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x01', displayIr: '0xE09F', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 8 — instruction fetched into IR
  {
    label: 'instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE1A0' },
    displayPc: '0x01', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 9 — PC++
  {
    label: 'čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R16, 0x9F',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 10 — decode
  {
    label: 'dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0xE1A0' },
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 11 — ALU execute
  {
    label: 'ALU zpracuje instrukci',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['dek-alu'], activeRegisters: [],
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 12 — write result to R17
  {
    label: 'výsledek zapsán do R17',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // ══ Instrukce 3: ADD R16, R17 ═════════════════════════════════════════════════

  // 13 — PC → RAM
  {
    label: 'PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x02', displayIr: '0xE1A0', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 14 — instruction fetched into IR
  {
    label: 'instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x0C01' },
    displayPc: '0x02', displayIr: '0x0C01', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 15 — PC++
  {
    label: 'čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'LDI', displayOperands: 'R17, 0xA0',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 16 — decode
  {
    label: 'dekódování instrukce',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0x0C01' },
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R16, R17',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 17 — ALU adds R16 + R17
  {
    label: 'ALU sečte 0x9F + 0xA0 = 0x3F',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['reg-R16-alu', 'reg-R17-alu', 'dek-alu'],
    activeRegisters: ['R16', 'R17'],
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R16, R17',
    displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 18 — write result 0x3F to R16
  {
    label: 'výsledek 0x3F zapsán do R16',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R16'],
    animateR16: true,
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R16, R17',
    displayR16: '0x3F', displayR17: '0xA0', displayFlags: false,
  },

  // 19 — update SREG (C=1, V=1, S=1 — signed overflow from 0x9F + 0xA0)
  {
    label: 'aktualizace příznaků SREG',
    activeFields: ['sreg'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: ['alu-sreg'], activeRegisters: [],
    displayPc: '0x03', displayIr: '0x0C01', displayOpcode: 'ADD', displayOperands: 'R16, R17',
    displayR16: '0x3F', displayR17: '0xA0', displayFlags: true,
  },
];

export const MAX_CPU_STEP = CPU_STEPS.length - 1; // 19
