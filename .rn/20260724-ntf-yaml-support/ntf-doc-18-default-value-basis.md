# 作業指示: `#18` デフォルト値の基準を実効値に統一し、`design.md` に2件を規定する

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-18-default-value-basis.md`

対象ブランチ: **`nablarch/nablarch-document` の `ntf-yaml-support`。** フォーク（`lovaizu/nablarch-document` の `work`）での作業は PR #730 のマージをもって終了する。**クローンの向き先を切り替えてから着手すること。**

マージはマージコミットを作る方式で行うため、**これまでの記録が出典としている commit hash はすべてそのまま有効である**（`4f78d11`・`9e90f4e`・`783eaac`・`04d8545` など）。読み替えは不要。マージ前の HEAD は `6274d6d`、`#17` の記録コミットは `9e90f4e`、最終内容コミットは `4f78d11`。

`steering.md` に作業ブランチを `work` と書いている箇所があれば、`ntf-yaml-support` に更新すること。

**ページを作らないタスクである。** `#17` の `decide` 2件を規定として `design.md` に定着させ、承認済みの `web.rst`・`common.rst` に残っている食い違いを是正する。残り27ページの設定項目表に効く。あわせて `#17` の user review のステータス記録を訂正する（STEP 6-4。`/rn:gm` と記録されているが実際は `/rn:ty`）。

`mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `style.md` / `ja/conf.py` は変更しない。新しいページを作らない。

---

## 背景 — 何が食い違っているか

`nablarch-testing` のデフォルト値には2つの水準がある。

1. **クラスのフィールド初期値** — `HttpTestConfiguration.java:29` の `webBaseDir = "../main/web"` など
2. **デフォルト設定を読み込んだ実効値** — `nablarch-testing-default-configuration` の `nablarch/test/http-request-test.xml` が `${...}` を設定し、`nablarch/test/http-request-test/http-request-test.config` が値を与える

**読者が実際に目にするのは 2 である。** ウェブアプリケーションのブランクプロジェクトは `nablarch/test/http-request-test.xml` を、RESTfulウェブサービスのブランクプロジェクトは `nablarch/test/rest-request-test.xml` を読み込む（`nablarch-web-archetype-6u3` / `nablarch-jaxrs-archetype-6u3` の `archetype-resources/src/test/resources/unit-test.xml`）。

`#15` が `web.rst` を作ったとき、`nablarch-testing` の `src/main/` だけを探索し、デフォルト設定が別モジュールにあることに気づかなかった。その結果 1 を採った。`#17` の `rest.rst` は 2 を採っている。

**2 が正しい。** 出典自身が REST 側で実効値を書いており（`RequestUnitTest_rest.rst:288` の `src/main/webapp`）、ウェブ側でも `htmlChecker`・`htmlCheckerConfig` は実効値相当を書いている（`02_RequestUnitTest.rst:345`・`:351`）。いずれも `2e501ad` から取得した。

実効値を基準にしても、読者が同名で上書きしたときに矛盾しない。同名・同クラスのコンポーネント定義は**プロパティ単位でマージ**され、後の定義に無いプロパティは先の定義の値が残る（`nablarch-core-repository`（`6a28491`）の `src/main/java/nablarch/core/repository/di/config/xml/XmlComponentDefinitionLoader.java:214`・`:238-273`・`:283-328`。既定ポリシーは `:119` の `DuplicateDefinitionPolicy.OVERRIDE`）。

---

## 参照する実物と、確認済みの `file:line`

参照点は次のとおり。**同じ調査をやり直さなくてよい。** 記載を変えるときは、この表の値を根拠として `checks/task-18.md` に引き写すこと。

| リポジトリ / 成果物 | 参照点 |
|---|---|
| `nablarch/nablarch-testing` | `main`（`e21bf67`） |
| `nablarch/nablarch-testing-rest` | `b7729df` |
| `nablarch/nablarch-core-repository` | `6a28491` |
| `com.nablarch.configuration:nablarch-testing-default-configuration` | **6u3**（Maven Central。`https://repo1.maven.org/maven2/com/nablarch/configuration/nablarch-testing-default-configuration/6u3/`） |
| `com.nablarch.archetype:nablarch-web-archetype` / `nablarch-jaxrs-archetype` | **6u3**（同） |

デフォルト設定の実効値は、jar 内の次の2ファイルの組で決まる。

- `nablarch/test/http-request-test.xml`（プロパティの割り当て）
- `nablarch/test/http-request-test/http-request-test.config`（値）

## STEP 1 — `web.rst` の設定項目表を実効値に改める

対象は `ja/development_tools/testing_framework/setup/request_unit_test/web.rst` の「コンポーネント設定ファイルに設定項目を登録する」の `list-table`（`:18`〜`:82`。ヘッダ1行＋設定項目19行）。

レビュー役が実測した**不一致9件**は次のとおり。**この表を鵜呑みにせず、STEP 5 のゲート1で全19行を自分で照合すること。**

| `web.rst` の行 | 設定項目 | 現在の記載 | 実効値 | 実効値の出典 |
|---|---|---|---|---|
| `:29` | `webBaseDir` | `../main/web` | `src/main/webapp` | `http-request-test.xml:15` → `http-request-test.config:1` |
| `:47` | `sessionInfo` | 該当なし | `commonHeaderLoginUserName` = `リクエスト単体テストユーザ`、`commonHeaderLoginDate` = `20100914` | `http-request-test.xml:19-25` → `.config:3-4` |
| `:50` | `htmlResourcesExtensionList` | `css`・`js`・`jpg`（3件） | `css`・`jpg`・`js`・`less`・`png`・`template`・`woff`・`eot`・`svg`・`ttf`（10件） | `http-request-test.xml:36-49` |
| `:53` | `jsTestResourceDir` | `../test/web` | `src/test/webapp` | `http-request-test.xml:16` → `.config:2` |
| `:65` | `htmlChecker` | 該当なし | `Html4HtmlChecker`（`htmlCheckerConfig` の設定に伴って自動的に設定される） | `HttpTestConfiguration.java:358-360`（`setHtmlCheckerConfig` が `new Html4HtmlChecker(...)` を代入する） |
| `:68` | `htmlCheckerConfig` | 該当なし | `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` | `http-request-test.xml:29-30` → `.config:5` |
| `:71` | `ignoreHtmlResourceDirectory` | 該当なし | `.svn` | `http-request-test.xml:59-62` |
| `:74` | `tempDirectory` | 該当なし（内蔵サーバ（Jetty）のデフォルト動作に従う） | `target/tmp` | `http-request-test.xml:65` → `.config:11` |
| （表外・`:216` の `tip`） | `htmlResourcesRoot` | `htmlResources` | `../htmlResources` | `http-request-test.xml:52` → `.config:7` |

**`htmlChecker` は特別扱いが要る。** デフォルト設定は `htmlChecker` を直接は設定しない。`htmlCheckerConfig` を設定した副作用として `Html4HtmlChecker` のインスタンスが入る。**「デフォルト設定が `htmlChecker` を設定する」とは書かないこと。**

## STEP 2 — 表の基準を本文で明示する

現在の導入文（`:16`）は「テスト用のコンポーネント設定ファイルに、`HttpTestConfiguration` を `httpTestConfiguration` という名前で登録する」としており、**デフォルト設定を読み込むことに触れていない。** このままでは実効値を載せる根拠が本文に無い。

`rest.rst:61` と**同じ構成**に改める。すなわち次の3点を述べる。

1. デフォルト設定（`nablarch/test/http-request-test.xml`）を読み込むと `HttpTestConfiguration` が `httpTestConfiguration` というコンポーネント名で登録されること
2. 実行環境に依存する設定値は、このコンポーネントを**同じ名前で上書き**して変更すること。上書きの記述はデフォルト設定の読み込みより後に置くこと
3. デフォルト値の欄が、**デフォルト設定を読み込んだ状態で有効になる値**であること

`rest.rst` と同じ趣旨を述べる箇所は、**同じ語彙・同じ語順で書くこと。** 2ページを並べて読んだときに差が意味を持たないようにする。

## STEP 3 — 表に連動する地の文3箇所を整合させる

表だけを直すと本文と矛盾する。次の3箇所を同時に直す。

| 行 | 現在の記述 | 問題 |
|---|---|---|
| `:86` の `important` | 「`checkHtml` を `true` のままにする場合は、`htmlChecker` と `htmlCheckerConfig` のどちらか一方を必ず設定する」 | デフォルト設定を読み込む前提では `htmlCheckerConfig` が既に設定済みで、「どちらも設定していない」状態が生じない。クラスの挙動としては正しいので、**削除せず、どういう場合に問題になるかが分かる形に直す** |
| `:102` の `tip` | 「`tempDirectory` を省略した場合、内蔵サーバ（Jetty）のデフォルト動作では `./work` がコンパイル先ディレクトリになる」 | デフォルト設定が `target/tmp` を入れるため、省略しても Jetty のデフォルト動作にはならない |
| `:104`〜`:155` の記述例 | 「デフォルト値と同じ値を明示的に記述している項目もある」とし、`webBaseDir` に `../main/web` を書いている | 表と矛盾する。`../main/web` はブランクプロジェクトに存在しないパスである（webapp は `src/main/webapp`） |

記述例（`:120`〜`:155`）は、**表と矛盾しない値に直す。** デフォルト値と異なる値を意図的に示している項目（`xmlComponentFile`・`tempDirectory` の `webTemp` など）は、そう読めるようにしてよい。**設定項目を増やしたり減らしたりしない。**

## STEP 4 — `common.rst` のテストデータ読み込み先を実効値に改める

`ja/development_tools/testing_framework/setup/common.rst:17` は「テストデータは、デフォルトでは `test/java` 配下から読み込まれる」としている。これは出典どおりであり（`03_Tips.rst:735`、`2e501ad`）、クラス定数とも一致する（`TestSupport.java:30` の `DEFAULT_RESOURCE_ROOT = "test/java/"`）。

しかし**デフォルト設定が `src/test/java` を与える**（jar 内 `nablarch/test/test-data.config` の `nablarch.test.resource-root=src/test/java`。`nablarch/test/test-data.xml` が `<config-file>` で読み込み、両アーキタイプの `unit-test.xml` がこれを `<import>` する）。

**`src/test/java` に改める。** 変更は当該1文に限る。`common.rst` の他のセクション・見出し・コードブロックは変更しない。

## STEP 5 — `design.md` §8 に2件を規定する

`#17` の `decide` 2件を規定として書き残す。既存の行は削除しない。**追加のみとする。**

### 5-1. 設定項目表のデフォルト値の基準

- **コンポーネント設定ファイルの設定項目一覧に載せる「デフォルト値」は、テスティングフレームワークのデフォルト設定（`nablarch-testing-default-configuration`）を読み込んだ状態で有効になる実効値とする。** クラスのフィールド初期値ではない
- 根拠は、ブランクプロジェクトがデフォルト設定を読み込むこと、および同名・同クラスのコンポーネント定義がプロパティ単位でマージされ、上書きしなかったプロパティにデフォルト設定の値が残ることである
- **表を持つページは、その基準を表の直前の地の文で明示する**
- フィールド初期値と実効値が食い違う場合、**実効値だけを載せる。** 両方を並べない

### 5-2. 出典が欠いている、実装上必須の設定の追記

- **出典にもマッピングにも無いが、それが無いとページに書かれた手順が動かない設定は、書き足してよい。** 「マッピングにない内容を追加しない」（§11.3）の例外とする
- 追記の根拠は、**実装で必須であることを確かめた結果**とする。確認した `file:line` とコミットハッシュを `reviews/page-*.md` に記録する
- 追記は**ページに書かれた手順を成立させるために必要なものに限る。** 出典が触れていない新しい主題を追加してよいという意味ではない
- `#17` の例: `httpServerFactory` の登録。デフォルト設定に含まれず（5u24〜6u3 の全版で0件）、未登録だと内蔵サーバの生成時に `IllegalConfigurationException` が発生する（`SimpleRestTestSupport.java:45`・`:298-300`）

## STEP 6 — 記録

1. `checks/task-18.md` を新規作成し、ゲートの実行出力を記録する
2. `reviews/page-request_unit_test_setting_web.md`・`page-common.md` に、是正の内容と根拠（`file:line` とコミットハッシュ）を追記する。**既存の記録は書き換えない。** `#15` の C-2・C-3（`htmlChecker`・`htmlCheckerConfig` を「該当なし」とした判断）が覆ったことを明記する
3. `steering.md` の `#18` エントリを、この作業指示の受領後の内容に更新する（`#17` の `DONE` 化と `#18` エントリの追加は `9e90f4e` で実施済み）
4. **`#17` の user review は `/rn:ty`（承認）である。`/rn:gm` と記録した3箇所を訂正する。** `checks/task-17.md` §6-1 の見出し、`steering.md` `#17` の「`decide` 2件の回答」冒頭と `Closed` 冒頭。回答に伴う是正作業が発生したことと、承認であったことは別である。記録の書き換えを禁じている対象は判断当時の記録であって、received したコマンドの取り違えはこれに当たらないため、直接訂正してよい

---

## ゲート

すべて実行結果で確認し、`checks/task-18.md` に記録すること。**全件表を求めるゲート1・2を実行順の先頭に置く。**

1. **`web.rst` の設定項目表の全19行について、「現在の記載」「デフォルト設定の実効値」「一致/不一致」「実効値の出典（`file:line`）」の全件表を作る。** 母集合は `list-table` から機械抽出する（`* - ` 行を数える。ヘッダを除いて19行であること）。**ホワイトリストで切り出さない。** 一致した行も理由を添えて表に載せる。本作業指示が挙げた9件と食い違う場合は、**実物を根拠に自分の判定を優先し、その旨を記録する**
2. **作成済み7ページ（`about/index.rst`・`implementation/testdata_notation.rst`・`implementation/testdata_examples.rst`・`setup/common.rst`・`setup/class_unit_test.rst`・`setup/request_unit_test/web.rst`・`setup/request_unit_test/rest.rst`）を全走査し、「デフォルト」「既定」を含む記述を全件抽出して、実効値と食い違っていないかを全件表で示す。** 非該当と判定したものも判定理由を添えて表に載せる。ゲート1・STEP 4 で扱った箇所以外に食い違いがあれば、**この作業指示の範囲外として `reviews/page-*.md` に記録し、是正しない**（範囲を広げない）
3. `git diff 6274d6d HEAD -- ja/` の変更が `setup/request_unit_test/web.rst` と `setup/common.rst` の2ファイルだけであること
4. `web.rst` の**見出しの文言と並び順が不変**であること。設定項目表の**行数・列構成・項目名と並び順が不変**であること（変えるのはデフォルト値の欄と、それに連動する説明・地の文だけ）
5. `common.rst` の差分が `:17` の1文に由来するものだけであること
6. `python3 mapping/tools/verify_mapping.py` が `exit 0`、**594行 / 12,986 / 11,983 が不変**
7. `git diff 6274d6d HEAD -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py` が**空**
8. `design.md` の差分が §8 の中だけに収まり、**既存の記述が削除されていないこと**（追記のみ。行単位の diff では末尾追記が `-1/+1` の対になりうるため、削除行数ではなく**削除された記述が0件**であることを内容で確認する）
9. `:ref:` の未定義参照が0件、段落内改行が0件
10. Docker でフルビルド（`-a`）し、`build succeeded` かつ警告が**既知の `db_double_submit.rst` 1件のみ**（新規0件）
11. `.rn/20260724-ntf-yaml-support/` 配下を全走査し、**`#17` の user review を `/rn:gm` と記した箇所が0件**であること（STEP 6-4）。`#17` 以外のタスクの `/rn:gm` の記録は対象外なので、ヒットした全件を「`#17` に関するものか」の判定理由付きで表に載せる

## 禁止事項

- 新しいページを作らない。`rest.rst` を変更しない（`#17` で承認済み。基準は既に実効値である）
- `web.rst` の設定項目表の**項目を増やさない・減らさない・並べ替えない**。列構成・見出しを変更しない
- `web.rst` の「テストの実行速度を上げる」「拡張例」の各セクションを変更しない（`:216` の `tip` の `htmlResourcesRoot` を除く）
- フィールド初期値と実効値を**両方併記しない**。実効値だけを載せる
- `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `style.md` / `ja/conf.py` を変更しない
- `design.md` は §8 以外を変更しない。**既存の行を削除しない**
- 4観点のレビューは回さない。**新しい内容を書かないタスクであり、ゲート1〜5 が変更の範囲を機械的に固定している**
- 既存のレビュー記録・チェック記録を書き換えない。**追記のみとする。** 例外は STEP 6-4 の `/rn:ty` への訂正3箇所だけである。これは判断の内容ではなく受領したコマンドの取り違えの訂正であり、**判断当時の記録（`checks/task-17.md` の §6 の `decide` 表・§7-2 の7項目表・`Overall Verdict` の `No` の行）には手を触れない**
- user review の承認を受けるまで `#19` に着手しない
