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
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
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
- [ ] レビュー記録を `reviews/page-<ページID>.md` に作成する
- [ ] 作成したページを、対応する部の表題ページ（`setup/index.rst` / `implementation/index.rst` /
      `tools/index.rst`）の `toctree` に追記する
- [ ] self-check（`checks/task-NN.md`）
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで次ページに進まない

**Completion criteria**:

- `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く）
- 4観点のレビューがすべて実施・記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が当該ページについてエラーを出さない

### #10a: 用語「テストショット」への統一と使用方法の並び替え

**Purpose**: `glossary.md` が `#5` で定めた「`テストケース` を正表記、`テストショット` を揺れ表記」の判断を覆し、`テストケース` を NTF解説書から無くす。あわせて `使用方法` 配下のセクション順を「全体から個別へ」に改め、内容の分からない見出し1件を改題する。用語と見出しが残り32ページに波及するため、`#11` の着手前に適用する。作業指示は `ntf-doc-terminology.md` と追補 `ntf-doc-terminology-addendum.md`。

**Prerequisites**: #10（承認済み）

**Steps**:

- [x] STEP 1 — `glossary.md` を改訂する（`:201`/`:207`/`:215`/`:359`/`:552`/`:557`〜`:559`/`:622`/`:637` を内容で照合して編集。`:403`〜`:449` の現行解説書見出し一覧は変更しない）
- [x] STEP 2 — 作成済みページの `テストケース` を1件ずつ判定して置き換える（`テストショット` / `テストメソッド` / `テスト` の3通り。全件を表で記録）
- [x] STEP 3 — `使用方法` 配下の並びを変更し、前方参照を手当てし、崩れた前後関係の参照を全数是正する
- [x] STEP 4 — `値を特殊記法で記述する` を `null・空文字・改行など特殊な値を記述する` に改題する
- [x] STEP 5 — `checks/task-10-quotes.md` の smartquotes 機構の記述を訂正する（`ja/conf.py:158` を根拠に）
- [x] STEP 6 — `checks/task-terminology.md` を新規作成し、`reviews/page-*.md` 2件に追記し、残り32ページへの申し送りを追加する
- [x] 追補 — `about/index.rst` の `テストケース` 2箇所（L24）を、第1部の文脈を読んだうえで判定する（推奨は `テスト`。`テストショット` を選ぶ場合は定義なし初出を承知した旨を記録）。`reviews/page-about_index.md` に追記する
- [x] 回答 — `design.md:65` の `テストケース` を `about/index.rst:24` と同じ語に揃える（`#8` フィードバックの引用文は改変しない）。`design.md` 全体を全数確認し全件表で記録する。是正の根拠は `design.md` §8 の経路とする
- [x] 回答 — `testdata_examples.rst` の特殊記法セクションは**見出しを変えず導入文を見出しに寄せる**（(c) を採用、(b) は不採用）。あわせて値の種類10種の記載例の突合を行い、出典の有無で判定する（**例の追加は行わない。調査と報告のみ**）
- [x] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（本レビュー4＋是正ラウンド1後の再レビュー4）
- [ ] 是正ラウンド2の残り — ゲート1〜17 の再実行（**Docker フルビルド未実施**）と、`checks/task-terminology.md` への C-1〜C-8 の記録反映
- [ ] 是正ラウンド2の再レビュー（4観点。ラウンド上限3のうち2を消化済み）
- [ ] ゲート1〜13、追補のゲート14（`about/index.rst` の差分が L24 の1行のみ）、回答のゲート15〜17（`design.md` の `テストケース` 0件／導入文と見出しの語の一致／10種の突合表）をすべて実行結果で確認し記録する
- [ ] commit & push
- [ ] **user review** — 承認を受けるまで `#11` に進まない

**Completion criteria**:

- 作業指示のゲート1〜13、追補のゲート14、回答のゲート15〜17 がすべて実行結果で確認され、`checks/task-terminology.md` に記録されている
- `about/index.rst` の `テストケース` 2箇所の語選択の理由が、判定表に1行ずつ記録されている
- 作業指示の禁止事項に抵触する変更が無い（`mapping.csv` / `_batch/` / `vocabulary.md` / `style.md` / `ja/conf.py` / `glossary.md` の現行解説書見出し一覧に差分が無い）
- STEP 2 の置換判定と STEP 3-2 の前後関係確認が、いずれも件数ではなく全件の表で記録されている
- `ja/development_tools/testing_framework/` 配下の全 `.rst` に `テストケース` が0件
- Docker フルビルドが `build succeeded` で、警告が既知の1件のみ（新規0件）

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

- **Status**: paused
- **Date**: 2026-08-07
- **Last completed**: `#10a` の STEP 1〜6・追補・回答の本文適用と、4観点レビュー2巡（本レビュー＋是正ラウンド1後の再レビュー）。是正ラウンド2の本文編集（A-1〜A-6・B-1〜B-2）も適用済み。
- **Next**: **是正ラウンド2の残りを完了させる。** (1) `checks/task-terminology.md` に C-1〜C-8 の記録を反映（内容は `reviews/page-*.md` の追記済み分と重複しないこと）。(2) **Docker フルビルド（`-a`）を含むゲート1〜17 を再実行**し実行結果を記録。(3) 是正ラウンド2の4観点再レビュー（ラウンド上限3のうち2消化済み）。(4) `checks/task-terminology.md` を含めて check-off コミット。C-1〜C-8 の内容は `ntf-doc-terminology.md`・`同-addendum.md`・`同-answer.md` と本 State の Notes を参照。
- **Notes**: ブランチ `work`、`origin`（`lovaizu` fork）と同期済み・PR未作成。`#10a` の作業指示は `ntf-doc-terminology.md`＋追補＋回答の3点。**`checks/task-terminology.md` はコーディネーターが check-off 時にコミットする設計**（実装エキスパートには commit させない）。レビュアー4名全員がこれを「未コミット＝重大・差し戻し相当」と判定したが、すべて却下済み。**中断時に `7ea37ac` でコミット済みなので、再開後は追跡下にある**（実装エキスパートには引き続きステージさせないこと）。**是正ラウンド2の未了記録項目 C-1〜C-8**: C-1 置換7行・8出現の件数訂正／C-2 禁止事項の例外として行った本文編集（`notation:725`・`:40`、`examples:397`・`:674-677`・`:204-212`・`:502`・`:1471`）の一覧／C-3 定義を「バリデーション実行」まで広げた指示字句からの逸脱／C-4 出典逸脱の記録（`input/…-examples-table.md:50`・`同-special.md:49` が誤り、`ntf-testdata-doc.md:252/535/549` が正。根拠は `input/testdata-converter-design.md:110-112` の QuotationTrimmer/SnakeYAML の適用順）。**【誤読の罠。再導出しないこと】`testdata_notation.rst:1358-1362`（`文字列の null` → `"null"` で表現可）と `:1409-1414`（`文字列の null` → `該当なし`）は矛盾ではない。前者は `:1344` `Excel形式の場合`、後者は `:1395` `YAML形式の場合` の配下で、ページは形式差を意図して書き分けている（`checks/task-09-recordtype.md:31` に `#9` 時点で「唯一の挙動差」として記録済み）。2026-08-07、この2つを並べて「同一ページ内の自己矛盾」と誤って報告し、ユーザーにエスカレーションしたうえで撤回した。本文の修正は不要**／C-5 C-4 を残り32ページへの申し送りに追加／C-6 ゲート17 の分類基準明記（厳密に0件は 文字列の`null`・空文字・`${文字種,文字数}`・改行文字の4種）／C-7 `input-0087`・`input-0089` を検討のうえ除外した旨／C-8 アンダーライン流儀の差（notation の L3/L4 は49固定、examples は `max(50,表示幅)`。`6ba0d2a` 以前からで退行ではない）。`_build/` はユーザーがブラウザで直接レビューするため削除しない。Docker ビルドは `ja/locales/ja/LC_MESSAGES/sphinx.mo` を再生成するため commit 前に `git checkout` で戻す。`#11` 以降への申し送りは `reviews/page-testdata_examples.md`・`page-testdata_notation.md` の各末尾。
