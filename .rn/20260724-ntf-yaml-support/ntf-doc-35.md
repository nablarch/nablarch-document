# 作業指示 #35: `#32` の是正3 が残した記述の誤り4件を直す

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support（`82322fa`）
`ja/` 配下のパスは ja/development_tools/testing_framework/ からの相対。
行番号は `82322fa` の作業ツリーのもの。

`#32` は完了条件を満たしており閉じたままにする。以下は `#32` の記述に残った誤りの是正であり、
`steering.md` に `### #35` として起こしてから着手する。是正ラウンドの上限は改めて3回。

---

## 判定

報告の5件はすべて指摘のとおりだった。1・2・3 は同じ1段落に集まるので1か所の書き換えで片づく。
4 は台帳と `design.md` の2か所。5 は既に実測どおりに直っているので作業は無い。

**5 について。**「7行のうち6行は役割が本文に残っていない」と書いたのは私の誤りである。
残っていないのはクラス名であって役割ではない。5行/2行という実測が正しいことは、
`implementation/request_unit_test/batch.rst:17`・同 `mom.rst:17`・同 `rest.rst:10`/`:15`/`:17`・
同 `web.rst:10`/`:42`/`:44` と、`grep -rn '実行環境' ja/development_tools/testing_framework/implementation/request_unit_test/`
が0件であることを自分で開いて確かめた。`design.md` の現行の記述で正しい。

---

## 1. `tools/testdata_converter.rst:71` の段落を書き換える（報告1・2・3）

3件とも成り立つことを確認した。

**適用範囲**（報告1）—— `HeaderLine` のコンストラクタが `trimTailCopy` を呼ぶ
（`nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/reader/HeaderLine.java:33`）。
呼び出し元は同 `ListMapParser.java:64` と同 `TableDataParser.java:93` で、
変換ツールは `TestCoreReaderAdapter.readTables`／`readListMap` からこの2つを使う
（`nablarch-testing-converter@e977824` の
`src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:85`・`:99`）。
さらに `HeaderLine.java:77` の `excludeMarkerColumns` はカラム名の行の長さでループするため、
データ行の側もその幅を超えたセルは中間モデルに入らない。
判断A で辿った3か所は変換ツール側の呼び出し元だけで、この経路が漏れていた。

**語の前例**（報告2）—— `grep -rn 'メッセージのテストデータ' ja/` は `:71` の1件のみ、
`grep -rn '電文のテストデータ' ja/` は8件。

**語義の衝突**（報告3）—— このページの「整形」は同 `:63`・`:247`・`:249` で
書き出し時の装飾に固定されている。

**直し方は、範囲を書き分けるのではなく落とす。** 同 `:69` のマーカーカラムの段落と同じ形にする。
そうすると3件が同時に解ける。

```
変更前
ファイルとメッセージのテストデータでは、\ Excel\ 形式から読み込むときに行末の空セルが取り除かれる。取り除かれたあとの状態が中間モデルに入るため、\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換すると、行末の空セルは変換後に現れない。\ YAML\ 形式から読み込むときは ``rows:``\ の各要素をそのまま扱うため、この整形は行われない。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。

変更後
行末の空セルは往復すると消える。テスティングフレームワークが\ Excel\ 形式を読み込む時点で取り除くため、中間モデルに入らない。\ YAML\ 形式から読み込むときは ``rows:``\ の各要素をそのまま扱うため、この処理は行われない。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
```

**この段落は「取り除く」を無限定に述べるので、書く前に反例を探すこと。**
`XlsFormatReader` が読むデータタイプはテーブル系・`LIST_MAP`・メッセージ・ファイル系・
同期応答電文の5系統である（`nablarch-testing-converter@e977824` の
`src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:146`・`:179`/`:182`・
`:229`/`:240`・`:206`/`:212`・`:268`/`:274`）。
5系統すべてで行末の空セルが落ちることを実装から確かめ、確かめた経路を
`reviews/page-testdata_converter.md` に記録する。
**1系統でも落ちない経路が見つかったら、この段落は書かずに報告すること。**

---

## 2. `implementation/testdata_notation.rst` の表に行を足す（報告1の裏返し）

`:1544`-`:1545` の行は対象を「ファイル・メッセージ」に限っており、
`HeaderLine.java:33` の経路を拾っていない。`:1545` の直後に1行足す。
既存の `:1544`-`:1545` は変えない（ファイル・メッセージでは行ごとに取り除かれる、で正しい）。

```
  * - テーブル・\ ``LIST_MAP``
    - カラム名の行の行末の空セルを取り除く。カラム名が無い位置のセルは読み込まれない（\ Excel\ 形式のみ）
```

インデントと記法は同じ `list-table` の既存行に合わせること。
`LIST_MAP` をコードリテラルで書くのは同ページ `:1532`・`:1534` の用法に合わせたもの。

`reviews/page-testdata_notation.md` に、この行の出典（`HeaderLine.java:33`・`:77`、
`ListMapParser.java:64`、`TableDataParser.java:93`。いずれも `nablarch-testing@e21bf67`）を記録する。

---

## 3. 台帳5行の `note` から列挙を外す（報告4）

指摘のとおり、5行の `note` に現れるクラス名は8件で7行と合わない。
`mom.rst` の表の出典が `current-0296`・`current-0323` の2行に分かれており、
両方の `note` に `StandaloneTestSupportTemplate` が入るためである。
**行ごとの列挙をやめてポインタだけにする。** 内訳は `design.md` にあり、
`design.md` §「マッピング台帳の運用」が `note` を1〜2文のポインタに留めると定めている。

`mapping.csv` の直接編集は禁止。`mapping/_batch/*.csv` を直してから昇順連結で作り直す
（先頭ファイルのみヘッダ込み）。

対象は `current-0201`・`current-0282`・`current-0296`・`current-0309`・`current-0323` の5行。
各行の `note` 末尾にある「なお同じ基準で 9031fa6 が …… の行を落としている（内訳は design.md 同節）。」を、
次の一文に置き換える。

```
なお 9031fa6 も同じ基準でこの表から行を落としている（内訳は design.md 同節）。
```

`disposition` を含む他の列は1文字も変えない。

---

## 4. `design.md` の2か所を、列挙を外したことに合わせて直す

どちらも §「利用側ページに内部構造の構成図を置かない」の中にある。
**この節の他の記述は変えないこと。**

**4-1. `:147` の件数の説明。** 「マッピング台帳の `note` 末尾に `9031fa6` の分として書き足した
……の一文だけを数えると、この7行の名前は8件現れる（……）。7行に対して1件多いのは、……ためである。」
を、列挙を外した事実の記述に置き換える。書く内容は次の2点だけ。

- `note` 末尾に書き足したのは `current-0201`・`current-0282`・`current-0296`・`current-0309`・
  `current-0323` の5行で、クラス名は列挙せず本節を指すだけにした。
- 行ごとに列挙しないのは、`mom.rst` の表の出典が `current-0296`・`current-0323` の2行に分かれており、
  列挙すると同じクラス名が二重に数えられるためである。

**4-2. `:143` の括弧書きの末尾。** 「同じマーカーの配下には `9031fa6` が落とした行の名前も書いてあるが、
それはこの11件に含まない」は、3 を適用すると成り立たなくなる。この一文を削る。
括弧内の `current-0201` の3件から `current-0323` の1件までの列挙と「計11件」は変えない
（この11件は是正2 で落とした名前の数であり、3 の変更の影響を受けない）。

---

## 5. `design.md:147` を読める単位に割る（文言は変えない）

`:147` は1段落で2600字を超え、7行の内訳が地の文に埋まっている。
後から読む人が使えるように、リード文＋箇条書きに割る。

**文言は1文字も変えない。** 文の順序も変えない。行頭に `- ` を付け、
改行を入れるだけにする。既存の `(1)`〜`(5)` の番号付けはそのまま各項目の先頭に残す。

差分の検算方法: 変更前後の `:147`（分割後は当該ブロック全体）から
改行・行頭の `- `・連続する空白を取り除いた文字列が完全一致することを確認する。
一致しない場合は文言を変えてしまっているので戻すこと。

---

## 完了条件

1. `tools/testdata_converter.rst` の該当段落が §1 の変更後の文と一致する。
   `grep -rn 'メッセージのテストデータ' ja/` が0件
2. `tools/testdata_converter.rst` に「この整形」が無い
   （`grep -n 'この整形' ja/development_tools/testing_framework/tools/testdata_converter.rst` が0件）
3. `reviews/page-testdata_converter.md` に、5系統すべてで行末の空セルが落ちることを
   実装から確かめた経路が記録されている
4. `implementation/testdata_notation.rst` の `list-table` に §2 の行があり、
   既存の `:1544`-`:1545` が変わっていない。`reviews/page-testdata_notation.md` に出典がある
5. `mapping.csv` の `note` に「なお同じ基準で 9031fa6 が」が0件、
   「なお 9031fa6 も同じ基準で」が5件
6. `_batch/*.csv` を昇順連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、
   `csv.DictReader` が597行。`82322fa` との差分が指定5行の `note` のみであることを
   `git diff` で全行確認する
7. `design.md` の `:147` に「8件」が無く、`:143` から
   「同じマーカーの配下には」で始まる一文が消えている。`:143` の「計11件」は残っている
8. `design.md:141`（採否基準の段落）が `82322fa` から1文字も変わっていない
   （`git show 82322fa:….rn/…/design.md | sed -n '141p' | md5sum` と一致）
9. §5 の検算（改行・行頭記号・連続空白を除いた文字列の完全一致）が通る
10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
13. 既存イメージでのフルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。
    直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`_build/` を削除する
14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
    `locales/` の `.gitignore` 追加）に触れていない
15. 「取り除く」「落ちる」など無限定の断定文それぞれについて、主語を明示したうえで
    反例を検索し、自分の括弧書きや直後の列挙が反例になっていないかを確かめてから確定した
    ことを `checks/task-35.md` に記録する
