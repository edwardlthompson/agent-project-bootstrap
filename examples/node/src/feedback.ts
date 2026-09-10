export type FeedbackKind = "bug" | "feature";

export function isPlaceholderRepo(repo: string): boolean {
  const trimmed = repo.trim();
  return !trimmed || trimmed.toUpperCase() === "OWNER/REPO";
}

export function feedbackRepo(): string {
  return process.env.GITHUB_REPO?.trim() || process.env.RELEASE_REPO?.trim() || "OWNER/REPO";
}

export function buildFeedbackUrl(repo: string, kind: FeedbackKind, title = ""): { url: string } {
  if (isPlaceholderRepo(repo)) {
    return { url: "" };
  }
  const template = kind === "feature" ? "feature_request.yml" : "bug_report.yml";
  const params = new URLSearchParams({ template });
  if (title.trim()) {
    params.set("title", title.trim());
  }
  return { url: `https://github.com/${repo.trim()}/issues/new?${params.toString()}` };
}
