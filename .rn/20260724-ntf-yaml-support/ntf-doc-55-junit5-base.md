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
