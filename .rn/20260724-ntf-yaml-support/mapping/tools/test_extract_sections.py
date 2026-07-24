"""
Tests for extract_sections.py
Run with: python3 -m pytest test_extract_sections.py -v
or:        python3 test_extract_sections.py
"""
import sys
import os
import io
import unittest

# Will import from extract_sections once implemented
sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Helpers to build in-memory "files"
# ---------------------------------------------------------------------------

def run_extract(text, src_file="test.rst", prefix="current"):
    from extract_sections import extract_sections
    return extract_sections(text, src_file, prefix)


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

# ---------------------------------------------------------------------------
# RST extraction tests
# ---------------------------------------------------------------------------

class TestRSTBasic(unittest.TestCase):

    def test_simple_extracts_two_l3_sections(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        self.assertEqual(len(sections), 2)

    def test_section_ids_are_sequential(self):
        sections = run_extract(RST_SIMPLE, "simple.rst", "current")
        # IDs assigned by caller; extract_sections returns raw dicts
        # section_id is set by the caller (build_mapping); extract returns list
        # so just check two items
        self.assertEqual(len(sections), 2)

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
        # L3見出し1 body: "本文行1\n本文行2\n\n" -> 2 non-empty + 1 blank = 3
        # but blank line between sections should not cross into next section
        self.assertGreater(sections[0]["lines"], 0)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
