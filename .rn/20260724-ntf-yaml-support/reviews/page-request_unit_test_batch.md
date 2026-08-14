# `#27-14` リクエスト単体テスト（Nablarchバッチアプリケーション）

対象ファイル: `ja/development_tools/testing_framework/implementation/request_unit_test/batch.rst`（197行）
ページラベル: `request_unit_test_batch`（`mapping/style.md:377` の一覧と一致）

## 1. 参照リポジトリ

| リポジトリ | コミット | 確認した内容 |
|---|---|---|
| `nablarch-testing` | `e21bf67` | `BatchRequestTestSupport` の親クラス・パッケージ・`@Published`、`StandaloneTestSupportTemplate#execute` の2シグネチャ（`:56` `public final`／`:178` `protected final`）、`TestShot#setUp`（`:140-146`）と `#assertAll`（`:126-138`）の順序、`REQUIRED_COLUMNS`（`:385-387`）、`BatchRequestTestSupport#compareStatus`（`:111-117`）、`RequestTestingMessagingProvider#assertSendingMessage`（`:230-257`）、`AsyncMessageSendActionForUt`（全38行）、`MainForRequestTesting`（`:13-32`） |

`nablarch-fw-messaging` は作業ディレクトリ（`/home/tie303177/work/nablarch/`）に存在しないため、`AsyncMessageSendAction` が起動パラメータ `messageRequestId` を要求する点は一次実装で確認していない。`nablarch-testing` の `src/test/java/nablarch/test/core/messaging/AsyncMessageSendActionForUtTest.java:30`（`-messageRequestId` を渡すテスト）と、旧版サンプル `/home/tie303177/work/nablarch/old-versions/_survey/out/1.2.8/Nablarch_sample/test/java/nablarch/sample/ss11AC/RM11AC0301RequestTest/testSendMessage.yaml:13,24` を根拠にした。本ページでは `AsyncMessageSendAction` を ``literal`` 表記としているため、リンク切れは生じない。

## 2. 出典行の消化

### 2-1. マッピング行

`mapping.csv` を `dest_page` =「リクエスト単体テスト（Nablarchバッチアプリケーション）」で絞った結果は25行・384行分である（`csv.DictReader` で抽出）。

| mapping_id | src_file | 出典行 | 行数 | disposition | dest_section |
|---|---|---|---|---|---|
| input-0032 | `input/ntf-doc-terms.md` | 488-499 | 12 | MOVE | 使用方法 |
| current-0032 | `05_UnitTestGuide/02_RequestUnitTest/batch.rst` | 10-29 | 20 | MOVE | 使用方法 |
| current-0033 | 同 | 33-52 | 20 | MOVE | 使用方法 |
| current-0034 | 同 | 56-62 | 7 | MOVE | 使用方法 |
| current-0035 | 同 | 65-70 | 6 | **REFERENCE** | 使用方法 |
| current-0039 | 同 | 489-493 | 5 | MOVE | 使用方法 |
| current-0040 | 同 | 496-506 | 11 | MOVE | 使用方法 |
| current-0041 | 同 | 509-528 | 20 | MOVE | 使用方法 |
| current-0042 | 同 | 532-535 | 4 | MOVE | 使用方法 |
| current-0043 | 同 | 544-549 | 6 | MOVE | 使用方法 |
| current-0044 | 同 | 552-567 | 16 | MOVE | 使用方法 |
| current-0045 | 同 | 570-619 | 50 | MOVE | 使用方法 |
| current-0051 | `05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst` | 8-12 | 5 | MERGE | 機能概要 |
| current-0052 | 同 | 15-22 | 8 | MOVE | 機能概要 |
| current-0053 | 同 | 26-43 | 18 | MOVE | 使用方法 |
| current-0054 | 同 | 47-51 | 5 | MERGE | 使用方法 |
| current-0055 | 同 | 54-118 | 65 | MERGE | 使用方法 |
| current-0280 | `06_TestFWGuide/RequestUnitTest_batch.rst` | 10-15 | 6 | MOVE | 機能概要 |
| current-0281 | 同 | 18-23 | 6 | MOVE | 機能概要 |
| current-0282 | 同 | 26-54 | 29 | MOVE | 機能概要 |
| current-0283 | 同 | 61-63 | 3 | MOVE | 使用方法 |
| current-0284 | 同 | 66-90 | 25 | MOVE | 使用方法 |
| current-0285 | 同 | 93-110 | 18 | MOVE | 使用方法 |
| current-0286 | 同 | 113-120 | 8 | MOVE | 使用方法 |
| current-0287 | 同 | 123-133 | 11 | MOVE | 使用方法 |

反映先の対応:

- 機能概要（`batch.rst:15-65`）: current-0280（全体像の文）・current-0281（画像）・current-0282（主なクラスとリソースの `list-table`）・current-0287（`FileSupport` を独立クラスとする理由）・current-0051／0052（応答不要メッセージ送信の導入とテスト対象の成果物）
- テストクラスを作成する（`:72-108`）: current-0032（通常のバッチ）・current-0053（応答不要メッセージ送信）
- テストメソッドを作成する（`:110-135`）: current-0033（1テストショット1メソッドの原則と例外）・current-0040／0041（`execute` の2形式）
- テストデータを作成する（`:137-173`）: current-0034・current-0035（REFERENCE。節を起こさず `:139` の `:ref:` 導線のみ — G11）・current-0054／0055（応答不要メッセージ送信固有の記述）
- テストを実行する（`:175-183`）: current-0039・current-0042・current-0283／0284（`StandaloneTestSupportTemplate`・`TestShot` の実行順序）・current-0286（`MainForRequestTesting`）
- テスト結果を確認する（`:185-197`）: current-0043（データベース）・current-0044（ファイル）・current-0045（ログ）・current-0285（`BatchRequestTestSupport` の各種アサート）・input-0032

### 2-2. 未消化行

意図的に落とした行は次の3種類である。いずれも本ページで繰り返すと G12（二重掲載）に触れる。

- current-0044 の `EXPECTED_FIXED`／`EXPECTED_VARIABLE` のグループID記法（出典 `batch.rst:552-567`）→ `testdata_notation.rst:902` にある。`:194` の `:ref:` へ置換
- current-0045 の `logLevel`・`message1`… の AND 条件と、空の `LIST_MAP` がエラーになる仕様（出典 `batch.rst:570-619`）→ `testdata_notation.rst:553` にある。`:194` の `:ref:` へ置換
- current-0042 のコマンドライン引数 `args[n]` の記法 → `testdata_notation.rst:500-519` にある。`:148` の `:ref:` へ置換

## 3. 実装で確認した事実（出典の記述を実装で上書きしたもの）

| # | 出典の記述 | 実装 | 本ページの記述 |
|---|---|---|---|
| 1 | `RequestUnitTest_batch.rst:118`「常駐化機能を無効化する」 | `MainForRequestTesting.java:13-32` はシステムリポジトリの再初期化と復帰しか行わない（`reInitializeRepository`／`revertDefaultRepository`）。常駐化を無効化するコードは無い | `:183` は再初期化と復帰だけを書き、常駐バッチは第2部の設定ページへ導線を張った |
| 2 | `batch.rst:490-491`「以下の手順でリクエスト単体テストを実行する」の後に手順が無い（出典の欠落） | `TestShot.java:70-89` の `executeTestShot` は `setUp()` → `createMain()`＋`invokeTarget` → `assertAll()` | `:179-181` に3手順として補った。準備の内訳は `TestShot.java:140-146` の4項目（DB・入力ファイル・期待するログ・要求電文の期待値） |
| 3 | `batch.rst:523-526` は `testRegister()` を宣言しながら「`execute("testRegisterUser")` と等価」とコメントしている（出典の誤り） | `StandaloneTestSupportTemplate.java:178-185` の引数なし `execute()` はメソッド名の読み込み単位を読む | `:132-135` でコード行とコメントの対応を正した |
| 4 | 出典に記述なし | `BatchRequestTestSupport.java:111-117` の `compareStatus` は無条件に比較し、`TestShot.java:385-387` の `REQUIRED_COLUMNS` に `expectedStatusCode` が含まれる | `:187` でステータスコードの確認だけを空欄スキップの対象外として分けた |
| 5 | 出典に記述なし | `TestShot.java:134`＋`RequestTestingMessagingProvider.java:230-236` により、`expectedMessage` が未指定だと要求電文のアサートが行われない | `:148` に `expectedMessage` の指定を、`:193` に要求電文の確認を加えた |
| 6 | 出典に記述なし | `AsyncMessageSendActionForUt.java:26-32` は `errorCase` をコマンドライン引数から読む。差し替えなければ `errorCase` は無視される | `:154` の `.. important::` に「切り替えないまま `errorCase` を記述しても、正常系として実行される」を加えた |

## 4. 実測値

### 下線幅

| 行 | 記号 | 下線長 | 表示幅 | 見出し |
|---|---|---|---|---|
| 4 | `=` | 54 | 54 | リクエスト単体テスト（Nablarchバッチアプリケーション） |
| 13 | `-` | 50 | 8 | 機能概要 |
| 68 | `-` | 50 | 8 | 使用方法 |
| 73 | `~` | 49 | 22 | テストクラスを作成する |
| 111 | `~` | 49 | 24 | テストメソッドを作成する |
| 138 | `~` | 49 | 22 | テストデータを作成する |
| 176 | `~` | 49 | 16 | テストを実行する |
| 186 | `~` | 49 | 20 | テスト結果を確認する |

### 参照ラベルの解決

`:ref:` は11件。飛び先の `.. _<label>:` の実在と、リンク文字列＝飛び先見出しの一致を全件確認した。

| ラベル | 飛び先 |
|---|---|
| `mom_system_messaging-async_message_send` | `libraries/system_messaging/mom_system_messaging.rst:133` |
| `request_unit_test_setting_batch` | `setup/request_unit_test/batch.rst:1`（2件） |
| `testdata_notation` | `implementation/testdata_notation.rst:1`（2件） |
| `testdata_notation-test_shots` | 同 `:350`（2件） |
| `testdata_notation-setupdb` | 同 `:668` |
| `testdata_notation-messaging_data` | 同 `:1148` |
| `testdata_notation-command_line` | 同 `:500`（本タスクで付与。D-3 参照） |
| `testdata_examples` | `implementation/testdata_examples.rst:1` |

### 画像

`git mv` 1件（`design.md:897,907` の規約どおり `<ページのディレクトリ>/images/<ページのベース名>/` へ移した）。

| 移動元 | 移動先 |
|---|---|
| `guide/development_guide/06_TestFWGuide/_images/batch_request_test_class.png` | `implementation/request_unit_test/images/batch/batch_request_test_class.png` |

## 5. 判断（decide）

### D-1. Excel形式の画像2枚を落とした

- 対象: `05_UnitTestGuide/02_RequestUnitTest/_image/delayed_send.png`（`messageRequestId` カラムを足したテストショット一覧）・`delayed_send_error.png`（`errorCase` カラム）
- 判断: 移さず落とした。両画像の情報量は「テストショット一覧にカラムを1つ足し、値を1つ書く」だけであり、`:148`・`:150` の地の文で完全に置き換わる。加えて両画像は Excel 形式のシートを写したものであり、Excel／YAML 共通の節に置くと `style.md:434-443`（S-10 規約3）に反する。`reviews/page-deal_unit_test_http_messaging.md` の decide-2 に、Excel 形式の記載例画像を落とした先例がある
- 元に戻す場合: `git show 2e501ad:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/_image/delayed_send.png` で取り出し、`implementation/request_unit_test/images/batch/` に置いて `:148`・`:150` の直後に `.. image::` を足す。ただし S-10 規約3 により、その場合は「Excel形式の場合」「YAML形式の場合」の L4 対に分ける必要がある

### D-2. Excel形式・YAML形式の記載例を本ページに置かなかった

- 設計観点のレビューから、`messageRequestId`・`errorCase` の記載例が解説書のどこにも無いという指摘があった（`testdata_examples.rst` に「応答不要」は0件。`mapping.csv` 上、`delayed_send.rst` 由来の行はすべて本ページか「取引単体テスト（MOMによるメッセージング）」行きで、記載例ページには振られていない）
- 判断: 置かなかった。第3部のリクエスト単体テスト5ページはいずれも記載例を持たず、`:ref:` で `testdata_notation` と `testdata_examples` に送る作りで統一されている（`implementation/request_unit_test/*.rst` に「Excel形式の場合」「YAML形式の場合」の見出しは0件）。本ページだけ例外にすると兄弟ページと不揃いになる。`deal_unit_test/batch.rst` が記載例を持つのは、複数処理を1つの読み込み単位に並べる書き方そのものがそのページの主題だからであり、事情が異なる
- 残る課題: 判断待ち #1 に挙げた

### D-3. `testdata_notation.rst` に `testdata_notation-command_line` ラベルを1行足した

- `:148` の「テストショット一覧に `messageRequestId` カラムを追加する」がなぜ成立するかは、`testdata_notation.rst:508`「テストショット一覧に上記以外のカラムを追加すると、そのカラムはコマンドラインオプションとみなされる」が根拠である（`AsyncMessageSendActionForUt.java:26-32` が `CommandLine#getParam("errorCase")` で読むことも確認済み）。この節にラベルが無かったため参照できなかった
- 判断: `testdata_notation.rst:500` の見出し直前にラベルを1行足した。既存本文には手を触れていない

### D-4. 「一時テーブル」を採った

- 出典 `delayed_send.rst:18` は「電文送信テーブル」と書くが、FW解説書 `mom_system_messaging.rst:151` は同じものを「一時テーブル」と呼ぶ。`glossary.md:43` の採用順位1「FW解説書に同じ概念の用語があれば、その表記を採用する」に従い、`:20`・`:25`・`:148` を「一時テーブル」に揃えた
- 同じ理由で、ステータスの呼称も FW（`mom_system_messaging.rst:171-172`）に合わせて「処理済み」「送信失敗」に統一した

### D-5. テスト対象の成果物を2項目のままにした

- FW解説書 `mom_system_messaging.rst:166-174` は成果物を4項目（一時テーブル・フォーマット定義ファイル・SQLファイル・ステータス更新用のフォームクラス）挙げるが、出典 `delayed_send.rst:15-22` は「テスト対象の成果物」として2項目（フォーマット定義ファイル・3種類のSQL文）しか挙げない
- 判断: 出典どおり2項目にした。FW側は「機能を作るために必要な成果物」、出典側は「リクエスト単体テストで確認する成果物」で、対象が異なる。出典に無い項目を足すと、テストで確認しないものを確認対象として書くことになる

### D-6. JUnit 5 拡張への導線を置かなかった

- `setup/junit5_extension.rst:40-42` に `BatchRequestTestExtension`／`@BatchRequestTest` があるが、本ページは JUnit 4 の継承方式のみを説明した。`web.rst`・`mom.rst` も同じ扱いである（`implementation/` 配下に `junit5_extension` への参照は0件）
- `#27-12` decide-5・`#27-13` decide-9 と同じ、第3部全体の方針に関わる論点のため、判断待ち #4 に送った

## 6. 4観点レビューの結果

QA・設計・クラフト・検証の4観点を別々のサブエージェントで実施した（`steering.md` の Rules、作業指示 §4 の4）。指摘は延べ33件（QA 7・設計 5・クラフト 10・検証 11）。観点をまたぐ重複を除くと28件で、反映16件・反映しなかったもの12件。反映しなかったもののうち9件は判断待ちへ送った。

反映した16件:

1. 「テストケース」5件を「テストショット」へ（`glossary.md:556`。ゲートは0件を求める）— クラフト
2. `.. tip::` → `.. important::`（`style.md:232-235`。差し替えなければ異常系が成立しないため必須の注意事項）— QA・クラフト
3. ステータスコードの確認を空欄スキップの対象外として分けた — QA・検証
4. 要求電文の確認（`expectedMessage`）を `:148` と `:193` に追加 — QA・検証
5. 実行手順の準備の内訳に「要求電文の期待値の登録」を追加 — QA
6. `:29` の「Action クラスが Nablarch の一部として提供されるため」という因果を落とした（出典に理由の記述が無い）— QA
7. 「電文送信テーブル」→「一時テーブル」— クラフト・検証（D-4）
8. 「送信済み」→「処理済み」— クラフト・検証
9. 「送信失敗（エラー）」「エラー」→「送信失敗」— クラフト
10. `:44` の「期待する結果」→「期待値」（`glossary.md:218`）— クラフト
11. `expectedStatusCode` の「必須」の説明を、`testdata_notation.rst:381` の「必須＝カラムを定義しておくこと」と矛盾しない書き方に改めた — クラフト
12. `// 中略` をクラス本体の中へ移した（`mom.rst:120-126` に合わせた）— 検証
13. `execute("testRegisterUser")` のコメントを、コード行と主語が一致する書き方に改めた — クラフト
14. 「（例：…）」を「（例えば、…）」へ（全角コロンの用例はNTF解説書内でここだけだった）— クラフト
15. 上書き設定に「本番用のコンポーネント設定ファイルを取り込んだうえで」を補った（旧版の実設定 `/home/tie303177/work/nablarch/old-versions/1.4.11/Nablarch-tutorial-workspace/workspace/tutorial/test/resources/send-messaging-test-component-configuration.xml:8` が `<import>` を持つ）— 検証
16. 異常系の `expectedStatusCode` に異常終了時の終了コードを書く旨を補った — 検証

反映しなかった12件（理由）:

- `.. important::` の本体（コンポーネント設定とクラス差し替え）を第2部へ移す（設計）→ `mapping.csv` の current-0055 は `dest_page` が本ページ・`dest_section` が「使用方法」である。`design.md:299` が第2部へ送ると定めるのは「拡張例」であり、この内容は異常系テストを行うための必須手順である。配置は `mapping.csv` に従った
- Excel形式・YAML形式の記載例を足す（設計）→ D-2
- 図の `handle(ExecutionContext, CommandLine)` の引数順が実装（`MainForRequestTesting.java:20`）と逆（検証）→ 画像の作り直しが必要。判断待ち #2
- 図の「Excelファイル(テストデータ)」がYAML形式に対応していない（検証）→ 同上。判断待ち #2
- 図の `FileSupport` の操作が「固定長ファイル」限定（検証）→ 同上。判断待ち #2
- 成果物にフォームクラスを足す（クラフト）→ D-5
- `StandaloneTestSupportTemplate`・`TestShot`・`DbAccessTestSupport`・`FileSupport` を `:java:extdoc:` にする（検証。4クラスとも `@Published`）→ `mom.rst:73-104` の一覧表が ``literal`` で統一されているため揃えた。判断待ち #5
- `:29` を `.. tip::` に入れる（クラフト。`mom.rst:27` は同趣旨を tip に入れている）→ `style.md:232-235` の tip の定義（読まなくても機能は正しく使える補足）に照らすと、地の文が適切と判断した
- `messagingProvider` の差し替え手順を第2部に足す（QA）→ 出典にも既存ページにも無く、新規追加になる。判断待ち #3
- JUnit 5 拡張の導線を足す（QA）→ D-6。判断待ち #4
- `mom.rst` から本ページへの導線を足す（設計）→ `#27-13` はコミット済み。判断待ち #6
- `\ ` エスケープの不統一を直す（クラフト）→ 規範そのものが無い。判断待ち #7

## 7. 判断待ち（decide）

1. **応答不要メッセージ送信のテストデータの記載例が解説書のどこにも無い。** `testdata_examples.rst` に応答不要メッセージ送信の例は0件で、`mapping.csv` 上も記載例ページに振られた行が無い。D-2 のとおり本ページには置かなかった。`testdata_examples.rst` に節を足すか、記載例なしで確定するか
2. **`batch_request_test_class.png` に3つの食い違いがある。** ①`handle` の引数順が実装と逆（`MainForRequestTesting.java:20` は `handle(CommandLine, ExecutionContext)`）②「Excelファイル(テストデータ)」と書かれており、YAML形式に対応していない ③`FileSupport` の操作が「固定長ファイル」限定だが、実装は可変長も扱う（`DataType.java:37-40`）。図の作り直しが要る
3. **応答不要メッセージ送信のテストに必要な `messagingProvider` の差し替えが、第2部にも第3部にも無い。** `nablarch-testing` のテスト用設定 `src/test/resources/batch-test-component-configuration.xml:61-63` は `RequestTestingMessagingProvider` を登録しており、これが無いと要求電文のアサートが成立しない（`RequestTestingMessagingProvider.java:94-98`）。`setup/request_unit_test/batch.rst`（全119行）・`setup/request_unit_test/mom.rst`（全60行）のいずれにも記述が無い。出典（`RequestUnitTest_batch.rst:10-133`・`delayed_send.rst:8-118`）にも無いため、旧解説書からの欠落ではなく新規追加になる
4. **JUnit 5 拡張の導線。** D-6。第3部全体の方針として決める必要がある（`#27-12` decide-5・`#27-13` decide-9 と同一の論点）
5. **主なクラスとリソースの表を ``literal`` のままにするか、`:java:extdoc:` にするか。** 第3部の全ページに関わる。`#27-13` までは ``literal`` で統一している
6. **`mom.rst` から本ページへの導線が無い。** `mom.rst:10` は同期応答メッセージ受信・応答不要メッセージ受信・同期応答メッセージ送信の3つだけを挙げ、応答不要メッセージ**送信**に触れていない。`mom.rst:150`・`:173` は逆方向の導線を持つ。`#27-13` は `0674df7` でコミット済みのため、本タスクでは手を触れていない
7. **英数字と日本語の間の `\ ` エスケープに規範が無い。** `style.md:13-14` が「機械判定できない規則性は対象外」として明記を避けており、承認済みページ間で割れている（`testdata_notation.rst` 110件・`about/index.rst` 40件・`setup/common.rst` 7件・`mom.rst` 0件、本ページ11件）。`\ ` は出力に何も残さないためレンダリング結果は同一である。現状を許容するか、`style.md` に規則を足して一括で揃えるか
