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

## `#27-05` マスタデータ投入ツール

**成果物**: `ja/development_tools/testing_framework/tools/master_data_tool.rst`（161行。ラベル `master_data_tool`）＋移送アセット5件
**出典**: `index.rst`・`01_MasterDataSetupTool.rst`・`02_ConfigMasterDataSetupTool.rst`（削除済み。`git show 2e501ad:<path>` で参照）の13行・177行。`REFERENCE` 1件（`current-0355`）を含む
**参照実装**: `nablarch-testing`（`e21bf67`）、`nablarch-testing-yaml`（`190cc9a`）、配布物 `master-data-setup-tool.zip`（本リポジトリ内。`2e501ad` 時点から md5 不変）
**レビュー記録**: `reviews/page-master_data_tool.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は `R` 5件（`02_MasterDataSetup/_image/` の png 4件と `download/master-data-setup-tool.zip` の `git mv`）と ` M ja/.../tools/master_data_tool.rst`。記録3本（`reviews/page-master_data_tool.md`・本ファイル・`steering.md`）を含めても想定内 |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を `git status --porcelain` に明示指定して実行し、出力0行 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。**新規0件**。是正を全件畳んだ後の最終本文で再実行して確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）が0件。あわせて `本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス` も0件、`.. note::`／`.. warning::` も0件（`tip` 2件・`important` 3件）。`です・ます` 0件 |
| G7 | **PASS** | ページ先頭ラベル `master_data_tool` が `mapping/style.md:348` の第4部の表と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全10見出しについて「下線の文字数 ≥ 見出しの表示幅」を検査して NG 0件（下線は全件50、表示幅の最大は38） |
| G9 | **PASS** | 本文の `:ref:` 12件がすべて解決し、リンク文字列も飛び先の見出しと一致。例外は `:ref:`gsp-dba-maven-plugin <gsp-maven-plugin>`` の意図的な短縮1件（出典・`testdata_notation.rst:40` と同じ書き方）。`:download:` 1件・`:java:extdoc:` 1件・`.. image::` 4件もビルドで解決 |
| G10 | **PASS** | 13行177行すべてを分類。落としたのは3件（`index.rst` の toctree、`mvn` コマンドの再掲、Antビュー登録後の確認手順＋画像）で、いずれも理由を `reviews/page-master_data_tool.md`「意図して落とした出典」に記載 |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0355` 1件。使用方法のリード文で `:ref:`導入 <master_data_tool-setup>`` に変換し、節としては起こしていない |
| G12 | **PASS** | 枝分かれ（`-a`／`-b`）の `mapping_id` が無い。`src_file` 3本はいずれも本ページ専用 |
| G13 | **PASS** | `.. image::` 4件のファイルが実在し、`git ls-files guide/development_guide/08_TestTools/02_MasterDataSetup/` が0件で移送元ディレクトリは残っていない |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（延べ70件＝QA 17・設計 21・クラフト 20・検証 12。**採用44件を本文への是正33箇所に畳み、不採用9件、残りは記録のみ**）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-master_data_tool.md`。

最も重いのは3件。①**出典が配布物の中身を誤って書いていた**こと（`MASTER_DATA.xlsx`／`tool/db/data/` 配下の5ファイル／小文字 `nablarch_test_master`）。zip の md5 は `2e501ad` 時点から変わっておらず、出典が当時から誤っていた。実物に合わせた。②**バックアップ用スキーマに必要なテーブルの範囲**。本ツールはマスタデータファイルに記述した全テーブルをコピーする（`MasterDataSetUpper.java:109-115` → `MasterDataRestorer.java:283-339`）ため、飛び先の「監視対象テーブルのみでよい」に従うと失敗する。前提事項を書き直した。③**`testDataParser` が YAML 形式用のとき、投入対象が0件になりエラーにもならない**こと（`YamlTestDataParser.java:102-111` → `YamlLoader.java:142-143`）。適用範囲として `important` に書いた。

不採用のうち最も重いのは、設計観点の「L3 見出しの下線を多数派の `~` 49文字に揃えよ」である。`style.md` S-04（`style.md:195`）は「タイトル文字列と同じ長さ以上」しか定めておらず違反ではなく、`request_data_tool.rst` も50文字であるため、片方だけ直すと第4部内でさらに割れる。規約側の判断に回した。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-master_data_tool.md`「判断待ち」に8件。承認済みページの変更を伴うものが3件ある。**①`master_data_restore.rst:91` のスキーマ名**（小文字 `nablarch_test_master`。配布物は大文字）、**②`master_data_restore.rst:59-61` の tip**（本ツール併用時はマスタデータファイルに記述した全テーブルが必要）、**③`testdata_notation.rst:40` の gsp への言及**（`mapping.csv` では gsp の推奨は本ページにのみ割り当てられており、出典 `01_Abstract.rst:607-609` は gsp に触れていない）。ほかに規約側の手当て3件（見出し下線長の固定、第4部のセクション構成、承認済みページとの事実の重複の扱い）、YAML 形式時の挙動を本体側で扱うかの判断、配布物の整理（`protect.main.resources` の綴り、存在しない `build/classes`）。

## `#27-06` HTMLチェックツール

**成果物**: `ja/development_tools/testing_framework/tools/html_check_tool.rst`（230行。ラベル `html_check_tool`）＋移送アセット1件（`how-to-trace-html.png`）
**出典**: `08_TestTools/03_HtmlCheckTool/index.rst`（削除済み。`git show 2e501ad:<path>` で参照）の9行・214行。`DROP`・`REFERENCE` なし
**参照実装**: `nablarch-testing`（`e21bf67`）、`nablarch-example-web`（デフォルト設定の設定ファイルと `unit-test.xml`）
**レビュー記録**: `reviews/page-html_check_tool.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../tools/html_check_tool.rst` と `R ja/.../guide/development_guide/08_TestTools/03_HtmlCheckTool/_image/how-to-trace-html.png -> ja/.../tools/images/html_check_tool/how-to-trace-html.png` の2件。記録3本（`reviews/page-html_check_tool.md`・本ファイル・`steering.md`）を含めても想定内 |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。復活させた `:scale: 70` も警告を出さない。是正を全件畳んだ後の最終本文で実行した |
| G6 | **PASS** | 作業指示 §5 の禁止語0件。あわせて `本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス`、および用語集が0件を求める `テストケース`（`glossary.md:556`）も0件。です・ます 0件、`.. note::`／`.. warning::` 0件（`tip` 2件・`important` 7件） |
| G7 | **PASS** | ページ先頭ラベル `html_check_tool` が `mapping/style.md:392` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全10見出しで「下線の文字数 ≥ 見出しの表示幅」。NG 0件（L1・L2 は50、L3 は49。表示幅の最大は34） |
| G9 | **PASS** | `:ref:` 5件（`request_unit_test_setting_web` ×3、`html_check_tool-switch`、`html_check_tool-replace`）がすべて解決。`:java:extdoc:` 3件・`.. image::` 1件もビルドで解決。削除された旧ラベル `01_custom`・`customize_html_check` への参照は `ja/` 配下の `.rst` に0件 |
| G10 | **PASS** | 9行214行すべてを分類。落としたのは2件（リード文の「目的、仕様、使用方法に関して記述する」、`:61-63` のコメントアウト）で、理由は `reviews/page-html_check_tool.md`「出典行の消化」に記載 |
| G11 | **PASS** | `disposition=REFERENCE` の行なし（9行すべて `MERGE`） |
| G12 | **PASS** | `HTMLチェック` を含む `.rst` は本ページと承認済みの `setup/request_unit_test/web.rst` のみ。後者は設定項目一覧としての記載で、本ページから `:ref:` している |
| G13 | **PASS** | `.. image::` 1件のファイルが実在。`git ls-files guide/development_guide/08_TestTools/` が0件で、空ディレクトリも削除済み |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（QA M2/S4/N5、設計 M4/S6/N5、クラフト M3/S13/N6、検証は突き合わせ24件のうち一致20・不一致3・未確認1）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-html_check_tool.md`。

最も重いのは3件。①**出典 `:24` の「HTML4.01で省略可能と規定されているタグについても、省略を許可しない」が実装と食い違う**こと。`head`・`body`・`tbody` は要素ごと省略できる（`Html4.jj:677, 2329` と実測）。②**構文エラー時の最上位メッセージ `syntax check failed. file = [...]` を表が落としていた**こと。`Parse error ...` は原因例外側にしか出ず（`Html4HtmlChecker.java:91-99`）、構文エラーではファイル名が最上位行にしか出ない。表を2段に分けた。③**画面をHTML5で記述しているプロジェクトでは本ツールを使用できない**こと。Nablarchのサンプルアプリケーション自身が `checkHtml` を `false` にしている（`nablarch-example-web/src/test/resources/unit-test.xml:49-51`）。

不採用のうち最も重いのは、QA観点の「HTMLダンプの文字コードがUTF-8以外だと字句エラーになる」である。`Html4HtmlChecker` を実際に動かして確認したところ、Shift_JISで保存した日本語入りHTMLは通る。UTF-8デコーダが不正バイトをU+FFFDに置換し、置換後の文字がテキスト内容として文法上受理されるためで、主張が成り立たない。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-html_check_tool.md`「判断待ち」に2件。**①`checkHtml`・`htmlChecker`・`htmlCheckerConfig` の説明を本ページと `web.rst` のどちらに置くか**（`design.md:360` の「ツール利用者が1箇所で完結できることを優先」と `design.md:522` の「承認済みページが同じ事実を持つ場合は `:ref:`」が逆を向く）。**②承認済みの `setup/request_unit_test/web.rst:154-155` のXML例が旧レイアウトのパスのままで、同ページ `:70` のデフォルト値と食い違う**。承認済みページのため本タスクでは触れていない。

## `#27-07` 取引単体テスト（RESTfulウェブサービス）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/rest.rst`（60行。ラベル `deal_unit_test_rest`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/03_DealUnitTest/rest.rst`（削除済み。`git show 2e501ad:<path>` で参照）の `:4-8`・`:11-37`。2行とも `MERGE`。`DROP`・`REFERENCE` なし
**参照実装**: `nablarch-testing-rest`（`9ada31e`）、`nablarch-example-web`（`ProjectUpdateForm` の実在確認）
**個別指示**: `ntf-doc-27-small-3rd.md` §1・§2・§6
**レビュー記録**: `reviews/page-deal_unit_test_rest.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../implementation/deal_unit_test/rest.rst` の1件。記録3本（`reviews/page-deal_unit_test_rest.md`・本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`Loaded 597 rows` / `12986` / `11983` / `OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。是正を全件畳んだ後の最終本文で実行し、全ログを `grep -i 'warning\|error'` して確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。あわせて `本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`既定`・`デフォルト設定`、および用語集が0件を求める `テストケース`（`glossary.md:556`）も0件。です・ます 0件、`.. note::`／`.. warning::` 0件（`tip` 1件・`important` 0件） |
| G7 | **PASS** | ページ先頭ラベル `deal_unit_test_rest` が `mapping/style.md:381` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 50（表示幅39）・L2 50（8）×2・L3 49（24）。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件 |
| G9 | **PASS** | `:ref:` 3件。飛び先はいずれも実在する（`request_unit_test_rest` = `implementation/request_unit_test/rest.rst:1`、`testdata_notation` = `implementation/testdata_notation.rst:1`、`deal_unit_test_setting_rest` = `setup/deal_unit_test/rest.rst:1`）。リンク文字列3件とも飛び先ページのタイトルと一致。**ただし `request_unit_test_rest` は4行のスタブである**（`decide-2`） |
| G10 | **PASS** | 出典 `:4-8`・`:11-37` の非空行を全件分類し、落とした行は0件。対応は `reviews/page-deal_unit_test_rest.md`「出典行の消化」に記載 |
| G11 | **PASS** | `disposition=REFERENCE` の行なし（2行とも `MERGE`） |
| G12 | **PASS** | 同じ出典ファイルの `:40-95`（`current-0150`〜`0152`）は `dest_page = 取引単体テストの設定（RESTfulウェブサービス）` で第2部の作成済みページが持つ。本ページは本文を持たず tip から `:ref:` で送るだけにした。`mapping_id` に枝（`-a`／`-b`）は無い |
| G13 | **対象外** | `.. image::` 0件 |

### 個別指示の追加ゲート（`ntf-doc-27-small-3rd.md` §6）

| | 結果 | 根拠 |
|---|---|---|
| S1 | **PASS** | L2は `機能概要`・`使用方法` の2つのみ（下線行の機械抽出） |
| S2 | **PASS** | L3は `テストメソッドを作成する` の1つのみで、`ntf-doc-27-small-3rd.md:60-67` の構成図と一致 |
| S3 | **対象外** | `#27-11` 向けのゲート |
| S4 | **対象外** | 本ページに `REFERENCE` 行なし |
| S5 | **PASS** | G9 と同じ（飛び先3件が実在し、リンク文字列が飛び先の見出しと一致） |
| S6 | **対象外** | `#27-15` 向けのゲート |
| S7 | **PASS** | `reviews/page-deal_unit_test_rest.md` を作成し、§1-1 のアウトライン適用の `decide` を `decide-1` として1回だけ記録した。`#27-10`・`#27-11`・`#27-15` はここを指す |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（QA 高2・中5・低3、設計 高2・中4・低6、クラフト 高2・中8・低8、検証は8項目すべて PASS）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-deal_unit_test_rest.md`。

最も重いのは3件。①**出典 `:7` の「リクエスト毎のテストを連続実行する」がテストメソッドを複数並べる読み方を許し、同じページの機能概要・使用方法と食い違っていた**こと。出典自身のコード例が1つのテストメソッドで3リクエストを送っており、`defaultProcessor.reset()` も各テストメソッドの開始時に呼ばれる（`SimpleRestTestSupport.java:96,103`）ため、実装に合わせた。②**コードブロックが出典のまま4字下げで `style.md` S-05 違反だった**こと。NTF解説書の新規ページ123件のコードブロックのうち122件が2字下げで、本ページが唯一の例外だった。③**末尾の tip が承認済みページの手順を書き写し、かつ実装に無い排他性を作っていた**こと。`sendRequest(HttpRequest, RequestResponseProcessor)`（`SimpleRestTestSupport.java:197`）が公開されており「コンポーネント設定ファイルに登録する以外に方法が無い」とは言えない。導線だけに削った。

不採用のうち最も重いのは、クラフト観点の「L3見出しを『1つのテストメソッドで複数のリクエストを送る』に改めよ」である。`ntf-doc-27-small-3rd.md:66` が `テストメソッドを作成する` と確定させ、同 `:194`（S2）が構成図との一致をゲートにしているため、個別指示を優先した。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-deal_unit_test_rest.md`「判断待ち」に3件。**①第3部に `style.md` S-02 の「出典が無い場合は見出し自体を置かない」を適用したこと**（`#27-10`・`#27-11`・`#27-15` にも及ぶ。規約本体に第3部の但し書きを足すかは未決）。**②`:22` の `:ref:` の飛び先 `implementation/request_unit_test/rest.rst` が現時点で4行のスタブであること**（`ntf-doc-27-small-3rd.md:44` の「参照先は先に作ってある」という前提が `#27-07`→`#27-12` には成立していない。`steering.md:590,595` で実測）。**③第2部 `setup/deal_unit_test/rest.rst` から本ページへの `:ref:` が無いこと**（承認済みページの変更を伴うため触れていない）。

## `#27-08` 取引単体テスト（Nablarchバッチアプリケーション）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/batch.rst`（487行。ラベル `deal_unit_test_batch`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/03_DealUnitTest/batch.rst`（削除済み。`git show 2e501ad:<path>` で参照。183行）の `:4-7`・`:8-25`・`:28-32`・`:35-41`・`:44-48`・`:51-79`・`:82-146`・`:149-183`。8行（`SPLIT` 2・`MOVE` 6）、`lines` 合計168行。`DROP`・`REFERENCE` なし
**参照実装**: `nablarch-testing`（`e21bf67`。作業指示 §4-2 の固定コミット）
**個別指示**: 無し（`ntf-doc-27-small-3rd.md:1` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15`）
**レビュー記録**: `reviews/page-deal_unit_test_batch.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../implementation/deal_unit_test/batch.rst` と `?? .rn/.../reviews/page-deal_unit_test_batch.md` の2件。記録3本（レビュー記録・本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。S-10 の構成を組み替えた後の最終本文で実行した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。あわせて `本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`既定`・`デフォルト設定`、および用語集が0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）も0件。です・ます 0件、`.. note::`／`.. warning::` 0件（`tip`・`important` とも0件） |
| G7 | **PASS** | ページ先頭ラベル `deal_unit_test_batch` が `mapping/style.md:383` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 50（表示幅48）・L2 50（8）×2・L3 49（22〜24）×3・L4 49（14〜15）×2。承認済み `testdata_notation.rst` の実測則（L1 `max(50,表示幅)`／L2 50固定／L3・L4 `max(49,表示幅)`）からの逸脱0件 |
| G9 | **PASS** | `:ref:` 5件。飛び先はいずれも実在する（`request_unit_test_batch` = `implementation/request_unit_test/batch.rst:1`、`testdata_notation` = `implementation/testdata_notation.rst:1`、`testdata_notation-test_shots` = 同 `:350`、`testdata_notation-group_id` = 同 `:248`、`testdata_examples` = `implementation/testdata_examples.rst:1`）。リンク文字列5件とも飛び先のタイトル／見出しと一致（`testdata_notation.rst:3,352,250`・`testdata_examples.rst:3`・`request_unit_test/batch.rst:3` で照合）。**ただし `request_unit_test_batch` は4行のスタブである**（`decide-6`） |
| G10 | **PASS** | 出典8区間の非空行を全件分類し、落とした行は0件。対応は `reviews/page-deal_unit_test_batch.md`「出典行の消化」に `mapping_id` ごとの反映先行番号つきで記載 |
| G11 | **PASS** | `disposition=REFERENCE` の行なし（`SPLIT` 2・`MOVE` 6） |
| G12 | **PASS** | 出典ファイル `03_DealUnitTest/batch.rst` の全行が本ページの `dest_page` に割り当てられており、他ページと分け合っていない（`mapping.csv` を `src_file` で絞って確認）。`current-0128` の枝 `-a`／`-b` は `:4-7`／`:8-25` で重ならない |
| G13 | **対象外** | `.. image::` 0件 |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（QA 11件、設計 10件、クラフト 13件、検証は G10 が FAIL＋3件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-deal_unit_test_batch.md`。

最も重いのは3件。①**`style.md` S-10 規約3 違反**（設計）。初版は「1つの読み込み単位にまとめる／複数の読み込み単位に分割する／1つの読み込み単位に複数のテストを含める」の3つをL4見出しにし、各L4の中で Excel と YAML を太字で切り分けていた。規約3 は形式別のL4対をL3の末尾2つに1組だけ置くと定めており、承認済みの `testdata_examples.rst:500-573` も同じ形をしている。**L3 `テストデータを作成する` を形式別L4対1組に組み替え、3つのパターンは各L4内の太字ラベル（S-10 太字の例外1）に落とした。** 形式に依存しない説明はL3の導入の箇条書きへ上げた（S-11）。②**必須カラム `diConfig`・`userId` の欠落**（検証で G10 FAIL）。`TestShot.java:385-387` の `REQUIRED_COLUMNS` は6カラムを必須とし、出典の表はこの2つを持たない。全7表に追記した（`design.md` §8「出典が欠く実装上必須の設定は追記可」）。③**import のパッケージ誤り**。出典 `:92` は `nablarch.test.core.messaging.BatchRequestTestSupport` だが、`nablarch-testing@e21bf67` に当該クラスは存在せず `nablarch.test.core.batch` にある。承認済みの `setup/junit5_extension.rst:40` とも一致させた。

不採用のうち最も重いのは、クラフト観点の「3つの記述パターンをそれぞれL3に昇格し、各L3に形式別L4対を持たせよ」である。`testdata_examples.rst:500-573` と完全に同形になるが、`design.md:281-296` のアウトラインに無いL3が3つ増え、目次に `Excel形式の場合` が3回並ぶ。S-10 規約3 が「同じL3内でExcel/YAMLの記述方法の説明が複数の話題にわたる場合も、2組目の見出し対を作らず、その1組の下にまとめる」と明記しているため、規約の明文を優先した。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-deal_unit_test_batch.md`「判断待ち」に6件。**①`使用方法` 配下のL3を出典に合わせて3つにし、`テストを実行する`・`テスト結果を確認する` を立てなかったこと**（`ntf-doc-27-small-3rd.md` §1-1 と同じ判断だが、同 `:1` の対象に `#27-08` は入っていない。`#27-07` の `decide-1` と同じ論点）。**②分割例と非分割例で `expectedTable` の有無が違い、検証範囲が異なること**（`TestShot.java:193-213`。出典どおりに写し、本文で触れていない）。**③`setUpTable: default` が全テストショットに付いており、テストショットごとにDBが再投入されること**（`TestShot.java:149-162`。取引を通しで検証するという趣旨と読み合わせると説明が要るが、出典に無い）。**④`expectedStatusCode` が出典では `100`、承認済み `testdata_examples.rst:500-573` では `"0"` で食い違うこと**（どちらが正しいかは未確認）。**⑤`expectedTable: fileInputBatch`（出典 `:76`）に対応するデータブロックが出典にも本ページにも無いこと**。**⑥`:20` の `:ref:` の飛び先 `implementation/request_unit_test/batch.rst` が現時点で4行のスタブであること**（本ページはテストの実行方法を全面委譲している。`#27-07` の `decide-2` と同じ論点）。
