#!/usr/bin/env python3
"""
extract_md.py -- Markdown ファイルから見出し・コードブロックを抽出して CSV に出力する。

usage: python extract_md.py <input_dir> <output_csv>
"""

import csv
import os
import re
import sys


def parse_md_file(filepath: str, repo_root: str):
    """
    Markdown ファイルを解析して (line, kind, depth, path, title, detail) のリストを返す。
    """
    rel_path = os.path.relpath(filepath, repo_root)

    with open(filepath, encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    lines = [l.rstrip("\n") for l in raw_lines]
    n = len(lines)

    records = []
    heading_stack: list[tuple[int, str]] = []  # (depth, title)

    def build_path(stack: list[tuple[int, str]]) -> str:
        return " > ".join(t for _, t in stack)

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

    i = 0
    in_code_fence = False
    fence_char = ""
    fence_lang = ""
    fence_start_line = 0
    fence_body_lines: list[str] = []

    while i < n:
        line = lines[i]

        # ---- コードフェンスの開始・終了 ----
        fence_match = re.match(r'^(`{3,}|~{3,})(.*)', line)
        if fence_match:
            fence_delim = fence_match.group(1)
            if not in_code_fence:
                # フェンス開始
                in_code_fence = True
                fence_char = fence_delim[0]
                fence_lang = fence_match.group(2).strip()
                fence_start_line = i
                fence_body_lines = []
                i += 1
                continue
            else:
                # フェンス終了（同じ文字種かつ同じ以上の長さ）
                if fence_delim[0] == fence_char and len(fence_delim) >= len(fence_delim):
                    path_str = build_path(heading_stack)
                    detail_lines = [l for l in fence_body_lines if l.strip()]
                    detail_lang = fence_lang
                    detail_content = "\n".join(detail_lines[:3])
                    if detail_lang:
                        detail = detail_lang + "\n" + detail_content if detail_content else detail_lang
                    else:
                        detail = detail_content
                    add_record(fence_start_line + 1, "code", 0, path_str, fence_lang, detail)
                    in_code_fence = False
                    fence_body_lines = []
                    i += 1
                    continue

        if in_code_fence:
            fence_body_lines.append(line)
            i += 1
            continue

        # ---- 見出し ----
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            depth = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # スタックを更新
            while heading_stack and heading_stack[-1][0] >= depth:
                heading_stack.pop()
            path_str = build_path(heading_stack)
            heading_stack.append((depth, title))
            add_record(i + 1, "heading", depth, path_str, title, "")
            i += 1
            continue

        # ---- Setext 形式の見出し（= か - のアンダーライン） ----
        if i + 1 < n and line.strip() and not in_code_fence:
            next_line = lines[i + 1]
            if re.match(r'^={3,}\s*$', next_line):
                depth = 1
                title = line.strip()
                while heading_stack and heading_stack[-1][0] >= depth:
                    heading_stack.pop()
                path_str = build_path(heading_stack)
                heading_stack.append((depth, title))
                add_record(i + 2, "heading", depth, path_str, title, "")
                i += 2
                continue
            if re.match(r'^-{3,}\s*$', next_line):
                depth = 2
                title = line.strip()
                while heading_stack and heading_stack[-1][0] >= depth:
                    heading_stack.pop()
                path_str = build_path(heading_stack)
                heading_stack.append((depth, title))
                add_record(i + 2, "heading", depth, path_str, title, "")
                i += 2
                continue

        i += 1

    return records


def main():
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv[0]} <input_dir> <output_csv>", file=sys.stderr)
        sys.exit(1)

    input_dir = sys.argv[1]
    output_csv = sys.argv[2]

    # リポジトリルートの推定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = input_dir
    check = script_dir
    for _ in range(10):
        if os.path.isdir(os.path.join(check, ".git")):
            repo_root = check
            break
        check = os.path.dirname(check)

    # MD ファイルを収集
    md_files = []
    for root, dirs, files in os.walk(input_dir):
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".md"):
                md_files.append(os.path.join(root, fname))

    fieldnames = ["file", "line", "kind", "depth", "path", "title", "detail"]

    with open(output_csv, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(
            fout,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for md_file in md_files:
            records = parse_md_file(md_file, repo_root)
            writer.writerows(records)

    with open(output_csv, encoding="utf-8") as f:
        row_count = sum(1 for _ in f) - 1
    print(f"Wrote {row_count} rows to {output_csv}")


if __name__ == "__main__":
    main()
