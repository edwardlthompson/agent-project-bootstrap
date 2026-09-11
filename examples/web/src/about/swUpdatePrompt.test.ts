import { describe, expect, it, vi } from "vitest";
import { createSwUpdatePrompt, hasWaitingWorker, watchWaitingWorker } from "./swUpdatePrompt";

describe("swUpdatePrompt", () => {
  it("detects waiting worker", () => {
    expect(hasWaitingWorker({ waiting: {} } as ServiceWorkerRegistration)).toBe(true);
    expect(hasWaitingWorker({ waiting: null } as ServiceWorkerRegistration)).toBe(false);
  });

  it("emits on watch and cleans up", () => {
    const listeners = new Map<string, EventListener>();
    const registration = {
      waiting: null,
      installing: null,
      addEventListener: (type: string, fn: EventListener) => listeners.set(type, fn),
      removeEventListener: (type: string) => listeners.delete(type),
    } as unknown as ServiceWorkerRegistration;
    const onChange = vi.fn();
    const stop = watchWaitingWorker(registration, onChange);
    expect(onChange).toHaveBeenCalledWith(false);
    expect(listeners.has("updatefound")).toBe(true);
    stop();
    expect(listeners.has("updatefound")).toBe(false);
  });

  it("builds opt-in dialog without auto-apply", () => {
    const apply = vi.fn();
    const dismiss = vi.fn();
    const el = createSwUpdatePrompt(apply, dismiss);
    expect(el.dataset.testid).toBe("sw-update-prompt");
    el.querySelector<HTMLButtonElement>('[data-testid="sw-update-apply"]')?.click();
    el.querySelector<HTMLButtonElement>('[data-testid="sw-update-later"]')?.click();
    expect(apply).toHaveBeenCalledOnce();
    expect(dismiss).toHaveBeenCalledOnce();
  });
});
