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
    "第1部 テスティングフレームワークとは": ["全体像", "アーキテクチャ", "テストの種類", "テストデータ", "対象範囲", "稼動環境"],
    "第2部 導入と設定": ["機能概要", "使用方法", "拡張例"],
    "第3部 テストの実装方法": ["機能概要", "使用方法"],
    "第4部 ツール": ["機能概要", "導入", "使用方法"],
}

# (dest_part, dest_page) — ページ単位。design.mdがこのページ自体を0件になる
# 設計として定めている場合のみここに載せる。理由には必ずdesign.mdの該当箇所を引用する。
EXPECTED_ZERO_PAGES = {
    ("第2部 導入と設定", "リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）"):
        "design.md §6「中身は導線のみとする」。独自の設定内容を持たない",
    ("第2部 導入と設定", "取引単体テストの設定（テーブルをキューとして使ったメッセージング）"): "同上",
    ("第3部 テストの実装方法", "リクエスト単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
    ("第3部 テストの実装方法", "取引単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
}

# (dest_part, dest_page, dest_section) — セクション単位。design.mdがこのセクション
# 自体を0件になる設計として定めている場合のみここに載せる。
EXPECTED_ZERO_SECTIONS = {
    ("第4部 ツール", "HTMLチェックツール", "導入"):
        "design.md §5「インストール手順を持たないため『導入』セクションは設けず」",
}

# #6のユーザー判断を待っている0件（ページ単位2-tuple／セクション単位3-tuple）。
# STEP 2・STEP 4で判明したものをここに追記する。理由には必ず#6のどの未確定事項に
# 対応するかを書く。根拠・実測は checks/task-05b.md 参照。
PENDING_ZERO = {
    # --- STEP 4 報告項目1: 第1部「稼動環境」0件 ---
    ("第1部 テスティングフレームワークとは", "テスティングフレームワークとは", "稼動環境"):
        "design.md §2「モジュール一覧の集約」は依存関係を本セクションに集約すると定めるが、"
        "該当候補(current-0180/current-0267)は既に第2部JUnit5用拡張機能ページに割当済みで"
        "移動の要否は#6未確定事項#1（第2部のページ分割）と連動する。『Java・Jakarta EEの要件』は"
        "出典なし（grep 0件）。#6でA/B/C案（checks/task-05b.md）から選択し確定する。",

    # --- STEP 4 報告項目2: 第2部「テストデータの形式」0件 ---
    ("第2部 導入と設定", "テストデータの形式"):
        "design.md §3はExcel/YAMLの比較・使い分け・YAML設定を役割とするが実測0行。"
        "既存の関連記述は第3部テストデータの書き方/記載例へMERGE済み。ページ新設か第3部への"
        "統合かは#6未確定事項#1（第2部のページ分割）確定時に判断する。",

    # --- STEP 4 報告項目3: 取引単体テストの設定 2ページ 0件 ---
    ("第2部 導入と設定", "取引単体テストの設定（ウェブアプリケーション）"):
        "#6未確定事項#2（取引単体テストのページ構成）の確定待ち。current-0158と同様、"
        "取引単体テスト設定の受け皿ページ自体が暫定語彙であり、内容の有無以前にページ構成が未確定。",
    ("第2部 導入と設定", "取引単体テストの設定（Nablarchバッチアプリケーション）"):
        "同上（#6未確定事項#2）。",

    # --- STEP 2 再判定: 第2部「設定」系ページの機能概要/拡張例 ---
    # 実ファイル通読の結果、各処理方式の「概要/全体像/主なクラス」に相当する内容は
    # 第3部の対応ページ（実装方法）へ既に割当済みで、設定ページ側に重複させない限り
    # 独立した機能概要の出典が存在しない（design.md §3の機能概要定義「全体像(図)/
    # 主なクラスとリソース/前提事項」に合う専用記述が現行資料側に無い）。同様に
    # 拡張例（<拡張手順>する）に該当する内容も無く、既存行はすべて「設定」（使用方法）。
    # 第2部のページ split が#6で確定した際に、設定ページの機能概要の扱い（新規執筆にするか
    # セクション自体を持たないことにするか）を#6未確定事項#1と合わせて判断する。
    ("第2部 導入と設定", "クラス単体テストの設定", "機能概要"):
        "出典なし（実ファイル通読済み、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "クラス単体テストの設定", "拡張例"):
        "出典なし（同上）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "共通設定", "機能概要"):
        "出典なし（03_Tips.rst由来の個別設定断片のみ、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "共通設定", "拡張例"):
        "出典なし（同上）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（ウェブアプリケーション）", "機能概要"):
        "出典なし。概要/全体像/主なクラス相当の内容(current-0199〜0202)は第3部リクエスト単体テスト"
        "（ウェブアプリケーション）に割当済みで重複させられない。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（RESTfulウェブサービス）", "機能概要"):
        "出典なし。同様に概要相当(current-0307〜0309)は第3部側に割当済み。current-0310/0311は"
        "モジュール一覧・設定というdesign.md使用方法定義の内容で機能概要には該当しない。"
        "#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（RESTfulウェブサービス）", "拡張例"):
        "出典なし。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（HTTPメッセージング）", "機能概要"):
        "出典なし（設定内容のみ、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（HTTPメッセージング）", "拡張例"):
        "出典なし（同上）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（Nablarchバッチアプリケーション）", "機能概要"):
        "出典なし（同上）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（Nablarchバッチアプリケーション）", "拡張例"):
        "出典なし（同上）。#6未確定事項#1の確定と合わせて判断。",
    ("第2部 導入と設定", "リクエスト単体テストの設定（MOMによるメッセージング）", "機能概要"):
        "出典なし（拡張例は既存7行で充足済み、機能概要のみ出典なし）。#6未確定事項#1の確定と合わせて判断。",

    # --- STEP 2 再判定: 取引単体テストの設定（HTTP/MOM）の機能概要/拡張例 ---
    ("第2部 導入と設定", "取引単体テストの設定（HTTPメッセージング）", "機能概要"):
        "出典なし（設定内容のみ、checks/task-05b.md）。#6未確定事項#2の確定と合わせて判断。",
    ("第2部 導入と設定", "取引単体テストの設定（HTTPメッセージング）", "拡張例"):
        "出典なし（同上）。#6未確定事項#2の確定と合わせて判断。",
    ("第2部 導入と設定", "取引単体テストの設定（MOMによるメッセージング）", "機能概要"):
        "出典なし（同上）。#6未確定事項#2の確定と合わせて判断。",
    ("第2部 導入と設定", "取引単体テストの設定（MOMによるメッセージング）", "拡張例"):
        "出典なし（同上）。#6未確定事項#2の確定と合わせて判断。",

    # --- STEP 2 再判定: マスタデータ復旧機能の拡張例 ---
    ("第2部 導入と設定", "マスタデータ復旧機能", "拡張例"):
        "出典なし。04_MasterDataRestore.rst全215行は機能概要4行・使用方法6行のみで構成され、"
        "拡張（クラス差し替え等）に相当する記述が存在しない（実ファイル全文確認、checks/task-05b.md）。"
        "#6未確定事項#1の確定と合わせて、拡張例を持たないページとして扱うか判断する。",

    # --- STEP 2 再判定: 第3部テストデータの2ページの機能概要 ---
    # design.md §4「テストデータの2ページ」節は「役割」表のみを定義し、他の第3部ページに
    # 適用される「機能概要/使用方法」のページアウトラインへの言及が無い。#5時点でも
    # 既存noteに「この特殊2ページには機能概要相当のアウトラインがdesign.mdに定義されていない
    # ため」と明記され、3観点レビューを経て承認済み（batch-11 input-0058のnote参照）。
    # 一方でSTEP2の実ファイル調査により、機能概要の定義「このページで何ができるようになるか」に
    # 適合しうる候補（テストデータの書き方: input-0098/0099/0114、テストデータの記載例:
    # input-0036/0037/0058/0082/0093）が実在することも判明した。既承認の判断を#5bで独自に
    # 覆さず、候補の存在とdesign.mdの規定の欠落を#6に提示して判断を仰ぐ。
    ("第3部 テストの実装方法", "テストデータの書き方", "機能概要"):
        "design.md §4「テストデータの2ページ」に機能概要の定義がない（#5時点で承認済みの解釈）。"
        "一方でinput-0098/0099/0114（各資料のL1直下導入文・全体像節）が機能概要の定義"
        "「このページで何ができるようになるか」に適合しうる。新規未確定事項として#6提示。"
        "詳細はchecks/task-05b.md参照。",
    ("第3部 テストの実装方法", "テストデータの記載例", "機能概要"):
        "同上。候補: input-0036/0037/0058/0082/0093（各記述例ドキュメントのL1直下導入文）。"
        "新規未確定事項として#6提示。",

    # --- STEP 2 再判定: 第3部 取引単体テスト（Nablarchバッチアプリケーション）の機能概要 ---
    ("第3部 テストの実装方法", "取引単体テスト（Nablarchバッチアプリケーション）", "機能概要"):
        "current-0128（batch.rst 4-25、(L1直下)）はページ冒頭2行のみ概要的記述で、"
        "残り大部分（8-24行）はテストクラス作成条件・命名規則・コード例という使用方法の内容が"
        "同一セクションに混在する。#4a/#5bの対象外である新規SPLITを本タスクの権限で追加しない"
        "ため無理に分割・移動しない。#6で新規SPLIT対象として扱うか、機能概要なしのページとして"
        "扱うかを判断する。",

    # --- STEP 2 再判定: 第4部 テストデータ変換ツールの導入 ---
    ("第4部 ツール", "テストデータ変換ツール", "導入"):
        "design.md §5はHTMLチェックツールのみ導入セクション省略を明記しており、"
        "テストデータ変換ツールへの同様の言及はない。実ファイル通読（"
        "testdata-converter-design.md全362行）の結果、インストール手順・依存関係・設定に"
        "該当する記述は存在しない（該当候補input-0183/0184/0190は『解くべき課題』"
        "『形式に依存するか否か』という設計思想の説明で機能概要が正しい）。HTMLチェックツールと"
        "同様の例外をEXPECTED_ZERO_SECTIONSに追加するか、#6でdesign.md §5に明記するかを判断する。",
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

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    print("\nOK: no errors")


if __name__ == "__main__":
    main()
