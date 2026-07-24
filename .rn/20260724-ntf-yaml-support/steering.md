Rn version: 0.8.0

# Goal

`design.md` の章構成に従って、NTF（Nablarch Testing Framework）解説書を白紙から再構築する。

# Acceptance criteria

- **全量を失わない** — 現行解説書とinput資料の記載内容が、新構成のどこかに必ず存在する
- **重複がない** — 同じ内容が複数箇所に存在しない。参照で解決する
- **用語が統一されている** — 全ページで `glossary.md` に従った表記になっている
- **トンマナが揃っている** — FW解説書のライブラリと記述の調子が一致する
- **`make html` がエラー0で完了する**

# Assumptions

- 作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-rebuild-instruction.md`
- 章構成設計: `.rn/20260724-ntf-yaml-support/design.md`
- 現行解説書（IN側）: `ja/development_tools/testing_framework/` 配下の全 `.rst`（develop ブランチ）
- input資料（IN側）: `.rn/20260724-ntf-yaml-support/input/` 配下の全 `.md`（`design.md` を除く）
- トンマナ基準: `ja/application_framework/application_framework/libraries/` 配下の `.rst`

# Rules

- commit and push every change; one completion marker per task
- 日本語で記述する
- マッピングが唯一の基準。マッピングにない内容を追加しない。マッピングにある内容を落とさない
- user review の承認を受けるまで次タスクに着手しない
- CSVのレコード数は `csv.DictReader` でカウントする。`wc -l` は使わない

# Tasks

### #1: 作業指示の受領とタスク詳細化

**Purpose**: 作業指示を受領し、steering.md を確定させる。

**Prerequisites**: none

**Steps**:

- [x] ユーザーから作業指示を受け取る（`ntf-doc-rebuild-instruction.md`）
- [x] Acceptance criteria を具体化して更新する
- [x] Tasks を作業指示に基づいて詳細化して更新する
- [x] commit & push

**Completion criteria**:

- Acceptance criteria に具体的な検証可能な条件が記載されている
- Tasks にユーザー指示に対応したタスクが分解・記載されている

### #2: セクション抽出ツールの作成

**Purpose**: 現行解説書とinput資料の記載内容を、セクション単位で機械的に抽出する。

**Prerequisites**: #1

**Steps**:

- [x] `mapping/tools/extract_sections.py` を作成する
  - RST と Markdown の両方を扱う
  - 抽出単位は **L3相当のセクション**。RSTは見出しレベル3（ページタイトルをL1とする）、MarkdownはH3
  - L3配下にL4以下がある場合、それらはL3セクションに含める（別項目にしない）
  - 出力列: `section_id, src_file, src_line, heading_path, lines, code_blocks, tables, figures`
  - **人の判断・要約を入れない。** 原文から機械的に取れる情報のみ
- [x] `mapping/tools/build_mapping.sh` を作成する
  - 現行解説書は `git show <base>:<path>` で取得する（base は `git merge-base origin/develop HEAD`）
  - input資料は作業ツリーから取得する
  - 出力: `mapping/sections-current.csv`、`mapping/sections-input.csv`
- [x] self-check（`checks/task-02.md`）
- [x] commit & push
- [ ] **user review** — 承認を受けるまで #3 に進まない

**Completion criteria**:

- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）
- 抽出対象ファイル数が実ファイル数と一致することを Evidence に記載
- CSVのレコード数を **`csv.DictReader` でカウントした値** で Evidence に記載
- 抽出したセクション数が、実ファイルから独立に数えた見出し数と一致することを Evidence に記載

### #3: 用語集の作成

**Purpose**: 全ページで統一する用語を確定する。

**Prerequisites**: #2

**Steps**:

- [ ] `mapping/glossary.md` を作成する
- [ ] 現行解説書・input資料（特に `input/ntf-doc-terms.md`）・FW解説書から用語を抽出する
- [ ] 各用語について「正表記 / 意味 / 揺れ表記（file:line付き） / 採用根拠」を記載する
- [ ] 採用優先順位: FW解説書 > 現行解説書・input資料（意味が明確で一貫しているもの） > 新規定義
- [ ] 表記揺れを機械的に検出する（読点・接続の揺れ、処理方式名称、テスト種別名称）
- [ ] self-check（`checks/task-03.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #4 に進まない

**Completion criteria**:

- 用語集に、現行解説書とinput資料に登場する主要な用語が網羅されている
- 各用語の「揺れ表記」に file:line の根拠がある
- 処理方式の名称が design.md の正式名称と一致している
- FW解説書と異なる表記を採用した場合、理由が採用根拠に記載されている

### #4: トンマナ規約の作成

**Purpose**: FW解説書のライブラリの記述の調子を規約として明文化する。

**Prerequisites**: #3

**Steps**:

- [ ] `mapping/style.md` を作成する
- [ ] 抽出元は `ja/application_framework/application_framework/libraries/` 配下の `.rst`（複数ページから抽出）
- [ ] 各規約に規約ID（`S-01` 形式）、規約内容、根拠（file:line、**2件以上**）を付す
- [ ] 観点: 文体 / セクション構成 / セクションタイトル形式 / 見出しアンダーライン記法 / コードブロック / アドモニション / 表の記法 / `:ref:` ラベル命名規則 / 文の長さ・改行位置 / 図の配置
- [ ] **現行解説書のRSTを基準にしない**
- [ ] self-check（`checks/task-04.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #5 に進まない

**Completion criteria**:

- 全規約に FW解説書ライブラリからの根拠 file:line が2件以上ある
- design.md の第2部・第3部のページアウトラインと矛盾がない

### #5: マッピングリストの作成

**Purpose**: 現行解説書とinput資料の全セクションを design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。

**Prerequisites**: #4

**Steps**:

- [ ] `mapping/mapping.csv` を作成する（列: `mapping_id, src_type, src_file, src_line, heading_path, lines, audience, dest_part, dest_page, dest_section, disposition, note`）
- [ ] `disposition` は5値（`MOVE` / `MERGE` / `SPLIT` / `REFERENCE` / `DROP`）
- [ ] 全行に `audience`（`user` / `developer`）を付与。`developer` は `disposition=DROP`
- [ ] `sections-current.csv` / `sections-input.csv` の全 `section_id` が `mapping.csv` に最低1回現れること
- [ ] `mapping/volume.md` を作成する（`dest_page` ごとに `lines` を集計）
- [ ] self-check（`checks/task-05.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #6 に進まない

**Completion criteria**:

- `sections-current.csv` / `sections-input.csv` の全 `section_id` が取りこぼしゼロで `mapping.csv` に存在する
- `disposition` / `audience` が空欄の行が0件
- `DROP` の全行に `note` が記入されている
- `dest_page` / `dest_section` に design.md に存在しないものが含まれていない
- `volume.md` にページ別文量の集計表がある

### #6: 未確定事項の確定と design.md 更新

**Purpose**: 文量集計に基づいて未確定事項を確定させる。

**Prerequisites**: #5

**Steps**:

- [ ] `volume.md` の集計をもとに、design.md「10. 未確定事項」の3件を確定する
- [ ] design.md を更新する（「未確定事項」節を削除し、確定した構成を本文に反映）
- [ ] 確定に伴い `mapping.csv` の `dest_page` を更新する
- [ ] self-check（`checks/task-06.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #7 に進まない

**Completion criteria**:

- design.md に未確定事項が残っていない
- design.md の章構成と `mapping.csv` の `dest_page` の集合が一致する
- ファイル名に連番（`01_`, `02_` 等）が使われていない

### #7: 現行NTF解説書の削除

**Purpose**: 白紙の状態を作る。

**Prerequisites**: #6

**Steps**:

- [ ] `ja/development_tools/testing_framework/` 配下の `.rst` を削除する
- [ ] `ja/development_tools/index.rst` の NTF への toctree 参照の現状を `checks/task-07.md` に記録する
- [ ] 削除前の全ファイル一覧（パスと行数）を `checks/task-07.md` に記録する
- [ ] 画像ファイル（`_image/`、`_images/`）およびダウンロード素材は削除しない
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #8 に進まない

**Completion criteria**:

- `ja/development_tools/testing_framework/` 配下に `.rst` が存在しない
- 削除前のファイル一覧が Evidence に記録されている
- 画像・ダウンロード素材が保持されている

### #8〜: ページの作成（1ページにつき1タスク）

**Purpose**: マッピングに従ってページを1つ作成する。

**Prerequisites**: #7（以降は直前のページタスク）

作成順: 第1部 → 第3部のテストデータ2ページ → 第2部 → 第3部の残り

タスク番号・ページIDは #5 のマッピング完了後に確定する。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] 抽出した行の出典（`src_file:src_line`）を実際に読み、ページを作成する
- [ ] マッピングにない内容を追加しない。マッピングにある内容を落とさない
- [ ] 出典の文面をそのまま流用しない。`style.md` に従って書き直す
- [ ] 用語は `glossary.md` の正表記を使う
- [ ] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（A:網羅性 / B:トンマナ / C:用語 / D:整合性）
- [ ] 指摘への対応を行う（最大3ラウンド）
- [ ] レビュー記録を `reviews/page-<ページID>.md` に作成する
- [ ] self-check（`checks/task-NN.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで次ページに進まない

**Completion criteria**:

- `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く）
- 4観点のレビューがすべて実施・記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が当該ページについてエラーを出さない

### #last: Evaluation sign-off

**Purpose**: NTF ドキュメント刷新の完了を Acceptance criteria に照らして確認し、ユーザーの承認を得る。

**Prerequisites**: すべてのページ作成タスク完了

**Steps**:

- [ ] Acceptance criteria の達成状況を確認する
- [ ] `make html` がエラー0で完了することを確認する
- [ ] 結果をユーザーに提示して `/rn:ty`（承認）または `/rn:gm`（修正）の判定をもらう

**Completion criteria**:

- すべての Acceptance criteria が達成されていることが確認できる
- ユーザーが `/rn:ty` で承認している

# State

- **Status**: paused
- **Date**: 2026-07-24
- **Last completed**: #2 セクション抽出ツールの作成（ユーザーレビュー待ち。/rn:ty で承認後 #3 に進む）
- **Next**: #3 用語集の作成
- **Notes**: PR #728 (ntf-yaml-support)。mapping.csv に src_section_id カラム追加をユーザーが指示済み（選択肢1）— タスク #5 で対応。#2 user review はサスペンド時点で未取得。
