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
- `#9` 差し戻し是正指示: `.rn/20260724-ntf-yaml-support/ntf-doc-09-fix.md`
- `#9` 再構成指示: `.rn/20260724-ntf-yaml-support/ntf-doc-09-restructure.md`
- `#10a` 用語統一・並び替え指示: `.rn/20260724-ntf-yaml-support/ntf-doc-terminology.md`
- `#10a` 追補（`about/index.rst` の扱い）: `.rn/20260724-ntf-yaml-support/ntf-doc-terminology-addendum.md`
- `#10a` 回答（`design.md:65` の是正・特殊記法セクションの導入文）: `.rn/20260724-ntf-yaml-support/ntf-doc-terminology-answer.md`
- `#10b` 作業指示（`#10a` 承認後の仕上げ）: `.rn/20260724-ntf-yaml-support/ntf-doc-10a-followup.md`
- `#11` 作業指示（共通設定）: `.rn/20260724-ntf-yaml-support/ntf-doc-11-common.md`
- `#12` 作業指示（`:ref:` ラベル命名規則の確定）: `.rn/20260724-ntf-yaml-support/ntf-doc-12-ref-labels.md`
- `#13` 作業指示（ページ作成の共通手順の定着）: `.rn/20260724-ntf-yaml-support/ntf-doc-13-standing-rules.md`
- `#16` 作業指示（リード文の確定と `design.md` の3点追記）: `.rn/20260724-ntf-yaml-support/ntf-doc-16-lead-and-design.md`
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
- **ビルド確認は自分でDockerを使って行う。**`make html`の確認をユーザーに丸投げしない。ローカルvenv（`/home/tie303177/venv`）が`requirements.txt`のピン留め版と非互換（Python 3.12・`javasphinx`未対応）であることは、Docker実行を省略してよい理由にはならない。README「環境構築」＞「Docker」の手順（`docker build -t nablarch-document-build .`、`docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"`）に従い、コンテナ内で実行する。2026-08-03、同一の確認を2回ユーザー自身にやらせてしまい指摘を受けた
- **日本語の地の文（段落）は、途中で改行しない。1段落は1行で書く（文の区切りであっても改行しない）。** RSTの段落はソース上の改行をHTML出力時にも生の`\n`として残し、ブラウザは`white-space: normal`のもとでこれを半角スペース1個として描画するため、ソースを折り返すと本文に不要な隙間が入る（2026-08-03、`testing_framework/index.rst`で実測・`build succeeded`のHTMLソースで`\n`の残存を確認して特定）。`about/index.rst`にも同種の改行が複数箇所残っている（8〜9行目・12〜13行目等、`#8`のuser review未了分として要修正）。ページ作成・レビュー時は、段落内に改行がないか（空行を挟まず日本語の行が連続する箇所がないか）を確認する
- **文章表現は、design.md等の内部設計文書の言い回しをそのまま使わない。既存の解説書（FW解説書ライブラリ等）に同種の表現があるか`grep`で確認してから書く。** design.mdは開発チーム内部の設計文書であり、その文体（例:「読者は2種類に分かれる」のように読者を外側から分析する言い回し）を利用者向けページにそのまま持ち込むと、実際の解説書のどこにも使われていない不自然な文になる（2026-08-03、`testing_framework/index.rst`で`grep -rn "対象読者|読者は"`が0件だったことで実際に確認）。design.mdの内容（意図・構造）を参照するのは良いが、文言をそのまま転記しない
- **`=`のみで罫線を引く簡易tableのセル文字列を編集するときは、列位置を「表示幅」（全角文字は2、半角文字は1）で揃える。文字数（Pythonの`len()`等）で揃えない。** 見出し行の`=`の並びが表示幅基準の列境界を表しており、セル文字列の表示幅がずれると`sphinx-build`が`Malformed table`エラーを出す（2026-08-03、`about/index.rst`の表でセル文字列を短くした際に文字数基準で詰めて実際に発生・`unicodedata.east_asian_width`で是正）。編集後は必ずDockerビルドで確認する
- **各ページのセクション・小見出しの並び順は、「元資料（現行解説書・input資料・マッピングの行順）の構成」ではなく「そのページに来た読者が最初に欲しい答えは何か」を起点に組み立て直す。** マッピングは「何を書くか（事実・表・図）」の典拠として使い、「どの順で書くか」はページごとに読者の問いから毎回考える。ただし第2部・第3部の大見出し順（機能概要→使用方法→拡張例等）は`style.md` S-02で既に確定・FW解説書で裏付け済みのテンプレートであり、これを崩す原則ではない。この原則が主に効くのは、テンプレートが無い第1部の節順（2026-08-05、design.md §2で「テストの種類」をアーキテクチャより前に並べ替えた判断が最初の適用例）と、各節内の小見出し・項目の並び順
- **design.mdが特定のページを「〜の構成に倣う」と指定している場合、そのページを実際に開いて構成（見出しの分け方・`:ref:`の使い方・文の続け方）を確認してから設計する。「倣う」対象の話題や見出し名だけを真似て、実際のファイルを読まずに構成を推測しない。** `#8`のフィードバック2ラウンド目で、design.mdが「FW解説書の`Nablarchアプリケーションフレームワークとは`の構成に倣う」と明記していたにもかかわらず、実際に`nablarch/big_picture.rst`を読まないまま「全体像」「特徴」を別見出しに分け`:ref:`で行き来させる独自構成を作ってしまい、ユーザー指摘で発覚した（2026-08-05）。実際のファイルは「全体像」と「特長」を1つの節にまとめ、「Xができる」という提示に具体的なメリットを同じ場所で続ける一体の構成だった。「倣う」という指示がある箇所では、着手前に必ず参照先ファイルを`Read`する
- **複数点のフィードバックに対応するときは、各指摘を個別に直す対症療法で終えず、直した結果のページを上から通しで読み直し、指摘されていない箇所も含めて整合性（前後の重複、矛盾、行き来するだけのリンク、浮いた記述）を確認してから報告する。** `#8`のフィードバック1ラウンド目は、6点の指摘それぞれには機械的に対応したが、その結果生じた新たな不整合（「特徴」から直前に読んだばかりの「全体像」へ戻る`:ref:`等）に気づかず、2ラウンド目で「品質が低すぎて指摘だらけ、なぜ？」という指摘を受けた（2026-08-05）。個別修正がすべて完了した後、必ず通し読みの確認ステップを独立して行う
- **タスクが完全に閉じたら（全Steps完了・レビュー通過・user review承認済み）、次のタスクに進む前にそのタスクのエントリを圧縮する。** 見出しに`— DONE`を付し、Steps・差し戻し経緯・narrativeを削り、Purpose（1行）とCompletion criteriaのみ残して`checks/task-XX.md`と最終コミットへのポインタを添える。rnプラグイン自身の設計方針（`steering.md`は「lean forward contract」であり、履歴はgit + PRに置きsteering.mdには残さない）に基づく。#8以降34ページのページ作成タスクで積み上がるのを防ぐため、圧縮を都度行い最後にまとめてやらない（2026-08-05、`#1`〜`#7`をこの方針で圧縮・steering.mdを720行→約260行に縮小）
- **1件のフィードバック対応につき、詳細な理由づけを書く場所を1箇所に決め、他の場所は1〜2行のポインタにとどめる。** 設計判断そのもの（何を・なぜ）は`design.md`の該当節にのみ書く。レビュー監査の記録（指摘→対応の対応表）は`reviews/page-*.md`にのみ書く。`steering.md`のStepsには「Nラウンド目、M点対応。一言の要約。詳細はdesign.md§X・reviews/page-Y.md参照。commit `<hash>`」程度の1〜2行のみ記載し、同じ理由づけを全文で書き直さない。2026-08-05、`#8`のフィードバック対応が5ラウンド積み重なった結果、同じ内容を`design.md`・`reviews/page-about_index.md`・`steering.md`の3箇所にほぼ全文で重複記載してしまい、ユーザーから「文量が大量なんだけど、こんなに必要なの？」と指摘を受けたことによる（Steps 16件・約165行を1〜2行×16件に圧縮）
- **ページのタスクが`user review`承認で閉じたら、`design.md`の該当節も同様に圧縮する。** 各ラウンドの元の指摘文の引用・差し戻し経緯は削り、最終決定と一言の理由、`reviews/page-*.md`へのポインタのみ残す。34ページ分を通しで行う設計文書のため、圧縮しないとページ数に比例して際限なく肥大化する

# Tasks

**（`#1`〜`#7` は完了済み。2026-08-05、`steering.md`肥大化対策として、Steps・差し戻し経緯などの詳細をgit履歴・`checks/`配下へのポインタに圧縮した。rnプラグイン自身の設計方針「steering.md is a lean forward contract — heavy content lives elsewhere...history live in git + PR, never in steering」に基づく。以降、タスクが閉じたら次のタスクに進む前に同様の圧縮を行う（本節末尾のRules参照）。）**

### #1: 作業指示の受領とタスク詳細化 — DONE

**Purpose**: 作業指示を受領し、steering.md を確定させる。

**Completion criteria**:

- Acceptance criteria に具体的な検証可能な条件が記載されている
- Tasks にユーザー指示に対応したタスクが分解・記載されている

**Closed**: commit & push 済み。詳細は git 履歴を参照。

### #2: セクション抽出ツールの作成 — DONE

**Purpose**: 現行解説書とinput資料の記載内容を、セクション単位で機械的に抽出する。

**Completion criteria**:

- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）
- 抽出対象ファイル数が実ファイル数と一致することを Evidence に記載
- CSVのレコード数を **`csv.DictReader` でカウントした値** で Evidence に記載
- 抽出したセクション数が、実ファイルから独立に数えた見出し数と一致することを Evidence に記載

**Closed**: user review 承認済み。詳細は `checks/task-02.md` および git 履歴を参照。

### #2a: セクション抽出の取りこぼし解消 — DONE

**Purpose**: 見出し階層のどこにも属さない本文が発生しないよう抽出ルールを修正し、行の取りこぼしゼロを機械的に証明する。

**Completion criteria**:

- `lines` が当該セクションのカバー範囲そのものである（`body_end_line - body_start_line + 1 == lines`）
- セクションのカバー範囲の和集合と全行集合の差が、見出し行を除いて非空行0件である
- 見出し行以外に未カバー行が残る場合、その行と理由が `checks/task-02a.md` に全件列挙されている
- 抽出対象ファイル数が RST 47・MD 10 であり、セクション0件のファイルが存在しない
- `bash mapping/tools/build_mapping.sh` を2回実行して同一のCSVが生成される（md5一致）

**Closed**: user review 承認済み。詳細は `checks/task-02a.md` および git 履歴を参照。

### #3: 用語集の作成 — DONE

**Purpose**: 全ページで統一する用語を確定する。ラウンド1〜3のレビューが収束せず、用語候補を機械抽出した母集合に再構成。その後のレビューで、用語集の役割を「ページ作成時に表記を揃えるための参照物」に縮小する方針転換があった（ユーザー判断。全量保証の基準は`#5`マッピングが担うため、そちらに力を配分）。

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

**Closed**: user review 承認済み。差し戻し経緯・指摘トリアージの詳細は `checks/task-03.md` および git 履歴を参照。

### #4: トンマナ規約の作成 — DONE

**Purpose**: `style.md` は「ページ作成時にCCが従う基準」である。FW解説書ライブラリの記述の調子を写し取れば足り、網羅性を追求する対象ではない（ユーザー判断）。観点は8つに限定: 文体／ページのセクション構成／セクションタイトルの形式／見出しのアンダーライン記法／コードブロックの記法／アドモニションの使い分け／表の記法／`:ref:`ラベルの命名規則。

**Completion criteria**:

- 上記8観点すべてに規約と根拠（FW解説書ライブラリの file:line、各2件以上）がある
- design.md の第2部・第3部のページアウトラインと矛盾がない
- 観点が8つ以外に増えていない

**未決事項（#4のスコープ外）**: `glossary.md` §6・§11.2 の3項目（括弧の全角・半角、英数字と日本語の間の空白、送り仮名・漢字/かなの揺れ）は上記8観点に該当しないため扱わない。#8以降のページ作成で実際に必要になった場合、その都度FW解説書ライブラリの多数派表記に合わせて個別判断する。

**Closed**: user review 承認済み。詳細は `checks/task-04.md` および git 履歴を参照。

### #4a: 大きいセクションの分割判断 — DONE

**Purpose**: マッピング作成の前に、複数の割当先に分かれるセクション（`lines >= 100`の23件）を特定し、分割位置を確定する。

**Completion criteria**:

- 対象23セクションすべてに `split` の判定と `rationale` がある
- `split=yes` の全件について、`parts` の行範囲の和集合が元のセクションの `body_start_line`〜`body_end_line` と一致する（隙間・重複ゼロ）
- `parts` の割当先が design.md の章構成に存在するページ・セクションである

**Closed**: user review 承認済み。詳細は `checks/task-04a.md`・`mapping/split-plan.md` および git 履歴を参照。

### #5: マッピングリストの作成 — DONE

**Purpose**: 現行解説書とinput資料の全セクションを design.md の章構成に割り当てる。本作業の全工程で唯一の基準となる。2026-07-28、ユーザー差し戻し2回（DROP見直し13件の再検証・第4部新設に伴うdest_part付け替え44行・verify_mapping.pyのvocabulary突合バグ修正）と「導入」0件指摘への対応（15行の再判定）を経て確定。

**Completion criteria**:

- `mapping.csv` に `DROP` 行も含めて全セクションが残っている（追跡可能性のため削除しない）
- `sections-current.csv` / `sections-input.csv` の全 `section_id` が `mapping.csv` の `src_section_id` に最低1回現れる
- 各 `src_section_id` について、紐づく全マッピング行の `[src_body_start, src_body_end]` の和集合が、元のセクションの `[body_start_line, body_end_line]` と一致する（隙間・重複ゼロ）
- `DROP` を除いた `lines` 合計が `volume.md` に記載されている
- `disposition` / `audience` が空欄の行が0件、`DROP` の全行に `note` が記入されている
- `dest_page` / `dest_section` に design.md に存在しないものが含まれていない
- 検証は `mapping/tools/verify_mapping.py` で行い、コミットされている（手作業で確認しない）

（注: 行数不変条件は#5確定当時591行・12,986・DROP除く11,973。`#5c`/`#5d`の是正を経て最終確定値は593行/12,986/11,983。最新値は`mapping.csv`・`volume.md`を参照）

**Closed**: user review 承認済み。詳細は `checks/task-05.md` および git 履歴を参照。

### #5b: 割当先0件問題の解消 — DONE

**Purpose**: 「語彙が定義しているのに割当が0件」を機械検出できる状態にし、再判定で解消できるものを解消し、`#6` のユーザー判断が必要なものを調査報告として残す。詳細な仕様は `.rn/20260724-ntf-yaml-support/ntf-doc-05b-instruction.md`。

**Completion criteria**:

- `verify_mapping.py` に `check_unused_vocabulary` が実装され、コミットされている
- `EXPECTED_ZERO` の全エントリに `design.md` の該当箇所の引用が理由として付いている
- `PENDING_ZERO` の全エントリに `#6` のどの未確定事項に対応するかが書かれている
- `check_unused_vocabulary` の ERROR が0件
- `checks/task-05b.md` に、`dest_section` を変更した行と変更しなかった行の両方が根拠付きで列挙されている
- `volume.md` に0行ページと `dest_section` 単位の集計が載っている
- `design.md` が変更されていない

**Closed**: user review 承認済み（独立検証。指摘2点は`#5d`の追加STEPとして反映）。詳細は `checks/task-05b.md` および git 履歴を参照（コミット `ca1e9cf`）。

### #5c: `DROP` 全件レビュー — DONE

**Purpose**: `design.md` §11.8「`DROP` は件数の多寡にかかわらず全件を対象とする」の未達分を解消する。初回レビューの分類基準の欠陥（判定保留の2行が根拠なく「レビュー済み」に分類）を差し戻しで是正。

**Completion criteria**:

- `DROP` 96行すべてが `checks/task-05c.md` の表に現れ、各行に確定した判定と根拠がある（保留のまま閉じた行がない）
- 判定が覆った行（`input-0178`・`input-0198`）は `_batch/*.csv` を修正し、`verify_mapping.py` がエラー0件
- `check_unused_vocabulary` に許可リストの陳腐化検出（`stale allowlist`）が実装され、コミットされている

**Closed**: user review 承認済み（差し戻し対応後、独立検証APPROVE相当）。詳細は `checks/task-05c.md` および git 履歴を参照（コミット `109b736`）。

### #5d: 記録の整合とセクション境界の是正 — DONE

**Purpose**: `#5` までの成果物に残った記録上の不整合を解消し、`#5b` のレビューで検出したセクション境界の欠陥を是正する。既存の割当判断（dest_page / disposition / audience）は変更しない。

**Completion criteria**:

- `split-plan.md`・`checks/task-05.md`（暫定扱い一覧）が整合している
- `check_reference_only_sections` / `check_intro_section_split` が `verify_mapping.py` に実装され、コミットされている
- `check_intro_section_split` の ERROR が0件（是正2件: `current-0150`/`current-0269`）
- `reference-only sections` の advisory 2件に `#6` への引き継ぎが記録されている
- `[セクション境界]` note追記4件の判断理由が `checks/task-05d.md` に記録されている
- 593行 / 12,986 / 11,983 が不変

**Closed**: user review 承認済み（`/rn:ty`）。詳細は `checks/task-05d.md` および git 履歴を参照。

### #6: 未確定事項の確定と design.md 更新 — DONE

**Purpose**: 文量集計に基づいて design.md の未確定事項3件を確定する。承認後のフォローアップで小さな漏れ2件（`[セクション境界]` note未反映1件・self-check記述の実態不一致1件）に対応。

**Completion criteria**:

- design.md に未確定事項が残っていない
- design.md の章構成と `mapping.csv` の `dest_page` の集合が一致する
- `mapping.csv` の `note` が「暫定。」で始まる行がすべて解消されている
- `mapping.csv` の `dest_page` に暫定語彙が1件も残っていない（機械検証）
- `verify_mapping.py` の `PENDING_ZERO` が0件
- `reference-only sections` の全件に判断が記録されている

**Closed**: user review 承認済み（本体・フォローアップとも）。詳細は `checks/task-06.md`・`checks/task-06-followup.md` および git 履歴を参照。

### #7: 現行NTF解説書の削除 — DONE

**Purpose**: 白紙の状態を作る。

**Completion criteria**:

- `ja/development_tools/testing_framework/` 配下に `.rst` が存在しない
- 削除前のファイル一覧が Evidence に記録されている
- 画像・ダウンロード素材が保持されている

**Closed**: user review 承認済み（本体・フォローアップとも。State欄2026-07-28時点の記録「#6本体・フォローアップ、#7本体・フォローアップとも承認済み」で確認。本タスクのuser reviewチェック行が未チェックのまま残っていたのを今回是正した）。フォローアップで外部被参照ラベル1件（`db_double_submit.rst`からの参照）を検出し、`#8〜`・`#last`にラベル再定義・解消確認のStepを追加済み。詳細は `checks/task-07.md` および git 履歴（`0cc47d3`）を参照。

### #8: 第1部「テスティングフレームワークとは」の作成（`about/index.rst`）— DONE

**Purpose**: マッピングに従って第1部（概念、1ページ）を作成する。design.md 11.5「最初の1ページで基準を作る」の対象タスク。

**Completion criteria**:

- `mapping.csv` の `dest_page=テスティングフレームワークとは` の全行（8行、複数回のフィードバック対応による
  再割当を経て確定）が反映されている
- 4観点のレビューがすべて実施・記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が `about/index.rst` についてエラーを出さない
- `ja/development_tools/testing_framework/index.rst` から `about/index.rst` / `setup/index.rst` /
  `implementation/index.rst` / `tools/index.rst` への toctree 導線がある

**Closed**: user review 承認済み（`/rn:ty`、2026-08-05）。フィードバック対応は本体レビュー3ラウンド＋ユーザー直接
指摘6ラウンド超に及んだ。詳細（各ラウンドの指摘・判断理由・出典根拠）は `design.md`§2、`reviews/page-about_index.md`、
`checks/task-08.md` および git 履歴（最終内容コミット `cb0d8d9`）を参照。
2026-08-06、`/rn:gm`フィードバック（各ページ先頭への目次追加）を受け、`.. contents::` を追記（`style.md` S-09）。

### #9〜: ページの作成（1ページにつき1タスク）

**Purpose**: マッピングに従ってページを1つ作成する。

**個別の作業指示を出す条件**: **個別の作業指示は、次のいずれかに当たるページにのみ出す。** それ以外のページは本節の共通 Steps に従って進める。(1) 出典が500 lines を超えるページ、(2) `design.md` の確定事項どうし、または `design.md` と `mapping.csv` が食い違うページ、(3) 出典が0行で、書く内容を設計から決める必要があるページ（導線のみの3ページなど）。

**Prerequisites**: #8（以降は直前のページタスク）

作成順: 第3部のテストデータ2ページ → 第2部 → 第3部の残り → 第4部

タスク番号・ページIDは #8 完了後、ページごとに確定する。

**前方参照によるスタブページ**: #8で`setup/junit5_extension.rst`・`tools/testdata_converter.rst`を見出しのみで作成し、`setup/index.rst`・`tools/index.rst`のtoctreeに追記済み（undefined label警告解消のため。2026-08-05）。該当ページのタスクが来たら、新規作成ではなく既存ファイルへの追記として扱う。同様に他ページからの前方参照でundefined label警告が出た場合も、対象ページの見出しのみのスタブを先行作成し対応するtoctreeに追記する運用とする（毎回の警告差分確認の手間を減らすため）。#9の作業で同じ理由により`implementation/testdata_examples.rst`（`#10`用）を見出しのみで先行作成し`implementation/index.rst`のtoctreeに追記済み。

### #9: テストデータの書き方（`implementation/testdata_notation.rst`）— DONE

**Purpose**: マッピングに従って「テストデータの書き方」（記法の仕様。どう書けばどう解釈されるか。design.md §4）を作成する。対象は `mapping.csv` の `dest_page=テストデータの書き方` の140行。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-07）。差し戻し3回（`ntf-doc-09-fix.md` STEP1〜7 / `ntf-doc-09-restructure.md` STEP A〜G / `ntf-doc-09-recordtype.md`）とユーザー直接フィードバック多数を経て確定。承認時点で本文に `important` 2件（レコード種別の形式差・テーブルデータの行内カラム値未記載時の形式差）が入っており、作業指示の「追記1件のみ」に対し横並び確認で自発検出した1件を含む構成のまま承認された。詳細は `reviews/page-testdata_notation.md`（ラウンド1〜8）・`checks/task-09.md`・`checks/task-09-restructure.md`・`checks/task-09-recordtype.md` および git 履歴（最終内容コミット `73e84dc`）を参照。`#10` 以降への申し送り15件は `reviews/page-testdata_notation.md` 末尾。

### #10: テストデータの記載例（`implementation/testdata_examples.rst`）— DONE

**Purpose**: マッピングに従って「テストデータの記載例」（用途別の実例。design.md §4）を作成する。対象は `mapping.csv` の `dest_page=テストデータの記載例` の65行。機能概要・使用方法のいずれも持たない例外ページ。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-07）。本体（4観点レビュー・`must` 7件/`should` 14件対応）＋`/rn:gm` 差し戻し2回で確定。1回目はセル格子への識別子行追加（`style.md` S-10 規約2 の差し替え、47表＋`#9` 2表）、2回目はセル値の描画忠実性（smartquotes 対策の4セル）と規約2 へのスコープ条件追記。詳細は `checks/task-10.md`・`checks/task-10-cellgrid.md`・`checks/task-10-quotes.md`、`reviews/page-testdata_examples.md`、作業指示 `ntf-doc-10-cellgrid.md`・`ntf-doc-10-quotes.md` および git 履歴（最終内容コミット `6ba0d2a`）を参照。`#11` 以降への申し送り13件は `reviews/page-testdata_examples.md` 末尾。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] **ページ先頭ラベルは `style.md` S-08「NTF解説書のページ先頭ラベル一覧」から引く。新たに考案しない**（`#12` で34ページ分を確定済み。表に無いページが出た場合は勝手に命名せず `decide` としてユーザー判断に回す）
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
- [ ] **出典が述べている事実のうち、クラス名・プロパティ名・キー名・既定値・書式・桁数など実装で確かめられるものは、`nablarch/nablarch-testing`（YAML 側は `nablarch/nablarch-testing-yaml` の `feature/ntf-yaml`）を clone して実コードで確認してから書く。** 出典どうしが食い違う場合、および出典と実装が食い違う場合は**実装を優先**する（`design.md` §8）。確認した `file:line` と参照コミットを `reviews/page-*.md` に記録する
- [ ] **第2部と第3部の記載範囲を守る**（`design.md` §3「記載範囲」）。第2部にはコンポーネント設定ファイル・環境設定ファイルの設定項目と記述例、拡張方法を置く。**テストソースコードの実装例とテストデータの記述例は第2部に置かず、第3部へ `:ref:` で導線を張る。** 出典に含まれていても同じ。内容を落とすのではなく、事実は地の文に残してコードブロックを置かない
- [ ] マッピングにない内容を追加しない。マッピングにある内容を落とさない
- [ ] 出典の文面をそのまま流用しない。`style.md` に従って書き直す
- [ ] `design.md` 等の内部設計文書の言い回しをそのまま転記しない。既存の解説書に同種の表現があるか `grep` で確認してから書く（Rules参照）
- [ ] 用語は `glossary.md` の正表記を使う
- [ ] L2セクション（`-`の下線）を1つ以上持つページは、タイトル下線の直後に `.. contents:: 目次`（`:depth: 3` `:local:`）を置く。`toctree`のみのインデックスページには置かない（`style.md` S-09）
- [ ] Excel形式/YAML形式の書き分けは `style.md` S-10 に従う（比較して伝える価値がある内容だけ共通の地の文・比較表にする／それ以外の「記述方法」の説明はExcel専用/YAML専用に分け、L3セクションにつき1組のL4見出し「Excel形式の場合」「YAML形式の場合」でまとめる／太字ラベルは見出しを追加できない場合の例外としてのみ使う／Excelのセル格子を表す表では識別子行・ディレクティブ行などシート上に実在する行をすべて表に含め、`:header-rows: 0` とする。識別子は普通の文字で書く）
- [ ] 段落内で改行しない（1段落は1行で書く）。改行はHTML出力時に半角スペースとして残るため（Rules参照）
- [ ] 当該 `dest_page` の行に `note` の `[セクション境界]` が含まれる場合、導入文と本体の接続をページ内で再構成する（出典の分断をそのまま持ち込まない）
- [ ] 当該 `dest_page` に `reference-only sections`（`verify_mapping.py` の advisory）が該当する場合、`#6` で確定した方針に従う
- [ ] 当該ページが、削除された現行解説書の外部被参照ラベルを引き継ぐ場合、
      同名の `:ref:` ラベルを新ページに定義する（対象は `checks/task-07.md`
      「リンク切れになる参照」の表を参照。現時点で1件、
      `implementation/request_unit_test/web.rst` の
      `how_to_set_token_in_request_unit_test`）
- [ ] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（A:網羅性 / B:トンマナ / C:用語 / D:整合性）
  - **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
  - この4観点はページ内容の観点であり、Rules の4観点（QA / 設計 / クラフト / 検証）とは別軸である。ページ作成タスクでは**本欄のA〜Dを用いる**（A:網羅性がQAを、B:トンマナがクラフトを、C:用語とD:整合性が検証を兼ねる）
- [ ] 指摘への対応を行う（最大3ラウンド）
- [ ] **是正ラウンド2以降は、是正差分に限定した検証観点のみを回す。** ラウンド1で4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を回し、ラウンド2以降は「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」だけを見る。**各ラウンドの指摘件数と観点を `reviews/page-*.md` に記録する**（効果測定のため）
- [ ] レビュー記録を `reviews/page-<ページID>.md` に作成する
- [ ] 作成したページを、対応する部の表題ページ（`setup/index.rst` / `implementation/index.rst` /
      `tools/index.rst`）の `toctree` に追記する
- [ ] self-check（`checks/task-NN.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで次ページに進まない

**Completion criteria**:

- `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く）
- 当該 `dest_page` のマッピング行が**全件**、ページのどこに反映されたかの対応表が `checks/task-NN.md` にある（`mapping_id` ごとに反映先のセクション）
- **全件表を求める項目は、ゲートの実行順の先頭に置く。母集合をホワイトリストで切り出さない**（`#10b` の申し送り）
- 4観点のレビューがすべて実施・記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が当該ページについてエラーを出さない

### #10a: 用語「テストショット」への統一と使用方法の並び替え — DONE

**Purpose**: `#5` の「`テストケース` を正表記」判断を覆して `テストケース` を NTF解説書から無くし、あわせて `使用方法` 配下の並び替えと見出し1件の改題を行う（残り32ページに波及するため `#11` の着手前に適用）。

**Completion criteria**:

- 作業指示のゲート1〜13、追補のゲート14、回答のゲート15〜17 がすべて実行結果で確認され、`checks/task-terminology.md` に記録されている
- `about/index.rst` の `テストケース` 2箇所の語選択の理由が、判定表に1行ずつ記録されている
- 作業指示の禁止事項に抵触する変更が無い（`mapping.csv` / `_batch/` / `vocabulary.md` / `style.md` / `ja/conf.py` / `glossary.md` の現行解説書見出し一覧に差分が無い）
- STEP 2 の置換判定と STEP 3-2 の前後関係確認が、いずれも件数ではなく全件の表で記録されている
- `ja/development_tools/testing_framework/` 配下の全 `.rst` に `テストケース` が0件
- Docker フルビルドが `build succeeded` で、警告が既知の1件のみ（新規0件）

**Closed**: user review 承認済み（`/rn:ty`、2026-08-07）。4観点レビュー3巡＋是正4ラウンドを要した。**ラウンド上限3を超過**したのは、ラウンド3の是正が公開本文に事実誤り（`testShots` に存在しないカラム `リクエストID`）と語釈の消失を持ち込んだためで、上限で打ち切らず是正を優先した。承認時点で、レビュアー間で判断の割れた2件（`testdata_examples.rst:401` の数え方、記載例ページの特殊記法セクションへの参照文追加）はいずれも**現状維持**のまま承認された（両論は `checks/task-terminology.md` §13-4）。詳細は `checks/task-terminology.md`（§10 ラウンド1／§11 ラウンド2／§12 ラウンド3／§13 ラウンド4）・`reviews/page-testdata_notation.md`・`page-testdata_examples.md`・`page-about_index.md` および git 履歴（最終内容コミット `6e63e27`）を参照。`#11` 以降への申し送りは `page-testdata_notation.md` の16〜27、`page-testdata_examples.md` の14〜18。

### #10b: `#10a` 承認後の仕上げ3件 — DONE

**Purpose**: `#10a` の user review 承認時に現状維持のまま残った2件（`testdata_examples.rst` の数詞、記載例ページ特殊記法セクションの参照文）と、定義セルの括弧書き削除を適用する。作業指示は `ntf-doc-10a-followup.md`、締めの作業指示は `ntf-doc-10b-close.md`。残り32ページに波及するため `#11` の着手前に適用する。

**Steps**:

- [x] STEP 1 — `testdata_examples.rst` の「2件」をテストショットを数える形に改め、他の導入文の数詞の曖昧さを**全件表**で確認・報告する（是正はしない）
- [x] STEP 2 — 記載例ページの特殊記法セクションの導入文に、例が無い値の種類の記法の在処を示す1文を足し、`testdata_notation-special_notation` へリンクする
- [x] STEP 3 — 値の種類10件について記載例ページの例の有無を**全件表**で突合し、例が無いものを「出典なし」か「網羅性の欠落（`must`）」に判定する（例の追加はしない）
- [x] STEP 4 — `testdata_notation.rst` の定義セルから `（番号・説明・期待するステータスコード）` を削除する（言い換えない）
- [x] STEP 5 — `checks/task-10a-followup.md` を新規作成し、`reviews/page-testdata_notation.md`・`page-testdata_examples.md` に追記（既存記録は書き換えない）。残り32ページへの申し送り2件を追加する
- [x] ゲート1〜10 をすべて実行結果で確認し、`checks/task-10a-followup.md` に記録する（**全件表を求めるゲート7を実行順の先頭に置く**）
- [x] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（QA / 設計 / クラフト / 検証）— 3巡実施
- [x] 指摘への対応を行う（最大3ラウンド）— ラウンド1（`eef48f5`）・2（`4c16caa`）・3（`f87629f`）実施済み。**上限3に到達**。3巡目は QA・設計・検証が pass、クラフトのみ fail で、**公開本文の `must` は4観点とも0件**。未解決はクラフト must-1（数詞の全件表が助数詞ホワイトリスト方式の穴で出現単位の全件になっていない。記録側のみ・本文の是正は不要）で、4ラウンド目の実施可否はユーザー判断
- [x] commit & push — `b2f616a` → `eef48f5` → `4c16caa` → `f87629f`
- [x] **user review** — **公開本文は承認**（`/rn:gm`、2026-08-07）。判断待ちの2件に結論が出た（数詞の全件表は4ラウンド目を実施しない／`:401` はセルの実値に揃える）。締めの作業指示は `ntf-doc-10b-close.md`

**Steps（締め — `ntf-doc-10b-close.md`）**:

- [x] STEP 1 — `testdata_examples.rst:401` の `認証エラーケース` を `認証エラー` に改める（セルの実値に揃える。`2つのテストショット` と後半の文は変更しない）
- [x] STEP 2 — 数詞の全件表は作り直さない。`checks/task-10a-followup.md` §1-2 の冒頭に、方式の限界と独立全走査による検証結果（真の数詞の取りこぼし0件）を1段落だけ追記する
- [x] STEP 3 — 「全件表を求める完了条件では母集合をホワイトリストで切り出さない」を `reviews/page-testdata_examples.md`（申し送り23）・`page-testdata_notation.md`（申し送り32）の双方に追記する
- [x] STEP 4 — `checks/task-10a-followup.md` §8 に記録し、`reviews/page-testdata_examples.md` に `:401` の語の変遷と実測根拠を残し、`steering.md` を締める
- [x] ゲート1〜10 をすべて実行結果で確認し、`checks/task-10a-followup.md` §8-4 に記録する — 全件 PASS・NG 0件
- [x] 4観点のレビューは**回さない**（作業指示が明示的に禁止。変更は1語の削除で、ゲート10 が差分を1行に固定している）
- [x] commit & push
- [x] **user review**（締め） — **承認済み**（`/rn:ty`、2026-08-07）。`#10b` は完全に閉じた

**Completion criteria**:

- 作業指示のゲート1〜10 がすべて実行結果で確認され、`checks/task-10a-followup.md` に記録されている
- STEP 1 の数詞の全件確認表、STEP 3 の値の種類の突合表が、いずれも件数ではなく**全件**の表で記録されている
- 両ページに `（番号・説明・期待するステータスコード）` が0件である
- 記載例ページの特殊記法セクションの導入文が `testdata_notation-special_notation` を参照している
- 作業指示の禁止事項に抵触する変更が無い（`mapping.csv` / `_batch/` / `vocabulary.md` / `style.md` / `glossary.md` / `design.md` / `ja/conf.py` に差分が無く、見出しの文言・並び順が不変）
- Docker フルビルドが `build succeeded` で、警告が既知の `db_double_submit.rst` 1件のみ（新規0件）
- 残り32ページへの申し送り2件が `reviews/page-*.md` に追記されている

**Closed**: 締めの user review 承認済み（`/rn:ty`、2026-08-07）。公開本文は先行して承認（`/rn:gm`、2026-08-07）。4観点レビュー3巡＋是正3ラウンド（`eef48f5`・`4c16caa`・`f87629f`）で公開本文の `must` は4観点とも0件に到達し、締めの作業指示 `ntf-doc-10b-close.md` で残り2件に結着した。(1) **数詞の全件表は作り直さない** — レビュー役がホワイトリストを使わない全走査を独立に組んで検証し、既存35行の表が取りこぼしている**真の数詞は0件**であることを確認したため（3巡目に3観点が挙げた9出現はいずれも数を数えていない）。未達だったのは「表が全件でないこと」ではなく「同じ表が全件であることを、その抽出方式では証明できないこと」であり、方式の是正は `#11` 以降への申し送りとした。(2) **`:401` の `認証エラーケース` を `認証エラー` に是正** — 実在するセル値は `:430`・`:484` の `認証エラー` であり、`認証エラーケース` は `ja/`・`input/`・`mapping/` のいずれにも存在しない地の文だけの語であった（`ntf-doc-10a-followup.md` の当該禁止事項は指示側の誤りとして取り消された）。締めの変更は**この1行のみ**で、ゲート1〜10 を全件 PASS（Docker フルビルド `build succeeded, 1 warning.`／新規警告0件）。詳細は `checks/task-10a-followup.md`（§1-2 冒頭の追記／§8 締め）・`reviews/page-testdata_examples.md`（`#10b` 締め・申し送り23）・`page-testdata_notation.md`（申し送り32）および git 履歴を参照。`#11` 以降への申し送りは `page-testdata_notation.md` の28〜32、`page-testdata_examples.md` の19〜23。

### #11: 共通設定（`setup/common.rst`）— DONE

**Purpose**: マッピングに従って第2部の1ページ目「共通設定」を作成する。対象は `mapping.csv` の `dest_page=共通設定` の5行（129 lines、すべて `dest_section=使用方法`）。作業指示は `ntf-doc-11-common.md`。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。加えて、作業指示のゲート1〜11 が実行結果で確認され `checks/task-11.md` に記録されていること、`dest_page=共通設定` の5行が**全件**の対応表で記録されていること（母集合をホワイトリストで切り出さない）。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。4観点レビュー ラウンド1（`must` 2 / `should` 6 / `note` 18）→ 是正ラウンド1（`0a71a75`）で解消 → ラウンド2（`#10b` 申し送りに従い是正差分限定）で `must` 0 / `should` 0 の pass。ゲート1〜11 全件 PASS、Docker フルビルド `build succeeded`（新規警告0件）。**作業指示から外れて是正した2件も承認された** — (1) `nablarch.test.resource-root` の設定先を `コンポーネント設定ファイル` → `環境設定ファイル`、(2) `OracleSequenceIdGenerator` の完全修飾名を `nablarch.common.idgenerator.*` → `com.example.common.idgenerator.*`（いずれも `design.md` §8「出典と実装が食い違う場合は実装を優先する」の適用）。詳細は `checks/task-11.md`・`reviews/page-common.md`（作成時の判断 D-1〜D-6／ラウンド1 R1-1〜R1-12）および git 履歴（最終内容コミット `0a71a75`）を参照。`#12` 以降への申し送り4件は `reviews/page-common.md`（`FastTableIdGenerator` の初期化設定欠落 R1-6／既定値 `test/java` と `testdata_notation.rst` の配置説明の基準ディレクトリ不一致 R1-8／L3 セクションラベル未設置 R1-7／採番の記述例をピンポイント参照するためのラベル追加 D-3）。

### #12: `:ref:` ラベル命名規則の確定（`style.md` S-08 改訂）— DONE

**Purpose**: ページを作らないタスク。`style.md` S-08 を改訂し、残り30ページ分のページ先頭ラベルを先に確定する。Sphinx のラベルはプロジェクト大域であり、ファイル名の語幹をそのまま使うと衝突するため（`ja/conf.py:103` の `keep_warnings = True` により重複ラベルは `#last` まで表面化しない）、21ページ分の判断を先に済ませた。作業指示は `ntf-doc-12-ref-labels.md`。

**Completion criteria**: S-08 の37ラベルと `ja/` 既存ラベルの**全件**突き合わせで衝突0件（母集合は `ja/` の実ファイルから機械抽出）／S-08 の一覧が `design.md` §13 の34ページと過不足なく対応／`verify_mapping.py` が exit 0・594行 / 12,986 / 11,983 不変／`style.md` の差分が S-08 の節内に収まり既存の根拠4件が残っている／禁止事項に抵触する変更が無い／Docker フルビルドが `build succeeded`・新規警告0件。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。ゲート1〜8 全件 PASS。`ja/` の299ファイルから **959ラベル**を機械抽出し37件（34ページ＋表題3件）と突合して **NG 0件**、`design.md` §13 との差集合は双方向で空、Docker フルビルド（`-a`）は `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・`duplicate label` 0件）。**語幹の衝突は実在**であることを実測で確認した（`http_messaging` は `ja/application_framework/application_framework/web_service/http_messaging/index.rst:1` が定義済み。`web`/`rest`/`mom`/`batch`/`db_queue` は `ja/` 全体では未定義だが NTF内部で3〜4ページが共有する）。あわせて**改訂前の `ja/` に既存の重複ラベルが0件**（定義箇所959 = ユニーク959）であることも記録しており、以降 `duplicate label` 警告が出た場合は原因を新規追加分に絞れる。4観点のレビューは作業指示の指定により回していない（ゲート1・2 が全件突合を機械的に担保）。詳細は `checks/task-12.md` および git 履歴（最終内容コミット `18c7856`）を参照。**以降のページ作成タスクは、ページ先頭ラベルを `style.md` S-08 の一覧から引く**（共通 Steps に追加済み）。

### #13: ページ作成の共通手順を `steering.md` に定着させる — DONE

**Purpose**: ページを作らないタスク。`#11` で個別の作業指示として渡した内容のうち以降の全ページに効くものを、「#9〜: ページの作成」の共通 Steps・完了条件に一度だけ入れる。以降の小さいページは個別の作業指示を出さず、`steering.md` だけで進める。作業指示は `ntf-doc-13-standing-rules.md`。

**Completion criteria**:

- 追加が STEP 1 の4件・STEP 2 の2件・STEP 3 の1段落のみで、それ以外の追加が無い
- `steering.md` の差分が「#9〜: ページの作成」の節の中に収まり、既存の Steps・完了条件・Rules に削除・変更が無い（削除行0行）
- `ja/` 配下の `.rst`・`mapping/`・`design.md` に差分が無い
- `verify_mapping.py` が exit 0 で、594行 / 12,986 / 11,983 が不変
- ゲート1〜4 が実行結果で `checks/task-13.md` に記録されている

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。ゲート1〜4 全件 PASS・NG 0件（追加7行 / 削除0行）。STEP 1 の追加は3件 — ページ先頭ラベルの項目は `#12` の締めで既に共通 Steps に入っていたため重複行を作らず、理由を `checks/task-13.md` 冒頭に記録した。4観点のレビューは作業指示の指定により回していない。詳細は `checks/task-13.md` および git 履歴（最終内容コミット `dacd7af`）を参照。**以降のページ作成タスクは、個別の作業指示を出す条件（本節「#9〜」冒頭）に当たらない限り、共通 Steps のみで進める。**

### #14: クラス単体テストの設定（`setup/class_unit_test.rst`）— DONE

**Purpose**: マッピングに従って第2部の2ページ目「クラス単体テストの設定」を作成する。対象は `mapping.csv` の `dest_page=クラス単体テストの設定` の3行（193 lines）。`#13` で定着させた共通 Steps のみで進めた初のページ（個別の作業指示なし）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。4観点レビュー ラウンド1（4観点とも fail・`must` 4 / `should` 8 / `note` 12）→ 是正20件（`ca699c5`）→ ラウンド2は是正差分限定の検証で pass（`must` 0）・残る7件を是正（`5a55ada`）→ `/rn:gm` による締めの追記（`1624182`、作業指示 `ntf-doc-14-close.md`）。ゲート全件 PASS・Docker フルビルド `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規警告0件）。**decide 1件と付録の事実誤り2件が判定で解決した** — `validationTestStrategy` は「載せる」（`current-0010` に実在するため落とすと「マッピングにある内容を落とさない」に抵触）、`minMessageId` が `current-0021` に無いのは欠落ではなく正しい（`CharsetTestVariation.java:126-129` により Nablarch Validation では到達不能）。いずれも事前調査の付録（`ntf-doc-13-standing-rules.md:79`）の記述が指示側の誤りとして取り消された。詳細は `checks/task-14.md`・`reviews/page-class_unit_test.md`（実装で確認した `file:line` と参照コミット `e21bf67`）および git 履歴（最終内容コミット `1624182`）を参照。`#15` 以降への申し送り6件は `reviews/page-class_unit_test.md`（特に「`#10a` の用語一括置換は referent を実装で確かめてから適用する」「出典の制約は実装が検査しているかで採否を決めず、挙動を確かめて理由を書き添える」）。

### #15: リクエスト単体テストの設定（ウェブアプリケーション）（`setup/request_unit_test/web.rst`）— DONE

**Purpose**: マッピングに従って第2部の3ページ目「リクエスト単体テストの設定（ウェブアプリケーション）」を作成する。対象は `mapping.csv` の `dest_page=リクエスト単体テストの設定（ウェブアプリケーション）` の6行（250 lines）。共通 Steps のみで進めた（個別の作業指示なし）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。4観点レビュー ラウンド1（A pass / B pass / C fail / D fail、`must` 3件）→ 是正（`f4c9fad`）→ ラウンド2は是正差分限定の検証で pass（`must` 0）・`should`/`note` 5件を是正（`74e1b10`）。ゲート全件 PASS・Docker フルビルド `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規警告0件）。**出典と実装の食い違い6件を実装優先で解消した**（`dumpVariableItem` の意味の反転 `HttpServer.java:427-430` 等。参照コミット `e21bf67`）。**新構成で最初に画像を使うページ**であり、`guide/` 配下の4件を `setup/request_unit_test/images/web/` へ `git mv` した。**decide 3件は3件とも本ページの判断が承認され、`#16` で `design.md` の規定にした** — 画像の配置（§13「画像の配置」）／陳腐化した例示は落としてよい（§8）／§8 の「実装」には JVM・JDK 等の外部の挙動を含む（§8）。詳細は `checks/task-15.md`・`reviews/page-request_unit_test_setting_web.md` および git 履歴（最終内容コミット `74e1b10`）を参照。`#17` 以降への申し送り11件は `reviews/page-request_unit_test_setting_web.md`（特に「出典の『デフォルト値』欄はフィールドの初期値と一致するとは限らない」「是正で `tip` を新設するときは直上の本文の言い換えになっていないか確認する」）。

### #16: ページのリード文の確定と `design.md` の3点追記 — user review 待ち

**Purpose**: ページを作らないタスク。(1) ページのリード文（目次の直後・最初のL2見出しより前に置く、見出しの無い導入の段落）の位置を `style.md` S-02 と `design.md` §3・§4 で確定し、作成済みの第2部3ページに反映する。(2) `#15` の `decide` 3件を `design.md` §8・§13 に規定として書き残す。いずれも残り29ページに効く。作業指示は `ntf-doc-16-lead-and-design.md`。

**Steps**:

- [x] STEP 1 — `style.md` S-02 にリード文の規約と根拠を追加（規約8行・根拠21行、削除0行）。根拠は FW解説書ライブラリの**全件**調査（`.. contents::` を持つ20ページ中19ページがリード文を持つ。例外は `format.rst` 1件）
- [x] STEP 2 — `design.md` §3・§4 の擬似ツリーにリード文の行を追加し、位置の規約を1段落ずつ添えた
- [x] STEP 3 — 第2部の3ページ（`setup/common.rst`・`setup/class_unit_test.rst`・`setup/request_unit_test/web.rst`）の導入文を目次の直後へ移し、文頭の `ここでは、` を落として主語のある言い切りに直した。差分は3ページとも `+2 / -1` 行のみ
- [x] STEP 4 — `decide` 3件を `design.md` に規定化（§13「画像の配置」を新設／§8 に陳腐化した例示の扱い／§8 に外部の挙動の変化の追記）
- [x] STEP 5 — `checks/task-16.md`・`reviews/` 3件への追記・本エントリ
- [x] ゲート1〜9 — 全件 PASS（`checks/task-16.md`）。Docker フルビルド（`-a`）は `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）
- [x] commit & push
- [ ] **user review**

**Completion criteria**:

- リード文の位置と書き出しが `style.md` S-02 に規約として書かれ、根拠が FW解説書の実ファイルの `file:line` で裏付けられている
- 第2部の作成済み3ページのリード文が目次の直後・最初のL2見出しより前にあり、`使用方法` の直下に地の文が残っていない
- 3ページの `ja/` 差分がリード文の移動と文頭の書き直しに由来するものだけで、見出しの文言・並び順が不変である
- `#15` の `decide` 3件が `design.md` §8・§13 に規定として書かれ、以降のページが参照できる
- `design.md` の差分が §3・§4・§8・§13 に、`style.md` の差分が S-02 に収まり、いずれも削除0行である
- ゲート1〜9 が実行結果で `checks/task-16.md` に記録されている

**注記**: 本タスクを `#16` としたため、**第2部4ページ目「リクエスト単体テストの設定（RESTfulウェブサービス）」（`setup/request_unit_test/rest.rst`）は `#17` になる。** 作業指示の指定により4観点のレビューは回していない（新しい内容を書かないタスクであり、ゲート1〜3 が変更の範囲を機械的に固定している）。作業指示から外れた点3件は `checks/task-16.md` の末尾に記録した（ゲート5の適用範囲／`style.md` の根拠を実測に合わせた訂正2件／`design.md` §4 への1文の追加）。

### #last: Evaluation sign-off

**Purpose**: NTF ドキュメント刷新の完了を Acceptance criteria に照らして確認し、ユーザーの承認を得る。

**Prerequisites**: すべてのページ作成タスク完了

**Steps**:

- [ ] Acceptance criteria の達成状況を確認する
- [ ] `make html` を実行し、**警告を含めて**未解決参照が0件であることを確認する。
      `keep_warnings = True` のため未解決参照はビルド失敗にならないので、
      エラー0の確認だけでは不十分。ビルドログに対し次を確認する
      - `undefined label` が0件
      - `toctree contains reference to nonexisting document` が0件
      - `unknown document` が0件
      確認したコマンドとログの該当箇所を `checks/task-last.md` に記録する
- [ ] `checks/task-07.md`「リンク切れになる参照」3件それぞれについて、
      解消後の参照先（新ファイルパス・ラベル名）を実ファイルで確認して記録する
- [ ] 結果をユーザーに提示して `/rn:ty`（承認）または `/rn:gm`（修正）の判定をもらう

**Completion criteria**:

- すべての Acceptance criteria が達成されていることが確認できる
- `checks/task-07.md`「リンク切れになる参照」の3件すべてが解消されている
  （toctree・`:doc:` の更新、外部被参照ラベルの再定義）
- ユーザーが `/rn:ty` で承認している

# State

(written by /rn:dn, read and reset to this placeholder by /rn:up. `Status` is `paused` while a
session is suspended — the signal /rn:up and /rn:dn search for — and resets to `not suspended` here,
so only a genuinely suspended session reads `paused`.)

- **Status**: not suspended
- **Date**: 2026-08-12
- **Last completed**: `#15`（user review 承認、`/rn:ty`。`decide` 3件も本ページの判断が承認）。続けて `#16`（リード文の確定と `design.md` の3点追記）を実施し、ゲート1〜9 全件 PASS
- **Next**: `#16` の user review の判定（`/rn:ty` 承認 または `/rn:gm` 修正）を受ける。承認なら `#16` エントリを圧縮して締め、`#17`（リクエスト単体テストの設定（RESTfulウェブサービス）、`setup/request_unit_test/rest.rst`）へ
- **Notes**: ブランチ `work`。**実装の clone は session 固有のため再開時に再 clone が必要**（`nablarch/nablarch-testing` の `e21bf67`、`nablarch/nablarch-core`。確認済みの `file:line` は `reviews/page-request_unit_test_setting_web.md`・`checks/task-15.md` に記載済みで再調査は不要）。既知警告は `db_double_submit.rst` の `undefined label` 1件のみ。**`#17` 以降のページは `style.md` S-02 に従い、目次の直後にリード文を置く。画像は `design.md` §13「画像の配置」に従い `images/<ページのファイル名>/` に置く。** 申し送りは `reviews/page-request_unit_test_setting_web.md`（11件。特に「出典の『デフォルト値』欄はフィールドの初期値と一致するとは限らない」「是正で `tip` を新設するときは直上の本文の言い換えになっていないか確認する」）・`page-class_unit_test.md`（6件）・`page-common.md`（4件）・`page-testdata_notation.md`（28〜32）・`page-testdata_examples.md`（19〜23）
