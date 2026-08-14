# page-component_unit_test

対象: `ja/development_tools/testing_framework/implementation/class_unit_test/component.rst`（第3部）
タスク: `#27-19`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-large-pages.md`

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-yaml` | `190cc9a` |
| `nablarch-document`（旧解説書） | `2e501ad` |

## 2. 出典の反映状況

`mapping.csv` で `dest_page` が「コンポーネント単体テスト」の行は26件・770行（`csv.DictReader` で全行走査、実測）。**23件を本文に反映し、3件を意図して落とした。**

### 反映した23件

| mapping_id | 出典 | 反映先 |
| --- | --- | --- |
| `current-0025` | `02_componentUnitTest.rst:6-8` | `:10` リード文 |
| `current-0027` | 同 `:25-39` | `:41-58` 確認する対象の4分類 |
| `current-0028` | 同 `:42-355` | `:63` 以降（テストデータの作成・テストクラスの作成・処理終了後のDB状況・メッセージID） |
| `current-0181` | `02_DbAccessTest.rst:8-15` | `:10`・`:15` |
| `current-0182` | 同 `:18-44` | `:17` 図・`:21-39` 主なクラスとリソースの表 |
| `current-0183` | 同 `:48-52` | `:63` 使用方法のリード文 |
| `current-0184-a` | 同 `:55-100` | `:151-178` 参照系のテストを作成する |
| `current-0185-a` | 同 `:168-220` | `:180-219` 更新系のテストを作成する |
| `current-0194` | 同 `:527-535` | `:365-368` `assertSqlResultSetEquals` の性質 |
| `current-0195` | 同 `:538-543` | `:189-191` コミットに関する `important` |
| `current-0196`（REFERENCE） | 同 `:546-548` | `:313`（本文を持たず `:ref:` のみ。§9 `decide-2`） |
| `current-0216` | `03_Tips.rst:50-75` | `:245-263` テストデータから引数と期待値を取得する |
| `current-0218` | 同 `:109-114` | `:267` |
| `current-0219` | 同 `:117-144` | `:269-287` |
| `current-0222` | 同 `:231-242` | `:297-303` |
| `current-0230` | 同 `:437-452` | `:223` |
| `current-0231` | 同 `:455-468` | `:225-233` |
| `current-0233` | 同 `:491-496` | `:315` |
| `current-0234` | 同 `:499-507` | `:317-320` |
| `current-0235` | 同 `:511-514` | `:121` |
| `current-0236` | 同 `:517-553` | `:123-141` `@BeforeClass`・`@AfterClass` の `important` |
| `current-0237` | 同 `:557-570` | `:89-93`（配置の変更は §6 D-1） |
| `current-0238`・`current-0239` | 同 `:574-580`・`:583-618` | `:95-119` 委譲の説明とコード例 |

### 意図して落とした3件

- **`current-0026`（`02_componentUnitTest.rst:12-22`）** — サンプルアプリケーションの成果物4点への `:download:` リンク（`ユーザ登録_UserComponent_クラス単体テストケース.xlsx`・`UserComponentTest.java`・`UserComponentTest.xlsx`・`UserComponent.java`）。
  **訂正（`#27-21` 作業時に判明）**：当初ここに「リンク先の4ファイルは `2e501ad` で削除済み」と書いたが、これは誤りだった。`git ls-files ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/_download/` は10ファイルすべてを返す。`2e501ad` が削除したのは `.rst` だけで、`_download/` 配下の資産は追跡されたまま残っている。
  落とす判断そのものは維持する。理由は資産の不在ではなく、これらが本再構築で置き換える旧 `guide/` ツリー配下にあることである。第3部の新ページからそこへリンクを張ると、旧ツリーを撤去した時点で参照が壊れる。**資産の移設要否は `decide` としてユーザーへ上げる。**
- **`current-0220`（`03_Tips.rst:147-201`）** — 「Excelファイル記述例」。`LIST_MAP`・`SETUP_TABLE` の記述例そのものであり、`design.md` の方針により記述例は `implementation/testdata_examples.rst` に集約する。本ページは `:309` から `:ref:`テストデータの記載例 <testdata_examples>`\ ` へ送っている。Excel形式のみの例で、YAML形式の対を持たない点も落とす理由になる。
- **`current-0028` のうち画像4枚とサンプルアプリ固有の記述** — 下記 §3 のとおり。

## 3. 画像

`ntf-doc-weekend-queue.md:172` は本ページの画像を7枚としている。**3枚を `git mv` で移設し、4枚を落とした。**

| 移設元 | 移設先 | 実測サイズ |
| --- | --- | --- |
| `guide/development_guide/06_TestFWGuide/_images/class_structure.png` | `implementation/class_unit_test/images/component/class_structure.png` | 728×296 |
| 同 `_images/select_sequence.png` | 同 `images/component/select_sequence.png` | 510×421 |
| 同 `_images/update_sequence.png` | 同 `images/component/update_sequence.png` | 531×453 |

落とした4枚は、いずれも `05_UnitTestGuide/01_ClassUnitTest/_image/` 配下のExcelシートのスクリーンショットである（`2e501ad:.../02_componentUnitTest.rst:116`・`:173`・`:262`・`:324` が参照）。テストデータの記述例は `testdata_examples.rst` にExcel形式・YAML形式の両方をテキストで持つため、Excel形式だけの画像を本ページに置くと形式の書き分けが崩れる。

`:scale:` は3枚とも付けていない。承認済みの `implementation/request_unit_test/rest.rst:17` が1009pxの画像に無指定であり、本ページの3枚はいずれもそれより小さい。

## 4. 出典の誤りと、実装に基づく訂正

出典と実装が食い違う場合は実装を優先する（`design.md` §8、`ntf-doc-weekend-queue.md:69`）。**本体の不具合ではなく旧解説書の記述誤りであるため、`decide` には上げず本文で訂正した。**

| 出典の記述 | 実装（`nablarch-testing` `e21bf67`） | 本ページ |
| --- | --- | --- |
| `02_DbAccessTest.rst:93` `assertSqlResultSetEquals("testSelectAll", "expected", actual)`（3引数） | `DbAccessTestSupport.java:226` は `(String message, String sheetName, String id, SqlResultSet actual)` の1オーバーロードのみ | `:176` で4引数 |
| `03_Tips.rst:140` `assertSqlResultSetEquals("testSelectByPk", expectedDataId, actual)`（3引数） | 同上 | `:285` で4引数 |
| `03_Tips.rst:612` `dbSupport.assertSqlResultSetEquals("test", "id", actual)`（3引数） | 同上 | `:117` で4引数 |
| `02_DbAccessTest.rst:217` `assertTableEquals("testDeleteExpired", actual)` | `DbAccessTestSupport.java:299`・`:313`・`:328`・`:342`・`:357` の5オーバーロードはいずれも実測値を引数に取らない | `:217` で `assertTableEquals("testDeleteExpired")` |
| `03_Tips.rst:503` `parser.getListMap("/foo/bar/Baz.xlsx", "sheet001", "params")` | `TestDataParser.java:53` は `(path, resourceName, id)`。`PoiXlsReader.java:47-78` は `resourceName` を `/` で分割し `path + '/' + <前半> + ".xls"`（無ければ `.xlsx`）を開く。出典の呼び方では `invalid data name.` になる | `:320` で `("/test/data/common", "CommonTestData/employees", "params")` |

## 5. 実装に基づく追記

出典が欠いている実装上必須の設定を書き足した（`ntf-doc-weekend-queue.md:68`）。

- **`:89-93` `dbAccessTest.dbTransactionName`** — 出典 `03_Tips.rst:561` は「プロパティファイルにトランザクション名を記載しておけば」とだけ述べ、キー名も値の意味も書いていない。根拠は `nablarch-testing` `e21bf67` の `DbAccessTestSupport.java:38`（`TRANSACTIONS_KEY = "dbAccessTest.dbTransactionName"`）、`:80-93`（Javadoc。カンマ区切り、デフォルトトランザクションは記述の有無に関わらず開始）、`:101-108`（値を `SystemRepository.getObject(key)` に渡して `SimpleDbTransactionManager` にキャストし、取れなければ `IllegalStateException`）。**値は「トランザクションの名前」ではなくシステムリポジトリに登録した `SimpleDbTransactionManager` のコンポーネント名である**ため、その旨と未登録時に例外になることを本文に書いた。

## 6. 判断

- **D-1 `current-0237` を「テストクラスを作成する」に置いた。** 個別指示 `ntf-doc-27-large-pages.md:72` の目安は「テストメソッドを作成する」だが、出典 `03_Tips.rst:565-566` が示す手順の実体は「テストクラスにて `DbAccessTestSupport` を継承する」であり、`:87` の継承とトランザクションの説明の直後が文脈上連続する。
- **D-2 `current-0216` を「テストメソッドを作成する」に置いた。** 目安は「テストデータを作成する」だが、出典 `03_Tips.rst:50-75` の内容はJavaコードでの `getListMap` の呼び方であって、テストデータの記述方法ではない。
- **D-3 `current-0218`〜`0220`・`current-0222` を「テストメソッドを作成する」に置いた。** 目安は「テストを実行する」だが、内容はループの組み方と `setUpDb`／`assertTableEquals` のオーバーロードの呼び分けであり、実行手順ではない。
- **D-4 `current-0027` の4分類表を「機能概要」に置いた。** `mapping.csv` の `dest_section` は「使用方法」だが、`design.md:285-295` が使用方法配下の5つのL3を固定しており、分類そのものはどのL3にも属さない見取り図である。機能概要の末尾（`:41-58`）に置き、`:328` の「テスト結果を確認する」の表と対応させた。
- **D-5 「テストメソッドを作成する」配下にL4を6つ置いた。** `style.md:193` は L4 を「用例が薄いページでのみ使う」としているが、承認済みページのL4実測は `testdata_examples.rst` 58件・`testdata_notation.rst` 27件・`deal_unit_test/batch.rst` 2件などで、6件は外れ値ではない（→ §9 `decide-1`）。
- **D-6 例のクラス名を出典の `DbAccessTestSample` から `EmployeeDbAccessTest` に変えた。** 本ページ `:70` が「クラス名は `<テスト対象クラス名>Test` とする」と定めており、出典のままでは自ら示した規則に反する。
- **D-7 テストデータの配置規則（同ディレクトリ・同名）を本ページに書かず参照に委ねた。** `testdata_notation.rst:53` が「ファイルは、テストコードと同じディレクトリに、テストコードと同じ名前（拡張子のみ異なる）で配置することを推奨する。」と定義しており、二重掲載になる。導入文は承認済みの `implementation/request_unit_test/batch.rst:139` と同型にした。
- **D-8 `TestDataParser` の直接使用（`:315`）をExcel／YAMLで書き分けなかった。** 第2引数の形（`<ファイル名>/<読み込み単位の名前>`）は両形式で同一で、違いはファイルの解決先だけである（`PoiXlsReader.java:47-78` と `nablarch-testing-yaml` `190cc9a` の `YamlLoader.java:81-85`）。`style.md` S-10 規約1「比較して伝える価値があるものだけ共通にする」に従い、1文で両形式を併記した。
- **D-9 `current-0221`（`03_Tips.rst:205-228`）は本ページに書かない。** `mapping.csv` は同行を「テストデータの書き方」に割り当てており、動機とグループIDの書式は `testdata_notation.rst:251`（`testdata_notation-group_id`）に既にある。本ページ `:295` にはテストコード側の操作（オーバーロードメソッドの呼び出し）だけを残し、記述方法は `:305` の `:ref:` に委ねた。

## 7. 実測値

| 項目 | 値 |
| --- | --- |
| 総行数 | 373行 |
| ページ先頭ラベル | `component_unit_test`（`style.md:373` と一致。`ja/` 配下で重複定義0件） |
| L1 下線 `=` | 50（表示幅24。`max(50, 表示幅)`） |
| L2 下線 `-` | 50 × 2件 |
| L3 下線 `~` | 49 × 5件（最大表示幅24） |
| L4 下線 `^` | 49 × 6件（最大表示幅42） |
| `code-block` | 12件（`java` 11・`properties` 1） |
| `list-table` | 3件（いずれも `:widths:` 指定あり） |
| `.. image::` | 3件（参照先ファイルはすべて実在） |
| `:ref:` | 11件。飛び先はすべて実在し、リンク文字列は飛び先の見出しと一致 |
| `:java:extdoc:` | 5件 |
| `important` / `tip` | 5件 / 2件 |
| 禁止語（`不具合`・`バグ`・`将来`・`修正され`） | 0件 |
| 禁止表記（`テストケース`・`テストソースコード`・`プロパティファイル`・`事前準備データ`・`想定結果`・`想定値`） | 0件 |
| `verify_mapping.py` | `OK: no errors`（exit 0） |
| Dockerフルビルド（`-E`） | `build succeeded, 1 warning.`。既知の `db_double_submit.rst:108: undefined label: how_to_set_token_in_request_unit_test` のみ。新規warning 0件 |

## 8. 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施した。**必須指摘は5件で、いずれも本文に反映済み。**

| 指摘 | 観点 | 対応 |
| --- | --- | --- |
| G6 禁止語「不具合」が `:363` にある | 検証 | 「誤り」に置換 |
| L2 違反。`:295` が `current-0221`（他ページ割当）の動機・書式を再掲している | 検証 | `:295` をテストコード側の操作2文に切り詰めた（D-9） |
| S-11 違反。L4を6つ持つL3の導入文が2つしか予告していない | 設計・クラフト | `:149` に予告を追加 |
| `dbAccessTest.dbTransactionName` の値がコンポーネント名である旨と、コンポーネント登録の手順が抜けている | QA・設計 | `:89` を書き直した（§5） |
| `TestDataParser` の第2引数の説明が「テストクラス名」になっているが、実体はファイル名 | QA | `:315` を「ファイル名」に訂正。あわせて `.xls`／`.xlsx` の両方を明記 |

推奨として採用したもの: 出典 `02_componentUnitTest.rst:257` の「期待値には自動設定項目も用意する」と同 `:112-114` の「採番用テーブルを初期化しないと挿入結果を検証できない」を `テストデータを作成する` に追記（G10 の取りこぼし解消）／`:41` の主語を「確認する対象」に変更／`:265` の見出しを「データを変えて同じテストメソッドを実行する」に変更／`:293` の見出しを「テストショットごとにデータを使い分ける」に変更／`:267` の造語「データバリエーション」を「テストショット」に置換（`ja/` 配下で0件、`glossary.md:201` に正表記あり）／`:324` の重複文を削除／`:235` の `LIST_MAP` の1文を `important` の前へ移動／`:117` のメッセージと `// 中略` の補足。

**不採用**

- `dbAccessTest.dbTransactionName` の設定手順を `setup/class_unit_test.rst` に新設し、本ページからは `:ref:` で送る案（設計）。`mapping.csv` は `current-0237` を本ページに割り当てており、第2部への移設は割当の変更にあたる。1ページ1コミットの原則からも他ページの本文追記は行わない（→ `decide-3`）。
- `:125` の因果を「同名の `static` メソッドによる隠蔽」に書き換える案（クラフト）。出典 `03_Tips.rst:523-524` の記述をそのまま踏襲した。JUnitの内部挙動は参照リポジトリで確認できず、実装で裏を取れない（→ `decide-4`）。
- `setup/master_data_restore.rst` に外部キー用のラベルを新設して `:313` の飛び先を節に変える案（設計）。他ページの変更にあたる（→ `decide-2`）。

## 9. 判断待ち

- **`decide-1`（参考）** `style.md:193` の L4「用例が薄いページでのみ使う」は、判定基準として使えない。承認済みページのL4件数は0件から58件まで分布しており、「薄い」の閾値がない。条文側の課題として別途判定が必要である。
- **`decide-2`（推奨）** `current-0196`（REFERENCE）の飛び先が、出典では節アンカー `MasterDataRestore-fk_key` だったのに対し、現在はページ先頭ラベル `master_data_restore` になっている。対応する記述は `setup/master_data_restore.rst:163` にあるが、その節の見出しは「テーブルの依存関係の解析を抑止する」（`master_data_restore-suppress_table_sort`）で、外部キーの扱いそのものを表していない。節ラベルを新設して飛び先を細かくするかを判断する必要がある。
- **`decide-3`（推奨）** `:89-93` は環境設定ファイルとコンポーネント設定ファイルの設定手順であり、`design.md:725` の観点D「第3部に設定が混入していないか」に抵触する可能性がある。ただし `mapping.csv` の `current-0237` は `dest_page` = コンポーネント単体テスト・`dest_section` = 使用方法である。マッピングを優先して本ページに置いたが、第2部 `setup/class_unit_test.rst` へ移すかを判断する必要がある。
- **`decide-4`（参考）** `:125` の「同名のメソッドに同種のアノテーションを付けると、スーパクラスのメソッドが起動されなくなる」は出典どおりだが、直後のコード例は `static` メソッドの同名宣言であり、実際の原因はアノテーションではなくメソッドの隠蔽と考えられる。JUnit4のランナーの挙動は参照リポジトリ（`nablarch-testing`・`nablarch-testing-yaml`）で確認できず**未確認**である。
- **`decide-5`（推奨）** `setUpDb` は `testTran` という名前の `SimpleDbTransactionManager` をシステムリポジトリから取得する（`DbAccessTestSupport.java:42`・`:188` → `TransactionTemplate.java:43-49`。未登録なら `IllegalArgumentException`）。`nablarch-testing` 側の設定例は `src/test/resources/framework.xml:8` にある。しかし `grep -rn "testTran" ja/` は新旧いずれの `.rst` でも0件で、解説書にこの前提を書いたページが存在しない。ブランクプロジェクトのテンプレートが提供しているかは作業ディレクトリ外のため**未確認**である。書くとすれば第2部 `setup/class_unit_test.rst` が帰属先になる。
- **`decide-6`（参考）** 例題のドメインがページ内で3系統に分かれている（`UserComponent`／`EmployeeDbAccess`／`EmployeeComponent`）。出典が `02_componentUnitTest.rst`・`02_DbAccessTest.rst`・`03_Tips.rst` の3本にまたがるためで、事実誤認ではない。統一するかは編集方針の判断事項である。
