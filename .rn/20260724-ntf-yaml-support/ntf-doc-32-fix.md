# 作業指示 #32-是正: 有効な指摘11件の処理

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support
記録先: .rn/20260724-ntf-yaml-support/checks/task-32.md

user 判断待ち5件の結論が出た。判断なしで直す6件とあわせて処理し、#32 を閉じる。
以下、`ja/` 配下のパスは ja/development_tools/testing_framework/ からの相対。
行番号は現在の作業ツリー（`9031fa6`）のもの。
モジュール側リポジトリの一次情報は逐語で引用してあるので、見に行く必要はない。

---

## 1. `tools/testdata_converter.rst` の表と前提事項（判断1）

**結論: 空エントリを両方から落とす。マーカーカラムだけにする。** CC 案（Excel 形式に限定）は
空エントリには正しいがマーカーカラムには過剰であり、空エントリを残すこと自体が誤りである。

### 1-1. `:39` から「空エントリ」を削る

```
変更前  　　- 保持しない。コメント、マーカーカラム、空エントリ、データブロックの外側にある空行、行末の空セルは除去する
変更後  　　- 保持しない。コメント、マーカーカラム、データブロックの外側にある空行、行末の空セルは除去する
```

理由: 空エントリの除去は Excel 起点でしか起きない。`XlsFormatReader#dropEmptyEntries`
（`:566`、呼び出しは `:162`・`:193`）は変換ツール自身のコードで、`YamlFormatReader` に対応物が無い。
nablarch-testing-converter `1093144` の
`src/main/java/nablarch/test/tool/converter/model/ColumnRowDataBlock.java:40-42` 逐語:

> <li><b>カラム名 0 件・セルを 1 つも持たない行が n 件</b>——マーカーカラムだけのブロックが
>     {@code :1550} の除外を受けるとこの形になる（<b>XLS-08</b> ／ <b>YML-04</b>）。値を持たないため
>     値の消失は起きず、扱いの非対称（辺①は落とし辺②は残す）は当該項の課題である

辺①＝Excel 読み、辺②＝YAML 読み。表は形式を問わない中間モデルの説明なので、非対称な扱いを
無条件に書けない。

### 1-2. `:69` の段落を差し替える

```
変更前
マーカーカラムと空エントリも、往復すると消える。マーカーカラムはテスティングフレームワークが読み込み対象から除外し、空エントリは読み飛ばすため、どちらも中間モデルに入らない。テストの実行結果は変わらないが、変換後のテストデータには残らない。

変更後
マーカーカラムは往復すると消える。テスティングフレームワークが読み込み対象から除外するため、中間モデルに入らない。マーカーカラムだけで構成したデータブロックは、\ Excel\ 形式から読み込むとデータ行も残らない。
```

「テストの実行結果は変わらない」は出典が無く、出典は逆を述べていた。
`.rn/ntf-test-data-converter/coverage/issues.md:481-482` 逐語:

> - 影響: 失われるのは「セルを 1 つも持たない行」であり、**値としての情報は失われない**。
>   行数だけが変わる。

`EXPECTED_TABLE` なら期待行数が変わるため、実行結果は変わりうる。

新しい3文の根拠（すべて逐語）:

- マーカーカラムが両形式で除外されること
    - `implementation/testdata_notation.rst:1550` が記法として定めている（本リポジトリ内）
    - Excel: `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129`
          `return Arrays.asList(header.getEffectiveColumnNames());`
    - YAML: `src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java:491`
          `* エントリ先頭行のキー（YAML 記述順）からマーカーカラム（{@code [COL]}）を除いたカラム名を返す。`
- マーカーカラムだけのブロックが Excel 起点で行ごと消えること
    - `coverage/issues.md:470` の表 逐語:
      `| SETUP_TABLE=T／カラム行 [no] のみ／データ行 1, 2 | 修正前: columnNames=[]、rows=[[], []]（セルを 1 つも持たない行が 2 件）／修正後: columnNames=[]、rows=[] | ... |`

### 1-3. `:278` は触らない

`markerColumnColor` が効くのは、書き手が合成する `XlsFormatWriter.EMPTY_BLOCK_MARKER_COLUMN`
（`:543`。値は `"[空]"` ではなく **`"[EMPTY]"`**）だけである。ただしこれは是正前から成り立って
いた事実で、`#32` が矛盾を新規に作ったのではない。是正前の `:37`「マーカーカラムは無損失で保持する」
が誤りだっただけである。`:278` の説明不足は独立した別件として `checks/task-32.md` に1行記録し、
本文は変更しない。

---

## 2. `about/index.rst:106`（判断2）

削除した図が持っていた「Nablarch Application Framework →（読み取る）→ コンポーネント設定ファイル／
環境設定ファイル」が本文に無い。指示書 §5-2 の3つ目の理由「図の内容が `:106` の本文に既に
書かれている」は成り立たなかった。

`:106` の2文目「…本番相当の基盤の上でテスト対象クラスの動作を検証できる。」の直後に、次の1文を
挿入する（段落は1行のまま。改行しない）。

```
このとき\ Nablarch Application Framework\ が読み取るコンポーネント設定ファイルと環境設定ファイルは、\ :ref:`テスティングフレームワークの導入と設定 <testing_framework_setup>`\ で用意する。
```

3文目「テストクラスは、Excelファイルなどの…」はそのまま残す。

---

## 3. `design.md` と マッピング台帳（判断3）

**前提の訂正**: `design.md` は禁止事項に入っていない。禁止事項は `steering.md:752`・`:813`・`:860`
が繰り返し挙げる「`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
`locales/` の `.gitignore` 追加」であり、`design.md` はここに無い。`steering.md:190` の
「`design.md` が変更されていない」は `#5b` の完了条件で、当該タスク限定である。
`steering.md:68` は「設計判断そのもの（何を・なぜ）は `design.md` の該当節にのみ書く」と定めている。

### 3-1. `design.md` に新しい節を1つ足す

`### 「アーキテクチャ」は図のみとし、構成物一覧の表は置かない`（`design.md:137`）の**直前**に、
次の節を新設する。理由づけはここ1箇所にだけ書く。

見出し: `### 利用側ページに内部構造の構成図を置かない`

本文に含める内容（文面は CC が書く。以下は必須要素）:

- 2026-08-21 user 判断による `#32` の決定であること
- 決定の内容 —— 利用者はテスティングフレームワークの内部の作りを知らなくてもテストを書けるため、
  利用側ページに内部構造の UML クラス図を置かない
- 削除した画像9件の一覧（`#32` のコミット `9031fa6` を参照先として書く）
- 図が持っていた関係のうち本文へ移したもの —— `about/index.rst` の「アーキテクチャ」節に
  「NAF がコンポーネント設定ファイル／環境設定ファイルを読み取る」を1文で統合した（本指示 §2）
- 影響を受けるマッピング行7件（`current-0165`・`0182`・`0200`・`0281`・`0295`・`0308`・`0322`）と、
  `disposition` を `MOVE` のまま動かさない理由 —— `mapping.csv` は「現行解説書のどのセクションを
  新解説書のどこへ割り当てたか」の台帳であり、図を落としたのは割当のあとに下した設計判断である。
  `DROP` に書き換えると割当の履歴が消え、`design.md` §11.8「`DROP` は件数の多寡にかかわらず
  全件を対象とする」に基づいて `#5c` で閉じた全件レビューの前提が後から動く
- `send_sync_base.png` ほか残置図の禁止語は本決定の対象外で、`#33` へ送ったこと（本指示 §6）

### 3-2. `design.md:137` の節見出しと本文を実態に合わせる

現物に図が無いため、見出しが実態と食い違っている。

```
変更前  ### 「アーキテクチャ」は図のみとし、構成物一覧の表は置かない
変更後  ### 「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない
```

節の末尾（`design.md:143` の段落の後）に、次の趣旨の段落を1つ足す。理由は書かず、ポインタに留める。

- 2026-08-21 `#32` で図 `abstract_structure.png` も削除し、本節は本文のみになった
- 図が示していた関係は本文に統合済み
- 判断の理由は `design.md` §「利用側ページに内部構造の構成図を置かない」

`design.md:139`・`:141`・`:143` の既存3段落は削除も書き換えもしない。過去の判断の記録である。

### 3-3. マッピング台帳7行の `note` にポインタを足す

`mapping.csv` の直接編集は禁止事項。実体は `_batch/*.csv` の連結なので、`_batch/` を直してから
`mapping.csv` を作り直す。連結規則は実測で確認済み —— ファイル名の昇順で、先頭ファイルは
ヘッダ行を含め全行、2つ目以降はヘッダ行を除く全行。これで現行の `mapping.csv` とバイト一致する。

対象行と所在:

| mapping_id | ファイル | 行 |
|---|---|---|
| `current-0165` | `_batch/batch-03.csv` | 6 |
| `current-0182` | `_batch/batch-09.csv` | 6 |
| `current-0200` | `_batch/batch-13.csv` | 4 |
| `current-0281` | `_batch/batch-19.csv` | 4 |
| `current-0295` | `_batch/batch-21.csv` | 3 |
| `current-0308` | `_batch/batch-17.csv` | 4 |
| `current-0322` | `_batch/batch-28.csv` | 3 |

`current-0322` は CC の報告に含まれていなかった。`heading_path` に「全体像」「構成」を含む
非 `DROP` 行を全走査して見つけたものである。

既存の `note` は消さず、末尾に追記する。行ごとに次の文を足す。

- `current-0200`・`0281`・`0295`・`0308`

  `【#32・2026-08-21】この図は削除した。本行の内容は図のみのため、移送先に対応する記述は無い。disposition は割当の履歴として MOVE のまま残す。理由は design.md「利用側ページに内部構造の構成図を置かない」。`

- `current-0165`

  `【#32・2026-08-21】図 abstract_structure.png は削除した。図が示していた関係は about/index.rst の「アーキテクチャ」節の本文に統合済み。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。`

- `current-0182`

  `【#32・2026-08-21】図 class_structure.png は削除した。「主なクラスとリソース」の表は implementation/class_unit_test/component.rst に存在する。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。`

- `current-0322`

  `【#32・2026-08-21】図 send_sync.png は削除した。テストクラスのスーパクラスに関する tip は implementation/request_unit_test/mom.rst の「テストクラスを作成する」に存在する。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。`

CSV のクォート規則に注意する。`note` に読点が入るため、追記後のセルは必ず `"` で囲む。
編集後、`python3 -c "import csv; print(len(list(csv.DictReader(open('...')))))"` で
各 `_batch` の行数が編集前と同じであることを確認してから連結する。

---

## 4. 「主なクラスとリソース」の採否基準（判断4）

CC 案をそのまま採る。指示書 §7-1 の「`AbstractHttpRequestTestTemplate` を残す
（web.rst:78・88 で継承する）」という根拠は誤りだった。`implementation/request_unit_test/web.rst`
の継承例は `:73`・`:83`・`:116` いずれも `BasicHttpRequestTestTemplate` で、
`AbstractHttpRequestTestTemplate` は表の `:41` 以外に出てこない。
`setup/request_unit_test/web.rst:229` 逐語:

> ``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのテストクラスのスーパクラスである。アプリケーションプログラマが直接使用することはなく、テスティングフレームワークを拡張する際に用いる。

### 4-1. リード文を揃える

6ページ中4ページが「このページで扱う主な」、web と rest だけが「テストを構成する主な」に
割れている。新しい採否基準（このページの手順で利用者が意識するものだけ載せる）と整合するのは前者。

```
implementation/request_unit_test/web.rst:17
  変更前  テストを構成する主なクラスとリソースは次のとおりである。
  変更後  このページで扱う主なクラスとリソースを次に示す。

implementation/request_unit_test/rest.rst:19
  変更前  テストを構成する主なクラスとリソースは次のとおりである。
  変更後  このページで扱う主なクラスとリソースを次に示す。
```

### 4-2. `implementation/request_unit_test/web.rst:41-43` から `AbstractHttpRequestTestTemplate` を落とす

```
変更前
  * - ``AbstractHttpRequestTestTemplate``\ ・\ ``BasicHttpRequestTestTemplate``
    - テストショットを1件ずつ実行する定型処理を提供する。テストクラスのスーパクラスになる
    - －

変更後
  * - ``BasicHttpRequestTestTemplate``
    - テストショットを1件ずつ実行する定型処理を提供する。テストクラスのスーパクラスになる
    - －
```

`mom.rst:143` の独自拡張用スーパクラスの一覧に残る `AbstractHttpRequestTestTemplate` は
変更しない。拡張する利用者が名前を書くものである。

### 4-3. `implementation/request_unit_test/rest.rst:40-42` に `SimpleRestTestSupport` を足す

同ページ `:53-54` は `RestTestSupport` と `SimpleRestTestSupport` を継承先の選択肢として
並べているのに、表には `RestTestSupport` しかない。

```
変更前
  * - ``RestTestSupport``
    - 内蔵サーバの起動や、リクエスト単体テストで必要となるステータスコードのアサートなどの機能を提供する。
    - －

変更後
  * - ``RestTestSupport``\ ・\ ``SimpleRestTestSupport``
    - 内蔵サーバの起動や、リクエスト単体テストで必要となるステータスコードのアサートなどの機能を提供する。テストクラスのスーパクラスになる。\ ``RestTestSupport``\ は、これにデータベース関連機能を加えたクラスである。
    - －
```

このファイルの表のセルは句点で終わる書式なので、それに合わせる。

---

## 5. 判断なしで直す6件

CC の判断のとおり直す。`web.rst:186` の `Run Configurations...` と
`checks/task-32.md` の jar の記録は、指示書の字面より CC の実測が正しい。

jar については私も実測した。`nablarch/test/core/http/dump/template.xls`（15872 バイト）は
1.2.0・1.3.0・2.0.0 のいずれにも存在し、1.3.0 以降で消えたのは `.class` 7件だけである。
`checks/task-32.md` の §2-2 の記録をこの内容に直す。`.. important::` の結論は倒れない。

---

## 6. `#33` を起こす

`steering.md` に次のタスクを新設する。**本タスクでは中身の作業をしない。**
Purpose と背景・未決点だけを書く。

見出し: `### #33: 記法の適用順序の明文化と、残置図の禁止語点検`

含める内容:

**(a) XLS-08 の記法明文化（converter からの申し送り）**

converter は解説書側へ明文化を申し送っている。`XlsFormatReader.java:557-560` 逐語:

> 記法は 2 つの規則の前後関係を定めていない。「除外 → 空エントリ判定」を前提とする
> （ユーザー確定・2026-08-18。解説書側へ明文化を申し送る）。課題は
> {@code coverage/issues.md} の XLS-08 に記録している。

未決点: 本体は現在**逆順**で動いている。`coverage/issues.md:499` 逐語:

> **原因は適用順序である。** 現状は**空エントリ判定をマーカーカラム除外の前に**行っている
> （本体 `PoiXlsReader#readLine` が生の行で判定 → `TableDataParser#onReadLine` が除外）。

したがって `implementation/testdata_notation.rst` に「除外 → 空エントリ判定」と書くことは、
NTF 本体の不具合を宣言することと同じである。他の `TODO(NTF-MOD-*)` と同じ判定を要する。

**(b) 残置図の禁止語**

`implementation/request_unit_test/images/mom/send_sync_base.png` に、`glossary.md` が禁止する
「自動テストフレームワーク」のノードが2つある（私が画像を開いて確認）。`ja/` 配下の png は26枚あり、
同種の全点検が要る。差し替え図の作成を伴う。

あわせて線引き（内部クラス構造を示す図は落とす／テスト範囲・作業の流れを示す図は残す）を
`design.md` §「利用側ページに内部構造の構成図を置かない」に追記する。

---

## 完了条件

1. `grep -n '空エントリ' ja/development_tools/testing_framework/tools/testdata_converter.rst` が0件
2. `grep -n 'マーカーカラム' ja/development_tools/testing_framework/tools/testdata_converter.rst` が
   `:39`・`:69`・`:278` の3件（`:37` に無い）
3. `grep -n 'testing_framework_setup' ja/development_tools/testing_framework/about/index.rst` が1件
4. `grep -c 'AbstractHttpRequestTestTemplate' ja/development_tools/testing_framework/implementation/request_unit_test/web.rst` が0
5. `_batch/*.csv` を昇順に連結（先頭のみヘッダ込み、2つ目以降はヘッダ除く）した結果が
   `mapping/mapping.csv` とバイト一致する。`csv.DictReader` の行数が編集前と同じ597行
6. `design.md` に `### 利用側ページに内部構造の構成図を置かない` が存在し、`:137` の見出しが
   `### 「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない` になっている
7. `steering.md` に `#33` のエントリが存在する
8. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK`
9. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`
10. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed`
11. Docker フルビルドで `grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。
    直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する
12. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・
    `locales/` の `.gitignore` 追加）に触れていない
13. `checks/task-32.md` に §1-3（`:278`）・§3-3（台帳7行）・§5（jar の実測）の記録がある
14. `#32` が check-off されている
