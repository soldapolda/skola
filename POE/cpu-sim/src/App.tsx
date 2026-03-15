import { useState, useEffect } from 'react';
import { initialState } from './data';
import CpuSlide from './components/CpuSlide';
import { MAX_CPU_STEP } from './cpuSteps';

export default function App() {
  const [cpuStep, setCpuStep] = useState(0);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') setCpuStep(s => Math.min(s + 1, MAX_CPU_STEP));
      else if (e.key === 'ArrowLeft') setCpuStep(s => Math.max(0, s - 1));
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  return <CpuSlide state={initialState} step={cpuStep} />;
}
