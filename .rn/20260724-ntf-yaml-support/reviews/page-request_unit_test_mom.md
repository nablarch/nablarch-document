# `#27-13` リクエスト単体テスト（MOMによるメッセージング）

対象ファイル: `ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst`（209行）
ページラベル: `request_unit_test_mom`（`mapping/style.md:378` の一覧と一致）

## 1. 参照リポジトリ

| リポジトリ | コミット | 確認した内容 |
|---|---|---|
| `nablarch-testing` | `e21bf67` | `MessagingRequestTestSupport` / `MessagingReceiveTestSupport` の継承関係とパッケージ、`StandaloneTestSupportTemplate#execute` の2シグネチャ、`TestShot#executeTestShot` の実行順序、`MainForRequestTesting` の差異、`RequestTestingMessagingProvider` の委譲先、`RequestTestingSendSyncSupport` のテストデータ解決パス、`SendSyncSupport` の利用元、`TestDataConverter` の実名、`BatchRequestTestSupport` の親クラスと `@Published` |

`nablarch-fw-messaging` は作業ディレクトリ（`/home/tie303177/work/nablarch/`）に存在しないため、`MessageSender` は実装で確認していない。FW解説書 `ja/application_framework/application_framework/libraries/system_messaging/mom_system_messaging.rst:361` と出典（`06_TestFWGuide/RequestUnitTest_send_sync.rst:113-121`）を根拠にした。本ページでは `:java:extdoc:` を使わず ``literal`` 表記としているため、リンク切れは生じない。

## 2. 出典行の消化

### 2-1. マッピング行

`mapping.csv` を `dest_page` = 「リクエスト単体テスト（MOMによるメッセージング）」で絞った結果は36行・461行分である（`csv.DictReader` で抽出）。

| mapping_id | src_file | 出典行 | 行数 | disposition | 本ページでの反映先 |
|---|---|---|---|---|---|
| input-0033 | `input/ntf-doc-terms.md` | 501-510 | 10 | MOVE | `mom.rst:60-105`（受信のクラス表） |
| input-0034 | 同 | 512-525 | 14 | MOVE | `mom.rst:60-105`（送信のクラス表） |
| current-0046 | `05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst` | 8-12 | 5 | MOVE | `mom.rst:20`・`:26-27` |
| current-0047 | 同 | 15-18 | 4 | MOVE | `mom.rst:22-24` |
| current-0048 | 同 | 22-38 | 17 | MOVE | `mom.rst:132-148` |
| current-0049 | 同 | 42-47 | 6 | **REFERENCE** | `mom.rst:177` の `:ref:` 導線のみ（節を起こしていない — G11） |
| current-0101 | `05_UnitTestGuide/02_RequestUnitTest/real.rst` | 10-29 | 20 | MOVE | `mom.rst:114-130` |
| current-0102 | 同 | 33-37 | 5 | MOVE | `mom.rst:157` |
| current-0103 | 同 | 41-47 | 7 | MOVE | `mom.rst:159-171` |
| current-0104 | 同 | 50-53 | 4 | **REFERENCE** | `mom.rst:177` の `:ref:` 導線のみ（G11） |
| current-0108 | 同 | 260-264 | 5 | MOVE | `mom.rst:159` |
| current-0109 | 同 | 267-277 | 11 | MOVE | `mom.rst:157` |
| current-0110 | 同 | 280-300 | 21 | MOVE | `mom.rst:161-171` |
| current-0111 | 同 | 304-307 | 4 | MOVE | `mom.rst:188` |
| current-0112 | 同 | 311-320 | 10 | MOVE | `mom.rst:196-202` |
| current-0124 | `05_UnitTestGuide/02_RequestUnitTest/send_sync.rst` | 10-61 | 52 | MERGE | `mom.rst:29`・`:34-38`・`:40-56` |
| current-0125 | 同 | 64-73 | 10 | MERGE | `mom.rst:110`・`:188` |
| current-0127 | 同 | 292-296 | 5 | MERGE | `mom.rst:206-209` |
| current-0294 | `06_TestFWGuide/RequestUnitTest_real.rst` | 8-14 | 7 | MOVE | `mom.rst:15` |
| current-0295 | 同 | 17-22 | 6 | MOVE | `mom.rst:17-18`（画像） |
| current-0296 | 同 | 25-62 | 38 | MOVE | `mom.rst:60-105`（`list-table`） |
| current-0297 | 同 | 69-71 | 3 | MOVE | `mom.rst:79-80` |
| current-0298 | 同 | 74-99 | 26 | MOVE | `mom.rst:79-80`・`:190` |
| current-0299 | 同 | 102-126 | 25 | MOVE | `mom.rst:177`（`fwHeaderDefinition` は導線に置換 — D-6） |
| current-0300 | 同 | 129-145 | 17 | MOVE | `mom.rst:82-83`・`:204` |
| current-0301 | 同 | 148-155 | 8 | MOVE | `mom.rst:88-89`・`:190`（常駐化は落とした — D-3） |
| current-0302 | 同 | 158-165 | 8 | MOVE | `mom.rst:94-95` |
| current-0321 | `06_TestFWGuide/RequestUnitTest_send_sync.rst` | 8-18 | 11 | MOVE | `mom.rst:29` |
| current-0322 | 同 | 21-36 | 16 | MOVE | `mom.rst:31-32`（画像）・`:152-153` |
| current-0323 | 同 | 39-67 | 29 | MOVE | `mom.rst:60-105`（`list-table`） |
| current-0324 | 同 | 74-81 | 8 | MOVE | `mom.rst:150-153` |
| current-0325 | 同 | 84-90 | 7 | MOVE | `mom.rst:173` |
| current-0326 | 同 | 93-110 | 18 | MOVE | `mom.rst:97-98`・`:192`・`:206` |
| current-0327 | 同 | 113-124 | 12 | MOVE | `mom.rst:100-101` |
| current-0329 | 同 | 143-146 | 4 | MOVE | `mom.rst:103-104` |
| current-0330 | 同 | 149-156 | 8 | **REFERENCE** | `mom.rst:183-184` の tip 内 `:ref:` 導線のみ（G11） |

### 2-2. 未消化行

**0行。** 意図して落とした行は §5 の D-3・D-6・D-8 の3件で、いずれも理由を記載している。

隣接する出典行が本ページに来ていないことも確認した（G12）。`send_sync.rst:77-288`（`current-0126`）・`real.rst:56-96`（`current-0105`）・`real.rst:211-253`（`current-0107`）・`delayed_receive.rst:50-56`（`current-0050`）は「テストデータの書き方」へ、`RequestUnitTest_send_sync.rst:127-140`（`current-0328`）は「リクエスト単体テストの設定（MOMによるメッセージング）」へ振られている。`csv.DictReader` で全行の `src_body_start`／`src_body_end` を並べ、本ページの36行と重なりが無いことを確認した。

## 3. 実装で確認した事実

すべて `nablarch-testing@e21bf67` で、ファイルを開いて確認した。

| 事実 | 出典 |
|---|---|
| `MessagingRequestTestSupport` のパッケージは `nablarch.test.core.messaging` | `src/main/java/nablarch/test/core/messaging/MessagingRequestTestSupport.java:1`・`:47-48`（`@Published`） |
| `MessagingReceiveTestSupport` は `MessagingRequestTestSupport` を継承し、`assertOutputData` は何もしない | 同 `MessagingReceiveTestSupport.java:12-13`・`:79-83` |
| `execute(String sheetName)` は `public final`、`execute()` は `protected final` でテストメソッド名を渡す | `standalone/StandaloneTestSupportTemplate.java:56`・`:178-186` |
| テストショットは 準備 → メインクラス起動 → 結果確認 の順で進む | `standalone/TestShot.java:70-89`（`setUp()` → `around.createMain()` + `invokeTarget` → `assertAll()`） |
| DB・ログの確認は期待値が空の場合スキップされる | 同 `:171-174`・`:198-202` |
| 構造化データ以外のフレームワーク制御ヘッダを使う場合、`expectedStatusCode` とステータスコードを照合する | `messaging/MessagingRequestTestSupport.java:195-210` |
| `MainForRequestTesting` はテスト用リポジトリの初期化と復元を行う。常駐化に関する処理は持たない | `standalone/MainForRequestTesting.java:20-32`。`@Published` は無い |
| `RequestTestingMessagingProvider` は内部クラス `RequestTestingMessagingContext` に委譲する。キューへアクセスしない | `messaging/RequestTestingMessagingProvider.java:31-40`・`:46-48`・`:60` |
| **同期応答メッセージ送信のテストデータは、テストクラス自身の読み込み単位から読まれる** | `messaging/RequestTestingSendSyncSupport.java:110-111`（`support.getResourceName(sheetName)` → `support.getPathOf(...)`）、`TestSupport.java:390`（`getBookName() + "/" + sheetName`）、`TestShot.java:188-190`（テストショットの `sheetName` を渡す） |
| **`sendSyncTestData` を使うのは取引単体テストのモックだけ** | `messaging/SendSyncSupport.java:49`・`:346-348`。利用元は `MockMessagingContext.java:52`・`:93` と `MockMessagingClient.java:54` の3箇所のみ（`git grep` で全件確認） |
| `TestDataConverter` が実名（出典の `TestDataConvertor` は誤り） | `src/main/java/nablarch/test/core/file/TestDataConverter.java` |
| `BatchRequestTestSupport` は `StandaloneTestSupportTemplate` を継承し `@Published` | `core/batch/BatchRequestTestSupport.java:25-26` |
| 常駐バッチでは `RequestThreadLoopHandler` の代わりに `OneShotLoopHandler` を使う | `src/main/java/nablarch/test/OneShotLoopHandler.java:16` |

## 4. 実測値

### 下線幅

`unicodedata.east_asian_width`（W/F/A = 2）で測定。L1 `:4` 50（表示幅47）・L2 `:13` `:108` 50×2・L3 `:113` `:156` `:176` `:187` `:195` 49×5。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L4 は使用していない。

### 参照ラベルの解決

`:ref:` 10件・`:java:extdoc:` 5件。すべて飛び先を開いて見出しと照合した。

| 参照 | 飛び先 | 見出し |
|---|---|---|
| `mom_messaging-action` | `ja/application_framework/application_framework/messaging/mom/architecture.rst:382` | `:384` 「MOMメッセージングで使用するアクション」 |
| `request_unit_test_setting_mom` | `setup/request_unit_test/mom.rst:1` | `:3` 「リクエスト単体テストの設定（MOMによるメッセージング）」 |
| `request_unit_test_web` | `implementation/request_unit_test/web.rst:1` | `:3` 「リクエスト単体テスト（ウェブアプリケーション）」（**4行のスタブ** — decide-3） |
| `request_unit_test_batch` | `implementation/request_unit_test/batch.rst:1` | `:3` 「リクエスト単体テスト（Nablarchバッチアプリケーション）」（**4行のスタブ** — decide-3） |
| `testdata_notation` | `implementation/testdata_notation.rst:1` | `:3` 「テストデータの書き方」 |
| `testdata_notation-messaging_data` | 同 `:1148` | `:1150` 「メッセージングのデータを記述する」 |
| `testdata_notation-test_shots` | 同 `:350` | `:352` 「テストショット一覧（testShots）を記述する」 |
| `testdata_notation-setupdb` | 同 `:668` | `:670` 「共通の準備データをまとめる」 |
| `testdata_notation-file_data` | 同 `:844` | `:846` 「ファイルのデータを記述する」 |

`:java:extdoc:` の5クラスは `e21bf67` でいずれも `@Published` を確認した（`MessagingRequestTestSupport:47`／`MessagingReceiveTestSupport:12`／`StandaloneTestSupportTemplate:20`／`AbstractHttpRequestTestTemplate:61`／`BatchRequestTestSupport:25`）。`@Published` が無い `MainForRequestTesting`（`:13` に無し）・`RequestTestingMessagingProvider`（`:39-40` に無し）は ``literal`` 表記にしてある。

### 画像

4点を `git mv` で移動した（`design.md:897`・`:907`。移動元に作図元の `.xlsx` は無い）。

| 移動元（`2e501ad` 時点のパス） | 移動先 |
|---|---|
| `06_TestFWGuide/_images/real_request_test_class.png` | `implementation/request_unit_test/images/mom/real_request_test_class.png` |
| `06_TestFWGuide/_images/send_sync.png` | 同 `images/mom/send_sync.png` |
| `05_UnitTestGuide/02_RequestUnitTest/_image/send_sync_base.png` | 同 `images/mom/send_sync_base.png` |
| `05_UnitTestGuide/02_RequestUnitTest/_image/hanrei.png` | 同 `images/mom/hanrei.png` |

`05_UnitTestGuide/02_RequestUnitTest/_image/` に残る同名の `send_sync.png` は別ページの図であり、移動していない。

## 5. 出典から変えた点

- **D-1: `real.rst:15` の `nablarch.test.core.http.MessagingRequestTestSupport` を `nablarch.test.core.messaging.MessagingRequestTestSupport` に直した。** 出典が誤っている。実装は `MessagingRequestTestSupport.java:1`。同じ出典群でも `delayed_receive.rst:27` は `nablarch.test.core.messaging` と正しく書いており、出典内でも割れていた。
- **D-2: 両FW解説書の class 表にある `TestDataConvertor` を `TestDataConverter` に直した。** 実装の実名は `nablarch.test.core.file.TestDataConverter`。承認済みの `setup/request_unit_test/mom.rst:35` も正しい綴りを使っている。
- **D-3: `RequestUnitTest_real.rst:153` の「常駐化機能を無効化する」を落とした。** `e21bf67` の `MainForRequestTesting` に該当コードが無い。常駐化の無効化は `nablarch.test.OneShotLoopHandler`（`:16`）へのハンドラ差し替えで行われており、`#27-14`（Nablarchバッチアプリケーション）の領域である。**`#27-14` への申し送り** とした。
- **D-4: `RequestUnitTest_send_sync.rst:49-53` が要求電文のアサートを `MockMessagingContext` に帰していたのを `RequestTestingMessagingProvider`（内部クラス `RequestTestingMessagingContext`）に直した。** `e21bf67` の `MockMessagingContext.java:14-24` は取引単体テスト向けと明記され、`TestShot.java:165-167` はリクエスト単体テストで `RequestTestingMessagingContext` を呼んでいる。
- **D-5: `send_sync.rst:19` の用語の断り書き（要求電文／応答電文）を、送信の説明の冒頭（`mom.rst:29`）に置いた。** 本ページは受信側と送信側を1ページで扱うため、向きの定義がないと読者が混乱する。「要求電文」「応答電文」自体は用語集の正表記（`glossary.md:273`・`:274`）である。
- **D-6: `RequestUnitTest_real.rst:120-125` の tip（`fwHeaderDefinition` の名前と `getFwHeaderDefinitionName()` のオーバーライド）を落とし、`:ref:` の導線に置き換えた。** 同内容は承認済みの `testdata_notation.rst:1154` に既載であり、再掲すると二重公開になる（G12）。
- **D-7: 出典がExcel専用に書いている箇所を形式中立にした（S-10）。** 「Excelファイル」「テストシート」を「テストデータ」「読み込み単位」に置き換え、`real.rst:318` の「（空欄であれば）」を落とした。YAML形式にセルの空欄という概念がない。
- **D-8: `delayed_receive.rst:54`・`:56`（応答電文＝`expectedMessages` が不要である旨）を本ページに書かなかった。** 当該行は `current-0050` として「テストデータの書き方」に振られている。同等の事実は `current-0300` の準備処理のみの表を根拠に `mom.rst:204` で述べている。
- **D-9: `mom.rst:181` で、同期応答メッセージ送信のテストデータの格納場所を「テストクラスに対応する読み込み単位」に直した。** 初版は `sendSyncTestData` 配下と書いていたが、これはリクエスト単体テストでは誤りである（§3 の実装確認を参照）。出典 `send_sync.rst:78-79` も「テストソースコードと同じディレクトリに同じ名前で格納する」としている。**承認済みの `testdata_notation.rst:1154` が同じ誤りを含んでおり、本ページの飛び先でもある**（decide-2）。
- **D-10: 図 `send_sync.png` のクラス名の誤りについて tip を足した（`mom.rst:34-35`）。** 図には `StandaloneSupportTemplate`（`Test` 抜け）と `BatchRequestTestSupportTemplate` が描かれているが、`e21bf67` の `nablarch/test/core/standalone/` は `MainForRequestTesting`・`StandaloneTestSupportTemplate`・`TestShot`・`package-info` の4ファイルのみで、後者に相当するクラスは `/home/tie303177/work/nablarch/` 全体に存在しない（`git grep` で0件）。画像自体は `2e501ad` の `06_TestFWGuide/_images/send_sync.png` とバイト同一の引き継ぎであり、作図元が無いため作り直せない。
- **D-11: 用語集の無条件置換を適用した。** 「メッセージ同期送信処理」→「同期応答メッセージ送信」2箇所（`glossary.md:528`）、「バッチ処理」→「Nablarchバッチアプリケーション」1箇所（`glossary.md:520`、処理方式を指す用法のため）、「主なクラス・リソース」→「主なクラスとリソース」1箇所（`glossary.md:308`）。
- **D-12: `MessageSender` の役割欄を「同期応答メッセージ送信を行う際に使用するコンポーネント」から具体化した。** 同語反復であったうえ、「コンポーネント」はシステムリポジトリの登録単位と紛れる（`glossary.md:170`）。出典 `RequestUnitTest_send_sync.rst:113-121` と図 `send_sync.png` の記載（`要求電文を生成する()`・`応答電文をパースする()`）を根拠に書き換えた。

## 6. 4観点レビューの結果

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘45件、本文への是正26件、不採用・判断待ち19件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。

最も重いのは3件。

1. **同期応答メッセージ送信のテストデータの格納場所が実装と逆だった**（QA）。初版は `sendSyncTestData` 配下と書き、`setup/common.rst` の該当節へ導線を張っていた。指摘を受けて自分で `e21bf67` を開き直し、`RequestTestingSendSyncSupport.java:110-111` がテストクラスの `sheetName` から解決していること、`SEND_SYNC_TEST_DATA_BASE_PATH` の利用元が取引単体テストのモック3箇所に限られることを確認した。**書き直したうえで、誤った導線を外した**（D-9）。
2. **テストショットと電文をグループIDで対応付ける説明が欠けていた**（QA）。同期応答メッセージ送信のテストで中核となる `expectedMessage`・`responseMessage` の役割が、本ページからも飛び先からも辿れなかった。**カラム名とグループIDによる対応付けを1文足し、`testdata_notation-test_shots` へ導線を張った**（`mom.rst:181`）。書式そのものは `testdata_notation.rst:440-441` の領域であるため再掲していない。
3. **図中のクラス名が実装に存在しなかった**（検証）。`send_sync.png` の `StandaloneSupportTemplate`・`BatchRequestTestSupportTemplate` は本文の表と綴り・名称が食い違う。**tip で対応関係を示した**（D-10）。

用語集の無条件置換違反（クラフト、4箇所・D-11）、「処理方式」の二義使用（設計・クラフトが独立に指摘。`glossary.md:123-137` が7名称に限定しているため `mom.rst:10` を「テスト対象によって」に改めた）、`expectedStatusCode` の照合が結果確認の一覧から辿れないこと（QA・検証。`MessagingRequestTestSupport.java:195-210` を確認して `mom.rst:202` に補った）も採った。

採らなかった主なものは4件。**①L3への節ラベル追加**（設計）— 承認済みの `implementation/request_unit_test/rest.rst`・`implementation/deal_unit_test/mom.rst` はどちらもページラベルのみで節ラベルを持たず、ここで基準を変えることになるため見送り、decide-4 に上げた。**②取引単体テスト側のリクエストID tip を `:ref:` に置き換える案**（設計）— 承認済みページの改稿を伴うため自分では直さず decide-1 に上げた。**③期待値の書き忘れによるスキップを `important` にする案**（クラフト）— 第3部に前例が無く、`#27-12` decide-5 と同型のため見送った。**④具象クラス `BatchRequestTestSupport`・`BasicHttpRequestTestTemplate` を継承の説明に足す案**（QA）— `web.rst`・`batch.rst` が持つべき内容であり二重公開になるため見送った（`BatchRequestTestSupport` は図の注記としてのみ登場する）。

## 7. 判断待ち（decide）

1. **リクエストIDの tip が `implementation/deal_unit_test/mom.rst:72-73` と逐語で同一であること。** 持ち込み元は別々の出典（`05_UnitTestGuide/02_RequestUnitTest/send_sync.rst:12-16` と `05_UnitTestGuide/03_DealUnitTest/send_sync.rst:58-62`。いずれも `2e501ad`）だが、片方だけ更新されると食い違う。定義側を1つ決めて他方を `:ref:` にする案がある。承認済みページの改稿になるため自分では直していない。
2. **承認済みの `testdata_notation.rst:1154` が、同期応答メッセージ送信のテストデータを一律 `sendSyncTestData` 配下としていること。** リクエスト単体テストでは誤りで（D-9）、本ページ `mom.rst:177` の飛び先でもある。リクエスト単体テストと取引単体テストのモックを書き分ける必要がある。同様に `implementation/testdata_examples.rst:1802` も取引単体テストの前提で書かれている。
3. **`:ref:` の飛び先 `request_unit_test_web`・`request_unit_test_batch` が4行のスタブであること。** 同期応答メッセージ送信のテストクラス・テストメソッドの作り方をこの2ページに委ねているため、埋まるまで読者が辿れない。`request_unit_test_batch` は `#27-14`、`request_unit_test_web` は `#27-20`。`#27-07` decide-2・`#27-08` decide-6・`#27-09` decide-4・`#27-10` decide-4・`#27-11` decide-3・`#27-12` decide-3 と同型。
4. **本ページに節ラベルが無いこと。** `ntf-doc-weekend-queue.md:110` は `#27-15`（HTTPメッセージング）を本ページとの差分ページと位置づけており、後続ページはページ全体しか指せない。承認済みの兄弟ページに前例が無いため見送った（§6 の①）。第3部全体の方針判断。
5. **受信テストを動かすためのコンポーネント設定が、解説書のどこにも書かれていないこと。** 受信テストは内蔵MQサーバに接続し、キュー名は `TEST.REQUEST`／`TEST.RESPONSE` に固定される（`MessagingRequestTestSupport.java:185-186`・`:197`）。`messagingProvider` という名前でのコンポーネント登録が必須である（同 `:106-110`）。飛び先の `setup/request_unit_test/mom.rst` は全60行で、`reader.fwHeaderfields` と `TestDataConverter` にしか触れていない。第2部への追記要否の判断が要る。
6. **同期応答メッセージ送信で `messagingProvider` を `RequestTestingMessagingProvider` に差し替える手順が、解説書のどこにも書かれていないこと。** `grep -rn "RequestTestingMessagingProvider" --include=*.rst ja/` のヒットは本ページの2件のみである。5と同じく第2部の判断。
7. **図2点が「Excelファイル（テストデータ）」の表記のままであること。** `real_request_test_class.png`・`send_sync.png` の両方。本文は形式中立に統一してある（D-7）。作図元が無く作り直せない。承認済みページで図中のExcel表記に注記を付けた前例は無く、`#27-12` decide-2・`reviews/page-deal_unit_test_http_messaging.md:79-80` と同型の横断課題である。
8. **承認済みの `testdata_notation.rst:528-533` が、メッセージングの `requestPath`・`userId` を「必須」としていること。** MOMの受信テストでは `MessagingRequestTestSupport.java:89-91` が `putIfAbsent` で補完するため、テストデータに書かなくても動作する。別ページの問題として上げる。
9. **JUnit 5 の導線が本ページに無いこと。** `setup/junit5_extension.rst:64-69` に `MessagingReceiveTestExtension`・`MessagingRequestTestExtension` がある。第1部 `about/index.rst:115` が全体を受けており、第3部の他ページも個別には張っていない。`#27-12` decide-5 と同じ、第3部全体の方針判断。
</content>
</invoke>
