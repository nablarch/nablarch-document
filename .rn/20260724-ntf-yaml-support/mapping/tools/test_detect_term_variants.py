"""
Tests for detect_term_variants.py
Run with: python3 -m pytest test_detect_term_variants.py -v
or:        python3 test_detect_term_variants.py

コーパスの読み込み（git / ファイルシステム）に依存しないよう、Doc を直接
組み立てて検証する。ただし term_candidates.tsv だけは実物を読んで整合を確認する。
"""
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import detect_term_variants as dtv  # noqa: E402


def doc(corpus, path, *lines):
    return dtv.Doc(corpus, path, list(lines))


# ===========================================================================
# 正規化関数
# ===========================================================================

class TestNormalizers(unittest.TestCase):

    def test_punct_removes_reading_marks_and_connector(self):
        self.assertEqual(dtv.norm_punct("主なクラス, リソース"), "主なクラスリソース")
        self.assertEqual(dtv.norm_punct("主なクラスとリソース"), "主なクラスリソース")
        self.assertEqual(dtv.norm_punct("主なクラス、リソース"), "主なクラスリソース")
        self.assertEqual(dtv.norm_punct("主なクラス・リソース"), "主なクラスリソース")

    def test_punct_removes_inner_space(self):
        self.assertEqual(dtv.norm_punct("HTML ダンプ出力"), dtv.norm_punct("HTMLダンプ出力"))

    def test_paren_masks_content_and_width(self):
        self.assertEqual(dtv.norm_paren("実施方法(バッチ)"), "実施方法（…）")
        self.assertEqual(dtv.norm_paren("実施方法（応答不要メッセージ受信処理）"), "実施方法（…）")

    def test_paren_leaves_bracketless_text_untouched(self):
        self.assertEqual(dtv.norm_paren("テストデータの書き方"), "テストデータの書き方")

    def test_longvowel_strips_prolonged_sound_mark(self):
        self.assertEqual(dtv.norm_longvowel("スーパクラス"), "スパクラス")
        self.assertEqual(dtv.norm_longvowel("スーパークラス"), "スパクラス")

    def test_paren_style_reports_both_ends(self):
        self.assertEqual(dtv.paren_style("実施方法(バッチ)"), "半角")
        self.assertEqual(dtv.paren_style("実施方法（バッチ）"), "全角")
        # 開きが全角、閉じが半角の混在を揺れとして拾えること
        self.assertEqual(dtv.paren_style("実施方法（バッチ)"), "全角,半角")

    def test_has_bracket(self):
        self.assertTrue(dtv.has_bracket("実施方法（バッチ）"))
        self.assertFalse(dtv.has_bracket("実施方法"))


# ===========================================================================
# 抽出単位
# ===========================================================================

class TestUnits(unittest.TestCase):

    def test_terms_include_headings_and_quoted_words(self):
        d = doc("design", "design.md",
                "# 章タイトル",
                "揺れ（例: 「主なクラス, リソース」と「主なクラスとリソース」）を直す。")
        got = sorted(dtv._iter_terms(d))
        self.assertEqual(got, [
            ("主なクラス, リソース", 2),
            ("主なクラスとリソース", 2),
            ("章タイトル", 1),
        ])

    def test_katakana_tokens_need_three_characters(self):
        d = doc("current", "a.rst", "スーパクラスとMQとデータ")
        got = [t for t, _ in dtv._iter_katakana(d)]
        self.assertEqual(got, ["スーパクラス", "データ"])


# ===========================================================================
# discover
# ===========================================================================

class TestDiscover(unittest.TestCase):

    def test_punct_groups_variants_across_corpora(self):
        docs = [
            doc("current", "a.rst", "主なクラス, リソース", "=========="),
            doc("design", "design.md", "「主なクラスとリソース」に統一する。"),
        ]
        rows = dtv.discover(docs, "punct")
        self.assertEqual([r["surface"] for r in rows],
                         ["主なクラス, リソース", "主なクラスとリソース"])
        self.assertEqual(rows[0]["norm_key"], rows[1]["norm_key"])
        self.assertEqual(rows[0]["locations"], "a.rst:1")
        self.assertEqual(rows[1]["corpora"], "design")

    def test_single_surface_group_is_not_reported(self):
        docs = [doc("current", "a.rst", "主なクラス, リソース", "==========")]
        self.assertEqual(dtv.discover(docs, "punct"), [])

    def test_paren_reports_only_when_bracket_style_differs(self):
        same = [doc("current", "a.rst",
                    "実施方法（バッチ）", "==========",
                    "実施方法（メール送信）", "==========")]
        self.assertEqual(dtv.discover(same, "paren"), [])

        differs = [doc("current", "a.rst",
                       "実施方法（バッチ）", "==========",
                       "実施方法(メール送信)", "==========")]
        rows = dtv.discover(differs, "paren")
        self.assertEqual([r["surface"] for r in rows],
                         ["実施方法(メール送信)", "実施方法（バッチ）"])

    def test_longvowel_groups_katakana_variants(self):
        docs = [doc("current", "a.rst", "スーパクラス", "スーパークラス")]
        rows = dtv.discover(docs, "longvowel")
        self.assertEqual([r["surface"] for r in rows], ["スーパクラス", "スーパークラス"])
        self.assertEqual([r["count"] for r in rows], [1, 1])

    def test_output_is_stable_and_sorted(self):
        docs = [
            doc("current", "b.rst", "スーパークラス", "スーパクラス"),
            doc("current", "a.rst", "インターフェース", "インタフェース"),
        ]
        first = dtv.discover(docs, "longvowel")
        second = dtv.discover(docs, "longvowel")
        self.assertEqual(first, second)
        keys = [(r["norm_key"], r["surface"]) for r in first]
        self.assertEqual(keys, sorted(keys))


# ===========================================================================
# match_line / scan
# ===========================================================================

TERMS = [
    dtv.TermEntry("全体", "テスティングフレームワーク", "テスティングフレームワーク"),
    dtv.TermEntry("全体", "テスティングフレームワーク", "自動テストフレームワーク"),
    dtv.TermEntry("全体", "テスティングフレームワーク", "テストフレームワーク"),
]


class TestMatchLine(unittest.TestCase):

    def test_longest_surface_wins_no_double_count(self):
        got = dtv.match_line("自動テストフレームワークを使う", TERMS)
        self.assertEqual([e.surface for e in got], ["自動テストフレームワーク"])

    def test_shorter_surface_still_counted_when_standalone(self):
        got = dtv.match_line("テストフレームワークを使う", TERMS)
        self.assertEqual([e.surface for e in got], ["テストフレームワーク"])

    def test_multiple_occurrences_on_one_line(self):
        got = dtv.match_line("自動テストフレームワークとテストフレームワーク", TERMS)
        self.assertEqual([e.surface for e in got],
                         ["自動テストフレームワーク", "テストフレームワーク"])

    def test_no_match(self):
        self.assertEqual(dtv.match_line("関係のない行", TERMS), [])


class TestScan(unittest.TestCase):

    def test_counts_and_locations_per_corpus(self):
        docs = [
            doc("current", "a.rst", "自動テストフレームワーク", "自動テストフレームワーク"),
            doc("fw", "b.rst", "テスティングフレームワーク"),
        ]
        rows = dtv.scan(docs, TERMS, max_locations=5)
        by = {(r["surface"], r["corpus"]): r for r in rows}
        self.assertEqual(by[("自動テストフレームワーク", "current")]["count"], 2)
        self.assertEqual(by[("自動テストフレームワーク", "current")]["locations"],
                         "a.rst:1;a.rst:2")
        self.assertEqual(by[("自動テストフレームワーク", "fw")]["count"], 0)
        self.assertEqual(by[("テスティングフレームワーク", "fw")]["count"], 1)

    def test_only_loaded_corpora_are_reported(self):
        docs = [doc("current", "a.rst", "テスティングフレームワーク")]
        corpora = {r["corpus"] for r in dtv.scan(docs, TERMS, 5)}
        self.assertEqual(corpora, {"current"})

    def test_locations_are_deduplicated_but_count_is_not(self):
        docs = [doc("current", "a.rst", "テストフレームワークとテストフレームワーク")]
        row = [r for r in dtv.scan(docs, TERMS, 5)
               if r["surface"] == "テストフレームワーク"][0]
        self.assertEqual(row["count"], 2)
        self.assertEqual(row["locations"], "a.rst:1")
        self.assertEqual(row["files"], 1)

    def test_max_locations_truncates(self):
        docs = [doc("current", "a.rst", *["テストフレームワーク"] * 4)]
        row = [r for r in dtv.scan(docs, TERMS, 2)
               if r["surface"] == "テストフレームワーク"][0]
        self.assertEqual(row["count"], 4)
        self.assertEqual(row["locations"], "a.rst:1;a.rst:2")

    def test_row_order_follows_terms_file_order(self):
        docs = [doc("current", "a.rst", "x")]
        rows = dtv.scan(docs, TERMS, 5)
        self.assertEqual([r["surface"] for r in rows], [e.surface for e in TERMS])


# ===========================================================================
# 用語定義ファイル
# ===========================================================================

class TestLoadTerms(unittest.TestCase):

    def _write(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False,
                                        encoding="utf-8", newline="\n")
        f.write(text)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_skips_comments_and_blank_lines(self):
        path = self._write("# コメント\n\n全体\tA\tB\n")
        self.assertEqual(dtv.load_terms(path), [dtv.TermEntry("全体", "A", "B")])

    def test_rejects_wrong_column_count(self):
        path = self._write("全体\tA\n")
        with self.assertRaises(ValueError):
            dtv.load_terms(path)

    def test_rejects_duplicate_entries(self):
        path = self._write("全体\tA\tB\n全体\tA\tB\n")
        with self.assertRaises(ValueError):
            dtv.load_terms(path)

    def test_rejects_empty_surface(self):
        path = self._write("全体\tA\t\n")
        with self.assertRaises(ValueError):
            dtv.load_terms(path)


class TestTermCandidatesFile(unittest.TestCase):
    """同梱の term_candidates.tsv 自体の整合性。"""

    def setUp(self):
        self.entries = dtv.load_terms(dtv.DEFAULT_TERMS_FILE)

    def test_file_is_not_empty(self):
        self.assertGreater(len(self.entries), 50)

    def test_every_canonical_is_listed_as_its_own_surface(self):
        """正表記そのものを探さないと、採用根拠の出現数が出せない。"""
        surfaces = {(e.canonical, e.surface) for e in self.entries}
        missing = sorted({e.canonical for e in self.entries
                          if (e.canonical, e.canonical) not in surfaces})
        self.assertEqual(missing, [])

    def test_canonical_belongs_to_exactly_one_category(self):
        seen = {}
        for e in self.entries:
            seen.setdefault(e.canonical, set()).add(e.category)
        multi = sorted(c for c, cats in seen.items() if len(cats) > 1)
        self.assertEqual(multi, [])

    def test_surface_is_not_shared_between_canonicals(self):
        """同じ表記を2つの正表記の揺れにすると、出現数の解釈が定まらない。"""
        seen = {}
        for e in self.entries:
            seen.setdefault(e.surface, set()).add(e.canonical)
        shared = sorted(s for s, cs in seen.items() if len(cs) > 1)
        self.assertEqual(shared, [])


# ===========================================================================
# 出力
# ===========================================================================

class TestWriteTsv(unittest.TestCase):

    def test_writes_header_and_lf_only(self):
        out = io.StringIO()
        dtv.write_tsv([{"a": 1, "b": "x"}], ("a", "b"), out)
        self.assertEqual(out.getvalue(), "a\tb\n1\tx\n")


class TestCorpusArgument(unittest.TestCase):

    def test_rejects_unknown_corpus(self):
        parser = dtv.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["discover", "--rule", "punct", "--corpus", "nope"])

    def test_accepts_comma_separated_list(self):
        args = dtv.build_parser().parse_args(
            ["scan", "--corpus", "current,fw"])
        self.assertEqual(args.corpus, ["current", "fw"])


if __name__ == "__main__":
    unittest.main()
