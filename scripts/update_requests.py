#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "docs", "REQUESTS")
WORKLOG = os.path.join(ROOT, "docs", "WORKLOG.md")


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT).decode("utf-8", errors="replace")


def get_last_commit() -> dict:
    fmt = "%H%n%s%n%cI"
    out = run(["git", "log", "-1", f"--pretty=format:{fmt}"])
    lines = out.splitlines()
    return {
        "hash": lines[0].strip() if len(lines) > 0 else "",
        "subject": lines[1].strip() if len(lines) > 1 else "",
        "date": lines[2].strip() if len(lines) > 2 else "",
    }


def sanitize_filename(text: str, maxlen: int = 128) -> str:
    # Keep unicode letters/digits/space/_/-; replace path separators
    text = text.strip()
    text = text.replace("/", "／").replace("\\", "＼")
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    # Trim length but preserve whole text as much as possible
    if len(text) > maxlen:
        text = text[:maxlen].rstrip()
    # Fallback
    return text or "커밋"


def find_pending_files() -> list[str]:
    if not os.path.isdir(REQ_DIR):
        return []
    result = []
    for root, _dirs, files in os.walk(REQ_DIR):
        for fn in files:
            if fn.endswith("--PENDING.md"):
                result.append(os.path.join(root, fn))
    # sort by mtime ascending so oldest first
    result.sort(key=lambda p: os.path.getmtime(p))
    return result


def find_seq_and_date_from_worklog(title: str) -> tuple[int | None, str | None]:
    try:
        with open(WORKLOG, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return (None, None)
    pat = re.compile(r"^## \[(\d{4,})\] (\d{4}-\d{2}-\d{2}) — (.+)$", re.M)
    matches = pat.findall(text)
    seq_date_title = [(int(s), d, t.strip()) for (s, d, t) in matches]
    for s, d, t in reversed(seq_date_title):
        if t == title.strip():
            return (s, d)
    return (None, None)


def annotate_file(path: str, info: dict) -> None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return
    header = (
        f"\n---\nCommit: {info['hash'][:7]}\n"
        f"Title: {info['subject']}\nDate: {info['date']}\n---\n\n"
    )
    if "\n---\nCommit:" not in content:
        content = content + header
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def rename_pending(path: str, info: dict) -> str:
    dirn, base = os.path.split(path)
    _ = base[:-len("--PENDING.md")]  # strip suffix
    title = info["subject"]
    seq, date = find_seq_and_date_from_worklog(title)
    if seq is not None and date is not None:
        new_base = f"[{seq:04d}] {date} — {sanitize_filename(title)}.md"
    else:
        new_base = f"{sanitize_filename(title)}.md"
    new_path = os.path.join(dirn, new_base)
    # Avoid overwrite
    if os.path.exists(new_path):
        ts = datetime.now().strftime("%H%M%S")
        new_base = f"{new_base[:-3]}--{ts}.md"
        new_path = os.path.join(dirn, new_base)
    os.rename(path, new_path)
    return new_path


def main() -> int:
    info = get_last_commit()
    if not info["hash"] or not info["subject"]:
        return 0
    pendings = find_pending_files()
    if not pendings:
        return 0
    # annotate and rename all pendings
    for p in pendings:
        annotate_file(p, info)
        rename_pending(p, info)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
