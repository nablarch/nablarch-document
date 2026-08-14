# page-request_unit_test_http_messaging

`#27-15` リクエスト単体テスト（HTTPメッセージング）
（`ja/development_tools/testing_framework/implementation/request_unit_test/http_messaging.rst`、ラベル `request_unit_test_http_messaging`）

個別作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-small-3rd.md` §5（`:150-199`）

## 1. 参照リポジトリ

| リポジトリ | コミット |
|---|---|
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |

旧解説書は `2e501ad` で削除済みのため、出典は `git show 2e501ad:<path>` で読んだ。

`nablarch-fw-messaging` は当環境に存在しない。HTTPメッセージ受信の実行経路が実際にキューを経由するかは**未確認**。本ページの記述はこの点に依存しない範囲で書いた。

## 2. 出典

### 2-1. 反映した行

| mapping_id | 出典 | disposition | 反映先 |
|---|---|---|---|
| `current-0064` | `2e501ad:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:4-8` | REFERENCE | 機能概要（`:15` 前半） |
| `current-0069` | `2e501ad:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:6-15` | REFERENCE | 機能概要（`:15` 後半）／使用方法 > 用語を読み替える（`:36-37`） |
| `input-0027` | `.rn/20260724-ntf-yaml-support/input/ntf-doc-terms.md:399-411` | MERGE | 使用方法 > 用語を読み替える（読み替え表） |

`mapping.csv` を `csv.DictReader` で全行走査し、`dest_page` が「リクエスト単体テスト（HTTPメッセージング）」の行はこの3件だけであることを確認した。

参照先ラベルの実体（`2e501ad` で実測）:

- `real_request_test` = `02_RequestUnitTest/real.rst:1`。タイトルは `:4`「リクエスト単体テストの実施方法(同期応答メッセージ受信処理)」
- `message_sendSyncMessage_test` = `02_RequestUnitTest/send_sync.rst:1`。タイトルは `:4`「リクエスト単体テストの実施方法(同期応答メッセージ送信処理)」

どちらも `#27-13` リクエスト単体テスト（MOMによるメッセージング）へ統合済み。

### 2-2. 意図的に落としたもの

| 内容 | 理由 |
|---|---|
| `current-0069` の範囲末尾 `.. _`http_send_sync_request_write_test_data`:`（`http_send_sync.rst:14`） | 次節のアンカーであって本文ではない。個別指示 `ntf-doc-27-small-3rd.md:183` の指定どおり本文に持ち込まない |
| `input-0027` の `MockMessagingContext` → `MockMessagingClient` の行（`ntf-doc-terms.md:407`） | D-1 を参照 |

## 3. 出典より実装を優先した点

| 事実 | 出典の記述 | 実装（`e21bf67`） | ページの記述 |
|---|---|---|---|
| 受信側の対応先 | `http_real.rst:5` は `real_request_test`（＝同期応答メッセージ受信処理）を指す | 受信側のスーパクラスは `MessagingRequestTestSupport`（同期応答メッセージ受信）と `MessagingReceiveTestSupport`（応答不要メッセージ受信、`MessagingReceiveTestSupport.java:13` で前者を継承）の2つ。HTTP専用のものはない | `:15`「同期応答メッセージ受信と同じ方法で実施する」。参照先 `mom.rst:10` の総称「メッセージ受信」は応答不要メッセージ受信を含むため使わない |
| 読み替えの適用範囲 | `http_send_sync.rst:9` は「送信キュー」「受信キュー」→「通信先」を `message_sendSyncMessage_test`（送信側）に対してのみ述べる | `MessagingRequestTestSupport.java:185-197` は受信側テストで `TEST.REQUEST` へ `send`、`TEST.RESPONSE` から `receiveSync` しており、受信側は実際にキューを使う | `:27`「同期応答メッセージ送信の説明で使う用語は」と範囲を限定。`mom.rst:190`（メッセージ受信の説明「要求電文が受信キューに PUT される」）には読み替えが及ばない |
| `RequestTestingMessagingClient` の内部構造 | 出典に記述なし | `RequestTestingMessagingClient.java` はクラス宣言が `:53` の1件のみで内部クラスを持たない。`RequestTestingMessagingProvider.java:60` は `public static class RequestTestingMessagingContext extends MessagingContext` を持つ | `:42` に1文を追記。読み替えを `mom.rst:192`（「同クラスの内部クラスである `RequestTestingMessagingContext` に委譲される」）へ当てると実装に無い記述になるため |

## 4. 実測値

- 見出し下線: L1 `:4` `=` 50（表示幅42）／L2 `:13`・`:20` `-` 50／L3 `:25` `~` 49（表示幅16）
- `:ref:` 5件。飛び先とリンク文字列の一致を実ファイルで確認
  - `request_unit_test_mom` → `implementation/request_unit_test/mom.rst:1`、見出し `:3`
  - `testdata_notation-test_shots` → `implementation/testdata_notation.rst:350`、見出し `:352`
  - `testdata_notation-messaging_data` → `implementation/testdata_notation.rst:1150`、見出し `:1152`
  - `request_unit_test_setting_http_messaging` → `setup/request_unit_test/http_messaging.rst:1`、見出し `:3`
- `.. code-block::` 0件、`.. image::` 0件、`.. note::` 0件、グリッドテーブル0件、`list-table` 1件
- 全42行

## 5. 判断

### D-1 `MockMessagingContext` → `MockMessagingClient` の行を読み替え表に入れない

`input-0027`（`ntf-doc-terms.md:407`）にある行だが、本ページには反映しない。

根拠（`e21bf67` および実ファイルで実測）:

- `MockMessagingContext.java:14-24` の Javadoc は「本クラスは、画面オンライン処理方式の**取引単体テスト**のように、VMを立ち上げたままで連続してテストを行う場面での使用を想定している」。リクエスト単体テスト用ではない
- `MockMessagingContext` を生成するのは `MockMessagingProvider.java:20-22` のみ。リクエスト単体テストの経路（`TestShot.java:188-190`、`AbstractHttpRequestTestTemplate.java:316-321`）は `RequestTestingMessagingContext` と `RequestTestingMessagingClient` を初期化しており、`MockMessagingContext` を呼ばない。`TestShot.java:187` と `AbstractHttpRequestTestTemplate.java:281,315` に `MockMessagingContext` の名が出るがコメント文中のみ
- 読み替え先である `implementation/request_unit_test/mom.rst` に `MockMessagingContext` は0件。登場しない用語は読み替えられない
- 同じ帰属の誤りは `#27-13` で是正済み（`reviews/page-request_unit_test_mom.md` D-4）

戻す場合: `:38-39`（`RequestTestingMessagingProvider` の行）の前に次の2行を挿入する。

```
  * - ``MockMessagingContext``
    - ``MockMessagingClient``
```

### D-2 「送信キュー」「受信キュー」を1行にまとめ、適用範囲を同期応答メッセージ送信に限定した

`current-0069` は「送信キュー」「受信キュー」をいずれも「通信先」に読み替えるとしており、対応先が同じであるため表では1行にまとめた。適用範囲を送信側に限定した根拠は §3 のとおり。兄弟ページ `implementation/deal_unit_test/http_messaging.rst:17` も送信の文脈に限定した書き方である。

### D-3 テストデータへの導線をページ先頭ではなく節アンカーに張った

`testdata_notation` は1300行を超えるため、ページ先頭に張ると読者が HTTP 固有の箇所を自力で探すことになる。HTTP 固有の差分は `testdata_notation.rst:557`（HTTPメッセージ受信の `diConfig`・`requestPath`・`userId`）と `:444`・`:455`（`expectedMessageByClient`・`responseMessageByClient`）にあり、それぞれ `testdata_notation-test_shots`（`:350`）と `testdata_notation-messaging_data`（`:1150`）の配下である。兄弟ページ `implementation/deal_unit_test/http_messaging.rst:26` も節アンカーに張っている。

### D-4 `current-0069` を `dest_section` の指定（機能概要）と使用方法の両方に振り分けた

`mapping.csv` の `current-0069` は `dest_section=機能概要` だが、うち「送信キュー」「受信キュー」→「通信先」の読み替えは使用方法 > 用語を読み替える に置いた。個別作業指示 `ntf-doc-27-small-3rd.md:179`「「送信キュー」「受信キュー」→「通信先」の読み替えも同じ節に入れる」の明示的な指定による。参照文（実施方法は MOM を参照する旨）は指定どおり機能概要に置いた。

### D-5 L3 見出しは「用語を読み替える」のままとした

見出しだけで読み替えの相手が分かるよう「MOMによるメッセージングの用語を読み替える」にする案があったが、個別作業指示 `ntf-doc-27-small-3rd.md:170-175` のセクション構成が「用語を読み替える」で固定されており、ゲートS2が §5 の構成との一致を求めるため変更しない。代わりに表の前に導入文（`:27`）を置き、読み替えの相手と範囲を示した。

### D-6 コード例・テストデータ例は0件

個別作業指示 `ntf-doc-27-small-3rd.md:181`「このページに手順・コード例・テストデータ例を書かない」およびゲートS6による。

### D-7 第3部のアウトライン適用（機能概要／使用方法の2セクション構成）

`#27-07` 取引単体テスト（RESTfulウェブサービス）の記録（`reviews/page-deal_unit_test_rest.md`）に1回書いた判断に従う。個別作業指示 `ntf-doc-27-small-3rd.md` §1-1 の指定どおり。

## 6. 4観点レビュー

QA・設計・クラフト・検証の4観点を、それぞれ別のサブエージェントで実施した。指摘は延べ29件（QA 7・設計 8・クラフト 10・検証 4）。重複を除くと13件で、反映8件・反映しなかったもの5件。

### 反映したもの（8件）

1. `:15` の「メッセージ受信」を「同期応答メッセージ受信」に限定（QA・クラフト・検証の3観点が一致）。`mom.rst:10` の総称は応答不要メッセージ受信を含み、出典 `real_request_test` の範囲より広い
2. 読み替え表から `MockMessagingContext` の行を削除（QA・設計・クラフト・検証の4観点が一致）。D-1
3. 読み替えの適用範囲を同期応答メッセージ送信の説明に限定（QA・設計・検証）。`mom.rst:190` に当てると成り立たない
4. `RequestTestingMessagingClient` が内部クラスを持たない旨の1文を表の後に追加（QA・設計）。`mom.rst:192` の読み替え結果が実装と食い違うため
5. `list-table` に `:widths: 50,50` を追加（クラフト）。`style.md:257-258` の S-07 が指定しており、NTF配下の `list-table` で `:widths:` が無いのは本件だけだった
6. 「送信キュー」「受信キュー」の2行を1行に統合（QA・クラフト）。D-2
7. テストデータへの導線を節アンカーに変更（設計）。D-3
8. L3 の直下に導入文を追加（設計）。表だけで始まると節単独では文脈が読めない

### 反映しなかったもの（5件）

1. L3 見出しを「MOMによるメッセージングの用語を読み替える」に変更（設計）→ D-5
2. 読み替え表を機能概要へ移す（クラフト）→ 個別作業指示 `ntf-doc-27-small-3rd.md:170-175` が使用方法配下と定めている
3. 読み替え表に「同期応答メッセージ受信 → HTTPメッセージ受信」の行を追加（クラフト）→ 出典（`input-0027`・`current-0069`）は送信側の読み替えのみを述べており、受信側の対応関係は `:15` の地の文で示している
4. `errorMode:timeout` で送出される例外クラスの違い（`RequestTestingMessagingProvider.java:161` の `MessageSendSyncTimeoutException` と `RequestTestingMessagingClient.java:150` の `HttpMessagingTimeoutException`）に触れる（検証）→ 「記述方法」の差ではなく挙動の差であり、`testdata_notation.rst:1240` が両者の違いを説明している
5. `\ ` エスケープを `MOM` と `HTTP` で揃える（クラフト）→ `style.md:13-14` が対象外としている。兄弟ページも同じ扱い

## 7. 判断待ち

1. **`input-0027` の1行を落としたことを `mapping.csv` に反映するか。** D-1 のとおり `MockMessagingContext` の行は本ページに書かなかったが、`mapping.csv` の `input-0027` は MERGE のままである。行単位の部分不採用を `mapping.csv` に表す欄がないため、この記録に留めている。
2. **`mapping.csv` の `current-0069` の `dest_section` を `使用方法` に更新するか。** D-4 のとおり個別作業指示が使用方法への配置を明示しているが、`mapping.csv` は `機能概要` のままである。
3. **第2部 `setup/request_unit_test/http_messaging.rst` から本ページへの逆方向の導線を張るか。** 第2部6ページのうち逆方向リンクを持つのは `setup/request_unit_test/web.rst:204` の1件のみで、本ページ固有の欠落ではない。第2部全体の方針として決めるべき事項。
4. **HTTPメッセージ受信の実行経路が実際にキューを経由するかは未確認。** `nablarch-fw-messaging` が当環境にないため追えない。本ページの記述はこの点に依存しない。
