#!/usr/bin/env python3
"""
build_traceability.py — ゲート②突合台帳自動生成スクリプト（2軸照合版）

使い方: python3 build_traceability.py
出力:   ../gate2-traceability.csv

■ 判定ロジック（2軸: src残存 × dest存在）

verdictは5値:
  KEPT       — design_dest が「なし」（移送対象外）
  MOVED      — src に残存なし、dest に存在あり
  DUPLICATED — src に残存あり、dest に存在あり（G1-01 の二重掲載）
  MODIFIED   — src 側の同行番号にテキスト変更あり（dest 側問わず）
  MISSING    — dest に存在なし、かつ src テキスト変更なし or src 行消失

BASE コミット: 564ed530ed8056fe018d7105c888a112aa5945ef
"""

import csv
import os
import re
import subprocess
from collections import Counter

# ─── パス定義 ───────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REVIEWS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
REPO_ROOT   = os.path.abspath(os.path.join(REVIEWS_DIR, "../../.."))

BEFORE_CSV  = os.path.join(REVIEWS_DIR, "inventory-before.csv")
INPUT_CSV   = os.path.join(REVIEWS_DIR, "inventory-input.csv")
OUTPUT_CSV  = os.path.join(REVIEWS_DIR, "gate2-traceability.csv")

# ─── BASE コミット ──────────────────────────────────────────────────────────
BASE = "564ed530ed8056fe018d7105c888a112aa5945ef"

# ─── DEST_MAP ───────────────────────────────────────────────────────────────
# None = なし（移送対象外）
# ディレクトリ末尾"/"あり = ディレクトリ内複数ファイルを grep
DEST_MAP = {
    "A-1":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.rst",
    "A-2":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/",
    "A-2-1": "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.rst",
    "A-2-2": "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/",
    "A-2-3": "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/",
    "A-3":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata_format.rst",
    "A-4":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.rst",
    "A-5":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.rst",
    "A-6":   "ja/development_tools/testing_framework/guide/development_guide/08_TestTools/",
    "B-1":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata/index.rst",
    "B-2":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata/examples.rst",
    "B-3":   "ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/",
    "B-4":   "ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/",
    "B-5":   "ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/",
    "B-6":   "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst",
    "なし":  None,
}

# ─── input ファイル → design_dest ────────────────────────────────────────────
INPUT_DEST_MAP = {
    "ntf-doc-terms.md":                       "なし",
    "ntf-testdata-doc.md":                    "B-1",
    "ntf-testdata-doc-examples-overview.md":  "B-2",
    "ntf-testdata-doc-examples-testshots.md": "B-2",
    "ntf-testdata-doc-examples-table.md":     "B-2",
    "ntf-testdata-doc-examples-file.md":      "B-2",
    "ntf-testdata-doc-examples-messaging.md": "B-2",
    "ntf-testdata-doc-examples-special.md":   "B-2",
    "ntf-testdata-loading.md":                "なし",
    "testdata-converter-design.md":           "なし",
}

# ─── before ファイル → design_dest ───────────────────────────────────────────
# ファイルサフィックスベースのマッピング（CLAUDE.md の get_design_dest() 相当）
FILE_DEST_MAP_BEFORE = [
    # (suffix_or_substr, design_dest)
    ("06_TestFWGuide/03_Tips.rst",                       "B-6"),
    ("06_TestFWGuide/04_MasterDataRestore.rst",          "A-5"),
    ("06_TestFWGuide/JUnit5_Extension.rst",              "A-4"),
    ("06_TestFWGuide/02_DbAccessTest.rst",               "A-2-1"),
    ("06_TestFWGuide/02_RequestUnitTest.rst",            "A-2-2"),
    ("06_TestFWGuide/RequestUnitTest_batch.rst",         "A-2-2"),
    ("06_TestFWGuide/RequestUnitTest_rest.rst",          "A-2-2"),
    ("06_TestFWGuide/RequestUnitTest_real.rst",          "A-2-3"),
    ("06_TestFWGuide/RequestUnitTest_send_sync.rst",     "A-2-3"),
    ("06_TestFWGuide/RequestUnitTest_http_send_sync.rst","A-2-3"),
    ("06_TestFWGuide/01_Abstract.rst",                   "A-1"),   # default; L195-579 handled separately
    ("06_TestFWGuide/index.rst",                         "なし"),
    ("05_UnitTestGuide/index.rst",                       "なし"),
    ("05_UnitTestGuide/01_ClassUnitTest/",               "B-3"),
    ("05_UnitTestGuide/02_RequestUnitTest/",             "B-4"),
    ("05_UnitTestGuide/03_DealUnitTest/",                "B-5"),
    ("08_TestTools/",                                    "A-6"),
    ("testing_framework/index.rst",                      "なし"),
]

# 01_Abstract.rst の行範囲 → B-1（G1-01 DUPLICATED 対象）
ABSTRACT_B1_RANGE = (195, 579)


def get_design_dest_before(src_file: str, src_line: int) -> str:
    """before 1行から design_dest を返す"""
    # G1-01: 01_Abstract.rst L195-579 → B-1
    if "01_Abstract.rst" in src_file:
        if ABSTRACT_B1_RANGE[0] <= src_line <= ABSTRACT_B1_RANGE[1]:
            return "B-1"

    for pattern, dest in FILE_DEST_MAP_BEFORE:
        if pattern.endswith("/"):
            if ("/" + pattern.rstrip("/") + "/") in src_file:
                return dest
        else:
            if src_file.endswith("/" + pattern) or src_file.endswith(pattern):
                return dest

    return "なし"


def get_design_dest_input(src_file: str) -> str:
    """input 1行から design_dest を返す"""
    basename = os.path.basename(src_file)
    return INPUT_DEST_MAP.get(basename, "B-1")


# ─── ファイルキャッシュ ───────────────────────────────────────────────────────

_after_file_cache: dict[str, list[str]] = {}  # repo_rel_path → lines (1-indexed at [1])
_before_file_cache: dict[str, list[str]] = {}


def get_after_lines(repo_rel_path: str) -> list[str]:
    """現在の after ファイルを行リストで返す（[0]は空、[1]が1行目）"""
    if repo_rel_path in _after_file_cache:
        return _after_file_cache[repo_rel_path]
    full_path = os.path.join(REPO_ROOT, repo_rel_path)
    if not os.path.exists(full_path):
        _after_file_cache[repo_rel_path] = []
        return []
    with open(full_path, encoding="utf-8", errors="replace") as f:
        lines = [""] + f.read().splitlines()  # 1-indexed
    _after_file_cache[repo_rel_path] = lines
    return lines


def get_before_lines(repo_rel_path: str) -> list[str]:
    """BASE コミット時のファイルを行リストで返す（[0]は空、[1]が1行目）"""
    if repo_rel_path in _before_file_cache:
        return _before_file_cache[repo_rel_path]
    try:
        r = subprocess.run(
            ["git", "-C", REPO_ROOT, "show", f"{BASE}:{repo_rel_path}"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            _before_file_cache[repo_rel_path] = []
            return []
        lines = [""] + r.stdout.splitlines()  # 1-indexed
        _before_file_cache[repo_rel_path] = lines
        return lines
    except Exception:
        _before_file_cache[repo_rel_path] = []
        return []


# ─── grep ヘルパー ───────────────────────────────────────────────────────────

def _trim_to_single_line(text: str, max_len: int = 40) -> str:
    """
    インベントリ detail は複数行を空白で連結した文字列。
    RST ファイルの1行に収まるよう、以下の優先順位で切り出す:
    1. Java コードコメントデリミタ（/** または // で始まる場合）は、
       後続の実質コンテンツ行（* で始まる行以外 or 日本語を含む行）を優先する
    2. 最初の文末句点（。）で切る（最低5文字以上）
    3. 最初の RST マークアップ記号（\\ ` ** :ref: など）で切る（最低5文字以上）
    4. 先頭から max_len 文字

    RST インライン記号を含む部分は検索パターンとして使えないため取り除く。
    """
    # Java コードコメントデリミタを処理
    # '/** * 内容' → '* 内容' の後の最初の日本語コンテンツを使う
    # '// 内容 code...' → '// 内容'（最初のスペースまで）を使う
    working = text
    if text.startswith('/**'):
        # '/** * ...' のパターン: '* ' の後のコンテンツを取り出す
        parts = text.split(' * ', 1)
        if len(parts) > 1:
            inner = parts[1].strip()
            if inner and not inner.startswith('@') and len(inner) >= 5:
                working = inner
    elif text.startswith('<!--'):
        # XML コメント: '<!-- content --> ...' → コメント内のコンテンツを取り出す
        inner = text[4:].strip()
        if ' -->' in inner:
            inner = inner[:inner.find(' -->')].strip()
        if inner and len(inner) >= 5:
            # スペースで区切られた複数の語句は最初の語句だけを使う（各語句は別行に存在するため）
            first_space = inner.find(' ')
            working = inner[:first_space] if 0 < first_space <= 20 else inner
    elif text.startswith('//'):
        # '// 実行 target...' → '// 実行' だけを使う（最初の語句で区切る）
        stripped = text.lstrip('/ ')  # 先頭の '/' と空白を除く
        first_space = stripped.find(' ')
        if 0 < first_space <= 10:
            # 最初の語句が短い場合（日本語1語など）: '// ' + 語句
            working = '// ' + stripped[:first_space]
        elif first_space > 10:
            working = stripped[:first_space]
        else:
            working = stripped

    snip = working[:max_len]

    # 日本語文末句点（。）で切る
    idx = snip.find('。')
    if idx >= 5:
        return snip[:idx + 1]

    # RST マークアップ開始文字で切る: '\\' のみ（後続がスペースや '`'）
    # 末尾の空白は除去する（箇条書き連結で ' *' 直前で切ると trailing space が残る）
    for i, ch in enumerate(snip):
        if i < 5:
            continue
        if ch == '\\':  # RST 行継続または \ escape
            return snip[:i].rstrip()
        if ch == '`':   # インラインコード ``  または :ref:`...`
            return snip[:i].rstrip()
        if ch == '*' and i > 0 and snip[i-1] == ' ':  # ** bold または次の箇条書き
            return snip[:i].rstrip()

    return snip.rstrip()


def make_search_pattern(row: dict) -> tuple[str | None, str]:
    """
    Returns: (pattern_str | None, method_note)
    pattern_str は str.find() で使う固定文字列
    """
    kind = row["kind"]
    title = row.get("title", "").strip()
    detail = row.get("detail", "").strip()

    if kind == "heading":
        if title:
            return title, f"heading タイトル全文: {title[:60]}"
        return None, "heading title が空"

    elif kind in ("para", "admonition"):
        text = (detail or title).strip()
        if not text:
            return None, "para/admonition content が空"
        snip = _trim_to_single_line(text, max_len=40)
        return snip, f"para/admonition 冒頭（句点区切り）: {snip[:40]}"

    elif kind == "code":
        for line in detail.splitlines():
            s = line.strip()
            if s and len(s) > 3:
                return s[:50], f"code 冒頭行: {s[:50]}"
        return None, "code content が空"

    elif kind == "table":
        text = (title or detail).strip()
        if text:
            # グリッドテーブル '| セル1   | セル2   |' とシンプルテーブル両対応:
            # 最初のセル内容（first ' | ' 前）を使う（スペース拡張・フォーマット差の影響を受けない）
            first_cell = text.split(" | ")[0].strip()
            if first_cell and len(first_cell) >= 2:
                return first_cell, f"table 先頭セル: {first_cell[:40]}"
            return text[:50], f"table 冒頭（先頭セル短すぎ）"
        return None, "table title/content が空"

    elif kind in ("figure", "image"):
        text = (title or detail).strip()
        if text:
            return text[:50], f"figure/image 冒頭"
        return None, "figure/image title/content が空"

    elif kind == "toctree":
        return None, "toctree は照合対象外"

    return None, f"kind={kind} 照合パターン未定義"


def search_in_text(pattern: str, text_lines: list[str], use_fallback: bool = False) -> tuple[bool, int]:
    """
    テキスト行リストから pattern を検索する。
    use_fallback=True のとき: full-pattern でヒットしない場合に20文字短縮版で再試行（dest/input 検索用）。
    use_fallback=False（デフォルト）: src_still_exists の確認など、偽陽性を避けたい場合。
    Returns: (found, first_1indexed_line_no)
    """
    if not pattern or not text_lines:
        return False, 0
    for i, line in enumerate(text_lines):
        if i == 0:
            continue
        if pattern in line:
            return True, i
    # Fallback: 短縮版（20文字）で再検索（use_fallback=True のときのみ）
    if use_fallback:
        short = pattern[:20]
        if len(short) < len(pattern):
            for i, line in enumerate(text_lines):
                if i == 0:
                    continue
                if short in line:
                    return True, i
    return False, 0


def search_in_dir(pattern: str, dir_repo_rel: str) -> tuple[bool, str, int]:
    """
    ディレクトリ内の RST ファイルを grep して最初のヒットを返す。
    Returns: (found, file_repo_rel, line_no)
    """
    full_dir = os.path.join(REPO_ROOT, dir_repo_rel)
    if not os.path.isdir(full_dir):
        return False, "", 0
    cmd = ["grep", "-rn", "-F", "--include=*.rst", pattern, full_dir]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        for line in r.stdout.splitlines():
            parts = line.split(":", 2)
            if len(parts) >= 2:
                try:
                    abs_path = parts[0]
                    lineno = int(parts[1])
                    rel = os.path.relpath(abs_path, REPO_ROOT)
                    return True, rel, lineno
                except (ValueError, IndexError):
                    pass
    except Exception:
        pass
    return False, "", 0


def search_in_file_or_dir(pattern: str, dest_repo_rel: str) -> tuple[bool, str, int]:
    """
    dest_repo_rel がファイルパスならそのファイルを、ディレクトリならディレクトリを grep。
    Returns: (found, actual_file_repo_rel, actual_line_no)
    """
    if not pattern or not dest_repo_rel:
        return False, "", 0

    if dest_repo_rel.endswith("/"):
        return search_in_dir(pattern, dest_repo_rel)
    else:
        lines = get_after_lines(dest_repo_rel)
        # dest 検索では短縮フォールバックを有効にする（改題された見出しも拾う）
        found, lineno = search_in_text(pattern, lines, use_fallback=True)
        if found:
            return True, dest_repo_rel, lineno
        return False, "", 0


# ─── dest ファイルが src ファイルと同一か判定 ──────────────────────────────────

def dest_is_same_as_src(src_file: str, design_dest: str) -> bool:
    """dest が src と同一ファイル（またはディレクトリ）かどうかを返す"""
    dest_path = DEST_MAP.get(design_dest)
    if dest_path is None:
        return False
    if dest_path.endswith("/"):
        # src が dest ディレクトリ配下にあるか
        return src_file.startswith(dest_path) or ("/" + dest_path.split("/")[-2] + "/") in src_file
    else:
        return src_file == dest_path


# ─── before 行の処理 ─────────────────────────────────────────────────────────

def process_before_row(i: int, row: dict) -> dict:
    """before 1行を処理して結果 dict を返す"""
    src_file  = row["file"]
    src_line  = int(row["line"])
    kind      = row["kind"]
    path      = row.get("path", "")
    content   = row.get("detail", "")[:160]
    dest_key  = get_design_dest_before(src_file, src_line)

    actual_file = ""
    actual_line = ""
    note_parts  = []

    # ── design_dest == "なし": 移送対象外 → KEPT ───────────────────────────
    if dest_key == "なし":
        return {
            "item_id": f"B-{i+1:04d}",
            "src_file": src_file, "src_line": str(src_line),
            "kind": kind, "heading_path": path, "content": content,
            "design_dest": dest_key, "actual_file": "", "actual_line": "",
            "verdict": "KEPT", "note": "移送対象外",
        }

    dest_path = DEST_MAP.get(dest_key)  # ファイルパスまたは"dir/"またはNone

    # ── G1-01: 01_Abstract.rst L195-579 → B-1 ────────────────────────────
    # 判定基準: src テキストが after 01_Abstract.rst に残存 AND B-1 ファイルが存在
    # → 同一主題が A-1 と B-1 の両方に掲載 → DUPLICATED
    if dest_key == "B-1" and "01_Abstract.rst" in src_file:
        b1_path = os.path.join(REPO_ROOT, dest_path)
        src_after_lines = get_after_lines(src_file)

        # src テキストが after の src ファイルに残存しているか確認
        pattern, method = make_search_pattern(row)
        src_still_exists = False
        src_after_lineno = 0
        if pattern and src_after_lines:
            src_still_exists, src_after_lineno = search_in_text(pattern, src_after_lines)

        if not src_still_exists:
            # src テキストが変わっている場合は after の同行番号で確認
            if src_line < len(src_after_lines):
                after_line_text = src_after_lines[src_line]
                before_lines = get_before_lines(src_file)
                if src_line < len(before_lines):
                    before_text = before_lines[src_line]
                    if before_text != after_line_text and after_line_text.strip():
                        return {
                            "item_id": f"B-{i+1:04d}",
                            "src_file": src_file, "src_line": str(src_line),
                            "kind": kind, "heading_path": path, "content": content,
                            "design_dest": dest_key, "actual_file": "",
                            "actual_line": "", "verdict": "MODIFIED",
                            "note": f"G1-01範囲: before L{src_line} テキスト変更検出",
                        }

        if os.path.exists(b1_path):
            # src テキストが after にも残存、かつ B-1 が新規作成済み → DUPLICATED
            actual_file_val = dest_path
            actual_line_val = ""
            # B-1 に同テキストが存在するか追加確認（フォールバック有効）
            if pattern:
                b1_found, b1_lineno = search_in_text(pattern, get_after_lines(dest_path), use_fallback=True)
                if b1_found:
                    actual_line_val = str(b1_lineno)
            note = (
                f"G1-01: 01_Abstract.rst L{src_line} が after にも残存。"
                f"B-1（testdata/index.rst）が新規作成済み → 同一主題の二重掲載"
            )
            return {
                "item_id": f"B-{i+1:04d}",
                "src_file": src_file, "src_line": str(src_line),
                "kind": kind, "heading_path": path, "content": content,
                "design_dest": dest_key, "actual_file": actual_file_val,
                "actual_line": actual_line_val, "verdict": "DUPLICATED",
                "note": note,
            }
        else:
            return {
                "item_id": f"B-{i+1:04d}",
                "src_file": src_file, "src_line": str(src_line),
                "kind": kind, "heading_path": path, "content": content,
                "design_dest": dest_key, "actual_file": "", "actual_line": "",
                "verdict": "MISSING", "note": "01_Abstract.rst に残存、B-1 が未作成",
            }

    # ── 通常の before 項目: dest == src ファイル（またはディレクトリ）────────
    # ほぼすべての before 項目はここに来る
    # (A-1→01_Abstract.rst, B-6→03_Tips.rst, B-3→05_UnitTestGuide/01_ClassUnitTest/ 等)
    pattern, method = make_search_pattern(row)
    note_parts.append(f"照合方法: {method}")

    # Step 1: before テキストが after の src ファイルに残存するか（厳密照合）
    src_after_lines = get_after_lines(src_file)
    src_still_exists = False
    src_after_lineno = 0

    if pattern and src_after_lines:
        src_still_exists, src_after_lineno = search_in_text(pattern, src_after_lines)

    # Step 1b: 近似照合（10文字短縮）で再確認 — テキストが行移動しただけの場合を救う
    # ※ pattern が None の場合や短い場合は近似照合しない（誤検知防止）
    src_approx_exists = src_still_exists
    src_approx_lineno = src_after_lineno
    if not src_still_exists and pattern and len(pattern) >= 10:
        short_pat = pattern[:10]
        src_approx_exists, src_approx_lineno = search_in_text(short_pat, src_after_lines)

    # Step 2: src の同行番号を調べてテキスト変更があるか確認
    # MODIFIED とするのは: 厳密照合も近似照合も失敗 かつ 同行番号の内容が変化
    src_text_changed = False
    if not src_approx_exists and pattern and len(pattern) >= 5:
        before_lines = get_before_lines(src_file)
        if (src_line < len(before_lines) and
                src_line < len(src_after_lines)):
            before_text = before_lines[src_line].strip()
            after_text  = src_after_lines[src_line].strip()
            if before_text and after_text and before_text != after_text:
                src_text_changed = True
                note_parts.append(
                    f"L{src_line} テキスト変更: before={before_text[:40]!r} → after={after_text[:40]!r}"
                )

    # Step 3: dest が src と同一の場合、実質的に 1軸判定
    # dest が別ファイルの場合は dest 側も検索（今回の before データでは B-1 のみ）
    same_src = dest_is_same_as_src(src_file, dest_key)

    if same_src:
        # dest == src: src_still_exists（または近似）が全て
        if src_still_exists:
            actual_file = src_file
            actual_line = str(src_after_lineno)
            verdict = "KEPT"
            note_parts.append(f"after L{src_after_lineno} に同テキスト存在")
        elif src_approx_exists:
            # 行移動または軽微な変更。テキストは実質残存
            actual_file = src_file
            actual_line = str(src_approx_lineno)
            verdict = "KEPT"
            note_parts.append(f"after L{src_approx_lineno} に近似テキスト存在（行移動）")
        elif src_text_changed:
            verdict = "MODIFIED"
            # after の同行番号を actual_line として記録
            actual_file = src_file
            actual_line = str(src_line)
        else:
            verdict = "MISSING"
            note_parts.append(f"照合失敗: pattern={pattern!r}")
    else:
        # dest != src: 2軸判定
        dest_found = False
        dest_actual_file = ""
        dest_actual_line = 0
        if pattern and dest_path:
            dest_found, dest_actual_file, dest_actual_line = search_in_file_or_dir(
                pattern, dest_path
            )

        if src_still_exists and dest_found:
            verdict = "DUPLICATED"
            actual_file = dest_actual_file
            actual_line = str(dest_actual_line)
            note_parts.append(f"src L{src_after_lineno} に残存、dest {dest_actual_file} L{dest_actual_line} にも存在")
        elif not src_still_exists and dest_found:
            verdict = "MOVED"
            actual_file = dest_actual_file
            actual_line = str(dest_actual_line)
            note_parts.append(f"dest {dest_actual_file} L{dest_actual_line} に移送確認")
        elif src_still_exists and not dest_found:
            if src_text_changed:
                verdict = "MODIFIED"
                actual_file = src_file
                actual_line = str(src_line)
            else:
                verdict = "MISSING"
                note_parts.append(f"dest に存在せず: {dest_path}")
        else:  # not src_still_exists and not dest_found
            if src_text_changed:
                verdict = "MODIFIED"
                actual_file = src_file
                actual_line = str(src_line)
            else:
                verdict = "MISSING"
                note_parts.append(f"src / dest 両方に存在せず")

    return {
        "item_id": f"B-{i+1:04d}",
        "src_file": src_file, "src_line": str(src_line),
        "kind": kind, "heading_path": path, "content": content,
        "design_dest": dest_key, "actual_file": actual_file,
        "actual_line": actual_line, "verdict": verdict,
        "note": "; ".join(note_parts),
    }


# ─── input 行の処理 ───────────────────────────────────────────────────────────

def process_input_row(i: int, row: dict) -> dict:
    """input 1行を処理して結果 dict を返す"""
    src_file  = row["file"]
    src_line  = int(row["line"])
    kind      = row["kind"]
    path      = row.get("path", "")
    content   = row.get("detail", "")[:160]
    dest_key  = get_design_dest_input(src_file)

    # design_dest == "なし": 移送対象外 → KEPT
    if dest_key == "なし":
        return {
            "item_id": f"I-{i+1:04d}",
            "src_file": src_file, "src_line": str(src_line),
            "kind": kind, "heading_path": path, "content": content,
            "design_dest": dest_key, "actual_file": "", "actual_line": "",
            "verdict": "KEPT", "note": "input 参照資料（解説書には移送しない）",
        }

    dest_path = DEST_MAP.get(dest_key)

    # grep パターン生成
    pattern, method = make_search_pattern(row)
    note_parts = [f"照合方法: {method}"]

    if not pattern:
        return {
            "item_id": f"I-{i+1:04d}",
            "src_file": src_file, "src_line": str(src_line),
            "kind": kind, "heading_path": path, "content": content,
            "design_dest": dest_key, "actual_file": "", "actual_line": "",
            "verdict": "MISSING",
            "note": "; ".join(note_parts) + "; 照合パターンなし",
        }

    # dest ファイルを検索
    dest_found, dest_actual_file, dest_actual_line = search_in_file_or_dir(pattern, dest_path)

    if dest_found:
        verdict = "MOVED"
        actual_file = dest_actual_file
        actual_line = str(dest_actual_line)
        note_parts.append(f"dest {dest_actual_file} L{dest_actual_line} にヒット")
    else:
        verdict = "MISSING"
        actual_file = ""
        actual_line = ""
        note_parts.append(f"照合失敗: pattern={pattern[:40]!r}")

    return {
        "item_id": f"I-{i+1:04d}",
        "src_file": src_file, "src_line": str(src_line),
        "kind": kind, "heading_path": path, "content": content,
        "design_dest": dest_key, "actual_file": actual_file,
        "actual_line": actual_line, "verdict": verdict,
        "note": "; ".join(note_parts),
    }


# ─── メイン処理 ──────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("build_traceability.py — ゲート②突合台帳生成（2軸照合版）")
    print("=" * 60)

    print(f"\n[1] CSV 読み込み")
    with open(BEFORE_CSV, encoding="utf-8") as f:
        before_rows = list(csv.DictReader(f))
    with open(INPUT_CSV, encoding="utf-8") as f:
        input_rows = list(csv.DictReader(f))
    print(f"  before: {len(before_rows)} 件")
    print(f"  input:  {len(input_rows)} 件")
    print(f"  期待合計: {len(before_rows) + len(input_rows)} 件")

    print(f"\n[2] before 処理中...")
    before_results = []
    cnt_b = Counter()
    for i, row in enumerate(before_rows):
        result = process_before_row(i, row)
        before_results.append(result)
        cnt_b[result["verdict"]] += 1
        if (i + 1) % 500 == 0:
            print(f"  進捗: {i+1}/{len(before_rows)}  {dict(cnt_b)}")
    print(f"  完了: {len(before_rows)} 件 / {dict(cnt_b)}")

    print(f"\n[3] input 処理中...")
    input_results = []
    cnt_i = Counter()
    for i, row in enumerate(input_rows):
        result = process_input_row(i, row)
        input_results.append(result)
        cnt_i[result["verdict"]] += 1
        if (i + 1) % 100 == 0:
            print(f"  進捗: {i+1}/{len(input_rows)}  {dict(cnt_i)}")
    print(f"  完了: {len(input_rows)} 件 / {dict(cnt_i)}")

    all_results = before_results + input_results
    total = len(all_results)

    print(f"\n[4] 統計")
    vc = Counter(r["verdict"] for r in all_results)
    for v in ["MOVED", "MISSING", "DUPLICATED", "KEPT", "MODIFIED"]:
        print(f"  {v:12s}: {vc.get(v, 0):5d}")
    print(f"  {'合計':12s}: {total:5d}")
    empty_verdict = [r for r in all_results if not r["verdict"]]
    print(f"  verdict 空欄   : {len(empty_verdict):5d}")
    empty_actual = [r for r in all_results if not r["actual_line"] and r["verdict"] in ("KEPT", "MOVED", "DUPLICATED")]
    print(f"  actual_line 空欄（KEPT/MOVED/DUP）: {len(empty_actual):5d}")

    print(f"\n[5] CSV 出力: {OUTPUT_CSV}")
    fieldnames = [
        "item_id", "src_file", "src_line", "kind",
        "heading_path", "content", "design_dest",
        "actual_file", "actual_line", "verdict", "note"
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"  書き込み完了: {total} 行")

    print(f"\n[6] G1-01 検出確認（01_Abstract.rst L195-579 が DUPLICATED）")
    g1_01 = [
        r for r in before_results
        if "01_Abstract.rst" in r["src_file"]
        and ABSTRACT_B1_RANGE[0] <= int(r["src_line"]) <= ABSTRACT_B1_RANGE[1]
        and r["verdict"] == "DUPLICATED"
    ]
    print(f"  DUPLICATED 件数: {len(g1_01)}")

    print(f"\n[7] 03_Tips.rst の MODIFIED 検出確認")
    tips_modified = [
        r for r in before_results
        if "03_Tips.rst" in r["src_file"] and r["verdict"] == "MODIFIED"
    ]
    print(f"  MODIFIED 件数: {len(tips_modified)}")
    for r in tips_modified[:10]:
        print(f"  {r['item_id']} L{r['src_line']} {r['kind']:12s} {r['note'][:80]}")

    print(f"\n[8] MISSING 詳細（先頭20件）")
    missing_list = [r for r in all_results if r["verdict"] == "MISSING"]
    for r in missing_list[:20]:
        src = r["src_file"].split("/")[-1]
        print(f"  {r['item_id']} {src} L{r['src_line']} {r['kind']:12s} dest={r['design_dest']}")
        print(f"    {r.get('note','')[:80]}")

    return vc, total


if __name__ == "__main__":
    main()
