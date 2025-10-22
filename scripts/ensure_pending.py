#!/usr/bin/env python3
from __future__ import annotations
import os
import re
from datetime import datetime
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "docs", "REQUESTS")
WLOG_DIR = os.path.join(ROOT, "docs", "WORKLOGS")


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT).decode("utf-8", errors="replace")


def get_prev_subject() -> str:
    try:
        out = run(["git", "log", "-1", "--pretty=%s"]).strip()
        return out if out else "처음"
    except Exception:
        return "처음"


def sanitize_filename(text: str, maxlen: int = 128) -> str:
    text = text.strip()
    text = text.replace("/", "／").replace("\\", "＼")
    text = re.sub(r"\s+", " ", text)
    if len(text) > maxlen:
        text = text[:maxlen].rstrip()
    return text or "제목"


def ensure_single_pending(dirpath: str, prev_subject: str, prefix: str) -> None:
    os.makedirs(dirpath, exist_ok=True)
    pendings = [fn for fn in os.listdir(dirpath) if fn.endswith("--PENDING.md")]
    if len(pendings) > 1:
        raise SystemExit(f"[ensure-pending] {dirpath} 에 PENDING 파일이 {len(pendings)}개 있습니다. 하나만 유지하세요.")
    if len(pendings) == 0:
        date = datetime.now().strftime("%Y-%m-%d")
        base = f"{date}--after-{sanitize_filename(prev_subject)}--PENDING.md"
        path = os.path.join(dirpath, base)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {prefix} 요약 (PENDING)\n\n이전 커밋: {prev_subject}\n\n")


def main() -> int:
    prev = get_prev_subject()
    ensure_single_pending(REQ_DIR, prev, "요청/대화")
    ensure_single_pending(WLOG_DIR, prev, "작업 로그")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

