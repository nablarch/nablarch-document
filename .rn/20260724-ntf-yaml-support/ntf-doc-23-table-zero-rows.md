# `#23` 作業指示 — テーブルデータの0件の扱いを解説書に書く

宛先: CC（`nablarch-document` の `ntf-yaml-support`）
発行: レビュー役、2026-08-14

参照点

- `nablarch-document` = `cf0eb2f`（本書の `file:line` はこのコミットで開いて確かめたもの。対象2ページは `41909d4` から1行も変わっていないことを `git diff` で確認済み）
- `nablarch-testing` = `e21bf67`（`main` / タグ `2.2.0`）
- `nablarch-testing-yaml` = `190cc9a`（`feature/ntf-yaml` の最新。`a966ab9` ではない）

**本書は単独で完結している。** 2026-08-13 に受領した「`#22` 追加指示 — 期待値0件は仕様どおりに書く」と、そこで差し替え元とされていた `指示/task-22.md` は、いずれも本書に統合して破棄した。**両方を無視し、本書だけに従うこと。**

---

## 0. このタスクの位置づけ

**ページを作らないタスクである。** 承認済みの2ページに追記する。

| 項目 | 内容 |
|---|---|
| 変更してよいファイル | `ja/development_tools/testing_framework/implementation/testdata_notation.rst`／同 `testdata_examples.rst`／`reviews/page-testdata_notation.md`／`reviews/page-testdata_examples.md`／`checks/task-23.md`（新規）／`steering.md`／本書の写し（`.rn/20260724-ntf-yaml-support/ntf-doc-23-table-zero-rows.md`） |
| 変更してはならないファイル | `mapping.csv`／`mapping/_batch/`／`volume.md`／`vocabulary.md`／`style.md`／`glossary.md`／`design.md`／`ja/conf.py`／上記2ページ以外の `ja/` 配下すべて |

**4観点のレビューは回す。** 公開本文に新しい記述が入るためである（`#16`・`#18` のようなレビュー省略の対象ではない）。**依頼プロンプトには §7 の段落を必ず入れること。**

---

## 1. なぜ書くか

**テストデータのテーブルを0件で書く方法が、34ページのどこにも書かれていない。** `41909d4` の `ja/development_tools/testing_framework/` 配下を全文検索し、`rows: []`・「空にする」（テーブルの意味で）・「1件も」のいずれも該当0件であることを確認した。

準備データを0件にしてテーブルを空にすること、期待値を0件にしてレコードが1件も無いことを検証することは、いずれも読者が普通に必要とする書き方である。書き方が無いと読者は書けない。

**`design.md` §8「出典が書いていない適用範囲・副作用の追記」（`#21` 確定）に当たる。** 判定基準は「書かなければ読者が誤るか」であり、上記のとおり誤る。**`design.md` に新しい類型を追加しない。既存の類型で足りる。`design.md` を変更しないこと。**

出典・マッピングにこの主題の行は無い。`mapping.csv` を変更しないこと（§0の禁止事項）。

---

## 2. 実装の事実

**この節の事実はレビュー役が実物を開いて確かめたものである。同じ調査をやり直す必要はない。** ただし本文に書く前に、CC 側でも `file:line` を開いて突き合わせること（`steering.md` の共通 Steps）。

**事実18 は本文に反映しない。** 理由は §2-5。突合の対象には含める。

### 2-1 列名が0個だと SQL が発行されない（`nablarch-testing` `e21bf67`）

| # | file:line | 事実 |
|---|---|---|
| 1 | `src/main/java/nablarch/test/core/db/TableData.java:337-346` | `loadData()` は列名が0個のとき、空のリストを入れて `return` する |
| 2 | 同 `:348` | SELECT 文の組み立ては上のガードの**後**にある。つまり列名が0個なら SQL は発行されず、常に0行が返る |
| 3 | 同 `:489-493` | `setColumnNames` は長さ0の配列をそのまま代入する（`null` にはならない） |
| 4 | 同 `:501-505` | `getColumnNames()` がデータベースの全カラムに落ちるのは、列名が `null` のときだけ。長さ0の配列では落ちない |
| 5 | 同 `:706-722`（特に `:721`） | `fillDefaultValues()` は最後に `setColumnNames(allColumns)` を実行し、列名をデータベースの全カラムで置き換える |
| 6 | 同 `:127-130` | `deleteData` は `DELETE FROM <テーブル名>` であり、列名を使わない |
| 7 | 同 `:137-217`・`:325-334` | `insertData` は `getNonComputedColumns()`（＝データベースの全カラムから自動計算カラムを除いたもの）を使う。テストデータに書いた列名は使わない |

### 2-2 期待値の比較が素通りする経路（`nablarch-testing` `e21bf67`）

| # | file:line | 事実 |
|---|---|---|
| 8 | `src/main/java/nablarch/test/Assertion.java:79-83` | `assertTableEquals` は期待値を clone して `loadData()` した結果を実際の値にする。つまり**実際の値を読むときの列名は、期待値に書かれた列名である** |
| 9 | 同 `:259`・`:263`・`:306-313` | 比較はループ2つだけである。(a) 期待値の行数ぶん回して主キーが一致する行を探す、(b) `dbDataFound`（長さ＝実際の値の行数）を走査して、期待値に無いデータベース行を検出する。**期待値0行・実際の値0行では、どちらのループも1回も回らず無条件で成功する** |
| 10 | `src/main/java/nablarch/test/core/db/DbAccessTestSupport.java:363-369` | `failIfNoDataFound` が捕まえるのは「期待値のデータブロックが1つも見つからない」場合だけである。データブロックはあってカラム名が0個の場合は、このガードを通り抜ける |

### 2-3 Excel形式はカラム名の行から列名を取る（`nablarch-testing` `e21bf67`）

| # | file:line | 事実 |
|---|---|---|
| 11 | `src/main/java/nablarch/test/core/reader/TableDataParser.java:89-97`（`:94`・`:96`） | 識別子行の次の行をカラム名の行として読み、そこから列名を決める |
| 12 | `src/main/java/nablarch/test/core/reader/TestDataParsingTemplate.java:176-178` | 全セルが空の行は読み飛ばされる。したがって、識別子行の次に置いた空行はカラム名の行にならず、その次の行がカラム名の行になる |
| 13 | `src/main/java/nablarch/test/core/reader/BasicTestDataParser.java:171-181`（`:177`） | Excel形式では `EXPECTED_COMPLETE_TABLE` に対して `fillDefaultValues()` が実行される |

### 2-4 YAML形式はカラム名を行のキーから取る（`nablarch-testing-yaml` `190cc9a`）

| # | file:line | 事実 |
|---|---|---|
| 14 | `src/main/java/nablarch/test/core/reader/yaml/YamlSection.java:156-161` | `resolveColumns` は `rows` が空なら空のリストを返す |
| 15 | `src/main/java/nablarch/test/core/reader/yaml/YamlTableDataBuilder.java:110-115` | 列名0個のまま `TableData` を生成する。同 `:110-114` にこの状態が偽陰性になる旨の `FIXME` がある |
| 16 | 同 `:127` | `fillDefaults` が真なら `fillDefaultValues()` が実行される（事実5により列名がデータベースの全カラムに置き換わる） |
| 17 | `src/main/java/nablarch/test/core/reader/YamlTestDataParser.java:114` | `setup_tables` は `fillDefaults=false` |
| 18 | 同 `:123` | `expected_tables` は `fillDefaults=false` |
| 19 | 同 `:125` | `expected_complete_tables` は `fillDefaults=true` |

### 2-5 実装との関係（本文には書かない）

**現時点の `nablarch-testing-yaml`（`190cc9a`）では、`expected_tables:` に `rows: []` を書いても比較が行われない**（事実18・14・15 → 事実1・2・9）。**これを把握したうえで、§3 のとおり仕様として書く。** 本体側の対応は Kiyo さんが別途判断し、解説書に追随する。

したがって次を守ること。

- **`design.md` §8「出典と実装が食い違う場合は実装を優先する」を本件に適用しない。** これは 2026-08-13 のユーザー判断による例外であり、**`design.md` は変更しない**（§0 の禁止事項のまま）。判断そのものは §6 のとおり記録する
- **事実18 は、調べた結果として記録には残すが、本文には反映しない**

---

## 3. 書く内容

**次の3点だけを書く。これ以外を書かない。**

### 3-1 準備データを0件にすると、対象テーブルが空になる

準備データの投入は「対象テーブルを一旦全件 DELETE したうえで INSERT し直す」動作である（この事実は `testdata_notation.rst:666` に既に書かれている。**同じ説明を書き直さず、0件のときは DELETE だけが行われる、という形で接続する**）。したがって、テーブルを空の状態にしてテストを始めたい場合は、行を0件にした準備データを書く。

### 3-2 期待値を0件にすると、そのテーブルにレコードが1件も無いことの検証になる

**形式とデータタイプで場合分けしない。** Excel形式の `EXPECTED_TABLE`・`EXPECTED_COMPLETE_TABLE`、YAML形式の `expected_tables:`・`expected_complete_tables:` のいずれでも同じである。

書き方は形式ごとに次のとおり。

- Excel形式 — 識別子行とカラム名の行を書き、データ行を書かない（§3-3）
- YAML形式 — `rows: []`

### 3-3 Excel形式ではカラム名の行を省略できない

データ行を書かない場合でも、識別子行の次にカラム名の行を書く。カラム名の行を書かないと、次に現れた行がカラム名の行として読まれる（事実11・12）。

---

## 4. どこに書くか

### 4-1 `testdata_notation.rst` — 新しいL4見出しを1つ足す

**位置**: L3「テーブルのデータを記述する」（`:648`）の配下。**L4「カラムを省略する」（`:690`）の直後、L4「Excel形式の場合」（`:729`）の直前。**

**見出し**: `0件のデータを記述する`（下線は `^`。`style.md` S-04）

`style.md` S-10 規約3 が「形式別のL4対はそのL3の末尾2つに置く」と定めているため、この位置になる。**形式別のL4対を新しく作らないこと**（同規約は1つのL3に1組だけと定めている）。

**書く内容**: §3-1 と §3-2 の意味の説明のみ。書式（セル格子・コードブロック）はここに置かない。**形式差の説明を置かない**（§3-1・§3-2 はいずれも形式共通の説明である）。

**あわせて `:650` の1文を直す。** 現在「ここでは、準備データの記述上の注意とテストクラス全体で共通する準備データのまとめ方、期待値の記述上の注意、カラムの省略について説明する。」とあり、新しいL4がこの列挙から漏れる。0件の扱いを列挙に加えること。**この1文以外の `:650` の記述を変えないこと。**

### 4-2 `testdata_notation.rst` — 既存の形式別L4に書式を足す

- **L4「Excel形式の場合」（`:729`）** — カラム名の行だけを書いてデータ行を書かないセル格子を1つ足す。`style.md` S-10 規約2・規約4 に従う（識別子行を表の1行目に含める・`:header-rows: 0`・識別子は普通の文字）。§3-3 の注意もここに書く
- **L4「YAML形式の場合」（`:779`）** — `rows: []` の `code-block:: yaml` を1つ足す

いずれも既存の記述の後ろに足す。**既存の行を書き換えないこと**（`:762` の「ヘッダ行は末尾に空セルが続いても…」など）。

### 4-3 `testdata_examples.rst` — 新しいL3見出しを1つ足す

**位置**: L2「テーブルのデータを記述する」（`:778`）の配下。**L3「期待値（EXPECTED_TABLE・EXPECTED_COMPLETE_TABLE）を記述する」（`:864`）の直後、L3「採番処理のテストデータを記述する」（`:951`）の直前。**

**見出し**: `0件のテーブルデータを記述する`（下線は `~`）

**構成**: このページの他のL3と同じ型にする。導入文 → L4「Excel形式の場合」→ L4「YAML形式の場合」（`style.md` S-03 例外1 により、このページは全L3に形式別L4対を置く）。

**内容**: 準備データで対象テーブルを空にし、処理後にそのテーブルが空のままであることを検証する、という1つの場面で通す。準備データの0件と期待値の0件が1つの記述例に両方現れる形にすること。テーブルは既存のL3が使っている `MEMBER` などと揃える。

**期待値のデータタイプは `EXPECTED_TABLE`（Excel形式）／`expected_tables:`（YAML形式）を使う。** 0件を検証したいだけの場面で `EXPECTED_COMPLETE_TABLE` 系を選ぶ理由は無い（省略カラムのデフォルト値補完は、行が0件なら意味を持たない）。

`testdata_notation.rst` の新L4から、このL3へ `:ref:` を張る。ラベルは既存の命名にならって `testdata_examples-empty_table` とする（`style.md` S-08 はページ先頭ラベルの一覧であり、ページ内ラベルはこの表の対象外である）。

---

## 5. 書いてはいけないこと

- **不具合・バグ・将来の修正に類する記述**
- **現時点の実装の制約に触れる記述**（「一部のデータタイプでは検証されない」等）
- **`expected_complete_tables:`（`EXPECTED_COMPLETE_TABLE`）を、0件の検証のための手段として勧める記述**
- **カラム名の決まり方を、0件の文脈で理由として持ち出す記述**（`rows:` の先頭要素のキーから決まる、という説明は `:792` にある既存の記述のままにする。0件の説明に持ち込まない）
- **形式やデータタイプによって期待値0件の扱いが違うと読める記述**
- **`TableData`・`Assertion`・`YamlTableDataBuilder` などのクラス名**。第3部の記法ページであり、`design.md` §3「記載範囲」の対象でもない
- **マーカーカラムだけのカラム名の行**。列名0個になるもう1つの経路だが、現実に書かれる形ではなく、書くと読者を混乱させる
- **「読み込みが別のデータタイプで止まる」挙動**。`TestDataParsingTemplate.java:207-217` の挙動は0件に固有ではないため、本タスクでは扱わない
- **`{}` だけの行**（`rows: - {}`）の話。`:1500` の「空エントリ」で既に扱っており、重複になる

---

## 6. ゲート

**実行順どおりに実行し、結果を `checks/task-23.md` に記録する。**

| # | ゲート | 判定 |
|---|---|---|
| 1 | `git status --porcelain` の**全件**を表にする（`ja/` などに絞らない） | §0 の「変更してよいファイル」以外が0件 |
| 2 | §2 の事実19件を全件表にし、`file:line` を実際に開いた結果を1行ずつ記録する | 19件すべて一致。**事実18 は「記録のみ・本文に反映しない」と表に明記する。** 一致しないものがあれば**本文を書かずに報告する** |
| 3 | 変更した2ページの `ja/` 差分を全件表にする | 追加のみ。既存行の削除・書き換えは §4-1 の `:650` の1文のみ |
| 4 | 「不具合」「バグ」「将来」「修正され」を変更後の2ページで検索する | 0件 |
| 4a | `EXPECTED_COMPLETE_TABLE` と `expected_complete_tables` を変更後の2ページで検索し、全件表にする | **0件の説明の中に1件も現れない。** 既存の「カラムを省略する」等に現れるものは対象外。表にはすべて挙げたうえで対象外の理由を書く |
| 4b | 新しく足した記述の中で、期待値0件の扱いが形式・データタイプで場合分けされていないこと | 場合分け0件 |
| 5 | `TableData`・`Assertion`・`YamlTableDataBuilder`・`YamlSection`・`TableDataParser` を変更後の2ページで検索する | 0件 |
| 6 | 新しく足した見出しの下線を、`style.md` S-04 の実測則（L3 は `max(49, 表示幅)`、L4 も同じ扱い）で確認する | 逸脱0件 |
| 7 | 新しく足した形式別L4対が0組であること（`testdata_notation.rst`）、1組であること（`testdata_examples.rst` の新L3） | S-10 規約3 に適合 |
| 8 | `:ref:` の参照先ラベルが実在すること | `undefined label` 0件 |
| 9 | `python3 mapping/tools/verify_mapping.py` | `exit 0`・595行 / 12,986 / 11,983 が不変 |
| 10 | `mapping.csv`・`_batch/`・`volume.md`・`vocabulary.md`・`style.md`・`glossary.md`・`design.md`・`ja/conf.py` の差分 | 0件 |
| 11 | Docker フルビルド（`-a`） | `build succeeded`・警告は既知の `db_double_submit.rst:108` のみ・新規0件。**直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo`** |
| 12 | ゲート1 を `commit & push` の直前にもう一度実行する | 同上 |

**`verify_glossary.py` はゲートに入れない**（`#22` からの扱いと同じ。`#pre-last` で一括是正する）。

---

## 7. レビューサブエージェントへの申し送り

**4観点のレビューを依頼するプロンプトに、次の段落をそのまま入れること。** 入れないと、観点A（網羅性）と観点D（整合性）が実装との不一致を `must` として挙げ、`expected_complete_tables:` へ限定する修正を提案してくる。

> 本ページの「期待値のデータ行を0件にすると、そのテーブルにレコードが1件も無いことの検証になる」という記述は、`expected_tables:` について、現時点の `nablarch-testing-yaml`（`190cc9a`）の挙動と一致しない。**これはユーザー判断による意図的なものであり、テスティングフレームワーク本体が追随する。** この不一致を指摘しないこと。`expected_complete_tables:` に限定する修正、実装の制約を注記として足す修正、いずれも提案しないこと。それ以外の観点は通常どおり敵対的にレビューすること。

---

## 8. 記録

- `checks/task-23.md`（新規）— ゲート1〜12 の実行結果
- `reviews/page-testdata_notation.md` — 追記した内容と、`design.md` §8「出典が書いていない適用範囲・副作用の追記」に当たると判断した理由。**§2 の19件の `file:line` と参照コミット（`e21bf67`・`190cc9a`）を記録する**
- `reviews/page-testdata_examples.md` — 同上（記載例側の追加分）
- `steering.md` — `#23` のエントリを追加する

**申し送りとして次を残すこと**（`reviews/page-testdata_notation.md`）。

> `expected_tables:` に `rows: []` を書いたときの期待値0件の検証は、`190cc9a` 時点の `nablarch-testing-yaml` では行われない。**解説書は、本体が追随する前提で仕様どおりに書いている**（2026-08-13 ユーザー判断）。本体の対応が入るまで、この記述は実装に先行している。本体の対応方針が決まった時点で、`testdata_notation.rst` の「0件のデータを記述する」と「YAML形式の場合」、`testdata_examples.rst` の「0件のテーブルデータを記述する」の3箇所を見直す。

あわせて `reviews/page-testdata_notation.md` と `checks/task-23.md` の双方に、**`design.md` §8 の実装優先の原則を本件に適用しないというユーザー判断があったこと**を1段落で記録する。`design.md` への規定化は本タスクでは行わない（同種の判断が再度出た時点で判断する）。

---

## 9. 判断が要る場合

§2 の事実と実物が食い違った場合、および §4 の位置が `style.md` の規約と両立しない場合は、**本文を書かずに報告すること。** 位置を自分で変えない。

**タスク番号 `#23` は仮である。** `steering.md` 上で別の番号を割り当てる必要があれば、CC 側で決めてよい。その場合は `checks/task-NN.md` のファイル名もあわせること。
