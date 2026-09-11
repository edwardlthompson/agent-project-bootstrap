const MAX_STACK_LINES = 200;

const GITHUB = /\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]+/g;
const JWT = /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g;
const AWS = /\bAKIA[0-9A-Z]{16}\b/g;
const EMAIL = /[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}/g;
const WIN_HOME = /C:\\Users\\[^\\]+\\/gi;
const UNIX_HOME = /\/(?:home|Users)\/[^/\s]+\//g;
const TOKEN = /(?:api[_-]?key|token)\s*[:=]\s*\S+/gi;
const URL_Q = /([?&])(token|key|code|access_token)=[^&\s]+/gi;
const INJECT = /(?:ignore\s+(?:all\s+)?previous\s+instructions|you\s+are\s+now|<<SYS>>|\[INST\])/gi;

export function sanitizeCrashText(text: string): string {
  let out = text.replace(GITHUB, "<redacted-secret>");
  out = out.replace(JWT, "<redacted-secret>");
  out = out.replace(AWS, "<redacted-secret>");
  out = out.replace(EMAIL, "<redacted-email>");
  out = out.replace(WIN_HOME, "<redacted-home>");
  out = out.replace(UNIX_HOME, "<redacted-home>/");
  out = out.replace(TOKEN, "<redacted-secret>");
  out = out.replace(URL_Q, "$1$2=<redacted-secret>");
  out = out.replace(INJECT, "<redacted-injection>");
  return out.split("\n").slice(0, MAX_STACK_LINES).join("\n");
}

export function sanitizeCrashPayload(raw: Record<string, unknown>): {
  message: string;
  stack: string;
} {
  return {
    message: sanitizeCrashText(String(raw.message ?? "")),
    stack: sanitizeCrashText(String(raw.stack ?? "")),
  };
}
