# レビュー記録 — リクエスト単体テストの設定（RESTfulウェブサービス）（`setup/request_unit_test/rest.rst`）

対象タスク: `#17`。ページ先頭ラベルは `style.md` S-08 から引いた `request_unit_test_setting_rest`。
`#13` で定着させた共通 Steps のみで進めるページ（個別の作業指示なし）。

## 出典

`mapping.csv` の `dest_page=リクエスト単体テストの設定（RESTfulウェブサービス）` の4行（125 lines、`DROP` なし）。
出典ファイルは `#7` で削除済みのため `origin/develop` の内容で参照した。

| mapping_id | 出典行 | 見出し | dest_section |
|---|---|---|---|
| current-0310 | `RequestUnitTest_rest.rst:49-74` | 概要 > モジュール一覧 | 使用方法 |
| current-0311 | `:77-93` | 概要 > 設定 | 使用方法 |
| current-0319 | `:278-281` | 各種設定値 > (L2直下) | 使用方法 |
| current-0320 | `:284-361` | 各種設定値 > コンポーネント設定ファイル設定項目一覧 | 使用方法 |

全件の反映対応表は `checks/task-17.md` の先頭に置いた（母集合は `mapping.csv` から `dest_page` 完全一致で機械抽出しており、ホワイトリストで切り出していない）。

## 実装で確認した事実

参照した実装と時点は次のとおり。clone・ダウンロードはいずれもスクラッチディレクトリで行い、リポジトリ内には置いていない。

| 参照先 | 取得方法 | 時点 |
|---|---|---|
| `nablarch/nablarch-testing` | `git clone --depth 50`、`main` | `e21bf67`（`#15` と同一） |
| `nablarch/nablarch-testing-rest` | `git clone --depth 50`、`main` | `b7729df` |
| `nablarch/nablarch-testing-jetty12` | `git clone --depth 50`、`main` | `646c3d9` |
| `nablarch/nablarch-core-repository` | `git clone --depth 20`、`main` | `6a28491` |
| `com.nablarch.configuration:nablarch-testing-default-configuration` | Maven Central の jar | `6u3` |
| `com.nablarch.archetype:nablarch-jaxrs-archetype` / `nablarch-web-archetype` / `nablarch-batch-archetype` | Maven Central の jar | `6u3` |

`nablarch-testing-default-configuration` は GitHub に公開リポジトリが存在しない（`nablarch/nablarch-testing-default-configuration` は `Repository not found`）。
`nablarch/test/rest-request-test.xml` の実体を確かめるため、Maven Central の jar を展開して参照した。

| # | 本文の記述 | 実装の根拠 |
|---|---|---|
| I-1 | 依存関係に追加する3モジュールの groupId / artifactId / scope | `nablarch-jaxrs-archetype-6u3.jar` の `archetype-resources/pom.xml:264-280`（`com.nablarch.framework:nablarch-testing-rest`・`com.nablarch.framework:nablarch-testing-jetty12`・`com.nablarch.configuration:nablarch-testing-default-configuration`、いずれも `<scope>test</scope>`）。3件とも Maven Central に実在する（`nablarch-testing-rest` 2.0.0 / `nablarch-testing-jetty12` 1.1.0 / `nablarch-testing-default-configuration` 6u3） |
| I-2 | `nablarch-testing-rest` は `nablarch-testing` に依存する | `nablarch-testing-rest/pom.xml:41`（`<dependency>` に `com.nablarch.framework:nablarch-testing` を持つ） |
| I-3 | 読み込む設定ファイルは `nablarch/test/rest-request-test.xml` | `nablarch-testing-default-configuration-6u3.jar` の `nablarch/test/rest-request-test.xml`（jar 内に実在）。`nablarch-testing-rest/src/test/resources/unit-test.xml:9` も同じファイルを `<import>` している |
| I-4 | コンポーネント名は `restTestConfiguration` | `nablarch-testing-rest` の `SimpleRestTestSupport.java:41`（`REST_TEST_CONFIGURATION_KEY = "restTestConfiguration"`）・`:88`（`SystemRepository.get(REST_TEST_CONFIGURATION_KEY)`）。`rest-request-test.xml:13-14` の `<component name="restTestConfiguration" class="nablarch.test.core.http.RestTestConfiguration">` と一致 |
| I-5 | `webBaseDir` のデフォルト値は `src/main/webapp` | `rest-request-test.xml:15` が `${nablarch.httpTestConfiguration.webBaseDir}` を設定し、`nablarch/test/http-request-test/http-request-test.config:1` が `nablarch.httpTestConfiguration.webBaseDir=src/main/webapp` を与える（下記「出典と実装が食い違った箇所」も参照） |
| I-6 | `webFrontControllerKey` のデフォルト値は `webFrontController` | `RestTestConfiguration.java:8`（フィールド宣言の初期値 `"webFrontController"`）。`rest-request-test.xml:16` と `http-request-test.config:12`（`nablarch.httpTestConfiguration.webFrontControllerKey=webFrontController`）も同じ値であり、両者が一致する |
| I-7 | `webFrontControllerKey` は内蔵サーバで実行するハンドラキューの取得元を決める | `SimpleRestTestSupport.java:270-275`（`SystemRepository.get(config.getWebFrontControllerKey())` で `WebFrontController` を取得し、その `getHandlerQueue()` を `server.setHandlerQueue(...)` に渡す） |
| I-8 | `webBaseDir` にカンマ区切りで複数指定でき、指定した順に探索される | `SimpleRestTestSupport.java:282-290`（`getWebBaseDir().split(",")` を順に `ResourceLocator` のリストにして `server.setWarBasePaths(...)`）。`nablarch-testing-jetty12` の `HttpServerJetty12.java:250-259`（リスト順に `Resource` を並べて `ResourceFactory.combine(...)`）。Jetty 12.0.12 の `CombinedResource.java:131`「is a file that exists in at least one of the collection, then the first one found is returned」・`:151-157`（リスト順に `resolve` して最初に見つかったものを返す）。ソースは `org.eclipse.jetty:jetty-util:12.0.12` の sources jar で確認した（`nablarch-testing-jetty12/pom.xml:26` が `jetty.version` を `12.0.12` に固定している） |
| I-9 | RESTfulウェブサービスのブランクプロジェクトには読み込みが既に含まれ、ウェブアプリケーション・Nablarchバッチアプリケーションでは追加が必要 | `nablarch-jaxrs-archetype-6u3.jar` の `archetype-resources/src/test/resources/unit-test.xml:16` が `nablarch/test/rest-request-test.xml` を `<import>` している。`nablarch-web-archetype-6u3.jar` の同ファイル `:16` は `nablarch/test/http-request-test.xml` のみ、`nablarch-batch-archetype-6u3.jar` の同ファイルはいずれも読み込んでいない |
| I-10 | デフォルト設定を読み込んだ後に `restTestConfiguration` を上書きできる | `nablarch-core-repository` の `XmlComponentDefinitionLoader.java:238-273`（同名のコンポーネント定義は後勝ちでマージされる）・`:284-297`（**クラスが同じ場合は先の定義のプロパティが引き継がれ**、異なる場合のみ全置換）。FW解説書の `libraries/repository.rst:167-201` の記述とも一致する |

## 出典と実装が食い違った箇所

| # | 出典の記述 | 実装 | 採用した記述と理由 |
|---|---|---|---|
| M-1 | `webBaseDir` のデフォルト値は `src/main/webapp`（`:290`） | `RestTestConfiguration` が継承する `HttpTestConfiguration.java:29` の**フィールド初期値は `../main/web`**。一方、本ページが読み込ませる `nablarch/test/rest-request-test.xml:15` は `http-request-test.config:1` 経由で `src/main/webapp` を設定する | **`src/main/webapp` を採用した。** 本ページは `nablarch/test/rest-request-test.xml` の読み込みを手順として示しており、その状態で有効になる値は `src/main/webapp` である。読者が実際に目にする値と一致させるため、表の直前に「デフォルト値は、前述の `nablarch/test/rest-request-test.xml` が設定する値である」と根拠を明示した。`#15` の申し送り2（出典のデフォルト値欄はフィールドの初期値と一致するとは限らない）を受けてフィールド初期値を確認した結果、**両者が食い違う理由まで特定できた**ケースである |
| M-2 | 出典のXML例のコメントは `nablarch-testing-rest` を「テスティングフレームワーク本体」としている（`:51`） | 本体は `nablarch-testing` であり、`nablarch-testing-rest` はそれに依存する RESTfulウェブサービス向けのモジュールである（I-2） | コメントを「RESTfulウェブサービス用のテスティングフレームワーク」に改めた。直後の `tip` で `nablarch-testing` への依存関係を述べており、本体との関係はそこで分かる |
| M-3 | 「Nablarch5u18以降のアーキタイプから…作成した場合上記が既に設定されている」（`:89-93`） | 6u3 のアーキタイプで確認済み（I-9） | **バージョンの条件を落とした**（`design.md` §8「陳腐化した例示は落としてよい」）。現在サポートされている 6 系のアーキタイプでは無条件に成り立つ条件であり、5 系のバージョン番号を残すと読者に「6 系では確認が必要か」という余計な判断を強いる。事実（RESTfulウェブサービスのブランクプロジェクトには含まれる／他の2つでは追加が必要）は落としていない |

## 作成時の判断

| # | 判断 | 理由 |
|---|---|---|
| D-1 | L2 は `使用方法` の1つのみとし、`機能概要`・`拡張例` の見出しを置かなかった | 対象4行はすべて `dest_section=使用方法` であり、機能概要・拡張例に相当する出典が無い。`design.md` §3 が「出典が無い場合は見出し自体を置かない」と定めている |
| D-2 | L3 は `テストを実行できるようにする`（current-0310・current-0311）と `コンポーネント設定ファイルに設定項目を登録する`（current-0319・current-0320）の2つにした | 前者は「動かすまでに何をするか」、後者は「動いた後で何を変えられるか」という別の問いに答える。後者の見出しは姉妹ページ `web.rst` と同一にし、横並びで読んだときに同型に見えるようにした |
| D-3 | `モジュール一覧` の見出しを置かず、依存関係を `テストを実行できるようにする` の中に置いた | `style.md` S-02 が第2部・第3部に `モジュール一覧` の見出しを置かないと定めている。処理方式固有の依存関係を当該ページに書くことは `design.md` §2 で確定済み（第1部には集約しない） |
| D-4 | 出典の脚注（`[#]_`）2件を、表の直後の地の文に展開した | 姉妹ページ `web.rst` の前例に倣った。出典の脚注機構は使わない |
| D-5 | 出典の `:ref:`テスティングフレームワーク <unitTestGuide>`` を `testing_framework_about` に張り替えた | `unitTestGuide` は `#7` で削除済み（`grep -rn "^\.\. _unitTestGuide:" ja/` は0件）。新構成の対応ページは第1部「テスティングフレームワークとは」（`about/index.rst`）であり、ラベルは `style.md` S-08 の一覧から引いた |
| D-6 | 出典の `:ref:`rest-test-configuration`` へのリンクは張らず、ページ内の流れとして書いた | 新構成では参照元・参照先がいずれも本ページの `使用方法` 配下になる。同一ページ内を行き来するだけのリンクを作らないため |
| D-7 | `:doc:` によるブランクプロジェクト3件へのリンクは、新ページからの相対パス（4階層上）に直した | 出典は `guide/development_guide/06_TestFWGuide/` からの5階層上だった。参照先3ファイルの実在を確認済み |
| D-8 | 出典の `webFrontControllerKey` の脚注にあるコンポーネント定義XML全文2件（`webFrontController` と `jaxrsController` のハンドラキュー構成）は、FW解説書の `change_web_front_controller_name` へ `:ref:` で参照する形にした | FW解説書 `web_front_controller.rst:82-117` が、同じシナリオ・同じコンポーネント名（`webFrontController` / `jaxrsController`）の2件の定義を既に持っている。Acceptance criteria の「重複がない — 参照で解決する」に従った。**初版では地の文に畳んでいたが、ラウンド1の R1-M4 を受けて参照に改めた** |
| D-9 | 出典が `important` にしていた「`nablarch-testing` のAPIもあわせて使用できる」を `tip` に変えた | `style.md` S-06 は `important` を「無視すると不具合・非推奨機能の誤用・データ不整合につながる、読者が必ず守るべき注意事項」に限っている。当該の記述は読まなくても機能を正しく使える補足であり `tip` に当たる |
| D-10 | 設定項目の表の導入を「主な設定項目は次のとおりである」とした | `RestTestConfiguration` は `HttpTestConfiguration` を継承しており、表の2項目以外にも有効な設定項目がある（`SimpleRestTestSupport.java:263` は `tempDirectory` を、`HttpRequestTestSupportHandler.java:95` は `sessionInfo` を使用する）。表に無い項目を足すと「マッピングにない内容を追加しない」に反するため、項目は増やさず導入文で網羅を主張しない形にした（`#15` の R1-6 と同型の判断） |
| D-11 | `webBaseDir` の複数指定の説明が姉妹ページ `web.rst` とほぼ同文になっている | `RestTestConfiguration` は `HttpTestConfiguration` を継承しており、`webBaseDir` は同一のプロパティである。出典も両ファイルに同じ脚注を独立して持っており、マッピングは両方を各ページに割り当てている。処理方式の違うページから相互参照させる方が読者の負担になるため、参照ではなく記述で解決した |

## 書かなかったが確認した事実（`decide` 候補）

| # | 事実 | 実装の根拠 | 本ページで書かなかった理由 |
|---|---|---|---|
| X-1 | 内蔵サーバを起動するには `httpServerFactory` という名前で `HttpServerFactoryJetty12` をコンポーネント登録する必要がある。デフォルト設定（`nablarch/test/rest-request-test.xml`）はこれを定義していないため、プロジェクト側の設定が必須である | `SimpleRestTestSupport.java:45`（`HTTP_SERVER_FACTORY_KEY = "httpServerFactory"`）・`:298-301`（`SystemRepository.get(HTTP_SERVER_FACTORY_KEY)` が `null` なら `IllegalConfigurationException`）。`nablarch-testing-default-configuration-6u3.jar` に `httpServerFactory` の定義は無い（jar 内全ファイルを `grep` して0件）。`nablarch-jaxrs-archetype-6u3.jar` の `archetype-resources/src/test/resources/unit-test.xml:53` はこれを定義している | **出典（`RequestUnitTest_rest.rst` 全体）にも `mapping.csv` にも `httpServerFactory` は1件も現れない**（`git grep` / `grep` でいずれも0件）。マッピングに無い内容の追加になるため書かなかった。ブランクプロジェクトから作成した読者は既に定義されているため詰まらないが、既存プロジェクトに後から追加する読者は詰まる可能性がある。**追記の要否はユーザー判断に上げる（`decide`）** |
| X-2 | `restTestConfiguration` を同じクラスで上書きすると、先の定義のプロパティ（`webBaseDir` など）は引き継がれる | `XmlComponentDefinitionLoader.java:284-297`。FW解説書 `libraries/repository.rst:188-201` | 出典が触れていない挙動であり、上書きの記述例が正しく動くことの裏付けとしてのみ使った。本文には書いていない（`#15` の R1-X6 と同型の判断） |

## レビュー記録

### ラウンド1（2026-08-12）

4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を、それぞれ**別のサブエージェント**で実施した。各観点には成果物・目的・完了条件・チェックリストのみを渡し、`checks/`・`reviews/` 配下の自己申告記録は渡していない。プロンプトには Rules の3点（実測で裏付ける／付属の検証物を正解にせず独立に組む／敵対的に見る）を入れた。

**判定: A fail（`must` 2）/ B fail（`must` 1）/ C fail（`must` 1）/ D fail（`must` 2）。重複を除いた `must` は5件。**

| 観点 | 判定 | must | should | note |
|---|---|---|---|---|
| A 網羅性 | fail | 2 | 3 | 4 |
| B トンマナ | fail | 1 | 2 | 5 |
| C 用語 | fail | 1 | 4 | 3 |
| D 整合性 | fail | 2 | 3 | 5 |

#### must（重複除去後5件）

| # | 観点 | 指摘 | 根拠 | 対応 |
|---|---|---|---|---|
| R1-M1 | C・D（A は should） | **`httpServerFactory` の登録が抜けており、ページのとおりに設定してもテストが起動しない。** デフォルト設定（`nablarch/test/rest-request-test.xml`）はこのコンポーネントを登録せず、`nablarch-testing-jetty12` も `src/main/resources` を持たない | `SimpleRestTestSupport.java:45`・`:298-301`（`SystemRepository.get("httpServerFactory")` が `null` なら `IllegalConfigurationException`）。`nablarch-testing-default-configuration-6u3.jar` 全体に `httpServerFactory` は0件。`nablarch-jaxrs-archetype-6u3` の `unit-test.xml:53` は明示登録している | **登録の記述を追加し、`important` で理由を添えた。** 出典（`RequestUnitTest_rest.rst` 全体）にも `mapping.csv` にも `httpServerFactory` は0件だが、`design.md` §8「出典が勧める手順が現在は…挙動変更になっている場合、その事実を書き足してよい」の趣旨（手順どおりに動かない記述を残さない）を適用した。**追加の可否はユーザー判断に上げる（`decide` 1）** |
| R1-M2 | A・C・D | 「テスト用のコンポーネント設定ファイルに `RestTestConfiguration` を `restTestConfiguration` という名前で登録する」が、直前に読み込ませたデフォルト設定による登録と二重で、ページ内で矛盾していた | `rest-request-test.xml:13-14` が既に `restTestConfiguration` を登録している | 「デフォルト設定を読み込むと、`RestTestConfiguration` が `restTestConfiguration` というコンポーネント名で登録される。実行環境に依存する設定値は、このコンポーネントを同じ名前で上書きして変更する」に是正した。L3の見出しも `コンポーネント設定ファイルに設定項目を登録する` から `コンポーネント設定ファイルで設定値を変更する` に改題した（姉妹ページと同じ見出しにしていたが、REST側は実態と合わないため） |
| R1-M3 | B | L3見出し `テストを実行できるようにする` が、ページタイトルと組にしても中身が分からない。`style.md` S-03 が不可とする `準備する` と同性質 | NTF全ページのL2/L3を機械抽出した結果、対象物を名指ししていないのは本見出しのみ（`common.rst:15,37,52`・`class_unit_test.rst:15`・`web.rst:16,158` はすべて名指ししている） | `必要なモジュールとデフォルト設定を追加する` に改題した |
| R1-M4 | A | `current-0320` の脚注2にあった `webFrontController` / `jaxrsController` 2件のコンポーネント定義XML（出典 `:313-348`）が丸ごと落ちていた | 出典 `RequestUnitTest_rest.rst:313-348` | **FW解説書に同じ例が既にあることを実測し、参照で解決した。** `ja/application_framework/application_framework/web/feature_details/web_front_controller.rst:82-117` の `change_web_front_controller_name` は、同じシナリオ（ウェブアプリケーションとRESTfulウェブサービスの併用）と、同じ名前（`webFrontController` / `jaxrsController`）の2つのコンポーネント定義を持つ。Acceptance criteria の「重複がない — 同じ内容が複数箇所に存在しない。参照で解決する」に従い、当該セクションへ `:ref:` を張った。初版で地の文に畳んだ判断（旧 D-8）は取り消した |
| R1-M5 | D | 同じ `webBaseDir` のデフォルト値が、姉妹ページ `web.rst:31` では `../main/web`（クラスのフィールド初期値）、本ページでは `src/main/webapp`（デフォルト設定ファイルの値）で食い違う | `HttpTestConfiguration.java:29` と `http-request-test.config:1`。`nablarch-web-archetype-6u3` の `unit-test.xml:14` も `nablarch/test/http-request-test.xml` を読み込むため、**ウェブアプリケーションのブランクプロジェクトでも実効値は `src/main/webapp`** である | **本ページは `src/main/webapp` のまま**とし、表の直前に「デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す」と基準を明示した。`web.rst` は承認済みページであり、本タスクのスコープ外（作業指示の「絶対に変更しないファイル」に他ページの `.rst` が含まれる）。**両ページの基準を揃えるかどうかはユーザー判断に上げる（`decide` 2）** |

#### should / note のうち是正したもの

| # | 観点 | 指摘 | 対応 |
|---|---|---|---|
| R1-1 | C | `リポジトリキー` は `ja/` 全体で本ページにしか無い。FW解説書は同概念を `コンポーネント名` と呼ぶ（`ja/` 全体70件、`web_front_controller.rst:34`・`:95`） | 表のセルと地の文の2箇所を `コンポーネント名` に是正 |
| R1-2 | C | `ウェブアプリケーション実行基盤` / `RESTfulウェブサービス実行基盤` は本ページにしか無い造語。FW解説書は同じシナリオを「ウェブアプリケーションとウェブサービスを併用したい場合」と書く（`web_front_controller.rst:85-88`） | 「ウェブアプリケーションとRESTfulウェブサービスを併用し、ハンドラ構成の異なるWebフロントコントローラを複数定義する構成」に是正 |
| R1-3 | C | 「1つのWARで動かす場合に指定する」は実装より狭い。実装の条件は「`WebFrontController` が `webFrontController` 以外の名前で登録されている」だけ（`SimpleRestTestSupport.java:270`） | 条件を「`webFrontController` 以外のコンポーネント名で登録している場合」に一般化し、具体例として併用構成を挙げる形にした |
| R1-4 | C | 「デフォルト値は、前述の `nablarch/test/rest-request-test.xml` が設定する値である」は不正確。実値は `rest-request-test.xml` が `<config-file>` で読む `nablarch/test/http-request-test/http-request-test.config:1,12` にある | 「デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す」に是正 |
| R1-5 | C | `ウェブアプリケーションのルートディレクトリ` は、RESTfulウェブサービスのページでは処理方式名の `ウェブアプリケーション`（`glossary.md` §5.2）と referent が衝突する | 「内蔵サーバに配備するウェブアプリケーションのルートディレクトリ」に是正し、referent を内蔵サーバに固定した。姉妹ページの語（`ウェブアプリケーションのルートディレクトリ`）は残しているため、同一プロパティの説明として読み比べられる |
| R1-6 | B・D | `webBaseDir` の複数指定を説明する段落が、承認済み `web.rst:88` と105文字にわたり逐語一致していた | REST側の文として組み直し、実装で確認した「最初に見つかったリソースを使用する」（Jetty の `CombinedResource`）まで含めた |
| R1-7 | A | 上書き例のXMLが `</component>` 未閉じで終わっていた（出典 `:355-361` も切れている） | 閉じた。`webBaseDir` の例も `<component>` を含む完全な形に揃えた |
| R1-8 | B | L3見出しの下線が48文字。NTF他ページはすべて49 | 49に是正 |
| R1-9 | B | 「もあわせて使用できる」は `ja/` 全体で本ページ以外に1件のみ。FW解説書ライブラリの定型は「〜することで」（88件） | 「上記の3つを追加することで、…も使用できる」に是正 |
| R1-10 | B | コードブロック内のコメント「デフォルト設定のコンポーネント定義を上書きする」が直前の地の文の言い換えだった | コメントを削除した |
| R1-11 | A | 出典 `:78-80` の「アーキタイプからブランクプロジェクトを作成した場合、`unit-test.xml` にテスティングフレームワークの設定がされている」という事実が括弧書きに圧縮され、含意が弱まっていた | 「テスティングフレームワークの設定は、テスト用のコンポーネント設定ファイルに記述する。ブランクプロジェクトでは `src/test/resources/unit-test.xml` が該当する」と独立した文に戻した |
| R1-12 | D | `tip` が設定ファイルの読み込みにしか触れていないが、RESTfulウェブサービスのブランクプロジェクトには依存関係3件も定義済み（`nablarch-jaxrs-archetype-6u3` の `pom.xml:262-279`）。読者が重複して追加しかねない | `tip` を「上記の依存関係と設定が既に記述されている」に拡張し、他2つは「不足している記述を追加する」とした（`nablarch-web-archetype` は `httpServerFactory` を登録済み・`nablarch-batch-archetype` は jetty12 も持たないため、一律の記述にできない） |
| R1-13 | B | 本ページだけ `important` が0件で、`webFrontControllerKey` 未設定時の落とし穴が地の文にあった | R1-M1 の `httpServerFactory` を `important` に切り出した。`webFrontControllerKey` の方は、指定する条件を述べる段落の結論であり、切り出すと直上の言い換えになるため地の文のままとした（`#15` の R2-1 の再発防止） |

#### 対応しなかった指摘

| # | 観点 | 指摘 | 判断 |
|---|---|---|---|
| R1-X1 | A | 上書き例に「`webBaseDir` を再指定しないとクラスの既定値 `../main/web` に戻る」旨の注記を足すべき（`DiContainer.java:319` が名前単位で丸ごと置換するため） | **対応しない。事実誤りである。** 観点A は `DiContainer.register()` だけを見ているが、XMLからの読み込みでは `XmlComponentDefinitionLoader.java:214` が `mergeComponentDefinitions` を呼び、`:282-297` で**同一クラスなら先の定義のプロパティを引き継ぐ**。FW解説書 `libraries/repository.rst:188-189` も「同じクラスを設定した場合、上書き前のpropertyへの設定が上書き後のクラスに全て引き継がれる」と明記している。観点C・Dはいずれも独立に同じ結論に達しており、**観点AとC・Dで判断が割れた1件** |
| R1-X2 | D | `RestTestConfiguration` が `HttpTestConfiguration` を継承していること（＝`web.rst` の表の項目も指定できること）を `tip` で書くべき | **対応しない。** マッピング対象外の追加であることに加え、姉妹ページの表へ読者を誘導すると、基準の異なる `webBaseDir` のデフォルト値（R1-M5）に突き当たる。R1-M5 の `decide` が決着するまで導線は張らない |
| R1-X3 | D | `RestTestSupport` を使う場合は `testDataParser` 等の読み込みも必要だが、どのページにも記載がない | **対応しない。** 処理方式に固有ではなく `setup/common.rst` の担当範囲である。申し送りとして記録する |
| R1-X4 | B・D | `:doc:` の使用がNTF新規ページで本ページの3件のみ。ラベルを足して `:ref:` に寄せるべき | **対応しない。** 参照先3ページ（`blank_project/setup_blankProject/*`）にラベルが無く、ラベルの追加は本タスクの「絶対に変更しないファイル」の外にある他ページの変更になる。出典も `:doc:` を使っていた |
| R1-X5 | D | `ja/migration/index.rst:536` は同じ Jetty を「組み込みサーバ」と呼んでおり不統一 | **対応しない。** `glossary.md` の正表記は `内蔵サーバ` であり、NTF解説書内は統一されている。FW解説書側の語の是正は本タスクの範囲外 |
| R1-X6 | A | 出典 `:86` の「リクエスト単体テストの設定は `:ref:`rest-test-configuration`` を参照」が未反映 | **対応しない。** 参照先が同一ページの次のL3になるため、リンクにすると同じページ内を行き来するだけになる。観点A自身も「実害は無い」と判定している |
| R1-X7 | D | `:doc:` のリンク文言（`ウェブプロジェクト` 等）と参照先ページタイトル（`ウェブプロジェクトの初期セットアップ`）が一致しない | **是正済み**（リンク文言を参照先タイトルの語幹に合わせた）。初版の `ウェブアプリケーション` / `Nablarchバッチアプリケーション` から `ウェブプロジェクト` / `Nablarchバッチプロジェクト` に変えている |

### ラウンド2（2026-08-12） — 是正差分限定の検証

`#10b` の申し送りに従い、ラウンド1の是正を対象に、**「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」の2点のみ**を検証した。ページ全体の再レビューはしていない。

**判定: pass（`must` 0件）。指摘は `should` 2件・`note` 4件で、うち3件を是正した。**

| # | 区分 | 指摘 | 対応 |
|---|---|---|---|
| R2-1 | should | `tip` の「ブランクプロジェクトから作成した場合」は主客が逆。作成されるのがブランクプロジェクトであり、元はアーキタイプである。出典（`:89`）は「アーキタイプから…ブランクプロジェクトを作成した場合」と正しく書いており、書き直しで劣化していた | 「アーキタイプから\ :doc:`RESTfulウェブサービスプロジェクト`\ を作成した場合は」に是正した |
| R2-2 | should | L3見出し `必要なモジュールとデフォルト設定を追加する` が節の内容を1つ取りこぼしている。この節は (1)3モジュール (2)デフォルト設定の読み込み (3)`httpServerFactory` の登録 の3点を扱うが、(3) は同節の `important` 自身が「デフォルト設定では登録されない」と述べているため2語では覆えない。**ラウンド1の M3（改題）と M1（`httpServerFactory` の追加）が噛み合っていなかった** | `必要なモジュールとコンポーネント設定を追加する` に改題した。(2)(3) はいずれもコンポーネント設定ファイルへの記述であり、1つの見出しで覆える |
| R2-3 | note | 2つの記述例で `<import>` の有無が不揃い。`webFrontControllerKey` の例だけ `<import>` を含んでいた | `<import>` を落として2つの例を揃え、代わりに地の文へ「上書きの記述は、デフォルト設定の読み込みより後に置く」を足した。同じ内容をコード内コメントと地の文の両方に書かない形にもなる |
| R2-4 | note | `webBaseDir` のコード例の値（`/path/to/web-a/,/path/to/web-common`）が `web.rst:92` と同一 | **対応しない。** 出典（`:300`）がこの値を使っており、意味を持たないプレースホルダである。値を変えても読者の得るものは無い |
| R2-5 | note | `HttpRequestTestSupport.java:387` も同じ `httpServerFactory` を要求するのに `web.rst` には記述が無く、対の2ページで説明の粒度が食い違う | **本ページでは対応しない。** `web.rst` は承認済みで、本タスクの「絶対に変更しないファイル」に含まれる。申し送りとして記録する |
| R2-6 | note | 作業ツリーに `locales/ja/LC_MESSAGES/sphinx.mo` の差分（Docker ビルドの副産物） | コミット前に `git checkout` で戻した（`f6947b2`・`73e84dc` と同じ運用） |

**ラウンド2で新たな事実誤りは検出されなかった。** 検証側も「同名上書きで `webBaseDir` がクラス既定値に戻る」という `must` 級の指摘を立てかけたうえで、`XmlComponentDefinitionLoader.marge()` の確認により撤回している（ラウンド1の R1-X1 と同じ経路をたどって同じ結論に達した）。

**この2ラウンドで得られた最大の知見**: 出典が「これで動く」と読める手順を書いていても、実際に必要な設定が抜けていることがある（R1-M1 の `httpServerFactory`）。**出典の手順は、書き写す前に実装側の必須コンポーネントを洗い出して突き合わせる。**

## `#18` 以降への申し送り

1. **出典の手順は、実装側が要求する必須コンポーネントと突き合わせてから書く。** `#17` の `httpServerFactory` は、出典にもマッピングにも1件も現れないが、無ければ内蔵サーバの生成時に例外になる。処理方式ページの「テストを実行できるようにする」相当の節では、テストの起点クラス（`*TestSupport`）が `SystemRepository.get(...)` で引いているキーを列挙し、デフォルト設定（`nablarch-testing-default-configuration` の jar）が提供しているかどうかを確認する。
2. **`nablarch-testing-default-configuration` は GitHub に公開リポジトリが無い。** Maven Central の jar（`com.nablarch.configuration:nablarch-testing-default-configuration`）を展開して参照する。`nablarch/test/*.xml` と `nablarch/test/http-request-test/http-request-test.config` に、デフォルト値の実体がある。
3. **アーキタイプの jar（`com.nablarch.archetype:nablarch-*-archetype`）は、ブランクプロジェクトの初期状態を確認する一次資料である。** `archetype-resources/pom.xml` と `archetype-resources/src/test/resources/unit-test.xml` を見れば、依存関係・読み込む設定ファイル・登録済みコンポーネントが分かる。「ブランクプロジェクトでは設定済み」と書く前に必ず確認する。
4. **`webBaseDir` のデフォルト値は、ページによって基準が違う状態になっている**（`web.rst` はクラスのフィールド初期値 `../main/web`、`rest.rst` はデフォルト設定ファイルの値 `src/main/webapp`）。実効値はどちらのブランクプロジェクトでも `src/main/webapp` である。**残りのリクエスト単体テスト4ページを書く前に、どちらを基準にするか決める**（`#17` の `decide` 2）。
5. **同名・同一クラスのコンポーネント上書きは、先の定義のプロパティを引き継ぐ**（`XmlComponentDefinitionLoader.java:282-297`、FW解説書 `libraries/repository.rst:188-189`）。`DiContainer.register()` の `nameIndex.put` だけを見ると「丸ごと置換」に見えるため、レビュアーが誤検出しやすい（`#17` ではラウンド1・2の2回とも立てられ、2回とも撤回された）。
6. **FW解説書に同じ設定例が既にある場合は、書き写さず `:ref:` で参照する。** `#17` では出典が持っていたコンポーネント定義XML 2件を `change_web_front_controller_name` への参照で解決した。出典の内容を落とすことにはならない。
7. **`RestTestSupport` を使う場合に必要な `testDataParser` 等の読み込みが、NTF解説書のどのページにも無い**（`setup/common.rst` にも無い）。処理方式に固有ではないため `setup/common.rst` の担当範囲として扱う。
8. **`web.rst` にも `httpServerFactory` の記述が無い**（`HttpRequestTestSupport.java:387` が同じキーを要求する）。`#17` では rest 側だけに書いたため、対の2ページで粒度が食い違っている。`decide` 1 の判断が出た後、`web.rst` の追補を別タスクで検討する。
