# Goal

NTF（Nablarchテストフレームワーク）解説書（`ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/` 配下）の全体構成を見直し、テストデータ記述形式として YAML を Excel と並列でサポートする記述を追加する。

作業フロー: RSTビルド確認 → 全体構成の認識合わせ → 影響範囲確認・タスク更新 → 文書表現・トンマナ確認・CLAUDE.mdへの作業ルール記載 → 解説書修正

# Acceptance criteria

- `feature/ntf-yaml-support` ブランチで作業し、PR は `develop` ブランチへ向けて作成されている
- 変更前後で `make html`（RST → HTML ビルド）がエラーなく完了する
- 解説書の全体構成について、ユーザーと認識を合わせた内容がステアリングの Decisions に記録されている
- CLAUDE.md に解説書修正の作業ルール（文書表現・トンマナ）が記載されている
- Excel のみ言及していた箇所が YAML にも対応した記述（ExcelまたはYAML形式で記述できると明示）に更新されている
- 新規追加・変更した RST が Sphinx でビルドエラーなく通る
- 既存の RST の toctree 参照が壊れていない

# Assumptions

- YAML 対応は `nablarch-testing` 本体（PR #75 / `convert-testdata-excel-to-text` ブランチ）で実装済みであり、解説書はそれに合わせたドキュメント変更である
- 入力資料（`.rn/ntf-yaml-support/input/` 配下10ファイル）が YAML 形式の仕様・記述例の正典となる
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

### Excel/YAML 並列記述の方針

- 「Excelの場合」「YAMLの場合」の見出し分けで並列掲載する（sphinx-tabs は使用しない — D-1 合意）
- 共通説明は見出し分けせず冒頭にまとめる。冒頭に「テストデータは Excel または YAML ファイルで記述できる。」を入れる
- 見出し分けの例（`小見出し` レベルの `-` アンダーライン）:

  ```rst
  Excelの場合
  -----------

  （Excel 向けの説明・例）

  YAMLの場合
  ----------

  （YAML 向けの説明・例）
  ```

### 用語対応表（Excel ↔ YAML）

YAML 追記時、以下の対応で表記する（input/ の仕様資料を正典とする）:

| Excel 用語 | YAML 対応用語 |
|---|---|
| シート | ファイル（YAMLファイル） |
| データタイプ行（1行目） | `dataType` キー |
| グループID | `id` キー |

- `testShots`・`LIST_MAP` 等の識別子名は既存ページでの表記をそのまま使う
- YAML 固有のキー名・構造は `.rn/ntf-yaml-support/input/ntf-testdata-doc.md` を参照する

### ファイル構造（このブランチで追加するファイル）

```
06_TestFWGuide/
  testdata/
    index.rst          ← B-1 の入口
    overview.rst       ← B-1-1 全体像
    data-blocks.rst    ← B-1-2 データブロック種別
    testshots.rst      ← B-1-3 testShots
    table-data.rst     ← B-1-4 テーブルデータ
    file-data.rst      ← B-1-5 ファイルデータ
    messaging.rst      ← B-1-6 メッセージング
    values.rst         ← B-1-7 値の書き方
```

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

- `make html` がエラーなく完了した事実が `checks/task1.md` に記録されている（警告は許容、エラーは不可）

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
- ユーザーが全体構成を確認・承認している（Decisions に記録）

### #3: 文書表現・トンマナ確認とCLAUDE.md作業ルール記載

**Purpose**: 既存解説書の文書表現・トンマナ（用語の統一・文体・表記ルール）を確認し、解説書修正作業のルールをCLAUDE.mdに記載する。

**Prerequisites**: #2

**Steps**:

- [ ] 既存解説書（`06_TestFWGuide/01_Abstract.rst` 等）と入力資料（`ntf-doc-terms.md`）から用語・表記ルールを抽出する
- [ ] 文体（です・ます調 vs だ・である調）・用語統一ルールをまとめる
- [ ] `CLAUDE.md` に作業ルールを記載する
- [ ] self-check (OK/NG per completion criterion, record in checks/task3.md)
- [ ] QA expert review (subagent)
- [ ] user review

**Completion criteria**:

- `CLAUDE.md` にNTF解説書修正の作業ルール（文書表現・用語・トンマナ）が記載されている

### #4: toctree 構成変更（A章・B章の骨格作成）

**Purpose**: proposed-structure.md の新構成ツリーに合わせて、既存の toctree を組み替え、A章・B章の骨格（index.rst）を作成する。ファイル移動は行わず toctree の付け替えと新規 index.rst の追加のみで完結させる。

**Prerequisites**: #3

**Steps**:

- [ ] 新構成ツリーに合わせた index.rst の変更・新規ファイルを確認・作成する
  - `06_TestFWGuide/index.rst`（または親ページ）の toctree を A章・B章構成に組み替える
  - `06_TestFWGuide/testdata/index.rst` を新規作成（B-1 の入口）
- [ ] `make html` でビルドエラーがないことを確認する
- [ ] self-check (OK/NG per completion criterion, record in checks/task4.md)
- [ ] QA expert review (subagent)
- [ ] user review

**Completion criteria**:

- A章（`Nablarchテスティングフレームワークとは`）・B章（`テストの実装方法`）が toctree に現れている
- `make html` がエラーなく完了する
- 既存ファイルへの toctree 参照が壊れていない

### #5: B-1「テストデータの記述方法」新規作成

**Purpose**: `ntf-testdata-doc.md` を主素材に、テストデータ仕様リファレンス（B-1-1〜B-1-7）を RST ファイルとして新規作成する。Excel/YAML 並列記述は「Excelの場合」「YAMLの場合」見出し分けで行う。

**Prerequisites**: #4

**Steps**:

- [ ] `06_TestFWGuide/testdata/` 配下に以下の7ファイルを作成する:
  `overview.rst` / `data-blocks.rst` / `testshots.rst` / `table-data.rst` / `file-data.rst` / `messaging.rst` / `values.rst`
- [ ] 各ファイルに `ntf-testdata-doc.md` の対応章（§1〜10）と examples ファイルの内容を RST 化して記述する
- [ ] `testdata/index.rst` の toctree にすべて追加する
- [ ] `make html` でビルドエラーがないことを確認する
- [ ] self-check (OK/NG per completion criterion, record in checks/task5.md)
- [ ] QA expert review (subagent)
- [ ] user review

**Completion criteria**:

- `testdata/` 配下に B-1-1〜B-1-7 の RST ファイルが存在し、toctree に追加されている
- `ntf-testdata-doc.md` の全章（§1〜10）が B-1 のいずれかの節に対応している
- Excel/YAML の記述例が各節に両方掲載されている
- `make html` がエラーなく完了する

### #6: 既存ページのテストデータ参照をB-1へ差し替え

**Purpose**: `05_UnitTestGuide/` 配下の各ページで「テストデータの書き方」を解説している箇所を B-1 への参照リンクに置き換え、重複記述を解消する。

**Prerequisites**: #5

**Steps**:

- [ ] proposed-structure.md の新旧マッピング表を参照し、対象ページ（B-3〜B-5 相当）を特定する
- [ ] 各ページの「テストデータの書き方」節を `:ref:` 参照リンクに置き換える
- [ ] `02_DbAccessTest.rst` の冒頭にテストデータ参照誘導を追加する
- [ ] `make html` でビルドエラー・壊れた参照がないことを確認する
- [ ] self-check (OK/NG per completion criterion, record in checks/task6.md)
- [ ] QA expert review (subagent)
- [ ] user review

**Completion criteria**:

- 対象ページの「テストデータの書き方」節が B-1 への参照に変わっている
- `make html` がエラーなく完了する
- 既存の `:ref:` ラベルが壊れていない

# Decisions

### D-1: 新構成案への合意（2026-06-26）

ユーザーと議論の上、proposed-structure.md（`.rn/ntf-yaml-support/proposed-structure.md`）に記載の新構成案で合意した。主な合意内容:

- トップ2ページ: 「Nablarchテスティングフレームワークとは」（A章）「テストの実装方法」（B章）
- テストデータは B-1「テストデータの記述方法」（仕様）+ B-2「テストデータの記述例」の2ページ構成（※B-2はタスク追加時に検討）
- Excel/YAML 並列表示は「Excelの場合」「YAMLの場合」見出し分けを採用（sphinx-tabs は使わない）
- ディレクトリ構造は既存パスを維持し toctree のみ組み替える
- input/ のうち `ntf-testdata-loading.md` と `testdata-converter-design.md` は使わない

# State

- **Status**: paused
- **Date**: 2026-06-26
- **Last completed**: #3 文書表現・トンマナ確認とCLAUDE.md作業ルール記載（QA PASS、ユーザーレビュー待ち）
- **Next**: #3 のユーザー承認 → チェックオフ → #4 toctree 構成変更
- **Notes**: |
    Task #3 は実装・QA ともに完了し、ユーザーレビュー段階で中断した。
    CLAUDE.md をユーザー指摘により刷新済み（汎用ルール集に絞り、タスク固有ルールはステアリングの Rules に移動）。

    【CLAUDE.md の現在の内容】
    - 文体: だ・である調（既存ページ実測）
    - 用語: 「既存ページに合わせる、推測しない」を原則
    - RST 記法: 見出しレベル・コードブロック（4スペース）・テーブル・ラベル等
    - ビルドコマンド: make html SPHINXBUILD=/tmp/sphinx_env/bin/sphinx-build

    【Task #3 完了基準】
    - CLAUDE.md にNTF解説書修正の作業ルール（文書表現・用語・トンマナ）が記載されている → OK

    【次のアクション】
    1. ユーザーに Task #3 の承認を求める
    2. 承認後 steering.md の #3 をチェックオフしてコミット
    3. Task #4（toctree 構成変更 — A章・B章の骨格作成）に着手

    ビルド環境: `/tmp/sphinx_env`（Sphinx 1.8.6）、`make html SPHINXBUILD=/tmp/sphinx_env/bin/sphinx-build`
