# task-35 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `tools/testdata_converter.rst` の該当段落が §1 の変更後の文と一致する。`grep -rn 'メッセージのテストデータ' ja/` が0件 | NG | **§1 の反例検索で反例が見つかったため、指示書 §1 の「1系統でも落ちない経路が見つかったら、この段落は書かずに報告すること」に従い `:71` を変更していない。** `grep -rn 'メッセージのテストデータ' ja/ \| wc -l` → `1`（`:71` の既存文）。反例の実測は `reviews/page-testdata_converter.md` §「`#35`（`:71` の段落の書き換え可否を実装から検証、2026-08-21）」(b) に記録した | | |
| 2. `tools/testdata_converter.rst` に「この整形」が無い（`grep -n 'この整形' …` が0件） | NG | `grep -n 'この整形' ja/development_tools/testing_framework/tools/testdata_converter.rst` → 2行ヒット（`:71`・`:249`）。`:71` は 1 の理由で未変更。**`:249` は `:71` とは無関係の既存文であり、この完了条件は指示書の範囲内では満たせない。** `:249` の逐語は「\ Excel\ 形式へ書き出す場合は、人が見て編集することを前提に、行の種別ごとの装飾やレイアウトを付けて読みやすく整える。この整形は設定で変更でき、設定しなかった項目にはデフォルト値が適用される。」で、指示書 §1 が「このページの「整形」は同 `:63`・`:247`・`:249` で書き出し時の装飾に固定されている」と述べているその `:249` そのものである | | |
| 3. `reviews/page-testdata_converter.md` に、5系統すべてで行末の空セルが落ちることを実装から確かめた経路が記録されている | OK（条件付き） | 5系統すべての経路を記録した（同節 (a) の表。テーブル系 `TableDataParser.java:93`→`HeaderLine.java:33`／`LIST_MAP` `ListMapParser.java:64`＋`TestCoreReaderAdapter.java:128`／ファイル系 `DataFileParser.java:68`／メッセージ `MessageParser.java:115`→`:44`・`:58`→`DataFileParser.java:68`／同期応答電文 `SendSyncMessageParser.java:16`＋`TestCoreReaderAdapter.java:318`）。**ただし「落ちる」が成り立つのはカラム名の行（フィールド名の行）の行末の空セルとカラム名が無い位置のセルに限られ、データ行のカラム名がある位置の行末の空セルは `HeaderLine.java:81` / `XlsFormatReader.java:424` で空文字として中間モデルへ埋め戻される。** 同節 (b) に実測（`XlsFormatReaderCellTypeTest.java:182`-`:188`、`XlsFormatReaderInvalidInputTest.java:765`-`:766`・`:811`-`:812`）を記録した | | |
| 4. `implementation/testdata_notation.rst` の `list-table` に §2 の行があり、既存の `:1544`-`:1545` が変わっていない。`reviews/page-testdata_notation.md` に出典がある | OK | `git diff -- ja/development_tools/testing_framework/implementation/testdata_notation.rst` が `+  * - テーブル・\ ``LIST_MAP``` と `+    - カラム名の行の行末の空セルを取り除く。カラム名が無い位置のセルは読み込まれない（\ Excel\ 形式のみ）` の2行の追加のみ（`1 file changed, 2 insertions(+)`）。文脈行に `:1544`-`:1545` が変更なしで現れる。出典は `reviews/page-testdata_notation.md` §「`#35`（読み込み時の整形・補完の表に「テーブル・`LIST_MAP`」の行を追加、2026-08-21）」 | | |
| 5. `mapping.csv` の `note` に「なお同じ基準で 9031fa6 が」が0件、「なお 9031fa6 も同じ基準で」が5件 | OK | `grep -o 'なお同じ基準で 9031fa6 が' mapping/mapping.csv \| wc -l` → `0`。`grep -o 'なお 9031fa6 も同じ基準で' mapping/mapping.csv \| wc -l` → `5` | | |
| 6. `_batch/*.csv` を昇順連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、`csv.DictReader` が597行。`82322fa` との差分が指定5行の `note` のみであることを `git diff` で全行確認する | OK | Python で `sorted(glob('_batch/*.csv'))` 30ファイルをバイナリ連結（2つ目以降は最初の `\n` まで除去）→ `mapping.csv` と `byte identical: True`（541685 バイト）。`csv.DictReader` → `597`。`git diff 82322fa --stat -- …/mapping.csv` → `1 file changed, 5 insertions(+), 5 deletions(-)`。`csv.DictReader` で新旧597行を全列比較した結果、差分セルは `[('current-0201','note'),('current-0309','note'),('current-0282','note'),('current-0296','note'),('current-0323','note')]` の5個のみで `disposition` を含む他の列は不変。**`mapping.csv` は直接編集せず、`_batch/*.csv` の該当5ファイルを直してから再生成した**（連結規則が `82322fa` の `mapping.csv` をバイト一致で再現することを、編集前に検証済み） | | |
| 7. `design.md` の `:147` に「8件」が無く、`:143` から「同じマーカーの配下には」で始まる一文が消えている。`:143` の「計11件」は残っている | OK | `sed -n '147,155p' design.md \| grep -c '8件'` → `0`。`grep -c '同じマーカーの配下には' design.md` → `0`。`awk 'NR==143' design.md \| grep -c '計11件'` → `1`（括弧内の `current-0201` の3件〜`current-0323` の1件の列挙も残存） | | |
| 8. `design.md:141`（採否基準の段落）が `82322fa` から1文字も変わっていない | OK | `awk 'NR==141' design.md \| md5sum` → `f1cd55908582c3c602f7d3f471c9714e`。`git show 82322fa:.rn/20260724-ntf-yaml-support/design.md \| sed -n '141p' \| md5sum` → 同値 | | |
| 9. §5 の検算（改行・行頭記号・連続空白を除いた文字列の完全一致）が通る | OK | `82322fa` の `:147` に §4-1 の置換のみを当てた文字列と、分割後のブロック（`:147`-`:155`）から `^- `・改行・連続空白を除いた文字列を比較 → `True`（正規化長 3401 で一致）。ブロックはリード文1行＋空行＋`- (1)`〜`- (5)` の5行＋空行＋末尾段落1行 | | |
| 10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK` | OK | `RESULT: OK` / `exit=0` | | |
| 11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors` | OK | `OK: no errors` / `exit=0` | | |
| 12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | `183 passed, 96 subtests passed in 0.60s` | | |
| 13. 既存イメージでのフルビルドで `grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` が 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`_build/` を削除する | OK | `docker run --rm -v …:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` → `exit=0` / `build succeeded.`。`grep -cE 'WARNING:\|ERROR:\|SEVERE:' <scratchpad>/build.log` → `0`。直後に `git -C … checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を絶対パスで実行。`_build/` は root 所有だったため `docker run … rm -rf /root/document/_build` で削除し、`ls -d _build` が `No such file or directory` であることを確認。`build.log` はスクラッチパッドに置き作業ツリーに残していない | | |
| 14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `git status --short` の変更は9ファイル（`design.md`／`_batch/batch-13,17,19,21,28.csv`／`mapping.csv`／`reviews/page-testdata_converter.md`／`reviews/page-testdata_notation.md`／`testdata_notation.rst`）のみ。`ja/conf.py`・`mapping/glossary.md`・`en/` 配下・`.gitignore` はいずれも未変更。`locales/ja/LC_MESSAGES/sphinx.mo` はビルド直後に `git checkout` で戻し `git status` に現れない。`mapping.csv` は `_batch/*.csv` からの再生成のみで直接編集していない（6 の連結バイト一致が証拠） | | |
| 15. 「取り除く」「落ちる」など無限定の断定文それぞれについて、主語を明示したうえで反例を検索し、自分の括弧書きや直後の列挙が反例になっていないかを確かめてから確定したことを `checks/task-35.md` に記録する | OK | 下記「## 無限定の断定文の反例検索」に5件記録 | | |

## Overall Verdict

- Self-check: NG（完了条件1・2 が未達。1 は指示書 §1 の停止条件に従った意図的な未実施、2 は 1 の未実施と `:249` の既存文により指示書の範囲内で満たせない）

## 無限定の断定文の反例検索

この作業で書いた断定文は5件。それぞれ主語を明示し、反例を検索してから確定した。

### 1. `testdata_notation.rst:1547`「カラム名の行の行末の空セルを取り除く」

- **主語** —— `Excel` 形式を読み込むときのテスティングフレームワーク（`nablarch-testing@e21bf67` の `HeaderLine` コンストラクタ）。**対象** —— テーブル系・`LIST_MAP` の**カラム名の行**の行末の空セル。
- **探した反例** —— (a) データ行の行末の空セルも同じく取り除かれるか。(b) テーブル系・`LIST_MAP` のうち片方だけ経路が違わないか。
- **検索と結果** —— (a) `git show e21bf67:src/main/java/nablarch/test/core/reader/HeaderLine.java` を全文読み、`:81` に `String val = (i >= line.size()) ? "" : line.get(i);` があることを確認。データ行は行が短ければ空文字で埋め戻されるため、**データ行については反例が成立する。** よって主語の対象を「カラム名の行」に限定した。裏付けとして `git show e977824:src/test/java/nablarch/test/tool/converter/xls/XlsFormatReaderInvalidInputTest.java \| sed -n '745,773p'` の `assertThat("足りないセルは空文字で埋められる", shortRow.getRows(), is(Arrays.asList(Arrays.asList("a1", ""))));`（`:765`-`:766`）を実測。(b) `TableDataParser.java:93` と `ListMapParser.java:64` がどちらも `new HeaderLine(...)` を呼ぶことを `git show` で確認。経路は同一で反例なし。
- **自分の括弧書きが反例になっていないか** —— 同じセルに書いた「（\ Excel\ 形式のみ）」が反例か。`e21bf67` の `src/main/` 配下の全 `.java` を `git show` して `implements TestDataReader` を探した結果、`PoiXlsReader.java:30` の1件のみ。`HeaderLine` の経路は `TestDataParsingTemplate` の行読み込みの上に載るため `Excel` 経路だけである。反例なし。

### 2. `testdata_notation.rst:1547`「カラム名が無い位置のセルは読み込まれない」

- **主語** —— データ行のセルのうち、カラム名の行より右にあるもの。
- **探した反例** —— (a) 行の途中（両隣にカラム名がある位置）の空セルも読み込まれないのではないか。(b) はみ出したセルが警告として残らないか。
- **検索と結果** —— (a) `HeaderLine.java:77` の `for (int i = 0; i < keys.size(); i++) {` はカラム名の行の長さでループするため、限定は「より右」であって「空セル一般」ではない。行の途中の空セルは読み込まれることを `git show e977824:src/test/java/nablarch/test/tool/converter/xls/XlsFormatReaderCellTypeTest.java \| sed -n '201,223p'` の `assertThat(table.getRows(), is(Arrays.<List<String>>asList(Arrays.asList("k", "", "z"))));`（`:222`）で実測。**この反例に当たらないよう「カラム名が無い位置」と限定してある。** (b) `XlsFormatReaderInvalidInputTest.java:770`-`:772` に `assertThat("カラム行よりも右のセル e1 は黙って捨てられる（issues.md XLS-12）", longRow.getRows(), is(Arrays.asList(Arrays.asList("c1", "d1")))); assertNoWarning(reading, "issues.md XLS-12");` を確認。警告も出ないため「読み込まれない」で正しい。
- **直後の列挙が反例になっていないか** —— 同じセルの前半「カラム名の行の行末の空セルを取り除く」と両立するか。前半はカラム名の行、後半はデータ行を主語にしており重ならない。反例なし。

### 3. `reviews/page-testdata_converter.md` (a)「5系統とも `Excel` 読み込み時に行末の空セルを取り除く」

- **主語** —— `XlsFormatReader.read`（`e977824` の `XlsFormatReader.java:101`-`:134`）が分岐する5系統それぞれの読み込み処理。
- **探した反例** —— 5系統のうち `trimTailCopy` を通らない経路。
- **検索と結果** —— 各系統の入口（`XlsFormatReader.java:146`・`:179`/`:182`・`:206`/`:212`・`:229`/`:240`・`:268`/`:274`）から `TestCoreReaderAdapter` → 本体パーサまで `git show` で辿り、テーブル系＝`TableDataParser.java:93`→`HeaderLine.java:33`、`LIST_MAP`＝`ListMapParser.java:64`→同、ファイル系＝`DataFileParser.java:68`、メッセージ＝`MessageParser.java:115`→`:44`/`:58`→`DataFileParser.java:68`、同期応答電文＝`SendSyncMessageParser.java:16`（`extends MessageParser`）→同、をそれぞれ確認。加えて変換ツールが原文復元に使う生行も `TestCoreReaderAdapter.java:464` の `bodyLines.add(NablarchTestUtils.trimTailCopy(line));` を通る。**反例なし（5系統とも通る）。**

### 4. `reviews/page-testdata_converter.md` (b)「データ行の行末の空セルは中間モデルへ入り直す」

- **主語** —— カラム名（フィールド名）がある位置にある、データ行の行末の空セル。
- **探した反例** —— (a) 中間モデルへ入らない系統があるか。(b) 3 の (a) と矛盾しないか。
- **検索と結果** —— (a) テーブル系・`LIST_MAP` は `HeaderLine.java:81`、ファイル系・メッセージ・同期応答電文は `XlsFormatReader.java:424` の `String cellValue = i < valueCells.size() ? valueCells.get(i) : "";` が埋め戻す。後者は `:298` `toRecordLayouts` 経由で `:215`・`:247`・`:278` の3系統が共有する1本の実装であるため系統差は無い。実測は `XlsFormatReaderCellTypeTest.java:182`-`:188`（テーブル系。中間モデルの値が `""`）と `XlsFormatReaderInvalidInputTest.java:811`-`:812`（`SETUP_FIXED`）。(b) 3 は「取り除く」（行の長さが縮む）、4 は「埋め戻す」（器のカラム数まで戻る）で、処理段階が違う。矛盾ではなく、**両方を書かないと「往復すると消える」という結論が誤りになる**という関係にある。
- **括弧書きが反例になっていないか** —— (b) の末尾で「往復して消えるのはカラム名の行の行末の空セルとカラム名が無い位置のセルに限られる」と限定を書いた。この限定自体が (a) の裏返しであり、両立する。

### 5. `mapping.csv` の5行の `note`「なお 9031fa6 も同じ基準でこの表から行を落としている」

- **主語** —— コミット `9031fa6`。**対象** —— 各行の `dest_page` の「主なクラスとリソース」の表。
- **探した反例** —— 5行のうち、その `dest_page` の表から `9031fa6` が1行も落としていない行があるか（あれば「この表から」が成り立たない）。
- **検索と結果** —— 5行の `dest_page` を `csv.DictReader` で実測すると `current-0201`＝ウェブアプリケーション、`current-0309`＝RESTfulウェブサービス、`current-0282`＝Nablarchバッチアプリケーション、`current-0296`・`current-0323`＝MOMによるメッセージング。`git show 9031fa6 -- …/request_unit_test/{web,rest,batch,mom}.rst` の差分に、`web.rst` から `* - ``HttpServer```、`rest.rst` から `* - ``HttpServer```、`batch.rst` から `* - ``StandaloneTestSupportTemplate``` と `* - ``TestShot```、`mom.rst` から `* - ``StandaloneTestSupportTemplate``` と `* - ``AbstractHttpRequestTestTemplate``` と `* - ``TestShot``` の削除行があることを確認。4ページすべてで1行以上落ちている。**反例なし。**
- **列挙が反例になっていないか** —— 旧文は行ごとにクラス名を列挙しており、`mom.rst` の表の出典が `current-0296`・`current-0323` の2行に分かれるため `StandaloneTestSupportTemplate` が二重に現れていた。新文は列挙をやめて `design.md` を指すだけにしたので、この二重計上は起きない。

## QA Expert Review
