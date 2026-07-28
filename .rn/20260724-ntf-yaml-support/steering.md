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
- `#5b`/`#5c`/`#5d` 作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-05b-instruction.md`
- `#5c` 追補（STEP 0）: `.rn/20260724-ntf-yaml-support/ntf-doc-05c-addendum.md`
- `#5d` 追補（STEP 6〜8）: `.rn/20260724-ntf-yaml-support/ntf-doc-05d-addendum.md`
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

**#3 差し戻し（ラウンド1〜3のレビューで収束しなかったため、母集合を定義して再構成する）**:

ラウンド1〜3のレビュー指摘（G-1, G-2, G-5, G-9, G-10）はいずれも「用語集に対象とする用語の母集合が定義されていない」ことが原因。母集合がないためレビューのたびに探し方が変わり、指摘が収束しなかった。母集合を機械抽出し、レビューを「母集合に対する未判定ゼロ」の機械検証に置き換える。

- [x] `mapping/tools/extract_terms.py` を作成する。以下から用語候補を機械的に列挙する
  - 現行解説書の全見出し（`sections-current.csv` の `heading_path` を分解）
  - `input/ntf-doc-terms.md` の全見出し（H1を除く全見出し。H2/H3/H4）
  - `design.md` に登場する章・セクション名および処理方式名
- [x] `mapping/term-candidates.csv` を出力する（列: `term, source, occurrences, file_line`）
- [x] `glossary.md` の各項目を `term-candidates.csv` のどの候補に対応するか記録する
- [x] 不採用の理由を記録する欄を `glossary.md` に設ける（「一般語のため」「1箇所のみの出現で用語ではないため」等、候補ごとに具体的な理由を記す）
- [x] `verify_glossary.py` を母集合との突合に変更する。以下を機械判定すること
  - `term-candidates.csv` の全候補が `glossary.md` に「採用」または「不採用（理由付き）」のいずれかで現れる
  - 未判定の候補が0件であること
  - `design.md` の章・セクション名がすべて `glossary.md` に存在すること
  - 処理方式名が `design.md` の正式名称と一致すること
- [x] 個別の誤りを修正する（母集合とは別の、根拠を実測せずに書いたことによる記述ミス）
  - G-4: 採用根拠の引用行が主張を裏付けていない
  - G-6: 件数の誤り
  - G-7: 150字超の表セル41個
  - G-8: 分類の誤り
  - 全項目の根拠 file:line を機械的に再検証する
- [x] self-check（`checks/task-03.md`）を更新する
- [x] commit & push
- [ ] 4観点のレビュー（**ラウンドを1から数え直す** — 母集合突合を基準とした新しい検証のため、ラウンド1〜3の指摘履歴はこの再構成で解消される）— **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
- [ ] **user review** — 承認を受けるまで #4 に進まない

**母集合ラウンド1レビュー（対象 `5276d1e`）の指摘を受けた対応 — 用語集の役割を最小化する方針転換**:

QA/設計/クラフト/検証の4観点とも NG。トリアージの詳細は `checks/task-03.md`「母集合ラウンド1の指摘トリアージ」を参照。

ユーザー判断: `#5`（マッピング）が全量保証の唯一の根拠であり #8 以降の全ページの基準になる。用語集は表記の問題にすぎず、マッピングは内容が失われるかどうかの問題であるため、用語集は最小限で切り上げ、力を `#5` に配分する。**全候補の本文出現を数え直す再監査の指示は取り下げ、実施しない。**

用語集の役割を「ページ作成時に表記を揃えるための参照物」に限定し、網羅性の証明は求めない。表記の一貫性は #8 以降のページ作成時、観点C（用語）のレビューで担保する。

- [x] 掲載基準（§3）を次の2種類に限定するよう書き換える
  - 表記揺れが実在し正表記を確定した用語（複数の表記が現行解説書・input資料に存在するもの）
  - `design.md` が章・セクション名として使う用語（処理方式の正式名称7件、テスト種別3件、ページアウトラインのセクション名）
- [x] 上記2種類に該当しない候補は `term-candidates.csv` に残したまま、§5.15 を一括で「今回は判定しない」という記録に置き換える。候補ごとの個別理由は不要
- [x] `verify_glossary.py` の母集合突合系の検査（`population`/`reasons` 等）を、この新しい掲載基準（「採用」「不採用（理由付き）」「一括：今回は判定しない」の3値のいずれかに全候補が対応していること）に合わせて更新する
- [x] §5.4/§5.5 ほか、揺れ表記の代表file:line根拠が皆無の行（10行・27箇所）に代表1件のfile:lineを補充する（指摘3・対応する）
- [x] `エンティティバリデーション`・`Excel形式`の「意味」欄にある旧表記（`バッチ処理`・`ブック`）を正表記に統一する（指摘4・対応する）
- [x] self-check（`checks/task-03.md`）を更新する
- [x] commit & push
- [x] **user review** — 承認済み（ユーザーが #4 のスコープ定義に進んだことを承認とみなす。異なる場合は指摘してください）

指摘1（代理指標の誤り）・指摘2（紋切り型の不採用理由）は対応不要（網羅性を求めず一括記録に変更するため）。

**Completion criteria**:

- 用語集の役割は「ページ作成時に表記を揃えるための参照物」であり、網羅性の証明は求めない
- 掲載する用語は次の2種類に限定する
  - 表記揺れが実在し正表記を確定した用語（複数の表記が現行解説書・input資料に存在するもの）
  - `design.md` が章・セクション名として使う用語（処理方式の正式名称7件、テスト種別3件、ページアウトラインのセクション名）
- 上記に該当しない候補は `term-candidates.csv` に残したまま一括で「今回は判定しない」と記録している（候補ごとの理由は不要）
- 掲載した用語の揺れ表記に file:line の根拠がある
- 「意味」欄に、用語集自身が定める旧表記（`バッチ処理`・`ブック` 等）が無変換で残っていない
- 処理方式の名称が design.md の正式名称と一致している
- FW解説書と異なる表記を採用した場合、理由が採用根拠に記載されている

### #4: トンマナ規約の作成

**Purpose**: `style.md` は「ページ作成時にCCが従う基準」である。FW解説書ライブラリの記述の調子を写し取れば足り、網羅性を追求する対象ではない（ユーザー判断。`#5`（マッピング）に力を配分するため、#3 に続き #4 もスコープを絞る）。

**Prerequisites**: #3

**Steps**:

- [x] `mapping/style.md` を作成する
- [x] 抽出元は `ja/application_framework/application_framework/libraries/` 配下の `.rst`（複数ページから抽出）。**現行解説書のRSTを基準にしない**
- [x] 各規約に規約ID（`S-01` 形式）、規約内容、根拠（file:line、**2件以上**）を付す
- [x] 観点は次の8つに限定する。機械判定できるか、ページ作成時に確実に効くもののみ
  1. 文体（だ・である調）
  2. ページのセクション構成（機能概要 / モジュール一覧 / 使用方法 / 拡張例）
  3. セクションタイトルの形式（「〜する」形式）
  4. 見出しのアンダーライン記法とレベル対応
  5. コードブロックのインデント幅と言語指定
  6. アドモニション（tip / note / important）の使い分け基準
  7. 表の記法
  8. `:ref:` ラベルの命名規則
- [x] **観点を追加しない**。抽出中に他の規則性に気づいても `style.md` には載せない（1文の長さ・改行位置、図の配置は当初案にあったが対象外とする。判断が要り機械判定できず、ページ作成時のレビューでも指摘が主観的になるため）
- [x] self-check（`checks/task-04.md`）
- [x] commit & push
- [x] **user review** — 承認済み

**Completion criteria**:

- 上記8観点すべてに規約と根拠（FW解説書ライブラリの file:line、各2件以上）がある
- design.md の第2部・第3部のページアウトラインと矛盾がない
- 観点が8つ以外に増えていない

**未決事項（#4のスコープ外。今回は解決しない）**: `glossary.md` §6・§11.2 が「#4 で決めること」として申し送っていた3項目（括弧の全角・半角、英数字と日本語の間の空白、送り仮名・漢字/かなの揺れ）は、上記8観点のいずれにも該当しないため、今回の `style.md` では扱わない。実測データは `glossary.md` §6 に残っている。#8以降のページ作成で実際にこれらの表記が必要になった場合は、その都度、当該箇所のFW解説書ライブラリの多数派表記に合わせて個別に判断する（`style.md` に規約として立てるのではなく、都度の実装判断とする）。

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

- [x] `mapping/split-plan.md` を作成する
- [x] 対象23セクションについて、内容を実際に読み、design.md のどの割当先に属するかを検討する
- [x] 単一の割当先に収まるか、複数に分かれるかを判定する
- [x] 複数に分かれる場合、分割位置を行番号で特定する
- [x] 表形式で記録する（列: `section_id, heading_path, lines, split, parts, rationale`）
  - `split` は `no` / `yes`
  - `parts` は `開始行-終了行 → 割当先` を1行1件で列挙
- [x] **分割しない判断も `rationale` を記す。** 内容に基づく理由を書く。行数が少ないから、では不可
- [x] 分割する場合、分割後の行範囲が元のセクション範囲を過不足なく覆うこと
- [x] self-check（`checks/task-04a.md`）
- [x] 2観点のレビューを、それぞれ**別のサブエージェント**で実施する。QA/クラフト/検証は行範囲の隙間・重複ゼロの機械検証で代替するため実施しない
  - **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**。各サブエージェントに対象セクションの実内容と `design.md` を渡し、`split-plan.md` の判断が妥当かを検証させる
  - 割当先の妥当性: `design.md` の章構成に照らして、その割当先が正しいか。第2部（設定）と第3部（使い方）の切り分けが適切か
  - 分割位置の妥当性: 分割する場合、その位置で内容が切れるか。分割しない場合、本当に一体として意味を持つか
  - ラウンド1でNG3件ずつ（current-0037の境界／current-0156・0184・0185の宛先）を検出、修正（`ac533b5`）後の再レビューで4行ともOK
- [x] commit & push
- [x] **user review** — 承認済み

**Completion criteria**:

- 対象23セクションすべてに `split` の判定と `rationale` がある
- `split=yes` の全件について、`parts` の行範囲の和集合が元のセクションの `body_start_line`〜`body_end_line` と一致する（隙間・重複ゼロ）
- `parts` の割当先が design.md の章構成に存在するページ・セクションである

**注記**: `lines < 100` のセクションでも分割が必要と判明した場合は #5 の中で対応してよい。その場合は `split-plan.md` に追記し `rationale` を残す。

### #5: マッピングリストの作成

**Purpose**: 現行解説書とinput資料の全セクションを design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。

**Prerequisites**: #4a

**Steps**:

- [x] `mapping/mapping.csv` を作成する（列: `mapping_id, src_section_id, src_type, src_file, src_body_start, src_body_end, heading_path, lines, audience, dest_part, dest_page, dest_section, disposition, note`）
  - `src_section_id` は `sections-current.csv` / `sections-input.csv` の `section_id` を指す
  - `lines` は `src_body_end - src_body_start + 1`
  - `disposition` が `SPLIT` 以外 — セクションの `body_start_line` / `body_end_line` をそのまま入れる
  - `disposition` が `SPLIT` — `split-plan.md` の `parts` に従い分割後の行範囲を入れる。行を複製し、各行に異なる範囲と割当先を記す
- [x] 出典ファイル単位でサブエージェントに分担させる（579セクションを1コンテキストで処理すると後半で判断がぶれるため）
  - 1エージェントあたり10〜20セクション程度
  - 入力: 担当ファイルのセクション一覧 / 担当ファイルの実内容 / `design.md` / `glossary.md` / `split-plan.md`（100行超セクションを含む場合）
  - 出力を統合し、`mapping_id` の重複と割当先の表記揺れを機械的に検査する
- [x] `disposition` は5値（`MOVE` / `MERGE` / `SPLIT` / `REFERENCE` / `DROP`）
- [x] 全行に `audience`（`user` / `developer`）を付与。`developer` は `disposition=DROP` とし `note` に理由を記す
  - `input/ntf-testdata-loading.md` は原則 `developer` だがセクション単位で判定する
- [x] 現行の `03_Tips.rst` の各項目は該当ページの「使用方法」に `MERGE` する。独立ページにしない
- [x] **design.md に確定した割当先ページが存在しないセクションは、`dest_page` を空欄にせず暫定値を置く。**（#4a `current-0158` — `split-plan.md` で「割当先ページは未確定」とされた行が該当。design.md 第2部に「取引単体テストの設定」ページが未定義で、#6 の未確定事項#1（第2部のページ分割）に依存するため）
  - 暫定の `dest_page` は `mapping/vocabulary.md` の暫定語彙（処理方式付きの仮ページ名）を用いる。由来（どの処理方式・どのカテゴリの内容か）を `dest_page` の値自体に保持させ、`note` だけに頼らない（2026-07-27 ユーザー判断: 該当見込みが40件超あり、`note` の文言だけでは #6 での再分離に全行の読み直しが必要になり非現実的なため）
  - `current-0158` は「第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング）」を暫定値とする（旧: 「リクエスト単体テストの設定」は由来を失うため撤回）。`note` は「暫定。」で始める。`current-0158` の `note` は次の文言とする: 「暫定。取引単体テスト向けの設定だが、design.md 第2部に「取引単体テストの設定」ページが未定義のため。#6 で第2部のページ分割が確定した時点で見直す。」
  - `#5` の作業中に同様のケース（design.md に適切な割当先がないセクション）が他に見つかった場合も同じ扱いとする
  - 暫定扱いとしたセクションを `checks/task-05.md` に一覧化する
- [x] `heading_path` が `(L2直下)`（親L2見出し直下の導入文で子L3を持たない）で終わる行は、同じ親を持つ配下セクションと同じ `dest_section` に置く（親子でセクションが分かれページ内で内容が分断されるのを防ぐ。2026-07-27 batch-01差し戻し指摘②。`checks/task-05.md`「batch-01 差し戻し」参照）
- [x] `mapping/tools/verify_mapping.py` を作成する（batch-02〜15差し戻し対応の一環、2026-07-28）
  - 現状は `mapping.csv` 未作成のため `mapping/_batch/batch-*.csv` 全件を対象に検証（`mapping.csv` 作成後は自動でそちらを対象にする）
  - `lines` 合計（全行）と `lines` 合計（`DROP` を除く）を出力する
  - disposition=DROPかつnoteに「重複」を含む行は、noteにcurrent-XXXX/input-XXXX形式の重複先が記載されていることを検証する（2026-07-28 user差し戻し指摘②により追加）
  - disposition/audience空欄0件、DROP行のnote必須も検証する
  - `mapping.csv`統合後（2026-07-28）に`check_coverage`（取りこぼし検証、行範囲の集合演算）と`check_vocabulary`（`dest_page`等のvocabulary.md突合）を追加。全591行でエラー0件
- [x] `mapping/volume.md` を作成する（`dest_page` ごとに `lines` を集計）
  - `DROP` を除いた `lines` 合計を記載する（新構成に移る実質的な分量）
  - `DROP` の合計行数と、その内訳（`note` の理由別）も記載する
- [x] self-check（`checks/task-05.md`）
- [x] 3観点のレビューを、それぞれ**別のサブエージェント**で実施する。取りこぼしゼロは `verify_mapping.py` の機械検証で担保するため、レビューは判断の妥当性のみに集中させる
  - **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
  - 割当先の妥当性: `dest_page` / `dest_section` が `design.md` に照らして正しいか。第2部と第3部の切り分けが適切か
  - dispositionの妥当性: `MOVE` / `MERGE` / `SPLIT` / `REFERENCE` / `DROP` の判定が内容に合っているか。特に `DROP` と `REFERENCE` を精査する
  - audienceの妥当性: `user` / `developer` の判定が正しいか。`developer` と判定して落としたものに利用者向けの内容が含まれていないか
- [x] commit & push
- [x] **user review** — 承認済み（`/rn:dn` 呼び出しにあわせユーザーが「#5はOK」と明示）

**2026-07-28 ユーザー差し戻し対応（2回）**: (1) DROP見直し13件の実測再検証（12件維持・current-0293は取消指示自体を覆しDROP維持で確定）と、design.md第4部「ツール」新設に伴うdest_part付け替え44行・vocabulary.md更新・extract_vocabulary.py追随・design.md章番号参照の修正（詳細: `checks/task-05.md`「ユーザー差し戻し対応」節）。(2) 独立検証で見つかった`verify_mapping.py`のvocabulary突合バグ（`dest_part`を無視した`dest_section`単独照合。第2部/第3部の`拡張例`が第4部の行にも誤って一致）を修正し、`current-0374`の不一致を検出→`使用方法`へ変更（詳細: `checks/task-05.md`「第4部対応への再差し戻し」節）。

**「導入」0件の指摘対応（2026-07-28、解決済み）**: `batch-22`（`SetUpHttpDumpTool.rst`由来8行）・`batch-23`（`ConfigMasterDataSetupTool.rst`由来7行、計15行・201行分）を実ファイル通読で1件ずつ再判定し、14行を`機能概要`/`使用方法`から`導入`へ変更（1行は使用方法からの`:ref:`参照先であることを実ファイル突合で確認し使用方法のまま維持）。`_batch/batch-22.csv`・`batch-23.csv`を修正して`mapping.csv`を再統合し、`verify_mapping.py`で591行・エラー0件を確認済み。詳細・判断根拠は `checks/task-05.md`「『導入』0件の指摘対応」節を参照。

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

### #5b: 割当先0件問題の解消

**Purpose**: 「語彙が定義しているのに割当が0件」を機械検出できる状態にし、再判定で解消できるものを解消し、`#6` のユーザー判断が必要なものを調査報告として残す。詳細な仕様は `.rn/20260724-ntf-yaml-support/ntf-doc-05b-instruction.md` を参照。

**Prerequisites**: #5

**Steps**:

- [x] STEP 1: `mapping/tools/verify_mapping.py` に `check_unused_vocabulary`（`EXPECTED_ZERO`/`PENDING_ZERO`/ERROR の3分類）を追加し、RED（ERROR で `exit 1`）を確認して commit する
- [x] STEP 2: `機能概要`/`導入`/`拡張例` 0件の16ページを実ファイル通読で再判定し、`_batch/*.csv` を修正、`mapping.csv` を全30バッチ連結で再生成する
- [x] STEP 3: `volume.md` に0行ページと `dest_section` 単位の集計表を追加する
- [x] STEP 4: 未解決の0件（第1部「稼動環境」／第2部「テストデータの形式」／第2部 取引単体テストの設定2ページ）を調査報告として `checks/task-05b.md` にまとめ、`PENDING_ZERO` に登録する（`design.md` は変更しない）
- [x] STEP 5: self-check（`checks/task-05b.md`）、`steering.md` 更新（本タスク追記・#6 Prerequisites 更新）、commit & push
- [x] **user review** — 承認済み（`ca1e9cf` に対する独立検証。指摘2点は `#5b` を再オープンせず `#5d` の追加STEPとして反映。詳細: `.rn/20260724-ntf-yaml-support/ntf-doc-05d-addendum.md`）

**Completion criteria**:

- `verify_mapping.py` に `check_unused_vocabulary` が実装され、コミットされている
- `EXPECTED_ZERO` の全エントリに `design.md` の該当箇所の引用が理由として付いている
- `PENDING_ZERO` の全エントリに `#6` のどの未確定事項に対応するかが書かれている
- `check_unused_vocabulary` の ERROR が0件（残りは `EXPECTED_ZERO` か `PENDING_ZERO` に分類済み）
- `lines` 合計 12,986 / DROP除く 11,973 / 591行 が不変
- `checks/task-05b.md` に、`dest_section` を変更した行と変更しなかった行の両方が根拠付きで列挙されている
- `volume.md` に0行ページと `dest_section` 単位の集計が載っている
- `design.md` が変更されていない（`git diff` で確認）

### #5c: `DROP` 全件レビュー

**Purpose**: `design.md` §11.8「`DROP` は件数の多寡にかかわらず全件を対象とする」の未達分を解消する。詳細は `.rn/20260724-ntf-yaml-support/ntf-doc-05b-instruction.md` を参照。`#5c` の先頭に追加した STEP 0 の詳細は `.rn/20260724-ntf-yaml-support/ntf-doc-05c-addendum.md` を参照。

**Prerequisites**: #5b

**Steps**:

- [x] STEP 0: `verify_mapping.py` の `check_unused_vocabulary` に許可リストの陳腐化検出（`stale allowlist` ERROR）を追加し、ERROR 0件・`EXIT: 0` を確認して commit する（`checks/task-05c.md` 参照）
- [x] `mapping.csv` の `disposition=DROP` 全96行を抽出し、`checks/task-05.md` の既存レビュー記録とレビュー済み/未レビューを機械的に分類する
- [x] 未レビュー分を実ファイル通読で判定する（理由の妥当性／重複DROPの実ファイル確認／開発者向けDROPの該当性／空・TOC・アンカーの実態）
- [x] 全96行の判定結果を `checks/task-05c.md` に1つの表としてまとめる
- [x] 判定が覆った行があれば `_batch/*.csv` を修正し `mapping.csv` を再生成する（初回レビュー時点は0件のため修正なし。差し戻し対応で2件発生、下記参照）
- [x] commit & push
- [ ] **user review** — 承認を受けるまで #5d に進まない（**サブエージェントによるレビューは実施しない**）

**`#5c` 差し戻し対応（`ntf-doc-05c-rework.md`、2026-07-28、コミット `109b736`）**:

初回レビューの分類基準（`checks/task-05.md` に文字列出現するか）は記録が「判定確定」か
「判定保留」かを区別せず、保留のまま閉じられていた `input-0178`・`input-0198` の2行が
根拠なく「レビュー済み・DROP維持」に分類されていた。

- [x] 分類基準に「記録が当該行自身の判定を確定しているか」を追加し96行を再分類（真の保留は2件と確認）
- [x] `input-0178`: 実装確認（`nablarch/nablarch-testing` commit `e21bf67`、`TestDataParser.java:21` の `@Published(tag="architect")`）と現行解説書の先例（`current-0233`/`current-0234`）により `DROP→MERGE`・`audience developer→user`
- [x] `input-0198`: `input-0194` を実測し元noteの誤りを確認、`YamlTestDataValidator` の1文のみ3分割で抽出し `DROP→MERGE`、残り2区間はDROP維持。`split-plan.md` に追記
- [x] `_batch/batch-02.csv`・`_batch/batch-18.csv` を修正し `mapping.csv` を全30バッチ連結で再生成（591→593行、`lines`合計12,986は不変）
- [x] `verify_mapping.py` 再実行（`stale allowlist` 含めエラー0件・`EXIT: 0`）、`volume.md` を実測値に更新
- [x] `checks/task-05c.md` に実測根拠を追記、commit & push（`109b736`）
- [x] **user review** — 承認済み（独立検証APPROVE相当、`/rn:ty` で承認）

**Completion criteria**:

- `DROP` 96行すべてが `checks/task-05c.md` の表に現れる
- 各行に「レビュー済み（記録の所在）」または「今回レビュー（判定と根拠 file:line）」のいずれかがある
- 判定が覆った行は `_batch/*.csv` を修正し、`verify_mapping.py` がエラー0件
- `lines` 合計 12,986 が不変
- `check_unused_vocabulary` に許可リストの陳腐化検出が実装され、コミットされている
- `DROP` 判定を覆した行がある場合、`stale allowlist` の ERROR が0件になるまで
  許可リスト（`EXPECTED_ZERO_*` / `PENDING_ZERO`）・`mapping/volume.md`・
  `checks/task-05b.md` を更新済みであること

**`#5c`（差し戻し対応後）の追加 Completion criteria**:

- 分類基準が「記録に当該行自身の保留表現が含まれる場合はレビュー済みとしない」を含む
- `input-0178`・`input-0198` を含む全96行に、保留ではない確定した判定がある
- `input-0198` の `note` から、実測で否定された理由（「input-0194で既にカバー」）が除かれている
- `DROP` 解除があった場合、`volume.md`・許可リスト・`checks/task-05b.md` が更新され
  `stale allowlist` の ERROR が0件

### #5d: 記録の整合とセクション境界の是正

**Purpose**: `#5` までの成果物に残った記録上の不整合を解消し、あわせて `#5b` のレビューで
検出したセクション境界の欠陥を、機械検査の追加と既存ルールに基づく是正で解消する。
既存の割当判断（dest_page / disposition / audience）は変更しない。詳細は `.rn/20260724-ntf-yaml-support/ntf-doc-05b-instruction.md` および `.rn/20260724-ntf-yaml-support/ntf-doc-05d-addendum.md` を参照。

**Prerequisites**: #5c

**Steps**:

- [x] `split-plan.md` に `input-0016`/`input-0030` を表形式で追記し、冒頭の対象定義に2件追加した旨を記す
- [x] `checks/task-05.md` に「暫定扱い一覧」節を新設し、`note` が「暫定」で始まる27行全件を表にする
- [x] `HTMLチェックツール` 8行（`current-0367`〜`current-0375`）について、第4部新設で受け皿問題が解消済みであり `#6` では文言更新のみで済む旨を暫定一覧に明記する
- [x] `design.md` §12 未確定事項#3（ファイル名・ディレクトリ構成）の確定時期のズレを `checks/task-05d.md` に申し送りとして記録する（`design.md` は変更しない）
- [x] commit & push（STEP 1〜5、以下 STEP 6〜8 とは別コミット）
- [x] STEP 6: `mapping/tools/verify_mapping.py` に `check_reference_only_sections` を追加する。`CONTENT_BEARING = {"MOVE", "MERGE", "SPLIT"}` を定義し、`mapping.csv` が使う全 `(dest_part, dest_page, dest_section)` のうち `CONTENT_BEARING` の行が1件も無いものを列挙する。advisory 出力とし `exit 1` しない
- [x] STEP 6: `#6` の Steps に「`reference-only sections` の全件について本文なしで確定するか本文行を割り当てるかを判断し `checks/task-06.md` に記録する」を追加し、Completion criteria に「`reference-only sections` の全件に判断が記録されている（0件にする必要はない）」を追加する（既存のsteering.md #6に記載済みであることを確認）
- [x] STEP 6: commit
- [x] STEP 7: `verify_mapping.py` に `check_intro_section_split` を追加する。`heading_path` が `(L1直下)`/`(L2直下)`/`(冒頭)` で終わる非DROP行（導入文行）の `dest_section` が、同じ `src_file` かつ同じ親 `heading_path` を持つ他の非DROP行（同階層行）のどれとも一致しない場合に検出する。`(L2直下)` は ERROR（`exit 1`）、`(L1直下)`/`(冒頭)` は advisory（比較対象は `dest_section` 単独とした。理由・実測は `checks/task-05d.md` STEP7参照）
- [x] STEP 7: ERROR 2件（`current-0150`/`current-0269`）を `git show c241906:<src_file>` で実ファイル通読のうえ是正する。`#5` Steps のルール「`(L2直下)` 行は同じ親を持つ配下セクションと同じ `dest_section` に置く」を適用し、同階層行の `dest_section` が複数ある場合は導入文が実際にどちらを導くかを実ファイルで確認して決める（行数の多寡で決めない）。`_batch/*.csv` を編集し `mapping.csv` を再生成する。`dest_page`/`disposition`/`audience` は変更しない。`note` に旧→新と根拠 file:line を追記する
- [x] STEP 7: advisory 4件（`input-0114`/`current-0060`/`current-0142`/`current-0148`）はマッピングを変更せず、`note` 末尾に `[セクション境界]` 形式の申し送りを追記する（既存 note は削除しない）
- [x] STEP 7: commit
- [x] STEP 8: `#8〜: ページの作成` の Steps に「`note` に `[セクション境界]` がある場合は導入文と本体の接続をページ内で再構成する」「`reference-only sections`（advisory）に該当する場合は `#6` で確定した方針に従う」の2行を追加する（既にsteering.md #8〜 Steps に記載済みであることを確認、line 519・520）
- [x] STEP 8: `checks/task-05d.md` に、STEP7で是正した2行の旧→新と根拠 file:line、advisory 4件の判断理由を記録する
- [x] STEP 8: commit & push
- [x] **user review** — 承認済み（`/rn:ty` で承認、ARGUMENTS「#5dはOK、次に進んで」）

**Completion criteria**:

- `split-plan.md` に `input-0016`/`input-0030` の行があり、`parts` の行範囲が `mapping.csv` と一致する（機械検証）
- `checks/task-05.md` の暫定一覧に27行全件が現れる（機械検証: `note` が「暫定」で始まる行の `mapping_id` 全件が一覧表に存在する）
- `design.md` に差分がない（`git diff` で確認）。`mapping.csv`/`_batch/*.csv` はSTEP7の是正2件（`current-0150`/`current-0269`の`dest_section`）とSTEP1-5・STEP7のnote追記のみが差分であり、`dest_page`/`disposition`/`audience`に差分がないことを`git diff`で確認済み（当初の「差分がない」は`#5d`をSTEP1-5のみと想定した時点の記述で、`ntf-doc-05d-addendum.md`がSTEP7で`_batch/*.csv`編集を明示的に指示したことにより古くなっていた）
- `check_reference_only_sections` / `check_intro_section_split` が `verify_mapping.py` に実装され、コミットされている
- `check_intro_section_split` の ERROR が0件
- `reference-only sections` の advisory 件数が2件で、`#6` の Steps・Completion criteria に引き継ぎが追記されている
- `[セクション境界]` の `note` 追記が4件あり、対象 `mapping_id` がレビュー時の実測と一致する
- 593行 / 12,986 / 11,983 が不変（`591行 / 12,986 / 11,973`は`#5c`差し戻し対応完了前の旧基準値。`#5c`（`#5d`のPrerequisites）が`109b736`で591→593行・DROP除く11,973→11,983に確定させており、`#5d`はこの値を維持することが正しい不変条件）
- `checks/task-05d.md` に、是正した2行の旧→新と根拠 file:line、advisory 4件の判断理由が記録されている

### #6: 未確定事項の確定と design.md 更新

**Purpose**: 文量集計に基づいて未確定事項を確定させる。

**Prerequisites**: #5d

**Steps**:

- [x] `volume.md` の集計をもとに、design.md「10. 未確定事項」の3件を確定する
- [x] design.md を更新する（「未確定事項」節を削除し、確定した構成を本文に反映）
- [x] 確定に伴い `mapping.csv` の `dest_page` を更新する
- [x] `mapping.csv` の `note` が「暫定。」で始まる行をすべて洗い出し、確定した構成に基づいて正式な `dest_page` に更新し、`note` の「暫定。」表記を解消する
- [x] `verify_mapping.py` の `reference-only sections` の全件について、「本文なしで成立するページ構成として確定する」か「本文を持つ行を割り当てる」かを判断し、結果を `checks/task-06.md` に記録する
- [x] self-check（`checks/task-06.md`）
- [x] commit & push
- [ ] **user review** — 承認を受けるまで #7 に進まない（**サブエージェントによるレビューは実施しない**。self-check のみで user review に上げる）

**`#6` レビュー指摘対応（`ntf-doc-06-followup.md`、2026-07-28）**:

判定: `#6` は承認。差し戻しではなく、レビューで見つかった小さな漏れ2件（`[セクション境界]` note未反映1件・
self-check記述の実態不一致1件）の対応。`design.md`/`mapping.csv` の判断内容は変更しない。詳細は
`checks/task-06-followup.md` を参照。

- [x] 対応1-2: `verify_mapping.py` に `check_intro_note_present` を追加し、RED（`current-0128-a` を ERROR で検出、`exit 1`）を確認する
- [x] 対応1-1: `current-0128-a` の `note` に `[セクション境界]` を追記し、`mapping.csv` を `_batch/*.csv` の単純連結で再生成する
- [x] 対応1-3: GREEN（`exit 0`、advisory 5件全件に `[セクション境界]` note）を確認する
- [x] 対応1-4: `#8〜` の Steps に件数固定の記述がないか確認する（なし、修正不要と確認）
- [x] 対応2: `checks/task-06.md:906` の self-check 記述を実態に合わせて書き換える
- [x] commit & push
- [x] **user review** — 承認済み（`/rn:ty` で承認）

**Completion criteria**:

- design.md に未確定事項が残っていない
- design.md の章構成と `mapping.csv` の `dest_page` の集合が一致する
- ファイル名に連番（`01_`, `02_` 等）が使われていない
- `mapping.csv` の `note` が「暫定。」で始まる行がすべて解消されている（design.md 確定後に正式な `dest_page` へ更新済み）
- `mapping.csv` の `dest_page` に `mapping/vocabulary.md` の暫定語彙（第2部の暫定8ページ、処理方式付きの仮ページ名）が1件も残っていない（機械検証。置換漏れの検出手段）
- `verify_mapping.py` の `PENDING_ZERO` が0件であること（#6 で全件が確定または EXPECTED_ZERO へ移動）
- `reference-only sections` の全件に判断が記録されている（0件にする必要はない）

### #7: 現行NTF解説書の削除

**Purpose**: 白紙の状態を作る。

**Prerequisites**: #6

**Steps**:

- [x] `ja/development_tools/testing_framework/` 配下の `.rst` を削除する
- [x] `ja/development_tools/index.rst` の NTF への toctree 参照の現状を `checks/task-07.md` に記録する
- [x] 削除前の全ファイル一覧（パスと行数）を `checks/task-07.md` に記録する
- [x] 画像ファイル（`_image/`、`_images/`）およびダウンロード素材は削除しない
- [x] commit & push
- [ ] **user review** — 承認を受けるまで #8 に進まない（**サブエージェントによるレビューは実施しない**。self-check のみで user review に上げる）

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
- [ ] 当該 `dest_page` の行に `note` の `[セクション境界]` が含まれる場合、導入文と本体の接続をページ内で再構成する（出典の分断をそのまま持ち込まない）
- [ ] 当該 `dest_page` に `reference-only sections`（`verify_mapping.py` の advisory）が該当する場合、`#6` で確定した方針に従う
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

(written by /rn:dn, read and reset to this placeholder by /rn:up. `Status` is `paused` while a
session is suspended — the signal /rn:up and /rn:dn search for — and resets to `not suspended` here,
so only a genuinely suspended session reads `paused`.)

- **Status**: paused
- **Date**: 2026-07-28
- **Last completed**: `/rn:ty`で`#6`フォローアップのuser reviewを承認として記録し、`#7`（現行NTF解説書の削除）を実施。削除前に`ja/development_tools/testing_framework/`配下の`.rst`全47件（パス・行数）と`ja/development_tools/index.rst`のtoctree参照（`testing_framework/index`）・`ja/index.rst:54`の`:doc:`参照の現状を`checks/task-07.md`に記録（いずれもリンク切れになるが本タスクでは更新しない旨を明記）。`git rm`で`.rst`47件を削除し、画像・ダウンロード素材125件（`_image/`/`_images/`/`download/`/`_download/`配下）は無変更であることを`find`で確認。`steering.md`の`#7` Steps5件を`[x]`化。
- **Next**: `#7`のcommit & pushを行い、`user review`（承認を受けるまで`#8〜`に進まない）を提示する。承認後は`#8〜`（ページ作成、作成順: 第1部 → 第3部のテストデータ2ページ → 第2部 → 第3部の残り）に着手する。
- **Notes**: branch/PR: `lovaizu/nablarch-document`の`work` = PR #730（`nablarch/nablarch-document`）のhead。base commitは`c24190607fef5d76c607aa08b36d2ab2f813efe5`。push権限は解決済み（`kiyobot`=`GH_TOKEN`がwrite権限を保有）。`#6`本体・フォローアップとも承認済み。open blocker: `#7`のuser review待ち。承認後`#8〜`のタスク番号・ページIDは`mapping.csv`の`dest_page`一覧から確定する必要あり（steering.mdに未記載）。
