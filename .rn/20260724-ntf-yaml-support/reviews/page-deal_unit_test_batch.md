# レビュー記録 — 取引単体テスト（Nablarchバッチアプリケーション）

**成果物**: `ja/development_tools/testing_framework/implementation/deal_unit_test/batch.rst`（487行。ラベル `deal_unit_test_batch`）
**キュー番号**: `#27-08`（`ntf-doc-weekend-queue.md` §3）
**個別指示**: 無し（`ntf-doc-27-small-3rd.md` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15` の4ページであり、本ページは含まれない。同 `:1` で確認）

## 1. 参照リポジトリ

| リポジトリ | コミット | 用途 |
|---|---|---|
| `nablarch-document` | 作業ツリー（`df7bff7` の続き） | 成果物・規約・マッピング |
| 削除済みの旧解説書 | `2e501ad` | 出典。`git show 2e501ad:<path>` で読む |
| `nablarch-testing` | `e21bf67`（作業指示 §4-2 の固定） | `TestShot` / `BatchRequestTestSupport` の挙動確認 |

**固定コミットでの読みが作業ツリーと同じであることを確認した。** `nablarch-testing` の作業ツリー HEAD は `fdf55d4b`（ブランチ `convert-testdata-excel-to-text`）だが、`git diff e21bf67 HEAD -- src/main/java/nablarch/test/core/standalone/TestShot.java src/main/java/nablarch/test/core/batch/BatchRequestTestSupport.java` は出力0行である。本記録の行番号はすべて `e21bf67` のものである。

## 2. 出典行の消化（全168行）

`mapping.csv` を `csv.DictReader` で読み、`dest_page == '取引単体テスト（Nablarchバッチアプリケーション）'` を抽出した結果は8行、`lines` 合計168行。出典はすべて `05_UnitTestGuide/03_DealUnitTest/batch.rst`（`2e501ad` 時点で183行）である。`DROP`・`REFERENCE` は無い。

| `mapping_id` | 出典行 | 行数 | disposition | `dest_section` | 反映先 |
|---|---|---|---|---|---|
| `current-0128-a` | `:4-7` | 4 | SPLIT | 機能概要 | `:10`（リード）・`:15` |
| `current-0128-b` | `:8-25` | 18 | SPLIT | 使用方法 | `:22-41`（テストクラスを作成する） |
| `current-0129` | `:28-32` | 5 | MOVE | 使用方法 | `:83`（原則） |
| `current-0130` | `:35-41` | 7 | MOVE | 使用方法 | `:85`（例外1）・`:90` |
| `current-0131` | `:44-48` | 5 | MOVE | 使用方法 | `:85`（例外2）・`:91` |
| `current-0132` | `:51-79` | 29 | MOVE | 使用方法 | `:43-53`（`execute()`）・`:89`・`:97-164`・`:339-377` |
| `current-0133` | `:82-146` | 65 | MOVE | 使用方法 | `:55-79`（3回の `execute`）・`:90`・`:166-255`・`:379-437` |
| `current-0134` | `:149-183` | 35 | MOVE | 使用方法 | `:91`・`:257-335`・`:439-487` |

**落とした行は0件。** 出典の非空行はすべて上表で消化している。出典が持つ4つのL2見出し（`テストケース分割方針`／`基本的な記述方法`／`1テストケースを複数シートに分割する場合`／`1シートに複数ケースを含める場合`）は見出しとしては残していないが、これは見出しの落としではなく再構成である（§5 D-1）。出典の Excel 表はすべて YAML 形式でも書き起こしており（`style.md` S-10 規約2）、出典に無い YAML 側の記述は Excel 表の機械的な写しである。

**`tips_groupId` への参照（出典 `:181-183`）は `:93` の `:ref:`グループIDによる使い分け <testdata_notation-group_id>`` に置き換えた。** 参照先の手順は書き写していない。

## 3. 実装で確認した事実

| 事実 | 実装 | 本文への反映 |
|---|---|---|
| `no` は文字列として扱われ、値の形式に制約が無い | `TestShot.java:295-296`（`getNo()` が `testData.get(NO)` をそのまま返す）・`:348`（`NO = "no"`） | 枝番 `1-1` の例をそのまま採用（§5 D-4） |
| Nablarchバッチの必須カラムは `no`・`title`・`expectedStatusCode`・`diConfig`・`requestPath`・`userId` の6つ | `TestShot.java:385-387`（`REQUIRED_COLUMNS`） | 出典の表に無い `diConfig`・`userId` を全表に足した（§5 D-3） |
| `setUpTable` が空なら準備をせず、値があれば `default` のデータブロックを投入したうえで、`default` 以外なら当該グループIDのブロックも投入する | `TestShot.java:149-162`（`setUpTable()`） | §5 D-6 に記録。本文には書いていない |
| `expectedTable` が空ならテーブルの検証をしない | `TestShot.java:193-213`（`assertTables()`。`return; // 指定がない場合はアサートしない。`） | §5 D-7 に記録。本文には書いていない |

**`REQUIRED_COLUMNS` の定数 `TITLE` が保持する文字列は `"description"` である**（`TestShot.java:351`）。`testdata_notation.rst:391-392` の `description`（旧名 `case` も可）と一致する。本ページの表は `description` で統一した。

## 4. 実測

| 項目 | 値 | 取得方法 |
|---|---|---|
| 行数 | 487行 | `wc -l` |
| 見出し | L1×1・L2×2・L3×3・L4×2 | 下線行の機械抽出 |
| 下線 | L1 50（表示幅48）・L2 50（8）・L3 49（22〜24）・L4 49（14〜15） | `unicodedata.east_asian_width` で表示幅を計算 |
| `:ref:` | 5件（`request_unit_test_batch`・`testdata_notation`・`testdata_notation-test_shots`・`testdata_examples`・`testdata_notation-group_id`） | 正規表現抽出 |
| `.. code-block::` | 9件（java 2・text 1・yaml 6）。ディレクティブ0字下げ・本文2字下げ | インデント計測 |
| `.. list-table::` | 7件。`:widths:` の合計はすべて100 | 数値の機械集計 |
| グリッドテーブル | 0件（S-07） | `grep '^+-'` |
| `note` / `warning` | 0件（S-06） | `grep` |
| `.. image::` | 0件 | `grep` |
| YAML の妥当性 | 6ブロックすべて `yaml.safe_load` が成功。`list_maps[0].rows` の各行のキー集合は同一 | Python で全ブロックを抽出して実行 |
| 禁止語（G6） | `不具合`・`バグ`・`将来`・`修正され` すべて0件 | `grep` |
| ビルド（G5） | `build succeeded, 1 warning.` | Docker で `sphinx-build -E` を全ビルド |

**ビルドの警告1件は既知の `db_double_submit.rst:108`（undefined label `how_to_set_token_in_request_unit_test`）である。** 本ページ由来の新規警告は0件。この警告は `#27-20` が解消する。

## 5. 出典から変えた点

### D-1. 出典の4つのL2見出しを、`design.md` の第3部アウトラインに組み替えた

出典は「テストケース分割方針（＋2つのL3）／基本的な記述方法／1テストケースを複数シートに分割する場合／1シートに複数ケースを含める場合」という、記述パターンごとの見出し構成を持つ。`design.md:281-296` の第3部アウトラインは `機能概要` と `使用方法`（配下に手順のL3）を定めており、そのままでは載らない。

**分割方針（出典 `:28-48`、方針3件）を `テストデータを作成する` の導入に置き、3つの記述パターンをその配下に収めた。** 方針とその実演が出典では離れており、パターンごとに「なぜこう書くのか」を追うのに往復が要る。導入で3パターンを名指ししてから実例を並べる形にした（`style.md` S-11）。

### D-2. `使用方法` 配下のL3を3つにした（`テストを実行する`・`テスト結果を確認する` を立てていない）

`design.md:281-296` は `使用方法` 配下に5つのL3を挙げるが、**出典にはテストの実行手順も結果確認の手順も無い。** 出典 `:5-6` は「リクエスト単体テストと同じ」と述べるだけである。立てれば出典に無いことを書くことになるため、`:20` で `:ref:`リクエスト単体テスト（Nablarchバッチアプリケーション） <request_unit_test_batch>`` に送った。

**この扱いは `ntf-doc-27-small-3rd.md` §1-1 と同じだが、同指示の対象に本ページは入っていない**（同 `:1` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15`）。適用の可否を §7 の `decide-1` に上げる。

### D-3. 出典の表に無い必須カラム `diConfig`・`userId` を全表に足した

出典の表（`:74-76`・`:100`・`:114`・`:126`・`:171-174`）は `diConfig` も `userId` も持たない。**`TestShot.java:385-387` の `REQUIRED_COLUMNS` は6カラムを必須とし、欠けるとテストが動かない。** `design.md` §8 の「出典が欠く実装上必須の設定は追記してよい」に当たる。値は出典 `:57` のパッケージ `ss21AC01`／取引ID `B21AC01` から `ss21AC01/B21AC01.xml`、`userId` は `testdata_examples.rst:500-573` に合わせて `test` とした。

### D-4. 出典のカラム名 `case`・`outFile` を `description`・`expectedFile` に直した

出典 `:118`・`:130`・`:141` は `case`、`:141` は `outFile` を使う。**`testdata_notation.rst:391-392` は `description`（旧名 `case` も可）、`:462-491` の Nablarchバッチのカラム一覧は `expectedFile` である。** 承認済みページと表記が割れると、読者が2つの名前を持ち帰る。`design.md` §8 の実装優先を適用した。

### D-5. 出典の `import nablarch.test.core.messaging.BatchRequestTestSupport` を `nablarch.test.core.batch.BatchRequestTestSupport` に直した

出典 `:92` はパッケージが `messaging` になっている。**`nablarch-testing@e21bf67` に `nablarch/test/core/messaging/BatchRequestTestSupport.java` は存在せず、`nablarch/test/core/batch/BatchRequestTestSupport.java` が実在する。** 承認済みの `setup/junit5_extension.rst:40` も `nablarch.test.core.batch.BatchRequestTestSupport` である。あわせて出典 `:17` の `package nablarch.sample.ss21AC01`（セミコロン無し）と、閉じ括弧の欠けたコード例を補った。

### D-6. 出典 `:74-76` の「前項で示したテストケース」を「同じ構成の取引（取引ID は `B21AA01`）」に改めた

出典 `:84` は「前項(基本的な記述方法)で例示したテストケースは、以下のように分割して記述可能である」と述べるが、**分割側のクラスは `B21AA01Test`（出典 `:94`）、パッケージは `ss21AA01`（同 `:90`）であり、基本例の `B21AC01Test`（同 `:19`）とは別の取引である。** D-3 で `diConfig` を明記した結果、この食い違いが表面に出た。同一だと述べると読者が混乱するため、「同じ構成の取引」に改めた。**出典のクラス名自体は変えていない。**

### D-7. 分割例で `expectedTable` の有無が例ごとに違う点を、出典どおりにした

出典の分割例では、ファイル入力シート（`:100`）に `expectedTable` が無く、ユーザ削除シート（`:114`）にはある。**`TestShot.java:193-213` は `expectedTable` が空ならテーブルを検証しないため、まとめて書いた例と分割した例では検証範囲が異なる。** 出典に忠実に写し、本文でこの差には触れていない。§7 の `decide-2` に上げる。

### D-8. コードブロックのインデントを2字にした

出典 `:11-25` などは4字下げである。`style.md` S-05 は2字下げと定めており、承認済みページもすべて2字下げである。**出典のインデントは持ち込んでいない。**

### D-9. 語彙の置き換え

`glossary.md:509` により `自動テストフレームワーク` → `テスティングフレームワーク`（無条件）、`:556` により `テストケース` → `テストショット`／`テストメソッド`／`テスト` を文脈で使い分けた。出典が「シート」と呼ぶ単位は、Excel/YAML の両方を指すため `読み込み単位`（Excel形式では1シート、YAML形式では1ファイル）と書いた（`:83` で定義）。

### D-10. 出典の `expectedStatusCode` の `100` を `0` に直した（`#28` §2-1）

出典の3例（`:74-76`・`:120`・`:132`・`:143`・`:171-174`。出典に `100` が現れるのはこの10行だけである）はいずれも `100` である。**実装・FW解説書と食い違うため、`design.md` §8「出典と実装が食い違う場合は実装を優先する」に従って `0` に変えた。** 本ページの `expectedStatusCode` は Excel 形式の表10セル・YAML 形式10箇所のすべてが `0` になっている。

根拠:

- FW解説書 `ja/application_framework/application_framework/handlers/standalone/status_code_convert_handler.rst:40-42` が `important` で「アプリケーションのエラー処理でステータスコードを指定する場合は、100～199を使用する」と定め、同 `:44-57` の変換表は `0～199` を「変換は行わない」としている。**`100` はエラー処理用の値であり、正常終了を表さない。** 本ページの3例はいずれも正常系である
- 承認済み `implementation/testdata_examples.rst:561`・`:568`（Nablarchバッチの記載例）は `"0"` である
- `nablarch-example-batch` の実データ `src/test/java/com/nablarch/example/app/batch/action/ImportZipCodeFileActionRequestTest/testNormalEnd.yaml:7`・`testAbNormalEnd.yaml:7` はいずれも `expectedStatusCode: "0"` である

### D-11. 出典 `:76` の `expectedTable: fileInputBatch` を空欄にした（`#28` §2-17）

出典 `:76`（基本例のテストショット3「ファイル出力」）は `expectedTable` に `fileInputBatch` を置くが、**このグループIDのデータブロックは出典のどこにも存在しない**（出典全体で `fileInputBatch` が現れるのは `:74`・`:76`・`:120`・`:171`・`:173` で、`:76` 以外はすべて `requestPath` 列の値である）。無いデータブロックを創作せず、当該セルを空欄にした。

### D-7 の追記（`#28` §2-16・§2-15）

D-7 が「本文でこの差には触れていない」とした点は `#28` §2-16 で解消し、`:97` の段落（`expectedTable`・`expectedFile` を空欄にしたテストショットでは検証を行わないこと、期待値のカラムの有無の違いが意図的であること）を足した。あわせて `#28` §2-15 で `:95` に `setUpTable`・`setUpFile` の投入がテストショットごとに行われることを足した。

根拠（`nablarch-testing@e21bf67`。`fdf55d4` との差分は `pom.xml` のみで Java ソースは無差分）:

- `src/main/java/nablarch/test/core/standalone/TestShot.java:150-162` — `setUpTable()` は値が空なら何もせず、値があれば準備データを投入する。呼び出しは `:81 setUp()` 経由でテストショットごとに毎回通る
- 同 `:198-213` — `assertTables()` は `expectedTable` が空なら `return` してアサートしない（**D-7 が書いた `:193-213` の `:193-197` は Javadoc であり、実体は `:198` から**）
- `src/main/java/nablarch/test/core/batch/BatchRequestTestSupport.java:73-82`（`setUpInputData`）・`:88-97`（`assertOutputData`）— `setUpFile`・`expectedFile` も同じく、空欄なら何もしない

## 6. 4観点レビュー

QA／設計／クラフト／検証の4観点をそれぞれ別のサブエージェントで実施した。指摘は QA 11件、設計 10件、クラフト 13件、検証は G10 が FAIL＋3件。**是正は1ラウンドで畳み、成果物の `.rst` に含めている。**

### 是正した指摘（重い順）

1. **`style.md` S-10 規約3 違反 — 形式別のL4対が無く、太字を複数ブロックの区切りに使っている**（設計高）→ L3 `テストデータを作成する` を、形式別L4対1組（`Excel形式の場合`／`YAML形式の場合`）に組み替えた。3つの記述パターンは各L4の中の太字ラベルとし（S-10 太字の例外1「既にL4見出しの下にあり、これ以上下の見出しレベルを追加できない場合」）、形式に依存しない説明はL3の導入の箇条書きに上げた（S-11）。**承認済みの `testdata_examples.rst:500-573` が同じ形をしている**
2. **必須カラム `diConfig`・`userId` の欠落**（検証 G10 FAIL・QA高）→ D-3
3. **import のパッケージ誤り**（QA高・クラフト高）→ D-5
4. **`case`・`outFile` が承認済みページの用語と割れている**（QA中・設計中）→ D-4
5. **「前項で示したテストケース」が `diConfig` の違いと矛盾する**（設計中）→ D-6
6. **`自動テストフレームワーク` が `glossary.md:509` の無条件置換に反する**（クラフト高）→ D-9
7. **L4下線が48字で、`testdata_notation.rst` の49字と揃っていない**（クラフト中）→ 49字に直した
8. **`:widths:` の合計が116・118・118 で100でない**（クラフト中）→ 全7表を100に直した
9. **YAML 例3が、Excel の空セルに対応するキーを省略していた**（検証中）→ `testdata_notation.rst:656` の `.. important::`（Excel の空セル＝空文字、YAML のキー無し＝`null`）に従い、10キーすべてを `""` 込みで書き下した
10. **末尾の tip がグループIDの説明を重複して持っている**（設計低・クラフト低）→ tip を削し、内容を `:93` の地の文に移した

### 採らなかった指摘

- **3つの記述パターンをそれぞれL3に昇格し、各L3に形式別L4対を持たせよ**（クラフト中）— `testdata_examples.rst:500-573` と完全に同形になるが、`design.md:281-296` のアウトラインに無いL3が3つ増え、目次に `Excel形式の場合` が3回並ぶ。`style.md` S-10 規約3 は「同じL3内でExcel/YAMLの記述方法の説明が複数の話題にわたる場合も、2組目の見出し対を作らず、その1組の下にまとめる」と明記しており、**規約が明示的に本ページの形を指している**
- **`setUpTable: default` がテストショットごとにDBを再投入する点を書け**（QA中）— 出典に無い。§7 の `decide-3` に上げた
- **`expectedStatusCode: 100` は `testdata_examples.rst` の `0` と違う。揃えよ**（QA中・検証中）— 出典 `:74-76` が `100` である。バッチの正常終了コードがどちらかを実装で確定できていない。§7 の `decide-4` に上げた
- **`expectedTable: fileInputBatch`（出典 `:76`）に対応するデータブロックがページ内に無い**（検証中）— 出典どおりである。§7 の `decide-5` に上げた
- **リクエスト単体テストとの違いを機能概要でもっと説明せよ**（QA低）— 出典 `:5-6` の範囲を超える
- **拡張例（テストデータの準備方法のバリエーション）を足せ**（設計低）— `design.md:281-296` が「拡張例は第3部に置かない」と定めている

## 7. 判断待ち（`decide`）

### decide-1. `使用方法` 配下のL3を出典に合わせて3つにしたこと

`ntf-doc-27-small-3rd.md` §1-1 は「`使用方法` 配下のL3見出しは、出典にある手順がそのまま見出しになる。出典に無いL3は立てない」と定めるが、**同 `:1` の対象は `#27-07`・`#27-10`・`#27-11`・`#27-15` の4ページであり、`#27-08` は入っていない。** 出典に無い手順を書かないという判断は他ページと同じにしたが、指示の射程外での適用である。`#27-07` の `decide-1`（`reviews/page-deal_unit_test_rest.md` §7）と同じ論点であり、まとめて判断されたい。

### decide-2. 分割例と非分割例で検証範囲が違うことを本文に書いていない

出典の分割例はファイル入力シートに `expectedTable` を持たない（出典 `:100`）。`TestShot.java:193-213` により、このシートではテーブルの検証が行われない。**まとめて書いた例（`expectedTable: default`）とは検証範囲が異なるが、出典に説明が無いため書いていない。** 「分割しても検証内容は変わらない」と読む読者が出うる。注記を足すかどうかは user 判断に回す。

### decide-3. `setUpTable: default` が全テストショットに付いていることの意味を書いていない

`TestShot.java:149-162` により、`setUpTable` に値があるテストショットは実行前に `default` のデータブロックを投入する。**出典の基本例（`:74-76`）は3件すべてに `default` を置いており、そのまま写すと「前のバッチが更新したDBの状態が次のバッチに引き継がれない」ことになる。** 取引単体テストの趣旨（取引全体を通しで検証する）と読み合わせると説明が要る箇所だが、出典に無い。

### decide-4. `expectedStatusCode: 100` が `testdata_examples.rst` の `0` と食い違う

出典 `:74-76` は `100`、承認済みの `testdata_examples.rst:500-573` は `"0"` である。**どちらがバッチの正常終了コードとして正しいかは実装で確定できていない（未確認）。** 出典に忠実に `100` としたが、承認済みページと並べて読まれると矛盾する。

### decide-5. `expectedTable: fileInputBatch` に対応するデータブロックがページ内に無い

出典 `:76` の3件目は `expectedTable` に `fileInputBatch` を指定する。**これは同名の `requestPath` と字面が同じグループIDであり、対応する期待値データブロックは出典にも本ページにも無い。** 出典どおりに写したが、読者が `requestPath` の値を書くカラムと誤読する余地がある。

### decide-6. `:20` の `:ref:` の飛び先が現時点で4行のスタブである

`implementation/request_unit_test/batch.rst` は `#27-00` で作ったラベル＋タイトルのみの4行である（`wc -l` で実測）。**本ページはテストの実行方法をこのページに全面委譲しているため、`#27-12` を書き終えるまで、実行方法を追った読者は空ページに着く。** `#27-07` の `decide-2` と同じ論点である。
