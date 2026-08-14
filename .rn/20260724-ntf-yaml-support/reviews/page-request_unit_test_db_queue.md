# page-request_unit_test_db_queue

対象: `ja/development_tools/testing_framework/implementation/request_unit_test/db_queue.rst`（第3部）
タスク: `#27-17`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-db-queue.md`
姉妹ページ: `#27-16` = `reviews/page-request_unit_test_setting_db_queue.md`（`34bd9c7`）

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |
| `nablarch-document`（旧解説書） | `2e501ad` |

## 2. 出典

**0行である。欠落ではなく設計である。**

- `mapping/mapping.csv` に `dest_page` が「テーブルをキューとして使ったメッセージング」を含む行は1件も無い（`csv.DictReader` で全行走査、実測）。
- `checks/task-06.md:590` が同ページを `0` / `EXPECTED_ZERO（design.md §6「導線のみ」）` と記録している。
- 旧解説書にも対応記述が無い。`git grep -inE "テーブルをキュー|キューとして|データベースをキュー|db_messaging|DatabaseTableQueue" 2e501ad -- ja/development_tools/testing_framework/` が0件。旧 `05_UnitTestGuide/02_RequestUnitTest/` 配下の `.rst` 12本にも該当ページは無い。

## 3. 導線のみとした根拠

`design.md:384` の「導線のみ」規定と、個別指示 `ntf-doc-27-db-queue.md:19-20`（`機能概要`・`使用方法` の見出しも `.. contents::` も置かず、リード文だけで完結させる）による。本文は個別指示 `:50` の型に、実ファイルで確認したラベルを入れたものである。

`style.md` の S-02（第3部は「機能概要 → 使用方法」の順、`style.md:47-52`）と S-09（`.. contents::`、`style.md:402`・`:413-417`）は適用しない。S-09 は「複数のL2セクションを持つページ」が条件で、本ページはL2が0件のため条文上も外れる。S-02 の例外列挙は `testdata_notation.rst`・`testdata_examples.rst` の2ページのみで、導線のみ3ページが入っていない（→ 6節 `decide-5`）。

## 4. 実測値

| 項目 | 値 |
| --- | --- |
| 総行数 | 6行（ラベル・タイトル・リード文のみ） |
| L1 タイトル表示幅 | 66（`unicodedata.east_asian_width` で W/F/A=2） |
| L1 下線 `=` | 66 → `max(50, 表示幅)` に一致 |
| L2 以下の見出し | 0件 |
| `code-block` | 0件 |
| `.. contents::` | 0件 |
| ページ先頭ラベル | `request_unit_test_db_queue`（`style.md:379` と一致、`ja/` 配下で重複定義0件） |
| `:ref:` 飛び先 | `request_unit_test_batch`（`implementation/request_unit_test/batch.rst:1` の実物と一致） |
| リンクテキスト | 「リクエスト単体テスト（Nablarchバッチアプリケーション）」（`batch.rst:3` の見出しと一致） |
| `toctree` 位置 | `implementation/index.rst:18`（`:17` の `mom` の次、グループ最後）。`design.md:873` と一致 |

## 5. 判断

- **D-1 述語を「同じ方法で行う」とした。** 個別指示 `ntf-doc-27-db-queue.md:50` の型、`design.md:384` の「同じ方法でテストする」旨、第1部 `about/index.rst:91`「Nablarchバッチアプリケーションと同じ方法で行うテスト」の3つと一致する。
- **D-2 姉妹ページ `#27-16` との述語の差は意図した差である。** `setup/request_unit_test/db_queue.rst:6` は主語が「設定」（状態）のため「同じである」、本ページは主語が「テスト」（行為）のため「同じ方法で行う」。揃えるべきは述語ではなく「ラベル → タイトル → リード文1文、目次・見出しなし」という構造である。
- **D-3 `#27-18` も本ページの型に合わせる。** 「テーブルをキューとして使ったメッセージングの取引単体テストは、\ :ref:`取引単体テスト（Nablarchバッチアプリケーション） <deal_unit_test_batch>`\ と同じ方法で行う。」とする。飛び先ラベルは `implementation/deal_unit_test/batch.rst:1` の実物で確認済み。
- **D-4 第1部の「テーブル上の未処理レコードを対象に」は書き足さない。** `about/index.rst:91` の限定句は処理方式一覧表で各方式を識別させるためのもので、本ページに足すと `design.md:384` の「導線のみ」を超える。

## 6. 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施した。**本文への必須指摘は0件。** 判断待ちへ5件、不採用2件。

**不採用**

- `style.md` S-02 / S-09 への導線のみ3ページの例外追記。`style.md` は G2 の禁止ファイルで、この週末は変更できない（→ `decide-5`）。
- 導線先の条件節・分量の問題を本ページに1文足して補う案。個別指示 `ntf-doc-27-db-queue.md:52`「『同じ方法で行う』以上のことを書かない」に反する（→ `decide-1`・`decide-2`）。

## 7. 判断待ち

- **`decide-1`（必須）** 飛び先 `implementation/request_unit_test/batch.rst:183` は「テスト対象が常駐バッチの場合は、あわせてリクエストスレッド内ループ制御ハンドラの置き換えが必要である」と条件付きで書いている。しかしFW解説書では、Nablarchバッチアプリケーションの使用ハンドラ一覧（`batch/nablarch_batch/architecture.rst:110-113`）にも常駐バッチの最小ハンドラ構成（同 `:283`・`:334`・`:389`）にも `request_thread_loop_handler` は無く、同ファイル全体で0件である。これを最小ハンドラ構成に含むのは `messaging/db/architecture.rst:49`・`:155` と `messaging/mom/architecture.rst` のみで、`messaging/db/` 配下に「常駐」の語は0件である。さらに `batch/nablarch_batch/architecture.rst:29-30` は「新規開発プロジェクトでは、常駐バッチではなく、上記問題が発生しない :ref:`db_messaging` を使用することを推奨する」と、両者を別物として区別している。つまりDBキューの読者にとって必須の設定が、読者が自分とは別物と認識する「常駐バッチ」の条件節に入っており、「同じ方法で行う」で飛ばすと読み飛ばされる経路がある。この条件節の帰属先を判断する必要がある。**姉妹ページ `reviews/page-request_unit_test_setting_db_queue.md:66`（`decide-2`）と同一事象だが、あちらは第2部 `setup/request_unit_test/batch.rst:17`、こちらは第3部 `implementation/request_unit_test/batch.rst:183` で、第3部側でも独立に成立する。**
- **`decide-2`（推奨）** 飛び先 `implementation/request_unit_test/batch.rst` は、使用方法4節のうち3節に「応答不要メッセージ送信」の説明を含む（`:10`・`:20-29`・`:92-108`・`:141-150`・`:152-173`）。応答不要メッセージ送信はMOMの機能であり（`batch.rst:20` が `mom_system_messaging-async_message_send` を参照）、テーブルをキューとして使ったメッセージングには当てはまらない。「同じ方法で行う」だけを頼りに飛んだ読者が、自分に該当しない記述を切り分けることになる。導線先の分量配分を許容するか、`batch.rst:10` のリード文にこの方式を併記するかを判断する必要がある。
- **`decide-3`（参考）** 同じ骨格の導線文で動詞が割れている。本ページ `:6` は「同じ方法で行う」、`implementation/request_unit_test/http_messaging.rst:15` は「同じ方法で実施する」。`glossary.md` §6.3（`:485`）の揺れ一覧にこの対は無く、`glossary.md:589` の `実施方法` → `使用方法` はセクションタイトル限定のため、規約上はどちらも違反ではない。揃えるなら承認済みの `http_messaging.rst` 側を触ることになる。
- **`decide-4`（参考）** `decide-1` の食い違いは新解説書で作り込まれたものではなく、旧解説書から引き継がれたものである。旧 `2e501ad:ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.rst:184-190` に「常駐バッチのテスト用ハンドラ構成」節があり、`RequestThreadLoopHandler` → `OneShotLoopHandler` の置き換えを説明している。現行 `setup/request_unit_test/batch.rst:15-33` の出典元はここである。
- **`decide-5`（参考）** `style.md` S-02 の第3部セクション構成規約（`style.md:47-52`）の例外列挙は `testdata_notation.rst`・`testdata_examples.rst` の2ページのみで、`design.md:384` の導線のみ3ページが入っていない。S-09 の適用除外列挙（`style.md:413-417`）も `index.rst` 系4ページのみである。条文を機械的に適用する後続レビューがこの3ページを誤って指摘する。`style.md` は G2 の禁止ファイルのため、この週末は変更しない。**姉妹ページ `decide-4` と同一。**

**姉妹ページの記録で足りる項目（本ページでは再掲しない）**

- 参照実装 `e21bf67` にDBキュー専用のリクエスト単体テスト用クラス・設定が存在しないこと → `page-request_unit_test_setting_db_queue.md` の `decide-5`。本ページでも独立に確認した（`git grep -n "DatabaseTableQueue" e21bf67` のヒットは `OneShotLoopHandler.java` とそのテストのみ、`git grep -inE "dbqueue|db_queue|テーブルをキュー" e21bf67` は0件、`BatchRequestTestSupport` は処理方式で分岐しない）。
- `OneShotLoopHandler` が `DatabaseTableQueueReader` を名指しで分岐すること → 同 `decide-3`。

**確認済みの否定所見**

- `about/index.rst:100`「マルチスレッド機能を使うアプリケーションも、テスティングフレームワークの対象外である」はDBキュー固有の差分ではない。`multi_thread_execution_handler` はDBキュー最小構成（`messaging/db/architecture.rst:140`）にも都度起動バッチ最小構成（`batch/nablarch_batch/architecture.rst:186`）にも同じく含まれる。
- `process_stop_handler` はDBキュー最小構成（`messaging/db/architecture.rst:162`）と常駐バッチ最小構成（`batch/nablarch_batch/architecture.rst:342`）の双方に含まれ、都度起動バッチ最小構成には含まれない。これがテスト実行時の手当を要する差分になるかは**未確認**。一次資料で裏が取れていないため判断待ちには載せない。
