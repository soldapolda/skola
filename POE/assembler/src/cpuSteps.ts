export type ConnectionType =
  | 'reg-R16-alu' | 'reg-R17-alu' | 'reg-R18-alu' | 'reg-R19-alu'
  | 'reg-R20-alu' | 'reg-R21-alu' | 'reg-R22-alu' | 'reg-R23-alu'
  | 'ri-alu' | 'alu-sreg' | 'pc-ram' | 'portf-out';

export interface FlightDef {
  fromId: string;
  toId:   string;
  value:  string;
}

export interface CpuStepDef {
  label: string;
  activeFields:      Array<'ir' | 'pc' | 'sreg'>;
  activeAlu:         boolean;
  activeRamRow:      boolean;
  activeConnections: ConnectionType[];
  animateIr?:        boolean;
  animatePc?:        boolean;
  animateR16?:       boolean;
  animateR17?:       boolean;
  animateR18?:       boolean;
  animatePortF?:     boolean;
  flight?:           FlightDef;
  displayPc:         string;
  displayIr:         string;
  displayR16:        string;
  displayR17:        string;
  displayR18:        string;
  displayPortF:      string;
  displayFlags:      boolean;
  displayFlagZ?:     boolean;
  activeRegisters:   string[];
  activePortF?:      boolean;
}

export const CPU_STEPS: CpuStepDef[] = [
  // ── 0 — blank slate ────────────────────────────────────────────────────────
  {
    label: '', activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    displayPc: '0x00', displayIr: '—',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // ══ JMP Program ══════════════════════════════════════════════════════════════

  // 1 — PC → FLASH
  {
    label: 'JMP Program — PC ukazuje na instrukci',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x00', displayIr: '—',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 2 — JMP fetched into RI
  {
    label: 'JMP Program — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x940C' },
    displayPc: '0x00', displayIr: 'JMP Program',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 3 — JMP executed: PC jumps to 0x01
  {
    label: 'JMP Program — skok: PC = 0x01 (Program)',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x01', displayIr: 'JMP Program',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // ══ LDI R16, 0xFF ════════════════════════════════════════════════════════════

  // 4 — PC → FLASH
  {
    label: 'LDI R16, 0xFF — PC ukazuje na instrukci',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x01', displayIr: 'JMP Program',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 5 — LDI R16 fetched into RI
  {
    label: 'LDI R16, 0xFF — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xEF0F' },
    displayPc: '0x01', displayIr: 'LDI R16, 0xFF',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 6 — PC++
  {
    label: 'LDI R16, 0xFF — čítač programu zvýšen',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x02', displayIr: 'LDI R16, 0xFF',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 7 — ALU execute
  {
    label: 'LDI R16, 0xFF — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['ri-alu'], activeRegisters: [],
    displayPc: '0x02', displayIr: 'LDI R16, 0xFF',
    displayR16: '—', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 8 — R16 = 0xFF
  {
    label: 'LDI R16, 0xFF — výsledek zapsán: R16 = 0xFF',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R16'],
    animateR16: true,
    displayPc: '0x02', displayIr: 'LDI R16, 0xFF',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // ══ STS DDRF, R16 — DDRF ════════════════════════════════════════════════════

  // 9 — PC → FLASH
  {
    label: 'STS DDRF, R16 — nastavení DDRF (port F jako výstup)',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x02', displayIr: 'LDI R16, 0xFF',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 10 — STS fetched + PC++ + execute (compressed)
  {
    label: 'STS DDRF, R16 — DDRF = 0xFF: všechny piny portu F jsou výstupy',
    activeFields: ['ir', 'pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram', 'reg-R16-alu'], activeRegisters: ['R16'],
    animatePc: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x9300' },
    displayPc: '0x03', displayIr: 'STS DDRF, R16',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // ══ LDI R17, 0x01 ════════════════════════════════════════════════════════════

  // 11 — PC → FLASH
  {
    label: 'LDI R17, 0x01 — PC ukazuje na instrukci',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x03', displayIr: 'STS DDRF, R16',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 12 — LDI R17 fetched
  {
    label: 'LDI R17, 0x01 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0xE001' },
    displayPc: '0x03', displayIr: 'LDI R17, 0x01',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 13 — PC++
  {
    label: 'LDI R17, 0x01 — čítač programu zvýšen',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x04', displayIr: 'LDI R17, 0x01',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 14 — ALU execute
  {
    label: 'LDI R17, 0x01 — ALU zpracuje instrukci',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['ri-alu'], activeRegisters: [],
    displayPc: '0x04', displayIr: 'LDI R17, 0x01',
    displayR16: '0xFF', displayR17: '—', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 15 — R17 = 0x01
  {
    label: 'LDI R17, 0x01 — R17 = 0x01 (světlo na bitu 0)',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x04', displayIr: 'LDI R17, 0x01',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // ══ LOOP — STS PORTF, R17 (PORTF) — iterace 1 ═══════════════════════════════

  // 16 — PC → FLASH (loop:)
  {
    label: '← loop: STS PORTF, R17 — zápis do PORTF',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x04', displayIr: 'LDI R17, 0x01',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 17 — STS PORTF fetched
  {
    label: 'STS PORTF, R17 — instrukce načtena do RI',
    activeFields: ['ir'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x9310' },
    displayPc: '0x04', displayIr: 'STS PORTF, R17',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 18 — PC++
  {
    label: 'STS PORTF, R17 — čítač programu zvýšen',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x05', displayIr: 'STS PORTF, R17',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '—',
    displayPortF: '0x00', displayFlags: false,
  },

  // 19 — STS execute → PORTF = 0x01, LED bit 0 ON
  {
    label: 'STS PORTF, R17 — PORTF = 0x01 → LED bit 0 svítí! 💡',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: ['portf-out'], activeRegisters: ['R17'],
    activePortF: true, animatePortF: true,
    displayPc: '0x05', displayIr: 'STS PORTF, R17',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '—',
    displayPortF: '0x01', displayFlags: false,
  },

  // ══ Čekací smyčka (fast-forward) ════════════════════════════════════════════

  // 20 — delay loop fast-forward
  {
    label: 'Čekací smyčka: R18 = 0xFF → DEC × 255 → R18 = 0x00 (čekání)',
    activeFields: [], activeAlu: false,
    activeRamRow: true, activeConnections: [], activeRegisters: ['R18'],
    animateR18: true,
    displayPc: '0x08', displayIr: 'BRNE for_loop',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // ══ LSL R17 — iterace 1 ══════════════════════════════════════════════════════

  // 21 — PC → FLASH
  {
    label: 'LSL R17 — PC ukazuje na instrukci (posun bitu doleva)',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    displayPc: '0x08', displayIr: 'BRNE for_loop',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // 22 — LSL fetched + PC++
  {
    label: 'LSL R17 — instrukce načtena do RI, PC zvýšen',
    activeFields: ['ir', 'pc'], activeAlu: false,
    activeRamRow: true, activeConnections: ['pc-ram'], activeRegisters: [],
    animateIr: true, animatePc: true,
    flight: { fromId: 'ram-row-pc', toId: 'ri-row', value: '0x0F11' },
    displayPc: '0x09', displayIr: 'LSL R17',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // 23 — LSL execute → R17 = 0x02
  {
    label: 'LSL R17 — posun doleva: R17 = 0x02 (bit se posunul)',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R17-alu'], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x09', displayIr: 'LSL R17',
    displayR16: '0xFF', displayR17: '0x02', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // ══ TST + BRNE skip_reset (bit != 0) ═════════════════════════════════════════

  // 24 — TST Z=0, BRNE taken
  {
    label: 'TST R17 → Z=0, BRNE skip_reset: bit není nula → skok proveden, PC = 0x0C',
    activeFields: ['pc'], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R17-alu'], activeRegisters: [],
    animatePc: true,
    displayPc: '0x0C', displayIr: 'BRNE skip_reset',
    displayR16: '0xFF', displayR17: '0x02', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // ══ RJMP loop ════════════════════════════════════════════════════════════════

  // 25 — RJMP back to loop
  {
    label: 'RJMP loop — skok zpět na začátek: PC = 0x04',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: [],
    animatePc: true,
    displayPc: '0x04', displayIr: 'RJMP loop',
    displayR16: '0xFF', displayR17: '0x02', displayR18: '0x00',
    displayPortF: '0x01', displayFlags: false,
  },

  // ══ LOOP — iterace 2 (zkrácená) ══════════════════════════════════════════════

  // 26 — STS PORTF iter 2 → PORTF = 0x02
  {
    label: 'Iterace 2: STS PORTF, R17 — PORTF = 0x02 → LED bit 1 svítí!',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: ['portf-out'], activeRegisters: ['R17'],
    activePortF: true, animatePortF: true,
    displayPc: '0x05', displayIr: 'STS PORTF, R17',
    displayR16: '0xFF', displayR17: '0x02', displayR18: '0x00',
    displayPortF: '0x02', displayFlags: false,
  },

  // 27 — delay + LSL iter 2 → R17 = 0x04
  {
    label: 'Čekání + LSL R17 → R17 = 0x04 (bit se posouvá dál…)',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R17-alu'], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x09', displayIr: 'LSL R17',
    displayR16: '0xFF', displayR17: '0x04', displayR18: '0x00',
    displayPortF: '0x02', displayFlags: false,
  },

  // ══ Po 7 iteracích: bit 7 ════════════════════════════════════════════════════

  // 28 — PORTF = 0x80, LED bit 7
  {
    label: 'Po 7 iteracích: R17 = 0x80 — STS PORTF → LED bit 7 svítí!',
    activeFields: [], activeAlu: false,
    activeRamRow: false, activeConnections: ['portf-out'], activeRegisters: ['R17'],
    activePortF: true, animatePortF: true,
    displayPc: '0x05', displayIr: 'STS PORTF, R17',
    displayR16: '0xFF', displayR17: '0x80', displayR18: '0x00',
    displayPortF: '0x80', displayFlags: false,
  },

  // ══ LSL R17 → přetečení ════════════════════════════════════════════════════

  // 29 — LSL R17 → 0x00 (overflow)
  {
    label: 'LSL R17 → 0x00: bit vypadl z registru! (přetečení)',
    activeFields: [], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R17-alu'], activeRegisters: ['R17'],
    animateR17: true,
    displayPc: '0x09', displayIr: 'LSL R17',
    displayR16: '0xFF', displayR17: '0x00', displayR18: '0x00',
    displayPortF: '0x80', displayFlags: false,
  },

  // ══ TST R17 → Z=1, BRNE NOT taken ═══════════════════════════════════════════

  // 30 — TST Z=1, BRNE not taken
  {
    label: 'TST R17 → Z=1 (nula!), BRNE skip_reset: skok NEPROVEDEN → PC = 0x0B',
    activeFields: ['sreg', 'pc'], activeAlu: true,
    activeRamRow: false, activeConnections: ['reg-R17-alu', 'alu-sreg'], activeRegisters: [],
    animatePc: true,
    displayFlagZ: true,
    displayPc: '0x0B', displayIr: 'BRNE skip_reset',
    displayR16: '0xFF', displayR17: '0x00', displayR18: '0x00',
    displayPortF: '0x80', displayFlags: false,
  },

  // ══ LDI R17, 0x01 — reset ════════════════════════════════════════════════════

  // 31 — LDI R17 = 0x01, then RJMP loop
  {
    label: 'LDI R17, 0x01 — reset: světlo zpět na bit 0 → RJMP loop',
    activeFields: ['pc'], activeAlu: false,
    activeRamRow: false, activeConnections: [], activeRegisters: ['R17'],
    animateR17: true, animatePc: true,
    displayPc: '0x04', displayIr: 'RJMP loop',
    displayR16: '0xFF', displayR17: '0x01', displayR18: '0x00',
    displayPortF: '0x80', displayFlags: false,
  },
];

export const MAX_CPU_STEP = CPU_STEPS.length - 1;
