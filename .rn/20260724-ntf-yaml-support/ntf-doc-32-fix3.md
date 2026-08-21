# 作業指示 #32-是正3: 判断A〜E の回答

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support（`456544e`）
`ja/` 配下のパスは ja/development_tools/testing_framework/ からの相対。
行番号は `456544e` の作業ツリーのもの。

これが `#32` の最後のラウンド。終わったら check-off する。

---

## 1. 判断A ── 指摘のとおり。`tools/testdata_converter.rst:71` を書き直す

因果のねじれも適用範囲の書き漏れも、実物で確認した。元の指示（是正2 §2-2）の文が誤っていた。

**適用範囲**は `implementation/testdata_notation.rst:1544-1545` の表行が
「ファイル・メッセージ」を対象としており、実装も一致する。行末の空セルを落とすのは
`core/reader/TestCoreReaderAdapter.java:264` `readBlockBodyLines` だけで、その呼び出し元は
`xls/XlsFormatReader.java:212`（ファイル系）・`:240`（メッセージ）・`:274`（同期応答電文）の3か所である。
テーブル系（`:146` `readTables`）と `LIST_MAP`（`:179`・`:182`）は通らない。
いずれも `nablarch-testing-converter@e977824` を `git show` で開いて確認した（2026-08-21）。

**因果**は Excel 側で取り除かれることが理由であり、YAML 側の読み込み方は理由ではない。

```
変更前
行末の空セルも、\ Excel\ 形式から読み込むときだけ取り除かれる。\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込むため、\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換すると、行末の空セルは変換後に現れない。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。

変更後
ファイルとメッセージのテストデータでは、\ Excel\ 形式から読み込むときに行末の空セルが取り除かれる。取り除かれたあとの状態が中間モデルに入るため、\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換すると、行末の空セルは変換後に現れない。\ YAML\ 形式から読み込むときは ``rows:``\ の各要素をそのまま扱うため、この整形は行われない。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
```

`reviews/page-testdata_converter.md:89` の「解説書での扱い」欄も、適用範囲（ファイル・メッセージ）を
含む記述に直すこと。

---

## 2. 判断B ── 判断1 は維持する。`reviews/` の記録を1文足して正確にする

**表の記述は変えない。** 空エントリはどちらの欄にも書けない、が結論のまま。

ただし是正2 指示 §1 の「Excel 経路の読み飛ばしを行うのは変換ツールではなく NTF 本体である」は
言い切りすぎだった。converter 側にも判断がある。`XlsFormatReader.java:566` `dropEmptyEntries` が
テーブル系（`:162`）と `LIST_MAP`（`:193`）に対して動く。同 `:551-555` 逐語:

> {@code notation:1535}「全要素が null または空文字のエントリは読み飛ばされる」を、
> <b>マーカーカラムの除外（{@code notation:1550}）のあとに</b>適用する。本体
> {@code PoiXlsReader#readLine} は除外前の生の行で空エントリを判定するため、
> マーカーカラムだけを持つ行は本体では空エントリにならず、除外後に「セルを 1 つも持たない行」として
> 残ってしまう。

つまり converter が落とすのは、本体の判定をすり抜けた残差（マーカーカラムだけの行）に限られる。
一般の空エントリは本体が落とす。結論（両形式で「無損失で保持」が成り立たない）は変わらない。

`reviews/page-testdata_converter.md:88` の「実装」欄に、この残差処理を1文足す。
`nablarch-testing-converter@e977824` の `src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:566`
と `:551-555` を出典として書くこと。

`steering.md` の `#33` (a) は現状（`:942-950`）で足りている。変更不要。

---

## 3. 判断C ── `#33` へ (d) として送る。表への行追加は `#32` ではやらない

送る理由は3つ。行の追加は「役割」「作成単位」の新規執筆であって、`#32` が当てた
「落とす側の基準」の適用ではない。台帳の出典側（`current-0282`・`current-0296`）にもその行は無く、
出典に無い行を足すには別の設計判断が要る。そして `design.md:143` が既に
「テスト対象クラスの行を持たない。これは基準を当てる前からそうであり」と事実として記録しており、
後から読む人が誤解する状態にはなっていない。

**指摘の内訳に1件誤りがある。** 「`mom.rst` の表にスーパクラスが無い」は成り立たない。
`mom.rst:70` `MessagingRequestTestSupport`・`:73` `MessagingReceiveTestSupport` が表にあり、
`:106`・`:124` の `extends` と一致している。正しくは
**「同期応答メッセージ送信で継承する `BatchRequestTestSupport`（`mom.rst:30`）が表に無い」**である。
`#33` (d) にはこちらを書くこと。

`steering.md:936` の `#33` に (d) を足し、見出しにも足す。書く内容は次の3点。

- **(d) 「主なクラスとリソース」の表の「載せる側」が6ページで揃っていない** ——
  `design.md` §「利用側ページに内部構造の構成図を置かない」の判定基準 (1) は
  「利用者が作成する成果物（テストクラス・テストデータ・テスト対象クラス）は載せる」だが、
  `implementation/request_unit_test/batch.rst`・同 `mom.rst` の表はテスト対象クラスの行を持たない
  （両ページとも `batch.rst:45`・`mom.rst:66` の作成単位欄で「テスト対象クラス（Action）につき1つ」と
  述べており、テスト対象クラスの存在自体は前提にしている）。
  また基準 (2) を満たす `BatchRequestTestSupport` が `mom.rst` の表に無い（`mom.rst:30` で
  同期応答メッセージ送信のスーパクラスとして継承すると書いている）。
  `#32` は落とす側だけを当てたため未処理。行を足すか、(1) をページ単位の任意とするかを着手時に決める。
  台帳 `current-0282`・`current-0296`・`current-0323` の出典表にも該当行が無いため、
  行を足す場合は台帳の `note` に足した理由を記録する必要がある。

---

## 4. 判断D ── 指摘のとおり。ただし置き場所は `design.md` にする

7行という数も内訳も、`git show 9031fa6~1` と `git show 9031fa6` の表を突き合わせて確認した。
`implementation/request_unit_test/batch.rst` から `StandaloneTestSupportTemplate`・`TestShot`、
同 `mom.rst` から `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`・`TestShot`、
同 `rest.rst` から `HttpServer`、同 `web.rst` から `HttpServer` の計7行である。

台帳の `note` に内訳を書き足すと1〜2文のポインタに収まらない（`design.md:153` に反する）。
`design.md` に書き、`note` からはそこを指す。

### 4-1. `design.md` §「利用側ページに内部構造の構成図を置かない」に1段落足す

`:145`（4類型の段落）と `:147` の間に入れる。内容は次の3点。

- `9031fa6` は、基準を明文化する前に同じ趣旨で7行を落としている（上記の内訳をページごとに書く）。
- **この7行のうち6行は、落としたクラスの役割が本文に残っていない。**
  `grep -rn` で確認した結果、`StandaloneTestSupportTemplate`（3行）・`HttpServer`（2行）・
  `AbstractHttpRequestTestTemplate`（1行）は `implementation/request_unit_test/*.rst` に1件も現れない
  （2026-08-21 実測）。利用者がテストコード・テストデータ・コンポーネント設定のいずれにも
  名前を書かず、役割を知らなくてもテストを書けるクラスであるため、本文にも残していない。
  残る1行の `TestShot` は、クラス名としては現れないが「テストショット」という語で
  `implementation/request_unit_test/batch.rst:15`・`:17`・`:102` 他に残っている。
- `:141` 末尾の「落としたクラスの役割は、各ページのリード文または本文に残す。」は
  是正2 で落とした10行について述べたものであり、この7行には当てはまらないことを明記する。

**`:141` の文そのものは書き換えないこと。**10行については実際に成り立っており
（`:145` が10行すべてについて残存箇所の行番号を挙げている）、変えると `:145` と食い違う。

### 4-2. 台帳5行の `note` に1文足す

`mapping.csv` の直接編集は禁止。`_batch/*.csv` を直してから昇順連結で作り直す
（先頭ファイルのみヘッダ込み）。既存の `note` は消さず、末尾に足す。

| mapping_id | 足す文 |
|---|---|
| `current-0201` | `なお同じ基準で 9031fa6 が HttpServer の行を落としている（内訳は design.md 同節）。` |
| `current-0282` | `なお同じ基準で 9031fa6 が StandaloneTestSupportTemplate・TestShot の行を落としている（内訳は design.md 同節）。` |
| `current-0296` | `なお同じ基準で 9031fa6 が StandaloneTestSupportTemplate・TestShot の行を落としている（内訳は design.md 同節）。` |
| `current-0309` | `なお同じ基準で 9031fa6 が HttpServer の行を落としている（内訳は design.md 同節）。` |
| `current-0323` | `なお同じ基準で 9031fa6 が StandaloneTestSupportTemplate・AbstractHttpRequestTestTemplate の行を落としている（内訳は design.md 同節）。` |

`input-0184` は表由来ではないので触らない。
`disposition` を含む他の列は1文字も変えない。

---

## 5. 判断E ── `#34` のままでよい。`#32` の check-off は止めない

`Dockerfile` は変更しない方針で `#34` を進める。社内 TLS 傍受の CA は環境固有のもので、
解説書リポジトリの `Dockerfile` に焼き込むと、その CA を持たない環境でビルドが壊れる。
`docker build` 時に CA を渡す手順（`--build-arg` またはビルドコンテキストへの一時配置と
ビルド後の削除）を `steering.md` の手順として残す方向で検討する。

**この方針を `#34` の「未決点」（`steering.md:970`）に書き加えること。**
`ca.crt`・`Dockerfile.ca` を作業ツリーに残さないという既存の制約も併記する。

`#32` の完了条件13 は `steering.md:972` の判断（既存イメージでのフルビルドをもって代替）どおりでよい。

---

## 6. `mapping/style.md:401` の参照を直す

`reviews/page-testdata_converter.md:94` は空行で、当該記述は同ファイルの `## クラス名の表記` 節
（`:101`）にある。`steering.md` Rules の「`.rn/` 内の文書どうしの相互参照は行番号ではなく
節見出しで指す」にも反する。

```
変更前  Javadocが公開されておらずリンク切れになるためである（`reviews/page-testdata_converter.md:94`）。
変更後  Javadocが公開されておらずリンク切れになるためである（`reviews/page-testdata_converter.md` §「クラス名の表記」）。
```

同ファイル内に他にも `.rn/` 内文書を行番号で指している箇所が無いか、
`grep -nE '(reviews|design|steering|checks)/[a-z0-9_-]+\.md:[0-9]+' mapping/style.md mapping/glossary.md mapping/vocabulary.md`
で確認し、あれば同じ形に直す。

---

## 完了条件

1. `tools/testdata_converter.rst` の該当段落が §1 の変更後の文と一致し、
   `grep -c '行末の空セル' ja/development_tools/testing_framework/tools/testdata_converter.rst` が 1
2. `reviews/page-testdata_converter.md` の空エントリの行に `XlsFormatReader.java:566` の残差処理が、
   行末の空セルの行に適用範囲（ファイル・メッセージ）が書かれている
3. `steering.md` の `#33` に (d) が足され、見出しにも反映されている。
   (d) に「`mom.rst` の表にスーパクラスが無い」という誤った記述が含まれていない
4. `design.md` の §「利用側ページに内部構造の構成図を置かない」に §4-1 の段落があり、
   `:141` の文は変わっていない（`git diff` で確認する）
5. `steering.md` の `#34` 未決点に §5 の方針が書かれている
6. `mapping/style.md` に `reviews/page-testdata_converter.md:94` が残っていない。
   §6 の `grep -nE` が0件
7. `_batch/*.csv` を昇順連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、
   `csv.DictReader` が597行。`456544e` との差分が指定5行の `note` のみであることを
   `git diff` で全行確認する
8. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
9. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
10. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
11. 既存イメージでのフルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。
    直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する
12. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
    `locales/` の `.gitignore` 追加）に触れていない
13. 「〜が無い」「すべて」「〜だけ」を書いた文それぞれについて、反例が出ないか走査してから確定した
    ことを `checks/task-32.md` に記録する
14. `checks/task-32.md` を staging して `#32` を check-off する
