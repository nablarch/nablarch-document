# NTF テストデータ解説書 — 記述例（メッセージングテストデータ）

<a name="messaging"></a>

メッセージング系データブロック（MESSAGE / SendSync 期待値 / sendSyncTestData 配置 / ステータスコードデフォルト）の Excel・YAML 記法をケースごとに引く。各ケースとも Excel と YAML の対応例を並べ、末尾に制約・補足を示す。

## 7.1 MESSAGE セクション（メッセージ送受信）

受信電文と応答電文を定義するケース。実物のデータは `MessageParserTest.xls` の `testParse` シートを参照。

### Excel

| MESSAGE=requestMessages | | | |
|---|---|---|---|
| text-encoding | Windows-31J | | |
| requestId | hoge | | |
| userId | moge | | |
| | ユーザ名 | 備考 | FILLER |
| | 全角 | 全角 | 半角 |
| | 50 | 200 | 252 |
| 1 | 電文太郎 | 特筆なし | |
| 2 | | ユーザ名が空欄なのでエラーが発生します。 | |

| MESSAGE=responseMessages | | | |
|---|---|---|---|
| no | 処理結果コード | 会員ID | FILLER |
| | X | X | X |
| | 2 | 10 | 490 |
| 1 | 00 | 1234567890 | |
| 2 | 01 | | |

### YAML

```yaml
messages:
  - id: requestMessages
    directives:
      text-encoding: Windows-31J     # ディレクティブ
    fw_header:                        # FW制御ヘッダ（任意キーのマップ）
      requestId: hoge
      userId: moge
    records:
      - record_type: default
        fields:
          - {name: ユーザ名, type: 全角, length: 50}
          - {name: 備考,     type: 全角, length: 200}
          - {name: FILLER,   type: 半角, length: 252}
        rows:
          - ["電文太郎", "特筆なし",                          ""]
          - ["",         "ユーザ名が空欄なのでエラーが発生します。", ""]
  - id: responseMessages
    records:
      - record_type: default
        fields:
          - {name: 処理結果コード, type: 半角, length: 2}
          - {name: 会員ID,         type: 半角, length: 10}
          - {name: FILLER,         type: 半角, length: 490}
        rows:
          - ["00", "1234567890", ""]
          - ["01", "",           ""]
```

### 制約・補足

- ディレクティブ行（`text-encoding` など）はフィールド定義より前に記述する
- Excel のフィールド名称行の先頭セルは空にする（Excel 固有）
- `no` 列（先頭列）はフレームワークが除去する。データとして保存されない
- `record_type` の値はフレームワーク内部で `"default"` に置き換えられる。任意の値を記述できる（`FW_HEADER` のような予約値はない。FW制御ヘッダは `fw_header:` マップに記述する）

---

## 7.2 要求電文・応答電文の期待値（SendSync メッセージング）

バッチリクエスト単体テストで電文の送受信をテストするケース。実物のデータは `RequestTestingSendSyncSupportTest.xls` を参照。

### Excel

| LIST_MAP=testShots | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|
| no | description | expectedStatusCode | setUpTable | expectedTable | expectedLog | diConfig | requestPath | userId | expectedMessage | responseMessage |
| 1 | 電文送受信テスト | 0 | | | | batch-test-component-configuration.xml | BM21AA0106 | batch_user | case1 | res_case1 |

| EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM21AA0104_01 | | | |
|---|---|---|---|
| text-encoding | ms932 | | |
| no | requestId | | |
| | 半角 | | |
| | 20 | | |
| 1 | RM21AA0104_01 | | |

### YAML

```yaml
list_maps:
  - id: testShots
    rows:
      - no: "1"
        description: "電文送受信テスト"
        expectedStatusCode: "0"
        setUpTable: ""
        expectedTable: ""
        expectedLog: ""
        diConfig: "batch-test-component-configuration.xml"
        requestPath: "BM21AA0106"
        userId: "batch_user"
        expectedMessage: "case1"
        responseMessage: "res_case1"

expected_request_header_messages:
  - group_id: case1
    id: RM21AA0104_01
    directives:
      text-encoding: ms932
    records:
      - record_type: default
        fields:
          - {name: requestId, type: 半角, length: 20}
        rows:
          - ["RM21AA0104_01"]
```

### 制約・補足

- `expectedMessage` カラムには要求電文の groupId、`responseMessage` カラムには応答電文の groupId を指定する
- YAML では `expected_request_header_messages:` の `group_id:` が `testShots` の `expectedMessage` カラムに対応する
- `id:` はリクエスト ID（フォーマット定義ファイルの解決に使われる）
- ヘッダとボディのエントリ数（rows 合計）は一致が必須

---

## 7.3 sendSyncTestData の配置規則

テストデータファイルを `sendSyncTestData/{requestId}/message` に配置するケース。

### Excel

| MESSAGE=sendSyncTestData/REQ001/message | | | |
|---|---|---|---|
| no | errorMode | field1 | field2 |
| 1 | | value1 | value2 |
| 2 | | value3 | value4 |

### YAML

```yaml
messages:
  - id: sendSyncTestData/REQ001/message
    records:
      - record_type: DATA
        fields:
          - {name: no,        type: 半角, length: 2}
          - {name: errorMode, type: 半角, length: 10}
          - {name: field1,    type: 半角, length: 10}
          - {name: field2,    type: 半角, length: 10}
        rows:
          - ["1", "",        "value1", "value2"]
          - ["2", "",        "value3", "value4"]
```

### 制約・補足

- `MESSAGE=sendSyncTestData/{requestId}/message` というパスで配置する
- `no` 列の値は送信順序と一致させる
- `errorMode` に `errorMode:timeout` を指定するとタイムアウトエラー、`errorMode:msgException` を指定すると例外エラーのシミュレーションになる。どちらを指定した場合も他フィールドはパース対象外になる
- N 回送信する場合はヘッダ件数とボディ件数をともに N 件ずつ記述する

---

## 7.4 ステータスコードのデフォルト値

HTTP 同期応答テストでステータスコードカラムを省略するケース。

### Excel

| RESPONSE_BODY_MESSAGES=REQ001 | | |
|---|---|---|
| no | body | |
| | 半角 | |
| | 10 | |
| 1 | RESULT_OK | |

### YAML

```yaml
response_body_messages:
  - id: REQ001
    records:
      - record_type: DATA
        fields:
          - {name: body, type: 半角, length: 10}
        rows:
          - ["RESULT_OK"]
```

### 制約・補足

- ステータスコード列がない場合、実行時にデフォルト値 `"200"` が使用される
