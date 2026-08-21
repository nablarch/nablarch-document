# 作業指示 #32-是正2: user 判断待ち6件の回答

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support（`f8f74f2`）
記録先: .rn/20260724-ntf-yaml-support/checks/task-32.md

`ja/` 配下のパスは ja/development_tools/testing_framework/ からの相対。
行番号は `f8f74f2` の作業ツリーのもの。
モジュール側の一次情報は逐語で引用してあるので、見に行く必要はない。

---

## 1. 判断1 空エントリ ── 現状維持。どちらの欄にも書かない

**推奨（保持側へ戻す）は採らない。** 根拠 `model/ListMapBlock.java:12` は YAML 経路の話で、
Excel 経路には当てはまらない。Excel 経路の読み飛ばしを行うのは変換ツールではなく NTF 本体である。
`nablarch-testing-converter` `e977824` の `.rn/ntf-test-data-converter/coverage/issues.md:299-300` 逐語:

> 読み飛ばしを実行するのも本体 `PoiXlsReader#isBlankLine`（L140-147）であり、
> converter に判断の余地は無い。

したがって Excel 起点では「無損失で保持する」が成り立たず、保持側にも書けない。
`:39` は現状（空エントリの記載なし）のままとする。

**「データブロックの外側にある」も残す。** 対語が消えて限定の意味が伝わらないという指摘は理解するが、
この書き分けは `reviews/page-testdata_converter.md:116` が「「空エントリ」と「完全な空行」が同一物に
見えるのに保持と除去に分かれている」を是正して入れたものである。「完全な空行」へ戻すと、
その是正を打ち消して同じ曖昧さが戻る。

---

## 2. 判断2 行末の空セル ── 表から落とし、前提事項へ移す

推奨（落とす）に同意する。`implementation/testdata_notation.rst:1545` 逐語:

> - 行末の空セルを取り除く（\ Excel\ 形式のみ。\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込む）

実装も Excel 経路だけである。`TestCoreReaderAdapter.java:254`「`NablarchTestUtils#trimTailCopy(List)`
で行末の空セルを除去済みである。」・同 `:410` にあり、`YamlFormatReader` には無い
（`grep -n 'trimTail' src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java` → ヒット無し）。
`TestCoreReaderAdapter` が Excel 経路であることは `StubDbInfo.java:11` 逐語
「{@link TestCoreReaderAdapter}（Excel 経路）と {@link YamlTestCoreAdapter}（YAML 経路）」による。

ただし出典（`input/testdata-converter-design.md:8`）にある内容なので、落とすのではなく移す。

### 2-1. `tools/testdata_converter.rst:39`

```
変更前  　　- 保持しない。コメント、マーカーカラム、データブロックの外側にある空行、行末の空セルは除去する
変更後  　　- 保持しない。コメント、マーカーカラム、データブロックの外側にある空行は除去する
```

### 2-2. `tools/testdata_converter.rst:69` の段落の直後に1段落足す

`:69`（マーカーカラムの段落）と `:71`（レコード種別の段落）の間に、空行を挟んで次を挿入する。

```
行末の空セルも、\ Excel\ 形式から読み込むときだけ取り除かれる。\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込むため、\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換すると、行末の空セルは変換後に現れない。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
```

---

## 3. 判断3 `mom.rst:142-143` の継承クラス ── `#33` へ送らず、いま直す

**推奨（`#33` へ送る）は採らない。** モジュール側の一次情報は jar から確定できる。
`~/.m2/repository/com/nablarch/framework/nablarch-testing/2.0.0/nablarch-testing-2.0.0.jar` を
展開して `javap` で実測した（2026-08-21）。

```
public abstract class nablarch.test.core.http.BasicHttpRequestTestTemplate
    extends nablarch.test.core.http.AbstractHttpRequestTestTemplate<nablarch.test.core.http.TestCaseInfo>
public class nablarch.test.core.batch.BatchRequestTestSupport
    extends nablarch.test.core.standalone.StandaloneTestSupportTemplate
```

`StandaloneTestSupportTemplate` の直接のサブクラスは `BatchRequestTestSupport` と
`MessagingRequestTestSupport` の2つ、`AbstractHttpRequestTestTemplate` の直接のサブクラスは
`BasicHttpRequestTestTemplate` の1つだけである（同 jar の全クラスを `javap` で走査）。

現状の `:142-143` は中間の抽象クラスを挙げており、同ページ `:30` の `BatchRequestTestSupport` とも
`web.rst:73`・`:83`・`:116` の `BasicHttpRequestTestTemplate` とも繋がらない。
`:140` は「テスト対象の処理方式に合わせて」と述べ、ウェブとバッチの2ページを参照しているので、
その2ページが挙げるクラスに揃える。

```
変更前
* :java:extdoc:`StandaloneTestSupportTemplate <nablarch.test.core.standalone.StandaloneTestSupportTemplate>`\ ：バッチやメッセージング処理などコンテナ外で動作する処理のテストで使用する。
* :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`\ ：ウェブアプリケーションのテストで使用する。

変更後
* :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ ：\ Nablarch\ バッチアプリケーションのテストで使用する。
* :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`\ ：ウェブアプリケーションのテストで使用する。
```

---

## 4. 判断4(a)・表の採否基準 ── 基準を明文化し、6ページ全部に当てる

**`TestDataConverter` を落とす推奨は採らない。** `AbstractHttpRequestTestTemplate` と同型ではない。
前者は `setup/request_unit_test/mom.rst:72`「拡張するには\ ``TestDataConverter``\ を実装する。」で
利用者（アーキテクト）が実装し、同 `:91` でコンポーネント設定にクラス名を書く。
後者は `setup/request_unit_test/web.rst:229`「アプリケーションプログラマが直接使用することはなく」と
一次情報が直接使用を否定している。`design.md:139` の基準では前者は残る側である。

### 4-1. 基準を `design.md:139` に明文化する

`:139` の末尾の文「同じ理由で「主なクラスとリソース」の表からも、利用者が名前を書かないクラスを落とした。」
の後に、次の趣旨を足す。

- 判定は次の2つで行う。(1) 利用者が作成する成果物（テストクラス・テストデータ・テスト対象クラス）は載せる。
  (2) クラスは、利用者がテストコード・テストデータ・コンポーネント設定のいずれかに**名前を書く**ものだけ載せる。
- 落とすのは、`design.md` の本節が名指しした「どのサポートクラスへ委譲するかという構造」にあたるクラスと、
  一次情報が直接使用を否定しているクラスである。落としたクラスの役割は、各ページのリード文または本文に残る。
- 2026-08-21 に6ページ全部へ適用した（`#32` の是正2）。

### 4-2. 6ページの表から次の行を落とす

各行は `* - クラス名` とそれに続く2行（役割・作成単位）の計3行。**表の他の行・列数・`:widths:` は変えない。**

| ページ | 落とすクラス | 現在の行 | 根拠 |
|---|---|---|---|
| `implementation/request_unit_test/web.rst` | `DbAccessTestSupport` | `:35` | `:108`「``HttpRequestTestSupport``\ が…\ ``DbAccessTestSupport``\ へ処理を委譲することで実現している」＝委譲構造 |
| 同上 | `HttpRequestTestSupport` | `:38` | 同上。委譲元であり、テストコードにも設定にも名前が出ない |
| `implementation/request_unit_test/rest.rst` | `DbAccessTestSupport` | `:37` | `:96`「``RestTestSupport``\ から\ ``DbAccessTestSupport``\ に処理を委譲することで実現している」 |
| `implementation/request_unit_test/batch.rst` | `MainForRequestTesting` | `:48` | 利用者が書く箇所が無い。役割は `:180` に残る |
| 同上 | `DbAccessTestSupport` | `:51` | `:17`「テーブルについては\ ``DbAccessTestSupport``\ が…行う」＝委譲 |
| 同上 | `FileSupport` | `:54` | 同上（`:17`「ファイルについては\ ``FileSupport``\ が行う」）。役割は `:58` に残る |
| `implementation/request_unit_test/mom.rst` | `MainForRequestTesting` | `:76` | 役割は `:190` に残る |
| 同上 | `DbAccessTestSupport` | `:79` | `:17`＝委譲 |
| 同上 | `MQSupport` | `:82` | `:17`＝委譲 |
| 同上 | `MessageSender` | `:88` | テスト側では書かない（テスト対象の\ Action\ が使う本番クラス）。役割は `:30` に残る |

**落とさない行**（判定の根拠も `checks/task-32.md` に記録すること）:

- `mom.rst:91` `TestDataConverter` —— コンポーネント設定に書く（`setup/request_unit_test/mom.rst:91`）
- `mom.rst:85` `RequestTestingMessagingProvider` —— コンポーネント設定に書く（`setup/request_unit_test/mom.rst:44`
  `class="nablarch.test.core.messaging.RequestTestingMessagingProvider"`）
- `web.rst:44` `TestCaseInfo` —— テストコードに書く（`web.rst:217`・`:224` のメソッドシグネチャ）
- `implementation/class_unit_test/component.rst`・`entity.rst` —— **変更なし。**
  表はどちらも4行で、`DbAccessTestSupport`（`component.rst:69`・`:81` で継承）・
  `EntityTestSupport`（`entity.rst:35`）はいずれも利用者が継承するクラスである

削除後、各ページの表が空にならないこと、`list-table` の `:header-rows: 1` と行の3行構成が保たれることを
確認する。落としたクラスの役割が本文に残っていることも、上表の「根拠」欄の行番号で1件ずつ確認する。

---

## 5. 判断4(b)・判断5 ── 台帳6行と `reviews/` への記録

### 5-1. `reviews/page-testdata_converter.md` に記録する

`design.md:501-502`「出典の記述が、検証可能な実装の挙動と食い違う場合は、実装を優先する。根拠として、
確認した実装のファイル名・行番号・参照したコミットを `reviews/page-*.md` に記録する。」に従う。

出典 `input/testdata-converter-design.md:7` 逐語:

> - 意図ある情報は無損失（マーカーカラム、空エントリ、空欄のレコード種別を保持）

この3つのうち2つが実装と食い違う。参照コミットは `nablarch-testing-converter` `e977824`。
次の3件を、既存の表の書式に合わせて追記する。

| 出典の記述 | 実装 | 解説書での扱い |
|---|---|---|
| マーカーカラムを保持 | 両形式で除外する。Excel は `TestCoreReaderAdapter.java:129` `return Arrays.asList(header.getEffectiveColumnNames());`、YAML は `YamlFormatReader.java:491`「エントリ先頭行のキー（YAML 記述順）からマーカーカラム（`[COL]`）を除いたカラム名を返す。」 | `tools/testdata_converter.rst:39` の除去側に置き、`:69` に往復時の挙動を書いた |
| 空エントリを保持 | 経路で割れる。Excel は本体 `PoiXlsReader#isBlankLine` が読み飛ばす（`coverage/issues.md:299-300`）、YAML は `YamlFormatReader` に処理が無い（`grep -rn 'dropEmptyEntries\|isEmptyEntry' src/main/java/` のヒットは `XlsFormatReader.java` のみ） | どちらの欄にも書けないため表から外した。読み飛ばしそのものは `implementation/testdata_notation.rst:1534` が説明している |
| （出典 `:8`）行末の空セルを除去 | Excel 経路のみ（`TestCoreReaderAdapter.java:254`・`:410`）。`implementation/testdata_notation.rst:1545` が「Excel 形式のみ」と明記 | 表から外し、`tools/testdata_converter.rst` の前提事項へ移した（本指示 §2-2） |

### 5-2. マッピング台帳6行に `#32` のポインタを足す

`mapping.csv` の直接編集は禁止事項。`_batch/*.csv` を直してから作り直す。連結規則は
ファイル名の昇順で、先頭ファイルはヘッダ行を含む全行、2つ目以降はヘッダ行を除く全行。

既存の `note` は消さず、末尾に追記する。

- **表由来の5行** —— `current-0201`（web、`disposition=MERGE`）・`current-0282`（batch）・
  `current-0296`（mom 受信）・`current-0309`（rest）・`current-0323`（mom 送信）

  `【#32・2026-08-21】「主なクラスとリソース」の表に採否基準（利用者が名前を書くものに絞る）を当て、〈落としたクラス名を列挙〉の行を落とした。落としたクラスの役割は同ページの本文に残る。disposition は割当の履歴として変更しない。基準は design.md「利用側ページに内部構造の構成図を置かない」。`

  〈落としたクラス名〉は本指示 §4-2 の表のとおり、そのページで落としたものだけを書く。
  `current-0201` は `#32`（`9031fa6`）で落とした `AbstractHttpRequestTestTemplate` も含めて書く。

- **出典側の1行** —— `input-0184`

  `【#32・2026-08-21】出典の「意図ある情報は無損失（マーカーカラム、空エントリを保持）」は実装と食い違うため採らず、マーカーカラムは除去側へ移し、空エントリと行末の空セルは表から外した（行末の空セルは前提事項へ移送）。判断の根拠は reviews/page-testdata_converter.md。disposition は変更しない。`

CSV のクォートに注意する。追記後のセルは必ず `"` で囲む。編集後、各 `_batch` の
`csv.DictReader` 行数が編集前と同じであることを確認してから連結する。

---

## 6. 判断6 `:278` の追跡先 ── `#33` に3項目目として足す

`steering.md:921` の `#33` に次を足す。見出しも
`### #33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検` へ改める。

- **(c) `tools/testdata_converter.rst:278` の `markerColumnColor` の説明不足** ——
  この設定が着色するのは、`XlsFormatWriter` がカラム名0件のブロックに合成するマーカーカラム
  （`XlsFormatWriter.java:543` `static final String EMPTY_BLOCK_MARKER_COLUMN = "[EMPTY]";`）だけである。
  入力に元からあったマーカーカラムは中間モデルに入らないため、着色の対象にならない。
  `:278`「マーカーカラムの背景色」はこの限定に触れていない。`#32` より前から成り立つ事実であり、
  `#32` が作った矛盾ではない（`#32` 以前の `:37`「マーカーカラムは無損失で保持する」が誤りだったため、
  当時の見かけ上の整合は誤り同士の整合だった）。

---

## 完了条件

1. `grep -n '行末の空セル' ja/development_tools/testing_framework/tools/testdata_converter.rst` が
   `:39` を含まず、前提事項の新段落1件のみ
2. `grep -n '空エントリ' ja/development_tools/testing_framework/tools/testdata_converter.rst` が0件
3. `grep -c 'StandaloneTestSupportTemplate\|AbstractHttpRequestTestTemplate' ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst` が0
4. §4-2 の10行が6ページの表から消えており、`grep -c 'TestDataConverter' .../mom.rst` が1、
   `grep -c 'RequestTestingMessagingProvider' .../mom.rst` が3、`grep -c 'TestCaseInfo' .../web.rst` が
   削除前と同じ。`component.rst`・`entity.rst` に差分が無い
5. 各ページの `list-table` の行が3行構成を保ち、docutils の parse エラーが0
6. `_batch/*.csv` を昇順に連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、
   `csv.DictReader` が597行。6行の `note` に `【#32` があり、`disposition` は編集前と同一
7. `design.md:139` の節に判定基準の2項目と適用範囲（6ページ）が書かれている
8. `reviews/page-testdata_converter.md` に §5-1 の3件が記録されている
9. `steering.md` の `#33` に (c) が足され、見出しが改まっている
10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
13. Docker フルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。
    直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する。
    **`docker build` から作り直すこと。** 前回は `pip install -r requirements.txt` が失敗し
    7日前のイメージを流用したため、イメージ自体は検証できていない。今回も失敗する場合は、
    失敗ログをそのまま `checks/task-32.md` に記録し、`#33` へ送る
14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
    `locales/` の `.gitignore` 追加）に触れていない
15. `checks/task-32.md` に §4-2 の「落とさない行」の判定根拠と、§1・§3 で推奨を採らなかった理由が
    記録されている
16. `#32` が check-off されている
