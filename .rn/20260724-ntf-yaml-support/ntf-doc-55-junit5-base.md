# `#55` 作業指示 — NTF解説書の JUnit 5 ベース化

**user 確定（2026-08-31）**: NTF解説書を JUnit 5 ベースへ反転し、JUnit 4 は移行者・既存資産向けの記載に変える。構成は「`setup/junit5_extension.rst` を「標準の使い方」へ改題して `common` 直後へ移動＋「JUnit 4で使用する」ページを setup 末尾に新設」。実装例は合成アノテーション＋インジェクション方式へ。ファイル名・ラベルは user 確定（2026-08-31）: `setup/standard_usage.rst`（ラベル `standard_usage`）／`setup/junit4.rst`（ラベル `junit4_support`）。

**進め方**: フェーズ0（着手前検証。`.rst` は1文字も変更しない）→ 報告して停止 → ディレクター OK → フェーズ1（実装）→ 報告して停止 → ディレクターが独立検証。

**参照ピン**（すべて `git show <pin>:<path>` で読む。作業ツリーを根拠にしない）:

| リポジトリ | ピン | 用途 |
|---|---|---|
| `nablarch-document` | `764fb9fd`（`ja/` は HEAD と同一・クリーン。2026-08-31 実測） | 書き換え対象 |
| `nablarch-testing-junit5` | `c06ebe8`（`worktree-fix-resolveTestRules`。ローカル worktree `~/work/nablarch/nablarch-testing-junit5/.claude/worktrees/fix-resolveTestRules`） | アノテーション・クラス名の正 |
| `nablarch-single-module-archetype` | `9ef4096`（`main` HEAD。2026-08-31 実測） | 実装例の書き方の正（scratchpad に clone する） |
| `nablarch-testing` | `e21bf67` | JUnit 4 の依存関係の根拠 |

**このタスクは 4観点レビューを回さない**（user 判断 2026-08-31。§8 に理由と代替を記す）。

---

## フェーズ0 — 着手前検証（`.rst` を変更しない）

0-1. **本指示書の逐語・`file:line`・件数を、1件ずつピンの実物で検証する。** 反例（行番号ずれ・引用不一致・件数不一致・成立しない主張）が出たら、§1 以降に進まず全件を報告して停止する。

0-2. **`code-block:: java` の全件表を作る。** 母集合を先に固定する: `grep -rn 'code-block:: java' ja/development_tools/testing_framework --include='*.rst'`（ディレクターの実測 2026-08-31: implementation 9ページで65件＋`testdata_notation.rst` 1件）。各ブロックに「ファイル・行・内容の種類・処置（§4 の方式へ書き換え／断片として書き換え／対象外＋理由）」を付ける。

0-3. **新ラベル2件（`standard_usage`・`junit4_support`）を `ja/` 配下の全既存ラベルと突合し、衝突0件を確認する。** 母集合は実ファイルからの機械抽出（`checks/task-12.md` ゲート1 と同方式。`` .. _`ラベル`: `` のバッククォート形式も含める — `#49` の検証手段の注意）。

0-4. **`mapping.csv` の `dest_page=JUnit 5用拡張機能` 17行（`current-0178`〜`0180`・`0265`〜`0278`。ディレクター実測 2026-08-31）の新割当表を作る。** `current-0178`（JUnit Vintage・18行）と `current-0180`（依存関係の追加・42行）は `JUnit 4で使用する` へ、残り15行は `標準の使い方` へ（機械的改名）。各行がどの `_batch/batch-NN.csv` にあるかを特定する。

0-5. **3ページの見出しレベルの構成案を作る**（§1〜§3 の指定に従い、L2/L3/L4 の見出し文言まで。本文は書かない）: `standard_usage.rst`・`junit4.rst`・`about/index.rst`（変更節のみ）。

0-6. **アーキタイプ `9ef4096` に `junit-vintage` への依存が無いことを確認する**（`grep -rn vintage` 全 pom）。標準セットアップに vintage を含めない根拠。

0-7. 結果を報告して停止する（是正案があれば添える。`.rst`・`mapping/`・`design.md` は未変更のまま）。

---

## フェーズ1 — 実装（ディレクター OK 後）

### §1 `setup/junit5_extension.rst` → `setup/standard_usage.rst`「標準の使い方」

- `git mv` で改名する。H1 を「標準の使い方」、ページ先頭ラベルを `.. _standard_usage:` にする。
- 画像ディレクトリも `git mv`: `setup/images/junit5_extension/` → `setup/images/standard_usage/`（`extension_class.png`・`.puml`）。`.puml` の `title`「JUnit 5用拡張機能のクラスと、インスタンスの生成・インジェクション」から「JUnit 5用拡張機能の」を外した題（例:「Extensionクラスによるインスタンスの生成・インジェクション」）に改め、README「図の作成方法」の手順（temurin-17 絶対パス・`03-検証スクリプト.md` §9 と同じ）で `.png` を再生成する。
- `setup/index.rst` の toctree を「`common` → `standard_usage` → `class_unit_test` → （方式別） → `master_data_restore` → `junit4`」の順に改める。
- **機能概要を JUnit 5 標準の立場で書き直す**: テスティングフレームワークは `TestSupport` などの機能実装クラス（サポートクラス）を提供しており、標準の使い方では対応する合成アノテーションを付けると Extension がインスタンスを生成してテストクラスのフィールドへインジェクションする — を冒頭で言い切る。現 `:16` の「JUnit 4では、これらのクラスをテストクラスが継承することで、その機能をテストクラスから使用していた。」の過去形の対比は、\ :ref:`JUnit 4で使用する <junit4_support>`\ への1文の導線に置き換える。「本拡張機能」という自称は、このページが標準を名乗る以上使わない（ページ全体で言い換える）。
- 「依存関係を追加する」（現 `:80`）を標準セットアップとして書き直す: `org.junit:junit-bom` **5.11.0** を `dependencyManagement` に import し、`org.junit.jupiter:junit-jupiter` と `com.nablarch.framework:nablarch-testing-junit5` を `test` スコープで追加する（根拠: アーキタイプ `9ef4096` の `nablarch-web/pom.xml:247-248`（junit-bom 5.11.0）・`:361`（nablarch-testing-junit5）・`:367`（junit-jupiter）。vintage は含めない — 0-6）。既存 tip（`nablarch-testing` 推移・`nablarch-testing-rest` は optional）は残す。
- **「JUnit 4で書いたテストをJUnit 5上で実行する」節（ラベル `junit5_extension-vintage`・`:180`〜`:225` 付近）を丸ごと `setup/junit4.rst` へ移設する**（§2）。移設時に junit-bom の例 `:200-201` の `5.8.2` を `5.11.0` に揃える。
- それ以外（Extension・合成アノテーション一覧表 `:28`〜、前提事項 `:73` surefire 2.22.0、合成アノテーション設定 `:98`〜、BasicHttpRequestTestTemplate `:131`〜、RegisterExtension `:151`〜、拡張例 `:227`〜、**「JUnit 4のTestRuleを再現する」`:397`〜は移設せず拡張例に残す**（独自拡張の Extension 機構の説明であり、JUnit 4 のまま使う話ではない））は内容を保つ。文中の「JUnit 5用拡張機能」の自称・見出し・`:ref:` は改名に追随させる。

### §2 `setup/junit4.rst`「JUnit 4で使用する」を新設（setup 末尾）

ページ先頭ラベル `.. _junit4_support:`。S-02 に従い「機能概要 → 使用方法」。

- **機能概要**: テスティングフレームワークは JUnit 4 でも使用できる。JUnit 4 ではサポートクラスをテストクラスが**継承**して使う。既存の JUnit 4 テスト資産を持つプロジェクト向けであることを述べ、標準（JUnit 5）は\ :ref:`標準の使い方 <standard_usage>`\ へ導線を張る。
- **使用方法**:
  - 「依存関係」: 追加は不要である。`nablarch-testing` が `junit:junit` 4.13.1 を `compile` スコープで推移的に提供する（根拠: `nablarch-testing@e21bf67` `pom.xml:151`-`:155`）。
  - 「テストクラスを作成する」: 継承方式の最小例1つ（`public class ○○Test extends DbAccessTestSupport` 等）。各テストの書き方は第3部の各ページ（JUnit 5 の例）を読み替える旨を1文で述べる（読み替え規則: 合成アノテーション＋フィールド宣言 → 対応するサポートクラスの継承。対応表は\ :ref:`標準の使い方 <standard_usage>`\ の一覧表を参照）。
  - 「テストの実行前後に共通処理を行う」: `implementation/class_unit_test/component.rst:122`-`:146`（`@Before`・`@After`・`@BeforeClass`・`@AfterClass` の説明と、`@BeforeClass` の同名メソッド上書きの important・コード例）を**移設**する（§4）。
  - 「テスティングフレームワークのクラスを継承せずに使用する」: `component.rst:93`〜（`DbAccessTestSupport` を new して委譲する方法）を**移設**する（継承の単一性制約は JUnit 4 固有の事情のため。§4）。
  - 「JUnit 4で書いたテストをJUnit 5上で実行する」: §1 から移設（JUnit Vintage）。

### §3 `about/index.rst`（3箇所＋図タイトル）

- `:30`-`:48` 特徴4節「使い慣れたJUnitの書き方をそのまま活かせる」: `:32` の「JUnit 4を基盤としており」を JUnit 5 前提に書き直し、`:34`-`:46` のコード例を JUnit 5 スタイル（`class` 無修飾・`void`・`org.junit.jupiter.api.Test`）へ、`:48` の tip を `@BeforeEach`・`@AfterEach` へ改める。
- `:106` アーキテクチャ:「テスティングフレームワークを継承したテストクラスは」の継承前提を外す（例:「テスティングフレームワークを使用するテストクラスは」）。`:110`「テストクラスが継承するクラスの系譜を次に示す。」は、サポートクラスの系譜であること＋標準ではインジェクションで使うこと（JUnit 4 では継承する）が分かる導入文に改める。`about/images/index/test_support_class.puml` の `title`「テストクラスが継承するサポートクラスの系譜」を「テスティングフレームワークが提供するサポートクラスの系譜」に改め、`.png` を README の手順で再生成する。**この2箇所（`:106`・`:110`・図タイトル）は 2026-08-31 の影響実測の報告に無かった追加検出である。**
- `:119` 稼動環境: 反転する。ただし「JUnit 5をベースに動作する」とは書かない（実体は JUnit 4 基盤のフレームワークを Extension 経由で使う。事実を偽る）。案:「テスティングフレームワークは、JUnit 5で使用する（\ :ref:`標準の使い方 <standard_usage>`\ ）。JUnit 4で使用する場合は、\ :ref:`JUnit 4で使用する <junit4_support>`\ を参照。」

### §4 implementation 9ページ（java ブロック65件）と tip 6件

- 0-2 の全件表に従い、**テストクラス例をすべて合成アノテーション＋インジェクション方式へ書き換える。** 対応（`c06ebe8` の `src/main` 23クラスが正。ページの一覧表 `:28`〜 と一致）:

| 現行の継承 | 書き換え後 |
|---|---|
| `extends BasicHttpRequestTestTemplate`（web `:79`・`:114`） | `@BasicHttpRequestTest(baseUri = "…")` ＋ `BasicHttpRequestTestTemplate support;` |
| `extends RestTestSupport`（rest `:75`） | `@RestTest` ＋ `RestTestSupport support;` |
| `extends BatchRequestTestSupport`（request batch `:76`・`:94`、deal batch `:40`・`:66`） | `@BatchRequestTest` ＋ `BatchRequestTestSupport support;` |
| `extends MessagingRequestTestSupport`（request mom `:104`、deal mom `:56`） | `@MessagingRequestTest` ＋ `MessagingRequestTestSupport support;` |
| `extends MessagingReceiveTestSupport`（request mom `:122`） | `@MessagingReceiveTest` ＋ `MessagingReceiveTestSupport support;` |
| `extends DbAccessTestSupport`（component `:81`・`:163`・`:201`） | `@DbAccessTest` ＋ `DbAccessTestSupport support;` |
| `extends EntityTestSupport`（entity `:95`） | `@EntityTest` ＋ `EntityTestSupport support;` |

- 書き方の正はアーキタイプ `9ef4096` のサンプル（`nablarch-web/.../SampleActionRequestTest.java`・`nablarch-jaxrs/.../SampleApiTest.java` ほか）: クラスは `public` を付けない・テストメソッドは `void`（`public` なし）・`org.junit.jupiter.api.Test`・フィールド名は `support`。継承前提でメソッドを裸で呼んでいた断片（例: deal rest `:30`〜 の `get`・`sendRequest`・`assertStatusCode`）は `support.` 経由に改める。`@Before`/`@After` を使う例は `@BeforeEach`/`@AfterEach` へ。
- web.rst「ベースURIを返すメソッドを実装する」（`getBaseUri` のオーバーライド節）は、`@BasicHttpRequestTest(baseUri = …)` の属性指定の説明に書き換える（指定値が `AbstractHttpRequestTestTemplate#getBaseUri()` の返り値になる事実は `standard_usage` の該当節 `:131`〜 が既に持つ。重複させず `:ref:` で送る）。
- **component.rst**: `:93`〜「継承せずに使用する」と `:122`-`:146`「共通処理」の JUnit 4 固有部分を `setup/junit4.rst` へ移設し（§2）、component.rst 側には JUnit 5 での共通処理（`@BeforeEach`・`@AfterEach`・`@BeforeAll`・`@AfterAll`）の記述を残す。`#50` G2〜G4 で復元した見出しの検索性を落とさないこと（移設先にも見出しとして残る）。
- **tip 6件の反転**（web `:87`・rest `:93`・request batch `:100`・request mom `:133`・component `:91`・entity `:105`。全ページ同文）。差し替えの逐語:

  ```
  .. tip::

    JUnit 4\ でテストを書く場合は、インジェクションではなく継承でテスティングフレームワークの機能を使用する（\ :ref:`JUnit 4で使用する <junit4_support>`\ ）。
  ```

- 対象外: `testdata_notation.rst`・`testdata_examples.rst`・setup 方式別11ページ・tools 5ページ（テストクラス例なし。2026-08-31 走査済み。0-2 で再確認する）。

### §5 波及（同一コミット群で追随させる）

1. **design.md**: §2 の表 row 4「稼動環境」の記載内容（JUnit 5が標準・JUnit 4も使用可の事実のみ、詳細は「標準の使い方」「JUnit 4で使用する」へ譲る）／§3 の構成ブロック（`common` 直後に「標準の使い方」、末尾に「JUnit 4で使用する」）／§13 のツリー・第2部の1対1対応表（13→14ページ）・集計（34→35ページ）。**過去の経緯を記す節の中の旧名は書き換えない**（当時の記録）。本節の決定として「`#55`・user 承認 2026-08-31」を該当箇所に明記する。
2. **`mapping/vocabulary.md`**: 第2部の `dest_page` から「JUnit 5用拡張機能」を外し、「標準の使い方」「JUnit 4で使用する」を加える（13件→14件、全体34件→35件）。
3. **`mapping/_batch/*.csv` → `mapping.csv` 再生成**: 0-4 の割当表どおり `dest_page` を書き換える（直接編集禁止。昇順連結で再生成しバイト一致を確認）。597行 / 12,986 / 11,983 は不変。
4. **`mapping/volume.md`**: ページ別集計を追随（旧ページの行数を2ページへ分ける。合計不変）。
5. **`mapping/style.md` S-08**: 「作成済み（改名しない）」の表の `junit5_extension` 行を改名後（`標準の使い方`・`setup/standard_usage.rst`・`standard_usage`）に差し替え、`JUnit 4で使用する`・`setup/junit4.rst`・`junit4_support` の行を追加する。「改名しない」規則の直後に、本タスクが user 承認（2026-08-31）で例外として改名した旨を1文追記する。
6. **`mapping/glossary.md`**: §5.12 の `JUnit 5用拡張機能` の行（`:298`）を処置し、新ページ名2件を §5.12 に加える。**§5.15「`term-candidates.csv` との対応」の節は1文字も変更しない**（`:360` の `JUnit 5用拡張機能` は §5.15 側なので触らない）。
7. **`:ref:` 参照元**: `junit5_extension` を参照する8箇所（tip 6件は §4 で処置、`about/index.rst:119` は §3、`setup/index.rst:20` は §1）以外に参照が無いことを走査で確認する（`grep -rn 'junit5_extension' ja/ --exclude-dir=_build` が処置後 0件）。

### §6 やらないこと

- モジュール（`nablarch-testing-junit5` 含む5リポジトリ）の変更。**junit5 の `src/main` 変更なしで完結する**（2026-08-31 実測: 全サポートクラス11種に Extension・合成アノテーションあり）
- `.rst`・`.puml` への解説書参照・`file:line` の持ち込み（`02-進め方.md` の禁止事項）
- `mapping/mapping.csv` の直接編集／`mapping/glossary.md` §5.15／`ja/conf.py`／`en/` 配下／`locales/` の `.gitignore` 追加
- 本文の新しい主題の追加（本指示書が指定した反転・移設・書き換えの範囲を超えない）
- `_build/` の削除（ホスト側から消さない。`03-検証スクリプト.md` §5）

### §7 検証（完了条件）

1. フェーズ0 の 0-1〜0-6 が全件表で記録され、ディレクター OK を得ている
2. `ja/development_tools/testing_framework` 配下に `junit5_extension` が0件（ファイル名・ラベル・`:ref:` とも）
3. 書き換え後の全合成アノテーション・Extension・サポートクラス名が `nablarch-testing-junit5@c06ebe8` の `src/main` 実物と1件ずつ一致する（全件表）
4. **代表例の実コンパイル**: junit5 worktree（`c06ebe8`）から `JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64` で `mvn -o -DskipTests install` して `~/.m2` の 6-NEXT-SNAPSHOT を最新化し（現 jar は 2026-06-25 ビルドで古い）、scratchpad の検証用 Maven プロジェクトで、書き換え後の代表例（web・rest・batch・mom 送信・mom 受信・component・entity の7種。`.rst` から機械的に抜き出す）を `mvn -o test-compile` でコンパイルする。`// 中略` の補完は最小限とし、補完箇所を記録する。rest は `nablarch-testing-rest` を依存に加える
5. **JUnit 4 語彙の残存走査**: `grep -rnE '@RunWith|@Rule\b|@BeforeClass|@AfterClass|@Before\b|@After\b|org\.junit\.Test\b|extends (TestSupport|DbAccessTestSupport|EntityTestSupport|BasicHttpRequestTestTemplate|HttpRequestTestSupport|BatchRequestTestSupport|MessagingRequestTestSupport|MessagingReceiveTestSupport|RestTestSupport|SimpleRestTestSupport|IntegrationTestSupport)\b' ja/development_tools/testing_framework --include='*.rst'` の全ヒットを表にし、`setup/junit4.rst` と `setup/standard_usage.rst` の「JUnit 4のTestRuleを再現する」節の中のもの以外が0件
6. `:ref:` の全解決（独立走査。`` .. _`ラベル`: `` のバッククォート形式定義を母集団に含める）・段落内改行 0件
7. Docker フルビルドが `build succeeded.`・`WARNING:`／`ERROR:`／`SEVERE:` 0件。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`。`_build/html` の実体で新旧2ページ・図2枚の表示を確認する
8. `verify_mapping.py` が `OK: no errors`（597行 / 12,986 / 11,983 不変）、`verify_glossary.py` が `RESULT: OK`、`_batch` 連結が `mapping.csv` とバイト一致
9. `.png` 2枚（`extension_class`・`test_support_class`）が temurin-17 で再生成され、`.puml` から再現できる
10. 差分範囲ゲート: `git status --porcelain` の全件表で、予定ファイル以外が0件（`sphinx.mo`・`build.log`・`ca.crt`・`Dockerfile.ca` の混入なし）
11. 修正意図ごとに1コミットし push 済み。`--amend`・force push なし
12. 判断・実測の記録が `checks/task-55.md` にあり、フェーズ1 完了時に §9 の報告をして停止している（レビューは回さない。§8）

### §8 レビュー — 回さない（user 判断 2026-08-31）

サブエージェントの4観点レビューは回さない。公開本文に新しい記述が入るタスクだが、(a) 指示文の誤りはフェーズ0 の実物突合が拾う、(b) 書き換えの正解は `c06ebe8`・`9ef4096`・`e21bf67` の実物で機械的に決まり、ディレクターが独立検証（コンパイル・全件走査・突合の再実行）で判定する、(c) 最終レビューは user の38本全量読みが担う、が理由である。判断・実測の記録先は `checks/task-55.md`（`reviews/page-*.md` は新設しない）。

### §9 報告

フェーズ0 完了時と、フェーズ1＋レビュー完了時の2回、報告して停止する。報告には完了条件の実測結果（コマンドと出力の要点）を添える。解説書側が誤っていると判断した項目は直さず、根拠を添えて報告して止める。

### §10 フェーズ0 の判定と反例10件への回答（ディレクター。2026-08-31）

**フェーズ0 を承認する。フェーズ1 に着手してよい。本節の回答は §1〜§7 の記載に優先する。**

0-1〜0-6 はディレクターが scratchpad の clone とピンで独立に再実測し、全件一致した（`code-block:: java` 母集合85件のページ別内訳・ラベル母集合 raw 1,054件＝ユニーク1,053件（重複は `DatadogMeterRegistry(外部サイト、英語)` の1件で衝突判定に影響なし）・`dest_page=JUnit 5用拡張機能` 17行/475行・`batch-03.csv` 3行＋`batch-14.csv` 14行・アーキタイプ vintage 0件）。反例10件もすべて実物で追認した。

#### 反例1・反例10 — 引数なし `execute()` の3ブロック（request batch `:113`・request mom `:148`・deal batch `:47`）

**読み込み単位名をリテラルで渡す `support.execute("<そのテストメソッド名>")` に書き換える**（CC の推奨案を採用）。

- `execute(String)` は `public final`（`StandaloneTestSupportTemplate.java:56`、`dcaed44`）で確実に呼べる
- アーキタイプの書き方 `support.execute(support.testName.getMethodName())` は採らない。`testName` の型は `org.junit.rules.TestName`（`TestEventDispatcher.java:94`、`dcaed44`）で、JUnit 5 を標準と名乗るページに JUnit 4 の型を持ち込む（反例10）。解説書の既存例（request batch `:126`・deal batch `:57`）が既にリテラル方式であり、これに揃える。`TestInfo` 方式も採らない（JUnit 5 API の説明負担が増え、例の主題である読み込み単位から焦点がずれる）
- **web は対象外。** `AbstractHttpRequestTestTemplate` の `execute` 8種は全部 `public`（`:118`-`:191`、`dcaed44`）なので、web.rst のブロック3は `support.execute()` のままでよい（`:182` の地の文も真のまま）。リテラル化するのは standalone 系（batch・mom）の3ブロックだけ
- 地の文・コメントの追随（ディレクター全件走査 2026-08-31。「引数なし」のヒットはこの5件で全部）: request batch `:120`（説明の主軸を「`execute` には読み込み単位の名前を渡す。名前はテストメソッド名と同じにする」へ）・`:126` の行末コメント・request mom `:143`-`:146`（箇条書きから `void execute()` を落とし `void execute(String sheetName)` のみに。`:146` の「引数なしを使用するとよい」を書き換え）・`:152` の行末コメント・deal batch `:55`（複数単位の記述は保つ）・`:89`（「引数なしの `execute` を1回呼ぶだけ」の部分を追随）
- アーキタイプとの差異（アーキタイプ側が JUnit 4 の型を露出している件)は申し送り。本タスクでは扱わない

#### 反例2 — `web.rst:294` のシグネチャ

**4引数の `public` 版に差し替える。** 逐語:

```
HttpResponse execute(Class<?> testClass, String caseName, HttpRequest req, ExecutionContext ctx)
```

直前の地の文 `:292` を追随させる: 第1引数にはテストクラス（自身のクラスを `getClass()` で渡す。クラス名が HTML ダンプの出力ディレクトリの決定に使われる）、第2引数に指定した名前が HTML ダンプのファイル名になる。根拠: `HttpRequestTestSupport.java:237`-`:250`（`dcaed44`）。3引数版 `:144` は `protected` で、内部で `execute(testClass, …)` へ委譲している。

#### 反例3 — 完了条件 §7-5 の除外範囲

次のとおり差し替える: 「`setup/junit4.rst` 全体と、`setup/standard_usage.rst` の L2『拡張例』節全体の中のもの以外が0件」。（現 `junit5_extension.rst:243` `extends TestSupport`・`:309` `extends BasicHttpRequestTestTemplate` は §1 が内容を保つと指定した独自拡張クラスの作成例で、必ず走査に残るため。）

#### 反例4 — 下位ラベルの新名称

**`standard_usage-inject`（現 `:98`）・`junit4_support-vintage`（現 `:180`）で確定**（衝突0件は 0-3 とディレクター再実測の両方で確認済み）。参照元の `:ref:` も追随させる。

#### 反例5 — `current-0180` の割当

**§5-3 のとおり `JUnit 4で使用する` へ割り当てる（変更なし）。** `current-0180` の実体は JUnit Vintage 有効化の依存関係（vintage-engine を含む）であり、移設先は vintage 節を引き受ける `junit4.rst` が正しい。一方 `standard_usage.rst` の「依存関係を追加する」に書く junit-bom 5.11.0＋junit-jupiter は現行解説書に由来しない**新規記述**（根拠はアーキタイプ `9ef4096` `nablarch-web/pom.xml:245`-`:250`・`:358`-`:369`）。`mapping.csv` は現行→刷新の対応表であり、新規記述に行は要らない。2ページに依存関係の記述が現れるが、内容が異なる（標準セットアップ／vintage 併用）ため矛盾ではない。

#### 反例6 — `style.md:414`

**§5-5 の対象に加える。** `:414` の `setup/junit5_extension.rst:30` への参照を改名後のパスに差し替え、行番号と件数（33件）は書き換え後に再実測して追随させる。

#### 反例7 — `volume.md`

**集計の行は追随させ、経緯の文は書き換えない**（design.md と同じ規則を volume.md にも適用する）。`:26` のページ別集計行は §5-4 のとおり2行に分割する（`標準の使い方` 415行・`JUnit 4で使用する` 60行。0-4 の実測）。既存の備考文（経緯）は「標準の使い方」側の行に残し、両行の備考に `#55` で分割した旨を追記する。`:31`・`:73`・`:75`・`:94`・`:145` と備考欄の文中に現れる旧名「JUnit 5用拡張機能」は当時の記録なので書き換えない。

#### 反例8 — `design.md:211`

**当該節（`:193`「モジュール一覧は第1部に置かない…」）は 2026-08-05 の決定記録なので本文は書き換えない。** 節末に上書きの明記を1段落追加する: この節が定めた「稼動環境」の文面（JUnit 4 ベース＋JUnit 5用拡張機能への `:ref:`）は `#55`（user 承認 2026-08-31）で上書きし、現在の仕様は §2 表 row 4 と `setup/standard_usage.rst`・`setup/junit4.rst` にある、の旨。

#### 反例9 — `nablarch-testing` のピン

**`dcaed44`（PR ブランチ `convert-testdata-excel-to-text` の HEAD。2026-08-31 実測）へ差し替える。** フェーズ1 で `nablarch-testing` を引用するときはすべて `dcaed44` を使う。§2 の依存関係の根拠は `nablarch-testing@dcaed44` `pom.xml:150`-`:155`（`junit:junit` 4.13.1 `compile`。ディレクターが `git show` で `e21bf67` と同一内容であることを確認済み）。

#### 記録

フェーズ0 の指摘10件＝方式不成立2・指示書の穴6・規則との食い違い1・型の露出1。いずれも成果物ではなくディレクターの指示文への指摘（`nablarch/CLAUDE.md` 3-4 の型）。全10件をディレクターが一次情報（`dcaed44`・`9ef4096`・`764fb9fd` の `git show`／自分の grep）で追認したうえで回答した。


### §11 フェーズ1 の判定 — ディレクター独立検証の結果と是正2件（ディレクター。2026-08-31）

**完了条件2〜11 をディレクターが独立に再実測し、すべて合格した。** フェーズ1 で CC が追加処置した3点（`readTextResource` の差し替え・「スーパクラス」49件・下位ラベル2件）も一次情報で追認した。ただし、§4 の反転が波及した文が setup 2ページに残っている（11-1・11-2。#55 自身の変更が作った不整合のため本タスクで直す。ラウンド1指摘2件・観点B）。**11-1〜11-3 を行い、報告して停止する。** 11-4・11-5 は CC の判断依頼への回答（11-4 は作業不要、11-5 は 11-3 に含む）。

ディレクターの実測（scratchpad の GitHub clone、先端 `49db8f6`。ピン: junit5 `c06ebe8`・testing `dcaed44`・rest `9ada31e`）: `junit5_extension` 0件／`:java:extdoc:` の junit5 FQCN 23件が `c06ebe8` の `src/main` 23件と集合一致／代表例7種を `.rst` から独立に抽出し junit5 プロジェクトで `mvn -o test-compile` → BUILD SUCCESS（rest 例のため jsonassert 1.5.0・json-path-assert 2.4.0・json 20230618 を test 依存に追加して補完）／JUnit 4 語彙の残存は `junit4.rst` 全件と `standard_usage.rst` 拡張例内5件（`:222`・`:288`・`:391`・`:393`・`:426`、拡張例 L2 は `:207`〜）のみ／ラベル定義ユニーク・NTF の `:ref:` 未解決0件／Docker フルビルド `build succeeded.`・WARNING/ERROR/SEVERE 0件・新2ページと図2枚（`_images/`）を実体確認／`verify_mapping.py` OK（597/12,986/11,983 不変）・`verify_glossary.py` RESULT: OK・`_batch` 連結バイト一致／`.png` 2枚を temurin-17 で再生成し md5 一致／コミット連鎖は線形5件＋記録、作業ツリークリーン。

#### 11-1 是正: `setup/request_unit_test/web.rst:232` の第1文

現行第1文「``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのテストクラスのスーパクラスである。」は、標準の使い方（テストクラスは継承しない）と矛盾する。**第1文だけ**を次の逐語に差し替える（同段落の第2文以降・`:230` は変更しない）:

```
``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのサポートクラスである\ ``BasicHttpRequestTestTemplate``\ のスーパクラスである。
```

根拠: `BasicHttpRequestTestTemplate.java:15`（`nablarch-testing@dcaed44`）`public abstract class BasicHttpRequestTestTemplate extends AbstractHttpRequestTestTemplate<TestCaseInfo>`。

#### 11-2 是正: `setup/request_unit_test/rest.rst:62`

「を継承したテストクラスで」を「を使用するテストクラスで」に差し替える（同文の他の部分は変更しない）。継承は JUnit 4 の使い方に限られるため（`setup/junit4.rst`）。

#### 11-3 後始末: `_build` の作り直し（正規の場所）

旧ページ `junit5_extension.html` が `_build/html` に残っている件は、`_build` を **docker の中から**削除し、正規の場所（`~/work/nablarch/nablarch-document`）でフルビルドして解消する（`03-検証スクリプト.md` §5「作り直すときは docker の中から消す」・§9.5）。ホスト側から `rm` しない。ビルド後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`。

#### 11-4 回答: 用語「サポートクラス」は `glossary.md` §5 に登録しない

`glossary.md` §3 の掲載基準（①表記揺れが実在する ②`design.md` が章・セクション名として使う）のどちらにも該当しない。揺れ候補（`機能実装クラス`・`支援クラス` 等）はディレクターの走査で `ja/` に0件、`サポートクラス` はセクション名でもない。現状の未登録が正しい。作業不要。

#### 11-5 回答: `junit5_extension.html` の残存は 11-3 で解消する

#### 完了条件（是正ラウンド1）

1. `ja/` の差分が 11-1・11-2 の2文に限られる（`git diff --stat` で当該2ファイルのみ）
2. 11-3 後、`build succeeded.`・WARNING/ERROR/SEVERE 0件、かつ `_build/html/development_tools/testing_framework/setup/junit5_extension.html` が存在しない
3. `sphinx.mo` を復元し、`git status --porcelain` が空
4. 実測を `checks/task-55.md` に追記し、修正意図ごとに1コミットで push、報告して停止する（レビューは回さない。§8。是正の検証はディレクターが差分限定2観点で行う）
