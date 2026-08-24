# task-35 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `tools/testdata_converter.rst` の該当段落が §1 の変更後の文と一致する。`grep -rn 'メッセージのテストデータ' ja/` が0件 | OK | 是正1 §1 の差し替え文（`ntf-doc-35-fix1.md:27`）を `:71` へ置いた。`sed -n '71p' …/testdata_converter.rst` と `sed -n '27p' ntf-doc-35-fix1.md` を `diff` して差分なし（追補 §3 のとおり、この差し替え文は追補の影響を受けない。判定は `#35` 本体 §1 の「変更後」ではなく是正1 §1 の文で行った）。`grep -rn 'メッセージのテストデータ' ja/ \| wc -l` → `0` | OK | QA・設計・検証・クラフトの4観点が独立に逐語一致を再現（Python の `==` 比較で `True`、257文字）。`grep -rn 'メッセージのテストデータ' ja/` → 0件も4観点で再現 |
| 2. `tools/testdata_converter.rst` に「この整形」が無い（`grep -n 'この整形' …` が0件） | OK | `grep -n 'この整形' ja/development_tools/testing_framework/tools/testdata_converter.rst` → `:249` の1件のみ。`:71` には無い。**是正1 §3 の読み替え（「`:71` に『この整形』が無い」と読む）を適用した。**読み替えの内容と `:249` を対象外とする根拠は下記「## 完了条件2 の読み替え（Step 1c）」に記録した | OK | 4観点とも `grep -n 'この整形'` のヒットが `:249` の1件のみであることを再現 |
| 3. `reviews/page-testdata_converter.md` に、5系統すべてで行末の空セルが落ちることを実装から確かめた経路が記録されている | OK | `reviews/page-testdata_converter.md` を開いて確認。`:223`（テーブル系・`LIST_MAP` ＝ `nablarch-testing@e21bf67` の `HeaderLine.java:81`）・`:224`（ファイル系・メッセージ・同期応答電文 ＝ `nablarch-testing-converter@e977824` の `XlsFormatReader.java:424`）・`:228`（`XlsFormatReaderCellTypeTest.java:182`-`:188`）の3出典で、名前の行とデータ行で扱いが異なることが記録されている。3出典の逐語は自分で `git show <参照コミット>:<path>` を実行して現物と突き合わせた（`HeaderLine.java:81` `String val = (i >= line.size()) ? "" : line.get(i);`、`XlsFormatReader.java:424` `String cellValue = i < valueCells.size() ? valueCells.get(i) : "";`、`XlsFormatReaderCellTypeTest.java:182`-`:188` `readsAbsentCellAsEmptyString`）。5系統の走査経路の記録は `17b0254` で済み | OK | QA・設計・検証が3出典を参照コミットで開き逐語一致を確認。ただし同ファイルに是正1 の結果が反映されておらず、`:236`「`:71` は変更していない」・`:238`「現行の `:71` の文も同じ誤りを含む」が HEAD について偽（QA F3・クラフト S10・検証 指摘2）。条件の逐語要求は満たすが記録は要修正 |
| 4. `implementation/testdata_notation.rst` の `list-table` に §2 の行があり、既存の `:1544`-`:1545` が変わっていない。`reviews/page-testdata_notation.md` に出典がある | OK | `#35` 本体 §2 で足した「テーブル・\ ``LIST_MAP``」の行が `list-table` の `:1546`-`:1547` にある（追補 §2 に従い説明文は書き換え済み）。出典は `reviews/page-testdata_notation.md` §「`#35`（読み込み時の整形・補完の表に「テーブル・`LIST_MAP`」の行を追加、2026-08-21）」（`:553`-`:578`）にある。**「既存の `:1544`-`:1545` が変わっていない」の部分は追補 §2 が `:1544`-`:1547` の書き換えを明示的に指示したため上書きされている**（steering の注記のとおり、行の存在と出典の有無で判定した） | OK（条件文に矛盾） | 4観点とも行の存在と出典を確認。検証 指摘5・設計 F-7 が「既存の `:1544`-`:1545` が変わっていない」の句と 4a の両立不能を指摘。コーディネータが steering の条件4 から当該句を落とした |
| 4a. `implementation/testdata_notation.rst` の該当4行が是正1 追補 §2 の文面と一致している | OK | `sed -n '1544,1547p' …/testdata_notation.rst` と `sed -n '45,48p' ntf-doc-35-fix1-addendum.md` を `diff` して差分なし。置換は指示書の当該行を Python で直接読み出して流し込んでおり、手打ちしていない | OK | 4観点とも追補 §2 の4行と `:1544`-`:1547` の完全一致を独立に再現 |
| 4b. 同ファイル `:1545`（旧）の「\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込む」が消えており、`:883` との矛盾が解消していることを `reviews/page-testdata_notation.md` の `## #35-是正1` 節に追記している。あわせて、機構B の補完側を表に書かなかった理由（`:658`・`:883` に既出）も1〜2文で記録している | OK | `reviews/page-testdata_notation.md` の `## #35-是正1` 節（`:583` 開始）の末尾に `### 追補（ntf-doc-35-fix1-addendum.md §2）に従って表の2行を書き換えた記録` を追記（既存の記述は削っていない）。`grep -n 'の各要素をそのまま読み込む' …/testdata_notation.rst` → 0件。`:883` との矛盾が解消したこと、および機構B の補完側を表に書かなかった理由（`:658`・`:883` に既出のため3つ目の言い方を足さない）を記載した | OK | 4観点とも `grep` 0件と `## #35-是正1` 節の追記を確認。ただし同ファイルの旧記述（`:555`・`:585`・`:644`・`:648`・`:654`）と申し送り38 が stale（検証 指摘3・設計 F-8） |
| 4c. `implementation/testdata_notation.rst:883` の既存記述（可変長ファイルの `""` 補完）と、新しく書いた記述が食い違っていないことを確認した記録がある | OK | 同追記の末尾段落に記録。`:883` を実際に開いて読み（「データ行のセル数（Excel形式）または ``rows:`` の各要素の長さ（YAML形式）がフィールド数より少ない場合、不足したフィールドは\ ``""``\ として補完される」）、(1) `:883` は行が短いときの補完、新しい2行は名前が宣言されていない値（行が名前より長い側）を述べており対象が重ならない、(2) 新しい2行の「（\ Excel\ 形式のみ）」は「名前の行の行末の空セルを取り除く」の句にだけ掛かり、両形式で起きる補完の側には掛けていない、の2点で食い違わないことを確認した。`:658` とも同じ理由で両立する | OK | QA・設計・検証が `:883`・`:658` を独立に開き、対象が重ならないことを再現 |
| 5. `mapping.csv` の `note` に「なお同じ基準で 9031fa6 が」が0件、「なお 9031fa6 も同じ基準で」が5件 | OK | `grep -o 'なお同じ基準で 9031fa6 が' mapping/mapping.csv \| wc -l` → `0`。`grep -o 'なお 9031fa6 も同じ基準で' mapping/mapping.csv \| wc -l` → `5`（`17b0254` の成果物を再検証。本ラウンドでは変更していない） | OK | 4観点とも `grep -c` で 0件／5件を再現 |
| 6. `_batch/*.csv` を昇順連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、`csv.DictReader` が597行。`82322fa` との差分が指定5行の `note` のみであることを `git diff` で全行確認する | OK | `sorted(glob('mapping/_batch/*.csv'))` 30ファイルをバイナリ連結（2つ目以降は先頭 `\n` まで除去）→ `mapping/mapping.csv` と `byte identical: True`、**541572 バイト**。`csv.DictReader` → `597` 行。`git diff 82322fa --stat -- …/mapping/mapping.csv` → `1 file changed, 5 insertions(+), 5 deletions(-)`。`82322fa` 版と現行版を `csv.DictReader` で597行×全列比較 → 差分セルは `[(current-0201,note),(current-0309,note),(current-0282,note),(current-0296,note),(current-0323,note)]` の5個のみ。**なお `17b0254` 時点の記録にあった「541685 バイト」は `82322fa` 版のサイズで、現行版は 541572 バイトである**（`git show 82322fa:…/mapping.csv \| wc -c` → `541685`、`git show 17b0254:…/mapping.csv \| wc -c` → `541572` を実行して確認） | OK | QA・設計・検証が独立に `_batch/*.csv` 30本を昇順連結し md5 一致（`feb443882ea2eead66881497a8c8a294`、541572バイト）、597行、差分は指定5セルのみを再現 |
| 7. `design.md` の `:147` に「8件」が無く、`:143` から「同じマーカーの配下には」で始まる一文が消えている。`:143` の「計11件」は残っている | OK | `sed -n '147,155p' design.md \| grep -c '8件'` → `0`。`grep -c '同じマーカーの配下には' design.md` → `0`。`awk 'NR==143' design.md \| grep -c '計11件'` → `1` | OK | 4観点とも再現。設計は台帳側の実数 3+3+3+1+1=11 が「計11件」と一致することも確認 |
| 8. `design.md:141`（採否基準の段落）が `82322fa` から1文字も変わっていない | OK | `awk 'NR==141' design.md \| md5sum` → `f1cd55908582c3c602f7d3f471c9714e`。`git show 82322fa:.rn/20260724-ntf-yaml-support/design.md \| sed -n '141p' \| md5sum` → 同値 | OK | QA・設計・検証が md5 `f1cd55908582c3c602f7d3f471c9714e` の一致を独立に再現 |
| 9. §5 の検算（改行・行頭記号・連続空白を除いた文字列の完全一致）が通る | OK | `82322fa` の `:147`（1行）と現行の `:147`-`:155`（分割後ブロック）から行頭 `- `・改行を除き連続空白を1つに畳んで比較。共通接頭辞 429 文字・共通接尾辞 2940 文字で、**差分は1箇所の連続領域のみ**（旧「「なお同じ基準で…落としている」の一文だけを数えると、この7行の名前は8件現れる（…）。7行に対して1件多いのは、…書かれてい」→ 新「のは `current-0201`…の5行で、クラス名は列挙せず本節を指すだけにした。行ごとに列挙しないのは、…二重に数えられ」）。これは §4-1 の置換そのものであり、`(1)`〜`(5)` の5項目と末尾段落を含む残り全体は正規化後に完全一致した。すなわち §5 の分割は文言を1文字も変えていない | OK | QA・設計・検証が独立の正規化スクリプトで検算。共通接頭429字・共通接尾2940字で、差分は §4-1 の置換区間のみ |
| 10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK` | OK | `python3 mapping/tools/verify_glossary.py`（`.rn/20260724-ntf-yaml-support/` で実行）→ `RESULT: OK` | OK | コーディネータおよび QA・設計・検証が再実行 → `RESULT: OK` |
| 11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors` | OK | `python3 mapping/tools/verify_mapping.py` → `OK: no errors` | OK | コーディネータおよび QA・設計・検証が再実行 → `OK: no errors` |
| 12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | `python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 0.67s` | OK | コーディネータおよび QA・設計・検証が再実行 → `183 passed, 96 subtests passed` |
| 13. 既存イメージでのフルビルドで `grep -cE 'WARNING:\ | OK | `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` → `exit=0` / `build succeeded.`。`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。直後に `git -C /home/tie303177/work/nablarch/nablarch-document checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`_build/` は root 所有のため `docker run … rm -rf /root/document/_build` で削除し、`ls -d _build` が `No such file or directory` であることを確認。`build.log` はスクラッチパッドに置き作業ツリーに残していない（`ls build.log` も `No such file or directory`）。`docker build` は行っていない（既存イメージ `nablarch-document-build:latest` を使用） | OK | コーディネータが既存イメージで独立に再実行 → `build succeeded.`、`grep -cE 'WARNING:|ERROR:|SEVERE:'` → 0。直後に `sphinx.mo` を `git checkout --` で復元し、`_build/` をコンテナ経由で削除 |
| 14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `git status --short` の変更は3ファイル（`reviews/page-testdata_notation.md`／`ja/…/implementation/testdata_notation.rst`／`ja/…/tools/testdata_converter.rst`）のみ。`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/` 配下・`locales/`・`.gitignore`・`design.md`・`steering.md` はいずれも未変更。`locales/ja/LC_MESSAGES/sphinx.mo` はビルド直後に `git checkout --` で戻し `git status` に現れない | OK | 4観点とも `git diff --name-only 82322fa..HEAD` に禁止対象が無いことを再現 |
| 15. 「取り除く」「落ちる」など無限定の断定文それぞれについて、主語を明示したうえで反例を検索し、自分の括弧書きや直後の列挙が反例になっていないかを確かめてから確定したことを `checks/task-35.md` に記録する | OK | 下記「## 無限定の断定文の反例検索（本ラウンド）」に、本ラウンドで書いた8つの断定について主語・探した反例・検索と結果・自分の括弧書き／直後の列挙が反例になっていないかの確認を記録した | NG | **記録はあるが、反例が実在する。** (a) `TestDataParsingTemplate.java:176`-`:177` `if (isBlankLine(line)) { continue; }`（`isBlankLine` は同 `:316`-`:317` `StringUtil.isNullOrEmpty(line)`）により、全セルが空のデータ行は5系統すべてで読み飛ばされる。`:71`「往復しても残る」の反例（QA F2。コーディネータが `nablarch-testing@e21bf67` で確認）。(b) `nablarch-testing-converter@e977824` `XlsFormatReader.java:566` `dropEmptyEntries` がテーブル・`LIST_MAP` の全空データ行を落とす（検証 指摘1）。自己チェック 3 は `null` 経路のみを探し、空エントリ経路を探していない |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 検証のやり方が目的に対して意味を持っているか | NG | 完了条件1〜9 は逐語一致・バイト一致・セル単位比較で判定でき、4観点とも再現できた。しかし条件3・4 は「出典が記録されているか」を問うだけで、**記録された出典が正しい層のものか**を担保しない。是正1 §2 が根拠に挙げた `XlsFormatReader.java:422`-`:426` は変換ツール側のデータ行の幅揃えで、`nablarch-testing` 側の trim 範囲とは別機構である。この隙間から `:1545` の narrowing が入った。条件15 も記録の有無に落ちており反例の実在を担保しない |

## Expert Reviews

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 構成・アプローチの適合 | NG | **F-1（must）** 新 `:1547` 第1句「カラム名の行の行末の空セルを取り除く」と同じ事実が同ページ `:774`（「ヘッダ行（2行目）は、末尾に空セルが続いても、そこで記述を止めたのと同じ結果になる」＋実例表）に既出。追補 §2 修正1 の「3つ目の言い方を足さない」を機構A にも当てると走査漏れ。機構B も `:658`・`:787` で既に二重。**F-4（should）** `対象` 列が ファイル・メッセージ → テーブル・`LIST_MAP` → メッセージ → テーブル → テーブル となり、メッセージ行が離れテーブル行が分断された |
| 系全体の整合性 | NG | **F-2（must）** `:71` 第3・4文が形式非依存に読め、`YAML` 形式で成り立たない。`YamlTableDataBuilder.java:198`-`:200` ＋ `YamlSection` の変換により、宣言済みカラムを持たない行の値は `null`。参照先の `:658`「\ ``YAML``\ 形式では……\ ``null``\ を明示的に指定したのと同じ扱いになる」と食い違う（コーディネータが両方を開いて確認）。「名前がある位置」「名前より右にあるセル」は追補 §2 修正2 が表で禁じた位置の語。**F-5（should）** `:71` の `:ref:` がページ先頭ラベルを指し、詳細（`:658`・`:883`・`:1544`-`:1547`）に届かない。同ページ `:63`・`:108` は節ラベルを指しており作法とも不一致。**F-6（should）** 台帳 `input-0172`（この `list-table` を担う唯一の行）の `note` が「4件の整形・補完仕様表」のままで、5行になった `#35` のポインタが無い。**F-8（note）** `reviews/page-testdata_notation.md:595`・`:642` が `.rn/` 内文書を行番号で指しており規約違反 |

### Craft Expert（執筆）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 日本語テクニカルライティングの作法 | NG | **S1/S2（中〜高）** `:1545` の「フィールド名称の行の」は実装より狭い。`nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/DataFileParser.java:68` の `trimTailCopy` が `switch (status)` の前にあり、`READING_DIRECTIVES_AND_NAMES`・`READING_TYPES`・`READING_LENGTHS`・`READING_VALUES` の全行に掛かる（コーディネータが確認）。旧文（無限定）が持っていたカバーを失った。**S5（低〜中）** 同じ表の下2行は既出を「（前述）」で示すが、新2行は `:774`・`:819` に既出でありながら付いていない。**S7・S8・S9（低）** 主語の受動／「空セル」と「空のセル」の混在／位置の語の基準不一致 |
| 既存の声・用語との一貫性 | NG | **S3（中）** `mapping/glossary.md:269` の正表記は「フィールド名称行」。既存 `.rst` 4箇所（`testdata_notation.rst:1267`・`:1269`・`:1271`、`testdata_examples.rst:1646`）はすべてこれに従うが、新規2箇所だけが「フィールド名称の行」（コーディネータが `grep` で確認）。`verify_glossary.py` は用語表自体の整合しか見ないため素通りする。**S4（中）** `testdata_converter.rst` で「メッセージ」を使うのは `:71` のみで、隣の `:73` と参照先 `testdata_notation.rst:1166` は同じものを「電文」と呼ぶ。**S6（低）** 表の `対象` 列で新行が「テーブル・`LIST_MAP`」と明示したことで、下の `:1550`「テーブル」が狭すぎることが目立つ |

### Verification Expert（ファクトチェック）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 主張が出典で検証されているか | NG（7件中1件が偽） | `:1545`・`:1547`・`:71` の主張を7件に分解して参照コミットで判定。真6件・偽1件。偽は「データ行は名前の行の幅に揃えられるため、名前がある位置の空のセルは空文字として中間モデルに入り、往復しても残る」で、`nablarch-testing-converter@e977824` `XlsFormatReader.java:566` `dropEmptyEntries`（呼び出しは同 `:162` テーブル系・`:193` `LIST_MAP`。ファイル系・メッセージ・同期応答電文には掛からない）が全空データ行を落とす。テストで固定済み（`XlsFormatReaderRealFileTest.java:384`-`:385`）。変換ツールページには空エントリの記述が1件も無い |
| 出典の網羅と実在 | OK（実在）／NG（記録の陳腐化） | `reviews/` 2ファイルに書かれた `file:line` と逐語を1件ずつ参照コミットで照合し、**不一致0件**（`nablarch-testing` 24件・`nablarch-testing-converter` 22件・`nablarch-testing-yaml` 11件）。一方、記録の断定が HEAD について偽なものが4か所（`page-testdata_converter.md:236`・`:238`、`page-testdata_notation.md:585`・`:644` ほか）。申し送り38「「無い」2件」は追補 §2 で前提が消え、実測1件 |

## Overall Verdict

- Self-check: OK（完了条件1〜15。是正1 §1 の差し替え文と追補 §2 の4行をいずれも逐語一致で反映し、検証コマンド全4種が通った）
- QA: NG（完了条件15。`:71`「往復しても残る」に反例が実在する）
- Design expert: NG（must 2件。`:1547` 第1句が同ページ `:774` に既出／`:71` 第3・4文が `YAML` 形式で成り立たず `:658` と食い違う）
- Craft expert: NG（`:1545` の限定が実装より狭い／用語が `glossary.md` の正表記「フィールド名称行」から外れる）
- Verification expert: NG（`:71` の主張7件中1件が偽。出典の `file:line` と逐語の不一致は0件）
- Ready to check off: No（NG の実体はいずれも user が逐語指定した文面そのものにあり、コーディネータの判断で書き換えられない。是正1 追補に続くラウンドとして user へエスカレーションした）

## 完了条件2 の読み替え（Step 1c）

完了条件2 を「`tools/testdata_converter.rst:71` に『この整形』が無い」と読み替えた。是正1 指示書 `ntf-doc-35-fix1.md` §3 が「`:249` の「この整形」は書き出し設定の既存文で、`#32` で確定した記述である。`#35` の対象外」と定めているためである。

実測は次のとおり。`grep -n 'この整形' ja/development_tools/testing_framework/tools/testdata_converter.rst` の唯一のヒットは `:249` で、逐語は「\ Excel\ 形式へ書き出す場合は、人が見て編集することを前提に、行の種別ごとの装飾やレイアウトを付けて読みやすく整える。この整形は設定で変更でき、設定しなかった項目にはデフォルト値が適用される。」である。この文は `:247` から続く書き出し設定の説明であり、`:71` の読み込み時の話とは対象が違う。`:71` は是正1 §1 の差し替え文に置き換えたため「この整形」を含まない。

## Method を適用した記録（どの主張をどの出典に当たって確認したか）

逐語の流し込みは、指示書の当該行を Python で読み出してそのまま書き込み、書き込み後に `diff` で機械的に検算した（完了条件1・4a の Evidence）。実装の主張はすべて参照コミット固定で `git show <commit>:<path>` を実行し、自分で現物を開いて確かめた。

| 主張 | 当たった出典（自分で `git show` して確認） | 逐語 |
|---|---|---|
| 名前の行の行末の空セルは `Excel` 読み込み時に取り除かれる（テーブル・`LIST_MAP`） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/HeaderLine.java:33` | `List<String> keys = trimTailCopy(headerLine);   // キャッシュを破壊しないようにコピーして編集` |
| 同（ファイル・メッセージ・同期応答電文） | 同 `src/main/java/nablarch/test/core/reader/DataFileParser.java:68`（メッセージは `MessageParser.java:44`・`:58`・`:115` の委譲、同期応答電文は `SendSyncMessageParser.java:16` の継承で到達。`FixedLengthFileParser.java:15` が `DataFileParser` を継承） | `List<String> line = NablarchTestUtils.trimTailCopy(original); // キャッシュを破壊しないようにコピーして編集`（`onReadLine` の冒頭。名前行・型行・長さ行・データ行のすべてを通る） |
| 変換ツール側でも同じ | `nablarch-testing-converter@e977824` `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:464` | `bodyLines.add(NablarchTestUtils.trimTailCopy(line));` |
| データ行は名前の行の幅へ揃えられる（テーブル・`LIST_MAP`、`Excel`） | `nablarch-testing@e21bf67` `HeaderLine.java:77`・`:81` | `for (int i = 0; i < keys.size(); i++) {` / `String val = (i >= line.size()) ? "" : line.get(i);` |
| 同（ファイル・メッセージ、`Excel`・YAML 共通） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/file/DataFileFragment.java:102`・`:105`・`:107`、`:169`・`:173`・`:175` | `public void addValue(List<String> line) {` / `for (int i = 0; i < names.size(); i++) {` / `String value = i < line.size() ? line.get(i) : "";`（`addValueWithId` も同形） |
| 同（変換ツールの `Excel` 読み込み） | `nablarch-testing-converter@e977824` `XlsFormatReader.java:423`・`:424` | `List<String> row = new ArrayList<>(names.size());` / `String cellValue = i < valueCells.size() ? valueCells.get(i) : "";` |
| 同（YAML のテーブル・`LIST_MAP`） | `nablarch-testing-yaml@190cc9a` `src/main/java/nablarch/test/core/reader/yaml/YamlTableDataBuilder.java:198`-`:200` | `List<String> rowValues = new ArrayList<String>(columnNames.size());` / `for (String col : columnNames) {` / `rowValues.add(objectToString(rowMap.get(col)));` |
| YAML のカラム名は先頭行のキーから決まる（＝名前の行に「行末の空セル」が存在しない） | `nablarch-testing-yaml@190cc9a` `src/main/java/nablarch/test/core/reader/yaml/YamlSection.java:156`・`:160` | `public static List<String> resolveColumns(List<Object> rows) {` / `return new ArrayList<String>(castMap(rows.get(0)).keySet());` |
| YAML のフィールド名称は `fields:` の `name` から決まる（同上） | `nablarch-testing-yaml@190cc9a` `src/main/java/nablarch/test/core/reader/yaml/YamlFileBuilder.java:193` | `names.add(toStr(field.get(FIELD_NAME)));` |
| YAML のファイル・メッセージも `DataFileFragment` の幅揃えを通る | 同 `YamlFileBuilder.java:233`・`:235` | `fragment.addValueWithId(rowValues, String.valueOf(rowNo));` / `fragment.addValue(rowValues);` |
| `testdata_notation.rst:658`・`:883` の既存記述と食い違わない | `ja/development_tools/testing_framework/implementation/testdata_notation.rst:658`・`:883`（現物を開いて読んだ） | `:658`「\ ``Excel``\ 形式では、データ行のセル数がヘッダ行のカラム数より少ない場合、記述しなかったカラムには空文字が設定されたものとして扱われる。」／`:883`「データ行のセル数（Excel形式）または ``rows:`` の各要素の長さ（YAML形式）がフィールド数より少ない場合、不足したフィールドは\ ``""``\ として補完される。」 |

## 無限定の断定文の反例検索（本ラウンド）

本ラウンドで確定した断定は8つ（`tools/testdata_converter.rst:71` に4つ、`implementation/testdata_notation.rst:1544`-`:1547` に4つ）。それぞれ主語を明示し、反例を検索してから確定した。逐語はいずれも指示書で確定済みだが、**「書けるかどうか」を自分で確かめたうえで置いた。**

### 1. `testdata_converter.rst:71`「名前の行……の行末の空セルは、\ Excel\ 形式から読み込む時点で取り除かれるため、往復すると消える」

- **主語** —— `Excel` 形式を読み込む側（テスティングフレームワークの `HeaderLine`／`DataFileParser`、および変換ツールの `TestCoreReaderAdapter`）。**対象** —— 名前の行の行末の空セル。
- **探した反例** —— (a) 5系統のうち名前の行が `trimTailCopy` を通らない経路。(b) 変換ツールの経路だけ違う可能性。
- **検索と結果** —— (a) `git grep -n 'trimTailCopy' e21bf67 -- src/main/java` を実行。ヒットは定義（`NablarchTestUtils.java:273`）と呼び出し2件（`DataFileParser.java:68`・`HeaderLine.java:33`）で全件。`HeaderLine` はテーブル系（`TableDataParser.java:93` `header = new HeaderLine(readLine());`）と `LIST_MAP`（`ListMapParser.java:64` `header = new HeaderLine(firstLine);`）が通る。`DataFileParser.onReadLine` はファイル系が直接、メッセージは `MessageParser.java:44`（`delegate = createFixedLengthFileParser(reader, interpreters, targetType);`）・`:58`（`return new FixedLengthFileParser(reader, interpreters, targetType) {`）・`:115`（`delegate.onReadLine(line);`）の委譲で、同期応答電文は `SendSyncMessageParser.java:16` `public class SendSyncMessageParser extends MessageParser {` を介して通る（`FixedLengthFileParser.java:15` `public class FixedLengthFileParser extends DataFileParser<FixedLengthFile> {`）。**`MessageParser` 自身は `DataFileParser` のサブクラスではなく `SingleDataParsingTemplate` を継承しているため、継承ではなく委譲で辿った。**5系統とも通り、**反例なし。** (b) 変換ツールは `TestCoreReaderAdapter.java:464` で収集する全ボディ行に `trimTailCopy` を掛けており、こちらも通る。
- **自分の括弧書きが反例になっていないか** —— 同じ文の括弧書き「（テーブルと\ ``LIST_MAP``\ ではカラム名の行、ファイルとメッセージではフィールド名称の行）」が5系統を覆うか。同期応答電文は `SendSyncMessageParser extends MessageParser` で「メッセージ」に含まれる。覆えており反例にならない。

### 2. `testdata_converter.rst:71`「データ行は名前の行の幅に揃えられる」

- **主語** —— 読み込み処理が組み立てるデータ行。**対象** —— 全系統。
- **探した反例** —— 幅を揃えない系統。
- **検索と結果** —— テーブル・`LIST_MAP`＝`HeaderLine.java:77`・`:81`、ファイル・メッセージ＝`DataFileFragment.java:105`・`:107`（`addValue`）と `:173`・`:175`（`addValueWithId`）、変換ツールの `Excel` 読み込み＝`XlsFormatReader.java:423`・`:424`。いずれも名前の数でループする。**反例なし。**
- **括弧書き・直後の記述が反例になっていないか** —— 直後の「名前がある位置の空のセルは空文字として中間モデルに入り」と「名前より右にあるセルは読み込まれない」は、この幅揃えの2つの帰結（不足側の埋めと超過側の切り捨て）であり、反例ではなく内訳である。

### 3. `testdata_converter.rst:71`「名前がある位置の空のセルは空文字として中間モデルに入り、往復しても残る」

- **主語** —— `Excel` 形式のデータ行のうち、名前がある位置にある空のセル。
- **探した反例** —— (a) 空文字ではなく `null` になる経路。(b) 中間モデルに入らない経路。
- **検索と結果** —— (a) 主語を `Excel` 形式に限っているため、`YAML` 形式で `null` になる経路（`YamlTableDataBuilder.java:200` の `rowMap.get(col)` が欠けたキーで `null` を返す。`testdata_notation.rst:658` が「\ ``YAML``\ 形式では……\ ``null``\ を明示的に指定したのと同じ扱いになる」と書いている）は反例に当たらない。**ただしこの `null` は、往復の途中で `YAML` から読み戻す局面に効きうるので、変換ツールの書き出し側を確かめた。** `nablarch-testing-converter@e977824` の `src/main/java/nablarch/test/tool/converter/yaml/YamlFormatWriter.java:268`-`:269` は `for (int i = 0; i < columns.size(); i++) { item.prop(columns.get(i), i < row.size() ? row.get(i) : null); }` で、全カラムを全行に書き出す。キーが欠けた `YAML` は変換ツールからは出ないため、この経路は往復では現れず反例にならない。(b) `nablarch-testing-converter@e977824` の `XlsFormatReaderCellTypeTest.java:182`-`:188` `readsAbsentCellAsEmptyString` を `git show` で開き、データ行の `V` 列のセルが不在の実 `.xlsx` を読んだとき中間モデルの値が `""` になること、および同 `:187` `assertThat(row.getLastCellNum(), is((short) 1));` を確認。**反例なし。**

### 4. `testdata_converter.rst:71`「名前より右にあるセルは読み込まれないため消える」

- **主語** —— データ行のセルのうち、名前の行の幅より右にあるもの。
- **探した反例** —— (a) 例外・警告になって「読み込まれない」で済まない経路。(b) 行の途中の空セルまで巻き込む読み方をされないか。
- **検索と結果** —— (a) `DataFileParser.onReadingValues`（同 `:182`-`:190`）を全文読み、データ行の要素数を検査する分岐が無いことを確認した（`currentFragment.addValue(tail(line));` を呼ぶだけ）。切り捨ては `DataFileFragment.java:105` のループ長で黙って起きる。テーブル系も `nablarch-testing-converter@e977824` の `XlsFormatReaderInvalidInputTest.java:770`-`:772` に `assertThat("カラム行よりも右のセル e1 は黙って捨てられる（issues.md XLS-12）", longRow.getRows(), is(Arrays.asList(Arrays.asList("c1", "d1")))); assertNoWarning(reading, "issues.md XLS-12");` があることを `git show` で確認。**反例なし。** (b) 「名前より右にある」と位置で限定してあり、行の途中の空セルは 3 の埋め戻しで残る。両立する。
- **直後の列挙が反例になっていないか** —— 直前の 3 と主語の範囲が「名前がある位置」／「名前より右」で排他になっている。反例なし。

### 5. `testdata_notation.rst:1545`「フィールド名称の行の行末の空セルを取り除く（\ Excel\ 形式のみ）」

- **主語** —— `Excel` 形式を読み込むテスティングフレームワーク（`DataFileParser.onReadLine`）。**対象** —— ファイル・メッセージのフィールド名称の行の行末の空セル。
- **探した反例** —— `YAML` 形式にも同じ処理があるか（あれば「`Excel` 形式のみ」が誤り）。
- **検索と結果** —— `nablarch-testing-yaml@190cc9a` の `YamlFileBuilder.java:193` `names.add(toStr(field.get(FIELD_NAME)));` を確認。フィールド名称は `fields:` の各要素の `name` から作られ、位置で並べる「行」ではないため行末の空セルという概念が生じない。**反例なし。** なお同ページ `:573` が根拠にしていた「`nablarch-testing` の `src/main/` に `TestDataReader` の実装が `PoiXlsReader` の1件しか無い」という走査は `nablarch-testing-yaml` を見ておらず不十分だったので、今回は `nablarch-testing-yaml` 側の実装を直接読んで判定した（この訂正は `reviews/page-testdata_notation.md` §「ラウンド`#35`（`17b0254`）の記録の訂正」に既にある）。
- **同じセルの後半が反例になっていないか** —— 後半「フィールド名称が宣言されていない値は読み込まない」は両形式に当たる（`DataFileFragment.java:105` を `Excel`・`YAML` の両経路が共有する）。**「（\ Excel\ 形式のみ）」を前半の句にだけ掛け、後半に掛けていない**ため、後半は反例にならない。掛け方が逆だったら誤りになる箇所である。

### 6. `testdata_notation.rst:1545`「フィールド名称が宣言されていない値は読み込まない」

- **主語** —— ファイル・メッセージのデータ行の値のうち、フィールド名称が宣言されていないもの。**対象** —— `Excel`・`YAML` の両形式。
- **探した反例** —— (a) エラーになる経路。(b) `YAML` 形式で読み込まれてしまう経路。
- **検索と結果** —— (a) 4 の (a) と同じく `DataFileParser.onReadingValues` に要素数の検査が無いことを確認。同ページ `:891` の列挙にある「データ要素数が不正である」は、`:889` の「フィールド名称・データ型・フィールド長リストのサイズが一致していない」・`:890` の「存在しないフィールド名称を指定している」と並ぶ定義側のエラーの列挙にあり、データ行が長い場合を指すものではない（`onReadingValues` に検査が無いことが根拠）。(b) `YamlFileBuilder.java:227`-`:235` は `rowList.size()` ぶんの値を作って `fragment.addValue(rowValues)` に渡すだけで、切り捨ては受け側の `DataFileFragment.java:105` の `names.size()` ループで起きる。**両形式とも読み込まれない。反例なし。**
- **「位置」と書かなかった理由** —— 追補 §2 修正2 のとおり、`YAML` 形式は位置ではなくキー／`name` で対応するため「位置」は使えない。「宣言されていない」なら両形式に当たる。

### 7. `testdata_notation.rst:1547`「カラム名の行の行末の空セルを取り除く（\ Excel\ 形式のみ）」

- **主語** —— `Excel` 形式を読み込むテスティングフレームワーク（`HeaderLine` コンストラクタ）。**対象** —— テーブル・`LIST_MAP` のカラム名の行の行末の空セル。
- **探した反例** —— (a) データ行も同じく取り除かれたままか。(b) `YAML` 形式にも同じ処理があるか。(c) テーブル系と `LIST_MAP` で経路が違わないか。
- **検索と結果** —— (a) `HeaderLine.java:81` の `String val = (i >= line.size()) ? "" : line.get(i);` により、データ行は短ければ空文字で埋め戻される。**データ行については反例が成立するため、主語を「カラム名の行」に限定してある。** (b) `YamlSection.java:156`・`:160` の `resolveColumns` はカラム名を先頭行の `keySet()` から作る。行末の空セルという概念が無く、**反例なし。** (c) `TableDataParser.java:93` と `ListMapParser.java:64` がどちらも `new HeaderLine(...)` を呼ぶことを `git show` で確認。経路は同一。
- **同じセルの後半が反例になっていないか** —— 5 と同じ構造で、「（\ Excel\ 形式のみ）」は前半の句にだけ掛けてある。後半は両形式に当たるので、掛けていないことが正しい。

### 8. `testdata_notation.rst:1547`「カラム名が宣言されていない値は読み込まない」

- **主語** —— テーブル・`LIST_MAP` のデータ行の値のうち、カラム名が宣言されていないもの。**対象** —— `Excel`・`YAML` の両形式。
- **探した反例** —— (a) 行の途中（両隣にカラム名がある位置）の空セルまで落ちないか。(b) `YAML` 形式で2行目以降が持つ余分なキーが読まれないか。(c) エラー・警告になる経路。
- **検索と結果** —— (a) `HeaderLine.java:77` の `for (int i = 0; i < keys.size(); i++) {` はカラム名の数でループするため、落ちるのは「カラム名が宣言されていない」ぶんだけである。行の途中の空セルが読み込まれることは `nablarch-testing-converter@e977824` の `XlsFormatReaderCellTypeTest.java:222` `assertThat(table.getRows(), is(Arrays.<List<String>>asList(Arrays.asList("k", "", "z"))));` で確認。**この反例に当たらないよう「宣言されていない」と限定してある。** (b) `YamlTableDataBuilder.java:199`-`:200` は `columnNames` を回して `rowMap.get(col)` を引くので、`columnNames`（＝先頭行のキー）に無いキーは読まれない。**反例なし。** (c) `XlsFormatReaderInvalidInputTest.java:770`-`:772` の `assertNoWarning(reading, "issues.md XLS-12");` により警告も出ない。
- **直後の列挙が反例になっていないか** —— 同じセルの前半（カラム名の行が主語）と後半（データ行の値が主語）は主語が重ならない。また表の1つ上の「ファイル・メッセージ」の行と同じ粒度・同じ構文にしてあり、2行が同じことを別の言い方で述べる状態にはなっていない（追補 §2 の趣旨）。

## QA Expert Review

## #35-是正2

### Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `tools/testdata_converter.rst:71` が §1 の1段落と逐語一致し、旧第1・3・4文が消えている | OK | 指示書 `ntf-doc-35-fix2.md` の20行目を Python で読み出してそのまま `:71` へ流し込み（手打ちしていない）、書き込み後に `c[70] == inst[19]` を評価 → `True`（175文字）。旧文の消滅は `grep -c` で確認 —— 「行末の空セルの扱いは、名前の行とデータ行で異なる」→ `0`、「名前がある位置の空のセルは空文字として中間モデルに入り」→ `0`、「名前より右にあるセルは読み込まれないため消える」→ `0`。段落は1行（途中改行なし） | OK | コーディネータが独立に検算。指示書のコードブロックを機械抽出し `conv[70]==b1[0]` → `True`。旧第1文「行末の空セルの扱いは、名前の行とデータ行で異なる」の残存を `grep` → 0件。差分ハンクは `@@ -71 +71 @@` の1行のみ（範囲統制レビューも同結果）。事実検証レビューが5系統すべてで反例を探し、0件だった（`HeaderLine.java:33`／`TableDataParser.java:93`／`ListMapParser.java:64`／`DataFileParser.java:68`・`:251`／`MessageParser.java:115`、変換ツール側は `TestCoreReaderAdapter.java:128`・`:464`） |
| 2. `implementation/testdata_notation.rst` の該当4行が §2 の文面と逐語一致している | OK | 指示書の33〜36行目を Python で読み出して `:1544`-`:1547` へ流し込み、`n[1543:1547] == inst[32:36]` を評価 → `True`。インデントは既存 `list-table` と同じ（`  * - ` / `    - `） | NG | 逐語一致そのものは検算済み（`nota[1543:1547]==b2` → `True`、差分ハンクは `@@ -1545 +1545 @@`・`@@ -1547 +1547 @@` の2行のみ）。**ただし逐語指定文そのものに反例が1件。** 「ファイル・メッセージ」の行を無限定に戻すと、データ行について同ページ `:883` と食い違う。`DataFileParser.java:68` の `trimTailCopy` が4分岐すべてに掛かるのは事実だが、データ行の分岐（`:79`→`:186` `currentFragment.addValue(tail(line));`）の直後に `DataFileFragment.java:105`-`:107` `String value = i < line.size() ? line.get(i) : "";` が名称の数まで `""` を埋め戻すため、データ行ではトリムの観測できる効果がゼロ。上流の実 `.xlsx` テスト `nablarch-testing-converter@e977824` の `XlsFormatReaderInvalidInputTest.java:811`-`:812`「足りないセルは空文字で埋められる」が固定（`f1`・`f2` にデータ行 `abc` のみ → `["abc", ""]`）。トリムに観測できる効果があるのはフィールド名称行・データ型行・フィールド長行の3つのみ（型行・長さ行は `DataFileFragment.java:203`・`:287` の `assertSameSizeAsNames` があるため）。**user 判断待ち。** |
| 3. `implementation/testdata_notation.rst` 内に「フィールド名称の行」が1件も残っていない | OK | `grep -c 'フィールド名称の行' ja/development_tools/testing_framework/implementation/testdata_notation.rst` → `0` | OK | コーディネータが独立に再実行。`ja/` 全体で `grep -rn "フィールド名称の行"` → 0件（`testdata_converter.rst` からも消えている） |
| 4. §3 の7箇所と申し送り38、行番号参照2箇所が処置済み | OK | 7箇所を書き直した —— `reviews/page-testdata_converter.md:236`（「`:71` は変更していない」→「本ラウンドでは変更しなかった」＋確定文面への案内）・`:238`（「現行の `:71` の文も同じ誤りを含む」→ 現在の `:71` の逐語と、(b) の反例に触れない理由）、`reviews/page-testdata_notation.md:555`・`:585`・`:644`・`:648`・`:654`（いずれも HEAD への断定を、当該ラウンド時点の記録＋現在の逐語への案内に改めた）。申し送り38 は見出し `### 申し送り` ごと削除（`grep -c '38. \*\*追加行の「無い」'` → `0`。同節の項目は38 のみだったため空見出しを残さない判断）。行番号参照2箇所は `:595` の「（`reviews/page-testdata_converter.md:12`・`:15`）」→「（`reviews/page-testdata_converter.md` §「参照リポジトリ」）」、`:642` の「本ページ `:573`」（2箇所）→「本ページ §「出典（すべて `nablarch-testing@e21bf67`。`git show e21bf67:<path>` で読んだ）」」と「同節の走査は」。`grep -cE '本ページ `:573`\|page-testdata_converter\.md:12'` → `0`。あわせて、現在の逐語の置き場として `reviews/page-testdata_notation.md` に `## #35-是正2（表の4行と `:71` の文面を確定、2026-08-24）` 節を新設し、A-1〜A-5 それぞれの変更と実測根拠を表で記録した。**7箇所のほかに `:658`（追補の記録の導入文）へ1文を追加した** —— 同節の逐語も是正2 で置き換わっており、そのままでは現行と読める記述が残るため（§3 が名指しした7箇所を超える追加。コーディネータの判断を仰ぐ） | NG | 7箇所・申し送り38・行番号参照2箇所はいずれも処置済み（範囲統制レビューが `git diff -U0` の旧行番号と `git show 9343a11:<path>` の実物を突き合わせて9件全件を確認）。参照先の節見出しも実在・一意（`page-testdata_converter.md:7`・`page-testdata_notation.md:562`・`:652`・`:669`）。**ただし2件の瑕疵。** (a) `page-testdata_notation.md:667` の「`:883` と食い違っていないことの確認」が旧文面（「名前の行の…の句」）を前提にしており、無限定化した現文面には当てはまらない（`:702`-`:704` が引き継いでいる）。§2 の文面確定後に書き直す。(b) 新節 A-5 行に `mapping/glossary.md:269` と行番号で書いた。`.rn/` 内文書は節見出し参照が規約（`glossary.md` §1・`steering.md` Rules）。`§5.10「ファイルデータの行の名称」` へ直す（実在・一意を確認済み）。**なお `:658` への1文追加（7箇所超）はコーディネータ判定で valid。** §2 が同じ4行を差し替えた結果、直後のコードブロックが HEAD と食い違うため、§3 の「HEAD についての記述を反映後の状態に合わせて書き直す」の必然的帰結である |
| 5. §4 のレビューを回し、指摘件数と観点を記録済み。`must` を残していない | —（対象外） | 本作業の担当範囲外。作業指示により §4 のレビューはコーディネータが回す。したがって本コミットには §4 の記録を含めていない | NG | §4 のレビューは回した（下記「差分限定レビュー」節）。指摘5件のうち `must` 2件が未処置のため NG。指摘件数と観点の `reviews/page-testdata_notation.md` への記録も未了 |
| 6. Docker フルビルドが成功し警告0、`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` 実施済み、`_build` 削除済み | OK | 既存イメージ `nablarch-document-build:latest`（`a974e0c8ac60`）で `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` を実行 → `build succeeded.`（パイプ先頭の終了コード `0`）。`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。直後に `git -C /home/tie303177/work/nablarch/nablarch-document checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`_build/` は root 所有のためホストの `rm` が `Permission denied` になり、`docker run … rm -rf /root/document/_build /root/document/build.log` で削除。`ls -d _build build.log` → いずれも `No such file or directory`。`docker build` は行っていない | OK | **コーディネータが独立に再実行**（`steering.md` Rules による）。同じ既存イメージで `docker run … sphinx-build -d _build/.doctrees/ja -b html ja _build/html` → `build succeeded.`（`exit=0`）。`grep -cE "WARNING:|ERROR:|SEVERE:"` → `0`。直後に `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`_build/` は root 所有のため `docker run … rm -rf /root/document/_build` で削除し `ls -d _build` → `No such file or directory` |
| 7. `ca.crt`・`Dockerfile.ca` が作業ツリーに残っていない | OK | `ls ca.crt Dockerfile.ca` → いずれも `No such file or directory`。作業ツリー直下の `Dockerfile` は既存（`7月 24 14:45`）で本作業では触れていない | OK | コーディネータが独立に再確認。`ls ca.crt Dockerfile.ca` → いずれも `No such file or directory` |
| 8. §1〜§4 を1コミットにまとめてプッシュ済み | NG（§4 のぶんが未収録） | `9aa06d7` `docs: 行末の空セルの記述を是正2 の逐語へ差し替え、記録側を反映後の状態に直す` に §1・§2・§3 の4ファイル（`.rst` 2件・`reviews/` 2件）をまとめてコミットし、`git push origin ntf-yaml-support` 済み（`2779e6b..9aa06d7`。force push は行っていない）。**§4 のレビュー記録はコーディネータ担当のため本コミットに含まれていない。** 1コミットにまとめる要件を満たすには、コーディネータが §4 の記録を `git commit --amend` で同コミットへ追加する必要がある | NG | `9aa06d7` に §1〜§3 が入り push 済み（force push なし）。§4 のレビュー記録は §1〜§3 の実装後にしか書けないため、原理的に同一コミットへ入らない。**原因はコーディネータの作業指示の組み立て**（実装エキスパートへ「§1〜§3 を1コミットで push」と指示した）。`--amend` ＋ force push で畳むことは可能だが、rn の手順が force push を禁じているため2コミット目での処置を推奨。**user 判断待ち。** |

### 差分限定レビュー（是正2。4観点は回さない）

`ntf-doc-13-standing-rules.md:20` の常設ルールにより、本ラウンドは是正ラウンド2に当たるため4観点（QA / 設計 / クラフト / 検証）は回していない。作業指示 `ntf-doc-35-fix2.md` §4 が指定した2観点だけを、それぞれ独立したサブエージェントで回した。各観点には目的・対象差分・完了条件・チェックリストのみを渡し、本ファイル（self-check）と他観点の判定は渡していない。

**指摘5件（`must` 2 / `nice` 3）。うち採用4件、却下1件。**

| 観点 | 判定 | 指摘 | 内訳 |
|---|---|---|---|
| 是正が §1〜§3 の範囲に収まっているか（範囲統制） | pass | 1件 | `nice` 1（`mapping/glossary.md:269` の行番号参照。採用） |
| 是正が新しい欠陥を生んでいないか（事実検証。とくに §1・§2 の逐語指定文そのものへの反例） | fail | 4件 | `must` 2（§2 の無限定化が `:883` と食い違う／`:667` の検証結果が旧文面前提。いずれも採用）、`nice` 2（`:71` の飛び先にメッセージのデータ行の記述が無い＝採用／「（`Excel` 形式のみ。前述）」の括弧の使い方が `:1551`・`:1553` と揃わない＝**却下**） |

**却下1件の理由。** 「（\ `Excel`\ 形式のみ。前述）」の括弧の使い方は、作業指示 §2 の A-4 が `:1551`・`:1553` を根拠に明示的に確定したものであり、完了条件2 が逐語一致を求めている。指摘は scope 外。

**コーディネータの独立検証。** 事実検証観点の `must` 1件は、コーディネータが自分で `git show e21bf67:…` を実行して裏づけた（`DataFileParser.java:182`-`:191`・`DataFileFragment.java:102`-`:115`・`PoiXlsReader.java:118`-`:128`・`DataFileFragment.java:202`-`:203`・`:222`-`:223`、`nablarch-testing-converter@e977824` の `XlsFormatReaderInvalidInputTest.java:788`-`:818`、`ja/…/testdata_notation.rst:787`・`:883`）。`nice`（メッセージの記述欠落）も、`testdata_notation.rst:1152`-`:1309`（「メッセージングのデータを記述する」節）で `grep "空セル|空文字|補完|少ない|省略"` が0件であることを確認した。範囲統制観点の `nice` も `mapping/glossary.md` §5.10「ファイルデータの行の名称」が実在・一意であることを確認した。

### Overall Verdict

- Self-check: OK（完了条件1〜4・6・7。5 は担当範囲外、8 は §4 のぶんが未収録のため NG）
- 範囲統制レビュー: OK（`nice` 1件。次のコミットで処置）
- 事実検証レビュー: NG（`must` 2件。うち1件は §2 の逐語指定文そのものへの反例で user 判断待ち）
- 4観点（QA / 設計 / クラフト / 検証）: N/A（常設ルールにより是正ラウンド2 では回さない）
- Ready to check off: No（§2 の文面が user 判断待ち。完了条件2・4・5・8 が未達）

### Method を適用した記録（#35-是正2。どの主張をどの出典で確認したか）

逐語の流し込みは、指示書 `ntf-doc-35-fix2.md` の当該行を Python で読み出してそのまま書き込み、書き込み後に Python の `==` で検算した（完了条件1・2 の Evidence）。実装を根拠にする記述は、すべて参照コミット固定で `git show <commit>:<path>` を実行し、自分で現物を開いて確かめた。`ja/` の記述は現物のファイルを開いて確かめた。

| 主張（どこに書いたか） | 当たった出典 | 逐語（自分で開いて確認） |
|---|---|---|
| A-3 の根拠。`trimTailCopy` は `switch (status)` より前にあり4分岐すべてに掛かる（`reviews/page-testdata_notation.md` §「`#35`-是正2」の表） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/DataFileParser.java:66`-`:81`（`git show e21bf67:… \| awk` で表示） | `:66` `final void onReadLine(List<String> original) {` / `:68` `List<String> line = NablarchTestUtils.trimTailCopy(original); // キャッシュを破壊しないようにコピーして編集` / `:69` `switch (status) {` / `:70` `case READING_DIRECTIVES_AND_NAMES:` / `:73` `case READING_TYPES:` / `:76` `case READING_LENGTHS:` / `:79` `case READING_VALUES:` |
| テーブル側の `trimTailCopy` はヘッダ行にしか掛からない（同上） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/HeaderLine.java:32`-`:33` | `:32` `HeaderLine(List<String> headerLine) {` / `:33` `List<String> keys = trimTailCopy(headerLine);   // キャッシュを破壊しないようにコピーして編集` |
| A-5 の正表記が `フィールド名称行` である（同上） | `.rn/20260724-ntf-yaml-support/mapping/glossary.md:269`（現物を開いた） | `\| `フィールド名称行` \| 各フィールドの名称を並べた行 \| 揺れなし \| なし \| input資料15件、5ファイル（`S:input/ntf-doc-terms.md:176`） \|` |
| A-4 の根拠。機構Aを実例つきで先に説明しているのはテーブル側だけ（同上） | `ja/development_tools/testing_framework/implementation/testdata_notation.rst:774` と直後の実例表 `:776`-`:785`（現物を開いた） | `:774`「ヘッダ行（2行目）は、末尾に空セルが続いても、そこで記述を止めたのと同じ結果になる。次のヘッダ行は、\ ``ID``\ ・\ ``NAME``\ の2カラムだけを記載した場合と同じ結果になる。」 |
| A-4 の根拠。同じ表が既に「（前述）」を使っている（同上） | 同 `:1551`・`:1553`（現物を開いた） | `:1551`「    - マーカーカラムを除外する（前述）」／`:1553`「    - データベース登録時に、値が省略されたカラムへデフォルト値を補完する（前述）」 |
| A-1・A-2 の根拠。データ行の空セルの扱いは形式で分かれる（同上） | 同 `:658`（現物を開いた） | 「\ Excel\ 形式では、データ行のセル数がヘッダ行のカラム数より少ない場合、記述しなかったカラムには空文字が設定されたものとして扱われる。\ YAML\ 形式では、\ ``rows:``\ の先頭行のキーの一部を後続の行が持たない場合、そのカラムは\ ``null``\ を明示的に指定したのと同じ扱いになる。」 |
| A-1 の根拠。全要素が空のエントリは読み飛ばされる（同上） | 同 `:1534`（現物を開いた） | 「全要素が\ null\ または空文字のエントリは読み飛ばされる。Excel\ では行の全セルが空の場合、YAML\ では ``rows:``\ 内の要素が空マッピング（\ ``{}``\ ）またはすべての値が空文字の場合にスキップされる。」 |
| 機構B が `:883` に既出である（`reviews/page-testdata_notation.md` §「`#35`-是正2」末尾） | 同 `:883`（現物を開いた） | 「データ行のセル数（Excel形式）または ``rows:`` の各要素の長さ（YAML形式）がフィールド数より少ない場合、不足したフィールドは\ ``""``\ として補完される。」 |
| 機構B が `:787` に既出である（同上） | 同 `:787`（現物を開いた） | 「同じしくみにより、データ行（3行目以降）のセル数がヘッダ行より少ない場合も、記述しなかった分のカラムには空文字が設定されたものとして扱われる。」 |
| 旧文「行末の空セルは変換後に現れない」が `:71` から消えている（`reviews/page-testdata_converter.md` §「結論」） | `ja/development_tools/testing_framework/tools/testdata_converter.rst`（`grep`） | `grep -c '変換後に現れない' …/testdata_converter.rst` → `0` |
| 参照先の節見出しが一意である（`:595`・`:642` の節見出し参照） | `reviews/page-testdata_converter.md`・`reviews/page-testdata_notation.md`（`grep -c`） | `grep -c '^## 参照リポジトリ$' page-testdata_converter.md` → `1`、`grep -c '^### 出典（すべて' page-testdata_notation.md` → `1` |

**未確認のまま残した点。** 指示書冒頭が挙げる `StringUtil.isNullOrEmpty(Collection<String>)`（`nablarch-core` 2.2.0 の `StringUtil.java:155`-`:165`）は、`nablarch-core` の clone が `/home/tie303177/work/nablarch/` に無いため自分では確認していない。この事実は本ラウンドで書いた文面のどこにも根拠として使っていない（A-1 の説明は `implementation/testdata_notation.rst:1534` の現物を出典にした）。

## #35-是正3

### Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 24. `implementation/testdata_notation.rst:1545` が §1 の1行と逐語一致している | OK | 指示書 `ntf-doc-35-fix3.md` の19行目（0-origin で18）を Python で読み出してそのまま `:1545` へ流し込み（手打ちしていない）、書き込み後に `cur[1544] == inst[18]` を評価 → `True`（80文字）。現物の逐語は `    - フィールド名称行・データ型行・フィールド長行の行末の空セルを取り除く（\ Excel\ 形式のみ）。フィールド名称が宣言されていない値は読み込まない` |  |  |
| 25. `:1547` が変更されていない | OK | `git show HEAD:<path>` と作業ツリーを Python で1行ずつ比較 → 差分は `:1545` の1行のみ（`total diff lines: 1`、行数も同一）。`:1544`・`:1546`・`:1547` はいずれも `cur[i]==head[i]` → `True`。`git diff -U0` のハンクヘッダも `@@ -1545 +1545 @@ YAML形式の場合` の1つだけ。`git diff --numstat` は `.rst` が `1  1` |  |  |
| 26. §2 の3件が処置済み | OK | (a) `reviews/page-testdata_notation.md` §「追補（`ntf-doc-35-fix1-addendum.md` §2）に従って表の2行を書き換えた記録」の末尾の段落を、確定後の `:1545`・`:1547` に対する突合として書き直した（旧文面前提の「（\ Excel\ 形式のみ）は『名前の行の行末の空セルを取り除く』の句にだけ掛かっており」は消えている）。同ファイル §「データ行の補完（機構B）を表に書かなかった理由」との重複を避けるため、機構Bの非記載理由は繰り返さず同節へ送った。(b) 同ファイル A-5 行が `mapping/glossary.md` を行番号で指していたのを、`mapping/glossary.md` §5.10「ファイルデータの行の名称」へ改めた（`steering.md` Rules の「`.rn/` 内の文書どうしの相互参照は、行番号ではなく節見出しで指す」による）。節の実在・一意は `grep -c '^### 5.10 ファイルデータの行の名称$' .rn/20260724-ntf-yaml-support/mapping/glossary.md` → `1` で確認。(c) 「（\ Excel\ 形式のみ。前述）」の括弧の指摘は user 却下のため `:1547` を変更せず、同ファイル §「却下した指摘」に1文を残した |  |  |
| 27. §3 の申し送りが起こしてある | OK | `reviews/page-testdata_notation.md` 末尾に `### 申し送り（続き2）` を新設し、申し送り39 を既存節の書式（番号＋太字の見出し文＋根拠）で追加した。38 が欠番である理由も1文添えた（`git show 9aa06d7 -- .rn/…/reviews/page-testdata_notation.md` の差分に `-38. **追加行の「無い」は、同ページの多数派表記（かな）と逆である。**` があり、`#35`-是正2 のコミットが削除したことを確認）。根拠の実行結果は `sed -n '1152,1309p' ja/…/testdata_notation.rst \| grep -c <語>` → `空セル` 0・`補完` 0・`空文字` 0・`取り除` 0。既存の申し送り34〜37 の本体は書き換えていない |  |  |
| 28. §4 のレビューを回し、指摘件数と観点を記録済み。`must` を残していない | —（対象外） | 本作業の担当範囲外。作業指示により §4 のレビューはコーディネータが回す |  |  |
| 29. Docker フルビルドが成功し警告0、`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` 実施済み、`_build` 削除済み | OK | 既存イメージで `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` を実行 → 末尾 `build succeeded.`、終了コード `EXIT=0`。`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。直後に `docker run … rm -rf /root/document/_build /root/document/build.log`（`_build/` が root 所有のため）と `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`ls -d _build build.log` → いずれも `No such file or directory`。`docker build` は行っていない。**なお本ラウンドではビルドで `sphinx.mo` が変化しなかった**（ビルド直後の `git status --porcelain` は `.rn/…/reviews/page-testdata_notation.md`・`ja/…/testdata_notation.rst` の2件と未追跡の `build.log` のみ）。`git checkout --` は指示どおり実行しており、結果は no-op である |  |  |
| 30. `ca.crt`・`Dockerfile.ca` が作業ツリーに残っていない | OK | `ls -d ca.crt Dockerfile.ca` → いずれも `No such file or directory`。どちらも作成していない |  |  |
| 31. `9aa06d7` に続く1コミットとしてプッシュ済み。`--amend` と force push は行わない | —（対象外） | 作業指示 §6 により、本ラウンドではコミットもプッシュも行っていない。変更3ファイル（`ja/…/testdata_notation.rst`・`reviews/page-testdata_notation.md`・`checks/task-35.md`）を作業ツリーに残したまま返却した。`git add` も行っていない |  |  |

### Overall Verdict

- Self-check: OK（完了条件24〜27・29・30。28・31 は担当範囲外）
- 差分限定レビュー（範囲統制／事実検証）: fail。指摘10件＝`must` 2・`nice` 3（採用）・`nice` 3（未処置）・却下2。内訳と出典は `reviews/page-testdata_notation.md` §「是正2・是正3 の指摘件数と観点（Steps 11・16 の積み残しをここへ移す）」にある
- Ready to check off: No（`must` 2件が user 判断待ちのため。是正4 §1 が `must-1` を、§2 が `must-2` を処置して閉じた）

### Method を適用した記録（#35-是正3。どの主張をどの出典で確認したか）

逐語の流し込みは、指示書 `ntf-doc-35-fix3.md` の19行目を Python で読み出してそのまま書き込み、書き込み後に Python の `==` で検算した（完了条件24 の Evidence）。実装を根拠にする記述は、すべて参照コミット固定で `git show <commit>:<path>` を実行し、自分で現物を開いて確かめた。`ja/` の記述は現物のファイルを開いて確かめた。作業指示 §1 が根拠として挙げた4点も、記録へ書く前に自分で裏を取った。

| 主張（どこに書いたか） | 当たった出典 | 逐語（自分で開いて確認） |
|---|---|---|
| `trimTailCopy` は `switch (status)` より前にあり4分岐すべてに掛かる（`reviews/page-testdata_notation.md` §「`#35`-是正3」の表 1行目） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/DataFileParser.java:66`-`:79` | `:66` `final void onReadLine(List<String> original) {` / `:68` `List<String> line = NablarchTestUtils.trimTailCopy(original); // キャッシュを破壊しないようにコピーして編集` / `:69` `switch (status) {` / `:70` `case READING_DIRECTIVES_AND_NAMES:  //------------- ディレクティブ、フィールド名称` / `:73` `case READING_TYPES:` / `:76` `case READING_LENGTHS:` / `:79` `case READING_VALUES:   //---------------- データ行` |
| データ行ではトリムの効果が観測できない（同表 2行目、および `:667` の段落 (3)） | 同 `DataFileParser.java:182`-`:186` と `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/file/DataFileFragment.java:102`-`:107` | `DataFileParser.java:182` `protected void onReadingValues(List<String> line) {` / `:186` `currentFragment.addValue(tail(line));`。`DataFileFragment.java:102` `public void addValue(List<String> line) {` / `:105` `for (int i = 0; i < names.size(); i++) {` / `:107` `String value = i < line.size() ? line.get(i) : "";` |
| データ型行・フィールド長行はトリムされないとエラーになる（同表 3行目） | 同 `DataFileFragment.java:202`-`:203`・`:286`-`:287` | `:202` `public void setTypes(List<String> types) {` / `:203` `assertSameSizeAsNames(types, "types");` / `:286` `public void setLengths(List<String> lengths) {` / `:287` `assertSameSizeAsNames(lengths, "lengths");` |
| 同じ制約が本文にも書かれている（同表 3行目） | `ja/development_tools/testing_framework/implementation/testdata_notation.rst:883`（現物を開いた） | 「固定長ファイルでは、フィールド名称・データ型・フィールド長の3リストが同サイズで必須であり、1ファイルデータブロック内の全レコード定義は同一レコード長でなければならない（違反時はエラー）。」 |
| メッセージも `DataFileParser.onReadLine` を通る（同表 4行目） | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/reader/MessageParser.java:27`・`:114`-`:115`、`src/main/java/nablarch/test/core/reader/FixedLengthFileParser.java:15` | `MessageParser.java:27` `private final FixedLengthFileParser delegate;` / `:114` `void onReadLine(List<String> line) {` / `:115` `delegate.onReadLine(line);`。`FixedLengthFileParser.java:15` `public class FixedLengthFileParser extends DataFileParser<FixedLengthFile> {` |
| 「宣言されていない値は読み込まない」は YAML 形式でも成り立つ（`:667` の段落 (3)） | `nablarch-testing-yaml@190cc9a` `src/main/java/nablarch/test/core/reader/yaml/YamlFileBuilder.java:235` | `:235` `fragment.addValue(rowValues);`（同 `:219` `for (Object rowObj : getList(record, FIELD_ROWS)) {` のループ内。渡された行は上記 `DataFileFragment.addValue` を通る） |
| データ行の補完を述べているのは `:658`・`:787`・`:883` であり、トリムの記述と対象が重ならない（`:667` の段落 (1)(2)） | `ja/…/implementation/testdata_notation.rst:658`・`:787`・`:883`（現物を開いた） | `:658`「\ Excel\ 形式では、データ行のセル数がヘッダ行のカラム数より少ない場合、記述しなかったカラムには空文字が設定されたものとして扱われる。」／`:787`「同じしくみにより、データ行（3行目以降）のセル数がヘッダ行より少ない場合も、記述しなかった分のカラムには空文字が設定されたものとして扱われる。」／`:883`「データ行のセル数（Excel形式）または ``rows:`` の各要素の長さ（YAML形式）がフィールド数より少ない場合、不足したフィールドは\ ``""``\ として補完される。」 |
| 申し送り39 の根拠。メッセージング節に空セル・補完の記述が0件（`reviews/page-testdata_notation.md` の申し送り39） | `ja/…/implementation/testdata_notation.rst:1150`-`:1308`（現物を開き、`sed \| grep -c` を実行） | `:1150` `.. _testdata_notation-messaging_data:` / `:1152` `メッセージングのデータを記述する` / `:1306`「実際の記述例は :ref:`メッセージングのデータを記述する <testdata_examples-messaging_data>` を参照。」 / `:1308` `.. _testdata_notation-special_notation:`。`sed -n '1152,1309p' … \| grep -c` は `空セル` 0・`補完` 0・`空文字` 0・`取り除` 0 |
| 申し送り39 の送り元の逐語（同上） | `ja/development_tools/testing_framework/tools/testdata_converter.rst:71`（現物を開いた） | 「……データ行の空セルの扱いは形式によって異なるため、詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。」 |
| 用語の正表記（`:1545` の3語） | `.rn/20260724-ntf-yaml-support/mapping/glossary.md` §5.10「ファイルデータの行の名称」（節を現物で開いて確認） | 同節の表に正表記として `フィールド名称行`（「各フィールドの名称を並べた行」）・`データ型行`（「各フィールドのデータ型を示す行」）・`フィールド長行`（「各フィールドのバイト長を示す行。固定長ファイルのみで使うもの」）がある |
| 申し送り38 が欠番である理由 | `git show 9aa06d7 -- .rn/20260724-ntf-yaml-support/reviews/page-testdata_notation.md`（自分で実行） | 差分に `-### 申し送り` と `-38. **追加行の「無い」は、同ページの多数派表記（かな）と逆である。**` がある |

**未確認のまま残した点。** なし。本ラウンドで書いた記述の根拠は、すべて自分で `git show <commit>:<path>` または現物のファイルを開いて確認した。`nablarch-core` の clone は無いため、そこを根拠にした記述は書いていない。

## #35-是正4（最終）

### Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| 32. `:1545` が §1 の逐語と1文字一致（`sed -n '1545p'` の出力を記録に貼る） | OK | 作業指示 §1 の逐語を Python 文字列として組み、書き込み前に `new.replace('ディレクティブ行・','',1) == old` を評価 → `True`（差し替えが先頭への「ディレクティブ行・」の挿入のみであることの検算）。書き込み後の `sed -n '1545p' ja/development_tools/testing_framework/implementation/testdata_notation.rst` の出力（そのまま貼る）: `    - ディレクティブ行・フィールド名称行・データ型行・フィールド長行の行末の空セルを取り除く（\ Excel\ 形式のみ）。フィールド名称が宣言されていない値は読み込まない`（89文字） |
| 33. `:1547`・`tools/testdata_converter.rst:71` が未変更（`git diff` で確認） | OK | `git diff -U0 -- ja/` のハンクヘッダは `@@ -1545 +1545 @@ YAML形式の場合` の1つだけ。`git diff --numstat` の `.rst` は `1  1`。`git show HEAD:<path>` と作業ツリーを Python で1行ずつ比較 → 行数一致、差分は `:1545` の1行のみ（`diff idx: [1545]`）、`:1544`・`:1546`・`:1547` はいずれも `cur==head` → `True`。`git diff --stat -- ja/development_tools/testing_framework/tools/testdata_converter.rst` は空（未変更）。`mapping/glossary.md` も `git status --porcelain` に出ていない |
| 34. 申し送り40 が起票済み | OK | `reviews/page-testdata_notation.md` の `### 申し送り（続き2）` に、申し送り39 と同じ書式（番号＋太字の見出し文＋根拠）で40 を追加した。`tools/testdata_converter.rst` は変更していない（criterion 33）。`#35` 着地後に申し送り39・`:883` の Excel 側括弧書きと合わせて1タスクにする旨を末尾の1文に書いた。根拠の `:71` の逐語と `DataFileParser.java:68`・`:69` は自分で現物を開いて確認した |
| 35. `nice` 3件が反映済み | OK | (1) `reviews/page-testdata_notation.md` の是正2 節の見出しを `### 差し替え後の逐語（現在の HEAD）` → `### 差し替え後の逐語（是正2 時点）` に改め、直後の段落へ `:555`・`:654` と同型の失効注記（「**次の逐語は本ラウンド時点のものであり、現在は残っていない。**」＋現在の逐語の置き場への案内）を書いた。同型化のついでに、失効していた是正3 節の見出しと、`:555`・`:654` が「現在の逐語」として指していた先（いずれも是正2 節を指したままだった）も是正4 節へ付け替えた。(2) `checks/task-35.md` の `## #35-是正3` 節の新規2行——完了条件26 の行（`reviews/page-testdata_notation.md:667`・`:702`-`:704`・`mapping/glossary.md:269`）と Method 表の用語の行（`mapping/glossary.md` の `:262`-`:271`・`:269`・`:270`・`:271`）——から `.rn/` 内への行番号参照を取り除き、節見出し参照に直した（`steering.md` Rules の「`.rn/` 内の文書どうしの相互参照は、行番号ではなく節見出し（`ファイル名` §番号「見出し」）で指す」）。参照先の実在・一意は、3つの見出し（`reviews/page-testdata_notation.md` の §「追補（ntf-doc-35-fix1-addendum.md §2）に従って表の2行を書き換えた記録」と §「データ行の補完（機構B）を表に書かなかった理由」、`mapping/glossary.md` の §5.10「ファイルデータの行の名称」）を `grep -c` で数えていずれも `1` であることで確認。(3) 新設見出しの直前の空行を入れた——`reviews/page-testdata_notation.md` の是正3 節の見出しと `checks/task-35.md` の `## #35-是正3` は、いずれも直前の段落と密着していた（`cat -A` で確認）。両方に空行を入れた |
| 36. `reviews/page-testdata_notation.md`・`checks/task-35.md`・`steering.md` が反映後の状態 | OK | `reviews/page-testdata_notation.md` に §「`#35`-是正4（「ディレクティブ行」を加えて `:1545` を確定、2026-08-24）」を新設し、確定逐語・用語の根拠・§5 の転記・本ラウンドはレビュー未実施であること・是正2/是正3 の指摘件数と観点（Steps 11・16 の積み残し）を記録した。`checks/task-35.md` は本節（完了条件32〜39）を追加し、是正3 節の Overall Verdict の空欄（差分限定レビュー／Ready to check off）を埋めた。`steering.md` は Steps 11・13・14・16〜22 を check off し、`#35` の Notes を本ラウンドの結果に更新した |
| 37. §5 の6点が記録に転記済み | OK | `reviews/page-testdata_notation.md` §「逐語の根拠（作業指示 §5 の転記。参照コミット `nablarch-testing@e21bf67`）」に表として転記した。**作業指示 §5 の箇条書きは5点で、参照コミットの指定（`nablarch-testing@e21bf67`）が別に1点ある。完了条件の「6点」はこの5点＋参照コミットの指定として扱った**（節見出しに参照コミットを含め、5点を表の5行にした）。転記にあたり5点すべてを `git show e21bf67:<path>` で自分で裏を取り、5点とも一致した。あわせて2点を記録に追記した——`throw` 文の実体は `:222`-`:223` でブロックの閉じが `:224` であること、`PoiXlsReader.java` の `e21bf67` での実体パスが `src/main/java/nablarch/test/core/reader/PoiXlsReader.java` であること（`git ls-tree -r --name-only e21bf67 \| grep 'PoiXlsReader.java$'` が1件） |
| 38. Docker フルビルド成功・警告0、`sphinx.mo` が未変更、`ca.crt`・`Dockerfile.ca` が無い | OK | 既存イメージ `nablarch-document-build:latest`（`a974e0c8ac60`）で `docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"` を1回実行 → `build succeeded.`、`EXIT=0`。`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。直後に `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`docker run … rm -rf /root/document/_build /root/document/build.log` で後始末（`_build/` が root 所有のため）。`ls -d _build build.log ca.crt Dockerfile.ca` → 4件とも `No such file or directory`。ビルド後の `git status --porcelain` は本ラウンドの変更3ファイルのみで、`locales/ja/LC_MESSAGES/sphinx.mo` は出ていない。`.gitignore` は変更していない（`locales/` を加えていない）。`docker build` は行っていない |
| 39. 1〜7 をまとめた1コミットを `3132688` に続けてプッシュ済み。`--amend` と force push は行わない | OK | 完了条件32〜38 の変更4ファイル（`ja/…/testdata_notation.rst`・`reviews/page-testdata_notation.md`・`checks/task-35.md`・`steering.md`）を1コミットにまとめて push した。**`3132688` の直後には、前セッションの `/rn:dn` が残した `1d88729`（`wip:` コミット。是正3 の変更3ファイルを保全したもの）と、本セッションの `/rn:up` が残した `13bd603`（Steps 18〜22・完了条件32〜39 の起票と `State` のリセット）が入っている。** 本コミットはその続きに置いた（`69ab972`。`git push origin ntf-yaml-support` → `1d88729..69ab972`）。`--amend` と force push は行っていない |

### Overall Verdict

- Self-check: OK（完了条件32〜39）
- 差分限定レビュー: **N/A。本ラウンドはレビューを回していない**（是正ラウンドの上限3に到達したため。作業指示の冒頭による。§1 の逐語の反例検証はディレクター側が実測で実施済み）
- 4観点（QA / 設計 / クラフト / 検証）: N/A（`ntf-doc-13-standing-rules.md:20` の常設ルール）
- Ready to check off: Yes

### Method を適用した記録（#35-是正4。どの主張をどの出典で確認したか）

`:1545` の差し替えは、作業指示 §1 の逐語を Python 文字列として組み、書き込み前に「先頭への『ディレクティブ行・』の挿入だけであること」を `assert` で検算してから書き込んだ（完了条件32 の Evidence）。実装を根拠にする記述は、すべて参照コミット固定で `git show e21bf67:<path>` を実行し、自分で現物を開いて確かめた。`ja/` と `.rn/` の記述は現物のファイルを開いて確かめた。作業指示 §5 の5点も、記録へ書く前に自分で裏を取った（一致。`reviews/page-testdata_notation.md` §「逐語の根拠（作業指示 §5 の転記。参照コミット `nablarch-testing@e21bf67`）」の表に、当たった `file:line` と逐語を全件書いた）。

| 主張（どこに書いたか） | 当たった出典 | 逐語（自分で開いて確認） |
|---|---|---|
| 「ディレクティブ行」は同ページが既に使う語である（`reviews/…` §「用語「ディレクティブ行」を採った根拠」） | `ja/development_tools/testing_framework/implementation/testdata_notation.rst`（`grep -n 'ディレクティブ行'` を差し替え前に実行） | `1010:識別子行の後にディレクティブ行を置き、続けて以下のようにレコード種別以降を記載する。` / `1055:  * - ディレクティブ行`。この2件のみ |
| `mapping/glossary.md` §5.10 はレイアウトを表す行に限った節である（同上） | `.rn/20260724-ntf-yaml-support/mapping/glossary.md` §5.10「ファイルデータの行の名称」（節を現物で開いた） | 導入文「ファイルデータのレイアウトを表す行の名称である。現行解説書に該当語はなく、input資料の表記をそのまま採用する。」。表の正表記は `レコード種別行`・`フィールド名称行`・`データ型行`・`フィールド長行` の4語で、`ディレクティブ行` は無い |
| ディレクティブは同 §5.8 にある（同上） | 同 `mapping/glossary.md` §5.8「テストデータ」（節を現物で開いた） | 表の行「\| `ディレクティブ` \| ファイル・電文のフォーマットに関する属性を、キー名と値の2要素で指定するもの \| 揺れなし \| なし \| FW解説書24件（`FW:libraries/data_io/data_format/format_definition.rst:79`）、現行解説書40件、input資料47件 \|」 |
| ディレクティブ行の要素数が2未満のときのエラーが本文に既出である（§5 の3点目の転記） | `ja/…/implementation/testdata_notation.rst:892`（現物を開いた） | 「- ディレクティブまたはレコード種別・フィールド名称定義の要素数が2未満である」 |
| 申し送り40 の根拠となる `:71` の現状（`reviews/…` の申し送り40） | `ja/development_tools/testing_framework/tools/testdata_converter.rst:71`（現物を開いた） | 「名前の行（テーブルと\ ``LIST_MAP``\ ではカラム名の行、ファイルとメッセージではフィールド名称行）の行末の空セルは、\ Excel\ 形式から読み込む時点で取り除かれるため、往復すると消える。データ行の空セルの扱いは形式によって異なるため、詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。」 |
| 是正2 の指摘件数と観点（`reviews/…` §「是正2・是正3 の指摘件数と観点」） | `.rn/20260724-ntf-yaml-support/checks/task-35.md` §「差分限定レビュー（是正2。4観点は回さない）」の表（同ファイルを開いた） | 「**指摘5件（`must` 2 / `nice` 3）。うち採用4件、却下1件。**」と、観点2行の表 |
| 是正3 の指摘件数と観点（同上） | `git show 1d88729 -- .rn/20260724-ntf-yaml-support/steering.md`（自分で実行） | 同コミットが書いた `State` の `Next`（`must-1`・`must-2` と「採用 `nice` 3件」）と `Notes`（「**却下2件**」「**未処置の `nice` 3件（事実検証）**」）。**観点別の生出力は保全されていない**ため、`must` 2件と採用 `nice` 3件・却下2件がどちらの観点から出たかは記録に無い |

**未確認のまま残した点。** 是正3 の差分限定レビューの観点別の生出力（どの観点がどの指摘を出したか）。上記のとおり `1d88729` の `State` の要約が唯一の記録であり、原文は保全されていない。是正3 の `nice` 3件（未処置）が挙げた `ja/…/testdata_notation.rst:1076`・`:1269`・`:1057`-`:1063`・`:866`-`:875` と `SendSyncMessageParser.java:134`・`DataFileFragment.java:172` は、本ラウンドの作業指示の範囲外のため自分では当たっていない（`reviews/…` にも `1d88729` の `State` を出典として明記して転記した）。

## #35-是正5（第1ラウンド。§1 で停止）

### Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| 40. §1 の4点の検証結果が記録にある。反例が出た場合は §2 以降に進まず報告していること | OK | `reviews/page-testdata_notation.md` §「`#35`-是正5 §1 の逐語検証（着手前。`.rst` は未変更、2026-08-24）」に4点それぞれの検証結果を記録した。**(1) で反例が出たため §2 以降には進んでいない。** `git diff --stat -- ja/` が空であることで、`ja/` を1文字も変更していないことを確認した |
| 41. `:1545` が §1 の逐語と1文字一致 | **N/A（未着手）** | Step 24（§2）に未着手。作業指示 §1 の停止条件による |
| 42. `git diff -U0` の `ja/` 側のハンクが `@@ -1545 +1545 @@` の1つだけ | **N/A（未着手）** | 同上。現状は `ja/` 側のハンクが0件 |
| 43. §3 の2観点を別サブエージェントで回し、生出力が要約なしで記録にある | **N/A（未着手）** | Step 25（§3）に未着手。§2 が確定していないため回していない |
| 44. 是正3 の `nice` 3件が処置済みとして記録が更新されている | **未達** | 3件のうち処置できるのは §2 の差し替えを前提とする2件（ラベル列との字面の衝突／行の呼称の不統一）であり、§2 未着手のため未処置のまま。3件目の記録の誤り（「『フィールド長行』は固定長ファイルにのみ存在する」）は `reviews/…` §「`#35`-是正5 §1 の逐語検証」の (3) に訂正を記録した（`:1076` が言うのは可変長ファイルに無いことだけで、メッセージには存在する。`:1158`・`:1196`）。あわせて `mapping/glossary.md` §5.10 の `フィールド長行` の「意味」欄が同じ誤りを含むことも記録した（作業指示 §2 の変更禁止に従い未変更） |
| 45. 申し送り41 が起票済み | OK | `reviews/page-testdata_notation.md` §「申し送り（続き2）」に41 を追加した。**内容は作業指示の文面をそのまま写さず、§1 (1) の実測に合わせた**——作業指示は「`:1055` の「ディレクティブ行」だけがページ内で『行』付きである」とするが、実測では `:1010`・`:1055`・`:1076`・`:1267`・`:1269`・`:1271` の6件がある |
| 46. Docker フルビルド成功・警告0、`sphinx.mo` が未変更、`ca.crt`・`Dockerfile.ca` が無い | **N/A（未着手）** | Step 27（§5）に未着手。`ja/` を変更していないためビルドを回していない。`ls -d ca.crt Dockerfile.ca _build build.log` は4件とも `No such file or directory`、`git status --porcelain` に `locales/ja/LC_MESSAGES/sphinx.mo` は出ていない |
| 47. 40〜46 をまとめた1コミットを `149277f` に続けてプッシュ済み | **N/A（未着手）** | 本セッションの `/rn:up` は、Steps 23〜27・完了条件40〜47 の起票、`State` のリセット、§1 の検証結果と申し送り41 の記録を1コミットにまとめて `149277f` に続けて push した。§2 以降の1コミットは未作成 |

### Overall Verdict

- Self-check: **NG（§1 で停止）。** 完了条件40・45 は OK、44 は一部、41〜43・46〜47 は未着手
- 差分限定レビュー: 未実施（§2 が確定していないため）
- 4観点（QA / 設計 / クラフト / 検証）: N/A（`ntf-doc-13-standing-rules.md:20` の常設ルール）
- Ready to check off: **No。user の判断待ち**（`:1545` の『行』の付け外しをページ全体の語法の決めごととして扱うか、`:1545` だけ先に落とすか）

### Method を適用した記録（#35-是正5 §1。どの主張をどの出典で確認したか）

作業指示 §1 が挙げた行番号・逐語・実装の参照は、要約や過去の記録を経由せず、すべて自分でコマンドを実行して現物に当たった。`ja/` 側は `grep -n` と `awk 'NR==N'`、実装側は参照コミット固定の `git show e21bf67:<path>` を使った。

| 主張（作業指示 §1 のどこか） | 当たった出典と実行したコマンド | 判定 |
|---|---|---|
| (1) 構成図は `:851`-`:856` | `awk 'NR>=849 && NR<=884'` で通しの行番号を出力 → 構成図の実体は `:854`-`:858`（`:852` が `.. code-block:: text`） | **行番号がずれている**（内容の『行』なしは正しい） |
| (1) 「各要素の名称と役割は、以下のとおりである。」は `:864` | `grep -n '各要素の名称と役割は'` → `860:` の1件のみ | **行番号がずれている**（文面は一致） |
| (1) 用語表は `:866`-`:875` | 同 `awk` の出力 → `:866`-`:867` が見出し行、`:868`-`:875` が4語 | 一致 |
| (1) `:1055` の「ディレクティブ行」だけが『行』付きである | `grep -n` を `レコード種別行`・`フィールド名称行`・`データ型行`・`フィールド長行`・`ディレクティブ行` の5語で `implementation/testdata_notation.rst`・`implementation/testdata_examples.rst`・`tools/testdata_converter.rst` に対して実行 | **反例あり。** `:1545` を除いても同ページに6件（`:1010`・`:1055`・`:1076`・`:1267`・`:1269`・`:1271`） |
| (3) `:874`「各フィールドのバイト長（固定長ファイルのみ存在）」 | 同 `awk` の出力 `874`・`875` | 一致 |
| (3) 可変長ファイルにフィールド長行が無いことは `:1076` | `awk 'NR==1076'` | 一致 |
| (3) メッセージにはフィールド長行が有る（`:1158`・`:1196`） | `awk 'NR==1158 \|\| NR==1196'` | 一致 |
| (4) `DataFileFragment.java:105`-`:107`・`:67`・`:169`-`:172`・`:471` | `git show e21bf67:src/main/java/nablarch/test/core/file/DataFileFragment.java` を行番号付きで出力 | 5箇所とも一致 |
| (4) `DataFileParser.java:186`・`:250`-`:251` | `git show e21bf67:src/main/java/nablarch/test/core/reader/DataFileParser.java` | 一致 |
| (4) `SendSyncMessageParser.java:134` | `git show e21bf67:src/main/java/nablarch/test/core/reader/SendSyncMessageParser.java`（`NO_COLUMN_NUMBER = 0` は同 `:99`） | 一致 |
| 参照コミット `nablarch-testing@e21bf67` | `git -C /home/tie303177/work/nablarch/nablarch-testing log -1 --format='%H %ad %s' --date=short e21bf67` → `e21bf67e26bca1cb3bddcd00cdecfd10943f9333 2024-09-27 Merge remote-tracking branch 'origin/release-6u2'` | `steering.md` の参照コミット表と一致 |

**未確認のまま残した点。** `mapping/glossary.md` §5.10 の `フィールド長行` の意味欄「固定長ファイルのみで使うもの」を採った input 資料側の出典（`S:input/ntf-doc-terms.md:178`）には当たっていない。作業指示 §2 が `mapping/glossary.md` を変更禁止としているため、本ラウンドでは訂正の要否を判断する材料として記録に残すにとどめた。

## #35-是正5 第2ラウンド（フェーズA。`.rst` は1文字も変更していない）

### Completion Criteria

**フェーズA**

| Criterion | Self-check | Evidence |
|---|---|---|
| 41.（A-a）A-2〜A-5 それぞれについて、逐語案または「変更不要」の判定が出ている | OK | `reviews/page-testdata_notation.md` §「`#35`-是正5 フェーズA（実測と逐語案。`.rst` は1文字も変更していない、2026-08-24）」。A-2・A-3・A-4 は逐語案、A-5 は「変更不要（別概念）」の判定 |
| 42.（A-b）各判定に `file:line` と参照コミットハッシュが添えてある。示せないものは「未確認」と書いてある | OK | 同節に `file:line` の表を A-2・A-3・A-4・A-5 それぞれに置いた。参照コミットは同節 §「実測の方法」の表（`nablarch-testing@e21bf67`／`nablarch-testing-yaml@190cc9a`／`nablarch-testing-converter@e977824`）。**未確認として明記したもの**——申し送り42 の `S:input/ntf-doc-terms.md:178`（`mapping/glossary.md` §5.10 の採用根拠）には当たっていない |
| 43.（A-c）`ja/` が1文字も変更されていない | OK | `git diff --stat -- ja/` が空（実行して確認） |

**フェーズB**

| Criterion | Self-check | Evidence |
|---|---|---|
| 44.（B-a）`:1545` が A-1 の逐語と1文字一致 | **N/A（未着手）** | user の承認待ち |
| 45.（B-b）`git diff` の `ja/` 側の変更が A-1 と承認された案だけに由来している | **N/A（未着手）** | 同上 |
| 46.（B-c）B-3 の2観点を別サブエージェントで回し、生出力が要約なしで記録にある | **N/A（未着手）** | 同上 |
| 47.（B-d）申し送り39・40・41 が処置済みまたはクローズとして記録が更新されている | **一部** | 41 は「クローズしてよい」判定と根拠を `reviews/…` の A-5 に記録した。39・40 はフェーズB の反映後に更新する |
| 48.（B-e）`mapping/glossary.md` §5.10 の誤りが申し送りとして起票されている | OK | `reviews/page-testdata_notation.md` §「申し送り（続き2）」の 42（`フィールド長行` の意味欄）。あわせて 43（`レコード種別行`）も起票した |
| 49.（B-f）Docker フルビルド成功・警告0、`sphinx.mo` が未変更、`ca.crt`・`Dockerfile.ca` が無い | **N/A（未着手）** | `ja/` を変更していないためビルドを回していない |
| 50.（B-g）B-1〜B-5 をまとめた1コミットをプッシュ済み | **N/A（未着手）** | 作業指示は「`956c723` に続けて」と書いているが、`956c723` の後に `/rn:dn` の `667f7e0` が既に push 済みであるため、実際には最新コミットに続けることになる |

### Overall Verdict

- Self-check: **フェーズA は OK（41〜43 充足、48 も充足）。フェーズB は未着手**
- Ready to check off: **No。フェーズA の逐語案について user の承認待ち**

### Method を適用した記録（#35-是正5 第2ラウンド フェーズA。どの主張をどの出典で確認したか）

本ラウンドは、実装の読解ではなく**実行**を根拠にした。参照コミットを `git worktree` で取り出して `mvn -o -DskipTests compile` でビルドし、入力を自分で組み立てて各パーサへ通し、結果をリフレクションで観測した。成果物に付属する検証スクリプトは使っていない。

| 主張 | 当たった出典と実行したこと | 判定 |
|---|---|---|
| A-2: トリムが `DataFileParser` の4分岐すべてに掛かる | `git show e21bf67:src/main/java/nablarch/test/core/reader/DataFileParser.java` を行番号付きで出力（`:68` が `:69` の `switch` より前）。加えて、4行すべてに行末の空セルを付けた `.xls` を `FixedLengthFileParser` へ通し、`names=[A, B]`（2件）になることを観測した | 一致 |
| A-2: 変換ツールも同じ経路を通る | `git show e977824:src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java`（`:148`・`:152`・`:179`・`:464`）と `git grep -n 'readBlockBodyLines\|readFiles(\|readMessage(' e977824 -- src/main/java` | 一致 |
| A-3: メッセージのデータ行の空セルの扱いが Excel と YAML で同じ | Excel は `MessageParser`／`SendSyncMessageParser` に `.xls` を通して観測。YAML は `YamlTestDataParser`（`190cc9a` をビルド）に `.yaml` を通して観測。両者とも「不足は `""` 補完・超過は読み込まない・途中の空はそのまま `""`」 | 一致 |
| A-3: Excel の全セル空の行だけが両形式で異なる | `PoiXlsReader#readLine()` の出力に全セル空の行が現れないことを観測。`git show e21bf67:…/PoiXlsReader.java`（`:93`・`:141`-`:147`）と `…/TestDataParsingTemplate.java`（`:176`・`:316`-`:317`） | 一致 |
| A-4: `:883` の「先頭セルが空の行」が `isBlankLine` に掛かる | 全セル空の行を含む可変長ファイルの `.xls` を `VariableLengthFileParser` へ通し、`values.size()=3`（`""` の行は残り、全セル空の行は残らない）を観測。セルを1つも作らない行でも同じ | **掛かる。現行の括弧書きは成り立たない** |
| A-4: 正しい Excel の記法が `""` である | `ja/…/testdata_notation.rst:1363`・`:1367`（現物）。加えて `git show e21bf67:src/test/java/nablarch/test/core/reader/VariableLengthFileParserTest.xls` を POI で読み出し、シート `testEmptyRowSingleItem`・`testEmptyRowMultiItems` が `""` を使っていることを確認 | 一致 |
| A-5: `mapping/glossary.md` §5.10 は「行」、`testdata_notation.rst` の用語表は「要素」 | `mapping/glossary.md` §5.10 の見出しと導入文（現物）／`ja/…/testdata_notation.rst:855`・`:860`・`:876`-`:879`（現物）／`ja/…/testdata_examples.rst:1082`（現物）／`git show e21bf67:…/DataFileParser.java:248`-`:252` | **別概念。ページの是正は不要** |

**未確認のまま残した点。** `mapping/glossary.md` §5.10 の `フィールド長行` の意味欄が採った input 資料側の出典（`S:input/ntf-doc-terms.md:178`）には当たっていない（申し送り42 にも明記した）。
