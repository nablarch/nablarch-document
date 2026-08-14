# `setup/deal_unit_test/http_messaging.rst`（取引単体テストの設定（HTTPメッセージング））

`#25` のレビュー記録。対象は `mapping.csv` の `dest_page=取引単体テストの設定（HTTPメッセージング）` の1行（`current-0140`、出典 `origin/develop` の `ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst:50-69`）。

## 実装で確認した事実

参照コミット: `nablarch/nablarch-testing` = `e21bf67`（`Merge remote-tracking branch 'origin/release-6u2'`）。読み方は `git -C /home/tie303177/work/nablarch/nablarch-testing show e21bf67:<path>`。

| 本文の記述 | 実装上の根拠 |
|---|---|
| `MockMessagingClient` はテスティングフレームワークが提供するモックアップクラスである | `src/main/java/nablarch/test/core/messaging/MockMessagingClient.java:31-35`（クラスJavadoc「テストデータの内容にもとづき、任意の応答電文を返却するMessageSenderClient」、`implements MessageSenderClient`） |
| メッセージの送信は行われず、テストデータに記述した内容から応答電文が生成されて返される | 同 `:48-91`（`sendSync` に送信処理が無く、`SendSyncSupport#getResponseMessageBinaryByRequestId`（`:57`）で得たバイト列から応答電文を組み立てて返す） |
| `charset` はメッセージングログに出力する電文の文字コード名である | 同 `:36-37`（`LoggerManager.get("MESSAGING")`）、`:149-154`（`emitLog` が `MessagingLogUtil.getHttpSentMessageLog` / `getHttpReceivedMessageLog` に `charset` を渡す）。応答電文の本文解析にはフォーマッタ定義の文字コードを使う（`:104-109`）ため、適用範囲をメッセージングログに限定して書いた |
| `charset` は省略でき、省略した場合は `UTF-8` が使われる | 同 `:46`（`private Charset charset = Charset.forName("UTF-8");`）。setter は `:226-228` の1つのみで、設定可能なプロパティは `charset` だけである |
| コンポーネント名の指定方法はリクエスト単体テストの設定（HTTPメッセージング）と同じである | コンポーネント名は `messageSender.<リクエストID>.messageSenderClient` の**値**から解決され、クライアント実装クラスに依存しない共通機構である（`nablarch-fw-messaging` の `MessageSenderSettings` を `javap -p -c` で確認。`createSettingKey` が `messageSender.<x>.<key>` を組み立て、`getComponent` が得た値を `SystemRepository.get(...)` に渡す）。既に同じ事実を承認済みの `setup/request_unit_test/http_messaging.rst:31` が持つため、書き下ろさずに `:ref:` で導線を張った |

## 出典に無い追記

`design.md` §8 の範囲として次の3件を書いた。上表が根拠。

1. `:21` 「このクラスを使用すると、メッセージの送信は行われず、テストデータに記述した内容から応答電文が生成されて返される。」— 対の承認済みページ（`setup/request_unit_test/http_messaging.rst:21`）が同型の文を持ち、`/rn:ty`（2026-08-13）で「残す」と回答されている（`reviews/page-request_unit_test_setting_http_messaging.md`）
2. `:31` コンポーネント名の指定方法への `:ref:`
3. `:33` 「メッセージングログに出力する電文の文字コード名」という精密化（出典は「ログに出力する文字コード」）

## 4観点レビュー ラウンド1

観点A（網羅性）／B（トンマナ）／C（用語）／D（整合性）を、それぞれ別のサブエージェントで実施した。依頼プロンプトには Rules の3点（実測で裏付ける／付属の検証スクリプトを正解にしない／敵対的にレビューする）を入れた。

判定: **A FAIL（`must` 1）／B PASS／C PASS／D FAIL（`must` 1）**。重複除去後の指摘は12件（`must` 2・`should` 6・`info` 4）。

### 是正を試みた4件（うち2件は検証ラウンドで取り消し）

| # | 観点 | 指摘 | 是正と、その後の扱い |
|---|---|---|---|
| R1-1 | D（`must`） | リード文に「テスト対象がウェブアプリケーションであり、HTTPメッセージ送信を伴う場合」という前提が無く、処理方式名から想定される読者と出典が想定する読者がずれる（出典 `http_send_sync.rst:7`、`design.md:125`） | いったんリード文を書き換えたが、**検証ラウンドの `must` により取り消して元に戻した**。根拠とした `design.md:125` は「**第3部の**2ページ」に課された規定であり、出典 `:7` も `current-0140` ではなく第3部割当の `current-0138` に属する。第2部にも広げるかは**判断待ち3**としてユーザーに上げる |
| R1-2 | D（`should`） | `.. tip::` の「テストを実装するアプリケーション開発者」が、取引単体テストにテスト実装がある前提を持ち込む | いったん「テストを実装する」を落としたが、**検証ラウンドの `should` により取り消して元に戻した**。取引単体テストにもテストデータの記述作業があり（`testdata_notation.rst:1251`、出典 `http_send_sync.rst:25`）、「テストを実装するアプリケーション開発者」は `index.rst:13` が定める役割名である。是正の**結果**は `design.md:113` に違反していなかったが、**根拠**が成り立たなかった |
| R1-3 | B（`should`） | `:31` の「決まり方」は `ja/` 配下で本ページの1件しか用例が無い造語的な体言化。既存は「導出方法」「定義方法」（`universal_dao.rst:672`・`nablarch_validation.rst:473`） | 「指定方法」に置き換えた（**確定**）。参照先 `request_unit_test/http_messaging.rst:31` の本文「コンポーネント名には…に指定した名前を使用する。」と語が対応する。検証ラウンドも妥当と判定 |
| R1-4 | B（`should`） | 電文のテストデータの記述方法への `:ref:` が1つも無い。承認済みの同種ページは必ず `testdata_notation-messaging_data` への導線を持つ（`request_unit_test/mom.rst:60` ほか） | `:35` に導線を足した（**確定**）。当初「応答電文の」と書いたが、検証ラウンドの `should`（モックアップクラスは要求電文のフォーマット定義も要る。`MockMessagingClient.java:52`・`:164-166`・`:40`、参照先 `testdata_notation.rst:1251`）を容れて「電文のフォーマットとデータの記述方法は…を参照。」に広げた |

### 対応せず記録に留めた8件

| # | 観点 | 指摘 | 対応しない理由 |
|---|---|---|---|
| R1-5 | A（`must`） | このページの手順だけでは `MockMessagingClient` が動作しない。`filePathSetting` の `sendSyncTestData` と `messagingTestDataParser` が必須（無い場合 `IllegalStateException`。`SendSyncSupport.java:49`・`:344-352`・`:413-419`。`nablarch-testing-default-configuration` にも含まれない） | **ユーザー判断に上げる（下記「判断待ち」1）。** この2つは `mapping.csv` の `current-0158` で `取引単体テストの設定（MOMによるメッセージング）`（`setup/deal_unit_test/mom.rst`、未作成）に割り当てられている。本ページ側で解決するには未作成ページへの `:ref:`（前方参照スタブが要る）か、`current-0158` の割当先を `setup/common.rst` に変える改訂が要る。どちらも本タスクの範囲を超える |
| R1-6 | D（`should`） | 本ページと `request_unit_test/http_messaging.rst` が同じコンポーネント名 `defaultMessageSenderClient` に別クラスを登録する例を示しており、両方を行うプロジェクトでは衝突する（実装リポジトリの試験資源は `messageSender.config:30-116` / `:121` でリクエストIDごとに別名にしている） | **ユーザー判断に上げる（下記「判断待ち」2）。** 出典に無い記述であり、かつ片方のページにだけ書くと非対称になる。承認済みページに手を入れる判断が要る |
| R1-7 | C（`should`） | `:21` の「メッセージの送信」は、同じ文の「応答電文」と層が揃わない。`電文` にすべき | 承認済みの兄弟ページ `request_unit_test/http_messaging.rst:21` が一字一句同じ文言で、片方だけ直すとページ間の新たな揺れになる。`メッセージ` は `glossary.md` §8 の置換表に無く（`glossary.md:158` の意味欄自身が「メッセージを送信し」と書く）、`must` ではない。2ページ同時に直すかは承認済みページの改訂判断であり、申し送りとする |
| R1-8 | C（`should`） | `アプリケーション開発者` が `glossary.md` に未収載で、`アプリケーション開発者`（4件）・`アプリケーションプログラマ`（`request_unit_test/web.rst:229` の1件）・`アプリ開発者`（`design.md:9-10`）の3表記が併存する | 用語集への追加と承認済みページ（`web.rst:229`）の統一を伴うため本タスクの範囲外。**`#pre-last` への申し送り**とする |
| R1-9 | D（`info`） | 「メッセージングログ」に `:ref:`<messaging_log>`` を張れる（`ja/application_framework/application_framework/libraries/log/messaging_log.rst:1`） | 兄弟ページ `request_unit_test/http_messaging.rst:33` も同じ地の文であり、本ページだけ張ると非対称になる。申し送りとする |
| R1-10 | D（`info`） | 応答電文のテストデータが見つからない場合は `HttpMessagingTimeoutException` になる（`MockMessagingClient.java:57-66`） | 例外時の挙動はコンポーネント設定の説明ではなく、第2部の記載範囲（`design.md` §3）に入らない |
| R1-11 | A・B・D（`info`） | `.. tip::`（アーキテクト向けの注記）が `setup/deal_unit_test/rest.rst` に無く、取引単体テストの設定ページどうしで扱いが揃っていない。また出典 `:51` の「通常」が本ページで落ちている | 本ページの注記は出典 `:51` に根拠がある。`rest.rst` は出典に同種の記述が無いため注記が無いのが正しく、非対称は出典の差に由来する。「通常」の欠落は承認済みの兄弟ページと同一文言であり、そちらに合わせた |
| R1-12 | C（`info`） | XMLの値 `Shift-JIS`（ハイフン）は `ja/` 全体で本ページと兄弟ページの2件のみで、他9件は `Shift_JIS` | 出典 `http_send_sync.rst:64` の逐語引き継ぎであり、Javaのエイリアスとして有効（観点Dが `Charset.forName("Shift-JIS")` の実行で確認）。値の表記をリポジトリ多数派に寄せるかは本ページ単独では決められない |

### 検証ラウンド（是正差分のみ）

是正4件に限定した検証観点を別のサブエージェントで1回実施した（`steering.md` `#10` の共通 Steps「是正ラウンド2以降は、是正差分に限定した検証観点のみを回す」に従う）。依頼プロンプトには Rules の3点を入れた。

判定: **FAIL（`must` 1・`should` 4・`info` 2）**。是正の範囲は逸脱なし（`git status --porcelain -uall` の全件が本作業の3ファイル）。指摘はすべて是正1・2・4 に集中しており、**是正1・2 を取り消し、是正4 を修正**して収めた。

| # | 種別 | 指摘 | 対応 |
|---|---|---|---|
| V-1 | `must` | 是正1 の根拠2件がいずれも第2部に適用されない（`design.md:125` は第3部2ページ宛て、出典 `:7` は `current-0138`＝第3部割当）。`design.md:696`「マッピングにない記述を追加しない」に触れる | 是正1 を取り消し、**判断待ち3** としてユーザーに上げる |
| V-2 | `should` | 是正1 のリード文が、第2部の本文を持つ8ページすべてが守る型（「〈処理方式〉の〈テスト種別〉では、」）を1ページだけ崩す。さらに「取引単体テスト（ウェブアプリケーション）」は `design.md:951` に実在する別ページ名であり、読者が取り違え得る | 是正1 の取り消しで解消 |
| V-3 | `should` | 是正1 で `:10` を「ウェブアプリケーション」に限定した一方、`:21` は無限定のままで適用範囲が食い違った（実装上も `MockMessagingClient` にウェブ限定の要素は無い。`MockMessagingClient.java:35`） | 是正1 の取り消しで解消 |
| V-4 | `should` | 是正1 の「その送信に使用するモックアップクラス」が、`:21` の「メッセージの送信は行われず」と噛み合わない | 是正1 の取り消しで解消 |
| V-5 | `should` | 是正2 の根拠が実測と合わない（取引単体テストにもテストデータの記述作業がある。`index.rst:13` が「テストを実装するアプリケーション開発者」を役割名として定義）。ただし是正後の本文が `design.md:113` に違反していたわけではない | 是正2 を取り消し、兄弟ページ `request_unit_test/http_messaging.rst:17` と一字一句揃えた |
| V-6 | `should` | 是正4 の「応答電文の」が狭い。モックアップクラスは要求電文のフォーマット定義も要る（`MockMessagingClient.java:52`・`:164-166`、`requestMessageFormatFileNamePattern = "%s_SEND"` は `:40`。試験資源に `RM11AC0202_SEND.fmt` と `RM11AC0202_RECEIVE.fmt` が両方ある） | 「電文のフォーマットとデータの記述方法は…」に広げた |
| V-7 | `info` | 是正3 は妥当。`:ref:` の文型・エスケープも既存慣行（`request_unit_test/batch.rst:82`）と同型。RST は独立に組んだ docutils パースで系統エラー0件、範囲外の変更0件 | 記録のみ |

**本文に残った是正は2件**（R1-3 の「指定方法」、R1-4 の `:ref:` 追加）。是正1・2 の取り消し後、`git diff` 上の本文は初版に対して2箇所の差分のみとなる。

## 判断待ちと、その回答（`/rn:ty`、2026-08-14）

公開本文は承認された（`/rn:ty`）。3件とも回答が出ており、**回答2・3 は本ページの本文を変更しない**。回答1 の作業は `#26`（`setup/deal_unit_test/mom.rst` 作成）で行う。

1. **`sendSyncTestData` と `messagingTestDataParser` の設定の置き場所**（R1-5、観点A の `must`／観点D の `should`）。本ページの手順だけではモックアップクラスが動作しない。案A: `setup/deal_unit_test/mom.rst` 作成タスク（`current-0158`）への申し送りとし、作成後に本ページから `:ref:` を張る。案B: 3処理方式に共通する設定として `setup/common.rst` に置き、`current-0158` の割当先を改訂する

   **回答: 案B を採る（`setup/common.rst` に置く）。ただし適用範囲の記述を訂正する。** 案Aを採らないのは、MOM をやらない読者を MOM のページへ送ることになり、`design.md:125` が問題としている読者のずれを解説書の側で作り出すため。未作成ページへの前方参照スタブも作らない（参照先が空のまま残る期間ができる）。`setup/common.rst` を選ぶ根拠は `design.md:192` が共通設定の範囲に「テストデータの配置」を挙げていること。ただし節の見出しで適用条件を名乗る（例:「同期応答メッセージ送信のテストデータの配置場所を設定する」）。

   **訂正 — 「3処理方式に共通」は誤りである。** この2つを必要とするのは取引単体テストのうち `HTTPメッセージング` と `MOMによるメッセージング` の2処理方式だけで、`RESTfulウェブサービス` の取引単体テストは通らない。`SendSyncSupport` を生成するのは `MockMessagingClient.java:54`（HTTPメッセージング）と `MockMessagingContext.java:52`・`:93`（MOM）の2クラスのみである（`nablarch/nablarch-testing` = `e21bf67` を `git grep 'new SendSyncSupport' -- src/main` で実測）。リクエスト単体テスト側は `RequestTestingSendSyncSupport` を通る別経路で、テストデータの取得は `RequestTestingSendSyncSupport.java:155-156` → `TestSupport.java:403-408` の `SystemRepository.get("testDataParser")`、パスもテストクラス自身のリソースパス（`:111-112`）であり、`sendSyncTestData` も `messagingTestDataParser` も参照しない。必須である事実そのもの（`SendSyncSupport.java:346-353`・`:416-419` の `IllegalStateException`）と、デフォルト設定に含まれない事実（`e21bf67` の `src/main` で `messagingTestDataParser` にヒットするのは `SendSyncSupport.java:416` の1件のみ。実測）は正しい。

2. **同一コンポーネント名 `defaultMessageSenderClient` の衝突**（R1-6、観点D の `should`）。リクエスト単体テストと取引単体テストの両方を行うプロジェクトでは、別名にしてリクエストIDごとに使い分ける必要がある。書くとすれば両ページに書くことになり、承認済みページの改訂判断を伴う

   **回答: 本文には書かない。`#pre-last` の横断確認項目とする。** 散文で注意書きを足す案は採らない（設定ページの本題から外れる）。名前がリクエストIDごとに決まることは承認済みの `setup/request_unit_test/http_messaging.rst:31` が既に書いており、本ページ `:31` はそこへ導線を張っているため、固定名と誤解する経路は塞がれている。残るのは**例示名の衝突**で、例示名は出典 `http_send_sync.rst:62` の逐語であり、片方だけ変えれば非対称・両方変えれば出典から離れる。2ページを揃えて判断すべき事項として `#pre-last` に送る。

3. **リード文に「テスト対象がウェブアプリケーションであり、HTTPメッセージ送信を伴う場合」という前提を明示するか**（R1-1／V-1・V-2）。明示する場合は `design.md:125` の適用範囲を第2部の当該ページにも広げる改訂が要り、第2部8ページが守るリード文の型を保つ書き方（例:「HTTPメッセージングの取引単体テストでは、テスト対象のウェブアプリケーションがHTTPメッセージ送信を行う場合に使用するモックアップクラスを登録する。」）にする必要がある。明示しない場合は、この前提の明示は第3部 `implementation/deal_unit_test/http_messaging.rst` の作成タスクに委ねる

   **回答: 明示しない（現状維持）。本文を変更しない。** 理由は3つ。(1) `design.md:125` は第3部の2ページ宛ての規定であり、適用範囲を第2部へ広げるには `design.md` の改訂が要るが、それを正当化する事情が本ページにはない（前提を必要とする出典 `http_send_sync.rst:7` は第3部割当の `current-0138` に属し、本ページの唯一の出典 `current-0140` は設定手順だけである）。(2) 第2部のリード文の型を1ページだけ崩す。(3) 実装にウェブ限定の要素が無く（`MockMessagingClient.java:35`）、限定すると本文 `:21` の無限定な記述と食い違う。前提の明示は第3部 `implementation/deal_unit_test/http_messaging.rst` の作成タスクに委ねる。

## `#26` 以降への申し送り（`/rn:ty` で扱いを確定済み）

1. **`sendSyncTestData` と `messagingTestDataParser` の設定の置き場所**（R1-5）。**`#26` で実施する**（上記回答1）。`current-0158` を SPLIT し、`sendSyncTestData`（`send_sync.rst:299-334`）と `messagingTestDataParser`（`:336-360`）を `setup/common.rst` へ、モックアップクラスの設定（`:286-297`）を `setup/deal_unit_test/mom.rst` へ割り当てる。`pom.xml` への dependency 追加（`:364-383`）の帰属は `#26` 着手時に判断する。**「どちらにするかを決める」という形では残さない**
2. **同一コンポーネント名の衝突**（R1-6）。**`#pre-last`**（上記回答2）。散文ではなく2ページの例示名を揃えて判断する
3. **`メッセージの送信` と `電文の送信` の統一**（R1-7）、**`アプリケーション開発者` の用語集への登録**（R1-8）、**`メッセージングログ` への `:ref:`**（R1-9）。**`#pre-last`**。`アプリケーション開発者` は `ja/` 配下（`guide/` を除く）で3件、`アプリケーションプログラマ` は `setup/request_unit_test/web.rst:229` の1件のみで、外れ値は承認済みの `web.rst` 側である
4. **第3部「取引単体テスト（HTTPメッセージング）」作成時の重複回避**。本ページ `:21` の「テストデータに記述した内容から応答電文が生成されて返される」は、`current-0139` の出典 `http_send_sync.rst:27` と同じ事実である。第3部で書き下ろすと重複する。**そのまま申し送る**
