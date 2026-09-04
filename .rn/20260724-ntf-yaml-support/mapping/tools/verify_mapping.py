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


CONTENT_BEARING = {"MOVE", "MERGE", "SPLIT"}


def check_reference_only_sections(rows):
    """mapping.csvが使う全(dest_part, dest_page, dest_section)のうち、
    CONTENT_BEARING（本文を持つdisposition）の行が1件も無いものを検出する。
    REFERENCEのみでセクションが充足されている状態は、design.md §11.6観点A
    「REFERENCEが本文を持っていないか」に照らして妥当な場合があるため、
    判定は人が行う（advisory出力。exit 1しない）。"""
    all_sections = defaultdict(int)
    content_bearing_sections = set()
    for r in rows:
        if r.get("disposition") == "DROP":
            continue
        dp = r.get("dest_part", "")
        pg = r.get("dest_page", "")
        sec = r.get("dest_section", "")
        if not (dp and pg and sec):
            continue
        key = (dp, pg, sec)
        all_sections[key] += 1
        if r.get("disposition") in CONTENT_BEARING:
            content_bearing_sections.add(key)

    ref_only = []
    for key in sorted(all_sections):
        if key not in content_bearing_sections:
            ref_only.append((key[0], key[1], key[2], all_sections[key]))
    return ref_only


INTRO_TAILS = {"(L1直下)", "(L2直下)", "(冒頭)"}
_INTRO_ERROR_TAIL = "(L2直下)"


def _heading_parent_and_tail(heading_path):
    parts = [p.strip() for p in (heading_path or "").split(">")]
    if not parts:
        return "", ""
    tail = parts[-1]
    parent = ">".join(parts[:-1]).strip()
    return parent, tail


def check_intro_section_split(rows):
    """導入文行（heading_pathが(L1直下)/(L2直下)/(冒頭)で終わる非DROP行）の
    dest_sectionが、同じsrc_file・同じ親heading_pathを持つ他の非DROP行（同階層行）
    のどのdest_sectionとも一致しない場合を検出する。dest_pageは比較しない
    — steering.md #5 Stepsの既存ルールが「同じ親を持つ配下セクションと同じ
    dest_sectionに置く」と定めるのはdest_section単位であり、design.md §4の
    記法統合方針により導入文と本体が意図的に別dest_page（同名dest_section）へ
    分かれる正当なケース（例: テストデータの書き方ページへの記法統合）を
    誤検出しないため。(L2直下)は既存ルールの明文違反のためERROR（exit 1）。
    (L1直下)/(冒頭)は明文ルールが無くページ作成時の書き直しで吸収できる場合が
    あるためadvisory。"""
    by_file_parent = defaultdict(list)
    for r in rows:
        if r.get("disposition") == "DROP":
            continue
        parent, tail = _heading_parent_and_tail(r.get("heading_path"))
        by_file_parent[(r.get("src_file", ""), parent)].append((r, tail))

    errors = []
    advisories = []
    for (src_file, parent), members in sorted(by_file_parent.items()):
        intro_members = [(r, tail) for r, tail in members if tail in INTRO_TAILS]
        if not intro_members:
            continue
        sibling_sections = {
            r.get("dest_section") for r, tail in members if tail not in INTRO_TAILS
        }
        if not sibling_sections:
            continue
        for r, tail in intro_members:
            dest_section = r.get("dest_section")
            if dest_section in sibling_sections:
                continue
            msg = (
                f"{r.get('mapping_id')} ({tail}): dest_section={dest_section!r} "
                f"not among sibling dest_section values {sorted(sibling_sections)}"
            )
            if tail == _INTRO_ERROR_TAIL:
                errors.append(msg)
            else:
                advisories.append({"msg": msg, "mapping_id": r.get("mapping_id")})
    return errors, advisories


INTRO_NOTE_MARK = "[セクション境界]"


def check_intro_note_present(rows, intro_advisories):
    """check_intro_section_splitがadvisoryとして報告した全行のnoteに
    [セクション境界]が含まれることを検証する。#5dでは advisory 4件に個別に
    noteを追記したが、#6でadvisoryが5件に増えた際に追記漏れ（current-0128-a）
    が発生した。件数固定の運用をやめ、advisory全件を機械的に突合することで
    将来advisoryが増減しても自動的に検出する（2026-07-28 #6レビュー指摘）。"""
    by_id = {r.get("mapping_id"): r for r in rows}
    errors = []
    for adv in intro_advisories:
        mapping_id = adv["mapping_id"]
        row = by_id.get(mapping_id)
        note = (row.get("note") if row else "") or ""
        if INTRO_NOTE_MARK not in note:
            errors.append(
                f"{mapping_id}: intro section split advisory is missing a "
                f"{INTRO_NOTE_MARK!r} note"
            )
    return errors


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
    """vocabulary.mdの全マークダウン表からdest_part単体の許容値集合と、
    dest_part×dest_page／dest_part×dest_sectionの許容組み合わせ集合を機械抽出する
    （確定・暫定の両方を含む）。

    どの`##`見出し配下の表かで dest_page 表か dest_section 表かを判定する。
    単純に「2列表の2列目を両方の集合に入れる」実装では、同じ語（例:
    `拡張例`）が第2部・第3部のdest_section表にだけ存在しても、部を無視した
    フラットな集合では第4部の行にも誤って一致してしまう（2026-07-28 ユーザー
    指摘）。dest_part とペアで照合することでこれを防ぐ。
    """
    path = os.path.join(MAPPING_DIR, "vocabulary.md")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    dest_parts = set()
    dest_page_pairs = set()
    dest_section_pairs = set()

    mode = None  # None | "page" | "section"
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("## dest_page"):
            mode = "page"
            continue
        if line.startswith("## dest_section"):
            mode = "section"
            continue
        if line.startswith("## "):
            mode = None
            continue
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or cols[0] in ("dest_part", "dest_page", "dest_section") or set(cols[0]) <= {"-", ":"}:
            continue
        # dest_part単独表（1列）。dest_part専用の"## dest_part"見出し配下に限らず
        # どこにあっても1列表は常にdest_part一覧として扱う。
        if len(cols) == 1 and cols[0].startswith("第"):
            dest_parts.add(cols[0])
            continue
        # dest_part + 値（2列以上、備考列があってもよい）表
        if len(cols) >= 2 and cols[0].startswith("第"):
            dest_parts.add(cols[0])
            if cols[1] and cols[1] != "備考":
                if mode == "page":
                    dest_page_pairs.add((cols[0], cols[1]))
                elif mode == "section":
                    dest_section_pairs.add((cols[0], cols[1]))

    return dest_parts, dest_page_pairs, dest_section_pairs


def check_vocabulary(rows):
    """dest_part/dest_page/dest_sectionがvocabulary.mdに存在する値・組み合わせで
    あることを検証する（disposition=MOVE/MERGE/SPLITの行が対象）。dest_page/
    dest_sectionはdest_partとの組み合わせで照合する（部をまたいだ誤一致を防ぐ）。"""
    errors = []
    dest_parts, dest_page_pairs, dest_section_pairs = _load_vocabulary()
    for r in rows:
        if r.get("disposition") not in ("MOVE", "MERGE", "SPLIT"):
            continue
        sid = r.get("mapping_id")
        dp = r.get("dest_part", "")
        pg = r.get("dest_page", "")
        sec = r.get("dest_section", "")
        if dp and dp not in dest_parts:
            errors.append(f"{sid}: dest_part {dp!r} not in vocabulary.md")
        if pg and (dp, pg) not in dest_page_pairs:
            errors.append(f"{sid}: dest_page {pg!r} not in vocabulary.md for dest_part {dp!r}")
        if sec and (dp, sec) not in dest_section_pairs:
            errors.append(f"{sid}: dest_section {sec!r} not in vocabulary.md for dest_part {dp!r}")
    return errors


SECTION_TEMPLATE = {
    "第1部 テスティングフレームワークとは": ["全体像", "アーキテクチャ", "テストの種類", "対象範囲", "稼動環境"],
    # 第2部は#6でdesign.md §3が改訂され「使用方法」のみ必須（機能概要・拡張例は任意）に
    # 変更された。機能概要・拡張例の0件検出をやめるわけではなく、
    # check_part2_optional_sections()がadvisoryとして出力し続ける（下記参照）。
    "第2部 導入と設定": ["使用方法"],
    "第3部 テストの実装方法": ["機能概要", "使用方法"],
    "第4部 ツール": ["機能概要", "導入", "使用方法"],
}

# (dest_part, dest_page) — ページ単位。design.mdがこのページ自体を0件になる
# 設計として定めている場合のみここに載せる。理由には必ずdesign.mdの該当箇所を引用する。
EXPECTED_ZERO_PAGES = {
    ("第2部 導入と設定", "リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）"):
        "design.md §6「中身は導線のみとする」。独自の設定内容を持たない",
    ("第3部 テストの実装方法", "リクエスト単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
    ("第3部 テストの実装方法", "取引単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
    # 第2部「取引単体テストの設定（テーブルをキューとして使ったメッセージング）」は#6で
    # ページ自体を廃止した（design.md §3「取引単体テストの設定は実データのある3処理方式
    # のみページ化する」）。vocabulary.mdから削除済みのためcheck_unused_vocabularyの
    # 対象外になり、ここへの登録は不要（登録するとstale allowlist検出が意味を持たない
    # まま残り続ける）。
}

# (dest_part, dest_page, dest_section) — セクション単位。design.mdがこのセクション
# 自体を0件になる設計として定めている場合のみここに載せる。
EXPECTED_ZERO_SECTIONS = {
    ("第4部 ツール", "HTMLチェックツール", "導入"):
        "design.md §5「インストール手順を持たないため『導入』セクションは設けず」",
    ("第4部 ツール", "テストデータ変換ツール", "導入"):
        "design.md §5「テストデータ変換ツールも『導入』を持たない。出典（testdata-converter-design.md"
        "全362行）にインストール手順・依存関係・設定に該当する記述が存在しないため」（#6確定）",
    ("第3部 テストの実装方法", "テストデータの記載例", "機能概要"):
        "design.md §4「テストデータの2ページ」。候補5件（各カテゴリ別記述例文書のL1直下"
        "導入文）はいずれも個別カテゴリの導入文であり、ページ全体を対象にした出典が存在"
        "しないため機能概要を持たない例外ページとして確定（#6確定、checks/task-06.md分類6参照）",
    ("第1部 テスティングフレームワークとは", "テスティングフレームワークとは", "稼動環境"):
        "design.md §2「モジュール一覧の集約」2026-08-05改訂。JUnit 5用拡張機能／JUnit Vintageの依存関係"
        "（current-0180/0267）は第2部「JUnit 5用拡張機能」使用方法へ差し戻し、本ページの「稼動環境」は"
        "選択基準の要約と`:ref:`のみとする（特徴3点目Excel/YAMLと同型の summary+ref パターン）",
}

# #6のユーザー判断を待っている0件（ページ単位2-tuple／セクション単位3-tuple）。
# `#6`（未確定事項の確定）により26件すべて解消済み（内訳: ①第1部稼動環境=解消
# （current-0180/0267割当）、②③廃止3ページ=語彙から削除、第2部設定ページの機能概要/
# 拡張例17件=SECTION_TEMPLATEから外れ任意化・check_part2_optional_sections()の
# advisoryへ移行、テストデータの書き方機能概要=解消（input-0114割当）、
# テストデータの記載例機能概要=EXPECTED_ZERO_SECTIONSへ、取引単体テスト
# （Nablarchバッチアプリケーション）機能概要=解消（current-0128-a割当）、
# テストデータ変換ツール導入=EXPECTED_ZERO_SECTIONSへ。詳細はchecks/task-06.md参照）。
PENDING_ZERO = {
}


def check_unused_vocabulary(rows):
    """vocabulary.mdが定義している(dest_part, dest_page)・(dest_part, dest_page,
    dest_section)のうち、mapping.csvで1件も使われていない組み合わせを検出する。
    check_vocabularyは逆方向（使われている値が語彙にあるか）しか見ておらず、
    「語彙にあるのに使われていない」を見落とすため別関数として追加する
    （2026-07-28 横断点検「dest_section=導入」0件と同型の欠陥への対応）。"""
    errors = []
    pending = []

    dest_parts, dest_page_pairs, dest_section_pairs = _load_vocabulary()

    used_pages = defaultdict(int)
    used_page_sections = defaultdict(int)
    for r in rows:
        if r.get("disposition") == "DROP":
            continue
        dp = r.get("dest_part", "")
        pg = r.get("dest_page", "")
        sec = r.get("dest_section", "")
        if dp and pg:
            used_pages[(dp, pg)] += 1
        if dp and pg and sec:
            used_page_sections[(dp, pg, sec)] += 1

    for dp, pg in sorted(dest_page_pairs):
        if used_pages.get((dp, pg), 0) > 0:
            continue
        key = (dp, pg)
        if key in EXPECTED_ZERO_PAGES:
            continue
        if key in PENDING_ZERO:
            pending.append(f"page [{dp} > {pg}]: {PENDING_ZERO[key]}")
            continue
        errors.append(
            f"page [{dp} > {pg}]: 0 non-DROP rows assigned "
            "(not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)"
        )

    for dp, pg in sorted(used_pages):
        template = SECTION_TEMPLATE.get(dp)
        if not template:
            continue
        for sec in template:
            if used_page_sections.get((dp, pg, sec), 0) > 0:
                continue
            key = (dp, pg, sec)
            if key in EXPECTED_ZERO_SECTIONS:
                continue
            if key in PENDING_ZERO:
                pending.append(f"section [{dp} > {pg} > {sec}]: {PENDING_ZERO[key]}")
                continue
            errors.append(
                f"section [{dp} > {pg} > {sec}]: 0 non-DROP rows assigned "
                "(not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)"
            )

    # 許可リストの陳腐化検出。0件として登録済みのキーに行が入った場合、
    # 許可リスト・volume.md・checks/task-05b.md が古くなったまま気づけない
    # （上のループはいずれも「使用数>0ならcontinue」で始まるため素通りする）。
    # 2026-07-28 #5c STEP 0 で追加。
    for key in list(EXPECTED_ZERO_PAGES) + [k for k in PENDING_ZERO if len(k) == 2]:
        n = used_pages.get(key, 0)
        if n > 0:
            errors.append(
                f"stale allowlist: page [{key[0]} > {key[1]}] has {n} non-DROP row(s) "
                "but is registered as zero (EXPECTED_ZERO_PAGES / PENDING_ZERO)"
            )
    for key in list(EXPECTED_ZERO_SECTIONS) + [k for k in PENDING_ZERO if len(k) == 3]:
        n = used_page_sections.get(key, 0)
        if n > 0:
            errors.append(
                f"stale allowlist: section [{key[0]} > {key[1]} > {key[2]}] has {n} "
                "non-DROP row(s) but is registered as zero "
                "(EXPECTED_ZERO_SECTIONS / PENDING_ZERO)"
            )

    return errors, pending


PART2_OPTIONAL_SECTIONS = ["機能概要", "拡張例"]


def check_part2_optional_sections(rows):
    """第2部の各ページについて、任意セクション（機能概要/拡張例）の行数が0件のものを
    advisoryとして一覧する。#6でSECTION_TEMPLATE["第2部 導入と設定"]を["使用方法"]のみに
    変更し機能概要・拡張例を必須から外したが、0件検出そのものはやめない。任意化に
    よって将来の割当漏れが見えなくなるのを防ぐため、reference-only sectionsと同じ
    advisory出力として一覧を出し続ける（exit 1しない）。"""
    used_page_sections = defaultdict(int)
    used_pages = set()
    for r in rows:
        if r.get("disposition") == "DROP":
            continue
        dp = r.get("dest_part", "")
        pg = r.get("dest_page", "")
        sec = r.get("dest_section", "")
        if dp != "第2部 導入と設定" or not pg:
            continue
        used_pages.add(pg)
        if sec:
            used_page_sections[(pg, sec)] += 1

    advisories = []
    for pg in sorted(used_pages):
        for sec in PART2_OPTIONAL_SECTIONS:
            if used_page_sections.get((pg, sec), 0) == 0:
                advisories.append(f"[第2部 導入と設定 > {pg} > {sec}]: 0 row(s) (optional since #6, not an error)")
    return advisories


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
        unused_errors, unused_pending = check_unused_vocabulary(rows)
        errors += unused_errors
        print(f"\npending zero assignments: {len(unused_pending)} (awaiting #6 decision)")
        for p in unused_pending:
            print(" -", p)

    total, total_excl_drop = line_totals(rows)
    print(f"lines total (all rows): {total}")
    print(f"lines total (excluding DROP): {total_excl_drop}")

    dup_findings = check_duplicate_destinations(rows)
    print(f"\ncandidate duplicate destinations: {len(dup_findings)} (advisory only, not auto-fixed)")
    for f in dup_findings:
        members = ", ".join(f"{sid}->{dest}({src})" for sid, dest, src in f["members"])
        print(f" - [{f['method']}] {f['key']!r}: {members}")

    ref_only = check_reference_only_sections(rows)
    print(f"\nreference-only sections: {len(ref_only)} (advisory only, not auto-fixed)")
    for part, page, section, n in ref_only:
        print(f" - [{part} > {page} > {section}]: {n} row(s), all non content-bearing")

    intro_errors, intro_advisories = check_intro_section_split(rows)
    errors += intro_errors
    print(f"\nintro section split advisories: {len(intro_advisories)} (not auto-fixed)")
    for a in intro_advisories:
        print(" -", a["msg"])
    # advisory 全件が [セクション境界] note を持つことを担保する。
    # #5d では4件を個別に追記したが、#6 で advisory が5件に増えた際に追記漏れが発生した。
    # 件数固定の運用をやめ、機械検査で担保する（2026-07-28 #6 レビュー指摘）。
    errors += check_intro_note_present(rows, intro_advisories)

    part2_optional = check_part2_optional_sections(rows)
    print(f"\npart2 optional sections (機能概要/拡張例) zero count: {len(part2_optional)} (advisory only, not an error)")
    for a in part2_optional:
        print(" -", a)

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    print("\nOK: no errors")


if __name__ == "__main__":
    main()
