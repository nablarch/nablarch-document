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
- `#32` 作業指示（`#31` の打ち切り、残TODOの整理、利用側ページの構成物記述の見直し。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-32.md`
- `#32-是正` 作業指示（4観点レビューの有効な指摘11件の処置。user 判断5件の結論を含む。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-32-fix.md`
- `#32-是正2` 作業指示（`#32-是正` が残した user 判断待ち6件の回答。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-32-fix2.md`
- `#32-是正3` 作業指示（`#32-是正2` が残した user 判断待ち5件（A〜E）の回答。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-32-fix3.md`
- `#35` 作業指示（`#32` の是正3 が残した記述の誤り4件の是正。単独で完結）: `.rn/20260724-ntf-yaml-support/ntf-doc-35.md`
- `#35-是正1` 作業指示（`#35` の Step 1 が上げた user 判断待ち2件の回答。§1 の差し替え文の逐語・§2 の「ファイル・メッセージ」の行の是正・§3 の完了条件2 の読み替え）: `.rn/20260724-ntf-yaml-support/ntf-doc-35-fix1.md`
- `#35-是正1` 追補（`#35` の Step 1b が上げた user 判断待ち1件の回答。表の2行の逐語を確定し、是正1 の完了条件3・4 を差し替える）: `.rn/20260724-ntf-yaml-support/ntf-doc-35-fix1-addendum.md`
- `#35-是正2` 作業指示（4観点レビューの A-1〜A-5 を全件成立と認め、`tools/testdata_converter.rst:71` と `implementation/testdata_notation.rst:1544`-`:1547` の逐語を再確定する。記録側の是正・差分限定レビューも同一コミット）: `.rn/20260724-ntf-yaml-support/ntf-doc-35-fix2.md`
- `#35-是正3` 作業指示（**是正ラウンドの上限3回目**。差分限定レビューの `must` 2件を受け、`implementation/testdata_notation.rst:1545` を案B の逐語へ確定する。記録側の是正3件・申し送り1件・差分限定レビューも同一コミット）: `.rn/20260724-ntf-yaml-support/ntf-doc-35-fix3.md`
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
| `nablarch-testing-converter`（`#32` のみ） | `e977824`（`#32` の作業指示 `ntf-doc-32-fix2.md` §5-1 が参照コミットとして指定。上のピン `45194f9` の131コミット後。実測: `git rev-list --count 45194f9..e977824` → `131`、2026-08-21） | — | **上のピンを書き換えるものではない。** `#32` が根拠に使う逐語だけがこのコミットで成立する（`#33` (a) の `XlsFormatReader.java:558-560` を含む）。他タスクの根拠は `45194f9` のまま |
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
- **`git checkout --` にディレクトリを渡さない。戻したいファイルだけを1つずつ指定する。**
  そのパス配下の未コミットの変更が**すべて**消える。2026-08-26 に
  `git checkout -- ja/development_tools/testing_framework/` を実行し、直前に完了していた
  `TODO(NTF-MOD-*)` 2件の削除を、意図していた別作業のやり直しごと巻き戻した（`8ac6e2a` で是正）。
  **やり直したい作業が複数ファイルに及ぶときは、先にその作業だけをコミットしてから
  `git revert` するか、対象ファイルを列挙して `checkout` する。**
- **コミットしたら、メッセージが述べた変更が実物に入っていることを確かめる。**
  上の巻き戻しは、`f31870e` のメッセージが「削除した」と書きながら差分に含まれていない、という形で
  現れた。**コミット直後に `git show --stat` と実物の `grep` で1度なぞる。**
  メッセージを書いた時点の記憶を根拠にしない（`~/.claude/CLAUDE.md`「推測でなく事実で判断する」）
- **見つけた欠陥は、そのタスクの中ですぐ直す。申し送り・先送り・別タスクへの起票をしない**（user 指示 2026-08-26）。よほど大幅な変更でない限り、範囲外を理由に残さない。**いまは解説書を SSoT にするため、解説書に関する残課題と作業を一掃するフェーズである。** `nablarch/CLAUDE.md` 4-1（タスク範囲外の欠陥はそのタスクで直さない）より、この指示が優先する
- **変更したら push する**（user 指示 2026-08-26）。手元だけに置かない。下の「`main` へのマージは user の明示指示があるまで行わない」はマージの話であり、`ntf-yaml-support` への push はこの指示により行う
- **今回の刷新とYAML対応はすべて PR 上で進める。整合したら一斉にマージし、そのあと他の修正も含めてリリースする。判断はすべて PR 上で行い、`main`・`develop` は対象外**（user 指示 2026-08-26）。**各モジュールの事実確認は PR ブランチを参照点にする。`main` を参照点にしない。** `ja/` の `TODO(NTF-MOD-*)` の解除条件も「マージされたら」ではなく「**モジュール側の PR で対応されたら**」とする。2026-08-26 時点の PR ブランチと先端は次のとおり。`nablarch-testing` = `convert-testdata-excel-to-text`（`3c4bd2a`）／`nablarch-testing-yaml` = `feature/ntf-yaml`（`0db2221`）／`nablarch-testing-converter` = `ntf-test-data-converter`（`60d9a2d`）／`nablarch-testing-junit5` = `worktree-fix-resolveTestRules`（`2ebea7e`）／`nablarch-testing-rest` = `fix-testdataparser-usage`（先端未確認）
- **Step 4 では、リリース済みの3モジュールで `src/main` を変更しない**（user 判断 2026-08-26）。対象は `nablarch-testing`・`nablarch-testing-rest`・`nablarch-testing-junit5` の3つ。解説書と実装が食い違い、**解説書側が正しいと判断した場合も**実装を直しに行かず、根拠を添えて報告して止める。理由は、この3つが既にリリース済みであり、実装を動かすと利用者の後方互換が壊れること。**何を直すかは報告を受けた user が決める。** 全件突合（各指示書の §4-2）では `src/test` も変更しない（不一致が疑われる現行挙動を特性テストで固定すると、誤っている疑いのある挙動を正解として確定させることになる）。既に user が扱いを確定済みの項目（`nablarch-testing` の論点4 の特性テスト等）とカバレッジのテスト追加は対象外
  - **未リリースの `nablarch-testing-yaml`・`nablarch-testing-converter` は禁止の対象外で、`src/main` を変更してよい。** 後方互換の対象になる利用者が存在しないため。線引きの根拠はタグの実測（2026-08-26、いずれも full clone）: `nablarch-testing` 17件・最新 `2.2.0`／`nablarch-testing-rest` 7件・最新 `2.0.0`／`nablarch-testing-junit5` 3件・最新 `2.1.0`／`nablarch-testing-yaml` **0件**／`nablarch-testing-converter` **0件**
  - `nablarch-testing` の指示書 `ntf-step4-01-nablarch-testing.md` には反映済み（`87a21d6`）
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
  `tools/request_data_tool.rst:102`）(2) `maven-surefire-plugin`「2.22.0以上」の下限値の出典 —
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
   `tools/request_data_tool.rst:102`）
2. `maven-surefire-plugin`「2.22.0以上」の下限値の出典 — `TODO(NTF-SRC-01)`
   （`setup/junit5_extension.rst:73`）

### #29: モジュール側の判定反映（4事象の確定と TODO 台帳の更新）

**Purpose**: `nablarch-testing`・`nablarch-testing-converter` で確定した判定を解説書に反映し、待つものが無くなった TODO を外して、残る TODO を「何がマージされたら外すか」が分かる状態にする。`#last`（Evaluation sign-off）の承認後に user から届いた追加依頼であり、承認済みの成果に対する差分タスクである。

**根拠（モジュール側の一次情報。両リポジトリとも clone 済みで、Assumptions の参照コミットから `git show <参照コミット>:<path>` で直接読める。以下は 2026-08-19 に実物を開いて確認した）**:

- `nablarch-testing` `8530497:docs/pr75/steering.md` — 4事象の判定（事象1=仕様・解説書側対応／事象2=現状維持／事象3=不具合・#21 で対応／事象4前半=仕様・現状維持／事象4後半の YAML 対応=#22 で対応）は同ファイル `:117`。#21・#22 はいずれも未着手（`:116`「#21 の再現テスト作成から着手」）。**`#21`・`#22` は同ファイル内の rn タスク番号であって GitHub issue ではない。マージ単位はブランチ `convert-testdata-excel-to-text`／ドラフト PR `lovaizu/nablarch-testing#1`（`:4-5`）**
- `nablarch-testing-converter` `b44268c:.rn/ntf-test-data-converter/steering.md` — 同名で拡張子違いの Excel ブックの同居は `XLS-28` として要対応（新規課題・2026-08-18 user 確定）。**`XLS-28` も同リポジトリの rn 課題番号。2026-08-19 実測では `5ab13d8`「fix: 拡張子違いの同名 Excel ブックの同居を辺①の入口で止める（XLS-28）」として実装済みで、ブランチ `ntf-test-data-converter` のみに存在し main 未マージ**

**Steps**:

- [x] A. `tools/request_data_tool.rst` の `TODO(NTF-MOD-02-1)` を3行とも削除する。本文は1文字も変えない（事象1は仕様と判定済み、かつ本文を現行解説書に合わせて据え置くという user 判断による）
- [x] B. `tools/master_data_tool.rst` の `TODO(NTF-MOD-02-4)` の直後に、確定した事象4前半の制約だけを1件書く。ディレクティブの要否は `mapping/style.md` S-06 に従って判断する。`#28` で削除した3文のうち「Excel 形式で記述する」「YAML 形式用のパーサを設定しているプロジェクトでは本ツールを使用できない」の2文は書き戻さない
- [x] C. TODO コメント3件（`NTF-MOD-02-4`・`NTF-MOD-02-3`・`NTF-MOD-01-2`）の1行目・3行目を判定後の文言に更新する。3行の書式は保つ。`.rst` の地の文は B の1件を除いて変えない
- [x] D. 記録を更新する。(1) `checks/task-last.md` §8 の台帳（`NTF-MOD-02-1` の行を削除、残る3件の「判定・情報が返ったときにやること」列を書き換え、実測を取り直す） (2) `checks/task-28.md` §7「本文の書き換えを伴った箇所」への追記と §7-3 の表からの `NTF-MOD-02-1` の除去 (3) `reviews/page-request_data_tool.md`・`reviews/page-master_data_tool.md` の該当箇所への追記 (4) 本 `steering.md` の Task list と State

**Completion criteria**:

- `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-MOD-02-1` が消え、`NTF-SRC-02` のみ2箇所）である
- `tools/request_data_tool.rst` の差分が TODO 3行（と体裁を合わせた空行）の削除だけであり、`:86` の httpDump.bat/httpDump.sh の1文と `:66` の `:download:` 1件は変わっていない
- `tools/master_data_tool.rst` に加わった地の文が B の1件だけであり、書き戻し禁止の2文が本文に無い
- TODO 3件が判定後の文言になっており、3行の書式（1行目に事象・2行目に依頼書のパスと節・3行目に扱い）を保っている
- D の記録4種がすべて更新され、`.rn/` 内どうしの参照が節見出しで書かれている（Rules）
- Docker フルビルドが WARNING・ERROR ともに0件（ゲート7）
- `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS
- 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない

**Verify の結果と user 判断（2026-08-19）**: Steps A〜D は `4ea9498`（本体）・`ec412d4`（レビュー指摘6件の是正）で実施済み。
その後の4観点レビューは4観点とも fail で、指摘は Valid 9件・Escalation 2件（全件・根拠・実測は
`checks/task-29.md` §「トリアージ結果（調整役・2026-08-19）」）。user がこれを受けて処置先を次のとおり定めた。

- **`#30` で処置する** — Escalation E1・E2 の回答と、Valid の V1・V2（`.. important::` の向きと `:ref:` 先）・
  V5（`XLS-28` の状態）・V6（`NTF-MOD-02-4` の TODO 3行目）
- **マージ直前にまとめて処置する（台帳。以後の追加はここへ足す）** — user 指示により今は手を付けない
  - `#29` から — V7（「本作業ディレクトリからは参照できない」が誤り。記録5箇所）・V8（`checks/task-last.md` §5-5 の
    「`web.rst` は `#29` では変更していない」が誤り）・V9（`#29` の行数変動でずれた `ja/` への `file:line` 13件。
    `mapping/style.md` 10行11件・`mapping/glossary.md:314`・`design.md:379`）と `checks/task-29.md` 自身の
    Self-check Evidence 3箇所（全件は `checks/task-29.md` §「トリアージ結果（調整役・2026-08-19）」）
  - `#30` から（`/rn:gm` 2026-08-19 の user 指示で追加） — `reviews/page-master_data_tool.md` の2箇所
    （設計 M-2 の行と「判断待ち」の 7）が `.. important::` を「パーサと形式が食い違う」＝双方向と説明したままで、
    `#30` で確定した向き（Excel 形式のファイル＋YAML 形式用のパーサ）だけに限定した現物と食い違う
  - `#30` から（同上） — `tools/testdata_converter.rst` に `TODO(NTF-MOD-01-3)` を新設したため `:62` 以降が
    一律4行下がり、`.rn/` 内の `file:line` がずれた（実測 2026-08-19: 「機能概要」`:12`・「前提事項」`:61` は不変、
    「導入」`:73`→`:77`、`<plugin>` 追加 `:77-89`→`:81-93`、`<dependency>` 追加 `:91-100`→`:95-104`、
    「使用方法」`:102`→`:106`、その導入部の `:ref:` `:104`→`:108`、`bash` の code-block `:130`→`:134`、
    「前提事項」節の範囲 `:61-69`→`:61-73`）。ずれている記録は `mapping/style.md:112`・`:273`・`:322` と
    `design.md:379`・`:381`
  - `#30` から（`/rn:ty` 2026-08-19 の user 指示で追加） — `checks/task-30.md` §「Verification Expert (fact-check)」の
    「Artifact actually checked」の行（指摘1）が、処置を「→ `b44268c` と但し書きに戻した」と書いたままで、
    `/rn:gm`（2026-08-19）で差し戻されて実物は `3ecf3db` が正となったことが同ファイルに無い。打ち消しの注記は
    本 `steering.md` §「#30: `#29` のレビュー指摘の処置（user 判断 2026-08-19 の反映）」の「`/rn:gm`（2026-08-19）の
    処置5件」(3) にあるが、`checks/task-30.md` 単体では台帳が今も `b44268c` を引くと読める。マージ直前に同行へ
    打ち消しの注記を足す
- **未処置のまま残る** — V3（`implementation/deal_unit_test/mom.rst` の `TODO(NTF-MOD-02-3)` 1行目に禁止語「不具合」）と
  V4（`#21`・`#22`・`XLS-28` が GitHub issue 番号のように読める）。`#30` の作業指示は前者に触れず、
  後者は差し替え文面が現行の書き方を踏襲しているため、いずれも判断を user に返す

### #30: `#29` のレビュー指摘の処置（user 判断 2026-08-19 の反映） — DONE

**Purpose**: `#29` の4観点レビューで挙がった指摘のうち user が今回の対象と定めた4件と、Escalation 2件への回答を、解説書へ反映する。

**根拠（user が作業指示に引用した、レビュー役が実物で確認した一次情報）**:

- `nablarch-testing` `65911f5` — `src/main/script/httpDump.sh` は存在するが、`pom.xml` に `src/main/script` を成果物へ取り込む設定が無く配布物に入らない。解説書側の配布物は `httpDump.bat` の1件のみ。読者が `httpDump.sh` を入手する手段は無い
- 同 `65911f5:docs/pr75/steering.md:107` — 「Excel形式＋YAML用パーサという取り違えケースの挙動（無言0件）は変更されていない」。**確定しているのはこの向きだけで、逆向き（YAML形式のファイル＋Excel用パーサ）は未確認**
- 同 `:25` — 「新事象（期待値0件テーブルの偽陰性）：…形式共通の2問題を本体で修正する（#23・#24）」。起票済み・未着手
- `nablarch-testing-converter` `3ecf3db:.rn/ntf-test-data-converter/coverage/issues.md:2562`（宛先に解説書担当が明記された申し送り） — 「0 件テーブル（YAML の `rows: []` を持つテーブル系エントリ。`setup_tables`・`expected_tables` など）を含む YAML は、Excel へ変換できない」「解除条件: 本体（`nablarch-testing`）の `TableDataParser` が…読めるようになり、辺③を『識別子行だけを書く』実装へ切り替えたとき」

**Steps**:

- [x] 1. `tools/request_data_tool.rst` の起動用スクリプトを選ぶ手順を `* 配置した起動用スクリプト(httpDump.bat)を選ぶ。` に改める（E1 の回答）。**「Windows専用」とは書かない**（断定できる一次情報が無い）。現行解説書（`2e501ad:.../02_SetUpHttpDumpTool.rst:91-92`）にある記述を落とす変更であるため、user 判断として記録に残す
- [x] 2. `tools/testdata_converter.rst`「前提事項」節の本文直前に `TODO(NTF-MOD-01-3)` を新設する（E2 の回答）。**本文には制約を書かない**（`ntf-doc-28-decide-disposition.md` §7「モジュール判定待ちの箇所の書き方」の決定による）
- [x] 3. `tools/master_data_tool.rst` の `.. important::` を、確定している向き（Excel形式のファイル＋YAML形式用のパーサ）に限定する（V1）。`:ref:` 先は現在の `testing_framework_common` が根拠にならないため、実物で確認して差し替える（V2）。逆向きは未確認なので書かない。文言は `mapping/style.md` S-06・S-13 に合わせる
- [x] 4. `tools/master_data_tool.rst` の `TODO(NTF-MOD-02-4)` 3行目を、`:10`・`:128`・`:130` の Excel 前提の記述を直す指示に改める（V6）。あわせて 3 の `.. important::` が `#22` マージ後も残るかを判断し、残らないならこの TODO の対象に含め、判断と理由を報告する
- [x] 5. `tools/testdata_converter.rst` の `TODO(NTF-MOD-01-2)` 1行目の `XLS-28` の状態を「実装済み（`5ab13d8`、`main` 未マージ）」に改める（V5）。3行目はそのまま
- [x] 6. 記録を更新する。(1) `checks/task-last.md` §8 の TODO 台帳に `NTF-MOD-01-3` を追加し、`NTF-MOD-01-2` の状態を更新して実測を取り直す (2) `reviews/page-request_data_tool.md` に 1 の本文変更を user 判断として追記する (3) 本 `steering.md` の Task list と State。**それ以外の記録整備は行わない**（`.rn/` の行番号ずれ・self-check の不整合はマージ直前にまとめて処置する。user 指示）

**Completion criteria**:

- `ja/` 配下の `TODO(NTF-` が **14件・13ID**（`NTF-MOD-01-3` が増え、`NTF-SRC-02` のみ2箇所）である
- `git ls-tree -r --name-only HEAD | grep -i httpdump` の出力に `httpDump.sh` が0件である（`httpDump.bat` は `ja/` と `en/` に各1件。残りは `en/` に残る旧ガイドのディレクトリ名 `01_HttpDumpTool` へのヒット。条件文は `/rn:gm`（2026-08-19）の user 指示で差し替え）
- `tools/request_data_tool.rst` に `httpDump.sh` が0件で、かつ「Windows専用」の趣旨の記述が無い
- `tools/master_data_tool.rst` の `.. important::` が Excel形式のファイル＋YAML形式用のパーサの向きだけを述べており、`:ref:` 先が実在し、飛び先に `testDataParser` の記述がある
- TODO 4件が3行の書式（1行目に事象・2行目に出典・3行目に扱い）を保っている
- Docker フルビルドが WARNING・ERROR ともに0件（ゲート7）
- `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS
- 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない

**Verify の結果（2026-08-19）**: 4観点とも独立サブエージェントで実施し、**4観点とも fail**。重複を除いた指摘を調整役が実物で確認し、11件を是正した（詳細と実測は `checks/task-30.md`）。是正後の再検証はゲート7を含めて全 PASS。

- **是正した主なもの** — (1) 台帳 `NTF-MOD-01-2` の出典が、確認した記録の無い `3ecf3db:…/steering.md` に書き換えられ但し書きも消えていた（4観点中3観点が独立に検出）→ `b44268c` と但し書きに戻した（**この判断は `/rn:gm`（2026-08-19）で差し戻された。実物は `3ecf3db` が正。下の「`/rn:gm`（2026-08-19）の処置5件」の (3)**）。(2) `TODO(NTF-MOD-02-4)` 1行目と台帳の同行が双方向のまま残り、`.. important::` の限定と矛盾していた → 確定した向きに揃えた。(3) `.. important::` が症状だけを述べ、`:ref:` 先も主張を裏付けていなかった → 規範先行に書き換え、`setup/request_unit_test/rest.rst:63` の先例にならって「`testDataParser` の記述例は… を参照」に限定した。(4) 存在しない節（`ntf-doc-28-decide-disposition.md`「本文の書き換えを伴った箇所」）を出典に挙げていた → §7 に直した（本 `steering.md` の Step 2 にも同じ誤りがあった）。(5) `reviews/page-request_data_tool.md` が旧状態の証拠として引く `:82` を `561c1ab:…:82` にコミット固定した
- **Step 4 が求めた判断** — `.. important::` は `#22` マージ後も**残る**が、その時点で書き直しが要るため `TODO(NTF-MOD-02-4)` 3行目の対象に**含めた**。理由は `checks/task-30.md` §「Step 4 が求めた判断」
- **`/rn:gm`（2026-08-19）の処置5件** — user が判断待ち4件をすべて「指摘のとおり」（指示文面の誤り）と裁定し、次を是正した。 (1) `TODO(NTF-MOD-02-4)` 3行目を、同一ファイル内の行番号指し（`:10`・`:128`・`:130`）から条件指しに変え、落ちていた配布物一覧の `MASTER_DATA*.xls` と「シート」も対象に含めた (2) `TODO(NTF-MOD-01-3)` 1行目と台帳から、本リポジトリに出典の無い converter 側の内輪の呼称を落とした (3) 台帳 `NTF-MOD-01-2` の出典を `3ecf3db:.rn/ntf-test-data-converter/steering.md:1203` に統一し、但し書きを「レビュー役が実物で確認して引用（`#30` 差し戻し）」と逐語の引用に改めた（`#30` で `b44268c` へ戻した判断は、そちらから検証できない以上プロセスとしては正しいが事実としては逆で、`b44268c:…:1120` は `- [ ]`、`3ecf3db:…:1203` は `- [x]` ＋ `5ab13d8`。user が両コミットを実物で確認した） (4) Completion criteria の `grep -i httpdump` の条件文を実測（11行。`httpDump.sh` 0件・`httpDump.bat` 2件・残り9件は `en/` の `01_HttpDumpTool`）に合う書き方へ差し替えた（本 Completion criteria と `checks/task-30.md` の2箇所） (5) マージ直前の一括処置の台帳（`#29` の「Verify の結果と user 判断」）に、`reviews/page-master_data_tool.md` の2箇所と `tools/testdata_converter.rst` の行番号ずれを追加した。**この2件は user 指示により今回は直していない**
- **`/rn:up`（2026-08-19）の処置2件** — `/rn:gm` の報告で残していた user 判断待ち2件を、user がどちらも「いま直す」と裁定し、次を是正した。 (1) `checks/task-30.md` の各表の Evidence 欄が引く `ja/` の `file:line` を `e023648a` 時点の現物に合わせ、案件ルール「事実には `file:line` と参照コミットハッシュを必ず添える」に従って測定時点を各行に明記した（節冒頭に基準を1行置き、該当6行に注記）。`ja/` は `e023648a`〜`4620c43` で無変更であることを md5 で確認したうえで実測した。番号の付け替えだけでは再発するという user 指摘への処置がこの明記である (2) 台帳 `NTF-MOD-01-3` の「2段目」の出典を `b44268c:.rn/ntf-test-data-converter/steering.md` から `3ecf3db:.rn/ntf-test-data-converter/steering.md:867` に差し替え、`NTF-MOD-01-2` と同じ形（逐語の引用＋「レビュー役が実物で確認して引用」）にした。同じ行が既に引く `3ecf3db:…/coverage/issues.md:2562` とコミットが揃う。user が両コミットを実物で確認し、逐語が同一であることを確認した。**(1) で user 指示に無い是正4件を追加した**（`tools/master_data_tool.rst:32` の逐語が是正前のもののまま、`setup/class_unit_test.rst` の節見出しが `:132` ではなく `:133`、`setup/junit5_extension.rst` の先例が `:70-71` ではなく `:71-72`、`checks/task-30.md` の「新設 TODO の前後には空行を各1行置いた」が現物と食い違う（`c650039` で下線直後の空行を削除済み））。いずれも Evidence 欄が引く `ja/` の記述であり、測定時点を `e023648a` と明記する以上そのままでは虚偽になるため直した。なお `:111-113`→`:110-112` は user 指示に含まれており、上の4件には数えない

**Closed**: user review 承認済み（`/rn:ty`、2026-08-19）。user が `97ecf31` を取得し、レビュー役が `ja/` の現物で
`/rn:up`（2026-08-19）の是正2件を独立に確認して全件一致した（`tools/master_data_tool.rst:32` の逐語、
`setup/class_unit_test.rst` の `:131` ラベル・`:133` 見出し・`:134` 下線、`setup/junit5_extension.rst` の `:71` 見出し・
`:72` 下線、`tools/testdata_converter.rst` は `:62` の下線直後から `:63-65` で `:66` が空行）。**user 指示に無い是正4件は
いずれも「直して正解」と裁定された。** `checks/task-30.md` の検証4件と、書き足した「`e023648a` 時点は直結164 / 空行0」も
レビュー役の独立走査で再現した。`## Method` 節を対象外とした判断も、同節が引く3件
（`setup/class_unit_test.rst:131`・`setup/request_unit_test/rest.rst:63`・`tools/request_data_tool.rst:82`）が現物で
正しいため実害なしと認められた。**あわせて user 指示により、マージ直前の一括処置の台帳（`#29` の
「Verify の結果と user 判断（2026-08-19）」）へ1件を追加した**（`checks/task-30.md` の指摘1 の行が `/rn:gm` の差し戻しを
反映していない件）。`ja/` と `.rn/` へのそれ以外の変更は不要と指示された。

### #31: `TODO(NTF-MOD-01-1)` の解消と「空エントリ」の記述の是正（user 判断 2026-08-20 の反映）— DONE

**Purpose**: `tools/testdata_converter.rst` の2点を直す。(1) 往復非可逆の判定が返ったため `TODO(NTF-MOD-01-1)` を削除する。(2) 中間モデルが保持しない「空エントリ」を「無損失で保持する」側に挙げている記述を是正する。

**根拠（user が作業指示に示した判定と、本リポジトリで確認できる一次情報）**:

- **(1) の判定（user 確定・2026-08-20）** — 往復で観測された3事象はいずれも判定済みである。(a) 全カラム空文字の行が消える → `nablarch-testing-converter` の課題 `XLS-05`。判定「対応不要（記法が明文で定めている挙動）」。(b) `- {}` が増減する → 同じ明文による。(c) 0件テーブルが直後のブロックを取り込む → 課題 `XLS-27`。判定「要対応」。修正済みで、残る制約は既に `TODO(NTF-MOD-01-3)` が保持している。3事象の観測記録と (a)(b)(c) のラベルは `ntf-mod-01-nablarch-testing-converter.md` §2（`:53`・`:73`・`:77`）にある。`reviews/page-testdata_converter.md` §「判断待ち（`decide`）」1 にあるのは (a) 相当と (b) の2事象だけで、(c) は無い（`#31` のレビュー4観点が独立に検出。調整役が実物で確認）
- **(2) の根拠（本リポジトリの一次情報）** — `ja/development_tools/testing_framework/implementation/testdata_notation.rst:1534`（`65a1756`）が「全要素が\ null\ または空文字のエントリは読み飛ばされる。Excel\ では行の全セルが空の場合、YAML\ では ``rows:``\ 内の要素が空マッピング（\ ``{}``\ ）またはすべての値が空文字の場合にスキップされる。」と定めている。読み飛ばしを実行するのは本体の `PoiXlsReader#isBlankLine`（L140-147）であり、変換ツール側に判断の余地は無い（`nablarch-testing-converter` の課題 `XLS-05` の判定より。同リポジトリは本作業ディレクトリの外にあるため読みに行かず、user が作業指示に示した内容による）。したがって空エントリは中間モデルに保持されない

**Steps**:

- [x] 1. `tools/testdata_converter.rst:22-25` の4行（`TODO(NTF-MOD-01-1)` 3行＋直後の空行1行）を削除する。削除後、tip 本文と「意味を変えずに往復できる」見出しの間に空行が1行だけ残ること。**本文は1文字も変えない**（判定が「あるべき姿（往復しても内容が保たれる）のとおり」であるため、注意書きの追加も不要）
- [x] 2. 同ファイルの表「意図のある情報」の行から「データブロックの内側にある空エントリ、」を削除する。**「マーカーカラム」「空欄のレコード種別」は検証していないためそのまま残す**（user 指示）
- [x] 3. 記録を更新する。(1) `checks/task-31.md` に2点を根拠付きで記録する (2) `checks/task-last.md` §8 の TODO 台帳から `NTF-MOD-01-1` の行を外し、実測を取り直す (3) `checks/task-28.md` §7-3 の表から `NTF-MOD-01-1` を外す（`#29` が `NTF-MOD-02-1` で確立した運用。同 `:461`） (4) 本 `steering.md` の Task list と State。**それ以外の記録整備は行わない**（`.rn/` の行番号ずれ・過去の記録との食い違いはマージ直前にまとめて処置する。`#30` Step 6 の user 指示を継続適用）

**Completion criteria**:

- `grep -rn 'NTF-MOD-01-1' ja/` が0件である（依頼書 `ntf-doc-28-decide-disposition.md` 側の記述は残してよい）
- `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-SRC-02` のみ2箇所）である
- `tools/testdata_converter.rst` の tip 本文と「意味を変えずに往復できる」見出しの間の空行が1行である
- 同ファイルの「意図のある情報」の行が「無損失で保持する。マーカーカラム、空欄のレコード種別が該当する」である
- 上記2点以外に `ja/` の差分が無い。**本文を1文字も変えていない**ことを、`git diff --numstat <開始コミット>..HEAD -- ja/` が `1	5`（追加1・削除5）であることで測る。削除5の内訳は TODO 3行＋直後の空行1行＋「意図のある情報」1行の置換分であり、置換の削除1行は追加1行と対になる
- `checks/task-last.md` §8 の台帳が13行・12ID で、削除した行が持っていた出典（依頼書 `ntf-mod-01-nablarch-testing-converter.md` §2・`checks/task-28.md` §7-3・`ntf-doc-28-decide-disposition.md` §7-2）が削除記録の段落に引き継がれている
- `checks/task-28.md` §7-3 の表から `NTF-MOD-01-1` が外れている（`#29` が `NTF-MOD-02-1` で確立した運用。同 `:461`）
- 台帳と `checks/task-28.md` §7-3 が指す `checks/task-31.md` が、`#31` の check-off コミットでブランチに入る。rn の運用上、check ファイルは実装担当が書き調整役が check-off コミットで staging するため、台帳を直したコミットとは別コミットになる（`task-execute-workflow.md`「Check file format」の "The expert does not commit it. The coordinator … commits the file … on the post-Verify steering check-off commit."）。したがって中間コミット単体ではポインタが解決しない
- Docker フルビルドが WARNING・ERROR ともに0件（ゲート7）
- `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS
- 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない

### #32: `#31` の是正打ち切りと、残TODOの整理、利用側ページの構成物記述の見直し（user 指示 2026-08-21）— DONE

**Purpose**: 3つを片づける。(1) `#31` が残した未決点を `tools/testdata_converter.rst` の本文で解消する。(2) 一次情報が揃った残TODO 4件（`NTF-MOD-02-2`・`NTF-SRC-01`・`NTF-SRC-02`・`NTF-FIG-01`〜`04`）を外し、`NTF-MOD-03-1` の文言を実状に合わせる。(3) 利用側ページから、利用者がNTFの内部の作りを知る必要のない記述（UMLクラス図7件・「主なクラスとリソース」表の7行）を落とす。

**指示書**: `.rn/20260724-ntf-yaml-support/ntf-doc-32.md`。手順1〜8の対象行・変更前後の文面・一次情報の逐語はすべて同ファイルにある。**モジュール側リポジトリは作業ディレクトリの外にあるため見に行かない**（必要な一次情報は指示書に逐語で引用されている）。

**Steps**:

- [x] 0. `#31` を閉じる（`checks/task-31.md` の誤記5件を削り、指摘1・2・4 を `#30` Step 6 へ送り、指摘5 を処置不要と記す。`#31` を check-off する）— `1618faf` で完了
- [x] 1. `tools/testdata_converter.rst` の `:37`・`:39` を書き換え、`:67` の直後に「前提事項」の段落を1つ足す。根拠の逐語3組を `checks/task-32.md` に記録する（指示書 §1）—— 該当段落は是正・是正2・是正3 で `b3e76fc`・`811d1cb`・`5c2c26f`・`4d0a48a` と4度動いた。最終形は是正3指示 §1 の逐語による
- [x] 2. `setup/request_unit_test/rest.rst` の `TODO(NTF-MOD-02-2)` を外し、jar の実測を `checks/task-32.md` に記録する（指示書 §2）
- [x] 3. `setup/junit5_extension.rst` の `TODO(NTF-SRC-01)` を外し、JUnit 5.3.0 リリースノートと Surefire 2.22.0 告知の逐語を `checks/task-32.md` に記録する（指示書 §3）
- [x] 4. `setup/request_unit_test/web.rst` の5行と `tools/request_data_tool.rst` の1行を書き換え、`TODO(NTF-SRC-02)` 2箇所を外す。出典と「Open With」の扱いを `checks/task-32.md` に記録する（指示書 §4）
- [x] 5. 利用側ページの構成図を全廃する。`TODO(NTF-FIG-01)`〜`04` の4ブロックと、残る `.. image::` 3件、および図に言及する本文2箇所を削る（指示書 §5）
- [x] 6. 参照されなくなった画像・作図元 9ファイルを削除する。`en/` 配下の同名ファイルは削除しない（指示書 §6）
- [x] 7. 「主なクラスとリソース」の表から7行を削り、本文4箇所から同じクラス名を落とす（指示書 §7）
- [x] 8. `setup/junit5_extension.rst:400-402` の `TODO(NTF-MOD-03-1)` の文言を実状に合わせる。TODO 自体は残す（指示書 §8）
- [x] 9. `checks/task-32.md` に、手順1〜8の後の TODO 台帳を節見出し方式で作り、`grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ | sort | uniq -c` の実測を貼る（指示書 §9）

**是正 Steps**（4観点レビューの有効な指摘11件。指示書 `ntf-doc-32-fix.md`。手順1〜5・7 の check-off はここが片づいてから行う）:

- [x] 10. `tools/testdata_converter.rst` の `:39` から「空エントリ」を削り、`:69` の段落を差し替える。`:278` は触らず `checks/task-32.md` に1行記録する（是正指示 §1）— `811d1cb`。**判断待ち1・2 が同じ `:39` を再度動かしうる**
- [x] 11. `about/index.rst:106` の2文目の直後に、NAF が読み取るコンポーネント設定ファイル／環境設定ファイルの入手先を指す1文を挿入する（是正指示 §2）— `811d1cb`
- [x] 12. `design.md` に節「利用側ページに内部構造の構成図を置かない」を新設し、既存節 `:137` の見出しと末尾段落を実態に合わせる（是正指示 §3-1・§3-2）— `811d1cb`、過剰主張の是正は `f8f74f2`
- [x] 13. マッピング台帳7行（`current-0165`・`0182`・`0200`・`0281`・`0295`・`0308`・`0322`）の `note` に `#32` のポインタを追記する。`_batch/*.csv` を直してから `mapping.csv` を作り直す（是正指示 §3-3）— `811d1cb`。**判断待ち4b が6行を追加しうる**
- [x] 14. `implementation/request_unit_test/web.rst`・`rest.rst` のリード文を揃え、`AbstractHttpRequestTestTemplate` を落とし、`SimpleRestTestSupport` を足す（是正指示 §4）— `811d1cb`
- [x] 15. 判断なしで直す6件を直す（`mom.rst:28`・`web.rst:48`・`mom.rst:22`・`junit5_extension.rst:73`・`web.rst:186`、および `checks/task-32.md` の jar の記録）（是正指示 §5）— `811d1cb`。`mom.rst:30` の行頭 `\ ` は `f8f74f2` で追加是正
- [x] 16. `steering.md` に `#33` を新設する。中身の作業はしない（是正指示 §6）— `/rn:up` の再開時に調整役が実施

**是正 Completion criteria**（是正指示「完了条件」の逐語）:

1. `grep -n '空エントリ' ja/development_tools/testing_framework/tools/testdata_converter.rst` が0件
2. `grep -n 'マーカーカラム' ja/development_tools/testing_framework/tools/testdata_converter.rst` が `:39`・`:69`・`:278` の3件（`:37` に無い）
3. `grep -n 'testing_framework_setup' ja/development_tools/testing_framework/about/index.rst` が1件
4. `grep -c 'AbstractHttpRequestTestTemplate' ja/development_tools/testing_framework/implementation/request_unit_test/web.rst` が0
5. `_batch/*.csv` を昇順に連結（先頭のみヘッダ込み、2つ目以降はヘッダ除く）した結果が `mapping/mapping.csv` とバイト一致する。`csv.DictReader` の行数が編集前と同じ597行
6. `design.md` に `### 利用側ページに内部構造の構成図を置かない` が存在し、`:137` の見出しが `### 「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない` になっている
7. `steering.md` に `#33` のエントリが存在する
8. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
9. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
10. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
11. Docker フルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する
12. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない
13. `checks/task-32.md` に §1-3（`:278`）・§3-3（台帳7行）・§5（jar の実測）の記録がある
14. `#32` が check-off されている

**是正2 Steps**（`#32-是正` が残した user 判断待ち6件の回答。指示書 `ntf-doc-32-fix2.md`。**手順1・5・7 と是正 Steps の残りの check-off はここが片づいてから行う**）:

- [x] 17. 判断1（空エントリ）は現状維持。`tools/testdata_converter.rst:39` の空エントリ・「データブロックの外側にある」を触らない。推奨を採らなかった理由を `checks/task-32.md` に記録する（是正2指示 §1）
- [x] 18. 判断2（行末の空セル）。`:39` から「行末の空セル」を落とし、`:69` の直後に前提事項の1段落を足す（是正2指示 §2）
- [x] 19. 判断3（継承クラス）。`implementation/request_unit_test/mom.rst:142-143` を `BatchRequestTestSupport`・`BasicHttpRequestTestTemplate` へ差し替える。jar 実測の逐語と、`#33` へ送らなかった理由を `checks/task-32.md` に記録する（是正2指示 §3）
- [x] 20. 判断4(a)。表の採否基準を `design.md:139` の節に明文化し、6ページへ当てて10行を落とす。`TestDataConverter` ほか「落とさない行」の判定根拠を `checks/task-32.md` に記録する（是正2指示 §4）
- [x] 21. 判断5。`reviews/page-testdata_converter.md` に出典と実装の食い違い3件を記録する（是正2指示 §5-1）
- [x] 22. 判断4(b)。マッピング台帳6行（`current-0201`・`0282`・`0296`・`0309`・`0323`・`input-0184`）の `note` に `#32` のポインタを追記する。`_batch/*.csv` を直してから `mapping.csv` を作り直す（是正2指示 §5-2）
- [x] 23. 判断6。`#33` に (c) `markerColumnColor` の説明不足を足し、見出しを改める（是正2指示 §6）
- [x] 24. 検証。`verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` と Docker フルビルド。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`（是正2指示 完了条件10〜13）。**`docker build` からのイメージ再作成は `#34` へ分離し、既存イメージでのフルビルドを完了条件13 の代替とする**（`#32` のレビュー是正、2026-08-21）。理由と失敗ログの所在は `steering.md` `#34`「`#32` の完了判定との関係」。—— Steps 17〜24 は `5c2c26f` で実施し、4観点レビュー3ラウンドの有効指摘27件を `72275f2`・`14053b5`・`456544e` で是正した。判定と triage は `checks/task-32.md` §「4観点レビューの判定（是正2。調整役が記入。2026-08-21）」。

**是正2 Completion criteria**: 是正2指示 `ntf-doc-32-fix2.md`「完了条件」1〜16 の逐語による（上の「是正 Completion criteria」2 と「Completion criteria」の「マーカーカラム」2件の条件は、是正2 の §2-2 が段落を1つ足すため、是正2 完了条件1・2 に置き換わる）。最終判定は下の「是正3 Completion criteria」に置き換わる。

**是正3 Steps**（`#32-是正2` が残した user 判断待ち5件（A〜E）の回答。指示書 `ntf-doc-32-fix3.md`。**`#32` 全体の check-off はここが片づいてから行う**）:

- [x] 25. 判断A・B・C・D・E を反映する。`tools/testdata_converter.rst:71` の因果と適用範囲（指示書 §1）、`reviews/page-testdata_converter.md` の残差処理と適用範囲（同 §2）、`#33` (d) の申し送り（同 §3）、`design.md` §「利用側ページに内部構造の構成図を置かない」への `9031fa6` の7行の記録と台帳5行の `note`（同 §4）、`#34` の未決点への方針（同 §5）、`.rn/` 内相互参照の節見出し化（同 §6）— `4d0a48a`
- [x] 26. 4観点レビュー2ラウンドの有効指摘31件を `1ccfc53`・`6946fa1` で是正する。落とした7行の役割の残り方を 5行/2行 に直し、`#33` (d) に `BasicHttpRequestTestTemplate` を足し、表の行数についての排他の主張と、帰属先についての主語の無い断定を除く。判定と triage は `checks/task-32.md` §「4観点レビューの判定（是正3。調整役が記入。2026-08-21）」

**是正3 では、指示書の記述3件を実測に合わせて変えた**（7行の分類・引用の行番号・呼び出し元の数）。指示どおりに書くと `.rn/` 内の文書に事実でない記述が入るためで、3件の内容・逐語・実測は `checks/task-32.md` §「4観点レビューの判定（是正3。調整役が記入。2026-08-21）」にある。

**是正3 Completion criteria**: 是正3指示 `ntf-doc-32-fix3.md`「完了条件」1〜14 の逐語による。**このタスクの最終判定はこの14件で行う**（本エントリの他の Completion criteria は、是正3 が同じ箇所を再度動かすため、この14件に置き換わる）

**Completion criteria**（指示書「完了条件」の逐語）:

- `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ | sort | uniq -c` の結果が5件・5ID になる（`NTF-MOD-01-2` / `NTF-MOD-01-3` / `NTF-MOD-02-3` / `NTF-MOD-02-4` / `NTF-MOD-03-1` の各1件）
- `tools/testdata_converter.rst` に「意図のある情報」の行として「無損失で保持する。空欄のレコード種別が該当する」があり、「マーカーカラム」は「意味を持たない情報」の行にだけ現れる。`grep -n 'マーカーカラム' ja/development_tools/testing_framework/tools/testdata_converter.rst` のヒットが「意味を持たない情報」の行と「前提事項」の新段落の2件だけになる
- 削除した9ファイルへの参照が `ja/` 配下に残っていない。`grep -rn 'batch_request_test_class\|real_request_test_class\|send_sync\|rest_request_unit_test_structure\|request_unit_test_structure\|class_structure\|abstract_structure' ja/` の結果が0件
- `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
- `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
- `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
- Docker でフルビルドし、`grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を必ず実行する
- `checks/task-32.md` に、手順1-3・2-2・3-2・4-3 の記録と、手順9の台帳がある
- `#31` が check-off されている（手順0）

### #33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検、「主なクラスとリソース」の表の載せる側の不揃い、`.rn/` の相互参照と役割記載の積み残し

**Purpose**: `#32` の是正で対象外とした記述課題5件を片づける。(a) マーカーカラム除外と空エントリ判定の適用順序を `implementation/testdata_notation.rst` に明文化する。(b) `ja/` 配下に残した図から `glossary.md` の禁止語を排する。(c) `tools/testdata_converter.rst` の `markerColumnColor` の説明が、着色の対象を限定していない点を直す。(d) 「主なクラスとリソース」の表の「載せる側」が6ページで揃っていない点を決める。(e) `#32` が範囲外とした2件 —— `.rn/` 内の相互参照の節見出し化の残りと、落とした行の役割を本文に残す規範を明文化前の7行へ遡って当てるかどうか —— を決める。

**処置状況（2026-08-24。`残作業-rst修正.md` による）**:

- **(a) 処置済み。** `implementation/testdata_notation.rst:1545` の段落末尾に2文を足し、`Excel` 形式では空エントリ判定がマーカーカラム除外の**前**に行われること、その結果マーカーカラムだけに値があるエントリは読み飛ばされないことを明文化した。下の未決点（「除外 → 空エントリ判定」と書くか）は、**実測どおり「空エントリ判定 → マーカーカラム除外」と書く**で決着した（`design.md` §8「出典と実装が食い違う場合は実装を優先する」を適用）。**本体の順序を変えるかどうかは解説書の範囲外であり、モジュール側の課題として残る。** 記録は `reviews/page-testdata_notation.md` §「`#35`-是正6 ／ `#33` (a) 空セル記述の書き直し（2026-08-24）」
- **(c) 処置済み。** `tools/testdata_converter.rst:280` を、着色対象が `XlsFormatWriter` の合成するマーカーカラム（`[EMPTY]`）に限られる旨の説明に差し替えた。記録は `reviews/page-testdata_converter.md` §「`#35`-是正6 ／ `#33` (c)（`:71` と `:280` の修正、2026-08-24）」
- **(d) クローズ（変更しない）。** 読み手の理解を妨げていない。両ページとも「リクエスト単体テストクラス」行の作成単位欄が「テスト対象クラス（Action）につき1つ作成する。」と明示している。加えて、行を足すと作成単位欄に書く事実が無い（`batch.rst`・`mom.rst` とも「取引」の語が0件で、`web.rst:34`・`rest.rst:36` の「取引につき1クラス」を当てられない）。事実として書けないものを埋めるより、書かない方がよい
- **(e-2) クローズ（変更しない）。** `AbstractHttpRequestTestTemplate` の役割は `setup/request_unit_test/web.rst:229` に残っている。`StandaloneTestSupportTemplate` は `ja/` 配下のどこにも現れないため、読み手がその役割を知る必要がある場面がない
- **(e-3) クローズ（変更しない）。** `design.md` の当該節が「リード文または本文」を許しており規約違反ではない。揃えるには `design.md` の改訂が要るが、`design.md` は変更禁止ファイルである
- **残るのは (b) 残置図の禁止語（`ja/` 配下の png 26枚の点検と差し替え。画像作成を伴う）と (e-1) `.rn/` 内の相互参照の節見出し化のみ。** 別に `#34` が残る

**背景と未決点**:

- **(a) XLS-08 の記法明文化（converter からの申し送り）** — converter は解説書側へ明文化を申し送っている。`nablarch-testing-converter@e977824` の `src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:558-560` 逐語（`:557` は `<p>`。Assumptions のピン `45194f9` では同じ行が `deduplicateColumnNames` の実装であり、この逐語は成立しない。いずれも 2026-08-21 に `git show` で実測）:

  > 記法は 2 つの規則の前後関係を定めていない。「除外 → 空エントリ判定」を前提とする（ユーザー確定・2026-08-18。解説書側へ明文化を申し送る）。課題は {@code coverage/issues.md} の XLS-08 に記録している。

  **未決点**: NTF 本体は現在**逆順**で動いている。`nablarch-testing-converter@e977824` の `.rn/ntf-test-data-converter/coverage/issues.md:493-494` 逐語（2026-08-21 に `git show` で実測。1巡目までの `:499` は作業ツリーを行番号で指した誤り）:

  > **原因は適用順序である。** 現状は**空エントリ判定をマーカーカラム除外の前に**行っている（本体 `PoiXlsReader#readLine` が生の行で判定 → `TableDataParser#onReadLine` が除外）。

  したがって `implementation/testdata_notation.rst` に「除外 → 空エントリ判定」と書くことは、NTF 本体の不具合を宣言することと同じである。他の `TODO(NTF-MOD-*)` と同じ判定を要する。着手時に user の判定を仰ぐ。

- **(b) 残置図の禁止語** — `implementation/request_unit_test/images/mom/send_sync_base.png` に、`glossary.md` が禁止する「自動テストフレームワーク」のノードが2つある（2026-08-21、user が画像を開いて確認）。`ja/` 配下の png は26枚あり、同種の全点検が要る。差し替え図の作成を伴う。

  あわせて線引き（内部クラス構造を示す図は落とす／テスト範囲・作業の流れを示す図は残す）を `design.md` §「利用側ページに内部構造の構成図を置かない」に追記する。

- **(c) `markerColumnColor` の説明不足** — `tools/testdata_converter.rst` の `markerColumnColor`（`#32` の是正2 適用後は `:277`・説明は `:280`「マーカーカラムの背景色」）が着色するのは、`XlsFormatWriter` がカラム名0件のデータブロックに合成するマーカーカラムだけである（`nablarch-testing-converter@e977824` の `src/main/java/nablarch/test/tool/converter/xls/XlsFormatWriter.java:543` 逐語: `static final String EMPTY_BLOCK_MARKER_COLUMN = "[EMPTY]";`。この行は `2f21bce` には存在しないため、参照コミットを明示する）。入力に元からあったマーカーカラムは中間モデルに入らないため、着色の対象にならない。現状の説明はこの限定に触れていない。

  `#32` より前から成り立つ事実であり、`#32` が作った矛盾ではない。`#32` 以前の「マーカーカラムは無損失で保持する」が誤りだったため、当時の見かけ上の整合は誤り同士の整合だった。

- **(d) 「主なクラスとリソース」の表の「載せる側」が6ページで揃っていない** — `design.md` §「利用側ページに内部構造の構成図を置かない」の採否基準 (1) は「利用者が作成する成果物（テストクラス・テストデータ・テスト対象クラス）は載せる」だが、`implementation/request_unit_test/batch.rst`・同 `mom.rst` の表はテスト対象クラスの行を持たない（残る4ページは持つ。`implementation/request_unit_test/web.rst:32`・同 `rest.rst:34`・`implementation/class_unit_test/component.rst:32`・同 `entity.rst:32`。2026-08-21 実測）。両ページとも `batch.rst:45`・`mom.rst:66` の作成単位欄で「テスト対象クラス（Action）につき1つ作成する。」と述べており、テスト対象クラスの存在自体は前提にしている。また基準 (2) を満たすスーパクラスが2つ、`mom.rst` の表に無い。同 `:130` の `BatchRequestTestSupport` と同 `:131` の `BasicHttpRequestTestTemplate` で、`mom.rst:128`-`:131` は同期応答メッセージ送信のテストクラスがこのどちらかを継承すると書いている（`BatchRequestTestSupport` は同 `:30` にも継承の記述がある）。`mom.rst` の表にあるスーパクラスは `MessagingRequestTestSupport`（同 `:70`）と `MessagingReceiveTestSupport`（同 `:73`）の2つで、表全体は見出し行を除くと6行ある（同 `:64`・`:67`・`:70`・`:73`・`:76`・`:79`。2026-08-21、`grep -n '^  \* - ' mom.rst` で実測）。`BasicHttpRequestTestTemplate` は `web.rst:35` の表にはあるが、採否の判定はページ単位で行う（`design.md` §「利用側ページに内部構造の構成図を置かない」）ため、`mom.rst` 側は独立に未処理である。`#32` は落とす側だけを当てたため未処理。

  **未決点**: 行を足すか、(1) をページ単位の任意とするかを着手時に決める。台帳 `current-0282`・`current-0296`・`current-0323` の出典表にも該当行が無いため、行を足す場合は台帳の `note` に足した理由を記録する必要がある。

- **(e) `#32` が範囲外とした2件** — どちらも `#32` の是正3 の4観点レビューで挙がり、`#32` の完了条件が拾わない範囲にあるため送った（2026-08-21）。

  - **(e-1) `.rn/` 内の相互参照の節見出し化が3ファイルで止まっている。** `#32` の是正3 は完了条件6 が名指しした `mapping/style.md`・同 `glossary.md`・同 `vocabulary.md` の4件だけを直した。残りは2つの形で残っている。`design.md`・`steering.md`・`reviews/`・`checks/`・`mapping/` の5つ（作業指示 `ntf-doc-*.md` を除いた、書き換わり続ける文書）を母集団として 2026-08-21 に実測した件数は、ディレクトリ接頭辞付き（`reviews/page-x.md:12` の形）が141件、ベアファイル名（`design.md:12`・`steering.md:12` の形）が271件である（`grep -rEo '(reviews|design|steering|checks)/[A-Za-z0-9_.-]+\.md:[0-9]+' --include='*.md' design.md steering.md reviews checks mapping | wc -l` と `grep -rEo '(^|[^/A-Za-z0-9_.-])(steering|design)\.md:[0-9]+' --include='*.md' design.md steering.md reviews checks mapping | wc -l`。いずれも `.rn/20260724-ntf-yaml-support/` で実行）。後者は完了条件6 の grep が拾わない形であり、`mapping/style.md` にも `ntf-doc-27-small-3rd.md:26`（同 `:58`）・同 `:129-132`（同 `:224`）として残っている。**未決点**: 対象を `.rn/` 全体に広げるか、生きている文書（`design.md`・`steering.md`・`reviews/`・`checks/`）に限るかを着手時に決める。`mapping/glossary.md` §1 は `#32` の是正3 で、受領後に書き換えていない作業指示と `input/` 配下を「実物の側」として `file:line` のまま指すと整理した。この線引きを `.rn/` 全体の規約として追認するかどうかも、あわせて決める。

  - **(e-2) 落とした行の役割を本文に残す規範を、明文化前の7行へ遡って当てるか。** `design.md` §「利用側ページに内部構造の構成図を置かない」の採否基準の段落の末尾は「落としたクラスの役割は、各ページのリード文または本文に残す。」と無条件に書いているが、`9031fa6` が落とした7行のうち2行（`implementation/request_unit_test/mom.rst` の `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`）はセルの内容が本文に残っていない。この規範の文は `#32` の是正2 で入ったもので、`9031fa6` はそれより前のコミットである（前後関係の実測は `design.md` §「利用側ページに内部構造の構成図を置かない」にある）。**未決点**: 2行の役割を `mom.rst` の本文へ書き足すか、規範は明文化以降にのみ当たると `design.md` に明記するかを着手時に決める。

  - **(e-3) 落としたクラスの役割の置き場所が4ページで揃っていない。** `implementation/request_unit_test/batch.rst`・同 `mom.rst` は機能概要のリード段落の本文、同 `web.rst` は使用方法配下の `.. tip::`、同 `rest.rst` は使用方法配下の本文にある。`design.md` §「利用側ページに内部構造の構成図を置かない」が「リード文または本文」を許すため規約違反ではないが揃ってはいない。`#32` の是正2 で挙がり、範囲外として持ち越した（`checks/task-32.md` §「3回の上限に達した時点で残る未解決の指摘」2）。**未決点**: 置き場所を1つに定めるか、ページ単位の任意とするかを着手時に決める。

**Steps**: 着手時に詳細化する。

### #34: ビルド用 Docker イメージを `docker build` から作り直せない（環境課題）

**Purpose**: 解説書のフルビルドに使う Docker イメージを `docker build` から作り直せるようにする。`#33` が扱う記述課題ではなく、検証環境そのものの課題であるため独立させた（`#32` のレビュー是正、2026-08-21）。

**背景と未決点**:

- 2026-08-21 に `docker build -t nablarch-document-build .` を実行したが、`Dockerfile:19` の `pip install` が社内 TLS 傍受の自己署名 CA を検証できず exit 1 で失敗する（`ERROR: Could not find a version that satisfies the requirement setuptools==57.5.0 (from versions: none)`。原因は `SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain'))`）。ホストには CA が `/usr/local/share/ca-certificates/ca.crt` として置かれ `SSL_CERT_FILE` も向いているが、`Dockerfile` はこれをイメージへ入れていない。`#32` の是正2 では既存イメージ（`a974e0c8ac60`、7日前）でフルビルドしたため、イメージ自体は2回続けて未検証である。`Dockerfile` は `#32` の作業範囲外のため触っていない。

- **未決点**: `Dockerfile` に社内 CA を取り込む変更を入れてよいか、それとも `docker build` 時に CA をマウントする回避手順を作業手順として残すかを、着手時に user へ諮る。

  **方針（2026-08-21、`#32` の是正3 で user が判断）**: `Dockerfile` は変更しない方向で進める。社内 TLS 傍受の CA は環境固有のものであり、解説書リポジトリの `Dockerfile` に焼き込むと、その CA を持たない環境でビルドが壊れるためである。`docker build` 時に CA を渡す手順（`--build-arg` またはビルドコンテキストへの一時配置とビルド後の削除）を本 `steering.md` の手順として残す方向で検討する。その際も `ca.crt`・`Dockerfile.ca` を作業ツリーに残さないという既存の制約を守る。

- **`#32` の完了判定との関係**: 是正2指示 `ntf-doc-32-fix2.md`「完了条件」13 は `docker build` からのイメージ再作成を求めつつ、「今回も失敗する場合は、失敗ログをそのまま `checks/task-32.md` に記録し、`#33` へ送る」という逃げ道を定めている。その逃げ道に沿って失敗ログを記録し、記述課題の `#33` ではなく環境課題として独立させた本タスクへ送った。**`#32` は、既存イメージでのフルビルドが警告0・`build succeeded.` であることをもって完了条件13 の代替とし、イメージ再作成の検証は本タスクで行う。**

**Steps**: 着手時に詳細化する。


### #35: `#32` の是正3 が残した記述の誤り4件を直す（user 指示 2026-08-21）— Closed（2026-08-24）

**Closed（2026-08-24）**: 是正6（`残作業-rst修正.md` §1）で、ラウンド2 の `must` M-1 と申し送り45 を処置して閉じた。**申し送り44 は5点のうち (a)(b)(c) が閉じ、(d)（`:883` に超過分の扱いが無く `:1169` と非対称）と (e)（`:885` の「空配列 ``[]``」が `:836`・`:1155` の0件の言い回しと同形）が残る**（内訳の表は下の記録先にある）。

**追記（2026-08-25）**: 申し送り44 の残り (d)(e) と、`glossary.md` §5.10 の申し送り42・43 を反映して**全4件を閉じた**。(d) は `:885` に「フィールドの数を超える位置の値は読み込まない。」を1文追加（`DataFileFragment.java:105-114` の `addValue` が `names.size()` でループを止めるため、固定長・可変長・\ Excel\ ・\ YAML\ すべてに効くことを実測）。(e) は「``rows:``\ に空配列 ``[]``\ を記載した行」→「``rows:``\ の要素を空配列 ``[]``\ とした行」に言い換え、`:836`・`:1155` の「リスト全体を `[]` にする」との混同を解消した。42・43 は `glossary.md` §5.10 の `フィールド長行`・`レコード種別行` の意味欄を実装に合わせて是正した（**用語集は全34ページ作成完了後のため、本件に限り変更禁止を解除**。正表記・揺れ表記・別義列は変更していない）。`verify_glossary.py` `RESULT: OK`（9カテゴリ不一致0件）、`verify_mapping.py` exit 0、Docker フルビルド `build succeeded.`（`WARNING:`／`ERROR:`／`SEVERE:` 0件）。**レビューは回していない**（実測に基づく訂正で申し送りの記述と1対1に対応するため）。記録は `reviews/page-testdata_notation.md` §「申し送り44 (d)(e)・申し送り42・43 の処置（2026-08-25）」。`implementation/testdata_notation.rst:883` を3ブロック（段落2つ ＋ `important` 1つ）へ書き直し、`:1160`・`:1547`・`tools/testdata_converter.rst:71` を同じ実測に揃えた。**数え方（「先頭要素を除いたセル数」「ラベル列を除いたセル数」）による説明をやめ、「末尾のフィールドの値を書かなければ ``""`` として扱われる」という結果の説明に置き換える**という方針で決着している。反映内容・根拠・検証は `reviews/page-testdata_notation.md` §「`#35`-是正6 ／ `#33` (a) 空セル記述の書き直し（2026-08-24）」と `reviews/page-testdata_converter.md` §「`#35`-是正6 ／ `#33` (c)（`:71` と `:280` の修正、2026-08-24）」。**是正6 はレビューを回していない**（逐語はディレクターが実測に基づいて確定済みで、作業は逐語の貼り付けとビルドのみ）。

**Purpose**: `#32` の完了後に user へ上げた5件の回答を受け、`#32` が残した記述の誤りを直す。`#32` は完了条件を満たしており閉じたままにする。**`#33`・`#34` より先に着手する**（両タスクとも自身のエントリのとおり着手時に user の判定を要し、本タスクは判定が出ている）。

**指示書**: `.rn/20260724-ntf-yaml-support/ntf-doc-35.md`。対象行・変更前後の逐語・出典はすべて同ファイルにある。**是正ラウンドの上限は3回**（指示書冒頭）。

**Steps**:

- [x] 1. `tools/testdata_converter.rst:71` の段落を、**是正1 指示書 §1 の差し替え文の逐語**に置き換える（`#35` 本体の §1 の「変更後」ではない。反例が出て停止条件に当たり、user が新しい文面を確定した）。「カラム名の行」で両系統を呼ばないこと、YAML 側の対称性を書かないことが判断の理由（是正1 §1）
- [x] 1a. `implementation/testdata_notation.rst:1544`-`:1547` の4行を、**是正1 追補 §2 の逐語**に置き換える（「ファイル・メッセージ」「テーブル・``LIST_MAP``」の両方が対象。追補 §1 で承認済み）。機構B の補完側（データ行を名前の幅へ揃える）は書かない（`:658`・`:883` に既出のため）。「位置」とも書かない（YAML の テーブル・``LIST_MAP`` はキー対応）（是正1 §2 ＋ 追補 §1・§2）
- [x] 1b. 両方の行の「（Excel 形式のみ）」が成り立つかを実装から確かめ、経路を `reviews/page-testdata_notation.md` の `## #35-是正1` 節に記録した（`cf80549`）。**停止条件に該当**——「名前の行の行末の空セルを取り除く」は Excel 形式のみで正しいが、「データ行を名前の幅へ揃える／名前が無い位置のセルを読まない」は YAML 形式にもある。`.rst` は未変更のまま user へ報告済み。YAML の解析実体は指示書が指した `nablarch-testing-converter@e977824` の `yaml/` ではなく `nablarch-testing-yaml@190cc9a` にあった（是正1 §2）
- [x] 1c. 完了条件2 を「`tools/testdata_converter.rst:71` に『この整形』が無い」と読み替えたことを `checks/task-35.md` に記録する。`:249` は書き出し設定の既存文で `#35` の対象外（是正1 §3）
- [x] 2. `implementation/testdata_notation.rst:1545` の直後に `list-table` の行を1行足す。既存の `:1544`-`:1545` は変えない。出典を `reviews/page-testdata_notation.md` に記録する（指示書 §2）
- [x] 3. 台帳5行（`current-0201`・`current-0282`・`current-0296`・`current-0309`・`current-0323`）の `note` 末尾の一文を、列挙を外したポインタ1文に置き換える。`mapping.csv` の直接編集は禁止で、`mapping/_batch/*.csv` を直してから昇順連結で作り直す（指示書 §3）
- [x] 4. `design.md` §「利用側ページに内部構造の構成図を置かない」の2か所を直す。`:147` の件数の説明を列挙を外した事実の記述に置き換え、`:143` の括弧書き末尾の一文を削る。**同節の他の記述は変えない**（指示書 §4）
- [x] 5. `design.md:147` をリード文＋箇条書きに割る。**文言は1文字も変えない**。改行・行頭記号・連続空白を除いた文字列の完全一致で検算する（指示書 §5）
- [x] 6. 検証。§1 の確定後に再実行する（2026-08-21 の `17b0254` 時点では全件 PASS・ビルド警告0）。`verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` と、既存イメージでの Docker フルビルド。ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し `_build/` を削除する（指示書 完了条件10〜13）
- [x] 7. 無限定の断定文それぞれについて主語を明示したうえで反例を検索し、自分の括弧書きや直後の列挙が反例になっていないかを確かめた記録を `checks/task-35.md` に書く（指示書 完了条件15）
- [x] 8. `tools/testdata_converter.rst:71` の段落を、**是正2 §1 の1段落の逐語**に置き換える。旧第1・第3・第4文を落とす。データ行の空セルは形式で分かれ全空行は読み飛ばされるため、1文で正しく言えず本文へ送るという判断（是正2 §1）
- [x] 9. `implementation/testdata_notation.rst:1544`-`:1547` の4行を、**是正2 §2 の逐語**に置き換える。「フィールド名称の行の」を落として無限定に戻し（A-3）、テーブル側の行にだけ「前述」を付ける（A-4）。データ行の補完は表に書かない（`:658`・`:787`・`:883` に既出）（是正2 §2）。**`9aa06d7` で実施済み。ただし A-3 の無限定化は誤りだったことが差分限定レビューで判明し、`:1545` は是正3 §1（Step 13）が置き換える**（`:1544`・`:1546`・`:1547` は是正2 の逐語のまま）
- [x] 10. `reviews/page-testdata_converter.md:236`・`:238`、`reviews/page-testdata_notation.md:555`・`:585`・`:644`・`:648`・`:654` の HEAD についての記述を §1・§2 反映後の状態に書き直し、申し送り38 を削除し、`:595`・`:642` の行番号参照を節見出し参照に直す（是正2 §3）。**`9aa06d7` で実施済み**（§3 の名指し7箇所に加え `:658` の導入文へ1文追加。同節の逐語も是正2 で置き換わったため。コーディネータ判定で valid）。**`:667` の書き直しは `:1545` の文面確定待ちで積み残し、是正3 §2（Step 14）が引き継ぐ**
- [x] 11. **4観点は回さない**（`ntf-doc-13-standing-rules.md:20` の常設ルール、是正ラウンド2）。差分限定の2点——是正が §1〜§3 の範囲に収まっているか、新しい欠陥を生んでいないか（特に §1・§2 の逐語指定文そのものへの反例）——だけを回し、指摘件数と観点を `reviews/page-testdata_notation.md` に記録する（是正2 §4）。**レビューは回し済み**（`8890a65`。指摘5件＝`must` 2／`nice` 3、採用4・却下1。記録は `checks/task-35.md` の `## #35-是正2` 節）。**`must` 2件が未処置のため未完了。`reviews/page-testdata_notation.md` への記録も未了。是正3 §4（Step 16）が引き継ぐ**。**是正4 で閉じた**（記録は `reviews/page-testdata_notation.md` §「是正2・是正3 の指摘件数と観点（Steps 11・16 の積み残しをここへ移す）」へ移した）
- [x] 12. 検証。Docker フルビルドが成功し警告0、直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し `_build` を削除する。`ca.crt`・`Dockerfile.ca` を残さない。Steps 8〜11 を1コミットにまとめてプッシュする（是正2 完了条件6〜8）。**フルビルド・後始末・`9aa06d7` の push は実施済み**（コーディネータが独立に再実行して確認）。**1コミットに畳む要件は達成不能**（§4 のレビュー記録は §1〜§3 の実装後にしか書けず、`9aa06d7` は push 済み）。**是正3 完了条件8 が「`9aa06d7` に続く1コミット」＝2コミットで確定と裁定したため、この要件は是正3 §4・完了条件6〜8（Step 17）へ引き継いで閉じる**。**是正4 で閉じた**（`#35` は `9aa06d7`・`1d88729`・是正4 の1コミットに分かれた。`--amend`・force push は一度も行っていない）
- [x] 13. `implementation/testdata_notation.rst:1545` を、**是正3 §1 の1行の逐語**に置き換える（案B）。トリムに観測できる効果があるのはフィールド名称行・データ型行・フィールド長行の3つだけで、データ行は `DataFileFragment.java:105`-`:107` が埋め戻すため効果が打ち消される。メッセージも `MessageParser.java:27`・`:115` が `FixedLengthFileParser` へ委譲し `DataFileParser.onReadLine` を通るため、「ファイル・メッセージ」の行に3行分をまとめて書いてよい。**`:1547`（テーブル・``LIST_MAP``）は変更しない**。用語は `mapping/glossary.md` §5.10「ファイルデータの行の名称」の正表記に従う（是正3 §1）。**`1d88729` で実施済み。ただしディレクティブ行が欠けていたことが差分限定レビューの `must-1` で判明し、`:1545` は是正4 §1（Step 18）が置き換えた**（`:1544`・`:1546`・`:1547` は是正2 の逐語のまま）
- [x] 14. 残りの指摘3件を処置する。(a) `reviews/page-testdata_notation.md:667` の「`:883` と食い違っていないことの確認」を §1 の確定文面に合わせて書き直す（`:702`-`:704` が引き継いでいる）、(b) 新節（`## #35-是正2`）の A-5 行の `mapping/glossary.md` への参照を行番号から §5.10「ファイルデータの行の名称」へ直す、(c) 「（\ Excel\ 形式のみ。前述）」の括弧についての指摘は**却下**（user 判断済み。A-4 で確定済みのため scope 外）（是正3 §2）。**`1d88729` で実施済み**（(a) は §「追補（`ntf-doc-35-fix1-addendum.md` §2）に従って表の2行を書き換えた記録」の末尾の段落を書き直し、(b) は §5.10 の節見出し参照へ改め、(c) は user 却下のため `:1547` 未変更）
- [x] 15. 申し送りを1件起こす。`tools/testdata_converter.rst:71` が「データ行の空セルの扱いは形式によって異なるため、詳細は参照」と送っている先に、メッセージのデータ行についての記述が無い（`implementation/testdata_notation.rst:1152`-`:1309` に空セル・補完の記述0件）。**`#35` では直さず申し送りに起こす**（是正3 §3）。**申し送り39 として起票済み**（`reviews/page-testdata_notation.md` §「申し送り（続き2）」。38 は `9aa06d7` が削除したため欠番。事実は自分で `sed`＋`grep` を再実行して確認済み）
- [x] 16. **4観点は回さない**（`ntf-doc-13-standing-rules.md:20` の常設ルール、是正ラウンド3）。差分限定の2点——是正が §1〜§3 の範囲に収まっているか、**§1 の逐語指定文そのものに反例がないか（実装で裏を取る）**——だけを回し、指摘件数と観点を `reviews/page-testdata_notation.md` に記録する。**Step 11 の記録未了分（是正2 の指摘5件・観点2件）も同ファイルへ移す**（是正3 §4）。**レビューは回し済み**（`1d88729`。指摘10件＝`must` 2／`nice` 3（採用）／`nice` 3（未処置）／却下2）。**記録は是正4 で `reviews/page-testdata_notation.md` §「是正2・是正3 の指摘件数と観点（Steps 11・16 の積み残しをここへ移す）」へ移して閉じた**
- [x] 17. 検証。Docker フルビルドが成功し警告0、直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し `_build` を削除する。`ca.crt`・`Dockerfile.ca` を残さない。**Steps 13〜16 を `9aa06d7` に続く1コミットにまとめてプッシュする。`--amend` と force push は行わない**（`#35` が2コミットに分かれることは確定。申し送り不要）（是正3 完了条件6〜8）。**フルビルド・後始末は実施済み**（`1d88729` 時点）。**コミットは `1d88729`（`wip:`）が担い、`must` 2件の処置は是正4（Steps 18〜22）が引き継いで閉じた**
- [x] 18. `implementation/testdata_notation.rst:1545` を、**是正4 §1 の1行の逐語**に置き換える（先頭に「ディレクティブ行・」を足す1行のみ）。`READING_DIRECTIVES_AND_NAMES` はディレクティブ行とフィールド名称行の2種を捌いており、ディレクティブ行にもトリムに観測できる効果がある（根拠は是正4 §5 の5点。ディレクター側が実測で反例検証済み）。**`:1547` と `tools/testdata_converter.rst:71` は変更しない**。`mapping/glossary.md` も変更しない（§5.10 は「ファイルデータのレイアウトを表す行の名称」に限った節で、ディレクティブは §5.8。「ディレクティブ行」は同ページ `:1055` が既に使う語）。メッセージのフレームワーク制御ヘッダを括弧書きで足さない（是正4 §1・§5）。**実施済み**（`sed -n '1545p'` の出力と検算は `checks/task-35.md` §「`#35`-是正4（最終）」の完了条件32）
- [x] 19. 差分限定レビューの `must-2`（`tools/testdata_converter.rst:71` が「フィールド名称行」だけを挙げており、§1 の4行と食い違う）を、**申し送り40 として起こす**。`reviews/page-testdata_notation.md` の `### 申し送り（続き2）` に申し送り39 と同じ書式で追加し、`#35` 着地後に申し送り39・`:883` の Excel 側括弧書きと合わせて1タスクにする旨を1文添える。**`tools/testdata_converter.rst` は変更しない**（是正4 §2）。**申し送り40 として起票済み**（`reviews/page-testdata_notation.md` §「申し送り（続き2）」。`tools/testdata_converter.rst` は未変更）
- [x] 20. 採用した `nice` 3件を反映する。(1) 是正2 節の見出し「差し替え後の逐語（現在の HEAD）」を `:555`・`:654` が既に採っている失効注記の型に揃え、§1 の差し替えで失効することを書く、(2) `checks/task-35.md` の新規2行が `.rn/` 内を行番号で指している箇所を節見出し参照に直す（`steering.md` Rules の「`.rn/` 内の文書どうしの相互参照」）、(3) 新設見出しの直前に空行を入れる（是正4 §3）。**3件とも反映済み**（完了条件35）
- [x] 21. 記録を反映後の状態にする。`reviews/page-testdata_notation.md` に本ラウンドの節を新設し、§1 の確定逐語・§2 の申し送り40・**本ラウンドはレビュー未実施であること**（是正ラウンド上限3に到達。逐語の検証はディレクター側が実施）を記録する。**是正4 §5 の根拠（5点＋参照コミット `nablarch-testing@e21bf67`）を転記する**。あわせて Steps 11・16 が積み残した是正2・是正3 の指摘件数と観点も同ファイルへ移す。`checks/task-35.md` の完了条件表と `steering.md` の `#35` の Notes を反映後の状態にする（是正4 §4・§5）。**実施済み**（`reviews/page-testdata_notation.md` §「`#35`-是正4（「ディレクティブ行」を加えて `:1545` を確定、2026-08-24）」を新設。§5 の5点は自分で `git show e21bf67:<path>` に当たり直して全件一致を確認した）
- [x] 22. 検証。Docker フルビルドを1回通し警告0を確認し、直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して `_build` を削除する。`locales/` を `.gitignore` に加えない。`ca.crt`・`Dockerfile.ca` を残さない。**完了条件32〜38 をまとめた1コミットを push する。`--amend` と force push は行わない**（是正4 §6・完了条件7〜8）。**実施済み**（`build succeeded.`・警告0、`sphinx.mo` 未変更、`_build`・`build.log`・`ca.crt`・`Dockerfile.ca` なし）
- [x] 23. **§1 逐語の検証（着手前。`.rst` には反映しない）。** 是正5 §1 の逐語案「\    - ディレクティブ・フィールド名称・データ型・フィールド長の各行の行末の空セルを取り除く（\ Excel\ 形式のみ）。フィールド名称の数を超える位置の値は読み込まない」に反例が無いかを、実物を開いて4点確かめる。(1) 『行』を落としてページの語法に揃うこと、(2)「各行の」で4語すべてに掛かると読めること、(3) フィールド長の限定が `:874` で担われ `:1545` に「固定長のみ」を足さないこと、(4)「フィールド名称の数を超える位置の値は読み込まない」が `nablarch-testing@e21bf67` の実装と一致すること。**反例が出たら §2 以降に進まず報告する**（是正5 §1・完了条件1）。**実施済み。(1) で反例が出たため §2 以降は未着手**（記録は `reviews/page-testdata_notation.md` §「`#35`-是正5 §1 の逐語検証（着手前。`.rst` は未変更）」）
- [x] 24. **フェーズA A-1**。`:1545` の扱いについての user 判断を受領した。**前半の『行』付き4語は据え置き、後半の句だけを「フィールド名称の数を超える位置の値は読み込まない」へ差し替える**（是正5 §1 の3択のうち (2)）。案の作成は不要。反映はフェーズB（是正5 第2ラウンド A-1）
- [x] 25. **フェーズA A-2**（申し送り40）。`tools/testdata_converter.rst:71` の逐語案を1つ作る。ファイル・メッセージ側でトリムが掛かる行を実測どおり列挙し、テーブル・`LIST_MAP` 側の「カラム名の行」と後段の1文は変えない。`:1545` と食い違わないこと（同 A-2）。**逐語案は `reviews/page-testdata_notation.md` §「`#35`-是正5 フェーズA（実測と逐語案。`.rst` は1文字も変更していない、2026-08-24）」の A-2 にある**
- [x] 26. **フェーズA A-3**（申し送り39）。メッセージのデータ行の空セルの扱いを `nablarch-testing@e21bf67` と `nablarch-testing-yaml@190cc9a` で実測し、Excel 経路と YAML 経路の異同を確定させたうえで、メッセージの節に足す1〜2文の逐語案を作る（同 A-3）。**実測結果と逐語案は同節の A-3 にある**
- [x] 27. **フェーズA A-4**。`:883` の Excel 側の括弧書き「先頭セルが空の行」が `PoiXlsReader.java:141`-`:147` の `isBlankLine` に掛かるかを実測で確定させ、掛かるなら書き換える逐語案を作る（同 A-4）。**掛かることを実測で確認し、逐語案を同節の A-4 に置いた**
- [x] 28. **フェーズA A-5**（申し送り41）。`mapping/glossary.md` §5.10 の『行』付き4語と、`testdata_notation.rst:854`-`:858`／`:866`-`:879` の『行』なしが、矛盾か別概念かを確定させる（同 A-5）。**別概念と確定。ページの是正は不要。申し送り41 はクローズしてよい**（根拠は同節の A-5）
- [x] 29. **フェーズB B-1・B-2**。A-1 の逐語を `:1545` に反映し、承認された A-2〜A-5 の案を反映する。「変更不要」と判定されたもの（A-5）は反映しない（是正5 第2ラウンド B-1・B-2）。**実施済み**（2026-08-24 の user 回答に従い、A-3 は第3文を足さず `:1158` の直後に1段落として挿入、A-4 は末尾1文を入れた。A-5 は変更していない。差分は `ja/` の2ファイル・4 hunk のみ。**A-3 の挿入で A-1 の行は `:1545` → `:1547` にずれた**）
- [x] 30. **フェーズB B-3**。差分限定の2観点（範囲統制／新しい欠陥。後者に**承認された逐語案そのものへの反例検証**を含める）を**それぞれ別のサブエージェント**で回す（同 B-3）。**ラウンド1・ラウンド2 とも実施済み。生出力は要約せず `reviews/page-testdata_notation.md` の是正5 の2節に貼付済み。** ラウンド1 は `must` 1・`should` 2・`nice` 3 で、`must`（`:883` の数え方が1つずれている）を user 判断の案A ＋ `should`② で是正した（Step 30-a〜30-e で走査・実測・反映を実施）。ラウンド2 は観点1 が `must` 0・`should` 0・`nice` 4、観点2 が `must` 1・`should` 2・`nice` 3。**採用した指摘は0件。`must`（M-1。行末の `null`／`""` が `trimTailCopy` で消えるため逐語の条件文が結果を言い当てられない）は、是正が持ち込んだ欠陥ではなく、処置すると user 承認済みの逐語4箇所に波及し、かつラウンド上限2に達しているため、本文を変えず user へエスカレーションした**（同ファイル §「user へのエスカレーション（M-1。本ラウンドでは処置していない）」）
- [x] 31. **フェーズB B-4**。`reviews/page-testdata_notation.md` の是正5 の節に、フェーズA の実測結果と確定した逐語（A-1〜A-5）・B-3 の生出力とラウンドごとの指摘件数と観点を記録する（同 B-4）。**実施済み。** ラウンド2 の節に、指摘件数・観点・両観点の生出力・処置とその理由（採用0件・却下3件・据え置き6件）・Step 30-a／30-b／30-e の走査の生出力・Step 30-d の逐語の根拠の再確認を書いた。申し送り39・40 を【処置済み】、41 を【クローズ】に更新し、是正2・是正3 の表の「`nice` 3（未処置）」を「処置済み」へ改め、3件それぞれに決着の内訳を付した。是正3 の `nice` 3件目の記録の誤りは申し送り42 が既に記録している。申し送り44・45 を新たに起票した。`checks/task-35.md` の完了条件44〜50 とフェーズB の Method 記録も反映済み。**記録に本ラウンドのコミットハッシュは書いていない**
- [x] 32. **フェーズB B-5**。Docker フルビルドを1回通し警告0を確認し、直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する（同 B-5）。**実施済み。** `_build` を消してからフルビルドし `SPHINX_EXIT=0`・`build succeeded.`、`WARNING:`／`ERROR:`／`SEVERE:` は0件（**既知の `db_double_submit.rst:108` の warning も出ていない**）。`sphinx.mo` は復元済みで `git status` に現れない。`_build`・`build.log`・`ca.crt`・`Dockerfile.ca` は作業ツリーに無い。`verify_mapping.py` は exit 0（`OK: no errors`）。**作業指示は「`d3017b8` に続けて」と書いているが、`d3017b8` の後に `/rn:dn` の `0a12ab6` と `/rn:up` の `ab2112e` が既に積まれているため、実際には `ab2112e` に続く1コミットとした**（`d3017b8` の子孫であり指示の意図は満たす）。`--amend` と force push は行っていない

- [x] 33. **是正6**（`残作業-rst修正.md`。`#35` の残りと `#33` (a)(c) を同時に処置）。§1（`:883`・`:1160`・`:1547`・`tools/testdata_converter.rst:71` の4箇所）・§2（`:1536` に2文追加）・§3（`tools/testdata_converter.rst:280`）を逐語1文字一致で反映し、記録2ファイルと `steering.md` を更新して1コミット（`173c0f7`）で push した。**レビューは回していない**（指示書「この指示の性格」）。完了条件7件はすべて充足（差分は `.rst` 2ファイル・6箇所、逐語一致、Docker フルビルド `build succeeded.`・`WARNING:`／`ERROR:`／`SEVERE:` 0件、`verify_mapping.py` exit 0、変更禁止7ファイルの差分0行、`git status --short` 空、`5d854ca` に続くコミットで `--amend`・force push なし）

**Completion criteria**（指示書 `ntf-doc-35.md`「完了条件」1〜15 の逐語）:

1. `tools/testdata_converter.rst` の該当段落が**是正1 §1 の差し替え文**と一致する。`grep -rn 'メッセージのテストデータ' ja/` が0件
2. `tools/testdata_converter.rst:71` に「この整形」が無い（`:249` は残ってよい。是正1 §3 の読み替え。読み替えたことを `checks/task-35.md` に記録する）
3. `reviews/page-testdata_converter.md` の該当行が、`HeaderLine.java:81`・`XlsFormatReader.java:424`・`XlsFormatReaderCellTypeTest.java:182`-`:188` を出典として、名前の行とデータ行で扱いが異なることを記録している（是正1 完了条件5。5系統の走査経路の記録は `17b0254` で済み）
4. `implementation/testdata_notation.rst` の `list-table` に §2 の行があり、`reviews/page-testdata_notation.md` に出典がある（**「既存の `:1544`-`:1545` が変わっていない」の句は追補 §2 が4行の差し替えを指示したため落とした。4a が差し替え後の判定を担う**）
4a. `implementation/testdata_notation.rst` の該当4行が是正1 追補 §2 の文面と一致している（是正1 完了条件3。追補で差し替え）
4b. 同ファイル `:1545`（旧）の「\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込む」が消えており、`:883` との矛盾が解消していることを `reviews/page-testdata_notation.md` の `## #35-是正1` 節に追記している。あわせて、機構B の補完側を表に書かなかった理由（`:658`・`:883` に既出）も1〜2文で記録している（是正1 完了条件4。追補で差し替え）
4c. `implementation/testdata_notation.rst:883` の既存記述（可変長ファイルの `""` 補完）と、新しく書いた記述が食い違っていないことを確認した記録がある（是正1 完了条件6）
5. `mapping.csv` の `note` に「なお同じ基準で 9031fa6 が」が0件、「なお 9031fa6 も同じ基準で」が5件
6. `_batch/*.csv` を昇順連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、`csv.DictReader` が597行。`82322fa` との差分が指定5行の `note` のみであることを `git diff` で全行確認する
7. `design.md` の `:147` に「8件」が無く、`:143` から「同じマーカーの配下には」で始まる一文が消えている。`:143` の「計11件」は残っている
8. `design.md:141`（採否基準の段落）が `82322fa` から1文字も変わっていない（`git show 82322fa:….rn/…/design.md | sed -n '141p' | md5sum` と一致）
9. §5 の検算（改行・行頭記号・連続空白を除いた文字列の完全一致）が通る
10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
13. 既存イメージでのフルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`_build/`・`build.log` を削除する（是正1 完了条件10）
14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない
15. 「取り除く」「落ちる」など無限定の断定文それぞれについて、主語を明示したうえで反例を検索し、自分の括弧書きや直後の列挙が反例になっていないかを確かめてから確定したことを `checks/task-35.md` に記録する

**Completion criteria（`#35-是正2` 指示書「完了条件」1〜8 の逐語）**。**上の 1・4a は是正2 §1・§2 の文面へ読み替える**（是正1 とその追補が定めた逐語は是正2 が差し替えた）:

16. `tools/testdata_converter.rst:71` が是正2 §1 の1段落と逐語一致し、旧第1・3・4文が消えている
17. `implementation/testdata_notation.rst` の該当4行が是正2 §2 の文面と逐語一致している
18. `implementation/testdata_notation.rst` 内に「フィールド名称の行」が1件も残っていない
19. 是正2 §3 の7箇所と申し送り38、行番号参照2箇所が処置済み
20. 是正2 §4 のレビューを回し、指摘件数と観点を記録済み。`must` を残していない
21. Docker フルビルドが成功し警告0、`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` 実施済み、`_build` 削除済み
22. `ca.crt`・`Dockerfile.ca` が作業ツリーに残っていない
23. 是正2 §1〜§4 を1コミットにまとめてプッシュ済み

**Completion criteria（`#35-是正3` 指示書「完了条件」1〜8 の逐語）**。**上の 17 は是正3 §1 の文面へ読み替える**（是正2 §2 が定めた `:1545` の逐語は是正3 §1 が差し替えた。`:1544`・`:1546`・`:1547` は是正2 のまま）:

24. `implementation/testdata_notation.rst:1545` が §1 の1行と逐語一致している
25. `:1547` が変更されていない
26. §2 の3件が処置済み
27. §3 の申し送りが起こしてある
28. §4 のレビューを回し、指摘件数と観点を記録済み。`must` を残していない
29. Docker フルビルドが成功し警告0、`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` 実施済み、`_build` 削除済み
30. `ca.crt`・`Dockerfile.ca` が作業ツリーに残っていない
31. **`9aa06d7` に続く1コミットとしてプッシュ済み。`--amend` と force push は行わない**（`#35` が2コミットに分かれることは、これで確定とする。申し送り不要）

**Completion criteria（`#35-是正4`（最終）指示書「完了条件」1〜8 の逐語）**。**上の 24 は是正4 §1 の文面へ読み替える**（是正3 §1 が定めた `:1545` の逐語は是正4 §1 が差し替えた。`:1544`・`:1546`・`:1547` は是正2 のまま）:

32. `:1545` が §1 の逐語と1文字一致（`sed -n '1545p'` の出力を記録に貼る）
33. `:1547`・`tools/testdata_converter.rst:71` が未変更（`git diff` で確認）
34. 申し送り40 が起票済み
35. `nice` 3件が反映済み
36. `reviews/page-testdata_notation.md`・`checks/task-35.md`・`steering.md` が反映後の状態
37. §5 の6点が記録に転記済み
38. Docker フルビルド成功・警告0、`sphinx.mo` が未変更、`ca.crt`・`Dockerfile.ca` が無い
39. 1〜7 をまとめた1コミットを `3132688` に続けてプッシュ済み。`--amend` と force push は行わない

**Completion criteria（`#35-是正5` 第2ラウンド。フェーズA / フェーズB）**。**上の 32 は是正5 §1 の文面へ読み替える**（是正4 §1 が定めた `:1545` の逐語を是正5 §1 が差し替える。`:1544`・`:1546`・`:1547` は是正2 のまま）。**40 は是正5 第1ラウンドのもので充足済み。41〜47（第1ラウンド）は第2ラウンドの 41〜50 へ差し替えた**:

40. §1 の4点の検証結果が記録にある。反例が出た場合は §2 以降に進まず報告していること

フェーズA:

41. （A-a）A-2〜A-5 それぞれについて、逐語案または「変更不要」の判定が出ている
42. （A-b）各判定に `file:line` と参照コミットハッシュが添えてある。示せないものは「未確認」と書いてある
43. （A-c）`ja/` が1文字も変更されていない（`git diff --stat` で `ja/` が空）

フェーズB:

44. （B-a）`:1545` が A-1 の逐語と1文字一致（`sed -n '1545p'` の出力を記録に貼る）
45. （B-b）`git diff` の `ja/` 側の変更が、A-1 と承認された案だけに由来している
46. （B-c）B-3 の2観点を別サブエージェントで回し、生出力が要約なしで記録にある。ラウンドごとの指摘件数と観点が記録にある
47. （B-d）申し送り39・40・41 が処置済みまたはクローズとして記録が更新されている
48. （B-e）`mapping/glossary.md` §5.10 の誤りが申し送りとして起票されている
49. （B-f）Docker フルビルド成功・警告0、`sphinx.mo` が未変更、`ca.crt`・`Dockerfile.ca` が無い
50. （B-g）B-1〜B-5 をまとめた1コミットをプッシュ済み。`--amend` と force push は行わない

**Notes（`#35`-是正5 第2ラウンド。フェーズB 完了時点の記録）**: **以下は フェーズB 完了時点のスナップショットである。`must` M-1 と申し送り45 は、その後の是正6（2026-08-24）で処置してクローズした。申し送り44 は (a)(b)(c) が閉じ、(d)(e) が残る。現在の状態は上の **Closed（2026-08-24）** を読むこと。**

- **Steps 1〜32 は check off 済み。** 是正1〜是正4 と、是正5 の §1 検証・フェーズA・フェーズB がすべて終わっている
- **`ja/` の差分は2コミットに分かれている。** B-1・B-2（A-1〜A-4 の反映。2ファイル・4 hunk）は `d3017b8`、B-3 ラウンド1 の `must` の是正（`implementation/testdata_notation.rst:883` の2文）は本ラウンドのコミット
- **【解消済み。是正6 で処置】** B-3 ラウンド2 の `must` 1件（M-1）を本文に反映せず user へエスカレーションしていた。 `:883` の是正後の1つめの文は、データ行の**末尾**フィールドに `null`／`""` を書いた場合の結果を言い当てられない（`nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/DataFileParser.java:68` の `trimTailCopy` が `:69` の `switch` より前にあり、データ行にも掛かるため）。**是正が持ち込んだ欠陥ではなく、是正前の文にも同じ不正確さがあった。** 処置すると `:1160`（A-3 で承認）・`:1547`（A-1 で確定）・`tools/testdata_converter.rst:71`（A-2 で承認）に波及し、いずれも user 承認済みの逐語である。B-3 のラウンドは上限2に達している。詳細と3つの波及先は `reviews/page-testdata_notation.md` §「user へのエスカレーション（M-1。本ラウンドでは処置していない）」
- **ラウンド2 で採用した指摘は0件。** 却下3件（S-1・S-2・N-3 の「フィールド数」の揺れ）と据え置き6件の理由は同ファイル §「処置とその理由」の表にある。**既決事項（`should`①・`nice`①〜③ を直さない判断、「フィールド数」を残す判断、`` ``rows:`` `` 直後の `\ `）に反する指摘は却下した**
- **申し送り45 は是正6 で処置済み（クローズ）。申し送り44 は (a)(b)(c) が閉じ、(d)(e) が残る。** 44 は `:883` の段落で指示範囲外として見送った改善5点、45 は `:1547` と `tools/testdata_converter.rst:71` が行末トリムの対象からデータ行を落としていた件。内訳の表は `reviews/page-testdata_notation.md` §「`#35`-是正6 ／ `#33` (a) 空セル記述の書き直し（2026-08-24）」にある
- **申し送り39・40 は処置済み、41 はクローズ。** 42・43（`mapping/glossary.md` §5.10 の2件）は用語集が変更禁止のため未処置のまま残る
- **観点1 の報告は出典に難がある。** 指示した参照コミット `e21bf67` ではなく作業ツリー HEAD（`2e43786`）を読んでおり、`file:line` が参照コミットに当たらない。結論は同一の2点をディレクターが `e21bf67` で独立に確認済み。対応表は `reviews/page-testdata_notation.md` §「観点1 の出典に関する但し書き（ディレクターによる）」
- **参照コミット**: `nablarch-testing@e21bf67`・`nablarch-testing-converter@e977824`・`nablarch-testing-yaml@190cc9a`。`nablarch-core` の clone は `/home/tie303177/work/nablarch/` に無く、`StringUtil` の実体は未確認（`#35` の判定はその内部仕様に依存しない）
- **実測用の `git worktree` は後始末済み**（2026-08-24 に確認。`nablarch-testing`・`nablarch-testing-yaml` のいずれにも `e21bf67`／`190cc9a` の worktree は残っていない。`nablarch-testing` に残る `.claude/worktrees/agent-*` 4件は別作業のもので触っていない）

### #36: 解説書に書く基準の確定と、テストデータ2ページのノイズ除去（user 指示 2026-08-25）— 進行中

**このタスクは CC への指示書を持たない。ディレクター（レビュー役）が `ntf-yaml-support` に直接コミットしている。**
user が「棚卸し一覧を出すのではなく2ファイルを直接修正し、修正意図単位でコミットして意図を
コミットメッセージに書く」方式を選択したため（2026-08-25）。**修正の根拠はすべてコミット
メッセージにある。** 本エントリは台帳との突き合わせのために置く。

**確定した基準（user 確定 2026-08-25）**:

> **解説書に書くのは「利用者が正しく書こうとしても踏むもの」だけ。「間違えたときにどうなるか」は書かない。**

判定の目安:

| | 書くか |
|---|---|
| 正しく書こうとしても踏む（例: マルチレイアウトのレコード長を揃える必要） | 書く |
| 記法を見れば分かる（例: フィールド名と型を同じ数だけ並べる） | 書かない |
| 間違えたときの帰結（例: 要素数が合わないとエラー、IOエラー、日付が解析できない） | 書かない |
| 他の箇所で既に言っている | 書かない |

**この基準はモジュール側のテストコードには適用しない**（文書とテストは目的が逆で、テストは
「間違えたときにどうなるか」を押さえるためにある）。

**「他の箇所で既に言っている」は同一ページ内にのみ適用する。2ページ間には適用しない**
（user 確定 2026-08-25）。2ページは役割が違うため、同じ話題が両方に出るのは当然である。

| ページ | 中身 | 読まれ方 |
|---|---|---|
| テストデータの書き方 | NTF が定義しているルールと書式。基本構文。**必須ルール**。メタな存在 | 一度読んで概念を掴む。記載例を引くための土台 |
| テストデータの記載例 | 具体的な記載方法とその説明。**全バリエーション**。利用PJがそのまま参考にできる水準 | 繰り返し引く |

例（改行文字）: 書き方は「値の種類に『改行文字』がある。Excel は ``\r`` と入力すると CR になる。
YAML は ``"\r"``・``"\n"`` と書く」というルールを述べる。記載例は実際のテストデータの形で
Excel／YAML の例を示し、それぞれに「なぜそう書くのか」「そう書くと何が出るか」を添える。

**この線引きが要る理由**: 記載例ページは例だけのページではなく、既に説明を持っている
（`testdata_examples.rst` の各節の導入文と表の前後の地の文）。基準を2ページ間に当てると、
その説明が「書き方に既出だから」と削られ、読者が2ページを往復する状態に戻る。
`design.md:47` は同一ページ内ですら「目と鼻の先のセクションへ読者を何度も行き来させ」ることを
欠陥として挙げており、ページを跨ぐ往復はなおさらである。
申し送り22（`reviews/page-testdata_examples.md:329`）・申し送り31
（`reviews/page-testdata_notation.md:416`）が記録した「書き方 → 記載例 → 書き方 の往復で
行き止まりになる」は、この線引きが無かったことによる。

**「全バリエーション」は記法表の行と1対1にしない**（user 指摘 2026-08-25）。網羅の単位は
**利用者がやりたいこと**であって表の行ではない。表の行と1対1にすると、利用者が困らないものにまで
例を作ることになり、本タスクがやってきたノイズ除去と逆方向になる。

**Purpose**: 34ページ作成期に積み上がった「エラーになる」系の記述が、利用者が読むべき記述を
埋もれさせている。上記の基準で `implementation/testdata_notation.rst` と
`implementation/testdata_examples.rst` の2ページを見直す。**対象はこの2ページのみ**（user 指定）。

**`#35`・`#33` の決定を上書きした箇所**（再開時に必ず読むこと。過去の記録と現在の本文が
食い違って見えるのはこのため）:

- `implementation/testdata_notation.rst` の「フィールドの数を超える位置の値は読み込まない。」
  — `#35` 追記（2026-08-25、申し送り44 (d)）が実測に基づいて足した1文。**基準に照らして落とした**
  （`3e01b69`）。実測結果が誤っていたのではなく、書く対象ではないという判断
- 同ページの `list-table`「読み込み時には以下のような整形・補完が行われる」（旧 `:1544`-`:1547`）
  — `#35` の是正1・是正2・是正3・是正4・是正5・是正6 が繰り返し推敲し、是正4 で「ディレクティブ行・」
  を加えて確定させた表。**表ごと落とした**（`672fde3`）。5項目のうち4項目が表自身の言葉で「前述」と
  断る再掲で、残る1項目も利用者の記述を変えないため
- 同ページ `:883` の「固有の記法制約」段落 — `#33` (a)／是正6 §1 が3ブロック（段落2つ ＋
  `important` 1つ）へ書き直したうちの1つめ。**段落ごと落とした**（`d004ec0`）。2つめ（値の並べ方）と
  3つめ（`important`）は残っている

**論点の決着**（`~/work/cowork/nablarch/ntf-doc-renewal/01-現在地.md` の13論点のうち3件）:

- 論点1（可変長ファイルのフィールド長）— **不成立**。回帰していない。記述順序の図・用語表・
  `testdata_examples.rst`「可変長ファイルを記述する」の Excel／YAML 両例が、旧解説書と同じことを
  より明示的に言えている
- 論点4（フィールド数と値の数の不一致）— **決着**。解説書からは落とす。超過値を黙って捨てる実装挙動
  （`nablarch-testing@e21bf67` `DataFileFragment.java:105-108`）は**ステップ4でモジュールへ申し送る**
- 論点8（「データ要素数が不正である」の出所不明）— **決着**。出所を調べるまでもなく基準で落ちる。
  実体は3リストのサイズ照合（`FixedLengthFileFragment.java:142-144`）で、同じ一覧の別項目と二重だった

**Steps**:

- [x] 1. `implementation/testdata_notation.rst` を基準で見直す。**完了**。10コミット
  （`3e01b69`・`09779f6`・`d6b5e7a`・`672fde3`・`d004ec0`・`19e6f2d`・`340e0e4`・`f46c076`・
  `e1f3d4c`・`85deedd`）。58行削除・21行追加
- [x] 1a. 波及の処置。`tools/testdata_converter.rst:276` の `otherHeaderColor` の説明から
  `DEFAULT` を落とした（`f46c076`）。データタイプ一覧から `DEFAULT` を外したことによる。
  あわせて `mapping/glossary.md` §5.8「データタイプ」の件数を14種→13種に合わせた（`19e6f2d`）
- [x] 1b. 走査漏れの拾い直し。1回目はキーワードを手掛かりに走査したため5件を取りこぼし、
  段落ごとに問う読み方で読み直して処置した（`e1f3d4c`・`85deedd`）
- [x] 2. `implementation/testdata_examples.rst`（2,264行）を同じ基準で見直す。**削除分は完了**。
  4コミット（`839c69f`・`8ee645d`・`7d5e844`・`6d88ec8`）。14行削除・9行追加。
  最初から段落ごとに問う読み方で行った（キーワード走査はしていない）。
  **「例そのものが多すぎないか」は基準に無い観点だが、該当する箇所は出なかった。**
  記載例ページのノイズは、例の繰り返しではなく「例に付けた注釈が帰結・既出」の形で出た
- [x] 2a-1. `record-separator` の「エラーにならない」の扱い。**決着**（user 判断 2026-08-25）。
  記述は残し、太字だけ外した（`4651903`）。`"\r\n"` は利用者が正しく書こうとして選ぶ書き方で、
  同じ段落のタブ文字の説明と同じ形をしており「正しく書こうとしても踏む」に当たる。
  裏付けは `4651903` のコミットメッセージ（`nablarch-testing@e21bf67` の
  `DataFile.java:304`／`:325-328`／`:294-300`、`LineSeparator.java:57-64`）。
  **下流の `nablarch-core-dataformat` の挙動は未確認**（`nablarch-core` は clone していない）
- [x] 2a-2. 特殊記法の記載例が無い件。**完了**（user 判断 2026-08-25「あるべき姿にして」）。
  2コミット（`db8a62e`・`fcf51c5`）。**空振りしていたのは空文字・改行だけではなく4項目**で、
  `${文字種,文字数}` と `${attach:ファイルパス}` にも記載例が無かった。4項目すべてに記載例を足し、
  節冒頭の断り書き「なお、空文字・改行の記述例は、この節では示していない。」を落とした。
  `implementation/testdata_notation.rst:1370`・`:1420`・`:1470` の3本の参照が成立した
- [x] 2b. 波及の処置。`implementation/testdata_notation.rst` の改行文字の行2箇所を実装に
  合わせた（`db8a62e`）。**元からあった欠陥だが、正しい記載例を足すと記法ページと矛盾するため、
  今回の変更が作る不整合として本タスクで直した**（`~/work/cowork/nablarch/ntf-doc-renewal/02-進め方.md`
  「範囲外と申し送りの使い分け」）。Excel の `\n` は既定で変換されず2文字のまま残ること、
  YAML は `"\r"`・`"\n"` の両方が効くこと。裏付けは `db8a62e` のコミットメッセージ
- [x] 2c. **レビュー。完了**（2026-08-25）。ラウンド1の4観点をサブエージェントで実施し、
  指摘22件（実質12件 ＋ 指示文への指摘1件）を全件是正、1件を却下した。**ラウンド2は回していない**
  （理由は下の「ラウンド1 の結果」）。是正は `bebd00b`・`6bdbcd7`、記録は `6b9771b`
- [x] 2d. **レビューを起点に確定した仕様2件とページ構成の是正1件**（2026-08-25、user 判断）。
  2コミット（`6e8e4f8`・`2204eb9`）
  - 2ページの役割分担を確定し、基準「他の箇所で既に言っている」の適用を**同一ページ内に限定**した
    （`6e8e4f8`。上の「確定した基準」に本文がある）
  - **YAML の null の仕様を確定した** — クォートなしの `null` は Java の null、`"null"` は
    文字列の null。YAML は構文自体が両者を区別できるため、形式の都合で決まる。
    `tools/testdata_converter.rst:20` は既にこの仕様で書かれており、記法ページ・記載例ページの
    側が食い違っていた（4箇所を是正）
  - **インタープリタの説明を第3部から第2部へ移した。** クラス名一覧はアーキテクトの領域で
    （`design.md:345`）、利用者はクラス名を知らなくても特殊記法を書ける。あわせて
    **第2部に「テストデータの形式をYAMLに変更する」を新設した** — YAML 形式を使うための設定が
    第2部のどこにも無く、読者は記法を読めても使い始められない状態だった
- [ ] 3. `01-現在地.md` の残り10論点を突き合わせ、基準で消えるものを落とす。**進行中。**
  着手前に上の「確定した基準」を読むこと（2ページの役割分担と適用範囲の線引きが入っている）。
  **表の行番号は `d86bb59` 時点でずれているため、使う前に実物を開く**

  **進め方の追加**（user 指示 2026-08-25）: **あるべき姿が自明なものは確認を仰がず直す。**
  上の「直接修正の段取り」3（書き直しになるものは案を出して止まる）は、**あるべき姿が
  自明でないものにだけ当てる**。

  | 論点 | 状態 |
  |---|---|
  | 2 `"-"` の副作用 | **決着（`f7a3257`）。** `:1057` に「この場合、値に含まれる改行と、その前後の空白は取り除かれる」を追記した。基準の「利用者が正しく書こうとしても踏む」に当たると判断（セル内で折り返して書いた値がどう格納されるかを知らないと期待値が組めず、`"-"` の1文字からは分からない）。**申し送りの元文言「値は改行コードと前後空白が除去される」（`input/ntf-testdata-doc.md:417`）は不正確なので採らなかった。** 実測（`nablarch-testing@e21bf67` に置いたプローブテストで `.xls` を組み `DataFile#write()` の出力バイト列を確認）: `"  abc  "` は7バイトのまま＝前後空白は残る（フィールド長も7）、`"line1\nline2"`→`"line1line2"`、`"p \n q"`→`"pq"`、`"tail\n"`→`"tail"`。実装は `DataFileFragment.java:76` `REMOVE_LS_SP_PATTERN = "\s*[\r\n]\s*"` を `:108`-`:110`（`addValue`）・`:176`-`:178`（`addValueWithId`）の `"-"` フィールドだけに適用し、除去後の値をそのまま格納する（埋め戻しなし。`:112`→`:114`→`:386` `toDataRecords()`／`:574` `writeWith()`） |
  | 2 続き: JSON・XML の電文 | **決着（`9cf44af`）。** `:1222` の tip が「電文ごとに電文長が異なるため、テストデータの内容に応じて電文長が自動計算される」と結果だけを書き、前提（メッセージボディのフィールド長に `"-"` を指定する）が抜けていた。実測: 同じセル値（19バイト、セル内改行つき）で `"-"`→record-length 15・改行除去、`"19"`→19・改行が残る、`"40"`→40・改行が残る。**内容に応じて決まるのは `"-"` のときだけ。** NTF 自身のテストデータも `src/test` の .xls 59件中、フィールド長に `"-"` を使う65件がすべて `core/messaging` 配下（`MessagingRequestTestSupportTest.xls` `testUseStructFwHeaderDefJSON`、`RequestTestingMessagingClientTest.xls` `testSendSync` ほか。XML はセル内改行で折り返して書かれている）。旧解説書も `http_real.rst:170` で同じことを言っており、作り直しで落ちていた |
| 5 パディング | **不成立（回帰していない）。** 「データ型に応じたパディング」は `:889` に `#9`（`a0d09aa`）から一貫してある。残っていた `:880` の括弧書き「スペースパディング」だけを `:889` と揃えた（`8fe964b`） |
  | 9 マーカーカラムの対象 | **決着。** 5箇所を是正（`faebf90`）。掛かるのは `SETUP_TABLE`・`EXPECTED_TABLE`・`EXPECTED_COMPLETE_TABLE`・`LIST_MAP` の4つだけで、ファイルデータ・メッセージングには掛からない。`HeaderLine` を参照するのは `ListMapParser`・`TableDataParser` の2クラスのみ（`nablarch-testing@e21bf67`）。`EXPECTED_COMPLETE_TABLE` の欠落も補った（`BasicTestDataParser.java:171-181`） |
  | 10 0件テーブルの書き方 | **決着済み（対応不要）。** `#23`（`b75f1d7`）で既に書かれている。`:728`-`:736` に専用節、Excel は `:786`、YAML は `:833` |
  | 3・6・7・11 | 未着手。仕様の判断が要る |
  | 12・13 | 未着手（TODO 管理） |

**検証**（Step 1 時点）:

- Docker フルビルド `build succeeded.`、`WARNING:`／`ERROR:` 0件。直後に
  `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し `_build`・`build.log` を削除済み
- `verify_mapping.py` exit 0（`OK: no errors`。597行 / lines 12,986 / DROP除く 11,983）、
  `verify_glossary.py` `RESULT: OK`（9カテゴリ不一致0件）
- 削除した文言が他ページに残っていないことを走査（`DEFAULT`・「データ要素数」・「整形・補完」・
  「数を超える位置の値」は `ja/development_tools/testing_framework/` 配下に残存0件）
- `tools/testdata_converter.rst:71` は削除した表を参照していない（事実を自分で述べており、
  参照は `:ref:` のページ単位）

**検証**（Step 2 時点）:

- Docker フルビルド `build succeeded.`、`WARNING:`／`ERROR:` 0件。直後に
  `_build`・`build.log` を削除し `git status --short` が空であることを確認
- `:ref:` の解決（このページの参照先ラベルが `ja/` 配下に全て存在すること）と段落内改行を
  独立に走査。未定義ref 0件、段落内改行 0件
- 削除した文言が他ページに残っていないことを走査。残ったのは
  `implementation/testdata_notation.rst:279`（「テストが成功してしまう」）のみで、これは
  帰結を正面から扱う節の本体であり、記載例ページはそこを `:ref:` で指している
- `verify_mapping.py` exit 0（597行 / lines 12,986 / DROP除く 11,983 と Step 1 から不変）、
  `verify_glossary.py` `RESULT: OK`。**ただしこの2つは `ja/` の本文を読まないため、
  本変更に対しては感度を持たない。**「緑だから正しい」の根拠には使えない
  （`nablarch/CLAUDE.md` 1-4）。本変更を検知しうるのはフルビルドと ref 走査だけである

**レビュー**: Step 1 と Step 2 の削除だけの範囲では回していない。削除が主で、公開本文に新しい記述が
入らないため（`nablarch/CLAUDE.md` 3-1 の「既存のものの是正」に当たる）。**判断の根拠は各コミット
メッセージにあり、user が差分を見る前提で進めている。**

**Step 2a-2（`fcf51c5`）で公開本文に新しい記述が入ったため、ここからは 3-1 により回す対象になる。**

**Step 2c の回し方**（ラウンド1・4観点。`nablarch/CLAUDE.md` 3-2）:

対象は `db8a62e`・`fcf51c5` の差分と、**ディレクターがコミットメッセージに書いた根拠そのもの**。
削除だけの13コミット（`3e01b69`〜`6d88ec8`、`4651903`）は対象外とする。既に user が差分を見る
前提で決着しており、蒸し返すとラウンドが伸びるため。

| 観点 | この差分で見るもの |
|---|---|
| A 充足 | `testdata_notation.rst` の特殊記法の節が挙げる記法のうち、記載例が無いものが他に残っていないか。`:1370`・`:1420`・`:1470` の3参照が本当に成立したか |
| B 整合 | 追加した記載例が `notation` の表・本文と食い違わないか。とくに改行文字の2行（`db8a62e` で変更）と記載例が一致しているか。他ページの相互参照を壊していないか |
| C 規約 | `mapping/style.md` の13観点（S-01〜S-13。**11観点ではない。S-11 は `#9`、S-12・S-13 は `#28` で追加済み**）、`mapping/glossary.md` の正表記。新設した3つの節見出しの語と、既存の節見出しのトンマナが揃っているか |
| D 検証の妥当性 | **ディレクターが行った確認は、誤りを検知できる形だったか。** フルビルドと `:ref:` 走査は「未定義ラベル」しか見ない。**表の値・パス・記法が実装と合っているかは検知しない**。そこを別の手段で確かめる |

**各担当のプロンプトに必ず入れる3点**（`steering.md` の Rules、`nablarch/CLAUDE.md` 3-2）:
実測で裏付ける／付属の検証スクリプトを正解として使わず独立に組む／敵対的に見る。

**3-4 を必ず入れる。** 今回はディレクターが実装を追って表の値・パス・記法を**逐語で**書いている。
直近2ラウンドで重大な指摘が出たのはいずれもこの形だった。観点B と観点D の担当に、
**「コミットメッセージが挙げる `file:line` を1件ずつ開き、そこに書いてあることが本当にその主張を
支えているか」** を明示的に指示する。検証すべき逐語は次のとおり:

- `PoiXlsReader.java:123`（空セル→空文字）
- `YamlFileBuilder.java:218-238`（YAML の `rows:` 配列は空要素でも読み飛ばされない）
- `CompositeInterpreter.java:21`・`:27-38` と `BasicJapaneseCharacterInterpreter.java:31`
  （`${文字種,文字数}` が文字列の一部にも使える理由）
- `BasicJapaneseCharacterGenerator.java:42`・`:43`・`:50`（例で使った文字種が有効）
- `HttpRequestTestSupport.java:977`・`:988-997`・`:948-974`・`:957`（`${attach:}` の経路とパス基準）
- `LineSeparatorInterpreter.java:31`・`:34`・`:60-65`（Excel の `\n` が変換されない）
- `unit-test-yaml.xml:56-76`（`:65`。`yamlInterpreters` が `LineSeparatorInterpreter` を含む）

参照コミットは `nablarch-testing@e21bf67`・`nablarch-testing-yaml@190cc9a`。**作業ツリーではなく
`git show <pin>:<path>` で読ませる**（`nablarch/CLAUDE.md` 1-1）。

**ラウンド2以降は差分限定の2観点だけ**（是正が指示範囲に収まっているか／是正が新しい欠陥を
生んでいないか）。上限3ラウンド。**各ラウンドの指摘件数と観点をここに記録する。**
**既決事項に反する指摘は却下し、却下の理由を記録する**（3-5）。既決事項は本エントリの
「確定した基準」「`#35`・`#33` の決定を上書きした箇所」「論点の決着」。

**ラウンド1 の結果**（2026-08-25。4観点を別々の担当で実施）:

| 観点 | 指摘 |
|---|---|
| A 充足 | 4件 |
| B 整合 | 7件 |
| C 規約 | 6件 |
| D 検証の妥当性 | 5件 |

計22件、重複を畳んで実質12件 ＋ ディレクターの指示文への指摘1件。是正は `bebd00b`（①）と
`6bdbcd7`（8件）。**差し戻しは0回**（是正はすべてディレクターが直接コミットした）。

**重大3件はいずれも観点B・D が拾った。**

1. **記載例が実装の出力と違っていた**（①）。観点D が `nablarch-testing-yaml` を実際にビルドし、
   `testdata_examples.rst` の YAML 記載例そのものを `YamlTestDataParser#getSetupFile` →
   `DataFile#write()` に通して実測した。「可変長ファイルの空行は `""` と記述する」で得られるのは
   `,,` であって空行ではない。**Step 2a-1 が「未確認」と明記した `nablarch-core-dataformat` の
   領域を、記載例として確定させていた。** 是正は `bebd00b`
2. **`db8a62e` のコミットメッセージの出典が実在しない行を指していた**（A・B・D が独立に検出）。
   下の「記録の訂正」を参照
3. **「欠けていたのは4項目」を、その読み方では証明できなかった**（`#10b` と同型）。観点D が
   記法2表の「値の種類」24項目を機械抽出して照合し、節内出現0件が2項目残ることを示した。
   うち Excel の文字列 `"null"` は例の不足ではなく**記述そのものの誤り**で、`6bdbcd7` で是正した
   （`true`・`false` は `:425` 等に実例があり、利用者は踏まないため例を足していない）

**却下した指摘**（3-5）:

- **観点C の指摘4・5**（`db8a62e` の備考セルが当該表で唯一の複数文かつ最長／「記述方法」列の
  括弧の意味が既存4件と異なる）。`mapping/style.md` に該当条項が無く、ページ全体では表セル538件中
  32件が複数文である。かつ「`\n` は変換されず2文字のまま残る」は利用者が正しく書こうとして踏む
  情報であり、置き場所が備考欄しかない。**観点C 自身も「規約違反には当たらない・記録にとどめる」
  としている**

**ディレクターの指示文への指摘**（3-4 が狙った形。**本ラウンドで最も価値のあった指摘**）:

- **本エントリの「Step 2c の回し方」が「`mapping/style.md` の11観点」と書いていたのは誤り。**
  `style.md:12`-`:13`・`:857` は「観点は次の13個に限定する」と明記し S-01〜S-13 を定義している。
  11観点だったのは `#9` より前（S-11 追加前）で、S-12・S-13 は `#28` で追加された。指示どおり
  11観点で判定すると、**今回の差分に多数該当する S-13（`\ ` エスケープ）が判定漏れになる**。
  観点C の担当が誤りに気づき13観点で判定し直した。**下の観点C の行を13観点に訂正済み**

**記録の訂正**（`db8a62e` のコミットメッセージ。コミットは push 前だが履歴を書き換えず、ここに残す）:

- `db8a62e` は「`yamlInterpreters` が `LineSeparatorInterpreter` を含むことは
  `nablarch-testing-yaml` `190cc9a` の `src/test/resources/unit-test-yaml.xml:56-76`（`:65`）で
  確認した」と書いているが、**`190cc9a` のこのファイルは全20行で `:56-76` は存在しない**。
  同ファイルは `:5` の `<import file="unit-test.xml"/>` と `:14` の `ref="yamlInterpreters"` を
  持つだけで、定義本体は無い。**正しい出典は同リポジトリの `src/test/resources/unit-test.xml:56`-`:76`
  （`:65` が `LineSeparatorInterpreter`）**。行番号レンジは一致しており、ファイル名だけの誤りである。
  主張の結論（YAML 経路にも `LineSeparatorInterpreter` が入る）は正しい
- あわせて、`db8a62e` が根拠に挙げたのは `src/test/resources` 配下のテスト用リソースであり、
  **出荷される既定設定は `nablarch-testing-default-configuration:5u26` の
  `nablarch/test/test-data-interpreter.xml:10-16`** である（観点D が実測）。Excel 側の
  「デフォルト設定で変換されるのは `\r` のみ」は出荷既定と一致することを観点D が確認した。
  **YAML 用の既定チェーンは出荷物に存在しない**（未出荷）。ただし現在の YAML 側の備考は
  パーサの挙動を述べており「デフォルト設定」の語を使っていないため、本文の是正は不要

**申し送り22・31 の解消**（`reviews/` は保全記録のため追記せず、ここに記録する）:

- 申し送り22（`reviews/page-testdata_examples.md:329`）・申し送り31
  （`reviews/page-testdata_notation.md:416`）が挙げた「書き方 → 記載例 → 書き方 の往復で
  行き止まりになる」は、**(c) 記載例ページに不足する例を追加する**を `fcf51c5` で実施して解消した。
  根本原因（基準を2ページ間に当てていたこと）は「確定した基準」の2ページの役割分担で解いている

**未決**: なし（論点13 は 2026-08-26 に決着。下の Step 3 の表を参照）。

`implementation/testdata_notation.rst:799` の「データ行を書かない場合でも、カラム名の行は省略できない。
識別子行の次の行がカラム名の行として読み込まれるため、カラム名の行を書かないと、その次に現れた行が
カラム名の行になる。」は、実測どおりで**変更不要**と確定した（この文は「Excel形式の場合」の節の中にあり、
`:803` の「YAML形式の場合」より前にあるため、形式の限定も正しい）。

**ステップ4でモジュールへ申し送るもの**（`#36` で増えた分。既存の `TODO(NTF-MOD-*)` 5件・
依頼書3本とは別）:

- **`nablarch-testing-yaml` のテスト用 `yamlInterpreters`**（`190cc9a` の
  `src/test/resources/unit-test.xml:56`-`:76`）が `NullInterpreter` と `LineSeparatorInterpreter` を
  含んでおり、**上で確定した YAML の null の仕様と食い違う**。`NullInterpreter` が入っていると
  `"null"` も Java の null になる。テスト側を仕様に合わせる。**解説書
  （`setup/common.rst` の「テストデータの形式をYAMLに変更する」）が SSoT である**
- 超過値を黙って捨てる実装挙動（論点4。`nablarch-testing@e21bf67`
  `DataFileFragment.java:105-108`）
- **`nablarch-testing-yaml` のスキーマ `ntf-testdata-yaml-schema.json:410` の `length` の
  description が不正確**（`0db2221` で実測）。「\"-\" フィールドの値は NTF が格納時に改行コード
  および前後空白を除去する」と書いているが、除去されるのは**改行と、その前後の空白**であって、
  改行を含まない値の前後空白は残る（論点2 の実測。解説書側は `f7a3257` で是正済み）。
  スキーマ description も SSoT 範囲なので、解説書の文言に合わせる
- **`nablarch-testing-yaml` の `YamlSection.isBlankRow` が Java null を空扱いしている**（論点6 の決着）。
  Excel は文字列に対して空判定を行うため文字列 `null` は非空で行が残る。YAML を Excel に合わせる。
  あわせてスキーマ `ntf-testdata-yaml-schema.json:108`・`:136` の description が現行の YAML 挙動を仕様として
  書いているため、解説書に合わせる
- **`nablarch-testing-converter` の中間モデルが Excel の表現を持っている**（論点11 の調査で判明。`60d9a2d` で実測）。
  `TestDataBlock.groupId` は整形済み（`[case1]`）で、`YamlFormatReader.java:486`-`:487` が YAML の生値を
  読み込んだ直後に `"[" + groupId + "]"` で囲んでいる。`[ ]` は Excel 形式の書式の一部であって値ではないため、
  **中間モデルが `[ ]` を持つのはあり得ない**（user 判断 2026-08-26）。中間モデルは生値で持ち、`[ ]` の
  付け外しは `XlsFormatWriter`（`:530`）と Excel リーダー（`TestCoreReaderAdapter.java:283`-`:285`）の
  中だけで行う。`YamlFormatWriter.rawGroup` の「外側1組が `[` `]` なら外す」という推測剥がしは不要になる。
  **現状は壊れていない**（`case1`・`[a]x[b]`・`a[1]`・`a]1` の4種で YAML→Excel→YAML を実測し、
  Excel 識別子が `SETUP_TABLE[[a]x[b]]=TEST_TABLE` 等と正しく囲まれ、4件とも元の値に戻ることを確認）。
  壊れていないのは両リーダーが必ず同じ形に揃えているためで、モデルの持ち方が正しいからではない。
  **申し送り XLS-39 が挙げた「`SETUP_TABLE[a]x[b]=` になり戻すと `a]x[b` になる」は現在のコードでは起きない**
  （申し送りは 2026-08-19 時点で、その後 converter は31タスクを完了している）
- **`nablarch-testing-junit5` に、解説書が書いた `TestRule` の順序を押さえるテストが無い**（`2ebea7e` で実測）。
  解説書 `setup/junit5_extension.rst` は「リストの先頭にあるものほど内側、末尾にあるものが最も外側」と書いたが、
  `resolveTestRules()` が返すリストの順序を検証するテストは存在しない（`StandardTestRuleIntegrationTest:186` の
  `RuleChain` のテストは `RuleChain` 自身の入れ子順であって、リストの順序ではない）。**追加を求める。**
  レビュー役の独立プローブでの実測: 2件のルールを `[FIRST, SECOND]` の順で返すと
  `SECOND:before, FIRST:before, BODY, FIRST:after, SECOND:after`、`[SECOND, FIRST]` に入れ替えると
  `FIRST:before, SECOND:before, BODY, SECOND:after, FIRST:after`（負のテストとして順序に感度があることを確認済み）。
  他の記述（包む範囲・`@BeforeEach` 失敗・`Timeout` × `DbAccessTestExtension`・`@TestFactory`・`@Nested`・
  `base` の呼び出し回数・基底実装が空リスト）は既にテストがある（`TestRuleLifecycleIntegrationTest:29`・`:40`、
  `TimeoutDbAccessIntegrationTest:80`・`:93`、`TestFactoryRuleIntegrationTest:37`、
  `NestedTestRuleSupportIntegrationTest:52`、`TestRuleInvocationContractIntegrationTest:47`・`:59`、
  `TestEventDispatcherExtensionTest:172`、`TestRuleEmulationIntegrationTest:118`）ため、求めるのはこの1件だけである
- **`nablarch-testing-junit5` の `TimeoutRuleIntegrationTest:80` のテスト名が、解説書に無くなった例を指す**（`2ebea7e`）。
  テスト名は「解説書の例と同じ実装でTimeoutを追加するとテストがタイムアウトすることをテスト」だが、`#36` で解説書の
  実装例を `Timeout` からプロジェクト独自の `TestRule` に差し替えたため、指す先が無くなった。テスト自体は `Timeout` の
  振る舞いを押さえるものとして残し、名前と Javadoc から解説書への参照を外す

| 2 続き2: JSON・XML の記載例 | **決着（`615b72c`）。** 記法ページが `:1165`・`:1222` で JSON・XML の注意を述べ `:1256`・`:1270`・`:1301` から記載例へ送っているのに、記載例ページのメッセージング節の例はすべて数値のフィールド長で、JSON・XML の書き方を一度も示していなかった。L3「JSON・XMLの電文を記述する」を新設し Excel・YAML 両形式を示した。題材は NTF 自身のテストデータの形（電文を複数フィールドに分割し各フィールド長を `"-"`）。**実測: `.rst` の `code-block:: yaml` から YAML を機械的に抜き出してファイル化し `YamlTestDataParser#getMessage` に、セル格子表を同じ値で `.xls` に組んで `BasicTestDataParser#getMessage` に通し、`toDataRecords()` と `getFwHeader()` が完全一致することを確認（総合=OK）** |
| 6 空行スキップ（論点3 を含む） | **決着（`5301d6e`。user 判断 2026-08-26「案A ＝ Excel に合わせる」）。** `notation:1498`・`examples:2519` の「全要素が **null または**空文字のエントリは読み飛ばされる」が誤り。**実測（`nablarch-testing@e21bf67` と `nablarch-testing-yaml@0db2221` の両方にプローブを置き、同じ意味のテストデータを `getListMap` に通して比較）: 食い違いは1点だけで、全セル／全値が null の行が Excel では残り YAML では消える。** 原因は空判定の対象の違い（Excel は文字列に対して判定するため文字列 `null` は非空＝`PoiXlsReader.java:140`-`:147` の `isBlankLine`。YAML はパース時点で Java null になった値を空扱い＝`YamlSection.isBlankRow`）。Excel を正とした理由は、NTF 仕様は1つで両形式はその表現にすぎないこと、Excel の後方互換を壊す理由がないこと、`YamlSection` の Javadoc 自身が「Excel の全セル空行と同じく扱う」と意図を宣言していること。**場合分けは書かなかった**（全セル／全値が null の行はローカルの nablarch 全リポジトリの `.xls` 302件に0件。利用者が正しく書こうとして踏む書き方ではない）。あわせて「Excel 形式では、この判定はマーカーカラムを除外する前に行われる」の限定を外した（YAML でも同じ挙動であることを実測）。**論点3（カラム名決定行）は本文変更不要**。「空行を除いたあとの先頭行がカラム名行」は両形式で挙動が一致することを実測で確認し、Excel 側 `:797`・YAML 側 `:816` のいずれも空行の読み飛ばしと矛盾しない。Docker フルビルドで WARNING・ERROR 0件 |
| 7 テーブル系識別子の大文字化 | **決着（2026-08-26。本文変更なし。user 判断「書かない」）。** **実測（`e21bf67`）: テーブル名は trim＋大文字化（`TableData.java:97` の `name.trim().toUpperCase()`）、カラム名は大文字化のみで trim されない（`:492`）、`LIST_MAP` のキーはどちらも掛からない**（`TableData` を通らない）。プローブで `"  test_table  "`→`TEST_TABLE`、`{"col1"," Col2 "}`→`COL1`・`  COL2 `、`LIST_MAP` のキー `user_id`・` Name ` は書いたまま、を確認した。**書かない理由**: 小文字で書いても大文字で書いても動くため大文字化は観測できず、`LIST_MAP` のキーは書いたとおりのものがテストコードへ返るので自分が書いたキーで引く限り一致する。確定した基準に当たらない。`testShots` のカラム名は `Map#get` の完全一致で引かれ大小を区別するが、解説書の表どおりに書けば当たる。スキーマ `ntf-testdata-yaml-schema.json:103` の「NTF により trim・大文字変換される」は**テーブル名については正しい**ため、スキーマ側の是正も不要。**未確認**: 小文字でなければ解決できない識別子を使う DB での挙動は動かして確かめていない |
| 11 グループIDに使える文字 | **決着（2026-08-26。本文変更なし。user 判断「書かない」）。** **実測（`e21bf67`）: `[` と `]` は解析されていない。** グループIDを扱う処理は2つだけで、`formatGroupId`（`BasicTestDataParser.java:253`-`:266`）が `"[" + gid + "]"` で囲み、`isTargetType`（`GroupDataParsingTemplate`）が `データタイプ名 + [グループID] + '='` を `startsWith` で比較する。角括弧を探す・外す・対応を取る処理は無い。プローブで `case1`・`ケース1`・`case 1`・`case-1`・`case_1`・`case.1`・`c/d`・`a b c`・` case1 `・`1`・`#c`・`//c`・タブ入り・`case[1]`・`case]1` がすべて hit=1 になることを確認した。**解析されるのは `=` だけ**で、`getTypeValue`（`TestDataParsingTemplate.java:250`）が最初の `=` で切ってテーブル名・ファイルパスにする（`TableDataParser.java:91`／`DataFileParser.java:115`）。そのためグループIDに `=` を含めると名前が黙ってずれる（`SETUP_FIXED[case=1]=out_6.dat` → パス `1]=out_6.dat`）。エラーにはならない。**書かない理由**: 通常のグループIDは英数字・ハイフン・アンダースコアであり、`=` を書くのは書き間違いで、確定した基準に当たらない（user 判断）。**converter は文字種で拒否しない** |
| 12 `TODO(NTF-MOD-01-3)` の解除可否 | **決着（2026-08-26）。TODO を削除した。** **実測: `nablarch-testing-converter` `60d9a2d` で、`setup_tables`・`expected_tables` の両方に `rows: []` を書いた YAML を Excel へ変換し、さらに YAML へ戻すと `rows: []` が保たれて元に戻る。** TODO 本文の「0件テーブルを含む YAML は Excel へ変換できない」は事実ではない。変換経路は `TableData#loadData()` を呼ばない（converter の `src/main/java` に `loadData` の参照は0件）ため、この結果は `nablarch-testing` の#23 の適用有無に依存しない。解除条件「`XLS-27` の2段目へ切り替わったら」は満たされ得ない（`XLS-27` はマーカーカラム方式 `[EMPTY]` で決着。`XlsFormatWriter.java:213`・`:252`・`:543`）。#23 は `origin/main`・`origin/develop` に未マージ（`TableData.java:341` の early return が残る）。本文の書き直しは不要で、`rows: []` を教える2節も現状のままで正しい。台帳 `checks/task-last.md` §8 から行を外した |
| — 業務サンプルからの参照 | **決着（2026-08-26）。** `ja/biz_samples/04/0401_ExtendedDataFormatter.rst:181` が「プログラミング・単体テストガイドの自動テストフレームワークの使用方法を参照すること」と地の文で書いており、`:ref:` になっておらずリンクにならないうえ、`glossary.md:515` の禁止語「自動テストフレームワーク」を使っていた。`setup/request_unit_test/mom.rst` の「テストデータの変換処理を実装する」節に S-08 の形式でラベル`request_unit_test_setting_mom-test_data_converter` を新設し（`ja/` 全体で重複0件を確認）、参照を `:ref:` にした |
| — マスタデータ投入ツールの YAML 対応 | **決着（2026-08-26）。`tools/master_data_tool.rst` を書き直し、`TODO(NTF-MOD-02-4)` を削除した。** #22 は `nablarch-testing` の PR ブランチ `convert-testdata-excel-to-text` `3c4bd2a` で実装済み（`MasterDataSetUpper.java:185-204`）。**実測**: YAML 形式のマスタデータファイルは `<masterdata.dir>/<ファイル名>.yaml`（テストクラスに対応するディレクトリは作らない）、1ファイルが1つの読み込み単位でシート相当の区切りは無い、拡張子 `.yml` は無言で0件。`masterdata.file` は Ant の `<include name>` パターンでありファイルを指す（`master_data-build.xml:65-67`）ため YAML 形式では `MASTER_DATA*.yaml`。`.. important::`（Excel ファイル＋YAML パーサ＝無言で0件）は残し、逆向き（YAML ファイル＋Excel パーサ）は `IllegalArgumentException: invalid data name. [MASTER_DATA]` になり無言ではないため書かない。実測の全件は `checks/task-last.md` §8 の `NTF-MOD-02-4` の段落 |
| — JUnit 5 拡張の `TestRule` 再現 | **決着（2026-08-26。user 判断「A ＝ 実装例を独自 `TestRule` に差し替える」）。`setup/junit5_extension.rst` の「JUnit 4のTestRuleを再現する」節を書き直し、`TODO(NTF-MOD-03-1)` を削除した。** 修正は `nablarch-testing-junit5` の PR ブランチ `worktree-fix-resolveTestRules` `2ebea7e` で実装済み。**旧本文の `.. important::`（スーパクラスの `resolveTestRules()` をベースにする）は実物では誤り**で、基底実装は `Collections.emptyList()` を返し（`TestEventDispatcherExtension.java:531-533`）、NTF 内部のルールは新設の `resolveInternalTestRules()`（`:479`）が返す。実装例を `Timeout` から独自 `TestRule` に差し替えたのは、実物が「JUnit 5 に同等機能があるならルールを移植するな」と定めており（`:44-50`）`Timeout` はその筆頭であること、`Timeout` は `DbAccessTestExtension` と併用すると DB 接続を取れないまま**テストが成功する**こと（`:166-177`）による。静かに壊れる5件を `.. warning::` に列挙した。リスト順序（先頭＝内側）はレビュー役が独立プローブで実測（負のテスト込み）。**Step 4 へ2件申し送った**（順序のテストが無い／`TimeoutRuleIntegrationTest:80` のテスト名が解説書の消えた例を指す） |
| 13 0件テーブルが次ブロックを食う | **決着（2026-08-26。user 判断「現行通り」）。`implementation/testdata_notation.rst` の「0件のデータを記述する」に形式差を明記し（「Excel 形式ではカラム名の行が必須であり、この行にはカラム名またはマーカーカラムを置く。YAML 形式ではカラム名は不要」）、同ページ「Excel形式の場合」と `implementation/testdata_examples.rst` の記述例にマーカーカラムの書き方を足した。** **user 指摘2件を反映している**: (a) 規則は「カラム名の行が必須で、そこにはカラム名またはマーカーカラムを置く」と1つにまとめる（レビュー役は当初2段落に分けて書いた） (b) 形式非依存の節が形式差を一言も述べていなかったため、そこで明言する。 user の整理: Excel はカラム名が必須、YAML は不要なので**各形式は単独では問題なく動く**。問題があるのは YAML → Excel の変換だけで、変換ツールがマーカーカラムを出すことで対応済み。**レビュー役が独立プローブで実測して確認した**（`nablarch-testing-converter` `60d9a2d`・`nablarch-testing` `3c4bd2a`）: (1) YAML の `rows: []` を Excel へ変換すると `r1` に `[EMPTY]` が1つだけ書かれ、次の `SETUP_TABLE=NEXT_TABLE` は無傷で残り、YAML へ戻すと元に戻る (2) **負のテスト**: 同じ版面からマーカーカラムの行だけを取り除いた Excel を `BasicTestDataParser` に読ませると `1 table(s)`／`EMPTY_TABLE columns=[SETUP_TABLE=NEXT_TABLE]` となり `NEXT_TABLE` が消える。マーカーカラムがあると `2 table(s)`／`EMPTY_TABLE columns=[]`・`NEXT_TABLE columns=[USER_ID, NAME]` (3) カラム名0件のとき本体は DB の全カラムを読む（`TableData.java:345-347`）。**置き場所は user 指示で決まった（2026-08-26）**: 変換ツールのページに書くのは「変換ツールが NTF 仕様以外にやっていること」だけである。形式間（Excel → YAML では〜／YAML → Excel では〜）の記述は、形式が増えるたびに組み合わせが増えるうえ、変換後の姿は記載例と重複するため書かない。マーカーカラムを置くのは NTF の書き方どおりの出力であって変換ツール固有ではないため、記法と記載例に書く。変換ツール固有なのは `[EMPTY]` という語だけで、これは既に `tools/testdata_converter.rst` の `markerColumnColor` の説明にある。**レビュー役は最初これを変換ツールのページに形式間の記述として書き、user 指摘で取り消した** |
| — `TODO(NTF-MOD-*)` の残2件 | **決着（2026-08-26）。`implementation/deal_unit_test/mom.rst` の `NTF-MOD-02-3` と `tools/testdata_converter.rst` の `NTF-MOD-01-2` を削除した。`ja/` の `TODO(NTF-*)` は0件になった。** どちらも解除条件が PR ブランチで満たされており、本文の書き直しが不要であることを実測で確認した。`NTF-MOD-02-3`: `nablarch-testing` `3c4bd2a` の `SendSyncSupport.java:359`・`:420-448` がディレクトリ配下の全エントリの最終更新日時をスナップショットで比較する。**実測（負のテスト込み）**: ディレクトリ配下の `message.yaml` を編集したとき、`main` の判定（ディレクトリ自身の `lastModified`）は**変化せず**、PR ブランチのスナップショットは**変化する**。よって `mom.rst:87`「テストデータのタイムスタンプが更新されると…読み込み直し」は PR ブランチで形式によらず正しい。`NTF-MOD-01-2`: **実測**: `FooTest.xls` と `FooTest.xlsx` を同居させて変換すると `ConverterException: same-name Excel books coexist: in/FooTest.xls, in/FooTest.xlsx (a test class corresponds to exactly one Excel book; remove or rename one of them)` で止まる（`60d9a2d`）。`testdata_converter.rst:112`「`.xls` と `.xlsx` をどちらも対象とする」は変わらず正しく、同名同居はエラーで気づけるため本文に書かない（「利用者が正しく書こうとしても踏むもの」だけを書く基準） |
| — リード文の廃止と `機能概要` の必須化 | **決着（2026-08-26。user 指示）。`ja/` の29ページで、目次と最初のL2見出しの間にあった見出し無しのリード文を「機能概要」の冒頭へ移した。第2部の10ページには「機能概要」のL2見出し自体を新設した。** 規約は `mapping/style.md` S-02・`design.md` §3／§4・`mapping/vocabulary.md` を更新した（第2部の「機能概要」を任意→必須。`#6` の決定を上書き）。**対象外4ページ**: 導線のみの `setup/request_unit_test/db_queue.rst`・`implementation/request_unit_test/db_queue.rst`・`implementation/deal_unit_test/db_queue.rst`（L2 を持たない6行のページ）と、設計上「機能概要」を持たない `implementation/testdata_examples.rst`（`design.md` §4・`vocabulary.md` 例外3）。第1部 `about/index.rst` は `全体像` のL2 が同じ役割を担う既存の例外のため触っていない。**FW解説書の慣習とは意図的に違えている**（FW解説書は見出し無しのリード文を目次と最初のL2の間に置く。20ページ中19ページ。`style.md` S-02 の根拠節）。書き出しの規約（「ここでは、」で始めず対象を主語に立てて言い切る）は引き続き揃える。**下線直後の空行はページごとに混在している**（実測: 空行あり38・空行なし31）ため、各ページの既存の書き方を保った |
| — ツールの並び順 | **決着（2026-08-26。user 判断「素直に一番後ろに置く」）。`tools/index.rst` の `toctree`・`design.md` §5 の図・`mapping/vocabulary.md` の `dest_page` 表の3箇所で、テストデータ変換ツールを末尾へ移した。あわせて `design.md` §5 に規則と理由を明記した。** 経緯: 変換ツールは現行解説書の3ツール（`08_TestTools/01_HttpDumpTool`・`02_MasterDataSetup`・`03_HtmlCheckTool`）の並びの2番目に挿し込まれていたが、**その位置の理由は `design.md`・`steering.md`・`checks/` のどこにも記録が無かった**（`mapping.csv` の行順とも一致しない）。レビュー役は「ライフサイクル順（作る→変換する→投入する→検査する）」という読みを推測として示したが、user が却下した。理由は、ライフサイクルで説明すると「変換ツールは先頭では」という話になり既存3ツールの順序まで組み替える議論になるため。**新設のツールは既存の並びの末尾に足す**という規則にすれば、次にツールが増えても同じ扱いで済む |
| — `[EMPTY]` の記載場所 | **決着（2026-08-26。user 指示）。`tools/testdata_converter.rst` の「前提事項」に1段落を追加した。** **規則: 変換ツールのページに書くのは、NTF 仕様とは別に変換ツールがやっていることだけである。** それ以外は各形式の「書き方」と「記載例」に書く。この規則により (1) マーカーカラムを置くこと自体は NTF の記法どおりなので `implementation/testdata_notation.rst` と `implementation/testdata_examples.rst` に書き、(2) その名前を `[EMPTY]` とするのは変換ツールの決めなので `tools/testdata_converter.rst` に書く、と分かれる。**レビュー役は最初 (1)(2) をまとめて変換ツールのページに形式間の記述として書き（user 指摘で取り消し）、次に両方を記法・記載例へ移して (2) を変換ツールのページから落とした（user 再指摘で復帰）。** `markerColumnColor` の設定項目の説明欄（`tools/testdata_converter.rst`）にも `[EMPTY]` は出てくるが、設定表の中だけでは変換結果を見た読者が辿り着けない |

### #37: Step 4 —— 各モジュールを SSoT（解説書）に合わせる — 進行中

**Purpose**: 解説書を SSoT と定めたうえで、依存する5モジュールの実装・テスト・スキーマを解説書に合わせる。
**指示はリポジトリごとに別ファイルへ分けて出す**（user 指示 2026-08-26）。解説書側の作業は `#36` で完了しており
（図＝png 26枚を除く）、本タスクは解説書を変更しない。

**依存順**（pom 実測 2026-08-26）: `nablarch-testing` → `{nablarch-testing-yaml, nablarch-testing-rest}`
→ `{nablarch-testing-junit5, nablarch-testing-converter}`。`-junit5` は `-rest` に、`-converter` は `-yaml` に依存する。

**参照点**（PR ブランチの先端。2026-08-26 に `git ls-remote` で実測。すべて remote と一致）:
`nablarch-document` = `ntf-yaml-support` `40b9c52` ／ `nablarch-testing` = `convert-testdata-excel-to-text` `3c4bd2a` ／
`nablarch-testing-yaml` = `feature/ntf-yaml` `0db2221` ／ `nablarch-testing-converter` = `ntf-test-data-converter` `60d9a2d` ／
`nablarch-testing-junit5` = `worktree-fix-resolveTestRules` `2ebea7e` ／ `nablarch-testing-rest` = `fix-testdataparser-usage` `a4ec1ee`
（ローカルには未 push の `a8aeb52` があるが、参照点は remote の `a4ec1ee`）。

**全リポジトリ共通の範囲**（user 確定 2026-08-26）:

- **レビューの回し方は指示書ごとに決める**（user 判断 2026-08-26）。**未着手の3本（`-rest` 440行・`-junit5` 453行・`-converter` 333行）はレビューを回さない。**サブエージェントの4観点も rn の既定レビュー（QA / Design / Craft / Verification）も回させず、レビュー役が担当範囲を全量読み直して全件表と突き合わせ独立検証する。担当が小さく再読できること、成果物が記録だけで `src/main`・`src/test` を変更しないこと、**rn の既定4軸に「解説書との一致・呼び出し元・後方互換」を見る軸が無く、既定の QA は完了条件ごとの gate のため完了条件そのものの誤りを素通りすること**（実物: `~/.claude/plugins/cache/ccpm/rn/0.8.0/references/task-execute-workflow.md:18`-`:24`・`:99`・`:103`。2026-08-26 実測）が理由である。**渡し済みの2本（`nablarch-testing` 9,822行・`-yaml` 6,640行）はレビューを残す**（全量再読が重く、「その抽出方式で全件を証明できるか」をレビュー役が代替できない）。ただし**「rn の既定レビューではなく §6 の4観点で回す」ことを伝言で明示する**
- **既知の是正項目＋解説書の全件突合。** 突合の母集合はページ単位で先に固定し、キーワード走査で切り出さない
- **カバレッジ C0/C1 は全件開示方式**（数値目標を置かず、未到達を全件列挙してテスト追加か不要根拠を書く）。
  **対象は今回の変更が持ち込んだ未到達に限り、元から未達のものは対象外**
- **解説書は直さない。** 解説書側が誤っていると判断した項目は、根拠を添えて報告し止める

**指示書**:

- [x] `ntf-step4-01-nablarch-testing.md` —— **渡し済み**。`87a21d6` で `src/main` 変更禁止を反映して差し替えた（差し替えの伝言も渡した）
- [x] `ntf-step4-02-nablarch-testing-yaml.md` —— 作成済み。**本モジュールは `src/main` を変更してよい**（未リリース）。突合の母集合は38ファイル・9,822行を先に固定し、`YAML`/`yaml` が現れる12ファイル・6,640行を担当、残り26ファイル・3,182行は0件を数え直したうえで「対象外」と理由を1行ずつ書かせる（26ファイル分は `nablarch-testing` の母集合が拾うため隙間が出ない）
- [x] `ntf-step4-03-nablarch-testing-rest.md` —— 作成済み。**`src/main` 変更禁止**（リリース済み）。既知の是正項目は無い（申し送りが求めた記述は解説書に0件）。担当は4ページ440行と `setup/junit5_extension.rst` の3箇所（`:55`-`:60`・`:254`）で、母集合38ファイル・9,822行を先に固定したうえ、残り33ファイルに本モジュールの13クラスが0件であることを数え直させる。`:94`（`optional` 指定）は `nablarch-testing-junit5` の `pom.xml` が決めるため junit5 担当
- [x] `ntf-step4-04-nablarch-testing-junit5.md` —— 完了・`#7` 承認済み（2026-08-27）
- [x] `ntf-step4-05-nablarch-testing-converter.md` —— `#33`〜`#39` 完了（`d611bec`）。ディレクター独立検証 合格（2026-08-28。`mvn -o clean test` 656件緑・`@Ignore` 0・ミューテーション9件すべて検知。指示書の誤り2件を `afa4f9e` で訂正）
- [ ] `ntf-step4-06-nablarch-testing-yaml-2.md` —— **第2回。作成済み・未送付**（`c39f701`）。`#42` の追随7件（末尾 null→`""`／電文 `records:` は1つ／`fw_header:` のキー検査／空エントリは `{}` だけ（第1回 2-1 を上書き）／2文字 `\r` はエラー／`@Ignore` 1件の削除／スキーマ description）。本体を oracle にしたテストを求める
- [ ] `ntf-step4-07-nablarch-testing-converter-2.md` —— **第2回。作成済み・未送付**。yaml 第2回の完了後に「渡す前にやること」5点を済ませてから渡す。是正5件（本体にインタープリタ列を渡して解釈させる（A）／マーカーカラムだけの行を残す／交互記述の警告／yaml 第2回への追随／4経路テストの oracle を本体にする）

**ディレクターが各 PR ブランチのピンで実測済みの事実**（指示書に逐語で載せる根拠。すべて `git show <pin>:<path>`）:

- **nablarch-testing**（論点4）—— `DataFileFragment.java:102`-`:115`（`addValue`）・`:169`-`:183`（`addValueWithId`）が
  `for (int i = 0; i < names.size(); i++)` でループを止め、超過値を読まない。同ファイルにログ出力0件。
  呼び出し元は `DataFileParser.java:197`・`MessageParser.java:75`・`SendSyncMessageParser.java:129`・`:134` の4箇所。
  **解説書側は0件**（`grep -rn "数を超える\|超えた位置\|余り" ja/…/testing_framework` が0件）。
  **user 判断（2026-08-26）「現行どおりで解説書影響なし、利用者影響なしなら仕様です」** —— 残るのは利用者影響の判定だけ
- **nablarch-testing-yaml**（論点6）—— `YamlSection.java:201`-`:209` の `isBlankRow` が `toStr`（同 `:127`-`:128`。
  `value != null ? value.toString() : null`）経由で Java null を空扱いする。Excel 側 `PoiXlsReader.java:140`-`:147`
  （`3c4bd2a`）の `isBlankLine` は文字列の `isEmpty()` のみを見る。解説書 `implementation/testdata_notation.rst:1500` は
  「すべての値が**空文字**の場合にスキップされる」と述べ null に触れていないため、YAML 側が食い違う
- **nablarch-testing-yaml**（テスト用インタープリタ）—— `src/test/resources/unit-test.xml:56`-`:76` の
  `yamlInterpreters` が `NullInterpreter`（`:58`）と `LineSeparatorInterpreter`（`:65`）を含む。
  解説書 `setup/common.rst`「テストデータの形式をYAMLに変更する」は `DateTimeInterpreter` と
  `CompositeInterpreter` の2つだけとし、`NullInterpreter` は `.. important::` で明示的に禁じている
- **nablarch-testing-yaml**（スキーマ）—— `src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json` の
  `:410`（`length`。「改行コードおよび前後空白を除去する」）・`:108`・`:136`（いずれも「全ての値が null または空文字の行は
  取り除かれる」）が解説書と食い違う。`:108` には FK 制約の案内と BOOLEAN 型カラムの記述が両立しない箇所も含む
- **nablarch-testing-converter**（論点11）—— `YamlFormatReader.java:485`-`:488` の `formatGroup` が
  `"[" + groupId + "]"` で囲み、`XlsFormatWriter.java:529`-`:531` の `marker` が整形済み前提で連結し、
  `YamlFormatWriter.java:479`-`:488` の `rawGroup` が外側1組の `[` `]` を推測で剥がす。Excel 側は
  `TestCoreReaderAdapter.java:282`-`:286` の `markerGroupId` が `[case1]` ごと切り出す。
  **解説書はグループIDに触れていない**（`tools/testdata_converter.rst` に「グループID」0件）
- **nablarch-testing-junit5** —— `setTestRules` の呼び出しは `src/test/java` に19件あり、**すべて1件または `RuleChain`**。
  リストの順序を押さえるテストは0件。`StandardTestRuleIntegrationTest:186` は `RuleChain` 自身の入れ子順。
  解説書 `setup/junit5_extension.rst:439` の「リストの先頭にあるものほど内側、末尾にあるものが最も外側」は
  `TestEventDispatcherExtension.java:427`-`:428`（`applyTestRules` が順に包む）と Javadoc `:509`-`:510` に対応する。
  `TimeoutRuleIntegrationTest:80` のテスト名「解説書の例と同じ実装でTimeoutを追加すると…」は、解説書が実装例を
  独自 `TestRule` に差し替えたため指す先が無い
- **nablarch-testing-rest** —— 申し送り `.rn/fix-testdataparser-usage/handoff-to-docs.md` が求めた
  「シートが存在しない場合は `setUpDb` が呼ばれない」旨の記述は、**解説書に0件**
  （`grep -rn "setUpDbIfSheetExists\|isExisting\|isResourceExisting" ja/…/testing_framework` が0件）。
  **解説書側の対応は不要**。PR #38 は task #3 が check-off されず user review 待ち
- **nablarch-testing-rest（E-1。2026-08-26 にディレクターが一次情報で独立確認）** —— `setUpDb.yaml` を置いていない
  テストクラスでは、メソッド固有の YAML が**黙って投入されない**。`RestTestSupport.java:79`-`:81`（`ec718a2`）の
  `setUpDb()` が `setUpDbIfSheetExists("setUpDb")` → 同 `(<メソッド名>)` の順に2回呼ぶが、`isExisting()`
  （同 `:216`・`:222`）は `getPathOf()` が null になると `testDataExists` を落とし、以降 parser を呼ばない。
  Excel は**ファイル単位**判定（`PoiXlsReader.java:232`-`:252`（`3c4bd2a`）が `splitLastResourceName` の
  `splitted[0]`＝クラス名だけで `listFiles`。シート名を見ない）のためラッチが落ちないが、YAML は
  **リソース単位**判定（`YamlLoader.java:142`-`:143`・`:81`-`:86`（`0db2221`）が
  `basePath + "/" + resourceName + ".yaml"` の存在を見る）のため落ちる。**そのブランチの Acceptance criteria
  「`YamlTestDataParser` を登録した場合 YAML が読み込まれる」に直接抵触する。** ラッチは `c2604a7` より前から
  あり、同コミットが作ったものではない（差分は `isExisting()` 末尾1行の置換と `getSheet()` の削除だけ）。
  **リリース済みモジュールの `src/main` を触るため user 判断待ち。** ディレクターの推奨は直す。
  判断の前に「ラッチを外すと Excel 経路の挙動が変わるか」の実測を rest CC へ依頼済み（ディレクターの読みでは
  変わらないが**未確認**）。**この判断が出るまで `ntf-step4-03-nablarch-testing-rest.md` を渡さない。
  直す場合は `src/main` が動くため、渡す前にピンを取り直す**

**解説書のページと担当リポジトリ**（2026-08-26 実測。解説書が名指しするクラス103件を各リポジトリの `src/main/java` と
突き合わせ、あわせて `YAML` の出現をページ別に数えた）:

| リポジトリ | 担当するページ |
|---|---|
| nablarch-testing | 38ファイル全部（本体）。他4リポジトリが担当する記述は「対象外」として理由を記録する |
| nablarch-testing-yaml | `YAML` が現れる12ページ（`testdata_examples.rst` 81・`testdata_notation.rst` 42・`tools/testdata_converter.rst` 23・`setup/common.rst` 12・`tools/master_data_tool.rst` 4・`implementation/deal_unit_test/batch.rst` 3 ほか。計171件） |
| nablarch-testing-rest | `setup/request_unit_test/rest.rst`・`setup/deal_unit_test/rest.rst`・`implementation/request_unit_test/rest.rst`・`implementation/deal_unit_test/rest.rst`・`setup/junit5_extension.rst` の rest 記述 |
| nablarch-testing-junit5 | `setup/junit5_extension.rst`（junit5 のクラス23件が出現） |
| nablarch-testing-converter | `tools/testdata_converter.rst`（converter のクラス6件が出現） |

**Completion criteria**:

- 5本の指示書がすべて作成され、各リポジトリへ渡っている
- 各リポジトリが指示書の完了条件を満たし、報告を返している
- 「解説書側の誤りの疑い」として上がった項目に、ディレクターの判定が付いている
- 解説書（`ja/`・`mapping/`・`design.md`）に差分が無い


### #38: `setup/common.rst` —— YAML 形式の電文用インタープリタが自ページの禁止に反していた件の是正 — 完了

**問題**（`c6559eb` で逐語確認）。同じページの中で矛盾していた。

- `:81`（important）「``NullInterpreter`` を指定してはならない。指定すると、文字列として記述した ``"null"`` も Java の null になり、両者を区別できなくなる」
- `:77`「``NullInterpreter``・``QuotationTrimmer``・``LineSeparatorInterpreter`` は指定しない」
- 一方 `:170`「テストデータの記法を解釈するクラスは、Excel 形式と YAML 形式で共通である」とし、`NullInterpreter`・
  `QuotationTrimmer` を含む `messagingTestInterpreters` を、**YAML 形式の** `messagingTestDataParser`（`:250`-`:252`）に
  参照させていた

設定した interpreters は電文の値に実際に掛かる（`YamlMessageBuilder.java:85`・`:110`・`:150`、`0db2221` が
`interpreterResolver.resolve(basePath)` の結果を値加工に使う）ため、`:81` の禁止に実際に抵触する。

**あるべき姿**。YAML の集合は、Excel の集合から YAML 構文が担う分を引いたものになる（`nablarch/CLAUDE.md`・
`02-進め方.md`「NTF 仕様は1つで、Excel 形式と YAML 形式はその表現が違うだけ」）。Excel の電文用は
`NullInterpreter`・`QuotationTrimmer`・`BasicJapaneseCharacterInterpreter` の3つ（`:176`-`:184`）で、
`DateTimeInterpreter` は入っていない（Excel 用パーサ `:220` も同じリストを参照）。`null`／`"null"` の区別は
YAML では構文が担うため、YAML の電文用に残るのは `BasicJapaneseCharacterInterpreter` だけになる。
`yamlInterpreters` の流用は採らない。`DateTimeInterpreter` が電文にも効き、Excel ではリテラルのまま残る
`${systemTime}` が YAML だけ日時に変わって往復変換で意味が変わるため。

**是正**（3箇所）。

1. `:170` の「解釈するクラスは Excel 形式と YAML 形式で共通である」を取り下げ、`:187` に「テストデータの記法を
   解釈するクラス群」を加えて、形式ごとに後述する形にした
2. `messagingTestInterpreters` の定義を Excel 形式の節のコードブロックへ移した
3. YAML 形式の節に `yamlMessagingInterpreters`（`CompositeInterpreter` → `BasicJapaneseCharacterInterpreter` のみ）を
   置き、`messagingTestDataParser` の参照先を差し替えた

**上書きした過去の決定**: `reviews/page-deal_unit_test_setting_mom.md` の R1-2 と V-1。R1-2 は「両形式で共通の
`messagingTestInterpreters` の定義が Excel 形式の節の中だけにあり、YAML 形式しか読まない読者が未定義コンポーネントを
参照してしまう」として定義を共通部へ移し、V-1 はその補強として両 L4 に「前掲の ``messagingTestInterpreters`` の定義と
あわせて記述する」を足していた。**前提だった「両形式で共通」が誤りだったため、両方を取り下げた。**
R1-2 が防ごうとした失敗モードは、各形式の節がそれぞれ自分のリスト定義を持つことで解消している。

**検証**: `docker run --rm -v $PWD:/root/document nablarch-document-build /bin/bash -c "cd /root/document;
sphinx-build -E -a -d _build/.doctrees/ja -b html ja _build/html"` が `build succeeded`、行頭 WARNING/ERROR 0件。
生成物 `_build/html/development_tools/testing_framework/setup/common.html` に `yamlMessagingInterpreters` が2箇所。

**波及先**（実測）: `ja/` 内で `messagingTestInterpreters` を参照するのは `setup/common.rst` だけ
（`grep -rn --exclude-dir=_build` が本ページ以外0件）。

### #39: 電文のレコード種別 —— 形式差として書いていた記述を、データタイプ差の記述に改める — 解説書は完了、モジュール是正は `#37` の yaml 指示書へ

**未決だった論点の決着**（`01-現在地.md` §4 converter 節「レコード種別を `nablarch-testing-yaml` 側で直して Excel と
揃えるか、YAML 形式の制約として解説書に残すか」）。**直す。** 未リリースで後方互換の制約がなく、直さなければ
「Excel で書けるものが YAML では書けない」状態が残るため。

**Excel 側の実測**（`nablarch-testing@3c4bd2a`。呼び出し元から `setRecordType` まで末端まで追った）:

| 解説書の呼び方 | API | パーサ | レコード種別 |
|---|---|---|---|
| `MESSAGE`（`setUpMessages`・`expectedMessages`） | `getMessage` ← `MQSupport.java:87` | `MessageParser.java:60`-`:67` が `onReadingNames` で先頭要素を `"default"` に置換 | **`"default"`** |
| 同期応答メッセージ送信の4データタイプ | `getMessageWithoutCache` ← `SendSyncSupport.java:478` | `SendSyncMessageParser.java:110` が `createFixedLengthFileParser` を上書きし `onReadingNames` は上書きしない | 記載値 |
| 取引単体テストのモックアップクラスの電文 | `getSendSyncMessage` ← `RequestTestingSendSyncSupport.java:157` | `GroupMessageParser.java:43` が `SendSyncMessageParser` へ委譲 | 記載値 |

いずれも `DataFileParser.java:163`-`:166` → `:259`-`:262` の `setRecordType(fieldNamesLine.get(0))` に落ちる。

**YAML 側の実測**（`nablarch-testing-yaml@0db2221`）: `YamlFileBuilder.java:187`-`:189` が `messaging` 経路すべてで
`"default"` に固定する。`buildFragmentsForMessage`（`:139`-`:141`）と `buildFragmentsForSendSync`（`:162`-`:164`）の
両方が `messaging=true` を渡すため、送信同期4キーでも記載値が捨てられる。

**差は送信同期4キーだけである。** `messages` は Excel も `"default"` にするため、YAML と既に一致している。

**解説書の是正**（3箇所）:

1. `implementation/testdata_notation.rst:1163` —— 「Excel 形式と YAML 形式で異なる」という形式差の記述を、
   データタイプ差の記述に改めた。変換で扱いが変わる旨も落とした
2. 同 `:1295` —— 「`record_type` の値は…常に `"default"` に置き換えられる。任意の値を装飾的に記述できるが、
   実行時の挙動には影響しない」の2文を落とした。**既出箇所は `:1163`**
3. `tools/testdata_converter.rst:71` —— 前提事項から「電文のレコード種別も、両形式で扱いが異なる」の段落を削除した

**モジュール側の是正は未了である。** `nablarch-testing-yaml` が送信同期4キーで `record_type` を保持するまで、
解説書が述べる状態に実装が追いついていない。是正は `#37` の yaml 指示書に含める。
既存テスト（`record_type: HEADER` 7件・`record_type: FW_HEADER` 16件が `"default"` を期待している）の
更新もそこで扱う。

**検証**: Docker（README の手順）で ja をビルドし `build succeeded`。警告1件は `_build/html/.buildinfo` の
形式に関するもので、本変更とは無関係。

### #40: Step 4 —— `nablarch-testing-yaml` の突合と指示書の作り直し — 指示書は完成、渡すのはこれから

**旧 `ntf-step4-02-nablarch-testing-yaml.md` は取り消して、新しい型で作り直した**（`#37` の型変更）。
やることは「解説書に書いてあることをテストで押さえる」であり、読み比べて不一致を洗い出す形にしない。

**担当ページの範囲**（ディレクターが実測して確定）。`ja/development_tools/testing_framework/` 配下の
`.rst` 37本のうち、`yaml`（大小文字問わず）が現れる12本から `tools/testdata_converter.rst`（converter 担当）を
除いた **11ファイル・6,307行を全量**。0件の25ファイルを担当外とする根拠は、`テキスト形式`／`両形式`／
`形式によらず`／`どちらの形式` のいずれも0件であること（`c6559eb` 実測。YAML 形式に触れずに YAML 固有の
挙動を述べているページは無い）。

**突合の規模**（実測）:

| | 件数 |
|---|---|
| 担当ページ | 11ファイル・6,307行 |
| テストで検証できる粒度に分解した項目 | **335件**（`可` 259・`不可(静的)` 19・`不可` 57） |
| 既存テスト | 7クラス・**226メソッド**（`@Ignore` 0件） |
| **確定した作業** | **18件**（実装の是正5・テスト追加13） |

分解はサブエージェント3本（`notation.rst`+`common.rst` / `testdata_examples.rst` / 残り8ファイル）に
全量読ませ、拾わなかった行範囲と理由を1行ずつ書かせて行数の検算を取った（3本とも一致、隙間・重複0）。
既存テストの目録も別のサブエージェントに作らせた。**突き合わせと未カバーの判定はディレクターが自分で行い、
指示書の `file:line`・逐語・件数は書いたあとに全部ピンで照合した。** 照合で自分の誤りが1件出た
（`buildListMapRows_blankValueRow*` を3件と書いたが実測2件）。

**実装の是正5件**（`src/main` を変更してよい側）:

1. 空行判定が Java null を空扱いしている（`YamlSection.java:201`-`:208`）。SSoT は
   `implementation/testdata_notation.rst:1500`「空マッピング `{}` またはすべての値が空文字」で null に触れていない
2. `isResourceExisting` の判定単位が Excel と違う（E-1）。呼び出し元3箇所を全走査済み。
   `nablarch-testing-converter` の `YamlTestCoreAdapter.java:102` に波及し、
   `YamlTestCoreAdapterTest.java:365`-`:370` が落ちる（converter は直さず報告させる）
3. 送信同期4キーでレコード種別が潰れる（`YamlFileBuilder.java:187`-`:189`）。`#39` で解説書を先に直した
4. テスト用 `yamlInterpreters` が `setup/common.rst:77`・`:81` の禁止に反する
5. スキーマの `description` 3件（`:108`・`:136`・`:410`）

**テスト追加13件**: いずれも解説書に記述があり既存226件が押さえていないもの。実測で0件を確認した。

**レビューは回さない。** 作業が18件に確定していて探索を含まないため。観点D は完了条件
「期待値をわざと崩すと落ちること」で代替する。

**未確認として残したもの**（サブエージェントが自己申告した「自信の無い箇所」計28件のうち、
指示書に落とさなかったもの）。いずれも解説書に記述が無いために項目化できなかったものであり、
**解説書の記述漏れの疑いとして残る**:

- YAML ファイル名とテストメソッド名の対応が YAML 節に無い（Excel は `notation.rst:69`・`:73` で推奨と書く）
- 可変長ファイルの `fields[].length` の要否が YAML 節に無い（`notation.rst:1135`）
- スキーマ検証違反時の挙動（例外型・メッセージ）が `notation.rst:92` に無い
- YAML の言語機能（アンカー・エイリアス・複数ドキュメント・ブロックスカラ）に解説書が一切触れていない
- `notation.rst:452` のカンマ・バックスラッシュのエスケープを YAML でどう書くかが特殊記法表に無い
- Excel の `[EMPTY]` マーカーカラムに相当する YAML の書き方が無い

### #41: Step 4 —— `nablarch-testing-converter` の突合と、変換ツールのページの是正 — 進行中

**担当ページ**: `tools/testdata_converter.rst`（`45c3852` で329行）。yaml の突合（`#40`）で
担当範囲から除外したのはこの1ページだけである。

**完了条件の母集合**（2026-08-26 ユーザー確定）: 「書き方（`implementation/testdata_notation.rst`）と
記載例（`implementation/testdata_examples.rst`）に載っている状態が、変換後も同じ意味で読めること」。
母集合は notation の特殊記法の表2つ（Excel 形式13行・YAML 形式13行）と、examples の
「null・空文字・改行など特殊な値を記述する」の節。「同じ意味」は**テスティングフレームワークが
解釈したあとの値が一致すること**を指す。セルの見た目ではない。

**突合の規模**（実測）:

| | 件数 |
|---|---|
| 担当ページ | 1ファイル・329行 |
| テストで検証できる粒度に分解した項目 | **81件**（`可` 65・`不可(静的)` 12・`不可` 4） |
| 既存テスト | **43ファイル・605メソッド**（`@Ignore` 2件） |

分解はサブエージェントに全量読ませ、拾わなかった行範囲と理由を1行ずつ書かせて行数の検算を取った
（1〜331 に隙間・重複0）。既存テストの目録も別のサブエージェントに作らせた。
**目録の自己申告に誤りが1件あり、ディレクターが実測で訂正した**（テストファイル数を当初45と数えたが
実測43。`git ls-tree -r --name-only 60d9a2d src/test | grep -c '\.java$'`）。

**ディレクターが実測した往復の壊れ方**（読み取り専用のプローブ。converter `60d9a2d` ×
本体 `3c4bd2a`。どのリポジトリも変更していない）。テスティングフレームワークが解釈したあとの値を
往復の前後で比べたもの。

| 記法 | 原本 | XLS→XLS | XLS→YAML |
|---|---|---|---|
| `notation.rst:1360` `null`（DBに null） | Java null | Java null | **文字列 `null`** |
| `notation.rst:1363` `"null"`（文字列の null） | 文字列 `null` | **Java null** | 文字列 `null` |
| `notation.rst:1378` `"""`（ダブルクォート1文字） | `"` | **再読込で例外** | `"` |
| `notation.rst:1390` `\r`（CR） | CR | CR | **2文字の `\` ＋ `r`** |

加えて `testdata_examples.rst:2231` の記載例（可変長ファイルの全フィールド空文字レコード）は
往復でレコードごと消える（本体が読むレコードが原本3件・XLS→XLS 後2件・XLS→YAML→XLS 後2件）。

**原因は1つである。** 中間モデルが「テスティングフレームワークが解釈したあとの値」ではなく
「Excel 記法の生文字列」を持っている。Excel の読み込みは `QuotationTrimmer` だけを掛け
（`XlsFormatReader.java:526`・`:539`-`:545`）、`NullInterpreter`・`LineSeparatorInterpreter` を掛けない。
書き出しは Java null だけを `null` リテラルにする（`XlsFormatWriter.java:581`）。
**読みで外した記法を書きで戻さないため、写像が非対称になっている。**
Excel 形式に必要なインタープリタが3つであることは `setup/common.rst:77` が述べている。

**解説書側の是正2コミット**（レビュー役が直接コミット）:

- `7f194a7` —— 前提事項のうち実測と食い違っていた2件。(1) マーカーカラムだけに値がある
  エントリが往復で消えることを書き足した（`notation.rst:1500` の「空エントリの判定はマーカーカラムを
  除外する前に行われる」に対し、実測で本体3行・変換ツール2行）。(2) 行末の空セルの記述を
  「テーブルと `LIST_MAP` のカラム名の行」だけに絞った。「ファイルとメッセージではデータ行を
  含むすべての行について……往復すると消える」は誤りで、`XlsFormatReader.java:416`-`:431`（`:424` が該当行）が
  不足セルを `""` で埋め直すため往復後も保たれる（実測）
- `45c3852` —— クォート記法の例外の段落を前提事項から削除した。意味を持つ情報が壊れることの
  記述であり、同ページ `:22`「意味を変えずに往復できる」と両立しない。前提事項に残すと
  直すべきものを仕様として固定してしまう

**申し送りの未確認2件は決着した**（`01-現在地.md` §4 の (a)・(b)）:

- (a) マーカーカラムだけで構成した行 —— **欠陥ではあるが直せない。** 記法上どちらの形式でも
  全要素が空のエントリを表せないため。解説書 `:63` に明記した（`7f194a7`）
- (b) 行末の空セル —— **欠陥ではなかった。解説書側の記述が誤りだった**（`7f194a7`）

**既存の `@Ignore` 2件は、解説書に記述の無い「あるべき姿」を追っている**（`60d9a2d` 実測）:

- `YamlFormatReaderInvalidInputTest.java:740` `YML-14` —— 「反映されない値がある入力はエラーに
  なるべき（`testdata_notation.rst:891`）」。**`45c3852` の `:891` はパディングとバイナリの記述で、
  この主張は無い。** 超過値を黙って捨てる挙動は論点4 として **user 判断済み（現行どおりで仕様）**
- `YamlFormatReaderInvalidInputTest.java:1280` `XLS-40` —— 「カラム名の大小を保つあるべき姿」。
  解説書にテーブルのカラム名の大小についての記述は0件（`45c3852` 全走査）

いずれも `解説書に無い書き方は直さない・テストしない` に反するため、指示書で削除させる。

**依存の前提（2026-08-26 user 了承）**: **`nablarch-testing-yaml` の Step 4 が完了するまで、
converter の指示書を渡さない。** converter は yaml に依存し（`pom.xml:40`-`:44`。`1.0.0-SNAPSHOT`）、
yaml 指示書の 2-2（`isResourceExisting` の判定単位）は converter のテストを意図的に落とす。
`mvn -o clean test -Dtest=YamlTestCoreAdapterTest` の実測（2026-08-26 20:58）は
`Tests run: 18, Failures: 1` / `isResourceExisting_reflectsFileExistence:370`。
同時点で yaml は作業中（ピン `0db2221` → `e9bee93`、`src/main` 7ファイル・+187/-65。
18件のうち 2-1・2-2・2-3 が済み、2-4・2-5 とテスト追加13件が残る）。
`~/.m2` の yaml jar は 20:31 install の作業途中の版である。
**`nablarch-testing` は取り直し不要**（`~/.m2` の jar は PR ブランチ由来と `javap` で確認。
ピン `3c4bd2a` とブランチ先端 `44b9cc9` は `src/main` がバイト同一）。

**ディレクター自身の指示文の誤りを1件見つけて直した**（`f29a631`）。完了条件9 に
「`jacoco.exec` は `.gitignore` に無いので消すこと」と書いたが、converter では `.gitignore:3` にある。
`nablarch-testing-rest` についてのメモを、対象リポジトリで確かめずに持ち込んだものだった。
あわせて完了条件8 を `mvn clean test` に改めた（`target/classes` が jacoco 計装済みのまま残ると
`mvn test` は `Cannot process instrumented class` で失敗する。実測）。

**指示書**: `ntf-step4-05-nablarch-testing-converter.md`（`672fb4b` で作成、`f29a631` で更新）。
**確定した作業は15件（実装の是正4・テスト追加11）。未送付。**

実装の是正4件: Excel の読み書きの対称化／全フィールド空文字レコードの書き戻し／
中間モデルからの `[ ]` の除去／解説書に記述の無い「あるべき姿」を追う既存 `@Ignore` 2件の削除。

テスト追加11件はいずれも既存605メソッドが0件であることをディレクターが自分の grep で
裏を取った（`with～` 5種・結合セル・コメント・`excludeSheets` の YAML 側・`validate` の
サブディレクトリ・`to=yaml` での整形設定の無効化・変換経路からの検証の非呼び出し）。


### #42: 形式間の意味集合を揃える是正と、構造上の疑い A・B の調査（user 判断 2026-08-28）— 解説書は完了、モジュール是正は `#37` の指示書へ

**経緯**。`#41` の後、解説書3ページ（`notation.rst`・`testdata_converter.rst`・`testdata_examples.rst`）を全量読み、
`testdata_converter.rst:14`・`:22`（両形式は同じ意味を別の記法で表す）に反して形式ごとに規則が違う5点を見つけた。
判定の軸（user 確定）: **中間モデル＝NTF 仕様＝現行 Excel 実装の意味。「YAML で表せて Excel で表せない意味」は存在しない。
Excel に定めがあれば同じ規則、無ければエラー。**

**解説書の是正（3コミット）**。

- `6bfc058` — 5点を Excel 側へ揃えた。空エントリ（YAML は `{}` だけ）／末尾フィールドの `null` は形式によらず `""`／
  交互記述／FW ヘッダの名前は `reader.fwHeaderfields`（YAML の他キーはエラー）／YAML でダブルクォート除去は行わない
- `04b9405` — 2文字 `\r` は YAML ではエラー（`6bfc058` の「CR として解釈」は `setup/common.rst:77` と両立しなかった）
- `6ba3c83` — 交互記述を「エラー」から「警告して変換」に改めた（**`6bfc058` の文言を上書き**。user 判断: 意味は Excel と
  同じで、既存利用者の大量データの変換を止めない。0件テーブルのカラム名 `:736` と同じ扱い）。
  電文のレコードレイアウトは1つと明記（`notation.rst:1153`・`:1299`）

**構造上の疑い A・B の調査（user 指示。プローブ実測。本体 `3c4bd2a`・yaml `3ee39c9`・converter `d611bec`）**。
結果の全文は `~/work/cowork/nablarch/ntf-doc-renewal/01-現在地.md`「A・B の調査結果」、プローブは同 `probe/`。

- **A** converter の Excel 読みは本体と値処理の順序が逆（`TestCoreReaderAdapter:40` が interpreters 空で本体パーサを回し、
  `XlsFormatReader.readDataRows:429` で後から解釈）。仕様内の入力で意味が変わるのは末尾の `null` だけ（本体 `""`、converter null）。
  `#37` の4経路が捕まえなかったのは、母集合にファイル・電文の末尾 `null` が無く、正解値が本体でなく converter 自身の reader だったため。
  **是正方針（user 了解）**: converter が自分で解釈するのをやめ、本体パーサにインタープリタ列を渡して本体に解釈させる。値は器から取る
- **B** yaml はファイル・電文の値行で本体 `DataFileParser` を通していない。**通さない（user 判断）**: 構造は YAML が明示するので判定する
  ものが無い。足りないのは (1) 末尾 null → `""`（`trimTailCopy` を `addValue` 直前で呼ぶ）(2) 電文の `records:` 2つ以上はエラー
  （スキーマ `maxItems: 1`）(3) `fw_header:` のキー検査（`6bfc058` 済み）

**検証**: Docker フルビルド `build succeeded`、行頭 WARNING/ERROR 0件。`verify_mapping` OK（597行）・`verify_glossary` OK。
生成物 `testdata_notation.html` に「レコードレイアウトは1つ」2箇所、`testdata_converter.html` に「警告を出す」1箇所。

**モジュール側の追随**（`#37` の指示書で扱う）: yaml — 上記 B の (1)(2)、`isBlankRow`、2文字 `\r` のエラー。
converter — A の是正方針、交互記述の警告、YAML 読みの末尾 null・`records:` 2つ以上・2文字 `\r`。

### #43: yaml 第2回（#36〜#44）の独立検証（合格）と、検証で見つけた解説書の曖昧2点の是正 — 完了

**検証（ディレクター実測。yaml `3ee39c9..aac55ad`。CC の報告書 `.rn/ntf-yaml/report-step4-2.md` は根拠にしていない）**。

- `src/main` の差分5ファイル（+441/−92）を全量読み、指示書 2-1〜2-7 の範囲内であることを確認。2-3 の許可集合は本体
  `MessageParser.java:107`-`:110`（`3c4bd2a`）と同じキー・既定4つ・`makeArray`
- scratchpad の clone で `mvn -o clean test` → `Tests run: 318, Failures: 0, Errors: 0, Skipped: 0`・`@Ignore` 0件
- ミューテーション7件・すべて検知: 2-1 `trimTailCopy` 無効（F1・F4・F6・S2 の4件）／2-3 未知キー素通し（8件）／2-3 設定値無視（5件）／
  2-4 全値 `""` を落とす旧判定（12件）／2-5 検査無効（15件）／2-5 `fw_header` 経路だけ未検査（2件）／2-5 判定を過剰に（`\n` も拒否。4件）
- oracle（2-1 `YamlTrailingNullOracleTest` 8件・2-4 `YamlBlankEntryOracleTest` 10件）は本体 `BasicTestDataParser`＋`PoiXlsReader`
  で POI が組んだ `.xlsx` を読む（`BodyExcelOracle.java:71`-`:72`）
- converter `d611bec` を yaml `aac55ad` の jar で `mvn -o clean test` → `656 / Failures: 3, Errors: 1`。落ちる4件は報告書 §7.2 と同じ
  （`fillsMissingRecordFragmentValuesWithEmptyStringInsteadOfNull`・`readsUnquotedNullAsJavaNullInRecordFragmentPath`・
  `skipsRowWhoseValuesAreAllEmpty`・`keepsFwHeaderNamedRecordInSendSyncFromRealYaml`）。converter 第2回の指示書 2-4 で是正する

**解説書の是正（検証で見つけた曖昧2点。あるべき姿が自明なので判断は仰いでいない）**。

- `implementation/testdata_notation.rst:889` — 「後ろに値のあるフィールドがあれば null のまま保持される」の「値」に `""` を含むかが
  `:1502`（`""` は値）と読み合わせると曖昧だった。本体 `NablarchTestUtils.trimTail`（`3c4bd2a` の `:251`-`:263`）は末尾から
  null と `""` を連続して取り除くため `["x", null, ""]` は `x`,`""`,`""`。「空文字でも null でもないフィールドがあれば」に改めた
- `implementation/testdata_notation.rst:1502` — 「マーカーカラムだけに値があるエントリは…他のカラムがすべて空文字のエントリとして
  読み込まれる」が、YAML でキーを省略した場合に `:818`（省略は null を明示したのと同じ）と矛盾していた。値は通常どおり
  （Excel の空セルは `""`、YAML のキー省略は null）に改めた。**yaml 報告書 §8.1 の「本体と恒久的に食い違う仕様差」は、この矛盾を
  仕様差と読んだもの。入力が非等価（Excel の空セル＝`""`、YAML のキー省略＝null）なだけで、仕様差ではない**
- `tools/testdata_converter.rst:63` — `:1502` の旧文を引いていたので合わせた（マーカーカラムの値だけを除いたエントリとして残す）
- converter 第2回の指示書 2-2 の引用を新しい文言に差し替えた

**yaml 報告書 §8 の判断**（user 判断が要るのは §8.5 だけ）: §8.1 上記のとおり仕様差ではない。T5/L5 のテストは正しいが Javadoc の
「仕様差」の枠組みを `:818` に沿って改める（#45）。§8.2 converter 第2回の指示書 2-4 で是正（既定）。§8.3 上記 `:889` で是正済み。
§8.4 スキーマ description は SSoT の適用範囲（2026-08-25 user 確定）なので追随する（#45）。§8.5 出典方式は user 判断へ。

# State

(written by /rn:dn, read and reset to this placeholder by /rn:up. `Status` is `paused` while a
session is suspended — the signal /rn:up and /rn:dn search for — and resets to `not suspended` here,
so only a genuinely suspended session reads `paused`.)

- **Status**: paused
- **Date**: 2026-08-30
- **Last completed**: junit5・yaml・converter の3モジュールとも Step 4 完了。承認記録は yaml `886849c`・converter `a5f006c` に反映済み（`src/` 差分なし、実測）。図の形式を PlantUML に決定（user 2026-08-30）。見本5パターンを作って user が確認済み
- **Next**: **図の作業**（詳細は `~/work/cowork/nablarch/ntf-doc-renewal/01-現在地.md` §3「図の作業」）。`#32` との整合は user 判断で決着（2026-08-30: 利用者への説明に必要な図は作る、クラス図も含む。`design.md` の同節に上書きを明記済み）。(1) README に「図の作成方法」を足す。(2) 現行画像27件を仕分け、パターン①〜⑤から図を作って RST に入れる。(3) `#48` を起こし、4観点レビューを回す。レビュー役が直接コミットする
- **Notes**: ブランチ `ntf-yaml-support`、作業ツリーはクリーン。**変更したら push する**。`TODO(NTF-*)` は0件。解説書ピン `a6da1f6`。`main` へのマージと `.rn/` の扱いは user の明示指示待ち。**英語版 `en/` は別PR**
