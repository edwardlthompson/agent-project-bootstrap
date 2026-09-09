"""Tests for hello.about."""

from hello.about import APP_VERSION, about_payload, about_summary


def test_about_includes_version_and_donate() -> None:
    text = about_summary()
    assert APP_VERSION in text
    assert "donate" in text


def test_about_payload_matches_shared_contract() -> None:
    payload = about_payload()
    assert payload["version"] == APP_VERSION
    assert payload["donate"].startswith("http")
    assert payload["summary"] == about_summary()
    assert payload["update"] == {"status": "current", "version": None, "url": None}
