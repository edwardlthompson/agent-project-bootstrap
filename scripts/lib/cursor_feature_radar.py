"""Weekly Cursor feature radar — soft-fail doc diff vs registry."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

LLMS_URL = "https://cursor.com/llms.txt"
URL_RE = re.compile(r"https://cursor\.com/docs/[^\s)]+")


def fetch_llms() -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(LLMS_URL, headers={"User-Agent": "agent-project-bootstrap-radar/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return text, digest
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"WARN: fetch failed: {exc}", file=sys.stderr)
        return None, None


def parse_urls(text: str) -> set[str]:
    return set(URL_RE.findall(text))


def load_registry(root: Path) -> dict:
    path = root / "docs/CURSOR_FEATURE_REGISTRY.json"
    return json.loads(path.read_text(encoding="utf-8"))


def save_registry(root: Path, data: dict) -> None:
    path = root / "docs/CURSOR_FEATURE_REGISTRY.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def score_new(url: str, tier: str) -> int:
    """Heuristic adoption score (0–10) for undocumented URLs."""
    score = 5
    lower = url.lower()
    if any(k in lower for k in ("hook", "skill", "subagent", "mcp", "cli")):
        score += 2
    if "cloud" in lower or "bugbot" in lower or "automation" in lower:
        score += 1 if tier == "commercial" else -1
    if "design" in lower or "canvas" in lower:
        score += 1
    return max(0, min(10, score))


def read_backlog(root: Path) -> set[str]:
    path = root / "CURSOR_RADAR_BACKLOG.md"
    if not path.is_file():
        return set()
    return set(re.findall(r"https://cursor\.com/docs/[^\s)]+", path.read_text(encoding="utf-8")))


def append_backlog(root: Path, url: str, score: int) -> None:
    path = root / "CURSOR_RADAR_BACKLOG.md"
    line = f"- [{score}] {url} ({datetime.now(timezone.utc).date().isoformat()})\n"
    if path.is_file() and url in path.read_text(encoding="utf-8"):
        return
    with path.open("a", encoding="utf-8") as fh:
        if path.stat().st_size == 0:
            fh.write("# Cursor feature radar backlog (gitignored)\n\n")
        fh.write(line)


def run(root: Path) -> int:
    today = datetime.now(timezone.utc).date()
    tier = "foss"
    sel = root / ".cursor/stack-selection.json"
    if sel.is_file():
        try:
            tier = json.loads(sel.read_text(encoding="utf-8")).get("distribution_tier", "foss")
        except json.JSONDecodeError:
            pass

    registry = load_registry(root)
    entries = {e["doc_url"]: e for e in registry.get("entries", []) if e.get("doc_url")}
    backlog_urls = read_backlog(root)

    text, digest = fetch_llms()
    report_lines = [
        "# Cursor Feature Radar Report",
        "",
        f"Generated: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        f"Distribution tier: {tier}",
        "",
    ]

    if text is None:
        report_lines.extend(["status: fetch_failed", "", "Network or parse failure — CI continues."])
        (root / "CURSOR_RADAR_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        print("Cursor feature radar: fetch_failed (exit 0)")
        return 0

    live_urls = parse_urls(text)
    known_urls = set(entries)
    new_urls = sorted(live_urls - known_urls)
    removed = sorted(known_urls - live_urls)
    stale: list[str] = []

    for entry in registry.get("entries", []):
        url = entry.get("doc_url")
        if not url:
            continue
        if url in live_urls:
            entry["last_seen"] = today.isoformat()
        ignore_until = entry.get("ignore_until")
        if ignore_until:
            try:
                if today < datetime.fromisoformat(ignore_until).date():
                    continue
            except ValueError:
                pass
        last = entry.get("last_seen")
        if last:
            try:
                if today - datetime.fromisoformat(last).date() > timedelta(days=90):
                    if entry.get("template_status") not in ("rejected", "shipped"):
                        stale.append(entry.get("id", url))
            except ValueError:
                pass

    scored: list[tuple[str, int]] = []
    for url in new_urls:
        if url in backlog_urls:
            continue
        entry_status = next(
            (e.get("template_status") for e in registry.get("entries", []) if e.get("doc_url") == url),
            None,
        )
        if entry_status in ("shipped", "rejected"):
            continue
        s = score_new(url, tier)
        scored.append((url, s))
        if s >= 7:
            append_backlog(root, url, s)

    report_lines.append(f"status: ok")
    report_lines.append(f"live_doc_urls: {len(live_urls)}")
    report_lines.append(f"new_urls: {len(new_urls)}")
    report_lines.append(f"removed_urls: {len(removed)}")
    report_lines.append(f"stale_entries: {len(stale)}")
    report_lines.append("")

    if scored:
        report_lines.append("## New URLs (scored)")
        for url, s in sorted(scored, key=lambda x: -x[1])[:20]:
            flag = " **suggest BUILD_PLAN**" if s >= 9 else ""
            report_lines.append(f"- [{s}] {url}{flag}")
        report_lines.append("")

    if removed:
        report_lines.append("## Removed from llms.txt")
        for url in removed[:20]:
            report_lines.append(f"- {url}")
        report_lines.append("")

    if stale:
        report_lines.append("## Stale (watch)")
        for item in stale[:20]:
            report_lines.append(f"- {item}")
        report_lines.append("")

    report_lines.append(f"llms_txt_sha256: {digest}")
    (root / "CURSOR_RADAR_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    save_registry(root, registry)

    top = sorted(scored, key=lambda x: -x[1])[:3]
    if top:
        print("Top new Cursor doc URLs:")
        for url, s in top:
            print(f"  [{s}] {url}")
    else:
        print("Cursor feature radar: no new high-score URLs")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    return run(Path(args.root).resolve())


if __name__ == "__main__":
    sys.exit(main())
