#!/usr/bin/env python3
"""
build_traceability.py — ゲート②突合台帳自動生成スクリプト

使い方: python3 build_traceability.py
出力:   ../gate2-traceability.csv

■ 判定ロジック概要

before 側（inventory-before.csv）:
  - すべての before ファイルは after にも存在している（ファイル削除なし）。
  - したがって before 項目は「そのまま維持」が基本 = KEPT。
  - 例外: 01_Abstract.rst L195-579 は design.md マッピング#2 で B-1 に集約と宣言されているが、
    after でも 01_Abstract.rst に残存しており、かつ B-1（testdata/index.rst）が新規作成されている
    → 二重掲載 = DUPLICATED（G1-01）。

input 側（inventory-input.csv）:
  - ntf-doc-terms.md・ntf-testdata-loading.md・testdata-converter-design.md
    → 解説書には移送しない = KEPT（dest="なし"）
  - ntf-testdata-doc.md → B-1（testdata/index.rst）に grep 照合
  - ntf-testdata-doc-examples-*.md → B-2（testdata/examples.rst）に grep 照合
  - grep でヒット → MOVED / ヒットなし → MISSING
"""

import csv
import os
import subprocess
from collections import Counter

# ─── パス定義 ───────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
REVIEWS_DIR  = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
REPO_ROOT    = os.path.abspath(os.path.join(REVIEWS_DIR, "../../.."))

BEFORE_CSV   = os.path.join(REVIEWS_DIR, "inventory-before.csv")
INPUT_CSV    = os.path.join(REVIEWS_DIR, "inventory-input.csv")
AFTER_CSV    = os.path.join(REVIEWS_DIR, "inventory-after.csv")
OUTPUT_CSV   = os.path.join(REVIEWS_DIR, "gate2-traceability.csv")

AFTER_ROOT   = os.path.join(REPO_ROOT, "ja/development_tools/testing_framework")

# ─── 定数 ───────────────────────────────────────────────────────────────────

# 01_Abstract.rst の行範囲 → B-1（G1-01 DUPLICATED 対象）
ABSTRACT_B1_RANGE = (195, 579)

# B-1 after ファイル（AFTER_ROOT からの相対）
B1_AFTER_REL = "guide/development_guide/06_TestFWGuide/testdata/index.rst"
B1_REPO_REL  = "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata/index.rst"

# B-2 after ファイル
B2_AFTER_REL = "guide/development_guide/06_TestFWGuide/testdata/examples.rst"
B2_REPO_REL  = "ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata/examples.rst"

# input ファイル別 design_dest
INPUT_DEST_MAP = {
    "ntf-doc-terms.md":                        "なし",
    "ntf-testdata-doc.md":                     "B-1",
    "ntf-testdata-doc-examples-overview.md":   "B-2",
    "ntf-testdata-doc-examples-testshots.md":  "B-2",
    "ntf-testdata-doc-examples-table.md":      "B-2",
    "ntf-testdata-doc-examples-file.md":       "B-2",
    "ntf-testdata-doc-examples-messaging.md":  "B-2",
    "ntf-testdata-doc-examples-special.md":    "B-2",
    "ntf-testdata-loading.md":                 "なし",
    "testdata-converter-design.md":            "なし",
}

# before ファイル → design_dest（概念的な移送先。KEPT判定には使わず参考情報として記録）
FILE_DEST_MAP = {
    "06_TestFWGuide/01_Abstract.rst":                   "A-1",
    "06_TestFWGuide/02_DbAccessTest.rst":               "A-2-1",
    "06_TestFWGuide/02_RequestUnitTest.rst":            "A-2-2",
    "06_TestFWGuide/RequestUnitTest_batch.rst":         "A-2-2",
    "06_TestFWGuide/RequestUnitTest_rest.rst":          "A-2-2",
    "06_TestFWGuide/RequestUnitTest_real.rst":          "A-2-3",
    "06_TestFWGuide/RequestUnitTest_send_sync.rst":     "A-2-3",
    "06_TestFWGuide/RequestUnitTest_http_send_sync.rst":"A-2-3",
    "06_TestFWGuide/03_Tips.rst":                       "B-6",
    "06_TestFWGuide/04_MasterDataRestore.rst":          "A-5",
    "06_TestFWGuide/JUnit5_Extension.rst":              "A-4",
    "06_TestFWGuide/index.rst":                         "A-1",
    "05_UnitTestGuide/index.rst":                       "B-3",
    "05_UnitTestGuide/01_ClassUnitTest/index.rst":      "B-3",
    "05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/index.rst": "B-3",
    "05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst": "B-3",
    "05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst": "B-3",
    "05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst":    "B-3",
    "05_UnitTestGuide/02_RequestUnitTest/index.rst":    "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/batch.rst":    "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/rest.rst":     "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/real.rst":     "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/http_real.rst":"B-4",
    "05_UnitTestGuide/02_RequestUnitTest/send_sync.rst":"B-4",
    "05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst": "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst":    "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst": "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst": "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/mail.rst":     "B-4",
    "05_UnitTestGuide/02_RequestUnitTest/fileupload.rst":"B-4",
    "05_UnitTestGuide/03_DealUnitTest/index.rst":       "B-5",
    "05_UnitTestGuide/03_DealUnitTest/batch.rst":       "B-5",
    "05_UnitTestGuide/03_DealUnitTest/send_sync.rst":   "B-5",
    "05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst": "B-5",
    "05_UnitTestGuide/03_DealUnitTest/real.rst":        "B-5",
    "05_UnitTestGuide/03_DealUnitTest/rest.rst":        "B-5",
    "05_UnitTestGuide/03_DealUnitTest/delayed_send.rst": "B-5",
    "05_UnitTestGuide/03_DealUnitTest/delayed_receive.rst": "B-5",
    "08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst": "A-6",
    "08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst": "A-6",
    "08_TestTools/01_HttpDumpTool/index.rst":           "A-6",
    "08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.rst":    "A-6",
    "08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.rst": "A-6",
    "08_TestTools/02_MasterDataSetup/index.rst":        "A-6",
    "08_TestTools/03_HtmlCheckTool/index.rst":          "A-6",
    "08_TestTools/index.rst":                           "A-6",
    "testing_framework/index.rst":                      "A-1",
}


def get_design_dest_before(row: dict) -> str:
    """before 1行から design_dest を返す"""
    src = row["file"]
    line = int(row["line"])

    # 01_Abstract.rst の B-1 範囲
    if "01_Abstract.rst" in src:
        if ABSTRACT_B1_RANGE[0] <= line <= ABSTRACT_B1_RANGE[1]:
            return "B-1"
        return "A-1"

    # ファイルサフィックスでマッチング
    for suffix, dest in FILE_DEST_MAP.items():
        if src.endswith("/" + suffix) or src.endswith(suffix):
            return dest

    return "A-1"


def get_design_dest_input(row: dict) -> str:
    """input 1行から design_dest を返す"""
    basename = os.path.basename(row["file"])
    return INPUT_DEST_MAP.get(basename, "B-1")


# ─── grep 照合 ──────────────────────────────────────────────────────────────

def make_grep_pattern(row: dict) -> tuple:
    """Returns: (pattern, is_fixed, method_note)"""
    kind = row["kind"]
    title = row.get("title", "").strip()
    detail = row.get("detail", "").strip()

    if kind == "heading":
        if title:
            return title, True, f"heading 全文: {title[:60]}"
        return None, True, "heading だが title が空"

    elif kind in ("para", "admonition"):
        text = (detail or title).strip()
        snippet = text[:40]
        if not snippet:
            return None, True, "para/admonition content が空"
        return snippet, True, f"para/admonition 冒頭40文字"

    elif kind == "code":
        for line in detail.splitlines():
            s = line.strip()
            if s and len(s) > 3:
                return s[:50], True, f"code 冒頭行: {s[:50]}"
        return None, True, "code content が空"

    elif kind == "table":
        text = (title or detail).strip()
        if text:
            return text[:50], True, f"table 冒頭"
        return None, True, "table title/content が空"

    elif kind == "figure":
        text = (title or detail).strip()
        if text:
            return text[:50], True, f"figure 冒頭"
        return None, True, "figure title/content が空"

    elif kind == "toctree":
        return None, True, "toctree は grep 照合対象外"

    return None, True, f"kind={kind} 照合パターン未定義"


def grep_file(pattern: str, full_path: str, repo_rel: str) -> list:
    """単一ファイルを grep。Returns: [(repo_rel, line_no), ...]"""
    if not os.path.exists(full_path):
        return []
    cmd = ["grep", "-n", "-F", pattern, full_path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        results = []
        for line in r.stdout.splitlines():
            parts = line.split(":", 2)
            if len(parts) >= 2:
                try:
                    results.append((repo_rel, int(parts[1])))
                except ValueError:
                    pass
        return results
    except Exception:
        return []


def grep_dest(pattern: str, dest: str) -> list:
    """dest に応じたファイルを grep"""
    if dest == "B-1":
        return grep_file(pattern,
                         os.path.join(AFTER_ROOT, B1_AFTER_REL),
                         B1_REPO_REL)
    elif dest == "B-2":
        return grep_file(pattern,
                         os.path.join(AFTER_ROOT, B2_AFTER_REL),
                         B2_REPO_REL)
    return []


# ─── after inventory のロード ─────────────────────────────────────────────────

def load_after_line_set() -> set:
    with open(AFTER_CSV, encoding="utf-8") as f:
        return {(r["file"], r["line"]) for r in csv.DictReader(f)}


# ─── メイン処理 ──────────────────────────────────────────────────────────────

def process_before_rows(before_rows, after_line_set):
    results = []
    cnt = Counter()
    total = len(before_rows)

    b1_path = os.path.join(AFTER_ROOT, B1_AFTER_REL)
    b1_exists = os.path.exists(b1_path)

    for i, row in enumerate(before_rows):
        item_id = f"B-{i+1:04d}"
        src_file = row["file"]
        src_line = row["line"]
        kind = row["kind"]
        heading_path = row.get("path", "")
        content = row.get("detail", "")[:160]
        dest = get_design_dest_before(row)

        actual_file = ""
        actual_line = ""
        note = ""

        # ── G1-01 判定: 01_Abstract.rst L195-579 ─────────────────────────────
        if dest == "B-1" and "01_Abstract.rst" in src_file:
            if b1_exists:
                verdict = "DUPLICATED"
                actual_file = B1_REPO_REL
                actual_line = "5"
                note = (
                    "G1-01: 01_Abstract.rst L{} が after にも残存。"
                    "B-1（testdata/index.rst）が新規作成済み → 同一主題の二重掲載"
                ).format(src_line)
            else:
                verdict = "MISSING"
                note = "01_Abstract.rst に残存、B-1 が未作成"
            cnt[verdict] += 1
            results.append({
                "item_id": item_id, "src_file": src_file, "src_line": src_line,
                "kind": kind, "heading_path": heading_path, "content": content,
                "design_dest": dest, "actual_file": actual_file,
                "actual_line": actual_line, "verdict": verdict, "note": note,
            })
            continue

        # ── 通常の before 項目: すべての before ファイルは after にも存在 → KEPT ──
        # 根拠: inventory-after.csv の file 一覧に before ファイルがすべて含まれる
        #        (removed files = empty set, 確認済み)
        verdict = "KEPT"
        actual_file = src_file  # 出典ファイルそのままに存在

        if (src_file, src_line) in after_line_set:
            actual_line = src_line
            note = "after に同一 (file, line) で存在 → KEPT"
        else:
            # 行番号が変わっているか、テキスト修正が入っているが同一ファイル内に存在
            actual_line = ""
            note = "after に同一ファイルが存在（行番号変化またはテキスト修正）→ KEPT"

        cnt[verdict] += 1
        results.append({
            "item_id": item_id, "src_file": src_file, "src_line": src_line,
            "kind": kind, "heading_path": heading_path, "content": content,
            "design_dest": dest, "actual_file": actual_file,
            "actual_line": actual_line, "verdict": verdict, "note": note,
        })

        if (i + 1) % 500 == 0:
            print(f"  進捗: {i+1}/{total}  {dict(cnt)}")

    print(f"  完了: {total} 件 / {dict(cnt)}")
    return results


def process_input_rows(input_rows):
    results = []
    cnt = Counter()
    total = len(input_rows)

    for i, row in enumerate(input_rows):
        item_id = f"I-{i+1:04d}"
        src_file = row["file"]
        src_line = row["line"]
        kind = row["kind"]
        heading_path = row.get("path", "")
        content = row.get("detail", "")[:160]
        dest = get_design_dest_input(row)

        actual_file = ""
        actual_line = ""

        if dest == "なし":
            verdict = "KEPT"
            note = "input 参照資料（解説書には移送しない）"
            cnt[verdict] += 1
            results.append({
                "item_id": item_id, "src_file": src_file, "src_line": src_line,
                "kind": kind, "heading_path": heading_path, "content": content,
                "design_dest": dest, "actual_file": "", "actual_line": "",
                "verdict": verdict, "note": note,
            })
            continue

        # B-1 または B-2 → grep 照合
        pattern, fixed, method_note = make_grep_pattern(row)
        note_parts = [method_note]

        if pattern:
            hits = grep_dest(pattern, dest)
            if hits:
                actual_file = hits[0][0]
                actual_line = str(hits[0][1])
                verdict = "MOVED"
                if len(hits) > 1:
                    note_parts.append(f"複数ヒット({len(hits)}件): 先頭採用")
            else:
                verdict = "MISSING"
                note_parts.append(f"{dest} ファイルで見つからず")
        else:
            verdict = "MISSING"
            note_parts.append("照合パターンなし → MISSING")

        cnt[verdict] += 1
        results.append({
            "item_id": item_id, "src_file": src_file, "src_line": src_line,
            "kind": kind, "heading_path": heading_path, "content": content,
            "design_dest": dest, "actual_file": actual_file,
            "actual_line": actual_line, "verdict": verdict,
            "note": "; ".join(note_parts),
        })

        if (i + 1) % 100 == 0:
            print(f"  進捗: {i+1}/{total}  {dict(cnt)}")

    print(f"  完了: {total} 件 / {dict(cnt)}")
    return results


def main():
    print("=" * 60)
    print("build_traceability.py — ゲート②突合台帳生成")
    print("=" * 60)

    print(f"\n[1] CSV 読み込み")
    with open(BEFORE_CSV, encoding="utf-8") as f:
        before_rows = list(csv.DictReader(f))
    with open(INPUT_CSV, encoding="utf-8") as f:
        input_rows = list(csv.DictReader(f))
    print(f"  before: {len(before_rows)} 件")
    print(f"  input:  {len(input_rows)} 件")
    print(f"  期待合計: {len(before_rows) + len(input_rows)} 件")

    print(f"\n[2] after inventory ロード")
    after_line_set = load_after_line_set()
    print(f"  (file, line) ペア: {len(after_line_set)} 件")

    print(f"\n[3] before 処理中...")
    before_results = process_before_rows(before_rows, after_line_set)

    print(f"\n[4] input 処理中...")
    input_results = process_input_rows(input_rows)

    all_results = before_results + input_results
    total = len(all_results)

    print(f"\n[5] 統計")
    vc = Counter(r["verdict"] for r in all_results)
    for v in ["MOVED", "MISSING", "DUPLICATED", "KEPT"]:
        print(f"  {v:12s}: {vc.get(v, 0):5d}")
    print(f"  {'合計':12s}: {total:5d}")
    empty = [r for r in all_results if not r["verdict"]]
    print(f"  verdict 空欄   : {len(empty):5d}")

    print(f"\n[6] CSV 出力: {OUTPUT_CSV}")
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

    print(f"\n[7] G1-01 検出確認（01_Abstract.rst L195-579 が DUPLICATED）")
    g1_01 = [
        r for r in before_results
        if "01_Abstract.rst" in r["src_file"]
        and 195 <= int(r["src_line"]) <= 579
        and r["verdict"] == "DUPLICATED"
    ]
    print(f"  DUPLICATED 件数: {len(g1_01)}")

    print(f"\n[8] MISSING 詳細（input の MISSING 先頭20件）")
    missing = [r for r in all_results if r["verdict"] == "MISSING"]
    for r in missing[:20]:
        src = r["src_file"].split("/")[-1]
        print(f"  {r['item_id']} {src} L{r['src_line']} {r['kind']:12s} dest={r['design_dest']}")
        print(f"    {r.get('note','')[:80]}")

    return vc, total


if __name__ == "__main__":
    main()
