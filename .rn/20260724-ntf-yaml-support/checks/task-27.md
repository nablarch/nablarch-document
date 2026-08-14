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

---

## `#27-02` JUnit 5用拡張機能

**成果物**: `ja/development_tools/testing_framework/setup/junit5_extension.rst`（440行。ラベル `junit5_extension`）
**出典**: `JUnit5_Extension.rst`（14行）＋ `01_Abstract.rst`（3行）の計17行・475行。`MOVE` 16件・`MERGE` 1件（`current-0266`）
**レビュー記録**: `reviews/page-junit5_extension.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain` の全件（ディレクトリで絞らずに実行）が1エントリ。` M ja/development_tools/testing_framework/setup/junit5_extension.rst` のみ |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` のいずれも `git status --porcelain` に現れない |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が `OK: no errors` で exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件**。是正の途中で外部リンクの表示名を揃えた際に `junit5_extension.rst:6: WARNING: Duplicate explicit target name: "公式のユーザガイド(外部サイト、英語)"` が出たため、移行ガイド側の表示名を「公式の移行ガイド」に変えて解消した（`reviews/page-junit5_extension.md` R1-17） |
| G6 | **PASS** | `grep -nE '本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用'` が0件。`.. note::`／`.. warning::` の使用も0件（`tip` 5件・`important` 4件のみ） |
| G7 | **PASS** | ページ先頭ラベル `junit5_extension` が `style.md:343` の第2部の表と一致（同行の「（スタブ）」の除去は `decide` に回した） |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全見出しについて「下線の文字数 ≥ 見出しの表示幅」を検査して NG 0件。L1 下線50 / タイトル表示幅18、L2 下線50 / 最長8、L3 下線は13本とも49 / 最長42（「RegisterExtensionでExtensionクラスを適用する」） |
| G9 | **PASS** | 生成HTMLで確認。本文の `:ref:` 4件がすべて解決している。`#junit5-extension-inject` → 「テストクラスに合成アノテーションを設定する」、`../about/index.html#testing-framework-about` → 「テスティングフレームワーク」、`request_unit_test/rest.html#request-unit-test-setting-rest` → 「リクエスト単体テストの設定（RESTfulウェブサービス）」、`../implementation/testdata_notation.html#testdata-notation-file-structure` → 「テストクラスとテストデータの対応」。`href="#"` の空リンクは0件。`:java:extdoc:` は55件がすべて javadoc の URL に展開されている |
| G10 | **PASS** | 17行すべてを本文に反映。落とした行は無い。行ごとの反映先は `reviews/page-junit5_extension.md`「出典行の消化」。うち2行（`current-0178`・`current-0269`）は `dest_section` と異なる節に置いた。理由と判定依頼は同記録の「判断待ち」1・2 |
| G11 | **N/A** | 17行に `disposition=REFERENCE` の行が無い |
| G12 | **N/A** | 17行とも `-a`／`-b`／`-c` の枝を持たない単独の `mapping_id` |
| G13 | **N/A** | 画像を持たない |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、`must` 4件を含む指摘を1ラウンドで是正した。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-junit5_extension.md`。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-junit5_extension.md`「判断待ち（`decide`）」に5件（`dest_section` との不一致2件、`resolveTestRules()` の制約が本体の不具合かどうか1件、`style.md:343` の「（スタブ）」の除去1件、surefire 2.22.0 の一次情報が未確認である旨1件）。

### コミット

`ja/` の1ファイル＋記録2本。件名 `docs: JUnit 5用拡張機能のページを作成する — #27-02`。

---

## `#27-03` テストデータ変換ツール

**成果物**: `ja/development_tools/testing_framework/tools/testdata_converter.rst`（321行。ラベル `testdata_converter`）
**出典**: `input/testdata-converter-design.md` の6行・75行。`MOVE` 5件・`MERGE` 1件（`input-0198-b`）
**参照実装**: `nablarch-testing-converter`（作業指示に固定コミットの指定なし。作業ツリーは `2f21bce`）、`nablarch-testing`（`e21bf67`）、`nablarch-testing-yaml`（固定 `190cc9a`。作業ツリーは `b91abc1`）
**レビュー記録**: `reviews/page-testdata_converter.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain` の全件（ディレクトリで絞らずに実行）が2エントリ。` M ja/development_tools/testing_framework/tools/testdata_converter.rst` と `?? .rn/20260724-ntf-yaml-support/reviews/page-testdata_converter.md` |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` のいずれも `git status --porcelain` に現れない |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が `OK: no errors` で exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件**。是正を全件畳んだ後の最終本文で再実行して確認した |
| G6 | **PASS** | `grep -nE '本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス'` が0件。`.. note::`／`.. warning::` の使用も0件（`tip` 3件・`important` 1件のみ） |
| G7 | **PASS** | ページ先頭ラベル `testdata_converter` が `style.md:347` の第4部の表と一致（同行の「（スタブ）」の除去は `decide` に回した） |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全10見出しについて「下線の文字数 ≥ 見出しの表示幅」を検査して NG 0件 |
| G9 | **PASS** | 生成HTMLで確認。本文の `:ref:` 3件がすべて解決している。`testdata_converter.rst:46`・`:65` → `../implementation/testdata_notation.html#testdata-notation`（飛び先の見出しは `testdata_notation.rst:3`「テストデータの書き方」でリンク文字列と一致）、`:59` → `#testdata-converter-xls-format`（飛び先は同ページ `:229`「Excel形式の出力を整形する」で一致）。`href="#"` の空リンクは0件。`:java:extdoc:` 1件（`nablarch.test.core.file.TestDataConverter`）が javadoc の URL に展開されている |
| G10 | **PASS** | 6行75行すべてを本文に反映。落とした行は無い。行ごとの反映先は `reviews/page-testdata_converter.md`「出典行の消化」 |
| G11 | **N/A** | 6行に `disposition=REFERENCE` の行が無い |
| G12 | **PASS** | 枝を持つのは `input-0198-b`（1行）のみ。相方の `input-0198-a`（22行）・`input-0198-c`（3行）はいずれも `disposition=DROP` で `dest_page` が空のため、二重掲載の相手になるページが存在しない |
| G13 | **N/A** | 画像を持たない（`.. image::`／`.. figure::` が0件） |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（是正26件、採らなかった指摘5件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-testdata_converter.md`。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-testdata_converter.md`「判断待ち（`decide`）」に5件。筆頭は**往復の非可逆**で、同梱の `ProjectActionRequestTest.xlsx` を XLS→YAML→XLS で往復させると `confirmOfCreateAbNormal` の `LIST_MAP`／`requestParams` からリクエストパラメータ4件が落ちる実測がある。作業指示 §2 の「本体の不具合が疑われる場合は書かずに `decide` に上げる」に従い、本文は出典に忠実な「意味を変えずに往復できる」のままにしてある。

---

## `#27-04` リクエスト単体データ作成ツール

**成果物**: `ja/development_tools/testing_framework/tools/request_data_tool.rst`（119行。ラベル `request_data_tool`）＋移送アセット7件
**出典**: `01_HttpDumpTool.rst`・`02_SetUpHttpDumpTool.rst`（削除済み。`git show 2e501ad:<path>` で参照）の17行・163行。全件 `MOVE`
**参照実装**: `nablarch-testing`（`e21bf67`）、`nablarch-testing-jetty12`（作業指示に固定コミットの指定なし。`/home/tie303177/work/nablarch/` 配下にソースが無いため `~/.m2/repository` の jar を参照。Rule §1-9 からの逸脱として `reviews/page-request_data_tool.md` に記録）
**レビュー記録**: `reviews/page-request_data_tool.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain` の全件（ディレクトリで絞らずに実行）が8エントリ。`R` 7件（`guide/development_guide/08_TestTools/01_HttpDumpTool/_image/` の png 5件と `image.xlsx`、`download/httpDump.bat` の `git mv`）と ` M ja/.../tools/request_data_tool.rst` 1件。記録2本（`reviews/page-request_data_tool.md`・本ファイル）を含めても想定内 |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を `git status --porcelain` に明示指定して実行し、出力0行 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件**。是正を全件畳んだ後の最終本文で再実行して確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）が0件。あわせて `本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス` も0件、`.. note::`／`.. warning::` も0件（`tip` 2件のみ）。`です・ます` 0件 |
| G7 | **PASS** | ページ先頭ラベル `request_data_tool` が `mapping/style.md:391` の第4部の表と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全12見出しについて「下線の文字数 ≥ 見出しの表示幅」を検査して NG 0件（下線は全件50、表示幅の最大は46） |
| G9 | **PASS** | 生成HTMLで確認。本文の `:ref:` 4件がすべて解決し、リンク文字列も飛び先の見出しと一致。`:18`・`:96` →「テストショット一覧（testShots）を記述する」、`:88` → 同ページ内「導入」（`request_data_tool-setup`）、`:94` →「リクエスト単体テストの設定（ウェブアプリケーション）」。`href="#"` の空リンクは0件 |
| G10 | **PASS** | 17行163行すべてを分類。落としたのは3件（「開発環境構築ガイド」の前提条件＝参照先が存在しない、`httpDump.sh` の案内＝配布物が無い、pomスニペットの `<!-- 中略 -->` 行）で、いずれも理由を `reviews/page-request_data_tool.md`「意図して落とした出典」に記載 |
| G11 | **N/A** | 17行に `disposition=REFERENCE` の行が無い |
| G12 | **PASS** | 枝分かれ（`-a`／`-b`）の `mapping_id` が無い。`src_file` 2本はいずれも本ページ専用で、他ページと範囲が重ならない |
| G13 | **PASS** | `.. image::` 5件のファイルが実在し、ビルド後に `_build/html/_images/` へコピーされている。`:download:` の `httpDump.bat` も `_build/html/_downloads/` に出力されている。`git ls-files guide/development_guide/08_TestTools/01_HttpDumpTool/` が0件で、移送元ディレクトリは残っていない |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（延べ42件。**是正26件・不採用9件・記録のみ7件**）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-request_data_tool.md`。

不採用のうち最も重いのは、検証観点の「`nablarch-testing` にダンプツールのクラスは1つも無い（`7c545e5` で削除済み）ので、2モジュール必要という記述は誤り」という NG である。`~/.m2/repository` の jar を実測したところ、クラス群は `nablarch-testing-jetty12` に、`RequestDumpAgent` がクラスパスから読む `template.xls` は `nablarch-testing` にあり、**両方必要**であることを確認したため、記述を維持した。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_data_tool.md`「判断待ち（`decide`）」に6件。筆頭は **Linux で本ツールを起動できない**こと。出典は `httpDump.sh` を選ぶよう案内しているが、この解説書リポジトリに `.sh` は無く、`nablarch-testing@e21bf67` の `src/main/script/httpDump.sh` は Nablarch 1.x 時代のクラスパス指定のままで、かつ jar にも同梱されない。本文は Windows 前提（`httpDump.bat`）に寄せてある。ほかに、本体側 `src/main/script/httpDump.{bat,sh}` の陳腐化、`rest.rst:53` の記述が実装より狭いこと、`web.rst:31` の `webBaseDir` 既定値の食い違い、第3部から本ページへの導線が無いこと、規約側の手当て4件。
