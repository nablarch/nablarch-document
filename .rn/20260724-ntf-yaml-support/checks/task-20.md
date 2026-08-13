# `#20` self-check — リクエスト単体テストの設定（Nablarchバッチアプリケーション）

対象ページ: `ja/development_tools/testing_framework/setup/request_unit_test/batch.rst`（新規作成）

着手時の HEAD: `499304a`（作業指示に明示されたもの）。作業ツリーの直前のコミットは `9f0eb52`。

## ゲート1 — マッピング全件（母集合を先に固定。ホワイトリストで切り出さない）

母集合は `mapping.csv` の**全594行**を `csv.DictReader` で読み、`dest_page` が
`リクエスト単体テストの設定（Nablarchバッチアプリケーション）` である行を抽出した（`wc -l` は使っていない）。
抽出結果は**3行**で、`DROP` は0件である。

| `mapping_id` | 出典 | 範囲 | `lines` | `disposition` | 反映先セクション |
|---|---|---|---|---|---|
| `current-0037-b` | `.../05_UnitTestGuide/02_RequestUnitTest/batch.rst` | `263`〜`316` | 54 | SPLIT | 「符号無数値・符号付数値のテスト用データ型を登録する」（`batch.rst:80-119`）。うちテストデータの記述に関する部分は地の文として保持し、記述方法は第3部へ `:ref:`（ゲート4） |
| `current-0291` | `.../06_TestFWGuide/RequestUnitTest_batch.rst` | `186`〜`222` | 37 | MOVE | 「常駐バッチのループ制御ハンドラを置き換える」（`batch.rst:15-37`） |
| `current-0292` | `.../06_TestFWGuide/RequestUnitTest_batch.rst` | `225`〜`262` | 38 | MOVE | 「ディレクティブの既定値を設定する」（`batch.rst:39-78`） |

合計 129 lines。反映漏れ**0件**。

出典の実物は、現行解説書が本ブランチで削除済みのため `git show origin/develop:<src_file>` で読んだ。
`note` 欄の説明文は根拠にしていない。

### 出典の各要素とページ内の対応（落としていないことの確認）

| 出典の要素 | 出典の所在 | ページでの扱い |
|---|---|---|
| 常駐バッチのテストで本番用ハンドラ構成のままではテストが終わらない | `current-0291`（`:186-187`） | `batch.rst:17` |
| 変更対象・変更後のハンドラと変更理由の表 | `current-0291`（`:189-200`） | 表を置かず地の文にした（`batch.rst:17`・`:19`）。データ行が1件のみの表で、3列の内容がそのまま文になるため |
| プロダクション用設定のXML例 | `current-0291`（`:204-211`） | `batch.rst:21-26` |
| テスト用設定のXML例と同名上書きの説明 | `current-0291`（`:213-220`） | `batch.rst:28-33`・`:35-37` |
| ディレクティブの既定値をコンポーネント設定ファイルに書ける旨 | `current-0292`（`:226-233`） | `batch.rst:41` |
| 対象ファイル種別と `name` 属性の対応表 | `current-0292`（`:235-241`） | `batch.rst:43-54` |
| 設定例のXML | `current-0292`（`:244-262`） | `batch.rst:58-74` |
| 符号無数値・符号付数値のテストデータには固定長ファイル上の表現をそのまま書く | `current-0037-b`（`:264-265`） | `batch.rst:82`（地の文。第3部へ `:ref:`） |
| 表したい数値とテストデータ上の記載の例（フォーマット定義の条件つき） | `current-0037-b`（`:267-274`） | `batch.rst:82`（表を置かず地の文に残した。ゲート4） |
| テスト用のデータ型を設定する必要がある旨 | `current-0037-b`（`:276-278`） | `batch.rst:84` |
| `fixedLengthConvertorSetting` のXML例（既定の設定を併記しないと上書きされる旨のコメントを含む） | `current-0037-b`（`:280-316`） | `batch.rst:86-119`（コメントの内容は `important` に移した） |

## ゲート2 — ページ先頭ラベル

`style.md` S-08「NTF解説書のページ先頭ラベル一覧」の表から引用した。**新規考案なし。**

- ページ: `リクエスト単体テストの設定（Nablarchバッチアプリケーション）`（`style.md:352`）
- ファイル: `setup/request_unit_test/batch.rst`（S-08 の表・`design.md:863` と一致）
- ラベル: `request_unit_test_setting_batch`（S-08 の表と一致）

`ja/` 全体に同名ラベルが存在しないことを確認した（`grep -rn "^\.\. _\`\?request_unit_test_setting_batch\`\?:" --include=*.rst ja/` が本ページ以外0件）。

## ゲート3 — 実装で確認した事実

### 参照した成果物とコミット

| 成果物 | 取得元 | 参照コミット・版 |
|---|---|---|
| `nablarch/nablarch-testing` | ローカルクローン | `main` = **`e21bf67`**（ローカルの作業ブランチ HEAD は `fdf55d4`。本ページが引用する `OneShotLoopHandler.java`・`core/file/` 配下・`src/test/resources/unit-test.xml` は両者で**差分0**であることを `git diff --name-only fdf55d4 e21bf67 -- <対象>` で確認した。差分があったのは `core/reader/DataFileParser.java` 1件のみで、引用箇所（`processDirectives`）の本文は同一。行番号は `e21bf67` のものを記載） |
| `com.nablarch.framework:nablarch-core-dataformat` | ローカル Maven リポジトリの jar | `6-NEXT-SNAPSHOT`（MANIFEST の `git-hash: f21787e4bead839d194139c1a7cd9d8b02940e41`） |
| `com.nablarch.framework:nablarch-fw-standalone` | 同上 | `6-NEXT-SNAPSHOT`（`git-hash: 8e7235ea334c63d5686faf23a49d07badde658d0`） |
| `com.nablarch.configuration:nablarch-testing-default-configuration` | 同上 | `6u3` |
| `com.nablarch.configuration:nablarch-main-default-configuration` | 同上 | `6u3` |

### 確認した事実

| ページの記述 | 実装での裏付け |
|---|---|
| 置き換え先は `nablarch.test.OneShotLoopHandler`（テスティングフレームワークが提供） | `nablarch-testing` `src/main/java/nablarch/test/OneShotLoopHandler.java:25`（`package nablarch.test;` は `:1`） |
| `RequestThreadLoopHandler` のままでは要求データを処理し終えてもバッチが終了せず、テストコードに制御が戻らない | 同 `:16-21`（クラスJavadoc「常駐バッチ（サービス型）処理のテスト時に、`RequestThreadLoopHandler` の代わりに本ハンドラを設定することで、テスト実行前にセットアップした要求データを処理後にバッチ処理を終了することができる」「入力データを全て処理し終わった後も引き続き要求データの検索処理が継続される。このため、バッチ処理が終了せずにテストが実施できなくなる」） |
| 置き換えると、準備した要求データを処理し終えた時点でバッチが終了する | 同 `:44-51`（`while (context.hasNextData())` で回し、`NoMoreRecord` で `break`） |
| 置き換え対象の完全修飾名は `nablarch.fw.handler.RequestThreadLoopHandler` | `nablarch-fw-standalone` `6-NEXT-SNAPSHOT` の jar に `nablarch/fw/handler/RequestThreadLoopHandler.class` が存在する（`nablarch-fw` には存在しない）。FW解説書 `handlers/standalone/request_thread_loop_handler.rst:35`・`:41-44`（モジュールは `nablarch-fw-standalone`）とも一致 |
| コンポーネント名 `requestThreadLoopHandler` が本番用設定の名前である | `nablarch-main-default-configuration` `6u3` の `nablarch/common/standalone/process-service.xml:10`（`<component name="requestThreadLoopHandler" class="nablarch.fw.handler.RequestThreadLoopHandler">`） |
| 同名のコンポーネントを後から定義すると上書きされ、クラスが異なる場合は上書き前のプロパティが引き継がれない | FW解説書 `libraries/repository.rst:167-169`・`:183-186`（`repository-override_bean`） |
| 既定値のマップ名は 共通=`defaultDirectives` / 固定長=`fixedLengthDirectives` / 可変長=`variableLengthDirectives` | `nablarch-testing` `DataFile.java:60`、`FixedLengthFile.java:17`、`VariableLengthFile.java:20`（いずれも `SystemRepository` から引くキー。`DataFile.java:68-81` の `prepareDefaultDirectives`） |
| 共通の既定値が先、ファイル種別ごとの既定値が後に適用される | `DataFile.java:91`（コンストラクタで `defaultDirectives`）→ `FixedLengthFile.java:25-26`／`VariableLengthFile.java:28-30`（`super(path)` の後に種別ごとの既定値）。適用は `setDirective` による `Map#put` のため後勝ち（`DataFile.java:294-305`） |
| 個々のテストデータに書いたディレクティブが既定値より優先される | `DataFileParser.java:116`（識別子行で `DataFile` を生成＝この時点で既定値が入る）→ `:227-229`（ディレクティブ行で `currentFile.setDirective`） |
| 指定できるディレクティブは種別ごとに決まっており、それ以外はエラー | `DataFile.java:296-299`（`valueOf` が `null` なら `IllegalArgumentException`）。有効なキーは実行で確認した（下記「実行して確認した内容」） |
| データ型 符号無数値＝型記号 `X9`、符号付数値＝型記号 `SX9` | `BasicDataTypeMapping.java:52-53` |
| 型記号の前に `TEST_` を付けた名前のデータ型が登録されていれば、元の型に代えて使用される | `DataFileFragment.java:70`（`TEST_SYMBOL_PREFIX = "TEST_"`）・`:238-245`（`getTypeForTest`。`convertorTable` に存在すれば `TEST_` 付きを返す） |
| `StringDataType` は値の変換を行わずテストデータの記述をそのまま入出力する | `StringDataType.java:12`（クラスJavadoc「テストケースに記載した入力ファイル、出力ファイルのデータを、そのまま文字列として使用する場合に使用する」） |
| 設定先のコンポーネント名は `fixedLengthConvertorSetting` | `nablarch-core-dataformat` `FixedLengthConvertorSetting.getInstance()` が `SystemRepository` から `"fixedLengthConvertorSetting"` を引く（`javap -c` の定数プール `#33 // String fixedLengthConvertorSetting`）。未登録なら `DEFAULT_SETTING` を返す |
| `convertorTable` を設定すると既定の対応表が**置き換わる** | `ConvertorFactorySupport.setConvertorTable` は新しい `CaseInsensitiveMap` を組み立てて `convertorTable` フィールドに代入する（`javap -c`。`putfield convertorTable` の直前に既存表のマージが無い）。既定表はコンストラクタで `getDefaultConvertorTable()` を代入しているだけ |

### 実行して確認した内容（javap では確かめられない挙動）

`nablarch-core-dataformat` `6-NEXT-SNAPSHOT` と `nablarch-core` `6-NEXT-SNAPSHOT` の jar を classpath に置き、
次の2点を実際に実行して確認した。

- 固定長の既定の対応表は**16件**である（`X` `N` `XN` `Z` `SZ` `P` `SP` `B` `X9` `SX9` `pad` `encoding`
  `_LITERAL_` `number` `signed_number` **`replacement`**）。`FixedLengthConvertorSetting.getInstance()
  .getConvertorFactory().getConvertorTable()` を出力して確認した
- 有効なディレクティブキーは固定長11件（`file-type` `text-encoding` `record-length` `record-separator`
  `positive-zone-sign-nibble` `negative-zone-sign-nibble` `positive-pack-sign-nibble`
  `negative-pack-sign-nibble` `required-decimal-point` `fixed-sign-position` `required-plus-sign`）、
  可変長9件である。`testdata_notation.rst:873-925` の記載と一致する

### デフォルト値の基準（`design.md` §8）に照らした確認

**本ページには「デフォルト値」の欄を持つ設定項目表を置いていない。** 本ページが扱う3つの設定は、いずれも
「値を変える設定項目」ではなく「登録するかどうか」の設定であるためである。そのうえで、`design.md` §8 の
基準（デフォルト設定 `nablarch-testing-default-configuration` を読み込んだ状態の実効値を書く）に照らし、
デフォルト設定の内容を確認した結果は次のとおりである。

`nablarch-testing-default-configuration` `6u3` の jar を展開（XML 18ファイル・`.config` 5ファイル・
`.class` 7ファイル）し、全体を `grep` した。

| 対象 | デフォルト設定での定義 |
|---|---|
| `requestThreadLoopHandler` の置き換え | `nablarch/common/standalone/process-service_test.xml:15-16` に**存在する**（`nablarch.test.OneShotLoopHandler`） |
| `fixedLengthConvertorSetting`（`TEST_X9`・`TEST_SX9` を含む） | `nablarch/core/fixed-length-convertor-setting_test.xml:16-42` に**存在する** |
| `defaultDirectives`・`fixedLengthDirectives`・`variableLengthDirectives` | **0件**（該当ファイルなし） |

**ただし、この2ファイルはデフォルト設定の中のどこからも `import` されていない**（jar 内の `import file` は
`fixed-length-convertor-setting_test.xml:10` / `override_test.xml:8-11`（4件） / `test-data.xml:7`・`test-data-dbless.xml:7` の計7件のみで、
`process-service_test.xml` を指すものは無い。`fixed-length-convertor-setting_test.xml` を指すのは
`override_test.xml:9` のみ）。`nablarch-example-batch` の
`src/test/resources/unit-test.xml:16-17` が読み込むのは `nablarch/test/test-data.xml` と
`nablarch/test/test-transaction.xml` の2つで、`override_test.xml` も `process-service_test.xml` も
読み込んでいない。したがって Nablarchバッチアプリケーションのテストでは、いずれの設定も**自動では有効に
ならず**、出典が述べる「自分で設定する」という手順がそのまま正しい。

**この2ファイルの存在をページに書くかどうかは判断が要る**（下記「ユーザー判断を仰ぐ事項」参照）。
本ページでは書いていない。

## ゲート4 — `design.md` §3 記載範囲の線引き

`current-0037-b` は「テストデータの記載例」と「コンポーネント設定の追加手順」が1つの `.. tip::` に同居して
いるため、本ページの線引きの山場である。次のとおり分けた。

| 出典の要素 | 判定 | 扱い |
|---|---|---|
| 「符号無数値・符号付数値のデータには、パディング文字・符号を含めた固定長ファイル上の値をそのまま記載する」 | テストデータの記述**方法** → 第3部 | 事実は地の文に残し（`batch.rst:82`）、`:ref:`\ `ファイルのデータを記述する <testdata_notation-file_data>` へ導線を張った |
| 表「表したい数値／テストデータ上の記載」（`12345`→`0000012345`、`-12.34`→`-000012.34`。フォーマット定義の条件つき） | テストデータの記述**例** → 第2部に表・コードブロックを置かない | **表は置かず、同じ情報を地の文1文に残した**（`batch.rst:82`）。`steering.md` 共通 Steps「内容を落とすのではなく、事実は地の文に残してコードブロックを置かない」に従った |
| 「テスト用のデータ型を設定する必要がある」＋ `fixedLengthConvertorSetting` のXML | コンポーネント設定ファイルの設定と記述例 → 第2部 | 本ページに置いた（`batch.rst:84-119`） |

導線先（`testdata_notation-file_data`）の本文は実際に読んだうえで張った（`#19` の申し送り2）。
同節の `testdata_notation.rst:957-962` が符号無数値＝`X9`・符号付数値＝`SX9` を、`:967` が
「`X9`・`SX9` 型のフィールドには…実際のバイト列表現をそのまま記述する」「`TEST_{型名称}` という名前の
データ型を定義すると、同名の基底型より優先して使用される」を述べており、本ページの記述と矛盾しない。

`current-0291`・`current-0292` はいずれもコンポーネント設定ファイルの設定項目と記述例であり、
第2部にそのまま置いた。テストソースコードの実装例は3行のいずれにも含まれていない。

## ゲート5 — Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

結果（2回実行。いずれも同じ）:

```
build succeeded, 1 warning.
```

ログ全体を `grep -i "warning\|error"` した結果、`WARNING`/`ERROR` を含む行は次の1件のみである。
既知の `#7` 検出分（`#last` で解消予定）であり、**新規警告0件**。

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

（他の `error` 一致行は `global_error_handler` などファイル名・画像名に `error` を含む進捗行であり、
警告ではない。）

前方参照によるスタブページの新規作成は**行っていない**（`undefined label` の新規発生が0件のため）。

ビルドの直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、再生成された副産物を戻した
（2回とも実行。実行後の `git status --porcelain` に当該ファイルが現れないことを確認済み。ゲート6）。

## ゲート6 — 差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**とする（`ja/` 等に絞らない。`git diff` は未追跡ファイルを
出さないため使わない）。

| 状態 | ファイル | 予定していた変更か |
|---|---|---|
| `M` | `ja/development_tools/testing_framework/setup/index.rst` | 予定どおり（`toctree` に `request_unit_test/batch` を1行追記） |
| `??` | `ja/development_tools/testing_framework/setup/request_unit_test/batch.rst` | 予定どおり（本ページ） |

予定外**0件**。`.rn/20260724-ntf-yaml-support/checks/task-20.md`（本ファイル）は**コミットしない**ため、
上表は本ファイルを書き出す前の時点の全件である。

Docker フルビルドの直後に `locales/ja/LC_MESSAGES/sphinx.mo` が `M` で現れた（通算5回目）。
その場で `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻し、上表のとおり0件にした。

## 判断の記録

### マッピングにない追記（全件）

| # | 追記 | `design.md` §8 の類型 | 根拠 |
|---|---|---|---|
| 1 | `fixedLengthConvertorSetting` のXML例に `<entry key="replacement" .../>` を加えた | **出典と実装が食い違う場合**（実装優先） | 出典のXMLは「デフォルトの設定」と称して15件を挙げるが、実装の既定の対応表は16件で `replacement`（`nablarch.core.dataformat.convertor.value.CharacterReplacer`）を含む（ゲート3の実行結果）。`convertorTable` は置き換えであるため（同）、出典をそのまま写すと `replacement` が使えなくなる |
| 2 | ディレクティブ設定例の固定長のマップ名を `variableLengthDirectives` から `fixedLengthDirectives` に改めた | **出典と実装が食い違う場合**（実装優先） | 出典（`current-0292`）は「ディレクティブ（固定長）」というコメントの下で `variableLengthDirectives` を使っており、可変長の例と同名になっている。実装が固定長用に読むキーは `fixedLengthDirectives`（`FixedLengthFile.java:17`）。`nablarch-testing` 自身の `src/test/resources/unit-test.xml:115` も `fixedLengthDirectives` である |
| 3 | 可変長の `quoting-delimiter` の値を空文字から `&quot;` に改めた | **出典と実装が食い違う場合**（実装優先） | 出典の `value=""` はクォート文字を空にする設定であり、既定と同じで何も変えない。クォート文字を指定する例として成立しない。実在する設定（`nablarch-testing` `src/test/resources/unit-test.xml:121`）の値に合わせた |
| 4 | 「共通の既定値が先に適用され、ファイルの種別ごとの既定値がその後に適用される。同じディレクティブを両方に設定した場合は、ファイルの種別ごとの設定が有効になる」 | いずれの類型にも当たらない（**出典の表の説明**として書いた） | 出典の表が「共通／固定長ファイル／可変長ファイル」の3つを並べている以上、両方に同じキーを書いたときの結果は表そのものの意味に属する。新しい主題を追加したものではない。裏付けは `DataFile.java:91` → `FixedLengthFile.java:25-26`／`VariableLengthFile.java:28-30` の適用順（ゲート3） |
| 5 | `:ref:` 3件（`nablarch_batch-resident_batch`・`request_thread_loop_handler`・`repository-override_bean`）と、第3部への `:ref:` 2件（`testdata_notation-file_data`） | 導線 | いずれも本文の主題を増やさず、既存ページの記述と矛盾しないことを本文を読んで確認した（ゲート4・下記「参照先の本文の確認」） |

### 出典の表を地の文にした判断（`current-0291`）

出典の「変更が必要なハンドラ」の表はデータ行が1件（`RequestThreadLoopHandler` → `OneShotLoopHandler`、
変更理由）しかなく、3列の内容はそのまま2文になる。表の形を保つと、読者は1行の表から3つのセルを読み取る
ことになり、地の文より情報量が増えない。内容（変更対象・変更後・理由）は `batch.rst:17`・`:19` に
すべて残している。

### 参照先の本文の確認（`#19` の申し送り2）

| 参照先 | 読んだ内容 | 本ページとの整合 |
|---|---|---|
| `request_thread_loop_handler`（`handlers/standalone/request_thread_loop_handler.rst`） | `:9`「プロセスの停止要求があるまで、後続のハンドラを繰り返し実行するハンドラ」 | 一致。本ページの「プロセスの停止要求があるまで後続のハンドラを繰り返し実行する」はこの記述と実装（`OneShotLoopHandler.java:19-21`）の双方に一致する |
| `nablarch_batch-resident_batch`（`batch/nablarch_batch/architecture.rst:19-23`） | 「常駐バッチ：プロセスを起動しておき、一定間隔でバッチ処理を実行する」 | 矛盾なし |
| `repository-override_bean`（`libraries/repository.rst:163-186`） | 同名で登録すると後に読み込んだものが優先される。クラスが異なる場合は上書き前の property の設定が破棄される | 一致。本ページの `tip`（`batch.rst:37`）はこの記述に基づく |
| `testdata_notation-file_data`（`implementation/testdata_notation.rst:811-969`） | `:957-962` の型記号表、`:967` の `X9`・`SX9` の記述規則と `TEST_` 付きデータ型の優先、`:873-925` のディレクティブキー一覧 | 一致。重複を避けるため、本ページは設定手順のみを書き、記述規則とキー一覧は参照に寄せた |

### 用語（`glossary.md`）

| 語 | 出典の表記 | ページの表記 | 根拠 |
|---|---|---|---|
| データブロックの用途を表す予約語 | 出典は `TEST_X9` 等を「テスト用のデータタイプ」と呼ぶ | **「データ型」**に改めた | `glossary.md:213` が `データタイプ` を「データブロックの用途を表す予約語（`SETUP_TABLE` 等）」と定め、フィールドの型は別概念であると明記している。承認済みの `testdata_notation.rst:967` も `TEST_{型名称}` を「データ型」と呼んでいる |
| `常駐バッチ` | 同じ | 同じ | `glossary.md:145` |
| `ディレクティブ` / `固定長ファイル` / `可変長ファイル` / `コンポーネント設定ファイル` / `テストデータ` / `テスティングフレームワーク` / `テストコード` | — | 正表記どおり | `glossary.md:223`・`:226`・`:227`・`:281`・`:207`・`:119`・`:199` |

`テストケース` は本ページに0件（`grep -c` で確認）。

### 「デフォルト設定」の語（`#18`・`#19` からの申し送り）

`design.md` §8 が定める語義（`nablarch-testing-default-configuration` を読み込んだ状態）と衝突しないよう、
本ページではディレクティブの既定値を**「既定値」**と表記し、「デフォルト値」「デフォルト設定」の語を
使っていない（`grep -c "デフォルト" batch.rst` = 0）。承認済みの `testdata_notation.rst:871` も同じ機能を
「既定値」と呼んでいる。

## Completion criteria に対する self-check

| # | Completion criterion | 判定 | Evidence |
|---|---|---|---|
| 1 | `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く） | **OK** | ゲート1。3行・129 lines、`DROP` 0件、反映漏れ0件 |
| 2 | 当該 `dest_page` のマッピング行が全件、反映先の対応表として `checks/task-20.md` にある | **OK** | ゲート1の表（3行すべて）＋出典の要素ごとの対応表 |
| 3 | 全件表を求める項目をゲートの実行順の先頭に置き、母集合をホワイトリストで切り出さない | **OK** | ゲート1が先頭。母集合は `mapping.csv` 全594行を `csv.DictReader` で読んだうえでの抽出 |
| 4 | 4観点のレビューがすべて実施・記録されている | **未実施（本タスクの担当外）** | 作業指示により4観点レビューはコーディネータ側で行う。本作業では実施していない |
| 5 | 未対応の指摘が残っていない、または残す判断とその理由が記録されている | **OK**（現時点） | レビュー未実施のため指摘0件。自己判断で保留した事項は下記「ユーザー判断を仰ぐ事項」に記載 |
| 6 | `make html` が当該ページについてエラーを出さない | **OK** | ゲート5。`build succeeded, 1 warning.`（既知の1件のみ・新規0件） |

## ユーザー判断を仰ぐ事項（`decide`）

### `decide` 1 — デフォルト設定が同じ設定を持つ2ファイルの存在を、ページに書くかどうか

`nablarch-testing-default-configuration` `6u3` には、本ページが手で書くよう案内している設定と
**同じ内容のファイルが2つ含まれている**（ゲート3の表）。

- `nablarch/common/standalone/process-service_test.xml:15-16` — `requestThreadLoopHandler` を
  `nablarch.test.OneShotLoopHandler` で上書きする定義
- `nablarch/core/fixed-length-convertor-setting_test.xml:16-42` — `TEST_X9`・`TEST_SX9` を含む
  `fixedLengthConvertorSetting`（`nablarch/override_test.xml:9` から `import` されている）

どちらもデフォルト設定の他のファイルからは自動で読み込まれず、`nablarch-example-batch` の
`unit-test.xml` も読み込んでいないため、**出典の手順（自分で書く）は現在も正しい。** 一方で、
`<import file="nablarch/common/standalone/process-service_test.xml"/>` を1行書けば同じ結果になる
読者にとっては、この事実を知らないまま長いXMLを書き写すことになる。

**本ページには書いていない。** `design.md` §8 の例外のどれにも当たらないためである（出典と実装が
食い違っているわけではなく、出典が欠いている「実装上必須の設定」でもない）。承認済みの
`common.rst:56-82` も、同種の上書き（採番設定）をデフォルト設定のファイルに触れずに書いている。

**推奨**: 書き足す。読者が同じ結果をより少ない記述で得られる事実であり、第2部（アーキテクト向けの設定）の
読者にとっては判断材料になる。書き足す場合は、各節に `tip` を1つずつ加える形（本文の手順は変えない）に
なる。書き足さない場合は、現状のままでよい。

### `decide` 2 — `testdata_notation.rst:967` の `TEST_{型名称}` という表記

承認済みの第3部ページ `testdata_notation.rst:967` は「`TEST_{型名称}` という名前のデータ型を定義すると」と
書いているが、実装が `TEST_` を前置するのは**型記号**（`X9`・`SX9`）であって型名称（`符号無数値`・
`符号付数値`）ではない（`DataFileFragment.java:238-245`。`types` に入っているのは
`convertToFrameworkExpression` 済みの型記号である。同 `:202-209`）。同ページ `:933-935` が
「型名称／型記号」を別の列として定義しているため、`:967` の表記は自身の用語法とも食い違う。

本ページでは実装どおり「型記号の前に `TEST_` を付けた名前」と書いた。`testdata_notation.rst` は user review
承認済みのページであり、本タスクの Scope 外のため**是正していない。** 是正するかどうかはユーザー判断。

## 未確認として残した事項

- `nablarch-core-dataformat`・`nablarch-fw-standalone` はソースを取得できず（ローカル Maven リポジトリに
  sources jar が無い）、`javap` による逆アセンブルと実行による確認にとどめた。行番号を伴う `file:line` は
  記録していない。該当するのは `FixedLengthConvertorSetting.getInstance()` のリポジトリキーと
  `ConvertorFactorySupport.setConvertorTable` の置き換え挙動の2点で、いずれも `javap -c` の出力と
  実行結果の両方で確認している
- `replacement`（`CharacterReplacer`）が固定長の既定の対応表に入った時期は確認していない。確認したのは
  現行の `6-NEXT-SNAPSHOT` と、手元にあった `2.0.0` の2版でいずれも16件であることのみ

---

# 是正ラウンド1（4観点レビューの指摘への対応）

以下は是正ラウンド1で追記したゲートである。**上記の既存の記録は書き換えていない**（ページの行番号は
是正で移動したため、本節では是正後の行番号を記す。差分は `14 insertions(+) / 14 deletions(-)`、
`batch.rst` 1ファイルのみ）。

## ゲート7 — must の対応

| # | 指摘 | 対応 | 自分で確かめた根拠（`file:line`） |
|---|---|---|---|
| M-1 | 「常駐バッチのループ制御ハンドラ」がFW解説書の別コンポーネントの正式名称と衝突する | リード文（`:10`）と見出し（`:15`）を「リクエストスレッド内ループ制御ハンドラ」に統一。見出し下線を62に引き直した（表示幅62） | `handlers/batch/dbless_loop_handler.rst:3` のページ表題が「ループ制御ハンドラ」（`DbLessLoopHandler`）、`handlers/batch/loop_handler.rst:3` が「トランザクションループ制御ハンドラ」。`batch/nablarch_batch/architecture.rst:110-111` が常駐バッチのハンドラ構成に `loop_handler`・`dbless_loop_handler` の両方を挙げている。いずれも実ファイルを開いて確認した。是正後、本ページの「ループ制御ハンドラ」6件はすべて「リクエストスレッド内ループ制御ハンドラ」の一部である（`grep -n` で全件確認） |
| M-2 | `:82` の具体的な数値記述例が第2部の記載範囲を越える | 当該1文（フォーマット定義の条件と `0000012345`・`-000012.34`）を**削除**した。残したのは「符号無数値（`X9`）・符号付数値（`SX9`）のフィールドは、パディング文字や符号を含めた固定長ファイル上の表現をテストデータにそのまま記述する」という事実そのもの（`:82`）と、`:ref:`\ `ファイルのデータを記述する <testdata_notation-file_data>` への導線 | `design.md:203-206` の記載範囲表が「テストデータの記述例」を**記載しない**側に置いている（実ファイルで確認）。第3部への移設は行っていない |

### M-2 で同時に消えた既存の欠陥（確認済み）

- 出典 `05_UnitTestGuide/02_RequestUnitTest/batch.rst:267` は「データ型が**符号付数値**の場合」と限定して
  例を示しているのに、削除前の本ページはその例を符号無数値・符号付数値の両方を受けた文に続けており、
  射程が広かった。**削除により解消**（`git show origin/develop:` で出典 `:263-274` を再読して確認）
- 同じフォーマット定義（`小数点必要`）から `0000012345`（小数点なし）と `-000012.34`（小数点あり）の
  両方を導いていた不整合も、**削除により解消**

### 本ページでは直さない must 2件

| 指摘 | 判断 |
|---|---|
| `implementation/testdata_notation.rst:967` の `TEST_{型名称}` が実装と食い違う | **本ページは変更不要**（`:84` の「型記号の前に `TEST_` を付けた」が正しい）。第3部の是正はユーザー判断に回す。既存記録の `decide` 2 と同じ事項 |
| FW解説書 `libraries/data_io/data_format.rst:786-796` が `convertorTable` を非推奨としている | **手順の書き換え不要**。テスティングフレームワーク自身のデフォルト設定（`nablarch-testing-default-configuration:6u3` の `nablarch/core/fixed-length-convertor-setting_test.xml:17-19`）が同じ `convertorTable` で `TEST_X9`・`TEST_SX9` を登録している |

## ゲート8 — should / note の対応

| # | 指摘 | 対応 | 自分で確かめた根拠 |
|---|---|---|---|
| S-1 | L3見出しの下線長 | 則を **`max(49, 見出しの表示幅)`** として引き直した（`:16` = 62 / `:40` = 49 / `:81` = 52） | `ja/development_tools/testing_framework/` 配下を自分で走査した。`~`/`^` の下線は `about/index.rst` 4件・`testdata_notation.rst` 36件・`setup/` 既存5ページ（`class_unit_test` 2 / `common` 3 / `http_messaging` 2 / `rest` 2 / `web` 5）が**すべて49**。50以上は `testdata_examples.rst` のみで、同ページも見出し幅が49を超える箇所は幅ちょうど（52・56・59・60・63）である。L1（`=`）60・L2（`-`）50 は変更していない |
| S-2 | 適用範囲がバッチ固有でないことの明示 | リード文（`:10`）に1文、ディレクティブ節（`:41`）と データ型節（`:84`）にそれぞれ1文を加えた。**「リクエスト単体テスト全般」とは書かず「ウェブアプリケーションのリクエスト単体テスト」と特定した** | `nablarch-testing`（`e21bf67`）で `FileSupport`（`src/main/java/nablarch/test/core/file/FileSupport.java:22-23`。`@Published`）の利用元を全走査した結果、`core/batch/BatchRequestTestSupport.java:10`・`:59`・`:66` と `core/http/AbstractHttpRequestTestTemplate.java:20`・`:95`・`:101`・`:111` の2クラスのみ。RESTfulウェブサービスの `SimpleRestTestSupport` は利用元に含まれないため、範囲を広げて書かなかった |
| S-3 | 共通の既定値マップの制約 | `:78` に「`defaultDirectives` は固定長ファイル・可変長ファイルの両方に適用されるため、片方の種別にしかないキーを設定すると、もう一方の種別のテストデータを読み込む時点でエラーになる。共通の既定値には、両方の種別で有効なキーだけを設定する」を追記した | `DataFile.java:91`（コンストラクタが `defaultDirectives` を全種別に適用）→ `DataFile.java:294-299`（`valueOf` が `null` を返すと `IllegalArgumentException("invalid directive found.")`）。`null` を返すことは**実行して確認**した（`FixedLengthDirective.valueOf("field-separator")` → `null`、`VariableLengthDirective.valueOf("record-length")` → `null`、`FixedLengthDirective.valueOf("text-encoding")` → 非 `null`。`nablarch-core-dataformat` `6-NEXT-SNAPSHOT`） |
| S-4 | 「個々のテストデータに」の粒度 | `:41`・`:76` を「個々の**ファイルデータブロック**に」に改めた | 承認済み `implementation/testdata_notation.rst:871` が「**Excel 形式**ではファイルデータブロックの先頭（レコード定義より前）に…記載し」とこの粒度を使っている（実ファイルで確認）。`glossary.md:207` の `テストデータ` は準備データ・期待値・テストショット一覧の総称であり粒度が粗い |
| S-5 | キー名を指す文脈の語 | `:78` を「指定できる**ディレクティブキー**は…それ以外の**キー名**を指定すると」に改めた | `testdata_notation.rst:873`「固定長ファイルで有効なディレクティブキーは…」と同 `:879` の表の列見出し「ディレクティブキー」 |
| S-6 | `:17` の「ため」2回と `:19` の情報量 | 2段落を書き直した。`:17` は「…繰り返し実行する。準備した要求データを処理し終えた後も要求データの検索が続くため、バッチが終了しない。」、`:19` は「`OneShotLoopHandler` は、後続のハンドラが処理するデータが無くなった時点で繰り返しを終える。これに置き換えると、準備した要求データの処理を終えた時点でテストコードに制御が戻る。」 | 是正後 `grep -rnE "ため、[^。]*ためである。" ja/development_tools/testing_framework/` は**0件**。`:17` の書き換え後の内容は `OneShotLoopHandler.java:19-21`（「入力データを全て処理し終わった後も引き続き要求データの検索処理が継続される。このため、バッチ処理が終了せずにテストが実施できなくなる」）、`:19` の終了条件は同 `:44-51`（`while (context.hasNextData())` と `NoMoreRecord` での `break`） |
| S-7 | リード文の条件の置き方 | 1文目を「テスト対象が常駐バッチの場合に」と条件付きにした | 同型の書き方は `setup/request_unit_test/http_messaging.rst:10`（「HTTPメッセージ送信を伴うテストで使用する…」「HTTPメッセージ受信のテストで、…変更している場合は」） |
| S-8 | `:56`「設定例を示す。」 | 「記述例を示す。」に改めた | 是正前の `grep -rn "設定例を示す\|記述例を示す" ja/development_tools/testing_framework/` は「記述例を示す」8件（`testdata_examples.rst` 4 / `web.rst` 1 / `class_unit_test.rst` 3）に対し「設定例を示す」は本行のみ。是正後は「設定例を示す」0件 |
| note-1 | 「テスト用データ型」と「テスト用のデータ型」の揺れ | 見出し（`:80`）を本文と同じ「テスト用のデータ型」に揃え、`テスト用データ型` を0件にした | `grep -c "テスト用データ型"` = 0 |
| note-2 | 「冗長である」に用例が無い | 「個々のファイルデータブロックに同じディレクティブを繰り返し記述することになる」に置き換えた | `grep -rn "冗長" ja/application_framework/ ja/development_tools/testing_framework/` の用例7件はすべて「冗長化構成」「冗長化されている」の意で、「くどい」の意の用例は0件。是正後、本ページの「冗長」は0件 |

## ゲート9 — S-3 の追記の位置づけ（`design.md` §8）

S-3 の追記は `design.md` §8「**出典が欠いている、実装上必須の設定の追記**」に当たる。

- 出典（`current-0292`）は `defaultDirectives`・`fixedLengthDirectives`・`variableLengthDirectives` の
  対応表を示すだけで、共通マップに書けるキーの制約に触れていない
- この制約を知らずに共通マップへ片方の種別専用のキー（例: 可変長専用の `field-separator`）を書くと、
  もう一方の種別のテストデータを読む時点で `IllegalArgumentException` が発生し、**ページに書かれた手順
  （既定値をまとめて設定する）がそのままでは動かない**
- 根拠は実装で確かめた結果である（ゲート8 の S-3 行。`DataFile.java:91`・`:294-299` と、`valueOf` が
  `null` を返すことの実行確認）

## ゲート10 — 是正後の Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

結果: `build succeeded, 1 warning.`。ログ全体を `grep -n "WARNING\|ERROR"` した結果、該当は
既知の1件（`db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test`）
のみで、**新規警告0件**。

ビルドの直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、再生成された副産物を戻した
（通算6回目）。

## ゲート11 — 是正ラウンド1の差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の全件。

| 状態 | ファイル | 予定していた変更か |
|---|---|---|
| `M` | `ja/development_tools/testing_framework/setup/request_unit_test/batch.rst` | 予定どおり（是正対象） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-20.md` | 予定どおり（self-check。**コミットしない**） |

予定外**0件**。`setup/index.rst` は前回のコミットで確定しており、本ラウンドでは変更していない。

---

# 是正ラウンド2（適用範囲の文の畳み込み）

**上記の既存の記録は書き換えていない。** 本節は是正ラウンド2で追記したゲートである。
差分は `batch.rst` 1ファイルのみ（`4 insertions(+) / 4 deletions(-)`）。見出しは変更していないため、
L3の下線（`:16`=62 / `:40`=49 / `:81`=52）はそのままである。

## ゲート12 — 適用範囲の記述の是正

| # | 指摘 | 対応 | 自分で確かめた根拠 |
|---|---|---|---|
| 1 | 適用範囲が実装より狭い（「ウェブアプリケーション」限定は誤り。**電文のテストデータにも効く**） | リード文の1文を「後の2つはNablarchバッチアプリケーションに固有の設定ではなく、ファイルデータや電文のテストデータを扱うテストで使用する。」に改めた。**処理方式の列挙をやめた**（取りこぼしと、未作成ページへの前方参照を避けるため） | `nablarch-testing`（`e21bf67`。引用3ファイルは `fdf55d4` と差分0を `git diff --name-only` で確認）の経路を自分で開いて追った。`core/reader/MessageParser.java:54-58`（`createFixedLengthFileParser` が `FixedLengthFileParser` の無名サブクラスを返す）→ `core/reader/FixedLengthFileParser.java:30-32`（`createNewFile` が `new FixedLengthFile(filePath)`）→ `core/file/FixedLengthFile.java:24-27`（`super(path)` で `defaultDirectives`、続けて `prepareDefaultDirectives("fixedLengthDirectives")`）。`MessageParser` は `core/reader/BasicTestDataParser.java:83` が `DataType.MESSAGE` で生成しており、電文のテストデータの経路である。テスト用のデータ型も同じ経路で効く（`FixedLengthFile` の断片は `FixedLengthFileFragment` で、`getTypeForTest` は `FixedLengthFileFragment.java:94` から呼ばれる） |
| 2 | 適用範囲の文が3箇所に散っている | `:41`「ウェブアプリケーションのリクエスト単体テストでファイルデータを扱う場合も同じである。」と `:84`「この設定も、ウェブアプリケーションのリクエスト単体テストでファイルデータを扱う場合に同じように効く。」の**2文を削除**し、リード文の1文だけに畳んだ | 是正後 `grep -c "ウェブアプリケーション"` = 0 |
| 3 | 「効く」に用例がない | 上記2文の削除で本ページから消えた。新しい1文の述語は「使用する」にした | 是正前 `grep -rn "効く" ja --include=*.rst \| grep -v _build` の該当は `:84` の1件のみ。是正後は**0件**。「使用する」「も使用する」は既存解説書に用例がある（`libraries/log.rst:117`・`:123`、`setting_guide/CustomizingConfigurations/CustomizeSystemTableName.rst:42` ほか）。接続は「に限らず」ではなく既存用例のある形にした（`grep -rn "に限らず" ja --include=*.rst \| grep -v _build` は**0件**、`だけでなく` は5件以上。最終的にはどちらも使わず「〜に固有の設定ではなく」とした） |
| 4 | `:41` の説明の分断 | 割り込んでいた文を削除し、「既定値をmap形式で登録すると、この記述を省略できる。」→「mapの `name` 属性には…」が直接つながるようにした | 削除後に段落を通しで読み直して確認（下記ゲート13） |
| 5 | `:78` が4文になった | 2文目と3文目を1文にまとめた。「``defaultDirectives``\ は固定長ファイル・可変長ファイルの両方に適用されるため、共通の既定値には両方の種別で有効なキーだけを設定する（片方の種別にしかないキーを設定すると、もう一方の種別のテストデータを読み込む時点でエラーになる）。」 | 理由を括弧で添える形は承認済み `implementation/testdata_notation.rst:873`（「…11個に限定される（無効なキーを指定するとエラーになる）。」）と同じ |

## ゲート13 — 是正後の通し読みで自分が見つけた不整合（2件・その場で是正）

| # | 通し読みで見つけた不整合 | 是正 |
|---|---|---|
| 1 | リード文2文目の条件「ファイルを入出力するテストでは」と、3文目の「ファイルデータや**電文**のテストデータを扱うテスト」が噛み合わない（電文はファイルの入出力ではない） | 2文目から条件節を外し「ディレクティブの既定値と、固定長ファイルの数値フィールドで使用するテスト用のデータ型も、コンポーネント設定ファイルに設定できる。」とした。適用範囲は3文目が1度だけ述べる形に統一した |
| 2 | `:78` を1文にまとめた結果、末尾の「一覧は…を参照。」の指す先が2文前になり、指示語が浮いた | 「**ディレクティブキーの**一覧は…を参照。」と明示した |

通し読みの結果、上記2件以外に前後の重複・宙に浮いた指示語・つながらない段落は見つからなかった。
段落内の改行が0件であること（日本語の段落がすべて1行であること）も機械的に確認した。

## ゲート14 — 是正ラウンド2の Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

結果: `build succeeded, 1 warning.`。`grep -n "WARNING\|ERROR"` の該当は既知の1件
（`db_double_submit.rst:108: undefined label: how_to_set_token_in_request_unit_test`）のみで、**新規警告0件**。
直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して副産物を戻した（通算7回目）。

## ゲート15 — 是正ラウンド2の差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の全件。

| 状態 | ファイル | 予定していた変更か |
|---|---|---|
| `M` | `ja/development_tools/testing_framework/setup/request_unit_test/batch.rst` | 予定どおり（是正対象。コミットする） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-20.md` | 予定どおり（self-check。**コミットしない**） |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_batch.md` | **本作業の成果物ではない。** コーディネータが作成したレビュー記録であり、`reviews/` は触ってはならない対象のため作成も変更もしていない。**コミットしない**（ステージは明示パスのみのため混入しない） |

予定外**0件**。ビルド副産物（`locales/ja/LC_MESSAGES/sphinx.mo`）は上表に現れていない。
