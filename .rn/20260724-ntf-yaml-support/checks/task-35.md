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
