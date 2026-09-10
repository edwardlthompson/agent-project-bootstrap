"""CLI About slice: version + donate URL + update stub (no crash payload)."""

from __future__ import annotations

from typing import TypedDict

APP_VERSION = "0.1.0"
DONATE_URL = "https://github.com/sponsors"


class AboutUpdate(TypedDict):
    status: str
    version: str | None
    url: str | None


class AboutPayload(TypedDict):
    version: str
    donate: str
    summary: str
    update: AboutUpdate


def about_summary() -> str:
    """Return a one-line About string."""
    return f"golden-path {APP_VERSION} donate {DONATE_URL}"


def about_payload() -> AboutPayload:
    """Return the shared About/donate/update JSON object."""
    return {
        "version": APP_VERSION,
        "donate": DONATE_URL,
        "summary": about_summary(),
        "update": {"status": "current", "version": None, "url": None},
    }
