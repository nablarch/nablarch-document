# page-request_unit_test_setting_db_queue

対象: `ja/development_tools/testing_framework/setup/request_unit_test/db_queue.rst`（第2部）
タスク: `#27-16`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-db-queue.md`

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |
| `nablarch-document`（旧解説書） | `2e501ad` |

## 2. 出典

**0行である。欠落ではなく設計である。**

- `mapping/mapping.csv` を `dest_page` が「リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）」の行で抽出 → 0件（`csv.DictReader` で実測）。
- `checks/task-06.md:569` が同ページを `0` / `EXPECTED_ZERO（design.md §6「導線のみ」）` と記録している。
- 旧解説書にも対応記述が無い。`git grep -inE "テーブルをキュー|キューとして|データベースをキュー|db_messaging|DatabaseTableQueue" 2e501ad -- ja/development_tools/testing_framework/` が0件。

したがって本ページは旧解説書からの移送ではなく、`design.md:384` にもとづく新規の導線ページである。

## 3. 導線のみとした根拠

`design.md:384` が、テーブルをキューとして使ったメッセージングの3ページ（`リクエスト単体テストの設定` / `リクエスト単体テスト` / `取引単体テスト`）について「章として立てる」「中身は導線のみとする」「『Nablarchバッチアプリケーションと同じ方法でテストする』旨と、Nablarchバッチアプリケーションの章への `:ref:` 参照だけを記載する」「コード例・テストデータ例は記載しない」と規定している。

これを受けて個別指示 `ntf-doc-27-db-queue.md:19-20` が、`機能概要`・`使用方法` の見出しと `.. contents::` も置かず、リード文だけで完結させると定めている。本ページは全6行（ラベル・タイトル・リード文のみ）でこれに従った。

`style.md` の S-02（第2部は「使用方法」必須、`style.md:45-46`）と S-09（`.. contents::`、`style.md:402`・`:413-415`）は、この規定により適用しない。S-09 は「L2セクションを1つも持たないページには適用しない」ため条文上も外れる。S-02 には導線のみページの除外規定が無く、条文と実物が食い違っている（→ 6節 `decide-4`）。

## 4. 実測値

| 項目 | 値 |
| --- | --- |
| L1 タイトル表示幅 | 72（`unicodedata.east_asian_width` で W/F/A=2） |
| L1 下線 `=` | 72 → `max(50, 表示幅)` に一致 |
| L2 以下の見出し | 0件 |
| `code-block` | 0件 |
| ページ先頭ラベル | `request_unit_test_setting_db_queue`（`style.md:363` と一致） |
| `:ref:` 飛び先 | `request_unit_test_setting_batch`（`setup/request_unit_test/batch.rst:1` の実物と一致） |
| リンクテキスト | 「リクエスト単体テストの設定（Nablarchバッチアプリケーション）」（`batch.rst:3` の見出しと一致） |

## 5. 判断

- **D-1 述語を「同じである」とした。** 初稿の「〜のリクエスト単体テストは、…と同じ設定を行う。」は主述がねじれていた（「行う」の目的語が「設定」で埋まっているため、テストが設定を行う主体に読める）。主題を「設定」に移し「〜のリクエスト単体テストの設定は、…と同じである。」とした。承認済みの同型導線文（`implementation/deal_unit_test/batch.rst:20`・`rest.rst:22`、`setup/deal_unit_test/http_messaging.rst:31`）がいずれも「〜と同じである。」で受けている。
- **D-2 兄弟5ページの「〜では、」形には揃えなかった。** `setup/request_unit_test/` の web:10・rest:10・http_messaging:10・mom:10・batch:10 はいずれも「何を設定するか」を述べる文であり、導線文ではない。文型が違うのは内容が違うためで、不整合ではないと判断した。
- **D-3 3ページの文型を先に決めた。** `#27-17`・`#27-18` は個別指示 `ntf-doc-27-db-queue.md:50` の型どおり「〜は、…と同じ方法で行う。」とし、本ページのみ主題を「設定」にする。述語「同じ方法で行う」は `about/index.rst:91` の既存記述と一致する。
- **D-4 `design.md:384` の「同じ方法でテストする」を「同じである」に言い換えた。** 第2部（設定）のページであり、個別指示 `ntf-doc-27-db-queue.md:42`「ページごとに主語を変える」の範囲内。

## 6. 4観点レビュー

QA / 設計 / クラフト / 検証 の4観点を別々のサブエージェントで実施した。延べ指摘16件、重複を除き10件。うち反映1件（D-1）、判断待ちへ送り5件、不採用4件。

**不採用**

- 兄弟5ページの「〜では、」形への統一（→ D-2）。
- `style.md` S-02 / S-09 への例外規定の追記。`style.md` は G2 の禁止ファイルで、この週末は変更できない（→ `decide-4`）。
- 「常駐バッチの場合」という条件が読者に伝わるよう導線ページに一言足す案。個別指示 `ntf-doc-27-db-queue.md:52`「『同じ方法で行う』以上のことを書かない」に反する（→ `decide-1`）。
- `Nablarch` と和文の間の `\ ` エスケープの統一。`style.md:13-14` が規約対象外と明記している。

## 7. 判断待ち

- **`decide-1`（必須）** 飛び先 `setup/request_unit_test/batch.rst` の設定3件のうち、テーブルをキューとして使ったメッセージングに確実に該当するのは「リクエストスレッド内ループ制御ハンドラの置き換え」（`batch.rst:15-37`）のみである。残る2件（ディレクティブのデフォルト値 `batch.rst:39-78`、`TEST_X9`・`TEST_SX9` の登録 `batch.rst:80-119`）はファイルデータ・固定長ファイル向けで、FW解説書 `ja/application_framework/application_framework/messaging/db/` にデータフォーマットの記述は無い。`batch.rst:10` 自身が「後の2つはNablarchバッチアプリケーションに固有の設定ではなく、ファイルデータや電文のテストデータを扱うテストで使用する」と断っているため直ちに誤りではないが、「設定は同じである」が過大でないかを判断する必要がある。
- **`decide-2`（必須）** `setup/request_unit_test/batch.rst:17` は、リクエストスレッド内ループ制御ハンドラの置き換えを「\ :ref:`常駐バッチ <nablarch_batch-resident_batch>`\ のリクエスト単体テスト」の設定として説明している。しかしFW解説書では、Nablarchバッチアプリケーションの使用ハンドラ一覧（`batch/nablarch_batch/architecture.rst:110-113`）にも常駐バッチの最小ハンドラ構成（同 `:283`・`:334`・`:389`）にも `request_thread_loop_handler` は無く、`loop_handler`・`dbless_loop_handler`・`process_resident_handler` が使われる。同ファイル全体で `request_thread_loop_handler` は0件。これを最小ハンドラ構成に含むのは `messaging/db/architecture.rst:49`・`:155` と `messaging/mom/architecture.rst` だけである。つまり飛び先で唯一DBキューに該当する設定は、本来DBキュー／MOM側に属する可能性がある。`batch.rst` 当該節の帰属先を判断する必要がある。
- **`decide-3`（参考）** `OneShotLoopHandler`（`nablarch-testing` `e21bf67` `src/main/java/nablarch/test/OneShotLoopHandler.java`）の `handle` は `DatabaseTableQueueReader` を名指しで分岐し、内部のオリジナルリーダに差し替える。DBキューを明示的に想定した実装だが、`batch.rst` はこれに触れていない。`decide-2` の裏付けでもある。この週末は書かない。
- **`decide-4`（推奨）** `style.md` S-02（`style.md:45-46`、第2部は「使用方法」必須）と S-09 の適用外ページ列挙（`style.md:413-415`、`index.rst` 系4ページのみ）に、`design.md:384` の導線のみ3ページの除外規定が無い。条文を機械的に適用する後続レビューがこの3ページを誤って指摘する。`style.md` は G2 の禁止ファイルのため、この週末は変更しない。
- **`decide-5`（参考）** 参照実装 `e21bf67` に、テーブルをキューとして使ったメッセージング専用のリクエスト単体テスト用クラス・コンポーネント設定は存在しない。`git grep -n "DatabaseTableQueue" e21bf67` のヒットは `OneShotLoopHandler.java` と そのテストのみ。`nablarch-testing-integration`・`nablarch-example-batch`・`nablarch-testing-converter`・`nablarch-testing-yaml`（`190cc9a`）にも参照は無い。「バッチ用の道具立てをそのまま使う」という本ページの含意は参照実装と整合する。
