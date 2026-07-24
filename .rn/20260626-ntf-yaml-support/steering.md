Design: .rn/20260626-ntf-yaml-support/design.md

# Goal

NTF（Nablarchテストフレームワーク）解説書（`ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/` 配下）の全体構成を見直し、テストデータ記述形式として YAML を Excel と並列でサポートする記述を追加する。

作業フロー: RSTビルド確認 → 全体構成の認識合わせ → 影響範囲確認・タスク更新 → 文書表現・トンマナ確認・CLAUDE.mdへの作業ルール記載 → 解説書修正

# Acceptance criteria

- `feature/ntf-yaml-support` ブランチで作業し、PR は `develop` ブランチへ向けて作成されている
- 変更前後で `make html`（RST → HTML ビルド）がエラーなく完了する
- 解説書の全体構成について、ユーザーと認識を合わせた内容が `design.md` の Approach に記録されている
- CLAUDE.md に解説書修正の作業ルール（文書表現・トンマナ）が記載されている
- Excel のみ言及していた箇所が YAML にも対応した記述（ExcelまたはYAML形式で記述できると明示）に更新されている
- 新規追加・変更した RST が Sphinx でビルドエラーなく通る
- 既存の RST の toctree 参照が壊れていない

# Assumptions

- YAML 対応は `nablarch-testing` 本体（PR #75 / `convert-testdata-excel-to-text` ブランチ）で実装済みであり、解説書はそれに合わせたドキュメント変更である
- 入力資料（`.rn/20260626-ntf-yaml-support/input/` 配下10ファイル）が YAML 形式の仕様・記述例の正典となる
- Sphinx ビルド環境は `make html` で実行できる（`requirements.txt` の依存が解決済み）
- 解説書の構成見直しの範囲は `06_TestFWGuide/` 配下が主であり、`05_UnitTestGuide/` 配下への影響は最小限とする（要確認）
- 既存の Excel 記述は削除せず、YAML を「並列サポート」として追記する方向で進める

# Rules

- commit and push every change; one completion marker per task
- RST ビルドは各タスク完了前に必ず確認し、エラーがあれば修正してから完了マークをつける
- 文書表現・トンマナは CLAUDE.md に記載した汎用ルールに従う
- 日本語で記述する（ファイルパス・コマンド・コード例は除く）
- 既存の Excel 向け記述を削除しない（YAML を追記する形で対応）
- 新規 RST ファイルを追加する場合は toctree にも追記する

## このブランチ固有の記述ルール

CLAUDE.md の「NTF 解説書 YAML 対応 固有ルール」セクションを参照すること。

# Tasks

### #1: RSTビルド確認

**Purpose**: 変更作業開始前に現時点のRSTビルドが問題なく通ることを確認し、ベースラインを確立する。

**Prerequisites**: none

**Steps**:

- [x] `make html` を実行してビルドが通ることを確認する
- [x] ビルドエラーや警告があれば原因を調査する（修正は任意 — このタスクの目的はベースライン確認）
- [x] 結果を `checks/task1.md` に記録する
- [x] self-check (OK/NG per completion criterion, record in checks/task1.md)
- [x] user review

**Completion criteria**:

- `make html` がエラーなく完了した事実が `checks/task1.md` に記録されており、エラー行数が0であることが Evidence に記載されている
- 警告のみが含まれることが明示されている（警告は許容、エラーは不可）

### #2: 全体構成の認識合わせ

**Purpose**: NTF解説書の現状の全体構成をまとめ、ユーザーと認識を合わせる。どの文書がどんな役割を担っているかを確認し、YAML対応で修正が必要な範囲の見通しを得る。

**Prerequisites**: #1

**Steps**:

- [x] `06_TestFWGuide/` 配下の全RSTを読み、各ファイルの役割・構成を一覧にまとめる
- [x] `05_UnitTestGuide/` 配下の影響ありそうなRSTを確認する
- [x] 入力資料（`input/ntf-testdata-doc.md`・`ntf-doc-terms.md`）をもとに YAML 対応で更新が必要な箇所を洗い出す
- [x] 全体構成サマリーを `checks/task2.md` に記録しユーザーに提示する
- [x] user review（構成認識の合意）

**Completion criteria**:

- `06_TestFWGuide/` 配下の全ファイルの役割と、YAML対応で修正が必要な箇所の一覧が `checks/task2.md` に記録されている
- ユーザーが全体構成を確認・承認しており、その内容が `design.md` の Approach に記録されている

### #3: 文書表現・トンマナ確認とCLAUDE.md作業ルール記載

**Purpose**: 既存解説書の文書表現・トンマナ（用語の統一・文体・表記ルール）を確認し、解説書修正作業のルールをCLAUDE.mdに記載する。

**Prerequisites**: #2

**Steps**:

- [x] 既存解説書（`06_TestFWGuide/01_Abstract.rst` 等）と入力資料（`ntf-doc-terms.md`）から用語・表記ルールを抽出する
- [x] 文体（です・ます調 vs だ・である調）・用語統一ルールをまとめる
- [x] `CLAUDE.md` に作業ルールを記載する
- [x] self-check (OK/NG per completion criterion, record in checks/task3.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] user review

**Completion criteria**:

- `CLAUDE.md` にNTF解説書修正の作業ルール（文書表現・用語・トンマナ）が記載されており、第三者が実際の解説書修正に適用できる具体性を持っている
- 既存解説書と矛盾する記述が `CLAUDE.md` に含まれていない

### #4: toctree 構成変更（A章・B章の骨格作成）

**Purpose**: proposed-structure.md の新構成ツリーに合わせて、既存の toctree を組み替え、A章・B章の骨格（index.rst）を作成する。ファイル移動は行わず toctree の付け替えと新規 index.rst の追加のみで完結させる。

**Prerequisites**: #3

**Steps**:

- [x] 新構成ツリーに合わせた index.rst の変更・新規ファイルを確認・作成する
  - `06_TestFWGuide/index.rst`（または親ページ）の toctree を A章・B章構成に組み替える
  - `06_TestFWGuide/testdata/index.rst` を新規作成（B-1 の入口）
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task4.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] Design expert review (subagent)

**Completion criteria**:

- A章（`Nablarchテスティングフレームワークとは`）・B章（`テストの実装方法`）が toctree に現れており、`make html` の HTML 出力で両章が確認できる
- `make html` がエラーなく完了し、エラー行数が0であることが Evidence に記載されている
- 既存ファイルへの toctree 参照が壊れていない（変更前後で参照先ファイルが存在する）

### #5: B-1「テストデータの記述方法」新規作成

**Purpose**: `ntf-testdata-doc.md` を主素材に、テストデータ仕様リファレンス（B-1-1〜B-1-7）を RST ファイルとして新規作成する。Excel/YAML 並列記述は「Excelの場合」「YAMLの場合」見出し分けで行う。

**Prerequisites**: #4

**Steps**:

- [x] `06_TestFWGuide/testdata/` 配下に以下の7ファイルを作成する:
  `overview.rst` / `data-blocks.rst` / `testshots.rst` / `table-data.rst` / `file-data.rst` / `messaging.rst` / `values.rst`
- [x] 各ファイルに `ntf-testdata-doc.md` の対応章（§1〜10）と examples ファイルの内容を RST 化して記述する
- [x] `testdata/index.rst` の toctree にすべて追加する
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task5.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] Verification expert review (subagent, fact-check)

**Completion criteria**:

- `testdata/` 配下に B-1-1〜B-1-7 の RST ファイルが存在し、toctree に追加されている
- `ntf-testdata-doc.md` の全章（§1〜10）が B-1 のいずれかの節に対応しており、対応表が `checks/task5.md` の Evidence に記載されている
- Excel/YAML の記述例が各節に両方掲載されており、各節の Excel 例と YAML 例が対応している
- `make html` がエラーなく完了し、エラー行数が0であることが Evidence に記載されている

### #6: 既存ページのテストデータ参照をB-1へ差し替え

**Purpose**: `05_UnitTestGuide/` 配下の各ページで「テストデータの書き方」を解説している箇所を B-1 への参照リンクに置き換え、重複記述を解消する。

**Prerequisites**: #5

**Steps**:

- [x] design.md の新旧マッピング表を参照し、対象ページ（B-3〜B-5 相当）を特定する
- [x] 各ページの「テストデータの書き方」節を `:ref:` 参照リンクに置き換える
- [x] `02_DbAccessTest.rst` の冒頭にテストデータ参照誘導を追加する
- [x] `make html` でビルドエラー・壊れた参照がないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task6.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] Verification expert review (subagent, fact-check)

**Completion criteria**:

- 対象ページの「テストデータの書き方」節が B-1 への `:ref:` 参照に変わっており、参照先ラベルが `checks/task6.md` の Evidence に列挙されている
- `make html` がエラーなく完了し、既存の `:ref:` ラベルが壊れていないことが確認できる

### #7: A-3「テストデータの形式」新規作成

**Purpose**: Excel と YAML の違い・どちらを使うか・プロジェクト統一方針を説明するページを新規作成し、`06_TestFWGuide/index.rst` の toctree に追加する。

**Prerequisites**: #6

**Steps**:

- [x] `06_TestFWGuide/testdata_format.rst` を新規作成する（Excel/YAML の違い・選択指針・プロジェクト統一方針）
- [x] `06_TestFWGuide/index.rst` の toctree に `testdata_format` を追加する
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task7.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)

**Completion criteria**:

- `06_TestFWGuide/testdata_format.rst` が存在し、Excel/YAML 両形式の概要・違い・選択指針が記述されている
- `06_TestFWGuide/index.rst` の toctree に `testdata_format` が含まれており、HTML 出力でページが確認できる
- `make html` がエラーなく完了し、エラー行数が0である

### #8: B-2「テストデータの記述例」新規作成

**Purpose**: `input/ntf-testdata-doc-examples-*.md` 6本を素材に、Excel/YAML 対比例を一覧するページを新規作成し、`05_UnitTestGuide/index.rst` の toctree に追加する。

**Prerequisites**: #7

**Steps**:

- [x] `06_TestFWGuide/testdata/examples.rst` を新規作成する（6本の examples ファイルを統合、Excel/YAML 対比）
- [x] `06_TestFWGuide/testdata/index.rst` の toctree に `examples` を追加する
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task8.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] Verification expert review (subagent, fact-check)

**Completion criteria**:

- `06_TestFWGuide/testdata/examples.rst` が存在し、`input/ntf-testdata-doc-examples-*.md` 6本（overview・testshots・table・file・messaging・special）の内容がすべて掲載されている
- 各例について Excel 記述例と YAML 記述例が両方掲載されている
- `make html` がエラーなく完了し、エラー行数が0である

### #9: B-6（`03_Tips.rst` の開発者向け移動・Excel 表現修正）

**Purpose**: `06_TestFWGuide/03_Tips.rst` を「テストの実装方法」（`05_UnitTestGuide/index.rst`）の toctree に追加し、「Excelファイル」等の Excel 固有表現を「テストデータファイル」等に修正する。

**Prerequisites**: #8

**Steps**:

- [x] `05_UnitTestGuide/index.rst` の toctree に `../06_TestFWGuide/03_Tips` を追加する
- [x] `03_Tips.rst` 内の「Excelファイル」「Excelシート」等の Excel 固有表現を汎用表現（「テストデータファイル」等）に修正する
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task9.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)

**Completion criteria**:

- `05_UnitTestGuide/index.rst` の toctree に `03_Tips` が含まれており、HTML 出力で「テストの実装方法」配下にページが確認できる
- `03_Tips.rst` に「Excelファイル」「Excelシート」等の Excel 固有表現が単独で使われている箇所が残っていない（YAML も対象にした汎用表現に置き換えられている）
- `make html` がエラーなく完了し、エラー行数が0である

### #10: A章内部再編（A-1〜A-6 への細分化）

**Purpose**: `06_TestFWGuide/index.rst` の toctree を design.md の新構成ツリー（A-1〜A-6）に合わせて整理し、各 index.rst を作成・更新する。

**Prerequisites**: #9

**Steps**:

- [x] `06_TestFWGuide/index.rst` を A-1〜A-6 構成に組み替える:
  - A-1: `01_Abstract`（FW 概要・構成表）
  - A-2: リクエスト単体テスト用クラス（`02_DbAccessTest`・`02_RequestUnitTest`・`RequestUnitTest_*`）
  - A-3: `testdata_format`（#7 で作成済み）
  - A-4: `JUnit5_Extension`
  - A-5: `04_MasterDataRestore`
  - A-6: `../08_TestTools/index`（テストツール）
- [x] A-2 をまとめる `testclass/index.rst` を新規作成する（または見出し分けで対応）
- [x] `make html` でビルドエラーがないことを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task10.md)
- [x] QA expert review (subagent)
- [x] Craft expert review (subagent, writing)
- [x] Design expert review (subagent)

**Completion criteria**:

- `06_TestFWGuide/index.rst` の toctree が A-1〜A-6 の論理構成を反映しており、HTML 出力で A 章配下に A-1〜A-6 が確認できる
- 既存ファイルへの toctree 参照が壊れていない（変更前後で参照先ファイルが存在する）
- `make html` がエラーなく完了し、エラー行数が0である

### #11: B-1 テストデータ記述方法を1ページに統合

**Purpose**: design.md では B-1「テストデータの記述方法」は「★最大の変更点・1ページ★ … 10本以上に散在 → 1ページに集約」と規定されているが、task #5 で7ページ分割になった。これを1ページに統合して設計書に一致させる。

**Prerequisites**: #10

**Steps**:

- [x] `testdata/` 配下の7ファイル（overview/data-blocks/testshots/table-data/file-data/messaging/values）の内容を `testdata/index.rst` 1ページに統合する
- [x] 統合後の `testdata/index.rst` を B-1 として toctree に登録する（7ファイルは toctree から外す）
- [x] `make html` でビルドエラーがないことを確認する
- [x] HTML で B-1 が1ページとして表示されていることを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task11.md)
- [x] QA expert review (subagent)

**Completion criteria**:

- `05_UnitTestGuide/index.rst` の toctree に B-1 として1つのページエントリが現れ、HTML 出力で「テストデータの記述方法」が1ページに収まっている
- `make html` がエラーなく完了し、エラー行数が0である

### #12: B-1 各節から B-2（テストデータの記述例）へのリンク追加

**Purpose**: design.md に「仕様を調べるなら B-1、写して使うなら B-2」という誘導を明記しているが、B-1 の各節から `examples.rst`（B-2）への参照リンクがない。

**Prerequisites**: #11

**Steps**:

- [x] B-1（統合後の `testdata/index.rst`）の各節末尾に `examples.rst` の対応セクションへの `:ref:` リンクを追加する
- [x] `make html` でビルドエラーがないことを確認する
- [x] HTML でリンクが正しく機能していることを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task12.md)
- [x] QA expert review (subagent)

**Completion criteria**:

- B-1 の各節（testshots/テーブルデータ/ファイルデータ/メッセージング/特殊値 等）に B-2 の対応セクションへの `:ref:` リンクが存在する
- `make html` がエラーなく完了し、エラー行数が0である

### #13: A-1 ページタイトルを「テスティングフレームワーク概要」に変更

**Purpose**: design.md でタイトルを「テスティングフレームワーク概要」と確定しているが、`01_Abstract.rst` のページタイトルが「自動テストフレームワーク」のまま。

**Prerequisites**: #12

**Steps**:

- [x] `06_TestFWGuide/01_Abstract.rst` のページタイトルを「自動テストフレームワーク」→「テスティングフレームワーク概要」に変更する
- [x] ラベル `.. _auto-test-framework:` も `.. _ntf_abstract:` に変更し、既存の `:ref:` 参照を更新する
- [x] `make html` でビルドエラーがないことを確認する
- [x] HTML で A-1 が「テスティングフレームワーク概要」と表示されていることを確認する
- [x] self-check (OK/NG per completion criterion, record in checks/task13.md)
- [x] QA expert review (subagent)

**Completion criteria**:

- HTML 出力で A-1 のページタイトルが「テスティングフレームワーク概要」と表示されている
- 既存の `:ref:` 参照が壊れていない
- `make html` がエラーなく完了し、エラー行数が0である

### #14: HTML 出力が設計書に完全一致しているか確認

**Purpose**: design.md の新構成ツリー全体と HTML 出力を突き合わせて、差異がゼロであることを確認する。

**Prerequisites**: #13

**Steps**:

- [x] HTML 出力の各章・ページ構成を design.md の新構成ツリーと1項目ずつ照合する
- [x] 差異があれば追加修正する
- [x] self-check (OK/NG per completion criterion, record in checks/task14.md)

**Completion criteria**:

- HTML 出力の構成が design.md の新構成ツリーに完全一致している

### #15: T1 — 抽出ツールの作成 ✅

**Purpose**: 全量インベントリを機械的に生成し、第三者が同じ結果を再現できるようにする。

**Prerequisites**: #14

**Steps**:

- [x] `reviews/tools/extract_rst.py` を作成する（引数: 入力ディレクトリ・出力CSVパス。出力列: `file,line,kind,depth,path,title,detail`）
- [x] `reviews/tools/extract_md.py` を作成する（input/ 配下の md 用。見出しとコードフェンスを抽出）
- [x] `reviews/tools/build_inventory.sh` を作成する（変更前・PR後・input の3系統を抽出。base は `git merge-base origin/develop HEAD`）
- [x] self-check（Completion criteria ごとに OK/NG を `checks/review-t1.md` に記録）
- [x] commit & push
- [x] **user review** — 承認を受けるまで #16 に進まない

**Completion criteria**:

- `bash reviews/tools/build_inventory.sh` を2回実行して同一のCSVが生成される（冪等）
- 3本のCSVの行数が `checks/review-t1.md` の Evidence に記録されている
- 抽出対象ファイル数が、対象ディレクトリの rst / md 実ファイル数と一致することが Evidence に記載されている

**抽出対象範囲**:
- `ja/development_tools/testing_framework/` 配下の全 .rst
- `.rn/20260626-ntf-yaml-support/input/` 配下の全 .md

---

### #16: T2 — ゲート① 章構成レビュー

**Purpose**: design.md の章構成が PR の目的に適合しているかを判定する。

**Prerequisites**: #15

**Steps**:

- [x] `.rn/20260626-ntf-yaml-support/reviews/gate1-structure.md` を作成する
- [x] A-1〜A-6・B-1〜B-6 の各章について、章ID / 章タイトル / 実ファイルパス / 想定読者 / 判定 / 根拠（file:line）の表を作成する
- [x] 逸脱項目の問題と対処案を記述する
- [x] 既知の逸脱5件（G1-01〜G1-05）がすべて検出されているか照合する
- [x] self-check（Completion criteria ごとに OK/NG を `checks/review-t2.md` に記録）
- [x] commit & push
- [x] **user review** — ゲート①の合否判定を受ける。合格承認を受けるまで #17 に進まない

**既知の逸脱（全件検出必須）**:
- G1-01: `01_Abstract.rst` L195-579 — テストデータ記法385行が A-1 に残存し B-1 と二重掲載
- G1-02: `01_Abstract.rst` L613 — 「テストデータは全てExcelシートに記述する」が YAML 対応後と矛盾
- G1-03: `02_DbAccessTest.rst` 等 — 使い方（B章相当）が A 章に残存
- G1-04: `01_Abstract.rst` L665-704 — 「JUnit 5で自動テストフレームワークを動かす」が A-4 と重複
- G1-05: A-3 と B-1 の導線なし

**Completion criteria**:

- `reviews/gate1-structure.md` に全章の読者判定表が存在し、各判定に file:line の根拠がある
- 既知の逸脱5件がすべて表に含まれている
- 総合判定（合格 / 条件付き合格 / 不合格）とその論拠が明記されている

---

### #17: T3 — ゲート② 突合台帳の作成

**Purpose**: 変更前と input の全項目が新構成のどこに移送されたかを1項目ずつ追跡し、欠落と重複を検出する。

**Prerequisites**: #16

**Steps**:

- [x] `.rn/20260626-ntf-yaml-support/reviews/gate2-traceability.csv` を作成する（列: `item_id,src_file,src_line,kind,heading_path,content,design_dest,actual_file,actual_line,verdict,note`）
- [x] `verdict` は `MOVED` / `MISSING` / `DUPLICATED` / `KEPT` の4値のみ。空欄不可（MODIFIED も追加）
- [x] `actual_file` / `actual_line` は grep による実測で求める。推測で埋めない
- [x] `.rn/20260626-ntf-yaml-support/reviews/gate2-findings.md` を作成し、`MISSING` と `DUPLICATED` を一覧化して対処案を付す
- [x] self-check（Completion criteria ごとに OK/NG を `checks/review-t3.md` に記録）
- [x] commit & push
- [x] **user review** — `MISSING` / `DUPLICATED` の内容と対処案のレビューを受ける。承認を受けるまで #18 に進まない

**Completion criteria**:

- `gate2-traceability.csv` の行数が `inventory-before.csv` と `inventory-input.csv` の合計行数と一致する
- `verdict` が空欄の行が0件
- `MISSING` / `DUPLICATED` の全件が `gate2-findings.md` に列挙され、それぞれに対処案がある
- 既知の逸脱 G1-01（`01_Abstract.rst` の385行）が `DUPLICATED` として検出されている

---

### #18: T4 — ゲート③ 記述規約の抽出と逸脱検出

**Purpose**: 新規追加ページ（B-1/B-2/A-3）が既存ページと同じ書きっぷりかを判定する。

**Prerequisites**: #17

**Steps**:

- [x] `.rn/20260626-ntf-yaml-support/reviews/gate3-conventions.md` を作成する（規約ID `C-01` 形式・根拠 file:line 2件以上）
- [x] `.rn/20260626-ntf-yaml-support/reviews/gate3-findings.csv` を作成する（列: `finding_id,file,line,rule_id,detected,expected,severity,fix_proposal`）
- [x] 検査対象6ファイル: `testdata/index.rst`・`testdata/examples.rst`・`testdata_format.rst`・`06_TestFWGuide/index.rst`・`05_UnitTestGuide/index.rst`・`03_Tips.rst`
- [x] self-check（Completion criteria ごとに OK/NG を `checks/review-t4.md` に記録）
- [x] commit & push
- [x] **user review** — 抽出した規約の妥当性と逸脱判定のレビューを受ける。承認を受けるまで #19 に進まない

**Completion criteria**:

- `gate3-conventions.md` の全規約に、既存ページからの根拠 file:line が2件以上ある
- `gate3-findings.csv` の全行に `rule_id` が紐づいており、`gate3-conventions.md` に存在する規約IDである
- 検査対象6ファイルすべてについて検査実施済みであることが Evidence に記載されている

---

### #19: T5 — README.md の作成

**Purpose**: 第三者が同じ手順でレビューを再現・追検証できるようにする。

**Prerequisites**: #18

**Steps**:

- [x] `.rn/20260626-ntf-yaml-support/reviews/README.md` を作成する（3ゲートの定義・各成果物の意味・インベントリ再生成コマンド・verdict 4値の定義・判定サマリ・未対処事項一覧）
- [x] self-check（Completion criteria ごとに OK/NG を `checks/review-t5.md` に記録）
- [x] commit & push
- [ ] **user review** — 最終確認

**Completion criteria**:

- README.md だけを読んだ第三者が、成果物の意味を理解し、インベントリを再生成できる
- 判定サマリの件数が各成果物の実際の行数と一致している

---

### #20: 評価サインオフ

**Purpose**: セッション全体の成果物（#1〜#14 の解説書変更 + #15〜#19 のレビュー基盤）が Acceptance criteria を満たすことをユーザーに確認してもらう。

**Prerequisites**: #19

**Steps**:

- [ ] Acceptance criteria の各項目を実際の成果物に照らして確認する
- [ ] セッション全体の結果をユーザーに提示し、`/rn:ty` または `/rn:gm` の verdict を受け取る

**Completion criteria**:

- ユーザーが `/rn:ty` で承認している

# State

<!--
  Managed by rn — do not edit this block manually.
  Status: active | paused | complete
-->

Status: paused
Date: 2026-07-24
Last completed: #19 (T5) — README.md NG 指摘修正済み・user review 再待ち。
Next: #19 user review 合格 → #20（評価サインオフ）へ。
Notes: NG 指摘3件を修正してコミット済み（f51fcb1）。再レビュー待ち。
