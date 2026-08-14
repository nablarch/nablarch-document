# page-deal_unit_test_http_messaging — 取引単体テスト（HTTPメッセージング）

対象ファイル: `ja/development_tools/testing_framework/implementation/deal_unit_test/http_messaging.rst`
キュー番号: `#27-10`
個別指示: `ntf-doc-27-small-3rd.md` §3

## 1. 参照リポジトリ

| リポジトリ | 参照コミット | 用途 |
| --- | --- | --- |
| `nablarch-testing` | `e21bf67` | `MockMessagingClient` ・`SendSyncSupport` ・`MockMessagingContext` の実装確認 |

本ページで参照した3クラスについて `git diff --stat e21bf67 HEAD -- <3ファイル>` を実行した。差分は0行である。

## 2. 出典行の消化

`mapping.csv` で `dest_page` が「取引単体テスト（HTTPメッセージング）」である行は2件である。

| mapping_id | src_file | src 行 | 行数 | disposition | 反映先 |
| --- | --- | --- | --- | --- | --- |
| current-0138 | `03_DealUnitTest/http_send_sync.rst` | 6-15 | 10 | REFERENCE | `:10` `:15` `:17` `:22` |
| current-0139 | `03_DealUnitTest/http_send_sync.rst` | 24-46 | 23 | MERGE | `:26` `:28` `:30` |

同ファイルの `:1-2` は `current-0137` として DROP、`:50-69` は `current-0140` として第2部「取引単体テストの設定（HTTPメッセージング）」へ割り当てられている。`:16-23`・`:47-49` は見出しと空行であり、どの `mapping_id` にも割り当てられていない。

落とした行は §5 に記録する。

## 3. 実装で確認した事実

`nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/messaging/` 配下。

| 事実 | 出典 |
| --- | --- |
| `MockMessagingClient` は `MessageSenderClient` の実装である | `MockMessagingClient.java:35` |
| ロガー名は `MESSAGING` の1つだけ。`logInfo` で出力するため `INFO` レベルである | `MockMessagingClient.java:37,153` |
| 要求電文（`:52`）と応答電文（`:89`）の両方をログに出力する | `MockMessagingClient.java:52,89` |
| 読み込むのは `RESPONSE_BODY_MESSAGES`（`:57`）と `RESPONSE_HEADER_MESSAGES`（`:70`）の2つだけである。`EXPECTED_REQUEST_HEADER_MESSAGES` ・`EXPECTED_REQUEST_BODY_MESSAGES` は読み込まない | `MockMessagingClient.java:57,70` |
| 応答電文ヘッダが読み取れない場合は空の `Map` を使う（エラーにしない） | `MockMessagingClient.java:71-74` |
| ステータスコードが未設定の場合は `"200"` を設定する | `MockMessagingClient.java:76-79` |
| 要求電文のログ出力に使うフォーマットは、フォーマット定義ファイル `<リクエストID>_SEND`（ベースパス `format`）から取得する。テストデータではない | `MockMessagingClient.java:40,164-166` |
| 応答電文の解析に使うフォーマットは `<リクエストID>_RECEIVE` である | `MockMessagingClient.java:43,105-106,192-196` |
| `charset` の既定値は `UTF-8` である | `MockMessagingClient.java:46` |
| 応答電文本文が `null`（`errorMode:timeout`）の場合は `HttpMessagingTimeoutException` を送出する | `MockMessagingClient.java:58-66` |
| `errorMode:timeout` は `null` を返し、`errorMode:msgException` は `MessagingException` を送出する（`MockMessagingClient` ・`MockMessagingContext` に共通の実装） | `SendSyncSupport.java:290-296` |
| **MOM 版の `MockMessagingContext` は `parseRequestMessage` を呼び、`EXPECTED_REQUEST_HEADER_MESSAGES` ・`EXPECTED_REQUEST_BODY_MESSAGES` をテストデータから読み込んで要求電文のログを組み立てる。ここが `MockMessagingClient` との違いである** | `MockMessagingContext.java:55` ／ `SendSyncSupport.java:60,67,82` |
| `nablarch-testing` にフォーマット定義ファイルを生成するコードは無い（`grep -rn "_SEND\|_RECEIVE" src/main/java` の結果は4クラス5箇所で、いずれもファイル名パターンの組み立てと読み込みのみ） | `MockMessagingClient.java:40,43` ／ `RequestTestingMessagingClient.java:76,79,539` |

`HttpMessagingClient.SYNCMESSAGE_STATUS_CODE` の定数値（ステータスコードのカラム名）は `nablarch-fw-messaging` にあり、ルール §1-9 の作業ディレクトリの外であるため **未確認** である。本文でもカラム名を名指ししていない。

## 4. 実測

| 項目 | 実測値 |
| --- | --- |
| 本文行数 | 30行（末尾改行を除く） |
| 見出し | L1 1本・L2 2本（`機能概要` `使用方法`）・L3 1本（`テストデータを作成する`）。個別指示 §3 のセクション構成と一致 |
| 下線 | L1 `:4` = 50（表示幅36）／L2 `:13` `:20` = 50（同8）／L3 `:25` = 49（同22）。承認済み3ページと同じ |
| `:ref:` | 5本（`deal_unit_test_setting_http_messaging` ・`deal_unit_test_mom` ×2・`testdata_notation-messaging_data` ・`testing_framework_common-send_sync_test_data` ・`testdata_examples`）。すべて実ファイルに存在し、リンク文字列が飛び先の見出しと一致 |
| コードブロック・画像・表・`tip` | いずれも0件 |
| 行末空白 | 0件 |
| 禁止語（`不具合` `バグ` `将来` `修正され`） | 0件 |
| `glossary.md` の揺れ表記 | 0件（`HTTP同期応答メッセージ送信` ・`同期応答メッセージ送信処理` ・`メッセージング処理` ・`メッセージ同期送信` ・`メッセージ受信処理` ・`テストケース` ・`自動テストフレームワーク` ・`バッチ処理`） |
| `verify_mapping.py` | `OK: no errors`（exit 0） |
| Sphinx ビルド（`-E` フル） | `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで、新規0件 |

`:ref:` の飛び先（実測）

| ラベル | 飛び先 | 見出し |
| --- | --- | --- |
| `deal_unit_test_setting_http_messaging` | `setup/deal_unit_test/http_messaging.rst:1` | `:3` 取引単体テストの設定（HTTPメッセージング） |
| `deal_unit_test_mom` | `implementation/deal_unit_test/mom.rst:1` | `:3` 取引単体テスト（MOMによるメッセージング） |
| `testdata_notation-messaging_data` | `implementation/testdata_notation.rst:1148` | `:1150` メッセージングのデータを記述する |
| `testing_framework_common-send_sync_test_data` | `setup/common.rst:118` | `:120` 同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する |
| `testdata_examples` | `implementation/testdata_examples.rst:1` | `:3` テストデータの記載例 |

## 5. 出典から変えた点

出典は `2e501ad:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst`（69行）。

**D-1 Excel記載例の画像 `_images/http_send_sync_test_data.png` を採らなかった（出典 `:31`・`:32`・`:34`・`:36`・`:37`）。**
個別指示 `ntf-doc-27-small-3rd.md:102` は「判断がつかない場合は `git mv` して残す方（出典に忠実な方）を採り、`decide` に書く」と定めている。**本ページはこれに従わず、落とす方を採った。判断がついたためである。** 理由は2つ。第一に、画像内の要求電文ブロック（`EXPECTED_REQUEST_BODY_MESSAGES` に吹き出し「要求電文はフォーマットのみ定義する。」）は、`MockMessagingClient` が読まないデータブロックである（`MockMessagingClient.java:48-91` に `EXPECTED_REQUEST_*` の参照が無く、読むのは `:57` `RESPONSE_BODY_MESSAGES` と `:70` `RESPONSE_HEADER_MESSAGES` の2つだけ）。掲載すると、実装が無視する記述を読者に書かせることになる。`design.md` §8 の実装優先による。第二に、画像の応答電文ブロックに相当する内容は `implementation/testdata_examples.rst:1800`（同期応答メッセージ送信の応答電文を配置する）・`:1859`（ステータスコードを省略する）が Excel形式・YAML形式の両方で既に持っている。**`decide-2` として上げる。**

**D-2 出典の見出し2本を落とした（出典 `:31-32` 「書き方の例」・`:40-41` 「電文のフォーマットおよびデータの記載方法」）。**
前者は配下が D-1 の画像1枚だけであり、画像を落とすと中身が無くなる。後者は配下の本文（`:42`・`:44`）を `:26`・`:28` に統合した。個別指示 §1-1「出典に無いL3は立てない」に対応する裏側の判断であり、`使用方法` 配下のL3を §3 のセクション構成どおり1本に畳んだものである。

**D-3 「Excelファイル」を「テストデータ」に置き換えた（出典 `:25`）。**
個別指示 §3 判断2 による。記法は `テストデータの書き方` が引き受けており、`style.md` S-10 の Excel/YAML 書き分けを本ページで再現しない。

**D-4 要求電文のフォーマットについて、出典の記述を実装にもとづいて補正した（出典 `:28` → 本文 `:30`）。**
出典は「要求電文のフォーマットは、モックアップクラスが要求電文のログを出力するために使用される」と書いており、テストデータに要求電文のフォーマットを定義するように読める。`MockMessagingClient` はテストデータの要求電文を読まず、`format` のベースパスに置いたフォーマット定義ファイルからフォーマッタを生成する（`MockMessagingClient.java:40,164-166`）。`MOM` 版はテストデータから読む（`MockMessagingContext.java:55` → `SendSyncSupport.java:60,67,82`）ため、`mom.rst:68`「要求電文については、フォーマットのみ定義する」との対比を本文に残した。`design.md` §8 の実装優先による。

**D-5 テスト結果の確認に使うログの差分を追記した（出典に無い事実）。**
本ページは進め方を `deal_unit_test_mom` に送っているが、飛び先の `mom.rst:87-129` は `MESSAGING_MAP` ・`MESSAGING_CSV` へ `DEBUG` レベルで出す Map形式・CSV形式のログの説明で構成されており、HTTPメッセージングでは出力されない。`MockMessagingClient` は `MESSAGING` ロガーへ `logInfo` で要求電文・応答電文を出すだけである（`MockMessagingClient.java:37,52,89,149-154`）。Map形式・CSV形式のログは `SendSyncSupport#parseRequestMessage` 経由でのみ出力され、`MockMessagingClient` は同メソッドを呼ばない（`grep parseRequestMessage` の結果0件）。差分を書かないと「同じである」が誤りになるため、`:22` に2文で追記した。`design.md:517-520` にもとづく出典外事実の追記であり、実装の出典は本記録 §3 に記載済みである。

**D-6 応答電文のヘッダのデータブロックについて、出典に無い事実を追記した（本文 `:28` 3文目）。**
出典 `:44` は「HTTP通信は要求電文・応答電文ともにヘッダが存在しないため、本文のみ定義する」とだけ書いている。`RESPONSE_HEADER_MESSAGES` に記述したカラムは、そのまま応答電文のヘッダレコードとしてアプリケーションへ渡る（`MockMessagingClient.java:70` 読み込み、`:86` `setHeaderRecord`）。ヘッダを定義できないと読める記述を避けるため追記した。

**D-7 出典 `:44` の「フレームワーク制御ヘッダが無いため」という前提を本文に書かなかった。**
HTTPメッセージングでもフレームワーク制御ヘッダは使用できる（`ja/application_framework/application_framework/libraries/system_messaging/http_system_messaging.rst:197-198`「フレームワーク制御ヘッダを使用するか否かは任意に選択できる」）。前提として書くと誤りになるため、結論（本文のデータブロックだけを定義すればよい）だけを書いた。

**D-8 リード文を「対象とする」＋「検証する」の2文にした。**
承認済み3ページ（`rest.rst:10` ・`batch.rst:10` ・`mom.rst:10`）が「〜の取引単体テストは、…を検証する」で主述を対応させている。`design.md:125` の申し送りが求める前提（テスト対象がウェブアプリケーションであり、HTTPメッセージ送信を伴う場合）は、1文目「HTTPメッセージ送信を伴うウェブアプリケーションを対象とする」で満たしている。

**D-9 `HTTP` の直後の `\ ` エスケープを外した。**
対になる第2部ページ `setup/deal_unit_test/http_messaging.rst:10,21` が `HTTPメッセージ送信` をエスケープ無しで書いている。ページ内で `HTTPメッセージング` と表記が割れていたため、エスケープ無しに統一した。レンダリング結果は変わらない。

**落とした行の一覧（出典16行の非空行のうち）**: `:31`・`:32`・`:34`・`:36`・`:37`（D-1・D-2）、`:40`・`:41`（D-2）。残る行はすべて反映済みで、未消化は0行である。`:1-2` は `current-0137`（DROP）、`:50-69` は `current-0140`（第2部へ MOVE）で本ページの担当外。

## 6. 4観点レビュー

QA・設計・クラフト・検証の4観点を別々のサブエージェントで回した。指摘は計27件、うち採ったのは次の11件である。

**採った是正**

1. `:22`「テスト結果の確認方法は MOM と同じ」の削除と差分の明記（QA1・設計1・クラフト5）。→ D-5
2. `:15` 2文目の削除（設計2）。第2部 `setup/deal_unit_test/http_messaging.rst:21` のほぼ逐語コピーであり、個別指示 §1-3「参照先ページを本文で言い換えない」に反していた。
3. `:28`「ステータスコードを指定する場合にかぎり」の撤回（QA3）。→ D-6
4. `:28` の「フレームワーク制御ヘッダが無いため」という因果の削除（クラフト8・QA4）。→ D-7
5. `:30` の因果の向きを直した（クラフト10）。「ログ出力にフォーマット定義ファイルを使う**ため**、テストデータを読み込まない」と読める順序だった。
6. `:30` から `<リクエストID>_SEND` を落とした（設計4）。命名規則は `testdata_notation.rst:1208` が持っており、二重管理になる。あわせてクラフト10 が指摘した表記の不一致（承認済みは `{requestId}_SEND`）も解消した。
7. `:17` の「それを使った取引単体テストの進め方」を削り「機能は同じである」に絞った（クラフト3）。`:22` と同じことを2回述べていた。
8. `:22` の参照範囲を「同期応答メッセージ送信を伴うウェブアプリケーションを対象とする場合」に限定した（QA6）。`mom.rst:42-61` は受信アプリケーション向けで、HTTPに該当するのは `mom.rst:62` だけである。
9. `:26` にテストデータの置き場所の導線を足した（クラフト6）。`mom.rst:68` と同じく `testing_framework_common-send_sync_test_data` へ送る。同節の見出しは `HTTPメッセージ送信` を名指ししている。
10. `:26` に記述例の導線を足した（クラフト7・QA・検証）。D-1 で画像を落とした代替である。飛び先は `batch.rst:83` にならい `testdata_examples`（ページ単位）とした。節単位の `testdata_examples-messaging_data` は見出しが `testdata_notation-messaging_data` と同一文字列であり、同じページに2本並べると読者がどちらへ飛ぶか区別できないため採らなかった。
11. リード文の主述と `HTTP` のエスケープ（クラフト1・クラフト11）。→ D-8・D-9

**採らなかった指摘**

- **`:28` に「ステータスコードのカラムを省略した場合は `"200"` が使われる」を残す（QA3）** — 設計3 が同じ箇所について「`testdata_notation.rst:1208` と重複するため落とす」と逆向きの指摘をしている。個別指示 §3 判断2 が本ページに残すものを「HTTP固有の差分」に限定しているため、設計3 を採って落とした。既定値は `testdata_notation.rst:1208` と `testdata_examples.rst:1861` の2箇所にある。
- **`:17` にタイムアウト時の挙動の差を書く（QA6）** — `MockMessagingClient.java:58-66` は `HttpMessagingTimeoutException` を送出し、`MockMessagingContext.java:60-67` は `null` を返す。ただし `mom.rst:33` がモックアップクラスの機能として述べているのは「障害を発生させる」までであり、戻り値や例外型には触れていない。文書が説明している水準では「機能は同じ」が成り立つ。
- **「通信先」を「外部システム」に置き換える（クラフト2）** — `glossary.md:158,160` は同じ対象を「外部システム」と呼んでおり、「通信先」は `ja/` 配下で本ページにしか無い語である。一方、出典 `:11` が「『送信キュー』『受信キュー』は『通信先』と読み替える」と明記し、個別指示 §3 判断1 も「通信先」の語で読み替えを指示している。出典に忠実な方を採った。**`decide-3` として上げる。**
- **`testdata_notation.rst:1251` の修正（QA5）** — 別ページであり本ページの担当外。**`decide-4` として申し送る。**
- **`mapping.csv` の `current-0139` の `note` を更新する（QA）** — ルール §1-4 により `mapping.csv` を直接編集しない。

## 7. 判断待ち（decide）

**decide-1 第3部へのアウトライン適用** — 個別指示 §1-1 が求める `decide`（`style.md` S-02 の第2部向けの規定を第3部にも適用してよいか）は、`#27-07` の記録 `reviews/page-deal_unit_test_rest.md` §5 D-1 および §7 decide-1 に1回記録済みである。本ページはそこを指す。

**decide-2 Excel記載例の画像 `_images/http_send_sync_test_data.png` を落としてよいか** — §5 D-1 のとおり落とした。個別指示 `ntf-doc-27-small-3rd.md:102` の既定（判断がつかない場合は `git mv` して残す）とは逆の選択である。**覆す場合は `implementation/deal_unit_test/images/http_messaging/` へ `git mv` し、`テストデータを作成する` 配下に掲載する。** その場合でも、画像内の吹き出し「要求電文はフォーマットのみ定義する。」は `MockMessagingClient` の実装と食い違う点の扱いを別途決める必要がある。なお画像ファイルは `guide/development_guide/05_UnitTestGuide/03_DealUnitTest/_images/` に残置しており、旧ページ一式の削除時にあわせて処理される。

**decide-3 「通信先」の語を使ってよいか** — §6 のとおり出典と個別指示に従って採用した。`glossary.md:158,160` の「外部システム」に寄せるなら、本文 `:10` と `:17` の2箇所を置き換える。ただし `:17` は出典 `:11` の読み替え指示そのものであるため、置き換えると出典から離れる。

**decide-4 `testdata_notation.rst:1251` の申し送り** — 同行は取引単体テストのモックアップクラス全般について「要求電文はログ出力用のフォーマットのみを定義する」と書いており、HTTPメッセージングには当てはまらない（`MockMessagingClient` はテストデータの要求電文を読まない。§3 の表を参照）。MOM に限定する旨の修正が要る。承認済みページであるため本タスクでは触れていない。

**decide-5 `HttpMessagingClient.SYNCMESSAGE_STATUS_CODE` の定数値** — §3 末尾のとおり **未確認**。`nablarch-fw-messaging` はルール §1-9 の作業ディレクトリ外にある。本文でカラム名を名指ししていないため本ページの記述には影響しないが、`testdata_notation.rst:1208` の「ステータスコードカラム」がどのカラム名を指すかは未検証のまま残る。
