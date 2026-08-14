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

## `#27-09` 取引単体テスト（MOMによるメッセージング）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/mom.rst`（129行。ラベル `deal_unit_test_mom`。`#27-00` の4行スタブへの追記）＋画像4枚の `git mv`
**出典**: `05_UnitTestGuide/03_DealUnitTest/` の `real.rst:4-36`・`delayed_receive.rst:4-7`・`delayed_send.rst:4-7`・`send_sync.rst` の `:6-46`・`:50-63`・`:173-198`・`:224-276`（いずれも削除済み。`git show 2e501ad:<path>` で参照）。7行（`MOVE` 4・`SPLIT` 1・`REFERENCE` 2）、`lines` 合計175行
**参照実装**: `nablarch-testing`（`e21bf67`。作業指示 §4-2 の固定コミット）
**個別指示**: 無し（`ntf-doc-27-small-3rd.md:1` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15`）
**レビュー記録**: `reviews/page-deal_unit_test_mom.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../implementation/deal_unit_test/mom.rst`、画像4枚の `R`（rename）、`?? .rn/.../reviews/page-deal_unit_test_mom.md` のみ。記録3本（レビュー記録・本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:23` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。画像4枚の移動後の最終本文で実行した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`既定`・`デフォルト設定`、用語集が0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）も0件。です・ます 0件。`.. note::`／`.. warning::` 0件（`.. tip::` 1件・`.. important::` 0件）。**`以下の` が `:89` に1件あるが、これは私の自主チェック語であって規約の禁止語ではない**（承認済み `setup/deal_unit_test/mom.rst:17`・`testdata_notation.rst:44,140,206,364` に用例あり）。あわせて `glossary.md:130-160` の揺れ表記（`同期応答メッセージ送信処理`・`同期応答メッセージ受信処理`・`応答不要メッセージ受信処理`・`応答不要メッセージ送信処理`・`メッセージ受信処理`・`メッセージ同期送信`・`バッチ処理`）を grep して0件 |
| G7 | **PASS** | ページ先頭ラベル `deal_unit_test_mom` が `mapping/style.md:384` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 50（表示幅41）・L2 50（8）×2・L3 49（16〜22）×4・L4 0件。承認済み `batch.rst`・`rest.rst` の実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L2 下線の直後の空行あり（2箇所）、L3 下線の直後は空行なし（4箇所）で、`batch.rst:13-15`・`rest.rst:13-15` と同型 |
| G9 | **PASS** | `:ref:` 6件（うち `deal_unit_test_batch` は2回）。飛び先はいずれも実在する（`deal_unit_test_setting_mom` = `setup/deal_unit_test/mom.rst:1`、`deal_unit_test_batch` = `implementation/deal_unit_test/batch.rst:1`、`deal_unit_test_web` = `implementation/deal_unit_test/web.rst:1`、`testdata_notation-messaging_data` = `implementation/testdata_notation.rst:1148`、`testing_framework_common-send_sync_test_data` = `setup/common.rst:118`）。リンク文字列は6件とも飛び先の直後の見出しと一致（各ラベルの次行を読んで照合）。`:java:extdoc:` 1件（`nablarch.test.core.messaging.MessagingRequestTestSupport`。`e21bf67` の `MessagingRequestTestSupport.java:1,48` に実在）。**ただし `deal_unit_test_web` は4行のスタブである**（`decide-4`） |
| G10 | **PASS** | 出典7区間の非空行を全件分類した。落とした行は4件（`send_sync.rst:44-45` の脚注 `[#f1]`、`send_sync.rst:195` のラベル定義、`delayed_send.rst:4-7` 全体、ログ出力例の接頭辞）で、いずれも `reviews/page-deal_unit_test_mom.md`「出典から変えた点」に D-1〜D-4 として理由つきで記載。反映先の行番号は同「出典行の消化」に `mapping_id` ごとに記載 |
| G11 | **PASS** | `disposition=REFERENCE` は2件（`current-0135`・`current-0136`）。どちらも節にしていない。`current-0135` は `:15` の末尾の一文に畳み、`current-0136` は `design.md:119` により反映しない |
| G12 | **PASS** | `send_sync.rst` は6ページで分け合うが、割当区間 `:1-2`・`:6-46`・`:50-63`・`:67-172`・`:173-198`・`:199-220`・`:224-276`・`:280-297`・`:298-360`・`:361-383` に重なりはない（`mapping.csv` を `src_file` で絞って確認）。本ページが受け持つのは `:6-46`・`:50-63`・`:173-198`・`:224-276` の4区間のみ。**`:221-223` はどの `mapping_id` にも割り当てられていない**（旧ページの「要求電文のログ出力」見出し。本ページの `:87-88` が同じ役割を果たす） |
| G13 | **PASS** | `.. image::` 4件。`guide/development_guide/05_UnitTestGuide/03_DealUnitTest/_images/` から `implementation/deal_unit_test/images/mom/` へ `git mv` した（`design.md:897,907`）。`git status` は4件とも `R` として記録している。移動元を参照していた `en/` 側は `en/.../_images/` の別コピーを参照しており、ja 側の移動で壊れる参照は0件（`grep -rn` で確認）。`:scale:` は出典どおり（70／70／90／70） |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（採った是正14件、採らなかった指摘2件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-deal_unit_test_mom.md` §6。

最も重いのは3件。①**「モックアップクラスは返す応答電文を `no` の値で選ぶ」が実装と食い違う**（QA）。実装は `SendSyncSupport.java:288` の `getRecords().get(info.no - 1)` であり、選択はレコードの並び順で決まる。`no` は `Excel` 形式のラベル列であって `YAML` 形式には無く、承認済み `testdata_notation.rst:1156` も「対応付けは、連番の値ではなく記述した順序で行われる」と述べている。**「記述した順に応答電文を1件ずつ返す」に書き改めた**（`design.md` §8）。②**用語集の揺れ表記を全面的に使っていた**（クラフト）。初版は「同期応答メッセージ送信処理」「同期応答メッセージ受信処理」「応答不要メッセージ受信処理」「メッセージ受信処理」「バッチ処理」を使っており、`glossary.md:134,155,156,157` がいずれも揺れ表記としている。正表記に置き換え、受信側を指す「メッセージ受信処理」は応答不要受信と区別できないため「メッセージを受信するアプリケーション」と言い換えた。③**読み込み単位の説明が誤っていた**（クラフト・設計）。初版は「読み込み単位の名前をリクエストIDと一致させる」と書いていたが、`glossary.md:241` の定義では読み込み単位は `Excel` 1シート／`YAML` 1ファイルであり、リクエストIDの名前を持つのはファイル／ディレクトリの側で、読み込み単位の名前は固定の `message` である（`testdata_notation.rst:1154,1251`）。`:68` を書き直した。

不採用のうち重いのは、クラフト観点の「L3 `テストを実行する` を `複数回の同期送信に応答電文を対応付ける` に改名せよ」である。中身が実行手順ではなく実行時の動作である以上もっともな指摘だが、`design.md:281-296` が第3部の節名を5つに固定している。**節名は型に従い、代わりに `:77` の冒頭を「その回数分の応答電文をテストデータに記述する」という読者の作業から書き起こして、節名と中身のずれを詰めた。**

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-deal_unit_test_mom.md` §7 に6件。**①`YAML` 形式でテストデータの再読み込みが働かない疑い（未確認）**。実装は `getFileIfExists(sendSyncTestData, requestId)` で得た `File` の `lastModified()` を比較しており（`SendSyncSupport.java:348,361`）、`YAML` 形式ではこれがディレクトリになると読める（`setup/common.rst:216` が `fileExtensions` への `sendSyncTestData` 登録を禁じているため）。ディレクトリの最終更新日時は配下のファイルを上書き編集しても変わらないことをこの環境で実測した。ただし `FilePathSetting` の原本はルール §1-9 の範囲外にあり確認していない。**本体の不具合が疑われるため作業指示 `:69` に従い本文には書いていない。** **②`:77` の図が `Excel` 形式のものしかないこと**（`YAML` の図は作れない。`style.md` S-10 に規定がなく NTF 内に前例0件）。**③L3 `テストを実行する` の節名を型どおりに残したこと**（上記の不採用）。**④`:40`・`:62` が送信側のテストクラスの説明を `deal_unit_test_web` に委ねているが、その飛び先が現時点で4行のスタブであること**（`#27-11` への申し送り。`#27-07` の `decide-2`・`#27-08` の `decide-6` と同じ論点）。**⑤`MockMessagingContext` の未反映の実装事実**（`receiveMessage` は `UnsupportedOperationException`、`close()` は何もしない。出典にも `mapping.csv` の割当にも無い）。**⑥移行元 `03_DealUnitTest/_images/` に残る9枚の後始末**（ja 側からの参照0件。第3部の移行完了時にディレクトリごと削除するか判定する）。

## `#27-10` 取引単体テスト（HTTPメッセージング）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/http_messaging.rst`（30行。ラベル `deal_unit_test_http_messaging`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst`（削除済み。`git show 2e501ad:<path>` で参照。69行）の `:6-15`（`current-0138`・`REFERENCE`）・`:24-46`（`current-0139`・`MERGE`）。`lines` 合計33行
**参照実装**: `nablarch-testing`（`e21bf67`。作業指示 §4-2 の固定コミット）
**個別指示**: `ntf-doc-27-small-3rd.md` §1・§3・§6
**レビュー記録**: `reviews/page-deal_unit_test_http_messaging.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../implementation/deal_unit_test/http_messaging.rst` と `?? .rn/.../reviews/page-deal_unit_test_http_messaging.md` の2件。記録3本（レビュー記録・本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:21` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし（`git diff --stat` が空） |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。4観点の是正を全件畳んだ後の最終本文で実行し、全ログを `grep -i 'warning\|error'` して確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`既定`・`デフォルト設定` も0件。です・ます 0件。`.. note::`／`.. warning::`／`.. tip::`／`.. important::` いずれも0件。用語集の揺れ表記（`HTTP同期応答メッセージ送信`・`同期応答メッセージ送信処理`・`メッセージング処理`・`メッセージ同期送信`・`メッセージ受信処理`・`バッチ処理`）と、0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）も0件 |
| G7 | **PASS** | ページ先頭ラベル `deal_unit_test_http_messaging` が `mapping/style.md:382` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 50（表示幅36）・L2 `:13` `:20` 50（8）×2・L3 `:25` 49（22）×1・L4 0件。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L2 下線の直後は空行あり、L3 下線の直後は空行なしで、承認済み `mom.rst`・`batch.rst`・`rest.rst` と同型。行末空白0件 |
| G9 | **PASS** | `:ref:` 5件（`deal_unit_test_mom` は2回）。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する（`deal_unit_test_setting_http_messaging` = `setup/deal_unit_test/http_messaging.rst:1`／見出し `:3`、`deal_unit_test_mom` = `implementation/deal_unit_test/mom.rst:1`／`:3`、`testdata_notation-messaging_data` = `implementation/testdata_notation.rst:1148`／`:1150`、`testing_framework_common-send_sync_test_data` = `setup/common.rst:118`／`:120`、`testdata_examples` = `implementation/testdata_examples.rst:1`／`:3`）。各ラベルの次行を読んで照合した。飛び先5件はいずれも承認済みの本文を持つページであり、スタブは0件 |
| G10 | **PASS** | 出典の非空行16行を全件分類した。落とした行は7件（`:31`・`:32`・`:34`・`:36`・`:37`・`:40`・`:41`）で、いずれも `reviews/page-deal_unit_test_http_messaging.md` §5 に D-1・D-2 として理由つきで記載。残りはすべて反映済みで未消化0行 |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0138` の1件。節にしていない。同行の本文は `:10`（リード文）・`:15`（モックアップクラスと第2部への導線）・`:17`（機能は MOM と同じ・語の読み替え）・`:22`（進め方の参照先）に畳んでおり、`使用方法` 配下のL3は `テストデータを作成する` の1本のみ |
| G12 | **PASS** | 出典ファイル `03_DealUnitTest/http_send_sync.rst` を `dest_page` に持つ行は `current-0137`（`:1-2`・DROP）・`current-0138`（`:6-15`）・`current-0139`（`:24-46`）・`current-0140`（`:50-69`・第2部）の4件のみで、区間に重なりはない（`csv.DictReader` で `src_file` を絞って確認）。`mapping_id` に枝（`-a`／`-b`）は無い |
| G13 | **対象外** | 本文の `.. image::` 0件。出典が持つ画像1枚は §5 D-1 の理由で採らなかった（`decide-2`）。`git mv` していないため移動元 `guide/development_guide/05_UnitTestGuide/03_DealUnitTest/_images/http_send_sync_test_data.png` はそのまま残っている（`#27-09` の `decide-6` と同じ後始末の対象） |

### 個別指示の追加ゲート（`ntf-doc-27-small-3rd.md` §6）

| | 結果 | 根拠 |
|---|---|---|
| S1 | **PASS** | L2は `機能概要`（`:12`）・`使用方法`（`:19`）の2つのみ（下線行の機械抽出） |
| S2 | **PASS** | L3は `テストデータを作成する`（`:24`）の1つのみで、`ntf-doc-27-small-3rd.md` §3 のセクション構成図と一致 |
| S3 | **対象外** | `#27-11` 向けのゲート |
| S4 | **PASS** | `current-0138`（`REFERENCE`）の本文を節として起こしていない（G11 と同じ根拠） |
| S5 | **PASS** | G9 と同じ（飛び先5件が実在し、リンク文字列が飛び先の見出しと一致） |
| S6 | **対象外** | `#27-15` 向けのゲート |
| S7 | **PASS** | `reviews/page-deal_unit_test_http_messaging.md` を作成した。§1-1 のアウトライン適用の `decide` は `#27-07` の記録（`reviews/page-deal_unit_test_rest.md` §5 D-1・§7 decide-1）を指す旨を同記録 §7 decide-1 に書いた |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘計27件、採った是正11件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-deal_unit_test_http_messaging.md` §6。

最も重いのは3件。①**「テスト結果の確認方法は MOM によるメッセージングと同じである」が誤りだった**（QA・設計・クラフトが独立に指摘）。飛び先の `mom.rst:87-129` は `MESSAGING_MAP`・`MESSAGING_CSV` へ `DEBUG` レベルで出す Map形式・CSV形式のログの説明で構成されているが、これらは HTTPメッセージングでは出力されない。Map形式・CSV形式のログは `SendSyncSupport#parseRequestMessage` 経由でのみ出力され、`MockMessagingClient` は同メソッドを呼ばない（`grep` の結果0件）。`MockMessagingClient` は `MESSAGING` ロガーへ `logInfo` で要求電文・応答電文を出すだけである（`MockMessagingClient.java:37,52,89,149-154`）。`:22` に差分を明記した。②**「応答のステータスコードを指定する場合にかぎり、ヘッダのデータブロックを設ける」が誤りだった**（QA）。`RESPONSE_HEADER_MESSAGES` に記述したカラムはステータスコードに限らず、そのまま応答電文のヘッダとしてアプリケーションへ渡る（`MockMessagingClient.java:70` 読み込み、`:86` `setHeaderRecord`）。③**出典 `:44` の「HTTPはフレームワーク制御ヘッダが無いため」という前提が誤りだった**（クラフト）。`ja/application_framework/application_framework/libraries/system_messaging/http_system_messaging.rst:197-198` が「フレームワーク制御ヘッダを使用するか否かは任意に選択できる」と述べている。前提を落として結論だけを書いた。

不採用のうち最も重いのは、クラフト観点の「『通信先』は用語集に無い造語であり『外部システム』に置き換えよ」である。`glossary.md:158,160` が同じ対象を「外部システム」と呼んでおり、`ja/` 配下で「通信先」を使うのは本ページだけであることも実測した。それでも採らなかったのは、出典 `:11` が「『送信キュー』『受信キュー』は『通信先』と読み替える」と明記し、個別指示 `ntf-doc-27-small-3rd.md` §3 判断1 も「通信先」の語で読み替えを指示しているためである。**`decide-3` として上げる。**

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-deal_unit_test_http_messaging.md` §7 に5件。**①第3部へのアウトライン適用**（`#27-07` の `decide-1` を指す）。**②Excel記載例の画像 `_images/http_send_sync_test_data.png` を落としたこと**。個別指示 `ntf-doc-27-small-3rd.md:102` の既定（判断がつかない場合は `git mv` して残す）とは逆の選択である。理由は、画像内の要求電文ブロック（吹き出し「要求電文はフォーマットのみ定義する。」）が `MockMessagingClient` の読まないデータブロックであること（`MockMessagingClient.java:48-91` に `EXPECTED_REQUEST_*` の参照なし）と、応答電文側の内容は `testdata_examples.rst:1800,1859` が Excel形式・YAML形式の両方で既に持っていることの2点。**③「通信先」の語を使ってよいか**（上記の不採用）。**④`testdata_notation.rst:1251` の申し送り**。同行は取引単体テストのモックアップクラス全般について「要求電文はログ出力用のフォーマットのみを定義する」と書いており、HTTPメッセージングには当てはまらない。承認済みページのため触れていない。**⑤`HttpMessagingClient.SYNCMESSAGE_STATUS_CODE` の定数値が未確認であること**（`nablarch-fw-messaging` はルール §1-9 の作業ディレクトリ外）。本文でカラム名を名指ししていないため本ページの記述には影響しない。

## `#27-11` 取引単体テスト（ウェブアプリケーション）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/web.rst`（56行。ラベル `deal_unit_test_web`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/03_DealUnitTest/index.rst` の `:6-13`（`current-0142`）・`:16-23`（`current-0143`）・`:26-33`（`current-0144`）・`:36-46`（`current-0145`）と、`05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst` の `:27-39`（`current-0059`）。いずれも削除済みで `git show 2e501ad:<path>` で参照。5行すべて `MOVE`、`lines` 合計48行
**参照実装**: 無し（手動テストのページであり、テスティングフレームワークのクラスを説明していない）
**個別指示**: `ntf-doc-27-small-3rd.md` §1・§4・§6
**レビュー記録**: `reviews/page-deal_unit_test_web.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は ` M ja/.../implementation/deal_unit_test/web.rst` と `?? .rn/.../reviews/page-deal_unit_test_web.md` の2件。記録3本（レビュー記録・本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:19` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし（`git status --porcelain` 全件に現れない） |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。4観点の是正を全件畳んだ後の最終本文で実行し、コンテナ内で `grep -i 'warning\|error\|build succeeded'` を通して警告本文まで確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`既定`・`デフォルト設定` も0件。です・ます 0件。`.. note::`／`.. warning::` 0件（`.. tip::` 2件・`.. important::` 0件）。用語集が0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）0件。揺れ表記（`同期応答メッセージ送信処理`・`メッセージ同期送信`・`メッセージング処理`・`バッチ処理`・`Webアプリケーション`）0件。出典の社内用語 `打鍵` も0件（`reviews/page-deal_unit_test_web.md` D-3） |
| G7 | **PASS** | ページ先頭ラベル `deal_unit_test_web` が `mapping/style.md:380` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 50（表示幅40）・L2 `:13` `:18` 50（8）×2・L3 `:23` `:31` `:38` `:48` 49（16・16・32・32）×4・L4 0件。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L2 下線の直後は空行あり、L3 下線の直後は空行なしで、承認済み `mom.rst`・`batch.rst`・`rest.rst`・`http_messaging.rst` と同型。行末空白0件 |
| G9 | **PASS** | `:ref:` 3件。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する（`deal_unit_test_mom` = `implementation/deal_unit_test/mom.rst:1`／見出し `:3`、`deal_unit_test_http_messaging` = 同 `http_messaging.rst:1`／`:3`、`request_unit_test_web` = `implementation/request_unit_test/web.rst:1`／`:3`）。各ラベルの次行を読んで照合した。**ただし `request_unit_test_web` は4行のスタブである**（`decide-3`）。`:java:extdoc:` 0件 |
| G10 | **PASS** | 出典5区間の非空行16行を全件分類した。**未消化0行。** 反映先の行番号は `reviews/page-deal_unit_test_web.md` §2 の対応表に1行ずつ記載。出典から変えた点は同 §5 に D-1〜D-15 として理由つきで記載 |
| G11 | **PASS（対象外）** | 本ページに割り当てられた5行はすべて `disposition=MOVE`。`REFERENCE` 行は0件 |
| G12 | **PASS** | `mapping.csv` を `csv.DictReader` で読み、`03_DealUnitTest/index.rst`（`current-0141`〜`current-0146`）と `02_RequestUnitTest/double_transmission.rst`（`current-0057`〜`current-0059`）の全行の `src_body_start`／`src_body_end` を並べて重なりが無いことを確認した。**`current-0057`（`double_transmission.rst:6-12`。サーバサイドとクライアントサイドで機能するためテスト方法が異なる、という説明）は `リクエスト単体テスト（ウェブアプリケーション）` へ `MERGE` 済みであり、本ページは再掲せず `:49` の `:ref:` で送っている。** `index.rst:47-56` は `:34-43` と1バイト違わない重複節で、`current-0146`（`dest_page` 空・`DROP`）として除外済み。本ページには1回だけ書いている |
| G13 | **PASS（対象外）** | `.. image::` 0件 |

### 個別指示 §6 のゲート（S1〜S7）

| | 結果 | 根拠 |
|---|---|---|
| S1 | **PASS** | L2 は `機能概要`（`:12`）・`使用方法`（`:17`）の2つのみ |
| S2 | **PASS** | L3 は `テストを準備する`（`:22`）・`テストを実施する`（`:30`）・`テスト結果のエビデンスを取得する`（`:37`）・`二重サブミット防止機能を確認する`（`:47`）の4本。`ntf-doc-27-small-3rd.md:129-132` の構成図と文言・順序まで一致。出典に無いL3は0件 |
| S3 | **PASS** | **`grep -n "テストクラス\|テストメソッド" web.rst` が0件。** 手動テストのページであり、`ntf-doc-27-small-3rd.md:110`「書けない。書かない」に従っている |
| S4 | **PASS（対象外）** | `REFERENCE` 行を持たない（G11 と同じ） |
| S5 | **PASS** | G9 と同じ。3件とも実ファイルを開いてラベルの定義位置と直後の見出しを確かめた |
| S6 | **対象外** | `#27-15` 専用 |
| S7 | **PASS** | `reviews/page-deal_unit_test_web.md` を作成した。`ntf-doc-27-small-3rd.md` §1-1（出典に無いL3を第3部に適用する件）の `decide` は `reviews/page-deal_unit_test_rest.md` §5 D-1／§7 decide-1 に1回だけ記録済みで、本記録の冒頭からそこを指している |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘25件、本文への是正8件、不採用3件、`decide` へ回した3件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-deal_unit_test_web.md` §6。

最も重いのは3件。①**リード文の「テスティングフレームワークを使った自動実行は行わない。」が規約違反だった**（QA）。`design.md:117` が「『JUnitでの自動実行はできず』のような不可能性の記述は書かない」と明文で禁じており、`design.md:96` の走査2 が出典8ファイルに0件であることを実測している。対比材料の `03_DealUnitTest/batch.rst:5` はバッチが自動であることを述べるだけで、ウェブが自動でないことは述べていない。**第2文を削除した。** 設計観点が挙げた「`JUnitによる自動実行は行わない` に直す」案も同じ不可能性の記述であるため採らなかった。②**機能概要がリード文と使用方法の再掲だけになっていた**（設計・クラフトが独立に指摘）。初版の機能概要1文目は、リード文・使用方法の箇条書き・承認済み `about/index.rst:77` と合わせて同じ事実が4か所にあった。**機能概要を削り、デプロイの記述はリード文に統合した**（`design.md:678` の②「重複がない」）。③**エビデンスの表記が承認済みページと不一致で、同一ページ内でも割れていた**（QA・設計・クラフトの3観点が独立に指摘）。初版は本文を「画面のハードコピー」「データベースのダンプ」に書き換えていたが、`glossary.md` §8 の対応表にその置き換えを求める行は無く、承認済み `about/index.rst:75` は「画面ハードコピー・DBダンプ」である。**本文を出典と承認済みページに戻し、あわせて tip の `\ DB\ ` エスケープも外して出典と1バイト違わない形にした。**

不採用のうち重いのは、設計・クラフトの「tip1（テスト実行前のDBダンプ）を `.. important::` にせよ」である。`style.md:232-235` の `important` は「無視すると**不具合・非推奨機能の誤用・データ不整合**につながる」と結果を3つに限っており、エビデンスの取り直しはそのいずれでもない。`design.md:121` も S-06 を同じ狭さで読んで `important` を採らない判断をしている。出典 `index.rst:29` も `tip` である。**`tip` のまま残し、判断を `decide-5` に上げた。** L3「テストを準備する」「テストを実施する」が `style.md:155-156`（S-03 の内容条件「ページタイトルを足しても情報が増えない語は不可」）に反するという指摘も、`ntf-doc-27-small-3rd.md:129-132` の指定を優先して不採用とし、`decide-4` に上げた（`#27-09` の同種の指摘と同じ扱い）。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-deal_unit_test_web.md` §7 に6件。**①tip2「テスト補助ツールについては現在検討中。」を出典どおり残したこと**（`ntf-doc-27-small-3rd.md:139` の指示に従った。いつの時点の「現在」か読者に分からない）。**②`mom.rst:62` が本ページへ委譲している「テストクラスの作り方」を、本ページが受けられないこと**（S3 が0件を求めるため本ページには書けない。`mom.rst:62` の前半を落とす案を提案。承認済みページの改稿になるため自分では直していない。`#27-09` の判断待ち④の続き）。**③`:49` の `:ref:` の飛び先 `request_unit_test_web` が4行のスタブであること**（実体の `current-0057`・`current-0058` は `#27-20`。**`#27-20` への申し送り: `current-0057` を必ず本文化すること**。`#27-07` decide-2・`#27-08` decide-6・`#27-09` decide-4・`#27-10` decide-4 と同型）。**④L3 の見出し名が S-03 の内容条件に反すること**（上記の不採用）。**⑤tip1 を `important` にしなかったこと**（上記の不採用。第3部に前例が無く、ここで基準を作ることになる）。**⑥`glossary.md:201`／`:556` の断定に反例があること**（両行は「業務上のテストケースを指す用法は NTF解説書の本文に現れない」と断定しているが、本ページの出典 `index.rst:12`・`:27` は手動テストの手順であり `testShots` のエントリを指し得ない。規約ファイルは書き換えないため上申のみ）。

## `#27-12` リクエスト単体テスト（RESTfulウェブサービス）

**成果物**: `ja/development_tools/testing_framework/implementation/request_unit_test/rest.rst`（215行。ラベル `request_unit_test_rest`。`#27-00` の4行スタブへの追記）
**出典**: `06_TestFWGuide/RequestUnitTest_rest.rst` の `:10-14`（`current-0307`）・`:17-19`（`current-0308`）・`:22-46`（`current-0309`）・`:102-111`（`current-0313`）・`:114-118`（`current-0314`）・`:121-145`（`current-0315`）・`:148-195`（`current-0316`）・`:198-207`（`current-0317`）・`:210-274`（`current-0318`）と、`05_UnitTestGuide/02_RequestUnitTest/rest.rst` の `:14-52`（`current-0114`）・`:83-106`（`current-0120`）・`:109-111`（`current-0121`、REFERENCE）。いずれも削除済みで `git show 2e501ad:<path>` で参照。12行・`lines` 合計262行
**参照実装**: `nablarch-testing-rest` `9ada31e`（`RestTestSupport` / `SimpleRestTestSupport` / `RestMockHttpRequest`）、`nablarch-testing` `e21bf67`（`DbAccessTestSupport`）
**個別指示**: 無し（`ntf-doc-27-small-3rd.md` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15` のみ。本ページは作業指示 `ntf-doc-weekend-queue.md` のみに従う）
**レビュー記録**: `reviews/page-request_unit_test_rest.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は `R` 2件（画像の `git mv`）、` M ja/.../implementation/request_unit_test/rest.rst`、`?? .rn/.../reviews/page-request_unit_test_rest.md` の4件。記録2本（本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:14` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` に差分なし（`git status --porcelain` 全件に現れない） |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。4観点の是正を全件畳んだ後の最終本文で実行し、コンテナ内で `grep -i 'warning\|error\|build succeeded'` を通して警告本文まで確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`インターフェイス`・`既定`・`デフォルト設定` も0件（`上記の`・`利用者` は初版にあり、`reviews/page-request_unit_test_rest.md` D-15 で解消）。です・ます 0件。`.. note::`／`.. warning::` 0件（`.. tip::` 5件・`.. important::` 0件）。用語集が0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）0件。`glossary.md` §8 の揺れ表記（`想定結果`・`想定値`・`事前準備データ`・`セットアップデータ`・`オーバライド`・`HTML ダンプ`）0件 |
| G7 | **PASS** | ページ先頭ラベル `request_unit_test_rest` が `mapping/style.md:375` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 50（表示幅45）・L2 `:13` `:48` 50×2・L3 `:53` `:109` `:141` `:160` `:168` 49×5・L4 `:172` `:188` 49×2。実測則（L1 `max(50,表示幅)`／L2 50固定／L3・L4 `max(49,表示幅)`）からの逸脱0件。L2 下線の直後は空行あり、L3・L4 下線の直後は空行なしで、承認済み `web.rst`（第4部）・`mom.rst`・`batch.rst` と同型。行末空白0件 |
| G9 | **PASS** | `:ref:` 6件・`:doc:` 1件・`:java:extdoc:` 1件。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する（`request_unit_test_web` = `implementation/request_unit_test/web.rst:1`／見出し `:3`、`request_unit_test_setting_rest` = `setup/request_unit_test/rest.rst:1`／`:3`、`component_unit_test` = `implementation/class_unit_test/component.rst:1`／`:3`、`testdata_notation` = `implementation/testdata_notation.rst:1`／`:3`、`testdata_notation-setupdb` = 同 `:668`／`:670`、`testdata_notation-file_structure` = 同 `:22`／`:24`、`testdata_notation-list_map` = 同 `:580`／`:582`）。各ラベルの次行を読んで照合した。`:java:extdoc:` の `nablarch.fw.web.RestMockHttpRequest` は `nablarch-testing-rest@9ada31e` に `@Published` 付きで実在。**ただし `request_unit_test_web` と `component_unit_test` は4行のスタブである**（`decide-3`） |
| G10 | **PASS** | 出典12区間の非空行を全件分類した。**未消化0行。** 反映先の行番号は `reviews/page-request_unit_test_rest.md` §2-2 の対応表に1行ずつ記載。出典から変えた点は同 §5 に D-1〜D-18 として理由つきで記載 |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0121`（`05_UnitTestGuide/02_RequestUnitTest/rest.rst:109-111`）の1件。節を起こさず、`rest.rst:144` の箇条書き内の括弧書き `:ref:` に落としてある |
| G12 | **PASS** | `mapping.csv` を `csv.DictReader` で読み、`RequestUnitTest_rest.rst`（`current-0306`〜`current-0320`）と `02_RequestUnitTest/rest.rst`（`current-0113`〜`current-0122`）の全行の `src_body_start`／`src_body_end` を並べて重なりが無いことを確認した。設定関連の `current-0310`・`0311`・`0319`・`0320` は `リクエスト単体テストの設定（RESTfulウェブサービス）` へ、`current-0122` は `テストデータの書き方` へ振られており、本ページは再掲していない。`rest.rst:153-157` の3メソッドは `RestTestSupport` 固有で、`testdata_notation.rst:590-591` が挙げる `TestSupport#getListMap`／`DbAccessTestSupport#getListMap` とは別物 |
| G13 | **PASS** | `.. image::` 1件。`git mv` で `guide/development_guide/06_TestFWGuide/_images/rest_request_unit_test_structure.png` を `implementation/request_unit_test/images/rest/` へ移動（`design.md:897`・`:907`）。作図元の `.xlsx` も同時に移した（リポジトリ全体の前例: `ja/application_framework/application_framework/libraries/images/tag/images.xlsx` ほか）。`guide/` 配下に `*rest*` の残骸0件 |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘32件、本文への是正21件、不採用・判断待ち11件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-request_unit_test_rest.md` §6。

最も重いのは3件。①**出典の「内蔵サーバが起動されリクエストが送信される」が実装と一致しなかった**（検証）。内蔵サーバの起動は `@Before` の `setUp()` が行い（`nablarch-testing-rest@9ada31e` `SimpleRestTestSupport.java:84-89` → `:237-243` → `:266` の `server.startLocal()`）、しかも `static boolean initialized`（同 `:55`）で JVM 内1回に限られる。`sendRequest` は `:186` → `:197` → `:224-230` で `server.handle` を呼ぶだけである。**起動時期を実装に合わせて書き直した**（D-9）。②**ファイル配置表のパスから `src/` が抜けていた**（QA）。`readTextResource` はクラスパスから解決するため（同 `:343-347`）、`<PROJECT_ROOT>/test/resources/...` では見つからない。承認済みの `setup/request_unit_test/rest.rst:44` も `src/test/resources/unit-test.xml` と書いている。**`src/` を補った**（D-10）。ただし承認済みの `testdata_notation.rst:63` は `src/` 無しのままで、同ページ `:48` とも食い違っている（`decide-6`）。③**用語集の正表記違反が3種8箇所あった**（クラフト）。`スーパークラス`（6箇所）・`インターフェイス`（1箇所）・`期待する結果`（1箇所）で、`glossary.md:594`・`:595` はいずれも無条件置換を定めている。出典がそのまま持ち込まれたものである。**全件を正表記に直した**（D-13）。

`important` → `tip` の3箇所（D-5〜D-7）と S-10 に基づく Excel 表現の中立化（D-2）は、設計観点が妥当と判定した。クラフト観点が挙げた「`dbInfo` の tip を `important` にせよ」は、「準備しないと例外が発生する」という前提を一次情報で確認できなかったため採らず、`decide-1` に上げた。QA観点が挙げた `setBody` の追記は、出典（`06_TestFWGuide/RequestUnitTest_rest.rst:148-195`）に無い事実の追加にあたるため見送り、`decide-4` に上げた。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_unit_test_rest.md` §7 に6件。**①`dbInfo` / `testDataParser` の設定手順が解説書のどこにも書かれていないこと**（`rest.rst:61` の tip は出典どおり準備を求めるが、参照先の `setup/request_unit_test/rest.rst` は両者に触れておらず、`ja/development_tools/testing_framework/` 配下の `dbInfo` のヒットは当該1件のみ。第2部への追記要否の判断が要る）。**②構成図が本文と3点食い違うこと**（テストデータのノードが「Excelファイル」のまま／PATCH が無い／`SimpleRestTestSupport` が無い。作図元 `.xlsx` は同ディレクトリに移してあるが画像の作り直しは範囲外とした。前例は `reviews/page-deal_unit_test_http_messaging.md:79-80`）。**③`:ref:` の飛び先 `component_unit_test`・`request_unit_test_web` が4行のスタブであること**（`#27-07` decide-2・`#27-08` decide-6・`#27-09` decide-4・`#27-10` decide-4・`#27-11` decide-3 と同型）。**④`setBody` に触れていないこと**（上記の見送り。承認済み `implementation/deal_unit_test/rest.rst:43` が使用しており、同ページ `:22` は本ページを正典扱いしている）。**⑤JUnit 5 の導線が本ページに無いこと**（第1部 `about/index.rst:115` が全体を受けており、第3部の他ページも個別には張っていない。第3部全体の方針判断）。**⑥承認済み `testdata_notation.rst:63` のパス表記が `src/` 無しで、同ページ `:48` とも食い違っていること**（D-10 との揃えが要る）。

## `#27-13` リクエスト単体テスト（MOMによるメッセージング）

**成果物**: `ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst`（209行。ラベル `request_unit_test_mom`。`#27-00` の4行スタブへの追記）
**出典**: `06_TestFWGuide/RequestUnitTest_real.rst` の `:8-165`（`current-0294`〜`current-0302`）、`06_TestFWGuide/RequestUnitTest_send_sync.rst` の `:8-156`（`current-0321`〜`current-0327`・`current-0329`・`current-0330`）、`05_UnitTestGuide/02_RequestUnitTest/real.rst` の `:10-53`・`:260-320`（`current-0101`〜`current-0104`・`current-0108`〜`current-0112`）、同 `delayed_receive.rst` の `:8-47`（`current-0046`〜`current-0049`）、同 `send_sync.rst` の `:10-73`・`:292-296`（`current-0124`・`current-0125`・`current-0127`）、`input/ntf-doc-terms.md` の `:501-525`（`input-0033`・`input-0034`）。`current-*` はいずれも削除済みで `git show 2e501ad:<path>` で参照。36行・`lines` 合計461行
**参照実装**: `nablarch-testing` `e21bf67`
**個別指示**: 無し（`ntf-doc-27-small-3rd.md` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15` のみ。本ページは作業指示 `ntf-doc-weekend-queue.md` のみに従う）
**レビュー記録**: `reviews/page-request_unit_test_mom.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は `R` 4件（画像の `git mv`）、` M ja/.../implementation/request_unit_test/mom.rst`、`?? .rn/.../reviews/page-request_unit_test_mom.md` の6件。記録2本（本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:17` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を明示して `git status --porcelain` を実行し、出力0件 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。コンテナ内で `grep -i 'warning\|error\|build succeeded'` を通して警告本文まで確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`インターフェイス`・`既定`・`デフォルト設定` も0件。です・ます 0件。`.. note::`／`.. warning::` 0件（`.. tip::` 4件・`.. important::` 0件）。用語集が0件を求める `テストケース`（`glossary.md:556`）・`自動テストフレームワーク`（同 `:509`）0件。無条件置換の対象語 `メッセージ同期送信処理`（`:528`）・`主なクラス・リソース`（`:308`）0件、処理方式を指す `バッチ処理`（`:520`）0件 |
| G7 | **PASS** | ページ先頭ラベル `request_unit_test_mom` が `mapping/style.md:378` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 50（表示幅47）・L2 `:13` `:108` 50×2・L3 `:113` `:156` `:176` `:187` `:195` 49×5。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L4 未使用。L2 下線の直後は空行あり、L3 下線の直後は空行なしで承認済みページと同型 |
| G9 | **PASS** | `:ref:` 10件・`:java:extdoc:` 5件。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する。各ラベルの次行を読んで照合した一覧は `reviews/page-request_unit_test_mom.md` §4。`:java:extdoc:` の5クラスは `e21bf67` で `@Published` を確認済み。`@Published` の無い `MainForRequestTesting`・`RequestTestingMessagingProvider` は ``literal`` 表記にした。**ただし `request_unit_test_web` と `request_unit_test_batch` は4行のスタブである**（`decide-3`） |
| G10 | **PASS** | 出典36区間の非空行を全件分類した。**未消化0行。** 反映先は `reviews/page-request_unit_test_mom.md` §2-1 の対応表に記載。意図して落とした3件（D-3・D-6・D-8）は同 §5 に理由つきで記載 |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0049`（`delayed_receive.rst:42-47`）・`current-0104`（`real.rst:50-53`）・`current-0330`（`RequestUnitTest_send_sync.rst:149-156`）の3件。いずれも節を起こさず、`mom.rst:177`・`:183-184` の `:ref:` 導線に落としてある |
| G12 | **PASS** | `mapping.csv` を `csv.DictReader` で読み、隣接する `current-0126`（`send_sync.rst:77-288` → テストデータの書き方）・`current-0105`／`current-0107`（`real.rst:56-96`／`:211-253` → 同）・`current-0050`（`delayed_receive.rst:50-56` → 同）・`current-0328`（`RequestUnitTest_send_sync.rst:127-140` → リクエスト単体テストの設定（MOMによるメッセージング））と本ページ36行の `src_body_start`／`src_body_end` を並べ、重なりが無いことを確認した。`fwHeaderDefinition` の tip（`current-0299`）は `testdata_notation.rst:1154` に既載のため導線に置き換えた（D-6） |
| G13 | **PASS** | `.. image::` 4件。`git mv` で `06_TestFWGuide/_images/real_request_test_class.png`・`06_TestFWGuide/_images/send_sync.png`・`05_UnitTestGuide/02_RequestUnitTest/_image/send_sync_base.png`・同 `_image/hanrei.png` を `implementation/request_unit_test/images/mom/` へ移動（`design.md:897`・`:907`）。4点とも作図元の `.xlsx` は存在しない。`05_UnitTestGuide/02_RequestUnitTest/_image/` に残る同名の `send_sync.png` は別ページの図であり移動していない |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘45件、本文への是正26件、不採用・判断待ち19件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-request_unit_test_mom.md` §6。

最も重いのは3件。①**同期応答メッセージ送信のテストデータの格納場所が実装と逆だった**（QA）。初版は `sendSyncTestData` 配下と書いていたが、`nablarch-testing@e21bf67` の `RequestTestingSendSyncSupport.java:110-111` はテストクラスの `sheetName` から解決しており（`TestSupport.java:390` の `getBookName() + "/" + sheetName`）、`SEND_SYNC_TEST_DATA_BASE_PATH`（`SendSyncSupport.java:49`）の利用元は取引単体テストのモック3箇所に限られる。出典 `send_sync.rst:78-79` も「テストソースコードと同じディレクトリに同じ名前で格納する」としている。**書き直したうえで誤った導線を外した**（D-9）。②**テストショットと電文をグループIDで対応付ける説明が欠けていた**（QA）。`expectedMessage`・`responseMessage` の役割が本ページからも飛び先からも辿れなかったため、カラム名と対応付けを1文足して `testdata_notation-test_shots` へ導線を張った。③**図中のクラス名が実装に存在しなかった**（検証）。`send_sync.png` の `StandaloneSupportTemplate`・`BatchRequestTestSupportTemplate` は本文の表と食い違うため、tip で対応関係を示した（D-10）。

用語集の無条件置換違反4箇所（クラフト、D-11）、「処理方式」の二義使用（設計・クラフトが独立に指摘。`glossary.md:123-137` が7名称に限定しているため `mom.rst:10` を改めた）、`expectedStatusCode` の照合が結果確認の一覧から辿れないこと（QA・検証。`MessagingRequestTestSupport.java:195-210` を確認して `mom.rst:202` に補った）も採った。L3への節ラベル追加（設計）は承認済みの兄弟ページに前例が無いため見送り、取引単体テスト側 tip の `:ref:` 化（設計）は承認済みページの改稿になるため自分では直していない。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_unit_test_mom.md` §7 に9件。**①リクエストIDの tip が `implementation/deal_unit_test/mom.rst:72-73` と逐語で同一であること**（持ち込み元は別々の出典。定義側を1つ決める判断が要る）。**②承認済みの `testdata_notation.rst:1154` が、同期応答メッセージ送信のテストデータを一律 `sendSyncTestData` 配下としていること**（リクエスト単体テストでは誤りで、本ページの飛び先でもある。`testdata_examples.rst:1802` も同様）。**③`:ref:` の飛び先 `request_unit_test_web`・`request_unit_test_batch` が4行のスタブであること**（`#27-07` decide-2・`#27-08` decide-6・`#27-09` decide-4・`#27-10` decide-4・`#27-11` decide-3・`#27-12` decide-3 と同型）。**④本ページに節ラベルが無いこと**（`ntf-doc-weekend-queue.md:110` が `#27-15` を本ページとの差分ページとしている）。**⑤受信テストを動かすためのコンポーネント設定が解説書のどこにも無いこと**（内蔵MQ、固定キュー名 `TEST.REQUEST`／`TEST.RESPONSE`、`messagingProvider` の登録。第2部への追記要否）。**⑥同期応答メッセージ送信で `messagingProvider` を `RequestTestingMessagingProvider` に差し替える手順が解説書のどこにも無いこと**（⑤と同じく第2部の判断）。**⑦図2点が「Excelファイル（テストデータ）」の表記のままであること**（作図元が無く作り直せない。`#27-12` decide-2 と同型の横断課題）。**⑧承認済みの `testdata_notation.rst:528-533` が `requestPath`・`userId` を「必須」としていること**（`MessagingRequestTestSupport.java:89-91` が `putIfAbsent` で補完するため MOM の受信テストでは不要）。**⑨JUnit 5 の導線が本ページに無いこと**（`#27-12` decide-5 と同じ第3部全体の方針判断）。

**`#27-14` への申し送り**: 常駐バッチのテストでは `RequestThreadLoopHandler` を `nablarch.test.OneShotLoopHandler` に差し替える（`nablarch-testing@e21bf67` `src/main/java/nablarch/test/OneShotLoopHandler.java:16`、`input/ntf-doc-terms.md:498`）。出典 `RequestUnitTest_real.rst:153` が `MainForRequestTesting` の責務としていた「常駐化機能を無効化する」の実体はこちらであり、本ページからは落とした（D-3）。

## `#27-14` リクエスト単体テスト（Nablarchバッチアプリケーション）

**成果物**: `ja/development_tools/testing_framework/implementation/request_unit_test/batch.rst`（197行。ラベル `request_unit_test_batch`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/02_RequestUnitTest/batch.rst` の `:10-70`・`:489-619`（`current-0032`〜`current-0035`・`current-0039`〜`current-0045`）、同 `delayed_send.rst` の `:8-118`（`current-0051`〜`current-0055`）、`06_TestFWGuide/RequestUnitTest_batch.rst` の `:10-133`（`current-0280`〜`current-0287`）、`input/ntf-doc-terms.md` の `:488-499`（`input-0032`）。`current-*` はいずれも削除済みで `git show 2e501ad:<path>` で参照。25行・`lines` 合計384行
**参照実装**: `nablarch-testing` `e21bf67`
**個別指示**: 無し（`ntf-doc-27-small-3rd.md` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15` のみ。本ページは作業指示 `ntf-doc-weekend-queue.md` のみに従う）
**レビュー記録**: `reviews/page-request_unit_test_batch.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は4件。`R` 1件（画像の `git mv`）、` M ja/.../implementation/request_unit_test/batch.rst`、` M ja/.../implementation/testdata_notation.rst`（節ラベル1行の追加。D-3）、`?? .rn/.../reviews/page-request_unit_test_batch.md`。記録2本（本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:16` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を明示して `git status --porcelain` を実行し、出力0件 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。是正の反映後にもう一度フルビルドし直して同じ結果を確認した |
| G6 | **PASS** | 作業指示 §5 の禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。`本ページ`・`下さい`・`出来る`・`事が`・`以下の`・`上記の`・`利用`・`前提条件`・`スーパークラス`・`インターフェース`・`インターフェイス`・`既定`・`デフォルト設定` も0件。です・ます 0件。`.. note::`／`.. warning::` 0件（`.. important::` 1件・`.. tip::` 0件）。用語集が0件を求める `テストケース`（`glossary.md:556`）は初版に5件あり、`テストショット` へ全件置換した。`自動テストフレームワーク`（同 `:509`）・`主なクラス・リソース`（同 `:308`）・`バッチ処理`（同 `:520`）0件 |
| G7 | **PASS** | ページ先頭ラベル `request_unit_test_batch` が `mapping/style.md:377` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 54（表示幅54）・L2 `:13` `:68` 50×2・L3 `:73` `:111` `:138` `:176` `:186` 49×5。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L4 未使用のため S-11 は非該当 |
| G9 | **PASS** | `:ref:` 11件・`:java:extdoc:` 2件。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する（全件を `grep -rn '.. _<label>:' ja/` で解決して照合。一覧は `reviews/page-request_unit_test_batch.md` §4）。`:java:extdoc:` の `BatchRequestTestSupport` は `e21bf67` で `@Published` を確認済み。`@Published` の無い `MainForRequestTesting` は ``literal`` 表記にした |
| G10 | **PASS** | 出典25区間の非空行を全件分類した。**未消化0行。** 反映先は `reviews/page-request_unit_test_batch.md` §2-1。意図して落とした3件（`EXPECTED_FIXED`／`EXPECTED_VARIABLE` の記法・ログ期待値のAND条件・`args[n]` の記法）は、いずれも `testdata_notation.rst` に既載のため `:ref:` に置き換えた（同 §2-2） |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0035`（`batch.rst:65-70` テストクラスで共通のデータベース初期値）の1件。節を起こさず、`batch.rst:139` の `:ref:`共通の準備データをまとめる <testdata_notation-setupdb>`` 導線に落としてある |
| G12 | **PASS** | `mapping.csv` を `csv.DictReader` で読み、同じ3ファイルを出典とする他ページ行（`current-0036`・`current-0037-a`／`-b`／`-b2`／`-c`・`current-0038`・`current-0288`〜`current-0292`・`current-0136`）と本ページ25行の `src_body_start`／`src_body_end` を総当たりで突き合わせ、重なり0件を確認した。常駐バッチのハンドラ構成（`current-0291`）とディレクティブのデフォルト値（`current-0292`）は第2部の設定ページ行きのため、`batch.rst:183` から `:ref:` を張るだけにした |
| G13 | **PASS** | `.. image::` 1件。`git mv` で `06_TestFWGuide/_images/batch_request_test_class.png` を `implementation/request_unit_test/images/batch/` へ移動（`design.md:897`・`:907`）。作図元の `.xlsx` は存在しない。`05_UnitTestGuide/02_RequestUnitTest/_image/delayed_send.png`・同 `delayed_send_error.png` は意図して移していない（D-1） |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘は延べ33件、重複を除くと28件。本文への是正16件、不採用12件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-request_unit_test_batch.md` §6。

最も重いのは4件。①**「該当カラムが空欄なら確認は行われない」がステータスコードには当てはまらなかった**（QA・検証が独立に指摘）。`BatchRequestTestSupport.java:111-117` の `compareStatus` は無条件に比較し、`expectedStatusCode` は `TestShot.java:385-387` の `REQUIRED_COLUMNS` に含まれる。空欄スキップの一般則から外して書き分けた。②**要求電文の確認がページから抜けていた**（QA・検証）。`TestShot.java:134` → `RequestTestingMessagingProvider.java:230-236` により、`expectedMessage` を書かないと要求電文のアサートが黙ってスキップされ、テストが通ってしまう。`:148` と `:193` に補った。③**`.. tip::` が S-06 の基準に合っていなかった**（QA・クラフト）。異常系用の `Action` 差し替えは、行わなければ `errorCase` が無視される必須手順である（`AsyncMessageSendActionForUt.java:26-32`）。`.. important::` に改め、差し替えないとどうなるかを1文足した。④**用語がFW解説書と食い違っていた**（クラフト・検証）。`glossary.md:43` の採用順位1に従い、`電文送信テーブル`→`一時テーブル`、`送信済み`→`処理済み`、`送信失敗（エラー）`／`エラー`→`送信失敗` に揃えた（D-4）。

このほか、`テストケース` 5件の置換（クラフト）、`期待する結果`→`期待値`（クラフト、`glossary.md:218`）、`expectedStatusCode` の「必須」の説明が `testdata_notation.rst:381` と矛盾して読めた点（クラフト）、`// 中略` の位置（検証）、上書き設定に `<import>` の前提が抜けていた点（検証。旧版の実設定 `old-versions/1.4.11/.../send-messaging-test-component-configuration.xml:8` で確認）、異常系の `expectedStatusCode` の値（検証）を採った。`.. important::` の本体を第2部へ移す案（設計）は、`mapping.csv` の `current-0055` が本ページの「使用方法」宛であり、`design.md:299` が第2部へ送ると定めるのは「拡張例」であるため採らなかった。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_unit_test_batch.md` §7 に7件。**①応答不要メッセージ送信のテストデータの記載例が解説書のどこにも無いこと**（`testdata_examples.rst` に「応答不要」0件。`mapping.csv` 上も記載例ページに振られた行が無い。第3部の兄弟5ページが記載例を持たない作りで統一されているため本ページにも置いていない）。**②`batch_request_test_class.png` の3つの食い違い**（`handle` の引数順が `MainForRequestTesting.java:20` と逆／「Excelファイル(テストデータ)」表記／`FileSupport` の操作が「固定長ファイル」限定。作図元が無く作り直せない。`#27-12` decide-2・`#27-13` ⑦ と同型の横断課題）。**③応答不要メッセージ送信のテストに必要な `messagingProvider` の差し替えが第2部にも第3部にも無いこと**（`#27-13` ⑤⑥ と同じ論点。出典にも無いため新規追加になる）。**④JUnit 5 の導線**（`#27-12` decide-5・`#27-13` ⑨ と同一）。**⑤主なクラスとリソースの表を ``literal`` のままにするか `:java:extdoc:` にするか**（`StandaloneTestSupportTemplate`・`TestShot`・`DbAccessTestSupport`・`FileSupport` の4クラスは `@Published`。第3部全ページに関わる）。**⑥`mom.rst` から本ページへの導線が無いこと**（`mom.rst:10` が応答不要メッセージ**送信**に触れていない。`#27-13` はコミット済みのため手を触れていない）。**⑦英数字と日本語の間の `\ ` エスケープに規範が無いこと**（`style.md:13-14` が明記を避けており、承認済みページ間で割れている。レンダリング結果は同一）。

**`#27-20` への申し送り**: 変更なし（`#27-13` の申し送りを維持）。なお `#27-13` から本タスクへ送られた「常駐バッチでは `RequestThreadLoopHandler` を `OneShotLoopHandler` に差し替える」は、`setup/request_unit_test/batch.rst:15-37` に既載であり、`mapping.csv` でも `current-0291` が第2部宛であるため、本ページでは `:ref:` 導線に留めた。

## `#27-15` リクエスト単体テスト（HTTPメッセージング）

**成果物**: `ja/development_tools/testing_framework/implementation/request_unit_test/http_messaging.rst`（42行。ラベル `request_unit_test_http_messaging`。`#27-00` の4行スタブへの追記）
**出典**: `05_UnitTestGuide/02_RequestUnitTest/http_real.rst` の `:4-8`（`current-0064`、REFERENCE）、同 `http_send_sync.rst` の `:6-15`（`current-0069`、REFERENCE）、`input/ntf-doc-terms.md` の `:399-411`（`input-0027`、MERGE）。`current-*` はいずれも削除済みで `git show 2e501ad:<path>` で参照。3行・`lines` 合計28行
**参照実装**: `nablarch-testing` `e21bf67`
**個別指示**: `ntf-doc-27-small-3rd.md` §5（`:150-183`）。追加ゲートは同 §6（`:187-199`）
**レビュー記録**: `reviews/page-request_unit_test_http_messaging.md`

### ゲート結果

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は2件。` M ja/.../implementation/request_unit_test/http_messaging.rst`、`?? .rn/.../reviews/page-request_unit_test_http_messaging.md`。記録2本（本ファイル・`steering.md`）を含めても想定内。`implementation/index.rst:15` の `toctree` は `#27-00` で登録済みのため差分なし |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を明示して `git status --porcelain` を実行し、出力0件 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない（フルビルド後に確認） |
| G4 | **PASS** | `verify_mapping.py` が exit 0（`OK: no errors`）。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで**新規0件**。是正の反映後にもう一度フルビルドし直して同じ結果を確認した |
| G6 | **PASS** | `glossary.md` §8 の言い換え表（`:507-602`）を全行スクリプトで本文に突き合わせ、完全一致0件。`テストケース`・`同期応答メッセージ送信処理`・`HTTP同期応答メッセージ送信`・`HTTP同期応答メッセージ受信`・`メッセージ同期送信` いずれも0件。です・ます 0件。`.. note::`／`.. warning::`／`.. tip::`／`.. important::` 0件 |
| G7 | **PASS** | ページ先頭ラベル `request_unit_test_http_messaging` が `mapping/style.md:376` と一致 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、L1 `:4` 50（表示幅42）・L2 `:13` `:20` 50×2・L3 `:25` 49（表示幅16）。実測則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱0件。L4 未使用のため S-11 は非該当 |
| G9 | **PASS** | `:ref:` 5件（`request_unit_test_mom` 3件・`testdata_notation-test_shots`・`testdata_notation-messaging_data`・`request_unit_test_setting_http_messaging`）。飛び先はいずれも実在し、リンク文字列が飛び先の見出しと一致する（`mom.rst:1`／見出し `:3`、`testdata_notation.rst:350`／見出し `:352`、同 `:1150`／見出し `:1152`、`setup/request_unit_test/http_messaging.rst:1`／見出し `:3`）。`:java:extdoc:` 0件。`@Published` の確認が要るクラス参照は無い（``literal`` 表記のみ） |
| G10 | **PASS** | 出典3区間の非空行を全件分類した。**未消化0行。** 反映先は `reviews/page-request_unit_test_http_messaging.md` §2-1。意図して落としたのは2件（`http_send_sync.rst:14` の次節アンカー行、`input-0027` の `MockMessagingContext` 行）で、いずれも同 §2-2・§5 D-1 に理由を記録した |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0064`・`current-0069` の2件。どちらも節を起こさず、`:15` の `:ref:` 導線と `:36-37` の読み替え表の1行に落としてある |
| G12 | **PASS** | `mapping.csv` を `csv.DictReader` で読み、同じ2ファイルを出典とする他ページ行（`current-0065`〜`0067`・`0070`〜`0073` はテストデータの書き方、`current-0066-b`・`0074`・`0075` はリクエスト単体テストの設定（HTTPメッセージング）、`current-0138`〜`0140` は取引単体テスト側）と本ページ3行の `src_body_start`／`src_body_end` を突き合わせ、重なり0件を確認した |
| G13 | **PASS**（非該当） | `.. image::` 0件。出典に図は含まれない（`http_real.rst:172` の `http_real_test_data.png` と `http_send_sync.rst:26,41,112,122` の各図は、いずれも `current-0065`〜`0073` の範囲でテストデータの書き方ページ宛） |
| S1 | **PASS** | L2 は `:12` 機能概要・`:19` 使用方法 の2つのみ |
| S2 | **PASS** | L3 は `:24` 用語を読み替える の1つのみ。個別指示 `ntf-doc-27-small-3rd.md:170-175` のセクション構成と一致。出典に無いL3は無い |
| S4 | **PASS** | G11 と同じ。`current-0064`・`current-0069` を節として起こしていない |
| S5 | **PASS** | G9 と同じ |
| S6 | **PASS** | `.. code-block::` 0件。テストデータ例0件（`list-table` 1件は用語読み替え表であり、テストデータの記載例ではない） |
| S7 | **PASS** | `reviews/page-request_unit_test_http_messaging.md` を作成した。§1-1 の `decide`（第3部アウトラインの適用）は `#27-07` の記録 `reviews/page-deal_unit_test_rest.md` を指している（同 §5 D-7） |

### 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施し、1ラウンドで是正した（指摘は延べ29件、重複を除くと13件。本文への是正8件、不採用5件）。是正は成果物の `.rst` に畳んであり、別コミットに割っていない。内訳は `reviews/page-request_unit_test_http_messaging.md` §6。

最も重いのは4件で、いずれも「参照先ページに読み替えを当てると実装と食い違う」という同じ型の問題だった。①**読み替え表の `MockMessagingContext` 行は機能しない**（4観点すべてが指摘）。`MockMessagingContext.java:14-24` は取引単体テスト向けと明記され、リクエスト単体テストの経路（`TestShot.java:188-190`・`AbstractHttpRequestTestTemplate.java:316-321`）は `RequestTestingMessagingContext`／`RequestTestingMessagingClient` を初期化する。決め手は読み替え先の `mom.rst` に `MockMessagingContext` が0件であること。表から落とした（D-1）。②**「メッセージ受信」が出典より広かった**（QA・クラフト・検証）。`mom.rst:10` の総称は応答不要メッセージ受信を含むが、出典 `real_request_test` は同期応答メッセージ受信処理のみを指す。`:15` を「同期応答メッセージ受信」に限定した。③**読み替えの適用範囲が参照先ページ全体に及んでいた**（QA・設計・検証）。`http_send_sync.rst:9` の読み替え指示は送信側に対するもので、`MessagingRequestTestSupport.java:185-197` のとおり受信側テストは実際にキュー（`TEST.REQUEST`／`TEST.RESPONSE`）を使う。`mom.rst:190` に当てると成り立たないため、`:27` で範囲を同期応答メッセージ送信の説明に限定した。④**`RequestTestingMessagingProvider`→`RequestTestingMessagingClient` の読み替えが `mom.rst:192` で破綻する**（QA・設計）。`RequestTestingMessagingClient.java` はクラス宣言が `:53` の1件のみで内部クラスを持たず、`RequestTestingMessagingProvider.java:60` の `RequestTestingMessagingContext` に相当するものがない。表の後に例外を1文足した。

このほか、`list-table` への `:widths:` の追加（クラフト。`style.md:257-258` の S-07 が指定しており、NTF配下の `list-table` で欠けているのは本件だけだった）、「送信キュー」「受信キュー」の2行の統合（QA・クラフト）、テストデータへの導線をページ先頭から節アンカーへ変更（設計。`testdata_notation` は1300行を超える）、L3 直下への導入文の追加（設計）を採った。L3 見出しを「MOMによるメッセージングの用語を読み替える」に改める案（設計）は、個別指示のセクション構成が「用語を読み替える」で固定されており S2 が一致を求めるため採らなかった（D-5）。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_unit_test_http_messaging.md` §7 に4件。**①`input-0027` の1行（`MockMessagingContext`）を落としたことを `mapping.csv` に反映するか**（行単位の部分不採用を表す欄が `mapping.csv` に無いため、レビュー記録に留めている）。**②`mapping.csv` の `current-0069` の `dest_section` を `使用方法` に更新するか**（個別指示 `ntf-doc-27-small-3rd.md:179` が使用方法への配置を明示しているが、`mapping.csv` は `機能概要` のまま。D-4）。**③第2部 `setup/request_unit_test/http_messaging.rst` から本ページへの逆方向の導線を張るか**（第2部6ページのうち逆方向リンクを持つのは `setup/request_unit_test/web.rst:204` の1件のみで、本ページ固有の欠落ではない）。**④HTTPメッセージ受信の実行経路が実際にキューを経由するかは未確認**（`nablarch-fw-messaging` が当環境に無く追えない。本ページの記述はこの点に依存しない）。

**`#27-20` への申し送り**: 変更なし（`#27-13` の申し送りを維持）。

---

## `#27-16` リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）

- **成果物**: `ja/development_tools/testing_framework/setup/request_unit_test/db_queue.rst`（第2部、全6行）
- **出典**: 0行。`mapping.csv` に該当行なし（`csv.DictReader` で実測）。`checks/task-06.md:569` が `EXPECTED_ZERO（design.md §6「導線のみ」）` と記録。旧解説書（`2e501ad`）にも対応記述なし。
- **参照実装**: `nablarch-testing` `e21bf67` / `nablarch-testing-yaml` `190cc9a`
- **個別指示**: `.rn/20260724-ntf-yaml-support/ntf-doc-27-db-queue.md`
- **レビュー記録**: `reviews/page-request_unit_test_setting_db_queue.md`

### ゲート

| ゲート | 結果 | 根拠 |
| --- | --- | --- |
| G1 `git status --porcelain` 全件 | PASS | `M setup/request_unit_test/db_queue.rst` と `?? reviews/page-request_unit_test_setting_db_queue.md` の2件のみ |
| G2 禁止ファイル差分0 | PASS | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` の `git status --porcelain` が0行 |
| G3 `sphinx.mo` 未コミット | PASS | `git status --porcelain` に出現なし |
| G4 `verify_mapping.py` | PASS | `OK: no errors` |
| G5 フルビルド | PASS | `build succeeded, 1 warning.`。既知の `db_double_submit.rst:108: undefined label: how_to_set_token_in_request_unit_test`（`#27-20` で解消予定）のみ。新規0 |
| G6 禁止語 | PASS | です・ます・下さい・「ここでは、」いずれも0件 |
| G7 ラベル | PASS | `request_unit_test_setting_db_queue` が `style.md:363` と文字列一致 |
| G8 下線幅 | PASS | L1 表示幅72 / 下線72（`max(50, 表示幅)`）。L2以下は0件 |
| G9 `:ref:` 飛び先とリンクテキスト | PASS | `request_unit_test_setting_batch` が `setup/request_unit_test/batch.rst:1` の実物と一致。リンクテキストが同 `:3` の見出しと一致 |
| G10 出典の反映 | PASS | 出典0行。落とした行なし |
| G11 REFERENCE行を節にしない | N/A | 出典0行 |
| G12 二重掲載なし | PASS | 本文は導線1文のみ |
| G13 画像 `git mv` | N/A | 画像なし |
| DQ1 `code-block` 0件 | PASS | `grep -c` が `0` |
| DQ2 `機能概要`・`使用方法` の見出しなし | PASS | `grep -c` が `0`。見出しは L1 タイトルのみ |
| DQ3 飛び先ラベルが実ファイルと文字列一致 | PASS | G9 と同じ |
| DQ4 `setup/deal_unit_test/db_queue.rst` 未作成 | PASS | `setup/deal_unit_test/` は `rest.rst`・`http_messaging.rst`・`mom.rst` の3件のみ |
| DQ5 `undefined label` 増加なし | PASS | G5 と同じ。既知1件のまま |
| S-01 である調 | PASS | 常体 |
| S-02 リード文 | 適用外 | `design.md:384`「導線のみ」による。→ 判断待ち④ |
| S-04 下線記号 | PASS | L1 `=` のみ |
| S-05 code-block インデント | N/A | `code-block` 0件 |
| S-06 important / tip | N/A | ディレクティブなし |
| S-07 表 | N/A | 表なし |
| S-08 ラベル | PASS | G7 と同じ |
| S-09 `.. contents::` | 適用外 | L2セクション0件（`style.md:400-417`）。加えて `design.md:384`「導線のみ」による |
| toctree 並び | PASS | `setup/index.rst:13-18` が `web → rest → http_messaging → batch → mom → db_queue` で `design.md:845-853` と一致。`toctree` は変更していない |

### 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施。延べ16件、重複除き10件。反映1件・判断待ちへ5件・不採用4件。反映したのはリード文の主述のねじれ1件で、「〜のリクエスト単体テストは、…と同じ設定を行う。」を「〜のリクエスト単体テストの設定は、…と同じである。」に改めた。承認済みの同型導線文（`implementation/deal_unit_test/batch.rst:20`・`rest.rst:22`、`setup/deal_unit_test/http_messaging.rst:31`）に揃えた形である。

### 判断待ち（週明けに判定してほしい項目）

`reviews/page-request_unit_test_setting_db_queue.md` §7 に5件。**①飛び先 `setup/request_unit_test/batch.rst` の設定3件のうち、DBキューに確実に該当するのは `batch.rst:15-37` の1件のみ。「設定は同じである」が過大でないか**（必須）。**②`batch.rst:17` は当該設定を常駐バッチの設定として説明しているが、FW解説書では Nablarchバッチアプリケーションの常駐バッチ最小ハンドラ構成に `request_thread_loop_handler` が無く（`batch/nablarch_batch/architecture.rst` 全体で0件）、含むのは `messaging/db/architecture.rst:49`・`:155` と `messaging/mom/architecture.rst` だけ。`batch.rst` 当該節の帰属先の判断が要る**（必須）。**③`OneShotLoopHandler`（`e21bf67`）が `DatabaseTableQueueReader` を名指しで分岐している事実に `batch.rst` が触れていない**（参考）。**④`style.md` S-02（`:45-46`）と S-09 の適用外列挙（`:413-415`）に、`design.md:384` の導線のみ3ページの除外規定が無い。`style.md` は G2 の禁止ファイルのためこの週末は変更しない**（推奨）。**⑤参照実装 `e21bf67` にDBキュー専用のリクエスト単体テスト用クラス・設定は存在しない**（参考）。

**`#27-20` への申し送り**: 変更なし（`#27-13` の申し送りを維持）。
