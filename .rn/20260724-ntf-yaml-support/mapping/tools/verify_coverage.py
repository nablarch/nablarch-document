"""
verify_coverage.py
Prove mechanically that extract_sections.py loses no body line.

For every input file each line is classified into exactly one bucket:

  counted        – a body line inside a section, included in the CSV `lines` column
  trailing_blank – a blank line at the tail of a section, excluded from `lines`
  heading        – the heading line itself (RST: overline/text/underline, MD: "### x")
  gap_blank      – a blank-only stretch that belongs to no section
  UNEXPLAINED    – anything else.  Must be 0; a non-zero value means body text
                   was dropped by the extractor.

The identity that must hold for every corpus:

  total_lines == counted + trailing_blank + heading + gap_blank

Usage (same file-spec syntax as extract_sections.py):
  python3 verify_coverage.py <label> <file_spec> [...]

Exit code is 1 when any line is UNEXPLAINED, when section ranges overlap, or
when the identity does not hold.
"""

import os
import sys
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract_sections import (  # noqa: E402
    extract_sections,
    parse_headings,
    parse_file_specs,
)


class FileReport(Dict[str, Any]):
    pass


def verify_file(text: str, logical_path: str) -> Dict[str, Any]:
    """Classify every line of one file.  Returns a per-file report."""
    lines = text.splitlines(keepends=True)
    total = len(lines)

    sections = extract_sections(text, logical_path)
    headings = parse_headings(text, logical_path)

    # bucket[i] holds the classification of line i
    bucket: List[str] = ["gap"] * total

    # 1. Section ranges win.  A heading nested inside a leaf section (L4 and
    #    deeper) is part of that section's body and must stay counted.
    overlaps: List[str] = []
    counted = 0
    trailing_blank = 0

    for sec in sections:
        start = sec["_range_start"]
        end = sec["_range_end"]
        body = lines[start:end]
        # Recompute the trailing-blank boundary the same way the extractor does.
        last = len(body)
        while last > 0 and not body[last - 1].strip():
            last -= 1
        counted_end = start + last

        for i in range(start, end):
            if bucket[i] != "gap":
                overlaps.append(
                    f"{logical_path}:{i + 1} claimed twice "
                    f"(second claim: '{sec['heading_path']}')"
                )
                continue
            if i < counted_end:
                bucket[i] = "counted"
                counted += 1
            else:
                bucket[i] = "trailing_blank"
                trailing_blank += 1

    # 2. Whatever is left must be a structural heading line or a blank gap.
    structural_heading_lines = set()
    for h in headings:
        for i in range(h.start, min(h.body_start, total)):
            structural_heading_lines.add(i)

    heading_count = 0
    gap_blank = 0
    unexplained: List[str] = []
    for i, b in enumerate(bucket):
        if b != "gap":
            continue
        if i in structural_heading_lines:
            bucket[i] = "heading"
            heading_count += 1
        elif lines[i].strip():
            unexplained.append(f"{logical_path}:{i + 1}: {lines[i].rstrip()[:80]}")
        else:
            gap_blank += 1

    sum_lines_column = sum(s["lines"] for s in sections)

    return {
        "src_file": logical_path,
        "total": total,
        "counted": counted,
        "trailing_blank": trailing_blank,
        "heading": heading_count,
        "gap_blank": gap_blank,
        "sections": len(sections),
        "sum_lines_column": sum_lines_column,
        "unexplained": unexplained,
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
    counted = sum(r["counted"] for r in reports)
    trailing_blank = sum(r["trailing_blank"] for r in reports)
    heading = sum(r["heading"] for r in reports)
    gap_blank = sum(r["gap_blank"] for r in reports)
    n_sections = sum(r["sections"] for r in reports)
    sum_lines_column = sum(r["sum_lines_column"] for r in reports)

    unexplained = [m for r in reports for m in r["unexplained"]]
    overlaps = [m for r in reports for m in r["overlaps"]]

    print(f"=== coverage report: {label} ===")
    print(f"files                : {len(reports)}")
    print(f"sections             : {n_sections}")
    print(f"total lines          : {total}")
    print(f"  counted (CSV lines): {counted}")
    print(f"  trailing blank     : {trailing_blank}")
    print(f"  heading lines      : {heading}")
    print(f"  blank-only gaps    : {gap_blank}")
    print(f"  UNEXPLAINED        : {len(unexplained)}")
    identity = counted + trailing_blank + heading + gap_blank
    print(f"sum of buckets       : {identity}  (== total: {identity == total})")
    print(f"sum of CSV `lines`   : {sum_lines_column}  (== counted: {sum_lines_column == counted})")

    ok = True
    if unexplained:
        ok = False
        print(f"\n!! {len(unexplained)} UNEXPLAINED non-blank line(s):")
        for m in unexplained[:50]:
            print(f"   {m}")
    if overlaps:
        ok = False
        print(f"\n!! {len(overlaps)} overlapping section range(s):")
        for m in overlaps[:50]:
            print(f"   {m}")
    if identity != total:
        ok = False
        print(f"\n!! bucket identity broken: {identity} != {total}")
    if sum_lines_column != counted:
        ok = False
        print(f"\n!! CSV `lines` sum {sum_lines_column} != counted {counted}")

    print(f"\nRESULT: {'OK' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
