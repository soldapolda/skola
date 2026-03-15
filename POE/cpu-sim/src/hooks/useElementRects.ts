import { useEffect, useState, type RefObject } from 'react';

export type Rects = Record<string, DOMRect | null>;

/**
 * Measures bounding rects of elements by id, relative to a container element.
 * Re-computes on window resize and container resize.
 */
export function useElementRects(
  ids: string[],
  containerRef: RefObject<HTMLElement | null>,
): Rects {
  const [rects, setRects] = useState<Rects>({});
  const idsKey = ids.join(',');

  useEffect(() => {
    const compute = () => {
      const container = containerRef.current;
      if (!container) return;
      const base = container.getBoundingClientRect();
      const next: Rects = {};
      for (const id of ids) {
        const el = document.getElementById(id);
        if (!el) { next[id] = null; continue; }
        const r = el.getBoundingClientRect();
        next[id] = new DOMRect(r.left - base.left, r.top - base.top, r.width, r.height);
      }
      setRects(next);
    };

    compute();
    const ro = new ResizeObserver(compute);
    if (containerRef.current) ro.observe(containerRef.current);
    window.addEventListener('resize', compute);
    return () => { ro.disconnect(); window.removeEventListener('resize', compute); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idsKey, containerRef]);

  return rects;
}
