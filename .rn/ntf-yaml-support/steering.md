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
- 文書表現・トンマナは CLAUDE.md に記載したルールに従う
- 日本語で記述する（ファイルパス・コマンド・コード例は除く）
- 既存の Excel 向け記述を削除しない（YAML を追記する形で対応）
- 新規 RST ファイルを追加する場合は toctree にも追記する

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
- [ ] user review（構成認識の合意）

**Completion criteria**:

- `06_TestFWGuide/` 配下の全ファイルの役割と、YAML対応で修正が必要な箇所の一覧が `checks/task2.md` に記録されている
- ユーザーが全体構成を確認・承認している（Decisions に記録）

### #3: 影響範囲確認とタスク更新

**Purpose**: 全体構成の合意をもとに、修正が必要なファイルと修正内容を具体化し、タスク一覧を更新する。

**Prerequisites**: #2

**Steps**:

- [ ] 修正対象ファイルをリストアップし、各ファイルで必要な変更内容を `checks/task3.md` に記録する
- [ ] 解説書修正の各タスク（#5以降）をステアリングに追記する
- [ ] self-check (OK/NG per completion criterion, record in checks/task3.md)
- [ ] user review

**Completion criteria**:

- 修正対象ファイルと変更内容の一覧が `checks/task3.md` に記録されている
- ステアリングに解説書修正タスクが追記されている

### #4: 文書表現・トンマナ確認とCLAUDE.md作業ルール記載

**Purpose**: 既存解説書の文書表現・トンマナ（用語の統一・文体・表記ルール）を確認し、解説書修正作業のルールをCLAUDE.mdに記載する。

**Prerequisites**: #3

**Steps**:

- [ ] 既存解説書（`06_TestFWGuide/01_Abstract.rst` 等）と入力資料（`ntf-doc-terms.md`）から用語・表記ルールを抽出する
- [ ] 文体（です・ます調 vs だ・である調）・用語統一ルールをまとめる
- [ ] `CLAUDE.md` に作業ルールを記載する
- [ ] self-check (OK/NG per completion criterion, record in checks/task4.md)
- [ ] QA expert review (subagent)
- [ ] user review

**Completion criteria**:

- `CLAUDE.md` にNTF解説書修正の作業ルール（文書表現・用語・トンマナ）が記載されている

### #5以降: 解説書修正（タスク#3完了後に追記）

（#3完了後、影響範囲確認の結果をもとに具体的な修正タスクをここに追記する）

# Decisions

（未記入 — 作業中に記録）

# State

- **Status**: not suspended
- **Date**: 2026-06-26
- **Last completed**: #1 RSTビルド確認
- **Next**: #2 全体構成の認識合わせ
- **Notes**: ビルド環境は `/tmp/sphinx_env`（Sphinx 1.8.6）。`make html SPHINXBUILD=/tmp/sphinx_env/bin/sphinx-build` で実行。後続タスクも同 venv を再利用すること。
