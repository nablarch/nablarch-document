"""
verify_glossary.py
用語集 mapping/glossary.md の記述を出典と scan 出力に突き合わせる。

用語集の価値はほぼ全部が「file:line」と「N件」である。tsv や出典が変われば
これらは黙って古くなるため、#2/#2a の verify_coverage.py と同じ水準で
機械的に検査する。検査は9つ。

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

以下は #3 の母集団の再構成（term-candidates.csv による用語候補の網羅的な
機械抽出）に対応する4検査。3ラウンドのレビューがいずれも新しい抜けを
指摘し続けた原因は、用語集が「カバーすべき用語の母集団」を定義していな
かったことにあるため、母集団と用語集の対応を機械的に閉じる。

用語集の役割を「ページ作成時に表記を揃えるための参照物」に縮小した
（`steering.md` #3差し戻し）ため、判定は「採用」「不採用（理由付き）」
「一括：今回は判定しない」の3値のいずれかに全候補が対応していることを
機械検証する。理由の非空チェック（reasons）は「不採用（理由付き）」に
のみ適用し、「一括：今回は判定しない」には個別理由を要求しない。

  population        `mapping/term-candidates.csv` の全候補（表記の集合）が、
                     §5（採用）／§5.15 の不採用テーブル（理由付き）／
                     §5.15 の一括判定テーブルのいずれかに対応していること。
                     未判定を1件でも許さない。

  design_sections   term-candidates.csv の design-heading 候補（`design.md`
                     の章・セクション見出し）が、すべて glossary.md 中の
                     どこかのコードスパンとして存在すること。

  scheme_names      term-candidates.csv の design-scheme 候補（`design.md`
                     「5. 処理方式の名称」表の名称列）が、すべて §5.2 の
                     「正表記」列に文字列一致すること。

  reasons            §5.15 の不採用（理由付き）テーブルの全行に、空でない
                     理由が書かれていること。「一括：今回は判定しない」の
                     表（「候補」列のみ）は対象外（個別理由を要求しない）。

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
DEFAULT_CANDIDATES = os.path.join(MAPPING_DIR, "term-candidates.csv")

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
# 検査6〜9: term-candidates.csv による母集団の全件判定（#3 の再構成）
# ---------------------------------------------------------------------------

CANDIDATE_HEADER = "候補"
REASON_HEADER = "理由"


class CandidateRow(NamedTuple):
    term: str
    source: str
    occurrences: int
    file_line: str


def load_candidates(path: str) -> List[CandidateRow]:
    """`mapping/term-candidates.csv` を読む。csv.DictReader を使う（wc -l は使わない）。"""
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [
        CandidateRow(r["term"], r["source"], int(r["occurrences"]), r["file_line"])
        for r in rows
    ]


def listed_terms(tables) -> "set[str]":
    """§5（用語）に採用済みとして載っている表記の集合。"""
    canonicals = column_terms(tables, CANONICAL_HEADER, "5.")
    variants = column_terms(tables, VARIANT_HEADER, "5.")
    others = column_terms(tables, OTHER_HEADER, "5.")
    return set(canonicals) | set(variants) | set(others)


def rejected_terms(tables) -> Dict[str, str]:
    """「候補」列と「理由」列を持つ表（§5.15 の不採用〈理由付き〉テーブル）から

    {候補の表記: 理由} を作る。「候補」セル1つに複数のコードスパンが
    束ねてある行（表を圧縮した行）は、含まれる表記すべてに同じ理由を
    割り当てる。理由が空の行は採らない（reasons 検査が別途報告する）。
    候補ごとの理由を書かず一括判定する表（`bulk_terms` が読む、ヘッダーが
    「候補」の1列のみの表）はここでは扱わない。
    """
    result: Dict[str, str] = {}
    for _section, header, body in tables:
        if CANDIDATE_HEADER not in header or REASON_HEADER not in header:
            continue
        idx_cand = header.index(CANDIDATE_HEADER)
        idx_reason = header.index(REASON_HEADER)
        for row in body:
            if idx_cand >= len(row) or idx_reason >= len(row):
                continue
            reason = row[idx_reason].strip()
            if not reason:
                continue
            for m in CODE_SPAN_RE.finditer(row[idx_cand]):
                result.setdefault(m.group(1), reason)
    return result


def bulk_terms(tables) -> "set[str]":
    """§5.15 の「一括：今回は判定しない」表から候補の集合を返す。

    掲載基準（§3）の2種類（表記揺れが実在し正表記を確定した用語／
    `design.md` が章・セクション名として使う用語）のいずれにも該当しない
    候補は、候補ごとの個別理由を書かず一括で記録する（`steering.md` #3
    差し戻し）。この一括判定の表は「候補」列だけを持ち「理由」列を
    持たない（ヘッダーが `["候補"]` の1列のみ）ことで見分ける。1セルに
    複数のコードスパンを束ねた行（表を圧縮した行）は展開する。
    """
    result: "set[str]" = set()
    for _section, header, body in tables:
        if header != [CANDIDATE_HEADER]:
            continue
        idx_cand = header.index(CANDIDATE_HEADER)
        for row in body:
            if idx_cand >= len(row):
                continue
            for m in CODE_SPAN_RE.finditer(row[idx_cand]):
                result.add(m.group(1))
    return result


def check_population(tables, candidates: Sequence[CandidateRow]) -> Tuple[int, List[Problem]]:
    """term-candidates.csv の全候補（表記の集合）が、次の3値のいずれかに

    対応していること。未判定を1件でも許さない。

    - 採用（§5 のいずれかのコードスパンと文字列一致）
    - 不採用（理由付き）（§5.15 の候補＋理由の表に対応する理由がある）
    - 一括：今回は判定しない（§5.15 の候補のみの表に載っている）
    """
    listed = listed_terms(tables)
    rejected = rejected_terms(tables)
    bulk = bulk_terms(tables)
    unique_terms = sorted({c.term for c in candidates})
    problems: List[Problem] = []
    for term in unique_terms:
        if term in listed or term in rejected or term in bulk:
            continue
        problems.append(Problem(
            "population", "term-candidates.csv",
            f"候補 {term!r} が未判定（§5に採用も§5.15に不採用の理由も一括判定も無い）"))
    return len(unique_terms), problems


def check_design_sections(cells: Sequence[Cell], candidates: Sequence[CandidateRow]) -> Tuple[int, List[Problem]]:
    """design-heading 候補（design.md の章・セクション見出し）が

    すべて glossary.md 中のどこかのコードスパンとして存在すること。
    `cells` は `read_cells` の結果（1セル=1行のテキスト）を使う。生の
    ファイル全文に対して正規表現をかけると、コードブロックの ``` など
    バッククォートの数が奇数になる行をまたいでマッチが暴走するため。
    """
    spans: "set[str]" = set()
    for cell in cells:
        spans.update(CODE_SPAN_RE.findall(cell.text))
    terms = sorted({c.term for c in candidates if c.source == "design-heading"})
    problems = [
        Problem("design_sections", "design.md",
                f"章・セクション名 {t!r} が glossary.md に無い")
        for t in terms if t not in spans
    ]
    return len(terms), problems


def check_scheme_names(tables, candidates: Sequence[CandidateRow]) -> Tuple[int, List[Problem]]:
    """design-scheme 候補（design.md「5. 処理方式の名称」の名称列）が

    すべて §5.2 の「正表記」列に文字列一致すること。
    """
    canonicals_52 = column_terms(tables, CANONICAL_HEADER, "5.2")
    terms = sorted({c.term for c in candidates if c.source == "design-scheme"})
    problems = [
        Problem("scheme_names", "design.md",
                f"処理方式名 {t!r} が §5.2 の正表記に無い（design.mdの正式名称と不一致）")
        for t in terms if t not in canonicals_52
    ]
    return len(terms), problems


def check_reasons(tables) -> Tuple[int, List[Problem]]:
    """§5.15 の不採用（理由付き）テーブルの全行に、空でない理由が書かれていること。

    対象は「候補」列と「理由」列を両方持つ表だけである。「一括：今回は
    判定しない」の表（「候補」列のみ）は個別理由を要求しないため対象外。
    """
    problems: List[Problem] = []
    rows = 0
    for section, header, body in tables:
        if CANDIDATE_HEADER not in header or REASON_HEADER not in header:
            continue
        idx_reason = header.index(REASON_HEADER)
        for row in body:
            rows += 1
            if idx_reason >= len(row) or not row[idx_reason].strip():
                problems.append(Problem(
                    "reasons", f"§{section}", f"理由が空: {row[0][:40]}"))
    return rows, problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="用語集の記述を出典と scan 出力に突き合わせる")
    parser.add_argument("--glossary", default=DEFAULT_GLOSSARY)
    parser.add_argument("--scan", default=DEFAULT_SCAN)
    parser.add_argument("--terms", default=dtv.DEFAULT_TERMS_FILE)
    parser.add_argument("--candidates", default=DEFAULT_CANDIDATES)
    args = parser.parse_args(argv)

    cells = read_cells(args.glossary)
    tables = read_tables(args.glossary)
    entries = dtv.load_terms(args.terms)
    scan_counts = load_scan_counts(args.scan)
    candidates = load_candidates(args.candidates)

    results = [
        ("refs", *check_refs(cells, {e.surface for e in entries})),
        ("counts", *check_counts(cells, scan_counts)),
        ("sections", *check_sections(tables)),
        ("terms", *check_terms(tables, entries, scan_counts)),
        ("applies", *check_applies(tables)),
        ("population", *check_population(tables, candidates)),
        ("design_sections", *check_design_sections(cells, candidates)),
        ("scheme_names", *check_scheme_names(tables, candidates)),
        ("reasons", *check_reasons(tables)),
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
