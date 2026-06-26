# NTF テストデータ解説書 — 記述例（特殊値・ディレクティブ・ヘッダ）

特殊値・インタープリタ、ファイルディレクティブ、ヘッダ／コメント／空エントリの Excel・YAML 記法を項目ごとに引く。各項目とも Excel と YAML の対応例を並べ、末尾に制約を示す。

<a name="datetime"></a>

## 8. 特殊値・インタープリタ

### 8.1 日付型・Timestamp・特殊値

`EXPECTED_TABLE` で日付・タイムスタンプ・NULL・システム日時を使うケース。実物のデータは `BasicTestDataParserTest.xls` の `convertedValues` シートを参照。

#### Excel

| EXPECTED_TABLE=SCHEDULE | | | |
|---|---|---|---|
| ID | EVENT_NAME | START_DATE | CREATED_AT |
| 1 | 会議 | 2024-01-15 | 2024-01-01 09:00:00.0 |
| 2 | NULLテスト | NULL | NULL |
| 3 | システム時刻 | ${systemTime} | ${systemTime} |
| 4 | 更新時刻 | ${updateTime} | ${setUpTime} |

#### YAML

```yaml
expected_tables:
  - table: SCHEDULE
    rows:
      - ID: "1"
        EVENT_NAME: "会議"
        START_DATE: "2024-01-15"
        CREATED_AT: "2024-01-01 09:00:00.0"
      - ID: "2"
        EVENT_NAME: "NULLテスト"
        START_DATE: null
        CREATED_AT: null
      - ID: "3"
        EVENT_NAME: "システム時刻"
        START_DATE: "${systemTime}"
        CREATED_AT: "${systemTime}"
      - ID: "4"
        EVENT_NAME: "更新時刻"
        START_DATE: "${updateTime}"
        CREATED_AT: "${setUpTime}"
```

#### 制約

- `NULL` 文字列は `NullInterpreter` が Java null に変換する。大文字小文字不問（`null`・`Null` も同様）。YAML ではアンクォートの `null` で記述し、`"null"` とクォートすると文字列として格納される
- `${systemTime}` は完全一致のみ変換される。文字列中に埋め込むには `CompositeInterpreter` との組み合わせが必要
- `java.sql.Timestamp` 型カラムの期待値は末尾 `.0` が必須（`"2024-01-01 09:00:00.0"`）。末尾 `.0` がないとアサートが失敗する

> [要確認] `${updateTime}`・`${setUpTime}`（行 4）が解決する値の定義が本ファイルにない。`${systemTime}` との違いと対応するインタープリタを確認のうえ補う。

---

### 8.2 QuotationTrimmer によるスペース値明示記法

空白値やダブルクォート文字を明示して記述するケース。

#### Excel

| EXPECTED_TABLE=ITEM | | |
|---|---|---|
| ID | NAME | MEMO |
| 1 | " " | """ |

#### YAML

```yaml
expected_tables:
  - table: ITEM
    rows:
      - ID: "1"
        NAME: " "
        MEMO: "\""
```

#### 制約

- Excel: `" "` → 半角スペース1文字、`"""` → ダブルクォート1文字。半角または全角ダブルクォートで前後が囲まれた場合のみ外側1層を除去する
- YAML: `" "` でスペース1文字。ダブルクォート文字は `"\""` または `'"'` で記述する

---

### 8.3 バイナリデータ

BLOB カラムにバイナリデータを記述するケース。

#### Excel

| SETUP_TABLE=FILE_TABLE | | |
|---|---|---|
| FILE_ID | FILE_DATA | |
| 001 | 0xCAFEBABE | |
| 002 | ${binaryFile:testdata.bin} | |

#### YAML

```yaml
setup_tables:
  - table: FILE_TABLE
    rows:
      - FILE_ID: "001"
        FILE_DATA: "0xCAFEBABE"
      - FILE_ID: "002"
        FILE_DATA: "${binaryFile:testdata.bin}"
```

#### 制約

- `0x` プレフィクス付き16進数でバイナリ値を記述する。`0x` がない場合は文字列としてエンコードされる
- `${binaryFile:パス}` でファイル内容をバイナリ読み込みして HexString に変換する

---

<a name="directive"></a>

## 9. ディレクティブ

### 9.1 固定長ファイルのディレクティブ

エンコーディングとゾーン10進数の符号ニブルを指定するケース。

#### Excel

| SETUP_FIXED=input/data.dat | | |
|---|---|---|
| text-encoding | MS932 | |
| positive-zone-sign-nibble | C | |
| DATA | USER_ID | AMOUNT |
| | X | Z |
| | 10 | 10 |
| | 001 | 5000 |

#### YAML

```yaml
setup_files:
  - path: input/data.dat
    type: fixed
    directives:
      text-encoding: MS932
      positive-zone-sign-nibble: C
    records:
      - record_type: DATA
        fields:
          - {name: USER_ID, type: X, length: 10}
          - {name: AMOUNT,  type: Z, length: 10}
        rows:
          - ["001", "5000"]
```

#### 制約

- Excel のディレクティブ行は「キー | 値」の2セルで記述する。YAML は `directives:` オブジェクトの `key: value` 形式
- `file-type` と `record-length` はフレームワークが自動設定するため通常は記述不要
- 無効なディレクティブキーを指定すると `IllegalArgumentException` がスローされる

---

### 9.2 可変長ファイルのディレクティブ

タブ区切り・CRLF 改行のファイルを扱うケース。

#### Excel

| SETUP_VARIABLE=input/data.tsv | | |
|---|---|---|
| field-separator | \t | |
| record-separator | CRLF | |
| DATA | FIELD1 | FIELD2 |
| | X | X |
| | value1 | value2 |

#### YAML

```yaml
setup_files:
  - path: input/data.tsv
    type: variable
    directives:
      field-separator: "\\t"
      record-separator: CRLF
    records:
      - record_type: DATA
        fields:
          - {name: FIELD1, type: X}
          - {name: FIELD2, type: X}
        rows:
          - ["value1", "value2"]
```

#### 制約

- タブ文字の記法が形式で異なる。Excel セルには `\t`（バックスラッシュ + t の2文字）を入力し、フレームワークがタブ文字（0x09）に変換する。YAML は `"\\t"` と記述する（YAML の `\t` は実際のタブ文字になるためバックスラッシュをエスケープする）
- `record-separator` には `NONE` / `CR` / `LF` / `CRLF` または任意リテラル文字列が有効
- `field-separator` は1文字のみ有効。2文字以上は `IllegalArgumentException` がスローされる

---

<a name="header-comment"></a>

## 10. ヘッダ・コメント・空エントリ

### 10.1 コメントとマーカーカラム

#### Excel

| SETUP_TABLE=TEST_TABLE | | | | |
|---|---|---|---|---|
| // この行はコメントです | | | | |
| [no] | PK_COL1 | PK_COL2 | NUMBER_COL | [desc] |
| 1 | 0000000001 | AB | 100 | テスト1 |
| // この行もスキップされます | | | | |
| 2 | 0000000002 | CD | 200 | テスト2 |

#### YAML

```yaml
setup_tables:
  - table: TEST_TABLE
    rows:
      # この行はコメントです（YAML の # 構文）
      - "[no]": "1"
        PK_COL1: "0000000001"
        PK_COL2: "AB"
        NUMBER_COL: "100"
        "[desc]": "テスト1"
      - "[no]": "2"
        PK_COL1: "0000000002"
        PK_COL2: "CD"
        NUMBER_COL: "200"
        "[desc]": "テスト2"
```

#### 制約

- Excel: `//` で始まる行は丸ごとスキップされる（テスト実行に影響しない）。**行内コメント**は先頭以外の要素が `//` で始まる場合にその要素以降が切り捨てられる（Excel 固有）
- YAML: 標準のコメント構文（`#`）を使う。行末コメントも可（`NUMBER_COL: "100"  # 数値カラム`）
- `[no]`・`[desc]` のように角括弧で囲んだカラムはマーカーカラムで、DB 操作から除外される。YAML ではダブルクォートで囲む（`"[no]"`）

---

### 10.2 空エントリのスキップ

全要素が null または空文字のエントリは読み飛ばされる。

#### Excel

| SETUP_TABLE=USER | | |
|---|---|---|
| USER_ID | NAME | |
| 001 | 山田太郎 | |
| | | |
| 002 | 鈴木花子 | |

#### YAML

```yaml
setup_tables:
  - table: USER
    rows:
      - USER_ID: "001"
        NAME: "山田太郎"
      # 空行はここには書かない（YAML にはそもそも空エントリの概念がない）
      - USER_ID: "002"
        NAME: "鈴木花子"
```

#### 制約

- Excel: 全セルが空の行は自動的にスキップされる
- YAML: キーを省略するだけのため空エントリを記述する機会はほとんどない。空行を挿入しても無視される

---

<a name="db-assert"></a>

## 11. DB アサート

> テーブルアサートの記法・省略カラムの扱い・主キー突合は [ntf-testdata-doc-examples-table.md](ntf-testdata-doc-examples-table.md#table-data) と本体仕様（[ntf-testdata-doc.md](ntf-testdata-doc.md) 5.4）に詳しい。ここでは DB アサート固有の挙動だけを示す。

### 11.1 テーブルアサート（順序不問・主キー突合）

`EXPECTED_TABLE` は記述順と DB の格納順が違っても、主キーで突合して比較する。下記は順序が違っても成功するケース。

#### Excel

| EXPECTED_TABLE=USER | | |
|---|---|---|
| USER_ID | NAME | |
| 001 | 山田太郎 | |
| 002 | 鈴木花子 | |

#### YAML

```yaml
expected_tables:
  - table: USER
    rows:
      - USER_ID: "001"
        NAME: "山田太郎"
      - USER_ID: "002"
        NAME: "鈴木花子"
```

### 11.2 EXPECTED_COMPLETE_TABLE（省略カラムにデフォルト値補完）

省略したカラムにデフォルト値を補完してから比較する。

#### YAML

```yaml
expected_complete_tables:
  - table: USER
    rows:
      - USER_ID: "001"
        NAME: "山田太郎"
        # AGE など省略したカラムはデフォルト値（数値型なら "0"）で補完される
```
