"""
Tests for verify_glossary.py
Run with: python3 -m pytest test_verify_glossary.py -v
or:        python3 test_verify_glossary.py

verify_glossary.py が「不一致を見逃さない」ことを、壊した用語集を食わせて確認する。
検証器が素通しなら用語集の根拠は担保されないため、素通ししないことを明示的に見る。
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import detect_term_variants as dtv  # noqa: E402
import verify_glossary as vg  # noqa: E402


def write_md(case, text):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                    encoding="utf-8", newline="\n")
    f.write(text)
    f.close()
    case.addCleanup(os.unlink, f.name)
    return f.name


# 現行解説書の実在する行。`テスティングフレームワーク` を含む。
REAL_REF = "NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:55"
REAL_TERM = "テスティングフレームワーク"


# ===========================================================================
# 参照の解決
# ===========================================================================

class TestResolveRef(unittest.TestCase):

    def test_expands_each_prefix(self):
        # Given: 各接頭辞の参照
        # When/Then: 展開先とコミット基準が接頭辞ごとに決まる
        rel, from_base, line = vg.resolve_ref("NTF:a/b.rst:12")
        self.assertTrue(rel.startswith("ja/development_tools/testing_framework/guide"))
        self.assertTrue(from_base)
        self.assertEqual(line, 12)

        rel, from_base, _ = vg.resolve_ref("FW:libraries/x.rst:1")
        self.assertTrue(rel.startswith("ja/application_framework"))
        self.assertFalse(from_base)

    def test_ntf_root_is_matched_before_ntf(self):
        # Given: NTF-root は NTF と前方一致が重なる
        # When/Then: 長いほうが優先される
        rel, _, _ = vg.resolve_ref("NTF-root:index.rst:2")
        self.assertEqual(rel, "ja/development_tools/testing_framework/index.rst")

    def test_non_reference_returns_none(self):
        self.assertIsNone(vg.resolve_ref("テストデータ"))
        self.assertIsNone(vg.resolve_ref("NTF:a/b.rst"))


class TestLooksLikeTerm(unittest.TestCase):

    def test_paths_and_ellipses_are_not_terms(self):
        # Given: パス・省略記号を含むコードスパン
        # When/Then: 原文に現れる表記としては扱わない
        self.assertFalse(vg.looks_like_term("FW:libraries/..."))
        self.assertFalse(vg.looks_like_term("design.md"))
        self.assertFalse(vg.looks_like_term(":109"))

    def test_terms_with_slash_are_still_terms(self):
        # Given: スラッシュを含むが用語である表記
        # When/Then: 用語として扱う（パス判定でこれを落とさない）
        self.assertTrue(vg.looks_like_term("Form/Entity単体テスト"))


# ===========================================================================
# 表の解析
# ===========================================================================

TABLE_MD = """\
## 5. 用語

### 5.1 全体

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テストデータ` | 意味 | `想定結果` | `セクション` | 根拠 |

## 8. 対応表

| 現行解説書・input資料の語 | 正表記 | 適用条件 |
|---|---|---|
| `想定結果` | `テストデータ` | 無条件 |
"""


class TestTableParsing(unittest.TestCase):

    def setUp(self):
        self.path = write_md(self, TABLE_MD)
        self.tables = vg.read_tables(self.path)

    def test_tables_are_grouped_under_their_heading(self):
        # Given/When: 表を読む
        sections = [t[0] for t in self.tables]
        # Then: 直近の見出しが表に付く
        self.assertEqual(sections, ["5.1 全体", "8. 対応表"])

    def test_column_terms_picks_code_spans_of_the_named_column(self):
        # Given/When: 「揺れ表記」列のコードスパンを取る
        got = vg.column_terms(self.tables, vg.VARIANT_HEADER, "5.")
        # Then: その列だけが返る
        self.assertEqual(set(got), {"想定結果"})

    def test_cells_are_split_per_column(self):
        # Given/When: 検査単位に切る
        cells = vg.read_cells(self.path)
        # Then: 区切り行は落とし、表は列ごとのセルになる
        self.assertNotIn("---", [c.text for c in cells])
        self.assertIn("`テストデータ`", [c.text for c in cells if c.column == 0])


# ===========================================================================
# 5つの検査が不一致を見逃さないこと
# ===========================================================================

class TestChecksDetectProblems(unittest.TestCase):

    def _cells(self, text):
        return vg.read_cells(write_md(self, text))

    def test_ref_to_missing_file_is_reported(self):
        # Given: 存在しないファイルへの参照（表記と参照は同じセルに置く）
        cells = self._cells(f"| `{REAL_TERM}`（`NTF:no/such.rst:1`） |\n")
        # When: 参照を検査する
        checked, problems = vg.check_refs(cells, {REAL_TERM})
        # Then: 不一致として報告される
        self.assertEqual(checked, 1)
        self.assertIn("ファイルなし", problems[0].detail)

    def test_ref_out_of_range_is_reported(self):
        # Given: 行数を超える行番号
        cells = self._cells(f"| `{REAL_TERM}`（`NTF-root:index.rst:99999`） |\n")
        _, problems = vg.check_refs(cells, {REAL_TERM})
        self.assertIn("範囲外", problems[0].detail)

    def test_ref_whose_line_lacks_the_named_term_is_reported(self):
        # Given: 実在する行だが、直前で名指しした表記を含まない
        cells = self._cells(f"| `想定結果`（`{REAL_REF}`） |\n")
        _, problems = vg.check_refs(cells, {"想定結果"})
        self.assertIn("表記", problems[0].detail)

    def test_correct_ref_passes(self):
        # Given: 実在する行に、名指しした表記がある
        cells = self._cells(f"| `{REAL_TERM}`（`{REAL_REF}`） |\n")
        checked, problems = vg.check_refs(cells, {REAL_TERM})
        self.assertEqual((checked, problems), (1, []))

    def test_short_ref_binds_to_the_previous_file(self):
        # Given: 直前の完全な参照に続く略記 `:N`
        cells = self._cells(f"| `{REAL_TERM}`（`{REAL_REF}`、`:56`） |\n")
        checked, problems = vg.check_refs(cells, {REAL_TERM})
        # Then: 同じファイルの56行目として解決され、内容も検査される
        self.assertEqual(checked, 2)
        self.assertTrue(problems)  # :56 には当該表記が無い

    def test_expectation_does_not_leak_across_columns(self):
        # Given: 表記と参照が別の列にある行
        cells = self._cells(f"| `想定結果` | `{REAL_REF}` |\n")
        # When: 参照を検査する
        checked, problems = vg.check_refs(cells, {"想定結果"})
        # Then: 参照の実在は見るが、隣の列の表記は内容検査に使わない
        self.assertEqual((checked, problems), (1, []))

    def test_count_mismatch_is_reported(self):
        # Given: scan と食い違う件数
        cells = self._cells("| `テストデータ`（現行999件） |\n")
        checked, problems = vg.check_counts(cells, {("テストデータ", "current"): 223})
        self.assertEqual(checked, 1)
        self.assertIn("記載 999", problems[0].detail)

    def test_count_without_a_term_to_attach_to_is_reported(self):
        # Given: 係り先のコードスパンが無い件数
        cells = self._cells("| FW26件だけ書いた |\n")
        _, problems = vg.check_counts(cells, {})
        self.assertIn("係り先が無い", problems[0].detail)

    def test_counts_outside_tables_are_not_checked(self):
        # Given: 表ではない散文の件数
        cells = self._cells("`テストデータ` は現行999件ある。\n")
        checked, problems = vg.check_counts(cells, {("テストデータ", "current"): 223})
        # Then: 検査対象は表のセルだけ
        self.assertEqual((checked, problems), (0, []))

    def test_matching_count_passes(self):
        cells = self._cells("| `テストデータ`（現行223件） |\n")
        checked, problems = vg.check_counts(cells, {("テストデータ", "current"): 223})
        self.assertEqual((checked, problems), (1, []))

    def test_variant_missing_from_mapping_table_is_reported(self):
        # Given: §5 にあって §8 に無い揺れ表記
        broken = TABLE_MD.replace("| `想定結果` | `テストデータ` | 無条件 |\n", "")
        tables = vg.read_tables(write_md(self, broken))
        checked, problems = vg.check_sections(tables)
        self.assertEqual(checked, 1)
        self.assertIn("§8 対応表に無い", problems[0].detail)

    def test_consistent_sections_pass(self):
        tables = vg.read_tables(write_md(self, TABLE_MD))
        self.assertEqual(vg.check_sections(tables)[1], [])

    def test_row_without_apply_condition_is_reported(self):
        # Given: 適用条件が空の行
        broken = TABLE_MD.replace("| `想定結果` | `テストデータ` | 無条件 |",
                                  "| `想定結果` | `テストデータ` |  |")
        tables = vg.read_tables(write_md(self, broken))
        _, problems = vg.check_applies(tables)
        self.assertIn("適用条件が空", problems[0].detail)

    def test_missing_apply_column_is_reported(self):
        # Given: 適用条件の列そのものが無い対応表
        broken = TABLE_MD.replace("| 現行解説書・input資料の語 | 正表記 | 適用条件 |",
                                  "| 現行解説書・input資料の語 | 正表記 |")
        tables = vg.read_tables(write_md(self, broken))
        _, problems = vg.check_applies(tables)
        self.assertIn("「適用条件」列が無い", problems[0].detail)

    def test_canonical_missing_from_glossary_is_reported(self):
        # Given: tsv にあって §5 の正表記列に無い語
        tables = vg.read_tables(write_md(self, TABLE_MD))
        entries = [dtv.TermEntry("t", "テストデータ", "テストデータ"),
                   dtv.TermEntry("t", "存在しない正表記", "存在しない正表記")]
        counts = {("テストデータ", "current"): 1, ("存在しない正表記", "current"): 1}
        _, problems = vg.check_terms(tables, entries, counts)
        details = " ".join(p.detail for p in problems)
        self.assertIn("存在しない正表記", details)

    def test_unattested_surface_need_not_be_listed(self):
        # Given: 全コーパスで0件の表記（念のため探した候補）
        tables = vg.read_tables(write_md(self, TABLE_MD))
        entries = [dtv.TermEntry("t", "テストデータ", "テストデータ"),
                   dtv.TermEntry("t", "テストデータ", "未出現の表記"),
                   dtv.TermEntry("t", "想定結果", "想定結果"),
                   dtv.TermEntry("t", "セクション", "セクション")]
        counts = {("テストデータ", "current"): 1, ("想定結果", "current"): 1,
                  ("セクション", "input"): 1, ("未出現の表記", "current"): 0}
        _, problems = vg.check_terms(tables, entries, counts)
        # Then: 出現0の表記は掲載を求めない。正表記が足りない分だけが残る
        details = " ".join(p.detail for p in problems)
        self.assertNotIn("未出現の表記", details)


# ===========================================================================
# #3 母集団の全件判定（population / design_sections / scheme_names / reasons）
# ===========================================================================

# TABLE_MD（§5・§8）に加えて §5.15 相当の不採用テーブルを持つサンプル。
POPULATION_MD = TABLE_MD + """

### 5.2 処理方式

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `ウェブアプリケーション` | 画面を持つHTTPアプリケーション | 揺れなし | なし | design.md |

### 5.15 term-candidates.csv との対応

#### 5.15.2 不採用 — design.md の章・セクション見出し

| 候補 | design.md所在 | 理由 |
|---|---|---|
| `1. 読者と構成` | `S:design.md:3` | design.mdの章・セクション見出しであり用語ではない |

#### 5.15.5 不採用 — 現行解説書の見出し

| 候補 | 理由 |
|---|---|
| `該当ページ固有の見出し` | ページ固有の題であり骨格用語ではない |
"""


def make_candidate(term, source="current-heading", occurrences=1, file_line="a.rst:1"):
    return vg.CandidateRow(term, source, occurrences, file_line)


class TestLoadCandidates(unittest.TestCase):

    def test_reads_the_documented_four_columns(self):
        # Given: term,source,occurrences,file_line のCSV
        f = tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, encoding="utf-8", newline="\n")
        f.write("term,source,occurrences,file_line\n")
        f.write("テストデータ,current-heading,3,a.rst:1\n")
        f.close()
        self.addCleanup(os.unlink, f.name)
        # When: 読み込む
        rows = vg.load_candidates(f.name)
        # Then: 型つきで1件返る（occurrencesはint）
        self.assertEqual(rows, [vg.CandidateRow("テストデータ", "current-heading", 3, "a.rst:1")])


class TestListedAndRejectedTerms(unittest.TestCase):

    def test_listed_terms_is_the_union_of_the_three_5_columns(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        listed = vg.listed_terms(tables)
        # Then: §5の正表記・揺れ表記・別義がすべて入る
        self.assertIn("テストデータ", listed)
        self.assertIn("想定結果", listed)
        self.assertIn("セクション", listed)
        self.assertIn("ウェブアプリケーション", listed)

    def test_rejected_terms_maps_candidate_to_its_reason(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        rejected = vg.rejected_terms(tables)
        self.assertEqual(
            rejected["1. 読者と構成"],
            "design.mdの章・セクション見出しであり用語ではない")

    def test_rejected_terms_splits_a_bundled_candidate_cell(self):
        # Given: §5.15.5型の「1セルに複数候補」の行
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        rejected = vg.rejected_terms(tables)
        # Then: セル内のコードスパンごとに理由が割り当たる
        self.assertIn("該当ページ固有の見出し", rejected)


class TestPopulationCheck(unittest.TestCase):

    def test_unjudged_candidate_is_reported(self):
        # Given: §5にも§5.15の不採用テーブルにも無い候補
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [make_candidate("誰も判定していない候補")]
        # When: population検査
        checked, problems = vg.check_population(tables, candidates)
        # Then: 未判定として報告される
        self.assertEqual(checked, 1)
        self.assertIn("未判定", problems[0].detail)

    def test_adopted_candidate_passes(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [make_candidate("テストデータ")]
        self.assertEqual(vg.check_population(tables, candidates)[1], [])

    def test_rejected_with_reason_candidate_passes(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [make_candidate("1. 読者と構成", source="design-heading")]
        self.assertEqual(vg.check_population(tables, candidates)[1], [])

    def test_duplicate_terms_across_sources_are_judged_once(self):
        # Given: 同じ表記が current-heading と design-heading の両方の行として
        # term-candidates.csv にある（出典が違うだけ）
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [
            make_candidate("テストデータ", source="current-heading"),
            make_candidate("テストデータ", source="design-heading"),
        ]
        # When/Then: 表記としては1種類なので、判定は1件で済み不一致は出ない
        checked, problems = vg.check_population(tables, candidates)
        self.assertEqual((checked, problems), (1, []))


class TestDesignSectionsCheck(unittest.TestCase):

    def test_missing_design_heading_is_reported(self):
        cells = vg.read_cells(write_md(self, POPULATION_MD))
        candidates = [make_candidate("glossary.mdに存在しない章名", source="design-heading")]
        checked, problems = vg.check_design_sections(cells, candidates)
        self.assertEqual(checked, 1)
        self.assertIn("glossary.md に無い", problems[0].detail)

    def test_present_design_heading_passes(self):
        cells = vg.read_cells(write_md(self, POPULATION_MD))
        candidates = [make_candidate("1. 読者と構成", source="design-heading")]
        self.assertEqual(vg.check_design_sections(cells, candidates)[1], [])

    def test_non_design_heading_sources_are_ignored(self):
        # Given: design-heading以外の出典しか無い
        cells = vg.read_cells(write_md(self, POPULATION_MD))
        candidates = [make_candidate("どこにも無い語", source="current-heading")]
        # When/Then: design_sections検査の対象外なので検証0件
        self.assertEqual(vg.check_design_sections(cells, candidates), (0, []))


class TestSchemeNamesCheck(unittest.TestCase):

    def test_scheme_name_matching_5_2_canonical_passes(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [make_candidate("ウェブアプリケーション", source="design-scheme")]
        self.assertEqual(vg.check_scheme_names(tables, candidates)[1], [])

    def test_scheme_name_not_in_5_2_is_reported(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        candidates = [make_candidate("存在しない処理方式", source="design-scheme")]
        checked, problems = vg.check_scheme_names(tables, candidates)
        self.assertEqual(checked, 1)
        self.assertIn("design.mdの正式名称と不一致", problems[0].detail)


class TestReasonsCheck(unittest.TestCase):

    def test_empty_reason_is_reported(self):
        broken = POPULATION_MD.replace(
            "| `1. 読者と構成` | `S:design.md:3` | design.mdの章・セクション見出しであり用語ではない |",
            "| `1. 読者と構成` | `S:design.md:3` |  |")
        tables = vg.read_tables(write_md(self, broken))
        _, problems = vg.check_reasons(tables)
        self.assertIn("理由が空", problems[0].detail)

    def test_filled_reasons_pass(self):
        tables = vg.read_tables(write_md(self, POPULATION_MD))
        checked, problems = vg.check_reasons(tables)
        self.assertEqual(problems, [])
        self.assertEqual(checked, 2)  # 5.15.2 の1行 + 5.15.5 の1行


# ===========================================================================
# 実物
# ===========================================================================

class TestRealGlossary(unittest.TestCase):

    def test_glossary_passes_all_checks(self):
        # Given/When: コミットしてある用語集と scan 出力
        # Then: 5つの検査がすべて通る
        self.assertEqual(vg.main([]), 0)


if __name__ == "__main__":
    unittest.main()
