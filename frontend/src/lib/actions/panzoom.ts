import type { Action } from 'svelte/action';

export const panzoom: Action<HTMLElement, any> = (node, opts = {}) => {
  if (import.meta.env.SSR) return;

  let ctrl: any;
  let wheel: (e: WheelEvent) => void;

  (async () => {
    const mod     = await import('@panzoom/panzoom');
    const create  = mod.default ?? mod.Panzoom;

    ctrl = create(node, {
      maxScale: 8,
      minScale: 0.25,
      contain: 'contain',
      ...opts
    });

    /* wheel-to-zoom */
    wheel = e => ctrl.zoomWithWheel(e);
    node.addEventListener('wheel', wheel, { passive: false });
    opts.onInit?.(ctrl);
  })();

  return {
    destroy() {
      node.removeEventListener('wheel', wheel);
      ctrl?.destroy?.();
    }
  };
};