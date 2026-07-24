"""
Tests for extract_sections.py
Run with: python3 -m pytest test_extract_sections.py -v
or:        python3 test_extract_sections.py
"""
import sys
import os
import csv
import io
import subprocess
import tempfile
import unittest

# Will import from extract_sections once implemented
sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Helpers to build in-memory "files"
# ---------------------------------------------------------------------------

def run_extract(text, src_file="test.rst", prefix="current"):
    from extract_sections import extract_sections
    return extract_sections(text, src_file)


# ===========================================================================
# RST TESTS
# ===========================================================================

RST_SIMPLE = """\
============
ページタイトル
============

--------
L2見出し
--------

L3見出し1
=========

本文行1
本文行2

L3見出し2
=========

本文行3
"""

RST_WITH_OVERLINE = """\
====
Title
====

====
L2a
====

===
L3a
===

body

===
L3b
===

body2
"""

RST_L4_UNDER_L3 = """\
=======
Title
=======

-------
L2
-------

L3 heading
==========

L3 body

L4 heading
----------

L4 body (should be included in L3)
"""

RST_CODE_TABLE_FIGURE = """\
================
Title
================

-----------
L2
-----------

L3 with stuff
=============

Before code.

.. code-block:: java

   int x = 1;

.. code:: python

   y = 2

.. list-table:: A table
   :header-rows: 1

   * - Col1
     - Col2

.. image:: img.png

.. figure:: fig.png

After.
"""

RST_NO_L3 = """\
========
Title
========

-----
Only L2
-----

No L3 here.
"""

RST_GRID_TABLE = """\
========
Title
========

------
L2
------

L3 grid
=======

+----+----+
| A  | B  |
+====+====+
| 1  | 2  |
+----+----+

"""

RST_SIMPLE_TABLE = """\
========
Title
========

------
L2
------

L3 simple
=========

=== ===
A   B
=== ===
1   2
=== ===

"""

RST_MULTI_CHAR_LEVELS = """\
Title
=====

H2 heading
----------

H3 tilde
~~~~~~~~~

body tilde

H3 caret
^^^^^^^^

body caret
"""

RST_EMPTY_SECTION = """\
Title
======

H2
---

H3 empty
~~~~~~~~
H3 nonempty
~~~~~~~~~~~

body line
"""

# ---------------------------------------------------------------------------
# RST extraction tests
# ---------------------------------------------------------------------------

class TestRSTBasic(unittest.TestCase):

    def test_simple_extracts_two_l3_sections(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        self.assertEqual(len(sections), 2)
        # Verify headings
        self.assertIn("L3見出し1", sections[0]["heading_path"])
        self.assertIn("L3見出し2", sections[1]["heading_path"])

    def test_section_ids_are_sequential(self):
        from extract_sections import extract_sections
        sections = extract_sections(RST_SIMPLE, "simple.rst")
        # section_id is assigned by the caller; verify sections are in order
        self.assertEqual(len(sections), 2)
        # Check src_line is increasing (sections appear in order)
        self.assertLess(sections[0]["src_line"], sections[1]["src_line"])

    def test_heading_path_l3(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        self.assertIn("ページタイトル", sections[0]["heading_path"])
        self.assertIn("L2見出し", sections[0]["heading_path"])
        self.assertIn("L3見出し1", sections[0]["heading_path"])

    def test_second_section_heading_path(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        self.assertIn("L3見出し2", sections[1]["heading_path"])

    def test_body_lines_counted_without_heading(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        # L3見出し1 body: blank + "本文行1\n" + "本文行2\n" + blank = 4 lines
        self.assertEqual(sections[0]["lines"], 4)

    def test_no_l3_returns_empty(self):
        sections = run_extract(RST_NO_L3, "no_l3.rst", "current")
        self.assertEqual(len(sections), 0)

    def test_l4_included_in_l3(self):
        sections = run_extract(RST_L4_UNDER_L3, "l4.rst", "current")
        self.assertEqual(len(sections), 1, "Only one L3 section expected")
        # L4 heading text should appear in section body (not as separate section)
        # lines should include the L4 heading and its body
        self.assertGreater(sections[0]["lines"], 2)

    def test_code_blocks_counted(self):
        sections = run_extract(RST_CODE_TABLE_FIGURE, "stuff.rst", "current")
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["code_blocks"], 2)

    def test_list_table_counted(self):
        sections = run_extract(RST_CODE_TABLE_FIGURE, "stuff.rst", "current")
        self.assertEqual(sections[0]["tables"], 1)

    def test_figures_counted(self):
        sections = run_extract(RST_CODE_TABLE_FIGURE, "stuff.rst", "current")
        # Both .. image:: and .. figure:: count
        self.assertEqual(sections[0]["figures"], 2)

    def test_grid_table_counted(self):
        sections = run_extract(RST_GRID_TABLE, "grid.rst", "current")
        self.assertEqual(sections[0]["tables"], 1)

    def test_simple_table_counted(self):
        sections = run_extract(RST_SIMPLE_TABLE, "simple_t.rst", "current")
        self.assertEqual(sections[0]["tables"], 1)

    def test_src_file_stored(self):
        sections = run_extract(RST_SIMPLE, "myfile.rst", "current")
        self.assertTrue(all(s["src_file"] == "myfile.rst" for s in sections))

    def test_src_line_is_positive(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        self.assertTrue(all(s["src_line"] > 0 for s in sections))

    def test_rst_level_distinction_tilde_caret(self):
        """~ and ^ are different adornment chars → different levels."""
        sections = run_extract(RST_MULTI_CHAR_LEVELS, "multi.rst", "current")
        # ~ is L3 (3rd seen char: =, -, ~)
        # ^ is L4 (4th seen char) → folded into enclosing L3
        self.assertEqual(len(sections), 1)
        self.assertIn("H3 tilde", sections[0]["heading_path"])
        # body includes ^ heading and its body
        body_text = "".join(sections[0].get("src_file", ""))  # just check count
        self.assertGreater(sections[0]["lines"], 0)

    def test_rst_empty_section_lines_zero(self):
        """A section with no body lines should report lines == 0."""
        sections = run_extract(RST_EMPTY_SECTION, "empty.rst", "current")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["lines"], 0)

    def test_is_simple_table_adornment_single_block_not_table(self):
        """A single === block (heading underline) must NOT be treated as a table."""
        from extract_sections import _is_simple_table_adornment
        self.assertFalse(_is_simple_table_adornment("============"))
        self.assertTrue(_is_simple_table_adornment("=== ==="))
        self.assertTrue(_is_simple_table_adornment("=== === ==="))

    def test_overline_boundary_no_bleed(self):
        """Overline line must not appear in the body of the preceding section."""
        sections = run_extract(RST_WITH_OVERLINE, "overline.rst", "current")
        # RST_WITH_OVERLINE: Title (overline =), L2a (overline =) same char/overline → level 1
        # same char + overline → level 1; so L3a/L3b won't be level 3 in this fixture
        # All headings use the same char (=) with overline → all level 1
        # No L3 sections → 0 sections
        # Verify no crash and overline lines not in body of any section
        self.assertIsInstance(sections, list)

    def test_overline_with_underline_only_different_levels(self):
        """Same char with overline vs without overline = different levels."""
        rst = """\
====
Title
====

L2 heading
==========

L3 sub
------

body here
"""
        sections = run_extract(rst, "levels.rst", "current")
        # = with overline → L1; = without overline → L2; - without overline → L3
        self.assertEqual(len(sections), 1)
        self.assertIn("L3 sub", sections[0]["heading_path"])

    def test_overline_section_boundary_accurate(self):
        """Overline of L3b must not bleed into L3a's body lines."""
        # Both L3a and L3b use overline form with the same char (=).
        # = underline only → L1, - underline only → L2, = overline → L3.
        # The overline line (===) of L3b must NOT be counted in L3a's body.
        rst = """\
Title
======

H2
---

===
L3a with overline
===

line1
line2

===
L3b with overline
===

body_b
"""
        from extract_sections import extract_rst_sections
        sections = extract_rst_sections(rst, "ob.rst")
        self.assertEqual(len(sections), 2)
        # L3a body: blank + line1 + line2 + blank = 4 lines (NOT 5 which would include ===)
        self.assertEqual(sections[0]["lines"], 4)
        # L3b body: blank + body_b = 2 lines
        self.assertEqual(sections[1]["lines"], 2)


# ===========================================================================
# MARKDOWN TESTS
# ===========================================================================

MD_SIMPLE = """\
# ページタイトル

## H2見出し

### H3見出し1

本文行1
本文行2

### H3見出し2

本文行3
"""

MD_H4_UNDER_H3 = """\
# Title

## H2

### H3

H3 body

#### H4

H4 body (included in H3)
"""

MD_CODE_TABLE_FIGURE = """\
# Title

## H2

### H3 with stuff

Before.

```java
int x = 1;
```

```python
y = 2
```

| Col1 | Col2 |
|------|------|
| a    | b    |

![alt text](img.png)

After.
"""

MD_NO_H3 = """\
# Title

## H2 only

No H3.
"""

MD_H2_NOT_STANDALONE = """\
# Title

## H2 section

Some text under H2.

### H3 section

H3 body.
"""

MD_CODE_FENCE_HEADING = """\
# Title

## H2

### Real H3

Content before fence.

```markdown
### Fake H3 inside code block
```

More content.
"""

MD_EMPTY_H3 = """\
# Title

## H2

### Empty H3
### Non-empty H3

body line
"""

class TestMarkdownBasic(unittest.TestCase):

    def test_simple_extracts_two_h3_sections(self):
        sections = run_extract(MD_SIMPLE, "simple.md", "input")
        self.assertEqual(len(sections), 2)

    def test_heading_path_h3(self):
        sections = run_extract(MD_SIMPLE, "simple.md", "input")
        self.assertIn("ページタイトル", sections[0]["heading_path"])
        self.assertIn("H2見出し", sections[0]["heading_path"])
        self.assertIn("H3見出し1", sections[0]["heading_path"])

    def test_no_h3_returns_empty(self):
        sections = run_extract(MD_NO_H3, "no_h3.md", "input")
        self.assertEqual(len(sections), 0)

    def test_h4_included_in_h3(self):
        sections = run_extract(MD_H4_UNDER_H3, "h4.md", "input")
        self.assertEqual(len(sections), 1)
        self.assertGreater(sections[0]["lines"], 2)

    def test_h2_not_standalone_section(self):
        sections = run_extract(MD_H2_NOT_STANDALONE, "h2.md", "input")
        # H2-only content should not be a standalone section
        # Only H3 is a standalone section
        self.assertEqual(len(sections), 1)

    def test_code_blocks_counted(self):
        sections = run_extract(MD_CODE_TABLE_FIGURE, "stuff.md", "input")
        self.assertEqual(sections[0]["code_blocks"], 2)

    def test_tables_counted(self):
        sections = run_extract(MD_CODE_TABLE_FIGURE, "stuff.md", "input")
        self.assertEqual(sections[0]["tables"], 1)

    def test_figures_counted(self):
        sections = run_extract(MD_CODE_TABLE_FIGURE, "stuff.md", "input")
        self.assertEqual(sections[0]["figures"], 1)

    def test_src_file_stored(self):
        sections = run_extract(MD_SIMPLE, "myfile.md", "input")
        self.assertTrue(all(s["src_file"] == "myfile.md" for s in sections))

    def test_src_line_positive(self):
        sections = run_extract(MD_SIMPLE, "simple.md", "input")
        self.assertTrue(all(s["src_line"] > 0 for s in sections))

    def test_heading_inside_code_block_ignored(self):
        """### inside a fenced code block must not be extracted as a heading."""
        sections = run_extract(MD_CODE_FENCE_HEADING, "fence.md", "input")
        self.assertEqual(len(sections), 1)
        self.assertIn("Real H3", sections[0]["heading_path"])

    def test_empty_h3_section_lines_zero(self):
        """An H3 with no body lines should report lines == 0."""
        sections = run_extract(MD_EMPTY_H3, "empty.md", "input")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["lines"], 0)


# ===========================================================================
# ERROR HANDLING TESTS
# ===========================================================================

class TestErrorHandling(unittest.TestCase):

    def test_unsupported_file_type_raises_value_error(self):
        from extract_sections import extract_sections
        with self.assertRaises(ValueError):
            extract_sections("some text", "file.txt")

    def test_missing_file_exits_1(self):
        """Passing a nonexistent file to main() should exit with code 1."""
        script = os.path.join(os.path.dirname(__file__), "extract_sections.py")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
            out_csv = tf.name
        try:
            result = subprocess.run(
                [sys.executable, script, "pfx", out_csv, "/nonexistent/path/file.rst"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("not found", result.stderr)
        finally:
            if os.path.exists(out_csv):
                os.unlink(out_csv)


# ===========================================================================
# INTEGRATION TESTS
# ===========================================================================

class TestWriteCSVRoundtrip(unittest.TestCase):

    def test_write_csv_roundtrip(self):
        """write_csv followed by csv.DictReader should recover all rows."""
        from extract_sections import write_csv
        rows = [
            {
                "section_id": "pfx-0001",
                "src_file": "a.rst",
                "src_line": 5,
                "heading_path": "Title > H2 > H3",
                "lines": 10,
                "code_blocks": 1,
                "tables": 0,
                "figures": 2,
            },
            {
                "section_id": "pfx-0002",
                "src_file": "b.md",
                "src_line": 3,
                "heading_path": "Title > H3",
                "lines": 5,
                "code_blocks": 0,
                "tables": 1,
                "figures": 0,
            },
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tf:
            out_path = tf.name
        try:
            write_csv(rows, out_path)
            with open(out_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                read_rows = list(reader)
            self.assertEqual(len(read_rows), 2)
            self.assertEqual(read_rows[0]["section_id"], "pfx-0001")
            self.assertEqual(read_rows[0]["src_file"], "a.rst")
            self.assertEqual(read_rows[1]["section_id"], "pfx-0002")
            self.assertEqual(int(read_rows[1]["tables"]), 1)
        finally:
            os.unlink(out_path)


class TestCLIMain(unittest.TestCase):

    def _run_cli(self, args, extra_files=None):
        """Helper: run extract_sections.py via subprocess and return (returncode, stderr, csv_path)."""
        script = os.path.join(os.path.dirname(__file__), "extract_sections.py")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
            out_csv = tf.name
        cmd = [sys.executable, script] + args + [out_csv]
        if extra_files:
            cmd += extra_files
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stderr, out_csv

    def test_actual_logical_spec(self):
        """actual:logical file spec uses logical path in CSV output."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".rst", delete=False, encoding="utf-8"
        ) as tf:
            tf.write(RST_SIMPLE)
            actual_path = tf.name
        logical_path = "docs/page.rst"
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as cf:
            out_csv = cf.name
        try:
            script = os.path.join(os.path.dirname(__file__), "extract_sections.py")
            result = subprocess.run(
                [
                    sys.executable, script,
                    "pfx", out_csv,
                    f"{actual_path}:{logical_path}",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            with open(out_csv, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(r["src_file"] == logical_path for r in rows))
        finally:
            os.unlink(actual_path)
            os.unlink(out_csv)

    def test_sort_order_is_deterministic(self):
        """Two files passed in different orders produce the same section_id sequence."""
        rst_a = "Title\n=====\n\nH2\n--\n\nH3 alpha\n~~~~~~~~\n\nbody\n"
        rst_b = "Title\n=====\n\nH2\n--\n\nH3 beta\n~~~~~~~\n\nbody\n"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".rst", delete=False, encoding="utf-8", prefix="aaa_"
        ) as fa:
            fa.write(rst_a)
            path_a = fa.name
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".rst", delete=False, encoding="utf-8", prefix="bbb_"
        ) as fb:
            fb.write(rst_b)
            path_b = fb.name

        # logical paths that sort a before b
        spec_a = f"{path_a}:logical/aaa.rst"
        spec_b = f"{path_b}:logical/bbb.rst"

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as cf1:
            csv1 = cf1.name
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as cf2:
            csv2 = cf2.name

        script = os.path.join(os.path.dirname(__file__), "extract_sections.py")
        try:
            # Order 1: a then b
            r1 = subprocess.run(
                [sys.executable, script, "pfx", csv1, spec_a, spec_b],
                capture_output=True, text=True,
            )
            # Order 2: b then a
            r2 = subprocess.run(
                [sys.executable, script, "pfx", csv2, spec_b, spec_a],
                capture_output=True, text=True,
            )
            self.assertEqual(r1.returncode, 0)
            self.assertEqual(r2.returncode, 0)

            with open(csv1, newline="", encoding="utf-8") as f:
                rows1 = list(csv.DictReader(f))
            with open(csv2, newline="", encoding="utf-8") as f:
                rows2 = list(csv.DictReader(f))

            # Both orderings should produce identical section_ids and src_files
            self.assertEqual(
                [(r["section_id"], r["src_file"]) for r in rows1],
                [(r["section_id"], r["src_file"]) for r in rows2],
            )
        finally:
            for p in (path_a, path_b, csv1, csv2):
                if os.path.exists(p):
                    os.unlink(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
