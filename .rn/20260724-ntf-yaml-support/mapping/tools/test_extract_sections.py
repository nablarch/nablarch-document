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
        # L3見出し1 body: blank + "本文行1\n" + "本文行2\n" (trailing blank stripped) = 3 lines
        self.assertEqual(sections[0]["lines"], 3)

    def test_no_l3_extracts_the_l2_itself(self):
        """L3を持たないL2は、そのL2自体がセクションとして抽出されること。"""
        # Given: L1 と L2 のみで L3 を持たない RST
        # When: セクションを抽出する
        sections = run_extract(RST_NO_L3, "no_l3.rst", "current")
        # Then: L2 が1セクションとして抽出される
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["heading_path"], "Title > Only L2")
        # body: blank + "No L3 here.\n" = 2 lines
        self.assertEqual(sections[0]["lines"], 2)

    def test_l4_included_in_l3(self):
        sections = run_extract(RST_L4_UNDER_L3, "l4.rst", "current")
        self.assertEqual(len(sections), 1, "Only one L3 section expected")
        # L4 heading text should appear in section body (not as separate section)
        # lines should include the L4 heading and its body
        # body: blank + "L3 body\n" + blank + "L4 heading\n" + "----------\n" + blank + "L4 body...\n" = 7 lines
        self.assertEqual(sections[0]["lines"], 7)

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
        # body includes "body tilde\n" + blank + "H3 caret\n" + "^^^^^^^^\n" + blank + "body caret\n" + trailing = 7 lines
        self.assertEqual(sections[0]["lines"], 7)

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
        # Given: RST_WITH_OVERLINE - Title/L2a/L3a/L3b すべて同じ char (=) + overline → level 1 のみ
        # When: セクションを抽出する
        sections = run_extract(RST_WITH_OVERLINE, "overline.rst", "current")
        # Then: 4見出しがすべて同レベル＝子を持たないため、各々がセクションになる
        self.assertEqual(len(sections), 4)
        self.assertEqual(
            [s["heading_path"] for s in sections],
            ["Title", "L2a", "L3a", "L3b"],
        )
        # L3a の body は "body" 1行のみ。次見出しの overline は含まれない
        self.assertEqual(sections[2]["lines"], 2)

    def test_overline_with_underline_only_different_levels(self):
        """Same char with overline vs without overline = different levels."""
        # Given: = + overline → L1, = underline-only → L2, - underline-only → L3
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
        # When: セクションを抽出する
        sections = run_extract(rst, "levels.rst", "current")
        # Then: L3 sub のみが L3 セクションとして抽出される
        self.assertEqual(len(sections), 1)
        self.assertIn("L3 sub", sections[0]["heading_path"])

    def test_overline_section_boundary_accurate(self):
        """Overline of L3b must not bleed into L3a's body lines."""
        # Given: = underline-only → L1, - underline-only → L2, = overline → L3
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
        # When: セクションを抽出する
        sections = extract_rst_sections(rst, "ob.rst")
        # Then: セクション数と各セクションの lines が期待値と一致する
        self.assertEqual(len(sections), 2)
        # L3a body: blank + line1 + line2 (trailing blank stripped) = 3 lines
        self.assertEqual(sections[0]["lines"], 3)
        self.assertEqual(sections[0]["src_line"], 8)
        # L3b body: blank + body_b (trailing blank stripped) = 2 lines
        self.assertEqual(sections[1]["lines"], 2)
        self.assertEqual(sections[1]["src_line"], 15)


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

    def test_no_h3_extracts_the_h2_itself(self):
        """H3を持たないH2は、そのH2自体がセクションとして抽出されること。"""
        # Given: H1 と H2 のみで H3 を持たない Markdown
        # When: セクションを抽出する
        sections = run_extract(MD_NO_H3, "no_h3.md", "input")
        # Then: H2 が1セクションとして抽出される
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["heading_path"], "Title > H2 only")

    def test_h4_included_in_h3(self):
        sections = run_extract(MD_H4_UNDER_H3, "h4.md", "input")
        self.assertEqual(len(sections), 1)
        # body: blank + "H3 body\n" + blank + "#### H4\n" + blank + "H4 body...\n" = 6 lines
        self.assertEqual(sections[0]["lines"], 6)

    def test_h2_direct_body_becomes_its_own_section(self):
        """H3を持つH2の直下本文は、(L2直下) セクションとして抽出されること。"""
        # Given: H2 直下に本文があり、その後に H3 が続く Markdown
        # When: セクションを抽出する
        sections = run_extract(MD_H2_NOT_STANDALONE, "h2.md", "input")
        # Then: (L2直下) と H3 の2セクションになる
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["heading_path"], "Title > H2 section > (L2直下)")
        # body: blank + "Some text under H2.\n" = 2 lines（末尾空行は除外）
        self.assertEqual(sections[0]["lines"], 2)
        self.assertEqual(sections[1]["heading_path"], "Title > H2 section > H3 section")

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


# ===========================================================================
# ADDITIONAL TESTS (Round 1)
# ===========================================================================

RST_MULTI_SIMPLE_TABLE = """\
========
Title
========

------
L2
------

L3 two tables
=============

=== ===
A   B
=== ===

Some text.

=== === ===
X   Y   Z
=== === ===

"""


class TestRSTMultipleSimpleTables(unittest.TestCase):

    def test_two_simple_tables_counted(self):
        """2個の simple table が含まれるセクションで tables == 2 となること。"""
        # Given: 2つの simple table を含む RST テキスト
        # When: セクションを抽出する
        sections = run_extract(RST_MULTI_SIMPLE_TABLE, "multi_t.rst", "current")
        # Then: tables カウントが 2 になること
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["tables"], 2)


class TestMDCodeFenceExtended(unittest.TestCase):

    def test_four_backtick_fence_ignored_as_heading(self):
        """4個以上のバッククォートfenceの中にある ### はheadingとして抽出されないこと。"""
        # Given: 4個バッククォートfenceの中に ### を含む Markdown
        md = """\
# Title

## H2

### Real H3

Content before fence.

````markdown
### Fake H3 inside 4-backtick fence
````

More content.
"""
        # When: セクションを抽出する
        sections = run_extract(md, "fence4.md", "input")
        # Then: Real H3 のみが抽出され、fenceの中の ### は無視されること
        self.assertEqual(len(sections), 1)
        self.assertIn("Real H3", sections[0]["heading_path"])

    def test_four_backtick_fence_code_counted(self):
        """4個バッククォートfenceはコードブロックとして1件カウントされること。"""
        # Given: 4個バッククォートfenceを含む Markdown
        md = """\
# Title

## H2

### H3

````python
x = 1
````
"""
        # When: セクションを抽出する
        sections = run_extract(md, "fence4cb.md", "input")
        # Then: code_blocks == 1
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["code_blocks"], 1)


# ===========================================================================
# NO-LOSS EXTRACTION TESTS (task-02a)
# ===========================================================================

RST_L1_DIRECT_BODY = """\
Title
=====

L1 direct body.

H2
---

H2 body.
"""

RST_L2_DIRECT_BODY = """\
Title
=====

H2
---

H2 direct body.

H3
~~~

H3 body.
"""

RST_PREAMBLE = """\
.. _some_label:

Title
=====

body
"""

MD_PREAMBLE = """\
Intro sentence before any heading.

# Title

body
"""

MD_NO_HEADING_AT_ALL = """\
just text
more text
"""


class TestDirectBodySections(unittest.TestCase):
    """L2/L1 直下の本文が独立セクションとして抽出されること。"""

    def test_rst_l1_direct_body_marked(self):
        # Given: L1 直下に本文があり、その後に L2 が続く RST
        # When: セクションを抽出する
        sections = run_extract(RST_L1_DIRECT_BODY, "l1d.rst", "current")
        # Then: (L1直下) と L2 の2セクションになる
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["heading_path"], "Title > (L1直下)")
        self.assertEqual(sections[0]["lines"], 2)
        self.assertEqual(sections[1]["heading_path"], "Title > H2")

    def test_rst_l1_direct_body_src_line_points_at_body(self):
        """(L1直下) の src_line は見出し行ではなく本文開始行を指すこと。"""
        # Given/When
        sections = run_extract(RST_L1_DIRECT_BODY, "l1d.rst", "current")
        # Then: L1 見出しは1行目、その本文は3行目から始まる
        self.assertEqual(sections[0]["src_line"], 3)

    def test_rst_l2_direct_body_marked(self):
        # Given: L2 直下に本文があり、その後に L3 が続く RST
        # When: セクションを抽出する
        sections = run_extract(RST_L2_DIRECT_BODY, "l2d.rst", "current")
        # Then: (L2直下) と L3 の2セクションになる
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["heading_path"], "Title > H2 > (L2直下)")
        self.assertEqual(sections[1]["heading_path"], "Title > H2 > H3")

    def test_blank_only_direct_body_not_emitted(self):
        """直下が空行のみの場合、(L直下) セクションは作られないこと。"""
        # Given: RST_SIMPLE は L1/L2 直下が空行のみ
        # When: セクションを抽出する
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        # Then: L3 の2セクションのみ。直下マーカーは現れない
        self.assertEqual(len(sections), 2)
        self.assertFalse(any("直下" in s["heading_path"] for s in sections))


class TestPreambleSections(unittest.TestCase):
    """最初の見出しより前の本文が (冒頭) セクションになること。"""

    def test_rst_preamble_extracted(self):
        # Given: 先頭に参照ラベルがあり、その後にタイトルが続く RST
        # When: セクションを抽出する
        sections = run_extract(RST_PREAMBLE, "pre.rst", "current")
        # Then: (冒頭) と Title の2セクションになる
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["heading_path"], "(冒頭)")
        self.assertEqual(sections[0]["src_line"], 1)
        self.assertEqual(sections[0]["lines"], 1)

    def test_md_preamble_extracted(self):
        # Given: H1 より前に本文がある Markdown
        # When: セクションを抽出する
        sections = run_extract(MD_PREAMBLE, "pre.md", "input")
        # Then: (冒頭) と Title の2セクションになる
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["heading_path"], "(冒頭)")

    def test_file_without_any_heading_becomes_one_section(self):
        # Given: 見出しが1つもない Markdown
        # When: セクションを抽出する
        sections = run_extract(MD_NO_HEADING_AT_ALL, "flat.md", "input")
        # Then: ファイル全体が (冒頭) 1セクションになる
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]["heading_path"], "(冒頭)")
        self.assertEqual(sections[0]["lines"], 2)


class TestNoBodyLineLost(unittest.TestCase):
    """全サンプルについて、本文行の取りこぼしが0であることを機械的に確認する。"""

    SAMPLES = [
        ("RST_SIMPLE", RST_SIMPLE, "a.rst"),
        ("RST_WITH_OVERLINE", RST_WITH_OVERLINE, "b.rst"),
        ("RST_L4_UNDER_L3", RST_L4_UNDER_L3, "c.rst"),
        ("RST_CODE_TABLE_FIGURE", RST_CODE_TABLE_FIGURE, "d.rst"),
        ("RST_NO_L3", RST_NO_L3, "e.rst"),
        ("RST_GRID_TABLE", RST_GRID_TABLE, "f.rst"),
        ("RST_SIMPLE_TABLE", RST_SIMPLE_TABLE, "g.rst"),
        ("RST_MULTI_CHAR_LEVELS", RST_MULTI_CHAR_LEVELS, "h.rst"),
        ("RST_EMPTY_SECTION", RST_EMPTY_SECTION, "i.rst"),
        ("RST_MULTI_SIMPLE_TABLE", RST_MULTI_SIMPLE_TABLE, "j.rst"),
        ("RST_L1_DIRECT_BODY", RST_L1_DIRECT_BODY, "k.rst"),
        ("RST_L2_DIRECT_BODY", RST_L2_DIRECT_BODY, "l.rst"),
        ("RST_PREAMBLE", RST_PREAMBLE, "m.rst"),
        ("MD_SIMPLE", MD_SIMPLE, "a.md"),
        ("MD_H4_UNDER_H3", MD_H4_UNDER_H3, "b.md"),
        ("MD_CODE_TABLE_FIGURE", MD_CODE_TABLE_FIGURE, "c.md"),
        ("MD_NO_H3", MD_NO_H3, "d.md"),
        ("MD_H2_NOT_STANDALONE", MD_H2_NOT_STANDALONE, "e.md"),
        ("MD_CODE_FENCE_HEADING", MD_CODE_FENCE_HEADING, "f.md"),
        ("MD_EMPTY_H3", MD_EMPTY_H3, "g.md"),
        ("MD_PREAMBLE", MD_PREAMBLE, "h.md"),
        ("MD_NO_HEADING_AT_ALL", MD_NO_HEADING_AT_ALL, "i.md"),
    ]

    def test_every_sample_has_zero_unexplained_lines(self):
        """どのサンプルでも、セクションにも見出しにも属さない非空行が0であること。"""
        from verify_coverage import verify_file
        for name, text, path in self.SAMPLES:
            with self.subTest(sample=name):
                # Given: サンプルテキスト
                # When: 行の帰属を検証する
                r = verify_file(text, path)
                # Then: 未説明行・重複割当がなく、バケットの合計が総行数に一致する
                self.assertEqual(r["unexplained"], [], f"{name}: 本文行の取りこぼし")
                self.assertEqual(r["overlaps"], [], f"{name}: セクション範囲の重複")
                self.assertEqual(
                    r["counted"] + r["trailing_blank"] + r["heading"] + r["gap_blank"],
                    r["total"],
                    f"{name}: バケット合計が総行数に一致しない",
                )

    def test_sum_of_lines_column_equals_counted(self):
        """CSV の lines 列の合計が、実際に数えた本文行数と一致すること。"""
        from verify_coverage import verify_file
        for name, text, path in self.SAMPLES:
            with self.subTest(sample=name):
                r = verify_file(text, path)
                self.assertEqual(r["sum_lines_column"], r["counted"], name)


class TestWriteCSVDropsPrivateKeys(unittest.TestCase):

    def test_private_range_keys_not_written(self):
        """_range_start/_range_end は CSV に出力されないこと。"""
        from extract_sections import extract_sections, write_csv, CSV_COLUMNS
        sections = extract_sections(RST_SIMPLE, "x.rst")
        self.assertIn("_range_start", sections[0])
        for i, s in enumerate(sections, start=1):
            s["section_id"] = f"pfx-{i:04d}"
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
            out = tf.name
        try:
            write_csv(sections, out)
            with open(out, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.assertEqual(reader.fieldnames, CSV_COLUMNS)
        finally:
            os.unlink(out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
