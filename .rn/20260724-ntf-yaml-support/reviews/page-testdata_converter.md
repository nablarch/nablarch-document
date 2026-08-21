# page-testdata_converter — テストデータ変換ツール（`#27-03`）

対象ファイル: `ja/development_tools/testing_framework/tools/testdata_converter.rst`
ラベル: `testdata_converter`（`mapping/style.md:347`）
部: 第4部 ツール

## 参照リポジトリ

| リポジトリ | 作業指示のピン | 執筆・検証時の HEAD | `#32` の是正2 の追記分の参照コミット |
|---|---|---|---|
| `nablarch-testing-converter` | ピンなし（作業指示に記載がない） | 執筆時 `e80a4dd` → レビュー時 `2f21bce` | `e977824` |
| `nablarch-testing-yaml` | `190cc9a` | `b91abc1` | — |
| `nablarch-testing` | `e21bf67` | — | `e21bf67`（作業指示のピンと同値） |

第3列は執筆・検証の時点で記録した HEAD であり、その後も他セッションのコミットで動く。2026-08-21 に `git -C <repo> log -1` で実測した HEAD は、`nablarch-testing-converter` が `6d12021`（ブランチ `ntf-test-data-converter`）、`nablarch-testing` が `f41cc64`（ブランチ `convert-testdata-excel-to-text`。作業指示のピン `e21bf67` とは分岐している）、`nablarch-testing-yaml` が `0197071`（ブランチ `feature/ntf-yaml`）である。本ページの事実は第2列のピンと第4列の参照コミットで成り立っており、HEAD には依存しない。

`nablarch-testing-converter` は作業指示の参照リポジトリ表に記載がない第3のリポジトリである。執筆中に他セッションが同リポジトリへコミットしたため HEAD が `e80a4dd` から `2f21bce` へ進んだ。差分は `git diff e80a4dd 2f21bce` で `DirectiveUtil` / `XlsFormatReader`（レコード種別の空文字→null 化、区切り文字正規化の共通化）/ `YamlFormatReader` の3ファイルであり、本ページが記載した事実の対象外であることを確認した。**「出典から変えた点」の末尾3件を除く本ページの事実は、すべて `2f21bce` で再確認済みである。** 末尾3件（マーカーカラム・空エントリ・行末の空セル）は `#32` の是正2 で追記したもので、参照コミットは `2f21bce` の140コミット後の `e977824` である（`git rev-list --count 2f21bce..e977824` → `140`）。うち `TestCoreReaderAdapter.java` の3箇所は `2f21bce` でも同じ行に同じ逐語で成立するが、`src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java:491` は `2f21bce` では `result.add(entry);` であって成立しない（実測: `git show 2f21bce:src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java | sed -n '491p'`）。空エントリの根拠は `nablarch-testing` `e21bf67` で確認した。

`nablarch-testing-yaml` の作業ツリーはピン `190cc9a` より先の `b91abc1` にある。JSON Schema の所在についてはピン `190cc9a` で `git ls-tree` により直接確認した。

## 出典行の消化

`mapping.csv` を `csv.DictReader` で読み `dest_page == 'テストデータ変換ツール'` を抽出した全6行。DROP なし。

| mapping_id | 出典（`input/testdata-converter-design.md`） | ページ上の反映先 | 判定 |
|---|---|---|---|
| input-0183 | `:13-15` | リード文、機能概要冒頭 | 消化。「難所は変換ツールと本体で構造解釈をズラさないこと」は内部設計の論点のため落とした |
| input-0184 | `:17-33` | 機能概要「意味を変えずに往復できる」の表、前提事項 | 消化。mermaid 図は散文化。4項目（構造/値/意図ある情報/無意味な情報）を表の4行に対応させた。**ただし「無損失」の主張が実装で成り立たない（`decide` 1）** |
| input-0190 | `:106-115` | 前提事項の特殊記法・クォート記法、機能概要の `tip` | 消化。「全値ダブルクォート」は実装に合わせて修正。Excel 側のクォート記法が往復で失われる点を実装から追記 |
| input-0194 | `:155-171` | 「Excel形式の出力を整形する」全体 | 消化＋実装で補強。出典表の `[要確認]` 4色は実装値で確定。出典表の「データタイプ識別行の背景色」は落とした（`xls/RowKind.java:8` で META 行は背景色なしのため） |
| input-0198-b | `:295` | 機能概要「YAML形式のテストデータの記述ミスを検出できる」 | 消化。ただし**出典と逆の記述**（「出典から変えた点」参照） |
| input-0199 | `:300-326` | 「Javaのコードから変換を呼び出す」「YAML形式のテストデータを検査する」 | 消化。`FormatHandler`・`ConverterFileFilter`・`ConverterPathResolver`・クラス図は内部構造のため落とした |

## 実装で確認した事実

`nablarch-testing-converter@2f21bce`。パスは `src/main/java/nablarch/test/tool/converter/` からの相対。

| 記載内容 | 出典（file:line） |
|---|---|
| ゴール名 `convert`、`requiresProject = false` | `ConverterMojo.java:22` |
| `from`/`to`/`input`/`output` は `required = true`、プロパティ名は `nablarch-testing-converter.*` | `ConverterMojo.java:26-42` |
| `overwrite` の既定値 `false` | `ConverterMojo.java:41-42` |
| `<includes>`/`<excludes>`/`<excludeSheets>`/`<xlsOutput>` | `ConverterMojo.java:47-59` |
| すべての `@Parameter` は `<configuration>` でも指定できる。`property` 付きのものはコマンドラインでも指定できる | Maven の `@Parameter` 仕様。検証観点が Maven ゴールを実行し `<excludeSheets>`・`<xlsOutput>` が効くことを実測 |
| groupId `com.nablarch.framework`、artifactId `nablarch-testing-converter`、`1.0.0-SNAPSHOT`、`packaging: maven-plugin` | `pom.xml:14-17` |
| `nablarch-testing-yaml:1.0.0-SNAPSHOT` に依存 | `pom.xml:41-43` |
| `TestDataConverter` は static 専用。4引数 `convert` と `convert(ConversionRequest)` | `TestDataConverter.java:31-79` |
| パッケージは `nablarch.test.tool.converter` | `TestDataConverter.java:1` |
| 戻り値は「変換したコンテナ（テストクラス相当）の件数」 | `TestDataConverter.java:47, 62`（Javadoc の文言そのもの）。26シートのブック1冊で戻り値 `1` を実測 |
| `overwrite=false` で衝突すると `ConverterException` | `TestDataConverter.java:90-100` |
| `DataFormat.XLS("xls")` / `YAML("yaml")` | `DataFormat.java:16-19` |
| `Builder` の `include`/`excludeSheet`/`exclude`/`includes`/`excludes` はすべて public | `ConversionRequest.java:195, 206, 217, 230, 245` |
| Excel の読み込み対象拡張子は `.xls` と `.xlsx` | `ConverterFileFilter.java:29` |
| `<includes>`/`<excludes>` の評価対象は、YAML 変換元のときは**ディレクトリ** | `ConverterFileFilter.java:64-78`（`.map(Path::getParent)` 後に `accepted` へ渡す） |
| Excel→YAML: `foo/bar.xlsx` → `foo/bar/` 配下に `<シート名>.yaml` | `ConverterPathResolver.java:40-45`、`YamlFormatHandler.java:66` |
| YAML→Excel: `foo/bar/` → `foo/bar.xlsx` | `ConverterPathResolver.java:58-62`、`XlsFormatHandler.java:65` |
| `<excludeSheets>` は変換元 YAML では無視される | `YamlFormatHandler.java:36-37`（コメントで明記） |
| YAML 出力は全値ダブルクォート、ただし値なしは裸の `null` | `yaml/YamlFormatWriter.java:64`（`ScalarStyle.DOUBLE_QUOTED`）、`:372-377`（`q(null)` はクォートなしの `null` を返す） |
| Excel のクォート記法は読み込み時に外れ、書き戻し時に付け直されない | `xls/XlsFormatReader.java:157, 187, 423, 492, 537`（`stripQuotes`）／`xls/XlsFormatWriter.java` に quote 関連の処理なし（`grep -n 'quote\|Quote'` が0件） |
| `ExcelFormatConfig.defaults()` の11項目の既定値（LIME / PALE_BLUE / LIGHT_YELLOW / LAVENDER / LIGHT_ORANGE / true / 20 / true / true / false / 1） | `xls/ExcelFormatConfig.java:124-134` |
| `blankRowsBetweenBlocks >= 0`、`maxColumnWidthChars >= 1` | `xls/ExcelFormatConfig.java:85-92` |
| `drawBlockBorder` に対応するメソッドは `withBlockBorder`、`drawCellBorder` は `withCellBorder`（`draw` は付かない） | `xls/ExcelFormatConfig.java:233, 246` |
| 色を差し替えるメソッドの引数は `short` | `xls/ExcelFormatConfig.java:155` |
| `<xlsOutput>` の11要素名 | `XlsOutputConfig.java:20-64` |
| `<xlsOutput>` の色は `IndexedColors.valueOf` で解決する（＝列挙定数名） | `XlsOutputConfig.java:16, 178-188` |
| ヘッダ色のグループ分け（testShots / SETUP系 / EXPECTED・RESPONSE系 / その他） | `xls/Fill.java:7-18`、`xls/BlockLayout.java:110-143` |
| リンタの検査ルール V-COL/V-DIR/V-SCH/V-FNAME/V-DKEY/V-YAML と V-IO | `yaml/YamlTestDataValidator.java:36-45`、`:132`（V-IO） |
| `validate(Path)` は `listFiles` で**直下のみ**を走査し、再帰しない | `yaml/YamlTestDataValidator.java:110-114`。検証観点が `nested/bad.yaml` が検出されないことを実測 |
| リンタは変換の処理経路に組み込まれていない | `grep -rn 'YamlTestDataValidator' src/main/` の該当が自クラスの3行のみ |
| JSON Schema の提供元は `nablarch-testing-yaml` | `nablarch-testing-yaml@190cc9a:src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json`（`git ls-tree` で確認）。converter 側には存在しない |
| 利用者が書くデータタイプ名は `SETUP_TABLE`（`SETUP_TABLE_DATA` は enum 定数名） | `nablarch-testing/src/main/java/nablarch/test/core/reader/DataType.java:14` — `SETUP_TABLE_DATA(1, "SETUP_TABLE")` |
| 空マッピング由来の空行はデータブロック内で保持される | `model/ListMapBlock.java:12, 25` |

## 出典から変えた点

| 箇所 | 出典の記述 | ページの記述 | 変えた理由 |
|---|---|---|---|
| 全値ダブルクォート | `input/testdata-converter-design.md:114`「全値をダブルクォートで囲む」 | 「値なしを除いてすべて」 | 実装が `q(null)` で裸の `null` を書き出すため（`YamlFormatWriter.java:372-377`）。姉妹ページ `implementation/testdata_notation.rst:1430`「``null`` のみクォートなしで記述する」とも一致する |
| リンタの位置づけ | `input/testdata-converter-design.md:295`「`YamlTestDataValidator` は YAML OUT 後にスキーマ検証を行うリンター」、同 `:291` のクラス図も「出力後スキーマ検証」 | 「変換の処理経路には組み込まれていない」 | `grep -rn 'YamlTestDataValidator' src/main/` の参照が自クラスのみで `YamlFormatWriter` から呼ばれていないため。作業指示 §2「出典と実装が食い違う場合は実装を優先する」に従った。**`mapping.csv` の `note` 列は出典どおりのままなので、後続で「出典に戻す」是正をしないこと** |
| Excel 出力の色 | `input/testdata-converter-design.md:155-171` の表で既定色が `[要確認] 見やすい配色を調査して決定` | LIME / PALE_BLUE / LIGHT_YELLOW / LAVENDER / LIGHT_ORANGE | 実装 `ExcelFormatConfig.java:124-134` で確定済みのため |
| Maven プラグイン | 出典全362行に Maven / mvn / プラグイン / CLI の記述が0件 | 「Mavenプラグインで一括変換する」節を新設 | `ConverterMojo.java:22` が実在する。`TestDataConverter.java:26` の Javadoc「CLI・Maven プラグインはリポジトリ分割後に整備」はリポジトリ分割後の現状では古い。作業指示 §2「出典が欠いている、実装上必須の設定は書き足してよい」に従った |
| Java API の依存関係 | 出典に記述なし | test スコープの `<dependency>` を追加 | `pom.xml:17` が `maven-plugin` パッケージングであり `<plugin>` 宣言だけではテストのクラスパスに乗らない。先例は `setup/common.rst:20-36` |
| リンタの呼び出し方 | 出典に記述なし | 「YAML形式のテストデータを検査する」節を新設 | 出典 `:295` はリンタの存在を述べるのみで呼び出し方がなく、ページだけではリンタを実行できないため。章構成設計 `.rn/20260724-ntf-yaml-support/design.md` §5「第4部 ツール」の「ページのアウトライン」が 使用方法 の配下を `<操作手順>する` としていることに合わせて 使用方法 配下に置いた |
| 出力パスの構造 | 出典に記述なし | Excel↔YAML の入出力対応表 | `ConverterPathResolver.java:40-62`。出典の記述では読者が出力物の置かれ方を予測できないため |
| Excel クォート記法 | `input/testdata-converter-design.md:110-112` は Excel 側のクォート記法に触れているがページに落ちていなかった | 前提事項に1段落追記 | 往復で見える差分であり、変換の可否を判断する読者に必要なため |
| レコード種別 | 出典に記述なし（`testdata_notation.rst:1164`） | 前提事項に1段落追記 | 同上 |
| マーカーカラムの保持 | `input/testdata-converter-design.md:31`「意図ある情報は無損失（マーカーカラム、空エントリ、空欄のレコード種別を保持）」 | 「意味を持たない情報」の除去側に置き、往復時の挙動を 前提事項 に書いた | 実装は両形式で除外する。Excel は `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129` `return Arrays.asList(header.getEffectiveColumnNames());`、YAML は `src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java:491`「エントリ先頭行のキー（YAML 記述順）からマーカーカラム（`{@code [COL]}`）を除いたカラム名を返す。」。いずれも `nablarch-testing-converter@e977824` を `git show` で開いて照合した（`#32` の是正2、2026-08-21） |
| 空エントリの保持 | 同上 | どちらの欄にも書けないため表から外した。読み飛ばしそのものは `implementation/testdata_notation.rst:1534` が説明している | 実装は経路で割れる。Excel は NTF 本体が読み飛ばす（`nablarch-testing@e21bf67:src/main/java/nablarch/test/core/reader/PoiXlsReader.java:140-147` の `private boolean isBlankLine(List<String> line)` が全要素空のとき `true` を返し、同 `:93` `if (isBlankLine(list)) {` の直後の `continue;` で行が読み飛ばされる）。YAML は `YamlFormatReader` に処理が無い（`nablarch-testing-converter@e977824` で `grep -rn 'dropEmptyEntries\|isEmptyEntry' src/main/java/` のヒットは `xls/XlsFormatReader.java` のみ）。いずれも `git show` で開いて照合した。無損失が両形式で成り立たない（`#32` の是正2、2026-08-21） |
| 行末の空セルの除去 | `input/testdata-converter-design.md:32`「無意味な情報は持たない（コメント、完全な空行、行末の空セルを除去）」 | 「意味を持たない情報」の行から外し、前提事項へ1段落として移した | 実装は Excel 経路のみ（`src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:254`「{@link NablarchTestUtils#trimTailCopy(List)} で行末の空セルを除去済みである。」・同 `:410`「{@link NablarchTestUtils#trimTailCopy(List)}で行末の空セルを除去して返す。」。`src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java` には無く、`grep -n 'trimTail'` のヒットが0件。いずれも `nablarch-testing-converter@e977824` を `git show` で開いて照合した）。`implementation/testdata_notation.rst:1545` も「\ Excel\ 形式のみ。\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込む」と明記している（`#32` の是正2、2026-08-21） |

上表の末尾3件（マーカーカラム・空エントリ・行末の空セル）は `#32` の是正2 で追記した。逐語は 2026-08-21 に `nablarch-testing-converter@e977824` の `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129`・`:254`・`:410` と `src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java:491`、および `nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/reader/PoiXlsReader.java:93`・`:140-147` を `git show` で開いて照合し、行番号と文面が一致することを確認した。章構成設計 `.rn/20260724-ntf-yaml-support/design.md` §8「トンマナ」の「出典と実装が食い違う場合」が求める、確認した実装のファイル名・行番号・参照したコミットの記録にあたる。

## Mavenプラグインのバージョン表記

`<plugin>` に `<version>` を書いていない。`nablarch-testing-converter` は `1.0.0-SNAPSHOT`（`pom.xml:16`）で未リリースであり、作業指示 §8 の「未リリースモジュールはバージョンを書かず、他ページと同じ体裁にする」に従った。同じ体裁の先例は `ja/development_tools/toolbox/JspStaticAnalysis/01_JspStaticAnalysis.rst:223-226`。

**申し送り**: リリース時に `<version>` の要否と BOM への収録を判断すること。BOM に収録されるならバージョン省略のままでよい。収録されない場合は、本ページの XML 例3か所と `mvn` コマンド例にバージョン指定を足す必要がある。検証観点の実測では、プラグインを pom.xml に宣言せずに `mvn com.nablarch.framework:nablarch-testing-converter:convert` を実行すると `Error resolving version for plugin` になる（`:1.0.0-SNAPSHOT:convert` と明示すれば動く）。本ページは先にプラグインを pom.xml へ追加する手順を示しているため、記載どおりに進めた読者はこの問題にあたらない。

## クラス名の表記

converter のクラス（`TestDataConverter`・`ConversionRequest`・`ExcelFormatConfig`・`YamlTestDataValidator`・`ValidationError`・`DataFormat`）は `:java:extdoc:` を使わずインラインリテラルにした。`ja/conf.py:299-323` の `javadoc_url_map` が向く先は公開済み Javadoc であり、未リリースの `nablarch-testing-converter` のクラスはリンク切れになるため。`nablarch-testing-yaml` のクラスについて既存ページが採っている扱いと同じである。

例外は `nablarch.test.core.file.TestDataConverter`（`setup/request_unit_test/mom.rst:35` で既に `:java:extdoc:` 付きで解説されている別クラス）で、単純名が衝突するため `:java:extdoc:` 付きで並記して区別した。

## 4観点レビュー

QA / 設計 / クラフト / 検証の4観点を、それぞれ独立したサブエージェントで実行した。各エージェントには「実測コマンドで裏付けよ。推測で書くな」「成果物に付属する検証スクリプトを正解として使わず、独立に組め」「敵対的にレビューせよ」の3点を課した。QA と検証は Maven プラグインをローカルへ install してゴールを実行し、実フィクスチャで変換結果を観測している。是正は1ラウンドで畳んだ。

### 是正した指摘

| 指摘 | 観点 | 是正内容 |
|---|---|---|
| `SETUP_TABLE_DATA` は内部 enum 名。利用者が書くのは `SETUP_TABLE` | QA・クラフト・検証 | `SETUP_TABLE` に修正 |
| 「値をすべてダブルクォートで囲む」は誤り。値なしは裸の `null` | QA・検証 | 「値なしを除いてすべて」に修正し、`null` の扱いを明記 |
| 出力先のファイル・ディレクトリ構造が書かれていない | QA・クラフト・検証 | 入出力の対応表を 使用方法 冒頭に追加 |
| リンタは指定ディレクトリ直下しか見ない。親を渡すと無言で0件 | QA・検証 | 使用方法 に検査の節を新設し、`important` で非再帰を明記 |
| `<includes>`/`<excludes>` は YAML 変換元ではディレクトリを評価する | QA・検証 | 表の説明を書き分け |
| Java API を使う読者向けの `<dependency>` がない | QA・設計 | test スコープの `<dependency>` を追加 |
| `with` で始まるメソッド名の説明が `withDrawCellBorder` を導く（実際は `withCellBorder`） | 設計・クラフト | 表に「Javaのメソッド」列を追加し、11項目すべてのメソッド名を明記 |
| 背景色の指定方法が Maven（列挙定数名）と Java（`short`）で異なる | 設計・クラフト・検証 | 表の前書きで両方の指定方法を書き分け |
| `<excludeSheet>`（単数形）の子要素が表にない | クラフト | `<include>`/`<exclude>`/`<excludeSheet>` を各行に明記 |
| `TestDataConverter` が `nablarch.test.core.file.TestDataConverter` と同名 | クラフト | パッケージ名を明記し、別クラスである旨を `:java:extdoc:` 付きで並記 |
| 「空エントリ」と「完全な空行」が同一物に見えるのに保持と除去に分かれている | クラフト | 「データブロックの内側にある空エントリ」「データブロックの外側にある空行」に書き分け（`model/ListMapBlock.java:12`「空マッピング由来の空行も空リストとして保持」による） |
| 「往復」の定義が循環している | クラフト | 「変換元と変換先に同じ形式を指定した場合」と言い換え、Excel→YAML→Excel の往復にも触れた |
| リンタの操作手順が 機能概要 にある（`design.md:346-348` では 使用方法 が操作手順） | 設計・クラフト | 機能概要 は「何ができるか」だけにし、呼び出し方を 使用方法 へ移した |
| `important` 2件が「読者が必ず守るべき注意事項」（`style.md:232-234`）にあたらない。片方は重複 | 設計・クラフト | 末尾の `important` を削除（前提事項と重複）、ダブルクォートの `important` を `tip` に降格して 機能概要 冒頭へ移動 |
| 検査内容が225字1文で6項目 | QA・クラフト | 箇条書きに分解。あわせて V-IO を7項目目として追加 |
| 「レコード断片」は用語集にない造語 | 設計・QA・クラフト | `testdata_notation.rst:124, 879, 881, 904, 1107` が使う「レコード定義」に統一 |
| 「ブロック」「LIST_MAP=testShots」が正表記でない | 設計・クラフト | 「データブロック」「テストショット一覧」に統一（`glossary.md:212, 215`） |
| 地の文の `\ ` エスケープが承認済み9ページ中このページだけ未適用 | クラフト | 地の文の `Excel`・`YAML`・`Java` とインラインリテラルの区切りを `\ ` に統一。実測で `ja/` 全体は `\ Excel\ 形式`/`\ YAML\ 形式` が125件、素の表記が2件（本ページを除く）。見出しは素の表記が慣行のため対象外とした |
| `<plugin>` が `<build><plugins>` の外に単独で示されている | QA | 最初の例を `<build><plugins>` で包み、以降の例にコメントで補った |
| Java の Excel 出力例が `overwrite` 未指定で衝突しうる | QA | `.overwrite(true)` を追加 |
| Java からの `include`/`exclude` による絞り込みが未記載（出典 input-0199 の落とし） | 検証 | `include`/`exclude`/`includes`/`excludes` を本文で説明し、例に `.include(...)` を追加 |
| `<excludeSheets>` が変換元 Excel 限定である旨が未記載 | 検証 | 表の説明に追記（`YamlFormatHandler.java:36-37`） |
| Excel のクォート記法が往復で失われる（出典 input-0190 の落とし） | QA | 前提事項に追記 |
| レコード種別の扱いが両形式で異なる（`testdata_notation.rst:1164`） | 検証 | 前提事項に追記し、書き方ページへ誘導 |
| 「乗る」「本体」「入口」「見た目」など用語集外の口語 | クラフト | 「保持される」「テスティングフレームワーク」「変換を呼び出すクラス」「Excel形式の出力を整形する」に置き換え |
| 見出し「Excel出力の見た目を整える」とラベル `-xls_output` | 設計・クラフト | 「Excel形式の出力を整形する」／`testdata_converter-xls_format` に変更 |

### 採らなかった指摘

| 指摘 | 観点 | 採らなかった理由 |
|---|---|---|
| 見出し「前提事項」が `style.md:155-156` の禁止語（注意事項 等）と同型 | 設計 | `style.md:127-182` の「〜する」形式規約と内容条件は**「使用方法」「拡張例」配下の小見出し**を対象としており、機能概要 配下の「前提事項」は対象外。承認済みの `setup/junit5_extension.rst:71` も同じ見出しを使っている。`mapping.csv` の `heading_path` にも「前提事項」で終わる行が3件ある（current-0202 / current-0344 / current-0359） |
| 表4件は `about/index.rst` と同数なので `style.md:273` の全 `list-table` 例外の対象外 | 設計 | S-07 の本則は「セル内に複数行の説明や長文が入る表は `list-table`」であり、本ページの表はいずれも1セルに長文の説明が入る。例外条項に頼らず本則で `list-table` を選んでいる。クラフト観点の独立検査でも S-07 適合と判定された |
| 「区分」列（構造/値/意図のある情報/意味を持たない情報）が排他的でない | クラフト | 出典 `design.md:29-33` の4項目をそのまま表にしたもの。分類の組み替えは出典の主張の書き換えにあたるため採らない |
| 使用方法 配下を L4（`^`）で階層化すべき | 設計 | 4つの L3 で並列に読める構成であり、L4 を導入すると 第4部 の他ページと構成が揃わなくなる |
| 「目盛り線」は Excel 日本語 UI の表記と一致するか未確認 | クラフト | UI の表記を確認できていないため、UI ラベルを主張しない「グリッド線」に変更した |

## ゲート

`ntf-doc-weekend-queue.md` §5 の G1〜G13。

| ゲート | 内容 | 結果 | 実測 |
|---|---|---|---|
| G1 | 出典行の全消化 | OK | `dest_page == 'テストデータ変換ツール'` の6行すべてをページ上の位置に対応づけた（上表） |
| G2 | 出典外の記述に実装出典がある | OK | 「出典から変えた点」の9件すべてに `file:line` を付した |
| G3 | 作業ツリーが汚れていない | OK | ビルド後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`git status --porcelain` は本ページと本レビューファイルのみ |
| G4 | `verify_mapping.py` が exit 0 | OK | `OK: no errors` / `exit=0` |
| G5 | Sphinx ビルドが警告を増やさない | OK | `build succeeded, 1 warning.` 唯一の警告は既存の `ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` |
| G6 | 禁止表現なし | OK | `grep -nE '本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス\|です。\|ます。'` が0件 |
| G7 | `note`/`warning` を使っていない | OK | 0件。`tip` 3件・`important` 1件 |
| G8 | 見出し下線の長さ | OK | L1 `=`×50（タイトル表示幅22）、L2 `-`×50（最大幅8）、L3 `~`×49（最大幅44）。全10見出しで下線長 ≧ タイトル表示幅 |
| G9 | 生成 HTML のリンクが解決する | OK | `href="#"` 0件。`:ref:` がすべて解決 |
| G10 | 用語が用語集どおり | OK | データブロック / テストショット一覧 / Excel形式 / YAML形式 / 特殊記法 / マーカーカラム / フレームワーク制御ヘッダ / デフォルト を正表記で使用。`テストケース` 0件 |
| G11 | コードブロックに言語指定がある | OK | 全件に言語指定（`xml`・`bash`・`java`） |
| G12 | 目次3行の体裁 | OK | `.. contents:: 目次` / `:depth: 3` / `:local:` がラベル→タイトル→目次の順 |
| G13 | toctree に登録済み | OK | `ja/development_tools/testing_framework/tools/index.rst:10` |

## 判断待ち（`decide`）

1. **【重大】往復で意味が変わるケースがある。** 検証観点が `nablarch-testing-converter@2f21bce` 同梱のフィクスチャ `src/test/resources/nablarch/test/tool/converter/xls/reference/ProjectActionRequestTest.xlsx` で XLS→XLS 往復を実測したところ、`confirmOfCreateAbNormal` シートの `LIST_MAP`／`requestParams` でリクエストパラメータ4件が消滅した（`rows:` が空配列になる）。26シート中で `- {}`（空エントリ）が 1個→15個に増える箇所、1個→0個に消える箇所が計十数か所ある。Maven 経由・インプロセス直接呼び出しの両方で再現。
   - ページは「意味を変えずに往復できる」という見出しと、表の「意図のある情報 … 無損失で保持する」で、これを成り立つものとして書いている。出典 `design.md:25-30` の主張どおりの記述である。
   - 作業指示 §2「出典と実装が食い違う場合は実装を優先する。ただし**本体の不具合が疑われる場合は書かずに `decide` に上げる**」に従い、**ページには書かず、ここに上げる。** 変換ツールの欠陥と見るのが自然であり、「往復すると空エントリが増減する」と仕様化してしまうと修正を妨げる。
   - 判断が要るのは2点。(a) これは converter の不具合か、意図した挙動か。(b) 不具合なら、修正するまで本ページの「意味を変えずに往復できる」節をどう扱うか（そのまま出す／注記を付ける／節を落とす）。

2. **「導入」を置かない判断の根拠が古くなった。** `design.md:330-360` は「テストデータ変換ツールも『導入』を持たない。出典（`testdata-converter-design.md` 全362行）にインストール手順・依存関係・設定に該当する記述が存在しないため」としている。本ページは実装から Maven プラグインの追加手順と `<dependency>` を書き足したため、実質的な導入手順が 使用方法 配下に入っている。`design.md` §5 の記述を更新するか、この節の位置づけを決める必要がある。`design.md` は規約ファイル（Rule §1-3 で変更禁止）なので、こちらでは直していない。

3. **同名の `.xls` と `.xlsx` が同一ディレクトリにあると破綻する可能性がある。** `ConverterFileFilter.java:29, 144-159` は両方を列挙するが、`XlsFormatHandler.java:34, 46` は拡張子を落としたブック名で読み直し、`PoiXlsReader.java:62-64` が `.xls` を優先する。結果として2件が同じ内容・同じ出力先になる（コードからの帰結であり、実測はしていない）。converter の不具合が疑われるため、ページには書いていない。

4. **`nablarch-testing-converter` の参照コミットがピンされていない。** 作業指示の参照リポジトリ表に本リポジトリの記載がなく、執筆中に HEAD が `e80a4dd` → `2f21bce` へ動いた。後続ページで同リポジトリを参照する場合に、どのコミットを基準にするか決める必要がある。

5. **`mapping.csv` の `note` 列と実装が食い違う行がある。** input-0198-b の `note` は出典どおり「YAML OUT 後にスキーマ検証を行うリンター」と書かれているが、実装ではリンタは変換の処理経路に組み込まれていない。`disposition` は `MERGE` のままで、逸脱がマッピング側から追跡できない。Rule §1-4 で `mapping.csv` の直接編集は禁止のため、こちらでは直していない。
