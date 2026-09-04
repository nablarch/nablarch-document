# NTF テストデータ変換ツール 設計書

NTF のテストデータを Excel と YAML で相互変換するツールの設計です。
中核の設計判断は一つ──**読み込みロジックを NTF 本体と共有し、変換ツールと本体で解釈がズレないことを保証する**こと。ズレれば、変換ツールが妥当とみなしたデータを本体が別物として読む不整合が起きます。この一点から、以下の構造・再利用方針・品質担保がすべて導かれます。

本体の読み込み機構は [ntf-testdata-loading.md](ntf-testdata-loading.md) を参照。

---

## 1. 何を作るか（背景と決定）

### 解くべき課題

Excel で書かれてきた NTF テストデータを、AI エージェントが扱える YAML にも対応させる。そのため両形式を相互変換するツールを作る。難所は前述のとおり、変換ツールと本体で構造解釈をズラさないことにある。

### 基準は「形式」ではなく「NTF 仕様上の意味」

中間モデルを置き、Excel と YAML はその意味を各形式の記法で表したものとして扱う。どちらの形式も基準としない。

```mermaid
flowchart LR
  XLS[Excel] <--> MID[中間モデル<br/>NTF仕様上の意味] <--> YAML[YAML]
```

**可逆性**：ある形式 → 中間モデル → 同じ形式 と往復したとき、NTF 仕様上の意味が変わらないこと。形式に固有で意味を持たない情報（Excel の色・書式・結合セル、YAML のコメント等）は中間モデルに乗らず、可逆性の対象外とする。

**中間モデルが満たす状態**：

- 構造は解析済み（レコードレイアウトの区切り、各行の役割、フィールド名と値の対応を保持）
- 値は未変換（`${systemTime}` 等の特殊記法を解決せず文字列のまま保持）
- 意図ある情報は無損失（マーカーカラム、空エントリ、空欄のレコード種別を保持）
- 無意味な情報は持たない（コメント、完全な空行、行末の空セルを除去）

### 保持するか捨てるかの判断基準

迷う情報は一つの基準で割り切る。**その情報がテスト作成者の意図を持つなら保持し、持たない（本体が機械的に補う／捨てる）なら本体に従う。**

本体の読み込み（①読む→②掃除→③特殊記法変換→④組み立て）の各処理を、変換ツールが実行するかどうかは、この基準で決まる。

| 段 | 処理 | 変換ツール | 理由 |
|---|---|---|---|
| ① | 読む（形式→行・セル）| 実行 | 変換ツールも各形式を読む |
| ② | コメント行・行内コメント除去 | 実行 | 注釈用途。中間モデルに位置づける先がない |
| ② | 空行除去（完全な空行）| 実行 | 全セル空は無意味。仕様上もスキップ対象 |
| ③ | 特殊記法変換（`null`・`${...}`・`""`・`\r` 等）| **実行しない** | 不可逆。記法のまま保持しないと本体の挙動が壊れる |
| ④ | 構造解析（名前/型/長さ/データの読み解き）| 実行 | 中間モデルの組み立てに必須 |
| ④ | マーカーカラム除外 | **実行しない** | `[...]` を外せば意味あるカラム名。作成者の意図を持つ |
| ④ | 行末空セル除去 | 実行 | 末尾の無意味な余白。意図を持たない |
| ④ | レコード種別の default 補完 | **実行しない** | 元データにない値。補完は本体の責務 |
| ④ | デフォルト値補完（DB 登録時）| **実行しない** | DB 登録時の処理。読み込み構造化の対象外 |

補足が要るのは 2 点。**空行の区別**──「先頭フィールドのみ空」の空エントリは完全な空行ではなく、ファイルデータではデータ行として意味を持つため保持する。**補完の一貫性**──default 補完・DB デフォルト値補完は中間モデルでは行わず空欄のまま保持し、復元時も補完しない。最終的に本体が読む際に補うので結果は変わらず、補完の責務を本体に一貫させられる。

### 制約

- **既存 NTF 本体（Excel 読み込み）**：観測可能な挙動の維持が必達。挙動を変えないリファクタリングは可。明確なバグの修正は、観測挙動の維持を破らないため許容する。
- **YAML 対応・変換ツール**：新規開発につき変更可。
- 機能追加対象は最新バージョン **v6 のみ**。実装完了後、YAML 対応と変換ツールは別リポジトリへ分割する（他バージョンをフォークで作りやすくするため）。

---

## 2. どう作るか（設計判断）

冒頭の「本体と解釈をズラさない」を、**本体の構造解析を変換ツールが再利用する**ことで満たす。本体と同じ器（`DataFile`／`TableData`／`MessagePool`）に行き着けば、構造解釈は 1 箇所に集約されズレない。

再利用する処理としない処理の線引きは、1 章の表のとおり。①読む・④構造解析は再利用し、③特殊記法変換・④破壊的整形（本体 getter が被せる加工）は持ち込まない。

ここで設計判断が分かれるのは、**本体に Excel と YAML の 2 系統があり、再利用の取り回しが違う**点。経路ごとに判断を示す。

### 判断 A：Excel 経路 — アダプタで再利用

**検討した選択肢と却下理由**

本体の `BasicTestDataParser` の公開 API（`getSetupFile`／`getExpectedTableData` 等）をそのまま呼ぶ案は却下した。これらは結果を返す前に不要な加工を被せるため──`getSetupFile` は `BinaryFileInterpreter` を必ず先頭に積み `${binaryFile:...}` を解決し、`getExpectedTableData` は `fillDefaultValues`（DB 全カラム補完）と種別マージを行う。1 章の「記法のまま・無損失」に反する。

**決定**

公開 API を経由せず、配線役の責務だけを薄いアダプタが肩代わりする。`BasicTestDataParser` は各 Parser へ `reader`・`interpreters`（・テーブル系は `dbInfo`）を渡して生成しデータタイプで振り分ける配線役にすぎない。アダプタが同じ配線を、**空の `interpreters`** で行い、`parse → getResult` で生の器を取り出す。

これで `null`・`${...}`・`""` 等は解釈されず、補完・マージも起きない。特殊記法は記法のまま中間モデルへ運ばれ、本体がテストとして読む際に解釈される。

> 1 章で「実行する」と定めた整形（行末空セル除去など）は外さない。外すのは③特殊記法変換のみ。

**残る課題と対応**：本体の非公開メンバ（Parser の `getResult`・一部コンストラクタ、`DataFileFragment` の `names`/`types`/`lengths`/`values`）は、変換ツールの正しいパッケージから直接呼べない。これを越えるため、本体の非公開メンバを同一パッケージから読み plain で返す薄い**抽出アダプタ**を、器のパッケージごとに 1 枚ずつ置く。

| アダプタ | 相乗り先 | 役割 |
|---|---|---|
| `TestCoreReaderAdapter` | `nablarch.test.core.reader` | Parser を空 `interpreters` で `parse → getResult` し、生の器を取り出す。`readFiles`/`readTables`/`readListMap`/`readMessage`/`readSendSyncMessages`/`readHeaders`/`readBlockBodyLines` を提供。MESSAGE 本文は `MessageParser.getDelegate()` から `FixedLengthFile` を取る |
| `TestCoreFileAdapter` | `nablarch.test.core.file` | `DataFileFragment` の `names`/`types`/`lengths`/`values` を読んで plain で返す |

いずれも構造を組み立てず、読み取った値を plain で返すだけ。相乗りはこの 2 枚に閉じる。これにより本体の getter 追加・可視性拡大は不要で、本体は無変更。

### 判断 B：YAML 経路 — 本体の構造解釈を再利用（本体器を空インタープリタで取得）

**検討した選択肢と却下理由**

YAML も本体の読み込み（`YamlLoader` ＋ Builder 群）が構造解釈と値加工（特殊記法解釈・補完・マージ）を一体で行うため、変換ツールは値加工を外して器だけを取り出す必要がある。当初は本体読み込みを「構造マッピング層／値加工層」へ静的に二分割し、専用の中間表現（`Raw*`）を介す案を検討したが、本体に層と型を増やすコストに見合わず却下した（経緯は steering の D-F／D-H）。

**決定**

Excel 経路（判断 A）と対称に、本体の YAML ビルダ（`YamlTableDataBuilder`／`YamlFileBuilder`／`YamlMessageBuilder`）を **空のインタープリタ・デフォルト値補完なし** で配線するアダプタ（`YamlTestCoreAdapter`、`reader` パッケージ相乗り）を変換ツール側に置く。ビルダは `YamlLoader` が返す順序保持 Map を走査して本体の器（`TableData`／`DataFile`／`MessagePool` 本文）を組み立てる処理をそのまま再利用し、空インタープリタにより `${...}`・`${binaryFile:...}`・`null`・`""` は記法のまま運ばれる。構造解釈は本体 1 箇所に集約され、変換ツールは再実装しない。

> **依存の向き**：主軸は NTF 本体。本体の YAML 読み込みは本体基準で設計し本体の器を返す。変換ツールはそれを再利用する側で、依存は変換ツール → 本体の一方向。本体が変換ツールの中間モデルに合わせて設計されることはない。

### 特殊記法の扱い：形式に依存するか否かで分ける

特殊記法には 2 種類あり、扱いが異なる。

- **NTF 独自記法**（`${systemTime}`・`${binaryFile:...}` 等）：形式に依存しない NTF 仕様。Excel・YAML とも本体がテストとして読むときの値加工（インタープリタチェーン）で解釈する。変換ツールはいずれの形式でも（空インタープリタ配線により）解釈せず、記法のまま中間モデルへ運ぶ。
- **形式の構文に属する記法**（クォートによる文字列明示）：形式ごとに担い手が違う。
  - Excel：クォートは NTF 独自の記法で、本体の `QuotationTrimmer` が外す。
  - YAML：クォートは **YAML 標準仕様**であり、YAML ライブラリ（SnakeYAML Engine）が読み込み時に解決する。よって YAML には `QuotationTrimmer` を適用しない（適用すると二重処理になる）。

YAML の値は、数値・null・空白を文字列として保つため、書き出し時に**全値をダブルクォートで囲む**（YAML 標準では `123` は数値、`null` は null 値、前後空白はクォートなしだと脱落するため）。読み込み時は YAML ライブラリがこれを文字列として解決する。これは NTF 仕様として確定。

### 共通：器の中身を読む手段

取り出した器の中身は、`TableData`・`MessagePool` は本体の public getter で読める。`DataFile`／`DataFileFragment` は package-private/protected な内部を、`file` パッケージに相乗りした `TestCoreFileAdapter` が読む。いずれも**本体無変更**（getter 追加・可視性拡大は不要）。

| 器 | 中身を読む手段 |
|---|---|
| `TableData` | `getTableName`／`getColumnNames`／`getValue`（public） |
| `DataFile`／`DataFileFragment` | `TestCoreFileAdapter`（`file` 相乗り）が `names`／`types`／`lengths`／`values` を読む |
| `MessagePool` | FW 制御ヘッダは `getFwHeader`（public）。本文は `FixedLengthFile` として取る |
| LIST_MAP | 戻り値が `List<Map<String,String>>` の素の型 |

テーブル系は構造解析（`TableData.addRow`）の途中で `dbInfo.getColumnType` を要求する。値は文字列のままで型に依存しないが `dbInfo` が null だと読めないため、カラム型を返すだけの**スタブ `DbInfo`** を構成で差し込む。

### 共通：器が正規化する値の原文復元

本体の④構造解析は、テスト実行に必要な正規化を器に施す。変換ツールは原文（作成者の記述）が要るため、正規化される箇所だけ原文を補う。**原文の供給元は形式で異なる**：Excel は器を作る素材である**生行**（`PoiXlsReader` の出力）、YAML は器を作る素材である **`YamlLoader` の順序保持 Map**。いずれも器（構造の権威）と同じ素材から原文を取り、index／キーで器のフィールドへ対応させる。全データタイプを通した結果、取り出し経路で原文が変わるのは次の 3 点のみ（値の大半は無加工で器をそのまま使える）。

| 正規化 | 器の挙動 | Excel の原文復元（生行） | YAML の原文復元（YamlLoader Map） |
|---|---|---|---|
| カラム名・テーブル名の大文字化 | キーを大文字化（値は無損失） | 復元不要（NTF 仕様上カラム名の大小は無意味） | 同左（復元不要） |
| 長さ省略（`-`）フィールド | 値を改行除去・トリムし、長さを実バイト長に上書き | 長さ行のセルが `-`（`ONDEMAND_CALC_FIELD_SIZE`）かで省略を識別し、原文の値・長さは生行から取る | エントリ `records[].fields[].length` を Map 原文から取る（省略は `null`）。値は器（空インタープリタで未加工）から |
| 型表記 | 設計上の型名をフレームワーク表記（`X`/`N`/`B`/`Z`）に変換 | 原文の型は生行の型行から取る | エントリ `records[].fields[].type` を Map 原文から取る |
| LIST_MAP の列順 | 値 Map を `TreeMap` でキーソート | 元の列順は `HeaderLine` が保持＝器から取れる（生行不要） | 器は `TreeMap` で列順を喪失。エントリ先頭行のキー順（`YamlLoader` が記述順保持）から取る |

Excel は生行から**マーカー列（`[...]` 形式のセル）を除外**すると、残セルが器のフィールドと同じ順序・同数で並ぶ（index で 1 対 1 対応）。YAML は `YamlLoader` Map のエントリ列が器（グループ絞り込み済み・FW_HEADER スキップ済み）と同順・同数で対応する（zip で 1 対 1）。いずれも器の断片数と原文側の要素数が食い違えば、誤った原文を静かに充填せず即座に失敗させる（fail-fast）。

### 重複実装を避ける：ロジックの共通化

変換ツールが生行を扱う際、本体と同じ判定を二重に実装すると解釈ズレの温床になる。形式非依存の判定ロジックは本体からユーティリティへ切り出し、本体と変換ツールで共有する（切り出しは private 判定を public ユーティリティへ移すリファクタで、本体の観測挙動を変えない）。

| 共通化するロジック | 本体の現所在 | 共通化 |
|---|---|---|
| マーカー列判定（`[...]` 形式の識別）| `HeaderLine` の private 条件 | ユーティリティへ切り出し共有。除外機構 `ListWrapper` は既に独立 util |
| コメント行・空行判定 | `TestDataParsingTemplate` の判定メソッド | 純粋判定をユーティリティへ切り出し共有 |
| 行末空セル除去 | `NablarchTestUtils.trimTailCopy` | 既に独立 util。そのまま共有 |

行種別（名前行／型行／長さ行／値行）の判定は、本体の状態機械にパース進行と一体で埋め込まれており切り出せない。これは④の器（構造解析の結果）から構造を得て、生行と index 対応させることで、再実装せずに解決する。

### 書き出し（OUT）の整形方針

書き出しは形式の記法規則で定まるが、Excel だけ整形の判断が要る。読み手が違うため方針を分ける。

- **YAML OUT**：AI エージェントが読む前提。機械可読なら足り、記法どおりに書く（全値クォート・インデント程度）。
- **Excel OUT**：人が見て編集する前提。行種別ごとの装飾やレイアウトで読みやすく整える。整形は**設定で指定可能**とし、未設定でも見やすい既定値を用意する。

整形は NTF 仕様上の意味を持たないため中間モデルに乗らず、OUT 時に設定に従って新規付与する。よって Excel → 中間モデル → Excel の往復で元の色・書式は再現されず、設定（またはデフォルト）に従った整形が付く（可逆性の対象外）。

| 設定項目 | デフォルト |
|---|---|
| データタイプ識別行・各種ヘッダ行・マーカーカラムの背景色 | [要確認] 見やすい配色を調査して決定 |
| 列幅 | 各列の値の最大文字数に合わせ自動調整 |
| 罫線 | データブロックの外枠に細線 |
| データブロック間の空行 | 1 行挿入 |

---

## 3. 構造

中間モデルを介する Reader／Writer 構成。図に役割を持たせ、文は補足に絞る。

### 中間モデル

```mermaid
classDiagram
direction TB
class TestDataContainer
class TestDataSection
class TestDataBlock {
  <<sealed>>
  +dataType
  +groupId
  +identifier
}
class FileDataBlock {
  +fileType: FileType
}
class ColumnRowDataBlock {
  <<sealed>>
}
class TableDataBlock
class ListMapBlock
class MessageDataBlock
class RecordLayout
class FieldDef
TestDataContainer "1" --> "*" TestDataSection
TestDataSection "1" --> "*" TestDataBlock
TestDataBlock <|-- FileDataBlock
TestDataBlock <|-- ColumnRowDataBlock
TestDataBlock <|-- MessageDataBlock
ColumnRowDataBlock <|-- TableDataBlock
ColumnRowDataBlock <|-- ListMapBlock
FileDataBlock "1" --> "*" RecordLayout
MessageDataBlock "1" --> "*" RecordLayout
RecordLayout "1" --> "*" FieldDef
```

`TestDataContainer` がテストクラス 1 つ分（Excel は 1 ブック／YAML は 1 ディレクトリ）、`TestDataSection` が読み込み単位（Excel は 1 シート／YAML は 1 ファイル）。その下に、データブロック（`FileDataBlock`／テーブル・LIST_MAP をまとめる `ColumnRowDataBlock`／`MessageDataBlock`）と、レコードレイアウト・フィールド定義がぶら下がる。

### IN（形式 → 中間モデル）

各形式を本体の読み込み（2 章）で読み解き、本体の器を受け取って中間モデルへ組む。Excel・YAML とも `reader` 相乗りアダプタ（`TestCoreReaderAdapter`／`YamlTestCoreAdapter`）を空インタープリタで配線して器を取り出す対称な経路をとる。器が正規化する値は、**Excel は生行（`PoiXlsReader` 出力）から、YAML は `YamlLoader` の順序保持 Map から**原文を補う（2 章）。

```mermaid
classDiagram
direction LR
class TestDataFormatReader {
  <<interface>>
  +read(basePath, resourceName) TestDataContainer
}
class XlsFormatReader
class YamlFormatReader
class TestCoreReaderAdapter {
  <<reader相乗り>>
  +readFiles/readTables/readListMap/readMessage()
  +readSendSyncMessages/readHeaders/readBlockBodyLines()
}
class YamlTestCoreAdapter {
  <<reader相乗り>>
  +readFiles/readTables/readListMap/readMessage/readSendSyncMessages()
  +isResourceExisting/loadRawMap()
}
class TestCoreFileAdapter {
  <<file相乗り>>
  +names/types/lengths/values
}
class ExcelParsers {
  <<本体>> DataFileParser ほか
  +parse() / +getResult()
}
class YamlBuilders {
  <<本体>> YamlLoader + Yaml*Builder（器生成）
}
class StructuredObjects {
  <<本体>> DataFile / TableData / MessagePool
}
XlsFormatReader ..|> TestDataFormatReader
YamlFormatReader ..|> TestDataFormatReader
XlsFormatReader --> TestCoreReaderAdapter : 呼ぶ
XlsFormatReader --> TestCoreFileAdapter : file系の内部値を読む
TestCoreReaderAdapter --> ExcelParsers : 空interpretersを配線しparse→getResult
TestCoreFileAdapter --> StructuredObjects : DataFileFragment内部を読む
ExcelParsers ..> StructuredObjects : 構築
TestCoreReaderAdapter ..> StructuredObjects : 取り出して返す
YamlFormatReader --> YamlTestCoreAdapter : 呼ぶ（器＋loadRawMap 原文）
YamlFormatReader --> TestCoreFileAdapter : file系の内部値を読む
YamlTestCoreAdapter --> YamlBuilders : 空interpretersを配線し器生成
YamlBuilders ..> StructuredObjects : 構築
YamlTestCoreAdapter ..> StructuredObjects : 取り出して返す
XlsFormatReader ..> TestDataContainer : 組み立て
YamlFormatReader ..> TestDataContainer : 組み立て
```

受け取るのはいずれも**本体の器**で、それを変換ツールが中間モデルへ写す。中間モデルは変換ツール内部の表現で、本体には現れない（依存は変換ツール → 本体の一方向）。

経路ごとの要点は 2 章の判断 A・B のとおり。Excel は可視性の壁を越えるため、`nablarch.test.core.reader` に `TestCoreReaderAdapter`（Parser を parse→getResult し構造を取り出す）、`nablarch.test.core.file` に `TestCoreFileAdapter`（`DataFileFragment` の内部値を読む）を相乗りさせ、相乗りの影響をこの 2 枚に局所化する。YAML も対称に、`nablarch.test.core.reader` へ `YamlTestCoreAdapter` を相乗りさせ、本体の Yaml ビルダを空インタープリタで配線して器を取り出す。`YamlFormatReader` は器に加えて `loadRawMap`（`YamlLoader` の順序保持 Map）から原文を補い、`DataFile` 内部値は Excel と同じく `TestCoreFileAdapter` で読む。

### OUT（中間モデル → 形式）

```mermaid
classDiagram
direction LR
class TestDataFormatWriter {
  <<interface>>
  +write(container, path)
}
class YamlFormatWriter
class XlsFormatWriter
class ExcelFormatConfig {
  背景色 / 列幅 / 罫線 / 空行
}
class YamlTestDataValidator {
  +validate(yaml)
}
YamlFormatWriter ..|> TestDataFormatWriter
XlsFormatWriter ..|> TestDataFormatWriter
XlsFormatWriter --> ExcelFormatConfig : 整形設定を参照
YamlFormatWriter --> YamlTestDataValidator : 出力後スキーマ検証
```

`YamlTestDataValidator`（`ValidationError` と対）は YAML OUT 後にスキーマ検証を行うリンターで、不正な YAML が生成された場合は `ValidationError` リストを返す。

`YamlFormatWriter` は記法どおり（全値クォート）、`XlsFormatWriter` は `ExcelFormatConfig`（2 章の整形表。デフォルトを備え上書き可能）を参照して整形付きで書き出す。

### 利用の入口

利用 PJ も開発チームも、同じ入口 `TestDataConverter`（form／to と入出力先を受け、IN→OUT を実行）を使う。`FormatHandler`（`XlsFormatHandler`／`YamlFormatHandler`）がソース探索・IN・OUT 経路の解決を担い、`TestDataConverter` はこれらを介す。

```mermaid
classDiagram
direction LR
class TestDataConverter { +convert(from,to,input,output) }
class FormatHandler { <<interface>> +findSources/read/createWriter/resolveOutputBase/outputPaths() }
class XlsFormatHandler
class YamlFormatHandler
NTF本体TestCode --> TestDataConverter : テストコードから呼ぶ
TestDataConverter --> FormatHandler : IN/OUT経路解決
FormatHandler <|.. XlsFormatHandler
FormatHandler <|.. YamlFormatHandler
TestDataConverter --> TestDataFormatReader : IN
TestDataConverter --> TestDataFormatWriter : OUT
```

| 利用者 | やりたいこと | 呼び方 |
|---|---|---|
| NTF 利用 PJ | 既存 Excel を AI が扱える YAML へ移す（または逆） | `TestDataConverter` を `ConversionRequest`（include／exclude・上書き可否等）とともに呼ぶ。`ConverterFileFilter` / `ConverterPathResolver` がファイル選択・パス解決を担う |
| Nablarch 開発チーム | 本体テストを変えず YAML 経路でも通るか確認 | テストコードが `TestDataConverter` を直接呼び、実行時に Excel を一時 YAML へ変換 |

開発チーム用途では出力先に一時ディレクトリを渡し、変換結果の YAML は git 管理せず実行のたびに生成・破棄する。入口は出力先を引数で受けるだけで、一時／永続を区別しない（後始末はテストコード側の責務）。

---

## 4. 品質担保

品質は「変換しても NTF 仕様上の意味が変わらない」ことに尽きる。粒度の小さい順に 4 段で担保する。

1. **各クラスのユニットテスト**：IN／OUT／中間モデルを単体検証。カバレッジ C0／C1 100% を基準とし分岐はモックで網羅。全データブロック種別（FIXED／VARIABLE／TABLE／LIST_MAP／MESSAGE 系）を網羅し、特に IN で値が未変換（特殊記法が記法のまま）であること、器が正規化する 3 点（長さ省略値・型表記・LIST_MAP 列順）が原文どおり復元されることを確認する。
2. **往復変換の確認**：可逆性の検証。同一形式の往復（Excel→中間→Excel、YAML→中間→YAML）で NTF 仕様上の意味が変わらないこと。意味を持たない情報（色・書式・コメント）は対象外。
3. **本体テストの YAML 変換**：振る舞い不変の担保。`nablarch-testing` の既存 Excel テストを YAML へ変換し**全件 PASS** すること。アサーションは変えず読み込む形式だけを YAML に差し替える。Excel で全件 PASS の既存テストが YAML 経路でも全件 PASS すれば、変換が意味を保っている担保になる。
4. **サンプルアプリでの動作確認**：公式サンプルアプリ（Example 各種＋システム開発ガイドのサンプルプロジェクト）のテストデータをすべて YAML へ変換し、全件 PASS すること。

---

## 5. 開発とバージョン展開

### 開発とリポジトリ分割の手順

リポジトリ分割を見据え、`nablarch-testing` 内で分割先と同じ境界のパッケージとして分離開発する。

1. `nablarch-testing` 内で分割先と同じ境界でパッケージを分けて開発
2. 品質担保 3（本体テストの YAML 変換が全件 PASS）まで完了
3. 有識者レビュー
4. 承認後、分割先リポジトリ（nablarch-testing-yaml／nablarch-testing-converter）へ分割
5. 分割後、品質担保 4（サンプルアプリ確認）を実施

### 過去バージョンへの展開

機能追加対象は v6 だが、過去展開も見込む。**全バージョンのリリースノートを確認した範囲**での判断を以下に示す（Nablarch は後方互換に影響する変更を API・動的挙動ともリリースノートに記録する方針のため、この確認で判定できる）。

- **v6（機能追加対象）**：変換ツールが依存する本体 API・読み込み構造解析に、後方互換を壊す変更は確認されなかった。v6 の `nablarch-testing` は `2.x` 系で、主な変更は Jetty 12 化・Java 21 対応・公開 API 追加にとどまり読み込み構造解析に影響しない。機能追加は阻害なく成立する。
- **v5・v1.4〜v1.2（過去展開）**：YAML 対応はフォークで作成（対象バージョンに合わせ JDK と NTF バージョンを変える）。変換ツールは、依存する本体 API に後方互換を壊す変更が確認されなかったため、そのまま再利用できる。

過去バージョンでは本体の読み込み挙動そのものが次の境界で切り替わる。いずれも本体側の差で、変換ツールは本体の構造解析を再利用するため自動追従する（変換ツール固有の対応は不要）。

| 挙動差 | 境界 | 内容 |
|---|---|---|
| 空行の扱い | NTF 1.1 系で修正 | 全カラム空文字レコードを読み飛ばす不具合を、空行を明示記述できるよう修正。境界より前は空エントリの保持挙動が異なる |
| xlsx 形式対応 | NTF 1.2.0 で追加 | xls に加え xlsx 対応（Apache POI 入替）。境界より前は xlsx を読めない |
| 空文字→null 変換 | dataformat（v5 で明確化）| 可変長／固定長読込時、空文字を既定で null に変換（`convertEmptyToNull`）。設定で無効化可 |