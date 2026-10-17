import { useEffect, useRef, useState, type RefObject } from 'react';
import { useElementRects } from '../hooks/useElementRects';

interface Props {
  fromId: string;
  toId: string;
  value: string;
  triggerKey: number;
  containerRef: RefObject<HTMLDivElement | null>;
  onArrived: () => void;
}

type Phase = 'init' | 'flying' | 'done';

export default function FlyingValue({ fromId, toId, value, triggerKey, containerRef, onArrived }: Props) {
  const rects = useElementRects([fromId, toId], containerRef);
  const [phase, setPhase] = useState<Phase>('init');
  const onArrivedRef = useRef(onArrived);
  onArrivedRef.current = onArrived;

  // Reset and re-trigger animation whenever triggerKey changes
  useEffect(() => {
    setPhase('init');
    let raf1: number, raf2: number;
    raf1 = requestAnimationFrame(() => {
      raf2 = requestAnimationFrame(() => {
        setPhase('flying');
      });
    });
    return () => { cancelAnimationFrame(raf1); cancelAnimationFrame(raf2); };
  }, [triggerKey]);

  if (phase === 'done') return null;

  const fromRect = rects[fromId];
  const toRect   = rects[toId];
  if (!fromRect || !toRect) return null;

  const fromCx = fromRect.left + fromRect.width  / 2;
  const fromCy = fromRect.top  + fromRect.height / 2;
  const toCx   = toRect.left  + toRect.width    / 2;
  const toCy   = toRect.top   + toRect.height   / 2;

  const dx = toCx - fromCx;
  const dy = toCy - fromCy;

  const packetW = 90;
  const packetH = 34;

  const style: React.CSSProperties = {
    position: 'absolute',
    left: fromCx - packetW / 2,
    top:  fromCy - packetH / 2,
    width:  packetW,
    height: packetH,
    backgroundColor: '#4fb3bf',
    border: '3px solid #000',
    borderRadius: 4,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'monospace',
    fontWeight: 700,
    fontSize: 15,
    color: '#fff',
    boxShadow: '0 4px 16px rgba(0,0,0,0.4)',
    pointerEvents: 'none',
    zIndex: 100,
    transition: phase === 'flying'
      ? 'transform 1.1s cubic-bezier(0.4, 0, 0.2, 1)'
      : undefined,
    transform: phase === 'flying'
      ? `translate(${dx}px, ${dy}px) scale(0.85)`
      : 'translate(0,0) scale(1)',
    animation: phase === 'init' ? 'flyDeparture 0.08s ease-out forwards' : undefined,
  };

  return (
    <div
      style={style}
      onTransitionEnd={() => {
        setPhase('done');
        onArrivedRef.current();
      }}
    >
      {value}
    </div>
  );
}
