# `#12` 作業指示: `:ref:` ラベル命名規則の確定（`style.md` S-08 改訂）

対象ブランチ: `lovaizu/nablarch-document` の `work`（`#11` 承認後の HEAD の続き）

ページを作らないタスクである。`style.md` S-08 を改訂し、残り30ページ分のページ先頭ラベルを先に確定する。`ja/` 配下の `.rst` は1行も変更しない。

## なぜ先にやるか

Sphinx のラベルはプロジェクト大域である。`style.md` S-08 は「ページ先頭のラベルはページIDそのもの」と定めているが、これをファイル名の語幹と解すると、残りのページで衝突する。

**すでに現実の衝突が1件ある。** `http_messaging` は `ja/application_framework/application_framework/web_service/http_messaging/index.rst:1` が定義済みである（レビュー役が `ja/` 全体の959ラベルを機械抽出して実測）。`setup/request_unit_test/http_messaging.rst` に語幹をそのまま使うと、この既存ラベルと衝突する。

NTF解説書の内部でも語幹が重複する。

| 語幹 | 同じ語幹を持つページ数 |
|---|---|
| `rest` / `http_messaging` / `mom` | 4（第2部の設定2種＋第3部の実装2種） |
| `web` / `batch` / `db_queue` | 3 |

**規則を決めないと、21ページで同じ判断を繰り返し、しかも衝突に気づけない。** `ja/conf.py:103` が `keep_warnings = True` のため、重複ラベルは `#last` まで表面化しない。

## STEP 1 — `style.md` S-08 を改訂する

現行の規約文（`mapping/style.md` S-08）は次のとおり。

> ページ先頭のラベルはページIDそのもの（英語のスネークケース）を使う（例: `exclusive_control`）。ページ内の個別セクションのラベルは `<ページID>-<セクションの内容を表す英語スネークケース>` の形式にする。

次の趣旨に改める。**根拠（FW解説書の file:line）は現行のものをそのまま残すこと。**

- ページ先頭のラベルは、そのページを `ja/` 全体で一意に識別できる英語スネークケースとする。**ファイル名の語幹をそのまま使わない。** ディレクトリで区別されているだけの語幹（`web`・`rest`・`mom` など）は、ラベルとしては一意にならない
- NTF解説書では、テスト種別と処理方式を並べた名前を用いる（STEP 2 の一覧）
- ページ内のセクションラベルは `<ページ先頭ラベル>-<セクションの内容を表す英語スネークケース>` の形式とする（現行のまま）
- 新しいラベルを定義する前に、`ja/` 全体に同名のラベルが無いことを `grep` で確認する

**改訂は S-08 のみとする。** 他の観点（S-01〜S-07・S-09〜S-11）には手を入れない。

## STEP 2 — 30ページのラベルを確定して記録する

下表を `mapping/style.md` の S-08 にそのまま載せる。以降のページ作成タスクは、この表からラベルを引く。

レビュー役が `ja/` 全体の既存959ラベルと突き合わせ、下表26件に衝突が0件であることを実測済みである。

### 作成済み（変更しない）

いずれも `ja/` 全体で一意であり衝突していない。**改名しない。** 改名すると承認済みページ内の `:ref:` を書き換えることになり、`#8`〜`#11` の成果に手を入れることになる。

| ページ | ラベル |
|---|---|
| テスティングフレームワークとは | `testing_framework_about` |
| 共通設定 | `testing_framework_common` |
| テストデータの書き方 | `testdata_notation` |
| テストデータの記載例 | `testdata_examples` |
| JUnit 5用拡張機能（スタブ） | `junit5_extension` |
| マスタデータ復旧機能（スタブ） | `master_data_restore` |
| テストデータ変換ツール（スタブ） | `testdata_converter` |
| マスタデータ投入ツール（スタブ） | `master_data_tool` |
| 表題ページ3件 | `testing_framework_setup` / `testing_framework_implementation` / `testing_framework_tools` |

### 第2部（残り10ページ）

| ページ | ファイル | ラベル |
|---|---|---|
| クラス単体テストの設定 | `setup/class_unit_test.rst` | `class_unit_test_setting` |
| リクエスト単体テストの設定（ウェブアプリケーション） | `setup/request_unit_test/web.rst` | `request_unit_test_setting_web` |
| リクエスト単体テストの設定（RESTfulウェブサービス） | `setup/request_unit_test/rest.rst` | `request_unit_test_setting_rest` |
| リクエスト単体テストの設定（HTTPメッセージング） | `setup/request_unit_test/http_messaging.rst` | `request_unit_test_setting_http_messaging` |
| リクエスト単体テストの設定（Nablarchバッチアプリケーション） | `setup/request_unit_test/batch.rst` | `request_unit_test_setting_batch` |
| リクエスト単体テストの設定（MOMによるメッセージング） | `setup/request_unit_test/mom.rst` | `request_unit_test_setting_mom` |
| リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング） | `setup/request_unit_test/db_queue.rst` | `request_unit_test_setting_db_queue` |
| 取引単体テストの設定（RESTfulウェブサービス） | `setup/deal_unit_test/rest.rst` | `deal_unit_test_setting_rest` |
| 取引単体テストの設定（HTTPメッセージング） | `setup/deal_unit_test/http_messaging.rst` | `deal_unit_test_setting_http_messaging` |
| 取引単体テストの設定（MOMによるメッセージング） | `setup/deal_unit_test/mom.rst` | `deal_unit_test_setting_mom` |

### 第3部（残り14ページ）

| ページ | ファイル | ラベル |
|---|---|---|
| エンティティ単体テスト | `implementation/class_unit_test/entity.rst` | `entity_unit_test` |
| コンポーネント単体テスト | `implementation/class_unit_test/component.rst` | `component_unit_test` |
| リクエスト単体テスト（ウェブアプリケーション） | `implementation/request_unit_test/web.rst` | `request_unit_test_web` |
| リクエスト単体テスト（RESTfulウェブサービス） | `implementation/request_unit_test/rest.rst` | `request_unit_test_rest` |
| リクエスト単体テスト（HTTPメッセージング） | `implementation/request_unit_test/http_messaging.rst` | `request_unit_test_http_messaging` |
| リクエスト単体テスト（Nablarchバッチアプリケーション） | `implementation/request_unit_test/batch.rst` | `request_unit_test_batch` |
| リクエスト単体テスト（MOMによるメッセージング） | `implementation/request_unit_test/mom.rst` | `request_unit_test_mom` |
| リクエスト単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/request_unit_test/db_queue.rst` | `request_unit_test_db_queue` |
| 取引単体テスト（ウェブアプリケーション） | `implementation/deal_unit_test/web.rst` | `deal_unit_test_web` |
| 取引単体テスト（RESTfulウェブサービス） | `implementation/deal_unit_test/rest.rst` | `deal_unit_test_rest` |
| 取引単体テスト（HTTPメッセージング） | `implementation/deal_unit_test/http_messaging.rst` | `deal_unit_test_http_messaging` |
| 取引単体テスト（Nablarchバッチアプリケーション） | `implementation/deal_unit_test/batch.rst` | `deal_unit_test_batch` |
| 取引単体テスト（MOMによるメッセージング） | `implementation/deal_unit_test/mom.rst` | `deal_unit_test_mom` |
| 取引単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/deal_unit_test/db_queue.rst` | `deal_unit_test_db_queue` |

### 第4部（残り2ページ）

| ページ | ファイル | ラベル |
|---|---|---|
| リクエスト単体データ作成ツール | `tools/request_data_tool.rst` | `request_data_tool` |
| HTMLチェックツール | `tools/html_check_tool.rst` | `html_check_tool` |

## STEP 3 — 引き継ぐ外部ラベルは例外として明記する

`implementation/request_unit_test/web.rst` は、削除された現行解説書から外部被参照ラベル `how_to_set_token_in_request_unit_test` を引き継ぐ（`checks/task-07.md`「リンク切れになる参照」3件目。参照元は `ja/application_framework/application_framework/libraries/db_double_submit.rst:106`）。

このラベルは `<ページ先頭ラベル>-<...>` の形式に合わないが、**FW解説書側の `:ref:` を壊さないため名前を変えてはならない。**

**S-08 に例外として1行明記すること。**「削除された現行解説書から引き継ぐ外部被参照ラベルは、参照元を壊さないため名前を変えない。対象は `checks/task-07.md` の表を参照」の趣旨とする。

## STEP 4 — 記録

- `checks/task-12.md` を新規作成し、ゲートの実行出力を記録する
- `steering.md` に `#12` のエントリを追加する。以降のページ作成タスクの Steps に「ページ先頭ラベルは `style.md` S-08 の一覧から引く」を追加すること
- `reviews/` には記録しない（ページを作らないため）

## ゲート

すべて実行結果で確認し、`checks/task-12.md` に記録すること。**ゲート1（全件表）を実行順の先頭に置く。**

1. S-08 に載せたラベル26件と、`ja/` 配下の全 `.rst` が定義する既存ラベルとの突き合わせ表（全件）。衝突0件であること。突き合わせは `.rn/` 配下ではなく `ja/` 配下の実ファイルから機械抽出して行う
2. S-08 の一覧が、`design.md` §13「1対1対応表」の34ページと過不足なく対応していること（作成済み・スタブを含む全件）
3. `git diff <基準コミット> HEAD -- ja/` が空
4. `python3 mapping/tools/verify_mapping.py` が exit 0、594行 / 12,986 / 11,983 が不変
5. `git diff <基準コミット> HEAD -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv .rn/20260724-ntf-yaml-support/mapping/_batch/ .rn/20260724-ntf-yaml-support/mapping/vocabulary.md .rn/20260724-ntf-yaml-support/mapping/glossary.md .rn/20260724-ntf-yaml-support/design.md` が空
6. `style.md` の差分が S-08 の節の中だけに収まっていること（S-01〜S-07・S-09〜S-11 の行に差分が無いこと）
7. S-08 の既存の根拠（FW解説書の file:line 4件）が削除されていないこと
8. Docker でフルビルド（`-a`）し、`build succeeded` かつ警告が既知の `db_double_submit.rst` 1件のみ（新規0件）

## 禁止事項

- **`ja/` 配下の `.rst` を1行も変更しない。** ページは作らない。既存ページのラベルも改名しない
- `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `design.md` / `ja/conf.py` を変更しない
- `style.md` の S-08 以外の観点を変更しない
- S-08 の既存の根拠（FW解説書の file:line）を削除しない。規約文の改訂と一覧の追加にとどめる
- **ラベルを新たに考案しない。STEP 2 の表をそのまま使う。** 表に無いページが見つかった場合は、勝手に命名せず `decide` として報告する
- `how_to_set_token_in_request_unit_test` の名前を変えない
- 4観点のレビューは回さない。ページを作らないタスクであり、ゲート1・2が全件の突き合わせを機械的に担保している
- user review の承認を受けるまで次タスクに着手しない
