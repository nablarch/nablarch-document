.. _ntf_testdata_messaging:

==========================
メッセージングテストデータ
==========================

テストデータは Excel または YAML ファイルで記述できる。

メッセージングテストデータは ``MESSAGE`` / ``EXPECTED_REQUEST_*_MESSAGES`` / ``RESPONSE_*_MESSAGES`` の各データブロックで記述する。

----------------------------
sendSyncTestData の配置規則
----------------------------

テストデータファイルは ``sendSyncTestData/{requestId}/message`` というパスに配置する（末尾の ``message`` は固定のパスセグメント）。

- **Excel**: ``MESSAGE=sendSyncTestData/{requestId}/message`` をデータブロック識別子として記述する。
- **YAML**: ``messages:`` の ``id:`` に ``sendSyncTestData/{requestId}/message`` を指定する。

記述例
======

Excelの場合
-----------

.. code-block:: text

    MESSAGE=sendSyncTestData/REQ001/message
    | no | errorMode | field1 | field2 |
    |    | 半角      | 半角   | 半角   |
    |    | 10        | 10     | 10     |
    | 1  |           | value1 | value2 |
    | 2  |           | value3 | value4 |

YAMLの場合
----------

.. code-block:: yaml

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

- ``no`` 列の値は送信順序と一致させること。
- ``errorMode`` に ``errorMode:timeout`` を指定するとタイムアウトエラー、 ``errorMode:msgException`` を指定すると例外エラーのシミュレーションとなる。どちらを指定した場合も他フィールドはパース対象外となる。
- N 回送信する場合はヘッダ件数とボディ件数をともに N 件ずつ記述する。

--------------------------
FW 制御ヘッダフィールド
--------------------------

.. note::

  **適用範囲**: ``fw_header:`` マップは ``messages`` （MESSAGE: MockMessaging 経路の要求/応答電文）でのみ使用する。 ``expected_request_header_messages`` / ``expected_request_body_messages`` / ``response_header_messages`` / ``response_body_messages`` の4種では使用しない。これらは ``requestId`` 等のヘッダフィールドも含めて ``records`` の ``fields:`` / ``rows:`` にフィールド単位（型・長さつき）で記述する。

FW 制御ヘッダのフィールド名はプロジェクトごとに異なる。フレームワーク標準では4種が既定値だが固定ではなく、 ``SystemRepository`` の ``reader.fwHeaderfields`` キーでプロジェクトが任意の名前に変更できる（例: ``reader.fwHeaderfields=requestId,addHeader`` ）。

既定値の例: ``requestId`` , ``userId`` , ``resendFlag`` , ``resultCode``

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 形式
     - 記述方法
   * - Excel
     - フィールド名称行（ ``no`` 行）より前に ``| フィールド名 | 値 |`` （ディレクティブと同じ「名前｜値」形式）
   * - YAML
     - ``fw_header:`` マップ（キー: 値）。キー名は固定でなく任意（ ``reader.fwHeaderfields`` 設定に合わせる）

- **``directives:`` （ ``text-encoding`` 等）と ``fw_header:`` （ ``requestId`` 等）は別キーである。** Excel ではどちらも「名前｜値」の行だが、FW 制御ヘッダはフレームワークが電文ヘッダとして分離して扱うため YAML では区別する。
- **``fw_header:`` のキーはすべて FW 制御ヘッダとして扱われる。** ランタイムは ``fw_header:`` マップをそのまま FW ヘッダとして使い、 ``reader.fwHeaderfields`` でフィルタリングして取り捨てることはしない（記述したものが黙って消えない）。
- 電文ボディのフィールドは ``records:`` の ``fields:`` / ``rows:`` に記述する。

記述例（MESSAGE セクション）
============================

受信電文と応答電文を定義するケースを以下に示す。

Excelの場合
-----------

.. code-block:: text

    MESSAGE=requestMessages
    | text-encoding | Windows-31J |         |        |
    | requestId     | hoge        |         |        |
    | userId        | moge        |         |        |
    |               | ユーザ名    | 備考    | FILLER |
    |               | 全角        | 全角    | 半角   |
    |               | 50          | 200     | 252    |
    | 1             | 電文太郎    | 特筆なし |       |
    | 2             |             | ユーザ名が空欄なのでエラーが発生します。 | |

    MESSAGE=responseMessages
    | no | 処理結果コード | 会員ID     | FILLER |
    |    | X              | X          | X      |
    |    | 2              | 10         | 490    |
    | 1  | 00             | 1234567890 |        |
    | 2  | 01             |            |        |

YAMLの場合
----------

.. code-block:: yaml

    messages:
      - id: requestMessages
        directives:
          text-encoding: Windows-31J
        fw_header:
          requestId: hoge
          userId: moge
        records:
          - record_type: default
            fields:
              - {name: ユーザ名, type: 全角, length: 50}
              - {name: 備考,     type: 全角, length: 200}
              - {name: FILLER,   type: 半角, length: 252}
            rows:
              - ["電文太郎", "特筆なし", ""]
              - ["", "ユーザ名が空欄なのでエラーが発生します。", ""]
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

- ``record_type`` の値はフレームワーク内部で常に ``"default"`` に置き換えられる。任意の値を記述できる（ ``FW_HEADER`` のような予約値はない）。
- Excel のフィールド名称行の先頭セルは空にすること（Excel 固有）。
- ``no`` 列（先頭列）はフレームワークが除去する。データとして保存されない。

------------------------------------------
HEADER / BODY MESSAGES の構造と件数制約
------------------------------------------

``EXPECTED_REQUEST_HEADER_MESSAGES`` と ``EXPECTED_REQUEST_BODY_MESSAGES`` のエントリ数（rows 合計）は一致が必須である（不一致時はエラー）。

HTTP 同期応答メッセージ（ ``response_body_messages`` ）の各データエントリは文字列長が同一である必要がある。

記述例（要求電文・応答電文の期待値）
=====================================

バッチリクエスト単体テストで電文の送受信をテストするケースを以下に示す。

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description      | expectedStatusCode | diConfig                              | requestPath | userId     | expectedMessage | responseMessage |
    | 1  | 電文送受信テスト | 0                  | batch-test-component-configuration.xml | BM21AA0106  | batch_user | case1           | res_case1       |

    EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM21AA0104_01
    | text-encoding | ms932     |      |
    | no            | requestId |      |
    |               | 半角      |      |
    |               | 20        |      |
    | 1             | RM21AA0104_01 |  |

YAMLの場合
----------

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "電文送受信テスト"
            expectedStatusCode: "0"
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

- ``expectedMessage`` カラムには要求電文の groupId、 ``responseMessage`` カラムには応答電文の groupId を指定する。
- YAML では ``expected_request_header_messages:`` の ``group_id:`` が ``testShots`` の ``expectedMessage`` カラムに対応する。
- ``id:`` はリクエスト ID（フォーマット定義ファイルの解決に使われる）。

--------------------
ステータスコード
--------------------

ステータスコードカラムがない場合はデフォルト値 ``"200"`` が使用される。Excel・YAML 両方で共通である。

記述例
======

Excelの場合
-----------

.. code-block:: text

    RESPONSE_BODY_MESSAGES=REQ001
    | no | body    |
    |    | 半角    |
    |    | 10      |
    | 1  | RESULT_OK |

YAMLの場合
----------

.. code-block:: yaml

    response_body_messages:
      - id: REQ001
        records:
          - record_type: DATA
            fields:
              - {name: body, type: 半角, length: 10}
            rows:
              - ["RESULT_OK"]

-----------------
その他の仕様
-----------------

no 行（フィールド名称行）と errorMode
======================================

**電文の行構造**: ディレクティブ群・FW 制御ヘッダの後、 ``no`` で始まる行がフィールド名称行である。以降、データ型行・フィールド長行・データ行が続く。

- **Excel**: フィールド名称行の先頭セルに ``no`` を記述する。データ行の先頭セル（ ``no`` カラム）はフレームワークが除去しデータとして保存しない。
- **YAML**: フィールド名称は ``fields:`` 、データは ``rows:`` に記述する（ ``no`` カラム自体は YAML の構造に現れない）。

**errorMode（RESPONSE 系・MockMessaging 経路のみ）**:

- ``response_header_messages`` / ``response_body_messages`` で、データ行の先頭値が ``errorMode:timeout`` または ``errorMode:msgException`` の場合、そのエントリは送受信エラーをシミュレートするマーカーとして扱われる。
- errorMode 行は ``fw_header:`` の分離とは独立した別の仕組みである。
- ``RequestTestingSendSyncSupport`` 経路（GroupMessageParser）では errorMode は使用されない。

複数回送信
==========

N 回送信する場合は、ヘッダ件数とボディ件数をともに N 件ずつ記述する。同一リクエスト ID で複数回送信する場合は ``no`` 値を変えて連続記述し、送信順序と ``no`` 値を一致させる。

フォーマット定義ファイルの命名規則
====================================

- 応答電文: ``{requestId}_RECEIVE``
- 要求電文: ``{requestId}_SEND``

アサート方式の切り替え
======================

``SystemRepository`` の ``messaging.assertAsMapFileType`` キーの設定値に応じてアサート方式が切り替わる。未設定時のデフォルトは ``"Fixed"`` 形式（項目単位アサート）。
