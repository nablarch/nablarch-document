"""
Tests for detect_term_variants.py
Run with: python3 -m pytest test_detect_term_variants.py -v
or:        python3 test_detect_term_variants.py

純関数の検証は、コーパスの読み込み（git / ファイルシステム）に依存しないよう
Doc を直接組み立てて行う。ただし次の2つは実物を読む。

  - term_candidates.tsv 自体の整合性
  - コーパス取得層（どのコミットの・どのファイルを読むか）。ここが壊れると
    用語集の file:line が全部ずれるため、実リポジトリに対して検証する。
"""
import io
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import detect_term_variants as dtv  # noqa: E402


def git(*args):
    return subprocess.run(
        ["git", "-C", dtv.REPO_ROOT, *args],
        check=True, capture_output=True, text=True,
    ).stdout


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

    def test_spacing_removes_ascii_space_only(self):
        # Given: 英数字と日本語の間に半角空白を挟んだ表記と挟まない表記
        # When: spacing 用に正規化する
        # Then: 同じキーに畳まれる
        self.assertEqual(dtv.norm_spacing("グループ ID"), dtv.norm_spacing("グループID"))
        self.assertEqual(dtv.norm_spacing("リクエスト ID"), "リクエストID")

    def test_mixes_scripts_selects_boundary_cases_only(self):
        # Given: 英数字と日本語が混在する塊／英字だけの塊／日本語だけの塊
        # When: spacing ルールの対象かを判定する
        # Then: 混在するものだけが対象になる
        self.assertTrue(dtv.mixes_scripts("グループ ID"))
        self.assertTrue(dtv.mixes_scripts("HTML ダンプ"))
        self.assertFalse(dtv.mixes_scripts("Bean Validation"))
        self.assertFalse(dtv.mixes_scripts("表記の揺れ"))


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

    def test_spaced_tokens_come_from_body_text_not_only_headings(self):
        # Given: 見出しでも「」内でもない散文・表セルに空白入りの語がある
        d = doc("input", "a.md",
                "| `context` | リクエスト ID・ユーザを記載した表 |")
        # When: spacing の抽出単位で取り出す
        got = [t for t, _ in dtv._iter_spaced_tokens(d)]
        # Then: 散文中の「リクエスト ID」が拾える（term 単位では拾えない）
        self.assertIn("リクエスト ID", got)
        self.assertEqual([t for t, _ in dtv._iter_terms(d)], [])

    def test_spaced_tokens_do_not_span_multiple_spaces(self):
        # Given: RSTの表の桁揃えで空白が連続している行
        d = doc("current", "a.rst", "MESSAGES            応答電文")
        # When: spacing の抽出単位で取り出す
        got = [t for t, _ in dtv._iter_spaced_tokens(d)]
        # Then: 桁揃えを1語として拾わない
        self.assertEqual(got, ["MESSAGES", "応答電文"])


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

    def test_spacing_groups_variants_found_in_body_text(self):
        # Given: 散文に「グループ ID」と「グループID」が混在するコーパス
        docs = [
            doc("input", "a.md", "同じシート内のデータを識別する グループ ID を指定する。"),
            doc("current", "b.rst", "グループIDを指定する。"),
        ]
        # When: spacing ルールで揺れを探す
        rows = dtv.discover(docs, "spacing")
        # Then: 空白の有無だけが違う2表記が同一グループとして報告される
        self.assertEqual([r["surface"] for r in rows], ["グループ ID", "グループID"])
        self.assertEqual(rows[0]["norm_key"], "グループID")

    def test_spacing_ignores_ascii_only_tokens(self):
        # Given: 英字だけの分かち書きの差
        docs = [doc("fw", "a.rst", "Bean Validation を使う"),
                doc("fw", "b.rst", "BeanValidation を使う")]
        # When: spacing ルールで揺れを探す
        # Then: 英文の通常の分かち書きは報告しない
        self.assertEqual(dtv.discover(docs, "spacing"), [])

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

    def test_longer_surface_wins_even_when_it_starts_later(self):
        # Given: 先に始まる短い表記と、後から始まるより長い表記が重なる行
        #        「疎通確認用の都度起動バッチアプリケーション」
        terms = [
            dtv.TermEntry("処理方式", "都度起動バッチ", "都度起動バッチ"),
            dtv.TermEntry("処理方式", "Nablarchバッチアプリケーション", "バッチアプリケーション"),
        ]
        # When: 1行からマッチを取る
        got = dtv.match_line("疎通確認用の都度起動バッチアプリケーションを実行する", terms)
        # Then: 最長一致で「バッチアプリケーション」が採られる。
        #       開始位置優先だと短い「都度起動バッチ」が長い方を抑止してしまう
        self.assertEqual([e.surface for e in got], ["バッチアプリケーション"])

    def test_non_overlapping_matches_are_returned_in_positional_order(self):
        # Given: 重ならない2表記が逆順の長さで並ぶ行
        terms = [
            dtv.TermEntry("t", "A", "シート"),
            dtv.TermEntry("t", "B", "テストデータファイル"),
        ]
        # When: 1行からマッチを取る
        got = dtv.match_line("シートはテストデータファイルの一部である", terms)
        # Then: 長さではなく行内の出現順で返る
        self.assertEqual([e.surface for e in got], ["シート", "テストデータファイル"])


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

    def test_preamble_is_written_as_comment_lines(self):
        # Given: 来歴を刻む preamble
        out = io.StringIO()
        # When: preamble 付きでTSVを書く
        dtv.write_tsv([{"a": 1}], ("a",), out, ["基準コミット: abc"])
        # Then: `#` 始まりのコメント行としてヘッダより前に出る
        self.assertEqual(out.getvalue(), "# 基準コミット: abc\na\n1\n")

    def test_output_preamble_records_base_commit_and_corpora(self):
        # Given/When: scan の来歴を組み立てる
        notes = dtv.output_preamble("scan", ["current", "fw"], "--terms t.tsv")
        # Then: 基準コミットとコーパスが出力自身に残る
        self.assertIn("current,fw", notes[1])
        self.assertIn(dtv.base_commit(), notes[2])


class TestCorpusArgument(unittest.TestCase):

    def test_rejects_unknown_corpus(self):
        parser = dtv.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["discover", "--rule", "punct", "--corpus", "nope"])

    def test_accepts_comma_separated_list(self):
        args = dtv.build_parser().parse_args(
            ["scan", "--corpus", "current,fw"])
        self.assertEqual(args.corpus, ["current", "fw"])

    def test_unknown_corpus_message_is_shared_and_japanese(self):
        # Given: 未知のコーパス名
        # When: CLI と load_corpora のそれぞれがエラーを出す
        with self.assertRaises(ValueError) as ctx:
            dtv.load_corpora(["nope"])
        # Then: 同一事象に同じ日本語の文言を使う
        self.assertEqual(str(ctx.exception), dtv.unknown_corpus_message("nope"))
        self.assertIn("未知", str(ctx.exception))


# ===========================================================================
# コーパス取得層 — どのコミットの・どのファイルを読むか
# ===========================================================================

class TestBaseCommit(unittest.TestCase):

    def setUp(self):
        self._saved = os.environ.pop(dtv.BASE_COMMIT_ENV, None)
        self.addCleanup(self._restore)

    def _restore(self):
        os.environ.pop(dtv.BASE_COMMIT_ENV, None)
        if self._saved is not None:
            os.environ[dtv.BASE_COMMIT_ENV] = self._saved

    def test_default_is_the_pinned_constant(self):
        # Given: 環境変数を設定していない
        # When: 基準コミットを求める
        # Then: 実行時に merge-base を解決せず、固定した定数を返す
        self.assertEqual(dtv.base_commit(), dtv.DEFAULT_BASE_COMMIT)
        self.assertRegex(dtv.DEFAULT_BASE_COMMIT, r"^[0-9a-f]{40}$")

    def test_pinned_commit_exists_and_holds_the_current_doc(self):
        # Given: 固定した基準コミット
        # When: そのコミットのツリーを引く
        listing = git("ls-tree", "-r", "--name-only",
                      dtv.DEFAULT_BASE_COMMIT, "--", dtv.CURRENT_DOC_ROOT + "/")
        # Then: 現行解説書が存在する
        self.assertTrue(listing.strip())

    def test_env_override_is_resolved_as_a_git_revision(self):
        # Given: 環境変数にリビジョン名（SHAではない）を設定
        os.environ[dtv.BASE_COMMIT_ENV] = "HEAD"
        # When: 基準コミットを求める
        # Then: rev-parse で解決したSHAが返る
        self.assertEqual(dtv.base_commit(), git("rev-parse", "HEAD").strip())


class TestCorpusLoading(unittest.TestCase):
    """「どのファイルを読むか」を実リポジトリに対して検証する。"""

    @classmethod
    def setUpClass(cls):
        cls.current = dtv.load_corpora(["current"])
        cls.inputs = dtv.load_corpora(["input"])

    def test_current_corpus_is_the_47_rst_files_of_the_base_commit(self):
        # Given: 基準コミットの testing_framework 配下
        listing = git("ls-tree", "-r", "--name-only",
                      dtv.DEFAULT_BASE_COMMIT, "--", dtv.CURRENT_DOC_ROOT + "/")
        expected = sorted(p for p in listing.splitlines() if p.endswith(".rst"))
        # When: current コーパスを読む
        # Then: .rst が過不足なく読まれている
        self.assertEqual([d.path for d in self.current], expected)
        self.assertEqual(len(self.current), 47)

    def test_current_corpus_excludes_non_rst_files(self):
        # Given: 同ディレクトリには .png / .xlsx / .java も置かれている
        listing = git("ls-tree", "-r", "--name-only",
                      dtv.DEFAULT_BASE_COMMIT, "--", dtv.CURRENT_DOC_ROOT + "/")
        others = [p for p in listing.splitlines() if not p.endswith(".rst")]
        # When/Then: それらは読み込まれない（読むと行番号が意味を持たない）
        self.assertTrue(others, "前提が崩れている: .rst 以外のファイルが無い")
        loaded = {d.path for d in self.current}
        self.assertEqual(loaded & set(others), set())

    def test_current_corpus_reads_the_base_commit_not_the_worktree(self):
        # Given: current の1ファイル
        sample = self.current[0]
        # When: 同じパスを基準コミットから直接取り出す
        text = git("show", f"{dtv.DEFAULT_BASE_COMMIT}:{sample.path}")
        # Then: 内容が一致する（作業ツリーではなく基準コミットを読んでいる）
        self.assertEqual(sample.lines, text.splitlines())

    def test_line_numbers_are_one_based_and_match_the_source(self):
        # Given: current の1ファイルと、そこから読んだ行のリスト
        sample = self.current[0]
        text = git("show", f"{dtv.DEFAULT_BASE_COMMIT}:{sample.path}")
        raw = text.splitlines()
        # When: scan が使う「index + 1」で行番号を作る
        # Then: 1始まりで原文の同じ行を指す
        for i in (0, len(raw) // 2, len(raw) - 1):
            self.assertEqual(sample.lines[i], raw[i])
            line_no = i + 1
            self.assertEqual(sample.lines[line_no - 1], raw[i])

    def test_input_corpus_is_the_10_markdown_files_of_the_worktree(self):
        # Given: input ディレクトリ
        names = sorted(n for n in os.listdir(dtv.INPUT_DIR) if n.endswith(".md"))
        # When: input コーパスを読む
        # Then: .md が過不足なく読まれている
        self.assertEqual(len(self.inputs), 10)
        self.assertEqual([os.path.basename(d.path) for d in self.inputs], names)
        for d in self.inputs:
            self.assertEqual(d.corpus, "input")

    def test_input_corpus_reads_the_worktree(self):
        # Given: input の1ファイル
        sample = self.inputs[0]
        # When: 作業ツリーの同じファイルを読む
        with open(os.path.join(dtv.REPO_ROOT, sample.path), encoding="utf-8") as f:
            raw = f.read().splitlines()
        # Then: 内容が一致する
        self.assertEqual(sample.lines, raw)

    def test_paths_are_repo_relative(self):
        # Given/When: 読み込んだ全ドキュメント
        # Then: パスはリポジトリルートからの相対で、絶対パスを含まない
        for d in self.current + self.inputs:
            self.assertFalse(os.path.isabs(d.path))
            self.assertTrue(os.path.isfile(os.path.join(dtv.REPO_ROOT, d.path))
                            or d.corpus == "current")

    def test_load_corpora_is_ordered_deterministically(self):
        # Given: 同じ指定で2回読む
        first = [(d.corpus, d.path) for d in dtv.load_corpora(["input", "design"])]
        second = [(d.corpus, d.path) for d in dtv.load_corpora(["design", "input"])]
        # Then: 指定順によらず corpus 名・パスの順に整列される
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(
            first, key=lambda t: (dtv.ALL_CORPORA.index(t[0]), t[1])))

    def test_design_corpus_is_a_single_file(self):
        # Given/When: design コーパスを読む
        docs = dtv.load_corpora(["design"])
        # Then: design.md 1ファイルだけ
        self.assertEqual(len(docs), 1)
        self.assertTrue(docs[0].path.endswith("design.md"))

    def test_fw_corpus_is_the_rst_files_of_the_worktree(self):
        # Given: FW解説書のディレクトリ
        root = os.path.join(dtv.REPO_ROOT, dtv.FW_DOC_ROOT)
        expected = sorted(
            os.path.relpath(os.path.join(d, n), dtv.REPO_ROOT)
            for d, _, files in os.walk(root) for n in files if n.endswith(".rst")
        )
        # When: fw コーパスを読む
        docs = dtv.load_corpora(["fw"])
        # Then: 作業ツリーの .rst が過不足なく読まれている
        self.assertEqual([d.path for d in docs], expected)
        self.assertTrue(all(d.path.endswith(".rst") for d in docs))


class TestMain(unittest.TestCase):
    """CLI を通した経路。出力ファイルに来歴が刻まれることまで見る。"""

    def _out_path(self):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_discover_writes_tsv_with_provenance_header(self):
        # Given: design コーパスだけを対象にした discover
        out = self._out_path()
        # When: CLI を実行する
        rc = dtv.main(["discover", "--rule", "punct", "--corpus", "design", "-o", out])
        # Then: 正常終了し、先頭に基準コミットとコーパスが刻まれる
        self.assertEqual(rc, 0)
        with open(out, encoding="utf-8") as f:
            lines = f.read().splitlines()
        self.assertTrue(lines[0].startswith("# 生成: detect_term_variants.py discover"))
        self.assertIn("design", lines[1])
        self.assertIn(dtv.base_commit(), lines[2])
        self.assertEqual(lines[3].split("\t"), list(dtv.DISCOVER_COLUMNS))

    def test_scan_writes_one_row_per_surface_and_corpus(self):
        # Given: design コーパスだけを対象にした scan
        out = self._out_path()
        # When: CLI を実行する
        rc = dtv.main(["scan", "--corpus", "design", "-o", out])
        # Then: 用語定義ファイルの表記数と行数が一致する（1コーパスなので1行ずつ）
        self.assertEqual(rc, 0)
        with open(out, encoding="utf-8") as f:
            rows = [l for l in f.read().splitlines() if not l.startswith("#")]
        entries = dtv.load_terms(dtv.DEFAULT_TERMS_FILE)
        self.assertEqual(len(rows) - 1, len(entries))
        self.assertEqual(rows[0].split("\t"), list(dtv.SCAN_COLUMNS))

    def test_output_goes_to_stdout_when_dash(self):
        # Given: 出力先に "-" を指定
        buf = io.StringIO()
        saved, sys.stdout = sys.stdout, buf
        try:
            # When: CLI を実行する
            rc = dtv.main(["discover", "--rule", "longvowel", "--corpus", "design"])
        finally:
            sys.stdout = saved
        # Then: 標準出力にTSVが出る
        self.assertEqual(rc, 0)
        self.assertIn("# 生成:", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
