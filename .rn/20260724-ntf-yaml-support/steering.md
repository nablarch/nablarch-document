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

**#9 = テストデータの書き方**（`implementation/testdata_notation.rst`）。役割は「記法の仕様。どう書けばどう解釈
されるか」（design.md §4）。対象 `mapping_id` は `dest_page=テストデータの書き方` の140行（機能概要1・使用方法139。
主要出典 `input/ntf-testdata-doc.md`49行のほか、現行解説書`06_TestFWGuide/`・`05_UnitTestGuide/`各所、
`input/ntf-doc-terms.md`・`ntf-testdata-doc-examples-testshots.md`・`ntf-testdata-loading.md`に分散）。
**#10 = テストデータの記載例**（`implementation/testdata_examples.rst`、機能概要なしの例外ページ）が続く。

**前方参照によるスタブページ**: #8で`setup/junit5_extension.rst`・`tools/testdata_converter.rst`を見出しのみで作成し、`setup/index.rst`・`tools/index.rst`のtoctreeに追記済み（undefined label警告解消のため。2026-08-05）。該当ページのタスクが来たら、新規作成ではなく既存ファイルへの追記として扱う。同様に他ページからの前方参照でundefined label警告が出た場合も、対象ページの見出しのみのスタブを先行作成し対応するtoctreeに追記する運用とする（毎回の警告差分確認の手間を減らすため）。#9の作業で同じ理由により`implementation/testdata_examples.rst`（`#10`用）を見出しのみで先行作成し`implementation/index.rst`のtoctreeに追記済み。

**#9の進捗（2026-08-06）**: 2026-08-05時点でDocker確認まで完了・`must`10件解消・`note`2件記録のみ・`decide`3件（A-3・B-F01・D-4）がuser review待ちだった。2026-08-06、user reviewで**差し戻し**。A-3・B-F01は実物確認で決着、D-4は`#9`に同梱と判断、加えて観点Aの網羅性欠落1件（`requestParams`/`responseResult`/`searchResult`）を検出。是正指示は`ntf-doc-09-fix.md`（STEP 1〜7）。詳細は`reviews/page-testdata_notation.md`・`checks/task-09.md`参照。**user review未了**。
2026-08-06、STEP1〜7是正提示に対し`/rn:gm`フィードバック（各ページ先頭への目次追加）を受け、`.. contents::` を追記（`style.md` S-09）。
2026-08-06、続けて`/rn:gm`フィードバック「Excelの例はRSTの表形式にしませんか？」を受領。出典（`input/ntf-testdata-doc.md:356-365`「各セルを`|`で区切って表示」）由来のExcelセル格子を`code-block:: text`で模していた2箇所（`SETUP_TABLE`例・`SETUP_FIXED`例）を`.. list-table::`（`:header-rows: 0`）に置換。ディレクトリ構成・概念階層のASCII図（3箇所）とディレクティブのみの空ファイル例（1箇所）はExcelセル格子ではないため対象外と判断。
2026-08-06、さらに`/rn:gm`フィードバック3点を受領し対応。(1) 識別子行（`SETUP_TABLE=テーブル名`・`SETUP_FIXED[グループID]=ファイルパス`）のcolspan化はdocutils 0.15.2でlist-table非対応・grid tableは全角文字幅計算が壊れやすくS-07が禁止のため、表から出して直前の地の文に移す案を採用。(2) 該当識別子はコード書式（`` `` ``）を外し普通の文字にした。(3)「Excel向け/YAML向けの説明ブロックが分かりにくい」への対応として、この2セクションに限り**Excel形式**\ ・\ **YAML形式**の太字ラベルを導入（他のExcel/YAML対比セクションは短い比較表1つ+YAMLコード例1つの構成で紛れがないため対象外、と判断した理由は報告で説明）。RST太字とCJK文字の境界で`Inline strong start-string`警告が出たため`**...**\ `（閉じ`**`直後に`\ `）で解消。Dockerフルビルドで警告1件（既知）のみ確認。
2026-08-06、ユーザーから「ファイル構成と記述時の注意点を確認する節にExcel/YAML区切りがなく分かりにくい」と指摘（前回対応の見落とし: 太字ラベルは複数ブロックにまたがる長いExcel/YAML説明の区切りとしては機能しなかった）。「ファイル構成と記述時の注意点を確認する」節と「ファイルのデータを記述する」節（SETUP_FIXED例を含む）の2箇所を、太字ラベルからL4見出し「Excel形式の場合」「YAML形式の場合」に格上げ。
2026-08-06、続けて2点の追加指摘を受領。(1)「太字/見出しの使い分けがセクションごとに違って混乱する」→太字とL4見出しの併用方針をやめ、L4見出し1本に統一する方向へ転換。(2)「読者はExcel/YAMLどちらか一方しか見ない。今の比較表構成に違和感がある」→「比較して伝える価値がある内容だけ共通、それ以外はExcel専用/YAML専用に分ける」という原則（`style.md` S-10規約1）を新設し、`testdata_notation.rst`の使用方法セクション全体（8箇所のL3セクション）を対象に比較表・比較文をExcel専用/YAML専用のL4見出し（またはL4見出しを追加できない箇所は例外的に太字1文）に分割。1セクションに見出し対が2組できていた「テーブルのデータを記述する」節は1組に統合。`style.md` S-10を規約1〜4で全面改訂。`testdata_notation.rst`全体を通し読みし、矛盾・重複がないことを確認済み。Dockerフルビルドで警告1件（既知）のみ確認。
2026-08-06、続けて`/rn:gm`フィードバック7点を受領し対応。(1)「書き方」の各L3セクション・各形式（Excel/YAML）の説明の直後に`テストデータの記載例`へのリンクを追加（従来はL3セクション末尾6箇所のみだった。Excel/YAML形式に分かれる8セクション×2形式=16箇所を新規追加、既存6箇所は維持）。(2)`#10`（テストデータの記載例、未着手）の実例水準について、Toy/サンプルレベルでなく実開発で参考にできる具体的かつ十分な分量の例にする方針を確認し、design.md「テストデータの2ページ」節に明記（`#10`着手時に適用）。(3)「〜を確認する」形式の見出し2箇所を目的志向の動詞に変更（「ファイル構成と記述時の注意点を確認する」→「テストデータを配置する」、「データブロックの種別を確認する」→「データブロックを定義する」）。(4)ファイル配置・命名の記述を「規約がある/推奨されており/読み込める（結果）」という他人事の書き方から、「推奨する。〜のためである」という解説書としての直接的・意図ベースの書き方に修正。(5)Excelのセル書式を文字列に統一する理由（数値・日付書式では`0001`が`1`になる等の自動変換により正しく読み取れなくなる）をimportantボックスに追記。(6)「ファイルが存在しない場合はエラーになる」等の自明なエラー動作の記述を削除し、非自明な挙動（空シート/空ファイルの扱い）のみ残した（整合性のためYAML側の対応する記述も同様に整理）。(7)「セルは必ず文字列書式で記述する」の重複記載を解消。全修正後、ページ全体を通し読みして整合性を確認済み。Dockerフルビルド（クリーン）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ、新規警告0件）を確認。
2026-08-06、続けて`/rn:gm`フィードバック9点を受領し対応。(1)YAML検証の説明から`YamlLoader`・`YamlSchemaValidationException`の内部クラス名を削除し「パース時にこのスキーマでの検証が行われ、〜エラーになる」に簡略化（JSON Schemaの同梱パスは実用情報のため維持）。(2)(3)「空シートは存在しないシート扱い」「空ファイル(0バイト)は空データ扱い」（Excel/YAML双方）を低価値な自明情報と判断し削除、また「値は必ずダブルクォートで囲む」はL1253以降で理由付き詳説済みのため冒頭の重複記載を削除。(4)「1つの読み込み単位に3用途のデータがデータブロック単位で共存する」という説明（従来はYAML形式サブセクション内に埋没）を「データブロックを定義する」節冒頭へ移動し、見出しを「データブロック（テストケース、準備データ、期待値）を定義する」に改称（section titleから辿れるようにする指摘への対応）。(5)マスタデータ投入ツール・マスタデータ復旧機能を`:ref:`リンク化。前方参照スタブ`tools/master_data_tool.rst`・`setup/master_data_restore.rst`を新規作成し対応するtoctreeに追記（#8で確立したパターンに従う）。マッピング`current-0365`の出典（削除前`08_TestTools/02_MasterDataSetup/index.rst:4-21`）を確認し、blank_project構築時はgsp-dba-maven-plugin（既存ラベル`:ref:`gsp-maven-plugin``）をマスタデータ投入ツールより優先する旨を追記（design.md#6の「両ツールとも非推奨の記録は無い」という確認結果と矛盾しないよう、全面非推奨ではなくblank_project時の優先順位という限定的な表現にした）。(6)データタイプ混在時の「まとめて記述する」importantボックスに、削除前`06_TestFWGuide/01_Abstract.rst:627-664`（`current-0177`出典）のNG/OK例（`EXPECTED_TABLE`/`EXPECTED_COMPLETE_TABLE`交互記述でTABLE3以降が検出されない例）を移植し、グループID版のNG/OK例（`case_001`グループの`EMPLOYEE`/`DEPT`分割が`case_002`を挟むと後半が読まれない例）を新規作成して追加。(7)「従業員の所属変更/氏名変更」の中途半端な具体例list-tableを削除し、既存の「実際の記述例は`テストデータの記載例`を参照」リンクに一本化。(8)(9)「グループID省略時のデフォルトグループ挙動」と「収集方式（単一/グループ）の表」は、従来Excel/YAML見出し対の後に配置されておりYAML固有の内容に見えていたが、実際は形式非依存の共通内容のため、Excel/YAML見出し対より前の共通イントロへ移動（`style.md` S-10規約1の趣旨に沿う配置）。全修正後、ページ全体を通し読みして整合性を確認済み。新設見出しのアンダーライン不足（東アジア文字幅換算で60必要なところ49しかなかった）をDockerビルドの警告で検出し是正。Dockerフルビルド（クリーン）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ、新規警告0件）を確認。
2026-08-06、続けて`/rn:gm`フィードバック12点（「テーブルのデータを記述する」節が対象）を受領し対応。着手前に`/home/tie303177/work/nablarch/`配下の実ソース（`nablarch-testing`・`nablarch-testing-yaml`）を`Read`し、記述の正誤を実装で裏付けた。(1)冒頭文が`LIST_MAP`を`SETUP_TABLE`等と同列の「テーブルデータ」と呼んでいた誤りを訂正。`LIST_MAP`はDBテーブルに対応せずメモリ上の`List<Map>`である旨に書き換え、詳細は`LIST_MAPのデータを記述する`への forward link とした。(2)ヘッダ末尾空カラム除去・データ行不足時の空文字補完の具体例が無いとの指摘を受け実装を確認したところ、この挙動は`HeaderLine.java`（`nablarch-testing`側、Excel専用）由来であり、従来YAML形式の下に誤って記載されていたことが判明（実際のYAML実装`YamlTableDataBuilder.java`は列名を先頭行のキーで決定し、後続行の欠落キーは空文字ではなく`null`になる）。Excel側に具体例（list-table）を追加して移設し、YAML側は正しい挙動（欠落キー→`null`、先頭行にないキーは無視）に書き換えた。実装との不一致を機械的にではなく着手前のRead経由で発見した事例。(3)`SETUP_TABLE=EMPLOYEE`/`DEPT`+`LIST_MAP=expected`の中途半端な具体例を、#9既存の precedent（従業員の所属変更/氏名変更の削除）と同じ理由で削除。(4)`setUpDb`の説明を独立したL4見出し「共通の準備データをまとめる」に格上げしYAMLサブセクション直下から分離。(5)主キー自動採番時の対処を具体化: 業務キーの複合主キー化に加え、設計変更不可の場合の代替として`LIST_MAP`（`expectedSearch`）による検索結果比較を明記。(6)「テーブルのデータを記述する」節に新設L4見出し「共通の準備データをまとめる」「準備データ（SETUP_TABLE）を記述する」「期待値（EXPECTED_TABLE等）を記述する」を追加し子見出し構成を整理。(7)DATE既定値のJVMタイムゾーン依存とExcel形式の`EXPECTED_TABLE`/`EXPECTED_COMPLETE_TABLE`混在制約が1つのimportantに混在していた件、混在制約は既存の「グループIDでデータブロックを分ける」節のNG/OK例と全く重複していたため削除（`EXPECTED_TABLE`/`EXPECTED_COMPLETE_TABLE`を使ったNG/OK例そのものが既にそこにある）、importantはDATEタイムゾーン依存のみに整理。(8)`SqlPStatement`型制約はExcel専用と確認し「Excel形式の場合」見出し配下へ移設。(9)グループIDでの紐付け文は「グループIDでデータブロックを分ける」節と完全重複のため削除。(10)RESTfulウェブサービスの記述は`mapping.csv`の`current-0120`行を確認したところ`dest_page`が「リクエスト単体テスト（RESTfulウェブサービス）」であり本ページへのマッピング違反だったため削除（当該ページのタスクで反映される。マッピング自体は変更していない）。(11)「利用者が呼び出す入口のAPI（TestDataParser）」の文にメソッド名`getExpectedTableData`を明記し、ファイルデータ節の対になる`getSetupFile`の文（L984付近、既存）と表現を揃えた。(12)Excel/YAML説明ごとに`テストデータの記載例`該当箇所への個別スクロールリンクを求める指摘は、`#10`（テストデータの記載例）がまだ見出しのみのスタブで個別アンカーが存在しないため、本ラウンドでは対応を見送り、`#10`着手時に個別アンカーへ張り替える宿題として引き継ぐ判断とした（ユーザーへの提示時に説明）。全修正後ページ全体を通し読みし整合性を確認。Dockerフルビルド（クリーン、`rm -rf _build`後再実行）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ、新規警告0件）を確認。
2026-08-06、上記(12)の見送りに対し、ユーザーから「見出しだけ作成してリンクを通そう」と指示を受け対応。`testdata_examples.rst`に見出し（本文なしのスキャフォルド）を作成し、`testdata_notation.rst`の20箇所の`実際の記述例は...を参照`を、対応する見出しへの個別`:ref:`に張り替えた（テストデータを配置するEcel/YAML2箇所は、ディレクトリ配置の話でデータ内容の実例を持たないためリンクを削除。ページ先頭の1箇所は総論のためページ全体を指す既存リンクのまま維持）。当初は「使用方法」1セクションの下に各カテゴリを「〜の記載例」という見出しで束ねる案（design.md L271の確定済み方針に追記）で作成したが、ユーザーから「記載例のセクションが並ぶだけのページに『使用方法』は合わない」「『〜の記載例』は要らない」「テストデータの書き方ページの使用方法の見出しと合わせられないか」と指摘を受け撤回。見出し文言を`testdata_notation.rst`のL3見出しと完全一致させ（例:「テーブルのデータを記述する」）、「使用方法」ラッパーを外してページ直下のL2として並べる構成に変更した（データ内容の実例を持たない「テストデータを配置する」は見出し自体を設けない）。design.mdの該当節（8. トンマナ→テストデータの2ページ節）をこの経緯に沿って書き換えた。あわせて、ユーザーから「対症療法・局所対応になっていないか、常に横並びチェックをしているか」という確認を受け、`nablarch-testing`/`nablarch-testing-yaml`の実ソースを追加で確認する横並びチェックを行い、2件を発見・修正した。(a)見出し「データブロックを定義する」が本文・他の全L3見出しの「〜を記述する」と語が不統一だったため「データブロックを記述する」に統一（`params`/電文本体を記述する2文の「定義する」も同様に統一。カスタムデータ型・フォーマットの定義を指す2文は意味が異なるため維持）。(b)ファイルデータ節の「可変長ファイルの空エントリ（先頭フィールドが空の行）」の記述が、Excel固有の判定ロジック（`DataFileParser.isDataRow`）由来の表現をYAMLにも通用する共通事実として書いていた不正確さを検出し、共通の空文字補完（`DataFileFragment.addValue`、Excel/YAML共有）とExcel/YAML双方のトリガー方法（Excel: 先頭セル空、YAML: `rows:`に`[]`）を書き分けて訂正。Dockerフルビルド（クリーン）で`build succeeded, 1 warning`（既知のみ、新規警告0件）を確認。
2026-08-06、`/rn:gm`「ここまでのFBを踏まえてページ全体を見直し、意味のある改善をする」指示を受け、著者自身による通し読みを実施（ラウンド3）。3点発見・対応。詳細は`reviews/page-testdata_notation.md`「ラウンド3」参照。
2026-08-06、再構成指示`ntf-doc-09-restructure.md`（STEP A〜G）を受領。L2「テストデータの構造」新設・各L3の「共通→形式別」統一・未解消の`must`2件/`note`1件・`style.md`の規約不整合（S-03とS-10の衝突、S-11新設）の解消。詳細は`checks/task-09-restructure.md`・`reviews/page-testdata_notation.md`「ラウンド4」参照。**user review未了**。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
- [ ] マッピングにない内容を追加しない。マッピングにある内容を落とさない
- [ ] 出典の文面をそのまま流用しない。`style.md` に従って書き直す
- [ ] `design.md` 等の内部設計文書の言い回しをそのまま転記しない。既存の解説書に同種の表現があるか `grep` で確認してから書く（Rules参照）
- [ ] 用語は `glossary.md` の正表記を使う
- [ ] L2セクション（`-`の下線）を1つ以上持つページは、タイトル下線の直後に `.. contents:: 目次`（`:depth: 3` `:local:`）を置く。`toctree`のみのインデックスページには置かない（`style.md` S-09）
- [ ] Excel形式/YAML形式の書き分けは `style.md` S-10 に従う（比較して伝える価値がある内容だけ共通の地の文・比較表にする／それ以外の「記述方法」の説明はExcel専用/YAML専用に分け、L3セクションにつき1組のL4見出し「Excel形式の場合」「YAML形式の場合」でまとめる／太字ラベルは見出しを追加できない場合の例外としてのみ使う／識別子行は表の外に地の文で普通の文字で書く）
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
- **Date**: -
- **Last completed**: -
- **Next**: -
- **Notes**: -
