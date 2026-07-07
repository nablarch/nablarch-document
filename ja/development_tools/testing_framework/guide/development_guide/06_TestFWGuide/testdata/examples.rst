.. _ntf_testdata_examples:

============================
テストデータの記述例
============================

テストデータは Excel または YAML ファイルで記述できる。

ここでは用途別の記述例を Excel と YAML の対比形式で示す。仕様の詳細は :ref:`ntf_testdata` 以降の各節を参照。

.. contents::
   :local:
   :depth: 2

--------------------------
テストデータ全体像の例
--------------------------

バッチ処理のリクエスト単体テストの例を以下に示す。1ファイルにテストケース・セットアップ・検証が共存する。

Excelの場合
-----------

各データブロックはシート先頭のラベルで種別が決まる。

.. code-block:: text

    LIST_MAP=testShots
    | no | description        | expectedStatusCode | setUpTable | expectedTable | setUpFile | expectedFile | diConfig                                   | requestPath      | userId | expectedLog |
    | 1  | 正しく更新されます | 0                  | default    | default       |           |              | nablarch/test/core/batch/BatchSample.xml   | DBtoDBBatchSample | test  | expectedLog |

    SETUP_TABLE=ORDER_HEADER
    | ORDER_ID | ITEM_COUNT | REMARKS    |
    | 10001    | 10         | 通常注文   |
    | 10002    | 20         | まとめ買い |

    EXPECTED_TABLE=ORDER_HEADER
    | ORDER_ID | ITEM_COUNT | REMARKS    | UPDATE_DATE              |
    | 10001    | 11         | 通常注文   | 2010-09-13 12:34:56.0    |
    | 10002    | 21         | まとめ買い | 2010-09-13 12:34:56.0    |

    LIST_MAP=expectedLog
    | message          | logLevel |
    | 注文ID[10001]    | INFO     |
    | 注文ID[10002]    | INFO     |

- 種別はブロック先頭のラベルで決まる。``LIST_MAP=testShots`` がテストケース定義、``SETUP_TABLE`` がセットアップ、``EXPECTED_TABLE`` が検証、``LIST_MAP=expectedLog`` が期待ログである。

YAMLの場合
----------

種別はトップレベルキーで決まる。

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正しく更新されます"
            expectedStatusCode: "0"
            setUpTable: "default"
            expectedTable: "default"
            setUpFile: ""
            expectedFile: ""
            diConfig: "nablarch/test/core/batch/BatchSample.xml"
            requestPath: "DBtoDBBatchSample"
            userId: "test"
            expectedLog: "expectedLog"
      - id: expectedLog
        rows:
          - message: "注文ID[10001]"
            logLevel: "INFO"
          - message: "注文ID[10002]"
            logLevel: "INFO"

    setup_tables:
      - table: ORDER_HEADER
        rows:
          - ORDER_ID: "10001"
            ITEM_COUNT: "10"
            REMARKS: "通常注文"
          - ORDER_ID: "10002"
            ITEM_COUNT: "20"
            REMARKS: "まとめ買い"

    expected_tables:
      - table: ORDER_HEADER
        rows:
          - ORDER_ID: "10001"
            ITEM_COUNT: "11"
            REMARKS: "通常注文"
            UPDATE_DATE: "2010-09-13 12:34:56.0"
          - ORDER_ID: "10002"
            ITEM_COUNT: "21"
            REMARKS: "まとめ買い"
            UPDATE_DATE: "2010-09-13 12:34:56.0"

- 種別はトップレベルキーで決まる。``list_maps:`` の ``id: testShots`` がテストケース定義、``setup_tables:`` がセットアップ、``expected_tables:`` が検証である。
- 同一ファイル内に ``list_maps:`` の複数エントリを並べることができる（YAML はトップレベルキーの重複不可のため、リスト形式で記述する）。

------------------------------------
グループIDを使った記述例
------------------------------------

テストケースごとに異なるセットアップ・検証データを使い分ける例を以下に示す。

Excelの場合
-----------

グループIDはセクションラベルの ``[...]`` で表す。

.. code-block:: text

    LIST_MAP=testShots
    | no | description | expectedStatusCode | setUpTable | expectedTable |
    | 1  | 正常注文    | 0                  | case01     | case01        |
    | 2  | 大量注文    | 0                  | case02     | case02        |

    SETUP_TABLE[case01]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 1001     | P-001        | 5        | 1500       |

    EXPECTED_TABLE[case01]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 1001     | P-001        | 5        | 1500       |

    SETUP_TABLE[case02]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 2001     | P-003        | 100      | 500        |
    | 2001     | P-004        | 200      | 300        |

    EXPECTED_TABLE[case02]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 2001     | P-003        | 100      | 500        |
    | 2001     | P-004        | 200      | 300        |

YAMLの場合
----------

グループIDは各セクションの ``group_id`` キーで表す。

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正常注文"
            expectedStatusCode: "0"
            setUpTable: "case01"
            expectedTable: "case01"
          - no: "2"
            description: "大量注文"
            expectedStatusCode: "0"
            setUpTable: "case02"
            expectedTable: "case02"

    setup_tables:
      - group_id: case01
        table: ORDER_DETAIL
        rows:
          - ORDER_ID: "1001"
            PRODUCT_CODE: "P-001"
            QUANTITY: "5"
            UNIT_PRICE: "1500"
      - group_id: case02
        table: ORDER_DETAIL
        rows:
          - ORDER_ID: "2001"
            PRODUCT_CODE: "P-003"
            QUANTITY: "100"
            UNIT_PRICE: "500"
          - ORDER_ID: "2001"
            PRODUCT_CODE: "P-004"
            QUANTITY: "200"
            UNIT_PRICE: "300"

    expected_tables:
      - group_id: case01
        table: ORDER_DETAIL
        rows:
          - ORDER_ID: "1001"
            PRODUCT_CODE: "P-001"
            QUANTITY: "5"
            UNIT_PRICE: "1500"
      - group_id: case02
        table: ORDER_DETAIL
        rows:
          - ORDER_ID: "2001"
            PRODUCT_CODE: "P-003"
            QUANTITY: "100"
            UNIT_PRICE: "500"
          - ORDER_ID: "2001"
            PRODUCT_CODE: "P-004"
            QUANTITY: "200"
            UNIT_PRICE: "300"

------------------------------
testShots の記述例
------------------------------

処理方式別の ``testShots`` 記述例を以下に示す。

ウェブアプリケーション（HttpRequestTestSupport）
=================================================

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description  | isValidToken | expectedStatusCode | forwardUri | context    |
    | 1  | 正常ケース   | 0            | 200                | /success   | context001 |
    | 2  | 認証エラー   | 0            | 400                | /error     | context002 |

    LIST_MAP=context001
    | REQUEST_ID | USER_ID | HTTP_METHOD |
    | REQ_001    | user001 | POST        |

YAMLの場合
----------

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正常ケース"
            isValidToken: "0"
            expectedStatusCode: "200"
            forwardUri: "/success"
            context: "context001"
          - no: "2"
            description: "認証エラー"
            isValidToken: "0"
            expectedStatusCode: "400"
            forwardUri: "/error"
            context: "context002"
      - id: context001
        rows:
          - REQUEST_ID: "REQ_001"
            USER_ID: "user001"
            HTTP_METHOD: "POST"

バッチ処理（BatchRequestTestSupport）
======================================

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description        | expectedStatusCode | diConfig                                   | requestPath        | userId | setUpFile |
    | 1  | 正しく更新されます | 0                  | nablarch/test/core/batch/BatchSample.xml   | DBtoDBBatchSample  | test   |           |
    | 2  | 入力ファイルあり   | 0                  | nablarch/test/core/batch/BatchSample.xml   | FileToFileBatchSample | test | case2   |

YAMLの場合
----------

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正しく更新されます"
            expectedStatusCode: "0"
            diConfig: "nablarch/test/core/batch/BatchSample.xml"
            requestPath: "DBtoDBBatchSample"
            userId: "test"
            setUpFile: ""
          - no: "2"
            description: "入力ファイルあり"
            expectedStatusCode: "0"
            diConfig: "nablarch/test/core/batch/BatchSample.xml"
            requestPath: "FileToFileBatchSample"
            userId: "test"
            setUpFile: "case2"

メッセージング（MessagingRequestTestSupport）
=============================================

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description      | expectedStatusCode | diConfig                              | requestPath | userId     | expectedMessage | responseMessage |
    | 1  | 電文送受信テスト | 0                  | batch-test-component-configuration.xml | BM21AA0106 | batch_user | case1           | res_case1       |

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

エンティティバリデーション（EntityTestSupport）
================================================

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | title     | expectedMessageId1 | propertyName1 |
    | 必須チェック | errors.required  | userName      |

YAMLの場合
----------

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - title: "必須チェック"
            expectedMessageId1: "errors.required"
            propertyName1: "userName"

----------------------------
テーブルデータの記述例
----------------------------

SETUP_TABLE（初期データ投入）
=============================

Excelの場合
-----------

.. code-block:: text

    SETUP_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | RATE | PROFILE          | PHOTO                         |
    | 0000000101 | 山田太郎 | 1    | 85000 | 1.5  | ゴールド会員です | ${binaryFile:testdata.txt}    |
    | 0000000102 | 鈴木花子 | 2    | Null  | 2.25 | シルバー会員     | ${binaryFile:member_photo.jpg} |

YAMLの場合
----------

.. code-block:: yaml

    setup_tables:
      - table: MEMBER
        rows:
          - MEMBER_ID: "0000000101"
            NAME: "山田太郎"
            RANK: "1"
            SCORE: "85000"
            RATE: "1.5"
            PROFILE: "ゴールド会員です"
            PHOTO: "${binaryFile:testdata.txt}"
          - MEMBER_ID: "0000000102"
            NAME: "鈴木花子"
            RANK: "2"
            SCORE: null
            RATE: "2.25"
            PROFILE: "シルバー会員"
            PHOTO: "${binaryFile:member_photo.jpg}"

- NULL 値は Excel では ``Null``（大文字小文字不問）、YAML ではアンクォートの ``null`` で記述する。YAML で ``"null"`` とクォートすると文字列として格納される。

EXPECTED_TABLE と EXPECTED_COMPLETE_TABLE
==========================================

Excelの場合
-----------

.. code-block:: text

    EXPECTED_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | UPDATED_DATE          |
    | 0000000101 | 山田太郎 | 1    | 87500 | 2024-04-01 09:00:00.0 |
    | 0000000102 | 鈴木花子 | 2    | 42000 | 2024-04-01 09:00:00.0 |

    EXPECTED_COMPLETE_TABLE=ORDER_HEADER
    | ORDER_ID | ITEM_COUNT | STATUS | UPDATE_DATE           |
    | 10001    | 3          | 1      | 2024-04-01 12:30:00.0 |
    | 10002    | 5          | 1      |                       |

YAMLの場合
----------

.. code-block:: yaml

    expected_tables:
      - table: MEMBER
        rows:
          - MEMBER_ID: "0000000101"
            NAME: "山田太郎"
            RANK: "1"
            SCORE: "87500"
            UPDATED_DATE: "2024-04-01 09:00:00.0"
          - MEMBER_ID: "0000000102"
            NAME: "鈴木花子"
            RANK: "2"
            SCORE: "42000"
            UPDATED_DATE: "2024-04-01 09:00:00.0"

    expected_complete_tables:
      - table: ORDER_HEADER
        rows:
          - ORDER_ID: "10001"
            ITEM_COUNT: "3"
            STATUS: "1"
            UPDATE_DATE: "2024-04-01 12:30:00.0"
          - ORDER_ID: "10002"
            ITEM_COUNT: "5"
            STATUS: "1"

- ``EXPECTED_TABLE`` / ``expected_tables:`` は省略カラムを比較対象外にする。``EXPECTED_COMPLETE_TABLE`` / ``expected_complete_tables:`` は ``BasicDefaultValues`` のデフォルト値を補完してから比較する。

LIST_MAP（汎用データ）
======================

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=searchParams
    | [no] | memberId   | orderStatus | fromDate   | toDate     | [desc]     |
    | 1    | 0000000101 | 1           | 2024-04-01 | 2024-04-30 | 4月注文検索 |
    | 2    | 0000000102 |             | 2024-01-01 |            | 全件検索   |

    LIST_MAP=expectedLog
    | message                                     | logLevel |
    | 会員ID[0000000101]の注文を処理しました      | INFO     |
    | 会員ID[0000000102]の注文を処理しました      | INFO     |

YAMLの場合
----------

.. code-block:: yaml

    list_maps:
      - id: searchParams
        rows:
          - "[no]": "1"
            memberId: "0000000101"
            orderStatus: "1"
            fromDate: "2024-04-01"
            toDate: "2024-04-30"
            "[desc]": "4月注文検索"
          - "[no]": "2"
            memberId: "0000000102"
            orderStatus: ""
            fromDate: "2024-01-01"
            toDate: ""
            "[desc]": "全件検索"
      - id: expectedLog
        rows:
          - message: "会員ID[0000000101]の注文を処理しました"
            logLevel: "INFO"
          - message: "会員ID[0000000102]の注文を処理しました"
            logLevel: "INFO"

- ``[no]`` ・ ``[desc]`` のように角括弧で囲んだカラムはマーカーカラムで、DB 操作から除外される。YAML ではダブルクォートで囲む（``"[no]"``）。

----------------------------
ファイルデータの記述例
----------------------------

固定長ファイル（SETUP_FIXED / EXPECTED_FIXED）
===============================================

Excelの場合
-----------

.. code-block:: text

    SETUP_FIXED=work/input.txt
    | データ | ID    | COUNTER | MESSAGE   |
    |        | 半角  | 数値    | 半角      |
    |        | 5     | 5       | 10        |
    |        | 10001 | 10      | hello     |
    |        | 10002 | 20      | good bye. |

    EXPECTED_FIXED=work/output.txt
    | データ | ID    | COUNTER | MESSAGE   |
    |        | 半角  | 数値    | 半角      |
    |        | 5     | 5       | 10        |
    |        | 10001 | 11      | HELLO     |
    |        | 10002 | 21      | GOOD BYE. |

YAMLの場合
----------

.. code-block:: yaml

    setup_files:
      - path: work/input.txt
        type: fixed
        records:
          - record_type: データ
            fields:
              - {name: ID,      type: 半角, length: 5}
              - {name: COUNTER, type: 数値, length: 5}
              - {name: MESSAGE, type: 半角, length: 10}
            rows:
              - ["10001", "10", "hello"]
              - ["10002", "20", "good bye."]

    expected_files:
      - path: work/output.txt
        type: fixed
        records:
          - record_type: データ
            fields:
              - {name: ID,      type: 半角, length: 5}
              - {name: COUNTER, type: 数値, length: 5}
              - {name: MESSAGE, type: 半角, length: 10}
            rows:
              - ["10001", "11", "HELLO"]
              - ["10002", "21", "GOOD BYE."]

可変長ファイル（SETUP_VARIABLE）
=================================

Excelの場合
-----------

.. code-block:: text

    SETUP_VARIABLE=input/data.csv
    | field-separator | , |   |
    | DATA | USER_ID | USER_NAME | AMOUNT |
    |      | X       | N         | X      |
    |      | 001     | 山田太郎  | 5000   |
    |      | 002     | 鈴木花子  | 3000   |

YAMLの場合
----------

.. code-block:: yaml

    setup_files:
      - path: input/data.csv
        type: variable
        directives:
          field-separator: ","
        records:
          - record_type: DATA
            fields:
              - {name: USER_ID,   type: X}
              - {name: USER_NAME, type: N}
              - {name: AMOUNT,    type: X}
            rows:
              - ["001", "山田太郎", "5000"]
              - ["002", "鈴木花子", "3000"]

- 可変長ファイルは ``type: variable`` とし、``fields:`` から ``length`` を省略する。

グループID付きファイル
======================

Excelの場合
-----------

.. code-block:: text

    SETUP_FIXED=work/input.txt
    | データ | ID    | COUNTER | MESSAGE |
    |        | 半角  | 数値    | 半角    |
    |        | 5     | 5       | 10      |
    |        | 10001 | 10      | hello   |

    SETUP_FIXED[case2]=work/input.txt
    | データ | ID    | COUNTER | MESSAGE |
    |        | 半角  | 数値    | 半角    |
    |        | 5     | 5       | 10      |
    |        | 20001 | 30      | morning |

YAMLの場合
----------

.. code-block:: yaml

    setup_files:
      - path: work/input.txt
        type: fixed
        records:
          - record_type: データ
            fields:
              - {name: ID,      type: 半角, length: 5}
              - {name: COUNTER, type: 数値, length: 5}
              - {name: MESSAGE, type: 半角, length: 10}
            rows:
              - ["10001", "10", "hello"]
      - group_id: case2
        path: work/input.txt
        type: fixed
        records:
          - record_type: データ
            fields:
              - {name: ID,      type: 半角, length: 5}
              - {name: COUNTER, type: 数値, length: 5}
              - {name: MESSAGE, type: 半角, length: 10}
            rows:
              - ["20001", "30", "morning"]

複数レコードレイアウト
======================

Excelの場合
-----------

.. code-block:: text

    SETUP_FIXED=input/multi.dat
    | HEADER | SEQ  | TYPE |
    |        | X    | X    |
    |        | 4    | 2    |
    |        | H001 | 01   |
    | DATA   | USER_ID | AMOUNT | NOTE |
    |        | X       | Z      | N    |
    |        | 10      | 10     | 20   |
    |        | 001     | 5000   | 備考 |

YAMLの場合
----------

.. code-block:: yaml

    setup_files:
      - path: input/multi.dat
        type: fixed
        records:
          - record_type: HEADER
            fields:
              - {name: SEQ,  type: X, length: 4}
              - {name: TYPE, type: X, length: 2}
            rows:
              - ["H001", "01"]
          - record_type: DATA
            fields:
              - {name: USER_ID, type: X, length: 10}
              - {name: AMOUNT,  type: Z, length: 10}
              - {name: NOTE,    type: N, length: 20}
            rows:
              - ["001", "5000", "備考"]

---------------------------------
メッセージングデータの記述例
---------------------------------

MESSAGE セクション
==================

Excelの場合
-----------

.. code-block:: text

    MESSAGE=requestMessages
    | text-encoding | Windows-31J |        |        |
    | requestId     | hoge        |        |        |
    | userId        | moge        |        |        |
    |               | ユーザ名    | 備考   | FILLER |
    |               | 全角        | 全角   | 半角   |
    |               | 50          | 200    | 252    |
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
              - ["電文太郎", "特筆なし",                               ""]
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

- FW制御ヘッダ（``requestId``・``userId`` 等）は YAML では ``fw_header:`` マップに記述する。
- ディレクティブ行（``text-encoding`` 等）はフィールド定義より前に記述する。

要求電文・応答電文の期待値（SendSync）
=======================================

Excelの場合
-----------

.. code-block:: text

    EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM21AA0104_01
    | text-encoding | ms932 |     |
    | no            | requestId |  |
    |               | 半角 |      |
    |               | 20   |      |
    | 1             | RM21AA0104_01 | |

YAMLの場合
----------

.. code-block:: yaml

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

- YAML では ``group_id:`` が ``testShots`` の ``expectedMessage`` カラムに対応する。

---------------------------------------
特殊値・ディレクティブ・ヘッダの記述例
---------------------------------------

日付・Timestamp・NULL・特殊値
==============================

Excelの場合
-----------

.. code-block:: text

    EXPECTED_TABLE=SCHEDULE
    | ID | EVENT_NAME   | START_DATE       | CREATED_AT            |
    | 1  | 会議         | 2024-01-15       | 2024-01-01 09:00:00.0 |
    | 2  | NULLテスト   | NULL             | NULL                  |
    | 3  | システム時刻 | ${systemTime}    | ${systemTime}         |

YAMLの場合
----------

.. code-block:: yaml

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

- NULL 値は Excel では ``NULL``（大文字小文字不問）、YAML ではアンクォートの ``null`` で記述する。
- ``java.sql.Timestamp`` 型カラムの期待値は末尾 ``.0`` が必須（例: ``"2024-01-01 09:00:00.0"``）。

バイナリデータ
==============

Excelの場合
-----------

.. code-block:: text

    SETUP_TABLE=FILE_TABLE
    | FILE_ID | FILE_DATA                    |
    | 001     | 0xCAFEBABE                   |
    | 002     | ${binaryFile:testdata.bin}   |

YAMLの場合
----------

.. code-block:: yaml

    setup_tables:
      - table: FILE_TABLE
        rows:
          - FILE_ID: "001"
            FILE_DATA: "0xCAFEBABE"
          - FILE_ID: "002"
            FILE_DATA: "${binaryFile:testdata.bin}"

- ``0x`` プレフィクス付き16進数でバイナリ値を記述する。``${binaryFile:パス}`` でファイル内容をバイナリ読み込みして HexString に変換する。

コメントとマーカーカラム
========================

Excelの場合
-----------

.. code-block:: text

    SETUP_TABLE=TEST_TABLE
    | // この行はコメントです        |            |          |            |        |
    | [no] | PK_COL1    | PK_COL2 | NUMBER_COL | [desc]  |
    | 1    | 0000000001 | AB      | 100        | テスト1 |
    | // この行もスキップされます    |            |          |            |        |
    | 2    | 0000000002 | CD      | 200        | テスト2 |

YAMLの場合
----------

.. code-block:: yaml

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

- Excel では ``//`` で始まる行がスキップされる。YAML では標準の ``#`` 構文を使う。
- ``[no]`` ・ ``[desc]`` のように角括弧で囲んだカラムはマーカーカラムで、DB 操作から除外される。YAML ではダブルクォートで囲む（``"[no]"``）。

ディレクティブ（固定長・可変長ファイル）
=========================================

Excelの場合
-----------

.. code-block:: text

    SETUP_FIXED=input/data.dat
    | text-encoding           | MS932 |         |
    | positive-zone-sign-nibble | C    |         |
    | DATA | USER_ID | AMOUNT |
    |      | X       | Z      |
    |      | 10      | 10     |
    |      | 001     | 5000   |

    SETUP_VARIABLE=input/data.tsv
    | field-separator  | \t     |
    | record-separator | CRLF   |
    | DATA | FIELD1 | FIELD2  |
    |      | X      | X       |
    |      | value1 | value2  |

YAMLの場合
----------

.. code-block:: yaml

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

- タブ文字の記法が形式で異なる。Excel セルには ``\t``（バックスラッシュ + t の2文字）を入力する。YAML では ``"\\t"`` と記述する（YAML の ``\t`` は実際のタブ文字になるためバックスラッシュをエスケープする）。
