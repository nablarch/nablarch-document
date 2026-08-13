# レビュー記録 — リクエスト単体テストの設定（Nablarchバッチアプリケーション）

対象ページ: `ja/development_tools/testing_framework/setup/request_unit_test/batch.rst`
ページ先頭ラベル: `request_unit_test_setting_batch`（`style.md` S-08 の表 `:352` から引用。新規考案なし）
タスク: `#20`

## 1. 出典（`mapping.csv` の全件）

`dest_page=リクエスト単体テストの設定（Nablarchバッチアプリケーション）` は3行。`csv.DictReader` で全594行を読んで抽出した（`wc -l` は使っていない）。

| `mapping_id` | `src_file` | 範囲 | `lines` | `disposition` | 反映先セクション |
|---|---|---|---|---|---|
| `current-0037-b` | `.../05_UnitTestGuide/02_RequestUnitTest/batch.rst` | `263`〜`316` | 54 | SPLIT | 符号無数値・符号付数値のテスト用のデータ型を登録する |
| `current-0291` | `.../06_TestFWGuide/RequestUnitTest_batch.rst` | `186`〜`222` | 37 | MOVE | 常駐バッチのリクエストスレッド内ループ制御ハンドラを置き換える |
| `current-0292` | `.../06_TestFWGuide/RequestUnitTest_batch.rst` | `225`〜`262` | 38 | MOVE | ディレクティブの既定値を設定する |

出典の実物は、現行解説書が本ブランチで削除済みのため `git show origin/develop:<src_file>` で読んだ。`note` 欄は根拠に使っていない。

SPLIT の相手側（`current-0037-a` の `170`〜`262`、`current-0037-c` の `317`〜`446`）は範囲が重ならず、本ページに来るべき内容の取りこぼしは0件（観点Aが独立に確認）。

## 2. 実装で確認した事実

参照コミット・版。

| リポジトリ / 成果物 | 取得元 | 参照コミット・版 |
|---|---|---|
| `nablarch/nablarch-testing` | ローカルクローン | `fdf55d4` |
| `com.nablarch.framework:nablarch-core-dataformat` | ローカル Maven リポジトリ | `2.0.3` sources / `6-NEXT-SNAPSHOT` jar |
| `com.nablarch.framework:nablarch-fw-standalone` | ローカル Maven リポジトリ | `6-NEXT-SNAPSHOT` jar |
| `com.nablarch.configuration:nablarch-testing-default-configuration` | ローカル Maven リポジトリ | `6u3` |
| `com.nablarch.configuration:nablarch-main-default-configuration` | ローカル Maven リポジトリ | `6u3` |

| ページの記述 | 実装での裏付け（`file:line`） |
|---|---|
| 置き換え対象は `RequestThreadLoopHandler`、置き換え後は `OneShotLoopHandler` | `nablarch-testing` `src/main/java/nablarch/test/OneShotLoopHandler.java:16-21`・`:25`・`:44-51`（`while (context.hasNextData())` と `NoMoreRecord` による打ち切り）。`RequestThreadLoopHandler` は `nablarch-fw-standalone` に存在（`nablarch-fw` にはない） |
| 本番用のコンポーネント名は `requestThreadLoopHandler` | `nablarch-main-default-configuration` `6u3` の `nablarch/common/standalone/process-service.xml:10` |
| 上書き前後でクラスが異なるとプロパティ値は引き継がれない | FW解説書 `libraries/repository.rst:183-186` |
| 既定値マップの名前は `defaultDirectives` / `fixedLengthDirectives` / `variableLengthDirectives` | `nablarch-testing` `src/main/java/nablarch/test/core/file/DataFile.java:60`、`FixedLengthFile.java:17`、`VariableLengthFile.java:20` |
| 共通が先、種別ごとが後に適用され、両方にあれば種別ごとが有効 | `DataFile.java:91`（コンストラクタで共通）→ `FixedLengthFile.java:25-26`（種別ごと。後勝ち） |
| テストデータに書いたディレクティブが既定値より優先される | `DataFileParser.java:116`・`:227-229` |
| 共通マップに片方の種別専用のキーを書くと、もう一方の解析時にエラーになる | `DataFile.java:91`（共通は全種別に適用）＋ `:294-300`（`valueOf` が `null` なら `IllegalArgumentException`）。`FixedLengthDirective.valueOf("field-separator")` が `null` を返すことは実行して確認 |
| テスト用データ型は**型記号**の前に `TEST_` を付けた名前 | `DataFileFragment.java:70`（`TEST_SYMBOL_PREFIX = "TEST_"`）・`:238-240`（`TEST_SYMBOL_PREFIX + baseType` で `convertorTable` を引く）。`baseType` は `setTypes` → `convertToFrameworkExpression` を通った後の値で、変換表は `BasicDataTypeMapping.java` の `DEFAULT_TABLE`（`符号無数値`→`X9`、`符号付数値`→`SX9`） |
| 符号無数値=`X9` / 符号付数値=`SX9` | `BasicDataTypeMapping.java` `DEFAULT_TABLE` |
| `convertorTable` を設定すると対応表は置き換わる（マージしない） | `ConvertorFactorySupport.java:148-162`（新しい `CaseInsensitiveMap` を作って差し替える） |
| 既定の対応表は16件（`replacement` を含む） | `FixedLengthConvertorFactory.java:61`（`nablarch-core-dataformat-2.0.3-sources.jar`）。`6-NEXT-SNAPSHOT` の `FixedLengthConvertorFactory$1` を `javap -c` でも確認し、`X,N,XN,Z,SZ,P,SP,X9,SX9,B,pad,encoding,_LITERAL_,number,signed_number,replacement` の16件で一致 |
| 既定値・テスト用データ型はNablarchバッチ固有ではない | ファイルデータ経路は `FileSupport.java` を `BatchRequestTestSupport.java:66` と `AbstractHttpRequestTestTemplate.java:101`・`:111` の双方が使う。電文経路は `MessageParser.java:57-58` → `FixedLengthFileParser.java:30-32`（`createNewFile` が `new FixedLengthFile(...)`）→ `FixedLengthFile.java:24-26`（`prepareDefaultDirectives`） |

### 出典を実装で上書きした3点（`design.md` §8「出典と実装が食い違う場合」）

| # | 出典 | ページ | 根拠 |
|---|---|---|---|
| 1 | 固定長の例のマップ名が `variableLengthDirectives`（`RequestUnitTest_batch.rst:254`。出典自身の表 `:239` とも矛盾） | `fixedLengthDirectives` | `FixedLengthFile.java:17` |
| 2 | 既定の対応表15件（`replacement` なし） | 16件（`replacement` を追加） | `FixedLengthConvertorFactory.java:61`。`javap -c` でも16件を確認 |
| 3 | 可変長の例が `quoting-delimiter` に空文字を指定 | `&quot;` | `VariableLengthDataRecordFormatter.java:289-297` が長さ1以外を `SyntaxErrorException` にするため、出典の値では動かない |

### デフォルト値の基準（`design.md` §8）

本ページに「デフォルト値」欄を持つ設定項目表は無い。`nablarch-testing-default-configuration` `6u3` の jar を展開して全走査した結果、本ページが扱う設定に関係するのは次の2ファイルで、いずれも**どこからも自動的には読み込まれない**。したがって出典の「自分で設定する」手順は現在も正しい。

- `nablarch/common/standalone/process-service_test.xml:15-16` — `requestThreadLoopHandler` を `OneShotLoopHandler` に置き換える設定。**jar 内のどのファイルからも `import` されていない**
- `nablarch/core/fixed-length-convertor-setting_test.xml:16-42` — `convertorTable` に `TEST_X9`・`TEST_SX9` を含む対応表。`import` しているのは `nablarch/override_test.xml` のみで、その `override_test.xml` 自体も jar 内のどこからも `import` されていない

## 3. 4観点レビュー

### ラウンド1（4観点・各観点を別のサブエージェントで実施）

| 観点 | 判定 | `must` | `should` | `note` |
|---|---|---|---|---|
| A 網羅性 | PASS | 0 | 2 | 1 |
| B トンマナ | FAIL | 2 | 6 | 5 |
| C 用語 | FAIL | 2 | 3 | 4 |
| D 整合性 | FAIL | 1 | 2 | 8 |

`must` は5件、重複除去後4件。うち**本ページで是正したのは2件**で、残り2件は是正不要または `decide` として上申した。

| # | 観点 | 指摘 | 対応 |
|---|---|---|---|
| 1 | C | 「常駐バッチの**ループ制御ハンドラ**」がFW解説書の別コンポーネントの正式名称と衝突する | リード文と見出しを「リクエストスレッド内ループ制御ハンドラ」に統一した。根拠は `handlers/batch/dbless_loop_handler.rst:3` の表題が「ループ制御ハンドラ」（`DbLessLoopHandler`）、`handlers/batch/loop_handler.rst:3` が「トランザクションループ制御ハンドラ」で、常駐バッチの最小ハンドラ構成（`batch/nablarch_batch/architecture.rst:110-111`）が両方を含むこと |
| 2 | D | 具体的な数値記述例（`12345`→`0000012345` 等）が第2部の記載範囲を越えている | 当該1文を削除した。`design.md:203-206` の記載範囲表が「テストデータの記述例」を第2部の記載しない側に置くため。事実（`X9`・`SX9` はパディング文字・符号込みの表現をそのまま記述する）と `:ref:` は残した。**第3部への移設は行わず `decide` 2 として上申** |
| 3 | B/C | `TEST_` の命名規則が承認済み `testdata_notation.rst:967` の「`TEST_{型名称}`」と矛盾する | **本ページは是正しない。** 実装照合の結果、本ページ（型記号の前に `TEST_`）が正しい。`decide` 1 として上申 |
| 4 | B | FW解説書 `libraries/data_io/data_format.rst:786-796` が `convertorTable` を非推奨としている | **手順は書き換えない。** テスティングフレームワーク自身のデフォルト設定 `nablarch-testing-default-configuration:6u3` の `nablarch/core/fixed-length-convertor-setting_test.xml:17-19` が同じ `convertorTable` で `TEST_X9`・`TEST_SX9` を登録しており、テスト用設定での使用は実装が追認している。`decide` 3 として上申 |
| 5 | B | L3見出しの下線長が `setup/` 配下の既存5ページ（49）と違う（50） | 実測則 `max(49, 表示幅)` に合わせた |
| 6 | D | 適用範囲がNablarchバッチ固有でないのに、ページ題と `toctree` の位置から限定に読める | 適用範囲を明示した（ラウンド2でさらに是正。下記） |
| 7 | D | 共通の既定値マップに片方の種別専用のキーを書くと、もう一方の解析時に必ず失敗する制約が書かれていない | 1文を追記した。`design.md` §8「出典が欠いている、実装上必須の設定の追記」に当たる |
| 8 | C | 「個々の**テストデータ**に」の粒度が `glossary.md` の `テストデータ` の定義より粗い | 承認済み `testdata_notation.rst:871` に合わせて「ファイルデータブロック」にした |
| 9 | C | キー名を指す文脈の「ディレクティブ」 | `testdata_notation.rst:873`・`:879` に合わせて「ディレクティブキー」「キー名」にした |
| 10 | B | 1文に因果の「ため」が2回入り、隣接段落が同語の裏返しになっている | 2段落を書き直した。是正後 `grep -rnE "ため、[^。]*ためである。"` は0件 |
| 11 | B | リード文の1文目に条件がなく、2文目にはある | 1文目に条件を持たせた |
| 12 | B | 「設定例を示す。」はNTFで本ページのみ | 「記述例を示す。」にした（既存用例8件側） |
| 13 | B/C | 「テスト用データ型／テスト用のデータ型」の揺れ、既存解説書に用例のない「冗長である」 | 統一・置換した |

**採らなかった指摘**

- B `must` 2（`convertorTable` の非推奨）— 上記4のとおり、テスティングフレームワーク自身のデフォルト設定が同じ手段を採っているため、手順は書き換えない
- C `should` 1（「既定値」を「デフォルト値」に寄せる）— **採らない。** 承認済みページ側で既に割れており（`testdata_notation.rst:871` は「既定値」、`:915` は「デフォルト」）、本ページ固有の問題ではない。`design.md` §8 の「デフォルト設定」の語義との衝突は0件であることをC自身が確認している
- D `should` 2 の後半（設定を `common.rst` へ移す）— **採らない。** マッピングが本ページに割り当てており、Rules「マッピングが唯一の基準」に反する。適用範囲の明示にとどめた

### ラウンド2（是正差分限定の検証）

判定 **PASS**（`must` 0 / `should` 2 / `note` 3）。是正が指示範囲に収まり、指示外のファイルへの変更・`locales/` の混入が無いことを確認した。

`should` 2件・`note` 3件は、適用範囲を述べる文が3箇所に散っていたことに起因するため、**リード文の1文に畳んで一括で解消した**（ラウンド3）。

| # | 指摘 | 対応 |
|---|---|---|
| 1 | 適用範囲を「ウェブアプリケーション」に限定したのは実装より狭い。電文のテストデータにも効く | 処理方式の列挙をやめ、ファイルデータ・電文のテストデータを扱うテスト全般とした。経路は §2 の実装表を参照 |
| 2 | `:84` の「同じように効く」は解説書全体で用例0件 | 当該文ごと削除した |
| 3 | 同趣旨の1文が3箇所に重複し、うち1つが `map` の説明を分断していた | リード文の1文に畳んだ |
| 4 | 共通マップの制約の追記が2文になり段落が4文になった | 1文にまとめた |

### ラウンド3（ラウンド2の指摘の一括是正）と、コーディネータの独立検証

ラウンド3は是正のみで、レビューのサブエージェントは回していない。**コーディネータが自分で最終版を通しで検証した**結果は次のとおり（すべてパス）。

| 検証 | 結果 |
|---|---|
| 見出し下線 | L1 幅60/`=`×60、L2 `-`×50、L3 は `:16` 幅62/62・`:40` 幅32/49・`:81` 幅52/52。L3 は実測則 `max(49, 表示幅)` に一致 |
| 段落内改行 | 0件（機械走査） |
| 是正語の残存 | 「ウェブアプリケーション」0件 / 「効く」0件 / 「冗長」0件 / 「設定例を示す」0件 / 「テスト用データ型」0件 / 「常駐バッチのループ制御ハンドラ」0件 / 「0000012345」0件 |
| 差分 | `fb3fd0f` は `batch.rst` の4行のみ。`git status --porcelain` の残余は未追跡の `checks/task-20.md` と本ファイルのみで、`locales/` の混入なし |

## 4. ユーザー判断を仰ぐ事項（`decide`）

（`#20` の user review で回答を仰ぐ。ここに残すのは判断を仰いだ時点の記録であり、回答は各 `decide` の直下に追記する。）

### `decide` 1 — 承認済み `testdata_notation.rst:967` の「`TEST_{型名称}`」が実装と食い違う

同行は「``TEST_{型名称}``\ という名前のデータ型を定義すると、同名の基底型より優先して使用される」と書く。しかし同ページ `:933-934` の表が自ら「型名称=``符号無数値``／型記号=``X9``」と定義しているため、この記述に従うと `TEST_符号無数値` という名前を書くことになり、動かない。

実装は**型記号**に `TEST_` を前置する（§2 の実装表）。`DataFileFragment.java:238-240` が `TEST_SYMBOL_PREFIX + baseType` で `convertorTable` を引き、その `baseType` は `setTypes` → `convertToFrameworkExpression` を通った後の値である。変換表は `BasicDataTypeMapping.java` の `DEFAULT_TABLE` で `符号無数値`→`X9`。本ページ（型記号の前に `TEST_`）が正しい。

**推奨**: `testdata_notation.rst:967` を「``TEST_{型記号}``」に是正する。1語の差し替えで済み、同ページの構造も表も変わらない。

**`#19` の申し送り4（`testdata_notation.rst:1244`）とは性質が違う。** `:1244` は言い回しが実装より狭いという問題で、読者が誤った設定を書く経路は無かった。本件は**読者が誤った名前を書き、テストが動かない**。承認済みページのため判断を仰ぐが、申し送りに留めると `#20` のページと第3部が正面から食い違ったまま公開される。

### `decide` 2 — `must` 対応で第2部から削った具体的な数値記述例の行き先

ラウンド1の `must` 対応で、`batch.rst` から次の1文を削った。`design.md:203-206` の記載範囲表が「テストデータの記述例」を第2部の**記載しない**側に置いているためである。

> フィールド長10桁・パディング文字\ ``0``\ ・小数点あり・符号位置固定・正の符号なしのフォーマット定義であれば、12345は\ ``0000012345``\ 、-12.34は\ ``-000012.34``\ と記述する。

出典は `05_UnitTestGuide/02_RequestUnitTest/batch.rst:267-274`（`current-0037-b` に含まれる）。**この内容は現在、新解説書のどこにも存在しない。** `implementation/testdata_examples.rst` の `X9`・`符号無数値`・`符号付数値` のヒットは**0件**、`testdata_notation.rst:967` は規則を述べるだけで具体例を持たない。Rules「マッピングにある内容を落とさない」に対する未充足である。

**推奨**: 第3部へ移す。`testdata_notation.rst:967` の直後が適切で、`decide` 1 と**同じ段落が対象のため1回の是正で済む**。落とす判断を採る場合は、`mapping.csv` の `current-0037-b` の扱い（当該部分を `DROP` 相当として記録する）を別途決める必要がある。

### `decide` 3 — デフォルト設定 `6u3` の同梱ファイルに触れるかどうか

`nablarch-testing-default-configuration` `6u3` には、本ページが手書きを案内している設定と同内容のファイルが同梱されている。ただし2つの性質は同じではない（§2 の「デフォルト値の基準」参照）。

| 同梱ファイル | 内容 | `import` の可否 |
|---|---|---|
| `nablarch/common/standalone/process-service_test.xml:15-16` | `requestThreadLoopHandler` → `OneShotLoopHandler` | jar 内のどこからも `import` されていない。**読者が1行 `import` すれば本ページの手順と同じ結果になる。副作用なし** |
| `nablarch/core/fixed-length-convertor-setting_test.xml:16-42` | `convertorTable` に `TEST_X9`・`TEST_SX9` を含む対応表 | `nablarch/override_test.xml` からしか `import` されておらず、その `override_test.xml` は日付固定・排他制御・ウェブUIスレッドコンテキストを**抱き合わせ**で読み込む。さらに同ファイルの対応表は `replacement` を欠くため、`import` すると現行の既定表（16件）から1件失われる |

**推奨**: どちらにも触れない（現状維持）。理由は3つ。(1) 出典どおりの手順で動くことは確認済みである。(2) マッピングにない追記であり、`design.md` §8 のどの類型にも当たらない。(3) 同梱ファイルはどこからも `import` されておらず、案内するとデフォルト設定の版差に追随する保守義務が生じる。

ただし、`fixed-length-convertor-setting_test.xml` が `replacement` を欠く事実は、読者が独自にこのファイルを見つけて `import` した場合に機能を1つ失うことを意味する。**`#last` までに `design.md` §8 の記録として残すかどうかは別途判断が要る。**

## 5. `#21` 以降への申し送り

1. **`defaultDirectives` / `fixedLengthDirectives` / `variableLengthDirectives` と `TEST_X9` / `TEST_SX9` は、Nablarchバッチアプリケーション固有ではない。** ファイルデータ経路（`FileSupport` を `BatchRequestTestSupport.java:66` と `AbstractHttpRequestTestTemplate.java:101`・`:111` が使う）に加え、電文経路（`MessageParser.java:57-58` → `FixedLengthFileParser.java:30-32` → `FixedLengthFile.java:24-26`）でも効く。**マッピングは本ページにのみ割り当てているため設定手順は本ページに置いたが、`setup/request_unit_test/web.rst`・`http_messaging.rst`・`mom.rst` を扱うタスクでファイル入出力に触れるときは、本ページへの導線を張るか検討すること**
2. **FW解説書の記述が「非推奨」としている手段を、テスティングフレームワーク側が正規の手段として使っていることがある。** `libraries/data_io/data_format.rst:786-796` は `convertorTable` を非推奨とするが、`nablarch-testing-default-configuration:6u3` の `fixed-length-convertor-setting_test.xml:17-19` は同じ手段を使う。FW解説書の推奨・非推奨をそのまま持ち込む前に、テスティングフレームワーク側の実配置を確認すること（`#19` の申し送り2 の続き）
3. **見出し下線の実測則は階層ごとに違う。** NTF全ページの実測で、L1（`=`）は `max(50, 表示幅)`、L2（`-`）は50固定、L3（`~`/`^`）は `max(49, 表示幅)` である。ただし `implementation/testdata_examples.rst` だけは L3 の下限が50で、コーパス自体が割れている。`setup/` 配下は5ページすべて49であり、新ページは49側に揃えた
4. **「デフォルト値」と「既定値」の呼称が、承認済みページ側で既に割れている。** `testdata_notation.rst:871` は「既定値」、同 `:915` は「デフォルト」、`web.rst:25`・`rest.rst:69` は設定項目表の列名が「デフォルト値」。`design.md` §8 が「デフォルト設定」「デフォルト値」を規範として使っている以上、どこかで統一の判断が要る。**本タスクでは本ページ固有の問題ではないため是正しなかった**
5. **`glossary.md:223` の `ディレクティブ` の意味列（「フォーマット定義を指定する**設定行**」）が、採用根拠より狭い。** 承認済み `testdata_notation.rst:871` は「キー名と値の2要素で記述するもの」と定義し、本ページの `<map>`/`<entry>` による登録は「行」ではない。`#19` の `decide` 1（`モックアップクラス`）と同型の欠陥である
6. **`glossary.md` に `型記号` / `型名称` の行がない。** `testdata_notation.rst:933-934` が定義して使っている語であり、行が無いことが `decide` 1 の食い違いの遠因になっている
7. **第3部から第2部への逆導線がない。** `testdata_notation.rst:871` は「既定値は、コンポーネント設定ファイルで\ map\ 形式によりまとめて指定することもできる」と触れるだけで、キー名を持つ本ページへリンクしていない
