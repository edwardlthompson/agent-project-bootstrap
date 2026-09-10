"""Build a GitHub issue-form URL for CLI feedback."""

from __future__ import annotations

import os
from urllib.parse import urlencode

Kind = str


def is_placeholder_repo(repo: str) -> bool:
    trimmed = repo.strip()
    return not trimmed or trimmed.upper() == "OWNER/REPO"


def feedback_repo() -> str:
    return (os.environ.get("GITHUB_REPO") or os.environ.get("RELEASE_REPO") or "OWNER/REPO").strip()


def build_feedback_url(repo: str, kind: Kind = "bug", title: str = "") -> str:
    if is_placeholder_repo(repo):
        return ""
    template = "feature_request.yml" if kind == "feature" else "bug_report.yml"
    params = {"template": template}
    if title.strip():
        params["title"] = title.strip()
    return f"https://github.com/{repo.strip()}/issues/new?{urlencode(params)}"
