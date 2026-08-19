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
- `#22` 事前情報（取引単体テストの設定（RESTfulウェブサービス））: `.rn/20260724-ntf-yaml-support/ntf-doc-22-deal-unit-test-rest.md`
- `#23` 作業指示（テーブルデータの0件の扱い。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-23-table-zero-rows.md`
- `#24` 作業指示（唯一の指示書。ラウンド3 まで反映。旧 `ntf-doc-24-round2.md` を改名・上書き）: `.rn/20260724-ntf-yaml-support/ntf-doc-24.md`
- 章構成設計: `.rn/20260724-ntf-yaml-support/design.md`
- 現行解説書（IN側）: `ja/development_tools/testing_framework/` 配下の全 `.rst`（develop ブランチ）
- input資料（IN側）: `.rn/20260724-ntf-yaml-support/input/` 配下の全 `.md`（`design.md` を除く）
- トンマナ基準: `ja/application_framework/application_framework/libraries/` 配下の `.rst`
- 参照リポジトリ（実装で事実を確かめる先。すべて `/home/tie303177/work/nablarch/` 配下に clone 済み）。**「参照コミット」の側を根拠に使う。作業ツリーの HEAD は動くので、`git show <参照コミット>:<path>` で読む。** 実測欄は `git -C <repo> log -1 --format='%H %ad %s' --date=short` を 2026-08-16 に実行した値（`#28` §4-7）

| リポジトリ | 参照コミット（本刷新が根拠に使う） | 実測 HEAD（2026-08-16） | 備考 |
| --- | --- | --- | --- |
| `nablarch-testing` | `e21bf67`（2024-09-27 `Merge remote-tracking branch 'origin/release-6u2'`） | `fdf55d4`（2026-08-05 `chore: jacoco.exec を .gitignore に追加`、ブランチ `convert-testdata-excel-to-text`） | **HEAD は参照コミットと分岐している**（merge-base `6aa6989`、HEAD 側に14コミット・`e21bf67` 側に16コミット）。作業ツリーを直接 `grep` すると `e21bf67` と違う内容を読む |
| `nablarch-testing-yaml` | `190cc9a`（2026-08-13 `revert: rows: [] の列名 DbInfo フォールバックを差し戻す`） | `e69b69f`（2026-08-14 `docs(steering): #14 Acceptance criteria 実行結果を記録`、ブランチ `feature/ntf-yaml`） | `190cc9a` は HEAD の祖先（12コミット前進）。`#26` までのページはすべて `190cc9a` で検証済み |
| `nablarch-testing-converter` | `45194f9`（2026-08-14 `docs(coverage): レビュー指摘を台帳へ反映し、実測と食い違う数値を直す`、ブランチ `ntf-test-data-converter`） | 同左（`45194f9`） | `#27-03` 執筆中に `e80a4dd`→`2f21bce`→`45194f9` と動いた。ここでピンする |
| `nablarch-testing-rest` | `9ada31e`（2026-06-25 `chore: suspend session — fix-testdataparser-usage`、ブランチ `fix-testdataparser-usage`） | 同左（`9ada31e`） | 動きなし |

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
- **ビルド確認は自分でDockerを使って行う。**`make html`の確認をユーザーに丸投げしない。ローカルvenv（`/home/tie303177/venv`）が`requirements.txt`のピン留め版と非互換（Python 3.12・`javasphinx`未対応）であることは、Docker実行を省略してよい理由にはならない。README「環境構築」＞「Docker」の手順（`docker build -t nablarch-document-build .`、`docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"`）に従い、コンテナ内で実行する。2026-08-03、同一の確認を2回ユーザー自身にやらせてしまい指摘を受けた。**ビルドの直後に必ず `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻す。復元処理をビルドコマンドに連結する場合は、作業ディレクトリに依存しない絶対パスで `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` と書く（2026-08-14 の `#25` user review による）。** このファイルはDockerフルビルドのたびに再生成され（`.gitignore` に `locales` の記載は0件）、放置すると作業対象外の副産物がコミットに混入する。2026-08-07・08-12・08-13 の3回混入し、`73e84dc`・`f6947b2`・`c0381ed` でいずれも戻している。混入を後から見つけて戻すのではなく、再生成された時点で戻す（2026-08-13 の作業指示による）。**`locales/` を `.gitignore` に加えてはならない。** リポジトリが追跡している成果物であり、追跡から外すと他の作業者の更新が失われる
- **日本語の地の文（段落）は、途中で改行しない。1段落は1行で書く（文の区切りであっても改行しない）。** RSTの段落はソース上の改行をHTML出力時にも生の`\n`として残し、ブラウザは`white-space: normal`のもとでこれを半角スペース1個として描画するため、ソースを折り返すと本文に不要な隙間が入る（2026-08-03、`testing_framework/index.rst`で実測・`build succeeded`のHTMLソースで`\n`の残存を確認して特定）。`about/index.rst`にも同種の改行が複数箇所残っている（8〜9行目・12〜13行目等、`#8`のuser review未了分として要修正）。ページ作成・レビュー時は、段落内に改行がないか（空行を挟まず日本語の行が連続する箇所がないか）を確認する
- **文章表現は、design.md等の内部設計文書の言い回しをそのまま使わない。既存の解説書（FW解説書ライブラリ等）に同種の表現があるか`grep`で確認してから書く。** design.mdは開発チーム内部の設計文書であり、その文体（例:「読者は2種類に分かれる」のように読者を外側から分析する言い回し）を利用者向けページにそのまま持ち込むと、実際の解説書のどこにも使われていない不自然な文になる（2026-08-03、`testing_framework/index.rst`で`grep -rn "対象読者|読者は"`が0件だったことで実際に確認）。design.mdの内容（意図・構造）を参照するのは良いが、文言をそのまま転記しない
- **`=`のみで罫線を引く簡易tableのセル文字列を編集するときは、列位置を「表示幅」（全角文字は2、半角文字は1）で揃える。文字数（Pythonの`len()`等）で揃えない。** 見出し行の`=`の並びが表示幅基準の列境界を表しており、セル文字列の表示幅がずれると`sphinx-build`が`Malformed table`エラーを出す（2026-08-03、`about/index.rst`の表でセル文字列を短くした際に文字数基準で詰めて実際に発生・`unicodedata.east_asian_width`で是正）。編集後は必ずDockerビルドで確認する
- **各ページのセクション・小見出しの並び順は、「元資料（現行解説書・input資料・マッピングの行順）の構成」ではなく「そのページに来た読者が最初に欲しい答えは何か」を起点に組み立て直す。** マッピングは「何を書くか（事実・表・図）」の典拠として使い、「どの順で書くか」はページごとに読者の問いから毎回考える。ただし第2部・第3部の大見出し順（機能概要→使用方法→拡張例等）は`style.md` S-02で既に確定・FW解説書で裏付け済みのテンプレートであり、これを崩す原則ではない。この原則が主に効くのは、テンプレートが無い第1部の節順（2026-08-05、design.md §2で「テストの種類」をアーキテクチャより前に並べ替えた判断が最初の適用例）と、各節内の小見出し・項目の並び順
- **design.mdが特定のページを「〜の構成に倣う」と指定している場合、そのページを実際に開いて構成（見出しの分け方・`:ref:`の使い方・文の続け方）を確認してから設計する。「倣う」対象の話題や見出し名だけを真似て、実際のファイルを読まずに構成を推測しない。** `#8`のフィードバック2ラウンド目で、design.mdが「FW解説書の`Nablarchアプリケーションフレームワークとは`の構成に倣う」と明記していたにもかかわらず、実際に`nablarch/big_picture.rst`を読まないまま「全体像」「特徴」を別見出しに分け`:ref:`で行き来させる独自構成を作ってしまい、ユーザー指摘で発覚した（2026-08-05）。実際のファイルは「全体像」と「特長」を1つの節にまとめ、「Xができる」という提示に具体的なメリットを同じ場所で続ける一体の構成だった。「倣う」という指示がある箇所では、着手前に必ず参照先ファイルを`Read`する
- **複数点のフィードバックに対応するときは、各指摘を個別に直す対症療法で終えず、直した結果のページを上から通しで読み直し、指摘されていない箇所も含めて整合性（前後の重複、矛盾、行き来するだけのリンク、浮いた記述）を確認してから報告する。** `#8`のフィードバック1ラウンド目は、6点の指摘それぞれには機械的に対応したが、その結果生じた新たな不整合（「特徴」から直前に読んだばかりの「全体像」へ戻る`:ref:`等）に気づかず、2ラウンド目で「品質が低すぎて指摘だらけ、なぜ？」という指摘を受けた（2026-08-05）。個別修正がすべて完了した後、必ず通し読みの確認ステップを独立して行う
- **タスクが完全に閉じたら（全Steps完了・レビュー通過・user review承認済み）、次のタスクに進む前にそのタスクのエントリを圧縮する。** 見出しに`— DONE`を付し、Steps・差し戻し経緯・narrativeを削り、Purpose（1行）とCompletion criteriaのみ残して`checks/task-XX.md`と最終コミットへのポインタを添える。rnプラグイン自身の設計方針（`steering.md`は「lean forward contract」であり、履歴はgit + PRに置きsteering.mdには残さない）に基づく。#8以降34ページのページ作成タスクで積み上がるのを防ぐため、圧縮を都度行い最後にまとめてやらない（2026-08-05、`#1`〜`#7`をこの方針で圧縮・steering.mdを720行→約260行に縮小）
- **1件のフィードバック対応につき、詳細な理由づけを書く場所を1箇所に決め、他の場所は1〜2行のポインタにとどめる。** 設計判断そのもの（何を・なぜ）は`design.md`の該当節にのみ書く。レビュー監査の記録（指摘→対応の対応表）は`reviews/page-*.md`にのみ書く。`steering.md`のStepsには「Nラウンド目、M点対応。一言の要約。詳細はdesign.md§X・reviews/page-Y.md参照。commit `<hash>`」程度の1〜2行のみ記載し、同じ理由づけを全文で書き直さない。2026-08-05、`#8`のフィードバック対応が5ラウンド積み重なった結果、同じ内容を`design.md`・`reviews/page-about_index.md`・`steering.md`の3箇所にほぼ全文で重複記載してしまい、ユーザーから「文量が大量なんだけど、こんなに必要なの？」と指摘を受けたことによる（Steps 16件・約165行を1〜2行×16件に圧縮）
- **ページのタスクが`user review`承認で閉じたら、`design.md`の該当節も同様に圧縮する。** 各ラウンドの元の指摘文の引用・差し戻し経緯は削り、最終決定と一言の理由、`reviews/page-*.md`へのポインタのみ残す。34ページ分を通しで行う設計文書のため、圧縮しないとページ数に比例して際限なく肥大化する
- **`#27` のサブ項目（`#27-00`〜`#27-21`）はタスクではない。`#27` 全体が1タスクである。** サブ項目の境界で user review を待たず、次のサブ項目に着手する。上の「user review の承認を受けるまで次タスクに着手しない」はタスク単位の規則であり、サブ項目の境界には適用しない（`#27` の作業指示 `ntf-doc-weekend-queue.md` §1-1 による）。
- **`.rn/` 内の文書どうしの相互参照は、行番号ではなく節見出し（`ファイル名` §番号「見出し」）で指す。`ja/` や他リポジトリの実物を出典として示す `file:line` は対象外で、そのまま使う。** 区別の基準は「指す先が `.rn/` 内の自分たちの文書か、実物か」。`mapping/glossary.md` §5.15 が既に採っている方式にそろえる。**同名の見出しがファイル内に複数あるときは、親の節番号を添えて特定する**（`checks/task-28.md` §7「他の担当への申し送り」。この見出しは同ファイルに3つあり（`## §2`・`## §6`・`## §7` の直下）、`### 7-3.` の兄弟であるため親を書かないと定まらない。同ファイル `:876` が以前から採っている書き方。2026-08-18 の `/rn:ty` で user が追認）。2026-08-18、`checks/task-last.md` §8 から `checks/task-28.md:519` を指していたところ、同じコミットで §7-3 の表が2行伸びたため参照先が別の行に変わり、誤った案内になった（user 差し戻し）。節見出しなら加筆で動かない
- **`main` へのマージは、user の明示指示があるまで行わない。`.rn/` をマージに含めるか外すかの判断も、その指示があるまで保留する。** 2026-08-18、`#last` クローズ後に `.rn/` の扱いを確認したところ、user から「指示するまでマージしない、`.rn/` もそれまでペンディング」との判断を受けた。ブランチ `ntf-yaml-support` は push 済みのまま保持し、マージ・rebase・`.rn/` の削除や `.gitignore` 追加を先回りして行わない。

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
- [ ] **差分の範囲を確認する（`#19` 以降の共通ゲート。`commit & push` の直前に置く）** — `git status --porcelain` の**全件**を表にし、そのタスクで変更する予定だったファイル以外が0件であることを確認する。**`ja/` や特定ディレクトリに絞らない**（母集合を先に固定してから判定する。`03-検証スクリプト.md` と同じ趣旨）。**母集合は `git status --porcelain` とする。`git diff` は未追跡ファイルを出さないため、新規に置かれた予定外のファイルを取りこぼす。** 2026-08-13、`#18` の `/rn:gm` で、ゲートが `ja/` と `mapping/`・`ja/conf.py` しか見ていなかったため Docker フルビルドが再生成した `locales/ja/LC_MESSAGES/sphinx.mo` の混入を素通りさせた（`f6947b2`・`73e84dc`・`c0381ed` で3回とも差し戻し済み）。**このゲートを `commit & push` の後ろに置くと、混入を検出できるのはコミットしてしまった後になる**（`#18` がその経路で公開まで届いた。2026-08-13 の作業指示による是正）
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

### #16: ページのリード文の確定と `design.md` の3点追記 — DONE

**Purpose**: ページを作らないタスク。リード文（目次の直後・最初のL2見出しより前に置く、見出しの無い導入の段落）の位置を `style.md` S-02・`design.md` §3・§4 で確定して作成済みの第2部3ページに反映し、`#15` の `decide` 3件を `design.md` §8・§13 に規定化する。

**Completion criteria**:

- リード文の位置と書き出しが `style.md` S-02 に規約として書かれ、根拠が FW解説書の実ファイルの `file:line` で裏付けられている
- 第2部の作成済み3ページのリード文が目次の直後・最初のL2見出しより前にあり、`使用方法` の直下に地の文が残っていない
- 3ページの `ja/` 差分がリード文の移動と文頭の書き直しに由来するものだけで、見出しの文言・並び順が不変である
- `#15` の `decide` 3件が `design.md` §8・§13 に規定として書かれ、以降のページが参照できる
- `design.md` の差分が §3・§4・§8・§13 に、`style.md` の差分が S-02 に収まり、いずれも削除0行である
- ゲート1〜9 が実行結果で `checks/task-16.md` に記録されている

**Closed**: user review 承認済み（`/rn:ty`、2026-08-12）。ゲート1〜9 全件 PASS・Docker フルビルド（`-a`）は `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）。`ja/` 側の差分は3ページとも `+2 / -1` 行のみ。作業指示の指定により4観点のレビューは回していない（新しい内容を書かないタスクで、ゲート1〜3 が変更範囲を機械的に固定している）。作業指示から外れた点3件（ゲート5の適用範囲／`style.md` の根拠を実測に合わせた訂正2件／`design.md` §4 への1文の追加）は `checks/task-16.md` 末尾に記録。詳細は `checks/task-16.md`・`reviews/page-common.md`・`page-class_unit_test.md`・`page-request_unit_test_setting_web.md` および git 履歴（最終内容コミット `04d8545`）を参照。**以降の全ページはリード文を目次の直後に置く**（共通 Steps の `.. contents::` の項に続く位置づけ）。

### #17: リクエスト単体テストの設定（RESTfulウェブサービス）（`setup/request_unit_test/rest.rst`）— DONE

**Purpose**: マッピングに従って第2部の4ページ目「リクエスト単体テストの設定（RESTfulウェブサービス）」を作成する。対象は `mapping.csv` の `dest_page=リクエスト単体テストの設定（RESTfulウェブサービス）` の4行（125 lines）。共通 Steps のみで進めた（個別の作業指示を出す条件に当たらない）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**`decide` 2件の回答**（2026-08-13、`/rn:ty`。判断を仰いだ時点の記録は `checks/task-17.md` §6 に残し、回答は同 §6-1 に追記した）:

1. **`httpServerFactory` の登録を本文に書いたこと → 残す。** 出典が触れていないのはアーキタイプからのプロジェクト作成を前提にしていたためで、アーキタイプ以外から作る読者には必須（未登録なら `SimpleRestTestSupport.java:45`・`:298-300` で `IllegalConfigurationException`。デフォルト設定は 5u24・5u26・6u1・6u2・6u3 のすべてで0件）。**`design.md` §8 の既存の例外2件のどちらでもない新しい類型**「出典が欠いている、実装上必須の設定」であり、規定化は `#18` で行う
2. **設定項目表の「デフォルト値」の基準 → デフォルト設定を読み込んだ実効値に統一する。** `rest.rst` が正しく、`web.rst`（クラスのフィールド初期値）を改める。根拠は出典自身が実効値を書いていること（`RequestUnitTest_rest.rst:288`・`02_RequestUnitTest.rst:345`・`:351`）。**是正対象は `checks/task-17.md` §7-2 の7項目では足りず、`web.rst` 9項目・`common.rst` 1項目**（レビュー役の実測）。全件と手順は `#18` の作業指示

**Closed**: user review 承認済み（`/rn:ty`、2026-08-13。公開本文を承認し `decide` 2件に回答）。4観点レビュー ラウンド1（A fail `must` 2 / B fail 1 / C fail 1 / D fail 2、重複除去5件すべて是正）→ ラウンド2は是正差分限定の検証で pass（`must` 0）。コーディネータの独立検証で本ページに新規の事実誤りなし、`decide` 2 の射程の広がりを新規検出。Docker フルビルド `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）。詳細は `checks/task-17.md`・`reviews/page-request_unit_test_setting_rest.md` および git 履歴（最終内容コミット `4f78d11`）を参照。

### #18: 設定項目表の「デフォルト値」の基準の統一と `design.md` §8 の類型追加 — DONE

**Purpose**: `#17` の `decide` 2件の回答を規定として定着させ、既存ページを是正する。(1) 設定項目表の「デフォルト値」をデフォルト設定を読み込んだ実効値に統一し、`web.rst`・`common.rst` を是正する。(2) 「出典が欠いている、実装上必須の設定」を `design.md` §8 の例外の新しい類型として追記する。**ページを作らないタスク。**

**Completion criteria**: 作業指示 `ntf-doc-18-default-value-basis.md` のゲート1〜11 が全件 PASS で `checks/task-18.md` に記録されていること。

**Closed**: user review 承認済み（`/rn:gm` 1回 →`must` 1件是正のうえ承認、2026-08-13）。`web.rst` 不一致8件＋表外1件・`common.rst` 1件を是正し、`design.md` §8 に2件を追記（追加39行 / 削除0行）。差し戻しは本文ではなく、Docker フルビルドが再生成した `locales/ja/LC_MESSAGES/sphinx.mo` の混入1件（`2993496` の版に戻して解消。過去2回と同一の副産物で `f6947b2`・`73e84dc` でも同様に差し戻し済み。再発防止として `#9〜` の共通 Steps に差分の範囲を確認するゲートを追加）。ユーザー回答3点は (1) 出典を示せない行番号は `design.md` に書かない対応で正、(2) ゲート9 は「新規0件」の解釈で正、(3) `testdata_notation.rst` の「デフォルト設定」の語の衝突は是正せず申し送りで正（`#19` 以降で `design.md` §8 の語と衝突する記述を書かないこと）。詳細は `checks/task-18.md`・`reviews/page-request_unit_test_setting_web.md`・`page-common.md`・`page-testdata_notation.md` および git 履歴（本文コミット `7424aeb`）を参照。

### #19: リクエスト単体テストの設定（HTTPメッセージング）（`setup/request_unit_test/http_messaging.rst`）— DONE

**Purpose**: マッピングに従って第2部の5ページ目「リクエスト単体テストの設定（HTTPメッセージング）」を作成する。対象は `mapping.csv` の `dest_page=リクエスト単体テストの設定（HTTPメッセージング）` の3行（計30 lines）。共通 Steps のみで進めた（個別の作業指示を出す3条件に当たらない）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**`decide` 3件・`should` 1件の回答**（2026-08-13、`/rn:ty`。判断を仰いだ時点の記録は `reviews/page-request_unit_test_setting_http_messaging.md` §4 に残し、回答は同 §4 の各 `decide` 直下に追記した。是正の実行結果は `checks/task-19.md` ゲート6）:

1. **`glossary.md:160` の `モックアップクラス` の意味列 → 是正する。** 「同期応答メッセージ送信・HTTPメッセージ送信で、外部システムの代わりに応答電文を返すクラス。リクエスト単体テスト・取引単体テストの双方で使い、実体は別のクラスである」に改めた。意味列は判断の記述であって証拠ではない。書き換えを禁じている対象は削除前の現行解説書に実在した見出し文字列の一覧（`glossary.md` の `:403`〜`:449` 相当）であり、採用根拠の列も実測値の記録として触らない。正表記が不変のため既存ページへの波及なし。ゲート4件（差分が意味列のセル1つ／`mapping.csv`・`_batch/` の差分0／`verify_mapping.py` `exit 0` で 594行・12,986・11,983 不変／`ja/` 差分0）を全件パス
2. **出典外の追記 → 残す。ただし追記は2件ではなく3件である（`should` 1 の訂正）。** (a) コンポーネント名の解決は `design.md` §8「出典が欠いている、実装上必須の設定」に当たる（`#17` の `httpServerFactory` と同じ類型）。(b) モックアップクラスの挙動説明は §8 のどの例外にも当たらないが残す（何をするクラスかを述べずに「登録する」だけでは、読者は登録の可否を判断できない。典拠は `RequestTestingMessagingClient.java:46`・`:48`）。(c) `http_messaging.rst:21` の「ウェブアプリケーションやNablarchバッチアプリケーション…も同じである」を数え落としており、3件目として加えた。**訂正したのは記録の件数のみで、本文は変更していない**
3. **FW解説書 `http_system_messaging.rst:85` → 対象外として記録に留める。別タスク化もしない**（`#last` でも扱わない）。実装と食い違うのは結論ではなく理由の部分である。同行は「ルックアップして使用されるため、コンポーネント名は `messageSenderClient` と指定する」と書くが、実際には `MessageSenderSettings#getComponent` が `messageSender.<リクエストID>.messageSenderClient` の**値**をコンポーネント名として `SystemRepository` から引くため任意の名前でよい

**Closed**: user review 承認済み（`/rn:ty`、2026-08-13。公開本文を承認。レビュー役の独立検証で `must` 残存0件・本文に事実誤りなしを確認）。4観点レビュー ラウンド1（A fail `must` 3 / B fail 1 / C fail 1 / D fail 3、重複除去後7件すべて是正）→ ラウンド2は是正差分限定の検証で PASS（`must` 0）。Docker フルビルド `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）。`#19` から導入した差分範囲ゲート（母集合は `git status --porcelain` の全件、`commit & push` の直前）が `locales/ja/LC_MESSAGES/sphinx.mo` の混入（通算4回目）を実際に検出し、コミット前に戻した。詳細は `checks/task-19.md`・`reviews/page-request_unit_test_setting_http_messaging.md` および git 履歴（本文コミット `98542ac`）を参照。`#20` 以降への申し送り7件は同レビュー記録 §5。

### #20: リクエスト単体テストの設定（Nablarchバッチアプリケーション）（`setup/request_unit_test/batch.rst`）— DONE

**Purpose**: マッピングに従って第2部の6ページ目「リクエスト単体テストの設定（Nablarchバッチアプリケーション）」を作成する。対象は `mapping.csv` の `dest_page=リクエスト単体テストの設定（Nablarchバッチアプリケーション）` の3行。共通 Steps のみで進めた（個別の作業指示を出す3条件に当たらない）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**`decide` 3件・`should` 3件の回答**（2026-08-13、`/rn:ty`。判断を仰いだ時点の記録は `reviews/page-request_unit_test_setting_batch.md` §4 に残し、回答は同 §4 の各 `decide` 直下に追記した。是正の実行結果は `checks/task-20.md` ゲート16〜24）:

1. **`testdata_notation.rst:967` の `TEST_{型名称}` → 是正する。** `TEST_{型記号}` に改め、第3文を「元の型に代えてその型が使用される」に直し、末尾に第2部への `:ref:` を追加した。是正する理由は、`#19` の申し送り4 と違って読者が誤った設定を書く経路があり、かつ `#20` のページ `:82` 自身がその経路を作っていること。差分は `:967` の1行のみ
2. **削った数値記述例 → 第3部「テストデータの書き方」へ移す。** 採る理由は「`decide` 1 と同じ段落だから」ではなく、`design.md:273-274` が「テストデータの書き方＝どう書けばどう解釈されるかの規則」「記載例＝Excel と YAML の対比」と役割を定めており、この記述は規則そのものかつ両形式で同一だからである。形式別 L4 には割らない（`style.md` S-10 規約1）。**`mapping.csv` を追随させた**: `current-0037-b` を `263`〜`274`（`current-0037-b2`・12行・第3部）と `275`〜`316`（42行・第2部）に分割し 594→**595行**（`#6` の `current-0128` と同じ手順）。`volume.md` は 3,391→3,403 / 129→117、合計 11,983 は不変
3. **デフォルト設定 `6u3` の同梱ファイル → どちらにも触れない（現状維持）。** 記録に1件追加した。`fixed-length-convertor-setting_test.xml` は自身の `:10` で `nablarch/batch/resume-point-manager_test.xml` を `import` しており、当該ファイルだけを直接 `import` してもレジュームポイント管理の設定が抱き合わせで入る。`#last` で `design.md` §8 に残すかを判断する（`#20` では別タスク化しない）
4. **`should` 1・2 — `glossary.md` を2点是正した。** `ディレクティブ` の意味列を「キー名と値の2要素で指定するもの」に改め（`<map>`／`<entry>` による登録を含む範囲にした）、§5.8 に `型名称`・`型記号` の2行を追加した（採用根拠は実測。input のみ6件・2件、現行解説書とFW解説書は0件）。正表記・揺れ・採用根拠の各列と `:403`〜`:449` の見出し一覧は不変
5. **`should` 3 — 申し送り3 に裏付けの範囲を書き添えた。** L3 の実測則 `max(49, 表示幅)` のうち**表示幅側**の裏付けは `implementation/testdata_examples.rst` の7箇所（うち下限50を超えて discriminating なのは5箇所）、**下限49の裏付けは `setup/` 配下の5ページ**である。両者を合わせて規則が立つ

**Closed**: user review 承認済み（`/rn:ty`、2026-08-13。公開本文を承認。レビュー役の独立検証で `must` 残存0件・本文に事実誤りなしを確認）。4観点レビュー ラウンド1（A PASS / B・C・D FAIL、`must` 重複除去後4件）→ 是正13件 → ラウンド2 PASS → ラウンド3で `should` 2・`note` 3 を一括是正。承認時の是正で `testdata_notation.rst:967`・`glossary.md`・`mapping.csv`（`_batch/batch-16.csv` 経由で再生成・バイト一致）・`volume.md` を更新し、`verify_mapping.py` は 595行 / 12,986 / 11,983 で `exit 0`、Docker フルビルドは `build succeeded, 1 warning.`（既知1件のみ・新規0件）。**`volume.md` の `dest_section` 別集計に既存の誤り2件（第3部「使用方法」が実測より453行多い／`テストデータの構造` 479行の行が欠落）を見つけ、あわせて是正した**（合計 11,957→11,983）。詳細は `checks/task-20.md`・`reviews/page-request_unit_test_setting_batch.md` および git 履歴（本文コミット `00cb161`・`2bb3cf6`・`fb3fd0f`、承認時是正コミット `4d9e3f7`）を参照。`#21` 以降への申し送り7件は同レビュー記録 §5。

### #21: リクエスト単体テストの設定（MOMによるメッセージング）（`setup/request_unit_test/mom.rst`）— DONE

**Purpose**: マッピングに従って第2部の7ページ目「リクエスト単体テストの設定（MOMによるメッセージング）」を作成する。対象は `mapping.csv` の `dest_page=リクエスト単体テストの設定（MOMによるメッセージング）` の8行（76 lines、`DROP` 0件）。共通 Steps のみで進めた（個別の作業指示を出す3条件に当たらない）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**`decide` 5件・`should` 3件の回答**（2026-08-13、`/rn:ty`。判断を仰いだ時点の記録は `reviews/page-request_unit_test_setting_mom.md` §4.5・§5.3、回答と反映は同 §6、ゲートの実行結果は `checks/task-21.md` §7）:

1. **`reader.fwHeaderfields` の重複 → (c) 現状維持。集約しない。** この設定を読む経路は `MessageParser` だけで、そこへ至るのは `MQSupport.java:87` の1箇所、`MQSupport` を生成するのは `MessagingRequestTestSupport.java:82` と `MessagingReceiveTestSupport.java:42` の2箇所のみ（`src/main/java` 全走査）。**メッセージング受信のテストに紐づいており、全テスト共通ではない。** `setup/common.rst` へ移すと読者に「共通設定なので自分のテストにも効く」と読ませる。非対称は `should` 1 で解消
2. **`testdata_notation.rst:1244` → 是正する。** `YAML` 経路は `reader.fwHeaderfields` を読まない（`YamlMessageBuilder.java:223-236`）。同ファイル `:1263` とだけ矛盾していた。差分は1行
3. **出典外の追記2件 → 2件とも残す。`design.md` §8 に類型を1つ追加した。** 「出典が書いていない適用範囲・副作用のうち、書かなければ読者が誤った設定に至るものは書き足してよい」。「適用範囲の限定」と「副作用の注意喚起」は**読者が誤るかという同じ判定基準**で決まるため1類型にまとめた
4. **`glossary.md` 3件 → 3件とも反映。** §5.12 に `環境設定ファイル`、§5.14 に `デフォルト`、§8 に置換3行（`propertiesファイル`／`プロパティファイル`→`環境設定ファイル`、`TestDataConvertor`→`TestDataConverter`、`既定`→`デフォルト`）。**`ja/` 4ファイルの `既定` 26箇所を `デフォルト` に置換した**（`batch.rst` 13・`testdata_notation.rst` 6・`mom.rst` 5・`http_messaging.rst` 2。全件表は `checks/task-21.md` §7-1）。判定根拠は語彙の実測で、**現行解説書に `既定` は0件**（`デフォルト` 58件）
5. **HTTPメッセージング受信への適用 → 効く。いま確定させた。** 決め手は識別子行が `MESSAGE=setUpMessages`／`expectedMessages` 固定であること（`c2419060:.../http_real.rst:56`・`:105`・`:168`）。この2つのIDを読む経路は `MQSupport.java:73-74`・`:63-64` の1つだけで、`BasicTestDataParser.java:82-85` の `new MessageParser(..., DataType.MESSAGE)` に至る。**適用範囲は MOM と同一**で、承認済み `http_messaging.rst:37-42` は正しい
6. **`should` 1・2 — `http_messaging.rst` に `mom.rst` と同じ2文とコメントを追加し、両ページに「値に空白を入れない」の1文を追加した。** 空白がトリムされない裏付けは `NablarchTestUtils.java:36`・`:45-49`、判定は `MessageParser.java:103`
7. **`should` 3 — レビュー記録の根拠を是正。** `createDefinition` が返すレイアウト定義は「書き出しにのみ」ではなく**書き出しと読み込みの双方**に使われる（`MessagePool.java:165`）。公開本文（方向を限定しない表現）は変えていない

**Closed**: user review 承認済み（`/rn:ty`、2026-08-13。レビュー役の独立検証で公開本文の事実誤り0件・`must` 残存0件）。4観点レビュー ラウンド1は4観点とも FAIL（重複除去後 `must` 3件）→ ラウンド2は是正差分限定で範囲検証 PASS／ファクトチェック不一致1件を是正。承認後の反映でゲート1〜10 を全件 PASS（`verify_mapping.py` 595行 / 12,986 / 11,983 で `exit 0`、Docker フルビルド `build succeeded, 1 warning.` 既知1件のみ・新規0件、`sphinx.mo` はビルド直後に復元）。詳細は `checks/task-21.md`・`reviews/page-request_unit_test_setting_mom.md` および git 履歴（本文コミット `8b956cd`・`2c9be08`・`346171d`・`e8854a5`、承認後の反映コミット `c0e12fc`）を参照。

**`#22` 以降への申し送り**:

- **`verify_glossary.py` は本タスクで不一致が 18→25 に増えた**（`checks/task-21.md` §7-4 に前後比較表）。増分7件はすべて、追加した3語と揺れ表記2語が `mapping/tools/term_candidates.tsv` に未登録であることに起因する。登録すると `glossary.md` の既存の全件数主張を再計算する作業になるため、`[ref]` 13件と合わせて**別タスクで一括して直す**
- `real.rst:15` はクラスのパッケージ名を `nablarch.test.core.http` と書いているが実体は `nablarch.test.core.messaging`。**第3部「リクエスト単体テスト（MOMによるメッセージング）」を書くタスク（`current-0295`〜`0301`）で是正する**
- `nablarch-testing-yaml` のスキーマ説明文（`ntf-testdata-yaml-schema.json`）の見直しは PR #75 側の話であり、本刷新の範囲外

### #22: 取引単体テストの設定（RESTfulウェブサービス）（`setup/deal_unit_test/rest.rst`）— DONE

**Purpose**: マッピングに従って第2部の8ページ目「取引単体テストの設定（RESTfulウェブサービス）」を作成する。対象は `mapping.csv` の `dest_page=取引単体テストの設定（RESTfulウェブサービス）` の3行（52 lines、すべて `MERGE`・`audience=user`）。`setup/deal_unit_test/` ディレクトリは本タスクで新設した。事前情報は `ntf-doc-22-deal-unit-test-rest.md`。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。加えて、事前情報 §4 のゲート1〜9 が実行結果で `checks/task-22.md` に記録されていること。

**Closed**: user review 承認済み（2026-08-14。レビュー役の独立検証で `must` 残存0件・出典 `03_DealUnitTest/rest.rst:40-95` の落ちている記述0件・Docker フルビルドをレビュー役自身の clone で再実行して `build succeeded, 1 warning.`）。4観点レビュー ラウンド1（B・C PASS／A・D が `must` 各1件で FAIL）→ 是正ラウンド1 `d90d28f`（A の `must` は「実装が `Set-Cookie` を扱わない」という誤認で、原因は `grep` に `-a` を付けずバイナリの `.class` を読み飛ばしたこと）→ 是正ラウンド2 `29269d4`（`must` 1・`should` 2。差分は本文3行）→ 検証ラウンド3は2観点とも PASS。出典に無い記述2件（`cookieName` 必須＝`RequestResponseCookieManager.java:41-43`、`processors` の実行順＝`ComplexRequestResponseProcessor.java:15-29`）はいずれも実装が根拠で `design.md` §8 の範囲内としてレビュー役が承認した。詳細は `checks/task-22.md`・`reviews/page-deal_unit_test_setting_rest.md` および git 履歴（本文コミット `c8c937e`・`d90d28f`・`29269d4`、self-check `cf0eb2f`）を参照。

**`#23` 以降への申し送り**: `checks/task-22.md` §7-2 の `note` N-2「CSRFトークンを引き継ぐ提供実装は存在しない」は、取引単体テスト残りページで CSRF に触れる場合に確認する。

**環境の事実（解決済み）**: `docker build` が失敗する原因は**社内proxyの自己署名証明書がイメージ内の CA ストアに無いこと**である（`pip` が `SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] ... self-signed certificate in certificate chain'))` で落ちる）。レビュー役が自分の clone で再現し、CA を注入した `Dockerfile` を作れば `docker build` が通り、そのイメージの `sphinx-build -a` が `build succeeded, 1 warning.` になることまで確認した（手順は `checks/task-22.md` §4）。**`ca.crt` と `Dockerfile.ca` は作業ツリーに残さない**（差分範囲ゲートに掛かる）。既存イメージ `nablarch-document-build` での `docker run` を続けてもよい。

### #23: テーブルデータの0件の扱いを解説書に書く — DONE

**Purpose**: ページを作らないタスク。承認済みの2ページ（`implementation/testdata_notation.rst`・`implementation/testdata_examples.rst`）に、テーブルデータを0件で書く方法を追記した。指示は `ntf-doc-23-table-zero-rows.md`。

**Completion criteria**: 作業指示のゲート1〜12（4a・4b を含む）が全件 PASS で `checks/task-23.md` に記録されていること。加えて4観点のレビューがすべて実施・記録されていること、未対応の指摘を残す判断とその理由が記録されていること、`make html` が当該2ページについてエラーを出さないこと。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-14）。ラウンド1 のみで確定（4観点レビューの重複除去後15件を triage し6件是正・1件 Invalid・8件は対応せず）。ゲート1〜12 は是正後の再実行で全件 PASS、Docker フルビルド（`-a`）は `build succeeded, 1 warning.` で新規警告0件。**`design.md` §8 の「実装優先」を本件に適用しない**（2026-08-13 のユーザー判断）ため、`expected_tables:` の `rows: []` は `190cc9a` 時点の `nablarch-testing-yaml` で検証されないまま仕様どおりに記述している。判定待ちに添えた報告2件も承認で決着した — (1) 指示書 §2 事実7 の `insertData` の範囲は `:137-217` ではなく `:137-178`（事実の内容は一致）、(2) 記法ページの見出し「0件のデータを記述する」と記載例ページの「0件のテーブルデータを記述する」の非対称は、指示書 §4-1・§4-3 の明示指定に従い**現状のまま確定**。詳細は `checks/task-23.md`・`reviews/page-testdata_notation.md` `## #23` 節・`page-testdata_examples.md` および git 履歴（本文コミット `b75f1d7`）を参照。

### #24: `about/index.rst` の「取引単体テストは手動操作」の是正と `style.md` S-02 の書き漏れ補い — DONE

**Purpose**: ページを作らないタスク。`#22` の user review で回答された判断待ち2件を、承認済み資産の是正として1タスクにまとめて行った。(a) 取引単体テストの実行方法は処理方式によって異なるという事実に `design.md` と `about/index.rst` を合わせる。(b) `style.md:45` に第2部セクションの必須・任意の区別を書き足す。指示は `ntf-doc-24.md`。

**Completion criteria**: ラウンド1 のゲート1〜12、`ntf-doc-24.md` §5-3 のゲートA〜N、§7-6 のゲートO〜U が全件 PASS で `checks/task-24.md` に記録されていること。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-14）。ラウンド1〜4 で確定。**公開本文で名指しするのは3処理方式のみ**（ウェブアプリケーション＝手動／RESTfulウェブサービス＝自動／Nablarchバッチアプリケーション＝自動）とし、出典が不可能性を述べていない3処理方式（`MOMによるメッセージング`・`HTTPメッセージング`・`テーブルをキューとして使ったメッセージング`）には公開本文で触れない形に落ち着いた。ラウンド4 は3行の是正のみ（`about/index.rst:77` 第2文の目的語補い＋「アプリケーション」3回の解消／`:81` の「このうち」の先行詞固定／`style.md:5` の `design.md`「7. トンマナ」→「8. トンマナ」）で、4観点のレビューは指示書 §7-7 により回していない。**ゲートP のみ指示の文言のままでは満たせず、第2文単位で PASS とし本文は変更していない**（段落単位では変更禁止の第3文の `Nablarchバッチアプリケーション` を含めて3回。`checks/task-24.md`「指示との食い違い1件」）。詳細は `checks/task-24.md`（ラウンド1〜4）・`reviews/page-about_index.md` `## #24` 節および git 履歴（本文コミット `82dbe16`・`443dccc`・`5e87f6e`・`db5a84a`、ラウンド4 `66fe4c9`、記録 `7ddc30f`）を参照。

### #25: 取引単体テストの設定（HTTPメッセージング）（`setup/deal_unit_test/http_messaging.rst`）— DONE

**Purpose**: マッピングに従って第2部の9ページ目「取引単体テストの設定（HTTPメッセージング）」を作成する。対象は `mapping.csv` の `dest_page=取引単体テストの設定（HTTPメッセージング）` の1行（`current-0140`、出典 `…/03_DealUnitTest/http_send_sync.rst:50-69`、20 lines）。共通 Steps のみで進めた（個別の作業指示を出す3条件に当たらない）。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**判断待ち3件の回答**（2026-08-14、`/rn:ty`。判断を仰いだ時点の記録と回答は `reviews/page-deal_unit_test_setting_http_messaging.md`「判断待ちと、その回答」節。**回答2・3 は本文を変更せず、回答1 の作業は `#26` で行う**）:

1. **`sendSyncTestData`・`messagingTestDataParser` の置き場所 → `setup/common.rst` に置く（案B）。作業は `#26`。** 根拠は `design.md:192` が共通設定の範囲に「テストデータの配置」を挙げていること。案A（MOMページに置いて `:ref:`）は、MOM をやらない読者を MOM のページへ送ることになり、`design.md:125` が問題としている読者のずれを解説書の側で作るため採らない。未作成ページへの前方参照スタブも作らない。節の見出しで適用条件を名乗る。**「3処理方式で共通」は誤りで、必要なのは取引単体テストの `HTTPメッセージング` と `MOMによるメッセージング` の2処理方式のみ** — `SendSyncSupport` を生成するのは `MockMessagingClient.java:54` と `MockMessagingContext.java:52`・`:93` の2クラスだけで、リクエスト単体テスト側は `RequestTestingSendSyncSupport` → `TestSupport.java:403-408` の `testDataParser` を通る別経路である（`e21bf67` を `git grep 'new SendSyncSupport' -- src/main` で実測）
2. **同一コンポーネント名 `defaultMessageSenderClient` の衝突 → 本文には書かない。`#pre-last` の横断確認項目とする。** 名前がリクエストIDごとに決まることは承認済みの `setup/request_unit_test/http_messaging.rst:31` が書いており、本ページ `:31` が導線を張っている。残るリスクは散文ではなく**例示名**（出典 `http_send_sync.rst:62` の逐語）にあり、2ページを揃えて判断すべき事項である
3. **リード文への前提の明示 → 明示しない（現状維持）。** `design.md:125` は第3部2ページ宛ての規定で本ページに及ばず、第2部のリード文の型を1ページだけ崩し、実装にウェブ限定の要素も無い（`MockMessagingClient.java:35`）。前提の明示は第3部 `implementation/deal_unit_test/http_messaging.rst` の作成タスクに委ねる

**Closed**: user review 承認済み（`/rn:ty`、2026-08-14。レビュー役の独立検証で出典 `current-0140` の4要素すべてが本文に対応し、公開本文に事実誤り0件。禁止ファイルの差分0行、`verify_mapping.py` は 595行 / 12,986 / 11,983 で `exit 0`）。4観点レビュー ラウンド1（A FAIL `must` 1 / B PASS / C PASS / D FAIL `must` 1、重複除去後12件）→ 是正4件 → 是正差分限定の検証ラウンドで FAIL（`must` 1）となり**是正1・2 を取り消し、是正4 を修正**。本文に残った是正は2件のみ。**是正1・2 を取り消した判断は正しいことをレビュー役が `mapping.csv` の実測で確認した**（`design.md:125` の宛先は第3部、出典 `http_send_sync.rst:7` は `current-0138`＝第3部割当。役割名は `ja/development_tools/testing_framework/index.rst:13` が定義）。Docker フルビルドは3回とも `build succeeded, 1 warning.`（既知の `db_double_submit.rst` のみ・新規0件）。詳細は `checks/task-25.md`・`reviews/page-deal_unit_test_setting_http_messaging.md` および git 履歴（本文コミット `acdcb75`）を参照。

### #26: 取引単体テストの設定（MOMによるメッセージング）（`setup/deal_unit_test/mom.rst`）— DONE

**Purpose**: マッピングに従って第2部の10ページ目を作成する。対象は `current-0158`（出典 `…/03_DealUnitTest/send_sync.rst:280-383`、104 lines）。`#25` の回答1 に従い出典を3分割したため、成果物は本ページと `setup/common.rst` の追加分にまたがる。

**Completion criteria**: 上記ページ作成タスクの Completion criteria に同じ。

**`current-0158` の分割（確定）**: `-a`（`:280-297`、18行）はモックアップクラスの設定で本ページへ。`-b`（`:298-360`、63行）はテストデータのベースディレクトリと解析コンポーネントの設定で `共通設定` へ。`-c`（`:361-383`、23行）は `pom.xml` への依存関係追加で `共通設定` へ。`mapping.csv` は 595→**597行**（`_batch/batch-25.csv` 経由で再生成・バイト一致）、12,986 / 11,983 は不変。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-14。公開本文を承認）。4観点レビュー ラウンド1 は**4観点とも FAIL**（重複除去後 `must` 5 / `should` 9 / `info` 8）→ 是正14件 → 是正差分限定の検証ラウンドは **PASS**（`must` 0、`should` 2 は本タスク内で是正）。ゲート1〜11 全件 PASS、Docker フルビルドは3回とも `build succeeded, 1 warning.`（既知1件のみ・新規0件）。**本タスクで確定した判断2件** — (1) `pom.xml` への `nablarch-testing` 追加の帰属は `共通設定`（処理方式・テスト種別によらず必要で、第2部の表題が「導入と設定」であるため）。(2) 出典に無い `nablarch-testing-yaml` の依存関係を追記（`YamlTestDataParser` を登録させながらモジュールの追加手順がどのページにも無く、書かれたとおりでは動かないため。`design.md` §8「出典が欠いている、実装上必須の設定の追記」・`design.md:176`）。**YAML形式の設定は実際に動かして確認した**（`fileExtensions` に `sendSyncTestData` を設定すると `IllegalStateException`、設定しなければ応答電文を取得できる）。詳細は `checks/task-26.md`・`reviews/page-deal_unit_test_setting_mom.md` および git 履歴（本文コミット `2bc3bf0`）を参照。

**`#27` 以降への申し送り**: (1) 用語 `同期応答メッセージ送信`（MOM側）と `HTTPメッセージ送信`（HTTP側）は `glossary.md:156`・`:158` の別の正表記であり、両方に掛かる場合は「同期応答メッセージ送信・HTTPメッセージ送信」と併記する（`implementation/testdata_notation.rst:497` に先例）。(2) `style.md` S-10 規約1 の「共通にしてよい2類型」に「両形式で同一の設定」が無い。類型追加の要否は `#pre-last` で判断する。(3) `messagingTestDataParser` は「テストデータを解析するコンポーネント」と呼ぶ（`setup/class_unit_test.rst:108` に合わせた）。


### #27: 週末の連続作成キュー（`#27-00` ＋21ページ。user review を挟まない）— DONE

**Purpose**: 残り21ページの「初版と自己レビューまで」を、user review を挟まずにキュー順で片づける。作業指示は `.rn/20260724-ntf-yaml-support/ntf-doc-weekend-queue.md`。個別指示は `ntf-doc-27-small-3rd.md`（`#27-07`・`#27-10`・`#27-11`・`#27-15`）・`ntf-doc-27-db-queue.md`（`#27-16`〜`#27-18`）・`ntf-doc-27-large-pages.md`（`#27-19`〜`#27-21`）。

**Completion criteria**: `#27-00` と21ページすべてがコミット済みで、各ページについて作業指示 §5 のゲートG1〜G13 の結果が `checks/task-27.md` に記録されていること。

**Closed**: user review 承認済み（`/rn:ty`、2026-08-15）。キュー22件すべてコミット済み（`6fceb6f`〜`7e19f68`）。`blocked` としたページは無い。レビュー役の独立検証（`7e19f68` を独立クローンで全量検証。結果は `ntf-doc-27-review.md`）は**要是正0件**で、申し送りは `guide/` 残骸2件のみ。フルビルド（`sphinx-build -a`）は WARNING・ERROR ともに0件、`verify_mapping.py` は exit 0、`verify_glossary.py` の不一致は既知25件で新規の劣化なし、`guide/` を除く `.rst` 38件が `design.md:830-890` のツリーと完全一致、ページ先頭ラベル37件が `style.md` S-08 一覧と0件不一致。**21ページが上げた判断待ち110件は `#28` で処理する。** 詳細は `checks/task-27.md`・`reviews/page-*.md`・`ntf-doc-27-review.md` および git 履歴を参照。

### #pre-last: `verify_glossary.py` の不一致25件の一括是正と、横断の是正 — DONE

**Purpose**: ページを作らないタスク。`#21` の申し送りで残った `verify_glossary.py` の不一致25件を、全ページ作成完了後・`#last` の直前に一括で解消し、あわせて横断の是正2件（例示のコンポーネント名の衝突・語の統一3件）を行う。

**Completion criteria**:

- `verify_glossary.py` の不一致が0件で exit 0
- 再発防止の判断（`design.md` のコーパス除外か行番号指定の廃止か）が記録されている
- 横断の是正2件（例示のコンポーネント名・語の統一3件）に判断と実行結果が記録されている
- `ja/` 配下の `.rst` の差分が、横断の是正2件に由来するものだけである

**Closed**: user review 承認済み（`/rn:up`、2026-08-16。**独立検証で要是正0件、判断3件ともそのまま承認**）。9検査すべて不一致0件（`RESULT: OK`）、`verify_mapping.py` は exit 0、`pytest` は `183 passed`、Docker フルビルド（`-a`）は `build succeeded.` で WARNING・ERROR ともに0件、`ja/` の差分は4ファイル・9行。**再発防止は二者択一ではなく両方を実施した** — `S:design.md:NN` の行番号39箇所を撤廃し、かつ `design` を `scan` のコーパスから外した（別々の検査が壊れていたため）。**承認された判断3件** — (1) 取引単体テスト側の例示名を `defaultRealTimeMessagingClient` に変更（NTF 自身のテストリソースが2クラスに別名を与えて共存させている実測による）、(2) `メッセージの送信` → `電文の送信` に統一、(3) `アプリケーション開発者` → `アプリケーションプログラマ`（**`#25` の申し送りとは逆の結論**。`#27` で21ページ増えた後の実測でFW解説書4対1・現行解説書13対0となり申し送りの前提が崩れたため）。詳細は `checks/task-pre-last.md` および git 履歴（`8193d21`）を参照。

### #28: `#27` の判断待ち110件の処理 — DONE

**Purpose**: `#27` の21ページが上げた判断待ち110件を、レビュー役の一次情報検証にもとづいて処理する。作業指示は `ntf-doc-28-decide-disposition.md`。

**Completion criteria**:

- 作業指示のゲート1〜11 がすべて記録され、赤が無い
- `glossary.md` の `:331-456`（§5.15）に差分が0行
- フルビルドで WARNING・ERROR がともに0件
- `ntf-mod-01`〜`ntf-mod-03` の3ファイルに差分が0行
- `en/` 配下と `ja/conf.py` に差分が0行
- `grep -rn "guide/development_guide" --include=*.rst ja/` が §5-2 の直前で0件

**Closed**: user review 承認済み（`/rn:ty`、2026-08-18。ユーザーが `30a8271` を独立検証し、S-04 の3ブロック（`style.md:252-257`・`:265-268`・`:276`）の再計測値が全項目一致、`ja/`・`en/`・`glossary.md` に差分0行、検証器3本 PASS、git status クリーンを確認）。**ゲート10**（`_build/html/_sources/*.txt` に `TODO(NTF-*)` が9件残る件）は**変更しないで進める**で確定（`_sources/` はリポジトリ全325ページの reST 原文を含み、`html_copy_source` を落とすとサイト全体の出力が変わるため、NTF解説書刷新のスコープ外。TODO はモジュール側の判定が返り次第消える暫定マーカー）。`ja/conf.py` は変更しない。他の10ゲートは PASS。詳細は `checks/task-28.md` および git 履歴（`c1e307e`・`30a8271`）を参照。

**`#last` への持ち越し2件**（`#last` の Steps で扱う）:

1. `setup/junit5_extension.rst:73` の `maven-surefire-plugin` 2.22.0 の一次情報（`checks/task-28.md:833`）
2. 規約確定にともなう機械的な掃き出し — S-13 エスケープ186件・S-04 下線長**96件**（`implementation/testdata_examples.rst` 82件・`tools/request_data_tool.rst` 8件・`tools/master_data_tool.rst` 6件。`checks/task-28.md:229` の表の94件はこの96件に読み替える）

### #last: Evaluation sign-off — DONE

**Purpose**: NTF ドキュメント刷新の完了を Acceptance criteria に照らして確認し、ユーザーの承認を得る。

**Prerequisites**: すべてのページ作成タスク完了（`#28` まで承認済み）

**Steps**:

- [x] Acceptance criteria の達成状況を確認する
- [x] `make html` を実行し、**警告を含めて**未解決参照が0件であることを確認する。
      `keep_warnings = True` のため未解決参照はビルド失敗にならないので、
      エラー0の確認だけでは不十分。ビルドログに対し次を確認する
      - `undefined label` が0件
      - `toctree contains reference to nonexisting document` が0件
      - `unknown document` が0件
      確認したコマンドとログの該当箇所を `checks/task-last.md` に記録する
- [x] `checks/task-07.md`「リンク切れになる参照」3件それぞれについて、
      解消後の参照先（新ファイルパス・ラベル名）を実ファイルで確認して記録する
- [x] **持ち越し(1)** `setup/junit5_extension.rst:73` の `maven-surefire-plugin` 2.22.0 —
      一次情報で裏が取れるのは親POM の 2.22.2 のみ。下限「2.22.0以上」の Nablarch 側根拠は無い。
      本文をどうするかの判断材料をそろえて提示する（`checks/task-28.md:833`）
- [x] **持ち越し(2)** 規約確定にともなう機械的な掃き出し — S-13 エスケープ186件・
      S-04 下線長96件（`testdata_examples.rst` 82・`request_data_tool.rst` 8・`master_data_tool.rst` 6）。
      掃き出すか現状のままとするかを実測にもとづき判断・実行する
- [x] **`/rn:gm`（2026-08-18）の追加処置8件** — (1) S-13 抽出器に外部リンク記法を加えて38ページを再走査し
      取りこぼし1件（`about/index.rst:96`）を是正 (2) `style.md` の `file:line` 引用を実物と全件突き合わせ
      (3) 申し送り a 下線直後の空行削除 (4) 申し送り b L4を1本新設 (5) 申し送り c 2語是正・9語は
      `TODO(NTF-SRC-02)` (6) 申し送り d `:java:extdoc:`→コードリテラル2件 (7) 申し送り e
      `testdata_converter.rst`「導入」L2 の新設 (8) surefire 下限値に `TODO(NTF-SRC-01)`。
      記録は `checks/task-last.md` §4・§5-2・§5-5・§5-6・§5-7
- [x] **区切り文字ディレクティブの説明の是正（申し送り）** — 申し送り原本は
      `ntf-doc-renewal/指示/申し送り-区切り文字ディレクティブの制御文字.md`。タスク番号は新設せず `#last` に含めた。
      (A-1) `testdata_examples.rst:1435` に `record-separator` へ制御文字を書いた場合の1文を追加
      (A-2) `testdata_notation.rst:923`（固定長）・`:948`（可変長）の `record-separator` の説明をそろえる
      (A-3) 同 `:950` の `field-separator` の説明を実装（2文字表記 `\t` は有効・0文字もエラー）に合わせる。
      根拠は `nablarch-testing` `origin/main` = `e21bf67` の `file:line`（`checks/task-last.md` §5-8 の表）。
      あわせて `style.md:263` の L4 実測（`request_unit_test/web.rst`）を15本→16本に是正
- [x] 結果をユーザーに提示して `/rn:ty`（承認）または `/rn:gm`（修正）の判定をもらう

**Completion criteria**:

- すべての Acceptance criteria が達成されていることが確認できる
- `checks/task-07.md`「リンク切れになる参照」の3件すべてが解消されている
  （toctree・`:doc:` の更新、外部被参照ラベルの再定義）
- 持ち越し2件がそれぞれ処理済み（実行または「現状のまま」の判断が記録されている）
- ユーザーが `/rn:ty` で承認している

**実測**（`checks/task-last.md`。`/rn:gm` の追加処置後のクリーンビルド）:

- Acceptance criteria 5件のうち4件が達成、1件（トンマナ）は条件付き達成。`mapping.csv` 597件で
  DROP 96件以外の501件はすべて `dest_page` を持つ。`verify_mapping.py` exit 0、
  `verify_glossary.py` `RESULT: OK`（9検査すべて不一致0件）、`pytest` `183 passed`
- フルビルド（`-a`・`rm -rf _build` 後）は `build succeeded.`・exit 0。WARNING 0件・
  `undefined label` 0件・`toctree contains reference to nonexisting document` 0件・`unknown document` 0件
- `checks/task-07.md` の3件はすべて解消。ラベル `how_to_set_token_in_request_unit_test` は
  `implementation/request_unit_test/web.rst:257` に定義、参照は `db_double_submit.rst:106` の1件
- **持ち越し(1)** surefire — 親POM 6/6u1/6u2/6u3/6-NEXT の各 `:52` はすべて 2.22.2。下限 2.22.0 の
  Nablarch 側一次情報は無く、オフラインでは JUnit/Maven 側の出典も取得できない（**未確認**）。
  「2.22.0以上」は現行解説書（`2e501ad:.../01_Abstract.rst:691-695`・`JUnit5_Extension.rst:26-33`）に
  元からあり `mapping.csv` の `current-0179`・`current-0266` が移設を指示している。**現状維持を推奨**
- **持ち越し(2)** 掃き出し実施 — S-04 は 96件を是正し 392/392 一致・不一致0件。S-13 は 192件を是正し
  違反0件（`style.md` の186件は `084dd28` 時点では正しく、`#28` §6-2 の加筆で192件に増えていた）。
  **掃き出し前後のクリーンビルドを全件比較し、`.html` 486ページ・`searchindex.js`・`objects.inv`・
  `_images` に差分0件、差分は編集した11ファイルの `_sources/*.txt` のみ**であることを確認済み
- **申し送り5件は `/rn:gm` の追加処置で全件クローズ**（`checks/task-28.md:229` の表7行）—
  a 下線直後の空行削除・b L4新設（`request_unit_test/web.rst:309`「スーパクラスが読み込むデータブロックを
  記述する」）・c UI項目名2語是正＋9語は保留・d `:java:extdoc:`→コードリテラル2件・
  e `testdata_converter.rst:73`「導入」L2 の新設。`checks/task-last.md` §5-5
- **追加処置後のクリーンフルビルド** は `build succeeded.`・exit 0・WARNING 0件。検証器3本も再実行して
  すべて PASS。`870e809` との全比較で `.html` の差分は5ページのみで、いずれも上記 b・c・d・e に対応する。
  `objects.inv` は `testdata_converter-setup` の1行追加。`_images` 差分0。作業(1)(3)(8) は出力を変えない
  （`about/index.html`・`testdata_notation.html`・`junit5_extension.html` は差分一覧に現れない）
- **未達として残るのは2件だけ**。いずれも一次情報が本作業環境で取得できないことに起因する。
  (1) S-12 のUI項目名9語 — `TODO(NTF-SRC-02)`（`setup/request_unit_test/web.rst:162`・
  `tools/request_data_tool.rst:106`）(2) `maven-surefire-plugin`「2.22.0以上」の下限値の出典 —
  `TODO(NTF-SRC-01)`（`setup/junit5_extension.rst:73`）。**推測で書かないという user 判断による保留**で、
  本文は変更していない。`checks/task-last.md` §4・§5-5
- **区切り文字ディレクティブの是正** — 是正3件・編集4行（`testdata_examples.rst:1435`／
  `testdata_notation.rst:923`・`:948`／同 `:950`）を差し替え。`d8d6114` とのクリーンフルビルド全比較で、差分は
  `testdata_examples.html`（1行）・`testdata_notation.html`（3行）・両ページの `_sources/*.txt`・
  `searchindex.js` の5件のみ。`objects.inv`・`_images`・残り484ページの `.html` は差分0。
  ビルドは `build succeeded.`・exit 0・WARNING 0件で、検証器3本も再実行して PASS。
  再計測は S-04 が394/394・不一致0（変化なし）、S-13 がインラインマークアップ2,263件・違反0
  （コードリテラルが8件増えた分）。`checks/task-last.md` §5-8

**Closed**: user review 承認済み（`/rn:ty`、2026-08-18）。ユーザーが `96596b3` を独立に検証し、A・B とも
指示どおりで新たな指摘なしと判定した。検証内容 — `d8d6114` との両側クリーンビルドによる HTML 全比較で
差分5件、`.html` は該当2ページの1行・3行のみ、他484ページと `objects.inv`・`_images/` は差分0。
S-04 394/394・不一致0、S-13 2,263件・違反0、検証器3本 PASS、`TODO` 13ID 不変、`style.md:263` の
60/27/16本がすべて実物と一致。A-3 の根拠（`VariableLengthFile.java:70-71`・`:75-79`）も実装で再確認。
詳細は `checks/task-last.md` および git 履歴（`870e809`・`d8d6114`・`96596b3`）を参照。

**残る未達2件**（本刷新のスコープ外として保留。いずれも一次情報が本作業環境で取得できないためで、
推測で書かないという user 判断により本文は変更していない）:

1. S-12 のUI項目名9語 — `TODO(NTF-SRC-02)`（`setup/request_unit_test/web.rst:162`・
   `tools/request_data_tool.rst:106`）
2. `maven-surefire-plugin`「2.22.0以上」の下限値の出典 — `TODO(NTF-SRC-01)`
   （`setup/junit5_extension.rst:73`）

### #29: モジュール側の判定反映（4事象の確定と TODO 台帳の更新）

**Purpose**: `nablarch-testing`・`nablarch-testing-converter` で確定した判定を解説書に反映し、待つものが無くなった TODO を外して、残る TODO を「何がマージされたら外すか」が分かる状態にする。`#last`（Evaluation sign-off）の承認後に user から届いた追加依頼であり、承認済みの成果に対する差分タスクである。

**根拠（モジュール側の一次情報。本作業ディレクトリからは参照できないため、user が作業指示に引用した文面による）**:

- `nablarch-testing` `8530497:docs/pr75/steering.md` — 4事象の判定（事象1=仕様・解説書側対応／事象2=現状維持／事象3=不具合・#21 で対応／事象4前半=仕様・現状維持／事象4後半の YAML 対応=#22 で対応）。#21・#22 はいずれも未着手
- `nablarch-testing-converter` `b44268c:.rn/ntf-test-data-converter/steering.md` — 同名で拡張子違いの Excel ブックの同居は `XLS-28` として要対応（新規課題・2026-08-18 user 確定）・未着手

**Steps**:

- [ ] A. `tools/request_data_tool.rst` の `TODO(NTF-MOD-02-1)` を3行とも削除する。本文は1文字も変えない（事象1は仕様と判定済み、かつ本文を現行解説書に合わせて据え置くという user 判断による）
- [ ] B. `tools/master_data_tool.rst` の `TODO(NTF-MOD-02-4)` の直後に、確定した事象4前半の制約だけを1件書く。ディレクティブの要否は `mapping/style.md` S-06 に従って判断する。`#28` で削除した3文のうち「Excel 形式で記述する」「YAML 形式用のパーサを設定しているプロジェクトでは本ツールを使用できない」の2文は書き戻さない
- [ ] C. TODO コメント3件（`NTF-MOD-02-4`・`NTF-MOD-02-3`・`NTF-MOD-01-2`）の1行目・3行目を判定後の文言に更新する。3行の書式は保つ。`.rst` の地の文は B の1件を除いて変えない
- [ ] D. 記録を更新する。(1) `checks/task-last.md` §8 の台帳（`NTF-MOD-02-1` の行を削除、残る3件の「判定・情報が返ったときにやること」列を書き換え、実測を取り直す） (2) `checks/task-28.md` §7「本文の書き換えを伴った箇所」への追記と §7-3 の表からの `NTF-MOD-02-1` の除去 (3) `reviews/page-request_data_tool.md`・`reviews/page-master_data_tool.md` の該当箇所への追記 (4) 本 `steering.md` の Task list と State

**Completion criteria**:

- `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-MOD-02-1` が消え、`NTF-SRC-02` のみ2箇所）である
- `tools/request_data_tool.rst` の差分が TODO 3行（と体裁を合わせた空行）の削除だけであり、`:86` の httpDump.bat/httpDump.sh の1文と `:66` の `:download:` 1件は変わっていない
- `tools/master_data_tool.rst` に加わった地の文が B の1件だけであり、書き戻し禁止の2文が本文に無い
- TODO 3件が判定後の文言になっており、3行の書式（1行目に事象・2行目に依頼書のパスと節・3行目に扱い）を保っている
- D の記録4種がすべて更新され、`.rn/` 内どうしの参照が節見出しで書かれている（Rules）
- Docker フルビルドが WARNING・ERROR ともに0件（ゲート7）
- `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS
- 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない

# State

(written by /rn:dn, read and reset to this placeholder by /rn:up. `Status` is `paused` while a
session is suspended — the signal /rn:up and /rn:dn search for — and resets to `not suspended` here,
so only a genuinely suspended session reads `paused`.)

- **Status**: not suspended
- **Date**: YYYY-MM-DD
- **Last completed**: #N description
- **Next**: #N description
- **Notes**: bounded forward pointer — branch/PR, next concrete action, open blockers, user-deferred paths, open questions / pending decisions not yet captured in `design.md`; not a re-narration of the session (that lives in `git log`)
