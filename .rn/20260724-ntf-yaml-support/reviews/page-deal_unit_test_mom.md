# page-deal_unit_test_mom — 取引単体テスト（MOMによるメッセージング）

対象ファイル: `ja/development_tools/testing_framework/implementation/deal_unit_test/mom.rst`
キュー番号: `#27-09`

## 1. 参照リポジトリ

| リポジトリ | 参照コミット | 用途 |
| --- | --- | --- |
| `nablarch-testing` | `e21bf67` | `SendSyncSupport` ・`MockMessagingContext` ・`MockMessagingProvider` ・`MessagingRequestTestSupport` の実装確認 |

本ページで参照した4クラスについて `git diff --stat e21bf67 HEAD -- <4ファイル>` を実行した。差分は0行である。

## 2. 出典行の消化

`mapping.csv` で `dest_page` が「取引単体テスト（MOMによるメッセージング）」である行は7件である。

| mapping_id | src_file | src 行 | 行数 | disposition | 反映先（mom.rst の行） |
| --- | --- | --- | --- | --- | --- |
| current-0135 | `delayed_receive.rst` | 4-7 | 4 | REFERENCE | `:15` 末尾の一文 |
| current-0136 | `delayed_send.rst` | 4-7 | 4 | REFERENCE | 反映しない（D-1） |
| current-0147 | `real.rst` | 4-36 | 33 | MOVE | `:15` `:40` `:44` `:46-48` `:50` `:52-60` |
| current-0154 | `send_sync.rst` | 6-46 | 41 | MOVE | `:17` `:19` `:21-22` `:24` `:26-27` `:29` `:31-33` `:35` |
| current-0155 | `send_sync.rst` | 50-63 | 14 | MOVE | `:68` `:72-73` |
| current-0156-b | `send_sync.rst` | 173-198 | 26 | SPLIT | `:77` `:79-80` `:82` `:84-85` |
| current-0157 | `send_sync.rst` | 224-276 | 53 | MOVE | `:89` `:91` `:93-97` `:99` `:101-109` `:111` `:113-129` |

落とした行は D-1 〜 D-4 に記録する。

## 3. 実装で確認した事実

`nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/messaging/` 配下。

| 事実 | 出典 |
| --- | --- |
| `Map` 形式のロガー名は `MESSAGING_MAP` 、`CSV` 形式のロガー名は `MESSAGING_CSV` | `SendSyncSupport.java:40,43` |
| 応答電文の読み込み単位名は `<リクエストID>/message` 、ベースパスのキーは `sendSyncTestData` | `SendSyncSupport.java:46,49,347,348` |
| キャッシュキーは `<データタイプ>_<リクエストID>` | `SendSyncSupport.java:401-403` |
| キャッシュにあり、かつファイルの最終更新日時が変わっていなければ `incrementNo()` を呼ぶ。変わっていれば作り直す | `SendSyncSupport.java:358-371` |
| `TestDataInfo` の `no` の初期値は 1 、`incrementNo()` は `no++` 。`fileCache` は `static` である | `SendSyncSupport.java:52,443,467-470` |
| **返す応答電文は `no` 列の値ではなく、読み込んだレコードの並び順で決まる**（`getRecords().get(info.no - 1)`） | `SendSyncSupport.java:288` |
| 記述件数を超えると `receive message did not exists.` の `RuntimeException` になる | `SendSyncSupport.java:282-287` |
| ログメッセージの先頭は `request id=[%s]. following message has been sent: ` ＋ 改行 | `SendSyncSupport.java:120-121` |
| `Map` 形式はタブ ＋ `message fw header = ` ／ タブ ＋ `message body      = ` | `SendSyncSupport.java:118,139-142` |
| `CSV` 形式は `message header = ` ／ `message body   = ` （出典の例の `header:` ／ `body:` とは異なる） | `SendSyncSupport.java:194,196` |
| どちらも `logDebug` で出力する（`DEBUG` レベル） | `SendSyncSupport.java:150,231` |
| `MockMessagingProvider` は `MessagingProvider` の実装であり、`createContext()` が `MockMessagingContext` を返す。3つのセッタは何もしない | `MockMessagingProvider.java:14,20-22` |
| モックアップクラスは、要求電文ヘッダに `requestId` という名前のフィールドがある前提で動作する | `MockMessagingContext.java:37,46-47` |
| `errorMode` が `timeout` なら `null` を返し、`msgException` なら `MessagingException` を送出する | `SendSyncSupport.java:290-296` |
| `MessagingRequestTestSupport` の完全修飾名は `nablarch.test.core.messaging.MessagingRequestTestSupport` | `MessagingRequestTestSupport.java:1,48` |

## 4. 実測

| 項目 | 実測値 |
| --- | --- |
| 行数 | 129 |
| 見出し内訳 | L1 1 / L2 2 / L3 4 / L4 0 |
| 下線の長さ | L1 50 / L2 50 / L3 49（すべて見出しの表示幅以上） |
| L2 見出しの下線直後の空行 | 2箇所ともあり（承認済み `batch.rst:13-15` ・`rest.rst:13-15` と同型） |
| `:ref:` | 6件。ラベルはすべて実在し、リンクテキストは飛び先の見出しと一致 |
| `:java:extdoc:` | 1件。`e21bf67` にクラスが実在 |
| `code-block` | 4件（`java` 1 / `text` 2 / `properties` 1）。本文はすべて2字下げ |
| `list-table` / grid table | 0 / 0 |
| 画像 | 4件。`implementation/deal_unit_test/images/mom/` に `git mv` 済み。移動元に残存なし、他 rst からの参照なし |
| `tip` / `important` / `note` / `warning` | 1 / 0 / 0 / 0 |
| 脚注（`.. [#`） | 0（D-2 参照） |
| 禁止語（`不具合` `バグ` `将来` `修正され`） | 0 |
| 用語集の揺れ表記 | 0（`送信処理` `受信処理` `メッセージ受信処理` `バッチ処理` `自動テストフレームワーク` `メッセージング処理` `メッセージ同期送信` を grep して0件） |
| 行末の空白・タブ | 0 |
| `verify_mapping.py` | `OK: no errors` （終了コード0） |
| Sphinx ビルド（`-E` 全ビルド） | `build succeeded, 1 warning.` 。警告は既知の `db_double_submit.rst:108: undefined label: how_to_set_token_in_request_unit_test` の1件のみで、新規警告0件 |
| `locales/ja/LC_MESSAGES/sphinx.mo` | 汚れなし |
| 親 toctree | `implementation/index.rst:23` に `deal_unit_test/mom` を登録済み |

## 5. 出典から変えた点

**D-1 `delayed_send.rst:5-6`（current-0136 の全体）を反映しなかった。**
`design.md:119` が「`delayed_send.rst:5-6` は根拠に使わない。本文とリンク先が食い違う出典であるため」と定めている。実物でも、本文が「応答不要メッセージ送信」を主語にしながらリンク先は受信側の `real.rst` である。よって応答不要メッセージ送信の記述は本文に置いていない。反映したのは受信側（current-0135）だけで、`:15` 末尾の「応答不要メッセージ受信も同じである。」がそれにあたる。

**D-2 脚注 `[#f1]` `[#f2]` を脚注として持ち込まなかった。**
`send_sync.rst:44-45` の `[#f1]` は「要求電文」「応答電文」の用語定義である。`glossary.md:273-274` が既定語として扱っており、承認済みページも定義なしで使っているため落とした。`send_sync.rst:58-61` の `[#f2]` は本ページ以外に記述が無い注意事項であるため、`:72-73` の `tip` として地の文に移した。NTF の新規ページに RST 脚注の用例は0件である。

**D-3 ログ出力例から日時とロガー名の接頭辞を落とし、`CSV` 形式のラベルを実装に合わせた。**
出典 `send_sync.rst:237,245` は `2011-10-26 13:16:10.958 MESSAGING_SEND_MAP` ／ `MESSAGING_SEND_CSV` で始まるが、実装のロガー名は `MESSAGING_MAP` ／ `MESSAGING_CSV` である（`SendSyncSupport.java:40,43`）。また接頭辞はログフォーマッタの設定に依存し、出典自身の `log.properties` 例（`writer.MESSAGING_CSV.formatter.format=$message$`）とも整合しない。よって例はメッセージ部分だけにし、`:89` に「日時やロガー名が付くかどうかは、ログの出力設定によって変わる」と添えた。あわせて出典の `header:` ／ `body:` を実装どおりの `message header = ` ／ `message body   = ` に直した（`SendSyncSupport.java:194,196`）。`design.md` §8 の「出典と実装が食い違えば実装を優先する」に従った。

**D-4 `send_sync.rst:195` のラベル定義 `.. _`send_sync_response_count_change.png`:` を落とした。**
どこからも参照されていない旧ページ内部のラベルであり、移行先に持ち込む意味がない。

**D-5 `real.rst:21-29` の Java コード例を修正した。**
出典はパッケージ宣言のセミコロンが欠け（`:23`）、クラス本体が閉じていない（`:29`）。`:54-60` では両方を補い、承認済み `batch.rst:32-41` と同じ書式に揃えた。

**D-6 「no の値で選ぶ」とは書かず「記述した順に1件ずつ返す」とした。**
出典 `send_sync.rst:179-182` は `no` のインクリメントとして説明するが、実装は `getRecords().get(info.no - 1)` であり、レコードの並び順で選ぶ（`SendSyncSupport.java:288`）。`no` は `Excel` 形式のラベル列であって `YAML` 形式には無く、承認済み `testdata_notation.rst:1156` も「対応付けは、連番の値ではなく記述した順序で行われる」と述べている。両形式を扱うページで `no` の語彙に寄せると矛盾するため、`:77` `:82` は並び順で書いた。

**D-7 適用可否の判断（`real.rst:5-10`）を「使用方法」ではなく「機能概要」に置いた。**
`mapping.csv` の current-0147 の `dest_section` は「使用方法」だが、同型の出典（`03_DealUnitTest/rest.rst:5-7`）を持つ承認済みページ `implementation/deal_unit_test/rest.rst:15-17` は機能概要に置いている。`dest_section` は節の粒度の指定であって判断文の置き場所までは縛らないと読み、型を揃えた。テストクラス・テストメソッド・テストデータの手順自体は「使用方法」に置いている。

**D-8 送信側（ウェブアプリケーション）のテストクラス・テストメソッドは書かず、`deal_unit_test_web` へ送った。**
出典4範囲（`send_sync.rst:6-46` `50-63` `173-198` `224-276`）にテストクラス・テストメソッドの記述は無い。テスト対象がウェブアプリケーションそのものであり（`design.md:125`）、差し替わるのはメッセージングプロバイダのコンポーネントだけである（`MockMessagingProvider.java:14`、承認済み `setup/deal_unit_test/mom.rst:21,29`）ことから、ウェブアプリケーションの取引単体テストと同じ書き方になると判断した。`:40` と `:62` で `deal_unit_test_web` に送っている。`#27-11` への申し送りは判断待ち decide-4 に記載する。

**D-9 実装上の前提を1文だけ追記した。**
`:70` の「モックアップクラスは、要求電文のフレームワーク制御ヘッダに ``requestId`` という名前のフィールドがあることを前提に動作する。」は出典に無い。`MockMessagingContext.java:37`（Javadoc）と `:46-47`（`get("requestId")`）が根拠である。フレームワーク制御ヘッダのフィールド名はプロジェクトで変更しうるため（`testdata_notation.rst:1170`）、`design.md` §8 の「出典が欠く実装上必須の設定は追記してよい」に従って残した。

**D-10 用語を用語集の正表記に統一した。**
出典の「同期応答メッセージ送信処理」「同期応答メッセージ受信処理」「応答不要メッセージ受信処理」「メッセージ受信処理」「バッチ処理」はいずれも `glossary.md:134,155,156,157` が揺れ表記としている。正表記（「同期応答メッセージ送信」「同期応答メッセージ受信」「応答不要メッセージ受信」「Nablarchバッチアプリケーション」）に置き換え、「メッセージ受信処理」は応答不要受信と区別できないため「メッセージを受信するアプリケーション」と言い換えた。

**D-11 読み込み単位の説明を承認済みページに合わせた。**
出典 `send_sync.rst:54-55` は「Excelファイル」の名前だけを述べる。`glossary.md:241` は読み込み単位を「Excel 形式では1シート、YAML 形式では1ファイル」と定義しており、このケースでは `message` が固定名である（`testdata_notation.rst:1154,1251`）。`:68` はファイル／ディレクトリの名前と読み込み単位の名前を分けて書いた。

**D-12 モックアップクラスの適用範囲を `.. important::` で明示した（`:37-39`）。**
出典に記述が無い。`nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/messaging/MockMessagingContext.java` を確認した結果、`receiveMessage(String, String, long)` は `throw new UnsupportedOperationException("this method was unsupported.")`、`close()` は空実装、`send(SendingMessage)` は要求電文をログに出力して固定値 `"messageId"` を返すだけである（`sendMessage` は `send` へ委譲）。`send`・`sendMessage` は `throws UnsupportedOperationException` を宣言しているが**実際には投げない**ため、「投げる」とは書いていない。同クラスは `@Published` を持たないため `:java:extdoc:` では参照せず、メソッド名を ``literal`` で書いた（§2-18）。

**D-13 ウェブアプリケーションのテストクラスの作り方に関する1文を落とした（旧 `:17` 付近）。**
「同期応答メッセージ送信を伴うウェブアプリケーションを対象とする場合、テストクラスの作り方はウェブアプリケーションの取引単体テストと同じである。」は、`:44` の「同期応答メッセージ送信を伴うウェブアプリケーションを対象とする場合は `取引単体テスト（ウェブアプリケーション）` と同じである」と重複していた（§2-12）。

**D-14 リクエスト ID の tip を `:ref:` に置き換えた（`:74`）。**
`implementation/request_unit_test/mom.rst:39-40` の tip と逐語同一であったため、記述量の少ない本ページから送る形にした（`design.md:522`「承認済みページが同じ事実を持つ場合は `:ref:`」）。飛び先は今回新設した節ラベル `request_unit_test_mom-request_id` である（§2-23・§2-24）。

## 6. 4観点レビュー

QA・設計・クラフト・検証の4観点を、それぞれ別のサブエージェントで実施した。

### 採った是正（14件）

| # | 観点 | 内容 |
| --- | --- | --- |
| 1 | QA | 「`no` の値で選ぶ」を「記述した順に1件ずつ返す」に改めた（D-6） |
| 2 | QA | 「本番用のメッセージング機能と同じ名前で登録」を「本番用のメッセージングプロバイダと同じコンポーネント名で登録」に改めた（`MockMessagingProvider.java:14`、`setup/deal_unit_test/mom.rst:29`） |
| 3 | QA | `Map` 形式のログ例の行頭がタブであることを `:91` に明記した |
| 4 | QA | 要求電文ヘッダの `requestId` 前提を追記した（D-9） |
| 5 | クラフト | 用語の揺れ表記を正表記に統一した（D-10） |
| 6 | クラフト / 設計 | 読み込み単位の説明を修正した（D-11） |
| 7 | クラフト / 設計 | 適用可否の判断を「機能概要」に移した（D-7） |
| 8 | クラフト | リード文を「何ができるか」を述べる形に書き直し、機能概要の1文目との重複を解消した |
| 9 | クラフト / 設計 | 「使用方法」の導入文に参照先の場合分けを集約し、配下のL3を名指しした（`batch.rst:20` と同型） |
| 10 | クラフト | 箇条書きの文末に「。」を付け、クラス名を ``<取引ID>Test`` のコードリテラルにした（`batch.rst:26-27` と同型）。あわせて継承条件を箇条書きの3つ目に移した |
| 11 | クラフト | 機能概要の3つ目の項目の主語をモックアップクラスに揃えた（「障害系のテストを行う」→「障害を発生させる」） |
| 12 | クラフト | 「〜する必要がないため／〜行うことなく／〜実施できる」の打消しの重複を解消した |
| 13 | クラフト | ログ出力例の予告文の重複を解消した |
| 14 | クラフト / 設計 | L2 見出しの下線直後に空行を入れた |

### 採らなかった指摘（2件）

| # | 観点 | 指摘 | 採らなかった理由 |
| --- | --- | --- | --- |
| 1 | クラフト | 「テストを実行する」の節名を「複数回の同期送信に応答電文を対応付ける」に変える | `design.md:281-296` が第3部の節名を「テストクラスを作成する／テストメソッドを作成する／テストデータを作成する／テストを実行する／テスト結果を確認する」と定めている。節名は型に従い、代わりに `:77` の冒頭を「その回数分の応答電文をテストデータに記述する」という読者の作業から書き起こして、節名と中身のずれを解消した |
| 2 | 設計 | `:68` の「応答電文のフォーマットとデータを定義する。要求電文については、フォーマットのみ定義する」が `testdata_notation.rst:1251` と同じ事実を述べている | 出典行は別（`send_sync.rst:51-52` と current-0156-a）で G12 には触れない。ここはテストデータに何を用意するかという手順の起点であり、削ると読者が記法ページへ移る動機を失う。記法の詳細は `:68` 末尾の `:ref:` に送っている |

## 7. 判断待ち

**decide-1 `YAML` 形式でのテストデータ再読み込みが働くかどうか（未確認）。**
`:82` は「テストデータのタイムスタンプが更新されると、モックアップクラスはテストデータを読み込み直し、次に返す応答電文を1件目に戻す」と書いた。これは出典 `send_sync.rst:176-177,187` のとおりである。ただし実装は `filePathSetting.getFileIfExists(sendSyncTestData, requestId)` で得た `File` の `lastModified()` を比較しており（`SendSyncSupport.java:348,361`）、`YAML` 形式では `fileExtensions` に `sendSyncTestData` を設定してはならないため（承認済み `setup/common.rst:216`）、この `File` はリクエストIDと同じ名前の**ディレクトリ**になると読める。ディレクトリの最終更新日時は、配下のファイルを上書き編集しても変わらないことをこの環境で実測した。したがって `YAML` 形式では再読み込みが働かない可能性がある。
`FilePathSetting` の実装は `nablarch-core` にあり、その原本はルール §1-9 の作業ディレクトリの外にあるため確認していない。**本体の不具合が疑われるため本文には書かず（作業指示 §69）、ここに上げる。** 判定は次のいずれかになる。(a) 本文はこのままとし、`nablarch-testing` 側に確認を上げる。(b) 本文を `Excel` 形式に限定する。

**decide-2 `:77` の「（図は `Excel` 形式の例である）」相当の断り書き。**
出典の画像は `Excel` のものしかなく、`YAML` の図は作れない。`style.md` S-10 の4規約はこの書き方を規定しておらず、NTF 内に前例が0件である。今回は `:77` の文中で「応答電文を2件記述した場合の例を `Excel` 形式で示す」と述べる形にした。この扱いでよいか。

**decide-3 「テストを実行する」節の名前。**
`design.md:281-296` の型に従って節名を残したが、中身は実行手順ではなく実行時の動作（応答電文の並び順と再読み込み）である。§6 の「採らなかった指摘1」を参照。型を優先する判断でよいか。

**decide-4 `#27-11`（取引単体テスト（ウェブアプリケーション））への申し送り。**
D-8 のとおり、同期応答メッセージ送信を伴うウェブアプリケーションのテストクラス・テストメソッドの説明は `deal_unit_test_web` に委ねている。`#27-11` の執筆時に、メッセージングのモックアップを使う場合も同じ書き方でよい旨が読み取れる状態になっているかを確認する必要がある。

**decide-5 `MockMessagingContext` の未反映の実装事実。**
`receiveMessage` は `UnsupportedOperationException` を送出し（`MockMessagingContext.java:148-151`）、`close()` は何もしない（`:120-123`）。また `send`（応答不要メッセージ送信）はログを出してメッセージIDを返すだけである。出典にこれらの記述は無く、`mapping.csv` の割当にも該当行が無いため本文に書いていない。書く必要があるか。

**decide-6 移行元 `_images` ディレクトリの後始末。**
`guide/development_guide/05_UnitTestGuide/03_DealUnitTest/_images/` には、本ページで移した4枚を除いて9枚が残っている。いずれも ja 側の rst からの参照が0件である。第3部の移行が全部終わった段階で、ディレクトリごと削除するかを判定する。
