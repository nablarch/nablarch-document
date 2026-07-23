#!/usr/bin/env python3
"""
extract_rst.py -- RST ファイルから構造項目を抽出して CSV に出力する。

usage: python extract_rst.py <input_dir> <output_csv> [<base_dir>]

  <base_dir>  : file フィールドの相対パス基点ディレクトリ（省略時は git リポジトリルート）。
                一時ディレクトリから展開した RST を処理する場合に指定する。
"""

import csv
import os
import re
import sys


# ---------------------------------------------------------------------------
# RST 見出し判定ヘルパー
# ---------------------------------------------------------------------------

ADORN_CHARS = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~=")


def is_adornment_line(line: str) -> bool:
    """行がアドーンメント（見出し装飾）行かどうか判定する。"""
    stripped = line.rstrip("\n")
    if len(stripped) < 2:
        return False
    ch = stripped[0]
    if ch not in ADORN_CHARS:
        return False
    return all(c == ch for c in stripped)


def adorn_char(line: str) -> str:
    return line.rstrip("\n")[0]


# ---------------------------------------------------------------------------
# RST パーサー
# ---------------------------------------------------------------------------

def parse_rst_file(filepath: str, repo_root: str):
    """
    RST ファイルを解析して (line, kind, depth, path_str, title, detail) のリストを返す。
    file フィールドはリポジトリルートからの相対パス。
    """
    rel_path = os.path.relpath(filepath, repo_root)

    with open(filepath, encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    lines = [l.rstrip("\n") for l in raw_lines]
    n = len(lines)

    # ------------------------------------------------------------------
    # 1st pass: 見出し構造を収集する
    # ------------------------------------------------------------------
    # RST の相対レベル: ファイル内で最初に登場した装飾文字がレベル1、次がレベル2...
    # オーバーライン付き（前後に装飾行）と アンダーラインのみを区別する。
    # ここでは両方を同一ランクで扱い、登場順にレベルを割り当てる。

    char_to_level: dict[str, int] = {}
    level_counter = [0]

    def get_level(ch: str) -> int:
        if ch not in char_to_level:
            level_counter[0] += 1
            char_to_level[ch] = level_counter[0]
        return char_to_level[ch]

    # heading エントリ: (lineno_1indexed, depth, title_text)
    headings: list[tuple[int, int, str]] = []

    i = 0
    while i < n:
        # オーバーライン付き見出し: 装飾行 + テキスト行 + 同じ装飾行
        if is_adornment_line(lines[i]) and i + 2 < n:
            ch = adorn_char(lines[i])
            text_line = lines[i + 1].strip()
            if (
                text_line
                and is_adornment_line(lines[i + 2])
                and adorn_char(lines[i + 2]) == ch
                and len(lines[i].rstrip()) >= len(text_line)
            ):
                depth = get_level(ch)
                headings.append((i + 2, depth, text_line))  # 行番号はアンダーライン行
                i += 3
                continue

        # アンダーラインのみの見出し: テキスト行 + 装飾行
        if (
            i + 1 < n
            and is_adornment_line(lines[i + 1])
            and lines[i].strip()
            and not is_adornment_line(lines[i])
        ):
            ch = adorn_char(lines[i + 1])
            text_line = lines[i].strip()
            depth = get_level(ch)
            headings.append((i + 2, depth, text_line))  # 1-indexed: アンダーライン行
            i += 2
            continue

        i += 1

    # headings をラインインデックスのセットに変換（title行・adornment行）
    heading_lines: set[int] = set()
    heading_by_adorn: dict[int, tuple[int, str]] = {}  # adorn_lineno(0-indexed) -> (depth, title)

    # 再度スキャンして heading に使われた行を記録
    i = 0
    temp_heading_idx = 0
    seen_headings = []
    i = 0
    while i < n:
        if is_adornment_line(lines[i]) and i + 2 < n:
            ch = adorn_char(lines[i])
            text_line = lines[i + 1].strip()
            if (
                text_line
                and is_adornment_line(lines[i + 2])
                and adorn_char(lines[i + 2]) == ch
                and len(lines[i].rstrip()) >= len(text_line)
            ):
                depth = char_to_level.get(ch, 0)
                seen_headings.append((i, i + 1, i + 2, depth, text_line))
                heading_lines.update([i, i + 1, i + 2])
                heading_by_adorn[i + 2] = (depth, text_line)
                i += 3
                continue

        if (
            i + 1 < n
            and is_adornment_line(lines[i + 1])
            and lines[i].strip()
            and not is_adornment_line(lines[i])
        ):
            ch = adorn_char(lines[i + 1])
            text_line = lines[i].strip()
            depth = char_to_level.get(ch, 0)
            seen_headings.append((i, None, i + 1, depth, text_line))
            heading_lines.update([i, i + 1])
            heading_by_adorn[i + 1] = (depth, text_line)
            i += 2
            continue

        i += 1

    # ------------------------------------------------------------------
    # 見出しパスを管理するスタック
    # ------------------------------------------------------------------
    heading_stack: list[tuple[int, str]] = []  # (depth, title)

    def build_path(stack: list[tuple[int, str]]) -> str:
        return " > ".join(t for _, t in stack)

    # ------------------------------------------------------------------
    # 2nd pass: 各要素を抽出
    # ------------------------------------------------------------------
    records = []

    def add_record(lineno_1idx, kind, depth, path_str, title, detail):
        records.append({
            "file": rel_path,
            "line": lineno_1idx,
            "kind": kind,
            "depth": depth,
            "path": path_str,
            "title": title,
            "detail": detail,
        })

    # 見出しレコードを先に追加し、heading_stack を更新するためにスキャン
    # 並行して para / code / table / figure / admonition / toctree も拾う
    # 一度の線形スキャンで処理する

    i = 0
    skip_until = -1  # ブロック終了まで通常処理をスキップ

    while i < n:
        if i <= skip_until:
            i += 1
            continue

        line = lines[i]

        # ---- 見出し (overline付き) ----
        if is_adornment_line(line) and i + 2 < n:
            ch = adorn_char(line)
            text_line = lines[i + 1].strip()
            if (
                text_line
                and is_adornment_line(lines[i + 2])
                and adorn_char(lines[i + 2]) == ch
                and len(line.rstrip()) >= len(text_line)
            ):
                depth = char_to_level.get(ch, 1)
                while heading_stack and heading_stack[-1][0] >= depth:
                    heading_stack.pop()
                path_str = build_path(heading_stack)
                heading_stack.append((depth, text_line))
                add_record(i + 3, "heading", depth, path_str, text_line, "")
                skip_until = i + 2
                i += 3
                continue

        # ---- 見出し (underlineのみ) ----
        if (
            i + 1 < n
            and is_adornment_line(lines[i + 1])
            and line.strip()
            and not is_adornment_line(line)
        ):
            ch = adorn_char(lines[i + 1])
            text_line = line.strip()
            depth = char_to_level.get(ch, 1)
            while heading_stack and heading_stack[-1][0] >= depth:
                heading_stack.pop()
            path_str = build_path(heading_stack)
            heading_stack.append((depth, text_line))
            add_record(i + 2, "heading", depth, path_str, text_line, "")
            skip_until = i + 1
            i += 2
            continue

        # ---- ディレクティブ系 ----
        directive_match = re.match(r'^(\s*)\.\.\s+(\S+)::(.*)', line)
        if directive_match:
            indent = directive_match.group(1)
            directive_name = directive_match.group(2).lower().rstrip(":")
            directive_arg = directive_match.group(3).strip()
            path_str = build_path(heading_stack)

            # toctree
            if directive_name == "toctree":
                entries = []
                j = i + 1
                while j < n:
                    jline = lines[j]
                    if not jline.strip():
                        j += 1
                        continue
                    # オプション行（:maxdepth: 等）はスキップ
                    if re.match(r'^\s+:\w[\w-]*:', jline):
                        j += 1
                        continue
                    # インデントがある行がエントリ
                    if jline.startswith(indent + "   ") or (indent == "" and jline.startswith("   ")):
                        entries.append(jline.strip())
                        j += 1
                    else:
                        break
                detail = ";".join(entries)
                add_record(i + 1, "toctree", 0, path_str, "toctree", detail)
                skip_until = j - 1
                i = j
                continue

            # code-block
            if directive_name in ("code-block", "code", "sourcecode"):
                lang = directive_arg
                # ブロック本体収集
                j = i + 1
                # オプション行をスキップ
                while j < n and re.match(r'^\s+:\w[\w-]*:', lines[j]):
                    j += 1
                # 空行スキップ
                while j < n and not lines[j].strip():
                    j += 1
                # インデントされた行を収集
                code_lines = []
                while j < n and (lines[j].startswith("    ") or lines[j].startswith("\t") or not lines[j].strip()):
                    if lines[j].strip():
                        code_lines.append(lines[j].strip())
                    j += 1
                detail = "\n".join(code_lines[:3])
                add_record(i + 1, "code", 0, path_str, lang, detail)
                skip_until = j - 1
                i = j
                continue

            # figure / image
            if directive_name in ("figure", "image"):
                img_path = directive_arg
                # :target: オプションを探す
                j = i + 1
                target = ""
                while j < n and (re.match(r'^\s+:', lines[j]) or not lines[j].strip()):
                    m = re.match(r'^\s+:target:\s+(.*)', lines[j])
                    if m:
                        target = m.group(1).strip()
                    j += 1
                detail = target if target else img_path
                add_record(i + 1, "figure", 0, path_str, "", detail)
                skip_until = j - 1
                i = j
                continue

            # admonition
            if directive_name in ("tip", "note", "important", "warning", "caution", "hint", "attention", "danger", "error"):
                # 本文収集
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                body_lines = []
                while j < n and (lines[j].startswith("   ") or lines[j].startswith("\t")):
                    body_lines.append(lines[j].strip())
                    j += 1
                body = " ".join(body_lines)
                detail = body[:80]
                add_record(i + 1, "admonition", 0, path_str, directive_name, detail)
                skip_until = j - 1
                i = j
                continue

            i += 1
            continue

        # ---- :: によるコードブロック ----
        if line.rstrip().endswith("::") and not line.strip().startswith(".."):
            path_str = build_path(heading_stack)
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            code_lines = []
            while j < n and (lines[j].startswith("    ") or lines[j].startswith("\t") or not lines[j].strip()):
                if lines[j].strip():
                    code_lines.append(lines[j].strip())
                j += 1
            if code_lines:
                detail = "\n".join(code_lines[:3])
                add_record(i + 1, "code", 0, path_str, "", detail)
                skip_until = j - 1
                i = j
                continue

        # ---- グリッドテーブル ----
        if re.match(r'^\+[-=+]+\+', line):
            path_str = build_path(heading_stack)
            # 1行目のセル内容を取得
            j = i + 1
            cells = []
            if j < n and lines[j].startswith("|"):
                cells = [c.strip() for c in lines[j].split("|") if c.strip()]
            # テーブル末尾まで
            while j < n and re.match(r'^[+|]', lines[j]):
                j += 1
            detail = " | ".join(cells)
            add_record(i + 1, "table", 0, path_str, "", detail)
            skip_until = j - 1
            i = j
            continue

        # ---- シンプルテーブル ----
        if re.match(r'^={2,}(\s+={2,})+\s*$', line):
            path_str = build_path(heading_stack)
            j = i + 1
            cells = []
            if j < n and lines[j].strip() and not re.match(r'^={2,}', lines[j]):
                cells = lines[j].split()
            while j < n and lines[j].strip():
                j += 1
            detail = " | ".join(cells)
            add_record(i + 1, "table", 0, path_str, "", detail)
            skip_until = j - 1
            i = j
            continue

        # ---- 段落 ----
        if line.strip() and not is_adornment_line(line) and not line.startswith(".."):
            # 見出し行は除外（前後にアドーンメント行がある行）
            if i not in heading_lines:
                path_str = build_path(heading_stack)
                # 段落全体を収集
                para_lines = []
                j = i
                while j < n and lines[j].strip() and not is_adornment_line(lines[j]):
                    if j not in heading_lines:
                        para_lines.append(lines[j].strip())
                    j += 1
                para_text = " ".join(para_lines)
                detail = para_text[:160]
                add_record(i + 1, "para", 0, path_str, "", detail)
                skip_until = j - 1
                i = j
                continue

        i += 1

    return records


# ---------------------------------------------------------------------------
# メインエントリポイント
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"usage: python {sys.argv[0]} <input_dir> <output_csv> [<base_dir>]", file=sys.stderr)
        sys.exit(1)

    input_dir = sys.argv[1]
    output_csv = sys.argv[2]

    if len(sys.argv) == 4:
        # 明示的に base_dir が指定された場合はそれを使用
        repo_root = sys.argv[3]
    else:
        # リポジトリルートの推定: このスクリプトの位置から上に辿る
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = input_dir  # デフォルト
        check = script_dir
        for _ in range(10):
            if os.path.isdir(os.path.join(check, ".git")):
                repo_root = check
                break
            check = os.path.dirname(check)

    # RST ファイルを収集
    rst_files = []
    for root, dirs, files in os.walk(input_dir):
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".rst"):
                rst_files.append(os.path.join(root, fname))

    fieldnames = ["file", "line", "kind", "depth", "path", "title", "detail"]

    with open(output_csv, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(
            fout,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for rst_file in rst_files:
            records = parse_rst_file(rst_file, repo_root)
            writer.writerows(records)

    # 行数をカウント（ヘッダー除く）
    with open(output_csv, encoding="utf-8") as f:
        row_count = sum(1 for _ in f) - 1
    print(f"Wrote {row_count} rows to {output_csv}")


if __name__ == "__main__":
    main()
