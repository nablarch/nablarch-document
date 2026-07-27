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
- レビューを依頼するサブエージェントのプロンプトには、必ず次の3点を入れる。#3 ラウンド1で実際に欠陥を掘り当てたのはこの3点である
  - **実測コマンドで裏付けよ。推測で書くな**（指摘は実行したコマンドまたは実ファイルの引用で裏付ける）
  - **成果物に付属する検証スクリプトを正解として使わず、独立に組め**（`verify_glossary.py` 等を信頼すると同じ穴を素通りする）
  - **敵対的にレビューせよ**（欠陥は存在するという前提で、境界・抜け道・見落としを探す）
- レビューは4観点を**それぞれ別のサブエージェント**で回す（QA / 設計 / クラフト / 検証）。各観点に成果物・目的・完了条件・チェックリストだけを渡し、self-check ファイルや他観点の判定は渡さない

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
  - **人の判断・要約を入れない。** 原文から機械的に取れる情報のみ
- [x] `mapping/tools/build_mapping.sh` を作成する
  - 現行解説書は `git show <base>:<path>` で取得する（base は `git merge-base origin/develop HEAD`）
  - input資料は作業ツリーから取得する
  - 出力: `mapping/sections-current.csv`、`mapping/sections-input.csv`
- [x] self-check（`checks/task-02.md`）
- [x] commit & push
- [x] **user review** — 承認済み

**Completion criteria**:

- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）
- 抽出対象ファイル数が実ファイル数と一致することを Evidence に記載
- CSVのレコード数を **`csv.DictReader` でカウントした値** で Evidence に記載
- 抽出したセクション数が、実ファイルから独立に数えた見出し数と一致することを Evidence に記載

### #2a: セクション抽出の取りこぼし解消

**Purpose**: 見出し階層のどこにも属さない本文が発生しないよう抽出ルールを修正し、行の取りこぼしゼロを機械的に証明する。

**Prerequisites**: #2

**Steps**:

- [x] `mapping/tools/extract_sections.py` の抽出ルールを修正する
  - L3セクションを持つL2は、各L3をセクションとして抽出する
  - 同じL2の直下にありL3配下に属さない本文は、独立したセクションとして抽出する。`heading_path` は当該L2までとし、L3相当の位置に `(L2直下)` の印を付ける
  - L3セクションを持たないL2は、そのL2をセクションとして抽出する
  - L1直下にありL2配下に属さない本文も、同様に `(L1直下)` として独立セクションにする
  - 最初の見出しより前の本文は `(冒頭)` として独立セクションにする
- [x] `lines` を「本文開始行から次のセクション開始行の直前まで」の全行数とする（末尾空行を除く処理を廃止）
- [x] カバー範囲をCSVに明示する（`body_start_line` / `body_end_line` 列を追加）
- [x] `mapping/tools/verify_coverage.py` を作成し、カバー範囲を行番号の集合として構築して全行との差集合で検証する
- [x] `build_mapping.sh` から検証を実行する
- [x] テストを新仕様に更新し、取りこぼしゼロの性質テストを追加する
- [x] self-check（`checks/task-02a.md`）
- [x] commit & push
- [x] **user review** — 承認済み

**Completion criteria**:

- `lines` が当該セクションのカバー範囲そのものである（`body_end_line - body_start_line + 1 == lines`）
- セクションのカバー範囲の和集合と全行集合の差が、見出し行を除いて非空行0件である
- 見出し行以外に未カバー行が残る場合、その行と理由が `checks/task-02a.md` に全件列挙されている
- 抽出対象ファイル数が RST 47・MD 10 であり、セクション0件のファイルが存在しない
- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）

### #3: 用語集の作成

**Purpose**: 全ページで統一する用語を確定する。

**Prerequisites**: #2a

**Steps**:

- [x] `mapping/glossary.md` を作成する
- [x] 現行解説書・input資料（特に `input/ntf-doc-terms.md`）・FW解説書から用語を抽出する
- [x] 各用語について「正表記 / 意味 / 揺れ表記（file:line付き） / 採用根拠」を記載する
- [x] 採用優先順位: FW解説書 > 現行解説書・input資料（意味が明確で一貫しているもの） > 新規定義
- [x] 表記揺れを機械的に検出する（読点・接続の揺れ、処理方式名称、テスト種別名称）
- [x] `mapping/tools/verify_glossary.py` を作成し、file:line・件数・§5と§8の整合を機械検証する
- [x] self-check（`checks/task-03.md`）
- [x] commit & push
- [ ] 4観点の再レビュー（ラウンド2、対象 `277e23a`）— ラウンド1は4観点とも NG で修正済み。**プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
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
- [ ] `glossary.md` §6・§11.2 の申し送りを取り込む（括弧の全角半角、英数字と日本語の間の空白、送り仮名・漢字/かなの揺れ。いずれも #3 で実測データを保存済み。規範の決定は #4 の管掌）
- [ ] **現行解説書のRSTを基準にしない**
- [ ] self-check（`checks/task-04.md`）
- [ ] 4観点のレビュー（QA / 設計 / クラフト / 検証）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #4a に進まない

**Completion criteria**:

- 全規約に FW解説書ライブラリからの根拠 file:line が2件以上ある
- design.md の第2部・第3部のページアウトラインと矛盾がない

### #4a: 大きいセクションの分割判断

**Purpose**: マッピング作成の前に、複数の割当先に分かれるセクションを特定し、分割位置を確定する。マッピング作成を機械的な作業にするため。

**Prerequisites**: #4

抽出の実態（#2a 完了時点の実測値）:

| 項目 | current | input |
|---|---|---|
| セクション数 | 377 | 202 |
| 行数（body） | 9,783 | 3,203 |
| 中央値 | 12行 | 12行 |
| 100行超 | 23件（全体の36%の行） | 0件 |
| 200行超 | 6件（15%） | 0件 |
| 最大 | 314行 | 63行 |

input側は最大63行のため分割は不要。current側の大きいセクションのみが対象。抽出粒度は変更しない（L4まで細分化すると全セクション数が倍増し、23セクションのために全体の判断コストが上がるため）。

**対象**: `sections-current.csv` のうち `lines >= 100` のセクション（23件）

**Steps**:

- [ ] `mapping/split-plan.md` を作成する
- [ ] 対象23セクションについて、内容を実際に読み、design.md のどの割当先に属するかを検討する
- [ ] 単一の割当先に収まるか、複数に分かれるかを判定する
- [ ] 複数に分かれる場合、分割位置を行番号で特定する
- [ ] 表形式で記録する（列: `section_id, heading_path, lines, split, parts, rationale`）
  - `split` は `no` / `yes`
  - `parts` は `開始行-終了行 → 割当先` を1行1件で列挙
- [ ] **分割しない判断も `rationale` を記す。** 内容に基づく理由を書く。行数が少ないから、では不可
- [ ] 分割する場合、分割後の行範囲が元のセクション範囲を過不足なく覆うこと
- [ ] self-check（`checks/task-04a.md`）
- [ ] 4観点のレビュー（QA / 設計 / クラフト / 検証）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #5 に進まない

**Completion criteria**:

- 対象23セクションすべてに `split` の判定と `rationale` がある
- `split=yes` の全件について、`parts` の行範囲の和集合が元のセクションの `body_start_line`〜`body_end_line` と一致する（隙間・重複ゼロ）
- `parts` の割当先が design.md の章構成に存在するページ・セクションである

**注記**: `lines < 100` のセクションでも分割が必要と判明した場合は #5 の中で対応してよい。その場合は `split-plan.md` に追記し `rationale` を残す。

### #5: マッピングリストの作成

**Purpose**: 現行解説書とinput資料の全セクションを design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。

**Prerequisites**: #4a

**Steps**:

- [ ] `mapping/mapping.csv` を作成する（列: `mapping_id, src_section_id, src_type, src_file, src_body_start, src_body_end, heading_path, lines, audience, dest_part, dest_page, dest_section, disposition, note`）
  - `src_section_id` は `sections-current.csv` / `sections-input.csv` の `section_id` を指す
  - `lines` は `src_body_end - src_body_start + 1`
  - `disposition` が `SPLIT` 以外 — セクションの `body_start_line` / `body_end_line` をそのまま入れる
  - `disposition` が `SPLIT` — `split-plan.md` の `parts` に従い分割後の行範囲を入れる。行を複製し、各行に異なる範囲と割当先を記す
- [ ] 出典ファイル単位でサブエージェントに分担させる（579セクションを1コンテキストで処理すると後半で判断がぶれるため）
  - 1エージェントあたり10〜20セクション程度
  - 入力: 担当ファイルのセクション一覧 / 担当ファイルの実内容 / `design.md` / `glossary.md` / `split-plan.md`（100行超セクションを含む場合）
  - 出力を統合し、`mapping_id` の重複と割当先の表記揺れを機械的に検査する
- [ ] `disposition` は5値（`MOVE` / `MERGE` / `SPLIT` / `REFERENCE` / `DROP`）
- [ ] 全行に `audience`（`user` / `developer`）を付与。`developer` は `disposition=DROP` とし `note` に理由を記す
  - `input/ntf-testdata-loading.md` は原則 `developer` だがセクション単位で判定する
- [ ] 現行の `03_Tips.rst` の各項目は該当ページの「使用方法」に `MERGE` する。独立ページにしない
- [ ] `mapping/tools/verify_mapping.py` を作成し、取りこぼし検証を行範囲の集合演算で行う
  - `lines` 合計（全行）と `lines` 合計（`DROP` を除く）を**両方出力する**
- [ ] `mapping/volume.md` を作成する（`dest_page` ごとに `lines` を集計）
  - `DROP` を除いた `lines` 合計を記載する（新構成に移る実質的な分量）
  - `DROP` の合計行数と、その内訳（`note` の理由別）も記載する
- [ ] self-check（`checks/task-05.md`）
- [ ] 4観点のレビュー（QA / 設計 / クラフト / 検証）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #6 に進まない

**Completion criteria**:

- `mapping.csv` に `DROP` 行も含めて全セクションが残っている（追跡可能性のため削除しない）
- `sections-current.csv` / `sections-input.csv` の全 `section_id` が `mapping.csv` の `src_section_id` に最低1回現れる
- 各 `src_section_id` について、紐づく全マッピング行の `[src_body_start, src_body_end]` の和集合が、元のセクションの `[body_start_line, body_end_line]` と一致する（隙間・重複ゼロ）
- `mapping.csv` の `lines` 合計が 12,986（9,783 + 3,203）と一致する（取りこぼしゼロの確認）
- `DROP` を除いた `lines` 合計が `volume.md` に記載されている（新構成に移る実質的な分量）
- `verify_mapping.py` が上記2つの数値を両方出力する
- `disposition` / `audience` が空欄の行が0件
- `DROP` の全行に `note` が記入されている
- `dest_page` / `dest_section` に design.md に存在しないものが含まれていない
- `volume.md` にページ別文量の集計表がある
- 検証は `mapping/tools/verify_mapping.py` で行い、コミットされている（手作業で確認しない）

### #6: 未確定事項の確定と design.md 更新

**Purpose**: 文量集計に基づいて未確定事項を確定させる。

**Prerequisites**: #5

**Steps**:

- [ ] `volume.md` の集計をもとに、design.md「10. 未確定事項」の3件を確定する
- [ ] design.md を更新する（「未確定事項」節を削除し、確定した構成を本文に反映）
- [ ] 確定に伴い `mapping.csv` の `dest_page` を更新する
- [ ] self-check（`checks/task-06.md`）
- [ ] 4観点のレビュー（QA / 設計 / クラフト / 検証）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
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
- [ ] 4観点のレビュー（QA / 設計 / クラフト / 検証）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
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
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
- [ ] マッピングにない内容を追加しない。マッピングにある内容を落とさない
- [ ] 出典の文面をそのまま流用しない。`style.md` に従って書き直す
- [ ] 用語は `glossary.md` の正表記を使う
- [ ] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（A:網羅性 / B:トンマナ / C:用語 / D:整合性）
  - **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
  - この4観点はページ内容の観点であり、Rules の4観点（QA / 設計 / クラフト / 検証）とは別軸である。ページ作成タスクでは**本欄のA〜Dを用いる**（A:網羅性がQAを、B:トンマナがクラフトを、C:用語とD:整合性が検証を兼ねる）
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
- **Date**: 2026-07-27
- **Last completed**: #2a セクション抽出の取りこぼし解消（ユーザーレビュー承認済み）
- **Next**: #3 用語集の作成 — 実装と修正ラウンド1は完了（`277e23a`）。**再開後の最初の具体的作業は、`277e23a` に対する4観点（QA / 設計 / クラフト / 検証）の再レビュー（ラウンド2）**。トリアージ上限3ラウンドのうち2ラウンド目。指摘と対応の対照は `checks/task-03.md`「レビューの経過」および「レビュー指摘への対応一覧」（A-1〜E）にある
- **Notes**: push 先はローカル `work` → `origin/work`（origin = fork `lovaizu/nablarch-document`）。親 `nablarch/nablarch-document` へは push しない。親の draft PR #728 は凍結中で触らない。完成後に fork → 親 の PR を出す。／利用枠の都合で Opus から Sonnet 5 への切替を挟んでいる。／#6 で解決する事項が #3 で判明: `design.md` に受け皿のないページ（HTMLチェックツール、メール送信、ファイルアップロード、二重サブミット防止機能、データベースを使用するクラスのテスト）。`glossary.md` §10 に記録済み。／#3 の再レビュー用プロンプトは会話に残らないため、`checks/task-03.md` の各観点の Evidence 列を起点に再構成すること
