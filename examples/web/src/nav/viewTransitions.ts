/** Progressive enhancement: View Transitions API for nav panel swaps when supported. */

export type ViewTransitionLike = {
  finished: Promise<void>;
};

export function canUseViewTransitions(): boolean {
  return (
    typeof document !== "undefined" &&
    "startViewTransition" in document &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

export function runNavTransition(update: () => void): ViewTransitionLike | null {
  if (!canUseViewTransitions()) {
    update();
    return null;
  }
  const doc = document as Document & {
    startViewTransition?: (cb: () => void) => ViewTransitionLike;
  };
  return doc.startViewTransition?.(update) ?? (update(), null);
}
