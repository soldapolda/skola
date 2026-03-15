import { useState, useEffect } from 'react';
import { initialState } from './data';
import CpuSlide from './components/CpuSlide';
import PhaseSlide, { MAX_PHASE_STEP } from './components/PhaseSlide';
import { MAX_CPU_STEP } from './cpuSteps';

export default function App() {
  const [slide,    setSlide]    = useState(0); // 0 = phase text, 1 = cpu diagram
  const [textStep, setTextStep] = useState(0);
  const [cpuStep,  setCpuStep]  = useState(0);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') {
        if (slide === 0) {
          if (textStep < MAX_PHASE_STEP) setTextStep(s => s + 1);
          else { setSlide(1); setCpuStep(0); }
        } else {
          setCpuStep(s => Math.min(s + 1, MAX_CPU_STEP));
        }
      } else if (e.key === 'ArrowLeft') {
        if (slide === 1) {
          if (cpuStep > 0) setCpuStep(s => s - 1);
          else setSlide(0);
        } else {
          setTextStep(s => Math.max(0, s - 1));
        }
      }
    };

    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [slide, textStep, cpuStep]);

  if (slide === 1) return <CpuSlide state={initialState} step={cpuStep} />;
  return <PhaseSlide step={textStep} />;
}
