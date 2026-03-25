export type ConnectionType =
  | 'reg-R16-alu' | 'reg-R17-alu' | 'reg-R18-alu' | 'reg-R19-alu'
  | 'reg-R20-alu' | 'reg-R21-alu' | 'reg-R22-alu' | 'reg-R23-alu'
  | 'ri-alu' | 'alu-sreg' | 'pc-ram';

export interface FlightDef {
  fromId: string;   // source element ID; 'ram-row-pc' = sentinel for current PC row
  toId:   string;   // destination element ID
  value:  string;   // text shown in the flying packet
}

export interface CpuStepDef {
  label: string;
  activeFields:  Array<'ir' | 'pc' | 'sreg'>;
  activeAlu:     boolean;
  activeRamRow:  boolean;
  activeConnections: ConnectionType[];
  // one-shot animations
  animateIr?:    boolean;
  animatePc?:    boolean;
  animateR16?:   boolean;
  animateR17?:   boolean;
  // flying value transition
  flight?: FlightDef;
  // what each field shows at this step
  displayPc:    string;
  displayIr:    string;   // human-readable instruction or '—'
  displayR16:   string;
  displayR17:   string;
  displayFlags: boolean;
  // which registers to highlight (amber pulse)
  activeRegisters: string[];
}

export const CPU_STEPS: CpuStepDef[] = [
  // ── 0 — blank slate ────────────────────────────────────────────────────────
  {
    label: '', activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    displayPc: '0x00', displayIr: '—', displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // ══ Instrukce 1: LDI R16, 0x9F ══════════════════════════════════════════════

  // 1 — PC → FLASH (fetch address)
  {
    label: 'LDI R16, 0x9F — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x00', displayIr: '—', displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 2 — instruction fetched into RI
  {
    label: 'LDI R16, 0x9F — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE09F' },
    displayPc: '0x00', displayIr: 'LDI R16, 0x9F', displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 3 — PC++
  {
    label: 'LDI R16, 0x9F — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x01', displayIr: 'LDI R16, 0x9F', displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 4 — ALU execute
  {
    label: 'LDI R16, 0x9F — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['ri-alu'], activeRegisters: [],
    displayPc: '0x01', displayIr: 'LDI R16, 0x9F', displayR16: '—', displayR17: '—', displayFlags: false,
  },

  // 5 — write result to R16
  {
    label: 'LDI R16, 0x9F — výsledek zapsán do R16',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R16'],
    animateR16: true,
    displayPc: '0x01', displayIr: 'LDI R16, 0x9F', displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // ══ Instrukce 2: LDI R17, 0xA0 ══════════════════════════════════════════════

  // 6 — PC → FLASH
  {
    label: 'LDI R17, 0xA0 — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x01', displayIr: 'LDI R16, 0x9F', displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 7 — instruction fetched into RI
  {
    label: 'LDI R17, 0xA0 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE1A0' },
    displayPc: '0x01', displayIr: 'LDI R17, 0xA0', displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 8 — PC++
  {
    label: 'LDI R17, 0xA0 — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x02', displayIr: 'LDI R17, 0xA0', displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 9 — ALU execute
  {
    label: 'LDI R17, 0xA0 — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['ri-alu'], activeRegisters: [],
    displayPc: '0x02', displayIr: 'LDI R17, 0xA0', displayR16: '0x9F', displayR17: '—', displayFlags: false,
  },

  // 10 — write result to R17
  {
    label: 'LDI R17, 0xA0 — výsledek zapsán do R17',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x02', displayIr: 'LDI R17, 0xA0', displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // ══ Instrukce 3: ADD R16, R17 ═════════════════════════════════════════════════

  // 11 — PC → FLASH
  {
    label: 'ADD R16, R17 — PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x02', displayIr: 'LDI R17, 0xA0', displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 12 — instruction fetched into RI
  {
    label: 'ADD R16, R17 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x0C01' },
    displayPc: '0x02', displayIr: 'ADD R16, R17', displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 13 — PC++
  {
    label: 'ADD R16, R17 — čítač programu se zvýší',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x03', displayIr: 'ADD R16, R17', displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 14 — ALU adds R16 + R17
  {
    label: 'ADD R16, R17 — ALU sečte 0x9F + 0xA0 = 0x3F',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R16-alu', 'reg-R17-alu', 'ri-alu'],
    activeRegisters: ['R16', 'R17'],
    displayPc: '0x03', displayIr: 'ADD R16, R17', displayR16: '0x9F', displayR17: '0xA0', displayFlags: false,
  },

  // 15 — write result 0x3F to R16
  {
    label: 'ADD R16, R17 — výsledek 0x3F zapsán do R16',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R16'],
    animateR16: true,
    displayPc: '0x03', displayIr: 'ADD R16, R17', displayR16: '0x3F', displayR17: '0xA0', displayFlags: false,
  },

  // 16 — update SREG
  {
    label: 'ADD R16, R17 — aktualizace příznaků SREG',
    activeFields: ['sreg'], activeAlu: false,
    activeRamRow: false, activeConnections: ['alu-sreg'], activeRegisters: [],
    displayPc: '0x03', displayIr: 'ADD R16, R17', displayR16: '0x3F', displayR17: '0xA0', displayFlags: true,
  },
];

export const MAX_CPU_STEP = CPU_STEPS.length - 1; // 16
