# `#27` 週末の連続作成キュー — ゲート記録

作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-weekend-queue.md`（§5 にゲートG1〜G13 の定義）
個別指示: `ntf-doc-27-small-3rd.md`（`#27-07`・`#27-10`・`#27-11`・`#27-15`）/ `ntf-doc-27-db-queue.md`（`#27-16`〜`#27-18`）/ `ntf-doc-27-large-pages.md`（`#27-19`〜`#27-21`）

**本ファイルは `#27` で1本にまとめる。ページごとに節を分ける。**

---

## `#27-00` 未作成15ページのスタブ一括作成

**着手前の3手順（作業指示 §0-1）**

| 手順 | 実行内容 | コミット |
|---|---|---|
| 1 | 作業指示4本を1バイトも変えずにコミット | `aacbf32` |
| 2 | `steering.md` の `#27` キューを作業指示 §3 の表（`#27-00` ＋21ページ）に作り直す | `7a05204` |
| 3 | `steering.md` の `Rules` に「`#27` のサブ項目はタスクではない」の1行を追加 | `7a05204` |

**作成した15ファイル**（`ja/development_tools/testing_framework/` からの相対。ラベルは `style.md` S-08、下線幅は `max(50, タイトルの表示幅)`）

| ファイル | ラベル | タイトル表示幅 | 下線 |
|---|---|---:|---:|
| `implementation/class_unit_test/entity.rst` | `entity_unit_test` | 22 | 50 |
| `implementation/class_unit_test/component.rst` | `component_unit_test` | 24 | 50 |
| `implementation/request_unit_test/rest.rst` | `request_unit_test_rest` | 45 | 50 |
| `implementation/request_unit_test/http_messaging.rst` | `request_unit_test_http_messaging` | 42 | 50 |
| `implementation/request_unit_test/batch.rst` | `request_unit_test_batch` | 54 | 54 |
| `implementation/request_unit_test/mom.rst` | `request_unit_test_mom` | 47 | 50 |
| `implementation/request_unit_test/db_queue.rst` | `request_unit_test_db_queue` | 66 | 66 |
| `implementation/deal_unit_test/web.rst` | `deal_unit_test_web` | 40 | 50 |
| `implementation/deal_unit_test/rest.rst` | `deal_unit_test_rest` | 39 | 50 |
| `implementation/deal_unit_test/http_messaging.rst` | `deal_unit_test_http_messaging` | 36 | 50 |
| `implementation/deal_unit_test/batch.rst` | `deal_unit_test_batch` | 48 | 50 |
| `implementation/deal_unit_test/mom.rst` | `deal_unit_test_mom` | 41 | 50 |
| `implementation/deal_unit_test/db_queue.rst` | `deal_unit_test_db_queue` | 60 | 60 |
| `setup/request_unit_test/db_queue.rst` | `request_unit_test_setting_db_queue` | 72 | 72 |
| `tools/request_data_tool.rst` | `request_data_tool` | 30 | 50 |

**下線幅の根拠**: 既存スタブ6本はいずれも `=` 50個だが、これはタイトル表示幅が50以下だったためである。表示幅が50を超えるページは既存の本体ページで下線を表示幅ちょうどまで伸ばしている（`setup/request_unit_test/batch.rst:3-4` — タイトル `リクエスト単体テストの設定（Nablarchバッチアプリケーション）` の表示幅60、下線 `=` 60個）。この運用に合わせ、`max(50, 表示幅)` とした。`style.md:195`（下線はタイトルの表示幅以上）を満たす。

**`setup/deal_unit_test/db_queue.rst` は作っていない。**`design.md:386`・`:891` が意図した非対称であると明記しているため（作業指示 §3-1）。

**`toctree` の並び**: `setup/index.rst`・`implementation/index.rst`・`tools/index.rst` の3本を `design.md:837-886` のファイルツリー順に並べ替え、最終形にした。以降のページ作成コミットは自分の `.rst` と記録ファイルだけを触る。

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain` 全件が `ja/development_tools/testing_framework/` 配下の予定18ファイル（新規15・変更3）のみ。ディレクトリで絞らずに実行した |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` は `git status --porcelain` に現れない（差分0行） |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git -C <repo> checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`、キャッシュを捨てた全量読み込み）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件**。未作成ページを指す `undefined label` は0件で、スタブの作り漏れが無いことを裏付ける |
| G6 | **PASS** | 本タスクで触った18ファイルに禁止語0件。※ `about/index.rst:20` に `不具合` が1件あるが `#8` で承認済みの既存本文であり本タスクの対象外（下記「判断待ち」参照） |
| G7 | **PASS** | 15件のラベルが `style.md` S-08 の一覧（第3部14ページの表・第4部2ページの表）と全件一致。上表のとおり |
| G8 | **PASS** | 全15件で下線幅 ≥ タイトル表示幅。上表のとおり |
| G9 | **N/A** | スタブは本文を持たず `:ref:` が0件 |
| G10 | **N/A** | 出典行を消費しない（`mapping.csv` の行を反映するタスクではない） |
| G11 | **N/A** | 同上 |
| G12 | **N/A** | 同上 |
| G13 | **N/A** | 画像を持たない |

### 判断待ち（週明けに判定してほしい項目）

1. **`about/index.rst:20` に禁止語 `不具合` が1件ある。** `#8` で user review 承認済みの本文であり、`#27` の各ページのゲートG6 はページ単位の規則であるため本タスクでは触っていない。実物を開いて確認した（該当は「経路に起因する不具合を早期に見つけられる」の1箇所）。横断の是正として `#pre-last` で扱うか、承認済みとしてそのまま残すかを判定してほしい。

### コミット

`ja/` の18ファイル＋本記録。件名 `chore: 未作成15ページのスタブを作成して toctree に登録する — #27-00`。

---

## `#27-01` マスタデータ復旧機能

**成果物**: `ja/development_tools/testing_framework/setup/master_data_restore.rst`（176行。ラベル `master_data_restore`）
**画像2点**: `guide/development_guide/06_TestFWGuide/_images/{modification_detected,copy_from_backup}.png` を `setup/images/master_data_restore/` へ `git mv` した
**出典**: `04_MasterDataRestore.rst`（9行）＋ `03_Tips.rst`（1行）の計10行・193行。いずれも `disposition=MERGE`
**レビュー記録**: `reviews/page-master_data_restore.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain` の全件（ディレクトリで絞らずに実行）が3エントリ。画像2点の `R`（rename）と ` M ja/development_tools/testing_framework/setup/master_data_restore.rst` のみ |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` のいずれも `git status --porcelain` に現れない |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が `OK: no errors` で exit 0（597行 / 12,986 / 11,983）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件** |
| G6 | **PASS** | `grep -nE '不具合\|バグ\|将来\|修正され'` が0件 |
| G7 | **PASS** | ページ先頭ラベル `master_data_restore` が `style.md` S-08 の第2部の表と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測って確認。L1 下線50 / タイトル表示幅20、L2 下線50 / 最長8、L3 下線は6本とも49 / 最長34。同一ページ内で基準幅を揃えている |
| G9 | **PASS** | 生成HTMLで確認。`#master-data-restore-watched-tables` → 見出し「監視対象テーブルを登録する」、`../tools/master_data_tool.html#master-data-tool` → 見出し「マスタデータ投入ツール」。いずれもリンク文字列と一致 |
| G10 | **PASS** | 10行のうち9行を本文に反映、`current-0245` の1行を意図して落とした。行ごとの反映先と、落とした理由は `reviews/page-master_data_restore.md`（「出典行の消化」と「判断待ち」1） |
| G11 | **N/A** | 本ページの10行はすべて `disposition=MERGE`。`REFERENCE` の行は無い（§5 の該当9ページにも `#27-01` は含まれない） |
| G12 | **N/A** | 10行とも `-a`／`-b`／`-c` の枝を持たない単独の `mapping_id`。§5 の該当2ページ（`#27-09`・`#27-19`）にも含まれない |
| G13 | **PASS** | `.. image::` 2件の指す先が `setup/images/master_data_restore/` に実在。`find ja/development_tools/testing_framework/guide -name modification_detected.png -o -name copy_from_backup.png` が0件で、移動元が残っていない |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、`must` 3件を含む指摘を是正した。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-master_data_restore.md`。

### コミット

`ja/` の3エントリ（`.rst` 1本＋画像2点の rename）＋記録2本。件名 `docs: マスタデータ復旧機能のページを作成する — #27-01`。
