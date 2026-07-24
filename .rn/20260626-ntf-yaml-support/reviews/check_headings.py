#!/usr/bin/env python3
"""
check_headings.py — RST heading structure analyzer

Usage: python3 check_headings.py <rst_file> [<rst_file> ...]

Determines heading level by tracking the ORDER of first appearance of each
decorator pattern in the file (RST spec: first decorator found = Level 1
within that file).

Output format:
  File: <path>
  L<line>  L<file_level>  <decorator_char><style>  <heading_text>
"""

import sys
import re


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
    """Analyze heading structure of a single RST file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    n = len(lines)
    results = []

    # RST heading detection:
    # A heading is: [optional overline] + text line + underline
    # Where overline and underline are same char, text is non-blank non-decorator

    # Pass 1: detect all heading occurrences with their decorator char and style
    i = 0
    while i < n:
        line = lines[i].rstrip('\n')
        dec = is_decorator_line(line)

        if dec is not None:
            # Could be start of over+under, or the underline of under-only
            # Look ahead for text + possible underline
            if i + 1 < n:
                text_line = lines[i + 1].rstrip('\n')
                # text_line should be non-empty and not a decorator itself
                if text_line.strip() and not is_decorator_line(text_line):
                    # Check if there's an underline after
                    if i + 2 < n:
                        under_line = lines[i + 2].rstrip('\n')
                        under_dec = is_decorator_line(under_line)
                        if under_dec == dec:
                            # over+under pattern
                            heading_line_num = i + 2  # 1-indexed line of text = i+2
                            results.append({
                                'line': i + 2,  # 1-indexed line number of text
                                'char': dec,
                                'style': 'over+under',
                                'text': text_line.strip(),
                            })
                            i += 3
                            continue
            # It's not an over+under start — could be an underline for previous text
            # Check if previous non-blank line is text
            if i > 0:
                prev_line = lines[i - 1].rstrip('\n')
                if prev_line.strip() and not is_decorator_line(prev_line):
                    # under-only: prev_line is the heading text
                    results.append({
                        'line': i,  # 1-indexed line number of underline; text is i (1-indexed)
                        'char': dec,
                        'style': 'under-only',
                        'text': prev_line.strip(),
                    })
            i += 1
        else:
            i += 1

    # Pass 2: assign file-level numbers based on order of first appearance
    # key = (char, style)
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_headings.py <rst_file> [<rst_file> ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        print(f"File: {filepath}")
        try:
            rows = analyze_rst_headings(filepath)
            if not rows:
                print("  (no headings found)")
            else:
                for line_num, file_level, char, style, text in rows:
                    print(f"  L{line_num:<5} FL{file_level}  {char} {style:<12}  {text}")
        except FileNotFoundError:
            print(f"  ERROR: file not found")
        except Exception as e:
            print(f"  ERROR: {e}")
        print()


if __name__ == '__main__':
    main()
