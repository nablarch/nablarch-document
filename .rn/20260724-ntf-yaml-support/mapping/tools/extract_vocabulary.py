"""
extract_vocabulary.py
design.md から dest_part / dest_page / dest_section の閉じた語彙を機械抽出する。

#5 のマッピング作成では、30バッチのプロンプトすべてにこの語彙を埋め込む。
語彙が誤っていると全バッチが誤った値を出力するため、抽出はdesign.mdの見出し・
表・ツリー図から機械的に行い、目視転記に頼らない。

design.md の章構成には「まだページ分割が確定していない」部分がある
（§3冒頭・§12 未確定事項#1・#2）。このスクリプトは design.md が確定として
書いている語彙のみを「確定」として抽出する。未確定分（第2部の8ページ・
処理方式ごとのページ分割）は、このスクリプトでは抽出せず、
`mapping/vocabulary.md` 側で「暫定」区分として別途手作業ドキュメント化する
（design.md 自身が「暫定構成」「未確定事項」と明記しており、機械抽出できる
確定情報がそもそも存在しないため）。
"""
import re
import sys
from pathlib import Path

DESIGN_MD = Path(__file__).resolve().parents[2] / "design.md"


def read_design():
    return DESIGN_MD.read_text(encoding="utf-8").splitlines()


def extract_dest_parts(lines):
    parts = []
    for line in lines:
        m = re.match(r"^## \d+\. (第[1234]部.+)$", line)
        if m:
            parts.append(m.group(1))
    assert len(parts) == 4, f"expected 4 dest_part, got {parts}"
    return parts


def extract_table(lines, start_idx, header_col_name):
    """start_idx: index of the header row '| col1 | col2 | ...'. Returns list of first-column values until a blank/non-table line."""
    header = lines[start_idx]
    cols = [c.strip() for c in header.strip("|").split("|")]
    col_idx = cols.index(header_col_name)
    values = []
    i = start_idx + 2  # skip header + separator
    while i < len(lines) and lines[i].strip().startswith("|"):
        row = [c.strip() for c in lines[i].strip("|").split("|")]
        values.append(row[col_idx])
        i += 1
    return values


def find_line(lines, pattern):
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            return i
    raise ValueError(f"pattern not found: {pattern}")


def extract_part1_sections(lines):
    idx = find_line(lines, r"^## 2\. 第1部")
    header_idx = find_line(lines[idx:], r"^\| セクション \|") + idx
    sections = extract_table(lines, header_idx, "セクション")
    return sections


def extract_part1_page_name(lines):
    idx = find_line(lines, r"^## 2\. 第1部")
    return re.match(r"^## \d+\. 第1部 (.+)$", lines[idx]).group(1)


def extract_code_fence(lines, after_idx):
    start = None
    for i in range(after_idx, len(lines)):
        if lines[i].strip() == "```":
            start = i
            break
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "```":
            end = i
            break
    return lines[start + 1:end]


TOP_MARKER = re.compile(r"^(├──|└──)\s*(.*)$")
NESTED_MARKER = re.compile(r"^│\s*(├──|└──)\s*(.*)$")


def _label(text):
    return re.split(r"\s{2,}", text.strip())[0].strip()


def tree_top_level_items(fence_lines):
    """Top-level tree leaves (marker at column 0), label only (trailing comment after 2+ spaces stripped)."""
    items = []
    for line in fence_lines:
        m = TOP_MARKER.match(line)
        if m:
            items.append(_label(m.group(2)))
    return items


def tree_nested_children(fence_lines, parent_label):
    """Children one level under a given top-level parent label (marker prefixed by '│')."""
    children = []
    in_parent = False
    for line in fence_lines:
        top = TOP_MARKER.match(line)
        if top:
            in_parent = _label(top.group(2)) == parent_label
            continue
        nested = NESTED_MARKER.match(line)
        if nested and in_parent:
            children.append(_label(nested.group(2)))
    return children


def extract_part2_tentative_pages(lines):
    idx = find_line(lines, r"^## 3\. 第2部")
    fence = extract_code_fence(lines, idx)
    return tree_top_level_items(fence)


def extract_part2_sections(lines):
    idx = find_line(lines, r"^### ページのアウトライン")
    fence = extract_code_fence(lines, idx)
    return tree_top_level_items(fence)


def extract_part3_tree(lines):
    idx = find_line(lines, r"^## 4\. 第3部")
    fence = extract_code_fence(lines, idx)
    top = tree_top_level_items(fence)
    children = {label: tree_nested_children(fence, label) for label in top}
    return top, children


def extract_part3_sections(lines):
    # second "### ページのアウトライン" (1st is Part2's, 3rd is Part4's)
    matches = [i for i, l in enumerate(lines) if l.strip() == "### ページのアウトライン"]
    assert len(matches) == 3, matches
    fence = extract_code_fence(lines, matches[1])
    return tree_top_level_items(fence)


def extract_part4_tree(lines):
    idx = find_line(lines, r"^## 5\. 第4部")
    fence = extract_code_fence(lines, idx)
    return tree_top_level_items(fence)


def extract_part4_sections(lines):
    # third "### ページのアウトライン" (1st is Part2's, 2nd is Part3's)
    matches = [i for i, l in enumerate(lines) if l.strip() == "### ページのアウトライン"]
    assert len(matches) == 3, matches
    fence = extract_code_fence(lines, matches[2])
    return tree_top_level_items(fence)


def extract_processing_methods(lines):
    idx = find_line(lines, r"^## 6\. 処理方式の名称")
    header_idx = find_line(lines[idx:], r"^\| 名称 \|") + idx
    names = extract_table(lines, header_idx, "名称")
    ntf = extract_table(lines, header_idx, "NTF対象")
    return [n for n, t in zip(names, ntf) if t == "○"]


def main():
    lines = read_design()
    dest_parts = extract_dest_parts(lines)
    part1_page = extract_part1_page_name(lines)
    part1_sections = extract_part1_sections(lines)
    part2_tentative_pages = extract_part2_tentative_pages(lines)
    part2_sections = extract_part2_sections(lines)
    part3_top, part3_children = extract_part3_tree(lines)
    part3_sections = extract_part3_sections(lines)
    part4_top = extract_part4_tree(lines)
    part4_sections = extract_part4_sections(lines)
    methods = extract_processing_methods(lines)

    # mapping/vocabulary.md はこの実行結果をそのまま転記したもの。件数が
    # 変わったら design.md 側が更新されたということなので、ここで止める。
    assert part1_page == "テスティングフレームワークとは", part1_page
    assert part1_sections == ["全体像", "アーキテクチャ", "テストの種類", "テストデータ", "対象範囲", "稼動環境"], part1_sections
    assert len(part2_tentative_pages) == 7, part2_tentative_pages
    assert part2_sections == ["機能概要", "使用方法", "拡張例"], part2_sections
    assert part3_top == ["テストデータの書き方", "テストデータの記載例",
                          "クラス単体テスト", "リクエスト単体テスト", "取引単体テスト"], part3_top
    assert part3_children["クラス単体テスト"] == ["エンティティ単体テスト", "コンポーネント単体テスト"]
    assert part3_children["リクエスト単体テスト"] == methods, (part3_children["リクエスト単体テスト"], methods)
    assert part3_children["取引単体テスト"] == [], part3_children["取引単体テスト"]  # 未確定事項#2、design.mdに子は列挙されていない
    assert part3_sections == ["機能概要", "使用方法"], part3_sections
    assert part4_top == ["リクエスト単体データ作成ツール", "テストデータ変換ツール",
                          "マスタデータ投入ツール", "HTMLチェックツール"], part4_top
    assert part4_sections == ["機能概要", "導入", "使用方法"], part4_sections
    assert len(methods) == 6, methods

    print("dest_part (確定, 4件):")
    for p in dest_parts:
        print(f"  - {p}")

    print(f"\n第1部 dest_page (確定, 1件): {part1_page}")
    print(f"第1部 dest_section (確定, {len(part1_sections)}件): {part1_sections}")

    print(f"\n第2部 暫定ページ一覧 (design.md §3 ツリー, {len(part2_tentative_pages)}件): {part2_tentative_pages}")
    print(f"第2部 ページ共通セクション (確定, {len(part2_sections)}件): {part2_sections}")

    print(f"\n第3部 トップレベル項目: {part3_top}")
    for label, kids in part3_children.items():
        if kids:
            print(f"  {label} の子: {kids}")
    print(f"第3部 ページ共通セクション (確定, {len(part3_sections)}件): {part3_sections}")

    print(f"\n第4部 トップレベル項目 (確定, {len(part4_top)}件): {part4_top}")
    print(f"第4部 ページ共通セクション (確定, {len(part4_sections)}件): {part4_sections}")

    print(f"\n処理方式名称 (design.md §6, NTF対象=○, {len(methods)}件): {methods}")


if __name__ == "__main__":
    sys.exit(main())
