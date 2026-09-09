"""Tests for hello.feedback."""

from hello.feedback import build_feedback_url, is_placeholder_repo


def test_placeholder_repo_is_empty() -> None:
    assert is_placeholder_repo("OWNER/REPO")
    assert build_feedback_url("OWNER/REPO", "bug") == ""


def test_builds_issue_form_url() -> None:
    url = build_feedback_url("acme/app", "feature", "Add locale")
    assert url.startswith("https://github.com/acme/app/issues/new?")
    assert "template=feature_request.yml" in url
    assert "title=Add" in url
