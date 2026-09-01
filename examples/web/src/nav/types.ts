export type GpRoute = "home" | "settings" | "about" | "feedback";
export type FeedbackKind = "bug" | "feature";

export type NavState = {
  stack: GpRoute[];
  feedbackKind?: FeedbackKind;
  scroll: Partial<Record<GpRoute, number>>;
  promptOpen: boolean;
};

export const PANEL_ROUTES: readonly GpRoute[] = ["settings", "about", "feedback"];
