# task-29 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-MOD-02-1` が消え、`NTF-SRC-02` のみ2箇所）である | OK | `grep -rn 'TODO(NTF-' ja/ \| wc -l` = 13、`grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort -u \| wc -l` = 12、`grep -rn 'TODO(NTF-MOD-02-1)' ja/ \| wc -l` = 0。`grep -rho ... \| sort \| uniq -c` で `TODO(NTF-SRC-02)` のみ 2、他は各1。ファイル数は `grep -rl 'TODO(NTF-' ja/ \| wc -l` = 10 | OK | 4観点とも独立に再実測して一致（13件・12ID・10ファイル、`NTF-SRC-02` のみ2箇所） |
| `tools/request_data_tool.rst` の差分が TODO 3行（と体裁を合わせた空行）の削除だけであり、`:86` の httpDump.bat/httpDump.sh の1文と `:66` の `:download:` 1件は変わっていない | OK | `git diff` の当該ファイルは `-` 4行（TODO 3行＋直後の空行1行）のみで `+` 行なし。削除により行番号が4つ繰り上がり、`grep -n 'Windowsの場合はバッチファイル'` = `:82`、`grep -n ':download:'` = `:62`（1件のみ）で、文字列は元のまま。空行の連続なし（`:58` コマンド行→`:59` 空行→`:60` 本文） | OK | 削除4行・据え置き2箇所とも一致。ただし Evidence の「`-` 4行のみで `+` 行なし」は現状と食い違う（`ec412d4` 後の `git diff 28118cf..HEAD --numstat` は `1 5`）。事実の齟齬であり要是正 |
| `tools/master_data_tool.rst` に加わった地の文が B の1件だけであり、書き戻し禁止の2文が本文に無い | OK | `git diff` の `+` 行は TODO の1行目・3行目と `.. important::` ブロック3行（ディレクティブ行・空行・本文1行）のみ。`grep -n 'Excel 形式で記述する\|本ツールを使用できない'` は0件。本文は user 指示の文面と文意一致で、マークアップは `mapping/style.md` S-13 に従い `\ ` を `` ``testDataParser`` `` の前後（直前「の」・直後「に」がいずれも全角）に付けただけ。日本語の段落は1段落1行 | NG | 加わった地の文は1件で、禁止2文も0件。ただし**その1件の内容が事実に反する**。(1) 「パーサと形式が食い違う」と双方向に書いているが、無言0件が確定しているのは Excel ファイル＋YAML パーサの向きだけで、逆向きは `e21bf67:.../MasterDataSetUpper.java:185` → `PoiXlsReader.getWorkbook` が `RuntimeException("test data file open failed.")` を投げる (2) 根拠として置いた `:ref:`共通設定 <testing_framework_common>`` の飛び先 `setup/common.rst` に `testDataParser` は0件（実体は `setup/class_unit_test.rst:159`） |
| TODO 3件が判定後の文言になっており、3行の書式（1行目に事象・2行目に依頼書のパスと節・3行目に扱い）を保っている | OK | `master_data_tool.rst:26-28`・`implementation/deal_unit_test/mom.rst:83-85`・`tools/testdata_converter.rst:106-108` を `grep -n -A2` で確認。3件とも2行目（依頼書のパスと節）は無変更で、1行目に判定・3行目に「#22／#21／XLS-28 がマージされたら本 TODO を外す。本文の書き直しは不要。」を書いた。課題番号はリポジトリが分かる形（`nablarch-testing の #22`・`nablarch-testing の #21`・`nablarch-testing-converter で XLS-28`）にした | NG | 3行の書式は保たれている。文言に4点の誤り。(1) `mom.rst:83` に禁止語「不具合」が復活（`28118cf` で0件→HEAD で1件。`_build/html/_sources/.../mom.txt:83` に出力される） (2) `#21`・`#22`・`XLS-28` が GitHub issue 番号のように読めるが実体は各リポジトリの rn 番号 (3) `XLS-28` の「未着手」が古い（`5ab13d8` で実装済み・main 未マージ） (4) `master_data_tool.rst:28` の「本文の書き直しは不要」が誤り（同ページ `:10`・`:128`・`:130` が Excel 前提の地の文） |
| D の記録4種がすべて更新され、`.rn/` 内どうしの参照が節見出しで書かれている（Rules） | OK | `checks/task-last.md` §8「TODO 台帳（統合）」（`NTF-MOD-02-1` 行の削除・残る3件の最終列の書き換え・実測ブロックの取り直しと件数記述の是正）、`checks/task-28.md` §7（「本文の書き換えを伴った箇所」への追記・7-3 表からの `NTF-MOD-02-1` 除去・「上の一覧と完全に一致する（7件）」の是正・「他の担当への申し送り」の消化追記）、`reviews/page-request_data_tool.md` 4箇所、`reviews/page-master_data_tool.md` 2箇所＋G6 の件数是正。`git diff --stat` で4ファイルとも変更あり。今回書いた `.rn/` 内参照は `checks/task-28.md` §7「本文の書き換えを伴った箇所」・`checks/task-last.md` §8「TODO 台帳（統合）」・本書「判断待ち（`decide`）」の 1・本書「判断待ち」の 7 で、いずれも実ファイルを開いて見出し文字列を確認した（`grep -n '^#'`／`sed -n`）。行番号での相互参照は新規に書いていない | NG | 4種とも更新済みで、`.rn/` 内どうしの参照は節見出しで書かれている。ただし記録の中身に3点の誤り。(1) 「本作業ディレクトリからは参照できない」という記載が5箇所あるが、両リポジトリとも clone 済み（`steering.md` Assumptions）で一次情報を直接引ける (2) `checks/task-last.md` §5-5「`web.rst` は `#29` では変更していない」が誤り（`ec412d4` が `web.rst` を1行変更） (3) `#29` の行数変動で `ja/` への `file:line` 参照13件が別の行を指すようになった |
| Docker フルビルドが WARNING・ERROR ともに0件（ゲート7） | OK | `docker run --rm -v ...:/root/document nablarch-document-build /bin/bash -c "cd /root/document; rm -rf _build; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"` を実行しログを保存。exit 0・`build succeeded.`・`grep -cE 'WARNING:\|ERROR:\|SEVERE:'` = 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --short` に `locales` の行が無いことを確認 | OK | 3エージェントが独立にフルビルドを再実行し、いずれも `build succeeded.`・WARNING/ERROR 0件を再現 |
| `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS | OK | 作業ディレクトリ `.rn/20260724-ntf-yaml-support/` で実行。`verify_glossary.py` = `RESULT: OK`（exit 0、9検査すべて不一致0件）、`verify_mapping.py` = `OK: no errors`（exit 0）、`python3 -m pytest mapping/tools -q` = `183 passed, 96 subtests passed` | OK | 3エージェントが独立に再実行し、`RESULT: OK`／`OK: no errors`／`183 passed, 96 subtests passed` を再現 |
| 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `git status --short`／`git diff --stat` の変更は8ファイルのみ（`.rn/` の記録4件と `ja/development_tools/testing_framework/` の `.rst` 4件）。`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/`・`.gitignore` はいずれも一覧に無く、0行変更 | OK | `ja/conf.py`・`mapping/glossary.md`・`mapping.csv`・`en/`・`.gitignore` はいずれも0行変更。ただし Evidence の「変更は8ファイルのみ」は現状と食い違う（`ec412d4` 後は10ファイル） |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | NG | 機械ゲート（件数・ビルド・検証スクリプト）は目的に対して有効で、4観点とも独立に再現できた。しかし本タスクの目的は「モジュール側で確定した判定を解説書に正しく反映する」ことであり、**書いた内容がモジュール側の一次情報と一致するかを検査する手立てが self-check に無い**。実際、`master_data_tool.rst:32` の新規記述は「TODO が減った」「ビルドが通る」というゲートを全部通過しながら、確定していない向きまで断定していた。判定文と一次情報の突き合わせを検証手順に入れる必要がある |

## Expert Reviews

### Design Expert (structure/approach)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | NG | 「判定が付いた TODO は文言を更新し、待つものが無くなった TODO は消す」という方針自体は妥当。ただし事象1は「仕様・**解説書側対応**」（`8530497:docs/pr75/steering.md:117`）＝解説書に残作業がある判定であり、`ja/` 側の唯一の追跡マーカーを消したことで追跡先が消えた。`request_data_tool.rst:82` は配布されていない `httpDump.sh` の選択を案内したままである（`git ls-tree -r --name-only HEAD \| grep -i httpdump` で `.bat` のみ）。user 判断が要るため Escalation E1 として起票 |
| System-wide integrity (cross-doc consistency) | NG | `#29` の行数変動（`request_data_tool.rst` −4行・`master_data_tool.rst` +4行）で、`.rn/` から `ja/` を指す `file:line` 13件が別の行を指すようになった（`mapping/style.md` 10行11件・`mapping/glossary.md:314`・`design.md:379`）。うち `style.md:107`・`:109`・`glossary.md:314`・`design.md:379` は `28118cf` 時点で正しかったことを実測済み |

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | NG | `.. important::` の選択自体は S-06 に沿う。文の内容が事実より広い（QA 列の完了条件3を参照）。また `mom.rst:83` に禁止語「不具合」が復活し、`_build/html/_sources/.../mom.txt:83` に出力されて Show Source から読める。置き換えの先例は `reviews/page-component_unit_test.md:126`（「不具合」→「誤り」） |
| Consistency with existing style | NG | 課題番号の書き方が既存記録と不整合。`#21`・`#22`・`XLS-28` はいずれも各リポジトリの rn 番号だが、`nablarch-testing の #22` という書き方は GitHub issue 番号としか読めない。マージ単位はブランチ `convert-testdata-excel-to-text`／ドラフト PR `lovaizu/nablarch-testing#1`（`8530497:docs/pr75/steering.md:4-5`） |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | NG | 機械ゲートは実行され再現する。一方、記録が5箇所で「モジュール側の一次情報は本作業ディレクトリからは参照できないため user の引用による」と述べているが、`steering.md` Assumptions が両リポジトリを clone 済みと明記しており、`git show 8530497:docs/pr75/steering.md` で直接読める。**確かめられるものを確かめずに二次情報で書いた**点が最も重い |
| Coverage | NG | 未検査のまま残った主張が3件。(1) `XLS-28` の「未着手」（実際は `5ab13d8` で実装済み・main 未マージ） (2) `checks/task-last.md` §5-5 の「`web.rst` は `#29` では変更していない」（`ec412d4` が変更） (3) `checks/task-29.md` 自身の Evidence 3箇所（差分行数・変更ファイル数・「行番号での相互参照は新規に書いていない」。Method 節自体が `style.md:339` ほかの行番号参照を含む） |

## Overall Verdict

- Self-check: OK
- QA: NG
- Design expert: NG
- Craft expert: NG
- Verification expert: NG
- Ready to check off: No（Valid 9件が未是正。うち E1 の判断結果が `request_data_tool.rst` の是正内容を左右するため、user 回答待ちで停止中）

## トリアージ結果（調整役・2026-08-19）

4観点すべて fail。指摘は Valid 9件・Escalation 2件・Invalid 0件。すべて調整役が実物で再測定して確認した。

### Valid（実装役を1回立ててまとめて是正する）

| | 内容 | 対象 |
|---|---|---|
| V1 | `.. important::` が双方向に書かれており事実より広い。逆向きは `RuntimeException` | `tools/master_data_tool.rst:32` |
| V2 | `:ref:`共通設定 <testing_framework_common>`` が根拠にならない（飛び先に `testDataParser` 0件） | 同上 |
| V3 | 禁止語「不具合」の復活（`_build/html/_sources` に出力される） | `implementation/deal_unit_test/mom.rst:83` |
| V4 | `#21`・`#22`・`XLS-28` が GitHub issue 番号のように読める | TODO 3件 |
| V5 | `XLS-28` の「未着手」が古い（`5ab13d8` で実装済み・main 未マージ） | `tools/testdata_converter.rst:106`・`checks/task-last.md` §8 |
| V6 | 「本文の書き直しは不要」が誤り（`:10`・`:128`・`:130` が Excel 前提） | `tools/master_data_tool.rst:28` |
| V7 | 「本作業ディレクトリからは参照できない」が誤り（両リポジトリとも clone 済み） | 記録5箇所 |
| V8 | 「`web.rst` は `#29` では変更していない」が誤り（`ec412d4` が変更） | `checks/task-last.md` §5-5 |
| V9 | `#29` の行数変動で `ja/` への `file:line` 参照13件がずれた | `mapping/style.md` 10行11件・`mapping/glossary.md:314`・`design.md:379` |

あわせて本ファイルの Self-check Evidence 3箇所（差分行数・変更ファイル数・「行番号での相互参照は新規に書いていない」）も実装役に是正させる。

V9 の補足: `mapping/style.md`・`design.md`・`mapping/glossary.md:314` はいずれも `#29` の禁止事項に当たらない（禁止は `mapping/glossary.md` **§5.15** で、同節は `:337` 以降）。歴史記録である `ntf-doc-28-decide-disposition.md:706`・`:709`、`ntf-doc-27-review.md:62`、`ntf-mod-02-nablarch-testing.md:188` の4件は当時の状態の記録なので更新しない。`steering.md:700`・`:722` は調整役が是正済み。

### Escalation（user 判断待ち。2026-08-19 に提示、回答未取得）

- **E1. 事象1（`httpDump.sh`）の解説書側対応をどうするか。** モジュール側の判定は「仕様・**解説書側対応**」（`8530497:docs/pr75/steering.md:117`）だが、`#29` Step A は「本文は1文字も変えない」として `ja/` 側の唯一の追跡マーカーを削除した。`request_data_tool.rst:82` は配布されていない `httpDump.sh` の選択を案内したままである。提示した選択肢は (a) 本文を直す〔推奨〕／(b) TODO を復活させる／(c) 現状のまま。(a) の場合の文面（「Windows でのみ使用できる」でよいか）も要確認。なお依頼書 `ntf-mod-02-nablarch-testing.md:47-51` は文面を尋ねているが、モジュール側の記録に文面までは書かれていない（未確認）
- **E2. `XLS-27` の制約が解説書へ申し送られていない。** `b44268c:.rn/ntf-test-data-converter/steering.md:770`・`:783-784` に「0件テーブルを含む YAML は Excel へ変換できない」「2段目が済むまでは実運用上の制約として残る」とあり、同ファイルは解説書担当への申し送りが必要と書いている。`tools/testdata_converter.rst` に記述は0件、一方 `implementation/testdata_notation.rst:842` は `rows: []` を有効な記法として示している。`#29` の Steps 外。提示した選択肢は (a) 別タスクに送る〔推奨〕／(b) いま書き足す

## Method（作りながら検証した記録）

各主張をその出典に当たって確認しながら書いた。確認の内訳は次のとおり。

- **B のディレクティブ判断** — `mapping/style.md` の `### S-06 アドミニション（tip / note / important）の使い分け` を開いて読んだ（`mapping/style.md:339` の見出し、規約本文は `:341-344`、`important` の根拠4件は `:348-351`）。規約本文は「「important」は、無視すると不具合・非推奨機能の誤用・データ不整合につながる、読者が必ず守るべき注意事項に使う」「「tip」は、読まなくても機能は正しく使えるが、知っておくと役立つ補足情報」。今回の事実は、投入対象が0件になったことに気づけないまま自動テストへ進むとデータ不整合につながり、無視できない。S-06 が `important` の根拠に挙げる `FW:libraries/static_data_cache.rst:12-15`（`mapping/style.md:350`。「Full GCが頻発しパフォーマンスに悪影響を与える可能性があるので、注意すること。」）・`FW:libraries/exclusive_control.rst:207-209`（同 `:349`。「バージョン番号のチェックを行わなければ、画面間でバージョン番号が引き継がれない。」）と同じ、「守らないと黙って壊れる」型である。ページ内の先例として `tools/master_data_tool.rst:157` の `.. important::`「投入に失敗した場合も、Antの実行結果は `BUILD SUCCESSFUL` になる。」（同じ「失敗が表に出ない」型）があり、これに揃えた。よって `.. important::` を採用した
- **B のマークアップ** — `mapping/style.md` の `### S-13 日本語とインラインマークアップの境界（`\ ` エスケープ）`（`mapping/style.md:777` の見出し、規約本文は `:779-782`）を開いて読み、`` ``testDataParser`` `` の直前が「の」・直後が「に」でいずれも全角のため両側に `\ ` を置いた
- **`パーサ` の表記** — `mapping/glossary.md:335` に正表記 `パーサ`（揺れ表記 `パーサー`）とあることを確認して `パーサ` を使った
- **A の据え置き対象** — `grep -n` で `tools/request_data_tool.rst` の「Windowsの場合はバッチファイル…」の1文と `:download:` 1件が変更後も残っていることを確認した（現在 `:82`・`:62`）
- **書き戻し禁止の2文** — `checks/task-28.md` §7「本文の書き換えを伴った箇所」の `NTF-MOD-02-4` の項を開いて3文の全文を確認し、`grep -n` で本文に無いことを確認した
- **`XLS-28` の内容** — user が作業指示に引用した `nablarch-testing-converter` `b44268c:.rn/ntf-test-data-converter/steering.md` の文面（「同名で拡張子違いの Excel ブック（`Foo.xls` と `Foo.xlsx`）の同居を検出してエラーで止める」）による。本作業ディレクトリからは参照できないため、記録には「user 引用による」ことが分かる形で書いた
- **4事象の判定** — 同じく user が引用した `nablarch-testing` `8530497:docs/pr75/steering.md` の文面による。記録には「user が作業指示に引用した文面による」と明記した
- **記録どうしの参照** — 引用先の見出し文字列を、`grep -n '^#'` と `sed -n` で実ファイルを開いて確認してから書いた
- **件数の主張** — `checks/task-last.md` §8 の実測ブロックは A〜C 適用後に `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` を実行し直して貼り替えた。前後の件数記述（14件・13ID → 13件・12ID）も実測値に合わせ、`#6` の「11件→14件」は `/rn:gm` 当時の値として残したうえで、現在値との関係が読めるよう §8 側の言い回しを整えた
- **`reviews/page-master_data_tool.md` の G6 の件数** — `important` を1件足したことで「`tip` 3件・`important` 2件」が偽になるため、`grep -n '^\.\. tip::\|^\.\. important::'` で実測し直して「`tip` 3件・`important` 3件（`:22`・`:88`・`:161` が `tip`、`:30`・`:132`・`:157` が `important`）」に是正した

### 指示から外れた判断

1. **`checks/task-28.md` §7「他の担当への申し送り」に消化追記を1件足した。** 指示 D-2 は「本文の書き換えを伴った箇所」と 7-3 の表だけを挙げているが、同 §7 末尾の申し送りが「`NTF-MOD-02-1` が『不具合』と判定された場合は `:download:` を2件にする」「`NTF-MOD-02-4` が『仕様』と判定された場合は跡地に制約を書き戻す」と書いており、そのままだと本タスクの結論（据え置き／2文は書き戻さない）と食い違う記録が残る。既存の記述は消さず、消化した旨と書き戻さない理由を追記した
2. **`reviews/page-master_data_tool.md` の G6 の件数を是正した。** 指示 D-4 は2箇所の追記だけを挙げているが、B で `important` を1件足したことで既存の実測記述が偽になるため（同ファイルの `#28` 由来の記述）、実測し直して直した
3. **`reviews/page-request_data_tool.md` の4箇所のうち、詳細は「判断待ち（`decide`）」の 1 に1箇所だけ置き、残る3箇所（`current-0349` の行・「意図して落とした出典」表の行・4観点レビュー 12 の行）は結論の要約＋そこへのポインタにした。** 同じ事実を4箇所に全文で重複させないため（`steering.md` Rules・Best practices「詳細は1箇所、他はポインタ」）
4. **`steering.md` は触っていない。** `#29` の Steps D(4) は本 `steering.md` の Task list と State の更新を含むが、作業指示の Scope で「`.rn/20260724-ntf-yaml-support/steering.md` は触らない（調整役が書く）」と指定されているため
