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
- **ビルド確認は自分でDockerを使って行う。**`make html`の確認をユーザーに丸投げしない。ローカルvenv（`/home/tie303177/venv`）が`requirements.txt`のピン留め版と非互換（Python 3.12・`javasphinx`未対応）であることは、Docker実行を省略してよい理由にはならない。README「環境構築」＞「Docker」の手順（`docker build -t nablarch-document-build .`、`docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"`）に従い、コンテナ内で実行する。2026-08-03、同一の確認を2回ユーザー自身にやらせてしまい指摘を受けた
- **日本語の地の文（段落）は、途中で改行しない。1段落は1行で書く（文の区切りであっても改行しない）。** RSTの段落はソース上の改行をHTML出力時にも生の`\n`として残し、ブラウザは`white-space: normal`のもとでこれを半角スペース1個として描画するため、ソースを折り返すと本文に不要な隙間が入る（2026-08-03、`testing_framework/index.rst`で実測・`build succeeded`のHTMLソースで`\n`の残存を確認して特定）。`about/index.rst`にも同種の改行が複数箇所残っている（8〜9行目・12〜13行目等、`#8`のuser review未了分として要修正）。ページ作成・レビュー時は、段落内に改行がないか（空行を挟まず日本語の行が連続する箇所がないか）を確認する
- **文章表現は、design.md等の内部設計文書の言い回しをそのまま使わない。既存の解説書（FW解説書ライブラリ等）に同種の表現があるか`grep`で確認してから書く。** design.mdは開発チーム内部の設計文書であり、その文体（例:「読者は2種類に分かれる」のように読者を外側から分析する言い回し）を利用者向けページにそのまま持ち込むと、実際の解説書のどこにも使われていない不自然な文になる（2026-08-03、`testing_framework/index.rst`で`grep -rn "対象読者|読者は"`が0件だったことで実際に確認）。design.mdの内容（意図・構造）を参照するのは良いが、文言をそのまま転記しない
- **`=`のみで罫線を引く簡易tableのセル文字列を編集するときは、列位置を「表示幅」（全角文字は2、半角文字は1）で揃える。文字数（Pythonの`len()`等）で揃えない。** 見出し行の`=`の並びが表示幅基準の列境界を表しており、セル文字列の表示幅がずれると`sphinx-build`が`Malformed table`エラーを出す（2026-08-03、`about/index.rst`の表でセル文字列を短くした際に文字数基準で詰めて実際に発生・`unicodedata.east_asian_width`で是正）。編集後は必ずDockerビルドで確認する
- **各ページのセクション・小見出しの並び順は、「元資料（現行解説書・input資料・マッピングの行順）の構成」ではなく「そのページに来た読者が最初に欲しい答えは何か」を起点に組み立て直す。** マッピングは「何を書くか（事実・表・図）」の典拠として使い、「どの順で書くか」はページごとに読者の問いから毎回考える。ただし第2部・第3部の大見出し順（機能概要→使用方法→拡張例等）は`style.md` S-02で既に確定・FW解説書で裏付け済みのテンプレートであり、これを崩す原則ではない。この原則が主に効くのは、テンプレートが無い第1部の節順（2026-08-05、design.md §2で「テストの種類」をアーキテクチャより前に並べ替えた判断が最初の適用例）と、各節内の小見出し・項目の並び順
- **design.mdが特定のページを「〜の構成に倣う」と指定している場合、そのページを実際に開いて構成（見出しの分け方・`:ref:`の使い方・文の続け方）を確認してから設計する。「倣う」対象の話題や見出し名だけを真似て、実際のファイルを読まずに構成を推測しない。** `#8`のフィードバック2ラウンド目で、design.mdが「FW解説書の`Nablarchアプリケーションフレームワークとは`の構成に倣う」と明記していたにもかかわらず、実際に`nablarch/big_picture.rst`を読まないまま「全体像」「特徴」を別見出しに分け`:ref:`で行き来させる独自構成を作ってしまい、ユーザー指摘で発覚した（2026-08-05）。実際のファイルは「全体像」と「特長」を1つの節にまとめ、「Xができる」という提示に具体的なメリットを同じ場所で続ける一体の構成だった。「倣う」という指示がある箇所では、着手前に必ず参照先ファイルを`Read`する
- **複数点のフィードバックに対応するときは、各指摘を個別に直す対症療法で終えず、直した結果のページを上から通しで読み直し、指摘されていない箇所も含めて整合性（前後の重複、矛盾、行き来するだけのリンク、浮いた記述）を確認してから報告する。** `#8`のフィードバック1ラウンド目は、6点の指摘それぞれには機械的に対応したが、その結果生じた新たな不整合（「特徴」から直前に読んだばかりの「全体像」へ戻る`:ref:`等）に気づかず、2ラウンド目で「品質が低すぎて指摘だらけ、なぜ？」という指摘を受けた（2026-08-05）。個別修正がすべて完了した後、必ず通し読みの確認ステップを独立して行う
- **タスクが完全に閉じたら（全Steps完了・レビュー通過・user review承認済み）、次のタスクに進む前にそのタスクのエントリを圧縮する。** 見出しに`— DONE`を付し、Steps・差し戻し経緯・narrativeを削り、Purpose（1行）とCompletion criteriaのみ残して`checks/task-XX.md`と最終コミットへのポインタを添える。rnプラグイン自身の設計方針（`steering.md`は「lean forward contract」であり、履歴はgit + PRに置きsteering.mdには残さない）に基づく。#8以降34ページのページ作成タスクで積み上がるのを防ぐため、圧縮を都度行い最後にまとめてやらない（2026-08-05、`#1`〜`#7`をこの方針で圧縮・steering.mdを720行→約260行に縮小）

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

### #8: 第1部「テスティングフレームワークとは」の作成（`about/index.rst`）

**Purpose**: マッピングに従って第1部（概念、1ページ）を作成する。design.md 11.5「最初の1ページで基準を作る」の対象タスク。

**Prerequisites**: #7

**ページID**: `about_index`（`reviews/page-about_index.md` / `checks/task-08.md` を使う）

対象 `mapping_id`（`dest_page=テスティングフレームワークとは`、11行、`DROP`なし。2026-08-05 #8フィードバック対応で
`input-0002`/`input-0116`（データブロックの記法仕様、計49行）を第3部「テストデータの書き方」へ再割当したため
13行→11行。詳細は本タスクStepsの当該項目・`design.md`§2「テストデータ」節・`mapping.csv`を参照）:
`current-0162`, `current-0163`, `current-0164`, `current-0166`, `current-0175`, `current-0176`,
`current-0180`, `current-0267`, `current-0377`, `current-0165`, `input-0028`

出典（削除済みのため base commit `c24190607fef5d76c607aa08b36d2ab2f813efe5` から `git show` で取得）:
`.../06_TestFWGuide/01_Abstract.rst`, `.../06_TestFWGuide/JUnit5_Extension.rst`,
`ja/development_tools/testing_framework/index.rst`（すべて base commit 時点）、
`input/ntf-doc-terms.md`, `input/ntf-testdata-doc.md`（作業ツリーから）

**Steps**:

- [x] `ja/development_tools/testing_framework/index.rst`（トップレベル、toctree・読者振り分け文。design.md §1）と
      `ja/development_tools/testing_framework/about/index.rst` の骨格を新規作成する（`#7` で全 `.rst` を削除済みのため）
- [x] `ja/development_tools/index.rst` の `testing_framework/index` toctree 参照は変更しない（既存のまま有効にする）
- [x] `mapping.csv` から上記 `mapping_id` の行を抽出する
- [x] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`、current側は base commit から `git show` で取得）を実際に読み、ページを作成する
- [x] セクション構成は design.md §2 の6セクション（全体像 / アーキテクチャ / テストの種類 / テストデータ / 対象範囲 / 稼動環境）に従う
- [x] マッピングにない内容を追加しない。マッピングにある内容を落とさない（観点Aラウンド3でPASS確認済み）
- [x] 出典の文面をそのまま流用しない。`style.md` に従って書き直す（`#8`差し戻し対応で是正後の基準により再レビューし、must指摘はすべて解消。旧R3-B1/B2/B3のうちR3-B2/B3相当の2箇所は、新基準の機械適用でも再度must判定されたが、ユーザーがA-5で既に「対応不要」と判定済みのためユーザー判定を優先し原文を維持。詳細は`reviews/page-about_index.md`参照）
- [x] 用語は `glossary.md` の正表記を使う（`#8`差し戻し対応A-2で「同期応答電文」→「同期応答メッセージ送信」に修正。`reviews/page-about_index.md` R3-C1解消）
- [x] 該当する `note` の `[セクション境界]` はない（対象13行を確認済み）。`reference-only sections` も本ページには該当しない
- [x] 外部被参照ラベルの引継ぎは本ページには該当しない（対象は `implementation/request_unit_test/web.rst` の1件のみ）
- [x] 4観点のレビューを、それぞれ**別のサブエージェント**で実施する（A:網羅性 / B:トンマナ / C:用語 / D:整合性）
  - **プロンプトは Rules「レビューを依頼するサブエージェント…」の3点を必ず含める**
- [x] 指摘への対応を行う（最大3ラウンド。3ラウンド実施済み。未解決5件は design.md 11.7 に従い記録の上ユーザーレビューへ）
- [x] レビュー記録を `reviews/page-about_index.md` に作成する
- [x] self-check（`checks/task-08.md`）
- [x] commit & push
- [x] decide案件1件（「対象範囲」節の処理方式一覧の要否）への回答（`ntf-doc-08-decide.md`、`/rn:gm`）を反映。
      選択肢2を採用し`design.md`§2を改訂、`about/index.rst`の`リクエスト単体テスト（テーブルをキューとして
      使ったメッセージング）`行を復元（`#8` A-3の判断を覆した）。`design.md`§8/§11.7に確定設計優先の規約を
      追加。新基準で再レビュー（ラウンドリセット）しmust 1件検出・解消、残存0件。コミット`710a1af`・`36deb4b`
      でcommit・push済み。詳細は`reviews/page-about_index.md`・`checks/task-08.md`参照
- [x] フィードバック対応（トップレベル `index.rst` の4部構成を箇条書きからtoctreeへ）を反映。
      `design.md`§13に第2部/第3部/第4部それぞれの表題ページ（`setup/index.rst` /
      `implementation/index.rst` / `tools/index.rst`、導線のみ・1対1対応表には含めない）を追加し、
      最上位`index.rst`の箇条書きを`toctree`（`about/index` / `setup/index` / `implementation/index` /
      `tools/index`の4件）に置き換えた（`ja/development_tools/index.rst`の二段toctree構成に倣う）。
      表題ページは現時点で見出しのみ（配下ページ未作成のため）。`#9〜`のSteps末尾に「作成したページを
      対応する表題ページのtoctreeに追記する」を追加した
- [x] フィードバック対応（トップレベル `index.rst` の読者振り分け文の順序・文面・改行）を反映。順序を
      「概要 → toctree → 読者振り分け文」に是正し、文面を指示文（「〜は…を参照する」）から意図と読み方を
      伝える文に書き直した。加えて、段落内改行がHTML出力時に半角スペースとして残ることを実測で特定し
      （ビルド後のHTMLソースに生の`\n`が残ることを確認）、段落を1行で書く形に修正。Rules に
      「日本語の地の文は段落内で改行しない」を追加した。`about/index.rst` に同種の改行が複数箇所
      （8〜9行目・12〜13行目等）残っていることを確認済みだが、本ページの`user review`で方針を確認してから
      対応する
- [x] フィードバック対応（第2部/第3部/第4部の表題ページのタイトルを検索性重視の名前に変更）を反映。
      「導入と設定」→「テスティングフレームワークの導入と設定」、「テストの実装方法」→
      「テスティングフレームワークによるテスト実装」、「ツール」→「テスティングフレームワークの提供ツール」
      に変更（単独で見ても何のページか分かるようにするため）。最上位`index.rst`本文のページ名言及を
      タイトル文字列の直接引用から`:doc:`参照に変更し、タイトル変更時の追随漏れを防止。`design.md`§13に
      表題ページのタイトル方針として記録した
- [x] フィードバック対応（「読者は2種類に分かれる」の文言を修正）を反映。design.md§1の内部設計文書としての
      言い回し（読者を外側から分類する書き方）を利用者向けページにそのまま転記していたことが原因。
      `grep -rn "対象読者|読者は" ja/`が既存解説書内で0件（このページの追記分を除く）であることを確認し、
      「読者は」を使わず、内容の構造について直接書く文に書き直した。Rulesに「design.md等の内部設計文書の
      言い回しをそのまま転記しない。既存の解説書に同種の表現があるかgrepで確認してから書く」を追加し、
      `#9〜`のStepsにも同項目を追加した
- [x] 今回のフィードバックセッションで判明したルール（段落内で改行しない）を `about/index.rst` にも適用。
      全19箇所の段落内改行（文末での改行11件、文の途中での改行8件。最悪例は「前のテストが更新した／
      データベースの内容が」のように複合語の途中で割れていた箇所）を、文言・意味を一切変えずに1行へ結合。
      置換前後で完全一致する文字列であることをPythonスクリプトで検証（各19箇所とも一致件数1件を確認して
      から置換）、Dockerビルドで`build succeeded`・警告0件、レンダリング後のHTMLに段落内`\n`が0件である
      ことを確認済み。`git diff`は改行の削除のみで文言変更なし。他の観点（design.md内部言い回しの転記等）
      は該当箇所なしと確認した
- [x] フィードバック対応（用語「テストデータファイル」「テストソースコード」の見直し）を反映。一律置換はせず
      根拠を確認して個別判断した。「テストソースコード」→「テストコード」は全6箇所を変更（`input/
      ntf-testdata-doc.md:24`が実際に「テストコード」を使っており、`#8`作成時の造語だったため）。
      「テストデータファイルへの外部化」→「テストデータの外部化」は見出し1箇所のみ変更（旧解説書の実際の
      見出しそのもの、`term-candidates.csv:107`・`06_TestFWGuide/01_Abstract.rst:21`で確認）。残り6箇所は
      `glossary.md`§5.9が「テストデータファイル」をExcel/YAML両対応の正式採用語と定めており、かつ
      「別のテストデータに記載できる」のように置換すると循環した文になる箇所があるため維持。1箇所
      （旧98行目）のみ「テストデータファイル」の重複を避けるため「ファイル」に短縮（意味は変えず）。
      Dockerビルドで`build succeeded`・警告0件を確認
- [x] ユーザーからの再指摘（「テストデータで不都合あるの？」）を受けて上記6箇所を再検討。「維持」判断が
      過剰に保守的だった3箇所（見るだけで把握できる／側に切り出せる／への追記で済む、のように動詞が
      「どこに」を要求しない箇所）は「テストデータ」に簡略化。「外部化する」「（両方に）散らばる」
      「集約する」のように動詞が行き先を要求し、かつ行き先の名詞が主語と同じ「テストデータ」になると
      循環文になる2箇所は維持理由を明確化した上で維持。表の1箇所（構成物一覧、隣接行との体裁統一という
      弱い理由のみ）は判断が割れるためユーザー確認待ちのまま維持。Dockerビルドで`build succeeded`・
      警告0件を確認
- [x] ユーザーからの再指摘（「テストクラス」等は「〜ファイル」にしていない、テストデータは概念、本ページ
      自体が概念を説明するページ）を受け、残り3箇所も「テストデータ」に統一。表の行は「として」構文
      （「テストデータとして外部化」「マスタデータを...テストデータとしてまとめて外部化」）で循環を回避し、
      「テストデータファイル」を本ページから完全に排除（`grep`で0件を確認）。表の列の置換時、日本語の
      表示幅（全角2・半角1）で列位置を揃える必要があることに気づかず文字数基準で詰めてしまい、
      `sphinx-build`で`Malformed table`エラー（`ERROR`だが集計上は`1 warning`）を検出→
      `unicodedata.east_asian_width`で表示幅を再計算し是正、`build succeeded`・警告0件に復帰したことを
      確認した
- [x] フィードバック対応（トップレベル `index.rst` の読者振り分け文を素直な文章に書き直す）を反映。理由づけの
      複文（「〜としてまとめているため、まずこのページを読めば、以降は…」）を、役割ごとに1文で書く短文3つに
      分解し、語尾をFW解説書ライブラリの慣用表現「〜を参照すること。」に合わせた（コミット `e56a578`）。
      あわせてユーザーから確認のあった3点に回答: (1) Jakarta Batch未対応は `about/index.rst`「対象範囲」節
      143行目（`current-0377`が出典、design.md§2の対象範囲定義に対応）に記載済み。(2) マルチスレッド機能の
      テストは同節147行目（同じく`current-0377`が出典）に記載済み。マスタデータ投入ツール自体の
      マルチスレッド非対応は別途第4部「ツール」の該当ページ（`current-0365`/`current-0354`）で扱う。
      (3) `#8`のスコープとマッピングは観点A（網羅性）ラウンド3で「13行全件OK、未解決指摘なし」とPASS済み
      （`reviews/page-about_index.md`参照）。Dockerビルドで`build succeeded`・警告0件を確認
- [x] フィードバック対応（セクションの並び順・ストーリーの見直し、ユーザー提案の「特徴」節新設）を反映。
      design.md §2を改訂し、並び順を 全体像 → **特徴（新設）** → テストの種類 → アーキテクチャ →
      テストデータ → 対象範囲 → 稼動環境 に変更（旧: 全体像 → テストの種類 → アーキテクチャ → …から
      「特徴」を追加）。「特徴」に3点（本番同等の経路／テストコードは定型・少量／Excel・YAML形式を選べる）
      を要約1〜2文＋詳細セクションへの`:ref:`で追加。マッピング行の`dest_section`は変更していない
      （要約と実体が1対1対応するため。3点目は`input-0183`が出典で第4部`テストデータ変換ツール`（未作成）
      に割当済みのまま、`:ref:`先行で導線。`undefined label`警告1件は`#last`ゲートで解消する前提の
      一時的なものとして許容）。あわせて「テスト種別の正式名称」の独立見出し・「正式名称」という文言を
      撤回し、テストの種類の対比表に自然文で統合（`:ref:`ラベルは維持、`対象範囲`からの参照文言も更新）。
      Dockerビルドで`build succeeded`（最終`1 warning`＝上記の想定内`undefined label`）を確認。
      あわせてsteering.md自体の肥大化対策として`#1`〜`#7`をPurpose/Completion criteriaのみに圧縮し
      （720行→418行）、タスク完了時に同様の圧縮を行う運用ルールをRulesに追加した
- [x] フィードバック対応（6点）を反映（2026-08-05、`/rn:gm`）。
      (1) 「全体像」に「3種類のテストを提供する」という核となる事実を追加し、`:ref:`で「テストの種類」へ導線
      （新規アンカー`testing_framework_about-test_types`）。「JUnitベースであること」は「なぜ使う価値があるか」
      に答える要素として「特徴」4点目へ格上げ（「使い慣れたJUnitの書き方をそのまま活かせる」、出典は
      既存の`current-0162`/`0166`のまま、新規マッピング行なし）。
      (2) 「テスト種別の正式名称」表（内訳表）からクラス単体テスト・取引単体テストの2行を削除し6処理方式のみに
      整理（「次の6つに分かれる」という導入文との矛盾・上段対比表との重複を解消）。列見出し「テスト種別」は
      `glossary.md`の用語区分（テスト種別=3分類、処理方式=6区分）に合わせ「処理方式」に変更。
      (3) 「特徴」2点目（テストコードは定型・少量）の「テストロジック」「テストデータ」の初出に具体語
      （「テストデータのセットアップや期待値とのアサート」「データベースへの準備データや期待するテスト結果」）
      を追加。
      (4) 「アーキテクチャ」の図下にあった構成物一覧表（構成物・説明・作成者）を削除。図と導入文のみに整理
      （`current-0165`の`dest_section`は変更なし。表という表現形式を採らないだけ）。
      (5) 「テストデータ」節の「データブロックの考え方」小見出し（`input-0002`/`input-0116`、49行）を、
      記法仕様そのものであるとして第3部「テストデータの書き方」ページへ`dest_part`/`dest_page`/`dest_section`
      ごと再割当（`mapping.csv`変更、`verify_mapping.py`エラー0件を確認）。あわせて「テストデータの外部化」
      小見出しの4項目箇条書き（「特徴」2点目と重複）を削除し、外部化の事実説明のみに短縮。`volume.md`の
      dest_page別・dest_section別集計とdiff note、傾向コメントを更新。design.md §2・§4に再割当の判断根拠を追記。
      (6) 「対象範囲」を独立セクションとして廃止し、「テストの種類」節の末尾（内訳表・除外`important`2件の並び）
      に統合。自節への`:ref:`導線1文は不要になったため削除。`dest_section`は`対象範囲`のまま変更なし。
      Dockerビルド（`nablarch-document-build-sandboxed`イメージ、README「環境構築」手順）で
      `build succeeded`（最終`1 warning`＝想定内の`undefined label: testdata_converter`のみ）を確認。
- [x] フィードバック対応（構成の全面見直し）を反映（2026-08-05、`/rn:gm`）。
      前回ラウンドは出典（現行解説書の記載順・話題）に引っ張られた「既存ありき」の修正にとどまり、
      「全体像」と「特徴」を別見出しのまま残して`:ref:`で往復させる構成の欠陥（4点目が直前に読んだばかりの
      「全体像」へ戻るバックリンクになっていた等）を残していた、というユーザー指摘を受けての抜本改訂。
      design.md本節が「倣う」としているFW解説書`Nablarchアプリケーションフレームワークとは`の実際の構成
      （`ja/application_framework/application_framework/nablarch/big_picture.rst`）を確認し、「全体像」と
      「特長」が別見出しに分かれず、能力の提示（Xができる）に続けて具体的なメリットを同じ場所で言い切る
      一体の節であることを根拠に反映。
      (1) 「全体像」と「特徴」を1つのH2「全体像」に統合（「特徴」という独立見出しは廃止、各特徴はH2「全体像」
      配下のH3見出しとして並べる）。design.md §2の並び順テーブルを7行→5行に整理。
      (2) 各特徴から他セクションへの`:ref:`（アーキテクチャ・テストデータ・全体像自身へのバックリンク）を削除。
      同一ページ内で数節先に自然に登場する内容への「詳細は参照」は不要と判断（第4部という別ページへの
      `:ref:`（Excel/YAML点目）のみ残す）。
      (3) 各特徴を「Xができる」の提示だけで終えず、それによる具体的な便益まで1つの塊で書く形に書き直した
      （例:「本番同等の経路でテストできる」→「単体テストの段階から経路に起因する不具合を早期に見つけられ、
      結合テストや本番運用まで問題を持ち越さずに済む」）。
      (4) 旧「全体像」にあったJUnit4アノテーション互換性の説明・コード例・tipを、「使い慣れたJUnitの書き方を
      そのまま活かせる」特徴点の直後にその具体的な裏付けとして移動（浮いていた既存記載を特徴の実証という
      文脈に接続）。
      (5) 「テストの種類」節の冒頭文が「全体像」で既に述べた3種類の名称列挙と重複していたため簡潔化。
      マッピング行の`dest_section`はすべて変更なし（実体は元の割当のまま、要約の書き方と配置のみ変更）。
      Dockerビルドで`build succeeded`（想定内の`undefined label`警告1件のみ）を確認。
- [x] フィードバック対応（2026-08-05、`/rn:gm`）。「全体像」冒頭の直後で「特徴」1点目が「リクエスト単体テストは〜」
      と個別の種類名を主語にした説明を始めるが、その時点で読者はまだ各種類の中身を知らないため意味が
      通らない、という指摘を反映。冒頭の1〜2文に「クラス単体テストはクラス単位、リクエスト単体テストは
      1リクエスト単位、取引単体テストは複数リクエストにまたがる業務単位でテストを行う。」を追加し、
      後続の「特徴」が使う名称を先に定義した。フルの対比表（実行方法・備考含む）は「テストの種類」節に
      譲り、ここでは名称と対象粒度の対応のみ。design.md §2に判断根拠を追記。Dockerビルドで`build succeeded`
      （想定内の`undefined label`警告1件のみ）を確認。
- [ ] **user review** — 承認を受けるまで #9 に進まない

**Completion criteria**:

- `mapping.csv` の `dest_page=テスティングフレームワークとは` の全13行が反映されている
- 4観点のレビューがすべて実施・記録されている
- 未対応の指摘が残っていない、または残す判断とその理由が記録されている
- `make html` が `about/index.rst` についてエラーを出さない
- `ja/development_tools/testing_framework/index.rst` から `about/index.rst` / `setup/index.rst` /
  `implementation/index.rst` / `tools/index.rst` への toctree 導線がある

### #9〜: ページの作成（1ページにつき1タスク）

**Purpose**: マッピングに従ってページを1つ作成する。

**Prerequisites**: #8（以降は直前のページタスク）

作成順: 第3部のテストデータ2ページ → 第2部 → 第3部の残り → 第4部

タスク番号・ページIDは #8 完了後、ページごとに確定する。

**Steps（各ページ共通）**:

- [ ] `mapping.csv` から当該 `dest_page` の行を抽出する
- [ ] 抽出した行の出典（`src_file` の `src_body_start`〜`src_body_end`）を実際に読み、ページを作成する
- [ ] マッピングにない内容を追加しない。マッピングにある内容を落とさない
- [ ] 出典の文面をそのまま流用しない。`style.md` に従って書き直す
- [ ] `design.md` 等の内部設計文書の言い回しをそのまま転記しない。既存の解説書に同種の表現があるか `grep` で確認してから書く（Rules参照）
- [ ] 用語は `glossary.md` の正表記を使う
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

- **Status**: paused
- **Date**: 2026-08-05
- **Last completed**: #8 フィードバック対応・3ラウンド目（2026-08-05、`/rn:gm`）。2ラウンド目（構成の全面見直し、
  コミット `4e07294`）で「全体像」と「特徴」を1つのH2に統合した結果、「特徴」1点目が「リクエスト単体テストは〜」
  と個別の種類名を主語にした説明を始めるが、その時点で読者はまだ各種類の中身（何単位のテストか）を知らない
  という指摘を受け、「全体像」冒頭の1〜2文に3種類それぞれの対象粒度（クラス単位／1リクエスト単位／複数
  リクエストにまたがる業務単位）を一言添える改訂を実施。design.md §2に判断根拠を追記。Dockerビルド確認済み
  （`build succeeded`、想定内warning1件のみ）
- **Next**: #8 の user review 承認を待つ。承認後、#9〜（ページ作成、作成順: 第3部のテストデータ2ページ → 第2部 → 第3部の残り → 第4部）に進む
- **Notes**: ブランチ `work`、`origin`（`lovaizu` fork）へ push 済み（PR未作成）。ブロッカーなし。ユーザー未解決の指摘なし。`about/index.rst`に`undefined label: testdata_converter`警告1件が残るが、第4部作成時に解消する前提の想定内の警告（`#last`ゲートで最終確認）
