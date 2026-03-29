import type { FlashWord } from './types';

/**
 * Default program: interactive LED value on PORTF, controlled by two PINK buttons.
 *
 * Button B0 (bit 0 of PINK) — active-low: press increments R20
 * Button B1 (bit 1 of PINK) — active-low: press returns to reset
 *
 * Assembly source:
 *   .org 0
 *   jmp Program
 *   Program:
 *       ldi r16, 0xff
 *       out DDRF, r16
 *       ldi r17, 0x00
 *   reset:
 *       ldi r20, 0x00
 *   main:
 *       lds r18, PINK
 *       sbrc r18, 0
 *       rjmp inc
 *       dec r20
 *       rjmp update
 *   inc:
 *       inc r20
 *   update:
 *       out PORTF, r20
 *       sbrc r18, 1
 *       rjmp main
 *       rjmp reset
 */
export const DEFAULT_FLASH: FlashWord[] = [
  // Reset vector — JMP to Program (2 words)
  { address: 0x00, hex: '0x940C', label: 'JMP Program',   instr: { op: 'JMP',  target: 0x02 } },
  { address: 0x01, hex: '0x0002', label: '[0x0002]',       instr: { op: 'WORD', value:  0x0002 }, isSecondWord: true },

  // Initialisation
  { address: 0x02, hex: '0xEF0F', label: 'LDI R16, 0xFF', instr: { op: 'LDI', rd: 16, k: 0xFF }, loopLabel: 'Program:' },
  { address: 0x03, hex: '0xBB00', label: 'OUT DDRF, R16', instr: { op: 'OUT', port: 'DDRF',  rr: 16 } },
  { address: 0x04, hex: '0xE010', label: 'LDI R17, 0x00', instr: { op: 'LDI', rd: 17, k: 0x00 } },

  // reset:
  { address: 0x05, hex: '0xEF4F', label: 'LDI R20, 0xFF', instr: { op: 'LDI', rd: 20, k: 0xFF }, loopLabel: 'reset:' },

  // main: — read PINK (2-word LDS)
  { address: 0x06, hex: '0x9120', label: 'LDS R18, PINK', instr: { op: 'LDS', rd: 18, addr: 0x106 }, loopLabel: 'main:' },
  { address: 0x07, hex: '0x0106', label: '[0x0106]',       instr: { op: 'WORD', value: 0x0106 }, isSecondWord: true },

  // Test bit 0 — skip RJMP inc if bit is SET (active-low: SET means button NOT pressed)
  { address: 0x08, hex: '0xFD20', label: 'SBRC R18, 0',   instr: { op: 'SBRC', rr: 18, bit: 0 } },
  { address: 0x09, hex: '0xC002', label: 'RJMP inc',       instr: { op: 'RJMP', target: 0x0C } },

  // Button NOT pressed path: decrement
  { address: 0x0A, hex: '0x954A', label: 'DEC R20',        instr: { op: 'DEC', rd: 20 } },
  { address: 0x0B, hex: '0xC001', label: 'RJMP update',    instr: { op: 'RJMP', target: 0x0D } },

  // inc:
  { address: 0x0C, hex: '0x9443', label: 'INC R20',        instr: { op: 'INC', rd: 20 }, loopLabel: 'inc:' },

  // update:
  { address: 0x0D, hex: '0xBBA0', label: 'OUT PORTF, R20', instr: { op: 'OUT', port: 'PORTF', rr: 20 }, loopLabel: 'update:' },

  // Test bit 1 — if SET (button NOT pressed) jump back to main
  { address: 0x0E, hex: '0xFD21', label: 'SBRC R18, 1',   instr: { op: 'SBRC', rr: 18, bit: 1 } },
  { address: 0x0F, hex: '0xCFF6', label: 'RJMP main',      instr: { op: 'RJMP', target: 0x06 } },
  { address: 0x10, hex: '0xCFF4', label: 'RJMP reset',     instr: { op: 'RJMP', target: 0x05 } },
];
