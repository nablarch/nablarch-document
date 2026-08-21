# 作業指示 #35-是正1: §1 の差し替え文と完了条件2

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support（`17b0254`）

報告の2点はどちらも指摘のとおり。判断は以下。

---

## 1. 差し替え文 ── 書く。ただし提案の文面は使わない

**書く方針は採る。**往復で消えるものと残るものが混在する以上、書かないほうが誤解を招くという
判断に同意する。

**提案の文面は「カラム名の行」がファイル・メッセージに当たらない。**同じ記法ページが、
テーブルと `LIST_MAP` では「カラム名」、ファイルとメッセージでは「フィールド名称」を使っている
（`implementation/testdata_notation.rst:870`・`:883`・`:887`-`:892`）。両方を1文で
「カラム名の行」と呼ぶと、ファイル・メッセージの読者に通じない。

**また「YAML 形式では ``rows:`` の各要素をそのまま扱う」は、この段落では書かないこと。**
同ページ `:883` は、YAML 形式でも `rows:` の各要素がフィールド数より短ければ `""` で補完されると
書いている。前提事項の段落は往復で失われるものを述べる場所であり、`Excel` 形式を読み込む側だけで
足りる。YAML 側の対称性を主張する必要はない。

`tools/testdata_converter.rst:71` を次の文に置き換える。

```
行末の空セルの扱いは、名前の行とデータ行で異なる。名前の行（テーブルと\ ``LIST_MAP``\ ではカラム名の行、ファイルとメッセージではフィールド名称の行）の行末の空セルは、\ Excel\ 形式から読み込む時点で取り除かれるため、往復すると消える。データ行は名前の行の幅に揃えられるため、名前がある位置の空のセルは空文字として中間モデルに入り、往復しても残る。名前より右にあるセルは読み込まれないため消える。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
```

---

## 2. `implementation/testdata_notation.rst` の「ファイル・メッセージ」の行も揃える

`#35` の §2 で足した「テーブル・``LIST_MAP``」の行は正確だが、**その1つ上にある既存の
「ファイル・メッセージ」の行（「行末の空セルを取り除く」）は、同じ機構を違う粒度で述べている。**
`XlsFormatReader.java:422`-`:426` が `names.size()` の幅へ揃えることを、この行は拾っていない。
2つの行が同じことを別々に言う状態を残さない。

「ファイル・メッセージ」の行の説明を、「テーブル・``LIST_MAP``」の行と同じ粒度に直す。
フィールド名称の行の行末の空セルは取り除かれること、データ行はフィールド名称の行の幅へ
揃えられ、フィールド名称が無い位置のセルは読み込まれないこと、の2点がわかる文にする。
表のセルに収まる長さにすること。

**あわせて、両方の行の「（Excel 形式のみ）」が成り立つかを確かめること。**
`nablarch-testing-converter@e977824` の
`src/main/java/nablarch/test/tool/converter/yaml/` 配下を実装から読み、YAML 形式の読み込みで
幅を揃える処理があるかを確認する。**あるなら「Excel 形式のみ」は誤りなので、直す前に報告すること。**
確認した経路は `reviews/page-testdata_notation.md` に記録する。

---

## 3. 完了条件2 ── 読み替えを認める

**「`tools/testdata_converter.rst:71` に『この整形』が無い」と読み替える。**
`:249` の「この整形」は書き出し設定の既存文で、`#32` で確定した記述である。`#35` の対象外。

読み替えたことを `checks/task-35.md` に記録すること。

---

## 完了条件（是正1）

1. `tools/testdata_converter.rst` の該当段落が §1 の文と一致する
2. 同ファイル `:71` に「この整形」が無い（`:249` は残ってよい）
3. `implementation/testdata_notation.rst` の「ファイル・メッセージ」の行が §2 のとおり直っており、
   「テーブル・``LIST_MAP``」の行と同じ粒度になっている
4. 両方の行の「（Excel 形式のみ）」の根拠が `reviews/page-testdata_notation.md` に記録されている。
   YAML 側にも幅を揃える処理があった場合は、直さずに報告している
5. `reviews/page-testdata_converter.md` の該当行が、`HeaderLine.java:81`・
   `XlsFormatReader.java:424`・`XlsFormatReaderCellTypeTest.java:182`-`:188` を出典として、
   名前の行とデータ行で扱いが異なることを記録している
6. `implementation/testdata_notation.rst:883` の既存記述（可変長ファイルの `""` 補完）と、
   新しく書いた記述が食い違っていないことを確認した記録がある
7. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
8. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
9. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
10. Docker フルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。
    直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`_build/`・`build.log` を消す
11. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
    `locales/` の `.gitignore` 追加）に触れていない
