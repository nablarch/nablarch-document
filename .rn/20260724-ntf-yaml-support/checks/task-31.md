# #31 Completion Check

対象コミット: 一次成果物 `69334be`、是正ラウンド（本ラウンド）は `.rn/` のみの変更。ブランチ `ntf-yaml-support`、開始コミット `65a1756`。

実行日: 2026-08-20。実行環境: Docker イメージ `nablarch-document-build`。

`file:line` は特記のない限り現在の作業ツリー（是正ラウンド適用後）を指す。`.rn/` 内の文書どうしの参照は節見出しで指す。

**節の並びと H1 が `checks/task-29.md`・`checks/task-30.md` と異なるのは意図したものである。** 「判定の内訳（3事象）」は `checks/task-last.md` §8 と `checks/task-28.md` §7-3 のポインタ先であるため、追加節を Overall Verdict の後ろに置く両ファイルの並びに従わず、読み手が最初に行き着く位置へ出した。H1 の `# #31 Completion Check` は `checks/task-05.md:1` の `# #5 Completion Check` の型に倣った。

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `grep -rn 'NTF-MOD-01-1' ja/` が0件である（依頼書 `ntf-doc-28-decide-disposition.md` 側の記述は残してよい） | OK | `$ grep -rn 'NTF-MOD-01-1' ja/ \| wc -l` → `0`。削除したのは `tools/testdata_converter.rst` の TODO 3行＋直後の空行1行で、`git diff -U0 65a1756..HEAD -- ja/` の第1ハンク `@@ -22,4 +21,0 @@` が `.. TODO(NTF-MOD-01-1): テストデータ変換ツールの往復非可逆。判定待ち。` 以下4行の削除であることを示す | | |
| `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-SRC-02` のみ2箇所）である | OK | `$ grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` → `NTF-FIG-01`〜`04`・`NTF-MOD-01-2`・`NTF-MOD-01-3`・`NTF-MOD-02-2`〜`04`・`NTF-MOD-03-1`・`NTF-SRC-01` が各1件、`NTF-SRC-02` が2件。合計13件・12ID。開始時（`65a1756`）は14件・13ID で、差は `NTF-MOD-01-1` の1件・1ID のみ。`$ grep -rl 'TODO(NTF-' ja/ \| wc -l` → `10`（`testdata_converter.rst` に `NTF-MOD-01-2`・`NTF-MOD-01-3` が残るためファイル数は増減なし） | | |
| `tools/testdata_converter.rst` の tip 本文と「意味を変えずに往復できる」見出しの間の空行が1行である | OK | `$ sed -n '20,23p' ja/development_tools/testing_framework/tools/testdata_converter.rst \| cat -A` → `:20` が tip 本文（`  YAML\ 形式へ書き出す値は、…`）、`:21` が `$` のみ（空行1行）、`:22` が見出し `意味を変えずに往復できる`、`:23` が `~` 下線 | | |
| 同ファイルの「意図のある情報」の行が「無損失で保持する。マーカーカラム、空欄のレコード種別が該当する」である | OK | `$ grep -n '無損失で保持する' ja/development_tools/testing_framework/tools/testdata_converter.rst` → ヒットは `:37` の1件のみ。逐語は `    - 無損失で保持する。マーカーカラム、空欄のレコード種別が該当する` | | |
| 上記2点以外に `ja/` の差分が無い。**本文を1文字も変えていない**ことを、`git diff --numstat <開始コミット>..HEAD -- ja/` が `1	5`（追加1・削除5）であることで測る。削除5の内訳は TODO 3行＋直後の空行1行＋「意図のある情報」1行の置換分であり、置換の削除1行は追加1行と対になる | OK | `$ git diff --numstat 65a1756..HEAD -- ja/` → `1	5	ja/development_tools/testing_framework/tools/testdata_converter.rst` の1ファイルのみで、criterion の指定値 `1	5` と一致する。`git diff -U0 65a1756..HEAD -- ja/` のハンクは `@@ -22,4 +21,0 @@`（TODO 3行＋直後の空行1行の削除）と `@@ -41 +37 @@`（1行置換。削除行の逐語 `    - 無損失で保持する。マーカーカラム、データブロックの内側にある空エントリ、空欄のレコード種別が該当する` と追加行の逐語の差は「データブロックの内側にある空エントリ、」19文字（読点を含む）の除去だけ）の2つだけで、削除5の内訳は criterion の記述どおりである。それ以外の本文は1文字も変わっていない | | |
| `checks/task-last.md` §8 の台帳が13行・12ID で、削除した行が持っていた出典（依頼書 `ntf-mod-01-nablarch-testing-converter.md` §2・`checks/task-28.md` §7-3・`ntf-doc-28-decide-disposition.md` §7-2）が削除記録の段落に引き継がれている | OK | `$ awk '/^## 8\./,/^\*\*実測\*\*/' .rn/20260724-ntf-yaml-support/checks/task-last.md \| grep -c '^\| \`NTF-'` → `13`（`NTF-SRC-02` が2行のため12ID）。`NTF-MOD-01-1` の削除記録の段落は3出典すべて（`ntf-mod-01-nablarch-testing-converter.md` §2、`checks/task-28.md` §7-3、あるべき姿の `ntf-doc-28-decide-disposition.md` §7-2 の表）を持ち、判定の但し書きと確定日・「内容」と「仕様上の意味」の水準の違い・表の1行を仕様に合わせて書き直したこと・詳細の置き場所（本ファイル「判定の内訳（3事象）」）を続けている。`checks/task-28.md` §7-3 の節は現在も存在し、同じ `#31` で外したのはその表の `NTF-MOD-01-1` の行だけであるため、行の現物を `git show 65a1756:.rn/20260724-ntf-yaml-support/checks/task-28.md` の `:452` で辿れる旨を添えた。段落の長さは「Method（作りながら検証した記録）」の「段落の長さの基準」の行で測った | | |
| `checks/task-28.md` §7-3 の表から `NTF-MOD-01-1` が外れている（`#29` が `NTF-MOD-02-1` で確立した運用。同 `:461`） | OK | `checks/task-28.md` §7-3「入れた TODO の一覧」の表は5行になり、`NTF-MOD-01-1` の行は無い（`$ awk 'NR>=448 && NR<=460' … \| grep -c '^\| \`NTF-'` → `5`）。criterion が指す `:461` の段落は、行削除で `:460` へ繰り上がった同じ段落である。件数を「現在6行」から「現在5行」へ直し、`NTF-MOD-01-1` を外した理由と `#31` への参照を `NTF-MOD-02-1` と同じ調子で書き足した（依頼書のファイル名 `ntf-mod-01-nablarch-testing-converter.md` は `a9f915f` で補い、本ラウンドでは §2 の指し方を `§2（事象1: XLS → YAML → XLS → YAML の往復で内容が変わる）に記録した3事象 (a)(b)(c)` に改めた。同じ表が §番号と事象番号を1対1に対応させているため、旧文言「§2 の3事象」は「§2 に事象が3つある」と読めた）。あわせて同節 `:509` の「現在の 7-3 の表（6行）とは `NTF-MOD-02-1` の1件だけずれる」を「（5行）とはこの2件ずれる」へ直した。`7c38797` で表を5行にしたことで生じた `#31` 自身の不整合であり、`steering.md` の `#31` Step 3「それ以外の記録整備は行わない」の対象外と判断した | | |
| 台帳と `checks/task-28.md` §7-3 が指す `checks/task-31.md` が、`#31` の check-off コミットでブランチに入る | 判定できない（本ラウンド時点では未達成） | 本ファイルは `git status --short` で `?? .rn/20260724-ntf-yaml-support/checks/task-31.md` のまま、すなわち**未追跡**である（本ラウンドで実行して確認）。rn の運用上、check ファイルは実装担当が書き、調整役が check-off コミットで staging するため（`task-execute-workflow.md`「Check file format」）、実装担当である私はこのファイルをコミットしない。したがって本 criterion の達成可否は本ラウンドの時点では判定できず、調整役の check-off コミットで初めて満たされる | | |
| Docker フルビルドが WARNING・ERROR ともに0件（ゲート7） | OK | 本ラウンドは `.rn/` のみの変更で `ja/` を一切変更していないため再実行不要（`$ git diff 69334be..HEAD -- ja/` → 出力0行）。`69334be` 時点で実行済み: `docker run --rm -v …:/root/document nablarch-document-build /bin/bash -c "cd /root/document; rm -rf _build; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` が exit 0・`build succeeded.`。`grep -ci warning <log>` → `0`。`grep -ciE '\berror\b' <log>` → `1` だが、内訳は `copying images... [ 43%] application_framework/application_framework/libraries/images/tag/error.png` の**ファイル名**のみでエラー出力は0件（`checks/task-last.md` §2 と同じ判定）。ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` で復元済み | | |
| `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS | OK | いずれも `.rn/20260724-ntf-yaml-support` を起点に本ラウンドで再実行。`python3 mapping/tools/verify_glossary.py` → exit 0・`RESULT: OK`。`python3 mapping/tools/verify_mapping.py` → exit 0・`OK: no errors`（`[第2部 導入と設定 > 取引単体テストの設定（RESTfulウェブサービス） > 機能概要]: 0 row(s) (optional since #6, not an error)` は既知の非エラー）。`python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 0.84s` | | |
| 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | 本ラウンドで変更したのは `.rn/20260724-ntf-yaml-support/checks/task-last.md`・同 `checks/task-28.md`・同 `checks/task-31.md`（未コミット）の3ファイルのみ。`69334be` を含めた通算でも `git diff --name-only 65a1756..HEAD` は `checks/task-last.md`・`checks/task-28.md`・`ja/development_tools/testing_framework/tools/testdata_converter.rst` の3件で、`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/` 配下・`.gitignore` はいずれも含まれない。`git status --short` の残りは `.rn/20260724-ntf-yaml-support/steering.md`（調整役の変更。本タスクでは触れていない）と本ファイルだけである | | |

## 判定の内訳（3事象）

**本節が3事象の詳細の唯一の置き場所である。** `checks/task-last.md` §8 の削除記録の段落は、台帳として要る分だけ（3事象の出典、判定が本作業ディレクトリからは裏を取れないことの但し書きと確定日、「あるべき姿と食い違わない」と言える理由の要旨、表の1行を仕様に合わせて書き直したこと）を持ち、事象ごとの内訳は本節を指している。`checks/task-28.md` §7-3 は、台帳の段落と本節へのポインタだけを持つ。

3事象 (a)(b)(c) の観測記録は、依頼書 `ntf-mod-01-nablarch-testing-converter.md` §2「事象1: XLS → YAML → XLS → YAML の往復で内容が変わる」にある（`:53` が `**(a) 全カラムの値が空文字の行が、行ごと消える**`、`:73` が `**(b) 空の行（\`- {}\`）が増える**`、`:77` が `**(c) 行が0件のテーブルが、直後のテーブルを取り込む**`。いずれも自分で開いて逐語を確認した）。

| 事象 | 依頼書 §2 の観測 | 返ってきた判定 | 帰結 |
|---|---|---|---|
| (a) | 全カラムの値が空文字の行が、行ごと消える（`confirmOfCreateAbNormal.yaml` の `requestParams` が `rows: []` になる。同種の変化が6ファイル） | `nablarch-testing-converter` の課題 `XLS-05` として**対応不要**（記法が明文で定めている挙動） | 本文の書き直し不要。あるべき姿「往復しても内容が保たれる」（`ntf-doc-28-decide-disposition.md` §7-2 の表）と食い違わない |
| (b) | 空の行（`- {}`）が増える（削除5行・追加84行） | (a) と同じ明文（空エントリの読み飛ばし）による挙動である。**課題番号への帰属は user 指示に示されていない**（根拠は「Method（作りながら検証した記録）」の該当行） | 本文の書き直し不要。ただし「意味を変えずに往復できる」節の `list-table` が空エントリを「意図のある情報」の行に挙げていたのは誤りだったため、その1行だけを仕様に合わせて書き直した（根拠は「Method（作りながら検証した記録）」の該当行） |
| (c) | 行が0件のテーブルが、直後のテーブルを取り込む（`setUpDb.yaml` の `setup_tables`） | 課題 `XLS-27` として**要対応**と判定され修正済み | 本文の書き直し不要。修正後も残る制約（0件テーブルを含む YAML は Excel へ変換できない）は既存の `NTF-MOD-01-3` が保持しており、`checks/task-last.md` §8 の同 ID の行に解除条件まで書いてある |

**「内容」の水準と「仕様上の意味」の水準を分けている。** `ntf-doc-28-decide-disposition.md` §7-2 の表が `NTF-MOD-01-1` の「前提とするあるべき姿」列に置いた逐語は「往復しても内容が保たれる」である。一方、(a) は `rows:` の行が `rows: []` になる変化、(b) は `- {}` が削除5行・追加84行という変化であり、**逐語の「内容」は保たれていない**。それでも食い違わないと言えるのは、`ja/development_tools/testing_framework/tools/testdata_converter.rst:24` が「ある形式から中間モデルを経て同じ形式へ往復したとき、テスティングフレームワークの仕様上の意味は変わらない。」と述べている**仕様上の意味**の水準においてである。(a)(b) が増減させているのは、`ja/development_tools/testing_framework/implementation/testdata_notation.rst:1534` の明文が「読み飛ばされる」と定めているエントリの表記だけであり、テスティングフレームワークが読み取る内容は変わらない。上の表の「帰結」列の「あるべき姿と食い違わない」は、この水準での判断である。

**表の1行を仕様に合わせて書き直したことと、注意書きを書いていないこと。** `ntf-doc-28-decide-disposition.md` §7 のリードは「各箇所について「あるべき姿」を §7-2 の表で明示した。判定が「仕様」で返った場合は、そのとき本文を仕様に合わせて書き直す。TODO はそのための目印である。」と指定している。(a)(b) は「記法が明文で定めている挙動」すなわち仕様と確定したため、その明文（下記）と矛盾していた「意図のある情報」の1行を仕様に合わせて書き直したのは、この指定どおりの処置である。一方、同 §7-2 の表が `NTF-MOD-01-1` の「本文の書き方」列に指定している「非可逆の注意書きを書かない」に従い、追加の注意書きは書いていない（`git diff -U0 65a1756..HEAD -- ja/` の追加行は「意図のある情報」の1行だけで、追加のブロックもディレクティブも無い）。

**判定そのものの出典について。** `XLS-05`「対応不要」・`XLS-27`「要対応」という判定は、`nablarch-testing-converter` 側の記録にある。同リポジトリは本作業ディレクトリの外にあり、user の明示指示により参照していないため、**本作業ディレクトリからは裏が取れない**。判定は user が作業指示に示した文面をそのまま前提として扱った（2026-08-20、user 確定）。`checks/task-last.md` §8 の削除記録の段落にも、同表の `NTF-MOD-01-2`・`NTF-MOD-01-3` の行と同じ水準の但し書きを付けてある。

**(b) の記法上の裏づけは本リポジトリ内で取れる。** `ja/development_tools/testing_framework/implementation/testdata_notation.rst:1534` が「全要素が\ null\ または空文字のエントリは読み飛ばされる。Excel\ では行の全セルが空の場合、YAML\ では ``rows:``\ 内の要素が空マッピング（\ ``{}``\ ）またはすべての値が空文字の場合にスキップされる。」と明文で定めている。

**`reviews/page-testdata_converter.md` は3事象の出典にならない。** 同ファイルの「判断待ち（`decide`）」1 にあるのは (a) 相当と (b) の2事象だけで、(c) は同ファイル全体に存在しない（`$ grep -n '0件テーブル\|取り込\|直後のブロック\|全カラム' .rn/20260724-ntf-yaml-support/reviews/page-testdata_converter.md` → 0件。自分で実行して確認した）。

## 申し送り

いずれも本文は変更していない。

**1. 「意味を持たない情報」の行に残る「外側」という限定。** `#32` の手順1で処置する。

**2. `reviews/` の craft 対応表が挙げる根拠と、今回の是正の結論が逆を向いている。**

`.rn/20260724-ntf-yaml-support/reviews/page-testdata_converter.md` §「4観点レビュー」の「是正した指摘」表は、「空エントリ」と「完全な空行」を「データブロックの内側にある空エントリ」「データブロックの外側にある空行」に書き分けている。その根拠として同表が挙げているのは `model/ListMapBlock.java:12`「空マッピング由来の空行も空リストとして保持」であり、同ファイル §「実装で確認した事実」の表にも同趣旨の行（「空マッピング由来の空行はデータブロック内で保持される | `model/ListMapBlock.java:12, 25`」）がある。今回の是正はこれと逆の結論を採った。`model/ListMapBlock.java` は本作業ディレクトリの外にあり**未確認**であるため、旧根拠が明示的に覆るのか、記法の別の側面（中間モデルの内部表現と、読み込み時のスキップ判定の別）を指していたのかは**判定していない**。マージ直前の一括処置で `reviews/` を見直す際の対象。

**3. 表に残した「マーカーカラム」「空欄のレコード種別」の検証。** `#32` の手順1で処置する。

**4. コミット済みの `locales/ja/LC_MESSAGES/sphinx.mo` が、`.po` からの再生成物と一致していない。**

コミット済みの `locales/ja/LC_MESSAGES/sphinx.mo` は、同じディレクトリの `sphinx.po` から Sphinx 自身のコード経路で作り直したものと2バイト分だけ食い違う（実測値・コード経路・`file:line` は「Method（作りながら検証した記録）」の該当行）。この作り直しが無条件に走るのは `sphinx-build` に `-a` を付けたときだけであり、作業ツリーの `.mo` が書き換わって `git status` が `M` になるのも `-a` 付きのビルドに限られる（`-a` の無い `#31` のゲート7 のコマンドでは、`.mo` の mtime が `.po` より新しい限り作り直されない。現在の作業ツリーはこの状態にある）。**`69334be` 時点のフルビルドで実際に `M` になったかは、当時の mtime が残っていないため未確認である。**処置は `.mo` をコミット済みから外すか再生成物で更新するかの判断を伴うため、**マージ直前の一括処置の候補**として user 判断を仰ぐ。

## Method（作りながら検証した記録）

書いた主張はすべて本リポジトリの実ファイル、または自分で実行したコマンドの出力で裏付けた。突き合わせの内訳は次のとおりである。

| 主張 | 突き合わせた出典 |
|---|---|
| 削除した TODO 4行の逐語 | 編集前の `tools/testdata_converter.rst:22-25`（`65a1756`）を `sed -n` で表示して一致を確認したうえで、Python の完全一致置換（`assert s.count(old)==1`）で削除した。推測で行番号を指定した削除はしていない |
| 「意図のある情報」行の変更前後の逐語 | 同じく編集前 `:41` を表示して一致を確認し、完全一致置換で1行だけ差し替えた（`assert s.count(old2)==1`）。是正後の逐語は `git diff -U0 65a1756..HEAD -- ja/` の第2ハンクで再確認した |
| 3事象 (a)(b)(c) の観測記録の所在 | `.rn/20260724-ntf-yaml-support/ntf-mod-01-nablarch-testing-converter.md` §2 を開き、`:53`・`:73`・`:77` の見出し3本と、それぞれに付く YAML 断片・件数（6ファイル、`- {}` 削除5行・追加84行）を読んだ。同ファイルの節構成（§2 が事象1）は `grep -n '^## '` で確認した |
| `reviews/page-testdata_converter.md` に (c) が無いこと | `grep -n '0件テーブル\|取り込\|直後のブロック\|全カラム' …` が0件であることを自分で実行して確認した。前ラウンドの記録が同ファイルを3事象の出典として挙げていたのは誤りで、本ラウンドで是正した |
| 削除した台帳行が持っていた出典3つ | `git show 65a1756:.rn/20260724-ntf-yaml-support/checks/task-last.md \| grep -n 'NTF-MOD-01-1'` で `:417` の行の現物を表示し、「依頼書または根拠の節」列の `ntf-mod-01-nablarch-testing-converter.md` §2 と `checks/task-28.md` §7-3、「前提としたあるべき姿」列の `ntf-doc-28-decide-disposition.md` §7-2 の表を写した |
| 但し書きの書式 | `checks/task-last.md` §8 の `NTF-MOD-01-2`・`NTF-MOD-01-3` の行を実際に読み、「**確定（user 引用による。…本作業ディレクトリからは参照できないため…）**」の形をそろえた |
| 段落の長さの基準 | 同 §8 の `NTF-MOD-02-1` の削除記録の段落を読み、括弧の内側の句点を除いて分割すると **2文156字・最長101字** であることを自分で測った。`NTF-MOD-01-1` の削除記録の段落は出典が3つあり同じ2文には収まらないため、文の数ではなく1文の長さをそろえる方針とし、本ラウンドの結果は **9文954字・最長162字** である。最長の1文は `NTF-MOD-01-2`・`NTF-MOD-01-3` と同型の但し書きで、162字のうち147字が丸括弧の内側である |
| 空エントリが中間モデルに保持されないこと | `ja/development_tools/testing_framework/implementation/testdata_notation.rst:1534` を実際に開いて逐語を確認した。**読み飛ばしを本体（`nablarch-testing`）のどのクラスが実行するかは、当該リポジトリが本作業ディレクトリの外にあるため未確認**で、user 指示に記された前提として扱った |
| `XLS-05`・`XLS-27` の判定 | user が作業指示に示した文面による（2026-08-20、user 確定）。その旨を `checks/task-last.md` §8 と本ファイル「判定の内訳（3事象）」の両方に明記した |
| TODO の件数・ID 数・ファイル数 | `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` と `grep -rl 'TODO(NTF-' ja/ \| wc -l` を本ラウンドで実行し直し、`checks/task-last.md` §8 の表の行数（13行・12ID）と突き合わせた |
| `checks/task-28.md` §7-3 の表の行数 | 行削除後に `awk 'NR>=448 && NR<=460' … \| grep -c '^\| \`NTF-'` → `5`。段落の「現在6行」を「現在5行」へ直した根拠である |
| 検証スクリプトの結果 | 3本とも `.rn/20260724-ntf-yaml-support` を起点に本ラウンドで実行し、exit code と出力末尾を確認した |
| (b) に課題番号を帰属させた出典が無いこと | `steering.md` の `#31`「根拠」節を開き、逐語が「(b) `- {}` が増減する → 同じ明文による。」までで、課題番号も判定行為も書かれていないことを確認した。あわせて `grep -rn 'XLS-05' .rn/20260724-ntf-yaml-support/` で (b) を `XLS-05` に結び付けた記録が他に無いことを確かめ、前ラウンドが書いていた「同じく `XLS-05` として対応不要」を取り消した |
| 「中間モデルでの扱い」が表題ではなく第2列の見出しであること | `ja/development_tools/testing_framework/tools/testdata_converter.rst:26-37` を開いた。`.. list-table::` に `:header-rows: 1` はあるが表題（`.. list-table:: <タイトル>`）は無く、`:30` `  * - 区分`／`:31` `    - 中間モデルでの扱い` がヘッダ行の2セルである |
| 「内容」と「仕様上の意味」の水準の違い | あるべき姿の逐語「往復しても内容が保たれる」を `ntf-doc-28-decide-disposition.md` §7-2 の表で、仕様上の意味の逐語を `tools/testdata_converter.rst:24`「…テスティングフレームワークの仕様上の意味は変わらない。」で、それぞれ現物を開いて確認した。(a)(b) が逐語の内容を変えていることは依頼書 §2 の `rows: []` の例と「削除された `- {}` が5行、追加された `- {}` が84行」で確認した |
| `#31` が本文に注意書きを追加していないこと | `git diff -U0 65a1756..HEAD -- ja/` の追加行が「意図のある情報」の1行だけであることを実行して確認した。指定「非可逆の注意書きを書かない」は `ntf-doc-28-decide-disposition.md` §7-2 の表の `NTF-MOD-01-1` の「本文の書き方」列で確認した |
| `reviews/page-testdata_converter.md` の該当箇所が属する節 | 同ファイルを `grep -n '^## \|^### '` で節構成を取り、`:116` が `## 4観点レビュー` > `### 是正した指摘` の表の行、`:70` が `## 実装で確認した事実` の表の行であることを確認したうえで、行番号による指し方をやめて節見出しで指す形に改めた |
| `locales/ja/LC_MESSAGES/sphinx.mo` が `.po` からの再生成物と一致しないこと | `$ git cat-file -s HEAD:locales/ja/LC_MESSAGES/sphinx.mo` → `23235`。リポジトリを読み取り専用でマウント（`-v "$PWD:/work:ro"`）した Docker イメージ `nablarch-document-build`（Sphinx 1.3.6・Babel 2.18.0。`import sphinx, babel` で取得）の中で、`sphinx/util/i18n.py:49-52` の `write_mo(mo, read_po(po, locale))` と同じ呼び出しにより `locales/ja/LC_MESSAGES/sphinx.po` からコンテナ内 `/tmp/y.mo` へ再生成すると `23237` バイトになり、`cmp` は `differ: byte 2189, line 11`・exit 1 を返した（リポジトリ内のファイルには書き込んでいない。**フルビルドは回していない**）。**未確認**: コンテナ内に `msgfmt` が無い（`command -v msgfmt` が空）ため GNU gettext との照合はしていない。2バイトの差の中身と、コミット済みの版を作ったツールの版も見ていない |
| その再生成が `sphinx-build -a` のときだけ無条件に走ること | 前ラウンドは `sphinx/locale/__init__.py:217` の `catinfo.write_mo(language)` という呼び出し行だけを見て「無条件に走る」と書いていたが、カタログの供給元を開いて誤りと分かったため本ラウンドで取り消した。`sphinx/util/i18n.py:117-118` が `if force_all or cat.is_outdated():` / `catalogs.add(cat)` で絞っており、`is_outdated()`（同 `:44-47`。本体は `not path.exists(self.mo_path) or path.getmtime(self.mo_path) < path.getmtime(self.po_path)`）が False のカタログは `locale/__init__.py:215-217` の `for catinfo in find_catalog_source_files(...)` にも `builders/__init__.py:198-205` の `compile_update_catalogs()` にも渡らない。`force_all=True` を渡すのは `builders/__init__.py:172-180` の `compile_all_catalogs()` だけで、そこへ入るのは `application.py:257-262` の `def build(self, force_all=False, filenames=None):` / `if force_all:` の分岐であり、`force_all` は `cmdline.py:69-71` の `group.add_option('-a', action='store_true', dest='force_all', …)` と同 `:244` の `app.build(opts.force_all, filenames)` により `sphinx-build -a` のときだけ True になる。`#31` のゲート7 のコマンド（本ファイル Completion Criteria 表のゲート7 の行）に `-a` は無い。現在の作業ツリーを同じコンテナから評価すると `CatalogInfo("locales/ja/LC_MESSAGES", "sphinx", "utf-8").is_outdated()` は `False`、`find_catalog_source_files(["locales"], "ja", domains=["sphinx"], charset="utf-8")` は0件、`force_all=True` を付けると1件であった。この経路が当該ファイルを指すことは `ja/conf.py:67` の `language = 'ja'`・同 `:68` の `locale_dirs = ['../locales']` と `application.py:199-200` が `locale_dirs = [None, path.join(package_dir, 'locale')] + [path.join(self.srcdir, x) for x in self.config.locale_dirs]` として `locale_dirs` を組み立てていることによる |
| `checks/task-28.md` §7-3 の `:509` の段落が言う表の行数とずれの件数 | `:450`〜`:459` の表のデータ行のうち ID セルが `NTF-` で始まる行を `awk` と `grep -c` で数えて **5** を得た。同節 `:509` の段落が言う「現在の 7-3 の表（6行）とは `NTF-MOD-02-1` の1件だけずれる」は `7c38797` 以降は誤りになるため、「（5行）とはこの2件ずれる」へ直した。`#31` 自身が生んだ不整合であるため、`steering.md` の `#31` Step 3「それ以外の記録整備は行わない」の対象外と判断した |
| `checks/task-28.md` §7-3 の箇条書き「置いた位置の判断」を直さない判断 | `sed -n '466p;468p' .rn/20260724-ntf-yaml-support/checks/task-28.md` で `- `01-1` — …` と `- `02-1` — …` の両方が残っていることを確認した。`02-1` は `#29` で表から外したあとも項が残っており、当該箇所を `#28` 時点の履歴として扱う運用が既に確立している。`01-1` も同じ扱いとした |
| 現在の Completion criteria の件数と文言 | `steering.md` の `#31` Completion criteria を開き、criterion 5 が `git diff --numstat <開始コミット>..HEAD -- ja/` が `1	5` であることで測る形に直っていること、`checks/task-31.md` の check-off コミットに関する criterion が1件増えて全11件になっていることを確認し、本ファイルの表を11行に合わせた |
| フルビルドを再実行しなかったこと | `git diff 69334be..HEAD -- ja/` が0行であること（`ja/` に本ラウンドの差分が無いこと）を確認したうえで、`69334be` の結果を援用した |
| `checks/task-28.md` §7-3 の節が現在も存在すること | `grep -n '^### 7-3' .rn/20260724-ntf-yaml-support/checks/task-28.md` → `448:### 7-3. 入れた TODO の一覧` の1件。前ラウンドの台帳が書いていた「§7-3 は…現在の版には無く」は誤りで、無くなったのは同節の表の `NTF-MOD-01-1` の行だけである。本ラウンドで台帳の当該文を主語ごと書き直した |
| 表の1行を書き直したことが指示書の指定に沿うこと | `ntf-doc-28-decide-disposition.md` §7 のリードを開き、逐語「各箇所について「あるべき姿」を §7-2 の表で明示した。判定が「仕様」で返った場合は、そのとき本文を仕様に合わせて書き直す。TODO はそのための目印である。」を確認した。あわせて同 §7-2 の表の `NTF-MOD-01-1` の行が「本文の書き方」列に `非可逆の注意書きを書かない` と指定していることも現物で確認し、「別件として是正した」という前ラウンドの切り分けを、この指定への対応として書き直した |
| 本案件の「4観点」の顔ぶれ | `steering.md:58` の `レビューは4観点を**それぞれ別のサブエージェント**で回す（QA / 設計 / クラフト / 検証）` と `checks/task-24.md:937` の `4観点をそれぞれ独立のサブエージェントで実施（QA / 設計 / クラフト / 検証）。` を確認した。「一次実装」は観点ではないため、前ラウンドの申し送り1 が書いていた検出者の内訳を取り消した。**`#31` のどの観点がこの点を挙げたかを示す記録は本作業ディレクトリ内に無く、未確認である** |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK（`a9f915f` 時点） | 完了条件11件を1件ずつ独立に実測して確認。`fe0c775` は `.rn/` の記録2行だけの変更で `ja/` の差分は0行（`git diff a9f915f..HEAD -- ja/` が0行。調整役が実行して確認）だが、事実記述に触れているため**本観点は `fe0c775` では再実施していない**。是正ラウンド上限に達したための未実施であり、未確認である |

## Expert Reviews (axes the task needs)

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | 判定なし | 本観点は一度実施したが、調整役が作業指示書にスコープ制約（`nablarch-testing-converter` / `nablarch-testing` / `nablarch-testing-yaml` を読みに行かないこと）を書き落としたため、担当が当該3リポジトリを参照した。user の明示指示に反する前提で出た判定であるため**採用しない**。調整役の指示書作成の誤りであり、担当の誤りではない |
| System-wide integrity (interfaces, cross-doc consistency) | 判定なし | 同上 |

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | NG | 「詳細な根拠の置き場所は1箇所」ルールの違反が残る。下記「未解決の指摘（是正ラウンド上限後）」の1〜5 |
| Consistency with existing style | NG | 記録どうしの自己記述と実物の食い違いが残る。同 3・6 |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked (claims verified) | OK | 逐語・行番号のずれは1件も検出されなかった。Sphinx の `.mo` 再生成のコード経路の8か所の `file:line`、`.mo` の実測値（23235 / 23237 バイト、`cmp differ: byte 2189, line 11`、`msgfmt` 不在）、文字数・文数（`:431` 2文156字・最長101字／`:433` 9文954字・最長162字・うち括弧147字）を、担当が読み取り専用マウントの Docker と自前のスプリッタで独立に再現した |
| Coverage (claims) | OK（指摘4件あり） | 検証スクリプト3本を独立に再実行（`verify_glossary.py` → `RESULT: OK`、`verify_mapping.py` → `OK: no errors`、`pytest mapping/tools -q` → `183 passed, 96 subtests passed`）。TODO 13件・12ID・10ファイル、`git diff --numstat 65a1756..HEAD -- ja/` → `1	5`、`grep -rn 'NTF-MOD-01-1' ja/` → 0件も再現。スコープ制約の遵守も確認された。指摘は下記 6〜9（いずれも記録の精度で、成果物本体の事実誤りではない） |

## Overall Verdict

- Self-check: OK（criterion 11件のうち10件は本ラウンドで実測して満たしている。`checks/task-31.md` を check-off コミットでブランチに入れる1件は、実装担当がコミットしない運用のため本ラウンドの時点では判定できない）
- QA: OK（`a9f915f` 時点。`fe0c775` では未実施）
- Design expert: 判定なし（スコープ制約を欠いた指示書で回したため採用しない）
- Craft expert: NG（未解決の指摘 1〜5）
- Verification expert: OK（指摘4件は記録の精度。未解決の指摘 6〜9）
- Ready to check off: Yes（user 裁定 2026-08-21。未解決9件は表の下のとおり処置済み・送付済み・処置不要に分かれ、`ja/` 本文への手当ては `#32` の手順1で行う）

## 未解決の指摘（是正ラウンド上限後）

`fe0c775` は rn の是正ラウンド上限（3回）にあたる。以下は上限到達後に残った有効な指摘である。**いずれも `.rn/` 配下の記録の記述に関するもので、成果物 `ja/development_tools/testing_framework/tools/testdata_converter.rst` に対する指摘は1件も無い。**

| # | 出た観点 | 場所 | 指摘 | 調整役が実測で裏を取ったか |
|---|---|---|---|---|
| 1 | クラフト | `checks/task-last.md:433` | 954字のまま（比較基準の `:431` `NTF-MOD-02-1` は156字）。事象別内訳を削った分を「内容／仕様上の意味」の説明の拡張で埋め戻しており、本ファイル「判定の内訳（3事象）」との重複が残る。「詳細な根拠の置き場所は1箇所」ルールに反する | 取った（`:433` 9文954字・`:431` 2文156字。推移は `7c38797` 526字 → `a9f915f` 960字 → `fe0c775` 954字） |
| 2 | クラフト | `checks/task-28.md:460` | 「重複を正す」と題した `fe0c775` で逆に伸びた。`:433` と連続87字が逐語一致し、その87字は `fe0c775` が追加した部分である。本ファイル `:29` の「§7-3 はポインタ**だけ**を持つ」という自己記述とも食い違う | 取った（`a9f915f` 470字 → `fe0c775` 525字。`difflib` で連続87字の一致を確認） |
| 3 | クラフト | 本ファイル「判定の内訳（3事象）」 | 「`checks/task-last.md` §8 の削除記録の段落にも、同じ趣旨を**1文で**書いてある」と述べるが、実物は2文198字である | 未確認（クラフト観点の測定値による） |
| 4 | クラフト | `checks/task-last.md:433` | 「行の現物は … で辿れる」の指す先が定まらない。直前2文が別ファイルの別の行を主語にしている | 取った（当該段落を読んで確認） |
| 5 | クラフト | `checks/task-last.md` §8 | `#31` が生んだ未決点（`tools/testdata_converter.rst:39` の「外側」の限定、未検証のまま残置した2語）が、マージ後も残る場所に記録されていない。台帳 §8 は「何が未決か」を引く場所だが、そこからは `NTF-MOD-01-1` が解決済みとしか読めない | 取った（`grep -c '外側'` → `checks/task-last.md` 0件、`steering.md` 1件のみ。`steering.md` はマージ後に流れる） |
| 6 | クラフト・検証（両方が独立に検出） | 本ファイル「申し送り」1 | 「複数の観点が独立に検出した」が、直後の但し書き「検出者の内訳は未確認である」および「Method」表の最終行と矛盾する。検出者の記録が無いなら「複数」「独立に」も裏付けられない | 取った（`grep -rn '外側' .rn/…/ --include=*.md` の結果に、`#31` のどの観点が挙げたかを示す記録は無い） |
| 7 | 検証 | 本ファイル「申し送り」3 | 「現状この未検証であることの記録は `steering.md` の `#31` にしか無く」が成り立たない。本ファイル自身（申し送り3 と Completion Criteria 表）が記録であり、criterion 8 のとおり check-off コミットでブランチに入る。「`checks/` は残るが台帳・TODO からは辿れない」と書き分けるべき。要求（追跡の要否を user に確認）自体は妥当なので結論は変わらない | 未確認（検証観点の `grep` 結果による） |
| 8 | 検証 | 本ファイル「Method」表の `XLS-05`・`XLS-27` の行 | 「本作業ディレクトリ内に出典が無い」が言い過ぎ。参照できないのは converter リポジトリ側の**判定そのもの**であって、user が示した文面は `steering.md` の `#31`「根拠」として本作業ディレクトリ内にある。同じ表の別の行が自らそこを出典にしている。`checks/task-last.md:433` は正しく書き分けており、この行だけが粗い | 未確認（検証観点の指摘による。`steering.md` の `#31`「根拠」に文面があること自体は調整役も確認済み） |
| 9 | 検証 | 本ファイル「判定の内訳（3事象）」の (b) の記法上の裏づけの段落 | 「是正した `tools/testdata_converter.rst:37` の1行は、これと逆の含意を与えていた」が、本ファイル冒頭の「`file:line` は現在の作業ツリーを指す」という宣言と衝突する。現在の `:37` は是正後の文であり当該含意を持たない。是正前の現物は `git show 65a1756:…` の `:41` | 未確認（検証観点の指摘による） |

**user 裁定（2026-08-21）**: 是正ラウンド上限に対し4ラウンド目を1回だけ認め、削るだけで直る 指摘3・6・7・8・9 を直した。指摘1・2・4 は直さず、`#30` Step 6 のマージ直前の一括処置へ送る。

**指摘5 は処置不要**: `#32` の手順1で `tools/testdata_converter.rst` の本文を直すことで、指摘5 が指す未決点（`:39` の「外側」の限定、未検証のまま残した「マーカーカラム」）そのものが消えるため。

**無効と判定した指摘（1件）**: `.rn/` 内文書への行番号参照の不統一（クラフト観点）。指摘者自身が軽微とし、ルール制定後の先例 `checks/task-29.md:74` が同じ書き方をしていることも挙げている。`steering.md` の `#30` Step 6「それ以外の記録整備は行わない」の対象であり、マージ直前の一括処置に回す。
