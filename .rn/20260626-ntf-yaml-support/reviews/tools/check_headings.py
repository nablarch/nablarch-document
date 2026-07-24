#!/usr/bin/env python3
"""
check_headings.py — RST heading structure analyzer + C-04 finding generator

Usage:
  # Heading structure report (human-readable)
  python3 check_headings.py <rst_file> [<rst_file> ...]

  # C-04 finding CSV (pipe-ready, for gate3-findings.csv C-04 rows)
  python3 check_headings.py --findings <repo_root> <rst_file> [<rst_file> ...]

C-04 standard body (from gate3-conventions.md):
  FL1  =  over+under
  FL2  -  over+under
  FL3  =  under-only
  FL4  -  under-only
  FL5  ~  under-only

--findings mode emits CSV rows (no header) for every FL that deviates from
the standard.  finding_id is auto-assigned starting from the first free slot
after existing non-C-04 findings (caller merges them in).  fix_proposal is
intentionally left empty — the coordinator fills it.
"""

import sys
import re
import os

# C-04 standard: file_level -> (char, style)
C04_STANDARD = {
    1: ('=', 'over+under'),
    2: ('-', 'over+under'),
    3: ('=', 'under-only'),
    4: ('-', 'under-only'),
    5: ('~', 'under-only'),
}


def is_decorator_line(line):
    """Return the decorator char if the line is a valid RST heading decorator, else None."""
    stripped = line.rstrip('\n')
    if len(stripped) == 0:
        return None
    char = stripped[0]
    if char not in ('=', '-', '~', '^', '+', '#', '*', '@'):
        return None
    if all(c == char for c in stripped) and len(stripped) >= 2:
        return char
    return None


def analyze_rst_headings(filepath):
    """Analyze heading structure of a single RST file.

    Returns list of (line_num, file_level, char, style, text).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    n = len(lines)
    results = []

    i = 0
    while i < n:
        line = lines[i].rstrip('\n')
        dec = is_decorator_line(line)

        if dec is not None:
            # Attempt over+under: current line is overline, next is text, i+2 is underline
            if i + 2 < n:
                text_line = lines[i + 1].rstrip('\n')
                under_line = lines[i + 2].rstrip('\n')
                if (text_line.strip()
                        and not is_decorator_line(text_line)
                        and is_decorator_line(under_line) == dec):
                    results.append({
                        'line': i + 2,  # 1-indexed: text line
                        'char': dec,
                        'style': 'over+under',
                        'text': text_line.strip(),
                    })
                    i += 3
                    continue
            # Attempt under-only: previous non-blank line is text
            if i > 0:
                prev_line = lines[i - 1].rstrip('\n')
                if prev_line.strip() and not is_decorator_line(prev_line):
                    results.append({
                        'line': i,  # 1-indexed: underline line (text is i-1)
                        'char': dec,
                        'style': 'under-only',
                        'text': prev_line.strip(),
                    })
            i += 1
        else:
            i += 1

    # Assign file-level numbers based on order of first appearance
    level_map = {}
    level_counter = 0
    output_rows = []
    for r in results:
        key = (r['char'], r['style'])
        if key not in level_map:
            level_counter += 1
            level_map[key] = level_counter
        file_level = level_map[key]
        output_rows.append((r['line'], file_level, r['char'], r['style'], r['text']))

    return output_rows


def generate_c04_findings(filepath, repo_root, first_finding_id):
    """Compare heading structure against C-04 standard.

    Returns list of CSV row strings (no header, no fix_proposal).
    finding_id starts at first_finding_id (int).
    """
    rows = analyze_rst_headings(filepath)
    if not rows:
        return []

    # Find which file_levels deviate from C-04 standard
    # Group by file_level to report each level once
    seen_levels = {}
    for line_num, file_level, char, style, text in rows:
        if file_level not in seen_levels:
            seen_levels[file_level] = (line_num, char, style, text)

    # Make path relative to repo_root for CSV
    try:
        rel_path = os.path.relpath(filepath, repo_root)
    except ValueError:
        rel_path = filepath

    csv_rows = []
    fid = first_finding_id
    for level in sorted(seen_levels.keys()):
        line_num, char, style, text = seen_levels[level]
        if level > 5:
            # Beyond standard range — flag as deviation
            expected_char, expected_style = '(L5超: 規約未定義)', ''
        elif (char, style) == C04_STANDARD[level]:
            continue  # Conforms to standard
        else:
            expected_char, expected_style = C04_STANDARD[level]

        if level <= 5:
            expected_str = f"{expected_char} {expected_style}"
        else:
            expected_str = expected_char

        detected_str = f"FL{level} に {char} {style} を使用（例: 「{text}」L{line_num}）"

        # Count occurrences of this level for the detected description
        count = sum(1 for _, fl, _, _, _ in rows if fl == level)
        if count > 1:
            detected_str = f"FL{level} に {char} {style} を使用（{count}箇所、例: 「{text}」L{line_num}）"

        csv_rows.append(
            f"F-{fid:03d},{rel_path},{line_num},C-04,"
            f"{detected_str},"
            f"FL{level} は {expected_str}（C-04 規定）,"
            f"medium,"  # fix_proposal empty — coordinator fills
        )
        fid += 1

    return csv_rows


def print_report(filepath):
    """Print human-readable heading structure report."""
    print(f"File: {filepath}")
    try:
        rows = analyze_rst_headings(filepath)
        if not rows:
            print("  (no headings found)")
        else:
            for line_num, file_level, char, style, text in rows:
                print(f"  L{line_num:<5} FL{file_level}  {char} {style:<12}  {text}")
    except FileNotFoundError:
        print("  ERROR: file not found")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == '--findings':
        if len(args) < 3:
            print("Usage: check_headings.py --findings <repo_root> <rst_file> [...]")
            sys.exit(1)
        repo_root = args[1]
        files = args[2:]
        fid = 1
        all_rows = []
        for filepath in files:
            rows = generate_c04_findings(filepath, repo_root, fid)
            all_rows.extend(rows)
            fid += len(rows)
        for row in all_rows:
            print(row)
    else:
        for filepath in args:
            print_report(filepath)


if __name__ == '__main__':
    main()
