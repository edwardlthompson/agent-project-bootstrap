"""CLI entry point for Golden Path Python stub."""

import argparse
import sys

from hello.about import about_summary
from hello.feedback import build_feedback_url, feedback_repo
from hello.greet import greet, validate_name


def main() -> None:
    """Run the hello CLI."""
    parser = argparse.ArgumentParser(description="Golden Path Python CLI stub")
    parser.add_argument("name", nargs="?", default="", help="Name to greet")
    parser.add_argument("--about", action="store_true", help="Print About (version + donate)")
    parser.add_argument("--feedback", action="store_true", help="Print a GitHub issue-form URL")
    parser.add_argument("--kind", choices=("bug", "feature"), default="bug")
    parser.add_argument("--title", default="", help="Optional issue title")
    args = parser.parse_args()

    if args.about:
        print(about_summary())
        return

    if args.feedback:
        url = build_feedback_url(feedback_repo(), args.kind, args.title)
        if not url:
            print("Set GITHUB_REPO=owner/name to open GitHub feedback.", file=sys.stderr)
            sys.exit(1)
        print(url)
        return

    try:
        validated = validate_name(args.name)
        print(greet(validated))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
