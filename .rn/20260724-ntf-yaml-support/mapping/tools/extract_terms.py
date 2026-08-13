"""
extract_terms.py
用語候補の母集団を機械的に抽出する。

用語集 `mapping/glossary.md` の3ラウンドのレビューがいずれも新しい抜けを
指摘し続けた原因は、用語集が「カバーすべき用語の母集団」を一度も定義して
いなかったことにある。本スクリプトはその母集団を4つの出典から機械的に
列挙し、`mapping/term-candidates.csv` に出力する。以後 `glossary.md` の
全項目はこのCSVの行と突き合わせて「採用」または「不採用（理由付き）」の
どちらかに判定され、`verify_glossary.py` が未判定0件を検査する。

出典は次の4つ（`source` 列の値）。

  current-heading       `mapping/sections-current.csv` の `heading_path` 列。
                         `>` 区切りのパスをセグメントに分解し、
                         `(冒頭)` `(L1直下)` のような合成マーカーを除いた
                         各セグメントを候補とする。
  ntf-doc-terms-heading  `input/ntf-doc-terms.md` のMarkdown見出し
                         （`#`〜`####`）のうち、H1（文書題）を除いた
                         H2〜H4すべて。H1はこのファイル自体の題であって
                         用語候補ではないため除く。母集団は網羅が目的で
                         あり、レベルを追加で絞り込む理由はない。H2見出し
                         がグルーピング的な節見出しで単一の用語でない場合は、
                         母集団から除外せず `glossary.md` 側で「不採用
                         （節見出しのため）」等の理由付きで判定する。
                         実測: H1=1 / H2=10 / H3=27 / H4=8（H1を除く45件）。
  design-heading         `design.md` の `##`/`###` 見出し。H1（文書題）を
                         除く。design.md には `####` が存在しない。
                         実測: H1=1 / H2=10 / H3=12（H1を除く22件）。
  design-scheme           `design.md` の「5. 処理方式の名称」表（167〜173行
                         付近）の「名称」列。処理方式の正式名称7件。

occurrences は「その表記が、同じ source の走査対象の中で見出し／名称として
現れた回数」。1つの見出しパスに同じセグメントが2回現れることは実質ない
ため、実務上は「何個の見出しがその表記に一致するか」と同義になる。
file_line は代表1件（最初に見つかった位置）の `path:line`（リポジトリ
ルート相対）。current-heading の file_line は、heading_path 上の出現位置
ではなく、基準コミット時点の現行解説書 `.rst` を実際に再パースして得た
「その見出しテキスト自身の行番号」である（子見出しを持つ見出しは
sections-current.csv 上に自分自身のセクション行を持たないため、CSVの行
だけからは代表行を作れない）。

使い方:

    python3 mapping/tools/extract_terms.py
    python3 mapping/tools/extract_terms.py -o /tmp/term-candidates.csv
"""

import argparse
import csv
import os
import re
import sys
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_sections import parse_headings  # noqa: E402
import detect_term_variants as dtv  # noqa: E402

# ---------------------------------------------------------------------------
# パス解決
# ---------------------------------------------------------------------------

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.abspath(os.path.join(TOOLS_DIR, "..", ".."))
REPO_ROOT = os.path.abspath(os.path.join(SESSION_DIR, "..", ".."))

DEFAULT_SECTIONS_CURRENT = os.path.join(SESSION_DIR, "mapping", "sections-current.csv")
DEFAULT_NTF_DOC_TERMS = os.path.join(SESSION_DIR, "input", "ntf-doc-terms.md")
DEFAULT_DESIGN = os.path.join(SESSION_DIR, "design.md")
DEFAULT_OUTPUT = os.path.join(SESSION_DIR, "mapping", "term-candidates.csv")

#: `extract_sections.py` が付ける合成マーカー。見出しではなく本文段落。
MARKER_RE = re.compile(r"^\(冒頭\)$|^\(L[0-9]+直下\)$")


def _strip_inline_code_markup(text: str) -> str:
    """見出しテキストからMarkdown/RSTのインラインコード記法（バッククォート）を除く。

    `term-candidates.csv` の表記をそのまま Markdown のコードスパン
    （`` `表記` ``）としてglossary.mdに埋め込むため、表記自身にバック
    クォートが残っていると（例: 見出し `` `FwHeaderDefinition` / `fwHeaderDefinition` ``
    や RST の ``RequestResponseProcessor`` ）二重引用になって崩れる。
    バッククォートは書式であって表記の一部ではないため取り除く。
    """
    return text.replace("`", "")

CSV_COLUMNS = ["term", "source", "occurrences", "file_line"]

# ソースの出力順。母集団の由来ごとにまとめて眺められるようにする。
SOURCE_ORDER = (
    "current-heading",
    "ntf-doc-terms-heading",
    "design-heading",
    "design-scheme",
)


class Candidate(NamedTuple):
    term: str
    source: str
    occurrences: int
    file_line: str


def _rel(path: str) -> str:
    """リポジトリルート相対のパスにする。"""
    return os.path.relpath(os.path.abspath(path), REPO_ROOT)


# ---------------------------------------------------------------------------
# heading_path の分解
# ---------------------------------------------------------------------------


def split_heading_path(heading_path: str) -> List[str]:
    """`>` 区切りの heading_path を見出しテキストのリストに分解する。

    `(冒頭)` `(L1直下)` のような合成マーカー（見出しではなく本文段落を表す）
    は除く。空セグメントも除く。
    """
    segments = [s.strip() for s in heading_path.split(">")]
    return [
        _strip_inline_code_markup(s) for s in segments
        if s and not MARKER_RE.match(s)
    ]


# ---------------------------------------------------------------------------
# 出典1: current-heading（sections-current.csv の heading_path 列）
# ---------------------------------------------------------------------------
#
# occurrences は heading_path セグメントとしての出現回数（CSVの行単位）だが、
# file_line は「そのセグメントの祖先見出し（子見出しを持つ見出し）を含む行の
# src_line」ではない。extract_sections.py の規則上、子見出しを持つ見出しは
# それ自身のセクション行を持たず、CSVの各行の src_line は「その行の最後の
# 見出しの本文開始行」または「マーカー直下の本文開始行」であって、祖先見出し
# 自身のテキスト行ではない（例: ページ題は個々の子セクション行の src_line に
# しか現れず、そのどれもページ題自身の行ではない）。CSVの行だけから代表
# file:line を作ると、見出しテキストと実際に無関係な行を指す誤引用になる
# （用語集で禁じている「採用根拠が引用先の内容を支持しない」G-4型の欠陥と
# 同じ失敗）。そのため、見出しテキストの真の行番号は基準コミット時点の
# 現行解説書（.rst）を実際に再パースして求める。


def _heading_locations(
    docs: Sequence[Tuple[str, str]]
) -> Dict[str, Tuple[str, int]]:
    """(相対パス, 本文) のリストから、見出しテキスト→最初に現れた

    (パス, 1-indexed行番号) を作る。同じテキストが複数ファイルにまたがって
    見出しとして現れる場合は、`docs` の順序で最初のものを採る。
    """
    locations: Dict[str, Tuple[str, int]] = {}
    for path, text in docs:
        for h in parse_headings(text, path):
            term = _strip_inline_code_markup(h.text)
            locations.setdefault(term, (path, h.text_line + 1))
    return locations


def load_current_docs() -> List[Tuple[str, str]]:
    """基準コミット時点の現行解説書 `.rst` 全ファイルを (パス, 本文) で返す。"""
    docs = dtv._load_current(dtv.base_commit())
    return [(d.path, "\n".join(d.lines)) for d in docs]


def extract_current_headings(
    csv_path: str, docs: Optional[Sequence[Tuple[str, str]]] = None
) -> List[Candidate]:
    counts: Dict[str, int] = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 1行（1セクション）の中で同じセグメントが重複しても1回だけ数える。
            for term in dict.fromkeys(split_heading_path(row["heading_path"])):
                counts[term] = counts.get(term, 0) + 1

    if not counts:
        return []
    if docs is None:
        docs = load_current_docs()
    locations = _heading_locations(docs)

    result: List[Candidate] = []
    for term in sorted(counts):
        loc = locations.get(term)
        if loc is None:
            # heading_path に現れるが、どのファイルの見出しとしても再検出
            # できなかった場合。CSVと現行解説書の乖離を隠さずエラーにする。
            raise ValueError(
                f"見出し {term!r} の実際の行番号が見つからない"
                f"（sections-current.csv と現行解説書の再パース結果が食い違う）"
            )
        result.append(Candidate(term, "current-heading", counts[term], f"{loc[0]}:{loc[1]}"))
    return result


# ---------------------------------------------------------------------------
# 出典2・3: Markdown見出し（ntf-doc-terms.md / design.md）
# ---------------------------------------------------------------------------


def extract_md_headings(
    md_path: str, source: str, min_level: int, max_level: int
) -> List[Candidate]:
    """Markdownファイルの見出しのうち [min_level, max_level] のレベルだけを候補にする。"""
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    headings = parse_headings(text, "dummy.md")
    counts: Dict[str, int] = {}
    first_line: Dict[str, int] = {}
    for h in headings:
        if not (min_level <= h.level <= max_level):
            continue
        term = _strip_inline_code_markup(h.text)
        counts[term] = counts.get(term, 0) + 1
        first_line.setdefault(term, h.text_line + 1)  # 1-indexed
    rel_path = _rel(md_path)
    return [
        Candidate(term, source, counts[term], f"{rel_path}:{first_line[term]}")
        for term in sorted(counts)
    ]


# ---------------------------------------------------------------------------
# 出典4: design-scheme（design.md「5. 処理方式の名称」表の名称列）
# ---------------------------------------------------------------------------

_SECTION5_HEADING_RE = re.compile(r"^##\s+5\.\s*処理方式の名称\s*$")
_NEXT_H2_RE = re.compile(r"^##\s+")
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


def extract_design_schemes(design_path: str) -> List[Candidate]:
    """design.md の「5. 処理方式の名称」表から、名称列（1列目）を候補にする。"""
    with open(design_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    start = None
    for i, line in enumerate(lines):
        if _SECTION5_HEADING_RE.match(line):
            start = i
            break
    if start is None:
        raise ValueError(f"{design_path}: 「## 5. 処理方式の名称」見出しが無い")

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if _NEXT_H2_RE.match(lines[i]):
            end = i
            break

    rel_path = _rel(design_path)
    candidates: List[Candidate] = []
    seen_header = False
    for i in range(start, end):
        m = _TABLE_ROW_RE.match(lines[i])
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if not cells:
            continue
        first_cell = cells[0]
        if not seen_header:
            # ヘッダ行（例: "名称"）。次の区切り行と合わせてスキップする。
            seen_header = True
            continue
        if set(first_cell) <= set("-: "):
            continue  # 区切り行
        candidates.append(
            Candidate(first_cell, "design-scheme", 1, f"{rel_path}:{i + 1}")
        )
    return candidates


# ---------------------------------------------------------------------------
# 統合・CSV出力
# ---------------------------------------------------------------------------


def extract_all(
    sections_current: str = DEFAULT_SECTIONS_CURRENT,
    ntf_doc_terms: str = DEFAULT_NTF_DOC_TERMS,
    design: str = DEFAULT_DESIGN,
) -> List[Candidate]:
    candidates: List[Candidate] = []
    candidates += extract_current_headings(sections_current)
    # ntf-doc-terms.md: H1（文書題）を除く全レベル(H2〜H4)。
    candidates += extract_md_headings(ntf_doc_terms, "ntf-doc-terms-heading", 2, 4)
    # design.md: H1（文書題）を除く全レベル(H2〜H3、H4は存在しない)。
    candidates += extract_md_headings(design, "design-heading", 2, 4)
    candidates += extract_design_schemes(design)
    return candidates


def write_csv(candidates: Sequence[Candidate], out_path: str) -> None:
    order = {name: i for i, name in enumerate(SOURCE_ORDER)}
    rows = sorted(candidates, key=lambda c: (order.get(c.source, 99), c.term))
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(CSV_COLUMNS)
        for c in rows:
            writer.writerow([c.term, c.source, c.occurrences, c.file_line])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="用語候補の母集団を見出し・処理方式名から機械的に抽出する"
    )
    parser.add_argument("--sections-current", default=DEFAULT_SECTIONS_CURRENT)
    parser.add_argument("--ntf-doc-terms", default=DEFAULT_NTF_DOC_TERMS)
    parser.add_argument("--design", default=DEFAULT_DESIGN)
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    candidates = extract_all(args.sections_current, args.ntf_doc_terms, args.design)
    write_csv(candidates, args.output)

    by_source: Dict[str, int] = {}
    for c in candidates:
        by_source[c.source] = by_source.get(c.source, 0) + 1
    print(f"Wrote {len(candidates)} candidates to {args.output}", file=sys.stderr)
    for name in SOURCE_ORDER:
        print(f"  {name}: {by_source.get(name, 0)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
