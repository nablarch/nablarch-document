# `#27-12` リクエスト単体テスト（RESTfulウェブサービス）

対象ファイル: `ja/development_tools/testing_framework/implementation/request_unit_test/rest.rst`
ページラベル: `request_unit_test_rest`（`mapping/style.md:375` の一覧と一致）

## 1. 参照リポジトリ

| リポジトリ | コミット | 確認した内容 |
|---|---|---|
| `nablarch-testing-rest` | `9ada31e` | `RestTestSupport` / `SimpleRestTestSupport` の継承関係、委譲メソッド、リクエスト生成・送信・アサートの各シグネチャ、内蔵サーバの起動位置、テストデータ不在時の挙動、`readTextResource` の解決方法 |
| `nablarch-testing` | `e21bf67` | `DbAccessTestSupport` が持つ「委譲していない6メソッド」の実在 |

## 2. 出典行の消化

### 2-1. マッピング行

`mapping.csv` を `dest_page` = 「リクエスト単体テスト（RESTfulウェブサービス）」で絞った結果は12行・262行分である（`csv.DictReader` で抽出）。

| mapping_id | src_file | 出典行 | 行数 | disposition | 本ページでの反映先 |
|---|---|---|---|---|---|
| current-0307 | `06_TestFWGuide/RequestUnitTest_rest.rst` | 10-14 | 5 | MOVE | `rest.rst:15` |
| current-0308 | 同 | 17-19 | 3 | MOVE | `rest.rst:17`（画像） |
| current-0309 | 同 | 22-46 | 25 | MOVE | `rest.rst:19-45`（`list-table`） |
| current-0313 | 同 | 102-111 | 10 | MOVE | `rest.rst:54-61` |
| current-0314 | 同 | 114-118 | 5 | MOVE | `rest.rst:56` |
| current-0315 | 同 | 121-145 | 25 | MOVE | `rest.rst:95-106` |
| current-0316 | 同 | 148-195 | 48 | MOVE | `rest.rst:110-138` |
| current-0317 | 同 | 198-207 | 10 | MOVE | `rest.rst:161-165` |
| current-0318 | 同 | 210-274 | 65 | MOVE | `rest.rst:169-215` |
| current-0114 | `05_UnitTestGuide/02_RequestUnitTest/rest.rst` | 14-52 | 39 | MOVE | `rest.rst:50`・`rest.rst:63-93` |
| current-0120 | 同 | 83-106 | 24 | MOVE | `rest.rst:142-157` |
| current-0121 | 同 | 109-111 | 3 | **REFERENCE** | `rest.rst:144`（`:ref:` の導線のみ。節を起こしていない — G11） |

### 2-2. 行単位の対応

出典 `06_TestFWGuide/RequestUnitTest_rest.rst`（`git show 2e501ad:` で取得）。

| 出典行 | 内容 | 反映先 |
|---|---|---|
| 11-13 | 内蔵サーバを使用する旨、モジュール追加が必要な旨、ウェブアプリ版とモジュール一覧への参照 | `rest.rst:15` |
| 18 | `.. image:: _images/rest_request_unit_test_structure.png` | `rest.rst:17` |
| 23-43 | 主なクラス・リソースの6行表（グリッドテーブル） | `rest.rst:21-45`（`list-table` に変換 — S-07） |
| 103-105 | `SimpleRestTestSupport` の位置づけ、`RestTestSupport` との機能差 | `rest.rst:54-57` |
| 107-110 | `dbInfo` / `testDataParser` の準備要否の tip | `rest.rst:59-61` |
| 115-116 | `RestTestSupport` が `SimpleRestTestSupport` を継承しデータベース関連機能を持つ | `rest.rst:56` |
| 122-123 | `DbAccessTestSupport` への委譲、詳細ページへの参照 | `rest.rst:95` |
| 125-134 | 委譲していない6メソッドの前置きと列挙 | `rest.rst:95`・`rest.rst:97-102` |
| 136-141 | 委譲の理由とAPI経由の検証を推奨する注記 | `rest.rst:104-106`（`important` → `tip`。D-5） |
| 149-152 | `RestMockHttpRequest` を作る5メソッドの前置き | `rest.rst:110` |
| 154-160 | `get`/`post`/`put`/`patch`/`delete` のコード例 | `rest.rst:112-118` |
| 163-170 | 引数の説明とインスタンスへのデータ設定 | `rest.rst:120` |
| 172-178 | `newRequest` の説明とコード例 | `rest.rst:122-126` |
| 180-192 | 流れるようなインタフェースの tip とリクエスト構築例 | `rest.rst:128-138` |
| 199-204 | `sendRequest` の説明とコード例 | `rest.rst:161-165`（起動時期の記述を実装に合わせて改めた。D-9） |
| 212-232 | ステータスコードの確認（`assertStatusCode`、引数、失敗条件） | `rest.rst:171-185` |
| 235-241 | レスポンスボディの検証は外部ライブラリを使う旨 | `rest.rst:189` |
| 243-249 | ブランクプロジェクトの tip | `rest.rst:191-193` |
| 252-263 | 補助機能 `readTextResource` の説明とコード例 | `rest.rst:195-201` |
| 265-271 | ファイル配置の対応表（グリッドテーブル） | `rest.rst:203-215`（`list-table` に変換 — S-07。パスに `src/` を補った。D-10） |

出典 `05_UnitTestGuide/02_RequestUnitTest/rest.rst`。

| 出典行 | 内容 | 反映先 |
|---|---|---|
| 15-19 | テストクラスの書き方の5ステップ（各項目は他節への `:ref:`） | `rest.rst:50`（本ページのL3構成そのものが受け皿になるため、地の文の流れ説明に変換。D-3） |
| 21-49 | `SampleTest` の実装例 | `rest.rst:65-93`（コード本体は逐語） |
| 84-88 | 自動的に読み込まれるデータの限定 | `rest.rst:142-145` |
| 90-93 | テストデータ不在でもエラーにならない旨（`important`） | `rest.rst:155-157`（`tip` に変更。D-6） |
| 95-105 | 上記以外のデータを書いた場合の取得処理と3メソッド | `rest.rst:147-153`（`important` → 地の文。D-7） |
| 110 | `:ref:`request_test_setup_db` 参照。` | `rest.rst:144` の括弧内 `:ref:`（REFERENCE行、G11） |

**未消化の行: 0行。**

## 3. 実装で確認した事実

| 記述 | 実装での確認 |
|---|---|
| `RestTestSupport` は `SimpleRestTestSupport` を継承する | `nablarch-testing-rest@9ada31e` `src/main/java/nablarch/test/core/http/RestTestSupport.java:26` |
| `RestTestSupport` は `DbAccessTestSupport` に委譲する | 同 `:43`（`private final DbAccessTestSupport dbSupport;`）、`:58`・`:66`（生成）、`:106`〜`:199`（委譲メソッド群） |
| 委譲していない6メソッドが `DbAccessTestSupport` に実在する | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/db/DbAccessTestSupport.java:96`・`:132`・`:147`・`:213`・`:226`・`:241` |
| 自動的に読み込まれるのは `setUpDb` とテストメソッド名の2つだけである | `RestTestSupport.java:79-82`（`setUpDb()` が `setUpDbIfSheetExists(SETUP_TABLE_SHEET)` と `setUpDbIfSheetExists(testDescription.getMethodName())` だけを呼ぶ）、`:39`（`SETUP_TABLE_SHEET = "setUpDb"`） |
| テストデータが無い場合はエラーにならず投入がスキップされる | 同 `:88-95`（`isExisting` が偽なら `logDebug` を出して何もしない） |
| `get`/`post`/`put`/`patch`/`delete`/`newRequest`/`sendRequest`/`assertStatusCode` は `SimpleRestTestSupport` にある | `SimpleRestTestSupport.java:126`・`:136`・`:146`・`:156`・`:166`・`:176`・`:186`・`:312` |
| `readTextResource(String)` は `SimpleRestTestSupport` にある | 同 `:333` |
| `getListMap`/`getListParamMap`/`getParamMap` は `RestTestSupport` の委譲メソッドである | `RestTestSupport.java:129`・`:141`・`:153` |
| **内蔵サーバを起動するのは `@Before` の `setUp()` であり、`sendRequest` ではない** | `SimpleRestTestSupport.java:84-89`（`@Before public void setUp()` が `initializeIfNotYet(config)` を呼ぶ）→ `:237-243`（未初期化のときだけ `createHttpServer`）→ `:266`（`server.startLocal()`）。`sendRequest` は `:186` → `:197` → `:224-230` で `server.handle(request, context)` を呼ぶだけである |
| **`readTextResource` はクラスパスからリソースを解決する** | 同 `:343-347`（`getUrl(testClass, testClass.getSimpleName() + "/" + fileName)`。`Class#getResource` 経由） |

## 4. 実測値

- 本文215行。
- 見出し下線: L1 = 50（タイトル表示幅45）、L2 = 50、L3 / L4 = 49。すべて `style.md` S-04 と `#25` 以降の実測基準に一致（`unicodedata.east_asian_width` で W/F/A を2として算出）。
- `verify_mapping.py`: `OK: no errors`（exit 0）。
- Docker フルビルド（`sphinx-build -E`）: `build succeeded, 1 warning.`。warning は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` の1件のみで、新規warningは0件。
- 用語走査: G6 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。拡張走査（`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`インターフェイス`・`既定`・`デフォルト設定`・です/ます）0件。`glossary.md` §8 の揺れ表記（`想定結果`・`想定値`・`事前準備データ`・`セットアップデータ`・`テストケース`・`自動テストフレームワーク`・`オーバライド`・`HTML ダンプ`）0件。
- 画像: `git mv` で `guide/development_guide/06_TestFWGuide/_images/` から `implementation/request_unit_test/images/rest/` へ `rest_request_unit_test_structure.png` と `rest_request_unit_test_structure.xlsx` を移動（`design.md:897`・`:907`）。移動元に残骸なし。

### 参照ラベルの解決

| 出典の参照 | 本ページでの参照先 | 確認 |
|---|---|---|
| `:ref:`リクエスト単体テスト(ウェブアプリケーション) <request-util-test-online>`` | `request_unit_test_web` | `implementation/request_unit_test/web.rst:1`（見出し `:3`） |
| `:ref:`モジュール一覧 <rest_test_modules>`` | `request_unit_test_setting_rest` | `setup/request_unit_test/rest.rst:1`（見出し `:3`） |
| `:doc:`02_DbAccessTest`` | `component_unit_test` | `implementation/class_unit_test/component.rst:1`（`mapping.csv` 上、`02_DbAccessTest.rst` の行き先は「コンポーネント単体テスト」） |
| `:ref:`how_to_write_excel`` | `testdata_notation` | `implementation/testdata_notation.rst:1`（見出し `:3`） |
| `:ref:`how_to_get_data_from_excel`` | `testdata_notation-list_map` | `implementation/testdata_notation.rst:580`（見出し `:582`） |
| `:ref:`request_test_setup_db`` | `testdata_notation-setupdb` | `implementation/testdata_notation.rst:668`（見出し `:670`） |
| （出典に対応なし。D-8 で追加） | `testdata_notation-file_structure` | `implementation/testdata_notation.rst:22`（見出し `:24` 「テストクラスとテストデータの対応」） |
| `:java:extdoc:`Javadoc <nablarch.fw.web.RestMockHttpRequest>`` | 変更なし | `nablarch-testing-rest@9ada31e` `src/main/java/nablarch/fw/web/RestMockHttpRequest.java:17-18`（`@Published`） |
| `:doc:`RESTfulウェブサービスのブランクプロジェクト <...setup_WebService>`` | 相対パスを `../../../../` に調整 | 同階層の `setup/request_unit_test/rest.rst:57` と同じ深さ |

リンクテキストはすべて参照先の見出しと一致する（G9）。

## 5. 出典から変えた点

| ID | 変更 | 理由と根拠 |
|---|---|---|
| D-1 | 主なクラス・リソースの表とファイル配置の表を、グリッドテーブルから `list-table` に変換した（出典 `06:23-43`・`06:265-271` → `rest.rst:21-45`・`:203-215`） | S-07（`style.md`）がグリッドテーブルを禁止している |
| D-2 | 「テストデータ（Excelファイル）」から「（Excelファイル）」を落とし、「Excelファイルが存在しない場合」などの記述を形式中立に改めた | S-10。形式に依らない挙動の説明であり、形式ごとの記述方法は `testdata_notation.rst:42`（Excel形式）・`:81`（YAML形式）に集約されている |
| D-3 | 出典 `05:15-19` の5項目の `:ref:` チェックリストを、地の文の流れ説明（`rest.rst:50`）に変換した | 参照先の各節が本ページ自身のL3になったため、リンクの受け皿が消えた |
| D-4 | `current-0121`（REFERENCE）を節にせず、箇条書き内の `:ref:` に落とした（`rest.rst:144`） | G11 |
| D-5 | 出典 `06:136-141` の `.. important::` を `.. tip::` にした（`rest.rst:104-106`） | S-06（`style.md:232-235`）。API経由の検証を薦める内容で、守らなくても機能は正しく使える |
| D-6 | 出典 `05:90-93` の `.. important::` を `.. tip::` にした（`rest.rst:155-157`） | 同上。守るべき行動を含まない挙動差の説明である |
| D-7 | 出典 `05:95-105` の `.. important::` を地の文にした（`rest.rst:147-153`） | 注意喚起ではなく手順の説明であるため |
| D-8 | 「テストメソッドごとの準備データ」に、読み込み単位の名前をテストメソッド名と同じにする旨と `:ref:`テストクラスとテストデータの対応 <testdata_notation-file_structure>`` を追加した（`rest.rst:145`） | 出典は自動読み込みの対象を挙げるだけで命名規則に触れておらず、読者が規則に到達できない。規則の記載先は `testdata_notation.rst:69` |
| D-9 | 「内蔵サーバが起動されリクエストが送信される」（出典 `06:199-200`）を、「内蔵サーバは、スーパクラスがテストメソッドの実行前に起動する。…起動済みの内蔵サーバにリクエストが送信される」に改めた（`rest.rst:161`） | 実装と一致しないため。起動は `@Before` の `setUp()` で行われる（§3 の実装確認欄を参照。`SimpleRestTestSupport.java:84-89`・`:237-243`・`:266`、`nablarch-testing-rest@9ada31e`） |
| D-10 | ファイル配置の表のパスに `src/` を補った（出典 `06:265-271` の `<PROJECT_ROOT>/test/java/...`・`<PROJECT_ROOT>/test/resources/...` → `rest.rst:211`・`:214`） | `readTextResource` はクラスパスから解決するため（`SimpleRestTestSupport.java:343-347`、`nablarch-testing-rest@9ada31e`）。Mavenの標準構成では `src/test/resources` がテストクラスパスに載る。承認済みの `setup/request_unit_test/rest.rst:44` も `src/test/resources/unit-test.xml` と書いている |
| D-11 | `rest.rst:15` の第2文を、モジュール追加だけでなくコンポーネント設定も設定ページに従う旨に改めた | 参照先 `setup/request_unit_test/rest.rst:44-53` が求めているのはモジュール追加・デフォルト設定の読み込み・`httpServerFactory` の登録の3つであり、出典の書き方ではモジュールだけと読める |
| D-12 | 「テストクラスの全体像」のコード例を、委譲メソッドの列挙より前に移した（`rest.rst:63-93`） | 出典 `05:14-49` はコード例を「テストクラスの書き方」の冒頭に置いており、その順序に戻した |
| D-13 | 用語を `glossary.md` の正表記に統一した。`スーパークラス` → `スーパクラス`（6箇所）、`インターフェイス` → `インタフェース`（1箇所）、`期待する結果` → `期待値`（1箇所）、`データベース初期値` → `準備データ`（2箇所） | `glossary.md:594`・`:595`（無条件置換）、`:218`（`期待値`）、`:217`（`準備データ`） |
| D-14 | 全角コロン直後の余分な半角スペースを削除した（`rest.rst:56`・`:57`） | エスケープ `\ ` に加えて実体の空白が入っており、出力に半角空きが残るため |
| D-15 | 語の重複・ねじれを整えた。`アサートを提供する` → `アサートなどの機能を提供する`（`:44`）、`返却する`/`返却された` → `返す`/`返された`（`:120`・`:183`）、`オブジェクト` → `インスタンス`（`:110`・`:122`）、`Enum` → `列挙型`（`:182`）、`上記の` → `これら`（`:122`・`:193`）、`利用者` → `アプリケーションプログラマ`（`:106`）、`記述` の4連と `ファイル` の3連の解消（`:147`・`:201`） | いずれも同一ページ内での不統一・冗長の解消。`上記の`・`利用` は G6 の拡張走査対象でもある |
| D-16 | 「テストメソッドを作成する」の冒頭に、節が何を扱うかを述べる1文を足した（`rest.rst:110`） | 見出しに対して中身がリクエスト生成に限られ、節単独で読めなかった |
| D-17 | 「テストデータの記述方法は」を「テストデータの格納場所と記述方法は」に改めた（`rest.rst:142`） | 参照先に格納場所も書かれている。承認済みの `implementation/deal_unit_test/batch.rst:19` と同じ書き方に揃えた |
| D-18 | テストデータ不在時の tip を節末（コード例の後）に移した（`rest.rst:155-157`） | 「この2つ以外のテストデータ」（`:147`）が指す箇条書きとの間に tip が割り込んでいたため |

## 6. 4観点レビューの結果

4観点（QA / 設計 / クラフト / 検証）をそれぞれ別のサブエージェントで実施した。指摘は計32件で、うち21件を本文に反映し（D-8〜D-18）、11件は判断待ちまたは不採用とした。

- **QA**: 8件。設定の前提がモジュール追加だけになっている（→ D-11）、`src/` 抜け（→ D-10）、テストメソッドごとの読み込み単位に導線がない（→ D-8）、格納場所に触れていない（→ D-17）、節の導入文がない（→ D-16）を反映。`dbInfo` / `testDataParser` の設定手順が解説書のどこにもない（→ decide-1）、`setBody` に触れていない（→ decide-4）、JUnit 5 の導線（→ decide-5）は判断待ち。
- **設計**: 4件。design.md:281-296 のアウトライン適合、G11・G12・G13、参照ラベルの張り先はすべて問題なしと確認された。節の導入文（→ D-16）、tip の位置（→ D-18）、コード例の位置（→ D-12）を反映。`dbInfo` / `testDataParser` の導線は decide-1。`important` → `tip` の3箇所（D-5〜D-7）と S-10 に基づく形式中立化（D-2）は、いずれも妥当と判定された。
- **クラフト**: 12件。用語集の正表記違反3種8箇所（→ D-13）、全角コロンの余分な空白（→ D-14）、係り受けのねじれと語の重複（→ D-15）を反映。S-02 / S-03 / S-04 / S-05 / S-07 / S-09 / S-11 と、`テストケース`・`自動テストフレームワーク` の0件要件は適合と確認された。`dbInfo` の tip を important にするかは decide-1 に含めた。
- **検証**: 3件。出典行の消化0件未消化、メソッドシグネチャ12本、参照ラベル6件、画像の実在を確認したうえで、`sendRequest` が内蔵サーバを起動するという出典の記述が実装と一致しない点を指摘（→ D-9）。構成図の内容と本文の食い違いは decide-2、参照先がスタブである点は decide-3。

指摘が重複した箇所（`dbInfo` / `testDataParser` の導線、節の導入文）は、両観点の根拠を実物で確認したうえで1つの対応にまとめた。

## 7. 判断待ち（decide）

- **decide-1: `dbInfo` / `testDataParser` の設定手順が解説書のどこにも書かれていない。** `rest.rst:61` の tip は「`RestTestSupport` を使用する場合は、`dbInfo` または `testDataParser` のコンポーネントを準備する必要がある」と述べている（出典 `06_TestFWGuide/RequestUnitTest_rest.rst:107-110` のまま）。しかし参照先の第2部 `setup/request_unit_test/rest.rst` は、モジュール3件・`rest-request-test.xml` の import・`httpServerFactory` の登録・`restTestConfiguration` の設定項目しか扱っておらず（同ファイル `:17-38`・`:44-49`・`:60` 以降）、この2つのコンポーネントに触れていない。`ja/development_tools/testing_framework/` 配下を `grep -rn "dbInfo"` した結果、ヒットは `rest.rst:61` の1件のみである。**本ページ側では出典どおりの記述を保った。第2部への追記が必要かどうかは判断をお願いする。** なお QA観点は「実装上この2つは対で必要であり『または』は誤解を招く」と指摘したが、その根拠はローカルの `~/.m2` から展開した jar であって固定コミットの一次情報ではないため、本ページでは採用していない（未確認）。クラフト観点はこの tip を `important` にすることを提案したが、「準備しないと例外が発生する」という前提が未確認のため、S-06 の important の条件を満たすと言い切れず、tip のままとした。
- **decide-2: 構成図の内容が本文と3点食い違う。** `rest.rst:17` の `rest_request_unit_test_structure.png` は、(a) テストデータのノードが「Excelファイル」と書かれている（本文 `:31` は形式中立の「テストデータ」）、(b) メソッド一覧が GET/POST/PUT/DELETE の4つで PATCH がない（本文 `:110` は5つ）、(c) `SimpleRestTestSupport` が描かれていない（本文 `:54-57` は2つのスーパクラスから選ぶ構成）。作図元の `.xlsx` は同ディレクトリに移してあるため改訂は可能だが、画像の作り直しは本タスクの範囲外とした。前例は `reviews/page-deal_unit_test_http_messaging.md:79-80`。**とくに (a) は本文と正面から食い違うため、改訂の要否を判断してほしい。**
- **decide-3: 参照先2ページがスタブである。** `rest.rst:95` の `:ref:`コンポーネント単体テスト <component_unit_test>`` の飛び先 `implementation/class_unit_test/component.rst` と、`rest.rst:15` の `:ref:`リクエスト単体テスト（ウェブアプリケーション） <request_unit_test_web>`` の飛び先 `implementation/request_unit_test/web.rst` は、いずれもラベルと見出しだけの4行である。ラベルは実在するのでビルドは通る。参照先の選択自体は `mapping.csv` の割り当てと一致しており正しい。`web.rst` は `#27-20` で、`component.rst` は別タスクで本文が入る。
- **decide-4: `setBody` に触れていない。** 本ページは `post` / `put` / `patch` を提示しながら、リクエストボディの設定方法を説明していない（tip の構築例は `setHeader` と `setCookie` のみ）。`RestMockHttpRequest#setBody` は実装に存在し（`nablarch-testing-rest@9ada31e` `src/main/java/nablarch/fw/web/RestMockHttpRequest.java`）、承認済みの `implementation/deal_unit_test/rest.rst:43` が実際に使用している。ただし出典（`06_TestFWGuide/RequestUnitTest_rest.rst:148-195`）にこの説明はなく、追記は出典にない事実の追加にあたるため見送った。**追記するかどうかを判断してほしい。**
- **decide-5: JUnit 5 の導線が本ページにない。** 本ページは継承前提で書かれ、コード例も JUnit 4 である。`setup/junit5_extension.rst:55-60` に `RestTestSupport` → `RestTestExtension` / `@RestTest` の対応表があるが、本ページからは張っていない。第1部 `about/index.rst:115` が全体を受けており、承認済みの `implementation/deal_unit_test/batch.rst` など第3部の他ページも個別には張っていない（`grep -rn "junit5_extension" implementation/` で0件）。第3部全体の方針であるため、本ページ単独では変更しない。
- **decide-6: 承認済みページのパス表記との不整合（申し送り）。** D-10 で `<PROJECT_ROOT>/src/test/...` に改めたが、承認済みの `implementation/testdata_notation.rst:63` は `<PROJECT_ROOT>/test/jp/co/tis/example/db/` と `src/` なしで書かれており、同じページ内の `:48`（`src/test/java/com/example/`）とも食い違っている。**両ページ揃えての修正が必要である。**
