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


def _load_sections(name):
    path = os.path.join(MAPPING_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return {r["section_id"]: r for r in csv.DictReader(f)}


def check_coverage(rows):
    """sections-current.csv/sections-input.csvの全section_idがmapping.csvに
    最低1回現れ、紐づく全マッピング行の行範囲の和集合が元セクションの
    body_start_line〜body_end_lineと過不足なく一致することを検証する。"""
    errors = []
    sections = {}
    sections.update(_load_sections("sections-current.csv"))
    sections.update(_load_sections("sections-input.csv"))

    by_section = defaultdict(list)
    for r in rows:
        sid = r.get("src_section_id")
        if not sid:
            continue
        try:
            start = int(r["src_body_start"])
            end = int(r["src_body_end"])
        except (KeyError, ValueError, TypeError):
            errors.append(f"{r.get('mapping_id')}: src_body_start/src_body_end is not an integer")
            continue
        by_section[sid].append((start, end, r.get("mapping_id")))

    missing = sorted(set(sections) - set(by_section))
    for sid in missing:
        errors.append(f"{sid}: appears in sections-*.csv but has no mapping.csv row")

    for sid, ranges in by_section.items():
        section = sections.get(sid)
        if section is None:
            errors.append(f"{sid}: appears in mapping.csv but not in sections-*.csv")
            continue
        expected_start = int(section["body_start_line"])
        expected_end = int(section["body_end_line"])
        covered = set()
        overlap_found = False
        for start, end, mapping_id in sorted(ranges):
            span = set(range(start, end + 1))
            if covered & span:
                errors.append(f"{sid}: mapping rows overlap in line range (see {mapping_id})")
                overlap_found = True
            covered |= span
        expected = set(range(expected_start, expected_end + 1))
        if not overlap_found and covered != expected:
            gap = expected - covered
            extra = covered - expected
            detail = []
            if gap:
                detail.append(f"gap={sorted(gap)[:10]}{'...' if len(gap) > 10 else ''}")
            if extra:
                detail.append(f"extra={sorted(extra)[:10]}{'...' if len(extra) > 10 else ''}")
            errors.append(f"{sid}: coverage mismatch ({', '.join(detail)})")

    return errors


_VOCAB_TABLE_RE = re.compile(r"^\|\s*(.+?)\s*\|")


def _load_vocabulary():
    """vocabulary.mdの全マークダウン表からdest_part/dest_page/dest_sectionの
    許容値集合を機械抽出する（確定・暫定の両方を含む）。"""
    path = os.path.join(MAPPING_DIR, "vocabulary.md")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    dest_parts = set()
    dest_pages = set()
    dest_sections = set()

    for line in lines:
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or cols[0] in ("dest_part", "dest_page", "dest_section") or set(cols[0]) <= {"-", ":"}:
            continue
        # dest_part単独表（1列）
        if len(cols) == 1 and cols[0].startswith("第"):
            dest_parts.add(cols[0])
            continue
        # dest_part/dest_page（2列以上、備考列があってもよい）表
        if len(cols) >= 2 and cols[0].startswith("第"):
            dest_parts.add(cols[0])
            if cols[1] and cols[1] != "備考":
                # dest_page表かdest_section表かはヘッダ文脈依存のため両方に登録候補として保持
                dest_pages.add(cols[1])
                dest_sections.add(cols[1])

    # dest_section確定表は見出し語（機能概要/使用方法/拡張例/全体像等）のみで
    # dest_pageと重ならないため、上の緩い抽出で両方に入れても実害はない
    # （dest_page側に紛れ込む「機能概要」等はdest_page値としては使われないため）。
    return dest_parts, dest_pages, dest_sections


def check_vocabulary(rows):
    """dest_part/dest_page/dest_sectionがvocabulary.mdに存在する値のみである
    ことを検証する（disposition=MOVE/MERGE/SPLITの行が対象）。"""
    errors = []
    dest_parts, dest_pages, dest_sections = _load_vocabulary()
    for r in rows:
        if r.get("disposition") not in ("MOVE", "MERGE", "SPLIT"):
            continue
        sid = r.get("mapping_id")
        dp = r.get("dest_part", "")
        pg = r.get("dest_page", "")
        sec = r.get("dest_section", "")
        if dp and dp not in dest_parts:
            errors.append(f"{sid}: dest_part {dp!r} not in vocabulary.md")
        if pg and pg not in dest_pages:
            errors.append(f"{sid}: dest_page {pg!r} not in vocabulary.md")
        if sec and sec not in dest_sections:
            errors.append(f"{sid}: dest_section {sec!r} not in vocabulary.md")
    return errors


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
    if files == [MAPPING_CSV]:
        # 取りこぼし検証・vocabulary突合はmapping.csv統合後のみ意味を持つ
        # （バッチ単位では対象セクションの一部しか含まれないため）。
        errors += check_coverage(rows)
        errors += check_vocabulary(rows)

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
