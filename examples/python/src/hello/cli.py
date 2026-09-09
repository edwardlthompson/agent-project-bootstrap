"""CLI entry point for Golden Path Python stub."""

from __future__ import annotations

import argparse
import json
import sys

from hello.about import about_summary
from hello.feedback import build_feedback_url, feedback_repo
from hello.greet import greet, validate_name
from hello.log import log_event, ready_json
from hello.openapi import load_openapi


def main() -> None:
    """Run the hello CLI."""
    parser = argparse.ArgumentParser(description="Golden Path Python CLI stub")
    parser.add_argument("name", nargs="?", default="", help="Name to greet")
    parser.add_argument("--about", action="store_true", help="Print About (version + donate)")
    parser.add_argument("--feedback", action="store_true", help="Print a GitHub issue-form URL")
    parser.add_argument("--kind", choices=("bug", "feature"), default="bug")
    parser.add_argument("--title", default="", help="Optional issue title")
    parser.add_argument("--ready", action="store_true", help="Print JSON readiness and exit")
    parser.add_argument("--openapi", action="store_true", help="Print the OpenAPI document")
    args = parser.parse_args()

    if args.ready:
        log_event("info", "ready")
        print(ready_json())
        return
    if args.openapi:
        log_event("info", "openapi")
        print(json.dumps(load_openapi()))
        return
    if args.about:
        log_event("info", "about")
        print(about_summary())
        return
    if args.feedback:
        url = build_feedback_url(feedback_repo(), args.kind, args.title)
        if not url:
            log_event("error", "feedback-repo")
            print("Set GITHUB_REPO=owner/name to open GitHub feedback.", file=sys.stderr)
            sys.exit(1)
        log_event("info", "feedback")
        print(json.dumps({"kind": args.kind, "url": url}))
        return

    try:
        validated = validate_name(args.name)
        log_event("info", "start")
        print(greet(validated))
    except ValueError as exc:
        log_event("error", "name")
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
