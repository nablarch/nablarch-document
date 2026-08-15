# `#26` self-check — 取引単体テストの設定（MOMによるメッセージング）

対象タスク: `#26`。成果物は `ja/development_tools/testing_framework/setup/deal_unit_test/mom.rst`（新規）と `setup/common.rst` の追加分（`#25` の user review の回答1 による分割の受け皿）。

## ゲート1 — マッピング全件の対応表（母集合を先に固定する）

母集合は `mapping.csv` の**全597行**を `csv.DictReader` で読み、`dest_page` で抽出した（`wc -l` は使っていない）。

### `dest_page=取引単体テストの設定（MOMによるメッセージング）`（1行、`DROP` 0件）

| `mapping_id` | 出典の範囲 | `lines` | `disposition` | 反映先 |
|---|---|---:|---|---|
| `current-0158-a` | `send_sync.rst:280-297` | 18 | SPLIT | `setup/deal_unit_test/mom.rst`「モックアップクラスを登録する」 |

### `dest_page=共通設定`（7行、`DROP` 0件）。うち本タスクで追加した2行

| `mapping_id` | 出典の範囲 | `lines` | `disposition` | 反映先 |
|---|---|---:|---|---|
| `current-0158-b` | `send_sync.rst:298-360` | 63 | SPLIT | `setup/common.rst`「同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する」 |
| `current-0158-c` | `send_sync.rst:361-383` | 23 | SPLIT | `setup/common.rst`「テスティングフレームワークを依存関係に追加する」 |

既存5行（`current-0225`・`current-0226`・`current-0227`・`current-0228`・`current-0246`）は `#11` で反映済みで、本タスクでは触っていない。

### 出典の要素ごとの反映先（全件）

| 出典の要素 | 出典の行 | 反映先 |
|---|---|---|
| これらの設定は取引単体テストでのみ必要／テスト用のプロファイルに設定する | `:281` | `mom.rst:31`（「この設定が必要なのは取引単体テストだけであるため、テスト用のコンポーネント設定ファイルに記述する」） |
| 環境ごとにコンポーネントを切り替える方法への参照 | `:282` | `mom.rst:31`（`:ref:` `how_to_change_componet_define`） |
| 通常アーキテクトが行う／アプリケーションプログラマは設定不要 | `:284` | `mom.rst:15-17`（`tip`。語は `glossary.md` に従い「テストを実装するアプリケーション開発者」） |

**`#pre-last` による是正**: 上表の「アプリケーション開発者」は当時 `glossary.md` に未収載だった。`#pre-last` で `アプリケーションプログラマ` を正表記と定めた（`glossary.md` §5.14。FW解説書4対1・現行解説書13対0）ため、`mom.rst:17` の本文は「テストを実装するアプリケーションプログラマ」に変わっている。根拠は `checks/task-pre-last.md` §5(b)。
| モックアップクラスを設定する旨 | `:289` | `mom.rst:21` |
| `messagingProvider` = `MockMessagingProvider` のXML例 | `:291-296` | `mom.rst:23-27` |
| Excelファイルの配置場所のパスを設定する旨 | `:304` | `common.rst:122`・`:124` |
| `filePathSetting` のXML例（`sendSyncTestData`・`format` のパスと拡張子） | `:306-324` | `common.rst:151-177`（Excel形式の場合）・`:185-207`（YAML形式の場合） |
| 配置イメージの画像 | `:326-328` | `common.rst:179-181`（画像は `setup/images/common/` へ `git mv`） |
| `file:` スキーム推奨（サーバ起動中に編集できる） | `:330-333` | `common.rst:145-147`（`tip`） |
| テストデータを解析するコンポーネントを設定する旨 | `:338` | `common.rst:122`・`:124` |
| `messagingTestDataParser` と解釈クラス群のXML例 | `:340-360` | 解釈クラス群は両形式共通のため `common.rst:128-141`。`messagingTestDataParser` は `:170-177`（Excel形式の場合）・`:203-207`（YAML形式の場合） |
| `pom.xml` に dependency を追加する旨 | `:366` | `common.rst:17`・`:28` |
| `nablarch-testing` の dependency のXML例 | `:368-383` | `common.rst:19-26`（`<exclusions>` は陳腐化のため落とした。`reviews/page-deal_unit_test_setting_mom.md`「出典から変えた点」）。あわせて `:28-37` に `nablarch-testing-yaml` を追記（出典外。ラウンド1 の `must` R1-1） |

反映漏れ **0件**。

## ゲート2 — ページ先頭ラベル

`style.md` S-08「NTF解説書のページ先頭ラベル一覧」の表（`mapping/style.md:366`）から引いた。**新規考案なし**。

- ページ: `取引単体テストの設定（MOMによるメッセージング）` → ラベル `deal_unit_test_setting_mom`
- セクションラベル `testing_framework_common-send_sync_test_data` は S-08 の `<ページ先頭ラベル>-<内容を表す英語スネークケース>` の形式に従って新設した

`ja/` 全体に同名ラベルが無いことを確認した（`grep -rn "^\.\. _\`\?<label>\`\?:" --include=*.rst ja/` が本ページ以外0件）。Docker フルビルドのログに `duplicate label` **0件**。

## ゲート3 — `design.md` §3 の記載範囲

第2部に置くのはコンポーネント設定ファイル・環境設定ファイルの設定項目と記述例、拡張方法であり、テストソースコードの実装例とテストデータの記述例は置かない。本タスクの成果物にテストソースコードは0件、テストデータの記述例（Excelのセル格子・YAMLの記述）も0件で、記述方法は `:ref:` で第3部（`testdata_notation-messaging_data`）へ導線を張った（`mom.rst:35`・`common.rst:124`）。

## ゲート4 — 実装での確認

`reviews/page-deal_unit_test_setting_mom.md`「実装で確認した事実」に `file:line` と参照コミット（`nablarch/nablarch-testing` = `e21bf67`）を記録した。YAML形式の `fileExtensions` の扱いは**実際に動かして確認**した（同節「実行して確認した結果」）。

## ゲート5 — `verify_mapping.py`

`python3 mapping/tools/verify_mapping.py` は `OK: no errors`・`exit 0`。**597行 / 12,986 / 11,983**（`#25` 時点は595行 / 12,986 / 11,983。行数の合計は不変で、行の分割による純増2）。

## ゲート6 — `_batch/*.csv` の再生成とバイト一致

```
{ head -1 _batch/batch-01.csv; for f in _batch/batch-*.csv; do tail -n +2 "$f"; done; } > /tmp/regen2.csv
md5sum mapping.csv /tmp/regen2.csv
d73e1710017bee2fd1c0a1dc1682b77d  mapping.csv
d73e1710017bee2fd1c0a1dc1682b77d  /tmp/regen2.csv
```

一致。素の `cat` ではなく各ファイルのヘッダ行を除いて連結している。変更したのは `_batch/batch-25.csv` の1ファイルのみ（`current-0158` の1行を3行に置換。`src_body_start` 昇順の並びを維持）。

## ゲート7 — `volume.md` の整合

`volume.md` の `dest_page` 別表の合計と `mapping.csv` の実測値（`DROP` 除く）がいずれも **11,983** で一致することを、独立に組んだ集計スクリプト（`csv.DictReader` と表のパース）で確認した。差分は次の3点のみ。

- 共通設定: 129 → **215**（+86）
- 取引単体テストの設定（MOMによるメッセージング）: 104 → **18**（-86）
- 行数・`disposition`・`audience`: 595→597行、MOVE 238→237 / SPLIT 19→22、user 567→569

`dest_section` 別集計（第2部「使用方法」1,334行）は不変である（3行とも `dest_part`・`dest_section` を変えていない）。

## ゲート8 — Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
  /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

`build succeeded, 1 warning.`。警告は既知の1件（`ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test`）のみで、**新規0件**。`duplicate label` 0件。ビルド直後に `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して復元した。

生成HTMLで次を確認した。

- `setup/deal_unit_test/mom.html` の `:ref:` 3件がすべて解決している（`common.html#testing-framework-common-send-sync-test-data`／`testdata_notation.html#testdata-notation-messaging-data`／`ManagingEnvironmentalConfiguration/index.html#how-to-change-componet-define`）
- `setup/common.html` に画像 `send_sync_test_data_structure.png` が出力されている
- `setup/index.rst` の `toctree` に `deal_unit_test/mom` が入っている

## ゲート9 — 段落内の改行と見出し下線

- 段落内の改行: 独立に組んだ走査（空行を挟まず日本語の行が連続する箇所の検出）で**0件**
- 見出し下線: `unicodedata.east_asian_width` で表示幅を計測し、L1=50・L2=50・L3=49（表示幅が49を超える「同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する」は76）・L4=49。いずれも表示幅以上で、承認済みページの実測則 `max(49, 表示幅)` に一致

## ゲート10 — 禁止語

`不具合`・`バグ`・`将来`・`修正され`・`なお、`・`することができ`・`行うことができ` の各**0件**（`mom.rst`・`common.rst`）。

## ゲート11 — 差分の範囲

母集合は `git status --porcelain -uall` の**全件**（`ja/` などに絞っていない）。

| 状態 | パス | 予定どおりか |
|---|---|---|
| `M` | `.rn/20260724-ntf-yaml-support/mapping/_batch/batch-25.csv` | 予定どおり（`current-0158` の分割） |
| `M` | `.rn/20260724-ntf-yaml-support/mapping/mapping.csv` | 予定どおり（`_batch` から再生成） |
| `M` | `.rn/20260724-ntf-yaml-support/mapping/volume.md` | 予定どおり（集計の追随） |
| `M` | `ja/development_tools/testing_framework/setup/common.rst` | 予定どおり（2セクション追加とリード文） |
| `M` | `ja/development_tools/testing_framework/setup/deal_unit_test/http_messaging.rst` | 予定どおり（`:ref:` 1文の追加） |
| `R` | `…/guide/…/03_DealUnitTest/_images/send_sync_test_data_structure.png` → `setup/images/common/send_sync_test_data_structure.png` | 予定どおり（`design.md` §13「画像の配置」） |
| `M` | `ja/development_tools/testing_framework/setup/index.rst` | 予定どおり（`toctree` 1行） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-26.md` | 本ファイル |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-deal_unit_test_setting_mom.md` | レビュー記録 |
| `??` | `ja/development_tools/testing_framework/setup/deal_unit_test/mom.rst` | 新規ページ |

予定外のファイル **0件**。`locales/ja/LC_MESSAGES/sphinx.mo` は混入していない（Docker フルビルドの直後に復元済み）。作業中に生成された `jacoco.exec`（実装確認で Maven を実行した副産物）は検出して削除した。

## ラウンド1（4観点レビュー）の是正後の再実行

4観点レビュー ラウンド1 の判定は **A・B・C・D の4観点とも FAIL**（重複除去後 `must` 5件・`should` 9件・`info` 8件）。指摘と是正の対応は `reviews/page-deal_unit_test_setting_mom.md`「4観点レビュー ラウンド1」に全件記録した。是正後にゲートを再実行した結果は次のとおり。

| ゲート | 再実行の結果 |
|---|---|
| 8（Docker フルビルド） | `build succeeded, 1 warning.`。既知の `db_double_submit.rst:108` のみで新規0件、`duplicate label` 0件。ビルド直後に `sphinx.mo` を復元 |
| 8（生成HTML） | `common.html` の目次に新しいL3とL4対（`Excel形式の場合`／`YAML形式の場合`）が並び、`mom.html`・`http_messaging.html` の `:ref:` が `common.html#testing-framework-common-send-sync-test-data` に解決 |
| 9（段落内の改行・見出し下線） | 改行0件。下線はすべて表示幅以上（新しいL3見出しの表示幅76に対し下線76） |
| 10（禁止語） | 各0件 |
| 11（差分の範囲） | 上表と同じ10件。予定外0件 |
| 用語の走査（追加） | `テスト種別`・`解析クラス`・`配置場所`・`配置イメージ` の各0件。地の文の素の `Excel形式`／`YAML形式` は0件（XMLコメント内の1件を除く） |

## 検証ラウンド（是正差分のみ）の結果

判定は **PASS（`must` 0件）**。`should` 2件（V-1 目次からL4へ直接飛んだ読者に共通定義が見えない／V-2 拡張子と実ファイルの一致を明示していない）は本タスク内で是正し、Docker フルビルドを再実行して `build succeeded, 1 warning.`（新規0件）を確認した。`info` 5件は対応せず理由を記録した。詳細は `reviews/page-deal_unit_test_setting_mom.md`「検証ラウンド（是正差分のみ）」。
