# task-55 Completion Check

`#55` NTF解説書の JUnit 5 ベース化。指示書 `.rn/20260724-ntf-yaml-support/ntf-doc-55-junit5-base.md`。

本ファイルはフェーズ0（着手前検証）とフェーズ1（実装）の実測記録である。フェーズ0 では `.rst`・`mapping/`・`design.md`
のいずれも変更していない。フェーズ1 はディレクターの承認（指示書 §10）を受けて着手した。

## フェーズ0 実施記録（2026-08-31）

### 参照ピンの実在確認

| リポジトリ | ピン | 実測 |
|---|---|---|
| `nablarch-document` | `764fb9fd` | `git diff --stat 764fb9fd..HEAD -- ja/ mapping/` が0件。`ja/`・`mapping/` は HEAD と同一 |
| `nablarch-testing-junit5` | `c06ebe8` | worktree `~/work/nablarch/nablarch-testing-junit5/.claude/worktrees/fix-resolveTestRules` の HEAD が `c06ebe8`（`docs: セッションクローズ時点の State を記録`） |
| `nablarch-single-module-archetype` | `9ef4096` | scratchpad へ clone。HEAD が `9ef4096`（`Merge remote-tracking branch 'origin/release-6u3'`） |
| `nablarch-testing` | `e21bf67` | `git cat-file -t e21bf67` = `commit`。**ただし `main` 上のコミット**（`Merge remote-tracking branch 'origin/release-6u2'`。`git branch -a --contains e21bf67` = `main` のみ） |

### 0-1 指示書の逐語・`file:line`・件数の突合

**一致した主張**

| 指示書の主張 | 実測 |
|---|---|
| `junit5_extension.rst:16`「JUnit 4では、これらのクラスをテストクラスが継承することで、その機能をテストクラスから使用していた。」 | 一致（`:16` の第2文） |
| Extension・合成アノテーション一覧表 `:28`〜 | L3 見出し `:28`「Extensionクラスと合成アノテーションの一覧」。表は `:32`-`:71`、11行 |
| 前提事項 `:73` surefire 2.22.0 | L3 見出し `:73`、本文 `:75`「`maven-surefire-plugin` が2.22.0以上」 |
| 「依存関係を追加する」`:80` | L3 見出し `:80` |
| 合成アノテーション設定 `:98`〜 | ラベル `.. _junit5_extension-inject:` が `:98`、L3 見出し `:100` |
| `BasicHttpRequestTestTemplate` `:131`〜 | L3 見出し `:131` |
| `RegisterExtension` `:151`〜 | L3 見出し `:151` |
| vintage 節 ラベル `junit5_extension-vintage`・`:180`〜`:225` | ラベル `:180`、L3 見出し `:182`、節末 `:225`（次節 `拡張例` が `:227`） |
| junit-bom の例 `:200-201` の `5.8.2` | `:200` `<artifactId>junit-bom</artifactId>`、`:201` `<version>5.8.2</version>` |
| 拡張例 `:227`〜 | L2 見出し `:227` |
| 「JUnit 4のTestRuleを再現する」`:397`〜 | L3 見出し `:397`。節末はファイル末尾 `:455` |
| `about/index.rst:30`-`:48` 特徴4節 | L3 見出し `:30`、節末 `:48`（tip 本文）。**コードブロック自体は `:36`-`:44`**（`:34` は導入文、`:46` は `.. tip::`） |
| `about/index.rst:32`「JUnit 4を基盤としており」 | 一致 |
| `about/index.rst:48` tip `@Before`・`@After` | 一致 |
| `about/index.rst:106`「テスティングフレームワークを継承したテストクラスは」 | 一致 |
| `about/index.rst:110`「テストクラスが継承するクラスの系譜を次に示す。」 | 一致 |
| `about/index.rst:119` 稼動環境 | L2 見出し `:117`、本文 `:119`（ファイル末尾） |
| §4 の継承7種12箇所（web `:79`・`:114` / rest `:75` / req batch `:76`・`:94` / deal batch `:40`・`:66` / req mom `:104`・`:122` / deal mom `:56` / component `:81`・`:163`・`:201` / entity `:95`） | `grep -rn 'extends ' implementation --include='*.rst'` の全16件と突合。指示書記載の14箇所はすべて一致（残り2件は `component.rst:100` `extends AnotherSuperClass`・`:140` `extends TestSuper` で、いずれも JUnit 4 固有節） |
| tip 6件（web `:87`・rest `:93`・req batch `:100`・req mom `:133`・component `:91`・entity `:105`） | 6件とも一致。6件は全ページ同一文 |
| `junit5_extension` の外部参照8箇所 | `grep -rn 'junit5_extension'` の全13ヒットのうち、`junit5_extension.rst` 自身の5件（ラベル定義3・画像パス1・自ページ内 `:ref:` 1）を除く8件。内訳は tip 6・`about/index.rst:119`・`setup/index.rst:20` |
| `nablarch-testing@e21bf67 pom.xml:151`-`:155` junit 4.13.1 compile | `:150` `<dependency>`／`:151` `<groupId>junit</groupId>`／`:152` `<artifactId>junit</artifactId>`／`:153` `<version>4.13.1</version>`／`:154` `<scope>compile</scope>`／`:155` `</dependency>` |
| アーキタイプ `nablarch-web/pom.xml:247-248` junit-bom 5.11.0 | `:247` `<artifactId>junit-bom</artifactId>`／`:248` `<version>5.11.0</version>` |
| 同 `:361` nablarch-testing-junit5 | `:361` `<artifactId>nablarch-testing-junit5</artifactId>`（`:362` `<scope>test</scope>`） |
| 同 `:367` junit-jupiter | `:367` `<artifactId>junit-jupiter</artifactId>`（`:368` `<scope>test</scope>`） |
| `c06ebe8` の `src/main` 23クラス | `git ls-tree -r --name-only c06ebe8 \| grep -c '^src/main/java/.*\.java$'` = 23。内訳は Extension 11・合成アノテーション 11・`TestEventDispatcherExtension` 1。ページの一覧表11行と対応 |
| `mapping.csv` 597行 / 12,986 / 11,983 | `csv.DictReader` で597行。`lines` 合計 12,986。`disposition != DROP` の `lines` 合計 11,983 |
| design.md §2 表 row 4 稼動環境 | `design.md:37` |
| design.md §3 構成ブロック | `design.md:238`（`├── JUnit 5用拡張機能`） |
| design.md §13 ツリー | `design.md:923`（`│   ├── junit5_extension.rst`） |
| design.md §13 第2部の1対1対応表 13ページ | `design.md:998`「#### 第2部（13ページ）」・`:1003` が該当行 |
| design.md §13 集計 34ページ | `design.md:1049` |
| `vocabulary.md` 第2部13件・全体34件 | `vocabulary.md:38`「### 第2部（13件）」・`:30`「## dest_page（確定・34件）」。該当行は `:44` |
| `style.md` S-08 の該当行 | `style.md:491` |
| `glossary.md` §5.12 の該当行 `:298`／§5.15 の `:360` | どちらも一致 |
| `extension_class.puml` の `title` | `title JUnit 5用拡張機能のクラスと、インスタンスの生成・インジェクション` |
| `test_support_class.puml` の `title` | `title テストクラスが継承するサポートクラスの系譜` |
| `03-検証スクリプト.md` §5・§9／`02-進め方.md` の禁止事項 | `/home/tie303177/work/cowork/nablarch/ntf-doc-renewal/` に実在。§5「Docker フルビルド」・§9「図の生成（PlantUML → PNG）」。§9 の temurin-17 絶対パス `/usr/lib/jvm/temurin-17-jdk-amd64/bin/java`・`~/.local/share/plantuml/plantuml-1.2025.4.jar`（22,592,450 bytes）・`~/.fonts/NotoSansJP-Regular.ttf` はいずれもホストに実在 |

**反例（是正が要る項目）** — 本文の「フェーズ0 の反例」節を参照。

### 0-2 `code-block:: java` 全件表

母集合の固定: `grep -rn 'code-block:: java' ja/development_tools/testing_framework --include='*.rst'` = **85件**。

| ディレクトリ／ページ | 件数 | 処置 |
|---|---|---|
| implementation 9ページ（下表） | 65 | §4 の対象 |
| `implementation/testdata_notation.rst` | 1 | 対象外（`:590` は `List<Map<String,String>>` の組み立て例。テストクラス例でない） |
| `setup/junit5_extension.rst` | 13 | §1 の対象（内容は保つ。vintage 節の分は §2 で移設） |
| `tools/testdata_converter.rst` | 4 | 対象外（`:207`・`:216`・`:238`・`:327` はいずれも `TestDataConverter`／`ConversionRequest`／`YamlTestDataValidator`／`ExcelFormatConfig` の API 呼び出し。テストクラス例でない） |
| `tools/html_check_tool.rst` | 1 | 対象外（`:148` は `HtmlChecker` の実装例） |
| `about/index.rst` | 1 | §3 の対象（`:36`-`:44`） |
| `implementation/testdata_examples.rst` | 0 | — |

`setup` の残り11ページ・`tools/index.rst`・`implementation` の残り6ページ（`deal_unit_test/{web,http_messaging,db_queue}.rst`・`request_unit_test/{http_messaging,db_queue}.rst`・`index.rst`）はいずれも0件。

**implementation 9ページ 65件の内訳**（分類 A=テストクラス例／B=テストメソッド断片／C=メソッドシグネチャの列挙／D=対象外／E=`junit4.rst` へ移設）

| # | ファイル:行 | 種類 | 分類 | 処置 |
|---|---|---|---|---|
| 1 | web.rst:73 | `extends BasicHttpRequestTestTemplate` クラス骨格 | A | `@BasicHttpRequestTest(baseUri=…)` ＋ `BasicHttpRequestTestTemplate support;` |
| 2 | web.rst:112 | 同上＋`getBaseUri()` オーバーライド | A | §4 のとおり `baseUri` 属性の説明へ書き換え。`getBaseUri()` は `protected abstract`（javap 実測）でインジェクション方式では呼べないため、コード例からは落とす |
| 3 | web.rst:175 | `@Test`＋`execute()` | B | `void`＋`support.execute()`（`AbstractHttpRequestTestTemplate.execute()` は `public`） |
| 4 | web.rst:184 | `execute` 4シグネチャ | C | そのまま（4つとも `public`） |
| 5 | web.rst:201 | `Advice` の2シグネチャ | C | そのまま |
| 6 | web.rst:208 | `@Test`＋`execute(new BasicAdvice(){…})` | B | `support.execute(...)` |
| 7 | web.rst:260 | `setValidToken` | C | そのまま（`public`） |
| 8 | web.rst:266 | `setToken` | C | そのまま（`public`） |
| 9 | web.rst:272 | `setToken(...)` 断片 | B | `support.setToken(...)` |
| 10 | web.rst:282 | `createHttpRequest`×2・`createExecutionContext` | C | そのまま（`HttpRequestTestSupport` の `public` 版と一致） |
| 11 | web.rst:294 | `HttpResponse execute(String, HttpRequest, ExecutionContext)` | C | **要是正。この3引数版は `protected`**（下記 反例2） |
| 12 | web.rst:357 | `@Test`＋`assertSqlResultSetEquals` | B | `support.` 経由 |
| 13 | web.rst:400 | `@Test`＋`assertEntity` | B | `support.` 経由 |
| 14 | web.rst:425 | `@Test`＋`getListMap` | B | `support.` 経由 |
| 15 | web.rst:445 | `@Test`＋`getParam` | B | `support.` 経由 |
| 16 | web.rst:464 | `assertObjectPropertyEquals` 他2 | C | そのまま（3つとも `public`） |
| 17 | web.rst:474 | `@Test`＋`assertObjectPropertyEquals` | B | `support.` 経由 |
| 18 | web.rst:498 | `assertApplicationMessageId` | C | そのまま（`public`） |
| 19 | web.rst:514 | `FileSupport` フィールド＋`@Test` | B | `support.execute(...)`。`new FileSupport(getClass())` はテストクラス自身の `getClass()` のため変更不要 |
| 20 | rest.rst:61 | `extends RestTestSupport` 全体像 | A | `@RestTest` ＋ `RestTestSupport support;`。`import org.junit.Test;` → `org.junit.jupiter.api.Test` |
| 21 | rest.rst:112 | `get`/`post`/`put`/`patch`/`delete` | C | そのまま |
| 22 | rest.rst:126 | `newRequest` | C | そのまま |
| 23 | rest.rst:136 | `post(...)` 断片 | B | `support.post(...)` |
| 24 | rest.rst:151 | `getListMap` 他2 | C | そのまま |
| 25 | rest.rst:165 | `sendRequest` | C | そのまま |
| 26 | rest.rst:177 | `assertStatusCode` | C | そのまま |
| 27 | rest.rst:199 | `readTextResource` | C | そのまま |
| 28 | request_unit_test/batch.rst:70 | `extends BatchRequestTestSupport` | A | `@BatchRequestTest` ＋ `BatchRequestTestSupport support;` |
| 29 | request_unit_test/batch.rst:88 | 同上 | A | 同上 |
| 30 | request_unit_test/batch.rst:113 | `@Test`＋`execute()` | B | **要是正。引数なし `execute()` は `protected final`**（下記 反例1） |
| 31 | request_unit_test/batch.rst:122 | `@Test`＋`execute("…")` | B | `support.execute("testRegisterUser")`（`public final`） |
| 32 | request_unit_test/mom.rst:98 | `extends MessagingRequestTestSupport` | A | `@MessagingRequestTest` ＋ フィールド |
| 33 | request_unit_test/mom.rst:116 | `extends MessagingReceiveTestSupport` | A | `@MessagingReceiveTest` ＋ フィールド |
| 34 | request_unit_test/mom.rst:148 | `@Test`＋`execute()` | B | **要是正**（反例1） |
| 35 | deal_unit_test/batch.rst:32 | `extends BatchRequestTestSupport` | A | `@BatchRequestTest` ＋ フィールド |
| 36 | deal_unit_test/batch.rst:47 | `@Test`＋`execute()` | B | **要是正**（反例1） |
| 37 | deal_unit_test/batch.rst:57 | クラス例＋`execute("…")`×3 | A | `execute(String)` は `public final` のため `support.execute("…")` でよい |
| 38 | deal_unit_test/mom.rst:50 | `extends MessagingRequestTestSupport` | A | `@MessagingRequestTest` ＋ フィールド |
| 39 | deal_unit_test/rest.rst:30 | `@Test`＋`get`/`sendRequest`/`assertStatusCode` | B | `support.` 経由（§4 が例示している箇所） |
| 40 | class_unit_test/component.rst:73 | `extends DbAccessTestSupport` | A | `@DbAccessTest` ＋ `DbAccessTestSupport support;` |
| 41 | class_unit_test/component.rst:98 | `extends AnotherSuperClass`＋委譲＋`@Before`/`@After` | E | `setup/junit4.rst`「テスティングフレームワークのクラスを継承せずに使用する」へ移設（§2） |
| 42 | class_unit_test/component.rst:131 | `@BeforeClass` の上書き例 | E | `setup/junit4.rst`「テストの実行前後に共通処理を行う」へ移設（§2） |
| 43 | class_unit_test/component.rst:161 | `extends DbAccessTestSupport`＋`setUpDb`/`assertSqlResultSetEquals` | A | クラス反転＋`support.` 経由 |
| 44 | class_unit_test/component.rst:199 | 同上＋`commitTransactions`/`assertTableEquals` | A | 同上 |
| 45 | class_unit_test/component.rst:225 | `@Test`＋`setThreadContextValues` | B | `support.` 経由 |
| 46 | class_unit_test/component.rst:245 | `@Test`＋`getListMap` | B | `support.` 経由 |
| 47 | class_unit_test/component.rst:269 | `@Test`＋`setUpDb`/`getListMap`/`assertSqlResultSetEquals` | B | `support.` 経由 |
| 48 | class_unit_test/component.rst:297 | `setUpDb`/`assertTableEquals` 断片 | B | `support.` 経由 |
| 49 | class_unit_test/component.rst:324 | `TestDataParser` を直接使う例 | D | 対象外（サポートクラス非依存） |
| 50 | class_unit_test/component.rst:354 | `@Test`＋try/catch | B | `@Test` の `public` を落とし `void` にする。本体はサポートクラス非依存 |
| 51 | class_unit_test/entity.rst:88 | `extends EntityTestSupport` | A | `@EntityTest` ＋ `EntityTestSupport support;`。`import org.junit.Test;` を差し替え |
| 52 | class_unit_test/entity.rst:237 | `testValidateCharsetAndLength` | C | そのまま（`public`） |
| 53 | class_unit_test/entity.rst:275 | `@Test`＋同メソッド呼び出し | B | `support.` 経由 |
| 54 | class_unit_test/entity.rst:324 | `testSingleValidation` | C | そのまま（`public`） |
| 55 | class_unit_test/entity.rst:328 | `@Test`＋同メソッド呼び出し | B | `support.` 経由。テストメソッド名と同名だった衝突が `support.` で解消する |
| 56 | class_unit_test/entity.rst:359 | `testSetterAndGetter` | C | そのまま（`public`） |
| 57 | class_unit_test/entity.rst:363 | `@Test`＋同メソッド呼び出し | B | `support.` 経由（同上） |
| 58 | class_unit_test/entity.rst:388 | `@Test`＋`testSetterAndGetter`/`getParamMap` | B | `support.` 経由 |
| 59 | class_unit_test/entity.rst:436 | `SampleForm` の例 | D | 対象外（Form の宣言例） |
| 60 | class_unit_test/entity.rst:459 | `testBeanValidation` | C | そのまま（`public`） |
| 61 | class_unit_test/entity.rst:463 | `@Test`＋同メソッド呼び出し | B | `support.` 経由 |
| 62 | class_unit_test/entity.rst:489 | `testValidateAndConvert` | C | そのまま（`public`） |
| 63 | class_unit_test/entity.rst:493 | `@Test`＋同メソッド呼び出し | B | `support.` 経由 |
| 64 | class_unit_test/entity.rst:514 | `testConstructorAndGetter` | C | そのまま（`public`） |
| 65 | class_unit_test/entity.rst:518 | `@Test`＋同メソッド呼び出し | B | `support.` 経由 |

集計: A=14 / B=27 / C=20 / D=2 / E=2。合計65。

**メソッド可視性の実測**（`javap -protected`、`~/.m2/.../nablarch-testing-6-NEXT-20250314.140856-24.jar`。ソースは `e21bf67` と PR ブランチ `convert-testdata-excel-to-text`（`dcaed44`）で同一）

`support.` 経由に改める全メソッドのうち、`public` であることを確認したもの: `setValidToken`・`setToken`・`createHttpRequest`(2種)・`createExecutionContext`・`assertSqlResultSetEquals`・`assertEntity`・`getListMap`・`getListParamMap`・`getParamMap`・`getParam`・`assertObjectPropertyEquals`・`assertObjectArrayPropertyEquals`・`assertObjectListPropertyEquals`・`assertApplicationMessageId`・`setUpDb`・`commitTransactions`・`beginTransactions`・`endTransactions`・`assertTableEquals`・`setThreadContextValues`・`testValidateCharsetAndLength`・`testSingleValidation`・`testSetterAndGetter`・`testBeanValidation`・`testValidateAndConvert`・`testConstructorAndGetter`・`AbstractHttpRequestTestTemplate.execute`(8種)・`StandaloneTestSupportTemplate.execute(String)`・`execute(String, boolean)`。

クラス階層（javap 実測）: `BasicHttpRequestTestTemplate` → `AbstractHttpRequestTestTemplate` → `HttpRequestTestSupport` → `TestEventDispatcher`。よって `BasicHttpRequestTestTemplate` 型のフィールド経由で `HttpRequestTestSupport` の `public` メソッドはすべて呼べる。

### 0-3 新ラベルの衝突確認

母集合: `grep -rhoE '^\.\. _`?[^:`]+`?:' ja/ --include='*.rst'` で機械抽出（バッククォート形式を含む）= **1,054件**。

- `standard_usage` — 完全一致0件、部分一致0件
- `junit4_support` — 完全一致0件、部分一致0件
- 下位ラベル候補 `standard_usage-inject`・`junit4_support-vintage` — 上記のとおり `standard_usage`／`junit4` を含む既存ラベルが0件のため衝突なし

### 0-4 `mapping.csv` の新割当表

`dest_page = JUnit 5用拡張機能` は **17行**（指示書の記載どおり `current-0178`〜`0180`・`current-0265`〜`0278`）。`lines` 合計 475。

| `src_section_id` | `lines` | `heading_path` の末尾 | 現 `dest_section` | 所在 `_batch` | 新 `dest_page` |
|---|---|---|---|---|---|
| current-0178 | 18 | JUnit 5で自動テストフレームワークを動かす > JUnit Vintage | 機能概要 | `batch-03.csv` | **JUnit 4で使用する** |
| current-0179 | 5 | JUnit 5で自動テストフレームワークを動かす > 前提条件 | 機能概要 | `batch-03.csv` | 標準の使い方 |
| current-0180 | 42 | JUnit 5で自動テストフレームワークを動かす > 依存関係の追加 | 使用方法 | `batch-03.csv` | **JUnit 4で使用する**（※ 反例5） |
| current-0265 | 9 | JUnit 5用拡張機能 > 概要 | 機能概要 | `batch-14.csv` | 標準の使い方 |
| current-0266 | 8 | JUnit 5用拡張機能 > 前提条件 | 機能概要 | `batch-14.csv` | 標準の使い方 |
| current-0267 | 11 | JUnit 5用拡張機能 > モジュール一覧 | 使用方法 | `batch-14.csv` | 標準の使い方 |
| current-0268 | 47 | JUnit 5用拡張機能 > 基本的な使い方 | 使用方法 | `batch-14.csv` | 標準の使い方 |
| current-0269 | 44 | Extension クラスと合成アノテーションの一覧 > (L2直下) | 使用方法 | `batch-14.csv` | 標準の使い方 |
| current-0270 | 22 | 〜の一覧 > BasicHttpRequestTest の使い方の補足 | 使用方法 | `batch-14.csv` | 標準の使い方 |
| current-0271 | 12 | 独自の拡張を加える > (L2直下) | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0272 | 22 | 独自の拡張を加える > 独自拡張クラスを作成する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0273 | 25 | 独自の拡張を加える > 独自拡張用のExtensionを作成する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0274 | 22 | 独自の拡張を加える > ExtendWithでテストクラスに適用する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0275 | 82 | 〜BasicHttpRequestTestTemplateを拡張する場合はアノテーションも作成する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0276 | 25 | 独自の拡張を加える > 事前処理・事後処理を実装する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0277 | 52 | 独自の拡張を加える > JUnit 4のTestRuleを再現する | 拡張例 | `batch-14.csv` | 標準の使い方 |
| current-0278 | 29 | JUnit 5用拡張機能 > RegisterExtensionで使用する | 使用方法 | `batch-14.csv` | 標準の使い方 |

編集対象の `_batch` は2ファイル（`batch-03.csv` 3行・`batch-14.csv` 14行）。`JUnit 4で使用する` 側 60行（`current-0178` 18 ＋ `current-0180` 42）、`標準の使い方` 側 415行。合計 475 で不変。

### 0-5 見出しレベルの構成案

**`setup/standard_usage.rst`「標準の使い方」**（ラベル `standard_usage`）

```
L1 標準の使い方
   .. contents:: 目次 (:depth: 3 :local:)
L2 機能概要
     （冒頭でサポートクラス＋合成アノテーション＋Extension のインジェクションを言い切る）
     （図 images/standard_usage/extension_class.png）
     （JUnit 4 の対比は :ref:`JUnit 4で使用する <junit4_support>` への1文の導線に置き換える）
   L3 Extensionクラスと合成アノテーションの一覧      ← 現 :28。据え置き
   L3 前提事項                                      ← 現 :73。据え置き
L2 使用方法
   L3 依存関係を追加する                             ← 現 :80。標準セットアップとして書き直す
   L3 テストクラスに合成アノテーションを設定する        ← 現 :100。ラベルは standard_usage-inject へ改名
   L3 BasicHttpRequestTestTemplateを使用する         ← 現 :131。据え置き
   L3 RegisterExtensionでExtensionクラスを適用する    ← 現 :151。据え置き
   （現 :182「JUnit 4で書いたテストをJUnit 5上で実行する」は junit4.rst へ移設して削除）
L2 拡張例                                            ← 現 :227。据え置き
   L3 独自拡張クラスを作成する                        ← 現 :237
   L3 独自拡張用のExtensionクラスを作成する            ← 現 :258
   L3 ExtendWithでテストクラスに適用する               ← 現 :279
   L3 baseUriを渡す合成アノテーションを作成する          ← 現 :301
   L3 事前処理・事後処理を実装する                     ← 現 :378
   L3 JUnit 4のTestRuleを再現する                     ← 現 :397。据え置き（§1 の明示指定）
```

**`setup/junit4.rst`「JUnit 4で使用する」**（ラベル `junit4_support`。setup 末尾）

```
L1 JUnit 4で使用する
   .. contents:: 目次 (:depth: 3 :local:)
L2 機能概要
     （JUnit 4 でも使用できること／サポートクラスを継承して使うこと／
       既存の JUnit 4 テスト資産を持つプロジェクト向けであること／
       標準は :ref:`標準の使い方 <standard_usage>` への導線）
L2 使用方法
   L3 依存関係                                        ← 追加不要。nablarch-testing が junit:junit 4.13.1 を compile で推移提供
   L3 テストクラスを作成する                           ← 継承方式の最小例1つ＋読み替え規則1文
   L3 テストの実行前後に共通処理を行う                   ← component.rst:122-:146 を移設（ブロック42を含む）
   L3 テスティングフレームワークのクラスを継承せずに使用する  ← component.rst:93〜 を移設（ブロック41）
   L3 JUnit 4で書いたテストをJUnit 5上で実行する          ← junit5_extension.rst:180-:225 を移設。
                                                        ラベル junit4_support-vintage。junit-bom を 5.8.2 → 5.11.0
```

**`about/index.rst`**（見出しは1つも変えない。本文のみ反転）

```
L3 使い慣れたJUnitの書き方をそのまま活かせる  :30   ← :32 の「JUnit 4を基盤としており」／
                                                    :34 の導入文／:36-:44 のコード例／:48 の tip
L2 アーキテクチャ                          :104  ← :106 の継承前提／:110 の導入文／
                                                    test_support_class.puml の title
L2 稼動環境                                :117  ← :119 の1文
```

### 0-6 アーキタイプに `junit-vintage` が無いこと

`grep -rn -i 'vintage' <archetype> --exclude-dir=.git` = **0件**（全ファイル。pom は11本）。標準セットアップに vintage を含めない根拠として成立する。

## フェーズ0 の反例（ディレクター回答済み）

**10件とも指示書 §10 で回答を得ており、フェーズ1 はその回答に従って実装した。** 以下は当時の記録である。

1. **引数なし `execute()` は `support.` 経由で呼べない**（ブロック30・34・36 と、その周辺の地の文）。`javap`: `nablarch.test.core.standalone.StandaloneTestSupportTemplate` の `protected final void execute();`。`public final` は `execute(String)`・`execute(String, boolean)` のみ。アーキタイプ `9ef4096` の `nablarch-batch/src/test/java/com/nablarch/archetype/SampleBatchActionRequestTest.java:21` は `support.execute(support.testName.getMethodName());` と書いている（`testName` は `TestEventDispatcher` の `public final org.junit.rules.TestName`。`getMethodName()` は `protected final` のため `support.getMethodName()` は不可）。
2. **`web.rst:294` のシグネチャは `protected`**。`javap`: `HttpRequestTestSupport` の `protected HttpResponse execute(String, HttpRequest, ExecutionContext);` と `public HttpResponse execute(Class<?>, String, HttpRequest, ExecutionContext);`。インジェクション方式では4引数の `public` 版しか呼べない。
3. **完了条件5 の除外範囲が足りない**。`standard_usage.rst` の拡張例節に残る `extends TestSupport`（現 `junit5_extension.rst:243`）と `extends BasicHttpRequestTestTemplate`（現 `:309`）は §1 が「内容を保つ」と指定した独自拡張クラスの作成例であり、走査に必ず残る。完了条件5 の除外を「`setup/junit4.rst` 全体と `standard_usage.rst` の L2『拡張例』全体」に広げる必要がある。
4. **下位ラベル2件の新名称が未指定**。`junit5_extension-inject`（現 `:98`）と `junit5_extension-vintage`（現 `:180`）。完了条件2・§5-7 は `junit5_extension` の0件を要求するため必ず改名が要る。案は `standard_usage-inject`・`junit4_support-vintage`（衝突0件を 0-3 で確認済み）。
5. **`current-0180` の割当が §1 と矛盾する**。`current-0180`（依存関係の追加・42行）の `note` は「JUnit Vintage を有効にするため pom.xml に junit-jupiter/junit-vintage-engine の2アーティファクトを依存関係に追加する手順と、dependencyManagement 込みの pom.xml 記述例」。§5-3 はこれを `JUnit 4で使用する` のみに割り当てるが、§1 は `標準の使い方` の「依存関係を追加する」にも junit-bom 5.11.0 と junit-jupiter を書くよう指示している。この結果 junit-bom／junit-jupiter の記述が2ページに現れるのに、マッピング上の根拠は junit4 側にしかない。
6. **`style.md:414` が §5-5 の対象から漏れている**。`:414` に `setup/junit5_extension.rst:30` への参照がある（S-08 の表 `:491` とは別）。
7. **`volume.md` の経緯記述の扱いが未指定**。`JUnit 5用拡張機能` は `:26`（ページ別集計）のほか `:31`・`:73`・`:75`・`:94`・`:145` に出る。§5-1 は design.md についてのみ「過去の経緯を記す節の中の旧名は書き換えない」と定めており、volume.md への適用は書かれていない。
8. **`design.md:211` の扱いが未指定**。`:211` は `about/index.rst` の稼動環境を「`:ref:`JUnit 5用拡張機能 <junit5_extension>`` を参照。」の1文のみとする現行仕様の記述であり、単なる経緯ではない。§3 が `:119` を書き換えるため追随の要否を決める必要がある。
9. **`nablarch-testing` のピン `e21bf67` は `main` のコミット**。steering.md Rules は「各モジュールの事実確認は PR ブランチを参照点にする。`main` を参照点にしない」と定める。当該主張（junit 4.13.1 compile）は PR ブランチ `convert-testdata-excel-to-text`（`dcaed44`）でも `pom.xml:151`-`:154` が同一のため結論は変わらないが、ピンは PR ブランチへ差し替えるのが規則に沿う。
10. **`support.testName` は JUnit 4 の型を露出する**（反例1 の解決策に伴う）。`org.junit.rules.TestName`。アーキタイプが採っている書き方をそのまま持ち込むと、JUnit 5 を標準と名乗るページに JUnit 4 の型名が現れる。

## フェーズ1 実施記録（2026-08-31）

指示書 §10（フェーズ0 承認・反例10件への回答）を §1〜§7 に優先して適用した。

### 参照ピン（フェーズ1 で実際に使ったもの）

| リポジトリ | ピン | 実測（本セッション） |
|---|---|---|
| `nablarch-testing-junit5` | `c06ebe8` | worktree `~/work/nablarch/nablarch-testing-junit5/.claude/worktrees/fix-resolveTestRules` の HEAD が `c06ebe8` |
| `nablarch-single-module-archetype` | `9ef4096` | scratchpad へ再 clone。HEAD が `9ef4096139bad64acf5fb91427e92fb430d1ee9d` |
| `nablarch-testing` | `dcaed44`（§10 反例9 で `e21bf67` から差し替え） | `git show dcaed44:pom.xml` の `:150`-`:155` が `junit:junit` 4.13.1 `compile` |
| `nablarch-testing-rest` | `9ada31e` | `readTextResource` の可視性の根拠に使用 |

### コミット

| commit | 範囲 |
|---|---|
| `40fee4b8` | §1〜§3（ページの改名・新設・about の反転・図2枚の再生成） |
| `6383045b` | §4（implementation 9ページ・java ブロック65件・tip 6件） |
| `b7feb866` | §5（design.md・mapping 5ファイル・tools 2ファイル） |
| `348c3200` | §7-4 の実コンパイルで検出した `readTextResource` の是正 |
| `8ad0dfc9` | §7-7 の Docker ビルドで検出した見出し罫線の是正 |

### フェーズ0 の全件表からの逸脱

フェーズ0 の全件表は 65件を A/B/C/D/E に分類していたが、実作業で次の3点を追加で処置した。

1. **`rest.rst` の `readTextResource`（フェーズ0 分類 C「そのまま」）は `protected` だった。**
   `nablarch-testing-rest@9ada31e` `SimpleRestTestSupport.java:333` が `protected String readTextResource(String)`、
   `:343` が `public String readTextResource(Class<?>, String)`。フェーズ0 の可視性実測は
   `nablarch-testing` の jar だけを対象にしており、`nablarch-testing-rest` のクラスを含めていなかった。
   §10 反例2（`web.rst:294`）と同型のため、同じ処置（`public` の `Class<?>` 版へ差し替え、
   シグネチャ列挙と直前の地の文も追随）を適用した。§7-4 の実コンパイルで検出（`348c3200`）。
2. **地の文の「スーパクラス」49件・「継承」の記述。** 継承が前提でなくなったことで事実に反するため、
   implementation 6ページで「サポートクラス」等へ改めた。全件表は `code-block` だけを母集合にしており、
   地の文の追随は §4 の指示にも入っていなかったが、書き換えの直接の帰結であるため同一タスクで処置した
   （steering.md Rules「見つけた欠陥は、そのタスクの中ですぐ直す」）。
3. **`standard_usage.rst` に下位ラベルを2件追加。** `standard_usage-base_uri`（`BasicHttpRequestTestTemplateを使用する`）と
   `standard_usage-extension`（`拡張例`）。§4 が `web.rst` の `getBaseUri` 節から「重複させず `:ref:` で送る」ことを
   指示しており、送り先に見出しラベルが要るため。S-08 の `<ページ先頭ラベル>-<内容>` に従う。
   0-3 の実測で `standard_usage` を含む既存ラベルは0件のため衝突なし（本セッションでも全 `ja/` のラベル1,018件が
   ユニークであることを再実測）。

### 用語「サポートクラス」の導入

指示書 §1・§2・§3 が使う語であり、`standard_usage.rst` の機能概要で `TestSupport` などを指す語として
導入した（「（以下、サポートクラス）」）。`mapping/glossary.md` §5 への語彙登録は行っていない。
`glossary.md` §5.12 は「設定・ツール」の名称の枠であり、本語は枠の名称ではなくクラス群の総称であるため。
**ディレクターの判断が要る項目**（後述）。

## Completion Criteria

指示書 §7 の1〜12（§10 反例3 により完了条件5 の除外範囲を差し替え）。

| Criterion | Self-check | Evidence |
|---|---|---|
| 1. フェーズ0 の 0-1〜0-6 が全件表で記録され、ディレクター OK を得ている | OK | 本ファイル「フェーズ0 実施記録」。承認は指示書 §10 |
| 2. `junit5_extension` が0件 | OK | `grep -rn 'junit5_extension' ja/ --exclude-dir=_build` → 0件（exit 1） |
| 3. アノテーション・Extension・サポートクラス名の1件ずつの一致 | OK | `git ls-tree -r c06ebe8 src/main/java` の FQCN 23件と、`ja/` 配下の `:java:extdoc:` が参照する `nablarch.test.junit5.*` の FQCN 23件が完全一致（集合として同一） |
| 4. 代表例の実コンパイル | OK | `c06ebe8` のソースを scratchpad へ `git archive` して `mvn -o -DskipTests install`（worktree のままでは `git-commit-id-plugin` が HEAD を読めず失敗する）。同プロジェクトの `src/test/java/doc/` に代表例7種を置き `mvn -o clean test-compile -Djacoco.skip=true` → `BUILD SUCCESS`（test 52ソース）。補完箇所は各ファイル冒頭のコメントに記録 |
| 5. JUnit 4 語彙の残存走査 | OK | §7-5 のコマンドのヒットは `setup/junit4.rst` 全件と `setup/standard_usage.rst` の `:222`・`:288`・`:391`・`:393`・`:426`。後者はすべて `拡張例`（`:206` 以降）の中で、§10 反例3 の除外範囲に収まる |
| 6. `:ref:` の全解決・段落内改行 0件 | OK | ラベル定義1,018件はすべてユニーク（重複0）。`testing_framework` 配下の `:ref:` に未解決0件。段落内改行の疑い20件はいずれも simple table の行・`- ` 箇条書き・番号付きリストの誤検出で、実体0件 |
| 7. Docker フルビルド | OK | `build succeeded.`／`WARNING:`・`ERROR:`・`SEVERE:` 0件。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`。`_build/html` で新2ページ・図2枚・toctree の並びを確認（図2枚は `ja/` 側と md5 一致） |
| 8. `verify_mapping.py`・`verify_glossary.py`・`_batch` 連結 | OK | `verify_mapping.py` → `OK: no errors`。`verify_glossary.py` → `RESULT: OK`。`_batch/batch-*.csv` の昇順連結（2件目以降はヘッダ1行を落とす）が `mapping.csv` とバイト一致（287,881 bytes）。597行 / 12,986 / 11,983 不変 |
| 9. `.png` 2枚の再生成 | OK | temurin-17 ＋ `plantuml-1.2025.4.jar` で再生成。`extension_class.png` `6b56372b…`→`2a0e8c14…`、`test_support_class.png` `6b365357…`→`c98514d5…` |
| 10. 差分範囲ゲート | OK | 各コミット後の `git status --porcelain` が空。`sphinx.mo`・`build.log`・`ca.crt`・`Dockerfile.ca` の混入なし（`build.log` は scratchpad へ出力） |
| 11. 修正意図ごとに1コミットし push 済み | OK | 上記5コミット。`--amend`・force push なし |
| 12. 記録が本ファイルにあり §9 の報告をして停止 | OK | 本ファイル。報告はチャット本文 |

## ディレクター判断が要る項目（フェーズ1） — 回答済み（指示書 §11-4・§11-5）

1. **用語「サポートクラス」を `mapping/glossary.md` §5 に登録するか。** 現状は未登録。
   `standard_usage.rst`・`junit4.rst`・implementation 6ページ・`about/index.rst`・`test_support_class.puml` で使っている。
   登録する場合は §5 のどのカテゴリに置くかの判断が要る（`設定・ツール` は名称の枠、
   `セクションタイトル` はページ構成の枠で、いずれも当てはまらない）。
   → **回答（§11-4）: 登録しない。** `glossary.md` §3 の掲載基準①②のいずれにも該当しない。作業不要。
2. **`_build/html` に旧ページ `setup/junit5_extension.html`（2026-08-31 08:38 のビルド成果）が残っている。**
   `_build/` はホスト側から消さない規則（`03-検証スクリプト.md` §5）のため触っていない。
   → **回答（§11-5）: §11-3 の `_build` 作り直しで解消する。** 下の「是正ラウンド1 実施記録」のとおり解消済み。

## 是正ラウンド1 実施記録（2026-08-31）— 指示書 §11

### 11-1 `setup/request_unit_test/web.rst:232` の第1文

差し替え前: ``` ``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのテストクラスのスーパクラスである。 ```
差し替え後: ``` ``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのサポートクラスである\ ``BasicHttpRequestTestTemplate``\ のスーパクラスである。 ```

同段落の第2文以降・`:230` は変更していない（`git diff` は当該1行のみ）。
根拠は一次情報で追認した。`~/work/nablarch/nablarch-testing`（HEAD `dcaed44`）の
`src/main/java/nablarch/test/core/http/BasicHttpRequestTestTemplate.java:15` =
`public abstract class BasicHttpRequestTestTemplate extends AbstractHttpRequestTestTemplate<TestCaseInfo>`。

### 11-2 `setup/request_unit_test/rest.rst:62`

「を継承したテストクラスで」→「を使用するテストクラスで」。同文の他の部分は変更していない。
是正後、同ファイルに `を継承したテストクラスで` は0件（`grep -c` → 0）。

### 11-3 `_build` の作り直し

1. 削除（docker の中から。ホスト側 `rm` は使っていない）:
   `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; rm -rf _build"`
   → 実行後 `ls -d _build` が `No such file or directory`
2. フルビルド（正規の場所 `~/work/nablarch/nablarch-document`。`03-検証スクリプト.md` §9.5 のコマンド）:
   `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"`
   → 終了コード 0・`build succeeded.`。ログは scratchpad の `build55.log` へ出力（作業ツリーに `build.log` を作っていない）
3. ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`、`rm -f build.log ca.crt Dockerfile.ca`

### 完了条件（是正ラウンド1）

| Criterion | Self-check | Evidence |
|---|---|---|
| 1. `ja/` の差分が 11-1・11-2 の2文に限られる | OK | `git diff --stat` = `rest.rst 2 +-` / `web.rst 2 +-` の2ファイルのみ、計 2 insertions / 2 deletions |
| 2. `build succeeded.`・WARNING/ERROR/SEVERE 0件、`_build/html/.../setup/junit5_extension.html` が存在しない | OK | ログ末尾 `build succeeded.`。`grep -c` で `WARNING` 0件・`ERROR` 0件・`SEVERE` 0件（`error` の小文字ヒット26件はすべて `..._error_process` 等のファイル名）。`ls` → `No such file or directory`。`setup/` 直下は `class_unit_test.html`・`common.html`・`deal_unit_test/`・`index.html`・`junit4.html`・`master_data_restore.html`・`request_unit_test/`・`standard_usage.html` の8エントリで、`junit5_extension.html` は無い |
| 3. `sphinx.mo` を復元し `git status --porcelain` が空 | OK | 復元後の `git status --porcelain` は是正2ファイルのみを表示し、コミット後は空 |
| 4. 実測を本ファイルに追記し、修正意図ごとに1コミットで push、報告して停止 | OK | 是正2文で1コミット、本記録で1コミット。`--amend`・force push なし |

是正2文の HTML 反映も実体で確認した。
`_build/html/.../request_unit_test/web.html` に
`サポートクラスである<code class="docutils literal"><span class="pre">BasicHttpRe...`、
`.../rest.html` に `RestTestSupport</a>を使用するテストクラスで` が出ている。

## 是正ラウンド1 のディレクター検証（差分限定2観点。2026-09-01）— 合格

観点A（是正が指示範囲に収まっているか）・観点B（新しい欠陥を生んでいないか）を、記録を根拠にせず一次情報で再実測した。**両観点とも合格。是正2文以外の変更・新しい欠陥は無い。**

| # | 確認事項 | 判定 | 実測（ディレクター） |
|---|---|---|---|
| A-1 | 差分が指示の2文に限られる | OK | `git show 96b59626 --stat` = `rest.rst | 2 +-` / `web.rst | 2 +-` の2ファイルのみ（2 files changed, 2 insertions(+), 2 deletions(-)）。他ファイルの変更0件 |
| A-2 | §11-1 の逐語一致 | OK | 差し替え後の `web.rst:232` 第1文が指示書 §11-1 のコードブロックと1文字一致。第2文以降と `:230` は差分に現れない |
| A-3 | §11-2 の逐語一致 | OK | `rest.rst:62` は「を継承した」→「を使用する」の1語のみ置換。同文の他部分は差分に現れない |
| A-4 | コミット・push の作法 | OK | `96b59626`（是正2文）→ `a7fe1add`（記録）の線形2件。`--amend`・force push なし。`origin/ntf-yaml-support` = `bd75933a` で push 済み |
| B-1 | §11-1 の根拠が一次情報で成立する | OK | `git show dcaed44:src/main/java/nablarch/test/core/http/BasicHttpRequestTestTemplate.java` `:15` = `public abstract class BasicHttpRequestTestTemplate extends AbstractHttpRequestTestTemplate<TestCaseInfo>`。`dcaed44` は PR ブランチ `convert-testdata-excel-to-text` 上（`git branch -a --contains` で確認）。`src/main` で `AbstractHttpRequestTestTemplate` を継承する実クラスは `BasicHttpRequestTestTemplate` の1件のみ（`git grep 'extends AbstractHttpRequestTestTemplate' dcaed44 -- src/main` のヒットは他に Javadoc の例示1件のみ） |
| B-2 | 用語「サポートクラス」の使い方が解説書内で整合する | OK | `setup/standard_usage.rst:12` が「サポートクラス」を定義し、同 `:49` の一覧表に `BasicHttpRequestTestTemplate` が載っている。是正文の呼称はこの表と一致する |
| B-3 | 同種の欠陥（継承を前提にした文）の残存 | 0件 | `grep -rn '継承' ja/development_tools/testing_framework --include='*.rst'` の全ヒットを分類。`setup/junit4.rst`（JUnit 4 の説明）・`setup/standard_usage.rst`（拡張例＝サポートクラスを継承して拡張する手順）・`implementation/*` の「JUnit 4では継承」注記6件・クラス階層の事実（`rest.rst:17`・`:52` の `RestTestSupport` が `SimpleRestTestSupport` を継承）・`setup/request_unit_test/web.rst:230`（拡張時の継承）のみ。標準の使い方でテストクラスが継承する前提の文は残っていない |
| B-4 | RST の記法（段落内改行・エスケープ） | OK | 是正2行はいずれも1段落1行。インラインリテラル前後の `\ ` エスケープが揃っている。下の B-5 のビルドが警告0件 |
| B-5 | フルビルドが清潔（独立再実行） | OK | ディレクターが `nablarch-document-build` で `sphinx-build -d /out/doctrees -b html ja /out/html`（出力先は scratchpad。`_build` に触れていない）を実行。終了コード0・`build succeeded.`・`WARNING` 0件・`ERROR` 0件・`SEVERE` 0件。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` |
| B-6 | 旧ページの残存と新ページの生成 | OK | 独立ビルドの出力にも `_build/html` 側にも `junit5_extension` を名前に含むファイルは0件（`find`）。`setup/` 直下に `standard_usage.html`・`junit4.html` が生成されている |
| B-7 | 是正2文が HTML に反映されている | OK | `_build/html/.../setup/request_unit_test/web.html` に「リクエスト単体テストのサポートクラスである`<code>`BasicHttpRequestTestTemplate…のスーパクラスである。」、`.../rest.html` に「を使用するテストクラスでデータベースを扱う場合」が1件。旧文はいずれも0件。したがって `_build` は是正後に作り直されている |
| B-8 | 作業ツリーの清潔 | OK | 独立ビルドと `sphinx.mo` 復元の後、`git status --porcelain` が空 |

**非是正の観察（1件・直さない判断）**: `web.rst:232` の第2文「アプリケーションプログラマが直接使用することはなく」は主語を持たず、直前の文の主題（`は` で受けた `AbstractHttpRequestTestTemplate`）を継ぐ。第1文の末尾に `BasicHttpRequestTestTemplate` が入ったため、字面上は後者を指す誤読の余地がある（後者はアプリケーションプログラマが使用する）。ただし主題の `は` が支配し、第3文が再び `AbstractHttpRequestTestTemplate` を明示して戻すため、既定の読みは正しい。是正の範囲を広げる価値はないと判断し、直さない。

## Overall Verdict

- Self-check: フェーズ1 完了（完了条件1〜12 すべて OK）。是正ラウンド1（§11-1〜11-3）完了（完了条件1〜4 すべて OK）
- ディレクター検証: 是正ラウンド1 の差分限定2観点（A・B）とも合格（2026-09-01）
- Ready to check off: user レビュー（38本の全量読み。指示書 §8 (c)）の承認待ち
