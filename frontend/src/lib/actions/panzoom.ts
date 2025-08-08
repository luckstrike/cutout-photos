import type { Action } from 'svelte/action';

function debounce<T extends (...args: any[]) => void>(fn: T, wait = 150) {
  let t: ReturnType<typeof setTimeout> | null = null;
  return (...args: Parameters<T>) => {
    if (t) clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

export const panzoom: Action<HTMLElement, any> = (node, opts = {}) => {
  if (import.meta.env.SSR) return;

  let ctrl: any;
  let wheel: (e: WheelEvent) => void;
  let dblHandler: (e: MouseEvent) => void;
  let touchHandler: (e: TouchEvent) => void;
  let resizeObserver: ResizeObserver | null = null;
  let lastTouch = 0;

  (async () => {
    try {
      const mod = await import('@panzoom/panzoom');
      const create = mod.default ?? (mod as any).Panzoom;

      ctrl = create(node, {
        maxScale: 8,
        minScale: 0.25,
        contain: 'contain',
        ...opts
      });

      /* wheel-to-zoom */
      wheel = (e: WheelEvent) => (ctrl as any).zoomWithWheel(e);
      node.addEventListener('wheel', wheel, { passive: false });

      /* double-click to reset fit */
      dblHandler = () => {
            try {
            // Prefer an animated reset if supported by the controller
            try {
              (ctrl as any).reset?.({ animate: true });
            } catch {
              (ctrl as any).reset?.({} as any);
            }
          } catch {
            /* noop */
          }
      };
      node.addEventListener('dblclick', dblHandler);

      /* touch double-tap => treat as double-click on mobile */
      touchHandler = (e: TouchEvent) => {
        const now = Date.now();
        const delta = now - lastTouch;
        lastTouch = now;
        // if two taps within 300ms, trigger reset
        if (delta > 0 && delta < 300) {
          e.preventDefault();
          dblHandler();
        }
      };
      node.addEventListener('touchend', touchHandler, { passive: false });

      /* ResizeObserver to keep image fitted on container resize */
      const target = node.parentElement ?? node;
      resizeObserver = new ResizeObserver(debounce(() => {
        try {
          // reset will fit the image to the container respecting 'contain'
            try {
            (ctrl as any).reset?.({ animate: false });
          } catch {
            (ctrl as any).reset?.({} as any);
          }
        } catch {
          /* noop */
        }
      }, 120));
      resizeObserver.observe(target);

      opts.onInit?.(ctrl);
    } catch (err) {
      // Fail silently; action should not break the app if panzoom can't load
      // eslint-disable-next-line no-console
      console.warn('panzoom action: failed to initialize', err);
    }
  })();

  return {
    destroy() {
      try {
        if (wheel) node.removeEventListener('wheel', wheel);
      } catch {}
      try {
        if (dblHandler) node.removeEventListener('dblclick', dblHandler);
      } catch {}
      try {
        if (touchHandler) node.removeEventListener('touchend', touchHandler);
      } catch {}
      try {
        if (resizeObserver) resizeObserver.disconnect();
      } catch {}
      try {
        ctrl?.destroy?.();
      } catch {}
    }
  };
};
