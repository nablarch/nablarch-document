# task-11 Completion Check

対象: `#11` 共通設定（`ja/development_tools/testing_framework/setup/common.rst`、新規作成 83行）
ベースコミット: `f4e4de8`（作業指示受領コミット `faca0e2` を含む。`faca0e2` は `steering.md` と作業指示書のみを変更）
作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-11-common.md`

## 作成したページの構成

| 行 | 種別 | 内容 |
|---|---|---|
| 1 | ラベル | `.. _testing_framework_common:` |
| 3-4 | L1 | `共通設定` |
| 6-8 | 目次 | `.. contents:: 目次` / `:depth: 3` / `:local:` |
| 10-11 | L2 | `使用方法` |
| 12 | 導入文 | 3つのL3の概要と、いずれもコンポーネント設定ファイルで設定する旨 |
| 14-15 | L3 | `テストデータの読み込み先を変更する` |
| 32-33 | L3 | `システム日時を固定する` |
| 47-48 | L3 | `シーケンス採番をテーブル採番に置き換える` |

`機能概要`・`拡張例` の見出しは置かない（出典0行）。トランザクションの節は作らない（割当行なし）。
L3の並びは作業指示 STEP 1 の確定どおり「読み込み先 → 日時固定 → 採番」である。

---

## ゲート（実行順。ゲート1を先頭に置く）

### ゲート1 — `dest_page=共通設定` の5行の全件反映対応表 → **PASS**

母集合の切り出しは `csv.DictReader` による全走査であり、ホワイトリストを使っていない。

```
python3 -c "
import csv
rows=[r for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv')) if r['dest_page']=='共通設定']
print(len(rows))
for r in rows: print(r['mapping_id'], r['src_body_start'], r['src_body_end'], r['lines'], r['dest_section'], r['disposition'])
"
```

出力（5件・129 lines・全件 `使用方法`／`MERGE`）:

```
5
current-0225 304 309 6  使用方法 MERGE
current-0226 312 342 31 使用方法 MERGE
current-0227 346 356 11 使用方法 MERGE
current-0228 359 388 30 使用方法 MERGE
current-0246 734 784 51 使用方法 MERGE
```

全5行の反映先対応表（母集合＝上記5行の全件。非反映の内容も理由を添えて記載する）:

| `mapping_id` | 出典行 | (i) 出典の内容の要旨 | (ii) 反映先セクションと `common.rst` の行 | (iii) 反映しなかった内容と理由 |
|---|---|---|---|---|
| `current-0225` | 304-309 | システム日時を設定する項目は実行日で値が変わるため自動テストで設定値を確認できないという課題／固定値を返す機能の提供／`SystemTimeProvider` インタフェースの実装クラスを固定値を返すテスト用クラスに差し替えるという仕組み | `使用方法 > システム日時を固定する`: `:34`（課題と機能の提供）、`:36` 前半（`SystemTimeProvider` の実装クラスがシステム日時を提供する／テストでは `FixedSystemTimeProvider` に差し替える） | なし（全件反映）。出典の見出し「システム日時を任意の値に固定したい」は `style.md` S-03 の「〜する」形式に置き換えた（`design.md` §7「〜したい形式の見出しを廃止する」） |
| `current-0226` | 312-342 | コンポーネント設定ファイルで `SystemTimeProvider` 実装クラス指定箇所を `FixedSystemTimeProvider` に置き換え `fixedDate` を設定する手順／2010年9月14日12時34分56秒の設定例XML／`fixedDate` の受け付ける形式の表／`SystemRepository` から `SystemTimeProvider` を取得し `getDate()` を呼ぶ Java コード例 | `使用方法 > システム日時を固定する`: `:36` 後半（設定手順と例の導入）、`:38-43`（設定例XML）、`:45`（`fixedDate` の受け付ける形式、および固定した日時が `SystemTimeProvider` を通じて取得される旨） | (a) **Java コード例（出典 `:334-338`）はコードブロックとして載せない。** `design.md` §3 記載範囲により、テストソースコードの実装例は第2部に置かない。内容（`SystemTimeProvider` を通じて取得される事実）は `:45` の地の文に保持（`reviews/page-common.md` D-2）。(b) **出典の「12桁 / 15桁」（`:330-331`）は写さない。** 実装は14桁 / 17桁であり `design.md` §8 により実装を優先（同 D-1）。(c) 出典の grid table（`:326-332`、データ行1件）は表にせず地の文にした。`style.md` S-07 が grid table を禁じており、かつ単一行の表は情報を増やさないため（同 D-4） |
| `current-0227` | 346-356 | シーケンスオブジェクトによる採番は次の採番値を予測できず期待値を設定できないという課題／設定ファイルの変更のみでテーブル採番に置き換える機能／手順①準備データをテーブルにセットアップ ②期待値はテーブルに設定した値を元に設定 | `使用方法 > シーケンス採番をテーブル採番に置き換える`: `:49`（課題・機能・手順①②を1段落で記述） | なし（全件反映）。出典の `|` 行ブロックによる①②の列挙は、2手順と短いため地の文に統合した（`style.md` に行ブロックの規約は無く、FW解説書のライブラリにも用例が無い） |
| `current-0228` | 359-388 | 本番用コンポーネント設定ファイルの `OracleSequenceIdGenerator` 設定例XML／テスト用で `FastTableIdGenerator` 設定に上書きする例XML／`IdGenerator` の Javadoc への `tip` | `使用方法 > シーケンス採番をテーブル採番に置き換える`: `:51`（本番用設定の導入）、`:53-65`（本番用XML）、`:67`（上書きの説明）、`:69-77`（テスト用XML）、`:79-81`（`IdGenerator` への `tip`）。加えて `:83` に記載例ページへの `:ref:` 導線 | なし（全件反映）。各プロパティの意味を補う説明は追加していない（作業指示 STEP 2-3・禁止事項。`OracleSequenceIdGenerator` / `FastTableIdGenerator` は `nablarch-testing` に存在せず未確認のため）。`:83` の `:ref:` は出典に無いが、`design.md` §3「『使い方』に該当するものは第3部に置き、第2部からは `:ref:` で参照する」に基づく導線であり、新規の主題内容ではない（`reviews/page-common.md` D-3） |
| `current-0246` | 734-784 | デフォルトの読み込み先 `test/java`／`nablarch.test.resource-root` のキーと値（カレントディレクトリからの相対パス、セミコロン区切りで複数指定可）／単一指定の設定例／複数指定の設定例／脚注1: VM引数による一時変更／脚注2: 同名のテストデータは最初に発見されたものが読み込まれる | `使用方法 > テストデータの読み込み先を変更する`: `:16`（デフォルト値・キー・値の意味）、`:18-20`（単一指定の設定例）、`:22`（セミコロン区切りと最初に見つかったものが読み込まれる旨＝脚注2）、`:24-26`（複数指定の設定例）、`:28-30`（VM引数の `tip`＝脚注1） | なし（全件反映）。ただし形は変えた。(a) **脚注（`.. [#]`）の形をそのまま持ち込まない**（作業指示 STEP 2-2・禁止事項）。脚注1は `tip`（`style.md` S-06「読まなくても機能は正しく使えるが知っておくと役立つ補足情報」）に、脚注2は本文の地の文に組み込んだ。(b) 単一行の simple table（`:740-745`）は表にせず地の文にした（`reviews/page-common.md` D-4）。(c) コードブロックの言語指定を `bash`/`text` から `properties` に統一した（`style.md` S-05。同 D-5） |

**5行すべてが表に現れている（5/5）。** 内容の欠落は0件であり、非反映としたのは `current-0226` の Java コード例（コードブロックの形のみ。事実は地の文に保持）と、出典の誤記（12桁/15桁）だけである。

### ゲート2 — `verify_mapping.py` が exit 0、594行 / 12,986 / 11,983 が不変 → **PASS**

```
cd .rn/20260724-ntf-yaml-support && python3 mapping/tools/verify_mapping.py
```

出力（抜粋）:

```
Loaded 594 rows from mapping.csv
pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11983
...
part2 optional sections (機能概要/拡張例) zero count: 18 (advisory only, not an error)
 - [第2部 導入と設定 > 共通設定 > 機能概要]: 0 row(s) (optional since #6, not an error)
 - [第2部 導入と設定 > 共通設定 > 拡張例]: 0 row(s) (optional since #6, not an error)
...
OK: no errors
EXIT=0
```

594 / 12986 / 11983 いずれも不変。`共通設定` の `機能概要`・`拡張例` が 0 row であることも同出力で確認でき、見出しを置かない判断（`design.md` §3）と一致する。

### ゲート3 — `mapping/` と `ja/conf.py` に差分が無い → **PASS**

```
git diff f4e4de8 HEAD -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py   # 出力なし
git diff f4e4de8      -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py | wc -l   # 0（作業ツリー込み）
git status --porcelain .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py    # 出力なし
```

禁止事項の個別ファイルも作業ツリー込みで 0 行差分を確認した。

| ファイル | `git diff f4e4de8 -- <path>` の行数 |
|---|---|
| `mapping/mapping.csv` | 0 |
| `mapping/_batch/` | 0 |
| `mapping/vocabulary.md` | 0 |
| `mapping/style.md` | 0 |
| `mapping/glossary.md` | 0 |
| `design.md` | 0 |
| `ja/conf.py` | 0 |

### ゲート4 — `testing_framework/` 配下の全 `.rst` に `テストケース` が0件 → **PASS**

```
grep -rn "テストケース" ja/development_tools/testing_framework/ --include=*.rst | wc -l
0
```

### ゲート5 — `common.rst` に `機能概要`・`拡張例` の見出しが0件、`使用方法` が1件 → **PASS**

```
grep -c "^機能概要$\|^拡張例$" ja/development_tools/testing_framework/setup/common.rst   → 0
grep -c "^使用方法$"           ja/development_tools/testing_framework/setup/common.rst   → 1
```

あわせてトランザクションの節が無いことも確認した（`grep -n "トランザクション" … | wc -l` → 0。XML例の `dbTransactionManager` は半角の属性値であり日本語の節見出しではない）。

### ゲート6 — `common.rst` に `12桁`・`15桁` が0件 → **PASS**

```
grep -c "12桁\|15桁" ja/development_tools/testing_framework/setup/common.rst
0
```

本文に書いた桁数は `:45` の「14桁」「17桁」のみである（実装優先。`reviews/page-common.md` D-1）。

### ゲート7 — `:ref:` がすべて解決し、`testdata_examples-table_data` への参照が1件以上ある → **PASS**

`common.rst` の `:ref:` は1件のみ。

```
grep -o ":ref:\`[^\`]*\`" ja/development_tools/testing_framework/setup/common.rst
:ref:`テーブルのデータを記述する <testdata_examples-table_data>`
```

ゲート10のフルビルドで `undefined label` 警告は `db_double_submit.rst:108` の既知1件のみであり、`common.rst` に対する未解決ラベル警告は0件。生成HTMLでリンクと着地点のアンカーの両方を実測した。

```
grep -o 'href="[^"]*testdata_examples[^"]*"' _build/html/development_tools/testing_framework/setup/common.html
href="../implementation/testdata_examples.html#testdata-examples-table-data"

grep -c 'id="testdata-examples-table-data"' _build/html/development_tools/testing_framework/implementation/testdata_examples.html
1
```

`:java:extdoc:` 3件も生成URLを実測した（ラベル解決の対象外だが、外部リンクとして生成されていることを確認）。

```
https://nablarch.github.io/docs/6-NEXT-SNAPSHOT/javadoc/nablarch/core/date/SystemTimeProvider.html
https://nablarch.github.io/docs/6-NEXT-SNAPSHOT/javadoc/nablarch/test/FixedSystemTimeProvider.html
https://nablarch.github.io/docs/6-NEXT-SNAPSHOT/javadoc/nablarch/common/idgenerator/IdGenerator.html
```

### ゲート8 — `setup/index.rst` の toctree に `common` があり、既存2件の順序が不変 → **PASS**

```
.. toctree::
   :maxdepth: 1

   common
   junit5_extension
   master_data_restore
```

差分は1行追加のみ（`git diff --stat f4e4de8 -- ja/` → `setup/index.rst | 1 +`）。生成HTMLの目次でも `共通設定 → JUnit 5用拡張機能 → マスタデータ復旧機能` の順を実測した。

### ゲート9 — 段落内改行が0件 → **PASS**

**検証方法（自作）**: 「空行を挟まずに日本語の行が連続している箇所」を機械的に数えるスクリプトを組んだ（`scratchpad/g9.py`）。付属の検証スクリプトは使っていない。手順は次のとおり。

1. `..` で始まり `::` を含む行をディレクティブとみなし、その行より深いインデントが続く範囲をリテラルブロック（`code-block` の中身など）として除外する。XMLコメント内の日本語を段落内改行と誤検出させないため
2. 残った行のうち、連続する2行がともに非空で、かつ両方に日本語文字（ひらがな・カタカナ・漢字）を含むものを「段落内改行」として計上する

`common.rst` の結果:

```
literal-block lines excluded: 28
paragraph-internal breaks: 0
```

**検出器が機能していることの対照実験**（0件が検出漏れでないことの確認）:

| ファイル | 検出件数 | 備考 |
|---|---|---|
| `FW:libraries/date.rst` | 15 | 段落内で改行するFW解説書。陽性対照として期待どおり検出 |
| `implementation/testdata_notation.rst` | 15 | 箇条書き項目・表の行の連続を拾ったもの（段落内改行ではない）。検出器が「連続する日本語行」を漏れなく拾うことの確認 |
| `about/index.rst` | 5 | 同上（simple table の行） |
| `setup/common.rst` | **0** | 本ページ |

`common.rst` は箇条書き・表を持たないため、0件がそのまま「段落内改行0件」を意味する。

### ゲート10 — Docker フルビルドが `build succeeded`、警告は既知の1件のみ → **PASS**

```
docker run --rm -v /home/tie303177/work/lovaizu/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

- 終了コード: `0`
- ログ末尾: `build succeeded, 1 warning.`
- 警告の全件（`grep -i "WARNING"`）:

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108:
  WARNING: undefined label: how_to_set_token_in_request_unit_test
  (if the link has no caption the label must precede a section header)
```

既知の `db_double_submit.rst` 1件のみで、新規警告は0件。`_build` ディレクトリは削除していない（ユーザーがHTMLを直接レビューするため）。

### ゲート11 — `ja/` 配下の変更が `common.rst`（新規）と `index.rst`（toctree 1行追加）だけ → **PASS**

```
git diff --stat f4e4de8 -- ja/
 ja/development_tools/testing_framework/setup/index.rst | 1 +
 1 file changed, 1 insertion(+)

git ls-files --others --exclude-standard ja/
ja/development_tools/testing_framework/setup/common.rst
```

`ja/` 配下の変更はこの2ファイルのみ。作業ツリー全体でも、これに `.rn/.../reviews/page-common.md`（新規）と `.rn/.../checks/task-11.md`（新規・コミットしない）が加わるだけである。

---

## Method の適用確認 — 本文の全主張の裏取り一覧

`common.rst` の地の文・コードブロックに書いたクラス名・プロパティ名・キー名・既定値・桁数・挙動を全件洗い出し、
出典行または実装 `file:line` を対応させた。**未確認のまま書いた主張は0件である。**

出典は `03_Tips.rst`（`git show 2e501ad:ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst`）。
実装は `nablarch/nablarch-testing` の `main`（`e21bf67`）で、作業指示 STEP 2 に記録された確認結果を根拠として採用した
（本タスクでは起動ディレクトリ外のため再取得していない）。

| # | `common.rst` | 主張 | 裏取り |
|---|---|---|---|
| 1 | `:12` | 3つの設定はいずれもコンポーネント設定ファイルで行う | 出典 `:313`（日時固定）、`:359`・`:375`（採番の本番用／テスト用設定ファイル）、`:738`（読み込み先） |
| 2 | `:16` | テストデータのデフォルトの読み込み先は `test/java` 配下 | 出典 `:735`。実装 `TestSupport.java:30`（既定値 `test/java/`） |
| 3 | `:16` | キー名は `nablarch.test.resource-root` | 出典 `:743`。実装 `TestSupport.java:33` |
| 4 | `:16` | 値はテスト実行時のカレントディレクトリからの相対パス | 出典 `:743` |
| 5 | `:16` | 設定先はコンポーネント設定ファイル | 出典 `:738` |
| 6 | `:20` | 設定例 `nablarch.test.resource-root=path/to/test-data-dir` | 出典 `:755` |
| 7 | `:22` | 区切り文字はセミコロン（`;`） | 出典 `:744`・`:760`。実装 `TestSupport.java:42,329` |
| 8 | `:22` | 複数指定時、同名のテストデータファイルは最初に見つかったものが読み込まれる | 出典 `:778-779`（脚注2）。実装 `TestSupport.java:285,291-298` |
| 9 | `:26` | 複数指定の例 `nablarch.test.resource-root=test/online;test/batch` | 出典 `:765` |
| 10 | `:30` | VM引数 `-Dnablarch.test.resource-root=path/to/test-data-dir` で一時的に変更できる | 出典 `:770-773`（脚注1） |
| 11 | `:34` | システム日時を設定する項目は実行日によって値が変わり、設定値が正しいことを自動テストで確認できない | 出典 `:304` |
| 12 | `:34` | テスティングフレームワークはシステム日時に固定値を返す機能を提供する／これにより期待値と比較して確認できる | 出典 `:305` |
| 13 | `:36` | Nablarch Application Framework では `SystemTimeProvider` インタフェースの実装クラスがシステム日時を提供する | 出典 `:307` |
| 14 | `:36` | `SystemTimeProvider` の完全修飾名は `nablarch.core.date.SystemTimeProvider` | `FW:libraries/date.rst:147` の `:java:extdoc:` 実績（`grep` で確認）。生成HTMLのURLでも実測 |
| 15 | `:36`,`:41` | 差し替え先は `nablarch.test.FixedSystemTimeProvider` | 出典 `:320`。実装 `FixedSystemTimeProvider.java:1,20` |
| 16 | `:36`,`:42` | プロパティ名は `fixedDate` | 出典 `:321`・`:329`。実装 `FixedSystemTimeProvider.java:42`（`setFixedDate(String)`） |
| 17 | `:38-43` | 設定例XML（`component name="systemTimeProvider"` / `fixedDate` = `20100914123456`） | 出典 `:319-322` を逐語で引き継ぐ（コードブロックは書き直し対象外） |
| 18 | `:36` | 例は2010年9月14日12時34分56秒 | 出典 `:315` |
| 19 | `:45` | 受け付ける形式は `yyyyMMddHHmmss` または `yyyyMMddHHmmssSSS` | 出典 `:330-331`。実装 `FixedSystemTimeProvider.java:23,26` |
| 20 | `:45` | 桁数は **14桁 / 17桁** | 実装 `FixedSystemTimeProvider.java:23,26`（フォーマット文字列）、`:46,48`（`LONGEST_FORMAT.length()` / `SHORTEST_FORMAT.length()` による判定）。**出典 `:330-331` の「12桁 / 15桁」は誤りとして採用せず**（`design.md` §8、`reviews/page-common.md` D-1）。出典自身の例 `20100914123456`（`:321`）も14桁 |
| 21 | `:45` | 固定した日時は `SystemTimeProvider` を通じて取得される | 出典 `:336-338`（Javaコード例の内容を地の文化。`reviews/page-common.md` D-2） |
| 22 | `:49` | シーケンスオブジェクトによる採番は次の値を予測できず期待値を設定できない | 出典 `:346` |
| 23 | `:49` | コンポーネント設定ファイルの変更だけでテーブル採番に置き換えられる | 出典 `:347` |
| 24 | `:49` | 採番用テーブルに準備データを投入し、その値を元に期待値を設定することで採番処理を確認できる | 出典 `:348`・`:352-353`（手順①②） |
| 25 | `:51`,`:56` | 本番用の設定クラスは `nablarch.common.idgenerator.OracleSequenceIdGenerator` | 出典 `:364`。**実装未確認**（`nablarch-testing` に存在せず、Nablarch本体側のクラス）。出典以上のことは書いていない（作業指示 STEP 2-3） |
| 26 | `:53-65` | 本番用設定例XML（`idTable` の `map`、`1101`〜`1104` → `SEQ_1`〜`SEQ_4`） | 出典 `:363-373` を引き継ぐ。各プロパティの意味の説明は追加していない |
| 27 | `:67` | テスト用の設定ファイルで本番用の設定をテーブル採番の設定で上書きする | 出典 `:375` |
| 28 | `:72` | テスト用の設定クラスは `nablarch.common.idgenerator.FastTableIdGenerator` | 出典 `:380`。**実装未確認**（同上） |
| 29 | `:69-77` | テスト用設定例XML（`tableName`・`idColumnName`・`noColumnName`・`dbTransactionManager`） | 出典 `:379-385` を引き継ぐ。出典 `:384` の `/ >`（空白入り）は `/>` に直した。各プロパティの意味の説明は追加していない |
| 30 | `:81` | 設定値の詳細は `nablarch.common.idgenerator.IdGenerator` の Javadoc を参照 | 出典 `:387` の `tip`（`:java:extdoc:` ごと引き継ぎ） |
| 31 | `:83` | 記述例の参照先ラベル `testdata_examples-table_data` と見出し「テーブルのデータを記述する」 | `testdata_examples.rst:776`（ラベル）、`:778`（見出し）。生成HTMLでアンカー着地も実測（ゲート7） |
| 32 | 全体 | 用語（`コンポーネント設定ファイル`・`テストデータ`・`テストデータファイル`・`準備データ`・`期待値`・`テスティングフレームワーク`） | `glossary.md:281`・`:207`・`:208`・`:217`・`:218`・`:119` の正表記に一致。禁止語 `テストケース` は0件（ゲート4） |
| 33 | 全体 | 表記「デフォルト」（「既定」を使わない） | `FW:libraries/*.rst` の実測で `デフォルト` が多数（`tag.rst` 48件ほか）に対し `既定` は0件。承認済みの `testdata_notation.rst`・`testdata_examples.rst` も `デフォルト` を使用 |

---

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 作業指示のゲート1〜11 がすべて実行結果で確認され、`checks/task-11.md` に記録されている | OK | 本ファイル「ゲート」節に11件すべて、実行コマンドと出力の要点つきで記録。全件 PASS。ゲート1を実行順の先頭に置いた |  |  |
| `dest_page=共通設定` の5行が全件、反映先のセクションと行番号の対応表で記録されている（母集合をホワイトリストで切り出さない） | OK | ゲート1の表に5/5行を記載。母集合は `csv.DictReader` で `dest_page=='共通設定'` を全走査して得た5行そのもの。非反映の内容（Javaコード例・出典の誤記・表の形）も理由つきで (iii) 列に記載 |  |  |
| 4観点のレビューがすべて実施・記録され、未対応の `must` が残っていない（または残す判断とその理由が記録されている） | NG（本タスクの範囲外） | 4観点レビューは作業指示 STEP 5 によりコーディネーター側の別サブエージェントが実施する。`reviews/page-common.md` に記録欄（ラウンド1の表）を用意済み。現時点で未実施のため `must` の有無は判定不能 | OK | 4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）をそれぞれ別のサブエージェントで実施し、`reviews/page-common.md` のラウンド1に R1-1〜R1-12 を全件記録した。`must` 2件（R1-1 設定先の語、R1-2 実在しないクラス名）は是正ラウンド1（`0a71a75`）で解消。是正後の限定検証（是正差分に限定した観点のみ、`#10b` 申し送り）で `must` 0 / `should` 0 の pass。**未対応の `must` は0件** |
| `setup/common.rst` に `機能概要`・`拡張例` の見出しが0件、`使用方法` が1件、`12桁`・`15桁` が0件、トランザクションの節が0件 | OK | ゲート5（0件 / 1件、トランザクション節0件）、ゲート6（0件） |  |  |
| `setup/common.rst` から `testdata_examples-table_data` への `:ref:` が1件以上あり、すべての `:ref:` が解決する | OK | ゲート7。`:ref:` は当該1件のみ。生成HTMLで `#testdata-examples-table-data` へのリンクと着地点アンカーの両方を実測。ビルド警告に未解決ラベルは無し |  |  |
| 作業指示の禁止事項に抵触する変更が無い（`mapping.csv` / `_batch/` / `vocabulary.md` / `style.md` / `glossary.md` / `design.md` / `ja/conf.py` に差分が無く、`ja/` 配下の変更が `setup/common.rst` と `setup/index.rst` だけである） | OK | ゲート3（禁止7ファイルすべて `git diff f4e4de8` で0行）、ゲート11（`ja/` の差分は `index.rst` 1行追加＋未追跡の `common.rst` のみ）。`steering.md` は変更していない |  |  |
| Docker フルビルドが `build succeeded` で、警告が既知の `db_double_submit.rst` 1件のみ（新規0件） | OK | ゲート10。`build succeeded, 1 warning.`／警告は `db_double_submit.rst:108` の1件のみ／`_build` は削除していない |  |  |

## QA Expert Review（観点A: 網羅性）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | OK | マッピング5行の母集合を `csv.DictReader` で全594行から独立に確定し（`dest_page` を `Counter` で全件列挙、「共通」を含む行・前後空白/全角空白混入も別途走査して追加0件）、出典129行を**空行・`\` エスケープ行まで含めて1行残らず**走査した。逆方向（本文→出典）も全走査し、本文中の全リテラル12件を出典と突合。落ちている内容0件、出典にも実装確認結果にも根拠の無い記述0件。`verify_mapping.py` は「合格の証拠」として使っていない。`must` 0 / `should` 0 / `note` 7 で pass |

## Expert Reviews

### Design Expert（観点D: 整合性）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK | `design.md` §3 の第2部アウトラインに整合（`使用方法` のみ・`機能概要`/`拡張例` 0件）。記載範囲の線引きも守られている（Javaコード例なし・テストデータ記述例なし、内容は地の文と `:ref:` で保持）。L3の並びは指示どおり「読み込み先 → 日時固定 → 採番」。導入文と3つのL3が語・順序とも一致 |
| System-wide integrity | OK（是正後） | **初回レビューで `must` 1件を検出**: `nablarch.common.idgenerator.OracleSequenceIdGenerator` が実在しないクラスであること（公開javadoc `6u2` で当該クラスのみ 404、兄弟クラス `FastTableIdGenerator`/`SequenceIdGeneratorSupport`/`TableIdGenerator`/`IdGenerator` は 200。同文書セットの `setting_guide/CustomizingConfigurations/index.rst:141` は同名クラスを `com.example` 名前空間で記載）。コーディネーターが javadoc の HTTP ステータスと当該既存ページを独立に実測して確認し、`design.md` §8 により是正（R1-2、`0a71a75`）。是正後は `:ref:` 2件とも解決、toctree 既存順不変、承認済み3ページとの矛盾なし |

### Craft Expert (writing)（観点B: トンマナ）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK（是正後） | `style.md` S-01〜S-11 の**全条**を突合し、機械判定可能な違反0件。段落内改行は独立検出器（陽性対照 `date.rst` で検出できることを事前確認）で0件。出典の逐語流用は地の文0件（`difflib` 総当たりで最大類似度0.88、逐語一致はコードブロックのみ）。脚注 `.. [#]`・「〜したい」形式見出しの持ち込みも0件。`should` 3件のうち F2（読み込み順を `important` に）を是正（R1-3）、F1 は用語観点の `must` と同一原因で是正（R1-1）、F3（採番プロパティの説明追加）は作業指示の禁止事項に抵触するため却下 |
| Consistency with existing style | OK | 見出し下線長の構成 `{=:50, -:50, ~:49}` が承認済み `about/index.rst` と完全一致。`.. contents::` の3行・2字インデントが `date.rst:4-6`・`about/index.rst:6-8` とバイト一致。アドモニション書式は `about/index.rst` および FW解説書ライブラリの用例と同一。インラインマークアップのエスケープは `pre_esc:13/pre_none:0`・`post_esc:14/post_none:0` でページ内完全一貫 |

### Verification Expert (fact-check)（観点C: 用語 ＋ 観点D の事実確認）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | OK（是正後） | 観点D が `nablarch-testing@e21bf67` を独自に clone し、本文の全主張27件を出典行または実装 `file:line` に対応させて検証。本タスクの目玉である「桁数 12/15 → 14/17 の是正」は `FixedSystemTimeProvider.java:23,26,46,48` を独立に読んで**正しいと確認**（実装Javadoc `:35-36` 側の同じ誤りも再現）。`nablarch.test.resource-root` の既定値・区切り・探索順も `TestSupport.java:30,33,42,308-315` と一致。Docker フルビルドは実装担当・観点D・観点B・限定検証の**4者が独立に実行**し、いずれも `build succeeded, 1 warning.`（既知の `db_double_submit.rst:108` のみ・新規0件） |
| Coverage | OK（是正後） | **初回レビューで `must` 1件を検出**: `nablarch.test.resource-root` の設定先を `コンポーネント設定ファイル` と書いていたが、`glossary.md` §5.12 は同語を「XMLファイル」と定義しており、`:18` の `properties` コードブロックと矛盾していた。コーディネーターが `repository.rst:478,504,537` および**削除前の現行NTF解説書自身**（`04_MasterDataRestore.rst:103` が同じ `nablarch.*=値` 形式を「環境設定ファイル」と呼び、直後の節で「コンポーネント設定ファイルに監視対象テーブルを記載」＝XML と書き分けている）を実測して確認し、是正（R1-1、`0a71a75`）。用語検査そのものは、`glossary.md` の揺れ表記**92件全件**が0件、本文出現語68塊の全件判定でも揺れ表記0件、独立母集合（`scan-terms.tsv` 193表記・`term-candidates.csv` 339候補）でもヒットは全て正表記側 |

## Overall Verdict

- Self-check: OK（ただし4観点レビューはコーディネーター側の実施待ちで、その1項目のみ未充足）
- QA（観点A: 網羅性）: OK
- Design expert（観点D: 整合性）: OK（初回 fail → 是正ラウンド1 で解消）
- Craft expert（観点B: トンマナ）: OK（初回 条件付き pass → 是正ラウンド1 で `should` 解消）
- Verification expert（観点C: 用語 ＋ 事実確認）: OK（初回 条件付き pass → 是正ラウンド1 で `must` 解消）
- Ready to check off: Yes（**user review の承認待ち**。`steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」により、`complete task #11` のマーカーは承認後に付す）

### レビューラウンドの記録（`#10b` 申し送り — レビューサイクル改善の効果測定用）

| ラウンド | 観点 | `must` | `should` | `note` | 判定 |
|---|---|---|---|---|---|
| 1 | A: 網羅性 | 0 | 0 | 7 | pass |
| 1 | B: トンマナ | 0 | 3 | 3 | 条件付き pass |
| 1 | C: 用語 | 1 | 1 | 4 | 条件付き pass |
| 1 | D: 整合性 | 1 | 2 | 4 | fail |
| 1 合計 | — | **2** | **6** | **18** | — |
| 2（是正後） | 是正差分限定（是正が指示範囲に収まっているか / 新しい欠陥を生んでいないか） | **0** | **0** | 2 | **pass** |

**ラウンド2で全観点の再走査を行わなかったのは `#10b` の申し送りによる。** `#10b` は全観点を3巡繰り返した結果、毎巡あたらしい観点の指摘が出てラウンドが伸び、公開本文の是正は一度も発生しなかった。本タスクではラウンド2の観点を「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」の2点に限定し、**1巡で収束した**（是正ラウンドは1回、レビューは計2巡）。`#10b` の3巡＋4是正ラウンドに対し、明確に短縮している。

---

## コーディネーターに上げる論点

1. **`:ref:` の表示テキストを作業指示から変更した。** 作業指示 STEP 3-2 は `` :ref:`テーブルデータを記述する <testdata_examples-table_data>` `` と指定していたが、参照先の実際の見出しは `testdata_examples.rst:778` 「テーブル**の**データを記述する」である。参照先の見出し文言に揃える方が整合するため、実見出しの表記を採用した（`reviews/page-common.md` D-3）。ラベル自体は指定どおり `testdata_examples-table_data` であり、ゲート7の要件は満たしている
2. **採番の記述例へのピンポイント参照は申し送りにした。** 現状の `:ref:` は L2 セクションを指しており、読者は着地後にページ内で L3 `採番処理のテストデータを記述する` を探す必要がある。`#10` 成果物にラベルを足さない禁止事項があるため、ラベル追加は行っていない（`reviews/page-common.md` D-3 の申し送り欄）
3. **本ページは表を1件も持たない。** 出典の2つの表はいずれもデータ行1件で、表にしても情報が増えないため地の文にした（`reviews/page-common.md` D-4）。`design.md` §3 の記載範囲は「コンポーネント設定ファイルの設定項目一覧」を第2部に置くとしており、設定項目が複数あるページでは表を使うことになる。本ページに限った判断である
4. **採番の2クラスは実装未確認のままである。** `OracleSequenceIdGenerator` / `FastTableIdGenerator` は `nablarch-testing` に存在せず（`e21bf67` で grep 0件）、Nablarch本体側のクラスである。作業指示 STEP 2-3 に従い出典以上のことは書いていないが、事実確認は未了である

---

## 是正ラウンド1

レビュー ラウンド1 の指摘に対する是正（`reviews/page-common.md` の R1-1〜R1-4）の検証記録。
`#10b` の申し送りに従い、**是正差分に限定した観点**（是正が指示範囲に収まっているか／是正が新しい欠陥を生んでいないか）のみを回した。4観点の全再走査は行っていない。

対象コミット: `d233c4b`（ページ作成）に対する是正差分。ベースは引き続き `f4e4de8`。

### 是正1〜4の適用箇所

| 是正 | 指摘ID | 変更前（該当行） | 変更後（該当行） |
|---|---|---|---|
| 是正1 | R1-1 | `:12` `…について説明する。いずれもコンポーネント設定ファイルで設定する。` | `:12` `…について説明する。いずれも設定ファイルへの記述で行う。` |
| 是正1 | R1-1 | `:16` `…読み込み先を変更する場合は、コンポーネント設定ファイルに ``nablarch.test.resource-root`` を設定する。` | `:16` `…読み込み先を変更する場合は、環境設定ファイルに ``nablarch.test.resource-root`` を設定する。` |
| 是正1 | R1-1 | `:30` `読み込み先を一時的に変更したい場合は、コンポーネント設定ファイルを変更せずに、テスト実行時のVM引数に ``-Dnablarch.test.resource-root=path/to/test-data-dir`` を指定してもよい。` | `:34` `読み込み先を一時的に変更したい場合は、環境設定ファイルを変更せずに、テスト実行時に ``-Dnablarch.test.resource-root=path/to/test-data-dir`` をシステムプロパティとして指定してもよい。詳細は :ref:`システムプロパティを使って環境依存値を上書きする <repository-overwrite_environment_configuration>` を参照。` |
| 是正2 | R1-2 | `:56` `<component name="idGenerator" class="nablarch.common.idgenerator.OracleSequenceIdGenerator">` | `:60` `<component name="idGenerator" class="com.example.common.idgenerator.OracleSequenceIdGenerator">` |
| 是正3 | R1-3 | `:22` `読み込み先は、セミコロン（ ``;`` ）で区切って複数指定できる。複数指定した場合、同名のテストデータファイルが複数のディレクトリに存在すると、最初に見つかったものが読み込まれる。` | `:22` `読み込み先は、セミコロン（ ``;`` ）で区切って複数指定できる。` ＋ `:28-30` `.. important::` / `同名のテストデータが複数のディレクトリに存在する場合、最初に見つかったものが読み込まれる。` |
| 是正4 | R1-4 | `:36`（4文・約230字）`…テストでは、この実装クラスを、固定値を返す FixedSystemTimeProvider に差し替える。コンポーネント設定ファイルで ``SystemTimeProvider`` インタフェースの実装クラスを指定している箇所を次のように書き換え、``fixedDate`` プロパティに固定したい日時を指定する。…` | `:40`（3文）`…テストでは、コンポーネント設定ファイルでこの実装クラスを指定している箇所を、固定値を返す FixedSystemTimeProvider に差し替え、``fixedDate`` プロパティに固定したい日時を指定する。…` |

### 検証1 — 是正が指示範囲に収まっているか → **PASS**

```
git diff --numstat -- ja/development_tools/testing_framework/setup/common.rst
10      6       ja/development_tools/testing_framework/setup/common.rst

git diff -U0 -- ja/development_tools/testing_framework/setup/common.rst | grep -c "^[+-][^+-]"
14
```

差分の実体行は 14 行（削除6 / 追加10、うち追加4行は `.. important::` ブロックと空行）。行単位の内訳:

| 差分の行 | 対応する是正 | 指示範囲内か |
|---|---|---|
| `-:12` / `+:12`（L2導入文） | 是正1（設定先を断定しない書き方に改める） | 内 |
| `-:16` / `+:16`（読み込み先の設定先） | 是正1（`環境設定ファイル` へ） | 内 |
| `-:22` / `+:22`（第2文の除去） | 是正3（`important` へ出す） | 内 |
| `+:28-30`（`.. important::` ブロック新設・3行＋前後の空行） | 是正3 | 内 |
| `-:30` / `+:34`（`tip` 本文） | 是正1（`システムプロパティ` と `-D`、`:ref:` 追加） | 内 |
| `-:36` / `+:40`（日時固定の段落） | 是正4（重複説明の統合） | 内 |
| `-:56` / `+:60`（クラス名） | 是正2（`com.example.` へ） | 内 |

**指示していない箇所の変更は0件。** 特に次は変更していないことを差分で確認した。

- コードブロックの言語指定 `properties`（是正1で据え置きを明示指示）
- `FastTableIdGenerator`（`:76`）のクラス名とその4プロパティ
- `fixedDate` の桁数記述（14桁 / 17桁）
- 末尾の `` :ref:`テーブルのデータを記述する <testdata_examples-table_data>` ``
- `IdGenerator` への `tip`、3件の `:java:extdoc:`
- セクション構成（L2 1件・L3 3件）、ページ先頭ラベル、`.. contents::`
- `setup/index.rst`（是正ラウンドでは無変更）

### 検証2 — 是正が新しい欠陥を生んでいないか → **PASS**

```
F=ja/development_tools/testing_framework/setup/common.rst

grep -c "^機能概要$\|^拡張例$" $F                                    → 0
grep -c "^使用方法$"           $F                                    → 1
grep -c "12桁\|15桁"           $F                                    → 0
grep -rn "テストケース" ja/development_tools/testing_framework/ --include=*.rst | wc -l → 0
grep -c "VM引数"               $F                                    → 0   （是正1で消えた）
grep -c "nablarch.common.idgenerator.OracleSequenceIdGenerator" $F   → 0   （是正2で消えた）
grep -c "^.. important::"      $F                                    → 1   （是正3で新設）
```

`VM引数` は `ja/` 全体でも `migration/index.rst:476` の `JVM引数`（別語）のみとなり、`VM引数` 単独の出現は0件。

**`:ref:` の解決**（生成HTMLで実測。是正1で新設した1件を含む）:

```
grep -o ":ref:\`[^\`]*\`" $F
:ref:`システムプロパティを使って環境依存値を上書きする <repository-overwrite_environment_configuration>`
:ref:`テーブルのデータを記述する <testdata_examples-table_data>`

grep -o 'href="[^"]*\(repository\|testdata_examples\)[^"]*"' _build/html/development_tools/testing_framework/setup/common.html
href="../../../application_framework/application_framework/libraries/repository.html#repository-overwrite-environment-configuration"
href="../implementation/testdata_examples.html#testdata-examples-table-data"

grep -c 'id="repository-overwrite-environment-configuration"' _build/html/application_framework/application_framework/libraries/repository.html   → 1
grep -c 'id="testdata-examples-table-data"'                   _build/html/development_tools/testing_framework/implementation/testdata_examples.html → 1
```

新設した `:ref:` の着地点アンカーも実測で確認した。`testdata_examples-table_data` への参照は1件残っている。表示テキスト `システムプロパティを使って環境依存値を上書きする` は参照先の実見出し（`FW:libraries/repository.rst:547`）と一致する。

**段落内改行が0件**（自作検出器 `scratchpad/g9.py`。付属の検証スクリプトは使っていない）:

```
python3 g9.py ja/application_framework/application_framework/libraries/date.rst   ← 陽性対照
literal-block lines excluded: 39
paragraph-internal breaks: 15

python3 g9.py ja/development_tools/testing_framework/setup/common.rst
literal-block lines excluded: 29
paragraph-internal breaks: 0
```

陽性対照 `date.rst` で 15 件を検出しており、検出器が機能していることを先に確認したうえで `common.rst` の 0 件を得た。
検出器はディレクティブ配下をリテラルブロックとして除外するため、新設した `.. important::` と書き換えた `.. tip::` の本文は除外側に入る。両者とも本文が**1行**であることを別途 `awk` で確認した（`:30` と `:34`。段落内改行の余地が無い）。

**マッピングと禁止ファイル**:

```
cd .rn/20260724-ntf-yaml-support && python3 mapping/tools/verify_mapping.py   → EXIT=0
Loaded 594 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors

git diff f4e4de8 HEAD -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py | wc -l   → 0
```

594 / 12,986 / 11,983 いずれも不変。

**`ja/` 配下の変更範囲**:

```
git diff --stat f4e4de8 -- ja/
 .../testing_framework/setup/common.rst | 87 ++++++++++++++++++++++
 .../testing_framework/setup/index.rst  |  1 +
 2 files changed, 88 insertions(+)
```

`ja/` 配下の変更は `setup/common.rst` と `setup/index.rst` の2ファイルのみ（是正ラウンド1で `index.rst` は無変更）。

### 検証3 — Docker フルビルド → **PASS**

```
docker run --rm -v /home/tie303177/work/lovaizu/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

- 終了コード: `0`
- ログ末尾: `build succeeded, 1 warning.`
- 警告の全件:

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108:
  WARNING: undefined label: how_to_set_token_in_request_unit_test
  (if the link has no caption the label must precede a section header)
```

既知の `db_double_submit.rst` 1件のみで、**新規警告は0件**。是正1で新設した `:ref:` による `undefined label` 警告も出ていない。
`_build` ディレクトリは削除していない（ユーザーがHTMLを直接レビューするため）。
ビルドで変更された `locales/ja/LC_MESSAGES/sphinx.mo` は `git checkout --` で復元し、コミットに含めていない。

### 是正ラウンド1のまとめ

| 検証 | 結果 |
|---|---|
| 1. 是正が指示範囲に収まっているか | PASS（差分14行すべてが是正1〜4に対応。指示外の変更0件） |
| 2. 是正が新しい欠陥を生んでいないか | PASS（全 grep 項目が期待値どおり。段落内改行0件、`:ref:` 全件解決、マッピング不変） |
| 3. Docker フルビルド | PASS（`build succeeded, 1 warning.`、新規警告0件） |

NG は0件。
