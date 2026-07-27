"""
extract_sections.py
Mechanically extract sections from RST and Markdown files with NO body-line loss.

Extraction rules (applied identically to RST and Markdown):

  1. A heading that has child headings and sits at depth < 3 is NOT itself a
     section; its children are extracted instead.
  2. Body text sitting directly under such a heading, before its first child,
     becomes its own section.  Its heading_path is the parent path plus a
     marker "(L{depth}直下)" so it is distinguishable from a real heading.
  3. A heading with no child headings is extracted as a section covering its
     whole body (this is how L2-only and L1-only pages are captured).
  4. A heading at depth 3 is extracted as a section covering its whole subtree
     (L4 and deeper are folded in).
  5. Body text before the first heading of the file becomes a section marked
     "(冒頭)".

  Consequence: every non-blank body line of every file belongs to exactly one
  section.  Only heading lines themselves (text + underline + optional
  overline) and blank-only gaps are outside the sections.  verify_coverage.py
  proves this mechanically.

Output columns per section (returned as list of dicts):
  section_id    – assigned by caller
  src_file      – path string passed by caller
  src_line      – 1-indexed line number where the section starts
                  (the heading line, or the first body line for "直下"/"冒頭")
  heading_path  – "PageTitle > H2 > H3" style path
  lines         – number of body lines, excluding the heading line itself and
                  excluding trailing blank lines
  code_blocks   – count of code blocks in the section
  tables        – count of tables in the section
  figures       – count of figures/images in the section

Each returned dict also carries two private keys used only by
verify_coverage.py; write_csv ignores them:
  _range_start  – 0-indexed first body line of the section
  _range_end    – 0-indexed line after the last body line of the section

RST heading levels:
  Level is determined file-locally by the ORDER in which underline characters
  first appear.  L1 = first seen char, L2 = second, L3 = third.
  Both "overline + text + underline" and "text + underline" patterns are
  recognised.

Markdown heading levels:
  ATX heading depth (#, ##, ###) as written.
"""

import re
import sys
import csv
import os
from typing import List, Dict, Any, Optional, Tuple, NamedTuple

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

HEADING_SEP = " > "

#: Marker used for body text that precedes the first heading of a file.
PREAMBLE_MARKER = "(冒頭)"


def _direct_marker(depth: int) -> str:
    """Marker for body text sitting directly under a depth-`depth` heading."""
    return f"(L{depth}直下)"


class Heading(NamedTuple):
    """A parsed heading, normalised across RST and Markdown."""

    start: int        # 0-indexed first line of the heading block (overline if any)
    text_line: int    # 0-indexed line holding the heading text
    body_start: int   # 0-indexed first line after the heading block
    level: int        # 1-based level as written / as ordered
    text: str         # heading text


def _has_content(body_lines: List[str]) -> bool:
    """True if any line carries non-whitespace."""
    return any(line.strip() for line in body_lines)


# ---------------------------------------------------------------------------
# RST parser
# ---------------------------------------------------------------------------

_RST_ADORNMENT_RE = re.compile(r'^([=\-~^"`.!*+#_])\1{2,}\s*$')
_RST_CODE_RE = re.compile(r'^\.\.\s+code(?:-block)?::', re.IGNORECASE)
_RST_LIST_TABLE_RE = re.compile(r'^\.\.\s+list-table::', re.IGNORECASE)
_RST_FIGURE_RE = re.compile(r'^\.\.\s+(?:figure|image)::', re.IGNORECASE)

# Grid table: line starts with +---... pattern
_RST_GRID_TABLE_RE = re.compile(r'^\+[-=+]+\+\s*$')


def _is_rst_adornment(line: str) -> Optional[str]:
    """Return the adornment character if the line is a valid RST adornment, else None."""
    stripped = line.rstrip('\n').rstrip()
    m = _RST_ADORNMENT_RE.match(stripped)
    if m:
        return m.group(1)
    return None


def _parse_rst_headings(lines: List[str]) -> List[Heading]:
    """
    Parse RST headings into normalised Heading records.

    Level 1 = first seen adornment style, 2 = second, 3 = third, etc.

    RST heading forms:
      Overline + text + underline  (same char, same length)  → key: (char, True)
      Text + underline                                        → key: (char, False)

    Same character with overline vs without overline are DIFFERENT levels.
    """
    level_map: Dict[Tuple[str, bool], int] = {}
    result: List[Heading] = []

    n = len(lines)
    i = 0
    while i < n:
        ch = _is_rst_adornment(lines[i])
        if ch is not None:
            # Could be overline: check if next line is text and line after is same adornment
            if i + 2 < n:
                text_line = lines[i + 1].rstrip('\n').strip()
                ch2 = _is_rst_adornment(lines[i + 2])
                if text_line and ch2 == ch:
                    # overline + text + underline
                    key = (ch, True)
                    if key not in level_map:
                        level_map[key] = len(level_map) + 1
                    result.append(Heading(
                        start=i,
                        text_line=i + 1,
                        body_start=i + 3,
                        level=level_map[key],
                        text=text_line,
                    ))
                    i += 3
                    continue
            # Not overline; skip (pure adornment line handled as underline below)
            i += 1
            continue
        else:
            # Could be "text + underline"
            stripped = lines[i].rstrip('\n').rstrip()
            if stripped and i + 1 < n:
                ch2 = _is_rst_adornment(lines[i + 1])
                if ch2 is not None:
                    # text + underline (no overline)
                    key = (ch2, False)
                    if key not in level_map:
                        level_map[key] = len(level_map) + 1
                    result.append(Heading(
                        start=i,
                        text_line=i,
                        body_start=i + 2,
                        level=level_map[key],
                        text=stripped,
                    ))
                    i += 2
                    continue
            i += 1

    return result


def _count_rst_code_blocks(body_lines: List[str]) -> int:
    count = 0
    for line in body_lines:
        if _RST_CODE_RE.match(line.lstrip()):
            count += 1
    return count


def _is_simple_table_adornment(stripped: str) -> bool:
    """Return True if the line is a simple RST table adornment line (=== === ...).
    Requires at least 2 blocks to avoid false-positive on heading underlines.
    """
    if not stripped or '+' in stripped:
        return False
    parts = stripped.split()
    return len(parts) >= 2 and all(re.match(r'^=+$', p) for p in parts)


def _count_rst_tables(body_lines: List[str]) -> int:
    """Count list-table directives and grid/simple tables."""
    n = len(body_lines)
    count = 0
    i = 0

    # Track state for grid tables (contiguous +---+ lines = one table)
    in_grid = False

    while i < n:
        stripped = body_lines[i].rstrip('\n').rstrip()

        # list-table directive
        if _RST_LIST_TABLE_RE.match(stripped.lstrip()):
            count += 1
            in_grid = False
            i += 1
            continue

        # grid table row: starts with +---+ or +===+, or | ... | content row
        if _RST_GRID_TABLE_RE.match(stripped) or (in_grid and stripped.startswith('|')):
            if not in_grid:
                in_grid = True
                count += 1
            i += 1
            continue

        # simple table top adornment: === === ... (only = and spaces, no +)
        if _is_simple_table_adornment(stripped):
            in_grid = False
            # It's a simple table border; scan for the closing border
            k = i + 1
            while k < n:
                s2 = body_lines[k].rstrip('\n').rstrip()
                if _is_simple_table_adornment(s2):
                    # found the closing border of this table
                    count += 1
                    i = k + 1
                    break
                k += 1
            else:
                i = k
            continue

        in_grid = False
        i += 1

    return count


def _count_rst_figures(body_lines: List[str]) -> int:
    count = 0
    for line in body_lines:
        if _RST_FIGURE_RE.match(line.lstrip()):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

_MD_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
_MD_CODE_FENCE_RE = re.compile(r'^`{3,}')
_MD_TABLE_ROW_RE = re.compile(r'^\|')
_MD_FIGURE_RE = re.compile(r'!\[.*?\]\(.*?\)')


def _parse_md_headings(lines: List[str]) -> List[Heading]:
    """Return normalised Heading records for all ATX headings outside code fences."""
    result: List[Heading] = []
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.rstrip('\n')
        if _MD_CODE_FENCE_RE.match(stripped):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = _MD_HEADING_RE.match(stripped)
        if m:
            level = len(m.group(1))
            result.append(Heading(
                start=i,
                text_line=i,
                body_start=i + 1,
                level=level,
                text=m.group(2).strip(),
            ))
    return result


def _count_md_code_blocks(body_lines: List[str]) -> int:
    count = 0
    in_fence = False
    for line in body_lines:
        stripped = line.rstrip('\n')
        if _MD_CODE_FENCE_RE.match(stripped):
            if not in_fence:
                count += 1
                in_fence = True
            else:
                in_fence = False
    return count


def _count_md_tables(body_lines: List[str]) -> int:
    """Count | delimited tables (each contiguous block = 1 table)."""
    count = 0
    in_table = False
    for line in body_lines:
        stripped = line.rstrip('\n').strip()
        if _MD_TABLE_ROW_RE.match(stripped):
            if not in_table:
                count += 1
                in_table = True
        else:
            in_table = False
    return count


def _count_md_figures(body_lines: List[str]) -> int:
    count = 0
    for line in body_lines:
        count += len(_MD_FIGURE_RE.findall(line))
    return count


# ---------------------------------------------------------------------------
# Generic section builder (shared by RST and Markdown)
# ---------------------------------------------------------------------------

#: Headings at this depth or deeper are emitted as a single section with their
#: whole subtree folded in.
LEAF_DEPTH = 3


def _build_heading_tree(headings: List[Heading]) -> Tuple[List[Optional[int]], Dict[Optional[int], List[int]]]:
    """
    Return (parent, children) where parent[j] is the index of j's parent heading
    (None for a top-level heading) and children maps a parent index (or None)
    to its ordered child indices.

    Parent = nearest preceding heading with a strictly smaller level.
    """
    parent: List[Optional[int]] = [None] * len(headings)
    children: Dict[Optional[int], List[int]] = {None: []}
    stack: List[int] = []

    for j, h in enumerate(headings):
        while stack and headings[stack[-1]].level >= h.level:
            stack.pop()
        p = stack[-1] if stack else None
        parent[j] = p
        children.setdefault(p, []).append(j)
        stack.append(j)

    return parent, children


def _subtree_end(
    headings: List[Heading],
    parent: List[Optional[int]],
    j: int,
    total_lines: int,
) -> int:
    """0-indexed line after the last line belonging to heading j's subtree."""

    def is_descendant(k: int) -> bool:
        p = parent[k]
        while p is not None:
            if p == j:
                return True
            p = parent[p]
        return False

    k = j + 1
    while k < len(headings) and is_descendant(k):
        k += 1
    return headings[k].start if k < len(headings) else total_lines


def _build_sections(
    lines: List[str],
    headings: List[Heading],
    src_file: str,
    count_code, count_tables, count_figures,
) -> List[Dict[str, Any]]:
    """Apply the extraction rules and return section dicts in document order."""
    sections: List[Dict[str, Any]] = []
    total = len(lines)

    def emit(range_start: int, range_end: int, path: List[str], src_line: int) -> None:
        body = lines[range_start:range_end]
        # Trailing blank lines do not count towards volume.
        stripped_body = body
        while stripped_body and not stripped_body[-1].strip():
            stripped_body = stripped_body[:-1]
        sections.append({
            "src_file": src_file,
            "src_line": src_line,
            "heading_path": HEADING_SEP.join(path),
            "lines": len(stripped_body),
            "code_blocks": count_code(body),
            "tables": count_tables(body),
            "figures": count_figures(body),
            "_range_start": range_start,
            "_range_end": range_end,
        })

    if not headings:
        # No headings at all: the whole file is one preamble section.
        if _has_content(lines):
            emit(0, total, [PREAMBLE_MARKER], 1)
        return sections

    parent, children = _build_heading_tree(headings)

    # Body text before the first heading of the file.
    preamble_end = headings[0].start
    if _has_content(lines[0:preamble_end]):
        emit(0, preamble_end, [PREAMBLE_MARKER], 1)

    def walk(j: int, depth: int, path: List[str]) -> None:
        h = headings[j]
        end = _subtree_end(headings, parent, j, total)
        kids = children.get(j, [])

        if depth >= LEAF_DEPTH or not kids:
            # Leaf section: covers the whole subtree body.
            emit(h.body_start, end, path, h.text_line + 1)
            return

        # Body directly under this heading, before its first child.
        first_child_start = headings[kids[0]].start
        direct = lines[h.body_start:first_child_start]
        if _has_content(direct):
            emit(
                h.body_start,
                first_child_start,
                path + [_direct_marker(depth)],
                h.body_start + 1,
            )

        for c in kids:
            walk(c, depth + 1, path + [headings[c].text])

    for top in children.get(None, []):
        walk(top, 1, [headings[top].text])

    return sections


def extract_rst_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """Extract sections from RST text."""
    lines = text.splitlines(keepends=True)
    headings = _parse_rst_headings(lines)
    return _build_sections(
        lines, headings, src_file,
        _count_rst_code_blocks, _count_rst_tables, _count_rst_figures,
    )


def extract_md_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """Extract sections from Markdown text."""
    lines = text.splitlines(keepends=True)
    headings = _parse_md_headings(lines)
    return _build_sections(
        lines, headings, src_file,
        _count_md_code_blocks, _count_md_tables, _count_md_figures,
    )


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

def extract_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """
    Extract sections from text.
    Dispatches to RST or Markdown extractor based on src_file extension.
    Returns list of dicts (section_id not yet assigned; caller assigns it).
    """
    if src_file.endswith(".rst"):
        return extract_rst_sections(text, src_file)
    elif src_file.endswith(".md"):
        return extract_md_sections(text, src_file)
    else:
        raise ValueError(f"Unsupported file type: {src_file}")


def parse_headings(text: str, src_file: str) -> List[Heading]:
    """Parse headings only — used by verify_coverage.py for line accounting."""
    lines = text.splitlines(keepends=True)
    if src_file.endswith(".rst"):
        return _parse_rst_headings(lines)
    elif src_file.endswith(".md"):
        return _parse_md_headings(lines)
    else:
        raise ValueError(f"Unsupported file type: {src_file}")


# ---------------------------------------------------------------------------
# CSV writer helper (used by build_mapping.sh via stdin/stdout)
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "section_id", "src_file", "src_line", "heading_path",
    "lines", "code_blocks", "tables", "figures",
]


def write_csv(sections_with_ids: List[Dict[str, Any]], out_path: str) -> None:
    """Write sections list (with section_id already set) to CSV.

    Private "_"-prefixed keys carried for coverage verification are dropped.
    """
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=CSV_COLUMNS, lineterminator="\n", extrasaction="ignore",
        )
        writer.writeheader()
        for row in sections_with_ids:
            writer.writerow(row)


# ---------------------------------------------------------------------------
# CLI: python3 extract_sections.py <prefix> <out_csv> <file_spec> [...]
#
# Each <file_spec> is either:
#   <actual_path>
#   <actual_path>:<logical_path>
#
# When <logical_path> is given, it is used as src_file in the CSV (for
# reproducibility when the actual file lives in a temp directory).
# ---------------------------------------------------------------------------

def parse_file_specs(raw_file_specs: List[str]) -> List[Tuple[str, str]]:
    """Parse "actual[:logical]" specs and sort by logical path for reproducibility."""
    file_specs: List[Tuple[str, str]] = []
    for spec in raw_file_specs:
        if ":" in spec:
            # Split on first colon only (Windows paths would break, but we're on Linux)
            actual, logical = spec.split(":", 1)
        else:
            actual = spec
            logical = spec
        file_specs.append((actual, logical))
    return sorted(file_specs, key=lambda x: x[1])


def main(argv: List[str]) -> None:
    if len(argv) < 3:
        print(
            "Usage: python3 extract_sections.py <prefix> <out_csv> <file_spec> [...]",
            file=sys.stderr,
        )
        sys.exit(1)

    prefix = argv[0]
    out_csv = argv[1]
    file_specs = parse_file_specs(argv[2:])

    all_sections: List[Dict[str, Any]] = []
    section_counter = 1
    for actual_path, logical_path in file_specs:
        if not os.path.isfile(actual_path):
            print(f"ERROR: file not found: {actual_path}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(actual_path, encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError as e:
            print(f"ERROR: {actual_path}: encoding error: {e}", file=sys.stderr)
            sys.exit(1)
        # Use logical_path (with correct extension) for dispatch
        try:
            sections = extract_sections(text, logical_path)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        for sec in sections:
            sec["section_id"] = f"{prefix}-{section_counter:04d}"
            section_counter += 1
            all_sections.append(sec)

    try:
        write_csv(all_sections, out_csv)
    except OSError as e:
        print(f"ERROR: {out_csv}: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Wrote {len(all_sections)} sections to {out_csv}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
