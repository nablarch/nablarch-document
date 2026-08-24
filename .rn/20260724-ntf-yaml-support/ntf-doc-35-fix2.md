# 作業指示 #35-是正2

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support（`7796c22`）

A-1〜A-5 はすべて成立する。実物で確認した。**A-1 の出典行番号（`:176`-`:177`・`:316`-`:317`）も
正しい。** 私が前回「誤り」と指摘したのは私の確認ミスで、取り消す。

`StringUtil.isNullOrEmpty(Collection<String>)` は `nablarch-core` 2.2.0 の
`StringUtil.java:155`-`:165` で「全要素が `null` または空文字なら `true`」。`DataFileParser`・
`TableDataParser`・`ListMapParser`・`MessageParser` はいずれも `TestDataParsingTemplate` の
子孫（`nablarch-testing@e21bf67`）なので、A-1 の「5系統すべて」も成立する。

---

## 1. `tools/testdata_converter.rst:71` を書き換える

第1文・第3文・第4文を落とし、次の1段落に置き換える。

```
名前の行（テーブルと\ ``LIST_MAP``\ ではカラム名の行、ファイルとメッセージではフィールド名称行）の行末の空セルは、\ Excel\ 形式から読み込む時点で取り除かれるため、往復すると消える。データ行の空セルの扱いは形式によって異なるため、詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
```

**前提事項は往復で失われるものを述べる節である。** データ行の空セルは、`Excel` 形式では空文字、
`YAML` 形式では `null`（`implementation/testdata_notation.rst:658`）と分かれるうえ、
全セルが空の行はそもそも読み飛ばされる（A-1）。1文で正しく言えないので、本文へ送る。
この書き換えで A-1・A-2 の両方が消える。

---

## 2. `implementation/testdata_notation.rst:1544`-`:1547` を書き換える

```
  * - ファイル・メッセージ
    - 行末の空セルを取り除く（\ Excel\ 形式のみ）。フィールド名称が宣言されていない値は読み込まない
  * - テーブル・\ ``LIST_MAP``
    - カラム名の行の行末の空セルを取り除く（\ Excel\ 形式のみ。前述）。カラム名が宣言されていない値は読み込まない
```

- **A-3** ── 「フィールド名称の行の」を落として無限定に戻す。`DataFileParser.java:68` の
  `trimTailCopy` は `:69` の `switch (status)` より前にあり、4分岐すべてに掛かる
  （`nablarch-testing@e21bf67`）。テーブル側（`HeaderLine.java:33`）はカラム名の行だけなので、
  2行が非対称な書き方になるのは実装どおりである。
- **A-4** ── 削除せず「前述」を付ける。**この表は要約表であり、`:1551`・`:1553` が既に
  「（前述）」を使っている。** 同ページ `:774` が機構Aを実例表つきで説明しているのは
  テーブル側だけなので、「前述」が付くのもテーブルの行だけでよい。
- **A-5** ── §1 の差し替え文で `フィールド名称行`（`mapping/glossary.md:269` の正表記）を使う。

**データ行の補完（不足分を空文字／`null` で埋める処理）は表に書かない。** `:658`・`:787`・`:883`
に既出であり、形式差を1セルで正しく書けないため。

---

## 3. B は §1・§2 と同じコミットで処置する

`reviews/page-testdata_converter.md:236`・`:238`、`reviews/page-testdata_notation.md:555`・
`:585`・`:644`・`:648`・`:654` の HEAD についての記述を、§1・§2 反映後の状態に合わせて書き直す。
申し送り38 は前提が消えたので削除する。`:595`・`:642` の行番号参照は節見出し参照に直す
（`steering.md` Rules）。

---

## 4. レビューは差分限定で回す

**4観点は回さない。** `ntf-doc-13-standing-rules.md:20` の常設ルールにより、本タスクは
是正ラウンド2に当たる。回すのは次の2点だけ。

- 是正が §1〜§3 の範囲に収まっているか
- 是正が新しい欠陥を生んでいないか（**特に §1・§2 の逐語指定文そのものに反例がないか**）

指摘件数と観点を `reviews/page-testdata_notation.md` に記録する（同ルールの効果測定）。

---

## 完了条件

1. `tools/testdata_converter.rst:71` が §1 の1段落と逐語一致し、旧第1・3・4文が消えている
2. `implementation/testdata_notation.rst` の該当4行が §2 の文面と逐語一致している
3. `implementation/testdata_notation.rst` 内に「フィールド名称の行」が1件も残っていない
4. §3 の7箇所と申し送り38、行番号参照2箇所が処置済み
5. §4 のレビューを回し、指摘件数と観点を記録済み。`must` を残していない
6. Docker フルビルドが成功し警告0、`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` 実施済み、
   `_build` 削除済み
7. `ca.crt`・`Dockerfile.ca` が作業ツリーに残っていない
8. §1〜§4 を1コミットにまとめてプッシュ済み

:883 の件は今回も含めていません。#35 の対象外なので、着地後に別タスクとして提案します。
