# `#23` self-check — テーブルデータの0件の扱いを解説書に書く

作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-23-table-zero-rows.md`（2026-08-14 受領）

参照コミット

| リポジトリ | コミット | 備考 |
|---|---|---|
| `nablarch-document` | `664df75`（着手時。指示書の参照点 `cf0eb2f` から本タスク開始までに対象2ページの差分0件） | `git diff --stat cf0eb2f HEAD -- ja/development_tools/testing_framework/implementation/` が空 |
| `nablarch-testing` | `e21bf67`（`main` / タグ `2.2.0`） | `git tag --points-at e21bf67` → `2.2.0` |
| `nablarch-testing-yaml` | `190cc9a` | `feature/ntf-yaml` の最新の**ソース**コミット。以降の3コミット（`7022be9`・`f7e1563`・`e3df790`）は `.rn/` 配下のみを変更しており `src/main/java` は同一（`git log --name-only 190cc9a..feature/ntf-yaml` で確認） |

---

## `design.md` §8 の実装優先の原則を本件に適用しないというユーザー判断

`design.md` §8 は「出典と実装が食い違う場合は実装を優先する」と定めているが、**本タスクではこの原則を適用しない**というユーザー判断が 2026-08-13 に下された。`expected_tables:` に `rows: []` を書いたときの期待値0件の検証は、`190cc9a` 時点の `nablarch-testing-yaml` では実際には行われない（事実18・14・15 → 事実1・2・9）。それでも解説書は、テスティングフレームワーク本体が追随する前提で**仕様どおりに**書く。したがって本文には、形式・データタイプによる場合分けも、実装の制約を注記する記述も置かない。この判断の `design.md` への規定化は本タスクでは行わない（同種の判断が再度出た時点で判断する）。

---

## ゲート1 — `git status --porcelain` の全件（着手時）

| # | 状態 | パス | 判定 |
|---|---|---|---|
| — | （出力0件） | — | PASS |

着手時点で作業ツリーはクリーンであった（`#24` の承認記録コミット `664df75` の直後）。

---

## ゲート2 — 実装事実19件の全件突合

すべて `git show <コミット>:<パス>` で開いて確認した。**事実18 は記録のみで、本文には反映しない。**

### `nablarch-testing` `e21bf67`

| # | file:line | 指示書の記述 | 実物での確認結果 | 判定 |
|---|---|---|---|---|
| 1 | `src/main/java/nablarch/test/core/db/TableData.java:337-346` | `loadData()` は列名が0個のとき空のリストを入れて `return` する | `:339` `String[] colNames = getColumnNames();`／`:343-346` `if (colNames.length == 0) { contents = new ArrayList<SqlRow>(0); return; }` | 一致 |
| 2 | 同 `:348` | SELECT 文の組み立てはガードの後にある | `:348` `final String sql = createSelectStatement(...)` がガード（`:343-346`）の後 | 一致 |
| 3 | 同 `:489-493` | `setColumnNames` は長さ0の配列をそのまま代入する | `:490` `this.columnNames = new String[columnNames.length];` — `null` にはならない | 一致 |
| 4 | 同 `:501-505` | `getColumnNames()` が全カラムに落ちるのは列名が `null` のときだけ | `:502` `if (columnNames == null) { columnNames = dbInfo.getColumns(tableName); }` | 一致 |
| 5 | 同 `:706-722`（特に `:721`） | `fillDefaultValues()` は最後に `setColumnNames(allColumns)` を実行する | `:706` メソッド開始・`:721` `setColumnNames(allColumns);`・`:722` 閉じ括弧 | 一致 |
| 6 | 同 `:127-130` | `deleteData` は `DELETE FROM <テーブル名>` で列名を使わない | `:128` `connection.prepareStatement("DELETE FROM " + tableName)` | 一致 |
| 7 | 同 `:137-217`・`:325-334` | `insertData` は `getNonComputedColumns()` を使い、テストデータに書いた列名は使わない | `:139` `String[] nonComputedColumns = getNonComputedColumns();`／`:325-334` は `dbInfo.getColumns(tableName)` から自動計算カラムを除く。**事実の内容は一致。ただし `insertData` の実体は `:137-178` であり、`:137-217` は続く `convert` の javadoc 途中までを含む** | 一致（範囲末尾のみ差異。§末尾に記録） |
| 8 | `src/main/java/nablarch/test/Assertion.java:79-83` | `assertTableEquals` は期待値を clone して `loadData()` した結果を実際の値にする | `:80` `TableData actual = expected.getClone();`／`:81` `actual.loadData();` | 一致 |
| 9 | 同 `:259`・`:263`・`:306-313` | 比較はループ2つだけで、期待値0行・実際の値0行ではどちらも回らない | `:259` `boolean[] dbDataFound = createArray(actual.size(), false);`／`:263` `for (int expIdx = 0; expIdx < expected.size(); expIdx++)`／`:307-313` `for (int i = 0; i < dbDataFound.length; i++)`（`:306` はその直前のコメント行） | 一致 |
| 10 | `src/main/java/nablarch/test/core/db/DbAccessTestSupport.java:363-369` | `failIfNoDataFound` が捕まえるのは期待値のデータブロックが1つも無い場合だけ | `:363` `if (expected.isEmpty() && failIfNoDataFound) {` — `expected` は `List<TableData>`。カラム名0個の `TableData` は要素として存在するため通り抜ける | 一致 |
| 11 | `src/main/java/nablarch/test/core/reader/TableDataParser.java:89-97`（`:94`・`:96`） | 識別子行の次の行をカラム名の行として読む | `:93` `header = new HeaderLine(readLine());`／`:94` `String[] columnNames = header.getEffectiveColumnNames();`／`:96` `processing = new TableData(dbInfo, tableName, columnNames, defaultValues);` | 一致 |
| 12 | `src/main/java/nablarch/test/core/reader/TestDataParsingTemplate.java:176-178` | 全セルが空の行は読み飛ばされる | `:176-178` `if (isBlankLine(line)) { continue; }` | 一致 |
| 13 | `src/main/java/nablarch/test/core/reader/BasicTestDataParser.java:171-181`（`:177`） | Excel形式では `EXPECTED_COMPLETE_TABLE` に対して `fillDefaultValues()` が実行される | `:175-178` `getTableData(..., DataType.EXPECTED_COMPLETED, gid)` の結果に対し `e.fillDefaultValues();` | 一致 |

### `nablarch-testing-yaml` `190cc9a`

| # | file:line | 指示書の記述 | 実物での確認結果 | 判定 |
|---|---|---|---|---|
| 14 | `src/main/java/nablarch/test/core/reader/yaml/YamlSection.java:156-161` | `resolveColumns` は `rows` が空なら空のリストを返す | `:157-159` `if (rows.isEmpty()) { return new ArrayList<String>(); }` | 一致 |
| 15 | `src/main/java/nablarch/test/core/reader/yaml/YamlTableDataBuilder.java:110-115` | 列名0個のまま `TableData` を生成する。`:110-114` に偽陰性の `FIXME` がある | `:110-114` に `FIXME:` コメント（「`dataColumns` が空（`rows: []`）のとき…検証が素通りする（偽陰性）」）／`:115` `TableData td = new TableData(dbInfo, tableName, dataColumns.toArray(new String[0]), defaultValues);` | 一致 |
| 16 | 同 `:127` | `fillDefaults` が真なら `fillDefaultValues()` が実行される | `:127-129` `if (fillDefaults) { td.fillDefaultValues(); }` | 一致 |
| 17 | `src/main/java/nablarch/test/core/reader/YamlTestDataParser.java:114` | `setup_tables` は `fillDefaults=false` | `:114` `buildTableDataList(yaml, YamlSection.KEY_SETUP_TABLES, gid, false, path)` | 一致 |
| 18 | 同 `:123` | `expected_tables` は `fillDefaults=false` | `:122-123` `buildTableDataList(yaml, YamlSection.KEY_EXPECTED_TABLES, gid, false, path)` | 一致。**記録のみ・本文に反映しない** |
| 19 | 同 `:125` | `expected_complete_tables` は `fillDefaults=true` | `:124-125` `buildTableDataList(yaml, YamlSection.KEY_EXPECTED_COMPLETE_TABLES, gid, true, path)` | 一致 |

**19件すべて一致。** 本文を書かずに報告すべき食い違いは0件。

### 指示書との差異1件（報告）

事実7 の `file:line` のうち **`insertData` の範囲末尾が `:217` ではなく `:178`** である。`git show e21bf67:src/main/java/nablarch/test/core/db/TableData.java | awk 'NR>=155 && NR<=200'` で確認したところ、`:177` `insert.executeBatch();`・`:178` `}` でメソッドが閉じ、`:180-188` は次のメソッド `convert` の javadoc、`:189` が `convert` の定義である。**事実の内容（`insertData` は `getNonComputedColumns()` を使い、テストデータに書いた列名は使わない）は一致している**ため、本文を書かずに報告する事案には当たらないと判断し作業を継続した。事実7 は本文に直接は反映していない。

### 追加で自分で確かめた事実（本文の裏付け）

| # | file:line | 事実 |
|---|---|---|
| 補-1 | `nablarch-testing` `e21bf67` `src/main/java/nablarch/test/core/db/DbAccessTestSupport.java:182-201` | 準備データの投入は `getSetupTableData` の戻り（`List<TableData>`）が空のときだけ早期 `return` する（`:184-186`）。行数0の `TableData` は要素として存在するため早期 `return` に掛からず、`:195` の `deleteData` が実行される。`:200` の `insertData` は0行のループになる。**「準備データを0件にすると DELETE だけが行われ、対象テーブルは空になる」という本文の記述は、この経路で裏付けられる** |

---

## ゲート3 — 変更した2ページの `ja/` 差分（全件）

`git diff --numstat -- ja/`

| ファイル | 追加 | 削除 |
|---|---|---|
| `ja/development_tools/testing_framework/implementation/testdata_examples.rst` | 50 | 0 |
| `ja/development_tools/testing_framework/implementation/testdata_notation.rst` | 34 | 1 |

追加ブロックの範囲（`git diff -U0` の hunk ヘッダ）

| ファイル | hunk | 内容 |
|---|---|---|
| `testdata_examples.rst` | `@@ -950,0 +951,50 @@` | 新L3「0件のテーブルデータを記述する」（ラベル・導入文・形式別L4対） |
| `testdata_notation.rst` | `@@ -650 +650 @@` | **唯一の既存行の書き換え。** `:650` の列挙に0件の扱いを加えた（是正前は「0件のデータの扱い」、R1-4 の是正後は「0件のデータの記述」） |
| `testdata_notation.rst` | `@@ -728,0 +729,10 @@` | 新L4「0件のデータを記述する」 |
| `testdata_notation.rst` | `@@ -776,0 +787,15 @@` | 既存L4「Excel形式の場合」への追記（セル格子1つ＋カラム名の行を省略できない旨） |
| `testdata_notation.rst` | `@@ -808,0 +834,8 @@` | 既存L4「YAML形式の場合」への追記（`rows: []` の `code-block`） |

**判定: PASS。** 追加のみで、既存行の削除・書き換えは §4-1 が指示した `:650` の1文だけである。

---

## ゲート4 — 「不具合」「バグ」「将来」「修正され」

`grep -cE "不具合|バグ|将来|修正され"` の結果は両ページとも **0件**。**判定: PASS。**

---

## ゲート4a — `EXPECTED_COMPLETE_TABLE` / `expected_complete_tables` の全件

`grep -nE "EXPECTED_COMPLETE_TABLE|expected_complete_tables"` の全22件。**このうち0件の説明の中（本タスクの追加ブロック `testdata_notation.rst:729-738`・`:787-801`・`:834-841`、`testdata_examples.rst:951-1000`）に現れるものは0件である。**

| # | file:line | 対象外の理由 |
|---|---|---|
| 1 | `testdata_examples.rst:780` | L2 の導入文。既存行 |
| 2 | `testdata_examples.rst:864` | 既存L3の見出し |
| 3 | `testdata_examples.rst:866` | 既存L3の導入文 |
| 4 | `testdata_examples.rst:870` | 既存の `important`（データタイプごとにまとめて記述する） |
| 5 | `testdata_examples.rst:907` | 既存のセル格子の識別子行 |
| 6 | `testdata_examples.rst:922` | 既存L4「YAML形式の場合」の地の文 |
| 7 | `testdata_examples.rst:941` | 既存の `code-block` 内 |
| 8 | `testdata_notation.rst:155` | 既存のデータタイプ一覧表 |
| 9 | `testdata_notation.rst:218` | 既存の Excel/YAML 対応表 |
| 10 | `testdata_notation.rst:219` | 同上（YAML 側キー名） |
| 11 | `testdata_notation.rst:282` | 既存の `important`（グループIDによる使い分け） |
| 12〜15 | `testdata_notation.rst:289`・`:293`・`:301`・`:303` | 既存の `code-block` 内の識別子行 |
| 16 | `testdata_notation.rst:432` | 既存のカラム説明表 |
| 17 | `testdata_notation.rst:541` | 同上 |
| 18 | `testdata_notation.rst:650` | 本タスクで書き換えた行だが、**書き換えたのは末尾の列挙のみ**で、`EXPECTED_COMPLETE_TABLE` はデータタイプ列挙として既存のまま残った部分にある |
| 19 | `testdata_notation.rst:684` | 既存の `important`（自動採番の主キー） |
| 20 | `testdata_notation.rst:696` | 既存の `important`（省略機能の適用範囲） |
| 21 | `testdata_notation.rst:698` | 既存の地の文（カラム省略時の挙動） |
| 22 | `testdata_notation.rst:725` | 既存の地の文（更新系テストの例） |
| 23 | `testdata_notation.rst:727` | 既存の地の文（`getExpectedTableData` のマージ） |
| 24 | `testdata_notation.rst:817` | 既存の地の文（`table` キーが必須・カラム名の決まり方）。本タスクの YAML 追記（`:834-841`）より前の行 |

**判定: PASS。**

---

## ゲート4b — 期待値0件の扱いの場合分け

追加ブロックの記述を全件確認した。

| 追加ブロック | 期待値0件に関する記述 | 場合分けの有無 |
|---|---|---|
| `testdata_notation.rst:729-738`（新L4） | 「期待値を0件にすると、そのテーブルにレコードが1件も無いことの検証になる。」 | データタイプ名・形式名をいずれも挙げていない。場合分け無し |
| `testdata_notation.rst:787-801`（Excel） | 「0件のデータは、以下のように記述する。準備データ・期待値のいずれでも同じである。」 | 準備データ／期待値を同じ扱いと明示。場合分け無し |
| `testdata_notation.rst:834-841`（YAML） | 「0件のデータは、``rows:`` に空の配列を指定して記述する。準備データ・期待値のいずれでも同じである。」 | 同上 |
| `testdata_examples.rst:951-1000` | 「準備データを0件にすることでテーブルが空になり、期待値を0件にすることで1件も無いことの検証になる。」 | 形式差は書式のみ（L4対）。意味の説明に場合分け無し |

**判定: PASS（場合分け0件）。**

---

## ゲート5 — クラス名

`grep -nE "TableData|Assertion|YamlTableDataBuilder|YamlSection|TableDataParser"` のヒットは1件のみ。

| file:line | ヒット内容 | 判定 |
|---|---|---|
| `testdata_notation.rst:727` | 既存の地の文中の**メソッド名** `getExpectedTableData`（部分文字列として `TableData` に一致）。クラス名の言及ではなく、本タスクで追加・変更した行でもない | 対象外 |

**本タスクの追加ブロックにクラス名は0件。判定: PASS。**

---

## ゲート6 — 新しく足した見出しの下線

`unicodedata.east_asian_width` で表示幅（全角=2・半角=1）を算出し、各ファイルの既存見出しの実測則と突き合わせた。

**実測した既存の則**（両ファイルの全見出しを機械走査）

| ファイル | L1 `=` | L2 `-` | L3 `~` | L4 `^` |
|---|---|---|---|---|
| `testdata_notation.rst` | 50（1件） | 50（3件） | **49（10件、例外なし）** | **49（26件、例外なし）** |
| `testdata_examples.rst` | 50（1件） | 50（9件） | **50（23件）＋表示幅がこれを超える5件は表示幅ちょうど**（52・56・59・60・63） | **50（56件、例外なし）** |

つまり `max(基準値, 表示幅)` で、基準値は `testdata_notation.rst` が 49、`testdata_examples.rst` が 50 である。

| 見出し | ファイル:行 | 表示幅 | 下線 | 期待値 | 判定 |
|---|---|---|---|---|---|
| `0件のデータを記述する`（L4） | `testdata_notation.rst:729` | 21 | `^`×49 | 49 | PASS |
| `0件のテーブルデータを記述する`（L3） | `testdata_examples.rst:953` | 29 | `~`×50 | 50 | PASS |
| `Excel形式の場合`（L4） | `testdata_examples.rst:957` | 15 | `^`×50 | 50 | PASS |
| `YAML形式の場合`（L4） | `testdata_examples.rst:987` | 14 | `^`×50 | 50 | PASS |

**判定: PASS（逸脱0件）。**

---

## ゲート7 — 形式別L4対の組数

`testdata_notation.rst` の L3「テーブルのデータを記述する」（`:648`）配下のL4を全件走査した。

| 行 | L4見出し |
|---|---|
| 660 | 準備データ（SETUP_TABLE）を記述する |
| 670 | 共通の準備データをまとめる |
| 674 | 期待値（EXPECTED_TABLE等）を記述する |
| 690 | カラムを省略する |
| **729** | **0件のデータを記述する（本タスクで追加）** |
| 739 | Excel形式の場合 |
| 804 | YAML形式の場合 |

**本タスクで追加した形式別L4対は0組**（既存の1組に追記しただけ）。追加したL4は形式別L4対より前にあり、S-10 規約3「形式別のL4対はそのL3の末尾2つに置く」を満たす。

`testdata_examples.rst` の新L3「0件のテーブルデータを記述する」（`:953`）配下のL4は `Excel形式の場合`（`:957`）・`YAML形式の場合`（`:987`）の**1組のみ**。

**判定: PASS。**

---

## ゲート8 — `:ref:` の参照先ラベル

| 参照元 | ラベル | 定義箇所 | 判定 |
|---|---|---|---|
| `testdata_notation.rst:737` | `testdata_examples-empty_table` | `testdata_examples.rst:951` | 実在 |

Docker フルビルドのログ（ゲート11）で `undefined label` は **`db_double_submit.rst:108` の既知1件のみ**であり、本タスクで追加した参照は含まれない。**判定: PASS。**

---

## ゲート9 — `verify_mapping.py`

```
$ python3 .rn/20260724-ntf-yaml-support/mapping/tools/verify_mapping.py
Loaded 595 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
exit=0
```

**判定: PASS（595行 / 12,986 / 11,983 が不変）。**

---

## ゲート10 — 禁止ファイル群の差分

`git status --porcelain` の全件が次の2件のみで、`mapping.csv`・`mapping/_batch/`・`volume.md`・`vocabulary.md`・`style.md`・`glossary.md`・`design.md`・`ja/conf.py` はいずれも差分0件。

```
 M ja/development_tools/testing_framework/implementation/testdata_examples.rst
 M ja/development_tools/testing_framework/implementation/testdata_notation.rst
```

**判定: PASS。**

---

## ゲート11 — Docker フルビルド（`-a`）

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
    nablarch-document-build /bin/bash -c \
    "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
...
build succeeded, 1 warning.
exit=0
```

警告の全件

| # | 警告 | 判定 |
|---|---|---|
| 1 | `ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` | 既知（`#7` のフォローアップで検出済み。`#last` で解消する） |

**新規警告0件。判定: PASS。**

ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、再生成された `sphinx.mo`（`git status` に ` M` で現れた）を戻した。戻した後の `git status --porcelain` は上記2件のみ。

---

## 4観点レビュー ラウンド1

4観点をそれぞれ別のサブエージェントで実施した（A:網羅性 / B:トンマナ / C:用語 / D:整合性）。依頼プロンプトには Rules の3点と、指示書 §7 の申し送り段落をそのまま入れた。

| 観点 | 判定 |
|---|---|
| A 網羅性 | PASS（`must` 0） |
| B トンマナ | PASS（`must` 0） |
| C 用語 | FAIL（`must` 1） |
| D 整合性 | 1回目 FAIL（`must` 2）→ 同一エージェントの2回目の走行で PASS（`must` 0） |

**重複除去後の指摘は15件（R1-1〜R1-15）。うち6件を是正、1件を Invalid と判定、8件を対応しない（うち3件は申し送り）。** 指摘→対応の対応表は `reviews/page-testdata_notation.md` の `## #23` 節「4観点レビュー ラウンド1」に全件記録している（Rules「レビュー監査の記録は `reviews/page-*.md` にのみ書く」に従う）。ラウンド2 は実施していない（`must` が残存せず、是正が6件とも語句の差し替えに収まったため）。

### Invalid と判定した指摘1件（R1-7）

観点D が1回目の走行で挙げた `must`「`testdata_notation.rst:800` の『その次に現れた行がカラム名の行になる』が実装と食い違う」は、**実物に当たって Invalid と判定した**。

- 指摘が引用した `isOtherType` / `foundTargetType` は、`e21bf67` の `TestDataParsingTemplate.java` に**存在しない**。`git show e21bf67:src/main/java/nablarch/test/core/reader/TestDataParsingTemplate.java | grep -n "isOtherType\|foundTargetType\|shouldStopOnNextOne"` のヒットは `:77`・`:202` の `shouldStopOnNextOne` のみで、実物の `parse` は `:193-219` にあり `nowReading` と `shouldStopOnNextOne()` で分岐する
- さらに `TableDataParser.java:93` の `onTargetTypeFound` が `header = new HeaderLine(readLine());` で**次の行を自ら消費する**。したがってその行が別のデータタイプの識別子行であっても、メインループの `break` 判定（`:202`・`:215`）に届く前にカラム名の行として読まれる
- **同じサブエージェントの2回目の走行では PASS（`must` 0）** になっており、この指摘は取り下げられている

### ユーザー判断事項として報告する1件（R1-12）

**記法ページの見出し「0件のデータを記述する」と、記載例ページの見出し「0件のテーブルデータを記述する」が非対称である。** 観点A・B・C の3観点が独立に挙げた。観点C の実測によれば、両ページの対応節はこれまで**9組すべてがタイトル完全一致**であり（`データブロックとデータタイプ`／`グループIDによる使い分け`／`テストショット一覧（testShots）を記述する`／`LIST_MAPのデータを記述する`／`テーブルのデータを記述する`／`ファイルのデータを記述する`／`メッセージングのデータを記述する`／`null・空文字・改行など特殊な値を記述する`／`コメント・マーカーカラム・空エントリを扱う`）、今回の追加だけが割れる。`testdata_notation.rst:737` の `:ref:` は参照先のタイトルを表示するため、隣り合う見出しと参照文で同じ話題が2つの名前で呼ばれる。

**見出し文言は指示書 §4-1・§4-3 が明示的に指定しているため、本タスクでは変更していない。** 揃えるなら記法ページ側を「0件のテーブルデータを記述する」にし、`:650` の列挙語も「0件のテーブルデータの記述」にすることになる。

---

## 是正後のゲート再実行

R1-1〜R1-6 の是正（本文6箇所の語句の差し替え）の後、影響するゲートを再実行した。

| ゲート | 再実行の結果 |
|---|---|
| 3 | 差分の形は不変（`examples` +50 / `notation` +34-1、hunk も5つで同じ）。**追加のみで、既存行の書き換えは `:650` の1文だけ**という判定も不変 |
| 4 | 0件（PASS） |
| 4a | 追加行に現れる `EXPECTED_COMPLETE_TABLE` は1件のみで、これは `:650` の書き換え行（データタイプの列挙として既存のまま残った部分）。**0件の説明の中には0件**（PASS） |
| 4b | 場合分け0件（PASS）。是正で「準備データ・期待値のいずれでも同じである。」の2文はそのまま残した |
| 5 | 追加行のヒット0件（PASS） |
| 6 | 下線に変更なし（見出し文言を変えていないため）。逸脱0件（PASS） |
| 9 | `exit 0`・595行 / 12,986 / 11,983 不変（PASS） |
| 10 | 禁止ファイル群の差分0件（PASS） |
| 11 | Docker フルビルド（`-a`）が `build succeeded, 1 warning.`／`exit 0`。警告は既知の `db_double_submit.rst:108` のみで新規0件。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して復元（PASS） |

### 是正した6箇所

| # | file:line | 是正前 → 是正後 |
|---|---|---|
| R1-4 | `testdata_notation.rst:650` | `0件のデータの扱いについて説明する。` → `0件のデータの記述について説明する。` |
| R1-2・R1-3 | `testdata_notation.rst:733` | `前述の全件\ DELETE\ だけが行われ` → `` ``SETUP_TABLE``\ による登録で行われる全件\ DELETE\ だけが行われ ``／`1件もレコードが無い状態から…行を0件にした準備データを記述する。` → `レコードが1件もない状態から…0件の準備データを記述する。` |
| R1-5 | `testdata_notation.rst:735` | `レコードが1件も無いことの検証` → `レコードが1件もないことの検証` |
| R1-1 | `testdata_notation.rst:834` | `` ``rows:``\ に空の配列を指定して記述する。 `` → `` ``rows:``\ に空配列 ``[]``\ を記載する。 `` |
| R1-6・R1-5 | `testdata_examples.rst:955` | `を空にした状態でバッチ処理を実行し、処理後もこのテーブルにレコードが1件も無いことを…1件も無いことの検証になる。` → `を空にした状態で、処理対象のデータが1件もない場合のバッチ処理を実行し、処理後もこのテーブルにレコードが1件もないことを…1件もないことの検証になる。` |
| R1-1 | `testdata_examples.rst:989` | `` ``rows:``\ に空の配列を指定する。 `` → `` ``rows:``\ に空配列を記述する。 `` |

---

## ゲート12 — `commit & push` 直前の差分範囲の再確認

`git status --porcelain` の全件

| # | 状態 | パス | §0 の「変更してよいファイル」か |
|---|---|---|---|
| 1 | ` M` | `.rn/20260724-ntf-yaml-support/reviews/page-testdata_examples.md` | 該当 |
| 2 | ` M` | `.rn/20260724-ntf-yaml-support/reviews/page-testdata_notation.md` | 該当 |
| 3 | ` M` | `.rn/20260724-ntf-yaml-support/steering.md` | 該当 |
| 4 | `??` | `.rn/20260724-ntf-yaml-support/checks/task-23.md` | 該当（新規） |
| 5 | ` M` | `ja/development_tools/testing_framework/implementation/testdata_examples.rst` | 該当 |
| 6 | ` M` | `ja/development_tools/testing_framework/implementation/testdata_notation.rst` | 該当 |

**「変更してよいファイル」以外は0件。判定: PASS。** 指示書の写し（`ntf-doc-23-table-zero-rows.md`）は着手時のコミット `664df75` で追加済みのため、ここには現れない。
