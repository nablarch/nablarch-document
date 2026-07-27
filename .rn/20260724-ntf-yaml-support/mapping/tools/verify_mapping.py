#!/usr/bin/env python3
import csv
import glob
import os
import re
import subprocess
import sys
from collections import defaultdict

MAPPING_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_CSV = os.path.join(MAPPING_DIR, "mapping.csv")
BATCH_DIR = os.path.join(MAPPING_DIR, "_batch")
REPO_ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=MAPPING_DIR, text=True
).strip()

DUP_TARGET_RE = re.compile(r"(current|input)-\d{4}")

# current側セクションの実体はこの基準コミットから取得する（作業ツリーは削除タスク#7で
# 変わりうるため固定）。環境変数 NTF_BASE_COMMIT で上書き可能。
DEFAULT_BASE_COMMIT = "c24190607fef5d76c607aa08b36d2ab2f813efe5"
BASE_COMMIT_ENV = "NTF_BASE_COMMIT"

_PLACEHOLDER_TAIL_RE = re.compile(r"^\(.+\)$")
_FILE_CACHE = {}


def base_commit():
    override = os.environ.get(BASE_COMMIT_ENV, "").strip()
    return override or DEFAULT_BASE_COMMIT


def load_rows():
    if os.path.exists(MAPPING_CSV):
        with open(MAPPING_CSV, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), [MAPPING_CSV]
    files = sorted(glob.glob(os.path.join(BATCH_DIR, "batch-*.csv")))
    rows = []
    for path in files:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["_source_file"] = os.path.basename(path)
                rows.append(row)
    return rows, files


def check_duplicate_citation(rows):
    errors = []
    for row in rows:
        if row.get("disposition") != "DROP":
            continue
        note = row.get("note", "")
        if "重複" in note and not DUP_TARGET_RE.search(note):
            errors.append(
                f"{row.get('src_section_id')} ({row.get('_source_file', 'mapping.csv')}): "
                f"note contains '重複' but cites no current-XXXX/input-XXXX target"
            )
    return errors


def check_required_fields(rows):
    errors = []
    for row in rows:
        sid = row.get("src_section_id")
        src = row.get("_source_file", "mapping.csv")
        if not row.get("disposition"):
            errors.append(f"{sid} ({src}): disposition is empty")
        if not row.get("audience"):
            errors.append(f"{sid} ({src}): audience is empty")
        if row.get("disposition") == "DROP" and not row.get("note"):
            errors.append(f"{sid} ({src}): DROP row has no note")
    return errors


def _file_lines(src_type, src_file):
    key = (src_type, src_file)
    if key in _FILE_CACHE:
        return _FILE_CACHE[key]
    if src_type == "current":
        text = subprocess.run(
            ["git", "show", f"{base_commit()}:{src_file}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    else:
        with open(os.path.join(REPO_ROOT, src_file), encoding="utf-8") as f:
            text = f.read()
    lines = text.splitlines()
    _FILE_CACHE[key] = lines
    return lines


def _body_prefix(row, length=40):
    try:
        start = int(row["src_body_start"])
        end = int(row["src_body_end"])
    except (KeyError, ValueError, TypeError):
        return None
    try:
        lines = _file_lines(row.get("src_type"), row.get("src_file"))
    except Exception:
        return None
    body = " ".join(l.strip() for l in lines[start - 1 : end] if l.strip())
    body = body.strip()
    return body[:length] if body else None


def _heading_tail(row):
    heading_path = row.get("heading_path", "") or ""
    parts = [p.strip() for p in heading_path.split(">")]
    tail = parts[-1] if parts else ""
    if not tail or _PLACEHOLDER_TAIL_RE.match(tail):
        return None
    return tail


def check_duplicate_destinations(rows):
    """同一内容が複数のdest_pageにMOVE/MERGEされていないかを検出する。
    自動修正はしない — 検出した組を一覧として返し、判断は人が行う。"""
    placed = [r for r in rows if r.get("disposition") in ("MOVE", "MERGE")]

    by_tail = defaultdict(list)
    by_prefix = defaultdict(list)
    for r in placed:
        tail = _heading_tail(r)
        if tail:
            by_tail[tail].append(r)
        prefix = _body_prefix(r)
        if prefix:
            by_prefix[prefix].append(r)

    findings = []
    seen_pairs = set()
    for method, groups in (("heading_path末尾一致", by_tail), ("本文先頭40文字一致", by_prefix)):
        for key, members in groups.items():
            dest_pages = {m.get("dest_page", "") for m in members}
            if len(members) < 2 or len(dest_pages) < 2:
                continue
            ids = tuple(sorted(m.get("src_section_id", "") for m in members))
            if (method, ids) in seen_pairs:
                continue
            seen_pairs.add((method, ids))
            findings.append(
                {
                    "method": method,
                    "key": key,
                    "members": [
                        (m.get("src_section_id"), m.get("dest_page"), m.get("_source_file", "mapping.csv"))
                        for m in members
                    ],
                }
            )
    return findings


def line_totals(rows):
    total = 0
    total_excl_drop = 0
    for row in rows:
        try:
            n = int(row["lines"])
        except (KeyError, ValueError):
            continue
        total += n
        if row.get("disposition") != "DROP":
            total_excl_drop += n
    return total, total_excl_drop


def main():
    rows, files = load_rows()
    source = "mapping.csv" if files == [MAPPING_CSV] else f"{len(files)} batch file(s) in mapping/_batch/"
    print(f"Loaded {len(rows)} rows from {source}")

    errors = []
    errors += check_duplicate_citation(rows)
    errors += check_required_fields(rows)

    total, total_excl_drop = line_totals(rows)
    print(f"lines total (all rows): {total}")
    print(f"lines total (excluding DROP): {total_excl_drop}")

    dup_findings = check_duplicate_destinations(rows)
    print(f"\ncandidate duplicate destinations: {len(dup_findings)} (advisory only, not auto-fixed)")
    for f in dup_findings:
        members = ", ".join(f"{sid}->{dest}({src})" for sid, dest, src in f["members"])
        print(f" - [{f['method']}] {f['key']!r}: {members}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    print("\nOK: no errors")


if __name__ == "__main__":
    main()
