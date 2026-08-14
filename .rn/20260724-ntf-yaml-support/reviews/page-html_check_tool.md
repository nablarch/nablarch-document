# page-html_check_tool — HTMLチェックツール（`#27-06`）

対象ファイル: `ja/development_tools/testing_framework/tools/html_check_tool.rst`
ラベル: `html_check_tool`（`mapping/style.md:392`）
部: 第4部 ツール（`ntf-doc-weekend-queue.md:63` により導入なし）

## 参照リポジトリ

| リポジトリ | 作業指示のピン | 事実の取得方法 |
|---|---|---|
| `nablarch-testing` | `e21bf67` | 作業ツリーHEADの祖先ではないため、すべて `git show e21bf67:<path>` で取得 |
| `nablarch-example-web` | ピンなし | 作業ツリーの内容を参照（デフォルト設定の設定ファイル、`unit-test.xml`） |

## 出典行の消化

`mapping.csv` を `csv.DictReader` で読み `dest_page == 'HTMLチェックツール'` を抽出した全9行。DROP なし。出典はすべて `2e501ad:ja/development_tools/testing_framework/guide/development_guide/08_TestTools/03_HtmlCheckTool/index.rst`。

| mapping_id | 出典行 | ページ上の反映先 | 判定 |
|---|---|---|---|
| current-0367 | `:6-9` | リード文 | 消化。「目的、仕様、使用方法に関して記述する」は目次で足りるため落とした |
| current-0368 | `:12-16` | リード文、機能概要冒頭 | 消化。2つの目的（構文不正の防止・禁止タグの防止）をチェックの2種類に対応させた |
| current-0369 | `:19-65` | 機能概要冒頭、構文チェックの仕様 | 消化。脚注3件は本文へ繰り込み（`:30` はカスタマイズ節へのリンク、`:32` は相違点節、`:34-36` はW3Cリンク付きで使用方法冒頭へ）。`:61-63` のコメントアウト（JavaScriptコーディング規約への参照）は落とした。**`:24` と `:40-55` は実装と食い違うため書き換えた（後述）** |
| current-0370 | `:68-82` | HTML4.01との相違点 | 消化 |
| current-0371 | `:88-92` | 機能概要 > 前提事項 | 消化。`dest_section` の指定どおり機能概要配下に置いた（`testdata_converter.rst:57-58` と同じ配置）。ラベル `01_custom` は S-08 に無いため削除し、参照元は本ページ内の節リンクに置き換えた |
| current-0372 | `:95-139` | 使用を禁止するタグ・属性を変更する | 消化。設定ファイルのパスは出典の `test/resources/httprequesttest/html-check-config.csv` が現行レイアウトと合わないため、例をプロジェクト固有パスに差し替えた |
| current-0373 | `:142-160` | HTMLチェックの実行要否を切り替える | 消化。ラベル `customize_html_check` は S-08 に無いため `html_check_tool-switch` に置き換えた |
| current-0374 | `:163-226` | チェックの内容を差し替える | 消化 |
| current-0375 | `:229-238` | 指摘の内容を確認する | 消化。`:scale: 70` も引き継いだ |

## 実装で確認した事実

`nablarch-testing@e21bf67`。パスは `src/main/java/` からの相対。

| 記載内容 | 出典（file:line） |
|---|---|
| チェック対象は `isCheckHtml()` かつ ステータスコード500未満 かつ `Content-Type` が `[^/]*/html?.*` に合致 | `nablarch/test/core/http/HttpRequestTestSupport.java:78, 285-290` |
| HTMLダンプはUTF-8固定で読み込む | `nablarch/test/tool/htmlcheck/Html4HtmlChecker.java:18, 78-81` |
| 構文チェック→使用禁止チェックの順、構文エラー時は後者に進まない | `Html4HtmlChecker.java:56-69` |
| 最上位メッセージ `syntax check failed. file = [<パス>]`、指摘箇所は原因例外側 | `Html4HtmlChecker.java:91-99`、`HtmlSyntaxChecker.java:35-52` |
| `Parse error at line N, column M.  Encountered: ...`（スペース2個） | `parser/Parser.java` の `generateParseException` |
| `Lexical error at line N, column M.  Encountered: "c" (code), after : "..."` | `parser/TokenMgrError.java:107-113` |
| 終了タグは省略不可、`head`/`body`/`tbody` は要素ごと省略可、`<html>`〜`</html>` は必須 | `parser/Html4.jj:677`（`... (head())? (body() \| frameset())? "</html>"`）、`:2329`（`(thead() \| tfoot() \| tbody() \| tr())*`） |
| 文書型宣言は省略可、記述する場合は `PUBLIC` ＋公開識別子のみ | `parser/Html4.jj:47, 230` |
| XML宣言を文書型宣言の前に記述できる | `parser/Html4.jj:230`（`(xmlDecl())? (<DOCTYPE>)? html()`） |
| 大文字・小文字を区別しない | `parser/Html4.jj:6`（`IGNORE_CASE = true`） |
| boolean属性を使用できる | `parser/Html4.jj:136`（`attrName() ( "=" <STRING> )?`） |
| 属性値のクォートは省略不可、シングルクォート可 | `parser/Html4.jj:32-35` |
| HTMLコメント内の `--` が字句エラーになる | `parser/Html4.jj:27-29` |
| 設定ファイルの行は `split(",", -1)`、行数不正・タグ名空で `IllegalArgumentException`、メッセージに `line = [N]` | `nablarch/test/tool/htmlcheck/util/FileUtil.java:35, 65`、`HtmlForbiddenNodeConf.java:64-77` |
| 設定ファイルのタグ名・属性名は `trim().toLowerCase()` | `HtmlForbiddenNodeConf.java:92-105` |
| タグ禁止は属性集合が空のときだけ有効 | `HtmlForbiddenNodeConf.java:127-139` |
| 禁止タグを検出したノードは配下を走査しない | `HtmlForbiddenChecker.java:72-75`（`continue` により `:92` の再帰呼び出しに到達しない） |
| 使用禁止の指摘は1つのメッセージにまとめて送出 | `HtmlForbiddenChecker.java:38-47` |
| `checkHtml` の既定値は `true` | `nablarch/test/core/http/HttpTestConfiguration.java:101` |
| `setHtmlCheckerConfig` が `htmlChecker` を無条件に上書き | `HttpTestConfiguration.java:358-360` |
| 相対パスは実行ディレクトリ基準 | `util/FileUtil.java:97-99`（`new File(filePath)`） |
| デフォルト設定の設定ファイルの中身（`applet,`・`center,`・`font,` などのタグ禁止と `table,align` などの属性禁止） | `nablarch-example-web/src/test/resources/nablarch/test/http-request-test/html-check-config.csv`（66行） |

### 実測

`e21bf67` から `nablarch/test/tool/htmlcheck/` 配下21ファイルを scratchpad に取り出し、`javac` で単体ビルドして `Html4HtmlChecker#checkHtml` を直接実行した（リポジトリは汚していない）。

| 検証 | 結果 |
|---|---|
| `head`/`body`/`tbody` の省略 | いずれも OK（構文エラーにならない） |
| `</p>` の省略、`<html>` の省略 | いずれも `syntax check failed` |
| `<!DOCTYPE html>` / `<nav>` | いずれも `syntax check failed` |
| `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" ...>` / XML宣言付き | いずれも OK |
| `<input type=text>` / `<input type='text'>` | 前者 NG、後者 OK |
| 構文エラー時のメッセージ階層 | 最上位 `syntax check failed. file = [...]`、`Caused by` に `Parse error at line 1, column 46.  Encountered: <p` |
| 設定ファイルにBOM | 先頭行 `table,align` の設定だけが例外なく無効になる |
| 設定ファイルが ` TABLE , ALIGN ` | `table,align` として機能する |
| 空行・カンマ2個・タグ名空 | `each line must have exactly two elements....line = [2]` / 同 / `tag name (1st column) must not be empty....line = [1]` |
| 禁止タグ配下の違反 | `div,` を禁止すると配下の `table,align` の指摘が出ない |

## 出典から変えた点

`design.md` §8（出典と実装が食い違えば実装優先）および `:518-521`（出典に無い適用範囲・副作用の追記）に基づく。

1. **`:24`「HTML4.01で省略可能と規定されているタグについても、省略を許可しない」は成り立たない。** `head`・`body`・`tbody` は要素ごと省略できる（実測・`Html4.jj:677, 2329`）。省略できないのは開始タグを書いた要素の終了タグと `<html>`〜`</html>` であるため、その形に書き換えた。
2. **`:40-55`「HTMLに直接記述したJavaScriptに `-` が2つ以上連続すると失敗」は条件が広すぎる。** 実測では、コメントで囲まない `count--;` も `var message = "--";` も通る。失敗するのは `<!--` 〜 `-->` の中に `--` が現れた場合である（`Html4.jj:27-29`）。条件を限定して記述した。
3. **`:28` のクォート省略の例 `<table align="center">` を `<input type="text">` に差し替えた。** デフォルト設定の設定ファイルが `table,align` を禁止しているため（`html-check-config.csv:51`）、許可される例として示すとページ内で矛盾する。
4. **`:96` の設定ファイルパス `test/resources/httprequesttest/html-check-config.csv` を採らなかった。** 現行のデフォルト値は `src/test/resources/nablarch/test/http-request-test/html-check-config.csv`（`setup/request_unit_test/web.rst:70`）。XMLの例はデフォルト値と同じ値を書いても意味がないため、プロジェクト固有のパスを例にした。
5. **出典に無い実装事実を4件追記した。** `<!DOCTYPE html>` が指摘の対象になること、タグ禁止と属性禁止を併記するとタグ禁止が無効になること、禁止タグの配下が走査されないこと、設定ファイルのBOMで先頭行が無効になること。いずれも黙って壊れる（例外もエラーも出ない）ため、読者が原因にたどり着けない。
6. **HTML5で記述しているプロジェクトでは使用できない旨を追記した。** Nablarchのサンプルアプリケーション自身が `checkHtml` を `false` にしている（`nablarch-example-web/src/test/resources/unit-test.xml:49-51`、コメントに「HTML5の仕様で記述しているため既存のHTMLチェッカを外す」）。
7. **`:35` のW3Cリンク（`https://www.w3.org/TR/html401/`）を使用方法の冒頭に復活させた。**

## 4観点レビュー

| 観点 | 指摘件数 |
|---|---|
| QA | M2 / S4 / N5 |
| 設計 | M4 / S6 / N5 |
| クラフト | M3 / S13 / N6 |
| 検証 | 突き合わせ24件のうち 一致20 / 不一致3 / 未確認1 |

### 是正した指摘

| 指摘 | 対応 |
|---|---|
| 「省略可能と規定されているタグも省略不可」が誤り（QA S2 / 検証） | 上記「出典から変えた点」1 |
| 構文エラーの最上位メッセージを表が落としている（QA S1 / 設計 / 検証） | メッセージの表を最上位と原因例外の2段に分けた |
| 「文字コードがUTF-8であること」を例外発生条件に挙げているのが誤り（QA M2 / 検証） | 削除。代わりにBOMの important を追加 |
| HTML5プロジェクトで全リクエスト単体テストが落ちる（QA M1） | 構文チェックの仕様に important を追加 |
| 禁止タグ配下が走査されない（QA S3） | important を追加 |
| クォート省略の例がデフォルト設定と矛盾（設計 / クラフト） | `<input type="text">` に差し替え |
| 前提の記述が `dest_section` と違う位置にある（設計） | 機能概要配下の L3「前提事項」に移した |
| ページの適用範囲がウェブアプリケーションに限られる（設計 / クラフト） | リード文・機能概要・前提事項・使用方法冒頭を「リクエスト単体テスト（ウェブアプリケーション）」に統一 |
| `テストケース` は用語集で0件が求められる（クラフト、`glossary.md:556`） | 2箇所とも `テストメソッド` に置き換えた |
| `htmlCheckerConfig` の例がデフォルト値と同じ（クラフト） | プロジェクト固有パスに変更 |
| 「クォーテーション」「デフォルトの設定」（クラフト） | 「クォート」「デフォルト設定」に統一 |
| W3Cリンクの欠落（QA N2） | 復活 |
| 設定ファイルのタグ名・属性名の正規化が未記載（QA N3） | 1文追記 |
| 設定ファイルの読み込みタイミングと行番号出力（QA N4） | 1文ずつ追記 |
| `:scale: 70` の欠落（QA N1） | 復活。ビルドで新規warningが出ないことを確認 |
| 「指摘」が定義なしで多用されている（クラフト） | 機能概要で「その内容を指摘として…」と初出を定義 |

### 採らなかった指摘

| 指摘 | 理由 |
|---|---|
| HTMLダンプの文字コードがUTF-8以外だと字句エラーになる（QA S4） | **実測で再現しなかった。** Shift_JISで保存した日本語入りHTMLをチェックしても OK になる。UTF-8デコーダが不正バイトをU+FFFDに置換し、置換後の文字はテキスト内容として文法上受理されるため。書き出し側が `res.getCharset()` を使うこと（`nablarch/fw/web/HttpServer.java:425, 431-432`）自体は事実だが、そこから字句エラーが導かれるという主張は成り立たない |
| 画像が旧バージョンのスタックトレース（パッケージ名 `nablarch.tool.htmlcheck`）である旨を断る（QA N1） | 画像の要点（最上位行にファイル名、`Caused by` に指摘箇所）は現行と一致しており、本文でメッセージ形式を正確に示したため実害がない。出典の画像をそのまま使う |
| `setup/request_unit_test/web.rst:154-155` のXML例が旧パスのまま（QA N5） | 承認済みページの修正は `#27-06` の範囲外。**`decide` 2 として残す** |
| L3見出しの下線を50に揃える（クラフト） | G8（下線がタイトル表示幅以上）は満たしている。承認済みページも `testdata_converter.rst` は49、`master_data_tool.rst`・`request_data_tool.rst` は50で揃っていない。導入を持たない `testdata_converter.rst` に合わせて49のままとする |
| `span` は HTML4.01 でも空を許すため相違点の例として不適（検証） | 出典 `:76-77` がそのまま挙げている例であり、実装も両方を許容する。出典に忠実な選択として残す |

## ゲート

| ゲート | 結果 |
|---|---|
| G1 `git status --porcelain` | 2件（`M ja/.../tools/html_check_tool.rst`、`R ja/.../guide/.../03_HtmlCheckTool/_image/how-to-trace-html.png -> ja/.../tools/images/html_check_tool/how-to-trace-html.png`） |
| G2 禁止ファイル差分 | 0 |
| G3 `sphinx.mo` | 差分なし（ビルド後に `git checkout` 済み） |
| G4 `verify_mapping.py` | exit 0 |
| G5 Dockerフルビルド | `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108`（`how_to_set_token_in_request_unit_test` 未定義、`#27-20` で解消予定）のみ |
| G6 禁止語 | 0件（`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`テストケース`）。です／ます 0件、`note`／`warning` 0件 |
| G7 先頭ラベル | `html_check_tool`（`style.md:392` と一致） |
| G8 見出し下線 | 全10件で下線長 ≧ タイトル表示幅 |
| G9 `:ref:` | 5件。`request_unit_test_setting_web` ×3（`web.rst:1`）、`html_check_tool-switch`・`html_check_tool-replace`（本ページ内）。いずれも実在。被参照側は `web.rst:66` の `:ref:`HTMLチェックツール <html_check_tool>`` |
| G10 出典行 | 全9行を消化（上表） |
| G11 REFERENCE | 該当行なし |
| G12 二重掲載 | `HTMLチェック` を含むページは本ページと `web.rst` のみ。`web.rst` は設定項目一覧としての記載で、本ページから `:ref:` している |
| G13 画像 | `images/html_check_tool/how-to-trace-html.png` 実在。`guide/development_guide/08_TestTools/` は空ディレクトリごと削除済み |

## 判断待ち（`decide`）

1. **`checkHtml`・`htmlChecker`・`htmlCheckerConfig` の説明を、本ページと `web.rst` のどちらに置くか。** `design.md:360` は「第2部・第3部からツールへは `:ref:`（ツール利用者が1箇所で完結できることを優先）」とし、`design.md:522` は「承認済みページが同じ事実を持つ場合は `:ref:`」とする。この3プロパティは両方に該当する。本ページは、ツール利用者が本ページだけで設定を変更できるよう値と例を載せ、「どちらか一方が必要」という設定全体の制約だけを `web.rst` へ `:ref:` する形にした。逆に本ページ側を全面的に `:ref:` にする選択もありうる。
2. **`setup/request_unit_test/web.rst:154-155` のXML例が旧レイアウトのパス `test/resources/httprequesttest/html-check-config.csv` のままである。** 同ページ `:70` が書くデフォルト値（`src/test/resources/nablarch/test/http-request-test/html-check-config.csv`）と食い違う。承認済みページのため本タスクでは触れていない。
