# task-13 Completion Check

`#13` ページ作成の共通手順を `steering.md` に定着させる。作業指示は `ntf-doc-13-standing-rules.md`。
基準コミット `9d94a38`（作業指示の配置と `#13` エントリ追加の直後）。**ページを作らないタスクであり、`ja/` 配下は1行も変更していない。**

変更したファイルは `steering.md` 1件のみである。`steering.md` は rn の役割定義上コーディネータが直接書く成果物であるため、実装サブエージェントには渡していない。

## 適用前に判明した既存項目の重複（STEP 1 の3項目目）

STEP 1 の3項目目「**ページ先頭ラベルは `style.md` S-08 の一覧から引く**」は、**`#12` の完了時に既に共通 Steps へ追加済み**であった。

実測（基準コミット `9d94a38` の時点）:

```
$ grep -n 'S-08' .rn/20260724-ntf-yaml-support/steering.md
282:- [ ] **ページ先頭ラベルは `style.md` S-08「NTF解説書のページ先頭ラベル一覧」から引く。新たに考案しない**（`#12` で34ページ分を確定済み。表に無いページが出た場合は勝手に命名せず `decide` としてユーザー判断に回す）
384:（`#12` エントリ）**以降のページ作成タスクは、ページ先頭ラベルを `style.md` S-08 の一覧から引く**（共通 Steps に追加済み）
```

`:282` は `#12` の締め（`f028322`）で入った行であり、STEP 1 の3項目目と同一の趣旨・同一の参照先（`style.md` S-08）である。同じ内容の行を2本並べると共通 Steps に重複が生じ、作業指示の「既存の項目は変更しない／追加のみとする」という方針にも反するため、**重複行は追加していない**。

したがって本タスクで追加した項目は **STEP 1 が3件（4件目は既存で充足済み）・STEP 2 が2件・STEP 3 が1段落**である。STEP 1 の4項目すべてが共通 Steps に存在する状態は達成されている。

## ゲート7相当（全件確認を先に置く）— 追加行の全件表

作業指示のゲート4「追加した項目が STEP 1 の4件・STEP 2 の2件・STEP 3 の1段落で、それ以外の追加が無いこと」は全件確認を求める項目であるため、`#10b` の申し送り（母集合をホワイトリストで切り出さない／全件表をゲート実行順の先頭に置く）に従い、**差分の全行を母集合として先頭で確認する**。

母集合は `git diff` の追加行**全件**であり、こちらで抽出条件を絞っていない。

```
$ git diff --numstat 9d94a38 -- .rn/20260724-ntf-yaml-support/steering.md
7	0	.rn/20260724-ntf-yaml-support/steering.md
```

追加7行・削除0行。その7行の全件は次のとおり。

| # | 新ファイルの行 | 由来 | 内容（先頭） |
|---|---|---|---|
| 1 | 255 | STEP 3 | `**個別の作業指示を出す条件**: **個別の作業指示は、次のいずれかに当たるページにのみ出す。** …` |
| 2 | 256 | STEP 3 | （空行。段落の区切り） |
| 3 | 286 | STEP 1-1 | `- [ ] **出典が述べている事実のうち、クラス名・プロパティ名・キー名・既定値・書式・桁数など実装で確かめられるものは、…** ` |
| 4 | 287 | STEP 1-2 | `- [ ] **第2部と第3部の記載範囲を守る**（`design.md` §3「記載範囲」）。…` |
| 5 | 306 | STEP 1-4 | `- [ ] **是正ラウンド2以降は、是正差分に限定した検証観点のみを回す。** …` |
| 6 | 317 | STEP 2-1 | `- 当該 `dest_page` のマッピング行が**全件**、ページのどこに反映されたかの対応表が `checks/task-NN.md` にある…` |
| 7 | 318 | STEP 2-2 | `- **全件表を求める項目は、ゲートの実行順の先頭に置く。母集合をホワイトリストで切り出さない**（`#10b` の申し送り）` |

由来が空欄の行・作業指示に対応しない行は**0件**。STEP 1-3（ページ先頭ラベル）は上記のとおり既存行 `:282` で充足しており、新規追加行は無い。

判定: **PASS**（追加はSTEP 1の3件＋既存1件・STEP 2の2件・STEP 3の1段落のみ。それ以外の追加0件）

## ゲート1 — `ja/` ・ `mapping/` ・ `design.md` の差分が空

```
$ git diff 9d94a38 HEAD -- ja/ .rn/20260724-ntf-yaml-support/mapping/ .rn/20260724-ntf-yaml-support/design.md | wc -l
0
```

あわせて、作業ツリー全体で変更のあるファイルが `steering.md` 1件のみであることも確認した。

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/steering.md
```

禁止事項に挙げられた `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `style.md` / `design.md` / `ja/conf.py` は、いずれも上記の1件に含まれないため未変更である。

判定: **PASS**

## ゲート2 — `verify_mapping.py` が exit 0、594行 / 12,986 / 11,983 が不変

```
$ python3 mapping/tools/verify_mapping.py ; echo exit=$?
Loaded 594 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
（中略。0 row(s) の advisory は `#6` 以降 optional。ERROR は無し）
OK: no errors
exit=0
```

スクリプトの出力を鵜呑みにせず、`csv.DictReader` で独立に数え直した（Rules「CSVのレコード数は `csv.DictReader` でカウントする」に従う。`wc -l` は使わない）。

```
$ python3 -c "
import csv
rows=list(csv.DictReader(open('mapping/mapping.csv',encoding='utf-8')))
print('rows =',len(rows))
print('lines total =',sum(int(r['lines']) for r in rows))
print('lines excl DROP =',sum(int(r['lines']) for r in rows if r['disposition']!='DROP'))
"
rows = 594
lines total = 12986
lines excl DROP = 11983
```

`#12` 承認時の確定値（594行 / 12,986 / 11,983）と一致。本タスクは `mapping/` を触っていないため当然ではあるが、独立計数でも不変を確認した。

判定: **PASS**

## ゲート3 — 差分が「#9〜: ページの作成」の節の中に収まり、削除行が0行

削除行数は上記 `--numstat` のとおり **0**。既存の Steps・完了条件・Rules の行に削除も変更も無い。

節の範囲は `steering.md` の見出し位置から機械的に確定した。

```
$ grep -n '^### ' .rn/20260724-ntf-yaml-support/steering.md | sed -n '/#9〜/,/#10a/p'
251:### #9〜: ページの作成（1ページにつき1タスク）
265:### #9: テストデータの書き方（`implementation/testdata_notation.rst`）— DONE
273:### #10: テストデータの記載例（`implementation/testdata_examples.rst`）— DONE
323:### #10a: 用語「テストショット」への統一と使用方法の並び替え — DONE
```

「#9〜: ページの作成」の節は **251行目から322行目**（次の `### #10a:` の直前）まで。`#9`・`#10` の完了エントリはこの節の内側に入れ子で置かれており、共通の `Steps（各ページ共通）`・`Completion criteria` はその後ろ、`#10a` の手前にある。

追加7行の位置は 255・256・286・287・306・317・318 で、**すべて 251〜322 の内側**にある（上記の全件表と一致）。節の外への差分は0件。

判定: **PASS**

## ゲート4 — 追加が STEP 1・2・3 のものだけで、それ以外の追加が無い

上記「ゲート7相当」の全件表のとおり。追加7行の全件に由来（STEP 1-1 / 1-2 / 1-4 / 2-1 / 2-2 / 3）が対応し、対応の付かない行は0件。

判定: **PASS**（ただし STEP 1 は3件＋既存1件。理由は冒頭の節を参照）

## 4観点のレビュー

作業指示の禁止事項により**回していない**。変更は共通 Steps・完了条件への7行の追加のみで、ゲート3が差分の位置と削除0行を、ゲート4（全件表）が追加行の全件を機械的に固定している。

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| 追加が STEP 1 の4件・STEP 2 の2件・STEP 3 の1段落のみで、それ以外の追加が無い | OK | ゲート4の全件表。追加7行すべてに由来が対応。STEP 1-3 は既存行 `:282`（`#12` で追加済み）で充足しており重複行は作っていない |
| `steering.md` の差分が節の中に収まり、既存の Steps・完了条件・Rules に削除・変更が無い（削除行0行） | OK | ゲート3。`--numstat` が `7 0`、追加位置 255〜318 はすべて節（251〜322）の内側 |
| `ja/` 配下の `.rst`・`mapping/`・`design.md` に差分が無い | OK | ゲート1。`git diff` が0行、`git status --porcelain` は `steering.md` 1件のみ |
| `verify_mapping.py` が exit 0 で、594行 / 12,986 / 11,983 が不変 | OK | ゲート2。`exit=0`・`OK: no errors`、`csv.DictReader` による独立計数でも 594 / 12,986 / 11,983 |
| ゲート1〜4 が実行結果で `checks/task-13.md` に記録されている | OK | 本ファイル。ゲート1〜4 すべて実行コマンドと出力付きで記録、NG 0件 |

## Overall Verdict

- Self-check: OK
- QA: N/A（作業指示により4観点のレビューを回していない）
- Design expert: N/A
- Craft expert: N/A
- Verification expert: N/A
- Ready to check off: Yes（ゲート1〜4 全件 PASS。user review の承認を待つ）

## 申し送り

- STEP 1 の3項目目が既存項目と重複していた件は、作業指示の側が `#12` の締めで共通 Steps に同項目が入ったことを織り込んでいなかったものである。以降、共通 Steps への追加を指示する作業指示を受けたときは、**着手前に既存の共通 Steps と突き合わせ、重複する項目は追加せず理由を記録する**。
