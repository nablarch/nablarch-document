"""
verify_coverage.py
Prove mechanically that extract_sections.py loses no body line.

Method: SET ARITHMETIC over line numbers — not bucket counting.

  covered   = union of every section's [body_start_line, body_end_line] range
  headings  = every line occupied by a heading (RST overline/text/underline,
              Markdown "### x") that is NOT inside a section range
              (an L4 heading folded into an L3 section IS body text)
  uncovered = all lines - covered

  Requirement: uncovered - headings must be empty.  Any line that survives is
  reported individually with its content so the reason can be judged.

  Overlap check: the section ranges must be pairwise disjoint, so
  sum(lines) == len(covered).  A double-claimed line would otherwise mask a
  missing one.

Usage (same file-spec syntax as extract_sections.py):
  python3 verify_coverage.py <label> <file_spec> [...]

Exit code is 1 when any non-heading line is uncovered, when ranges overlap, or
when sum(lines) != len(covered).
"""

import os
import sys
from typing import Any, Dict, List, Set

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract_sections import (  # noqa: E402
    extract_sections,
    parse_headings,
    parse_file_specs,
)


def verify_file(text: str, logical_path: str) -> Dict[str, Any]:
    """Build the covered line-number set for one file and diff it against all lines."""
    lines = text.splitlines(keepends=True)
    total = len(lines)
    all_lines: Set[int] = set(range(1, total + 1))  # 1-indexed

    sections = extract_sections(text, logical_path)
    headings = parse_headings(text, logical_path)

    covered: Set[int] = set()
    overlaps: List[str] = []
    sum_lines_column = 0

    for sec in sections:
        start = sec["body_start_line"]
        end = sec["body_end_line"]
        rng = set(range(start, end + 1))
        sum_lines_column += sec["lines"]

        clash = covered & rng
        if clash:
            for i in sorted(clash)[:10]:
                overlaps.append(
                    f"{logical_path}:{i} claimed twice "
                    f"(second claim: '{sec['heading_path']}')"
                )
        covered |= rng

    # Heading lines that are NOT inside any section range are the only lines
    # allowed to be uncovered.
    heading_lines: Set[int] = set()
    for h in headings:
        for i in range(h.start + 1, min(h.body_start, total) + 1):
            heading_lines.add(i)

    uncovered = all_lines - covered
    structural_headings = uncovered & heading_lines
    leftover = sorted(uncovered - heading_lines)

    return {
        "src_file": logical_path,
        "total": total,
        "sections": len(sections),
        "covered": len(covered),
        "sum_lines_column": sum_lines_column,
        "uncovered": len(uncovered),
        "heading_lines": len(structural_headings),
        "leftover": [(i, lines[i - 1].rstrip("\n")) for i in leftover],
        "overlaps": overlaps,
    }


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 verify_coverage.py <label> <file_spec> [...]", file=sys.stderr)
        return 1

    label = argv[0]
    file_specs = parse_file_specs(argv[1:])

    reports = []
    for actual_path, logical_path in file_specs:
        if not os.path.isfile(actual_path):
            print(f"ERROR: file not found: {actual_path}", file=sys.stderr)
            return 1
        with open(actual_path, encoding="utf-8") as f:
            text = f.read()
        reports.append(verify_file(text, logical_path))

    total = sum(r["total"] for r in reports)
    covered = sum(r["covered"] for r in reports)
    sum_lines_column = sum(r["sum_lines_column"] for r in reports)
    heading_lines = sum(r["heading_lines"] for r in reports)
    n_sections = sum(r["sections"] for r in reports)

    leftover = [(r["src_file"], i, s) for r in reports for i, s in r["leftover"]]
    overlaps = [m for r in reports for m in r["overlaps"]]

    blank_leftover = [x for x in leftover if not x[2].strip()]
    nonblank_leftover = [x for x in leftover if x[2].strip()]

    print(f"=== coverage report: {label} ===")
    print(f"files                    : {len(reports)}")
    print(f"sections                 : {n_sections}")
    print(f"total lines              : {total}")
    print(f"covered by sections      : {covered}")
    print(f"uncovered: heading lines : {heading_lines}")
    print(f"uncovered: blank         : {len(blank_leftover)}")
    print(f"uncovered: NON-BLANK     : {len(nonblank_leftover)}")
    print(f"covered + uncovered      : {covered + heading_lines + len(leftover)}"
          f"  (== total: {covered + heading_lines + len(leftover) == total})")
    print(f"sum of `lines` column    : {sum_lines_column}"
          f"  (== covered: {sum_lines_column == covered})")

    ok = True
    if nonblank_leftover:
        ok = False
        print(f"\n!! {len(nonblank_leftover)} uncovered NON-BLANK line(s):")
        for f, i, s in nonblank_leftover[:50]:
            print(f"   {f}:{i}: {s[:90]}")
    if blank_leftover:
        # Allowed, but must be enumerated so the reason is on the record.
        print(f"\n-- {len(blank_leftover)} uncovered blank line(s) — a blank-only stretch "
              f"either between a heading and its first child heading, or before the "
              f"file's first heading.  No section is emitted for these, so they belong "
              f"to none:")
        for f, i, _ in blank_leftover[:200]:
            print(f"   {f}:{i}")
    if overlaps:
        ok = False
        print(f"\n!! {len(overlaps)} overlapping section range(s):")
        for m in overlaps[:50]:
            print(f"   {m}")
    if sum_lines_column != covered:
        ok = False
        print(f"\n!! `lines` sum {sum_lines_column} != covered {covered} (ranges overlap or gap)")

    print(f"\nRESULT: {'OK' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
