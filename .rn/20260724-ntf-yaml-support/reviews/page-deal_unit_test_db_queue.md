# page-deal_unit_test_db_queue

対象: `ja/development_tools/testing_framework/implementation/deal_unit_test/db_queue.rst`（第3部）
タスク: `#27-18`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-db-queue.md`
姉妹ページ: `#27-16` = `reviews/page-request_unit_test_setting_db_queue.md`（`34bd9c7`）、`#27-17` = `reviews/page-request_unit_test_db_queue.md`（`c05baa4`）

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |
| `nablarch-document`（旧解説書） | `2e501ad` |

## 2. 出典

**0行である。欠落ではなく設計である。**

- `mapping/mapping.csv` に `dest_page` が「テーブルをキューとして使ったメッセージング」を含む行は1件も無い（`csv.DictReader` で全行走査、実測）。
- `checks/task-06.md:596` が同ページを `0` / `EXPECTED_ZERO（design.md §6「導線のみ」、未処理2の対象外）` と記録している。同 `:356` にも同じ記録がある。
- 旧解説書にも対応記述が無い。旧 `2e501ad:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/` 配下の `.rst` は8本で、この処理方式の取引単体テストを扱うページは無い。

## 3. 導線のみとした根拠

`design.md:384` の「導線のみ」規定と、個別指示 `ntf-doc-27-db-queue.md:19-20`（`機能概要`・`使用方法` の見出しも `.. contents::` も置かず、リード文だけで完結させる）による。本文は個別指示 `:50` の型に、実ファイルで確認したラベルを入れたものである。

`style.md` の S-02（第3部は「機能概要 → 使用方法」の順、`style.md:47-52`）と S-09（`.. contents::`、`style.md:402`・`:413-417`）は適用しない。S-09 は「複数のL2セクションを持つページ」が条件で、本ページはL2が0件のため条文上も外れる。

## 4. 実測値

| 項目 | 値 |
| --- | --- |
| 総行数 | 6行（ラベル・タイトル・リード文のみ） |
| L1 タイトル表示幅 | 60（`unicodedata.east_asian_width` で W/F/A=2） |
| L1 下線 `=` | 60 → `max(50, 表示幅)` に一致 |
| L2 以下の見出し | 0件 |
| `code-block` | 0件 |
| `.. contents::` | 0件 |
| ページ先頭ラベル | `deal_unit_test_db_queue`（`style.md:385` と一致、`ja/` 配下で重複定義0件） |
| `:ref:` 飛び先 | `deal_unit_test_batch`（`implementation/deal_unit_test/batch.rst:1` の実物と一致） |
| リンクテキスト | 「取引単体テスト（Nablarchバッチアプリケーション）」（`batch.rst:3` の見出しと一致） |
| `toctree` 位置 | `implementation/index.rst:24`（`:23` の `deal_unit_test/mom` の次、グループ最後）。`design.md:880` と一致 |
| `setup/deal_unit_test/db_queue.rst` | 未作成（`setup/deal_unit_test/` は `http_messaging.rst`・`mom.rst`・`rest.rst` の3本のみ。`design.md:386`・`:891` と一致） |

## 5. 判断

- **D-1 述語を「同じ方法で行う」とした。** `#27-17` の D-3 で先に決めた型（`reviews/page-request_unit_test_db_queue.md:49`）に従った。主語が「テスト」（行為）のため「同じ方法で行う」で受ける。個別指示 `ntf-doc-27-db-queue.md:50` の型、`design.md:384` の「同じ方法でテストする」旨と一致する。
- **D-2 3ページで揃えたのは構造であり述語ではない。** `#27-16` のみ主語が「設定」（状態）で「同じである」、`#27-17`・本ページは「同じ方法で行う」。揃えるべきは「ラベル → タイトル → リード文1文、目次・見出しなし」という構造である（`#27-17` D-2 と同じ）。
- **D-3 姉妹ページ `deal_unit_test/rest.rst:15`・`mom.rst:15` の留保は書き足さない。** 両ページは「1リクエストが1取引に対応する場合は取引単体テストを実施する必要はない」旨の留保を置いているが、本ページに同種の留保を足すことは個別指示 `ntf-doc-27-db-queue.md:52`「『同じ方法で行う』以上のことを書かない」に反する（→ 7節 `decide-1`）。
- **D-4 リクエストスレッド内ループ制御ハンドラの置き換えには触れない。** 同じく `ntf-doc-27-db-queue.md:52` による（→ 7節 `decide-2`）。

## 6. 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施した。**本文への必須指摘は0件。** 判断待ちへ4件、不採用2件。

**不採用**

- 姉妹ページに倣って「1リクエストが1取引に対応する場合は不要」旨の留保を1文足す案（→ D-3・`decide-1`）。
- ハンドラ置き換えが3ホップ先にあることを本ページで補う案（→ D-4・`decide-2`）。

いずれも個別指示 `ntf-doc-27-db-queue.md:52` に反するため採らない。

## 7. 判断待ち

- **`decide-1`（必須）** 飛び先 `implementation/deal_unit_test/batch.rst:10`・`:15` は「1つの取引を構成する複数のバッチ処理を1つのテストメソッドの中で順に動かす」「バッチアプリケーションでは、1つの取引が複数のバッチ処理に分かれることが多い」を前提に組み立てている。しかしFW解説書 `ja/application_framework/application_framework/messaging/db/` 配下に「取引」の語は0件で（実測）、複数リクエストで1取引が成立する構成の記述が無い。姉妹の `implementation/deal_unit_test/rest.rst:15`「RESTfulウェブサービスでは、取引が1つのリクエストで完結することがほとんどである。このように1リクエストが1取引に対応する場合は、取引単体テストを実施する必要はない。」と `mom.rst:15`「同期応答メッセージ受信では、取引が1つのメッセージで完結することがほとんどである。…複数のメッセージによって1つの取引が成立する場合は、リクエストごとのテストを1つのテストメソッドの中で連続して実行することで取引単体テストを実施できる。」は、この留保を明示している。本ページには留保が無い。テーブルをキューとして使ったメッセージングで複数リクエストが1取引を構成する形が成立するか否かは、FW解説書に肯定・否定いずれの記述も無く**未確認**である。留保を置くか、`batch.rst` の前提が本方式にも及ぶことを確認するかを判断する必要がある。
- **`decide-2`（必須）** テーブルをキューとして使ったメッセージングの最小ハンドラ構成には `request_thread_loop_handler` が含まれる（`messaging/db/architecture.rst:49`・`:155`）ため、テストにあたっては `OneShotLoopHandler` への置き換えが必須である。しかし `implementation/deal_unit_test/batch.rst` は「常駐」「OneShotLoop」いずれも0件で触れておらず、この情報は `deal_unit_test/batch.rst:20` →（`implementation/request_unit_test/batch.rst`）`:183` →（`setup/request_unit_test/batch.rst`）`:15-33` と**3ホップ**先にある。しかも `request_unit_test/batch.rst:183` は「テスト対象が常駐バッチの場合は」という条件節の中に置いており、`messaging/db/` 配下に「常駐」の語は0件、`batch/nablarch_batch/architecture.rst:29-30` は「新規開発プロジェクトでは、常駐バッチではなく、上記問題が発生しない :ref:`db_messaging` を使用することを推奨する」と両者を別物として区別している。**姉妹ページ `reviews/page-request_unit_test_db_queue.md:63`（`decide-1`）と同一事象だが、本ページはホップが1つ多い分、独立に成立する。**
- **`decide-3`（推奨）** 飛び先 `implementation/deal_unit_test/batch.rst:95-487`（ページの約8割）の記述例6件はすべてファイル入出力（`setUpFile`・`expectedFile`）を題材にしている。テーブルをキューとして使ったメッセージングの入力は `SqlRow` である（`getting_started/table_queue.rst:99-100`）。`setUpFile`・`expectedFile` は `nablarch-testing` `e21bf67` `BatchRequestTestSupport.java:130-132` で任意カラム扱いのため、記述例が該当しないこと自体は誤りではないが、「同じ方法で行う」で飛んだ読者が自分に該当する記述例を持たないことになる。
- **`decide-4`（推奨）** 第1部 `about/index.rst:77` は「取引単体テストの実行方法は、対象とする処理方式によって異なる。ウェブアプリケーションでは…RESTfulウェブサービスとNablarchバッチアプリケーションでは…」と述べ、テーブルをキューとして使ったメッセージング（およびHTTPメッセージング・MOM）を挙げていない。ただし `design.md:35` が第1部「テストの種類」に求めているのは**リクエスト単体テスト**が対象とする処理方式ごとの内訳（`about/index.rst:81`「リクエスト単体テストは、対象とする処理方式によって、次の6つに分かれる」）であって取引単体テストの内訳ではないため、設計違反ではない。本ページ固有ではなく `deal_unit_test/mom.rst`・`http_messaging.rst` にも同じく効く。

**姉妹ページの記録で足りる項目（本ページでは再掲しない）**

- `style.md` S-02（`:47-52`）・S-09（`:413-417`）の例外列挙に導線のみ3ページが無いこと → `page-request_unit_test_setting_db_queue.md` の `decide-4`、`page-request_unit_test_db_queue.md` の `decide-5`。
- 同型の導線文で動詞が割れていること（本ページ `:6`「同じ方法で行う」対 `implementation/request_unit_test/http_messaging.rst:15`「同じ方法で実施する」）→ `page-request_unit_test_db_queue.md` の `decide-3`。
- 参照実装 `e21bf67`・`190cc9a` にこの処理方式専用の取引単体テスト用クラス・コンポーネント設定が存在しないこと → `page-request_unit_test_setting_db_queue.md` の `decide-5`。本ページでも独立に確認した（`BatchRequestTestSupport` は処理方式で分岐しない）。
