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
| I-9 | `htmlResourcesCharset` はCSSファイルの読み書きに使う | `HttpRequestTestSupport.java:522`・`:525`（`rewriteResourceFile` 内の `InputStreamReader` / `OutputStreamWriter`）。同メソッドのjavadoc `:483` が「HTMLリソースディレクトリ内のCSSファイルを置換する」 |
| I-10 | `AbstractHttpRequestTestTemplate` は `TestCaseInfo` を型引数に取る | `AbstractHttpRequestTestTemplate.java:61-62`（`@Published public abstract class AbstractHttpRequestTestTemplate<INF extends TestCaseInfo> extends HttpRequestTestSupport`） |
| I-11 | `TestCaseInfo` が保持するのはテストショット1件分の情報 | `TestCaseInfo.java:33-39`（`no` / `case` / `description` の各カラム名）。いずれも `testShots` のカラムである |

`:java:extdoc:` で参照した6クラスの公開javadocはいずれも HTTP 200 を実測（`HttpTestConfiguration` / `AbstractHttpRequestTestTemplate` / `TestCaseInfo` / `HtmlChecker` / `Html4HtmlChecker` / `ApplicationException`）。

## 出典と実装が食い違った箇所（`design.md` §8 により実装を優先）

| # | 出典 | 実装 | 本文の記述 |
|---|---|---|---|
| C-1 | `jsTestResourceDir` は「javascriptの自動テスト実行時に使用するリソースの**コピー先**ディレクトリ名」（`:337`） | `FileUtils.copyDir(new File(config.getJsTestResourceDir()), destDir, filter, true)`（`HttpRequestTestSupport.java:436`）であり、**コピー元**である。コピー先は `destDir`（ダンプディレクトリ配下） | 「JavaScriptの自動テストで使用するリソースを配置したディレクトリ」 |
| C-2 | `htmlChecker` のデフォルト値は「`Html4HtmlChecker` クラスのインスタンス。クラスには `htmlCheckerConfig` で設定した設定ファイルが適用される」（`:345-348`） | フィールドの初期値は `null`（`HttpTestConfiguration.java:150`）。`Html4HtmlChecker` が入るのは `htmlCheckerConfig` を設定したときだけ（`:358-361`） | デフォルト値は「（なし）」とし、`htmlCheckerConfig` 側の説明に「この項目を設定すると `Html4HtmlChecker` が `htmlChecker` に設定される」と書いた |
| C-3 | `htmlCheckerConfig` のデフォルト値は `test/resources/httprequesttest/html-check-config.csv`（`:351`） | フィールドの初期値は `null`（`HttpTestConfiguration.java:96`）。この値を既定として与えるコンポーネント定義は `nablarch-testing` の `src/main/` に存在しない（`src/main/resources` 自体が無い） | デフォルト値は「（なし）」とした。当該パスは記述例（`:465-466`）に残っており、記述例としては保持されている |
| C-4 | `htmlResourcesExtensionList` のデフォルト値は `css、jpg、js`（`:335`） | `Arrays.asList("css", "js", "jpg")`（`HttpTestConfiguration.java:139`） | 実装の並び順に合わせて `css`・`js`・`jpg` とした（内容は同じ） |

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
本文では製品名2件を落とし、「処理性能が低いCPUを搭載したPCで効果がある。比較的新しいCPUを搭載したPCでは効果が小さいため、無理に設定する必要はない」とした。
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
