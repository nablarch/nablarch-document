# task-17 Completion Check

## 1. マッピング全件反映対応表（母集合は機械抽出）

母集合の抽出に使ったコマンド（`csv.DictReader` を使用。`wc -l`・grep で数えていない。ホワイトリストで切り出していない）:

```bash
python3 -c "
import csv
with open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv', newline='', encoding='utf-8') as f:
    rows=[r for r in csv.DictReader(f) if r['dest_page']=='リクエスト単体テストの設定（RESTfulウェブサービス）']
print(len(rows))
for r in rows:
    print(r['mapping_id'], r['src_body_start'], r['src_body_end'], r['lines'], r['disposition'], r['dest_section'], sep='|')
"
```

出力（4行。`DROP` なし）:

```
4
current-0310|49|74|26|MOVE|使用方法
current-0311|77|93|17|MOVE|使用方法
current-0319|278|281|4|MOVE|使用方法
current-0320|284|361|78|MOVE|使用方法
```

| mapping_id | 出典行 | 反映先セクション | 反映内容 |
|---|---|---|---|
| current-0310 | `RequestUnitTest_rest.rst:49-74` | 使用方法 > 必要なモジュールとコンポーネント設定を追加する（前半） | 依存関係に追加する3モジュール（`nablarch-testing-rest`・`nablarch-testing-default-configuration`・`nablarch-testing-jetty12`）の `pom.xml` 記述例と、`nablarch-testing` への依存を述べる `tip`。出典の `モジュール一覧` という見出しは置いていない（`style.md` S-02）。出典が `important` にしていた注記は `tip` に変えた（`style.md` S-06、`reviews` の D-9） |
| current-0311 | `:77-93` | 使用方法 > 必要なモジュールとコンポーネント設定を追加する（後半） | テスティングフレームワークの設定をテスト用のコンポーネント設定ファイル（ブランクプロジェクトでは `src/test/resources/unit-test.xml`）に記述すること、`nablarch/test/rest-request-test.xml` の読み込みの記述例、ブランクプロジェクト3種の状況を述べる `tip`。出典の `:ref:`rest-test-configuration`` は同一ページ内になるためリンクにせず、次のL3へ流れる形にした（`reviews` の D-6）。あわせて実装で必須と確認した `httpServerFactory` の登録を追加した（`reviews` の R1-M1・`decide` 1） |
| current-0319 | `:278-281` | 使用方法 > コンポーネント設定ファイルで設定値を変更する（導入文） | 「実行環境に依存する設定値は…上書きして変更する」と、主な設定項目を示すという導入。出典の「コンポーネント設定ファイルで変更できる」「設定可能な項目を以下に示す」の2文に対応する |
| current-0320 | `:284-361` | 使用方法 > コンポーネント設定ファイルで設定値を変更する（表と本文） | `webBaseDir`・`webFrontControllerKey` の設定項目一覧（`list-table`）とデフォルト値。脚注1（複数ディレクトリのカンマ区切り指定と探索順、記述例）と脚注2（Webフロントコントローラを別名で登録している場合のコンポーネント名の指定、記述例）を表の直後の地の文に展開した。脚注2にあったハンドラキュー構成のXML全文2件は、同じ例を持つFW解説書の `change_web_front_controller_name` への `:ref:` で解決した（`reviews` の D-8・R1-M4） |

**未反映の行: 0件。**

## 2. Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `mapping.csv` の当該 `dest_page` の全行（4行）が反映されている | OK | 上記 §1 の全件表。母集合は `csv.DictReader` で `dest_page` 完全一致抽出（4行・`DROP` 0件）。4行すべてに反映先セクションと反映内容がある。ラウンド1の観点A（網羅性）が独立に同じ4行を抽出し、出典の内容単位15件まで分解して突合した結果、欠落1件（`:313-348`）を検出。参照で解決済み | OK | コーディネータが `csv.DictReader` で `dest_page` 完全一致抽出を独立に実行し、4行・125 lines・`DROP` 0件を確認。4行とも本文に反映先がある |
| 当該 `dest_page` のマッピング行が全件、ページのどこに反映されたかの対応表が `checks/task-17.md` にある | OK | §1 が本ファイルの先頭にあり、抽出コマンドとその出力を併記している。ホワイトリストによる切り出しはしていない | OK | §1 が本ファイルの先頭にあり、抽出コマンドが `dest_page` 完全一致である（`#10b` 申し送りの「母集合をホワイトリストで切り出さない」に適合） |
| `make html`（Docker）が当該ページについてエラーを出さない | OK | §4 のビルドログ。`build succeeded, 1 warning.`（既知の `db_double_submit.rst` の1件のみ・新規0件） | OK | 本ページが張る4ラベル（`testing_framework_about`・`web_front_controller`・`change_web_front_controller_name`・自ページ）の定義をコーディネータが `grep` で実在確認。`keep_warnings = True` のため未定義なら警告に出るが、既知1件のみで新規0件 |
| 4観点のレビューがすべて実施・記録されている | OK | §5 と `reviews/page-request_unit_test_setting_rest.md`「レビュー記録」。A/B/C/D をそれぞれ別のサブエージェントで実施し、ラウンド2は是正差分限定の検証を1エージェントで実施した | OK | ラウンド1が4観点別サブエージェント、ラウンド2が是正差分限定（`#10b` 申し送りに適合）。指摘・根拠・対応が `reviews` に全件記録されている |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | OK | `reviews/page-request_unit_test_setting_rest.md` の「対応しなかった指摘」（R1-X1〜X7）と R2-4〜R2-5。いずれも理由を記録した。`decide` 2件はユーザー判断に上げる | OK | R1-X1〜X7・R2-4〜R2-6 に理由あり。`decide` 2件は user review に上げる。**コーディネータの独立検証で `decide` 2 の射程が報告より広いことが判明したため §7 に追記した** |

## 7. コーディネータの独立検証（2026-08-12）

実装エキスパートの自己申告と自ら回したレビューに依存せず、コーディネータが実コードとアーティファクトを直接確認した。

### 7-1. 裏付けを再確認した事実（いずれも一致）

| 主張 | 再確認の方法と結果 |
|---|---|
| `httpServerFactory` が未登録だと内蔵サーバの生成時に例外になる | `nablarch-testing-rest` の `SimpleRestTestSupport.java:45`（`HTTP_SERVER_FACTORY_KEY = "httpServerFactory"`）・`:298-301`（`SystemRepository.get(...)` が `null` なら `IllegalConfigurationException`）を直接読んだ。一致 |
| デフォルト設定は `httpServerFactory` を登録しない | `nablarch-testing-default-configuration-6u3.jar` を展開し全ファイルを `grep -rc "httpServerFactory"` した結果 **0件**。一致 |
| `webFrontControllerKey` の既定値は `webFrontController` | `RestTestConfiguration.java:8`（フィールド宣言 `private String webFrontControllerKey = "webFrontController";`）。一致 |
| `webFrontControllerKey` はハンドラキューの取得元コンポーネント名 | `SimpleRestTestSupport.java:270-273`（`SystemRepository.get(config.getWebFrontControllerKey())` → `getHandlerQueue()` → `server.setHandlerQueue(...)`）。一致 |
| `webBaseDir` はカンマ区切りで順に探索される | `SimpleRestTestSupport.java:282-290`（`getWebBaseDir().split(",")` を順に `basePaths` へ）。一致 |
| `webBaseDir` の実効デフォルト値は `src/main/webapp` | `rest-request-test.xml:15` が `${nablarch.httpTestConfiguration.webBaseDir}` を設定し、`http-request-test/http-request-test.config:1` が `src/main/webapp` を与える。クラスのフィールド初期値は `HttpTestConfiguration.java:29` の `../main/web`。一致 |
| 参照ラベル4件の実在 | `testing_framework_about`（`about/index.rst:1`）・`web_front_controller`（`web_front_controller.rst:1`）・`change_web_front_controller_name`（同 `:82`）。一致 |
| 用語 `Webフロントコントローラ` | `ja/` 全体で `Webフロントコントローラー`（長音あり）0件・`Webフロントコントローラ`（長音なし）15件。出典の長音表記を FW解説書の用法に是正した本ページの判断は正しい |
| `toctree` の順序 | `setup/index.rst:11-12` で `request_unit_test/web` の直後。`design.md` §3 の第2部構成どおり（`#15` 申し送り6 に適合） |

**本ページ（`rest.rst`）自体に、コーディネータ検証で新たに検出した事実誤りは無い。**

### 7-2. `decide` 2 の射程は報告より広い（コーディネータが新規に検出）

実装エキスパートは `webBaseDir` 1項目の食い違いとして報告したが、**同じ食い違いは `web.rst` の設定項目表の複数項目に及ぶ。**

原因は、`#15` が `htmlChecker`・`htmlCheckerConfig` の既定値を「該当なし」と判断した際（`reviews/page-request_unit_test_setting_web.md` の C-2・C-3）、**`nablarch-testing` の `src/main/` だけを探索し、デフォルト設定が別モジュール `nablarch-testing-default-configuration` にあることに気づかなかった**ことにある。ウェブアプリケーションのブランクプロジェクトも `nablarch/test/http-request-test.xml` を読み込むため（`nablarch-web-archetype-6u3` の `archetype-resources/src/test/resources/unit-test.xml:16`）、読者が実際に目にする値は次のとおり食い違う。

| 設定項目 | `web.rst` の記載（クラスのフィールド初期値） | デフォルト設定を読み込んだ実効値 | 出典 |
|---|---|---|---|
| `webBaseDir` | `../main/web` | `src/main/webapp` | `http-request-test.config:1` |
| `jsTestResourceDir` | `../test/web` | `src/test/webapp` | 同 `:2` |
| `htmlCheckerConfig` | 該当なし | `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` | 同 `:5` |
| `htmlChecker` | 該当なし | `htmlCheckerConfig` の副作用により `Html4HtmlChecker` が設定される | `HttpTestConfiguration.java:358-361` |
| `htmlResourcesExtensionList` | `css`・`js`・`jpg`（3件） | `css`・`jpg`・`js`・`less`・`png`・`template`・`woff`・`eot`・`svg`・`ttf`（10件） | `http-request-test.xml` の `htmlResourcesExtensionList` |
| `tempDirectory` | 該当なし（内蔵サーバのデフォルト動作） | `target/tmp` | `http-request-test.config:11` |
| `htmlResourcesRoot`（`web.rst` は `tip` で言及） | `htmlResources` | `../htmlResources` | 同 `:7` |

確認コマンド: `nablarch-testing-default-configuration-6u3.jar` を展開し、`nablarch/test/http-request-test.xml` と `nablarch/test/http-request-test/http-request-test.config` を直接参照。`nablarch-web-archetype-6u3.jar` の `archetype-resources/src/test/resources/unit-test.xml` の `<import>` 行を確認。

**副次的な確認**: 同 `unit-test.xml:57` は `httpServerFactory` を明示登録しており、`decide` 1 の「ブランクプロジェクトでは詰まらないが既存プロジェクトでは詰まる」という整理はウェブアプリケーション側でも成り立つ。

この事実は `#17` の本文には影響しない（`rest.rst` は実効値を採用し、表の直前でその基準を明示している）が、**承認済みの `web.rst` と、残り4ページの設定項目表の基準に影響する。** user review に上げる（`decide` 2 の判断材料）。

## 3. Method を適用した記録（本ページの全主張の裏付け）

本ページの記述を主張単位に分解し、出典行と実装の `file:line` で裏付けた一覧。**未確認の主張は0件である。**

| # | 本文の主張 | 出典 | 実装での裏付け |
|---|---|---|---|
| 1 | 3モジュールが必要で、いずれも `test` スコープ | `:49-68` | `nablarch-jaxrs-archetype-6u3.jar` の `archetype-resources/pom.xml:262-280`。3件とも Maven Central に実在（`nablarch-testing-rest` 2.0.0 / `nablarch-testing-jetty12` 1.1.0 / `nablarch-testing-default-configuration` 6u3） |
| 2 | `nablarch-testing-rest` は `nablarch-testing` に依存する | `:71-73` | `nablarch-testing-rest/pom.xml:41` |
| 3 | 設定はテスト用のコンポーネント設定ファイル（ブランクプロジェクトでは `src/test/resources/unit-test.xml`）に記述する | `:78-80` | `nablarch-jaxrs-archetype-6u3.jar` の `archetype-resources/src/test/resources/unit-test.xml` |
| 4 | `nablarch/test/rest-request-test.xml` を読み込む | `:82-84` | `nablarch-testing-default-configuration-6u3.jar` に実在。`nablarch-testing-rest/src/test/resources/unit-test.xml:9` も同じファイルを `<import>` する |
| 5 | `httpServerFactory` に `HttpServerFactoryJetty12` を登録する | 出典なし（実装から補った） | `SimpleRestTestSupport.java:45`・`:298-301`（未登録なら `IllegalConfigurationException`）。`nablarch-testing-default-configuration-6u3.jar` に `httpServerFactory` は0件。`nablarch-testing-jetty12` は `src/main/resources` を持たない。クラスは `nablarch-testing-jetty12/src/main/java/nablarch/fw/web/httpserver/HttpServerFactoryJetty12.java`。`nablarch-jaxrs-archetype-6u3` の `unit-test.xml:53` が同じ定義を持つ |
| 6 | RESTfulウェブサービスプロジェクトには依存関係と設定が既に記述されている | `:88-92` | `nablarch-jaxrs-archetype-6u3` の `pom.xml:262-280` と `unit-test.xml:16,53` |
| 7 | ウェブプロジェクト・Nablarchバッチプロジェクトでは不足分を追加する | `:88-92` | `nablarch-web-archetype-6u3` の `unit-test.xml:16`（`http-request-test.xml` のみ）・`:57`（`httpServerFactory` は登録済み）・`pom.xml`（`nablarch-testing-rest` が無い）。`nablarch-batch-archetype-6u3` は `unit-test.xml`・`pom.xml` とも jetty12 / `httpServerFactory` / rest を持たない |
| 8 | デフォルト設定を読み込むと `RestTestConfiguration` が `restTestConfiguration` というコンポーネント名で登録される | `:279-280`・`:355-361` | `rest-request-test.xml:13-14`。`SimpleRestTestSupport.java:41`・`:88` が同じ名前で引く |
| 9 | 同じ名前で上書きして変更する／上書きは読み込みより後に置く | `:355-361` | `XmlComponentDefinitionLoader.java:214`（`mergeComponentDefinitions` の呼び出し）・`:238-273`（後勝ち）・`:282-297`（同一クラスなら先の定義のプロパティを引き継ぐ）。FW解説書 `libraries/repository.rst:167-201` |
| 10 | `webBaseDir` のデフォルト値は `src/main/webapp` | `:290` | `rest-request-test.xml:15` → `http-request-test.config:1`。クラスのフィールド初期値は `HttpTestConfiguration.java:29` の `../main/web` であり、両者の差は表の直前の但し書きで説明した |
| 11 | `webFrontControllerKey` のデフォルト値は `webFrontController` | `:292` | `RestTestConfiguration.java:8`（フィールド初期値）と `http-request-test.config:12`（デフォルト設定）が一致 |
| 12 | `webFrontControllerKey` は内蔵サーバで実行するハンドラキューの取得元となるコンポーネント名 | `:340-348` | `SimpleRestTestSupport.java:270-275` |
| 13 | `webBaseDir` はカンマ区切りで複数指定でき、指定された順に探索して最初に見つかったリソースを使う | `:294-304` | `SimpleRestTestSupport.java:282-290` → `HttpServerJetty12.java:250-259`（`ResourceFactory.combine`）→ Jetty 12.0.12 の `CombinedResource.java:131`・`:151-157` |
| 14 | `webFrontController` 以外のコンポーネント名で登録している場合に指定する／併用構成が該当する | `:306-311` | `SimpleRestTestSupport.java:270`（条件はコンポーネント名だけで、WAR の数には依存しない）。FW解説書 `web_front_controller.rst:85-88` |
| 15 | 指定しないとウェブアプリケーション用のハンドラキューが内蔵サーバで実行される | `:350-353` | `SimpleRestTestSupport.java:270-275` と `RestTestConfiguration.java:8` |
| 16 | コンポーネント定義の例（`webFrontController` / `jaxrsController`） | `:313-348` | FW解説書 `web_front_controller.rst:82-117`（同じシナリオ・同じコンポーネント名の定義例）へ `:ref:` |

## 4. Docker ビルドの実行結果

```
docker run --rm -v /home/tie303177/work/lovaizu/nablarch-document:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

出力の該当箇所:

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
build succeeded, 1 warning.
```

- `build succeeded`。警告は既知の `db_double_submit.rst` の1件のみで、**新規警告は0件**。
- `undefined label` は上記の既知1件のみ。`duplicate label`・`toctree contains reference to nonexisting document` はいずれも0件。
- `_build/` は削除していない（`_build/html/development_tools/testing_framework/setup/request_unit_test/rest.html` を生成済み）。
- `docker build -t nablarch-document-build .` はサンドボックス環境で `pip install` が失敗するため再実行できなかった。既存の `nablarch-document-build:latest` イメージ（前タスクでビルド済み）を使用した。
- Docker ビルドが再生成した `locales/ja/LC_MESSAGES/sphinx.mo` は `git checkout` で戻した（`f6947b2`・`73e84dc` と同じ運用）。

## 5. 4観点レビューの結果

| ラウンド | 観点 | 判定 | must | should | note |
|---|---|---|---|---|---|
| 1 | A 網羅性 | fail | 2 | 3 | 4 |
| 1 | B トンマナ | fail | 1 | 2 | 5 |
| 1 | C 用語 | fail | 1 | 4 | 3 |
| 1 | D 整合性 | fail | 2 | 3 | 5 |
| 2 | 是正差分限定 | pass | 0 | 2 | 4 |

ラウンド1の `must` は重複を除いて5件で、すべて是正した（`httpServerFactory` の欠落／`restTestConfiguration` の二重登録／L3見出しの抽象度／コンポーネント定義XML 2件の欠落／姉妹ページとのデフォルト値の食い違い）。詳細と、対応しなかった指摘の理由は `reviews/page-request_unit_test_setting_rest.md` に記録した。

## 6. `decide`（ユーザー判断が必要な点）

| # | 内容 |
|---|---|
| 1 | **`httpServerFactory` の登録を本ページに書いたこと。** 出典（`RequestUnitTest_rest.rst` 全体）にも `mapping.csv` にも1件も現れないが、登録しないと内蔵サーバの生成時に例外になる（`SimpleRestTestSupport.java:298-301`）。「マッピングにない内容を追加しない」に対する例外として妥当かを判断してほしい。書かない場合は、リード文と見出しから「これで実行できるようになる」という含意も落とす必要がある |
| 2 | **`webBaseDir` のデフォルト値の基準。** 本ページはデフォルト設定ファイルの値（`src/main/webapp`）、姉妹ページ `web.rst` はクラスのフィールド初期値（`../main/web`）を載せている。実効値はどちらのブランクプロジェクトでも `src/main/webapp` である。両ページの基準を揃えるか（`web.rst` の変更が必要）、現状のまま但し書きで区別するかを判断してほしい |

### 6-1. user review の回答（2026-08-13、`/rn:gm`）

上記の表は判断を仰いだ時点の記録であり、書き換えない。以下は user review で示された回答である。根拠として挙げた `file:line` と参照コミットは、ユーザーおよびレビュー役の実測によるもの（本セッションのコーディネータが再実行して確かめたものではない）。

**`decide` 1 — `httpServerFactory` の登録を本文に書いたこと → 残す**

「マッピングにない内容を追加しない」（`design.md` §11.3）の例外として認める。理由は、出典が触れていないのはアーキタイプからのプロジェクト作成を前提にしていたためであり、アーキタイプ以外から作る読者には必須の記述で、落とすとページの内容だけではテストが動かないこと。

| 事実 | 出典 |
|---|---|
| 未登録なら `IllegalConfigurationException` が発生する | `nablarch-testing-rest`（`b7729df`）`src/main/java/nablarch/test/core/http/SimpleRestTestSupport.java:45`・`:298-300` |
| デフォルト設定は登録しない。**5u24・5u26・6u1・6u2・6u3 のすべてで0件** | `com.nablarch.configuration:nablarch-testing-default-configuration` の各版 jar を展開して全ファイル走査（レビュー役が実測） |
| `nablarch-testing-jetty12` は `src/main/resources` を持たない | `nablarch-testing-jetty12`（`646c3d9`） |
| アーキタイプは登録済み | `nablarch-web-archetype-6u3` / `nablarch-jaxrs-archetype-6u3` の `archetype-resources/src/test/resources/unit-test.xml` |

これは `design.md` §8 の既存の例外2件（陳腐化した例示／外部の挙動の変化）のどちらでもなく、「出典が欠いている、実装上必須の設定」という**新しい類型**である。類型としての規定は `#18` で `design.md` §8 に追記する。

**`decide` 2 — 設定項目表の「デフォルト値」の基準 → デフォルト設定を読み込んだ実効値に統一する**

`rest.rst` の基準（実効値）が正しい。`web.rst` の基準（クラスのフィールド初期値）を実効値に改める。根拠は**出典自身が実効値を書いていること**である。

- `RequestUnitTest_rest.rst:288`（`2e501ad`）の `webBaseDir` のデフォルト値は `src/main/webapp`。これは実効値であり、フィールド初期値（`HttpTestConfiguration.java:29` の `../main/web`）ではない
- `02_RequestUnitTest.rst:345`・`:351`（同）の `htmlChecker`・`htmlCheckerConfig` も実効値相当を書いている。`web.rst` はこれを「該当なし」に改めており、**出典と実効値の両方に反している**
- 「クラスのフィールド初期値」は出典にも実態にも無い基準である。`nablarch-web-archetype-6u3` の webapp は `archetype-resources/src/main/webapp` にあり、`web.rst` の `../main/web` はブランクプロジェクトに存在しないパスである
- 実効値を基準にしても上書き時に破綻しない。同名・同クラスのコンポーネント定義は**プロパティ単位でマージ**され、後の定義に無いプロパティは先の定義（デフォルト設定）の値が残る（`nablarch-core-repository`（`6a28491`）`src/main/java/nablarch/core/repository/di/config/xml/XmlComponentDefinitionLoader.java:214`・`:238-273`・`:283-328`。既定ポリシーは `:119` の `DuplicateDefinitionPolicy.OVERRIDE`）

**是正の対象は §7-2 の7項目では足りない。** レビュー役の実測で `web.rst` は9項目、`common.rst` にも同型が1件ある。全件と作業手順は `#18` の作業指示（`ntf-doc-18-default-value-basis.md`）に示される。§7-2 の表は当時の検出範囲の記録として残し、書き換えない。

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: OK（ラウンド1の観点D・整合性）
- Craft expert: OK（ラウンド1の観点B・トンマナ）
- Verification expert: OK（ラウンド1の観点A・網羅性／観点C・用語。ラウンド2は是正差分限定で pass）
- コーディネータの独立検証: OK（§7。本ページに新規の事実誤りは無し。`decide` 2 の射程の広がりを新規検出）
- Ready to check off: **No** — `decide` 2件の user review 待ち（`steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」）
- **2026-08-13 追記**（上記は判断を仰いだ時点の記録。書き換えずに追記する）: user review で公開本文が承認され、`decide` 2件に回答が出た（§6-1）。Ready to check off: **Yes**。`decide` 2 の是正（`web.rst` 9項目・`common.rst` 1項目）は本タスクでは行わず、`#18` で扱う
