# task-18 Completion Check

`#18` デフォルト値の基準を実効値に統一し、`design.md` に2件を規定する。作業指示は
`ntf-doc-18-default-value-basis.md`（2026-08-13 受領）。**ページを作らないタスク。**

基準コミット（マージ前 HEAD）: `6274d6d`。`ja/` の変更は本タスクで初めて入る。

## 0. 参照した実物と、自分で確認した取得元

作業指示の「参照する実物」の表は、**すべて自分で取得して確かめた**。同じ調査をやり直さなくてよいとの
指示だったが、`file:line` を記録に引き写す以上、引き写す値は自分が開いたものに限る必要があるため。

| 参照点 | 実際に確認した取得元 | 備考 |
|---|---|---|
| `nablarch-testing-default-configuration` 6u3 | `~/.m2/repository/com/nablarch/configuration/nablarch-testing-default-configuration/6u3/nablarch-testing-default-configuration-6u3.jar` を展開 | ローカル Maven リポジトリに存在。Maven Central と同一座標 |
| `nablarch-web-archetype` 6u3 | Maven Central から取得（`https://repo1.maven.org/maven2/com/nablarch/archetype/nablarch-web-archetype/6u3/nablarch-web-archetype-6u3.jar`、2,642,043 bytes） | ローカルに無かったため取得 |
| `nablarch-jaxrs-archetype` 6u3 | 同上（`nablarch-jaxrs-archetype-6u3.jar`、2,599,239 bytes） | 同上 |
| `nablarch/nablarch-testing` `e21bf67` | ローカルクローン `/home/tie303177/work/nablarch/nablarch-testing`。`git show e21bf67:<path>` で取得 | クローンの HEAD は `fdf55d4` だが、`git diff e21bf67 HEAD -- .../HttpTestConfiguration.java` が空であり、参照した内容は `e21bf67` と同一 |

**`nablarch-core-repository`（`6a28491`）は自分では開いていない。** ローカルにクローンが無く、
プロパティ単位マージの `XmlComponentDefinitionLoader.java:214`・`:238-273`・`:283-328`・`:119` は
**作業指示の記述をそのまま引いた（未確認）**。`design.md` §8 の追記では、この点について行番号を書かず
クラス名と既定ポリシー名のみを記した。

### 0-1. デフォルト設定が読み込まれることの確認（実測）

アーキタイプの `archetype-resources/src/test/resources/unit-test.xml` を jar から直接展開して確認した。

| アーキタイプ | 行 | 記述 |
|---|---|---|
| `nablarch-web-archetype` 6u3 | `:14` | `<import file="nablarch/test/test-data.xml"/>` |
| `nablarch-web-archetype` 6u3 | `:16` | `<import file="nablarch/test/http-request-test.xml"/>` |
| `nablarch-jaxrs-archetype` 6u3 | `:14` | `<import file="nablarch/test/test-data.xml"/>` |
| `nablarch-jaxrs-archetype` 6u3 | `:16` | `<import file="nablarch/test/rest-request-test.xml"/>` |

あわせて、ウェブアーキタイプの `unit-test.xml` 末尾に
`<component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty12"/>` が
実在することを確認した。`design.md` §8 に追記した 5-2（出典が欠いている実装上必須の設定）の裏づけになる。

---

## ゲート1 — `web.rst` の設定項目表 全19行の照合（全件表）

母集合は `list-table`（変更前 `:19`〜`:82`）から機械抽出した。`^  \* - ` の行数は **20**（ヘッダ1行＋
設定項目19行）。ホワイトリストは使っていない。

「実効値」は次の規則で判定した。デフォルト設定（`nablarch/test/http-request-test.xml`。以下 `xml`）が
そのプロパティを設定していれば、`nablarch/test/http-request-test/http-request-test.config`（以下
`config`）の値を解決したもの。設定していなければ、コンポーネントは生成されるだけなので
`HttpTestConfiguration.java`（`e21bf67`）のフィールド初期値がそのまま実効値になる。

| # | 行 | 設定項目 | 現在の記載 | デフォルト設定の実効値 | 判定 | 実効値の出典 |
|---|---|---|---|---|---|---|
| 1 | `:26` | `htmlDumpDir` | `./tmp/html_dump` | `./tmp/html_dump` | 一致 | `xml` に記述なし → フィールド初期値 `HttpTestConfiguration.java:24` |
| 2 | `:29` | `webBaseDir` | `../main/web` | `src/main/webapp` | **不一致** | `xml:15` → `config:1` |
| 3 | `:32` | `xmlComponentFile` | 該当なし | 該当なし（`null`） | 一致 | `xml` に記述なし → フィールド初期値 `:40`（`null`） |
| 4 | `:35` | `userIdSessionKey` | `user.id` | `user.id` | 一致 | `xml` に記述なし → `:45` |
| 5 | `:38` | `exceptionRequestVarKey` | `nablarch_application_error` | `nablarch_application_error` | 一致 | `xml` に記述なし → `:50` が `ExecutionContext.THROWN_APPLICATION_EXCEPTION_KEY`。同定数は `ExecutionContext.java:422` で `FW_PREFIX + "application_error"`、`FW_PREFIX` は `:34` で `nablarch_` |
| 6 | `:41` | `dumpFileExtension` | `html` | `html` | 一致 | `xml` に記述なし → `:55` |
| 7 | `:44` | `httpHeader` | `Content-Type`＝`application/x-www-form-urlencoded`、`Accept-Language`＝`ja JP` | 同左 | 一致 | `xml` に記述なし → `:123-128` の初期化ブロック |
| 8 | `:47` | `sessionInfo` | 該当なし | `commonHeaderLoginUserName`＝`リクエスト単体テストユーザ`、`commonHeaderLoginDate`＝`20100914` | **不一致** | `xml:19-25` → `config:3-4` |
| 9 | `:50` | `htmlResourcesExtensionList` | `css`・`js`・`jpg`（3件） | `css`・`jpg`・`js`・`less`・`png`・`template`・`woff`・`eot`・`svg`・`ttf`（10件） | **不一致** | `xml:36-49`（リテラル。`config` 経由でない） |
| 10 | `:53` | `jsTestResourceDir` | `../test/web` | `src/test/webapp` | **不一致** | `xml:16` → `config:2` |
| 11 | `:56` | `backup` | `true` | `true` | 一致 | `xml:53` → `config:8` が `true`。値は同じ |
| 12 | `:59` | `htmlResourcesCharset` | `UTF-8` | `UTF-8` | 一致 | `xml:54` → `config:9` が `UTF-8`。値は同じ |
| 13 | `:62` | `checkHtml` | `true` | `true` | 一致 | `xml:33` → `config:6` が `true`。値は同じ |
| 14 | `:65` | `htmlChecker` | 該当なし | `htmlCheckerConfig` の設定に伴って設定される `Html4HtmlChecker` | **不一致** | `xml` は `htmlChecker` を直接設定しない。`xml:29-30` の `htmlCheckerConfig` 設定により `HttpTestConfiguration.java:358-360` の `setHtmlCheckerConfig` が `this.htmlChecker = new Html4HtmlChecker(htmlCheckerConfig)` を実行する |
| 15 | `:68` | `htmlCheckerConfig` | 該当なし | `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` | **不一致** | `xml:29-30` → `config:5` |
| 16 | `:71` | `ignoreHtmlResourceDirectory` | 該当なし | `.svn` | **不一致** | `xml:59-62`（リテラル） |
| 17 | `:74` | `tempDirectory` | 該当なし（内蔵サーバ（Jetty）のデフォルト動作に従う） | `target/tmp` | **不一致** | `xml:65` → `config:11` |
| 18 | `:77` | `uploadTmpDirectory` | `./tmp` | `./tmp` | 一致 | `xml` に記述なし → `:75` |
| 19 | `:80` | `dumpVariableItem` | `false` | `false` | 一致 | `xml:57` → `config:10` が `false`。値は同じ |

**不一致 8件 / 一致 11件。** 表外の `:216`（`tip` の `htmlResourcesRoot`）を加えて **不一致9件**であり、
作業指示が挙げた9件と**完全に一致した**（自分の判定が作業指示と食い違った行は無い）。

- 表外1件: `htmlResourcesRoot` は現在の記載 `htmlResources`、実効値 `../htmlResources`（`xml:52` →
  `config:7`）。**不一致**。フィールド初期値は `HttpTestConfiguration.java:144` の `htmlResources` であり、
  デフォルト設定が上書きしている
- 一致と判定した11件のうち、#11・#12・#13・#19 の4件は「デフォルト設定が設定しているが、値が
  フィールド初期値と同じ」ため一致した。基準を実効値に変えても記載は変わらない
- 残る7件（#1・#3・#4・#5・#6・#7・#18）は「デフォルト設定が設定していない」ため、フィールド初期値が
  そのまま実効値になり一致した
- `config:12` の `nablarch.httpTestConfiguration.webFrontControllerKey=webFrontController` は
  `http-request-test.xml` から参照されていない（`rest-request-test.xml` 側で使う）。本表の対象外

---

## ゲート2 — 作成済み7ページの「デフォルト」「既定」全出現の照合（全件表）

7ページを全走査し、`grep -n "デフォルト\|既定"` で **50件**を抽出した。母集合をホワイトリストで
切り出していない。行番号は**是正前**のもの（抽出時点＝母集合確定時点）。

判定の凡例: **是正** = 本タスクで是正した / **非該当（値の話でない）** = 設定値のデフォルトを述べていない /
**非該当（一致）** = 実効値と一致している。

### testdata_notation.rst（23件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 1 | `:156` | 省略カラムにデフォルト値が入っているものとして比較 | 非該当（一致） | カラム省略時の補完値。デフォルト設定は `defaultValues` を設定しない（jar 全体を `grep` して0件）ため `BasicDefaultValues` のフィールド初期値が実効値 |
| 2 | `:254` | デフォルトグループ | 非該当（値の話でない） | グループIDの概念の呼称 |
| 3 | `:429` | 検索結果取得の既定キーは `searchResult` | 非該当（一致） | `setSearchResultKey` 未設定時のコード既定。デフォルト設定は設定しない |
| 4 | `:664` | 型に応じたデフォルト値（数値型 `0`、文字型半角スペース） | 非該当（一致） | #1 と同じ |
| 5 | `:692` | 省略カラムにデフォルト値が設定されているものとして扱う | 非該当（一致） | #1 と同じ |
| 6 | `:698` | 次の表のデフォルト値がそのまま INSERT される | 非該当（一致） | #1 と同じ |
| 7 | `:700` | 省略時のデフォルト値。`BasicDefaultValues` でカスタマイズ | 非該当（一致） | 本文が「コンポーネント設定ファイルで明示的に指定していない場合の値」と自ら限定しており、デフォルト設定が `defaultValues` を設定しないため実効値と一致 |
| 8 | `:707` | 表ヘッダ「デフォルト値」 | 非該当（一致） | #7 の表のヘッダ |
| 9 | `:723` | `DATE` カラムのデフォルト値は JVM のタイムゾーン依存 | 非該当（一致） | #1 と同じ。`BasicDefaultValues.java:41` の `dateValue = null` を経由する挙動 |
| 10 | `:725` | 省略カラムにデフォルト値が入っているものとして比較 | 非該当（一致） | #1 と同じ |
| 11 | `:727` | 省略カラムにデフォルト値を補完して統合 | 非該当（一致） | #1 と同じ |
| 12 | `:871` | ディレクティブの既定値はコンポーネント設定ファイルで map 形式で指定できる | 非該当（値の話でない） | 指定方法の説明であり、特定の既定値を書いていない |
| 13 | `:915` | フィールド区切り文字。デフォルトは `","` | 非該当（一致） | フォーマッタ側のコード既定。デフォルト設定に該当プロパティは無い |
| 14 | `:1131` | `record_type` は常に既定のレコード種別（`"default"`） | 非該当（値の話でない） | コードの固定挙動の呼称 |
| 15 | `:1137` | フレームワーク制御ヘッダの既定値は `requestId` ほか4種 | 非該当（一致） | `reader.fwHeaderfields` はデフォルト設定に0件（jar を `grep` して確認） |
| 16 | `:1175` | ステータスコードカラムが無い場合のデフォルト値 `"200"` | 非該当（一致） | コード既定。デフォルト設定に該当プロパティは無い |
| 17 | `:1177` | 未設定時のデフォルトは `"Fixed"` 形式 | 非該当（一致） | `messaging.assertAsMapFileType` はデフォルト設定に0件（jar を `grep` して確認） |
| 18 | `:1236` | 既定のレコード種別（`"default"`）に置き換える | 非該当（値の話でない） | #14 と同じ |
| 19 | `:1294` | `\r` を CR に変換する（デフォルト設定） | 非該当（一致） | ここでの「デフォルト設定」は `LineSeparatorInterpreter` の未設定時の挙動を指す語。デフォルト設定の `nablarch/test/test-data-interpreter.xml` は `lineSeparatorInterpreter` を**プロパティ無しで登録**しており（同ファイル内で確認）、フィールド初期値がそのまま実効値になる。値の食い違いは無い |
| 20 | `:1389` | デフォルト設定では CR のみが変換対象 | 非該当（一致） | #19 と同じ |
| 21 | `:1441` | デフォルト設定では CR のみが変換対象 | 非該当（一致） | #19 と同じ |
| 22 | `:1513` | 既定のレコード種別（`"default"`）に置き換える | 非該当（値の話でない） | #14 と同じ |
| 23 | `:1517` | 値が省略されたカラムへデフォルト値を補完 | 非該当（一致） | #1 と同じ |

### testdata_examples.rst（4件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 24 | `:866` | 書かなかったカラムにデフォルト値が入っていることまで比較 | 非該当（一致） | #1 と同じ |
| 25 | `:901` | デフォルト値の補完対象 | 非該当（一致） | #1 と同じ |
| 26 | `:940` | コード例中のコメント。デフォルト値が格納されているものとして比較 | 非該当（一致） | #1 と同じ |
| 27 | `:1811` | ステータスコードのデフォルト値 `"200"` | 非該当（一致） | #16 と同じ |

### common.rst（1件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 28 | `:17` | テストデータは、デフォルトでは `test/java` 配下から読み込まれる | **是正** | デフォルト設定 `nablarch/test/test-data.config` が `nablarch.test.resource-root=src/test/java` を与える。`nablarch/test/test-data.xml` が `<config-file>` で読み込み、両アーキタイプの `unit-test.xml:14` がこれを `<import>` する。STEP 4 で `src/test/java` に是正 |

### class_unit_test.rst（9件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 29 | `:10` | カラムの記述を省略したときのデフォルト値を設定できる | 非該当（一致） | #1 と同じ |
| 30 | `:17` | 文字列長・未入力で期待するメッセージIDのデフォルト値を `EntityTestConfiguration` で設定する | 非該当（値の話でない） | 「利用者が設定する」ことの説明で、具体的な既定値を書いていない。加えて `nablarch/test/entity-test.xml` は両アーキタイプの `unit-test.xml` から `import` されておらず（実測。jar 内の他ファイルからの `import` も0件）、ブランクプロジェクトでは読み込まれない |
| 31 | `:42` | メッセージIDはいずれもデフォルト値として使われる | 非該当（値の話でない） | #30 と同じ |
| 32 | `:106` | 見出し「省略したテーブルのカラムのデフォルト値を変更する」 | 非該当（値の話でない） | 見出しの文言 |
| 33 | `:108` | このデフォルト値は `BasicDefaultValues` で変更できる | 非該当（一致） | #1 と同じ |
| 34 | `:118` | 文字列型のデフォルト値（説明セル） | 非該当（値の話でない） | 設定項目の説明であり、既定値そのものを書いていない |
| 35 | `:121` | 数値型のデフォルト値（説明セル） | 非該当（値の話でない） | #34 と同じ |
| 36 | `:124` | 日付型のデフォルト値（説明セル） | 非該当（値の話でない） | #34 と同じ |
| 37 | `:133` | コード例中のコメント「データベースのデフォルト値」 | 非該当（値の話でない） | コメント文 |

### request_unit_test/web.rst（8件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 38 | `:25` | 設定項目表のヘッダ「デフォルト値」 | **是正（基準の明示）** | STEP 2 で表の直前の地の文に基準を明示した。ヘッダ文言自体は不変 |
| 39 | `:76` | `tempDirectory` の値「該当なし（内蔵サーバ（Jetty）のデフォルト動作に従う）」 | **是正** | ゲート1 #17。`target/tmp` に是正 |
| 40 | `:102` | `tip`。`tempDirectory` を省略した場合は Jetty のデフォルト動作 | **是正** | デフォルト設定が `target/tmp` を入れるため、省略しても Jetty のデフォルト動作にはならない。前提を明示する形に是正 |
| 41 | `:104` | 「デフォルト値と同じ値を明示的に記述している項目もある」 | **是正（連動）** | 記述例の `webBaseDir` が `../main/web` で表と矛盾していた。値を `src/main/webapp` に是正し、文はそのまま成立する |
| 42 | `:184` | Eclipse で JRE のデフォルトとして指定する | 非該当（値の話でない） | Eclipse の設定手順 |
| 43 | `:191` | JRE のデフォルトとして指定する場合の手順 | 非該当（値の話でない） | #42 と同じ |
| 44 | `:198` | 「デフォルトの VM 引数」欄 | 非該当（値の話でない） | Eclipse の UI ラベル |
| 45 | `:216` | HTMLリソースのコピー先ディレクトリ（デフォルトは `htmlResources`） | **是正** | 実効値は `../htmlResources`（`xml:52` → `config:7`）。表外の不一致1件 |

### request_unit_test/rest.rst（5件）

| # | 行 | 内容の要旨 | 判定 | 理由 |
|---|---|---|---|---|
| 46 | `:10` | 専用のモジュールとデフォルト設定の追加が必要 | 非該当（一致） | デフォルト設定の存在に言及しているだけ |
| 47 | `:27` | コード例中のコメント「テスティングフレームワークのデフォルト設定」 | 非該当（値の話でない） | コメント文 |
| 48 | `:44` | デフォルト設定として提供されている設定ファイルの読み込み | 非該当（一致） | 手順の説明 |
| 49 | `:61` | デフォルト設定を読み込むと…デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す | 非該当（一致） | `#17` で承認済みの基準の明示。**`web.rst` の STEP 2 はこの文を範とした** |
| 50 | `:69` | 設定項目表のヘッダ「デフォルト値」 | 非該当（一致） | 基準は `:61` で明示済み |

### ゲート2 の結論

- 是正した箇所: **web.rst 5件（#38・#39・#40・#41・#45）＋ common.rst 1件（#28）**
- 残り44件はいずれも**非該当**。うち「値の話でない」14件、「実効値と一致」30件
- **ゲート1・STEP 4 で扱った箇所以外の食い違いは0件。** 本作業指示の範囲外として記録すべき
  是正見送り項目は発生しなかった。`reviews/page-*.md` への範囲外事項の記録は不要と判断した
- なお #19〜#21 は「デフォルト設定」という語を `nablarch-testing-default-configuration` 以外の意味で
  使っている。値の食い違いは無いため是正しないが、`design.md` §8 に基準を規定した以降は語が衝突しうる。
  申し送りとして `reviews/page-testdata_notation.md` に記録した

---

## ゲート3 — `ja/` の変更が2ファイルだけか

`git diff 6274d6d HEAD -- ja/ --name-only`:

```
ja/development_tools/testing_framework/setup/common.rst
ja/development_tools/testing_framework/setup/request_unit_test/web.rst
```

**2ファイルのみ。PASS。**（`rest.rst` を含む他の `.rst`・画像・`conf.py` に差分なし）

## ゲート4 — `web.rst` の見出しと表構造の不変

- 見出し: 変更前後の「アンダーライン行＋直前行」を `diff` した結果が**空**。**行番号まで含めて同一**であり、
  文言・並び順・出現位置のいずれも不変。PASS
- 設定項目表: `^  \* - ` の行（設定項目名の列）を抽出して `md5sum` を取った結果が変更前後で一致
  （`0cf41b9e8d353b834daa455f2eb85efb`）。行数はいずれも **20**（ヘッダ1行＋19行）。項目名と並び順は不変。PASS
- 列構成: `:header-rows: 1` / `:widths: 22,48,30` に差分なし（ゲート3 の diff に現れていない）。PASS

## ゲート5 — `common.rst` の差分が `:17` の1文由来だけか

`git diff` の結果は `-1 / +1` 行。変更は `test/java` → `src/test/java` の1語のみで、同一文内に収まる。
他のセクション・見出し・コードブロックに差分なし。**PASS。**

## ゲート6 — `verify_mapping.py`

```
Loaded 594 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
exit=0
```

**594行 / 12,986 / 11,983 が不変。exit 0。PASS。**

## ゲート7 — `mapping/` と `ja/conf.py` の差分

`git diff 6274d6d HEAD -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py` の出力が**空**。**PASS。**
（`mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `style.md` はすべて `mapping/` 配下）

## ゲート8 — `design.md` の差分が §8 内に収まり、削除0件か

- hunk は `@@ -437,6 +437,45 @@` の**1つのみ**。追加39行・**削除0行**
- `-` で始まる行（`---` を除く）が **0件**。行単位でも内容でも、既存の記述の削除は無い
- §8 の範囲は現在 `design.md:372`（`## 8. トンマナ`）〜`:481`（`## 9. 対象外とするもの`）。追記位置は
  `:437` 付近であり **§8 の内側**。`## 9.` 以降は行がずれただけで内容は不変
- **PASS**

## ゲート9 — `:ref:` の未定義参照と段落内改行

- **未定義参照**: フルビルドのログで `undefined label` は **1件**。
  `ja/application_framework/application_framework/libraries/db_double_submit.rst:108` の
  `how_to_set_token_in_request_unit_test`。これは `#7` で検出済みの**既知の未解決参照**であり、
  参照先ページ（`implementation/request_unit_test/web.rst`）が未作成のため残っているもの。
  `checks/task-07.md`「リンク切れになる参照」に記録され、`#last` で解消する予定の項目である。
  **本タスクが新たに発生させた未定義参照は0件**（`ja/` の差分に `:ref:` の追加・変更・削除は無い）。
  `toctree contains reference to nonexisting document` 0件、`unknown document` 0件
- **段落内改行**: 変更した2ファイルについて、コードブロック・`list-table`・`image`・`contents` の
  配下と箇条書き（`* ` / `- `）を除外したうえで、空行を挟まず日本語の行が連続する箇所を機械検出した結果、
  **両ファイルとも0件**
- **PASS**（未定義参照は既知の1件のみで新規0件）

## ゲート10 — Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

結果: `build succeeded, 1 warning.`（exit 0）

警告の全件:

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

**既知の `db_double_submit.rst` 1件のみ。新規警告0件。PASS。**

## ゲート11 — `#17` の user review を `/rn:gm` と記した箇所（全件表）

`.rn/20260724-ntf-yaml-support/` 配下を全走査し `rn:gm` を抽出した結果は **34件**。
`#17` 以外のタスクの記録は対象外のため、全件に「`#17` に関するものか」の判定を付す。

| # | 箇所 | `#17` に関するものか | 判定理由 |
|---|---|---|---|
| 1 | `mapping/style.md:13` | いいえ | `#9` 時点の S-09 追加の由来（2026-08-06） |
| 2 | `mapping/style.md:422` | いいえ | 目次追加フィードバックの由来（2026-08-06） |
| 3 | `mapping/style.md:519` | いいえ | `#10` のセル格子フィードバック |
| 4 | `checks/task-10-quotes.md:7` | いいえ | `#10` の差し戻し |
| 5 | `steering.md:250` | いいえ | `#8` の目次追加フィードバック |
| 6 | `steering.md:280` | いいえ | `#10` の `Closed`。`/rn:ty` 承認＋`/rn:gm` 差し戻し2回の経緯 |
| 7 | `steering.md:354` | いいえ | `#10b` の user review 行（公開本文の承認） |
| 8 | `steering.md:377` | いいえ | `#10b` の `Closed` |
| 9 | `steering.md:415` | いいえ | `#14` の `Closed`（締めの追記が `/rn:gm`） |
| 10 | `steering.md:455` | **はい（訂正の記述側）** | `#18` の Purpose。「`#17` の user review を `/rn:gm` と記録した3箇所を `/rn:ty` に訂正する」と**訂正作業そのものを説明**する文であり、`#17` の判定を `/rn:gm` と記した箇所ではない |
| 11 | `steering.md:466` | **はい（訂正の記述側）** | `#18` の STEP 6。訂正作業の Step 名 |
| 12 | `steering.md:475` | **はい（訂正の記述側）** | `#18` の完了条件。ゲート11 の説明 |
| 13 | `steering.md:502` | いいえ | `#last` の Steps。判定コマンドの一般的な選択肢 |
| 14 | `mapping/vocabulary.md:105` | いいえ | `#8` のフィードバック対応 |
| 15 | `mapping/volume.md:91` | いいえ | `#8` のフィードバック対応 |
| 16 | `mapping/volume.md:131` | いいえ | `#8` のフィードバック対応 |
| 17 | `reviews/page-about_index.md:113` | いいえ | `#8` の判断の覆り |
| 18 | `reviews/page-about_index.md:257` | いいえ | `#8` の見出し |
| 19 | `reviews/page-about_index.md:270` | いいえ | `#8` の直接フィードバック |
| 20 | `reviews/page-about_index.md:298` | いいえ | `#8` の R1-D2 |
| 21 | `checks/task-09.md:228` | いいえ | `#9` の Ready to check off。判定コマンドの一般的な選択肢 |
| 22 | `ntf-doc-18-default-value-basis.md:11` | **はい（訂正の指示側）** | 本作業指示。「`/rn:gm` と記録されているが実際は `/rn:ty`」と**訂正を指示**する文 |
| 23 | `ntf-doc-18-default-value-basis.md:126` | **はい（訂正の指示側）** | 本作業指示 STEP 6-4 |
| 24 | `ntf-doc-18-default-value-basis.md:144` | **はい（訂正の指示側）** | 本作業指示 ゲート11 |
| 25 | `checks/task-06.md:4` | いいえ | `#6` の差し戻し |
| 26 | `checks/task-08.md:63` | いいえ | `#8` の Ready to check off。判定コマンドの一般的な選択肢 |
| 27 | `design.md:65` | いいえ | `#8` のフィードバック由来 |
| 28 | `design.md:102` | いいえ | `#8` のフィードバック由来 |
| 29 | `design.md:108` | いいえ | `#8` のフィードバック由来 |
| 30 | `design.md:386` | いいえ | `#8` の目次追加 |
| 31 | `design.md:387` | いいえ | `#10` のセル格子 |
| 32 | `reviews/page-testdata_notation.md:57` | いいえ | `#9` のラウンド3 |
| 33 | `reviews/page-testdata_notation.md:59` | いいえ | `#9` のラウンド3 |
| 34 | `checks/task-09-restructure.md:736` | いいえ | `#9` の判定待ち。判定コマンドの一般的な選択肢 |

**`#17` の user review の判定を `/rn:gm` と記した箇所は0件。PASS。**
`#17` に関する6件（#10〜#12・#22〜#24）は、いずれも**訂正すること自体を述べる文**であり、
`#17` の判定を誤って記録している箇所ではない。

訂正した3箇所（STEP 6-4）:

| 箇所 | 変更前 | 変更後 |
|---|---|---|
| `checks/task-17.md` §6-1 の見出し | `### 6-1. user review の回答（2026-08-13、/rn:gm）` | `### 6-1. user review の回答（2026-08-13、/rn:ty）` |
| `steering.md` `#17`「`decide` 2件の回答」冒頭 | `（2026-08-13、/rn:gm。判断を仰いだ時点の記録は…` | `（2026-08-13、/rn:ty。判断を仰いだ時点の記録は…` |
| `steering.md` `#17` `Closed` 冒頭 | `user review 承認済み（/rn:gm、2026-08-13。公開本文を承認し…` | `user review 承認済み（/rn:ty、2026-08-13。公開本文を承認し…` |

**判断当時の記録には手を触れていない。** `checks/task-17.md` の §6 の `decide` 表・§7-2 の7項目表・
`Overall Verdict` の `No` の行はいずれも変更していない（`git diff` で §6-1 見出しの1行のみの変更を確認）。

---

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| 作業指示のゲート1〜11 がすべて実行結果で確認され、`checks/task-18.md` に記録されている | OK | 本ファイル。ゲート1〜11 すべて PASS |
| ゲート1・2・11 が件数ではなく全件の表で記録されている（母集合をホワイトリストで切り出さない） | OK | ゲート1は `^  \* - ` の機械抽出（20行＝ヘッダ＋19行）で全19行、ゲート2は `grep` の全50件、ゲート11は `grep` の全34件を、いずれも判定理由付きで掲載 |
| `ja/` の差分が2ファイルのみで、`web.rst` の見出しと表の行数・列構成・項目名・並び順が不変 | OK | ゲート3・4 |
| `design.md` の差分が §8 の中だけに収まり、既存の記述の削除が0件 | OK | ゲート8。hunk 1つ・削除0行 |
| 禁止事項に抵触する変更が無い | OK | ゲート7（`mapping/` 配下と `ja/conf.py` の差分が空）。新しいページの作成なし、`rest.rst` の変更なし（ゲート3） |
| `verify_mapping.py` が exit 0 で 594行 / 12,986 / 11,983 が不変 | OK | ゲート6 |
| Docker フルビルド（`-a`）が `build succeeded` で警告が既知の1件のみ（新規0件） | OK | ゲート10 |

## Overall Verdict

- Self-check: **OK**
- 4観点レビュー: **N/A** — 作業指示が明示的に禁止（「4観点のレビューは回さない。新しい内容を書かない
  タスクであり、ゲート1〜5 が変更の範囲を機械的に固定している」）
- Ready to check off: **No** — `steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」
  および `#18` Steps の最終項目により、**user review の判定（`/rn:ty` または `/rn:gm`）待ち**

## 作業指示から外れた点・判断を記録すべき点

1. **`nablarch-core-repository`（`6a28491`）を自分では開いていない。** ローカルにクローンが無かった。
   プロパティ単位マージの行番号は作業指示の記述をそのまま引いたため、`design.md` §8 の追記では
   **行番号を書かず**、クラス名（`XmlComponentDefinitionLoader`）と既定ポリシー名
   （`DuplicateDefinitionPolicy.OVERRIDE`）のみを記した。出典を示せない行番号を規定に書かないため
2. **`nablarch-testing` のローカルクローンの HEAD は `fdf55d4` で `e21bf67` ではない。** `git show e21bf67:<path>`
   で `e21bf67` の内容を直接取得し、あわせて `git diff e21bf67 HEAD -- .../HttpTestConfiguration.java` が
   空であることを確認した。記録した `file:line` は `e21bf67` のもの
3. **アーキタイプ2件は Maven Central から新たに取得した。** ローカル Maven リポジトリに無かったため。
   デフォルト設定が読み込まれるという本タスクの前提を、自分で開いて確かめる必要があった（§0-1）
4. **ゲート9 の「未定義参照0件」は、厳密には満たしていない。** 既知の `db_double_submit.rst:108` の1件が
   残っている。これは `#7` で検出され `#last` で解消予定の項目であり、本タスクが発生させたものではない。
   ゲート10 が同じ1件を「既知」として明示的に許容していることから、ゲート9 の趣旨は「新規の未定義参照が
   0件であること」と解釈した。**新規0件**であることは `ja/` の差分に `:ref:` の増減が無いことで確認した
5. **ゲート2 で範囲外の食い違いは0件だったため、`reviews/page-*.md` への範囲外事項の記録は行っていない。**
   ただし「デフォルト設定」という語が `testdata_notation.rst` の3箇所で
   `nablarch-testing-default-configuration` 以外の意味で使われている点は、値の食い違いではないが
   `design.md` §8 の規定以降に語が衝突しうるため、申し送りとして記録した
