# レビュー記録 — リクエスト単体テストの設定（ウェブアプリケーション）（`setup/request_unit_test/web.rst`）

対象タスク: `#15`。ページ先頭ラベルは `style.md` S-08 から引いた `request_unit_test_setting_web`。
`#13` で定着させた共通 Steps のみで進めるページ（個別の作業指示なし）。

## 出典

`mapping.csv` の `dest_page=リクエスト単体テストの設定（ウェブアプリケーション）` の6行（250 lines、`DROP` なし）。
出典ファイルは `#7` で削除済みのため `origin/develop` の内容で参照した。

| mapping_id | 出典行 | 見出し | dest_section |
|---|---|---|---|
| current-0204 | `02_RequestUnitTest.rst:93-96` | 構造 > AbstractHttpRequestTestTemplate | 拡張例 |
| current-0205 | `:99-103` | 構造 > TestCaseInfo | 拡張例 |
| current-0210 | `:306-309` | 各種設定値 > (L2直下) | 使用方法 |
| current-0211 | `:312-415` | 各種設定値 > コンポーネント設定ファイル設定項目一覧 | 使用方法 |
| current-0212 | `:418-471` | 各種設定値 > コンポーネント設定ファイルの記述例 | 使用方法 |
| current-0213 | `:474-552` | 各種設定値 > その他の設定 | 使用方法 |

全件の反映対応表は `checks/task-15.md` の先頭に置いた（母集合はホワイトリストで切り出していない）。

## 実装で確認した事実

参照コミット: `nablarch/nablarch-testing` の `main` = `e21bf67`（`git clone --depth 50`）。
`nablarch/nablarch-core` の `main` も1件のみ参照した（`ExecutionContext` の定数）。

| # | 本文の記述 | 実装の根拠 |
|---|---|---|
| I-1 | コンポーネント名は `httpTestConfiguration` | `HttpRequestTestSupport.java:87`（`HTTP_TEST_CONFIGURATION`）、`:240`・`:1143`（`SystemRepository.getObject` の引数） |
| I-2 | 19項目のデフォルト値 | `HttpTestConfiguration.java:24`（`./tmp/html_dump`）・`:29`（`../main/web`）・`:34`（`../test/web`）・`:40`（`null`）・`:45`（`user.id`）・`:50`（`ExecutionContext.THROWN_APPLICATION_EXCEPTION_KEY`）・`:55`（`html`）・`:61`（`UTF-8`）・`:66`（`false`）・`:69`（`null`）・`:72`（`null`）・`:75`（`./tmp`）・`:96`（`null`）・`:101`（`true`）・`:123-130`（`httpHeader` の2エントリ）・`:133`（空の `Map`）・`:139`（`css`・`js`・`jpg`）・`:147`（`true`）・`:150`（`null`） |
| I-3 | `exceptionRequestVarKey` の既定値は `nablarch_application_error` | `nablarch-core` の `ExecutionContext.java:422`（`THROWN_APPLICATION_EXCEPTION_KEY = FW_PREFIX + "application_error"`）と `:34`（`FW_PREFIX = "nablarch_"`） |
| I-4 | `webBaseDir` はカンマ区切りで複数指定でき、指定した順に探索される | `HttpRequestTestSupport.java:366-373`（`getWebBaseDir().split(",")` を順に `basePaths` へ追加）、`:210-215`（先頭から順にコピー） |
| I-5 | `xmlComponentFile` はリクエスト送信の直前にシステムリポジトリを再初期化する | `HttpRequestTestSupport.java:268-272`（`RepositoryInitializer.reInitializeRepository`）。同メソッドの `:279` で `server.handle` を呼ぶ直前である |
| I-6 | `checkHtml` が `true` で `htmlChecker`・`htmlCheckerConfig` のどちらも未設定だと例外が発生する | `HttpRequestTestSupport.java:305-311`（`getHtmlChecker()` が `null` なら `RuntimeException`）。呼び出し条件は `:285-289`（`isCheckHtml()` かつ ステータス < 500 かつ Content-Type がHTML） |
| I-7 | `htmlCheckerConfig` を設定すると `Html4HtmlChecker` が `htmlChecker` に設定される | `HttpTestConfiguration.java:358-361`（`setHtmlCheckerConfig` が `new Html4HtmlChecker(htmlCheckerConfig)` を代入） |
| I-8 | `-Dnablarch.test.skip-resource-copy=true` でHTMLリソースのコピーを抑止する。ディレクトリが無い場合は指定の有無にかかわらずコピーされる | `HttpRequestTestSupport.java:96`（プロパティ名）・`:224-226`（`Boolean.getBoolean`）・`:197-207`（ディレクトリが存在するときだけ `return` し、存在しないときはコピーを続行） |
| I-9 | `htmlResourcesCharset` はパスの書き換え対象となるHTMLリソース（`css`・`js`・`template`）の読み書きに使う | `HttpRequestTestSupport.java:665`（`.css` / `.js` / `.template` を `replaceFiles` に収集）、`:521-525`（`rewriteResourceFile` 内の `InputStreamReader` / `OutputStreamWriter` に渡す）。**当初はCSS限定と書いていたが、ラウンド1の R1-1 で是正した** |
| I-10 | `AbstractHttpRequestTestTemplate` は `TestCaseInfo` を型引数に取る | `AbstractHttpRequestTestTemplate.java:61-62`（`@Published public abstract class AbstractHttpRequestTestTemplate<INF extends TestCaseInfo> extends HttpRequestTestSupport`） |
| I-11 | `TestCaseInfo` が保持するのはテストショット1件分の情報 | `TestCaseInfo.java:33-39`（`no` / `case` / `description` の各カラム名）。いずれも `testShots` のカラムである |

`:java:extdoc:` で参照した6クラスの公開javadocはいずれも HTTP 200 を実測（`HttpTestConfiguration` / `AbstractHttpRequestTestTemplate` / `TestCaseInfo` / `HtmlChecker` / `Html4HtmlChecker` / `ApplicationException`）。

## 出典と実装が食い違った箇所（`design.md` §8 により実装を優先）

| # | 出典 | 実装 | 本文の記述 |
|---|---|---|---|
| C-1 | `jsTestResourceDir` は「javascriptの自動テスト実行時に使用するリソースの**コピー先**ディレクトリ名」（`:337`） | `FileUtils.copyDir(new File(config.getJsTestResourceDir()), destDir, filter, true)`（`HttpRequestTestSupport.java:436`）であり、**コピー元**である。コピー先は `destDir`（ダンプディレクトリ配下） | 「JavaScriptの自動テストで使用するリソースを配置したディレクトリ」 |
| C-2 | `htmlChecker` のデフォルト値は「`Html4HtmlChecker` クラスのインスタンス。クラスには `htmlCheckerConfig` で設定した設定ファイルが適用される」（`:345-348`） | フィールドの初期値は `null`（`HttpTestConfiguration.java:150`）。`Html4HtmlChecker` が入るのは `htmlCheckerConfig` を設定したときだけ（`:358-361`） | デフォルト値は「該当なし」とし、`htmlCheckerConfig` 側の説明に「この項目を設定すると `Html4HtmlChecker` が `htmlChecker` に設定される」と書いた |
| C-3 | `htmlCheckerConfig` のデフォルト値は `test/resources/httprequesttest/html-check-config.csv`（`:351`） | フィールドの初期値は `null`（`HttpTestConfiguration.java:96`）。この値を既定として与えるコンポーネント定義は `nablarch-testing` の `src/main/` に存在しない（`src/main/resources` 自体が無い） | デフォルト値は「該当なし」とした。当該パスは記述例（`:465-466`）に残っており、記述例としては保持されている |
| C-4 | `htmlResourcesExtensionList` のデフォルト値は `css、jpg、js`（`:335`） | `Arrays.asList("css", "js", "jpg")`（`HttpTestConfiguration.java:139`） | 実装の並び順に合わせて `css`・`js`・`jpg` とした（内容は同じ）。ラウンド1の R1-5 で、XML記述例の並びも同じ順に揃えた |

C-2・C-3 の結果として「`checkHtml` は既定で `true` なのに、HTMLチェッカーは既定で存在しない」という状態が本文の表から読み取れるようになる。
この組み合わせが実行時に何を起こすかは `.. important::` として明記した（I-6）。`#14` の申し送り5（例外を投げる行だけでなく呼び出し元の条件まで辿る）と申し送り6（制約には実装の挙動を理由として書き添える）の適用である。

## 作成時の判断

### D-1 画像4件を `setup/request_unit_test/images/web/` へ移した

| 項目 | 内容 |
|---|---|
| 対象 | `vmoptions.png` / `installed_jre.png` / `edit_jre.png` / `skip_resource_copy.png`（`git mv`。バイナリは無変更） |
| 移動元 | `guide/development_guide/06_TestFWGuide/_images/`（`#7` で `.rst` のみ削除し、画像は保持されていた） |
| 理由 | 本ページはNTF解説書の新構成で**最初に画像を使うページ**である。`design.md` §13 のツリーに `guide/` は存在せず、いずれ削除される想定であるため、旧ツリーへの相対参照（`../../guide/development_guide/06_TestFWGuide/_images/…`）を新ページに残せない。配置は FW解説書の `images/<ページ名>/<ファイル名>` の形（`FW:libraries/mail.rst:20` → `images/mail/mail_system.png`）に倣った |
| 影響 | 残り30ページのうち画像を使うページは同じ形（`images/<ページ名>/`）に従うことになる。**この配置規約は `design.md`・`style.md` のいずれにも無い新規の判断であり、user review で確認したい**（`decide`） |

### D-2 出典の脚注2件を表の外の地の文にした

出典 `:396-412` の脚注2件（`webBaseDir` の複数指定、`xmlComponentFile` の再初期化）は、表のセルからの `[#]_` 参照で書かれている。
本文では脚注機構を使わず、表の直後の地の文に置いた。脚注1はコードブロックを含み `list-table` のセルにも脚注定義にも収まりが悪いこと、`ja/` の既存ページで説明表の脚注が使われていないことによる。内容（カンマ区切り・探索順・記述例・再初期化の時点・「通常は設定する必要はない」・クラス単体テストと設定を変える場合のみ）はすべて保持している。

### D-3 `その他の設定` を「テストの実行速度を上げる」に改題し、L4 2つに分けた

出典のL3見出しは `その他の設定` だが、`style.md` S-03 の内容条件が `その他` を明示的に禁じている。
出典自身が「リクエスト単体テスト実行速度を向上させたい場合は、以下の設定をすることで実行速度の改善が見込まれる」（`:475-476`）と、配下2件の目的を1つに束ねているため、その目的をL3見出しにした。
配下は出典のL4（`JVMオプションの指定` / `HTMLリソースコピーの抑止`）を S-03 の「〜する」形式に直して踏襲した。L3の導入文には配下2件が何かを書いた（S-11）。

### D-4 `tip` からCPUの製品名を落とした

出典 `:478-480` の `tip` は「Pentium4、Pentium Dual-Core等の処理性能が低いCPUを搭載したPCに効果がある。逆に、これら以降のCPUを搭載したマシンでは、それほど効果的ではない」である。
本文では製品名2件を落とし、「処理性能が低いCPUを搭載したPCで効果がある。比較的新しいCPUを搭載したPCでは効果が小さいため、無理に設定する必要はない」とした。ラウンド1の R1-8 で前半が導入文の言い換えになっていると指摘されたため、最終的に「JVMオプションの指定は、比較的新しいCPUを搭載したPCでは効果が小さいため、無理に設定する必要はない」の1文にした。
`tip` が伝えている事実（効果はCPUの世代に依存する／新しいCPUでは無理に設定しなくてよい）は保持しているが、**製品名という具体は落としている**。`decide` として user review に上げる。

### D-5 `-Xverify:none` の非推奨を `important` で書き足した

出典は `-Xverify:none` を無条件に勧めている（`:492-494`）が、このオプションはJDK 13で非推奨になっている。
ローカルの Temurin 21.0.11 で `java -Xverify:none -version` を実行し、`Options -Xverify:none and -noverify were deprecated in JDK 13 and will likely be removed in a future release.` の警告が出たうえで**起動自体は成功する**（exit 0）ことを実測した。
オプションを落とすと「マッピングにある内容を落とさない」に反し、そのまま書くと読者が非推奨と知らずに設定するため、**残したうえで理由を書き添える**形にした（`#14` 申し送り6 と同型）。
`nablarch-testing` の実装ではなくJVMの挙動に対する追記であるため、**マッピングにない内容の追加に当たるかどうかを user review で確認したい**（`decide`）。

### D-6 EclipseのUIラベルは画面キャプチャの表記に合わせた

`style.md` は本文の用語を FW解説書に合わせることを求めるが（`#11` R1-1 で `VM引数` → `システムプロパティ` に改めた前例がある）、本節の「VM 引数」はEclipseの画面上のラベルそのものである。
`vmoptions.png` を実際に開いて確認し、フィールドのラベルが `VM 引数(G):`、タブが `引数` であることを確認して、本文を「「VM 引数」欄」に揃えた。同様に `edit_jre.png` のラベルは `デフォルトの VM 引数(V):` であるため、出典の「「VM引数」欄」（`:513`）を「「デフォルトの VM 引数」欄」に改めた（**出典の記述がEclipseの実際のラベルと異なっていた**）。
システムプロパティ・JVMオプションを指す地の文では `システムプロパティ`・`JVMオプション` を使っている。

### D-7 前方参照のスタブを2件先行作成した

| ファイル | ラベル | 理由 |
|---|---|---|
| `implementation/request_unit_test/web.rst` | `request_unit_test_web` | 本ページがHTMLダンプへ2箇所リンクする。HTMLダンプ出力の説明（`current-0209`）の割当先が第3部の当該ページである |
| `tools/html_check_tool.rst` | `html_check_tool` | 出典 `:348` の `:ref:`customize_html_check`` に対応する。参照先は第4部「HTMLチェックツール」 |

いずれも見出しのみで作成し、対応する `toctree`（`implementation/index.rst` / `tools/index.rst`）に追記した（`steering.md`「前方参照によるスタブページ」の運用）。
ラベルは `style.md` S-08 の一覧から引いており、新規に考案していない。
出典が指していたラベル `customize_html_check` は旧ページのセクションラベルであり、S-08 が定めるページ先頭ラベルに置き換えた。

### D-8 表2件をいずれも `list-table` にした

設定項目一覧はセルに `:java:extdoc:`・`:ref:` と長文の説明を含むため `list-table` が必要である（S-07）。
`sessionInfo` のキー表は3列の短い表だが、`#14` 申し送り4（1つでも `list-table` が必要な表があるページは短い表も揃える。S-07:241「本例外の適用はページ単位で判断する」）に従い `list-table` に揃えた。

## `#16` 以降への申し送り

1. **画像は `images/<ページ名>/` に置く**（D-1）。旧ツリー `guide/development_guide/**/_image(s)/` に残っている画像は、そのページを作るタスクで `git mv` して移す。`design.md` §13 のツリーに画像ディレクトリの記載が無いため、全ページの移設が終わった時点で §13 に追記するか、`#last` で一括整理するかを決める必要がある。
2. **出典の「デフォルト値」欄は、フィールドの初期値と一致しているとは限らない**（C-2・C-3）。セッターが副作用で他のフィールドを設定する場合（`setHtmlCheckerConfig` → `htmlChecker`）、出典は「その副作用の結果」をデフォルト値として書いていることがある。**設定項目一覧を書くときは、フィールド宣言の初期値を1件ずつ確かめる。**
3. **出典がEclipse等のUI操作手順を持つ場合は、添付の画面キャプチャを実際に開いてラベルを確認する**（D-6）。出典の地の文とキャプチャのラベルが食い違っていた実例がある。
4. **`-Xverify:none` のように、出典が前提としていた実行環境が現在は変わっている記述がある。** JVMオプション・JDKバージョン・OS依存の記述は、書く前に現在の挙動を確認する（D-5）。
5. **`design.md` §13 のツリーに `guide/` が無い一方、実体は画像・ダウンロード素材を保持したまま残っている。** `#last` で `guide/` を空にできるかどうか（参照が残っていないか）を確認する。
6. **`design.md` §13 のツリーは「ファイル→サブディレクトリ」というファイルシステムの並びであり、`toctree` の順序の根拠にはならない**（R1-X2）。`toctree` の順序は §3・§4・§5 の各部の構成に従う。**`implementation/index.rst` には `request_unit_test/web` を末尾に追記したが、第3部の順序ではエンティティ単体テスト・コンポーネント単体テストが先に来る。** それらを作るタスクでは末尾に追記せず、`testdata_examples` の直後に挿入すること。
7. **`httpHeader` のセッターはマップ全体を置換する**（`HttpTestConfiguration.java:376-378`）。記述例のように一部だけ書くと既定の2エントリが失われる。本ページでは出典に無い挙動のため書かなかったが（R1-X6）、同種の `Map` プロパティを扱うページでは注意する。
8. **`glossary.md` §8 の置換対応表は、左辺を全件走査して残存を確認する。** 観点Cはこの走査で `オーバヘッド`・`基底クラス` のような**表の左辺に載っていない語**（FW解説書の用法・§5.14 の正表記に照らして初めて分かる語）も拾った。置換表の機械適用だけでは足りない。
9. **`#15` はレビュアー間で判断が2件割れた**（R1-X1 `:java:extdoc:` のリンク可否、R1-X5 `データシート` の置換先）。いずれも実測（javadocのHTTPステータス／`glossary.md` §5.9 の方針）で決着させ、本文は現状維持とした。

## レビュー記録

### ラウンド1（2026-08-12）

4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を、それぞれ**別のサブエージェント**で実施した。各観点には成果物・目的・完了条件・チェックリストのみを渡し、`checks/`・`reviews/` 配下の自己申告記録は渡していない。プロンプトには Rules の3点（実測で裏付ける／付属の検証物を正解にせず独立に組む／敵対的に見る）を入れた。

**判定: A pass / B pass / C fail（`must` 3）/ D fail（`must` 1）。`must` は重複を除いて3件。**

| 観点 | 判定 | must | should | note |
|---|---|---|---|---|
| A 網羅性 | pass | 0 | 4 | 6 |
| B トンマナ | pass | 0 | 5 | 7 |
| C 用語 | fail | 3 | 6 | 5 |
| D 整合性 | fail | 1 | 3 | 6 |

#### must（3件・すべて是正）

| # | 観点 | 指摘 | 根拠 | 対応 |
|---|---|---|---|---|
| R1-M1 | C・D | `dumpVariableItem` の説明が**実装と逆**。ページは「可変項目を出力するかどうか。毎回同じ内容にしたい場合は `false`」としていたが、実装は `true` のときに JSESSIONID と `nablarch_token` を**除去**する | `HttpServer.java:427-430`（`if (dumpVariableItem) { JSESSIONID_PATTERN.replaceAll(""); NABLARCH_TOKEN_PATTERN.replaceAll(""); }`）。設定値の受け渡しは `HttpRequestTestSupport.java:275` の1経路のみ。コーディネータが実コードで再確認済み | 「HTMLダンプから可変項目を除去するかどうか。…毎回同じ内容にしたい場合は `true` を指定する」に是正し、プロパティ名と挙動が逆である旨を `tip` に出した。**出典（`:379-392`）もフィールドのjavadoc（`HttpTestConfiguration.java:64`）も同じ誤りを持っており、出典を引き写すと必ずこの誤りに落ちる型である** |
| R1-M2 | C | `オーバヘッド` は FW解説書の用法（`オーバーヘッド`）に反する | `grep -rc "オーバヘッド" ja/` は本ページ1件のみ。`オーバーヘッド` は `azure_distributed_tracing.rst:27`・`micrometer_adaptor.rst:679` に実在。`glossary.md` §5.14 も語中の長音を保つ方針（`オーバーライド` を正表記に採用） | `オーバーヘッド` に是正 |
| R1-M3 | C | `基底クラス` は同概念の正表記 `スーパクラス`（`glossary.md:318`）を使っていない | `grep -rc "基底クラス" ja/` は本ページと `biz_samples/01/index.rst` の2件のみで FW解説書に0件。出典自身（`:85`）が同じ対象に「スーパクラス」を使っている | `スーパクラス` に是正。あわせて `前者`/`後者` をクラス名に戻した（B-N3） |

#### should / note のうち是正したもの

| # | 観点 | 指摘 | 対応 |
|---|---|---|---|
| R1-1 | C・D | `htmlResourcesCharset` の説明「CSSファイル（スタイルシート）の文字コード」が実装より狭い。実装は `.css`・`.js`・`.template` の読み書きに使う（`HttpRequestTestSupport.java:665`・`:521-525`） | 「パスの書き換え対象となるHTMLリソース（`css`・`js`・`template`）の文字コード」に是正。出典（`:341`）の誤りの是正でもある |
| R1-2 | C | `セッションのキー`／`セッションに格納する値` は FW解説書の `セッションスコープ`（FW21件）に揃えるべき。実装も `ctx.setSessionScopedVar`（`HttpRequestTestSupport.java:1133`）・`context.getSessionScopeMap()`（`HttpRequestTestSupportHandler.java:95`） | 両セルを `セッションスコープ` に是正 |
| R1-3 | C | `Jetty` を直接名指ししており、`glossary.md` §5.12 の正表記 `内蔵サーバ` を一度も導入していない。実装上も `HttpServer` は `HttpServerFactory` 経由の差し替え式（`HttpServer.java:52`） | `内蔵サーバ（Jetty）` に是正（正表記を主・製品名を従） |
| R1-4 | B | `（なし）` は `ja/` 全体で本ページにしか無い表記。同じ列で `（なし。Jettyの…）` と括弧の用法が割れている | `該当なし` に統一（`testdata_notation.rst:1413` の `該当なし（…）` と同形）。補足が要る1行だけ `該当なし（内蔵サーバ（Jetty）のデフォルト動作に従う）` |
| R1-5 | B・D | `htmlResourcesExtensionList` の並びが表（`css`・`js`・`jpg`）と記述例（`css`/`jpg`/`js`）で不一致 | 記述例の並びを実装のデフォルト値（`HttpTestConfiguration.java:139`）に揃えた。表の側が実装どおりで正しいため、例を動かした |
| R1-6 | D | 導入文が「設定できる項目は次のとおりである」と網羅を主張しているが、実装には表に無い `htmlResourcesRoot`（`HttpTestConfiguration.java:144`、既定値 `htmlResources`）がある | **項目は追加せず**（「マッピングにない内容を追加しない」）、導入文を「主な設定項目は次のとおりである」に緩めた |
| R1-7 | C | `tip` の「HTMLリソースのディレクトリ」がページ上で特定できない。実装の判定対象は `new File(htmlDumpDir, htmlResourcesRoot)`（`HttpTestConfiguration.java:420-422`） | 「ダンプディレクトリ配下の `htmlResources` ディレクトリ」と referent を明示。あわせて `htmlDumpDir` の説明で `ダンプディレクトリ` の語を導入した（C S-2） |
| R1-8 | B | 実行速度の `tip` が直前の導入文の言い換えになっている（CPU製品名を落とした結果、残ったのが重複部分だけになった） | 「比較的新しいCPUを搭載したPCでは効果が小さいため、無理に設定する必要はない」の1文に絞った |
| R1-9 | A・B | Eclipse操作手順が出典と**3文完全一致**し、かつページ内2箇所でほぼ逐語重複していた | 1箇所目は文の組み立てを変えて書き直し、箇条書きの粒度も揃えた。2箇所目は手順を書かず「JVMオプションと同じ実行構成の「VM 引数」欄である」の1文＋画像に縮めた |
| R1-10 | B | `:ref:`HTMLダンプ <request_unit_test_web>`` のリンク文言が参照先ページのタイトルと一語も重ならない | リンク文言を参照先タイトル `リクエスト単体テスト（ウェブアプリケーション）` に是正し、同じL4内の2度目はリンクにしない形にした |
| R1-11 | B・C | 見出しの `記法` と直後の本文の `書き方` が同じ対象で揺れていた | 見出しを `テストデータの書き方を拡張する` に是正（第3部のページ題「テストデータの書き方」と揃う） |
| R1-12 | D | `checkHtml` の `important` が発火条件のステータスコードに触れていない（実装は `res.getStatusCode() < 500` も条件。`HttpRequestTestSupport.java:285-289`） | 「ステータスコードが500未満のHTMLレスポンスに対する」を補った |
| R1-13 | D | 記述例の導入文「デフォルト値のままでよい項目も含めて記述しており」が、例に含まれる非デフォルト値（`xmlComponentFile`・`tempDirectory`・`htmlCheckerConfig`）と食い違う | 「デフォルト値と同じ値を明示的に記述している項目もある」に改めた |

#### 対応しなかった指摘

| # | 観点 | 指摘 | 判断 |
|---|---|---|---|
| R1-X1 | A | `Html4HtmlChecker` の `:java:extdoc:` は `@Published` が無く、`nablarch.test.tool.*` を extdoc で参照した先例も0件なのでリンクを外すべき | **対応しない。** 観点Dが同じクラスの公開javadocを実測して **HTTP 200** を確認しており（コーディネータ側でも `curl -o /dev/null -w "%{http_code}"` で 200 を再実測）、リンクは解決する。`:java:extdoc:` の解決先は `javadoc/` であり `publishedApi/` ではないため `@Published` の有無は関係しない。**観点AとDで判断が割れた1件** |
| R1-X2 | D | `setup/index.rst` の `toctree` で `request_unit_test/web` を `junit5_extension` より前に入れたのは `design.md` §13 のツリー・1対1対応表の順序と食い違う | **対応しない。** `design.md` §13 のツリーは**ファイルシステムの並び**（ファイル→サブディレクトリの順）であり、読者の閲覧順を定めたものではない。読者向けの順序は §3 の第2部構成（共通設定 → クラス単体テストの設定 → **リクエスト単体テストの設定** → 取引単体テストの設定 → JUnit 5用拡張機能 → マスタデータ復旧機能）であり、`toctree` はこちらに従う。現在の挿入位置は §3 どおりである |
| R1-X3 | D | `htmlResourcesRoot` を20項目目として表に追加すべき | **対応しない**（R1-6 で導入文を緩めることで解決）。出典に無い設定項目を足すと「マッピングにない内容を追加しない」に反する |
| R1-X4 | A | `-Xverify:none` のJDK 13非推奨注記はリポジトリ内に根拠が無く `decide` 相当 | **本文は現状維持**。user review に `decide`（D-5）として上げる |
| R1-X5 | A | `データシートに定義された` → `テストデータに定義された` は `glossary.md:566` の置換規則（`データシート` → `シート`）と食い違う | **対応しない。** 観点Cが同じ箇所を検証し「形式非依存の総称に置いた選択は §5.9 の方針に整合する」と判定している。`シート` はExcel形式のシートを指す語であり、YAML形式では成り立たない。**観点AとCで判断が割れた1件** |
| R1-X6 | C・D | `httpHeader` のセッターはマップ全体を置換するため、一部だけ書くと既定の2エントリが失われる旨を補足すべき | **対応しない。** 出典に無い挙動の追記であり、`decide` の件数をこれ以上増やさない。`#16` 以降への申し送りとする |
| R1-X7 | C | `BasicHttpRequestTestTemplate` に触れずに `AbstractHttpRequestTestTemplate` へ説明を寄せている | **対応しない。** `BasicHttpRequestTestTemplate` の説明（`current-0203`）の割当先は第3部「リクエスト単体テスト（ウェブアプリケーション）」であり、本ページのマッピング対象外である |

ラウンド1の是正はコミット `f4c9fad`（`web.rst` のみ）。Docker フルビルドは `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）。

### ラウンド2（2026-08-12） — 是正差分限定の検証

`#10b` の申し送りに従い、ラウンド1の是正差分（`ae89097..f4c9fad`、`web.rst` のみ）を対象に、**「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」の2点のみ**を検証した。ページ全体の再レビューはしていない。

**判定: pass（`must` 0件）。指摘は `should` 3件・`note` 6件で、うち5件を是正した（コミットは下記）。**

| # | 区分 | 指摘 | 対応 |
|---|---|---|---|
| R2-1 | should | ラウンド1で追加した `dumpVariableItem` の `tip` が直上の表セルの言い換えで、**ラウンド1で削らせた欠陥（`tip` が直前の文の言い換え）を是正が別の場所で再生産していた**。`tip` の新設自体も指示範囲外 | `tip` を削除し、注意を表セルの1文に畳んだ |
| R2-2 | should | `tip` が `htmlResources` をリテラルで名指しするが、それを決める `htmlResourcesRoot` はページに無い（R1-6 で表への追加を見送ったため）。読者は変更可能である事実を知れない | 表に項目を足さず（マッピング外の追加を避けるため）、`tip` を「HTMLリソースのコピー先ディレクトリ（デフォルトは `htmlResources`）」に書き換えた |
| R2-3 | should | R1-1 で `htmlResourcesCharset` に `template` を挙げた結果、直上の `htmlResourcesExtensionList`（`css`・`js`・`jpg`）との不整合がページ上で説明されない状態になった。実装では `.css`・`.js`・`.template` は拡張子リストと無関係に書き換え対象になる（`HttpRequestTestSupport.java` の `HtmlResourceExtensionFilter#accept`）| `htmlResourcesCharset` の説明に「`htmlResourcesExtensionList` の指定によらず書き換えの対象になる」を足した |
| R2-4 | note | 距離のある後方参照は「上記」より「前述」が本解説書の用法（`testdata_notation.rst:586` 等） | 2箇所目を「前述のオプション」に戻した |
| R2-5 | note | 1文中で「リクエスト単体テスト」が2回（リンク文言を参照先タイトルに合わせた副作用） | 前半を「テストの実行時に」に改めた |
| R2-6 | note | `sessionInfo` の実体は `null` ではなく空の `Map`（`HttpTestConfiguration.java:133`） | **対応しない。** 他5項目は `null` 初期化で「該当なし」が正しく、読者にとっての意味（初期状態で格納される値は無い）は同じ。1項目だけ表記を変えると列内が不揃いになる |
| R2-7 | note | 「該当なし」の外部前例は無い（`testdata_notation.rst:1413` のみ。FW解説書に0件） | 記録のみ。ラウンド1の指示どおりの是正である |

**ラウンド2で新たな事実誤りは検出されなかった。** 是正した各箇所（`dumpVariableItem` の反転・`checkHtml` の `important` の発火条件・`htmlResources` ディレクトリの `tip`・セッションスコープ・拡張子の並び・記述例の導入文・スーパクラスと型引数）は、いずれも実コードまで辿って実装と一致することを再確認した。

**この2ラウンドで得られた最大の知見**: 是正そのものがレビュー済みの規範に違反することがある（R2-1）。是正差分限定の検証を回さなければ、ラウンド1で指摘された欠陥と同型のものが残ったまま閉じていた。

## 追加の申し送り（ラウンド2から）

10. **是正で `tip` / `important` を新設するときは、直上の本文・表セルの言い換えになっていないか確認する。** `#15` の R2-1 は、ラウンド1で「`tip` が直前の導入文の言い換え」と指摘された欠陥を、別の箇所で是正自身が作り直した例である。
11. **実装の挙動に合わせて1つのセルを直すと、隣のセルとの整合が崩れることがある**（R2-3）。表のセルを是正したら、同じ対象に触れている他のセルを読み直す。

## `#16` リード文の移動と `decide` 3件の規定化（2026-08-12）

### リード文の移動

`#16`（`ntf-doc-16-lead-and-design.md`）で、`使用方法` の直下にあった導入文をページ先頭（目次 `.. contents::` の直後、`使用方法` の見出しより前）へ移した。規約は `mapping/style.md` S-02、アウトラインへの反映は `design.md` §3 に書いた。

| | 内容 |
|---|---|
| 移動前（`使用方法` 直下、`:12`） | ここでは、ウェブアプリケーションのリクエスト単体テストで使用する設定項目と、テストの実行速度を上げる設定について説明する。 |
| 移動後（目次の直後、`:10`） | ウェブアプリケーションのリクエスト単体テストでは、テストで使用する設定項目と、テストの実行速度を上げる設定を指定できる。 |

文頭の `ここでは、` を落とし、`ウェブアプリケーションのリクエスト単体テストでは、` と主語を立てて文末を `〜を指定できる。` の言い切りに変えた。説明の対象（設定項目と実行速度の設定）は変えていない。

見出しの文言・並び順、L3以下の本文・表・コードブロックは変更していない（`checks/task-16.md` ゲート3）。

### `#15` の `decide` 3件の帰結

user review で3件とも本ページの判断が承認され、`#16` で `design.md` に規定として書き残した。以降のページはこの規定に従う。

| `decide` | 帰結 | 規定の置き場所 |
|---|---|---|
| 1. 画像の配置規約 | 承認。ページの `.rst` があるディレクトリの下に `images/<ページのファイル名>/` を作る形に統一する | `design.md` §13「画像の配置」 |
| 2. CPU製品名の削除 | 承認。陳腐化した例示は落としてよい（§11.3「マッピングにある内容を落とさない」の例外） | `design.md` §8「出典と確定設計が食い違う場合」 |
| 3. `-Xverify:none` の非推奨の追記 | 承認。§8 の「実装」には出典が前提にしている外部の挙動（JVM・JDK・データベース・ビルドツール）を含む（§11.3「マッピングにない内容を追加しない」の例外） | `design.md` §8「出典と実装が食い違う場合」 |

いずれも実測の記録を `reviews/page-*.md` に残すことが条件として規定に入っている。本ページの該当記録は上記の各節（CPU製品名の削除の理由、Temurin 21 での `-Xverify:none` の起動確認）である。

---

## `#18` デフォルト値の基準の是正（2026-08-13、作業指示 `ntf-doc-18-default-value-basis.md`）

`#17` の `decide` 2 の回答により、設定項目表の「デフォルト値」の基準が**デフォルト設定
（`nablarch-testing-default-configuration`）を読み込んだ状態で有効になる実効値**に確定した
（規定は `design.md` §8「設定項目表の「デフォルト値」の基準」）。本ページは `#15` の作成時に
**クラスのフィールド初期値**を採っていたため、基準に合わせて是正した。既存の記録は書き換えていない。

### `#15` の C-2・C-3 の判断が覆ったことの明記

**`#15` の C-2・C-3（`htmlChecker`・`htmlCheckerConfig` のデフォルト値を「該当なし」とした判断）は、
`#18` で覆った。** 当時の判断は「フィールドの初期値は `null` であり、この値を既定として与える
コンポーネント定義は `nablarch-testing` の `src/main/` に存在しない」ことを根拠にしていたが、
**探索範囲が `nablarch-testing` の `src/main/` に限られていたことが誤りであった。**
デフォルト設定は別モジュール `com.nablarch.configuration:nablarch-testing-default-configuration` にあり、
そこに当該の定義が存在する。出典（`02_RequestUnitTest.rst:345`・`:351`）が書いていた値は、
フィールド初期値ではなく**このデフォルト設定を読み込んだ実効値**であり、**出典が正しかった。**

- C-2 の帰結: `htmlChecker` のデフォルト値は「`htmlCheckerConfig` の設定に伴って設定される
  `Html4HtmlChecker`」に是正した。**デフォルト設定は `htmlChecker` を直接は設定しない。**
  `http-request-test.xml:29-30` が `htmlCheckerConfig` を設定し、その副作用として
  `HttpTestConfiguration.java:358-360`（`e21bf67`）の `setHtmlCheckerConfig` が
  `this.htmlChecker = new Html4HtmlChecker(htmlCheckerConfig)` を実行する。したがって
  「デフォルト設定が `htmlChecker` を設定する」とは書いていない
- C-3 の帰結: `htmlCheckerConfig` のデフォルト値は
  `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` に是正した
  （`http-request-test.xml:29-30` → `http-request-test.config:5`）。出典が書いていた
  `test/resources/httprequesttest/html-check-config.csv` とはパスが異なるが、これは 6u3 の
  デフォルト設定の実値であり、実効値を採る基準に従った
- `#15` の申し送り2「出典の『デフォルト値』欄は、フィールドの初期値と一致しているとは限らない」は
  **方向が逆だった。** 正しくは「**フィールドの初期値が実効値と一致しているとは限らない。
  デフォルト設定を読み込んだ実効値を確かめる**」である。以降のページはこちらに従う

### 是正した箇所と根拠（`file:line` とコミット／成果物）

デフォルト設定の実効値は、`nablarch-testing-default-configuration` **6u3** の jar 内の次の2ファイルの組で
決まる。以下 `xml` = `nablarch/test/http-request-test.xml`、`config` =
`nablarch/test/http-request-test/http-request-test.config`。jar はローカル Maven リポジトリ
（`~/.m2/repository/com/nablarch/configuration/nablarch-testing-default-configuration/6u3/`）から展開して確認した。

| 箇所 | 設定項目 | 是正前 | 是正後 | 根拠 |
|---|---|---|---|---|
| 表 `:29` | `webBaseDir` | `../main/web` | `src/main/webapp` | `xml:15` → `config:1` |
| 表 `:47` | `sessionInfo` | 該当なし | `commonHeaderLoginUserName`＝`リクエスト単体テストユーザ`、`commonHeaderLoginDate`＝`20100914` | `xml:19-25` → `config:3-4` |
| 表 `:50` | `htmlResourcesExtensionList` | `css`・`js`・`jpg`（3件） | `css`・`jpg`・`js`・`less`・`png`・`template`・`woff`・`eot`・`svg`・`ttf`（10件） | `xml:36-49`（リテラル） |
| 表 `:53` | `jsTestResourceDir` | `../test/web` | `src/test/webapp` | `xml:16` → `config:2` |
| 表 `:65` | `htmlChecker` | 該当なし | `htmlCheckerConfig` の設定に伴って設定される `Html4HtmlChecker` | `HttpTestConfiguration.java:358-360`（`nablarch/nablarch-testing` `e21bf67`） |
| 表 `:68` | `htmlCheckerConfig` | 該当なし | `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` | `xml:29-30` → `config:5` |
| 表 `:71` | `ignoreHtmlResourceDirectory` | 該当なし | `.svn` | `xml:59-62`（リテラル） |
| 表 `:74` | `tempDirectory` | 該当なし（Jetty のデフォルト動作に従う） | `target/tmp` | `xml:65` → `config:11` |
| `tip` `:216` | `htmlResourcesRoot` | `htmlResources` | `../htmlResources` | `xml:52` → `config:7`。フィールド初期値は `HttpTestConfiguration.java:144` の `htmlResources` |

表の**残り11行は是正不要**であった（全19行の照合表は `checks/task-18.md` ゲート1）。うち4行
（`backup`・`htmlResourcesCharset`・`checkHtml`・`dumpVariableItem`）はデフォルト設定が設定しているが
値がフィールド初期値と同じ、7行（`htmlDumpDir`・`xmlComponentFile`・`userIdSessionKey`・
`exceptionRequestVarKey`・`dumpFileExtension`・`httpHeader`・`uploadTmpDirectory`）はデフォルト設定が
設定していないためフィールド初期値がそのまま実効値になる。

### 表に連動して是正した地の文

| 箇所 | 是正の内容 | 理由 |
|---|---|---|
| `:16` の導入文 | デフォルト設定を読み込むと `HttpTestConfiguration` が `httpTestConfiguration` というコンポーネント名で登録されること、同じ名前で上書きして変更すること、上書きはデフォルト設定の読み込みより後に置くこと、デフォルト値の欄が実効値であることを述べる形に改めた | 実効値を載せる根拠が本文に無かった。`rest.rst:61` と同じ語彙・同じ語順で書き、2ページを並べて読んだときに差が意味を持たないようにした（`design.md` §8「表を持つページは、その基準を表の直前の地の文で明示する」） |
| `:86` の `important` | 「どちらか一方を必ず設定する」を「どちらか一方が設定されている必要がある」に改め、デフォルト設定を読み込んでいる場合はこの状態が生じないこと、注意が要るのはデフォルト設定を読み込まない場合であることを追記した | デフォルト設定を読み込む前提では `htmlCheckerConfig` が設定済みで「どちらも設定していない」状態が生じない。クラスの挙動としては正しいため削除せず、どういう場合に問題になるかが分かる形にした |
| `:102` の `tip` | 「`tempDirectory` を省略した場合」を「デフォルト設定を読み込まず、`tempDirectory` も指定しない場合」に改めた | デフォルト設定が `target/tmp` を入れるため、省略しただけでは Jetty のデフォルト動作にならない |
| 記述例 `:124` | `webBaseDir` の値を `../main/web` から `src/main/webapp` に改めた | 表と矛盾していた。`../main/web` はブランクプロジェクトに存在しないパスである（webapp は `src/main/webapp`）。**設定項目の増減はしていない。** `xmlComponentFile`・`tempDirectory`（`webTemp`）など、デフォルト値と異なる値を意図的に示している項目はそのまま残した |

`:104` の「デフォルト値と同じ値を明示的に記述している項目もある」は、`webBaseDir` の是正後も成立する
（`htmlDumpDir`・`userIdSessionKey`・`httpHeader`・`backup`・`htmlResourcesCharset`・`sessionInfo`・
`ignoreHtmlResourceDirectory`・`webBaseDir` がデフォルト値と同値）ため、文は変更していない。

**見出しの文言・並び順、設定項目表の行数・列構成・項目名・並び順はいずれも不変**（`checks/task-18.md`
ゲート4。見出しは行番号まで含めて同一、項目名の列は `md5sum` 一致）。「テストの実行速度を上げる」
「拡張例」の各セクションは `:216` の `tip` を除いて変更していない。

### `#19` 以降への申し送り

12. **設定項目表の「デフォルト値」は、デフォルト設定を読み込んだ実効値を書く。** クラスのフィールド
    初期値ではない（`design.md` §8）。**実装を確かめる範囲を `nablarch-testing` の `src/main/` に
    限定しない。** デフォルト設定は別モジュール `nablarch-testing-default-configuration` にあり、
    `nablarch/test/*.xml`（プロパティの割り当て）と `nablarch/test/*/*.config`（値）の**組**で実効値が
    決まる。`#15` はこの探索漏れにより表の9項目を誤った
13. **表を持つページは、基準を表の直前の地の文で明示する。** 文言は `rest.rst:61` および本ページ `:16` に
    揃える（「デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す」）
14. **表を直したら、表に連動する地の文を必ず洗う。** 本ページでは表の8項目の是正に対し、地の文3箇所と
    記述例1箇所の是正が連動して必要だった。表だけを直すと `important`・`tip`・記述例が表と矛盾する
