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
├── design.md                  （既存。#6 で更新する）
├── input/                     （既存）
├── mapping/
│   ├── sections-current.csv   現行解説書のセクション一覧（#2 / #2a）
│   ├── sections-input.csv     input資料のセクション一覧（#2 / #2a）
│   ├── glossary.md            用語集（#3）
│   ├── style.md               トンマナ規約（#4）
│   ├── split-plan.md          大きいセクションの分割判断（#4a）
│   ├── mapping.csv            マッピングリスト（本作業の基準。#5）
│   ├── volume.md              ページ別文量集計（#5）
│   └── tools/
│       ├── extract_sections.py
│       ├── build_mapping.sh
│       ├── verify_coverage.py 抽出の取りこぼし検証（#2a）
│       └── verify_mapping.py  マッピングの取りこぼし検証（#5）
├── checks/
│   └── task-NN.md             タスクごとの Evidence
└── reviews/
    └── page-<ページID>.md      ページごとのレビュー記録
```

---

## タスク

### #1: 作業指示の受領とタスク詳細化

**Purpose**: 本作業指示書を受領し、達成条件とタスクを確定させる。

**Steps**:

- [ ] 本作業指示書を受け取る
- [ ] 達成条件を検証可能な形に具体化する
- [ ] タスクを分解して記録する
- [ ] commit & push

**Completion criteria**:

- 達成条件に具体的な検証可能な条件が記載されている
- タスクが分解・記載されている

---

### #2: セクション抽出ツールの作成

**Purpose**: 現行解説書とinput資料の記載内容を、セクション単位で機械的に抽出する。

**Steps**:

- [ ] `mapping/tools/extract_sections.py` を作成する
  - RST と Markdown の両方を扱う
  - 抽出単位は **L3相当のセクション**。RSTは見出しレベル3（ページタイトルをL1とする）、MarkdownはH3
  - L3配下にL4以下がある場合、それらはL3セクションに含める（別項目にしない）
  - **人の判断・要約を入れない。** 原文から機械的に取れる情報のみ
- [ ] `mapping/tools/build_mapping.sh` を作成する
  - 現行解説書は `git show <base>:<path>` で取得する（base は `git merge-base origin/develop HEAD`）
  - input資料は作業ツリーから取得する
  - 出力: `mapping/sections-current.csv`、`mapping/sections-input.csv`
- [ ] self-check（`checks/task-02.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #2a に進まない

**Completion criteria**:

- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）
- 抽出対象ファイル数が実ファイル数と一致することを Evidence に記載
- CSVのレコード数を **`csv.DictReader` でカウントした値** で Evidence に記載する（`wc -l` はフィールド内改行を多重カウントするため使わない）
- 抽出したセクション数が、実ファイルから独立に数えた見出し数と一致することを Evidence に記載

---

### #2a: セクション抽出の取りこぼし解消

**Purpose**: 見出し階層のどこにも属さない本文が発生しないよう抽出ルールを修正し、行の取りこぼしゼロを機械的に証明する。

**Prerequisites**: #2

抽出単位をL3のみとすると、L3を持たないページ全体と、L3配下に属さないL2/L1直下の本文が抽出対象外になる。

**Steps**:

- [ ] 抽出ルールを以下に改める
  - L3セクションを持つL2は、各L3をセクションとして抽出する（L4以下は畳み込む）
  - 同じL2の直下にありL3配下に属さない本文は、独立したセクションとして抽出する。`heading_path` は当該L2までとし、L3相当の位置に `(L2直下)` の印を付ける
  - L3セクションを持たないL2は、そのL2をセクションとして抽出する
  - L1直下にありL2配下に属さない本文も、同様に `(L1直下)` として独立セクションにする
  - 最初の見出しより前の本文は `(冒頭)` として独立セクションにする
- [ ] `lines` を「本文開始行から次のセクション開始行の直前まで」の全行数とする。末尾空行を除く処理を入れない
- [ ] カバー範囲をCSVに明示する。出力列を以下とする

```
section_id, src_file, src_line, body_start_line, body_end_line, heading_path, lines, code_blocks, tables, figures
```

  - `src_line` は**見出し行**を指す。本文はその後（RSTはアンダーラインを挟んで2行後、Markdownは1行後）から始まるため、カバー範囲を `src_line` から推測させない
- [ ] `mapping/tools/verify_coverage.py` を作成する
  - 各セクションの `[body_start_line, body_end_line]` を**行番号の集合**として構築する
  - 和集合を取り、全行集合との差集合を求める
  - 見出し行を除いて残った行を、**1行ずつ内容付きで列挙する**
  - `sum(lines) == len(covered)` を併せて確認し、範囲の重複を検出する
- [ ] `build_mapping.sh` から検証を実行する
- [ ] self-check（`checks/task-02a.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #3 に進まない

**Completion criteria**:

- `body_end_line - body_start_line + 1 == lines` が全セクションで成立する
- セクションのカバー範囲の和集合と全行集合の差が、見出し行を除いて非空行0件である
- 見出し行以外に未カバー行が残る場合、その行と理由が Evidence に全件列挙されている
- 抽出対象ファイル数が実ファイル数と一致し、セクション0件のファイルが存在しない
- 2回実行して同一のCSVが生成される（md5一致）

---

### #3: 用語集の作成

**Purpose**: 全ページで統一する用語を確定する。現行解説書とinput資料で用語が揺れているため、先に基準を作る。

**Prerequisites**: #2a

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
- [ ] self-check（`checks/task-03.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #4 に進まない

**Completion criteria**:

- 用語集に、現行解説書とinput資料に登場する主要な用語が網羅されている
- 各用語の「揺れ表記」に file:line の根拠がある
- 処理方式の名称が design.md の正式名称と一致している
- FW解説書に存在する用語について、FW解説書と異なる表記を採用した場合、その理由が採用根拠に記載されている

---

### #4: トンマナ規約の作成

**Purpose**: FW解説書のライブラリの記述の調子を規約として明文化する。

**Prerequisites**: #3

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
- [ ] self-check（`checks/task-04.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #4a に進まない

**Completion criteria**:

- 全規約に FW解説書ライブラリからの根拠 file:line が2件以上ある
- design.md の第2部・第3部のページアウトラインと矛盾がない

---

### #4a: 大きいセクションの分割判断

**Purpose**: マッピング作成の前に、複数の割当先に分かれるセクションを特定し、分割位置を確定する。マッピング作成を機械的な作業にするため。

**Prerequisites**: #4

#2a の完了により、セクション抽出の実態が判明した。

| 項目 | current | input |
|---|---|---|
| セクション数 | 377 | 202 |
| 行数（body） | 9,783 | 3,203 |
| 中央値 | 12行 | 12行 |
| 100行超のセクション | 23件（全体の36%の行を占める） | 0件 |
| 200行超のセクション | 6件（15%） | 0件 |
| 最大 | 314行 | 63行 |

input側は最大63行のため、1セクションが複数の割当先に分かれる可能性は低い。**current側の大きいセクションのみが問題となる。**

抽出粒度は変更しない。L4まで細分化すると全セクション数が倍増し、分割が必要な23セクションのために全体の判断コストを上げることになるため。

**対象**: `sections-current.csv` のうち `lines >= 100` のセクション（23件）

**Steps**:

- [ ] `mapping/split-plan.md` を作成する
- [ ] 対象23セクションについて、それぞれ以下を判断する
  - 内容を実際に読み、design.md の章構成のどの割当先に属するかを検討する
  - **単一の割当先に収まるか、複数に分かれるかを判定する**
  - 複数に分かれる場合、**分割位置を行番号で特定する**
- [ ] 以下の表形式で記録する

| 列 | 内容 |
|---|---|
| `section_id` | 対象セクションID |
| `heading_path` | 見出しパス |
| `lines` | 行数 |
| `split` | `no`（分割しない）/ `yes`（分割する） |
| `parts` | 分割する場合、`開始行-終了行 → 割当先` を1行1件で列挙 |
| `rationale` | 判断根拠。なぜその位置で分けるのか、なぜ分けないのか |

- [ ] **分割しない判断も根拠を記す。** 「一体として意味を持つため」等、内容に基づく理由を書く。行数が少ないから、では不可
- [ ] 分割する場合、**分割後の行範囲が元のセクション範囲を過不足なく覆うこと**。隙間や重複を作らない
- [ ] self-check（`checks/task-04a.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #5 に進まない

**Completion criteria**:

- 対象23セクションすべてに `split` の判定と `rationale` がある
- `split=yes` の全件について、`parts` の行範囲の和集合が元のセクションの `body_start_line`〜`body_end_line` と一致する（隙間・重複ゼロ）
- `parts` の割当先が design.md の章構成に存在するページ・セクションである

**注記**: `lines < 100` のセクションでも分割が必要と判明した場合は、#5 の中で対応してよい。その場合は `split-plan.md` に追記し、`rationale` を残すこと。

---

### #5: マッピングリストの作成

**Purpose**: 現行解説書とinput資料の全セクションを、design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。

**Prerequisites**: #4a

**Steps**:

- [ ] `mapping/mapping.csv` を作成する。列は以下:

| 列名 | 内容 |
|---|---|
| `mapping_id` | 一意ID |
| `src_section_id` | 出典セクションID（`sections-*.csv` の `section_id`） |
| `src_type` | `current`（現行解説書）/ `input`（input資料） |
| `src_file` | 出典ファイルパス |
| `src_body_start` | このマッピング行が担当する範囲の開始行 |
| `src_body_end` | 同 終了行 |
| `heading_path` | 出典の見出しパス |
| `lines` | 担当範囲の行数（`src_body_end - src_body_start + 1`） |
| `audience` | `user`（利用者向け）/ `developer`（Nablarch開発者向け） |
| `dest_part` | 割当先の部（第1部 / 第2部 / 第3部） |
| `dest_page` | 割当先のページID |
| `dest_section` | 割当先のセクション名（design.md のアウトラインに存在するもの） |
| `disposition` | 扱い（下記5値） |
| `note` | 判断根拠 |

- [ ] `src_body_start` / `src_body_end` は以下のとおり入れる
  - `disposition` が `SPLIT` 以外 — セクションの `body_start_line` / `body_end_line` をそのまま入れる
  - `disposition` が `SPLIT` — `split-plan.md` の `parts` に従い、分割後の行範囲を入れる。行を複製し、各行に異なる範囲と割当先を記す
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
  - **`DROP` を除いた `lines` 合計を記載する。** これが新構成に移る実質的な分量になる
  - `DROP` の合計行数と、その内訳（`note` の理由別）も記載する
- [ ] self-check（`checks/task-05.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #6 に進まない

#### サブエージェントによる分担

579セクションを1つのコンテキストで処理すると、後半で判断がぶれる。**出典ファイル単位でサブエージェントに分担させる。**

- current 47ファイル、input 10ファイル。1エージェントあたり10〜20セクション程度になるよう分割する
- 各サブエージェントには以下を入力として渡す
  - 担当ファイルのセクション一覧（`sections-*.csv` の該当行）
  - 担当ファイルの実内容
  - `design.md`
  - `mapping/glossary.md`
  - `mapping/split-plan.md`（担当ファイルに100行超セクションが含まれる場合）
- 各サブエージェントの出力を統合して `mapping.csv` を作る
- **統合時に `mapping_id` の重複と、割当先の表記揺れを機械的に検査する**

**Completion criteria**:

**取りこぼしゼロの検証を、行範囲の集合演算で行う。**

- **`mapping.csv` には `DROP` 行も含めて全セクションを残す。** 削除せずに残すことで、何をなぜ落としたかが追跡できる
- `sections-current.csv` / `sections-input.csv` の全 `section_id` が `mapping.csv` の `src_section_id` に最低1回現れる
- 各 `src_section_id` について、紐づく全マッピング行の行範囲 `[src_body_start, src_body_end]` の和集合が、元のセクションの `[body_start_line, body_end_line]` と一致する（隙間・重複ゼロ）
- `mapping.csv` の `lines` 合計が、`sections-current.csv` と `sections-input.csv` の `lines` 合計（9,783 + 3,203 = 12,986）と一致する（**取りこぼしゼロの確認**）
- **`DROP` を除いた `lines` 合計が `volume.md` に記載されている**（**新構成に移る実質的な分量**）
- **`verify_mapping.py` が上記2つの数値を両方出力する**
- `disposition` が空欄の行が0件
- `audience` が空欄の行が0件
- `DROP` の全行に `note` が記入されている
- `dest_page` に design.md に存在しないページIDが含まれていない
- `dest_section` に design.md のアウトラインに存在しないセクション名が含まれていない
- `volume.md` にページ別文量の集計表がある

**検証はスクリプトで行い、`mapping/tools/verify_mapping.py` としてコミットする。** 手作業で確認しない。

`lines` 合計 12,986 の一致は、`DROP` 行を残す限り必ず成立する。これは**取りこぼしがないこと**の確認であって、**全量が新構成に移ったこと**の証明ではない。両者を混同しないよう、`verify_mapping.py` は必ず次の2つを並べて出力する。

- `lines` 合計（全行）— 12,986 と一致すること
- `lines` 合計（`DROP` を除く）— 新構成に移る実質的な分量

`DROP` 分の行数が可視化されていれば、想定外に多い場合に気づける。

---

### #6: 未確定事項の確定と design.md 更新

**Purpose**: 文量集計に基づいて未確定事項を確定させる。

**Prerequisites**: #5

**Steps**:

- [ ] `volume.md` の集計をもとに、design.md「10. 未確定事項」の3件を確定する
- [ ] design.md を更新する。「未確定事項」の節は削除し、確定した構成を本文に反映する
- [ ] 確定に伴い `mapping.csv` の `dest_page` を更新する
- [ ] self-check（`checks/task-06.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #7 に進まない

**Completion criteria**:

- design.md に未確定事項が残っていない
- design.md の章構成と `mapping.csv` の `dest_page` の集合が一致する
- ファイル名に連番（`01_`, `02_` 等）が使われていない

---

### #7: 現行NTF解説書の削除

**Purpose**: 白紙の状態を作る。以降に増えるファイルはすべてマッピングに基づくものとなり、混入を構造的に防ぐ。

**Prerequisites**: #6

**Steps**:

- [ ] `ja/development_tools/testing_framework/` 配下の `.rst` を削除する
- [ ] `ja/development_tools/index.rst` の NTF への toctree 参照の現状を `checks/task-07.md` に記録する
- [ ] 削除前の全ファイル一覧（パスと行数）を `checks/task-07.md` に記録する
- [ ] 画像ファイル（`_image/`、`_images/`）およびダウンロード素材は削除しない。新構成で使用するため保持する
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで #8 に進まない

**Completion criteria**:

- `ja/development_tools/testing_framework/` 配下に `.rst` が存在しない
- 削除前のファイル一覧が Evidence に記録されている
- 画像・ダウンロード素材が保持されている

**注記**: この時点でビルドは通らなくなる。#8 以降で解消する。

---

### #8〜: ページの作成（1ページにつき1タスク）

**Purpose**: マッピングに従ってページを1つ作成する。

**Prerequisites**: 直前のページタスク

ページの作成順は、第1部 → 第3部のテストデータ2ページ → 第2部 → 第3部の残り、とする。参照される側を先に作り、`:ref:` の参照先が存在する状態を保つため。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
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
- 出典（`src_file` の `src_body_start`〜`src_body_end`）の内容と照合し、記載が欠落していないか

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
