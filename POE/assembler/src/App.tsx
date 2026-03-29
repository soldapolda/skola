import { useState, useEffect, useCallback } from 'react';
import { DEFAULT_FLASH } from './data';
import { resetEmulator, stepEmulator } from './logic/emulator';
import CpuSlide from './components/CpuSlide';
import type { EmulatorState } from './types';

export default function App() {
  const [state, setState] = useState<EmulatorState>(() => resetEmulator(DEFAULT_FLASH));

  const step = useCallback(() => {
    setState(s => stepEmulator(s));
  }, []);

  const reset = useCallback(() => {
    setState(s => resetEmulator(DEFAULT_FLASH, s.pink));
  }, []);

  const toggleButton = useCallback((bit: number) => {
    setState(s => ({ ...s, pink: s.pink ^ (1 << bit) }));
  }, []);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); step(); }
      else if (e.key === 'ArrowLeft') reset();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [step, reset]);

  return (
    <CpuSlide
      state={state}
      onStep={step}
      onReset={reset}
      onToggleButton={toggleButton}
    />
  );
}
