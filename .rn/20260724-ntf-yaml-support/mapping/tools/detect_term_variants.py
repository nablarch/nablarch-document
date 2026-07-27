"""
detect_term_variants.py
用語の表記揺れを機械的に検出する。

用途は2つある。

  discover  正解リストを持たずに揺れを見つける。表記を正規化してグループ化し、
            同一の正規化キーに2種類以上の表記が対応するものを揺れとして報告する。
            正規化ルールは --rule で選ぶ。

              punct      読点・接続の揺れ。見出しから「、」「,」「，」「・」
                         「/」「／」「と」「 」を除去して比較する。
                         例: 「主なクラス, リソース」と「主なクラスとリソース」
              paren      括弧の全角・半角の揺れ。見出しの「()」を「（）」に
                         寄せて比較する。
              longvowel  長音記号の揺れ。カタカナ語から「ー」を除去して比較する。
                         例: 「スーパクラス」と「スーパークラス」

  scan      用語定義ファイル（既定は同ディレクトリの term_candidates.tsv）に
            列挙した表記を全コーパスから検索し、出現数と file:line を報告する。
            用語集の「揺れ表記」欄の根拠を機械的に再現するために使う。
            部分文字列の二重計上を避けるため、1行内では長い表記を優先して
            非重複にマッチさせる（「自動テストフレームワーク」がマッチした
            位置では「テストフレームワーク」を数えない）。

コーパス（--corpus で選択、カンマ区切り）:

  current  現行のNTF解説書。ja/development_tools/testing_framework/ 配下の
           .rst を、develop との merge-base の内容で読む（作業ツリーではない）。
           したがって報告される行番号は merge-base 時点の行番号である。
  input    .rn/20260724-ntf-yaml-support/input/ 配下の .md。作業ツリーの行番号。
  fw       FW解説書。ja/application_framework/application_framework/ 配下の
           .rst。作業ツリーの行番号。
  design   .rn/20260724-ntf-yaml-support/design.md。作業ツリーの行番号。

出力はTSV。行はすべて辞書順に整列するため、同じ入力に対して同じ出力を返す。
パスはリポジトリルートからの相対パスで出力する。改行はLF。
"""

import argparse
import os
import re
import subprocess
import sys
from typing import Dict, Iterable, List, NamedTuple, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_sections import parse_headings  # noqa: E402

# ---------------------------------------------------------------------------
# パス解決
# ---------------------------------------------------------------------------

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.abspath(os.path.join(TOOLS_DIR, "..", ".."))
REPO_ROOT = os.path.abspath(os.path.join(SESSION_DIR, "..", ".."))

CURRENT_DOC_ROOT = "ja/development_tools/testing_framework"
FW_DOC_ROOT = "ja/application_framework/application_framework"
INPUT_DIR = os.path.join(SESSION_DIR, "input")
DESIGN_MD = os.path.join(SESSION_DIR, "design.md")

DEFAULT_TERMS_FILE = os.path.join(TOOLS_DIR, "term_candidates.tsv")

ALL_CORPORA = ("current", "input", "fw", "design")
#: discover は語彙の揺れを見るためのものなので、既定ではFW解説書を含めない。
#: FW解説書はNTF以外の話題を大量に含み、正規化グループが実務上の揺れと
#: 無関係な語で埋まるため。--corpus で明示すれば含められる。
DISCOVER_DEFAULT_CORPORA = ("current", "input", "design")
SCAN_DEFAULT_CORPORA = ALL_CORPORA


class Doc(NamedTuple):
    """コーパス中の1ファイル。"""

    corpus: str
    #: リポジトリルートからの相対パス。出力に使う。
    path: str
    #: 行のリスト（改行を含まない）。1行目が index 0。
    lines: List[str]


# ---------------------------------------------------------------------------
# コーパス読み込み
# ---------------------------------------------------------------------------


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", REPO_ROOT, *args],
        check=True, capture_output=True, text=True,
    ).stdout


def base_commit() -> str:
    """現行解説書を読む基準コミット（origin/develop と HEAD の merge-base）。"""
    return _git("merge-base", "origin/develop", "HEAD").strip()


def _load_current(base: str) -> List[Doc]:
    listing = _git("ls-tree", "-r", "--name-only", base, "--", CURRENT_DOC_ROOT + "/")
    docs = []
    for rel in sorted(p for p in listing.splitlines() if p.endswith(".rst")):
        text = _git("show", f"{base}:{rel}")
        docs.append(Doc("current", rel, text.splitlines()))
    return docs


def _load_worktree_tree(corpus: str, root_abs: str, suffix: str) -> List[Doc]:
    docs = []
    paths = []
    for dirpath, dirnames, filenames in os.walk(root_abs):
        dirnames.sort()
        for name in filenames:
            if name.endswith(suffix):
                paths.append(os.path.join(dirpath, name))
    for abs_path in sorted(paths):
        rel = os.path.relpath(abs_path, REPO_ROOT)
        with open(abs_path, encoding="utf-8") as f:
            docs.append(Doc(corpus, rel, f.read().splitlines()))
    return docs


def _load_single(corpus: str, abs_path: str) -> List[Doc]:
    rel = os.path.relpath(abs_path, REPO_ROOT)
    with open(abs_path, encoding="utf-8") as f:
        return [Doc(corpus, rel, f.read().splitlines())]


def load_corpora(names: Sequence[str]) -> List[Doc]:
    """指定されたコーパスを読み込む。戻り値は corpus 名・パスの順に整列済み。"""
    docs: List[Doc] = []
    for name in names:
        if name == "current":
            docs.extend(_load_current(base_commit()))
        elif name == "input":
            docs.extend(_load_worktree_tree("input", INPUT_DIR, ".md"))
        elif name == "fw":
            docs.extend(
                _load_worktree_tree("fw", os.path.join(REPO_ROOT, FW_DOC_ROOT), ".rst")
            )
        elif name == "design":
            docs.extend(_load_single("design", DESIGN_MD))
        else:
            raise ValueError(f"unknown corpus: {name}")
    return sorted(docs, key=lambda d: (ALL_CORPORA.index(d.corpus), d.path))


# ---------------------------------------------------------------------------
# discover — 正規化してグループ化する
# ---------------------------------------------------------------------------

#: 読点・接続の揺れを消すために除去する文字。
_PUNCT_NOISE_RE = re.compile(r"[、,，・･/／\s]|と")
#: 丸括弧（全角・半角）とその中身。
_BRACKET_RE = re.compile(r"[(（]([^()（）]*)[)）]")
#: カタカナ語（3文字以上）。長音を含む連なりを1語として取る。
_KATAKANA_TOKEN_RE = re.compile(r"[ァ-ヶー][ァ-ヶー]{2,}")
_LONG_VOWEL_RE = re.compile(r"ー")


def norm_punct(surface: str) -> str:
    return _PUNCT_NOISE_RE.sub("", surface)


def norm_paren(surface: str) -> str:
    """括弧の中身と全角・半角の差を伏せ、同じ「型」の見出しを1グループにする。"""
    return _BRACKET_RE.sub("（…）", surface)


def norm_longvowel(surface: str) -> str:
    return _LONG_VOWEL_RE.sub("", surface)


def identity(surface: str) -> str:
    return surface


def paren_style(surface: str) -> str:
    """その表記が使っている括弧の種類。開き括弧と閉じ括弧を別々に見る。

    開きと閉じで種類が異なる表記（例: 「（同期応答メッセージ受信処理)」）を
    揺れとして検出するため、両端をそれぞれ判定する。
    """
    styles = set()
    for m in _BRACKET_RE.finditer(surface):
        token = m.group(0)
        styles.add("半角" if token[0] == "(" else "全角")
        styles.add("半角" if token[-1] == ")" else "全角")
    return ",".join(sorted(styles))


def has_bracket(surface: str) -> bool:
    return _BRACKET_RE.search(surface) is not None


def always(surface: str) -> bool:
    return True


class Rule(NamedTuple):
    #: 表記をグループキーに畳む関数。
    normalize: object
    #: 抽出単位。"term" は見出しと「」で囲まれた語、"katakana" はカタカナ語。
    unit: str
    #: 抽出単位のうち、このルールの対象となるものを選ぶ述語。
    applies: object
    #: グループ内で「揺れている」と判定する軸。2種類以上あればグループを報告する。
    distinct_on: object


RULES: Dict[str, Rule] = {
    "punct": Rule(norm_punct, "term", always, identity),
    "paren": Rule(norm_paren, "term", has_bracket, paren_style),
    "longvowel": Rule(norm_longvowel, "katakana", always, identity),
}

#: 本文中で「」に囲まれた語。用語として名指しされている箇所を拾う。
_QUOTED_TERM_RE = re.compile(r"「([^「」]{2,60})」")


def _iter_terms(doc: Doc) -> Iterable[Tuple[str, int]]:
    """(用語らしき文字列, 1始まりの行番号) を返す。見出しと「」内の語を拾う。

    見出しだけでは、正表記の候補が本文でしか言及されない場合（design.md が
    「主なクラスとリソース」を提案しているが見出しではない、など）に揺れの
    対を検出できないため、「」内の語も抽出単位に含める。
    """
    text = "\n".join(doc.lines) + "\n"
    for h in parse_headings(text, doc.path):
        yield h.text, h.text_line + 1
    for i, line in enumerate(doc.lines):
        for m in _QUOTED_TERM_RE.finditer(line):
            yield m.group(1), i + 1


def _iter_katakana(doc: Doc) -> Iterable[Tuple[str, int]]:
    for i, line in enumerate(doc.lines):
        for m in _KATAKANA_TOKEN_RE.finditer(line):
            yield m.group(0), i + 1


_UNIT_ITER = {"term": _iter_terms, "katakana": _iter_katakana}


def discover(docs: Sequence[Doc], rule_name: str) -> List[Dict[str, object]]:
    """正規化キーごとに表記をまとめ、2表記以上のグループだけを返す。"""
    rule = RULES[rule_name]
    iterate = _UNIT_ITER[rule.unit]

    # key -> surface -> [(corpus, path, line), ...]
    groups: Dict[str, Dict[str, List[Tuple[str, str, int]]]] = {}
    for doc in docs:
        for surface, line_no in iterate(doc):
            surface = surface.strip()
            if not surface or not rule.applies(surface):
                continue
            key = rule.normalize(surface)
            if not key:
                continue
            groups.setdefault(key, {}).setdefault(surface, []).append(
                (doc.corpus, doc.path, line_no)
            )

    rows: List[Dict[str, object]] = []
    for key in sorted(groups):
        surfaces = groups[key]
        if len({rule.distinct_on(s) for s in surfaces}) < 2:
            continue
        for surface in sorted(surfaces):
            hits = sorted(surfaces[surface])
            rows.append({
                "rule": rule_name,
                "norm_key": key,
                "surface": surface,
                "count": len(hits),
                "corpora": ",".join(sorted({c for c, _, _ in hits})),
                "locations": ";".join(f"{p}:{n}" for _, p, n in hits),
            })
    return rows


# ---------------------------------------------------------------------------
# scan — 用語定義ファイルの表記を全コーパスから探す
# ---------------------------------------------------------------------------


class TermEntry(NamedTuple):
    category: str
    canonical: str
    surface: str


def load_terms(path: str) -> List[TermEntry]:
    """TSV（category / canonical / surface）を読む。`#` 始まりの行と空行は無視。"""
    entries: List[TermEntry] = []
    seen = set()
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                raise ValueError(
                    f"{path}:{lineno}: 3列（category/canonical/surface）ではない: {line!r}"
                )
            entry = TermEntry(*(p.strip() for p in parts))
            if not entry.surface:
                raise ValueError(f"{path}:{lineno}: surface が空")
            if entry in seen:
                raise ValueError(f"{path}:{lineno}: 重複エントリ: {entry.surface!r}")
            seen.add(entry)
            entries.append(entry)
    return entries


def match_line(line: str, entries: Sequence[TermEntry]) -> List[TermEntry]:
    """1行から、重複しない位置にマッチした表記を返す。長い表記を優先する。

    「自動テストフレームワーク」がマッチした範囲では「テストフレームワーク」を
    数えない。これがないと部分文字列が二重計上され、出現数が根拠にならない。
    """
    candidates: List[Tuple[int, int, TermEntry]] = []
    for entry in entries:
        start = line.find(entry.surface)
        while start != -1:
            candidates.append((start, start + len(entry.surface), entry))
            start = line.find(entry.surface, start + 1)
    # 開始位置の昇順、同位置なら長い方を優先。同長同位置は surface の辞書順で安定化。
    candidates.sort(key=lambda c: (c[0], -(c[1] - c[0]), c[2].surface))

    taken_end = -1
    result: List[TermEntry] = []
    for start, end, entry in candidates:
        if start < taken_end:
            continue
        result.append(entry)
        taken_end = end
    return result


def scan(
    docs: Sequence[Doc],
    entries: Sequence[TermEntry],
    max_locations: int,
) -> List[Dict[str, object]]:
    """表記ごとにコーパス別の出現数と file:line を返す。"""
    # (entry, corpus) -> [(path, line), ...]
    hits: Dict[Tuple[TermEntry, str], List[Tuple[str, int]]] = {}
    for doc in docs:
        for i, line in enumerate(doc.lines):
            for entry in match_line(line, entries):
                hits.setdefault((entry, doc.corpus), []).append((doc.path, i + 1))

    rows: List[Dict[str, object]] = []
    for entry in entries:
        for corpus in ALL_CORPORA:
            found = hits.get((entry, corpus))
            if found is None:
                # そのコーパスを読み込んでいない場合と0件を区別しない。
                # 読み込んだコーパスだけ 0 行として出す。
                if corpus not in {d.corpus for d in docs}:
                    continue
                found = []
            # count はマッチ数、locations は重複を除いた file:line。
            # 1行に同じ表記が複数回出ることがあるため両方を出す。
            distinct = sorted(set(found))
            shown = distinct if max_locations <= 0 else distinct[:max_locations]
            rows.append({
                "category": entry.category,
                "canonical": entry.canonical,
                "surface": entry.surface,
                "corpus": corpus,
                "count": len(found),
                "files": len({p for p, _ in distinct}),
                "locations": ";".join(f"{p}:{n}" for p, n in shown),
            })
    return rows


# ---------------------------------------------------------------------------
# 出力
# ---------------------------------------------------------------------------


def write_tsv(rows: Sequence[Dict[str, object]], columns: Sequence[str], out) -> None:
    out.write("\t".join(columns) + "\n")
    for row in rows:
        out.write("\t".join(str(row[c]) for c in columns) + "\n")


DISCOVER_COLUMNS = ("rule", "norm_key", "surface", "count", "corpora", "locations")
SCAN_COLUMNS = (
    "category", "canonical", "surface", "corpus", "count", "files", "locations",
)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _split_corpora(value: str) -> List[str]:
    names = [v.strip() for v in value.split(",") if v.strip()]
    for name in names:
        if name not in ALL_CORPORA:
            raise argparse.ArgumentTypeError(
                f"unknown corpus {name!r}; choose from {', '.join(ALL_CORPORA)}"
            )
    return names


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="用語の表記揺れを機械的に検出する",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_disc = sub.add_parser("discover", help="正規化グループ化で揺れを見つける")
    p_disc.add_argument("--rule", choices=sorted(RULES), required=True)
    p_disc.add_argument(
        "--corpus", type=_split_corpora,
        default=list(DISCOVER_DEFAULT_CORPORA),
        help="既定: " + ",".join(DISCOVER_DEFAULT_CORPORA),
    )
    p_disc.add_argument("-o", "--out", default="-")

    p_scan = sub.add_parser("scan", help="用語定義ファイルの表記を検索する")
    p_scan.add_argument("--terms", default=DEFAULT_TERMS_FILE)
    p_scan.add_argument(
        "--corpus", type=_split_corpora,
        default=list(SCAN_DEFAULT_CORPORA),
        help="既定: " + ",".join(SCAN_DEFAULT_CORPORA),
    )
    p_scan.add_argument(
        "--max-locations", type=int, default=5,
        help="表記×コーパスごとに出力する file:line の上限。0以下で全件",
    )
    p_scan.add_argument("-o", "--out", default="-")
    return parser


def main(argv: Sequence[str]) -> int:
    args = build_parser().parse_args(argv)
    docs = load_corpora(args.corpus)

    if args.command == "discover":
        rows = discover(docs, args.rule)
        columns = DISCOVER_COLUMNS
    else:
        rows = scan(docs, load_terms(args.terms), args.max_locations)
        columns = SCAN_COLUMNS

    if args.out == "-":
        write_tsv(rows, columns, sys.stdout)
    else:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            write_tsv(rows, columns, f)
    print(f"{len(rows)} rows", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
