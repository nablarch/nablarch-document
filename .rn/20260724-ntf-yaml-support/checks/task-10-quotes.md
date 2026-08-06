# self-check: `#10` セル値の描画忠実性と規約のスコープ

作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-10-quotes.md`
対象ブランチ: `work`（`38ad208` の続き）
実施日: 2026-08-07

`#10` の user review 差し戻し（`/rn:gm`）に対する2回目の対応である。1回目（セル格子への
識別子行追加）の記録は `checks/task-10-cellgrid.md`。

---

## 1. STEP 1 — ダブルクォートの描画の是正（`must`）

### 1-1. 事実の確認

`ja/conf.py` に `smartquotes` の設定が存在しないことを確認した。Sphinx の既定値は有効である。

```
$ grep -n "smartquote\|smart_quotes" ja/conf.py
(no smartquotes setting)
```

したがって、リテラル記法（`` `` ``）の外にある素のダブルクォートは丸クォート（`”`）に
変換されて描画される。

### 1-2. 是正した4セル

指示の対象4セルを、値を変えずにリテラル記法で囲んだ。

| 行（是正後） | セルの値 | 文脈 | 対応 |
|---|---|---|---|
| L1432 | `"` | `quoting-delimiter` ディレクティブの設定値 | `` `` `` で囲んだ |
| L1445 | `"hello, world"` | `NOTE` カラムのデータ | `` `` `` で囲んだ |
| L1939 | `" "` | `NAME` カラムのデータ（半角スペース1文字） | `` `` `` で囲んだ |
| L1940 | `"""` | `MEMO` カラムのデータ（ダブルクォート1文字） | `` `` `` で囲んだ |

値そのものは変えていない。`"""` は `"""` のままである（`git diff` で確認、§6 ゲート12）。

### 1-3. 横並び確認（全数走査）

両ページの全 `list-table` のセルを機械抽出し、リテラル記法（`` `` ``）の外に
`"` `'` `“` `”` `‘` `’` を含むセルを走査した。走査スクリプトは以下の手順で動作する。

1. `.. list-table::` ディレクティブを検出し、そのインデントより深い行をディレクティブ本体とする
2. 本体のうち、空行とオプション行（`:` で始まる行）を除いた行を対象とする
3. 行頭の箇条書きマーカー（`* - ` / `- `）を剥がしてセル値を得る
4. セル値から `` ``...`` `` にマッチする範囲を除去し、残りにクォート文字が含まれるかを判定する

**走査結果（是正後）**

```
=== ja/development_tools/testing_framework/implementation/testdata_examples.rst ===
list-table 件数: 49
該当セル件数: 0
=== ja/development_tools/testing_framework/implementation/testdata_notation.rst ===
list-table 件数: 34
該当セル件数: 0
```

**スクリプトの妥当性確認** — 同じスクリプトを是正前（`38ad208`）の両ファイルに対して実行し、
指示が挙げた4件を過不足なく検出することを確認した。0件という結果が「検出できていないだけ」で
ないことの裏付けである。

```
=== before/testdata_examples.rst ===
list-table 件数: 49
該当セル件数: 4
  L1432	["]	    - "
  L1445	["]	    - "hello, world"
  L1939	["]	    - " "
  L1940	["]	    - """
=== before/testdata_notation.rst ===
list-table 件数: 34
該当セル件数: 0
```

**結論**: 指示の4件以外に該当は無かった。`testdata_notation.rst` は是正前から0件である。

### 1-4. 表の外（地の文）の確認（指示範囲外・参考）

`list-table` / `code-block` / `literalinclude` の本体を除いた全行についても同じ判定を行い、
両ページとも **0件** であることを確認した。地の文に素のクォートは存在しない。

`testdata_notation.rst` の模式表にある `...`（L992・L996・L1000・L1004・L1008 付近）は、
指示のとおり**対象外**とし、手を入れていない。省略記号であり、写して動くことを意図した
値ではない。

---

## 2. STEP 2 — 行番号を指す表現の全数確認

### 2-1. 抽出方法

両ページの全行に対し、位置を指す表現を正規表現で全数抽出した。取りこぼしを防ぐため
2段階で走査している。

- **狭い走査**（行位置そのものを指す語）: `N行目` / `N列目` / `先頭行` / `最終行` / `末尾行` /
  `先頭の行` / `最後の行` / `最初の行` / `次の行` / `直後の行` / `直前の行` / `上の行` / `下の行` /
  `同じ行` / `N番目の行` / `N番目の列` / `先頭列` / `最終列` / `Nつ目の行`
- **広い走査**（列位置・件数・行内位置を指す語。誤って行位置を指していないかの確認用）:
  `先頭要素` / `先頭のセル` / `先頭のキー` / `末尾のセル` / `末尾の行` / `末尾に` / `末尾で` /
  `行頭` / `行末` / `最上段` / `最下段` / `N件目` / `Nつ目` / `セル行` / `その行` / `この行` ほか

抽出件数は狭い走査9件、広い走査25件（うち4件は狭い走査と重複）。**重複を除いた30件すべてを
以下に判定して掲げる。**

### 2-2. 判定表A — 行位置を指す表現（9件）

| # | ファイル | 行 | 表現 | 指しているもの | 判定 |
|---|---|---|---|---|---|
| A1 | examples | L137 | `先頭行` | Excel シートのデータブロックの先頭行（＝識別子行） | **正しい。現状維持。** 直前の4表（L69・L82・L101・L124）はいずれも `:header-rows: 0` で識別子行を1行目に持つ。印刷された表の先頭行とシートの先頭行が一致しており、どちらに読んでも識別子行を指す |
| A2 | notation | L360 | `` `rows:` の先頭行 `` | YAML の `rows:` 配列の先頭要素 | **対象外。現状維持。** Excel シートの行でも RST の表の行でもない |
| A3 | notation | L466 | `ヘッダ行（2行目）` | Excel シートの行 | **正しい。現状維持。** 直前の T07（L437）が識別子行を持つセル格子（`:header-rows: 0`）であり、シート上の行番号（1行目＝識別子行、2行目＝ヘッダ行）がそこで確立している |
| A4 | notation | L479 | `データ行（3行目以降）` | Excel シートの行 | **正しい。現状維持。** A3 と同じ根拠 |
| A5 | notation | L496 | `最初の行（``rows:`` の先頭要素）` | YAML の `rows:` 配列の先頭要素 | **対象外。現状維持。** 括弧内で YAML の要素であることを明示している |
| A6 | notation | L561 | `1行目` / `2行目` / `3行目以降` | Excel シートの行 | **正しい。現状維持。** 「1行目に `LIST_MAP=` に続けて ID を記載する」であり、識別子行を1行目と数えている。直後に表は無く `:ref:` で記載例へ送っている |
| A7 | notation | L678 | `先頭行`（テストケース一覧・リクエストパラメータ表） | 2つのデータブロックのデータ行同士の対応関係 | **対象外。現状維持。** 絶対的な行番号ではなく「行の順序で結び付く」ことの説明であり、識別子行の有無で意味が変わらない |
| A8 | notation | L1031 | `次の行` | Excel シート上の相対位置（レコードの続き） | **対象外。現状維持。** 相対位置であり識別子行の追加に影響されない |
| A9 | notation | L1451 | （旧）`2行目でテーブルの論理名を` | 直後の T32（L1453）の表の行 | **是正済み。**「ヘッダ行の下の行でテーブルの論理名を」に改めた |

**A9 の判断根拠** — T32（L1453）は識別子行を持たない断片である（`checks/task-10-cellgrid.md`
§6-2 で対象外と判定した3件のうちの1件）。印刷された表では確かに2行目が `// 番号` の行だが、
シート上では1行目が識別子行であるため、シートの行として読むと2行目はヘッダ行になり食い違う。
指示の「シートの行と誤読されないかを確認し、紛らわしい場合は行番号を使わない表現に改める」に
従い、行番号を使わない表現に改めた。表を実際に確認し、`// 番号` の行がヘッダ行（`NO` /
`FIRST_NAME` …）の直下にあることを確かめている（L1457〜L1466）。

### 2-3. 判定表B — 列位置・件数・行内位置を指す表現（21件）

いずれも**行位置を指していない**ため、識別子行の追加による影響を受けない。全件現状維持。

| # | ファイル | 行 | 表現 | 指しているもの |
|---|---|---|---|---|
| B01 | examples | L790 | `1件目` | 記述例の通し番号 |
| B02 | examples | L806 | `2件目` | 記述例の通し番号 |
| B03 | examples | L1032 | `先頭要素` | 行内の列位置（レコード種別行の1列目） |
| B04 | examples | L1055 | `先頭要素` | 行内の列位置（データ行の1列目） |
| B05 | examples | L1596 | `先頭要素` | 行内の列位置（ラベル列） |
| B06 | examples | L1760 | `先頭要素` | 行内の列位置（ラベル列） |
| B07 | examples | L2006 | `先頭要素` | 行内の列位置（`//` コメントの判定位置） |
| B08 | examples | L2017 | `この行` | 表のセルに書かれたコメント本文そのもの |
| B09 | examples | L2032 | `この行` | 表のセルに書かれたコメント本文そのもの |
| B10 | examples | L2045 | `行頭` / `行末` | YAML の1行の中の位置 |
| B11 | examples | L2052 | `この行` | `code-block` 内のコメント本文そのもの |
| B12 | notation | L160 | `2件目` | データブロックの件数（先着一致の説明） |
| B13 | notation | L175 | `2件目` | データブロックの件数（先着一致の説明） |
| B14 | notation | L390 | `末尾に` | 文字列（タイムスタンプ）の末尾 |
| B15 | notation | L555 | `2件目` | データブロックの件数（先着一致の説明） |
| B16 | notation | L973 | `先頭要素` | 行内の列位置（データの1列目） |
| B17 | notation | L1234 | `先頭要素` | 行内の列位置（ラベル列） |
| B18 | notation | L1236 | `先頭要素` | 行内の列位置（フィールド名称行の1列目） |
| B19 | notation | L1326 | `末尾に` | 文字列（タイムスタンプ）の末尾 |
| B20 | notation | L1478 | `先頭要素` / `行頭` / `行末` | 行内の列位置・YAML の1行の中の位置 |
| B21 | notation | L1511 | `行末` | 行内の位置（末尾の空セル） |

### 2-4. 指示が特に挙げた4箇所の突合

| 指示の記載 | 本記録での該当 | 結果 |
|---|---|---|
| `testdata_notation.rst` L466 `ヘッダ行（2行目）` | A3 | 正しい。現状維持 |
| `testdata_notation.rst` L479 `データ行（3行目以降）` | A4 | 正しい。現状維持 |
| `testdata_notation.rst` L561 `1行目に LIST_MAP= …` | A6 | 正しい。現状維持 |
| `testdata_notation.rst` L1451 `例えば以下のように、2行目で…` | A9 | 是正済み |
| `testdata_examples.rst` L137 `先頭行の識別子で決まる` | A1 | 正しい。現状維持 |

---

## 3. STEP 3 — `style.md` S-10 規約2 へのスコープ条件の追記

規約2 の末尾に次の2行を追記した。観点は11個のまま、規約2 以外は変更していない。

```
- **複数のデータタイプに共通する規則を示すための断片は、識別子行を持たなくてよい。**
  識別子を1つ選ぶと、その規則が特定のデータタイプ専用であるかのように読めてしまう
  ためである。特定のデータブロックの記述例を示す表には、識別子行を含める
```

これにより、`checks/task-10-cellgrid.md` §6-2 で「要判断」として残した `#9` の3件
（T11 L530・T32 L1453・T33 L1484）が、規約上も現状維持で正しいことになる。3件はいずれも
複数のデータタイプに共通する規則を示す断片である。

| 表 | 行 | 示している規則 | 特定のデータタイプ専用か |
|---|---|---|---|
| T11 | L530 | `LIST_MAP` と `List<Map>` の等価性 | いいえ（読み込み結果の構造の説明） |
| T32 | L1453 | `//` によるコメントの切り捨て | いいえ（カラム名を持つ全データブロック共通） |
| T33 | L1484 | マーカーカラムによる読み込み除外 | いいえ（`SETUP_TABLE`・`EXPECTED_TABLE`・`LIST_MAP` 共通） |

3件に識別子行は追加していない（指示の禁止事項）。

---

## 4. STEP 4 — 記録

- 本ファイル（`checks/task-10-quotes.md`）を新規作成した
- `reviews/page-testdata_examples.md` に「`#10` 差し戻し対応（2回目）」の節を**追記**した。
  既存の記録は書き換えていない
- 同ファイルの `#11` 以降への申し送りに、リテラル記法で囲む旨を追加した（申し送り11）。
  あわせて、smartquotes を未決事項として残していた既存の申し送り10 の決着を記録した

---

## 5. ゲートの実行結果

### ゲート1 — `verify_mapping.py`

```
$ cd .rn/20260724-ntf-yaml-support && python3 mapping/tools/verify_mapping.py; echo "EXIT=$?"
Loaded 594 rows from mapping.csv

pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11983
...
OK: no errors
EXIT=0
```

594行 / 12,986 / 11,983 で不変。**PASS**

### ゲート2 — マッピング成果物に差分が無いこと

```
$ git diff 38ad208 HEAD -- .rn/.../mapping.csv .rn/.../_batch/ .rn/.../vocabulary.md .rn/.../glossary.md
(出力なし)
$ git status --short .rn/20260724-ntf-yaml-support/mapping/
 M .rn/20260724-ntf-yaml-support/mapping/style.md
```

差分は `style.md`（STEP 3 で追記したもの）のみ。`mapping.csv` / `_batch/` /
`vocabulary.md` / `glossary.md` に差分は無い。**PASS**

### ゲート3 — `ja/conf.py` に差分が無いこと

```
$ git status --short ja/conf.py
(出力なし)
$ git diff -- ja/conf.py
(出力なし)
```

**PASS**

### ゲート4 — リテラル記法の外の素のクォートが0件

§1-3 の走査結果のとおり、両ページとも0件。スクリプトの妥当性は是正前の4件検出で確認済み。
**PASS**

### ゲート5 — 見出し数が不変

```
$ grep -cE "^-{3,}$"  testdata_examples.rst  → 9    (L2)
$ grep -cE "^~{3,}$"  testdata_examples.rst  → 28   (L3)
$ grep -cE "^\^{3,}$" testdata_examples.rst  → 56   (L4)
$ grep -cE "^-{3,}$"  testdata_notation.rst  → 3
$ grep -cE "^~{3,}$"  testdata_notation.rst  → 10
$ grep -cE "^\^{3,}$" testdata_notation.rst  → 26
```

`testdata_examples.rst` は L2 9 / L3 28 / L4 56、`testdata_notation.rst` は
`-` 3 / `~` 10 / `^` 26。いずれも指示の値と一致。**PASS**

### ゲート6 — `:header-rows: 0` の表の件数が不変

```
$ grep -c "header-rows: 0" testdata_examples.rst  → 47
$ grep -c "header-rows: 0" testdata_notation.rst  → 2
```

**PASS**

### ゲート7 — `style.md` の観点が11個

```
$ grep -nE "^#+ *S-[0-9]+" mapping/style.md
18:### S-01 文体（だ・である調）
33:### S-02 ページのセクション構成
89:### S-03 セクションタイトルの形式（「〜する」形式）
146:### S-04 見出しのアンダーライン記法とレベル対応
174:### S-05 コードブロックのインデント幅と言語指定
192:### S-06 アドミニション（tip / note / important）の使い分け
217:### S-07 表の記法
261:### S-08 `:ref:` ラベルの命名規則
282:### S-09 各ページ先頭の目次（`.. contents::` ディレクティブ）
316:### S-10 Excel形式/YAML形式の書き分け方
430:### S-11 L4見出しを持つL3セクションの導入文
```

11個で不変。**PASS**

### ゲート8 — 行番号を指す表現の全件判定表

§2-2（表A・9件）・§2-3（表B・21件）に全30件を掲げた。件数のみの報告はしていない。**PASS**

### ゲート9 — `:ref:` の未定義参照0件・段落内改行0件

段落内改行の走査（インデント0の地の文が空行を挟まず連続する箇所）:

```
testdata_examples.rst: 段落内改行 0件
testdata_notation.rst: 段落内改行 0件
```

未定義参照はゲート10 のビルドログで確認する。**PASS**

### ゲート10 — Docker フルビルド

```
$ docker run --rm -v /home/tie303177/work/lovaizu/nablarch-document:/root/document \
    nablarch-document-build-sandboxed /bin/bash -c \
    "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
...
build succeeded, 1 warning.
BUILD_EXIT=0
```

警告の全文（1件のみ）:

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108:
WARNING: undefined label: how_to_set_token_in_request_unit_test
(if the link has no caption the label must precede a section header)
```

既知の `db_double_submit.rst` 1件のみ。新規警告0件、ERROR 0件、`Malformed table` 0件。
未解決参照系（`undefined label` / `toctree contains reference to nonexisting document` /
`unknown document`）は上記の既知1件のみで、両ページ由来は0件。**PASS**

（この既知警告は `#7` で削除した現行解説書のラベルを指すもので、`#last` で解消する。
`checks/task-07.md`「リンク切れになる参照」参照。）

### ゲート11 — 描画結果の確認

`_build/html/development_tools/testing_framework/implementation/testdata_examples.html` の
該当4箇所を実際に読んだ。いずれも `&quot;`（直線のダブルクォート `"`）で出力されている。

**(1) `quoting-delimiter` ディレクティブの設定値**

```html
<td>quoting-delimiter</td> <td><code class="docutils literal"><span class="pre">&quot;</span></code></td>
```

**(2) `NOTE` カラムのデータ**

```html
<td>001</td>
<td><code class="docutils literal"><span class="pre">&quot;hello,</span> <span class="pre">world&quot;</span></code></td>
<td>5000</td>
```

**(3)(4) `NAME` カラム・`MEMO` カラムのデータ**

```html
<tr class="row-even"><td>ID</td> <td>NAME</td> <td>MEMO</td> </tr>
<tr class="row-odd"><td>1</td>
  <td><code class="docutils literal"><span class="pre">&quot;</span> <span class="pre">&quot;</span></code></td>
  <td><code class="docutils literal"><span class="pre">&quot;&quot;&quot;</span></code></td>
</tr>
```

`"""` は3個のまま保たれている（値を変えていない）。

**ページ全体の丸クォート出現数**

```
“: 0   ”: 0   &#8220;: 0   &#8221;: 0
```

**PASS**

#### smartquotes が実際に有効であることの実証

「設定が無いから既定で有効なはず」という推測ではなく、同じビルド成果物で実際に変換が
起きていることを確認した。

- 変換元（RST ソース、素のダブルクォート）:
  `ja/application_framework/application_framework/libraries/tag.rst:81`

  ```
  HTMLの中では「<」「>」「"」といった文字は、特別な意味を持つため、
  ```

- 変換後（HTML）: `_build/html/.../libraries/tag.html`

  ```html
  <p>HTMLの中では「&lt;」「&gt;」「&#8221;」といった文字は、特別な意味を持つため、
  ```

素の `"` が `&#8221;`（右丸クォート `”`）に変換されている。したがって STEP 1 の是正は
必要な対応であり、リテラル記法で囲んだことで変換を回避できていることが、上記(1)〜(4)の
`&quot;` 出力によって裏付けられる。

なお本リポジトリの Sphinx は 1.3.6・docutils 0.15.2 であり、`smartquotes` という名前の
Sphinx 設定値自体は存在しない（Sphinx 1.6.6 で追加されたもの）。変換は docutils 側の
smart_quotes 機構によって行われている。`ja/conf.py` に設定が無いという事実の確認に加えて
上記の実測を行ったのはこのためである。**是正の要否の結論は指示のとおりで変わらない。**

### ゲート12 — 情報の欠落が無いこと

```
$ git diff --numstat
3	0	.rn/20260724-ntf-yaml-support/mapping/style.md
4	4	ja/.../implementation/testdata_examples.rst
1	1	ja/.../implementation/testdata_notation.rst

$ git diff -U0 | grep -E "^-[^-]"
-    - "
-    - "hello, world"
-    - " "
-    - """
-**Excel\ 形式**\ では、…例えば以下のように、2行目でテーブルの論理名を、末尾で…
```

削除行は5行のみで、内訳は **STEP 1 の4セル**（同じ値をリテラル記法で囲んだ行に置換）と
**STEP 2 の A9**（L1451 の1文。行番号を使わない表現に置換）である。STEP 3 の `style.md` は
3行の追加のみで削除0行。**STEP 1〜3 に由来しない削除は無い。PASS**

---

## 6. 判断を仰ぐ事項

**なし。** `checks/task-10-cellgrid.md` §6 に「要判断」として残していた3件は、いずれも本作業で
決着した。

| §6 の項目 | 決着 |
|---|---|
| 6-2 `#9` の対象外セル格子3件（L530・L1453・L1484） | 現状維持で承認。STEP 3 で `style.md` S-10 規約2 にスコープ条件を明記した |
| 規約4 の参照整合 | 承認。取り消していない |
| smartquotes によるダブルクォートの描画 | `must` として STEP 1 で是正。ゲート11 で描画を実測確認 |

## 7. 禁止事項の遵守

| 禁止事項 | 確認 |
|---|---|
| `ja/conf.py` を変更しない | ゲート3 で差分0を確認 |
| `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` を変更しない | ゲート2 で差分0を確認 |
| 4セルの値そのものを変えない | ゲート12 の差分と §5 ゲート11 の描画で確認（`"""` は3個のまま） |
| `#9` の3件のセル格子に識別子行を足さない | ゲート6 で `:header-rows: 0` が2件のまま、ゲート5 で見出し数不変を確認。当該3表に差分なし |
| `testdata_notation.rst` の模式表の `...` に手を入れない | 差分は L1451 の1行のみ（ゲート12） |
| 承認済みの作業を取り消さない | 差分は追加5行・削除5行のみで、いずれも STEP 1〜3 由来 |
| `style.md` の観点を11個から増やさない・規約2 以外を変更しない | ゲート7 で11個を確認。差分は規約2 への3行追記のみ |
| 判定を件数だけで報告しない | §1-3 に走査結果全文、§2-2・§2-3 に全30件の判定表を掲載 |
| 既存のレビュー記録を書き換えない | `reviews/page-testdata_examples.md` は節の追記のみ |
| user review の承認を受けるまで `#11` に着手しない | 未着手 |
