.. _ntf_testdata_testshots:

================
テストケース定義
================

テストデータは Excel または YAML ファイルで記述できる。

``testShots`` はテストケース定義の予約 ID である。フレームワークがこの ID を自動的に読み込み、各エントリを1テストケースとして実行する。

-----------
testShots
-----------

``testShots`` の仕様を以下に記載する。

- テスト実行には ``testShots`` に1件以上のエントリが必要である（0件はエラー）。
- 旧称 ``testCases`` も動作するが、新規作成では ``testShots`` を使うこと。
- **Excel**: ``LIST_MAP=testShots`` データブロックに記述する。
- **YAML**: ``list_maps:`` 下の ``id: testShots`` エントリに記述する。

``testShots`` の1行が1テストケースとなる。カラムには値を直接書くものと、別データブロック（ ``LIST_MAP`` や各種テーブル／ファイル／電文ブロック）の groupId・名前を指す参照型がある。処理方式ごとに必須カラムとオプションカラムが定まる。

各処理方式と対応クラスを以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 処理方式
     - 対応クラス
   * - ウェブアプリケーション
     - ``HttpRequestTestSupport``
   * - バッチ処理
     - ``BatchRequestTestSupport``
   * - メッセージング
     - ``MessagingRequestTestSupport``
   * - エンティティバリデーション
     - ``EntityTestSupport``

.. _ntf_testshots_common:

共通カラム
==========

ウェブ・バッチ・メッセージングで共通の必須カラムを以下に示す。エンティティバリデーションは別体系である（後述の :ref:`ntf_testshots_entity` を参照）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - カラム名
     - 説明
   * - ``no``
     - テストケース番号。空の場合はエラー
   * - ``description``
     - テストケースの説明（旧名 ``case`` も可）。 ``description`` も ``case`` も未定義の場合はエラー
   * - ``expectedStatusCode``
     - 期待するステータスコード（ウェブは HTTP ステータスコード）

---------------------------------------------------
ウェブアプリケーション（HttpRequestTestSupport）
---------------------------------------------------

必須カラム
==========

:ref:`共通カラム <ntf_testshots_common>` （ ``no`` / ``description`` / ``expectedStatusCode`` ）に加えて以下が必須である。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - カラム名
     - 説明
   * - ``isValidToken``
     - CSRF トークン制御フラグ（ ``1``: あり、 ``0``: なし）
   * - ``forwardUri``
     - 期待するフォワード先 URI
   * - ``context``
     - リクエスト ID・ユーザ・HTTP メソッドを記載した ``LIST_MAP`` 名。1エントリのみ有効。 ``REQUEST_ID`` が空の場合は例外がスロー

オプションカラム
================

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - カラム名
     - 説明
     - 空の場合
   * - ``setUpDb``
     - この値と同じ名前の ``LIST_MAP`` を持つシートの全 ``SETUP_TABLE`` を、テストメソッド開始前に1回だけ INSERT
     - スキップ
   * - ``setUpTable``
     - この値と同じ groupId を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ groupId を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``expectedSearch``
     - 検索結果期待値の groupId（対応する ``LIST_MAP`` セクションを収集）
     - スキップ
   * - ``expectedMessageId``
     - 期待するメッセージ ID（カンマ区切りで複数指定可）
     - スキップ
   * - ``requestParams``
     - HTTP リクエストパラメータの ``LIST_MAP`` 名。指定した LIST_MAP の行数がテストケース番号より少ない場合はエラー
     - —
   * - ``responseResult``
     - HTTP レスポンス（リクエストスコープ）期待値の ``LIST_MAP`` 名
     - スキップ
   * - ``cookie``
     - Cookie 値の ``LIST_MAP`` 名。指定した LIST_MAP が空の場合はエラー
     - Cookie なし
   * - ``queryParams``
     - クエリパラメータの ``LIST_MAP`` 名。指定した LIST_MAP が空の場合はエラー
     - パラメータなし
   * - ``HTTP_METHOD``
     - HTTP メソッド
     - ``"POST"``
   * - ``expectedContentLength``
     - 期待する Content-Length
     - スキップ
   * - ``expectedContentType``
     - 期待する Content-Type
     - スキップ
   * - ``expectedContentFileName``
     - 期待する Content-Disposition ファイル名
     - スキップ
   * - ``expectedMessage``
     - この値と同じ groupId を持つ要求電文セクション（ ``EXPECTED_REQUEST_HEADER/BODY_MESSAGES`` ）で検証
     - スキップ
   * - ``responseMessage``
     - この値と同じ groupId を持つ応答電文セクション（ ``RESPONSE_HEADER/BODY_MESSAGES`` ）をレスポンスとして返す
     - スキップ
   * - ``expectedMessageByClient``
     - HTTP 同期応答メッセージ送信の要求電文グループ ID
     - スキップ
   * - ``responseMessageByClient``
     - HTTP 同期応答メッセージ送信の応答電文グループ ID
     - スキップ

記述例
======

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description | isValidToken | expectedStatusCode | forwardUri | context    |
    | 1  | 正常ケース  | 0            | 200                | /success   | context001 |
    | 2  | 認証エラー  | 0            | 400                | /error     | context002 |

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

-----------------------------------------
バッチ処理（BatchRequestTestSupport）
-----------------------------------------

必須カラム
==========

:ref:`共通カラム <ntf_testshots_common>` （ ``no`` / ``description`` / ``expectedStatusCode`` ）に加えて以下が必須である。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - カラム名
     - 説明
   * - ``diConfig``
     - DI コンポーネント設定ファイルパス
   * - ``requestPath``
     - リクエストパス
   * - ``userId``
     - 実行ユーザ ID

オプションカラム
================

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - カラム名
     - 説明
     - 空の場合
   * - ``setUpDb``
     - この値と同じ名前の ``LIST_MAP`` を持つシートの全 ``SETUP_TABLE`` を、テストメソッド開始前に1回だけ INSERT
     - スキップ
   * - ``setUpTable``
     - この値と同じ groupId を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ groupId を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``setUpFile``
     - この値と同じ groupId を持つ ``SETUP_FIXED`` / ``SETUP_VARIABLE`` セクションを入力ファイルとして配置
     - スキップ
   * - ``expectedFile``
     - この値と同じ groupId を持つ ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE`` セクションで出力ファイルを検証
     - スキップ
   * - ``expectedLog``
     - 期待ログの ``LIST_MAP`` 名。指定した LIST_MAP が空の場合はエラー
     - スキップ
   * - ``args[0]``, ``args[1]``, ...
     - コマンドライン引数
     - —
   * - その他任意カラム
     - コマンドラインオプション
     - —

記述例
======

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description        | expectedStatusCode | diConfig                                 | requestPath       | userId | setUpFile |
    | 1  | 正しく更新されます | 0                  | nablarch/test/core/batch/BatchSample.xml | DBtoDBBatchSample | test   |           |
    | 2  | 入力ファイルあり   | 0                  | nablarch/test/core/batch/BatchSample.xml | FileToFileBatch   | test   | case2     |

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

-------------------------------------------------
メッセージング（MessagingRequestTestSupport）
-------------------------------------------------

必須カラム
==========

:ref:`共通カラム <ntf_testshots_common>` （ ``no`` / ``description`` / ``expectedStatusCode`` ）に加えて以下が必須である。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - カラム名
     - 説明
   * - ``diConfig``
     - DI コンポーネント設定ファイルパス
   * - ``requestPath``
     - リクエストパス
   * - ``userId``
     - 実行ユーザ ID

オプションカラム
================

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - カラム名
     - 説明
     - 空の場合
   * - ``setUpDb``
     - この値と同じ名前の ``LIST_MAP`` を持つシートの全 ``SETUP_TABLE`` を、テストメソッド開始前に1回だけ INSERT
     - スキップ
   * - ``setUpTable``
     - この値と同じ groupId を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ groupId を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``expectedMessage``
     - この値と同じ groupId を持つ要求電文セクション（ ``EXPECTED_REQUEST_HEADER/BODY_MESSAGES`` ）で検証
     - スキップ
   * - ``responseMessage``
     - この値と同じ groupId を持つ応答電文セクション（ ``RESPONSE_HEADER/BODY_MESSAGES`` ）をレスポンスとして返す
     - スキップ
   * - ``expectedLog``
     - 期待ログの ``LIST_MAP`` 名。指定した LIST_MAP が空の場合はエラー
     - スキップ

記述例
======

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | no | description      | expectedStatusCode | diConfig                              | requestPath | userId     | expectedMessage | responseMessage |
    | 1  | 電文送受信テスト | 0                  | batch-test-component-configuration.xml | BM21AA0106  | batch_user | case1           | res_case1       |

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

.. _ntf_testshots_entity:

--------------------------------------------------
エンティティバリデーション（EntityTestSupport）
--------------------------------------------------

共通カラムとは別体系である。 ``no`` / ``description`` / ``expectedStatusCode`` は使用しない。

必須カラム
==========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - カラム名
     - 説明
   * - ``title``
     - テストケースの説明
   * - ``expectedMessageId1``
     - 期待するバリデーションメッセージ ID（複数ある場合は ``expectedMessageId2``, ``expectedMessageId3``, ... と連番で追加）
   * - ``propertyName1``
     - バリデーション対象プロパティ名（同上、連番で追加可能）

関連予約 ID
===========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 予約 ID
     - 説明
   * - ``params``
     - 入力パラメータ定義。 ``testShots`` の行数と一致が必須

記述例
======

Excelの場合
-----------

.. code-block:: text

    LIST_MAP=testShots
    | title    | expectedMessageId1 | propertyName1 |
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

---------------------------
データブロックのグループ化
---------------------------

複数のテストケースで異なるセットアップデータや期待値を使い分けたい場合、データブロックに **groupId** を付加してグループ化する。 ``testShots`` の各カラム（ ``setUpTable`` / ``expectedTable`` / ``setUpFile`` / ``expectedFile`` 等）に groupId の値を指定すると、そのテストケースでは対応する groupId を持つデータブロックだけが収集される。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 形式
     - 記述方法
   * - Excel
     - DataType 名の直後に ``[groupId]`` を付ける。例: ``SETUP_TABLE[case01]=USER_MASTER``
   * - YAML
     - ``group_id:`` フィールドを記述する

制約
====

- ``testShots`` の各カラムで groupId を省略すると、groupId なしのデータブロック（デフォルトグループ）が収集される。
- バッチ固有の動作として groupId に ``"default"`` を指定すると groupId なし扱いと同等になる（HTTP テスト・メッセージングテストでは適用されない）。

記述例
======

Excelの場合
-----------

groupId はデータブロック種別ラベルの ``[...]`` で指定する。

.. code-block:: text

    LIST_MAP=testShots
    | no | description | expectedStatusCode | setUpTable | expectedTable |
    | 1  | 正常注文    | 0                  | case01     | case01        |
    | 2  | 大量注文    | 0                  | case02     | case02        |

    SETUP_TABLE[case01]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 1001     | P-001        | 5        | 1500       |

    SETUP_TABLE[case02]=ORDER_DETAIL
    | ORDER_ID | PRODUCT_CODE | QUANTITY | UNIT_PRICE |
    | 2001     | P-003        | 100      | 500        |
    | 2001     | P-004        | 200      | 300        |

YAMLの場合
----------

groupId は各エントリの ``group_id:`` フィールドで指定する。

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

.. note::

  ウェブ・バッチ・メッセージングの共通必須カラムは ``no`` / ``description`` / ``expectedStatusCode`` の3つである。

