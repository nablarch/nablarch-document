"""
Tests for extract_terms.py
Run with: python3 -m pytest test_extract_terms.py -v
or:        python3 test_extract_terms.py
"""
import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import extract_terms as et  # noqa: E402


def write_file(case, text, suffix=".md"):
    f = tempfile.NamedTemporaryFile(
        "w", suffix=suffix, delete=False, encoding="utf-8", newline="\n"
    )
    f.write(text)
    f.close()
    case.addCleanup(os.unlink, f.name)
    return f.name


# ===========================================================================
# heading_path の分解
# ===========================================================================


class TestSplitHeadingPath(unittest.TestCase):

    def test_splits_on_arrow_separator(self):
        # Given: '>' 区切りの見出しパス
        # When: 分解する
        got = et.split_heading_path("親見出し > 子見出し > 孫見出し")
        # Then: 3セグメントに分かれる
        self.assertEqual(got, ["親見出し", "子見出し", "孫見出し"])

    def test_skips_preamble_marker(self):
        # Given: 冒頭マーカーを含むパス
        got = et.split_heading_path("ページ題 > (冒頭)")
        # Then: マーカーは落ちる
        self.assertEqual(got, ["ページ題"])

    def test_skips_direct_body_markers_at_any_level(self):
        # Given: L1直下・L2直下マーカー（extract_sections.py が付ける合成見出し）
        got1 = et.split_heading_path("親 > (L1直下)")
        got2 = et.split_heading_path("親 > 子 > (L2直下)")
        got3 = et.split_heading_path("親 > 子 > (L10直下)")
        # Then: レベルによらずマーカーだけが落ちる
        self.assertEqual(got1, ["親"])
        self.assertEqual(got2, ["親", "子"])
        self.assertEqual(got3, ["親", "子"])

    def test_real_example_from_sections_current_csv(self):
        # Given: mapping/sections-current.csv に実在する heading_path
        path = (
            "Bean Validationに対応したForm/Entityのクラス単体テスト > (L1直下)"
        )
        # When/Then: ページ題だけが残る
        self.assertEqual(et.split_heading_path(path), [
            "Bean Validationに対応したForm/Entityのクラス単体テスト"
        ])

    def test_does_not_treat_ordinary_parenthesised_text_as_marker(self):
        # Given: マーカーの形をしていない、丸括弧を含む普通の見出し
        got = et.split_heading_path("見出し(補足) > 子見出し")
        # Then: マーカーとして誤って落とさない
        self.assertEqual(got, ["見出し(補足)", "子見出し"])

    def test_strips_inline_code_backticks_from_segments(self):
        # Given: RSTのインラインリテラル(``...``)を含む見出し
        # （実例: current-heading の "``RequestResponseProcessor`` の実装..."）
        got = et.split_heading_path("``RequestResponseProcessor`` の実装クラスを作成する")
        # Then: バッククォートは書式なので除かれる。以後これを2重に
        # コードスパンで囲んでも崩れない
        self.assertEqual(got, ["RequestResponseProcessor の実装クラスを作成する"])
        self.assertNotIn("`", got[0])


# ===========================================================================
# current-heading（sections-current.csv）
# ===========================================================================

SECTIONS_CSV_HEADER = (
    "section_id,src_file,src_line,body_start_line,body_end_line,"
    "heading_path,lines,code_blocks,tables,figures\n"
)


# 「ページ題」(L1) > 「節A」(L2、子見出し「項目1」を持つ) > 「項目1」(L3)
# 「ページ題」(L1) > 「節B」(L2、子見出しなし)
# 行番号（1-indexed）: ページ題=1, 節A=4, 項目1=9, 節B=14
RST_DOC = (
    "ページ題\n"
    "========\n"
    "\n"
    "節A\n"
    "----\n"
    "\n"
    "本文A\n"
    "\n"
    "項目1\n"
    "~~~~~\n"
    "\n"
    "本文1\n"
    "\n"
    "節B\n"
    "----\n"
    "\n"
    "本文B\n"
)


class TestExtractCurrentHeadings(unittest.TestCase):

    def test_counts_each_segment_once_per_row_and_records_the_headings_own_line(self):
        # Given: 同じ見出しセグメントが複数行にまたがる heading_path と、
        # それに対応する見出しを実際に持つ .rst 本文
        csv_text = (
            SECTIONS_CSV_HEADER
            + 'c-0001,a.rst,1,1,2,"ページ題 > (L1直下)",2,0,0,0\n'
            + 'c-0002,a.rst,6,6,12,"ページ題 > 節A > (L2直下)",7,0,0,0\n'
            + 'c-0003,a.rst,16,16,20,"ページ題 > 節A > 項目1",5,0,0,0\n'
            + 'c-0004,a.rst,22,22,30,"ページ題 > 節B",9,0,0,0\n'
        )
        path = write_file(self, csv_text, suffix=".csv")
        # When: current-heading を抽出する（git を使わず docs を直接渡す）
        candidates = et.extract_current_headings(path, docs=[("a.rst", RST_DOC)])
        by_term = {c.term: c for c in candidates}
        # Then: 「ページ題」は4行すべてに現れるので4件。file_line は
        # CSVの行の src_line ではなく、見出しテキスト自身の実際の行
        self.assertEqual(by_term["ページ題"].occurrences, 4)
        self.assertEqual(by_term["ページ題"].file_line, "a.rst:1")
        # 「節A」は2行、「節B」は1行、いずれも source は current-heading
        self.assertEqual(by_term["節A"].occurrences, 2)
        self.assertEqual(by_term["節B"].occurrences, 1)
        self.assertEqual(by_term["節A"].source, "current-heading")
        # 「節A」はCSV上のどの行でも src_line が本文開始行（4ではない）だが、
        # file_line は実際の見出し行である4行目を指す
        self.assertEqual(by_term["節A"].file_line, "a.rst:4")
        # 「節B」もCSVのsrc_line(22)ではなく、実際の見出し行(14)を指す
        self.assertEqual(by_term["節B"].file_line, "a.rst:14")
        self.assertEqual(by_term["項目1"].file_line, "a.rst:9")

    def test_marker_only_path_contributes_no_candidate(self):
        # Given: (冒頭) だけの heading_path（本文冒頭セクション）
        csv_text = SECTIONS_CSV_HEADER + 'c-0001,a.rst,1,1,2,(冒頭),2,0,0,0\n'
        path = write_file(self, csv_text, suffix=".csv")
        # When/Then: 候補は出ない（見出し探索も走らない = docs=[] でも成立する）
        self.assertEqual(et.extract_current_headings(path, docs=[]), [])

    def test_missing_heading_in_docs_raises_instead_of_silently_mislocating(self):
        # Given: heading_path にはあるが、docs 側に対応する見出しが無い
        csv_text = SECTIONS_CSV_HEADER + 'c-0001,a.rst,1,1,2,"存在しない見出し",2,0,0,0\n'
        path = write_file(self, csv_text, suffix=".csv")
        # When/Then: 誤った代表行を作らず、エラーにする
        with self.assertRaises(ValueError):
            et.extract_current_headings(path, docs=[("a.rst", RST_DOC)])


# ===========================================================================
# Markdown見出し（ntf-doc-terms.md / design.md 共通のロジック）
# ===========================================================================

MD_SAMPLE = """\
# 文書題

## 見出しA

本文。

### 見出しB

本文。

#### 見出しC

本文。

## 見出しA
"""


class TestExtractMdHeadings(unittest.TestCase):

    def test_h1_excluded_when_min_level_is_2(self):
        # Given: H1〜H4を含むMarkdown
        path = write_file(self, MD_SAMPLE)
        # When: レベル2〜4を候補にする
        candidates = et.extract_md_headings(path, "design-heading", 2, 4)
        terms = {c.term for c in candidates}
        # Then: H1（文書題）は候補に出ない
        self.assertNotIn("文書題", terms)
        self.assertIn("見出しA", terms)
        self.assertIn("見出しB", terms)
        self.assertIn("見出しC", terms)

    def test_level_range_excludes_h4_when_max_level_is_3(self):
        # Given: 同じMarkdown
        path = write_file(self, MD_SAMPLE)
        # When: レベル2〜3だけを候補にする（design.mdの規則）
        candidates = et.extract_md_headings(path, "design-heading", 2, 3)
        terms = {c.term for c in candidates}
        # Then: H4の見出しCは含まれない
        self.assertNotIn("見出しC", terms)

    def test_duplicate_heading_text_is_counted_and_first_location_kept(self):
        # Given: 同じ見出しテキストが2回現れる（"見出しA" は2件目）
        path = write_file(self, MD_SAMPLE)
        candidates = et.extract_md_headings(path, "design-heading", 2, 4)
        by_term = {c.term: c for c in candidates}
        # Then: 出現回数は2、代表file_lineは最初の出現行
        self.assertEqual(by_term["見出しA"].occurrences, 2)
        self.assertTrue(by_term["見出しA"].file_line.endswith(":3"))

    def test_source_label_is_recorded_verbatim(self):
        path = write_file(self, MD_SAMPLE)
        candidates = et.extract_md_headings(path, "ntf-doc-terms-heading", 2, 4)
        self.assertTrue(all(c.source == "ntf-doc-terms-heading" for c in candidates))

    def test_strips_inline_code_backticks_from_heading_text(self):
        # Given: 実例 "#### `FwHeaderDefinition` / `fwHeaderDefinition`"
        # （input/ntf-doc-terms.md の実際の見出し）と同型のMarkdown
        text = "# 題\n\n## 見出しA\n\n#### `Foo` / `bar`\n"
        path = write_file(self, text)
        candidates = et.extract_md_headings(path, "ntf-doc-terms-heading", 2, 4)
        terms = {c.term for c in candidates}
        # Then: バッククォートを含まない表記になる
        self.assertIn("Foo / bar", terms)
        self.assertTrue(all("`" not in t for t in terms))


# ===========================================================================
# design-scheme（design.md「5. 処理方式の名称」表）
# ===========================================================================

DESIGN_SAMPLE = """\
# NTF解説書 章構成設計

## 4. 第3部 テストの実装方法

無関係な章。

## 5. 処理方式の名称

FW解説書の正式名称を使用する。

| 名称 | FW解説書の所在 | NTF対象 |
|---|---|---|
| ウェブアプリケーション | `application_framework/web/` | ○ |
| RESTfulウェブサービス | `application_framework/web_service/rest/` | ○ |

Jakarta Batch は対象外。

## 6. 用語

無関係な章。
"""


class TestExtractDesignSchemes(unittest.TestCase):

    def test_extracts_name_column_of_the_scheme_table(self):
        # Given: 「5. 処理方式の名称」表を含む design.md 相当のファイル
        path = write_file(self, DESIGN_SAMPLE)
        # When: 処理方式名を抽出する
        candidates = et.extract_design_schemes(path)
        terms = [c.term for c in candidates]
        # Then: 表の名称列の2行がそのまま候補になる
        self.assertEqual(terms, ["ウェブアプリケーション", "RESTfulウェブサービス"])
        self.assertTrue(all(c.source == "design-scheme" for c in candidates))
        self.assertTrue(all(c.occurrences == 1 for c in candidates))

    def test_does_not_pick_up_tables_in_other_sections(self):
        # Given: 「5.」以外の章にも表がある想定
        text = DESIGN_SAMPLE.replace(
            "無関係な章。\n\n## 5.",
            "| ダミー | 列 |\n|---|---|\n| 無関係表 | x |\n\n## 5.",
        )
        path = write_file(self, text)
        candidates = et.extract_design_schemes(path)
        terms = [c.term for c in candidates]
        # Then: 「5.」章の表だけが対象
        self.assertNotIn("無関係表", terms)

    def test_missing_section_raises(self):
        # Given: 「5. 処理方式の名称」見出しが無いファイル
        path = write_file(self, "# 題\n\n## 1. 何か\n")
        # When/Then: エラーになる（サイレントに空を返さない）
        with self.assertRaises(ValueError):
            et.extract_design_schemes(path)


# ===========================================================================
# 出力CSVのスキーマ
# ===========================================================================


class TestWriteCsv(unittest.TestCase):

    def test_header_and_columns_match_the_documented_schema(self):
        # Given: 4出典それぞれの候補を1件ずつ
        candidates = [
            et.Candidate("A", "current-heading", 3, "a.rst:1"),
            et.Candidate("B", "ntf-doc-terms-heading", 1, "input/x.md:2"),
            et.Candidate("C", "design-heading", 2, "design.md:3"),
            et.Candidate("D", "design-scheme", 1, "design.md:4"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "term-candidates.csv")
            # When: CSVに書き出す
            et.write_csv(candidates, out)
            # Then: ヘッダは term,source,occurrences,file_line
            with open(out, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(
                list(rows[0].keys()), ["term", "source", "occurrences", "file_line"]
            )
            self.assertEqual(len(rows), 4)
            terms_by_source = {r["source"]: r["term"] for r in rows}
            self.assertEqual(terms_by_source["current-heading"], "A")
            self.assertEqual(terms_by_source["design-scheme"], "D")

    def test_rows_are_grouped_by_source_in_a_fixed_order(self):
        # Given: source の出現順がバラバラな候補リスト
        candidates = [
            et.Candidate("Z", "design-scheme", 1, "design.md:1"),
            et.Candidate("A", "current-heading", 1, "a.rst:1"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "term-candidates.csv")
            et.write_csv(candidates, out)
            with open(out, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            # Then: current-heading が design-scheme より先に出る（再現可能な順序）
            self.assertEqual([r["source"] for r in rows],
                              ["current-heading", "design-scheme"])


# ===========================================================================
# 実物（このセッションのファイル群）に対する自己整合性
# ===========================================================================


class TestRealFiles(unittest.TestCase):

    def test_extract_all_runs_against_the_real_session_files(self):
        # Given/When: 実際の sections-current.csv / ntf-doc-terms.md / design.md
        candidates = et.extract_all()
        # Then: 4出典すべてから候補が出る
        sources = {c.source for c in candidates}
        self.assertEqual(sources, set(et.SOURCE_ORDER))
        # design-scheme は design.md の7名称と一致する
        schemes = {c.term for c in candidates if c.source == "design-scheme"}
        self.assertEqual(len(schemes), 7)
        self.assertIn("ウェブアプリケーション", schemes)
        self.assertIn("テーブルをキューとして使ったメッセージング", schemes)


if __name__ == "__main__":
    unittest.main()
