#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKLOG = os.path.join(ROOT, "docs", "WORKLOG.md")
WORKLOGS_DIR = os.path.join(ROOT, "docs", "WORKLOGS")


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT).decode("utf-8", errors="replace")


def get_last_commit() -> dict:
    fmt = "%H%n%s%n%b%n%cI"
    out = run(["git", "log", "-1", f"--pretty=format:{fmt}"])
    lines = out.splitlines()
    commit = {
        "hash": lines[0].strip() if lines else "",
        "subject": lines[1].strip() if len(lines) > 1 else "",
        "body": "\n".join(lines[2:-1]).strip() if len(lines) > 3 else (lines[2].strip() if len(lines) > 2 else ""),
        "date": lines[-1].strip() if lines else "",
    }
    return commit


def parse_body(body: str) -> dict:
    fields = {k: "" for k in ["When", "Scope", "Changes", "Problem", "Solution", "Notes"]}
    for line in body.splitlines():
        m = re.match(r"^(When|Scope|Changes|Problem|Solution|Notes):\s*(.*)$", line.strip())
        if m:
            fields[m.group(1)] = m.group(2).strip()
    if not fields["When"]:
        fields["When"] = datetime.now().strftime("%Y-%m-%d")
    return fields


def next_sequence(text: str) -> int:
    # Matches: ## [0001] 2025-01-01 — title
    seqs = [int(m.group(1)) for m in re.finditer(r"^## \[(\d{4,})\] ", text, flags=re.M)]
    return (max(seqs) + 1) if seqs else 1


def already_logged(text: str, commit_hash: str) -> bool:
    return commit_hash[:7] in text


def append_worklog(entry: str) -> None:
    with open(WORKLOG, "a", encoding="utf-8") as f:
        f.write(entry)


def sanitize_filename(text: str, maxlen: int = 128) -> str:
    text = text.strip()
    text = text.replace("/", "／").replace("\\", "＼")
    text = re.sub(r"\s+", " ", text)
    if len(text) > maxlen:
        text = text[:maxlen].rstrip()
    return text or "커밋"


def find_worklog_pending() -> str | None:
    if not os.path.isdir(WORKLOGS_DIR):
        return None
    candidates = [
        os.path.join(WORKLOGS_DIR, fn)
        for fn in os.listdir(WORKLOGS_DIR)
        if fn.endswith("--PENDING.md")
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p))
    return candidates[-1]


def main() -> int:
    if not os.path.exists(WORKLOG):
        os.makedirs(os.path.dirname(WORKLOG), exist_ok=True)
        with open(WORKLOG, "w", encoding="utf-8") as f:
            f.write("# WORKLOG (작업 이력 요약)\n\n")

    with open(WORKLOG, "r", encoding="utf-8") as f:
        current = f.read()

    c = get_last_commit()
    if not c["hash"] or not c["subject"]:
        return 0
    if already_logged(current, c["hash"]):
        return 0

    fields = parse_body(c["body"])
    seq = next_sequence(current)
    title = c["subject"].strip()
    date = fields["When"]
    # Build entry
    entry = []
    entry.append(f"## [{seq:04d}] {date} — {title}\n")
    if fields["Scope"]:
        entry.append(f"- Scope: {fields['Scope']}\n")
    if fields["Changes"]:
        entry.append(f"- Changes: {fields['Changes']}\n")
    if fields["Problem"]:
        entry.append(f"- Problem: {fields['Problem']}\n")
    if fields["Solution"]:
        entry.append(f"- Solution: {fields['Solution']}\n")
    if fields["Notes"]:
        entry.append(f"- Notes: {fields['Notes']}\n")
    entry.append(f"- Commit: {c['hash'][:7]}\n\n")

    append_worklog("".join(entry))

    # If there is a pending individual worklog file, rename and annotate it
    p = find_worklog_pending()
    if p:
        try:
            with open(p, "a", encoding="utf-8") as f:
                f.write(
                    f"\n---\nCommit: {c['hash'][:7]}\nTitle: {c['subject']}\nDate: {c['date']}\n---\n\n"
                )
            new_path = os.path.join(WORKLOGS_DIR, f"{sanitize_filename(title)}.md")
            if os.path.abspath(new_path) != os.path.abspath(p):
                if os.path.exists(new_path):
                    base, ext = os.path.splitext(new_path)
                    new_path = base + " (2)" + ext
                os.rename(p, new_path)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
