# レビュー記録 — リクエスト単体テストの設定（HTTPメッセージング）

対象ページ: `ja/development_tools/testing_framework/setup/request_unit_test/http_messaging.rst`
ページ先頭ラベル: `request_unit_test_setting_http_messaging`（`style.md` S-08 の表から引用。新規考案なし）
タスク: `#19`

## 1. 出典（`mapping.csv` の全件）

`dest_page=リクエスト単体テストの設定（HTTPメッセージング）` は3行。`csv.DictReader` で抽出した。

| `mapping_id` | `src_file` | 範囲 | `lines` | `disposition` | 反映先セクション |
|---|---|---|---|---|---|
| `current-0066-b` | `.../02_RequestUnitTest/http_real.rst` | `120`〜`129` | 10 | SPLIT | フレームワーク制御ヘッダの項目名を指定する |
| `current-0074` | `.../02_RequestUnitTest/http_send_sync.rst` | `143`〜`146` | 4 | MOVE | モックアップクラスを登録する（`tip`） |
| `current-0075` | `.../02_RequestUnitTest/http_send_sync.rst` | `149`〜`164` | 16 | MOVE | モックアップクラスを登録する（本文・XML例・`charset`） |

出典の実物は、現行解説書が本ブランチで削除済みのため `git show origin/develop:<src_file>` で読んだ。

## 2. 実装で確認した事実

参照したクローンとコミット。

| リポジトリ / 成果物 | 取得元 | 参照コミット・版 |
|---|---|---|
| `nablarch/nablarch-testing` | ローカルクローン | `fdf55d4` |
| `com.nablarch.framework:nablarch-fw-messaging` | ローカル Maven リポジトリの sources jar | `6-NEXT-SNAPSHOT` |
| `com.nablarch.configuration:nablarch-testing-default-configuration` | ローカル Maven リポジトリの jar | `6u3` |

| ページの記述 | 実装での裏付け（`file:line`） |
|---|---|
| モックアップクラスは `RequestTestingMessagingClient` | `nablarch-testing` `src/main/java/nablarch/test/core/messaging/RequestTestingMessagingClient.java:53`（`implements MessageSenderClient`） |
| メッセージ送信は行われず、要求電文のアサートと応答電文の返却を行う | 同 `:46`・`:48`（クラスJavadoc「テストデータの内容にもとづき、要求電文のアサートおよび応答電文の返却を行うMessageSenderClient。」「本クラスを使用する場合、メッセージ送信は行われない。」） |
| `charset` は省略可能で、省略時は `UTF-8` | 同 `:85`（`private Charset charset = Charset.forName("UTF-8");`）、`:569-570`（`setCharset`） |
| `charset` はメッセージングログに出力する電文の文字コード | 同 `:147`・`:525-526`（`MessagingLogUtil` への引き渡し） |
| コンポーネント名は `messageSender.<リクエストID>.messageSenderClient` の値から解決される | `nablarch-fw-messaging` `MessageSenderSettings.java:193`（`getComponent("messageSenderClient", SettingType.REQUEST_ID_ONLY, false)`）、同メソッド本体（`getStringSetting` で得た値を `SystemRepository.get(componentName)` に渡す）。実例は `nablarch-testing` `src/test/resources/nablarch/test/core/messaging/web/messageSender.config:121`（`messageSender.RM11AD0201.messageSenderClient=defaultMessageSenderClient`）と同 `web-component-configuration-request-testing.xml:37`（`<component name="defaultMessageSenderClient" class="nablarch.test.core.messaging.RequestTestingMessagingClient">`） |
| 環境設定ファイルで名前を指し示していないと、コンポーネントを登録してもモックアップクラスは使われない（＝この追記は `design.md` §8「出典が欠いている、実装上必須の設定」に該当する） | `nablarch-fw-messaging` `MessageSender.java:80-84`（`settings.canUseMessageSenderClient()` が偽ならプロバイダ経路へ分岐する）。偽になる条件は `MessageSenderSettings.java:280-283`（`canUseMessageSenderClient()` は `messageSenderClient != null` を返す）と `:191-193`（`required = false` のため未設定なら `null`） |
| キー名は `reader.fwHeaderfields` | `nablarch-testing` `src/main/java/nablarch/test/core/reader/MessageParser.java:33`（`FW_HEADER_KEY = "reader.fwHeaderfields"`） |
| 未指定時に解釈される項目名は `requestId`・`userId`・`resendFlag`・`resultCode` | 同 `:107-110`（`SystemRepository.getString(FW_HEADER_KEY)` が空なら `asSet("requestId", "userId", "resendFlag", "resultCode")`）。判定は同 `:102-104`・`:86-88` |

### デフォルト値の基準（`design.md` §8）

`nablarch-testing-default-configuration` `6u3` の jar を展開し（XML 19ファイル・`.config` 5ファイル）、
`grep -rl "MessagingClient\|fwHeaderfields\|defaultMessageSenderClient"` を jar 全体に対して実行した結果、
該当ファイルは**0件**である。
したがってデフォルト設定はこのページの設定項目を登録しておらず、`charset` はフィールド初期値
（`UTF-8`）がそのまま実効値になる。`reader.fwHeaderfields` も未設定であり、`MessageParser` の
既定の4項目がそのまま実効値になる。`design.md` §8「デフォルト設定が設定していない項目は、
フィールド初期値がそのまま実効値になる」に該当する。

## 3. 4観点レビュー

### ラウンド1（4観点・各観点を別のサブエージェントで実施）

| 観点 | 判定 | `must` | `should` | `note` |
|---|---|---|---|---|
| A 網羅性 | FAIL | 3 | 1 | 3 |
| B トンマナ | FAIL | 1 | 4 | 3 |
| C 用語 | FAIL | 1 | 2 | 2 |
| D 整合性 | FAIL | 3 | 2 | 5 |

`must` 8件（重複除去後7件）と主要な `should` への対応は次のとおり。

| # | 観点 | 指摘 | 対応 |
|---|---|---|---|
| 1 | D | `reader.fwHeaderfields` はHTTPメッセージ**受信**側にしか効かない。送信側（モックアップクラス経路）には効かないのに、ページは両者を同じテストの設定として書いていた | リード文と両節に適用範囲（送信／受信）を明記した。裏付けは §2 の実装表を参照 |
| 2 | D | `reader.fwHeaderfields` は\ YAML\ 形式では使用されない。`testdata_notation.rst:1263` と正面から矛盾していた | `important` で\ Excel\ 形式に限定した |
| 3 | D | 参照先 `http_system_messaging.rst:85` が「コンポーネント名は `messageSenderClient` と指定する」と書いており、本ページの例（`defaultMessageSenderClient`）と矛盾する | 当該 `:ref:` を削除し、コンポーネント名の解決規則を実装どおり1文で述べた。FW解説書側の記述が実装より狭い件は `decide` 3 として上申 |
| 4 | A | 既定のフィールド名4種の列挙が、マッピングにも `design.md` §8 のどの例外にも根拠がない | 列挙を削除し、`:ref:`testdata_notation-messaging_data`` への参照に置き換えた。D の `should` 1（`testdata_notation.rst:1137` との重複）も同時に解消した |
| 5 | A | `reader.fwHeaderfields` を設定する条件が出典より広い（出典は「項目を変更している場合」、ページは「読み書きを変更している場合」） | 「フィールド名を既定から変更している場合」に狭めた |
| 6 | B | 「フレームワーク制御ヘッダは…フレームワーク制御ヘッダとして解釈される」の同語反復で、文が情報を持たない | 当該文を削除した（対応4に含まれる） |
| 7 | C | `モックアップクラス` の用法が `glossary.md:160` の意味列（取引単体テストに限定）と衝突する | ページ側は出典どおりの用法を維持。`glossary.md` の意味列の是正は `decide` 1 として上申 |
| 8 | B/C | 「項目」「項目名」「フレームワーク制御ヘッダ名」の3語が混在 | `testdata_notation.rst:1137` に合わせて「フィールド名」に統一した |
| 9 | B | タイトル下線が52文字で、NTF全18ページの実測則（`max(50, タイトル表示幅)`）から外れる | 50文字にした。実測則は自分でも全ページ走査して確認した |
| 10 | A/D | `tip`（アーキテクトが行う旨）の射程が「モックアップクラスを登録する」節に閉じており、出典（L2節全体を指す）より狭い | `使用方法` 直下へ移し、両方の設定に掛かるようにした |

**採らなかった指摘**

- D `should` 2「`tip` を削除して `index.rst:13` に委ねる」— **採らない。** 削除すると `current-0074`（MOVE）を落とすことになり、Rules「マッピングにある内容を落とさない」に反する。射程の是正（対応10）にとどめた
- B `should` 5・note「『にもとづいて』の仮名書き／『に従って』との不統一」— リード文の当該表現自体を書き直したため解消した

### ラウンド2（是正差分限定の検証）

判定 **PASS**（`must` 0 / `should` 3 / `note` 3）。是正1〜10が実物に反映され、指示範囲外の変更が
作業ツリーに無いことが確認された。検証項目（`:ref:` の実在／送信側・受信側の効き方／`Excel` 形式限定／
`YAML` で使用されないこと／コンポーネント名の解決規則／`charset`／段落の途中改行0件／見出し下線の実測則）は
すべて実装・既存ページと一致した。

`should` への対応。

| # | 指摘 | 対応 |
|---|---|---|
| 1 | モックアップクラスを使うのはHTTPメッセージングのテストだけではない。ウェブ（`AbstractHttpRequestTestTemplate.java:316`）・スタンドアロン（`TestShot.java:188`）のリクエスト単体テストからも初期化される | リード文と本文を「HTTPメッセージ送信を伴うリクエスト単体テスト」に緩め、他の処理方式のテストでも同じである旨を1文加えた |
| 2 | `testdata_notation.rst:1244` の「キー名は `reader.fwHeaderfields` の設定に合わせる」が、本ページの「`YAML` 形式では使用されない」と字面で食い違う | **本ページ側は是正しない**（実装どおり）。`:1244` は同じファイルの `:1263` とも食い違っており、是正対象は第3部側である。申し送り4に記載 |
| 3 | キー名と例示値が本ページと `testdata_notation.rst:1137` に重複して残る | **本ページ側は是正しない**。設定手順は第2部に置くのが `design.md` §3 の記載範囲であり、寄せるなら第3部側を参照に置き換える。申し送り5に記載 |

`note` 1（引継ぎ記録の理由づけが逆である、という指摘）は**採らない。** 実物を確認した結果、指摘のほうが誤りである。
`SendSyncMessageParser.java:109-141` は `createFixedLengthFileParser` を override し、`MessageParser` の
無名サブクラス（`processDirectives` でフレームワーク制御ヘッダを吸収する実装）ではなく、
`FixedLengthFileParser` の無名サブクラス（override するのは `onReadingValues` と `createNewFile` のみ）を
返している。したがって送信側では `processDirectives` の吸収そのものが働かない。加えて
`GroupMessageParser.java:57-59` が `Collections.emptyMap()` を「FWヘッダ取得機能は使用しないので、
何も設定しない」というコメントとともに渡している。申し送り1の記述はこのままでよい。

## 4. ユーザー判断を仰ぐ事項（`decide`）

### `decide` 1 — `glossary.md:160` の `モックアップクラス` の意味列が、自らの採用根拠より狭い

意味列は「同期応答メッセージ送信・HTTPメッセージ送信を伴う**取引単体テスト**で、外部システムの代わりに
応答電文を返すクラス」と取引単体テストに限定している。しかし同じ行の採用根拠が数えた「現行解説書21件、
4ファイル」には `02_RequestUnitTest/http_send_sync.rst` が含まれ、その `:150` は
「コンポーネント設定ファイルに、**リクエスト単体テストで使用する**モックアップクラスを設定する。」である
（`git show origin/develop:` で確認）。本ページは出典どおりリクエスト単体テストの文脈で使っており、
実体は `RequestTestingMessagingClient`、取引単体テストのそれは別クラスである。

**推奨**: 意味列を「同期応答メッセージ送信・HTTPメッセージ送信で、外部システムの代わりに応答電文を返す
クラス。リクエスト単体テスト・取引単体テストの双方で使い、実体は別のクラスである」に是正する。正表記は
変わらないため既存ページの書き換えは発生しない。是正しない場合は、本ページで
`モックアップクラス` の語を使わない書き方に変える必要がある。

### `decide` 2 — 出典にもマッピングにも無い追記2件を残すかどうか

`design.md` §8「出典が欠いている、実装上必須の設定の追記」に該当するのは次の1件で、これは残した。

- 「コンポーネント名には、環境設定ファイルの `messageSender.<リクエストID>.messageSenderClient` に指定した
  名前を使用する。この名前で参照されていないコンポーネントは、モックアップクラスとして使用されない。」
  — 未設定だとモックアップクラスに到達しない（§2 の実装表）。`#17` の `httpServerFactory` と同じ類型

一方、次の1件は §8 のどの例外にも当たらない（設定ではなく挙動の説明であるため）。

- 「このクラスを使用すると、メッセージの送信は行われず、要求電文のアサートと応答電文の返却がテストデータの
  内容にもとづいて行われる。」— 典拠は `RequestTestingMessagingClient.java:46`・`:48` のJavadoc

**推奨**: 残す。`style.md` S-02 はリード文と各節に「そのページで何ができるようになるか」を求めており、
モックアップクラスが何をするクラスかを述べずに「登録する」だけでは、読者は登録の可否を判断できない。
落とす場合は当該1文のみを削る。

### `decide` 3 — FW解説書 `http_system_messaging.rst:85` の記述が実装より狭い

同行は「ルックアップして使用されるため、コンポーネント名は `messageSenderClient` と指定する。」と書くが、
実装ではコンポーネント名は `messageSender.<リクエストID>.messageSenderClient` の**値**から解決されるため、
任意の名前でよい（§2 の実装表。実配置例も `defaultMessageSenderClient`・`defaultRealTimeMessagingClient`
の2種がある）。本ページからは当該アンカーを参照しないことで矛盾を回避した。

**推奨**: FW解説書は本刷新の対象外のため、本タスクでは是正しない。`#last` までに別タスクとして扱うか、
対象外として記録に留めるかをユーザーが判断する。

## 5. `#20` 以降への申し送り

1. **`reader.fwHeaderfields` は `Excel` 形式・メッセージ受信側にのみ効く。** 送信側（`SendSyncMessageParser`）は
   `getFwHeader()` が `UnsupportedOperationException` を投げ、`processDirectives` も override していないため
   フィルタが働かない。`YAML` 形式（`nablarch-testing-yaml`）には参照するコードが無い。他の処理方式の
   ページで同じ設定に触れるときは、この適用範囲を守ること
2. **第2部の処理方式ページでは、FW解説書の `:ref:` 先の記述が実装より狭い場合がある。** 参照を張る前に
   参照先の本文を読み、ページの記述と矛盾しないか確認すること（`decide` 3）
3. **`glossary.md` の意味列は、正表記だけでなく適用範囲まで確認すること。** `decide` 1 のように、
   採用根拠が数えた出典より意味列が狭い行がある
4. **`testdata_notation.rst:1244` の「キー名は固定ではなく、`reader.fwHeaderfields` の設定に合わせる」は
   `YAML` 形式の `fw_header:` の説明であり、実装と食い違う。** `YAML` 経路は `reader.fwHeaderfields` を
   参照しない（`nablarch-testing-yaml` に参照コードが0件）。同じファイルの `:1263`
   （「`fw_header:` に記載したキーは全てフレームワーク制御ヘッダとして扱われ、`reader.fwHeaderfields` で
   フィルタして取り捨てられることはない」）とも食い違う。`:1244` は設定キーを持ち出さず
   「プロジェクトのフレームワーク制御ヘッダのフィールド名に合わせる」とするのが正しい。
   `testdata_notation.rst` は user review 承認済みのページのため、本タスクでは是正せず申し送りとする
5. **`reader.fwHeaderfields` のキー名と例示値が、本ページと `testdata_notation.rst:1137` に重複している。**
   設定手順は第2部に置くのが `design.md` §3 の記載範囲であり、寄せるなら第3部側を本ページへの `:ref:` に
   置き換える。あわせて `:1137` に `Excel` 形式限定である旨が無い点も是正対象になる
6. **`RequestTestingMessagingClient` はHTTPメッセージングのページにしか記載が無いが、ウェブ・スタンドアロンの
   リクエスト単体テストからも初期化される**（`AbstractHttpRequestTestTemplate.java:316`・`TestShot.java:188`）。
   `setup/request_unit_test/web.rst`・`batch.rst` を扱うタスクでは、本ページへの導線を張るか検討すること
