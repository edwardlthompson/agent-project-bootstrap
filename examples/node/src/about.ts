export const APP_VERSION = "0.1.0";
export const DONATE_URL = "https://github.com/sponsors";

export type AboutUpdate = {
  status: "current" | "available" | "unknown";
  version: string | null;
  url: string | null;
};

export type AboutPayload = {
  version: string;
  donate: string;
  summary: string;
  update: AboutUpdate;
};

export function aboutSummary(): string {
  return `golden-path ${APP_VERSION} donate ${DONATE_URL}`;
}

export function aboutPayload(): AboutPayload {
  return {
    version: APP_VERSION,
    donate: DONATE_URL,
    summary: aboutSummary(),
    update: { status: "current", version: null, url: null },
  };
}
