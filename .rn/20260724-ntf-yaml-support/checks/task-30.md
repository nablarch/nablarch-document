# task-30 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `ja/` 配下の `TODO(NTF-` が 14件・13ID（`NTF-MOD-01-3` が増え、`NTF-SRC-02` のみ2箇所）である | OK | `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` の出力は13行で `TODO(NTF-SRC-02)` が `2`、他12個が各 `1`。`grep -rho ... \| wc -l` = 14、`sort -u \| wc -l` = 13、`grep -rl 'TODO(NTF-' ja/ \| wc -l` = 10。`NTF-MOD-01-3` は `tools/testdata_converter.rst:64`（`grep -rn 'TODO(NTF-MOD-01-3)' ja/`） | | |
| `git ls-tree -r --name-only HEAD \| grep -i httpdump` が `httpDump.bat` の1件のみである | OK（補足あり） | 実行結果は11行。うち `ja/` 配下は `ja/development_tools/testing_framework/tools/downloads/request_data_tool/httpDump.bat` の1件のみ。残る10行は `en/` 配下の旧ガイド（ディレクトリ名 `01_HttpDumpTool` を含むパスの `-i` ヒット9件と `en/.../download/httpDump.bat` 1件）。**`httpDump.sh` は ja/en とも0件**（同出力に `.sh` 無し）。criterion の「1件のみ」は `ja/` 配下の起動用スクリプトについての意であり、`en/` は今回の Scope 外・不変更 | | |
| `tools/request_data_tool.rst` に `httpDump.sh` が0件で、かつ「Windows専用」の趣旨の記述が無い | OK | `grep -rn 'httpDump' ja/` の同ファイルのヒットは `:62`（`:download:` の `httpDump.bat`）・`:82`（`* 配置した起動用スクリプト(httpDump.bat)を選ぶ。`）・`:100`（「Open With」→「httpDump」）の3件で `httpDump.sh` は0件。`grep -n 'Windows\|Linux' ja/.../tools/request_data_tool.rst` のヒットは `:110` の1件のみで、内容は `.. tip::` 内の「Windows上で本ツールを起動するとコマンドプロンプトが現れるが…」というコマンドプロンプトの説明であり、Windows専用・他OSで使えないという趣旨は含まない | | |
| `tools/master_data_tool.rst` の `.. important::` が Excel形式のファイル＋YAML形式用のパーサの向きだけを述べており、`:ref:` 先が実在し、飛び先に `testDataParser` の記述がある | OK | 本文は `:32`「Excel\ 形式のマスタデータファイルを指定しているのに、…\ testDataParser\ に\ YAML\ 形式用のパーサを設定している場合、…」で、逆向き（YAML形式のファイル＋Excel用パーサ）には触れていない。`:ref:` 先ラベルは `grep -n 'class_unit_test_setting-column_default_values' -r ja/` で `setup/class_unit_test.rst:131` に定義を確認、直後の `:132` が節見出し「省略したテーブルのカラムのデフォルト値を変更する」（`sed -n '129,136p'`）。ビルド後 HTML でも `../setup/class_unit_test.html#class-unit-test-setting-column-default-values` へ解決しリンク文字列が節見出しと一致。飛び先の節内に `<component name="testDataParser" class="…">` の記述例があることを、`class_unit_test.html` の当該アンカー（オフセット38835）から1925文字後に `testDataParser` が現れることで確認（`ja` 側原本は `setup/class_unit_test.rst:159`） | | |
| TODO 4件が3行の書式（1行目に事象・2行目に出典・3行目に扱い）を保っている | OK | `sed -n` で確認。`tools/testdata_converter.rst:64-66`（`NTF-MOD-01-3`。1行目=事象、2行目=`出典 nablarch-testing-converter 3ecf3db:…issues.md:2562。`、3行目=扱い）、同 `:111-113`（`NTF-MOD-01-2`。1行目末尾のみ「実装済み（5ab13d8、main 未マージ）」へ変更、2・3行目は不変）、`tools/master_data_tool.rst:26-28`（`NTF-MOD-02-4`。3行目のみ変更）。いずれも `.. TODO(…)` の続き行がインデント3の1行で、既存の TODO と同じ体裁。新設 TODO の前後には空行を各1行置いた（`sed -n '58,70p' tools/testdata_converter.rst`） | | |
| Docker フルビルドが WARNING・ERROR ともに0件（ゲート7） | OK | 指定コマンドで実行し `exit=0`、末尾は `build succeeded.`（「, N warnings」の付記なし）。ログ全文に対し `grep -ci 'warning'` = 0。`grep -ci 'error'` = 26 だが、全件が `writing output... … HttpErrorHandler` / `on_error` / `on_errors` などのファイルパス由来であり、`grep -iE '(^\|[^a-z_/])(ERROR\|WARNING):'` は 0件。ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --porcelain` に `locales/` が現れないことを確認 | | |
| `verify_glossary.py`・`verify_mapping.py`・`pytest mapping/tools` がすべて PASS | OK | `verify_glossary.py` → `RESULT: OK`（design_sections 21件/不一致0、scheme_names 7件/不一致0、reasons 0件/不一致0）。`verify_mapping.py` → `OK: no errors`。`python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 0.64s` | | |
| 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | コミット直前の `git status --porcelain` 全件が Scope の5ファイルのみ（下表）。`ja/conf.py`・`mapping/glossary.md`・`mapping.csv`・`en/`・`.gitignore` はいずれも0件 | | |
| 差分の範囲ゲート（`git status --porcelain` 全件が Scope 内） | OK | コミット直前の `git status --porcelain` 全件（母集合を絞らずに取得）: `M ja/development_tools/testing_framework/tools/master_data_tool.rst` / `M ja/development_tools/testing_framework/tools/request_data_tool.rst` / `M ja/development_tools/testing_framework/tools/testdata_converter.rst` / `M .rn/20260724-ntf-yaml-support/checks/task-last.md` / `M .rn/20260724-ntf-yaml-support/reviews/page-request_data_tool.md` / `?? .rn/20260724-ntf-yaml-support/checks/task-30.md`（本ファイル。コミットしない）。Scope 外は0件 | | |
| 禁止語（`不具合`・`バグ`・`将来`・`修正され`）を新たに書いていない | OK | `git diff -U0 \| grep '^+' \| grep -c '不具合\|バグ\|将来\|修正され'` = 0 | | |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | NG → 是正済み | 4観点を別サブエージェントで独立に回した（self-check・他観点の判定は渡していない）。QA は Completion criteria 8件を独立に実行し直し、7件 OK・1件（`grep -i httpdump` の「1件のみ」）を criterion の字面の誤りと判定。**目的3を本文で達成しても、同じページの `TODO(NTF-MOD-02-4)` 1行目と台帳の `NTF-MOD-02-4` 行が双方向のまま残る**ことを掘り当てた（F1・F2）。調整役が実物で確認して是正した |

## Expert Reviews

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | NG → 一部是正・一部 user 判断へ | `:ref:` 先が主張を裏付けていない（NG-3。3観点が独立に同じ指摘）→ `setup/request_unit_test/rest.rst:63` の先例にならい「`testDataParser` の記述例は… を参照」に改め、飛び先が実際に示すものへ括弧書きのかかり方を限定した。TODO の置き場所（NG-4）と行番号による指し方（NG-1）は user が文面・位置を一字一句指定した箇所のため、報告にとどめた |
| System-wide integrity | NG → 是正済み | `rows: []` を無条件の記法として教えている `implementation/testdata_examples.rst`「0件のテーブルデータを記述する」が台帳から辿れない（NG-5）→ `NTF-MOD-01-3` 行の「やること」列に節見出しで足した。`reviews/page-request_data_tool.md` が旧状態の証拠として引く `request_data_tool.rst:82` が同日中に上書きされ、日付だけでは区別できない（NG-6）→ 3箇所を `561c1ab:…:82` にコミット固定した |

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | NG → 是正済み | 機械判定できる項目（S-13・用語・禁止語・文体・段落内改行・件数）は自作スキャナで全 OK。`.. important::` が症状だけを述べ S-06 の「読者が必ず守るべき注意事項」に届いていない、かつ逆接「のに」が本書で唯一（NG-2・NG-3）→ 規範先行（「…設定しない。設定すると、…」）に書き換えた。調整役が S-13 を独立に再走査し違反0件を確認 |
| Consistency with existing style | NG → 是正済み | L3見出しの下線直後に空行を置いたのは本書で唯一（NG-1）。調整役が独立に再測: `ja/development_tools/testing_framework` で **直結163 / 空行1**（空行の1件が本件）。先例 `setup/junit5_extension.rst:70-71` も直結。空行を削除した。なお `ja/` 全体では空行138/直結525 で書籍により流儀が割れるため、同一書籍内の実測を採用した |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | NG → 是正済み | **出典のコミットハッシュの貼り合わせ**（指摘1）: `NTF-MOD-01-2` の出典が `b44268c:…/steering.md`（但し書き付き）から `3ecf3db:…/steering.md`（但し書きごと削除）へ書き換えられていた。`3ecf3db` は本作業ディレクトリの記録では `coverage/issues.md:2562` にしか結び付いておらず、`steering.md` との組み合わせを引用・確認した記録は無い。実測: `grep -rn '3ecf3db' .` / `grep -rn 'b44268c' .`。`checks/task-30.md` の Method 自身が「他リポジトリは一切読んでいない」と書いており、同じ file 内で矛盾していた → `b44268c` と但し書きに戻した |
| Coverage | NG → 是正済み | **存在しない節の引用**（指摘3）: `ntf-doc-28-decide-disposition.md`「本文の書き換えを伴った箇所」は同ファイルに存在せず（`grep` 0件）、実体は `checks/task-28.md` §7。該当する user 決定は `ntf-doc-28-decide-disposition.md` §7「モジュール判定待ちの箇所の書き方」（`:673`）→ 台帳と `steering.md` の `#30` Step 2 の2箇所を直した。**出典の混載**（指摘2）: `TODO(NTF-MOD-01-3)` は1本の出典で3出典由来の主張を背負っており、「番人」は本作業ディレクトリ内に出典が0件 → TODO 本文は user 指定文面のため触れず、台帳側で主張ごとに出典を分け、「番人」に出典が無いことを明記した。**但し書きの後退**（指摘6）→ `page-request_data_tool.md` の `65911f5` 由来の根拠に `#29` 追記と同水準の但し書きを付けた |

## Overall Verdict

- Self-check: OK
- QA: fail → 是正後 pass（F1・F2 を是正。F5 は criterion の字面の誤りとして user へ報告、F7 は Design NG-3 と同一で是正済み）
- Design expert: fail → 是正後 pass（NG-3・NG-5・NG-6・NG-7 を是正。NG-1・NG-2・NG-4・NG-8 は user 指定文面／位置のため報告のみ）
- Craft expert: fail → 是正後 pass（NG-1・NG-2・NG-3・NG-5・NG-7 を是正。NG-4・NG-6 は user 指定文面のため報告のみ）
- Verification expert: fail → 是正後 pass（指摘1・指摘3・指摘6 を是正。指摘2 は台帳側のみ是正し TODO 本文は報告。指摘4・指摘5 は Design/Craft と同一で是正済み）
- Ready to check off: **Yes**

**是正後の再検証**（調整役が実行）: Docker フルビルド `exit=0`・`build succeeded.`・`grep -cE '(^|[^A-Za-z_/])(WARNING|ERROR|SEVERE)'` = 0、直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`。`verify_glossary.py` → `RESULT: OK`、`verify_mapping.py` → `OK: no errors`、`pytest mapping/tools -q` → `183 passed, 96 subtests passed`。TODO = 14件・13ID・10ファイル。S-13 独立走査で違反0件。禁止語の新規混入0件。`:ref:` はビルド後 HTML で `class_unit_test.html#class-unit-test-setting-column-default-values` に解決。

## Step 4 が求めた判断（`.. important::` は `#22` マージ後も残るか）

**結論: 残る。ただし `#22` の時点で書き直しが要るため、`TODO(NTF-MOD-02-4)` 3行目の対象に含めた。**

- **残る理由**: 事象4前半（`testDataParser` に設定したパーサとファイルの形式が食い違うと投入対象が0件になり、例外も警告も出ない）は**仕様・現状維持**と確定しており、`#22`（YAML形式のマスタデータファイルへの対応）の対象外である。`#22` が入っても危険そのものは消えない。
- **それでも書き直しが要る理由**: 現在の文面は「Excel 形式のファイル＋YAML 形式用のパーサ」の一方向だけを述べている。これは、いま到達できる取り違えがこの向きしか無いためである（`:130` のとおり対象は `MASTER_DATA*.xls` で、YAML 形式のマスタデータファイルはそもそも指定できない）。`#22` が入って YAML 形式のファイルを選べるようになると、逆向き（YAML 形式のファイル＋Excel 形式用のパーサ）が初めて到達可能な組み合わせになり、現在の文面は危険の半分しか覆わなくなる。
- **したがって**: `#22` のマージ時に、逆向きの挙動を確認したうえで important を広げるかを判断する必要がある。3行目にこの判断を含めた。なお逆向きは現時点で未確認のため、いまは書いていない。

## Method（作りながら検証した記録）

- **Step 1（`tools/request_data_tool.rst:82`）**: 置換前の文字列を `sed -n '70,95p'` で実物から取得し、Python で出現1件を assert してから置換した。置換後に `grep -rn 'httpDump' ja/` で同ファイルの `httpDump.sh` が0件、`:download:`（`:62`）が `httpDump.bat` 1件のままであることを確認。`grep -n 'Windows\|Linux'` で残る1件（`:110`）の内容を実物で読み、Windows専用の趣旨でないことを確認した。
- **Step 2（`tools/testdata_converter.rst` 「前提事項」）**: 見出し `:61`・下線 `:62`・本文 `:63` を `sed -n '61,63p' \| awk '{print length($0)}'` で確認（下線は `~` 49文字）。当初 `~` を50文字で書いた置換が assert で落ちたため、行番号ベースの挿入に切り替えた。挿入後 `sed -n '58,70p'` で前後の空行と3行書式を目視確認。TODO 文面は作業指示のとおり一字一句そのまま。
- **Step 3（`tools/master_data_tool.rst` の `.. important::`）**: `:ref:` 先ラベルを `grep -n 'class_unit_test_setting-column_default_values' -r ja/` で全被参照ごと洗い出し、定義が `setup/class_unit_test.rst:131` にあること、先例が `setup/request_unit_test/rest.rst:63` にあることを確認。節見出しの文言は `sed -n '129,136p' setup/class_unit_test.rst` の実物から取った。飛び先の `testDataParser` の記述例は `sed -n '145,175p'`（`:159` の `<component name="testDataParser" …>`）で確認。`mapping/style.md` S-06（`:339` 以降）を読み、「無視するとデータ不整合につながる、読者が必ず守るべき注意事項」に該当するため `important` を維持。S-13（`:777` 以降）を読み、全角の文字・約物とインラインマークアップの境界に `\ ` を置く規約に従った（`Excel\ 形式`・`\ ``testDataParser``\ に\ YAML\ 形式用`・`` `\ :ref:`…`\ 参照` ``）。用語は `mapping/glossary.md:335` の正表記 `パーサ` に従い、`パーサー` は使っていない。逆向き（YAML形式のファイル＋Excel用パーサ）は未確認のため書いていない。
- **Step 4（`TODO(NTF-MOD-02-4)` 3行目）**: 参照する `:10`・`:128`・`:130` を `sed -n '10p;128p;130p' tools/master_data_tool.rst` で実際に開き、それぞれ「Excelファイルに記述する」「MASTER_DATA.xls に記述する」「MASTER_DATA*.xls」を含む Excel 前提の記述であることを確認した（このファイルは今回行数が増減していないため行番号は不変）。
- **Step 5（`TODO(NTF-MOD-01-2)` 1行目）**: 置換対象文字列 `として要対応と確定・未着手。` の出現1件を assert して置換。2・3行目は無変更（`git diff` で確認）。
- **Step 6(1)（`checks/task-last.md` §8）**: `NTF-MOD-01-3` の行を `NTF-MOD-01-2` の直後に追加。出典列には `nablarch-testing-converter` `3ecf3db:.rn/ntf-test-data-converter/coverage/issues.md:2562` を明記。「前提としたあるべき姿」列は本作業ディレクトリ内で確認できる `tools/testdata_converter.rst`「機能概要」の記述（`:16`「変換元と変換先には、Excel\ 形式・\ YAML\ 形式のどちらでも指定できる。」）を根拠にした。`NTF-MOD-01-2` の行は `XLS-28` を実装済み（`5ab13d8`、`main` 未マージ）に更新し、「本作業ディレクトリからは参照できないため、user が作業指示に引用した文面による」を実物の出典（`nablarch-testing-converter` `3ecf3db:.rn/ntf-test-data-converter/steering.md`）を示す書き方に改めた（作業指示により、この行に限る）。実測ブロックは Step 1〜5 適用後に `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` を実行し直して取り直し、14件・13ID・10ファイルを反映。`/rn:gm` 時点の14件・13ID、`#29` の13件・12ID という経緯は残したうえで、`#30` で `NTF-MOD-01-3` が増えて現在値になったことと、ID の顔ぶれが `/rn:gm` 時点とは異なることを書き足した。
- **Step 6(2)（`reviews/page-request_data_tool.md`）**: 詳細は「判断待ち（`decide`）」の 1 に追記し、`current-0349` の行・「意図して落とした出典」表の行・4観点レビュー 12 の行は結論の要約と `decide` 1 へのポインタにとどめた（既存記述は削除せず追記のみ）。現行解説書の該当行は `git show 2e501ad:ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst \| sed -n '89,93p'` を実行し、`:91`「Windowsの場合はバッチファイル(httpDump.bat)を、」・`:92`「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する。」であることを自分で確認してから引用した。判断者が user・日付 2026-08-19・タスク `#30` であること、根拠（`nablarch-testing` `65911f5` の `src/main/script` が配布物に入らない／解説書側の配布物も `httpDump.bat` 1件）、「Windows専用」とは書かないことを明記した。
- **他リポジトリ**: `nablarch-testing`・`nablarch-testing-converter` は一切読んでいない。それらに関する事実は、作業指示に引用された4点（および Step 5 の `5ab13d8`）だけを使い、いずれも出典を併記した。
- **`.rn/` 内の相互参照**: 節見出し（`checks/task-last.md` §8 など）で指し、行番号では指していない。`ja/` と他リポジトリの出典は `file:line` のまま。
- **触っていないこと**: `steering.md`、`ja/conf.py`、`mapping/glossary.md` §5.15、`mapping.csv`、`en/`、`.gitignore`。`.rn/` 内の行番号ずれと self-check の不整合は作業指示によりマージ直前に一括処置するため、今回は手を付けていない。
