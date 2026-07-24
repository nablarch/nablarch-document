# 作業指示書：NTF解説書の刷新

対象ブランチ: PR #728（`.rn/20260724-ntf-yaml-support/`）

## ゴール

`design.md` の章構成に従って、NTF解説書を白紙から再構築する。

達成条件は4つ。

- **全量を失わない** — 現行解説書とinput資料の記載内容が、新構成のどこかに必ず存在する
- **重複がない** — 同じ内容が複数箇所に存在しない。参照で解決する
- **用語が統一されている** — 全ページで用語集に従った表記になっている
- **トンマナが揃っている** — FW解説書のライブラリと記述の調子が一致する

## 対象範囲

| 区分 | パス |
|---|---|
| 現行解説書（マッピングのIN側） | `ja/development_tools/testing_framework/` 配下の全 `.rst`（develop ブランチの状態） |
| input資料（マッピングのIN側） | `.rn/20260724-ntf-yaml-support/input/` 配下の全 `.md`（`design.md` を除く） |
| 章構成（マッピングのOUT側） | `.rn/20260724-ntf-yaml-support/design.md` |
| トンマナの基準 | `ja/application_framework/application_framework/libraries/` 配下の `.rst` |

## 成果物の配置

```
.rn/20260724-ntf-yaml-support/
├── design.md              （既存。#5 で更新する）
├── input/                 （既存）
├── mapping/
│   ├── mapping.csv        マッピングリスト（本作業の基準）
│   ├── glossary.md        用語集
│   ├── style.md           トンマナ規約
│   ├── volume.md          ページ別文量集計
│   └── tools/
│       ├── extract_sections.py
│       └── build_mapping.sh
└── reviews/
    └── page-<ページID>.md  ページごとのレビュー記録
```

---

## タスク

### #1: セクション抽出ツールの作成

**Purpose**: 現行解説書とinput資料の記載内容を、セクション単位で機械的に抽出する。

**Steps**:

- [ ] `mapping/tools/extract_sections.py` を作成する
  - RST と Markdown の両方を扱う
  - 抽出単位は **L3相当のセクション**。RSTは見出しレベル3（ページタイトルをL1とする）、MarkdownはH3
  - L3配下にL4以下がある場合、それらはL3セクションに含める（別項目にしない）
  - 出力列: `section_id, src_file, src_line, heading_path, lines, code_blocks, tables, figures`
  - **人の判断・要約を入れない。** 原文から機械的に取れる情報のみ
- [ ] `mapping/tools/build_mapping.sh` を作成する
  - 現行解説書は `git show <base>:<path>` で取得する（base は `git merge-base origin/develop HEAD`）
  - input資料は作業ツリーから取得する
  - 出力: `mapping/sections-current.csv`、`mapping/sections-input.csv`
- [ ] self-check（`checks/task-01.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #2 に進まない

**Completion criteria**:

- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）
- 抽出対象ファイル数が実ファイル数と一致することを Evidence に記載
- CSVのレコード数を **`csv.DictReader` でカウントした値** で Evidence に記載する（`wc -l` はフィールド内改行を多重カウントするため使わない）
- 抽出したセクション数が、実ファイルから独立に数えた見出し数と一致することを Evidence に記載

---

### #2: 用語集の作成

**Purpose**: 全ページで統一する用語を確定する。現行解説書とinput資料で用語が揺れているため、先に基準を作る。

**Prerequisites**: #1

**Steps**:

- [ ] `mapping/glossary.md` を作成する
- [ ] 用語を以下の3ソースから抽出する
  - 現行解説書（`ja/development_tools/testing_framework/`）
  - input資料（特に `input/ntf-doc-terms.md`）
  - FW解説書（`ja/application_framework/`）
- [ ] 各用語について以下を記載する

| 列 | 内容 |
|---|---|
| 正表記 | 採用する表記 |
| 意味 | 1〜2文 |
| 揺れ表記 | 現行解説書・input資料に存在する別表記（file:line 付き） |
| 採用根拠 | なぜその表記を正としたか |

- [ ] 採用の優先順位は次のとおり
  1. FW解説書に同じ概念の用語がある場合、**FW解説書の用語を採用する**
  2. FW解説書にない場合、現行解説書とinput資料のうち、意味が明確で一貫しているものを採用する
  3. どちらも不適切な場合、新たに定める（理由を採用根拠に記す）
- [ ] `input/ntf-doc-terms.md` を**そのまま採用しない**。候補として扱い、既存解説書およびFW解説書と突き合わせて確定する
- [ ] 表記揺れを機械的に検出する。少なくとも以下を確認する
  - 読点・接続の揺れ（例:「主なクラス, リソース」と「主なクラスとリソース」）
  - 処理方式の名称が design.md「5. 処理方式の名称」の正式名称と一致しているか
  - テスト種別の名称（クラス単体テスト / リクエスト単体テスト / 取引単体テスト）
- [ ] self-check（`checks/task-02.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #3 に進まない

**Completion criteria**:

- 用語集に、現行解説書とinput資料に登場する主要な用語が網羅されている
- 各用語の「揺れ表記」に file:line の根拠がある
- 処理方式の名称が design.md の正式名称と一致している
- FW解説書に存在する用語について、FW解説書と異なる表記を採用した場合、その理由が採用根拠に記載されている

---

### #3: トンマナ規約の作成

**Purpose**: FW解説書のライブラリの記述の調子を規約として明文化する。

**Prerequisites**: #2

**Steps**:

- [ ] `mapping/style.md` を作成する
- [ ] 抽出元は `ja/application_framework/application_framework/libraries/` 配下の `.rst`（複数ページから抽出すること）
- [ ] 各規約に規約ID（`S-01` 形式）、規約内容、根拠（file:line、**2件以上**）を付す
- [ ] 最低限、以下の観点を含める
  - 文体（だ・である調）
  - ページのセクション構成（機能概要 / モジュール一覧 / 使用方法 / 拡張例）
  - セクションタイトルの形式（「〜する」形式）
  - 見出しのアンダーライン記法とレベル対応
  - コードブロックのインデント幅と言語指定
  - アドモニション（`tip` / `note` / `important`）の使い分け基準
  - 表の記法（グリッド / シンプル / `list-table`）
  - `:ref:` ラベルの命名規則
  - 1文の長さ、改行位置の目安
  - 図の配置と説明文の関係
- [ ] **現行解説書のRSTを基準にしない。** 現行RSTは古く読みにくい可能性があるため、FW解説書のライブラリのみを基準とする
- [ ] self-check（`checks/task-03.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #4 に進まない

**Completion criteria**:

- 全規約に FW解説書ライブラリからの根拠 file:line が2件以上ある
- design.md の第2部・第3部のページアウトラインと矛盾がない

---

### #4: マッピングリストの作成

**Purpose**: 現行解説書とinput資料の全セクションを、design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。

**Prerequisites**: #3

**Steps**:

- [ ] `mapping/mapping.csv` を作成する。列は以下:

| 列名 | 内容 |
|---|---|
| `mapping_id` | 一意ID |
| `src_type` | `current`（現行解説書）/ `input`（input資料） |
| `src_file` | 出典ファイルパス |
| `src_line` | 出典行番号 |
| `heading_path` | 出典の見出しパス |
| `lines` | セクション配下の行数 |
| `audience` | `user`（利用者向け）/ `developer`（Nablarch開発者向け） |
| `dest_part` | 割当先の部（第1部 / 第2部 / 第3部） |
| `dest_page` | 割当先のページID |
| `dest_section` | 割当先のセクション名（design.md のアウトラインに存在するもの） |
| `disposition` | 扱い（下記5値） |
| `note` | 判断根拠 |

- [ ] `disposition` は以下の5値とする:
  - `MOVE` — そのまま新構成へ移す
  - `MERGE` — 他のセクションと統合する（統合先を `note` に記す）
  - `SPLIT` — 複数の割当先に分割する（行を複製し、それぞれに割当先を記す）
  - `REFERENCE` — 内容は他ページに置き、ここは `:ref:` 参照のみとする
  - `DROP` — 新構成に含めない（**理由を `note` に必ず記す**）
- [ ] `audience` を全行に付与する。`developer` と判定したものは `disposition=DROP` とし、`note` に理由を記す
  - `input/ntf-testdata-loading.md` は原則 `developer` だが、**セクション単位で判定する**。利用者向けの仕様が含まれる場合は `user` とし、解説書へ移す
- [ ] `dest_page` は design.md の章構成に存在するページのみを指定する。design.md にないページを勝手に作らない
- [ ] `dest_section` は design.md のページアウトライン（機能概要 / 使用方法 / 拡張例、およびその配下）に存在するセクションのみを指定する
- [ ] 現行の `03_Tips.rst`（目的別API使用方法）の各項目は、該当ページの「使用方法」セクションに `MERGE` する。独立ページにしない
- [ ] 現行の `08_TestTools` の各ツールは、design.md の割当先に従う
- [ ] **全セクションに `disposition` を付与する。空欄を残さない**
- [ ] `mapping/volume.md` を作成する
  - `dest_page` ごとに `lines` を集計し、ページ別の想定文量を表にする
  - 第2部の各ページ、および取引単体テストのページについて、分割の要否を判断できる形にする
- [ ] self-check（`checks/task-04.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #5 に進まない

**Completion criteria**:

- `sections-current.csv` / `sections-input.csv` の全 `section_id` が `mapping.csv` に最低1回現れる（**取りこぼしゼロ**）
- `disposition` が空欄の行が0件
- `audience` が空欄の行が0件
- `DROP` の全行に `note` が記入されている
- `dest_page` に design.md に存在しないページIDが含まれていない
- `dest_section` に design.md のアウトラインに存在しないセクション名が含まれていない
- `volume.md` にページ別文量の集計表がある

---

### #5: 未確定事項の確定と design.md 更新

**Purpose**: 文量集計に基づいて未確定事項を確定させる。

**Prerequisites**: #4

**Steps**:

- [ ] `volume.md` の集計をもとに、design.md「10. 未確定事項」の3件を確定する
- [ ] design.md を更新する。「未確定事項」の節は削除し、確定した構成を本文に反映する
- [ ] 確定に伴い `mapping.csv` の `dest_page` を更新する
- [ ] self-check（`checks/task-05.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #6 に進まない

**Completion criteria**:

- design.md に未確定事項が残っていない
- design.md の章構成と `mapping.csv` の `dest_page` の集合が一致する
- ファイル名に連番（`01_`, `02_` 等）が使われていない

---

### #6: 現行NTF解説書の削除

**Purpose**: 白紙の状態を作る。以降に増えるファイルはすべてマッピングに基づくものとなり、混入を構造的に防ぐ。

**Prerequisites**: #5

**Steps**:

- [ ] `ja/development_tools/testing_framework/` 配下の `.rst` を削除する
- [ ] `ja/development_tools/index.rst` の NTF への toctree 参照の現状を `checks/task-06.md` に記録する
- [ ] 削除前の全ファイル一覧（パスと行数）を `checks/task-06.md` に記録する
- [ ] 画像ファイル（`_image/`、`_images/`）およびダウンロード素材は削除しない。新構成で使用するため保持する
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #7 に進まない

**Completion criteria**:

- `ja/development_tools/testing_framework/` 配下に `.rst` が存在しない
- 削除前のファイル一覧が Evidence に記録されている
- 画像・ダウンロード素材が保持されている

**注記**: この時点でビルドは通らなくなる。#7 以降で解消する。

---

### #7〜: ページの作成（1ページにつき1タスク）

**Purpose**: マッピングに従ってページを1つ作成する。

**Prerequisites**: 直前のページタスク

ページの作成順は、第1部 → 第3部のテストデータ2ページ → 第2部 → 第3部の残り、とする。参照される側を先に作り、`:ref:` の参照先が存在する状態を保つため。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] 抽出した行の出典（`src_file:src_line`）を実際に読み、ページを作成する
- [ ] **マッピングにない内容を追加しない。マッピングにある内容を落とさない**
- [ ] **出典の文面をそのまま流用しない。** 内容は引き継ぐが、記述は `style.md` に従って書き直す
- [ ] 用語は `glossary.md` の正表記を使う
- [ ] セクション構成は design.md のページアウトラインに従う。セクションタイトルは「〜する」形式
- [ ] 4種類のレビューを、それぞれ**別のサブエージェント**で実施する（下記「レビュー観点」参照）
- [ ] 指摘への対応を行う。レビューは**最大3ラウンド**まで
- [ ] レビュー記録を `reviews/page-<ページID>.md` に作成する
- [ ] self-check（`checks/task-NN.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで次ページに進まない

**Completion criteria**:

- `mapping.csv` の当該 `dest_page` の全行が、作成したページに反映されている（`DROP` を除く）
- 4種類のレビューがすべて実施され、記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が当該ページについてエラーを出さない（未作成ページへの `:ref:` 警告は除く）

---

## レビュー観点

各ページについて、以下4つを**それぞれ別のサブエージェント**で実施する。1つのサブエージェントに複数観点を持たせない。

### 観点A: 網羅性

- `mapping.csv` の当該 `dest_page` の行が、すべてページに反映されているか
- `disposition` ごとの扱いが正しいか（`REFERENCE` が本文を持っていないか、`DROP` が混入していないか）
- 出典（`src_file:src_line`）の内容と照合し、記載が欠落していないか

**入力**: `mapping.csv` の該当行、作成したページ、出典ファイル

### 観点B: トンマナ

- `style.md` の全規約に適合しているか
- セクション構成が design.md のページアウトラインと一致しているか
- セクションタイトルが「〜する」形式になっているか
- **出典の文面がそのまま残っていないか**（古い言い回し、AI生成特有の不自然な表現）

**入力**: 作成したページ、`style.md`、design.md、FW解説書ライブラリの参照ページ

### 観点C: 用語

- `glossary.md` の正表記が使われているか
- 揺れ表記が混入していないか
- 処理方式の名称が正式名称と一致しているか

**入力**: 作成したページ、`glossary.md`

### 観点D: 整合性

- 他ページと内容が重複していないか
- `:ref:` の参照先が実在するか
- 参照が一方向で切れていないか（特に「テストデータの書き方」→「テストデータの記載例」のリンクは必須）
- 前提の矛盾がないか（例: Excel固定の記述がYAML対応後の文脈に残っていないか）
- 第2部に「使い方」が、第3部に「設定」が混入していないか

**入力**: 作成したページ、既に作成済みの全ページ、design.md

---

## レビュー記録

`reviews/page-<ページID>.md` に、以下の表形式で記録する。

| 列 | 内容 |
|---|---|
| 指摘ID | 一意（`<ページID>-001` 形式） |
| ラウンド | 1〜3 |
| 観点 | A（網羅性）/ B（トンマナ）/ C（用語）/ D（整合性） |
| 指摘内容 | サブエージェントの指摘 |
| 対応要否 | 要 / 不要 |
| 不要の理由 | 対応要否が「不要」の場合に必ず記入 |
| 対応内容 | 実際に行った修正 |

**ルール**:

- 指摘は対応の有無にかかわらず**全件記録する**。対応しないと判断したものも消さない
- 3ラウンドで解決しない指摘は、**未解決のまま記録して user review に上げる**。4ラウンド目を勝手に実施しない
- 指摘が0件だったラウンドもその旨を記録する

---

## 作業ルール

- **マッピングが唯一の基準。** マッピングにない内容を追加しない。マッピングにある内容を落とさない。判断に迷ったら user review に上げる
- **推測を書かない。** 出典を確認せずに内容を書かない。確認できない場合は user review に上げる
- **出典の文面を流用しない。** 現行RSTは古く、input資料はAI生成のため、いずれも読みにくい可能性がある。内容を理解したうえで `style.md` に従って書き直す
- **1ページずつ進む。** 複数ページをまとめて作成しない
- **user review の承認を受けるまで次タスクに着手しない**
- 指摘を受けた場合は当該タスク内で修正し、再度 push して再レビューを依頼する
- 各タスク完了時に `checks/` に Evidence を記録する
- CSVのレコード数は `csv.DictReader` でカウントする。`wc -l` は使わない
- commit and push every change

## 完了の定義

- `mapping.csv` の全行が処理済み（`DROP` を除き、すべて新構成のどこかに存在する）
- design.md の章構成にあるページがすべて作成されている
- 全ページについて4観点のレビューが実施され、記録されている
- 未解決の指摘が残っていない、または残す判断が user review で承認されている
- `make html` がエラー0で完了する
