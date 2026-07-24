"""
extract_sections.py
Mechanically extract L3-equivalent sections from RST and Markdown files.

Output columns per section (returned as list of dicts):
  section_id    – assigned by caller
  src_file      – path string passed by caller
  src_line      – 1-indexed line number of the L3 heading
  heading_path  – "PageTitle > H2 > H3" style path
  lines         – number of body lines (excluding the heading line itself)
  code_blocks   – count of code blocks in the section
  tables        – count of tables in the section
  figures       – count of figures/images in the section

RST heading levels:
  Level is determined file-locally by the ORDER in which underline characters
  first appear.  L1 = first seen char, L2 = second, L3 = third.
  Both "overline + text + underline" and "text + underline" patterns are
  recognised.  L4 and deeper are folded into the enclosing L3 section.

Markdown heading levels:
  H3 (###) is the extraction unit.
  H4 and below are folded into the enclosing H3.
  H1 / H2 are used only for the heading_path.
"""

import re
import sys
import csv
import os
from typing import List, Dict, Any, Optional, Tuple

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

HEADING_SEP = " > "

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


def _parse_rst_headings(lines: List[str]) -> List[Tuple[int, int, str, Optional[int]]]:
    """
    Parse RST headings.  Returns list of
    (text_line_index_0based, level, heading_text, overline_line_index_or_None).

    Level 1 = first seen adornment style, 2 = second, 3 = third, etc.

    RST heading forms:
      Overline + text + underline  (same char, same length)  → key: (char, True)
      Text + underline                                        → key: (char, False)

    Same character with overline vs without overline are DIFFERENT levels.
    The 4th tuple element is the overline line index for overline-form headings,
    or None for underline-only headings.
    """
    level_map: Dict[Tuple[str, bool], int] = {}
    result: List[Tuple[int, int, str, Optional[int]]] = []

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
                    result.append((i + 1, level_map[key], text_line, i))
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
                    result.append((i, level_map[key], stripped, None))
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


def extract_rst_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """Extract L3 sections from RST text."""
    lines = text.splitlines(keepends=True)
    headings = _parse_rst_headings(lines)

    # Build heading context: find the heading_path for each L3
    # Keep track of L1, L2 context
    sections: List[Dict[str, Any]] = []
    l1_text = ""
    l2_text = ""

    # Group headings by level
    for idx, (line_idx, level, heading_text, overline_idx) in enumerate(headings):
        if level == 1:
            l1_text = heading_text
            l2_text = ""
        elif level == 2:
            l2_text = heading_text
        elif level == 3:
            # Determine end of this section: next heading of level <= 3.
            # For overline-form headings, the boundary is the overline line (not
            # the text line) so the overline does not bleed into the previous
            # section's body.
            next_boundary = len(lines)
            for jdx in range(idx + 1, len(headings)):
                if headings[jdx][1] <= 3:
                    ov = headings[jdx][3]
                    next_boundary = ov if ov is not None else headings[jdx][0]
                    break

            # Body lines: from line after heading (and its underline) to next_boundary.
            # _parse_rst_headings stores the TEXT line index in both overline and
            # underline-only forms.  The underline is always at text_line + 1.
            body_start = line_idx + 2  # skip heading text line + underline line
            body_lines = lines[body_start:next_boundary]

            # Build heading path
            parts = [p for p in [l1_text, l2_text, heading_text] if p]
            heading_path = HEADING_SEP.join(parts)

            # Count metrics
            code_blocks = _count_rst_code_blocks(body_lines)
            tables = _count_rst_tables(body_lines)
            figures = _count_rst_figures(body_lines)
            line_count = len(body_lines)

            sections.append({
                "src_file": src_file,
                "src_line": line_idx + 1,  # 1-indexed
                "heading_path": heading_path,
                "lines": line_count,
                "code_blocks": code_blocks,
                "tables": tables,
                "figures": figures,
            })

    return sections


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

_MD_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
_MD_CODE_FENCE_RE = re.compile(r'^```')
_MD_TABLE_ROW_RE = re.compile(r'^\|')
_MD_FIGURE_RE = re.compile(r'!\[.*?\]\(.*?\)')


def _parse_md_headings(lines: List[str]) -> List[Tuple[int, int, str]]:
    """Return list of (line_index_0based, level, heading_text) for all ATX headings."""
    result = []
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.rstrip('\n')
        if _MD_CODE_FENCE_RE.match(stripped):
            in_code = not in_code
        if in_code:
            continue
        m = _MD_HEADING_RE.match(stripped)
        if m:
            level = len(m.group(1))
            result.append((i, level, m.group(2).strip()))
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


def extract_md_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """Extract H3 sections from Markdown text."""
    lines = text.splitlines(keepends=True)
    headings = _parse_md_headings(lines)

    sections: List[Dict[str, Any]] = []
    h1_text = ""
    h2_text = ""

    for idx, (line_idx, level, heading_text) in enumerate(headings):
        if level == 1:
            h1_text = heading_text
            h2_text = ""
        elif level == 2:
            h2_text = heading_text
        elif level == 3:
            # End of this section: next heading with level <= 3
            next_boundary = len(lines)
            for jdx in range(idx + 1, len(headings)):
                if headings[jdx][1] <= 3:
                    next_boundary = headings[jdx][0]
                    break

            body_lines = lines[line_idx + 1:next_boundary]

            parts = [p for p in [h1_text, h2_text, heading_text] if p]
            heading_path = HEADING_SEP.join(parts)

            code_blocks = _count_md_code_blocks(body_lines)
            tables = _count_md_tables(body_lines)
            figures = _count_md_figures(body_lines)
            line_count = len(body_lines)

            sections.append({
                "src_file": src_file,
                "src_line": line_idx + 1,  # 1-indexed
                "heading_path": heading_path,
                "lines": line_count,
                "code_blocks": code_blocks,
                "tables": tables,
                "figures": figures,
            })

    return sections


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

def extract_sections(text: str, src_file: str) -> List[Dict[str, Any]]:
    """
    Extract L3-equivalent sections from text.
    Dispatches to RST or Markdown extractor based on src_file extension.
    Returns list of dicts (section_id not yet assigned; caller assigns it).
    """
    if src_file.endswith(".rst"):
        return extract_rst_sections(text, src_file)
    elif src_file.endswith(".md"):
        return extract_md_sections(text, src_file)
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
    """Write sections list (with section_id already set) to CSV."""
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
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

def main(argv: List[str]) -> None:
    if len(argv) < 3:
        print(
            "Usage: python3 extract_sections.py <prefix> <out_csv> <file_spec> [...]",
            file=sys.stderr,
        )
        sys.exit(1)

    prefix = argv[0]
    out_csv = argv[1]
    raw_file_specs = argv[2:]

    # Parse file specs and sort by logical_path for reproducibility
    file_specs: List[Tuple[str, str]] = []
    for spec in raw_file_specs:
        if ":" in spec:
            # Split on first colon only (Windows paths would break, but we're on Linux)
            actual, logical = spec.split(":", 1)
        else:
            actual = spec
            logical = spec
        file_specs.append((actual, logical))

    # Sort by logical path for reproducibility
    file_specs = sorted(file_specs, key=lambda x: x[1])

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

    write_csv(all_sections, out_csv)
    print(f"Wrote {len(all_sections)} sections to {out_csv}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
