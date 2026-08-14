# page-request_unit_test_web

対象: `ja/development_tools/testing_framework/implementation/request_unit_test/web.rst`（第3部）
タスク: `#27-20`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-large-pages.md` §3
姉妹ページ: `implementation/request_unit_test/rest.rst`（承認済み・215行）、`setup/request_unit_test/web.rst`（承認済み・229行、第2部）

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |
| `nablarch-document`（旧解説書） | `2e501ad` |

## 2. 出典

`mapping.csv` を `csv.DictReader` で全行走査した実測。`dest_page='リクエスト単体テスト（ウェブアプリケーション）'` は **33件・914行**。`disposition` は MOVE 26／MERGE 7 で、DROP・REFERENCE は0件。`dest_section` は 使用方法 28／機能概要 5。

| `src_file` | 件数 | 行数 |
| --- | ---: | ---: |
| `05_UnitTestGuide/02_RequestUnitTest/index.rst` | 13 | 461 |
| `06_TestFWGuide/02_RequestUnitTest.rst` | 9 | 260 |
| `05_UnitTestGuide/02_RequestUnitTest/fileupload.rst` | 3 | 90 |
| `06_TestFWGuide/03_Tips.rst` | 2 | 39 |
| `.rn/20260724-ntf-yaml-support/input/ntf-doc-terms.md` | 2 | 31 |
| `05_UnitTestGuide/02_RequestUnitTest/mail.rst` | 2 | 18 |
| `05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst` | 2 | 15 |

`src_file` の distinct は **7**（接頭辞 `ja/development_tools/testing_framework/guide/development_guide/` を省略）。

**33件すべてを本文に反映した。意図して落とした出典行は0件である。**

**個別指示 §3-2 の出典件数表（`ntf-doc-27-large-pages.md:94-102`）は実測と合わない。** 表は7出典・31件・861行、見出し文は「出典は8つに散っている」だが、`mapping.csv` の実測は7出典・33件・914行である。差は `index.rst`（表 12件/455行 → 実測 13件/461行）と `02_RequestUnitTest.rst`（表 8件/213行 → 実測 9件/260行）。**母集合は `mapping.csv` を採った。**

## 3. 画像

`git mv` で3枚移設した。移動元は `guide/` 配下に残っていない（`ls` で実測）。

| 移動先 | 移動元 | 出典 |
| --- | --- | --- |
| `implementation/request_unit_test/images/web/request_unit_test_structure.png` | `06_TestFWGuide/_images/` | `02_RequestUnitTest.rst:19` |
| `implementation/request_unit_test/images/web/htmlDumpDir.png` | `06_TestFWGuide/_images/` | `02_RequestUnitTest.rst:298` |
| `implementation/request_unit_test/images/web/mail_overview.jpg` | `05_UnitTestGuide/02_RequestUnitTest/_image/` | `mail.rst:18` |

**ファイル名は原名のまま変えない。** 出典への追跡性を保つため。既存の `setup/request_unit_test/images/web/`（`vmoptions.png`・`installed_jre.png` など）も原名を保っている。

**落とした画像3枚。**

- `05_UnitTestGuide/02_RequestUnitTest/_image/htmlDumpDir.png`（`index.rst:724`）— `06_TestFWGuide/_images/htmlDumpDir.png` と**バイト同一**（md5 `c86af2b2e100bb9707ccaf00458612fd`、実測）。同じ画像を2枚持たない。
- `assert_entity.png`（`index.rst:523`）・`expected_download_csv.png`（`index.rst:672`）— どちらもExcelのスクリーンショット。テストデータの記述例は `implementation/testdata_examples.rst` に文字列で載っており、Excel形式に固有のスクリーンショットを第3部に持ち込まない（`#27-19` と同じ判断）。

## 4. 出典と実装の食い違い（実装を優先した箇所）

親指示 `ntf-doc-weekend-queue.md:69`「出典と実装が食い違う場合は実装を優先する」による。**いずれも旧解説書の記述誤りであり、本体の不具合ではないため `decide` には上げていない。** 根拠は `nablarch-testing` `e21bf67`。

1. **クラス名の誤記。** `02_RequestUnitTest.rst:49-50` は `AbstractHttpReqestTestSupport`・`BasicHttpReqestTestSupport`（`Reqest`）と書いている。実在するのは `AbstractHttpRequestTestTemplate`（`src/main/java/nablarch/test/core/http/AbstractHttpRequestTestTemplate.java`）と `BasicHttpRequestTestTemplate`（同 `BasicHttpRequestTestTemplate.java:15`）。実在名で書いた。
2. **システムリポジトリの再初期化は無条件ではない。** `02_RequestUnitTest.rst:232-245` は `execute` が常に再初期化・復元を行うように書いているが、実装は `HttpRequestTestSupport.java:268-272` の `if (StringUtil.hasValue(xmlComponentFile))` のとおり `xmlComponentFile` が指定されたときだけである。**この事実は第2部 `setup/request_unit_test/web.rst:94` が既に正しく書いているため、本ページには書かず `:ref:` で送った**（§5 D-1）。
3. **`03_Tips.rst:642` の実装例はコンパイルできない。** `extends HttpRequestTestSupport` と宣言したうえで `execute(String, Advice)` を呼んでいるが、このオーバーロードは `AbstractHttpRequestTestTemplate` にしかない（`HttpRequestTestSupport` を全文走査して不在を確認）。例からクラス宣言を外し、テストメソッドの断片にした。
4. **`getParam` の戻り値は `String[]`。** `index.rst:605` は `assertEquals("", getParam(request, "resetparameter"));` と `String` と比較しているが、`HttpRequestTestSupport.java:1394` の戻り値は `String[]`。`[0]` を付けた。
5. **`getTestCaseName()` が返すのは説明そのものではない。** `TestCaseInfo.java:406-409` は `{読み込み単位の名前}_Shot{番号}_{説明}` を連結して返す。表の記述をこの形に改めた。
6. **HTMLダンプのファイル名。** `index.rst:724` 付近と `02_RequestUnitTest.rst:288-290` は「テストケース説明と同名」と書くが、実際は `getTestCaseName()` がそのままファイル名になる（`HttpRequestTestSupport.java:260-261`、拡張子の既定は `HttpTestConfiguration.java:55` の `html`）。`読み込み単位の名前_Shot番号_説明.html` と書いた。
7. **ダウンロードファイルのファイル名。** `index.rst:669-670` は「シート名＋"_"＋テストケース名＋"_"＋ダウンロードされたファイル名」と書くが、「テストケース名」が既に `シート名_Shot番号_説明` である。実装は `HttpServer.java:496-499` のとおり、HTMLダンプのファイルパスから拡張子を落として `_` とダウンロードファイル名を連結する。`読み込み単位の名前_Shot番号_説明_ダウンロードされたファイル名` と書いた。
8. **トークン設定の位置。** `index.rst:349-350` はスーパクラスの処理フローでトークン設定を `beforeExecute` の**後**に置いているが、実装は `AbstractHttpRequestTestTemplate.java:257-262` のとおり**先**である。実装の順で書いた。

## 5. 判断

- **D-1 `xmlComponentFile` によるシステムリポジトリ再初期化の説明を本ページに書かない。** 個別指示 §3-3（`ntf-doc-27-large-pages.md:112`）「設定の話は第2部にあり、このページには書かない。設定に触れる必要があれば `:ref:` で送る」による。第2部 `setup/request_unit_test/web.rst:94` が同じ3つの事実（送信直前に再初期化される／通常は不要／クラス単体テストと設定を変える場合にのみ設定する）を既に書いている。出典 `current-0207`（`02_RequestUnitTest.rst:210-247`）のうち再初期化の部分は、本ページでは `:ref:` に置き換えた。同じ出典の「実行」の部分（`:208-227`、`HttpResponse execute(String caseName, HttpRequest, ExecutionContext)`）は本ページに書いた。
- **D-2 出典に無い実装上の事実を3件書き足した。** 親指示 `ntf-doc-weekend-queue.md:68` による。(a) `execute(boolean shouldSetUpDb)`・`execute(String, boolean)` の2オーバーロードと `setUpDb` の投入を省略できること（`AbstractHttpRequestTestTemplate.java:138-151`・`:199-201`）。旧解説書は `index.rst:400-404` で `execute()` と `execute(Advice)` の2つしか挙げていない。(b) `createHttpRequest(String, String, Map)` の3引数版と、2引数版が `POST` を設定すること（`HttpRequestTestSupport.java:918`・`:938-940`）。(c) ダンプディレクトリが既に存在する場合の `_bk` バックアップ（`HttpRequestTestSupport.java:838-852`）。(c) は出典 `02_RequestUnitTest.rst:295` にもあるが、第2部 `setup/request_unit_test/web.rst:56-58` の `backup` 項目は `_bk` という名前に触れていないため、名前は本ページに書いた。
- **D-3 主なクラスとリソースの表は `list-table` の `:widths: 30,45,25` とした。** 承認済みの姉妹ページ `implementation/request_unit_test/rest.rst:21-23` が同じ3列（名称／役割／作成単位）で同じ値を使っている。`style.md` に `:widths:` の算出基準は無い（`#24` の申し送り）ため、個別指示 §3-2 の「既存ページの表と同じ流儀に揃える」に従い、この値をそのまま採った。他の3表は列数と内容量に応じ `20,25,55`・`40,60`・`25,75` とした。
- **D-4 `current-0089`（255行、最大の塊）は表にせず、L4 4本に分けて記述例を並べた。** 出典は「リクエストスコープの値の確認」の型ごとの5例で、それぞれコード例を伴う。表に畳むと例が失われる。型と使用メソッドの対応だけを `list-table`（`:widths: 25,75`）にし、コード例は本文に置いた。
- **D-5 親ファイル `02_RequestUnitTest.rst`（構造）と子 `02_RequestUnitTest/index.rst`（実装手順）の重なりは、実装手順の側を採った。** 個別指示 §3-2 による。構造の説明（`current-0201` の主なクラスの表、`current-0206` の委譲の説明）は機能概要と「ハンドラが行う処理をテストクラスから省く」に1回だけ置いた。
- **D-6 `entity_unit_test` へは節アンカーではなくページ先頭ラベルで送った。** 出典 `index.rst:522` は `:ref:`entityUnitTest_SetterGetterCase`` を指しているが、この節ラベルは削除済みで、飛び先ページ `implementation/class_unit_test/entity.rst` は `#27-21` で作成する。粒度が粗くなることを承知でページ先頭ラベルにした（`#27-19` の同種判断と同じ）。
- **D-7 `assertListMapEquals` は `Assertion.` で修飾して書いた。** `nablarch.test.Assertion:128` の static メソッドであり、`HttpRequestTestSupport`（`:72` で `TestEventDispatcher` を継承）は持たない。同じ節に並ぶ `assertSqlResultSetEquals`・`assertEntity`・`assertObjectPropertyEquals` は継承メソッドのため、修飾の有無で区別が付くようにした。
- **D-8 ラベル `how_to_set_token_in_request_unit_test` は改名せずそのまま定義した。** 個別指示 §3-1 の `style.md` S-08 例外規定による。`ja/`（`_build/` を除く）での定義は1件のみ。参照元は `application_framework/libraries/db_double_submit.rst:106` の1件。**この定義によりフルビルドの警告が0件になった**（§6）。
- **D-9 ページ内の節ラベルを2件追加した。** `request_unit_test_web-upload_file`・`request_unit_test_web-mail`。`style.md:304-305` の `<ページ先頭ラベル>-<英語スネークケース>` 形式に従う。機能概要（`:61`）からファイルアップロードとメール送信の各節へ飛べるようにするため。`ja/` 配下で衝突0件。
- **D-10 L4見出しを18本使った。** `style.md:193` は L4 を「用例が薄いページでのみ使う」としており、承認済みの `rest.rst` は2本である。出典914行を「機能概要＋使用方法5節」の枠（`design.md:281-296`）に収める以上、L3配下の細分は避けられないと判断した（→ 7節 `decide-1`）。

## 6. ゲート

| ゲート | 結果 | 根拠 |
| --- | --- | --- |
| G1 `git status --porcelain` 全件 | PASS | `M web.rst`・`R` 画像3件・`?? reviews/page-request_unit_test_web.md`・`M checks/task-27.md`・`M steering.md` のみ |
| G2 禁止ファイル差分0 | PASS | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を指定した `git status --porcelain` が0行 |
| G3 `sphinx.mo` 未コミット | PASS | `git status --porcelain` に出現なし |
| G4 `verify_mapping.py` | PASS | `OK: no errors`（exit 0） |
| G5 フルビルド | PASS | `build succeeded.`。**警告0件**（`-E` 付きフルビルド、実測） |
| G6 禁止語 | PASS | `不具合`・`バグ`・`将来`・`修正され` が0件 |
| G7 ラベル | PASS | `request_unit_test_web` が `style.md:374` と一致。`ja/` 配下（`_build/` 除く）で重複定義0件 |
| G8 下線幅 | PASS | L1 50（タイトル表示幅46）／L2 `-` 50 × 2／L3 `~` 49 × 5／L4 `^` 49 × 18。すべて下線幅 ≧ 表示幅。`rest.rst` の実測値 50/50/49/49 と一致 |
| G9 `:ref:` 飛び先とリンクテキスト | PASS | 18種・のべ22箇所すべて飛び先が実在し、リンク文字列が飛び先見出しと文字列一致 |
| G10 出典の反映 | PASS | 33件すべてを反映。意図的dropは0件（§2） |
| G11 REFERENCE行を節にしない | PASS（該当なし） | 本ページ33件に `disposition=REFERENCE` は0件 |
| G12 二重掲載なし | PASS | 本ページ33件と他ページ全行の `src_file`＋行範囲の重なりを総当たりで判定し0件 |
| G13 画像 `git mv` | PASS | `.. image::` 3件の参照先が実在。移動元3パスは `guide/` 配下に残っていない |
| L1 全 `mapping_id` の反映または意図的drop | PASS | G10 と同じ |
| L2 他ページ割当の出典を書いていない | PASS | `index.rst:85-333`・`02_RequestUnitTest.rst:93-103`／`:306-552`・`fileupload.rst:16-28`・`double_transmission.rst:27-39`・`03_Tips.rst:665-676` の内容は書いていない（→ 7節 `decide-2`） |
| L3 「〜したい」形式の見出し0件 | PASS | 見出し23件のうち「したい」で終わるものは0件。本文中の3箇所は地の文 |
| L4 `拡張例` の見出しなし | PASS | `拡張例` が0件 |
| L5 L3見出しがすべて「〜する」形式 | PASS | L3 5件・L4 18件すべて動詞終止形の肯定形 |
| L6 `how_to_set_token_in_request_unit_test` | PASS | `web.rst:245` で定義。`ja/`（`_build/` 除く）で1件のみ。**フルビルドの警告が0件になった**（従前の唯一の警告 `db_double_submit.rst:108` が解消） |
| L7 `implementation/index.rst` の toctree | PASS | 未変更（`git status` に出現しない）。並びは `design.md:837-886` と一致 |
| S-01 である調 | PASS | です・ます・ください・下さい が0件 |
| S-02 セクション構成 | PASS | リード文（目次直後・最初のL2より前）→ 機能概要 → 使用方法 |
| S-03 見出し | PASS | 禁止語（概要・補足・注意事項・その他）0件。同一ページ内の重複0件 |
| S-04 下線記号 | PASS | L1 `=`／L2 `-`／L3 `~`／L4 `^` |
| S-05 code-block | PASS | 18件すべて `java` を指定。内容はディレクティブ行から相対2字下げ |
| S-06 important / tip | PASS | `tip` 10件はいずれも補足情報。`important` は0件（`DbAccessTestSupport` の非委譲メソッドは `rest.rst:95-102` の流儀に合わせ地の文＋箇条書きにした） |
| S-07 表 | PASS | `list-table` 4件、すべて `:widths:` 指定あり。grid/simple table は0件 |
| S-08 ラベル | PASS | ページ先頭ラベル1件（G7）、節ラベル3件。うち `how_to_set_token_in_request_unit_test` は S-08 例外（D-8）、残る2件は `<ページ先頭ラベル>-<英語>` 形式（D-9） |
| S-09 `.. contents::` | PASS | ラベル→タイトル→`.. contents:: 目次` / `:depth: 3` / `:local:` の順 |
| S-10 Excel／YAML書き分け | PASS | 形式に依存する記述を置いていない。`LIST_MAP` の期待値は「キーにプロパティ名、値に…」と行番号に踏み込まない書き方にした（§7 と `testdata_notation.rst:628` の Excel 専用記述との矛盾を避けるため） |
| S-11 L4を持つL3の導入文 | PASS | L4を持つL3 4件すべてに、配下のL4の個数と内容を述べた導入文がある（`:70` 3件・`:142` 5件・`:290` 2件・`:341` 4+2件） |
| 用語置換 | PASS | `テストケース`・`DI設定ファイル`・`propertiesファイル`・`プロパティファイル`・`テストソースコード`・`事前準備データ`・`想定結果`・`想定値` が0件 |

## 7. 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施した。**必須指摘は24件（QA 7・設計 4・クラフト 13。うち `LIST_MAP` の行番号は QA と設計で重複）。すべて本文に反映した。** 検証観点の FAIL 2件（G10・L1）は本レビュー記録の未作成が原因で、本記録の作成により解消した。任意指摘のうち17件を採用、残りは `decide` に上げるか、根拠を確かめて不採用とした。

**本文に反映した主な指摘**

- API・ファイル名の実装との食い違い6件（§4 の 5〜8 を含む）。
- `xmlComponentFile` の tip 削除（D-1）。
- `LIST_MAP` の期待値の説明から行番号を外した（`testdata_notation.rst:628` は「1行目に `LIST_MAP=`＋ID、2行目をキー、3行目以降を値」で、当初の記述は1行ずれていた。加えて行番号はExcel固有で `style.md` S-10 に反する）。
- 見出し「ハンドラが行う処理を書かない」を「ハンドラが行う処理をテストクラスから省く」に変更（否定形は `style.md:129-130` S-03 の「動詞終止形の『〜する』」に合わない。新解説書の全ページを走査して否定形の見出しはこの1件だけだった）。
- 「テスト結果を確認する」の導入文のねじれを解消（自動確認8項目にカラム名を添え、`afterExecute` に書く4つとテストコードを書かない2つに分けて予告）。
- 「テストショット」「読み込み単位」の初出に `:ref:` を追加。「テストデータの記載例」への導線を追加。
- 「テンプレート」と「スーパクラス」の語の揺れを「スーパクラス」に統一。
- `JUnit 5` 用拡張機能への tip を追加（`component.rst:145` と同文）。
- コード例の欠落した閉じ括弧、地の文を挟まない連続 `code-block`、`getListMap` の読み込み単位名の不一致、変数名 `isTokenValid`／カラム名 `isValidToken` の食い違いを修正。

**不採用**

- **`entity_unit_test` への `:ref:` を、期待値の書式の直接記述に置き換える案**（クラフト観点）。飛び先が現在4行のスタブであることが理由だが、`#27-21` で作成する。出典 `index.rst:522` の構造（エンティティ単体テストの書式を参照する）を保つほうが忠実である（D-6）。
- **`${attach:ファイルパス}` の記法自体を書かない案**（QA観点、割当外の `fileupload.rst:16-28` の内容であるため）。記法名を出さずに「アップロードファイルを指定する」とだけ書くと、割当内の `:31-60`・`:63-112` の具体例（`${attach:test/resources/images/picture.png}` など）が宙に浮く。記法名の提示に留め、詳細は `testdata_notation-special_notation` へ送った。

## 8. 判断待ち

- **`decide-1`（推奨）** **L4見出しの使用量が `style.md:193` の条文と噛み合っていない。** 条文は L4 を「用例が薄いページでのみ使う」とするが、本ページは18本使っている（承認済み `rest.rst` は2本、`component.rst` は6本）。出典914行を `design.md:281-296` の固定の枠（機能概要＋使用方法5節）に収める以上、L3配下の細分は避けられない。**`#27-19` の `decide-1`（同条文が判定基準として機能していない）と同一事象だが、本ページは件数が一桁多い分、条文の見直しの必要性がより明確である。** 条文を「L3が3つ以上の独立した操作に分かれる場合に使う」のような判定可能な形に改めるか、分量の多いページを別扱いにするかの判断が要る。
- **`decide-2`（推奨）** **`xmlComponentFile` という設定項目名は、割当外と明示された `02_RequestUnitTest.rst:306-552`（設定値一覧）の語である。** 本ページでは D-1 のとおり説明を書かず `:ref:` で送ったため語自体は本文から消えたが、「設定の話は第2部」という線引きは、設定項目名に言及すること自体を禁じているのか、説明を書くことだけを禁じているのかが個別指示 §3-3 からは読み取れない。以後のページで同じ判断が要る。
- **`decide-3`（推奨）** **`db_double_submit.rst:106` のリンク文字列が飛び先の見出しと一致しない。** 参照は `:ref:`テスティングフレームワークのトークン発行<how_to_set_token_in_request_unit_test>`` で、飛び先の見出しは「二重サブミット防止機能のトークンを設定する」である。ゲート G9 は本ページ本文中の `:ref:` を対象とするため FAIL ではないが、FW解説書側を直すかどうかの判断が要る。**FW解説書は本作業の対象外のため触っていない。**
- **`decide-4`（推奨）** **`implementation/testdata_notation.rst:392` の `description` カラムの説明が、HTMLダンプのファイル名の組み立てを正確に述べていない。** 「出力される HTML ダンプのファイル名にも使用される」とあり誤りではないが、実際のファイル名は `読み込み単位の名前_Shot番号_説明.html` である（§4 の6）。承認済みページのため触っていない。揃えるかどうかの判断が要る。
- **`decide-5`（参考）** **`guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/_image/` に36ファイルが残っている。** `guide/` 配下に `.rst` は既に0件で、これらは参照されていない。本ページの `git mv` の移動元（`06_TestFWGuide/_images/`）とは別ディレクトリのため G13 には影響しない。解説書全体の後片付けとして別途扱う対象と思われる。
- **`decide-6`（参考）** **個別指示 §3-2 の出典件数表が `mapping.csv` の実測と合わない**（§2）。同種のずれが他のページの個別指示にもある可能性がある。

## 9. `#27-21` への申し送り

`#27-19` からの申し送りに次を加える。

- **本ページから `entity_unit_test` へ「setter・getterのテストと同じ書式で期待値を記述する。ただしsetterの欄は不要」という前提で送っている**（`web.rst` の「リクエストスコープの値を確認する」）。`#27-21` でエンティティ単体テストのページを書く際、この書式（setter欄・getter欄を持つ `LIST_MAP`）の説明が読者に届く形になっていることを確認する。旧解説書の対応節ラベルは `entityUnitTest_SetterGetterCase` である。
