#!/usr/bin/env python3
"""semdiff.py — Sphinx HTMLツリーの意味的差分検証器 (cmd_707 P2-1)

新旧2つのビルド済みHTMLツリーを比較し、以下を機械検証する。

  V1: テキスト保全 — 旧ビルド本文の可読テキストが新ビルド本文に
      ページ単位で全量包含されること(包含照合・Unicode正規化なし)。
  V2: リンク保全 — 内部リンク/アンカー/画像/ダウンロード資材が
      新ビルド内で全て解決すること(新規リグレッションのみNG)。
      資材は「各ビルド内で解決したhref」をキーに内容SHA-256で照合
      する(新旧間の絶対ファイル名一致は判定に使わない)。
  V3: 仕分け — 差異を 意味的差異(NG) / 表示上の差異(許容) /
      グレー(人手判定) に3分類したレポートを出力する。

サブコマンド:
  verify   OLD_TREE NEW_TREE [--json OUT] [--limit N]
           → 合否判定。exit 0 = PASS, 2 = 意味的差異あり(NG)
  coverage TREE [--json OUT]
           → 本文抽出セレクタの被覆率検査(canary)。全ページの
             可読テキストノードが「本文コンテナ ∪ 既知チューム
             (ナビ・フッタ等)」で100%被覆されることを確認する。
             exit 0 = 被覆率100%, 2 = 被覆漏れあり

設計出典: output/dev/nablarch/cmd_707_modernization_design.md §4
"""

import argparse
import hashlib
import json
import posixpath
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

import lxml.html
from lxml.html import HTMLParser

# ---------------------------------------------------------------------------
# 抽出ルール
# ---------------------------------------------------------------------------

# 本文コンテナ候補 (優先順)。旧テーマ(rtd 0.2.4)・新テーマ(rtd 3.x)とも
# div[role="main"] を持つことを設計時に確認済み。
MAIN_XPATHS = [
    '//*[@role="main"]',
    '//*[contains(concat(" ", normalize-space(@class), " "), " rst-content ")]',
    '//*[contains(concat(" ", normalize-space(@class), " "), " document ")]',
]

# 可読テキストとして扱わないタグ
SKIP_TAGS = {"script", "style", "noscript", "template", "head", "title"}

# ブロック境界を成すタグ (この単位でテキスト片に分割する)
BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "caption", "colgroup",
    "dd", "details", "div", "dl", "dt", "fieldset", "figcaption", "figure",
    "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
    "legend", "li", "main", "nav", "ol", "option", "p", "pre", "section",
    "select", "summary", "table", "tbody", "td", "tfoot", "th", "thead",
    "tr", "ul",
}

# チューム(テーマ側UI)として被覆検査で許容するコンテナの判定
CHROME_TAGS = {"nav", "header", "footer"}
CHROME_ROLES = {"navigation", "search", "contentinfo", "banner"}
CHROME_CLASSES = {
    # sphinx-rtd-theme (旧0.2.4 / 新3.x 共通系)
    "wy-nav-side", "wy-side-nav-search", "wy-nav-top", "wy-breadcrumbs",
    "rst-versions", "rst-footer-buttons", "wy-menu",
    # basic/classic テーマ由来のフォールバック
    "sphinxsidebar", "related", "footer", "header", "searchbox",
    # 検索ページ等の動的プレースホルダ
    "search-summary",
}

# 生成系UIページ (rst由来の本文を持たないためV1/V2の対象外。存在自体は確認する)
GENERATED_BASENAMES = {"genindex.html", "search.html", "np-modindex.html",
                       "py-modindex.html", "modindex.html"}


def is_verbatim_page(rel: str) -> bool:
    """_static配下のHTML = Sphinxが変換せず逐語コピーする持込資材
    (例: yuidoc生成のJS APIドキュメント群)。テーマ構造を持たないため
    意味抽出は適用せず、より厳格なバイト同一(SHA-256)で照合する。"""
    return rel.startswith("_static/") or "/_static/" in rel

EXTERNAL_SCHEMES = ("http:", "https:", "mailto:", "ftp:", "javascript:",
                    "tel:", "data:")

_WS_RE = re.compile(r"\s+")

_PARSER = HTMLParser(encoding="utf-8")


def norm_text(s: str) -> str:
    """連続空白・改行の畳み込みのみ。Unicode正規化は行わない(意図的)。"""
    return _WS_RE.sub(" ", s).strip()


def _classes(el) -> set:
    return set((el.get("class") or "").split())


def is_headerlink(el) -> bool:
    return el.tag == "a" and "headerlink" in _classes(el)


def is_chrome(el) -> bool:
    if not isinstance(el.tag, str):
        return False
    if el.tag in CHROME_TAGS:
        return True
    if (el.get("role") or "") in CHROME_ROLES:
        return True
    if _classes(el) & CHROME_CLASSES:
        return True
    return False


def is_main(el) -> bool:
    if not isinstance(el.tag, str):
        return False
    if (el.get("role") or "") == "main":
        return True
    return False


# ---------------------------------------------------------------------------
# ページ解析
# ---------------------------------------------------------------------------

def _walk_segments(el, out):
    """DOMを辿り、テキストトークン列(ブロック境界=None)をoutへ集める。"""
    if not isinstance(el.tag, str):  # コメント・PI等
        if el.tail:
            out.append(el.tail)
        return
    if el.tag in SKIP_TAGS or is_headerlink(el):
        if el.tail:
            out.append(el.tail)
        return
    block = el.tag in BLOCK_TAGS
    if block:
        out.append(None)
    if el.tag == "br":
        out.append(" ")
    if el.text:
        out.append(el.text)
    for child in el:
        _walk_segments(child, out)
    if block:
        out.append(None)
    if el.tail:
        out.append(el.tail)


def extract_segments(root) -> list:
    """ブロック要素単位の正規化テキスト片リストを返す。"""
    tokens = []
    _walk_segments(root, tokens)
    segs, buf = [], []
    for tok in tokens:
        if tok is None:
            if buf:
                seg = norm_text("".join(buf))
                if seg:
                    segs.append(seg)
                buf = []
        else:
            buf.append(tok)
    if buf:
        seg = norm_text("".join(buf))
        if seg:
            segs.append(seg)
    return segs


class PageInfo:
    __slots__ = ("rel", "segments", "full_text", "ids", "page_links",
                 "fragments", "asset_refs", "external_urls", "main_found")

    def __init__(self):
        self.rel = None
        self.segments = []
        self.full_text = ""
        self.ids = set()
        self.page_links = set()       # 解決済み相対パス(ページ)
        self.fragments = set()        # (解決済みパス, フラグメント)
        self.asset_refs = []          # 解決済み相対パス(画像・DL資材等)
        self.external_urls = set()
        self.main_found = True


def resolve_ref(page_rel: str, href: str):
    """ページからの相対hrefをツリー内相対パス+fragmentへ解決する。"""
    href = href.strip()
    parts = urlsplit(href)
    frag = unquote(parts.fragment) if parts.fragment else None
    path = unquote(parts.path)
    if not path:
        return page_rel, frag  # 自ページ内アンカー
    base = posixpath.dirname(page_rel)
    target = posixpath.normpath(posixpath.join(base, path))
    return target, frag


def parse_page(tree_root: Path, rel: str) -> PageInfo:
    info = PageInfo()
    info.rel = rel
    doc = lxml.html.parse(str(tree_root / rel), parser=_PARSER).getroot()
    if doc is None:
        info.main_found = False
        return info

    # id/nameはページ全域から収集 (アンカー解決先は本文外にもあり得る)
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        v = el.get("id")
        if v:
            info.ids.add(v)
        if el.tag == "a":
            v = el.get("name")
            if v:
                info.ids.add(v)

    main = None
    for xp in MAIN_XPATHS:
        found = doc.xpath(xp)
        if found:
            main = found[0]
            break
    if main is None:
        info.main_found = False
        body = doc.find("body")
        main = body if body is not None else doc

    info.segments = extract_segments(main)
    info.full_text = " ".join(info.segments)

    for el in main.iter():
        if not isinstance(el.tag, str):
            continue
        if el.tag == "a":
            href = (el.get("href") or "").strip()
            if not href or href == "#" or is_headerlink(el):
                continue
            if href.lower().startswith(EXTERNAL_SCHEMES) or href.startswith("//"):
                info.external_urls.add(href)
                continue
            target, frag = resolve_ref(rel, href)
            if target.endswith((".html", ".htm")) or target == rel:
                info.page_links.add(target)
                if frag:
                    info.fragments.add((target, frag))
            else:
                info.asset_refs.append(target)
        elif el.tag in ("img", "embed", "source"):
            src = (el.get("src") or "").strip()
            if src and not src.lower().startswith(EXTERNAL_SCHEMES) \
                    and not src.startswith("//"):
                target, _ = resolve_ref(rel, src)
                info.asset_refs.append(target)
        elif el.tag == "object":
            data = (el.get("data") or "").strip()
            if data and not data.lower().startswith(EXTERNAL_SCHEMES):
                target, _ = resolve_ref(rel, data)
                info.asset_refs.append(target)
    return info


# ---------------------------------------------------------------------------
# ツリー走査
# ---------------------------------------------------------------------------

def list_pages(tree: Path) -> list:
    return sorted(
        str(p.relative_to(tree)).replace("\\", "/")
        for p in tree.rglob("*.html")
    )


def file_sha256(path: Path, cache: dict) -> str:
    key = str(path)
    if key not in cache:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        cache[key] = h.hexdigest()
    return cache[key]


def broken_refs(tree: Path, pages: dict) -> set:
    """ツリー内で解決不能な内部参照 (page, kind, ref) の集合。"""
    out = set()
    for rel, info in pages.items():
        for target in info.page_links:
            if target not in pages:
                if not (tree / target).exists():
                    out.add((rel, "page-link", target))
        for target, frag in info.fragments:
            tinfo = pages.get(target)
            if tinfo is None:
                if not (tree / target).exists():
                    out.add((rel, "page-link", target))
                continue
            if frag not in tinfo.ids:
                out.add((rel, "anchor", f"{target}#{frag}"))
        for target in info.asset_refs:
            if not (tree / target).exists():
                out.add((rel, "asset", target))
    return out


# ---------------------------------------------------------------------------
# verify (V1+V2+V3)
# ---------------------------------------------------------------------------

def cmd_verify(args):
    old_root = Path(args.old_tree).resolve()
    new_root = Path(args.new_tree).resolve()
    for r in (old_root, new_root):
        if not r.is_dir():
            print(f"ERROR: not a directory: {r}", file=sys.stderr)
            return 1

    old_pages_list = list_pages(old_root)
    new_pages_list = list_pages(new_root)
    if args.limit:
        old_pages_list = old_pages_list[: args.limit]

    ng = []          # 意味的差異 (1件でも不合格)
    gray = []        # 人手判定
    report_only = {"anchor_id_diffs": [], "fragment_diffs": [],
                   "old_build_broken_refs": [], "generated_pages_skipped": []}
    display_only_pages = []
    byte_identical_pages = []
    text_pass_pages = []

    new_set = set(new_pages_list)
    missing_pages = [p for p in old_pages_list if p not in new_set]
    for p in missing_pages:
        ng.append({"page": p, "type": "page-missing",
                   "detail": "旧ビルドのページが新ビルドに存在しない"})
    added_pages = [p for p in new_pages_list if p not in set(old_pages_list)] \
        if not args.limit else []

    sha_cache_old, sha_cache_new = {}, {}
    old_infos, new_infos = {}, {}

    compare_pages = [p for p in old_pages_list if p in new_set]
    generated = [p for p in compare_pages
                 if posixpath.basename(p) in GENERATED_BASENAMES]
    report_only["generated_pages_skipped"] = generated

    # 逐語コピー資材ページ(_static配下): バイト同一で照合 (V1/V2より厳格)
    verbatim_pages = [p for p in compare_pages if is_verbatim_page(p)
                      and posixpath.basename(p) not in GENERATED_BASENAMES]
    verbatim_identical = 0
    for rel in verbatim_pages:
        if (old_root / rel).read_bytes() == (new_root / rel).read_bytes():
            verbatim_identical += 1
        else:
            ng.append({"page": rel, "type": "verbatim-page-changed",
                       "detail": "_static配下の逐語コピーHTMLが"
                                 "バイト不一致(内容改変の疑い)"})

    content_pages = [p for p in compare_pages
                     if posixpath.basename(p) not in GENERATED_BASENAMES
                     and not is_verbatim_page(p)]

    for rel in content_pages:
        old_bytes = (old_root / rel).read_bytes()
        new_bytes = (new_root / rel).read_bytes()
        byte_same = old_bytes == new_bytes

        oi = parse_page(old_root, rel)
        ni = parse_page(new_root, rel)
        old_infos[rel] = oi
        new_infos[rel] = ni
        if not oi.main_found:
            gray.append({"page": rel, "type": "no-main-container-old",
                         "detail": "旧側で本文コンテナ未検出(body全体で比較)"})
        if not ni.main_found:
            ng.append({"page": rel, "type": "no-main-container-new",
                       "detail": "新側で本文コンテナ未検出。抽出前提が崩れて"
                                 "いるため要修正(false-PASS防止のためNG扱い)"})
            continue

        # ---- V1: テキスト包含照合 ----
        new_counter = Counter(ni.segments)
        new_full = ni.full_text
        page_missing_segs = []
        used_fallback = False
        for seg, cnt in Counter(oi.segments).items():
            have = new_counter.get(seg, 0)
            if have >= cnt:
                continue
            occurrences = new_full.count(seg)
            if occurrences >= cnt:
                used_fallback = True  # 分割/結合/移動はされたが全量存在
                continue
            page_missing_segs.append(seg)
        for seg in page_missing_segs:
            ng.append({"page": rel, "type": "text-missing",
                       "detail": seg[:400]})

        # ---- V2: 参照保全 (ページ単位の意味比較) ----
        lost_links = oi.page_links - ni.page_links
        for t in lost_links:
            ng.append({"page": rel, "type": "page-link-lost",
                       "detail": f"旧本文にあった内部リンク先 {t} が"
                                 f"新本文のリンク集合に存在しない"})
        lost_ext = oi.external_urls - ni.external_urls
        for u in lost_ext:
            ng.append({"page": rel, "type": "external-url-lost",
                       "detail": u})

        # 資材: 各ビルド内で解決したhrefをキーに内容SHA-256の多重集合で照合。
        # 新旧間のファイル名一致は判定に使わない。
        def asset_hashes(info, root, cache, missing_sink):
            hashes = Counter()
            for target in info.asset_refs:
                p = root / target
                if p.exists():
                    hashes[file_sha256(p, cache)] += 1
                else:
                    missing_sink.append(target)
            return hashes

        old_missing_assets, new_missing_assets = [], []
        oh = asset_hashes(oi, old_root, sha_cache_old, old_missing_assets)
        nh = asset_hashes(ni, new_root, sha_cache_new, new_missing_assets)
        lost_hashes = oh - nh
        for h, cnt in lost_hashes.items():
            srcs = sorted({t for t in oi.asset_refs
                           if (old_root / t).exists()
                           and file_sha256(old_root / t, sha_cache_old) == h})
            ng.append({"page": rel, "type": "asset-content-lost",
                       "detail": f"旧本文が参照する資材(SHA-256={h[:16]}…, "
                                 f"旧経路例: {srcs[:3]})と同内容の資材が"
                                 f"新本文の参照先に{cnt}件不足"})
        for t in old_missing_assets:
            report_only.setdefault("old_build_missing_assets", []).append(
                {"page": rel, "ref": t})

        # ---- report-only: アンカーID・フラグメントの新旧差 ----
        old_only_ids = oi.ids - ni.ids
        if old_only_ids:
            report_only["anchor_id_diffs"].append(
                {"page": rel, "old_only_ids": sorted(old_only_ids)[:50],
                 "count": len(old_only_ids)})
        frag_diff = oi.fragments - ni.fragments
        if frag_diff:
            report_only["fragment_diffs"].append(
                {"page": rel,
                 "old_only": sorted(f"{t}#{f}" for t, f in frag_diff)[:50]})

        # ---- V3: ページ分類 ----
        if page_missing_segs or lost_links or lost_ext or lost_hashes:
            pass  # 既にNG計上済み
        elif byte_same:
            byte_identical_pages.append(rel)
        elif used_fallback or oi.segments != ni.segments and \
                not _is_superset_sequence(oi.segments, ni.segments):
            gray.append({"page": rel, "type": "text-moved",
                         "detail": "本文テキストは全量存在するが配置/分割が"
                                   "変化(人手確認推奨)"})
        elif oi.segments == ni.segments:
            display_only_pages.append(rel)
        else:
            text_pass_pages.append(rel)  # 新側の追加テキストのみ(許容)

    # ---- V2: ビルド内自己整合 (新規リグレッションのみNG) ----
    old_all = {rel: (old_infos.get(rel) or parse_page(old_root, rel))
               for rel in content_pages}
    new_all = {rel: (new_infos.get(rel) or parse_page(new_root, rel))
               for rel in content_pages if rel in new_infos}
    old_broken = broken_refs(old_root, old_all)
    new_broken = broken_refs(new_root, new_all)
    regressions = new_broken - old_broken
    for page, kind, ref in sorted(regressions):
        ng.append({"page": page, "type": f"unresolved-{kind}",
                   "detail": f"新ビルド内で解決不能: {ref}"})
    report_only["old_build_broken_refs"] = [
        {"page": p, "kind": k, "ref": r} for p, k, r in sorted(old_broken)]

    verdict = "NG" if ng else "PASS"
    result = {
        "old": str(old_root), "new": str(new_root),
        "verdict": verdict,
        "summary": {
            "pages_old": len(old_pages_list),
            "pages_new": len(new_pages_list),
            "pages_compared": len(content_pages),
            "verbatim_pages_compared": len(verbatim_pages),
            "verbatim_pages_identical": verbatim_identical,
            "generated_pages_skipped": len(generated),
            "missing_pages": missing_pages,
            "added_pages": added_pages,
            "ng_count": len(ng),
            "gray_count": len(gray),
            "byte_identical": len(byte_identical_pages),
            "display_only": len(display_only_pages),
            "text_pass_with_additions": len(text_pass_pages),
            "old_build_broken_refs": len(old_broken),
            "new_build_broken_refs": len(new_broken),
            "broken_ref_regressions": len(regressions),
        },
        "ng": ng,
        "gray": gray,
        "report_only": report_only,
    }
    _emit(result, args.json_out)
    print(f"[semdiff verify] verdict={verdict} ng={len(ng)} "
          f"gray={len(gray)} compared={len(content_pages)} "
          f"(byte-identical={len(byte_identical_pages)}, "
          f"display-only={len(display_only_pages)})")
    for item in ng[:20]:
        print(f"  NG {item['type']}: {item['page']} :: "
              f"{item['detail'][:120]}")
    if len(ng) > 20:
        print(f"  ... 他 {len(ng)-20} 件 (JSONレポート参照)")
    return 0 if verdict == "PASS" else 2


def _is_superset_sequence(old_segs, new_segs):
    """new_segs が old_segs を順序保存で包含するか(追加のみか)を判定。"""
    it = iter(new_segs)
    return all(seg in it for seg in old_segs)


# ---------------------------------------------------------------------------
# coverage (穴1対策 canary)
# ---------------------------------------------------------------------------

def _coverage_walk(el, in_main, in_chrome, gaps, covered_len, page_rel):
    """テキストノードごとに main/chrome の被覆を判定する。"""
    if not isinstance(el.tag, str):
        return covered_len
    if el.tag in SKIP_TAGS or is_headerlink(el):
        return covered_len
    now_main = in_main or is_main(el)
    now_chrome = in_chrome or is_chrome(el)
    if el.text:
        t = norm_text(el.text)
        if t:
            if now_main or now_chrome:
                covered_len += len(t)
            else:
                gaps.append({"page": page_rel, "text": t[:200],
                             "element": el.tag})
    for child in el:
        covered_len = _coverage_walk(child, now_main, now_chrome, gaps,
                                     covered_len, page_rel)
        if child.tail:
            t = norm_text(child.tail)
            if t:
                # tail は child の親(=el)のコンテキストに属する
                if now_main or now_chrome:
                    covered_len += len(t)
                else:
                    gaps.append({"page": page_rel, "text": t[:200],
                                 "element": f"{child.tag}(tail)"})
    return covered_len


def cmd_coverage(args):
    root = Path(args.tree).resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 1
    pages = [p for p in list_pages(root)
             if posixpath.basename(p) not in GENERATED_BASENAMES
             and not is_verbatim_page(p)]
    if args.limit:
        pages = pages[: args.limit]
    gaps = []
    total_covered = 0
    total_gap = 0
    no_main = []
    for rel in pages:
        doc = lxml.html.parse(str(root / rel), parser=_PARSER).getroot()
        if doc is None:
            no_main.append(rel)
            continue
        if not doc.xpath(MAIN_XPATHS[0]):
            no_main.append(rel)
        body = doc.find("body")
        if body is None:
            continue
        page_gaps = []
        total_covered = _coverage_walk(body, False, False, page_gaps,
                                       total_covered, rel)
        gaps.extend(page_gaps)
        total_gap += sum(len(g["text"]) for g in page_gaps)

    denom = total_covered + total_gap
    ratio = (total_covered / denom * 100.0) if denom else 100.0
    ok = not gaps and not no_main
    result = {
        "tree": str(root),
        "pages_scanned": len(pages),
        "coverage_percent": round(ratio, 6),
        "uncovered_text_nodes": len(gaps),
        "pages_without_main_container": no_main,
        "gaps": gaps[:200],
        "verdict": "PASS" if ok else "NG",
    }
    _emit(result, args.json_out)
    print(f"[semdiff coverage] pages={len(pages)} "
          f"coverage={ratio:.4f}% gaps={len(gaps)} "
          f"no-main={len(no_main)} verdict={result['verdict']}")
    for g in gaps[:10]:
        print(f"  GAP {g['page']} <{g['element']}>: {g['text'][:100]}")
    return 0 if ok else 2


# ---------------------------------------------------------------------------

def _emit(obj, path):
    if path:
        Path(path).write_text(
            json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="V1+V2+V3 意味的差分検証")
    v.add_argument("old_tree")
    v.add_argument("new_tree")
    v.add_argument("--json", dest="json_out", default=None)
    v.add_argument("--limit", type=int, default=0,
                   help="先頭Nページのみ比較(動作確認用)")
    v.set_defaults(func=cmd_verify)

    c = sub.add_parser("coverage", help="本文抽出セレクタ被覆率検査(canary)")
    c.add_argument("tree")
    c.add_argument("--json", dest="json_out", default=None)
    c.add_argument("--limit", type=int, default=0)
    c.set_defaults(func=cmd_coverage)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
