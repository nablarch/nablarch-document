# task-29 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `ja/` 配下の `TODO(NTF-` が **13件・12ID**（`NTF-MOD-02-1` が消え、`NTF-SRC-02` のみ2箇所）である | OK | `grep -rn 'TODO(NTF-' ja/ \| wc -l` = 13、`grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort -u \| wc -l` = 12、`grep -rn 'TODO(NTF-MOD-02-1)' ja/ \| wc -l` = 0。`grep -rho ... \| sort \| uniq -c` で `TODO(NTF-SRC-02)` のみ 2、他は各1。ファイル数は `grep -rl 'TODO(NTF-' ja/ \| wc -l` = 10 |  |  |
| `tools/request_data_tool.rst` の差分が TODO 3行（と体裁を合わせた空行）の削除だけであり、`:86` の httpDump.bat/httpDump.sh の1文と `:66` の `:download:` 1件は変わっていない | OK | `git diff` の当該ファイルは `-` 4行（TODO 3行＋直後の空行1行）のみで `+` 行なし。削除により行番号が4つ繰り上がり、`grep -n 'Windowsの場合はバッチファイル'` = `:82`、`grep -n ':download:'` = `:62`（1件のみ）で、文字列は元のまま。空行の連続なし（`:58` コマンド行→`:59` 空行→`:60` 本文） |  |  |
| `tools/master_data_tool.rst` に加わった地の文が B の1件だけであり、書き戻し禁止の2文が本文に無い | OK | `git diff` の `+` 行は TODO の1行目・3行目と `.. important::` ブロック3行（ディレクティブ行・空行・本文1行）のみ。`grep -n 'Excel 形式で記述する\|本ツールを使用できない'` は0件。本文は user 指示の文面と文意一致で、マークアップは `mapping/style.md` S-13 に従い `\ ` を `` ``testDataParser`` `` の前後（直前「の」・直後「に」がいずれも全角）に付けただけ。日本語の段落は1段落1行 |  |  |
| TODO 3件が判定後の文言になっており、3行の書式（1行目に事象・2行目に依頼書のパスと節・3行目に扱い）を保っている | OK | `master_data_tool.rst:26-28`・`implementation/deal_unit_test/mom.rst:83-85`・`tools/testdata_converter.rst:106-108` を `grep -n -A2` で確認。3件とも2行目（依頼書のパスと節）は無変更で、1行目に判定・3行目に「#22／#21／XLS-28 がマージされたら本 TODO を外す。本文の書き直しは不要。」を書いた。課題番号はリポジトリが分かる形（`nablarch-testing の #22`・`nablarch-testing の #21`・`nablarch-testing-converter で XLS-28`）にした |  |  |
| D の記録4種がすべて更新され、`.rn/` 内どうしの参照が節見出しで書かれている（Rules） | OK | `checks/task-last.md` §8「TODO 台帳（統合）」（`NTF-MOD-02-1` 行の削除・残る3件の最終列の書き換え・実測ブロックの取り直しと件数記述の是正）、`checks/task-28.md` §7（「本文の書き換えを伴った箇所」への追記・7-3 表からの `NTF-MOD-02-1` 除去・「上の一覧と完全に一致する（7件）」の是正・「他の担当への申し送り」の消化追記）、`reviews/page-request_data_tool.md` 4箇所、`reviews/page-master_data_tool.md` 2箇所＋G6 の件数是正。`git diff --stat` で4ファイルとも変更あり。今回書いた `.rn/` 内参照は `checks/task-28.md` §7「本文の書き換えを伴った箇所」・`checks/task-last.md` §8「TODO 台帳（統合）」・本書「判断待ち（`decide`）」の 1・本書「判断待ち」の 7 で、いずれも実ファイルを開いて見出し文字列を確認した（`grep -n '^#'`／`sed -n`）。行番号での相互参照は新規に書いていない |  |  |
| Docker フルビルドが WARNING・ERROR ともに0件（ゲート7） | OK | `docker run --rm -v ...:/root/document nablarch-document-build /bin/bash -c "cd /root/document; rm -rf _build; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"` を実行しログを保存。exit 0・`build succeeded.`・`grep -cE 'WARNING:\|ERROR:\|SEVERE:'` = 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --short` に `locales` の行が無いことを確認 |  |  |
| `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS | OK | 作業ディレクトリ `.rn/20260724-ntf-yaml-support/` で実行。`verify_glossary.py` = `RESULT: OK`（exit 0、9検査すべて不一致0件）、`verify_mapping.py` = `OK: no errors`（exit 0）、`python3 -m pytest mapping/tools -q` = `183 passed, 96 subtests passed` |  |  |
| 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `git status --short`／`git diff --stat` の変更は8ファイルのみ（`.rn/` の記録4件と `ja/development_tools/testing_framework/` の `.rst` 4件）。`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/`・`.gitignore` はいずれも一覧に無く、0行変更 |  |  |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective |  |  |

## Expert Reviews

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice |  |  |
| Consistency with existing style |  |  |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked |  |  |
| Coverage |  |  |

## Overall Verdict

- Self-check: OK
- QA:
- Craft expert:
- Verification expert:
- Ready to check off:

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
