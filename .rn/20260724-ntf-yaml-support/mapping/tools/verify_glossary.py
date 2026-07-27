"""
verify_glossary.py
用語集 mapping/glossary.md の記述を出典と scan 出力に突き合わせる。

用語集の価値はほぼ全部が「file:line」と「N件」である。tsv や出典が変われば
これらは黙って古くなるため、#2/#2a の verify_coverage.py と同じ水準で
機械的に検査する。検査は5つ。

  refs      glossary.md 中の `PREFIX:path:line` 参照が実在するか。
            ファイルが存在し、行番号が範囲内で、その行に「直前で名指しした
            表記・引用文」が実在すること。NTF:/NTF-root: は基準コミットの
            内容、FW:/S: は作業ツリーを読む。

  counts    表の中の「現行N件 / inputN件 / FWN件 / designN件」という主張が
            scan 出力の出現数と一致すること。件数は必ず直前のコードスパン
            （表記）に係る形で書く。係り先が特定できない件数は不一致として
            報告する。

  sections  §5 の「揺れ表記」列に挙げた表記が、§8 の対応表にすべて載って
            いること。§5 と §8 がずれると #5 のサブエージェントが取りこぼす。

  terms     term_candidates.tsv の正表記が §5 の「正表記」列に、揺れ表記が
            §5 のいずれかの列（正表記／揺れ表記／別義・旧名称）に載って
            いること。逆に §5 の表記が tsv にあること。

  applies   §8 対応表の全行に「適用条件」が書かれていること。無条件置換は
            「機能概要」→「機能機能概要」のような壊れ方をするため。

使い方:

    python3 mapping/tools/verify_glossary.py
    python3 mapping/tools/verify_glossary.py --scan mapping/scan-terms.tsv

不一致があれば内訳を出力して終了コード1を返す。
"""

import argparse
import csv
import os
import re
import subprocess
import sys
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect_term_variants as dtv  # noqa: E402

TOOLS_DIR = dtv.TOOLS_DIR
SESSION_DIR = dtv.SESSION_DIR
REPO_ROOT = dtv.REPO_ROOT
MAPPING_DIR = os.path.join(SESSION_DIR, "mapping")

DEFAULT_GLOSSARY = os.path.join(MAPPING_DIR, "glossary.md")
DEFAULT_SCAN = os.path.join(MAPPING_DIR, "scan-terms.tsv")

#: 用語集の接頭辞 -> (リポジトリルートからの相対ディレクトリ, 基準コミットで読むか)
PREFIXES: Dict[str, Tuple[str, bool]] = {
    "NTF": ("ja/development_tools/testing_framework/guide/development_guide", True),
    "NTF-root": ("ja/development_tools/testing_framework", True),
    "FW": ("ja/application_framework/application_framework", False),
    "S": (".rn/20260724-ntf-yaml-support", False),
}
#: NTF-root と NTF は前方一致が重なるので、長いほうから試す。
PREFIX_ORDER = ("NTF-root", "NTF", "FW", "S")

#: 件数の主張。「現行47件」のようにコーパスを明示した形だけを認める。
COUNT_RE = re.compile(r"(現行|input|FW|design)([0-9][0-9,]*)件")
COUNT_LABEL_TO_CORPUS = {
    "現行": "current", "input": "input", "FW": "fw", "design": "design",
}
#: コードスパン。参照も表記もこの形で書く。
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
#: `PREFIX:path:line`
REF_RE = re.compile(r"^(?P<prefix>[A-Za-z-]+):(?P<path>[^:]+):(?P<line>[0-9]+)$")
#: 直前の参照と同じファイルを指す略記 `:123`
SHORT_REF_RE = re.compile(r"^:(?P<line>[0-9]+)$")
#: 日本語の引用。原文の見出し・文をそのまま引くときに使う。
QUOTE_RE = re.compile(r"「([^「」]{2,120})」")


class Problem(NamedTuple):
    kind: str
    where: str
    detail: str


# ---------------------------------------------------------------------------
# 出典の読み込み
# ---------------------------------------------------------------------------

_file_cache: Dict[Tuple[str, bool], Optional[List[str]]] = {}


def _read_source(rel_path: str, from_base: bool) -> Optional[List[str]]:
    key = (rel_path, from_base)
    if key in _file_cache:
        return _file_cache[key]
    lines: Optional[List[str]]
    if from_base:
        try:
            text = subprocess.run(
                ["git", "-C", REPO_ROOT, "show", f"{dtv.base_commit()}:{rel_path}"],
                check=True, capture_output=True, text=True,
            ).stdout
            lines = text.splitlines()
        except subprocess.CalledProcessError:
            lines = None
    else:
        abs_path = os.path.join(REPO_ROOT, rel_path)
        if os.path.isfile(abs_path):
            with open(abs_path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            lines = None
    _file_cache[key] = lines
    return lines


def resolve_ref(token: str) -> Optional[Tuple[str, bool, int]]:
    """`NTF:foo.rst:12` を (リポジトリ相対パス, 基準コミットで読むか, 行番号) に。"""
    m = REF_RE.match(token)
    if not m:
        return None
    prefix = m.group("prefix")
    for name in PREFIX_ORDER:
        if prefix == name:
            root, from_base = PREFIXES[name]
            return f"{root}/{m.group('path')}", from_base, int(m.group("line"))
    return None


# ---------------------------------------------------------------------------
# glossary.md の解析
# ---------------------------------------------------------------------------


class Cell(NamedTuple):
    line_no: int
    section: str
    #: 表の何列目か。表でない行は -1。
    column: int
    text: str


def read_cells(path: str) -> List[Cell]:
    """glossary.md を「検査単位」に切る。表は1セル、それ以外は1行。"""
    cells: List[Cell] = []
    section = ""
    with open(path, encoding="utf-8") as f:
        for i, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")
            if line.startswith("#"):
                section = line.lstrip("#").strip()
            if line.startswith("|"):
                parts = line.split("|")[1:-1] if line.endswith("|") else line.split("|")[1:]
                if all(set(p.strip()) <= set("-: ") for p in parts if p.strip()):
                    continue  # 区切り行
                for col, part in enumerate(parts):
                    cells.append(Cell(i, section, col, part.strip()))
            else:
                cells.append(Cell(i, section, -1, line))
    return cells


def iter_tokens(text: str) -> List[Tuple[int, str, str]]:
    """(開始位置, 種別, 中身) を出現順に返す。種別は code / quote。"""
    tokens = [(m.start(), "code", m.group(1)) for m in CODE_SPAN_RE.finditer(text)]
    masked = CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), text)
    tokens += [(m.start(), "quote", m.group(1)) for m in QUOTE_RE.finditer(masked)]
    tokens.sort()
    return tokens


def normalize_for_match(s: str) -> str:
    """引用の突き合わせ用。空白と強調記号の差を無視する。"""
    return re.sub(r"[\s*\\]", "", s)


#: 参照の内容検証で「直前に名指しした表記」として扱わないコードスパン。
#: パス・ファイル名・省略記号は原文に現れる表記ではないため。
_NOT_A_TERM_RE = re.compile(r"[…]|\.\.\.|\.(rst|md|py|tsv|sh|csv|xls|yaml|json)\b")


def looks_like_term(body: str) -> bool:
    return not _NOT_A_TERM_RE.search(body) and not body.startswith((":", "http"))


# ---------------------------------------------------------------------------
# 検査1: file:line 参照
# ---------------------------------------------------------------------------


def check_refs(cells: Sequence[Cell], known_terms) -> Tuple[int, List[Problem]]:
    """参照の実在と内容を検査する。

    内容の検査は「参照の直前に、同じセルで名指しした表記または引用」が
    参照先の行に実在するかで行う。名指しとして採るのは
    term_candidates.tsv に載っている表記か、「」で囲んだ引用だけにする。
    ルール名やクラス名まで採ると、原文に現れない語を探して誤検知するため。
    """
    problems: List[Problem] = []
    checked = 0
    for cell in cells:
        tokens = iter_tokens(cell.text)
        last_ref: Optional[Tuple[str, bool, int]] = None
        # 直前に名指しされた「表記」または「引用」。参照の内容検証に使う。
        expected: Optional[Tuple[str, str]] = None
        for _, kind, body in tokens:
            resolved = resolve_ref(body) if kind == "code" else None
            short = SHORT_REF_RE.match(body) if kind == "code" else None
            if resolved is None and short is not None and last_ref is not None:
                resolved = (last_ref[0], last_ref[1], int(short.group("line")))
            if resolved is None:
                if kind == "quote":
                    expected = ("quote", body)
                elif body in known_terms:
                    expected = ("code", body)
                continue

            last_ref = resolved
            checked += 1
            rel, from_base, line_no = resolved
            where = f"glossary.md:{cell.line_no}"
            lines = _read_source(rel, from_base)
            if lines is None:
                problems.append(Problem("ref", where, f"ファイルなし: {rel}"))
                continue
            if not (1 <= line_no <= len(lines)):
                problems.append(Problem(
                    "ref", where,
                    f"行番号が範囲外: {rel}:{line_no}（全{len(lines)}行）"))
                continue
            if expected is None:
                continue
            kind_e, want = expected
            haystack = normalize_for_match(lines[line_no - 1])
            needle = normalize_for_match(want)
            if needle and needle not in haystack:
                problems.append(Problem(
                    "ref", where,
                    f"{rel}:{line_no} に{'引用' if kind_e == 'quote' else '表記'}"
                    f" {want!r} が無い: {lines[line_no - 1].strip()[:70]!r}"))
    return checked, problems


# ---------------------------------------------------------------------------
# 検査2: 件数
# ---------------------------------------------------------------------------


def load_scan_counts(path: str) -> Dict[Tuple[str, str], int]:
    counts: Dict[Tuple[str, str], int] = {}
    with open(path, encoding="utf-8") as f:
        rows = csv.DictReader(
            [l for l in f if not l.startswith("#")], delimiter="\t")
        for row in rows:
            counts[(row["surface"], row["corpus"])] = int(row["count"])
    return counts


def check_counts(
    cells: Sequence[Cell], scan_counts: Dict[Tuple[str, str], int]
) -> Tuple[int, List[Problem]]:
    problems: List[Problem] = []
    checked = 0
    for cell in cells:
        if cell.column < 0:
            continue  # 件数の検査対象は表のセルだけ
        tokens = iter_tokens(cell.text)
        for m in COUNT_RE.finditer(cell.text):
            checked += 1
            where = f"glossary.md:{cell.line_no}"
            claim = int(m.group(2).replace(",", ""))
            corpus = COUNT_LABEL_TO_CORPUS[m.group(1)]
            # 同じセル内で、この件数より前にある最後のコードスパンに係る。
            term = None
            for pos, kind, body in tokens:
                if pos < m.start() and kind == "code" and resolve_ref(body) is None \
                        and looks_like_term(body):
                    term = body
            if term is None:
                problems.append(Problem(
                    "count", where,
                    f"{m.group(0)} の係り先が無い（同じセルに表記のコードスパンが必要）"))
                continue
            actual = scan_counts.get((term, corpus))
            if actual is None:
                problems.append(Problem(
                    "count", where,
                    f"{term!r} は scan 出力に無い（term_candidates.tsv 未登録）"))
                continue
            if actual != claim:
                problems.append(Problem(
                    "count", where,
                    f"{term!r} の{m.group(1)}件数: 記載 {claim} / scan {actual}"))
    return checked, problems


# ---------------------------------------------------------------------------
# 検査3・4・5: 表構造の整合
# ---------------------------------------------------------------------------

VARIANT_HEADER = "揺れ表記（使わない）"
OTHER_HEADER = "別義・旧名称（文脈により使う）"
CANONICAL_HEADER = "正表記"


def read_tables(path: str) -> List[Tuple[str, List[str], List[List[str]]]]:
    """(直近の見出し, ヘッダ行, データ行のリスト) を返す。"""
    tables: List[Tuple[str, List[str], List[List[str]]]] = []
    section = ""
    header: Optional[List[str]] = None
    body: List[List[str]] = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith("#"):
                section = line.lstrip("#").strip()
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if all(set(p) <= set("-: ") for p in parts if p):
                    continue
                if header is None:
                    header = parts
                else:
                    body.append(parts)
            else:
                if header is not None:
                    tables.append((section, header, body))
                header, body = None, []
    if header is not None:
        tables.append((section, header, body))
    return tables


def column_terms(tables, header_name: str, section_prefix: str = "") -> Dict[str, str]:
    """指定した見出しの列にあるコードスパンを {表記: 出典セクション} で返す。"""
    found: Dict[str, str] = {}
    for section, header, body in tables:
        if section_prefix and not section.startswith(section_prefix):
            continue
        if header_name not in header:
            continue
        idx = header.index(header_name)
        for row in body:
            if idx >= len(row):
                continue
            for m in CODE_SPAN_RE.finditer(row[idx]):
                body_text = m.group(1)
                if resolve_ref(body_text) or not looks_like_term(body_text):
                    continue
                found.setdefault(body_text, section)
    return found


def check_sections(tables) -> Tuple[int, List[Problem]]:
    """§5 の揺れ表記が §8 の対応表に載っていること。"""
    variants = column_terms(tables, VARIANT_HEADER, "5.")
    mapping_left: Dict[str, str] = {}
    for section, header, body in tables:
        if not section.startswith("8."):
            continue
        for row in body:
            for m in CODE_SPAN_RE.finditer(row[0]):
                mapping_left[m.group(1)] = section
    problems = [
        Problem("section", f"§{sec}", f"揺れ表記 {term!r} が §8 対応表に無い")
        for term, sec in sorted(variants.items())
        if term not in mapping_left
    ]
    return len(variants), problems


def check_terms(tables, entries, scan_counts) -> Tuple[int, List[Problem]]:
    """term_candidates.tsv と §5 の表記の集合が一致すること。"""
    canonicals = column_terms(tables, CANONICAL_HEADER, "5.")
    variants = column_terms(tables, VARIANT_HEADER, "5.")
    others = column_terms(tables, OTHER_HEADER, "5.")
    listed = set(canonicals) | set(variants) | set(others)

    tsv_canonical = {e.canonical for e in entries}
    tsv_surface = {e.surface for e in entries}
    # 全コーパスで0件の表記は「念のため探した候補」であり、§5 への掲載は求めない。
    attested = {
        s for s in tsv_surface
        if any(scan_counts.get((s, c), 0) for c in dtv.ALL_CORPORA)
    }
    problems: List[Problem] = []
    for c in sorted(tsv_canonical - set(canonicals)):
        problems.append(Problem("term", "§5", f"tsv の正表記 {c!r} が §5 の正表記列に無い"))
    for s in sorted(attested - listed):
        problems.append(Problem(
            "term", "§5", f"tsv の表記 {s!r}（出現あり）が §5 のどの列にも無い"))
    for t in sorted(listed - tsv_surface):
        problems.append(Problem(
            "term", "§5", f"§5 の表記 {t!r} が term_candidates.tsv に無い（件数を検証できない）"))
    return len(listed), problems


def check_applies(tables) -> Tuple[int, List[Problem]]:
    """§8 対応表の全行に適用条件が書かれていること。"""
    problems: List[Problem] = []
    rows = 0
    for section, header, body in tables:
        if not section.startswith("8."):
            continue
        if "適用条件" not in header:
            problems.append(Problem("applies", f"§{section}", "対応表に「適用条件」列が無い"))
            continue
        idx = header.index("適用条件")
        for row in body:
            rows += 1
            if idx >= len(row) or not row[idx]:
                problems.append(Problem(
                    "applies", f"§{section}", f"適用条件が空: {row[0][:40]}"))
    return rows, problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="用語集の記述を出典と scan 出力に突き合わせる")
    parser.add_argument("--glossary", default=DEFAULT_GLOSSARY)
    parser.add_argument("--scan", default=DEFAULT_SCAN)
    parser.add_argument("--terms", default=dtv.DEFAULT_TERMS_FILE)
    args = parser.parse_args(argv)

    cells = read_cells(args.glossary)
    tables = read_tables(args.glossary)
    entries = dtv.load_terms(args.terms)
    scan_counts = load_scan_counts(args.scan)

    results = [
        ("refs", *check_refs(cells, {e.surface for e in entries})),
        ("counts", *check_counts(cells, scan_counts)),
        ("sections", *check_sections(tables)),
        ("terms", *check_terms(tables, entries, scan_counts)),
        ("applies", *check_applies(tables)),
    ]

    problems: List[Problem] = []
    print(f"基準コミット(NTF:) {dtv.base_commit()}")
    for name, checked, found in results:
        print(f"{name:<10} 検証 {checked:>4} 件 / 不一致 {len(found):>3} 件")
        problems.extend(found)

    if problems:
        print("\n--- 不一致の内訳 ---")
        for p in problems:
            print(f"[{p.kind}] {p.where}: {p.detail}")
        print(f"\n不一致 {len(problems)} 件")
        return 1
    print("\nRESULT: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
