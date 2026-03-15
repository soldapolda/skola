export type ConnectionType =
  | 'reg-R0-alu' | 'reg-R1-alu' | 'reg-R2-alu' | 'reg-R3-alu'
  | 'dek-alu' | 'dek-ri' | 'alu-sreg' | 'pc-alu' | 'pc-ram';

export interface FlightDef {
  fromId: string;   // source element ID (use 'ram-row-pc' as sentinel for PC-addressed row)
  toId:   string;   // destination element ID
  value:  string;   // text shown in the flying packet
}

export interface CpuStepDef {
  label: string;
  activeFields:  Array<'ir' | 'pc' | 'sreg'>;
  activeAlu:     boolean;
  activeDek:     boolean;
  activeRamRow:  boolean;           // highlight the PC-addressed RAM row
  activeConnections: ConnectionType[];
  // one-shot animations
  animateIr?:   boolean;
  animatePc?:   boolean;
  animateDekod?: boolean;
  animateR0?:   boolean;
  // flying value transition
  flight?: FlightDef;
  // what each field shows at this step
  displayPc:       string;
  displayIr:       string;
  displayOpcode:   string;
  displayOperands: string;
  displayR0:       string;
  displayFlags:    boolean;         // false = all zeros
  // which registers to highlight (amber pulse)
  activeRegisters: string[];
}

export const CPU_STEPS: CpuStepDef[] = [
  // 0 — blank slate
  {
    label: '', activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    displayPc: '—', displayIr: '—', displayOpcode: '', displayOperands: '', displayR0: '—', displayFlags: false,
  },
  // 1 — PC → RAM
  {
    label: 'PC ukazuje na adresu instrukce',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x01', displayIr: '—', displayOpcode: '', displayOperands: '', displayR0: '—', displayFlags: false,
  },
  // 2 — instruction loaded into IR
  {
    label: 'Instrukce načtena do registru instrukce (RI)',
    activeFields: ['ir'], activeAlu: false, activeDek: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x2017' },
    displayPc: '0x01', displayIr: '0x2017', displayOpcode: '', displayOperands: '', displayR0: '—', displayFlags: false,
  },
  // 3 — PC incremented (no connection, just animation)
  {
    label: 'Čítač programu se zvýší o 1',
    activeFields: ['pc'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x02', displayIr: '0x2017', displayOpcode: '', displayOperands: '', displayR0: '—', displayFlags: false,
  },
  // 4 — decode: only Dekodovani ↔ RI shines
  {
    label: 'Identifikace operace a operandů',
    activeFields: ['ir'], activeAlu: false, activeDek: true,
    activeRamRow: false, activeConnections: ['dek-ri'], activeRegisters: [],
    animateDekod: true,
    flight: { fromId: 'ri-row', toId: 'dekodovani-box', value: '0x2017' },
    displayPc: '0x02', displayIr: '0x2017', displayOpcode: 'LD', displayOperands: 'R0, 0x09', displayR0: '—', displayFlags: false,
  },
  // 5 — ALU executes: only R0 connection shines
  {
    label: 'ALU provede operaci',
    activeFields: [], activeAlu: true, activeDek: false,
    activeRamRow: false, activeConnections: ['reg-R0-alu', 'dek-alu'], activeRegisters: ['R0'],
    displayPc: '0x02', displayIr: '0x2017', displayOpcode: 'LD', displayOperands: 'R0, 0x09', displayR0: '—', displayFlags: false,
  },
  // 6 — write result to Rd
  {
    label: 'Výsledek zapsán do registru Rd',
    activeFields: [], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animateR0: true,
    displayPc: '0x02', displayIr: '0x2017', displayOpcode: 'LD', displayOperands: 'R0, 0x09', displayR0: '0x09', displayFlags: false,
  },
  // 7 — update SREG
  {
    label: 'Aktualizace příznaků SREG',
    activeFields: ['sreg'], activeAlu: false, activeDek: false,
    activeRamRow: false, activeConnections: ['alu-sreg'], activeRegisters: [],
    displayPc: '0x02', displayIr: '0x2017', displayOpcode: 'LD', displayOperands: 'R0, 0x09', displayR0: '0x09', displayFlags: true,
  },
];

export const MAX_CPU_STEP = CPU_STEPS.length - 1; // 7
