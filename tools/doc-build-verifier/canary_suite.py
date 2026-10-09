#!/usr/bin/env python3
"""canary_suite.py — semdiff.py の自己検証(故意破壊テスト) (cmd_707 P2-1)

実ビルド済みHTMLツリー(基準ビルド)を入力に、意図的な破壊を仕込んだ
コピーを作り、検証器が
  - 真陽性: 意味的な欠損・破損を確実にNG検出すること
  - 真陰性: 無害な差異(表示差・ファイル名変更等)を誤検出しないこと
を機械的に確認する。全ケース合格で exit 0。

使い方:
  python3 canary_suite.py BASELINE_TREE WORK_DIR
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import lxml.html
from lxml.html import HTMLParser

HERE = Path(__file__).resolve().parent
SEMDIFF = HERE / "semdiff.py"
PARSER = HTMLParser(encoding="utf-8")

RESULTS = []


def log(msg):
    print(msg, flush=True)


def run_verify(old, new, out_json):
    p = subprocess.run(
        [sys.executable, str(SEMDIFF), "verify", str(old), str(new),
         "--json", str(out_json)],
        capture_output=True, text=True)
    data = json.loads(Path(out_json).read_text(encoding="utf-8"))
    return p.returncode, data, p.stdout


def run_coverage(tree, out_json):
    p = subprocess.run(
        [sys.executable, str(SEMDIFF), "coverage", str(tree),
         "--json", str(out_json)],
        capture_output=True, text=True)
    data = json.loads(Path(out_json).read_text(encoding="utf-8"))
    return p.returncode, data, p.stdout


def hardlink_copy(src: Path, dst: Path):
    """ツリーの実コピーを作る。

    基準ビルドはDockerビルド由来でroot所有のため、非rootからの
    ハードリンク作成は fs.protected_hardlinks により拒否される。
    実コピー(cp -a)なら読み取りだけで済み、コピー側は自ユーザ所有と
    なるので後段の破壊(書換・削除)も可能になる。
    """
    if dst.exists():
        shutil.rmtree(dst)
    subprocess.run(["cp", "-a", str(src), str(dst)], check=True)


def rewrite(path: Path, data: bytes):
    """コピー側ファイルを安全に書き換える(元ファイルは触らない)。"""
    os.remove(path)
    path.write_bytes(data)


def load(path: Path):
    return lxml.html.parse(str(path), parser=PARSER).getroot()


def dump(doc) -> bytes:
    return lxml.html.tostring(doc, encoding="utf-8", doctype="<!DOCTYPE html>")


def main_el(doc):
    found = doc.xpath('//*[@role="main"]')
    return found[0] if found else None


def iter_pages(tree: Path):
    for p in sorted(tree.rglob("*.html")):
        if p.name in ("genindex.html", "search.html"):
            continue
        if "_static" in p.parts:  # 逐語コピー資材(バイト照合対象)は触らない
            continue
        yield p


# ---------------------------------------------------------------------------
# 破壊対象の探索 (実データからプログラム的に選ぶ)
# ---------------------------------------------------------------------------

def find_text_page(tree: Path):
    """本文に十分な長さの<p>を持つページを返す。"""
    for p in iter_pages(tree):
        doc = load(p)
        m = main_el(doc)
        if m is None:
            continue
        for para in m.iter("p"):
            if para.text and len(para.text.strip()) >= 60:
                return p, para.text
    raise RuntimeError("suitable text page not found")


def find_asset_page(tree: Path, subdir: str, exts):
    """subdir配下の資材を参照するページと資材相対パスを返す。"""
    for p in iter_pages(tree):
        doc = load(p)
        m = main_el(doc)
        if m is None:
            continue
        for el in m.iter():
            if not isinstance(el.tag, str):
                continue
            ref = el.get("src") if el.tag == "img" else (
                el.get("href") if el.tag == "a" else None)
            if not ref or ref.startswith(("http:", "https:", "#", "mailto:")):
                continue
            if subdir in ref and ref.lower().endswith(exts):
                target = (p.parent / ref.split("#")[0]).resolve()
                if target.exists():
                    return p, ref.split("#")[0], target
    raise RuntimeError(f"page referencing {subdir} not found")


def find_fragment_link(tree: Path):
    """他ページの実在アンカーへ張られたリンク (src_page, href, tgt_page, frag)"""
    for p in iter_pages(tree):
        doc = load(p)
        m = main_el(doc)
        if m is None:
            continue
        for a in m.iter("a"):
            href = a.get("href") or ""
            if "headerlink" in (a.get("class") or ""):
                continue
            if href.startswith(("http:", "https:", "mailto:")) or \
                    "#" not in href or href.startswith("#"):
                continue
            path_part, frag = href.split("#", 1)
            if not path_part.endswith(".html") or not frag:
                continue
            tgt = (p.parent / path_part).resolve()
            if not tgt.exists():
                continue
            tdoc = load(tgt)
            if tdoc.xpath(f'//*[@id={json.dumps(frag)}]'):
                return p, href, tgt, frag
    raise RuntimeError("fragment link not found")


def find_internal_link(tree: Path):
    for p in iter_pages(tree):
        doc = load(p)
        m = main_el(doc)
        if m is None:
            continue
        for a in m.iter("a"):
            href = a.get("href") or ""
            if "headerlink" in (a.get("class") or ""):
                continue
            if href and not href.startswith(("http:", "https:", "#", "mailto:")) \
                    and href.split("#")[0].endswith(".html"):
                tgt = (p.parent / href.split("#")[0]).resolve()
                if tgt.exists():
                    return p, href
    raise RuntimeError("internal link not found")


# ---------------------------------------------------------------------------
# ケース定義
# ---------------------------------------------------------------------------

def check(name, expect_desc, cond, evidence):
    status = "PASS" if cond else "FAIL"
    RESULTS.append((name, status, expect_desc, evidence))
    log(f"  [{status}] {name} — 期待: {expect_desc} / 実測: {evidence}")


def case_tn_identical(base, work):
    log("== TN1: 同一コピー (真陰性: 差異ゼロでPASSすること)")
    c = work / "tn1"
    hardlink_copy(base, c)
    rc, data, _ = run_verify(base, c, work / "tn1.json")
    check("TN1-identical", "verdict=PASS, ng=0",
          rc == 0 and data["verdict"] == "PASS"
          and data["summary"]["ng_count"] == 0,
          f"rc={rc} verdict={data['verdict']} ng={data['summary']['ng_count']}")


def case_tp_sentence_deleted(base, work):
    log("== TP1: 新側から一文の後半を削除 (真陽性: text-missing NG)")
    c = work / "tp1"
    hardlink_copy(base, c)
    page, text = find_text_page(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    for para in main_el(doc).iter("p"):
        if para.text and para.text.strip() == text.strip():
            para.text = para.text[: len(para.text) // 2]
            break
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tp1.json")
    hits = [n for n in data["ng"] if n["type"] == "text-missing"
            and n["page"] == str(rel)]
    check("TP1-sentence-deleted", "text-missing NGを当該ページで検出",
          rc == 2 and len(hits) >= 1,
          f"rc={rc} hits={len(hits)} page={rel}")


def case_tp_page_deleted(base, work):
    log("== TP2: 新側からページ1枚を削除 (真陽性: page-missing NG)")
    c = work / "tp2"
    hardlink_copy(base, c)
    page, _ = find_text_page(base)
    rel = page.relative_to(base)
    os.remove(c / rel)
    rc, data, _ = run_verify(base, c, work / "tp2.json")
    hits = [n for n in data["ng"] if n["type"] == "page-missing"
            and n["page"] == str(rel)]
    check("TP2-page-deleted", "page-missing NGを検出",
          rc == 2 and len(hits) == 1, f"rc={rc} hits={len(hits)} page={rel}")


def case_tp_image_deleted(base, work):
    log("== TP3: 新側から参照画像ファイルを削除 (真陽性: NG)")
    c = work / "tp3"
    hardlink_copy(base, c)
    page, ref, target = find_asset_page(base, "_images", (".png", ".jpg", ".gif", ".svg"))
    rel_img = target.relative_to(base)
    os.remove(c / rel_img)
    rc, data, _ = run_verify(base, c, work / "tp3.json")
    hits = [n for n in data["ng"]
            if n["type"] in ("asset-content-lost", "unresolved-asset")]
    check("TP3-image-deleted", "資材喪失NGを検出",
          rc == 2 and len(hits) >= 1,
          f"rc={rc} hits={len(hits)} img={rel_img}")


def case_tp_image_swapped(base, work):
    log("== TP4: 新側の参照画像を別内容に差し替え (真陽性: asset-content-lost)")
    c = work / "tp4"
    hardlink_copy(base, c)
    page, ref, target = find_asset_page(base, "_images", (".png", ".jpg", ".gif", ".svg"))
    rel_img = target.relative_to(base)
    rewrite(c / rel_img, b"\x89PNG-broken-different-content")
    rc, data, _ = run_verify(base, c, work / "tp4.json")
    hits = [n for n in data["ng"] if n["type"] == "asset-content-lost"]
    check("TP4-image-swapped", "asset-content-lost NGを検出",
          rc == 2 and len(hits) >= 1,
          f"rc={rc} hits={len(hits)} img={rel_img}")


def case_tp_link_broken(base, work):
    log("== TP5: 新側の内部リンクhrefを実在しない先へ改変 (真陽性: NG)")
    c = work / "tp5"
    hardlink_copy(base, c)
    page, href = find_internal_link(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    for a in main_el(doc).iter("a"):
        if (a.get("href") or "") == href:
            a.set("href", "does-not-exist-canary.html")
            break
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tp5.json")
    hits = [n for n in data["ng"]
            if n["type"] in ("unresolved-page-link", "page-link-lost")]
    check("TP5-link-broken", "リンク破損NGを検出",
          rc == 2 and len(hits) >= 1, f"rc={rc} hits={len(hits)} page={rel}")


def case_tp_anchor_removed(base, work):
    log("== TP6: 新側でリンク先アンカーidを削除 (真陽性: unresolved-anchor)")
    c = work / "tp6"
    hardlink_copy(base, c)
    src, href, tgt, frag = find_fragment_link(base)
    rel_tgt = tgt.relative_to(base)
    target = c / rel_tgt
    doc = load(target)
    for el in doc.xpath(f'//*[@id={json.dumps(frag)}]'):
        del el.attrib["id"]
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tp6.json")
    hits = [n for n in data["ng"] if n["type"] == "unresolved-anchor"]
    check("TP6-anchor-removed", "unresolved-anchor NGを検出",
          rc == 2 and len(hits) >= 1,
          f"rc={rc} hits={len(hits)} anchor={rel_tgt}#{frag}")


def case_tp_download_deleted(base, work):
    log("== TP7: 新側からダウンロード資材を削除 (真陽性: NG)")
    c = work / "tp7"
    hardlink_copy(base, c)
    try:
        page, ref, target = find_asset_page(base, "_downloads", tuple([""]))
    except RuntimeError:
        check("TP7-download-deleted", "(_downloads参照が存在しないためスキップ不可)",
              False, "_downloads参照が見つからない")
        return
    rel_dl = target.relative_to(base)
    os.remove(c / rel_dl)
    rc, data, _ = run_verify(base, c, work / "tp7.json")
    hits = [n for n in data["ng"]
            if n["type"] in ("asset-content-lost", "unresolved-asset")]
    check("TP7-download-deleted", "DL資材喪失NGを検出",
          rc == 2 and len(hits) >= 1, f"rc={rc} hits={len(hits)} dl={rel_dl}")


def case_tp_mojibake(base, work):
    log("== TP8: 新側本文の文字を文字化け(置換文字)に改変 (真陽性: text-missing)")
    c = work / "tp8"
    hardlink_copy(base, c)
    page, text = find_text_page(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    for para in main_el(doc).iter("p"):
        if para.text and para.text.strip() == text.strip():
            para.text = "��" + para.text[2:]
            break
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tp8.json")
    hits = [n for n in data["ng"] if n["type"] == "text-missing"
            and n["page"] == str(rel)]
    check("TP8-mojibake", "文字化けをtext-missing NGとして検出",
          rc == 2 and len(hits) >= 1, f"rc={rc} hits={len(hits)} page={rel}")


def case_tp_coverage_orphan(base, work):
    log("== TP9(穴1): 本文コンテナ外・チューム外に本文テキストを注入 → "
        "coverage検査が被覆漏れを検出すること")
    c = work / "tp9"
    hardlink_copy(base, c)
    page, _ = find_text_page(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    body = doc.find("body")
    orphan = lxml.html.fragment_fromstring(
        "<div>COVERAGE-CANARY: この本文テキストは抽出セレクタの外にある</div>")
    body.insert(0, orphan)
    rewrite(target, dump(doc))
    rc, data, _ = run_coverage(c, work / "tp9.json")
    hits = [g for g in data["gaps"] if "COVERAGE-CANARY" in g["text"]]
    check("TP9-coverage-orphan", "被覆漏れテキストを検出しNG",
          rc == 2 and len(hits) >= 1,
          f"rc={rc} gaps={data['uncovered_text_nodes']} hit={len(hits)}")


def case_tn_display_only(base, work):
    log("== TN2: 表示上の差異のみ (span分割・class追加・UI文言追加) → PASS")
    c = work / "tn2"
    hardlink_copy(base, c)
    page, text = find_text_page(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    m = main_el(doc)
    for para in m.iter("p"):
        if para.text and para.text.strip() == text.strip():
            # テキストをspanで分割 (Pygments span分割の模擬)
            full = para.text
            half = len(full) // 2
            para.text = full[:half]
            span = para.makeelement("span", {"class": "canary-highlight"})
            span.text = full[half:]
            para.insert(0, span)
            para.set("class", "canary-restyled")
            break
    # 新テーマがUI文言を本文域へ追加するケースの模擬 (包含照合ゆえ許容)
    extra = lxml.html.fragment_fromstring('<div class="copy-btn">Copy</div>')
    m.append(extra)
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tn2.json")
    check("TN2-display-only", "verdict=PASS (誤検出なし)",
          rc == 0 and data["summary"]["ng_count"] == 0,
          f"rc={rc} ng={data['summary']['ng_count']} page={rel}")


def case_tn_asset_renamed(base, work):
    log("== TN3(穴2): 画像ファイル名を変更しhrefも整合更新 (内容同一) → PASS")
    c = work / "tn3"
    hardlink_copy(base, c)
    page, ref, target = find_asset_page(base, "_images", (".png", ".jpg", ".gif"))
    rel_page = page.relative_to(base)
    rel_img = target.relative_to(base)
    new_name = "renamed-canary-" + target.name
    new_img = c / rel_img.parent / new_name
    renamed_abs = new_img.resolve()
    old_abs = (c / rel_img).resolve()
    os.rename(c / rel_img, new_img)
    # 当該画像ファイル(解決パス一致)を参照する要素のみ更新する。
    # 同名の別ファイル(例: en側の同名画像)を誤って書き換えないこと。
    # Sphinxは縮小画像を <a href="_images/..."><img src="..."></a> と
    # 包むため、img[src] と a[href] の両方を更新する必要がある。
    old_name = target.name
    updated = 0
    for p in iter_pages(c):
        doc = load(p)
        changed = False
        for el in doc.iter("img", "a"):
            attr = "src" if el.tag == "img" else "href"
            ref = el.get(attr) or ""
            if not ref.endswith(old_name):
                continue
            resolved = (p.parent / ref).resolve()
            if resolved == old_abs:
                el.set(attr, ref[: -len(old_name)] + new_name)
                changed = True
        if changed:
            rewrite(p, dump(doc))
            updated += 1
    rc, data, _ = run_verify(base, c, work / "tn3.json")
    check("TN3-asset-renamed", "ファイル名不一致でも内容同一ならPASS(穴2対策)",
          rc == 0 and data["summary"]["ng_count"] == 0,
          f"rc={rc} ng={data['summary']['ng_count']} "
          f"renamed={rel_img.name}→{new_name} updated_pages={updated}")


def case_tn_anchor_renamed(base, work):
    log("== TN4: アンカーidを新ビルド内で整合的に改名 → PASS (report-onlyに記録)")
    c = work / "tn4"
    hardlink_copy(base, c)
    src, href, tgt, frag = find_fragment_link(base)
    new_frag = frag + "-renamed-canary"
    rel_tgt = tgt.relative_to(base)
    # id改名
    target = c / rel_tgt
    doc = load(target)
    for el in doc.xpath(f'//*[@id={json.dumps(frag)}]'):
        el.set("id", new_frag)
    rewrite(target, dump(doc))
    # 該当フラグメント参照のうち「改名したページ(解決パス一致)への参照」
    # のみ更新する。パス部が空(自ページ内リンク)の場合は、そのページが
    # 改名対象ページ自身であるときに限って更新する (en側の同名アンカーを
    # 持つ別ページを誤って書き換えないこと)。
    tgt_abs = (c / rel_tgt).resolve()
    for p in iter_pages(c):
        doc = load(p)
        changed = False
        for a in doc.iter("a"):
            h = a.get("href") or ""
            if not h.endswith("#" + frag):
                continue
            path_part = h.split("#")[0]
            if path_part:
                if (p.parent / path_part).resolve() != tgt_abs:
                    continue
            elif p.resolve() != tgt_abs:
                continue
            a.set("href", h[: -len(frag)] + new_frag)
            changed = True
        if changed:
            rewrite(p, dump(doc))
    rc, data, _ = run_verify(base, c, work / "tn4.json")
    reported = any(d for d in data["report_only"]["anchor_id_diffs"]
                   if d["page"] == str(rel_tgt))
    check("TN4-anchor-renamed", "PASSかつ旧IDの差をreport-onlyに記録",
          rc == 0 and data["summary"]["ng_count"] == 0 and reported,
          f"rc={rc} ng={data['summary']['ng_count']} reported={reported}")


def case_tn_old_side_deletion(base, work):
    log("== TN5: 旧側コピーから一文削除し(旧⊂新の方向), 包含照合ゆえPASSとなる"
        "こと (仕様確認)")
    c = work / "tn5"
    hardlink_copy(base, c)
    page, text = find_text_page(base)
    rel = page.relative_to(base)
    target = c / rel
    doc = load(target)
    for para in main_el(doc).iter("p"):
        if para.text and para.text.strip() == text.strip():
            para.getparent().remove(para)
            break
    rewrite(target, dump(doc))
    rc, data, _ = run_verify(c, base, work / "tn5.json")  # 旧=削除版
    check("TN5-old-side-deletion", "新側超過は許容されPASS",
          rc == 0 and data["summary"]["ng_count"] == 0,
          f"rc={rc} ng={data['summary']['ng_count']}")


def case_coverage_full(base, work):
    log("== 穴1本検査: 基準ビルド全ページの被覆率100%確認")
    rc, data, _ = run_coverage(base, work / "coverage_full.json")
    check("COVERAGE-full-tree", "被覆率100%・被覆漏れ0件",
          rc == 0 and data["coverage_percent"] == 100.0
          and data["uncovered_text_nodes"] == 0,
          f"rc={rc} coverage={data['coverage_percent']}% "
          f"gaps={data['uncovered_text_nodes']} "
          f"no-main={len(data['pages_without_main_container'])} "
          f"pages={data['pages_scanned']}")


CASES = {
    "coverage": case_coverage_full,
    "tn1": case_tn_identical,
    "tp1": case_tp_sentence_deleted,
    "tp2": case_tp_page_deleted,
    "tp3": case_tp_image_deleted,
    "tp4": case_tp_image_swapped,
    "tp5": case_tp_link_broken,
    "tp6": case_tp_anchor_removed,
    "tp7": case_tp_download_deleted,
    "tp8": case_tp_mojibake,
    "tp9": case_tp_coverage_orphan,
    "tn2": case_tn_display_only,
    "tn3": case_tn_asset_renamed,
    "tn4": case_tn_anchor_renamed,
    "tn5": case_tn_old_side_deletion,
}


def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        print("  第3引数(任意): 実行ケースのカンマ区切り (例: tn3,tn4)")
        sys.exit(1)
    base = Path(sys.argv[1]).resolve()
    work = Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    selected = (sys.argv[3].split(",") if len(sys.argv) == 4
                else list(CASES.keys()))

    for name in selected:
        CASES[name](base, work)

    log("")
    log("=== 結果一覧 ===")
    fails = 0
    for name, status, expect, evidence in RESULTS:
        log(f"[{status}] {name}: {evidence}")
        if status != "PASS":
            fails += 1
    log(f"=== 合計 {len(RESULTS)} ケース / FAIL {fails} 件 ===")
    sys.exit(0 if fails == 0 else 2)


if __name__ == "__main__":
    main()
