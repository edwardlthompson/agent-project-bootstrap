"""Parse BUILD_PLAN for autonomous /build sprint execution."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Shared patterns with parallel_scope
OPEN = r"(?:🔲|⬜|\[ \])"
ROW_NUMBERED = re.compile(
    rf"^(?P<num>\d+[a-z]?)\.\s+{OPEN}\s+\[(?P<owner>AGENT|AUTO|HUMAN|ADB)\]\s+(?P<task>.+)$"
)
ROW_BULLET = re.compile(
    rf"^- {OPEN} \[(?P<owner>AGENT|AUTO|HUMAN|ADB)\]\s+(?P<task>.+)$"
)
SPRINT_HEADER = re.compile(r"^###\s+Sprint\s+", re.I)
PARALLEL_HEADER = re.compile(r"^#{3,4}\s+.*Parallel", re.I)
SEQUENTIAL_HEADER = re.compile(r"^#{3,4}\s+.*Sequential", re.I)
HUMAN_GROUP_HEADER = re.compile(r"^#{3,4}\s+.*Human.*after automation", re.I)
TABLE_ROW = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|")
PARALLEL_EXCEPTION = re.compile(
    r"<!--\s*parallel_exception:\s*(.+?)\s*-->", re.I
)


@dataclass
class PlanRow:
    owner: str
    task: str
    sprint: str
    phase: str


def load_progress(root: Path) -> dict:
    path = root / ".cursor/agent-progress.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_backlog_keys(root: Path) -> set[str]:
    """sprint|task keys for HUMAN/ADB rows already backlogged (automation failed)."""
    path = root / "HUMAN_BACKLOG.md"
    if not path.exists():
        return set()
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "Deferred" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 4:
            keys.add(f"{parts[1]}|{parts[3]}")
    return keys


def row_action(owner: str) -> str:
    if owner == "HUMAN":
        return "automate_human"
    if owner == "ADB":
        return "automate_adb"
    return "execute"


def next_actionable_row(
    rows: list[PlanRow],
    backlog_keys: set[str],
) -> PlanRow | None:
    for row in rows:
        if row.owner in ("HUMAN", "ADB") and f"{row.sprint}|{row.task}" in backlog_keys:
            continue
        return row
    return None


def parse_open_numbered(lines: list[str], sprint: str, phase: str) -> list[PlanRow]:
    rows: list[PlanRow] = []
    for line in lines:
        m = ROW_NUMBERED.match(line)
        if m:
            rows.append(
                PlanRow(
                    owner=m.group("owner"),
                    task=m.group("task").strip(),
                    sprint=sprint,
                    phase=phase,
                )
            )
    return rows


def count_parallel_agents(lines: list[str]) -> int:
    in_table = False
    count = 0
    for line in lines:
        if PARALLEL_HEADER.match(line):
            in_table = True
            continue
        if in_table and line.startswith("#"):
            in_table = False
        if not in_table:
            continue
        m = TABLE_ROW.match(line)
        if not m or m.group(1).strip().lower() in ("task", "---"):
            continue
        if m.group(2).strip().upper() == "AGENT":
            scope = m.group(3).strip()
            if scope and "—" not in scope and "none" not in scope.lower():
                count += 1
    return count


def split_sprint_phases(
    lines: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Return pre_parallel, parallel_region, post_parallel, human_group line groups."""
    pre: list[str] = []
    parallel: list[str] = []
    post: list[str] = []
    human: list[str] = []
    phase = "pre"
    for line in lines:
        if line.startswith("### Sprint") or line.startswith("<!--"):
            continue
        if PARALLEL_HEADER.match(line):
            phase = "parallel"
            parallel.append(line)
            continue
        if HUMAN_GROUP_HEADER.match(line):
            phase = "human"
            human.append(line)
            continue
        if phase == "parallel" and SEQUENTIAL_HEADER.match(line):
            phase = "post"
        if phase == "pre":
            pre.append(line)
        elif phase == "parallel":
            parallel.append(line)
        elif phase == "post":
            post.append(line)
        else:
            human.append(line)
    return pre, parallel, post, human


def parse_sprint_blocks(text: str) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    in_child = False
    i = 0
    lines = text.splitlines()
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("## Child Repo Playbook"):
            in_child = True
            i += 1
            continue
        if not in_child:
            i += 1
            continue
        if line.startswith("## Ongoing Maintenance"):
            break
        if SPRINT_HEADER.match(line):
            title = line.strip().lstrip("#").strip()
            block_lines: list[str] = [line]
            i += 1
            while i < len(lines) and not (
                SPRINT_HEADER.match(lines[i])
                or (
                    lines[i].startswith("## ")
                    and not lines[i].startswith("### ")
                )
            ):
                block_lines.append(lines[i])
                i += 1
            blocks.append((title, block_lines))
            continue
        i += 1
    return blocks


def parse_maintenance_rows(text: str) -> tuple[list[PlanRow], list[PlanRow]]:
    """Return (automation_rows, human_group_rows) for Ongoing Maintenance."""
    auto_rows: list[PlanRow] = []
    human_rows: list[PlanRow] = []
    in_maint = False
    in_human = False
    for line in text.splitlines():
        if line.startswith("## Ongoing Maintenance"):
            in_maint = True
            continue
        if in_maint and line.startswith("## ") and not line.startswith("### "):
            break
        if not in_maint:
            continue
        if HUMAN_GROUP_HEADER.match(line):
            in_human = True
            continue
        m = ROW_BULLET.match(line)
        if not m:
            continue
        row = PlanRow(
            owner=m.group("owner"),
            task=m.group("task").strip(),
            sprint="Ongoing Maintenance",
            phase="human_group" if in_human else "maintenance",
        )
        if in_human:
            human_rows.append(row)
        else:
            auto_rows.append(row)
    return auto_rows, human_rows


def resolve_sprint(
    title: str,
    block_lines: list[str],
    progress: dict,
    backlog_keys: set[str],
) -> dict:
    body = "\n".join(block_lines)
    exc = PARALLEL_EXCEPTION.search(body)
    if exc and exc.group(1).strip().lower() not in ("none", ""):
        parallel_skipped = True
    else:
        parallel_skipped = count_parallel_agents(block_lines) == 0

    pre, parallel, post, human_lines = split_sprint_phases(block_lines)
    pre_open = parse_open_numbered(pre, title, "pre_parallel")
    post_open = parse_open_numbered(post, title, "post_parallel")
    human_open = parse_open_numbered(human_lines, title, "human_group")
    parallel_done = title in (progress.get("parallel_sprint_done") or [])

    open_aa_pre = [r for r in pre_open if r.owner in ("AGENT", "AUTO")]
    open_aa_post = [r for r in post_open if r.owner in ("AGENT", "AUTO")]
    open_ha = [r for r in human_open if r.owner in ("HUMAN", "ADB")]

    next_row = None
    action = None

    # AGENT/AUTO first (pre → parallel → post), then grouped human section
    pre_next = next_actionable_row(pre_open, backlog_keys)
    if pre_next and pre_next.owner in ("AGENT", "AUTO"):
        action = "execute"
        next_row = {
            "owner": pre_next.owner,
            "task": pre_next.task,
            "sprint": title,
            "phase": pre_next.phase,
            "action": action,
        }
    elif (
        not parallel_skipped
        and not parallel_done
        and count_parallel_agents(block_lines) > 0
        and not open_aa_pre
    ):
        action = "parallel_dispatch"
        next_row = {
            "owner": "AGENT",
            "task": "Parallel dispatch (/scope)",
            "sprint": title,
            "phase": "parallel",
            "action": "parallel_dispatch",
        }
    else:
        post_next = next_actionable_row(post_open, backlog_keys)
        if post_next and post_next.owner in ("AGENT", "AUTO"):
            action = "execute"
            next_row = {
                "owner": post_next.owner,
                "task": post_next.task,
                "sprint": title,
                "phase": post_next.phase,
                "action": action,
            }
        else:
            human_next = next_actionable_row(human_open, backlog_keys)
            if human_next:
                action = row_action(human_next.owner)
                next_row = {
                    "owner": human_next.owner,
                    "task": human_next.task,
                    "sprint": title,
                    "phase": human_next.phase,
                    "action": action,
                }

    open_aa = len(open_aa_pre) + len(open_aa_post)
    parallel_pending = (
        not parallel_skipped
        and not parallel_done
        and count_parallel_agents(block_lines) > 0
    )
    if parallel_pending and not open_aa_pre:
        open_aa += 1

    pending_ha = [
        r for r in open_ha if f"{r.sprint}|{r.task}" not in backlog_keys
    ]

    agent_auto_complete = (
        open_aa == 0
        and not parallel_pending
        and not pending_ha
    )

    backlogged_ha = [
        r for r in open_ha if f"{r.sprint}|{r.task}" in backlog_keys
    ]

    return {
        "sprint": title,
        "sprint_agent_auto_complete": agent_auto_complete,
        "sprint_complete": agent_auto_complete and not open_ha,
        "open_agent_auto": open_aa,
        "open_human_adb": len(open_ha),
        "halt": False,
        "halt_reason": None,
        "next_row": next_row,
        "action": action,
        "backlogged_human_adb": [
            {"owner": r.owner, "task": r.task, "sprint": r.sprint}
            for r in backlogged_ha
        ],
    }


def build_status(root: Path, *, lane: str = "auto") -> dict:
    bp = root / "BUILD_PLAN.md"
    text = bp.read_text(encoding="utf-8")
    progress = load_progress(root)
    backlog_keys = load_backlog_keys(root)

    if lane in ("auto", "child"):
        child_status = _child_status(text, progress, backlog_keys)
        if not child_status.get("all_sprints_agent_auto_complete"):
            return child_status
        if lane == "child":
            return child_status

    maint_auto, maint_human = parse_maintenance_rows(text)
    maint_open = maint_auto + maint_human
    maint_aa_next = next_actionable_row(maint_auto, backlog_keys)
    maint_human_next = (
        next_actionable_row(maint_human, backlog_keys) if not maint_aa_next else None
    )
    maint_next = maint_aa_next or maint_human_next
    if maint_next:
        act = row_action(maint_next.owner) if maint_next.owner in ("HUMAN", "ADB") else "execute"
        return {
            "lane": "maintainer",
            "sprint": "Ongoing Maintenance",
            "sprint_agent_auto_complete": False,
            "sprint_complete": False,
            "open_agent_auto": len([r for r in maint_auto if r.owner in ("AGENT", "AUTO")]),
            "open_human_adb": len(maint_human),
            "halt": False,
            "halt_reason": None,
            "next_row": {
                "owner": maint_next.owner,
                "task": maint_next.task,
                "sprint": "Ongoing Maintenance",
                "phase": "maintenance",
                "action": act,
            },
            "action": act,
            "chain_continue": False,
            "all_sprints_agent_auto_complete": False,
            "backlogged_human_adb": [],
        }

    return _child_status(text, progress, backlog_keys)


def _child_status(text: str, progress: dict, backlog_keys: set[str]) -> dict:
    blocks = parse_sprint_blocks(text)
    for title, block_lines in blocks:
        status = resolve_sprint(title, block_lines, progress, backlog_keys)
        if not status["sprint_agent_auto_complete"] or status.get("next_row"):
            status["lane"] = "child"
            status["chain_continue"] = status["sprint_agent_auto_complete"]
            status["all_sprints_agent_auto_complete"] = False
            return status

    return {
        "lane": "child",
        "sprint": None,
        "sprint_agent_auto_complete": True,
        "sprint_complete": True,
        "open_agent_auto": 0,
        "open_human_adb": 0,
        "halt": False,
        "halt_reason": None,
        "next_row": None,
        "action": None,
        "chain_continue": False,
        "all_sprints_agent_auto_complete": True,
        "backlogged_human_adb": [],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--lane", default="auto", choices=["auto", "child", "maintainer"])
    args = parser.parse_args()
    status = build_status(Path(args.root).resolve(), lane=args.lane)
    if args.json:
        print(json.dumps(status, indent=2))
    else:
        if status.get("all_sprints_agent_auto_complete"):
            print("All sprints: no open actionable rows")
        elif status.get("next_row"):
            nr = status["next_row"]
            print(f"NEXT [{nr['owner']}] {nr['task']} ({status['sprint']})")
        else:
            print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
