.. _testdata_examples:

テストデータの記載例
==================================================

.. contents:: 目次
  :depth: 3
  :local:

.. _testdata_examples-data_block_types:

データブロックとデータタイプ
--------------------------------------------------
1つの読み込み単位（\ Excel\ 形式では1シート、\ YAML\ 形式では1ファイル）に、テストショット・準備データ・期待値を共存させる記述例を示す。データブロックの識別子とデータタイプの仕様は\ :ref:`データブロックとデータタイプ <testdata_notation-data_block_types>`\ を参照。

1つの読み込み単位にテストショット・準備データ・期待値をまとめる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
注文ヘッダテーブル（\ ``ORDER_HEADER``\ ）の注文明細件数を加算する\ Nablarch\ バッチアプリケーションを、リクエスト単体テストで検証する例である。1つの読み込み単位に、テストショット一覧・準備データ・期待値・期待ログという用途の異なる4つのデータブロックを記述している。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

テストショット一覧の例を示す。カラム数が多いため、ここでは複数に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,32,20,20,20

  * - LIST_MAP=testShots
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - setUpTable
    - expectedTable
  * - 1
    - 注文カウンタが正しくインクリメントされます
    - 0
    - default
    - default

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,17,17,25,17,16

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
  * - no
    - setUpFile
    - expectedFile
    - diConfig
    - requestPath
    - userId
  * - 1
    -
    -
    - nablarch/test/core/batch/BatchSample.xml
    - DBtoDBBatchSample
    - test

期待ログを参照するカラム（\ ``expectedLog``\ ）は、後続の「LIST_MAP=expectedLog」のデータブロックを指す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,92

  * - LIST_MAP=testShots
    -
  * - no
    - expectedLog
  * - 1
    - expectedLog

準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - SETUP_TABLE=ORDER_HEADER
    -
    -
  * - ORDER_ID
    - ITEM_COUNT
    - REMARKS
  * - 10001
    - 10
    - 通常注文
  * - 10002
    - 20
    - まとめ買い

期待値の例を示す。バッチ処理によって ``ITEM_COUNT``\ が1加算され、\ ``UPDATE_DATE``\ が更新されることを検証している。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 20,20,25,35

  * - EXPECTED_TABLE=ORDER_HEADER
    -
    -
    -
  * - ORDER_ID
    - ITEM_COUNT
    - REMARKS
    - UPDATE_DATE
  * - 10001
    - 11
    - 通常注文
    - 2010-09-13 12:34:56.0
  * - 10002
    - 21
    - まとめ買い
    - 2010-09-13 12:34:56.0

期待ログの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 30,70

  * - LIST_MAP=expectedLog
    -
  * - logLevel
    - message1
  * - INFO
    - 注文ID[10001]
  * - INFO
    - 注文ID[10002]

データブロックの用途は、先頭行の識別子で決まる。この例では「LIST_MAP=testShots」がテストショット一覧、「SETUP_TABLE=ORDER_HEADER」が準備データ、「EXPECTED_TABLE=ORDER_HEADER」が期待値、「LIST_MAP=expectedLog」が期待ログである。

.. rubric:: YAML形式の場合

同じ内容を\ YAML\ 形式で記述すると、以下のようになる。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "注文カウンタが正しくインクリメントされます"
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
        - logLevel: "INFO"
          message1: "注文ID[10001]"
        - logLevel: "INFO"
          message1: "注文ID[10002]"

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

データブロックの用途は、トップレベルキーで決まる。この例では ``list_maps:``\ の ``id: testShots``\ がテストショット一覧、\ ``setup_tables:``\ が準備データ、\ ``expected_tables:``\ が期待値である。期待ログのように任意の\ ID\ を持つ ``list_maps:``\ のエントリも、同じファイルに並べて記述できる。

.. _testdata_examples-group_id:

グループIDによる使い分け
--------------------------------------------------
テストショットごとに異なる準備データ・期待値を使い分ける記述例を示す。グループIDの仕様は\ :ref:`グループIDによる使い分け <testdata_notation-group_id>`\ を参照。

テストショットごとに準備データと期待値を使い分ける
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
注文明細テーブル（\ ``ORDER_DETAIL``\ ）に対して、明細1件の正常注文と明細2件の大量注文という2つのテストショットを実行する例である。テストショット一覧の ``setUpTable``\ ・\ ``expectedTable``\ カラムに記述した値がグループIDになり、そのグループIDを持つデータブロックだけが対象になる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 25,25,50

  * - テストショット
    - ``setUpTable``\ の値
    - 投入されるデータブロック
  * - 1（正常注文）
    - ``case01``
    - グループID ``case01``\ の ``SETUP_TABLE``
  * - 2（大量注文）
    - ``case02``
    - グループID ``case02``\ の ``SETUP_TABLE``

``expectedTable``\ カラムも同様に、記述した値と同じグループIDを持つ期待値のデータブロックが検証に使われる。

.. rubric:: Excel形式の場合

グループIDは、識別子行のデータタイプ名の直後に半角角括弧で記述する。テストショット一覧の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,25,25,20,20

  * - LIST_MAP=testShots
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - setUpTable
    - expectedTable
  * - 1
    - 正常注文
    - 0
    - case01
    - case01
  * - 2
    - 大量注文
    - 0
    - case02
    - case02

テストショット1の準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_TABLE[case01]=ORDER_DETAIL
    -
    -
    -
  * - ORDER_ID
    - PRODUCT_CODE
    - QUANTITY
    - UNIT_PRICE
  * - 1001
    - P-001
    - 5
    - 1500

テストショット1の期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - EXPECTED_TABLE[case01]=ORDER_DETAIL
    -
    -
    -
  * - ORDER_ID
    - PRODUCT_CODE
    - QUANTITY
    - UNIT_PRICE
  * - 1001
    - P-001
    - 5
    - 1500

テストショット2の準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_TABLE[case02]=ORDER_DETAIL
    -
    -
    -
  * - ORDER_ID
    - PRODUCT_CODE
    - QUANTITY
    - UNIT_PRICE
  * - 2001
    - P-003
    - 100
    - 500
  * - 2001
    - P-004
    - 200
    - 300

テストショット2の期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - EXPECTED_TABLE[case02]=ORDER_DETAIL
    -
    -
    -
  * - ORDER_ID
    - PRODUCT_CODE
    - QUANTITY
    - UNIT_PRICE
  * - 2001
    - P-003
    - 100
    - 500
  * - 2001
    - P-004
    - 200
    - 300

.. important::

  同じグループIDのデータブロックは、シート内で連続させて記述する（\ :ref:`グループIDによる使い分け <testdata_notation-group_id>`\ 参照）。

.. rubric:: YAML形式の場合

グループIDは、各エントリの ``group_id:``\ キーで記述する。

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

.. _testdata_examples-test_shots:

テストショット一覧（testShots）を記述する
--------------------------------------------------
テストショット一覧（\ ``testShots``\ ）の記述例を、処理方式ごとに示す。これは\ ``LIST_MAP``\ というデータタイプを使うデータブロックの1つであり、同じデータタイプを使う他のデータブロックの記述例は後述の\ :ref:`LIST_MAPのデータを記述する <testdata_examples-list_map>`\ に示す。使用できるカラムの仕様は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ を参照。

ウェブアプリケーションのテストショット一覧を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
正常ケースと認証エラーの2つのテストショットを実行する例である。\ ``context``\ カラムには、リクエスト\ ID\ ・実行ユーザ・\ HTTP\ メソッドを記述した ``LIST_MAP``\ の\ ID\ を指定する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

テストショット一覧の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,20,15,20,17,20

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
  * - no
    - description
    - isValidToken
    - expectedStatusCode
    - forwardUri
    - context
  * - 1
    - 正常ケース
    - true
    - 200
    - /success
    - context001
  * - 2
    - 認証エラー
    - false
    - 400
    - /error
    - context002

リクエストパラメータは、テストショット数分の行を持つ ``requestParams``\ という\ ID\ の ``LIST_MAP``\ に記述する（\ :ref:`LIST_MAPのデータを記述する <testdata_examples-list_map>`\ 参照）。\ ``context``\ カラムから参照される ``LIST_MAP``\ は、テストショットごとに1つずつ記述する。1件目の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - LIST_MAP=context001
    -
    -
  * - REQUEST_ID
    - USER_ID
    - HTTP_METHOD
  * - REQ_001
    - user001
    - POST

2件目の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - LIST_MAP=context002
    -
    -
  * - REQUEST_ID
    - USER_ID
    - HTTP_METHOD
  * - REQ_002
    - user002
    - POST

.. rubric:: YAML形式の場合

``list_maps:``\ の下に、\ ``testShots``\ と参照先の ``LIST_MAP``\ を並べて記述する。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "正常ケース"
          isValidToken: "true"
          expectedStatusCode: "200"
          forwardUri: "/success"
          context: "context001"
        - no: "2"
          description: "認証エラー"
          isValidToken: "false"
          expectedStatusCode: "400"
          forwardUri: "/error"
          context: "context002"
    - id: context001
      rows:
        - REQUEST_ID: "REQ_001"
          USER_ID: "user001"
          HTTP_METHOD: "POST"
    - id: context002
      rows:
        - REQUEST_ID: "REQ_002"
          USER_ID: "user002"
          HTTP_METHOD: "POST"

Nablarchバッチアプリケーションのテストショット一覧を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースだけを処理するテストショットと、入力ファイルを使うテストショットの2件を実行する例である。後者では、\ ``setUpFile``\ カラムにグループIDを記述し、同じグループIDを持つファイルデータのデータブロックと紐付ける。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

テストショット一覧の例を示す。カラム数が多いため、ここでは前半・後半に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,27,20,45

  * - LIST_MAP=testShots
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
  * - 1
    - 正しく更新されます
    - 0
    - nablarch/test/core/batch/BatchSample.xml
  * - 2
    - 入力ファイルあり
    - 0
    - nablarch/test/core/batch/BatchSample.xml

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,45,20,25

  * - LIST_MAP=testShots
    -
    -
    -
  * - no
    - requestPath
    - userId
    - setUpFile
  * - 1
    - DBtoDBBatchSample
    - test
    -
  * - 2
    - FileToFileBatchSample
    - test
    - case2

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: testShots``\ のエントリに記述する。

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

メッセージングのテストショット一覧を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
電文の送受信を検証する例である。\ ``expectedMessage``\ カラムには要求電文のグループIDを、\ ``responseMessage``\ カラムには応答電文のグループIDを記述する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

テストショット一覧の例を示す。カラム数が多いため、ここでは前半・後半に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,25,20,47

  * - LIST_MAP=testShots
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
  * - 1
    - 電文送受信テスト
    - 0
    - batch-test-component-configuration.xml

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 8,25,22,22,23

  * - LIST_MAP=testShots
    -
    -
    -
    -
  * - no
    - requestPath
    - userId
    - expectedMessage
    - responseMessage
  * - 1
    - BM21AA0106
    - batch_user
    - case1
    - res_case1

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: testShots``\ のエントリに記述する。

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

エンティティバリデーションのテストショット一覧を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
必須入力チェックのバリデーションを検証する例である。エンティティバリデーションは他のカラム体系とは別の体系であり、\ ``title``\ ・\ ``expectedMessageId1``\ ・\ ``propertyName1``\ を使う。テストショット一覧と対にして、予約\ ID\ ``params``\ の\ ``LIST_MAP``\ に入力パラメータを記述する。\ ``params``\ の行はテストショット一覧の行と同じ順に対応させ、行数を一致させる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

テストショット一覧と入力パラメータの例を示す。入力パラメータの\ ``userName``\ を空欄にすることで、必須入力チェックのエラーを発生させている。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - LIST_MAP=testShots
    -
    -
  * - title
    - expectedMessageId1
    - propertyName1
  * - 必須チェック
    - errors.required
    - userName

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - LIST_MAP=params
    -
    -
  * - userName
    - password
    -
  * -
    - password1
    -

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: testShots``\ と ``id: params``\ のエントリに記述する。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - title: "必須チェック"
          expectedMessageId1: "errors.required"
          propertyName1: "userName"
    - id: params
      rows:
        - userName: ""
          password: "password1"

.. _testdata_examples-list_map:

LIST_MAPのデータを記述する
--------------------------------------------------
キーバリュー形式の汎用データ（\ ``LIST_MAP``\ ）の記述例を、用途ごとに示す。このデータタイプを使うデータブロックのうち、テストショット一覧（\ ``testShots``\ ）は前述の\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ で扱っている。記法の仕様は\ :ref:`LIST_MAPのデータを記述する <testdata_notation-list_map>`\ を参照。

リクエストパラメータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
注文検索画面に送信する\ HTTP\ リクエストパラメータを記述する例である。\ ``requestParams``\ は予約\ ID\ であり、この\ ID\ を持つ ``LIST_MAP``\ がリクエストパラメータとして読み込まれる。テストショット一覧とは行単位で対応するため、対応が分かるようテストショット番号と説明をマーカーカラム（\ ``[no]``\ ・\ ``[desc]``\ ）として記述している。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

リクエストパラメータの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,20,15,20,20,15

  * - LIST_MAP=requestParams
    -
    -
    -
    -
    -
  * - [no]
    - memberId
    - orderStatus
    - fromDate
    - toDate
    - [desc]
  * - 1
    - 0000000101
    - 1
    - 2024-04-01
    - 2024-04-30
    - 4月注文検索
  * - 2
    - 0000000102
    -
    - 2024-01-01
    -
    - 全件検索

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: requestParams``\ のエントリに記述する。マーカーカラムのキーは、\ YAML\ の配列構文との衝突を避けるためダブルクォートで囲む。

.. code-block:: yaml

  list_maps:
    - id: requestParams
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

期待ログを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バッチ処理が出力するログを検証する例である。テストショット一覧の ``expectedLog``\ カラムに、この ``LIST_MAP``\ の\ ID\ を記述して紐付ける。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

期待ログの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,75

  * - LIST_MAP=expectedLog
    -
  * - logLevel
    - message1
  * - INFO
    - 会員ID[0000000101]の注文を処理しました
  * - INFO
    - 会員ID[0000000102]の注文を処理しました

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: expectedLog``\ のエントリに記述する。同じトップレベルキーの下に、用途の異なる ``LIST_MAP``\ を並べて記述できる。

.. code-block:: yaml

  list_maps:
    - id: requestParams   # 前掲のリクエストパラメータ（抜粋）
      rows:
        - "[no]": "1"
          memberId: "0000000101"
    - id: expectedLog
      rows:
        - logLevel: "INFO"
          message1: "会員ID[0000000101]の注文を処理しました"
        - logLevel: "INFO"
          message1: "会員ID[0000000102]の注文を処理しました"

.. _testdata_examples-charset_and_length:

文字種と文字列長のテストデータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
エンティティ単体テストで、プロパティごとに未入力の可否・文字列長・許容する文字種を記述する例である。プロパティ1つにつき1行を記述し、テストメソッドにはこの ``LIST_MAP``\ の\ ID\ を指定する。ここでは\ Bean Validation\ を使用する場合を示す。カラムの仕様は\ :ref:`エンティティ単体テスト <entity_unit_test>`\ を参照。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

必須カラムだけを記述した例を示す。カラム数が多いため、ここでは文字列長の条件・半角の文字種・全角ほかの文字種に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 22,12,7,7,52

  * - LIST_MAP=charsetAndLength
    -
    -
    -
    -
  * - propertyName
    - allowEmpty
    - min
    - max
    - messageIdWhenNotApplicable
  * - userName
    - x
    - 5
    - 50
    - {nablarch.core.validation.ee.SystemChar.message}
  * - address
    - o
    -
    - 100
    - {nablarch.core.validation.ee.SystemChar.message}

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 28,18,18,18,18

  * - LIST_MAP=charsetAndLength
    -
    -
    -
    -
  * - propertyName
    - 半角英字
    - 半角数字
    - 半角記号
    - 半角カナ
  * - userName
    - o
    - o
    - x
    - x
  * - address
    - x
    - x
    - x
    - x

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 19,9,9,9,9,9,9,9,9,9

  * - LIST_MAP=charsetAndLength
    -
    -
    -
    -
    -
    -
    -
    -
    -
  * - propertyName
    - 全角英字
    - 全角数字
    - 全角ひらがな
    - 全角カタカナ
    - 全角漢字
    - 全角記号その他
    - 中国語
    - サロゲートペア
    - 改行
  * - userName
    - x
    - x
    - x
    - x
    - x
    - x
    - x
    - x
    - x
  * - address
    - o
    - o
    - o
    - o
    - o
    - o
    - x
    - x
    - x

``address``\ の ``min``\ のように、値を記述しないカラムも空欄のまま用意する。省略した ``messageIdWhenEmptyInput``\ ・\ ``messageIdWhenInvalidLength``\ には、\ :ref:`エンティティ単体テストの設定 <entity_unit_test_setting>`\ で設定したデフォルト値が使われる。

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: charsetAndLength``\ のエントリに記述する。文字種のカラムは日本語のキーになる。

.. code-block:: yaml

  list_maps:
    - id: charsetAndLength
      rows:
        - propertyName: "userName"
          allowEmpty: "x"
          min: "5"
          max: "50"
          messageIdWhenNotApplicable: "{nablarch.core.validation.ee.SystemChar.message}"
          半角英字: "o"
          半角数字: "o"
          半角記号: "x"
          半角カナ: "x"
          全角英字: "x"
          全角数字: "x"
          全角ひらがな: "x"
          全角カタカナ: "x"
          全角漢字: "x"
          全角記号その他: "x"
          中国語: "x"
          サロゲートペア: "x"
          改行: "x"
        - propertyName: "address"
          allowEmpty: "o"
          min: ""
          max: "100"
          messageIdWhenNotApplicable: "{nablarch.core.validation.ee.SystemChar.message}"
          半角英字: "x"
          半角数字: "x"
          半角記号: "x"
          半角カナ: "x"
          全角英字: "o"
          全角数字: "o"
          全角ひらがな: "o"
          全角カタカナ: "o"
          全角漢字: "o"
          全角記号その他: "o"
          中国語: "x"
          サロゲートペア: "x"
          改行: "x"

.. _testdata_examples-setter_and_getter:

setterとgetterのテストデータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
エンティティ単体テストで、\ setter\ に渡す値と\ getter\ から取得される期待値をプロパティごとに記述する例である。プロパティ1つにつき1行を記述する。カラムの仕様は\ :ref:`エンティティ単体テスト <entity_unit_test>`\ を参照。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

プロパティ名と、\ setter\ に渡す値・\ getter\ から取得される期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 26,37,37

  * - LIST_MAP=setterAndGetter
    -
    -
  * - name
    - set
    - get
  * - userName
    - yamada0001
    - yamada0001
  * - address
    - 東京都新宿区
    - 東京都新宿区
  * - birthday
    - 1998-08-07
    - 1998-08-07

``birthday``\ のような\ ``java.util.Date``\ 型のプロパティは、\ ``yyyy-MM-dd``\ 形式または\ ``yyyy-MM-dd HH:mm:ss``\ 形式で記述する。

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: setterAndGetter``\ のエントリに記述する。

.. code-block:: yaml

  list_maps:
    - id: setterAndGetter
      rows:
        - name: "userName"
          set: "yamada0001"
          get: "yamada0001"
        - name: "address"
          set: "東京都新宿区"
          get: "東京都新宿区"
        - name: "birthday"
          set: "1998-08-07"
          get: "1998-08-07"

.. _testdata_examples-table_data:

テーブルのデータを記述する
--------------------------------------------------
データベースのテーブルに対応するテストデータ（\ ``SETUP_TABLE``\ ・\ ``EXPECTED_TABLE``\ ・\ ``EXPECTED_COMPLETE_TABLE``\ ）の記述例を、用途ごとに示す。記法の仕様は\ :ref:`テーブルのデータを記述する <testdata_notation-table_data>`\ を参照。

準備データ（SETUP_TABLE）を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
会員テーブル（\ ``MEMBER``\ ）に初期データを登録する例である。数値・小数・\ NULL\ ・バイナリといった、実際のテーブルで扱う値の種類を一通り含んでいる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  主キーカラム（この例では ``MEMBER_ID``\ ）は省略できない。

.. rubric:: Excel形式の場合

準備データの例を示す。カラム数が多いため、ここでは前半・後半に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 30,25,20,25

  * - SETUP_TABLE=MEMBER
    -
    -
    -
  * - MEMBER_ID
    - NAME
    - RANK
    - SCORE
  * - 0000000101
    - 山田太郎
    - 1
    - 85000
  * - 0000000102
    - 鈴木花子
    - 2
    - Null

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,15,25,35

  * - SETUP_TABLE=MEMBER
    -
    -
    -
  * - MEMBER_ID
    - RATE
    - PROFILE
    - PHOTO
  * - 0000000101
    - 1.5
    - ゴールド会員です
    - ${binaryFile:testdata.txt}
  * - 0000000102
    - 2.25
    - シルバー会員
    - ${binaryFile:member_photo.jpg}

``SCORE``\ カラムの ``Null``\ は\ Java\ の\ null\ として登録される。\ ``PHOTO``\ カラムの ``${binaryFile:パス}``\ は、指定したファイルの内容をバイナリとして読み込む記法である。

.. rubric:: YAML形式の場合

``setup_tables:``\ の ``rows:``\ に、1行を1つのオブジェクトとして記述する。

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

``SCORE``\ カラムのようにアンクォートの ``null``\ を記述すると\ Java\ の\ null\ になる。\ ``"null"``\ とクォートした場合は、文字列の ``null``\ になる。

期待値（EXPECTED_TABLE・EXPECTED_COMPLETE_TABLE）を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バッチ処理の実行後に、会員テーブル（\ ``MEMBER``\ ）のスコアと注文ヘッダテーブル（\ ``ORDER_HEADER``\ ）の状態を検証する例である。会員テーブルは検証したいカラムだけを記述して ``EXPECTED_TABLE``\ で比較し、注文ヘッダテーブルは書かなかったカラムにデフォルト値が入っていることまで含めて ``EXPECTED_COMPLETE_TABLE``\ で比較している。ここでいう「書かない」とはカラム名自体を書かないことであり、カラム名を書いたうえで値だけを空にした場合はデフォルト値の補完対象にならない。期待値の行は主キーで突き合わされるため記述順は問わないが、テーブルに存在する行は漏れなく記述する必要がある。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  Excel\ 形式では、\ ``EXPECTED_TABLE``\ と ``EXPECTED_COMPLETE_TABLE``\ をデータタイプごとにまとめて記述する（\ :ref:`グループIDによる使い分け <testdata_notation-group_id>`\ 参照）。

.. rubric:: Excel形式の場合

省略したカラムを比較対象から外す期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 22,18,12,18,30

  * - EXPECTED_TABLE=MEMBER
    -
    -
    -
    -
  * - MEMBER_ID
    - NAME
    - RANK
    - SCORE
    - UPDATED_DATE
  * - 0000000101
    - 山田太郎
    - 1
    - 87500
    - 2024-04-01 09:00:00.0
  * - 0000000102
    - 鈴木花子
    - 2
    - 42000
    - 2024-04-01 09:00:00.0

省略したカラムにデフォルト値を補完して比較する期待値の例を示す。ここでは ``UPDATE_DATE``\ カラムをカラム名の行に書いていない。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - EXPECTED_COMPLETE_TABLE=ORDER_HEADER
    -
    -
  * - ORDER_ID
    - ITEM_COUNT
    - STATUS
  * - 10001
    - 3
    - 1
  * - 10002
    - 5
    - 1

.. rubric:: YAML形式の場合

``expected_tables:``\ と ``expected_complete_tables:``\ は別のトップレベルキーであるため、同じファイルに並べて記述できる。

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

  # UPDATE_DATE はどの行にも書かないため、デフォルト値が格納されているものとして比較される
  expected_complete_tables:
    - table: ORDER_HEADER
      rows:
        - ORDER_ID: "10001"
          ITEM_COUNT: "3"
          STATUS: "1"
        - ORDER_ID: "10002"
          ITEM_COUNT: "5"
          STATUS: "1"

.. _testdata_examples-empty_table:

0件のテーブルデータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
注文ヘッダテーブル（\ ``ORDER_HEADER``\ ）を空にした状態で、処理対象のデータが1件もない場合のバッチ処理を実行し、処理後もこのテーブルにレコードが1件もないことを検証する例である。準備データを0件にすることでテーブルが空になり、期待値を0件にすることで1件もないことの検証になる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - SETUP_TABLE=ORDER_HEADER
    -
    -
  * - ORDER_ID
    - ITEM_COUNT
    - STATUS

期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - EXPECTED_TABLE=ORDER_HEADER
    -
    -
  * - ORDER_ID
    - ITEM_COUNT
    - STATUS

いずれもカラム名の行までを記述し、データ行を記述していない。

カラム名を1つも書かない場合は、カラム名の行にマーカーカラムを1つだけ置く。次の例では\ ``[EMPTY]``\ を置いている。半角角括弧で囲んであれば名前は何でもよい。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - SETUP_TABLE=ORDER_HEADER
    -
    -
  * - [EMPTY]
    -
    -

.. rubric:: YAML形式の場合

``rows:``\ に空配列を記述する。

.. code-block:: yaml

  setup_tables:
    - table: ORDER_HEADER
      rows: []

  expected_tables:
    - table: ORDER_HEADER
      rows: []

採番処理のテストデータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テーブル採番を使う処理では、採番用テーブルの準備データと期待値、および採番した値が登録される業務テーブルの期待値を記述する。ここでは、採番対象\ ID\ が ``1101``\ の採番処理をテストする例を示す。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. tip::

  この記述例は、テスト内で採番処理が1度だけ行われることを想定している。このため、採番用テーブルの期待値は「準備データの値 + 1」になっている。

.. rubric:: Excel形式の場合

採番用テーブルの準備データの例を示す。準備データには、テスト範囲で使用する採番対象のレコードだけを記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 50,50

  * - SETUP_TABLE=TEST_SBN_TBL
    -
  * - ID_COL
    - NO_COL
  * - 1101
    - 100

採番用テーブルの期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 50,50

  * - EXPECTED_TABLE=TEST_SBN_TBL
    -
  * - ID_COL
    - NO_COL
  * - 1101
    - 101

採番した値が登録される業務テーブルの期待値の例を示す。\ ``USER_ID``\ に採番された値が登録される。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - EXPECTED_TABLE=USER_INFO
    -
    -
  * - USER_ID
    - KANJI_NAME
    - KANA_NAME
  * - 0000000101
    - 漢字名
    - ｶﾅﾒｲ

.. rubric:: YAML形式の場合

同じ内容を\ YAML\ 形式で記述すると、以下のようになる。

.. code-block:: yaml

  setup_tables:
    - table: TEST_SBN_TBL
      rows:
        - ID_COL: "1101"
          NO_COL: "100"

  expected_tables:
    - table: TEST_SBN_TBL
      rows:
        - ID_COL: "1101"
          NO_COL: "101"
    - table: USER_INFO
      rows:
        - USER_ID: "0000000101"
          KANJI_NAME: "漢字名"
          KANA_NAME: "ｶﾅﾒｲ"

.. _testdata_examples-file_data:

ファイルのデータを記述する
--------------------------------------------------
固定長ファイル・可変長ファイルのテストデータの記述例を、用途ごとに示す。記法の仕様は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

Excel\ 形式では、レコード種別行の先頭要素にレコード種別を、以降の要素にフィールド名称を記述する。同じ内容を表す\ Excel\ 形式の行と\ YAML\ 形式のキーの対応は、以下のとおりである。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 50,50

  * - Excel\ 形式の行
    - YAML\ 形式のキー
  * - 識別子行（「SETUP_FIXED[グループID]=ファイルパス」）
    - ``path``\ ・\ ``type``\ ・\ ``group_id``
  * - レコード種別行
    - ``record_type``\ ・\ ``fields:``\ の ``name``
  * - データ型行・フィールド長行
    - ``fields:``\ の ``type``\ ・\ ``length``
  * - データ行
    - ``rows:``\ の値の配列

固定長ファイルを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定長の入力ファイルを読み込んで処理し、結果を固定長の出力ファイルに書き出すバッチ処理を検証する例である。準備用のファイルと期待値のファイルは、データタイプだけが異なる同じ書式で記述する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

入力ファイルの例を示す。データ行の先頭要素は空にする。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_FIXED=work/input.txt
    -
    -
    -
  * - データ
    - ID
    - COUNTER
    - MESSAGE
  * -
    - 半角
    - 数値
    - 半角
  * -
    - 5
    - 5
    - 10
  * -
    - 10001
    - 10
    - hello
  * -
    - 10002
    - 20
    - good bye.

出力ファイルの期待値は、同じ書式で記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - EXPECTED_FIXED=work/output.txt
    -
    -
    -
  * - データ
    - ID
    - COUNTER
    - MESSAGE
  * -
    - 半角
    - 数値
    - 半角
  * -
    - 5
    - 5
    - 10
  * -
    - 10001
    - 11
    - HELLO
  * -
    - 10002
    - 21
    - GOOD BYE.

.. rubric:: YAML形式の場合

``setup_files:``\ ・\ ``expected_files:``\ の各エントリに、\ ``path``\ ・\ ``type``\ ・\ ``records``\ を記述する。

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

可変長ファイルを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CSV\ 形式の顧客データファイルを入力として使う例である。固定長との違いは、フィールド長を記述しない点と、フィールド区切り文字をディレクティブで指定する点である。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

入力ファイルの例を示す。可変長ファイルではフィールド長行を記述しない。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_VARIABLE=input/data.csv
    -
    -
    -
  * - field-separator
    - ,
    -
    -
  * - DATA
    - USER_ID
    - USER_NAME
    - AMOUNT
  * -
    - 半角
    - 全角
    - 半角
  * -
    - 001
    - 山田太郎
    - 5000
  * -
    - 002
    - 鈴木花子
    - 3000

.. rubric:: YAML形式の場合

``type: variable``\ を指定し、\ ``fields:``\ の各要素から ``length``\ を省略する。

.. code-block:: yaml

  setup_files:
    - path: input/data.csv
      type: variable
      directives:
        field-separator: ","
      records:
        - record_type: DATA
          fields:
            - {name: USER_ID,   type: 半角}
            - {name: USER_NAME, type: 全角}
            - {name: AMOUNT,    type: 半角}
          rows:
            - ["001", "山田太郎", "5000"]
            - ["002", "鈴木花子", "3000"]

複数レコードレイアウトを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ヘッダレコードとデータレコードが混在する振込依頼ファイルを扱う例である。1つのデータブロックの中に、レコードレイアウトを複数記述する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  1つの固定長ファイルのデータブロック内では、全てのレコードレイアウトのレコード長を一致させる。この例では、フィールド長の合計が40バイトになるよう、ヘッダレコードに\ FILLER\ を置いて調整している。

.. rubric:: Excel形式の場合

入力ファイルの例を示す。データ行の後に新しいレコード種別行を続けて書くと、そこから次のレコードレイアウトとして扱われる。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_FIXED=input/multi.dat
    -
    -
    -
  * - HEADER
    - SEQ
    - TYPE
    - FILLER
  * -
    - 半角
    - 半角
    - 半角
  * -
    - 4
    - 2
    - 34
  * -
    - H001
    - 01
    -
  * - DATA
    - USER_ID
    - AMOUNT
    - NOTE
  * -
    - 半角
    - 数値
    - 全角
  * -
    - 10
    - 10
    - 20
  * -
    - 001
    - 5000
    - 備考

.. rubric:: YAML形式の場合

``records:``\ 配列に、レコードレイアウトを複数並べて記述する。

.. code-block:: yaml

  setup_files:
    - path: input/multi.dat
      type: fixed
      records:
        - record_type: HEADER
          fields:
            - {name: SEQ,    type: 半角, length: 4}
            - {name: TYPE,   type: 半角, length: 2}
            - {name: FILLER, type: 半角, length: 34}
          rows:
            - ["H001", "01", ""]
        - record_type: DATA
          fields:
            - {name: USER_ID, type: 半角, length: 10}
            - {name: AMOUNT,  type: 数値, length: 10}
            - {name: NOTE,    type: 全角, length: 20}
          rows:
            - ["001", "5000", "備考"]

固定長ファイルのディレクティブを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文字エンコーディングとゾーン10進数の正符号ニブルを明示して、顧客データファイルを読み込む例である。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

入力ファイルの例を示す。ディレクティブ行はレコード定義より前に置く。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_FIXED=input/data.dat
    -
    -
    -
  * - text-encoding
    - MS932
    -
    -
  * - positive-zone-sign-nibble
    - C
    -
    -
  * - DATA
    - USER_ID
    - USER_NAME
    - AMOUNT
  * -
    - 半角
    - 全角
    - 数値
  * -
    - 10
    - 20
    - 10
  * -
    - 001
    - 山田太郎
    - 5000
  * -
    - 002
    - 鈴木花子
    - 3000

.. rubric:: YAML形式の場合

``directives:``\ オブジェクトに ``key: value``\ 形式で記述する。

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
            - {name: USER_ID,   type: 半角, length: 10}
            - {name: USER_NAME, type: 全角, length: 20}
            - {name: AMOUNT,    type: 数値, length: 10}
          rows:
            - ["001", "山田太郎", "5000"]
            - ["002", "鈴木花子", "3000"]

可変長ファイルのディレクティブを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
タブ区切り・\ CRLF\ 改行のファイルを扱う例である。タブ文字の記述方法は形式によって異なる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

入力ファイルの例を示す。タブ文字はセルに ``\t``\ （バックスラッシュと ``t``\ の2文字）と入力する。テスティングフレームワークがタブ文字に変換する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 34,33,33

  * - SETUP_VARIABLE=input/data.tsv
    -
    -
  * - field-separator
    - \\t
    -
  * - record-separator
    - CRLF
    -
  * - DATA
    - FIELD1
    - FIELD2
  * -
    - 半角
    - 半角
  * -
    - value1
    - value2

.. rubric:: YAML形式の場合

タブ文字は ``"\\t"``\ と記述する。\ YAML\ の ``"\t"``\ は実際のタブ文字になってしまうため、バックスラッシュをエスケープする。\ ``record-separator``\ も同様に、\ ``"\r\n"``\ と記述すると実際の制御文字になり、値が除去されて区切りが無くなる。この場合はエラーにならないため、改行コードは ``CRLF``\ のようにシンボルで指定する。

.. code-block:: yaml

  setup_files:
    - path: input/data.tsv
      type: variable
      directives:
        field-separator: "\\t"
        record-separator: CRLF
      records:
        - record_type: DATA
          fields:
            - {name: FIELD1, type: 半角}
            - {name: FIELD2, type: 半角}
          rows:
            - ["value1", "value2"]

カンマを含む値を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CSV\ 形式のファイルで、フィールドの値そのものにカンマが含まれる場合の例である。\ ``quoting-delimiter``\ ディレクティブを指定すると、ダブルクォートで囲まれた範囲のカンマが区切り文字として扱われなくなる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. tip::

  クォートで囲まれた範囲の中にダブルクォート文字そのものを含めたい場合は、\ ``""``\ と二重に記述してエスケープする（\ RFC 4180\ に準拠する）。

.. rubric:: Excel形式の場合

期待値の例を示す。\ ``quoting-delimiter``\ に指定できるのは1文字だけである。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - EXPECTED_VARIABLE=output/data.csv
    -
    -
    -
  * - field-separator
    - ,
    -
    -
  * - quoting-delimiter
    - ``"``
    -
    -
  * - DATA
    - USER_ID
    - NOTE
    - AMOUNT
  * -
    - 半角
    - 半角
    - 半角
  * -
    - 001
    - ``"hello, world"``
    - 5000

.. rubric:: YAML形式の場合

``quoting-delimiter``\ には ``"\""``\ と記述する。値そのものにはダブルクォートを付けない。\ Excel\ 形式ではセルに書いた外側のダブルクォート1層が読み込み時に除去されるが、\ YAML\ 形式ではこの除去が行われないため、囲みを外した値を記述する。

.. code-block:: yaml

  expected_files:
    - path: output/data.csv
      type: variable
      directives:
        field-separator: ","
        quoting-delimiter: "\""
      records:
        - record_type: DATA
          fields:
            - {name: USER_ID, type: 半角}
            - {name: NOTE,    type: 半角}
            - {name: AMOUNT,  type: 半角}
          rows:
            - ["001", "hello, world", "5000"]

グループIDでファイルを使い分ける
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストショットごとに異なる入力ファイルを使い分ける例である。グループIDなしのデータブロックが1件処理に、\ ``case2``\ のデータブロックが複数件処理に対応する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

グループIDなしの入力ファイルの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_FIXED=work/input.txt
    -
    -
    -
  * - データ
    - ID
    - COUNTER
    - MESSAGE
  * -
    - 半角
    - 数値
    - 半角
  * -
    - 5
    - 5
    - 10
  * -
    - 10001
    - 10
    - hello

グループID付きの入力ファイルの例を示す。同じファイルパスであっても、グループIDが異なれば別のデータブロックとして扱われる。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_FIXED[case2]=work/input.txt
    -
    -
    -
  * - データ
    - ID
    - COUNTER
    - MESSAGE
  * -
    - 半角
    - 数値
    - 半角
  * -
    - 5
    - 5
    - 10
  * -
    - 20001
    - 30
    - morning
  * -
    - 20002
    - 40
    - evening

.. rubric:: YAML形式の場合

グループIDなしのエントリとグループID付きのエントリを、同じ ``setup_files:``\ のリストに並べて記述する。

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
            - ["20002", "40", "evening"]

空ファイルを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
0バイトの空ファイルを表現する例である。レコード定義を持たないデータブロックとして記述する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

「SETUP_FIXED=input/empty.dat」の行に続けてディレクティブ行「text-encoding | MS932」だけを記述し、レコード定義以降は記述しない。

.. rubric:: YAML形式の場合

``records:``\ に空配列を記述する。

.. code-block:: yaml

  setup_files:
    - path: input/empty.dat
      type: fixed
      directives:
        text-encoding: MS932
      records: []

.. _testdata_examples-messaging_data:

メッセージングのデータを記述する
--------------------------------------------------
要求電文・応答電文のテストデータの記述例を、用途ごとに示す。記法の仕様は\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。

要求電文・応答電文を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
同期応答メッセージ受信のテストで、受信する要求電文と、それに対する応答電文の期待値を記述する例である。データタイプ ``MESSAGE``\ の識別子は固定であり、要求電文には ``setUpMessages``\ 、応答電文の期待値には ``expectedMessages``\ を使う。要求電文には、電文全体で共通のディレクティブとフレームワーク制御ヘッダを付ける。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

要求電文の例を示す。メッセージボディの先頭要素はラベル列であり、フィールド名称行には慣行として ``no``\ と記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,30,30,30

  * - MESSAGE=setUpMessages
    -
    -
    -
  * - text-encoding
    - Windows-31J
    -
    -
  * - requestId
    - hoge
    -
    -
  * - userId
    - moge
    -
    -
  * - no
    - ユーザ名
    - 備考
    - FILLER
  * -
    - 全角
    - 全角
    - 半角
  * -
    - 50
    - 200
    - 252
  * - 1
    - 電文太郎
    - 特筆なし
    -
  * - 2
    -
    - ユーザ名が空欄なのでエラーが発生します。
    -

応答電文の期待値は、同じ書式で記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,30,30,30

  * - MESSAGE=expectedMessages
    -
    -
    -
  * - no
    - 処理結果コード
    - 会員ID
    - FILLER
  * -
    - 半角
    - 半角
    - 半角
  * -
    - 2
    - 10
    - 490
  * - 1
    - 00
    - 1234567890
    -
  * - 2
    - 01
    -
    -

.. rubric:: YAML形式の場合

``messages:``\ の下に電文ごとのエントリを並べ、ディレクティブは ``directives:``\ に、フレームワーク制御ヘッダは ``fw_header:``\ に記述する。\ ``rows:``\ には\ Excel\ 形式のようなラベル列を置かない。

.. code-block:: yaml

  messages:
    - id: setUpMessages
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
    - id: expectedMessages
      records:
        - record_type: default
          fields:
            - {name: 処理結果コード, type: 半角, length: 2}
            - {name: 会員ID,         type: 半角, length: 10}
            - {name: FILLER,         type: 半角, length: 490}
          rows:
            - ["00", "1234567890", ""]
            - ["01", "", ""]

JSON・XMLの電文を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSON\ ・\ XML\ の電文を、同期応答メッセージ受信のテストで記述する例である。固定長の電文と違い、電文長がテストショットごとに変わるため、メッセージボディのフィールド長には\ ``"-"``\ を指定する。1つのフィールドに記述すると可読性が落ちる場合は、電文を複数のフィールドに分割する（フィールド名は任意でよい）。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  JSON\ ・\ XML\ を使用する場合は、\ ``file-type``\ ディレクティブを指定して電文全体を文字列としてアサートする。理由と、\ ``file-type``\ の値によるアサート方法の違いは\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。

.. rubric:: Excel形式の場合

要求電文の例を示す。フィールド長行にはフィールドの数だけ\ ``-``\ を記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,30,30,30

  * - MESSAGE=setUpMessages
    -
    -
    -
  * - text-encoding
    - UTF-8
    -
    -
  * - file-type
    - XML
    -
    -
  * - requestId
    - RM11AD0102
    -
    -
  * - no
    - XML1
    - XML2
    - XML3
  * -
    - 全半角
    - 全半角
    - 全半角
  * -
    - ``-``
    - ``-``
    - ``-``
  * - 1
    - ``<?xml version="1.0" encoding="UTF-8"?><request>``
    - ``<userId>0000000101</userId><userName>電文太郎</userName>``
    - ``</request>``

応答電文の期待値は、同じ書式で記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,30,30,30

  * - MESSAGE=expectedMessages
    -
    -
    -
  * - no
    - XML1
    - XML2
    - XML3
  * -
    - 全半角
    - 全半角
    - 全半角
  * -
    - ``-``
    - ``-``
    - ``-``
  * - 1
    - ``<?xml version="1.0" encoding="UTF-8"?><response>``
    - ``<statusCode>200</statusCode><userId>0000000101</userId>``
    - ``</response>``

.. tip::

  フィールド長に\ ``"-"``\ を指定したフィールドでは、値に含まれる改行とその前後の空白が取り除かれる。長い電文は、セル内で改行（\ Alt+Enter\ ）して読みやすく折り返して記述できる。上の表はセル内の改行を示せないため、1行に詰めた状態で示している。

.. rubric:: YAML形式の場合

``length``\ には文字列として ``"-"``\ を記述する。クォートを外すと\ YAML\ の記法上の意味を持つため、必ずダブルクォートで囲む。

.. code-block:: yaml

  messages:
    - id: setUpMessages
      directives:
        text-encoding: UTF-8
        file-type: XML
      fw_header:
        requestId: RM11AD0102
      records:
        - record_type: default
          fields:
            - {name: XML1, type: 全半角, length: "-"}
            - {name: XML2, type: 全半角, length: "-"}
            - {name: XML3, type: 全半角, length: "-"}
          rows:
            - ["<?xml version=\"1.0\" encoding=\"UTF-8\"?><request>",
               "<userId>0000000101</userId><userName>電文太郎</userName>",
               "</request>"]
    - id: expectedMessages
      records:
        - record_type: default
          fields:
            - {name: XML1, type: 全半角, length: "-"}
            - {name: XML2, type: 全半角, length: "-"}
            - {name: XML3, type: 全半角, length: "-"}
          rows:
            - ["<?xml version=\"1.0\" encoding=\"UTF-8\"?><response>",
               "<statusCode>200</statusCode><userId>0000000101</userId>",
               "</response>"]

同期応答メッセージ送信の要求電文の期待値を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarch\ バッチアプリケーションのリクエスト単体テストで、送信される要求電文のヘッダが期待どおりであることを検証する例である。テストショット一覧の ``expectedMessage``\ カラムに記述したグループIDと、要求電文の期待値のデータブロックが紐付く。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  要求電文ヘッダと要求電文本文のデータ件数は一致させる。

.. rubric:: Excel形式の場合

テストショット一覧の記述例は\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ を参照。要求電文ヘッダの期待値の例を示す。半角角括弧の中がグループID、\ ``=``\ の右がリクエスト\ ID\ である。リクエスト\ ID\ はフォーマット定義ファイルの解決に使われる。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 20,80

  * - EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM21AA0104_01
    -
  * - text-encoding
    - ms932
  * - no
    - requestId
  * -
    - 半角
  * -
    - 20
  * - 1
    - RM21AA0104_01

.. rubric:: YAML形式の場合

``expected_request_header_messages:``\ のエントリに、\ ``group_id:``\ とリクエスト\ ID\ （\ ``id:``\ ）を記述する。\ ``group_id:``\ の値がテストショット一覧の ``expectedMessage``\ カラムに対応する。\ ``record_type:``\ には、\ Excel\ 形式のフィールド名称行の先頭要素がそのまま入る。同期応答メッセージ送信で使う4つのデータタイプでは記載した値がそのままレコード種別になるため、慣行に従って ``no``\ と記載した\ Excel\ 形式に合わせて ``"no"``\ と記述する（\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ 参照）。

.. code-block:: yaml

  expected_request_header_messages:
    - group_id: case1
      id: RM21AA0104_01
      directives:
        text-encoding: ms932
      records:
        - record_type: "no"
          fields:
            - {name: requestId, type: 半角, length: 20}
          rows:
            - ["RM21AA0104_01"]

.. _testdata_examples-send_sync_response:

同期応答メッセージ送信の応答電文を配置する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
同期応答メッセージ送信の取引単体テストで、モックアップクラスが返す応答電文を、リクエスト\ ID\ ごとの決まった場所に配置する例である。配置先は、コンポーネント設定ファイルで ``sendSyncTestData``\ というキーに設定したベースディレクトリである。その配下に、リクエスト\ ID\ と同じ名前の読み込み単位（\ Excel\ 形式ではリクエスト\ ID\ と同じ名前のファイルの ``message``\ シート、\ YAML\ 形式ではリクエスト\ ID\ と同じ名前のディレクトリ配下の ``message.yaml``\ ）を置き、その中に応答電文のデータブロックを記述する。ここでは応答電文本文を例に、\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  ``errorMode:``\ による障害系テストの値を記述できるのは、応答電文（\ ``RESPONSE_HEADER_MESSAGES``\ ・\ ``RESPONSE_BODY_MESSAGES``\ ）のデータブロックだけである。要求電文の期待値は障害の発生契機にならない。値は応答電文のヘッダと本文の両方に記述する。

.. rubric:: Excel形式の場合

``sendSyncTestData``\ 配下の ``REQ001.xls``\ の ``message``\ シートに記述する。\ ``=``\ の右がリクエスト\ ID\ である。先頭列はラベル列であり、フィールド名称行には慣行として ``no``\ と記述し（この値がそのままレコード種別になる）、データ行には送信順序と一致する連番を記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,30,30,30

  * - RESPONSE_BODY_MESSAGES=REQ001
    -
    -
    -
  * - no
    - errorMode
    - field1
    - field2
  * -
    - 半角
    - 半角
    - 半角
  * -
    - 10
    - 10
    - 10
  * - 1
    -
    - value1
    - value2
  * - 2
    -
    - value3
    - value4

.. rubric:: YAML形式の場合

``sendSyncTestData``\ 配下の ``REQ001/message.yaml``\ に、\ ``response_body_messages:``\ のエントリとして記述する。\ ``id:``\ にはリクエスト\ ID\ を記述する。\ Excel\ 形式のラベル列に相当するフィールドは置かず、連番は ``rows:``\ の記述順から自動的に付与される。

.. code-block:: yaml

  response_body_messages:
    - id: REQ001
      records:
        - record_type: "no"
          fields:
            - {name: errorMode, type: 半角, length: 10}
            - {name: field1,    type: 半角, length: 10}
            - {name: field2,    type: 半角, length: 10}
          rows:
            - ["", "value1", "value2"]
            - ["", "value3", "value4"]

応答不要メッセージ送信の要求電文の期待値を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
応答不要メッセージ送信のリクエスト単体テストで、送信される要求電文が期待どおりであることを検証する例である。応答電文が存在しないため、テストショット一覧の ``responseMessage``\ と応答電文のデータブロック（\ ``RESPONSE_HEADER_MESSAGES``\ ・\ ``RESPONSE_BODY_MESSAGES``\ ）は記述しない。テストショット一覧には、電文のリクエスト\ ID\ を渡す ``messageRequestId``\ カラムを追加し、\ ``expectedMessage``\ に記述したグループIDで要求電文の期待値と対応付ける。要求電文の期待値は、ヘッダと本文の両方を記述する。記述方法は\ :ref:`リクエスト単体テストの実施（Nablarchバッチアプリケーション） <request_unit_test_batch>`\ を参照。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. tip::

  異常系のテストでは、テストショット一覧に ``errorCase``\ カラムを追加して ``true``\ を記述する。電文が送信されないため、要求電文の期待値は記述しない。

.. rubric:: Excel形式の場合

テストショット一覧のうち、応答不要メッセージ送信に固有のカラムを示す。テストショット一覧全体の記述例は\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ を参照。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,45,45

  * - LIST_MAP=testShots
    -
    -
  * - no
    - messageRequestId
    - expectedMessage
  * - 1
    - RM11AC0301
    - case1

要求電文ヘッダの期待値の例を示す。半角角括弧の中がグループID、\ ``=``\ の右がリクエスト\ ID\ である。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,45,45

  * - EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM11AC0301
    -
    -
  * - text-encoding
    - ms932
    -
  * - no
    - requestId
    - userId
  * -
    - 半角
    - 半角
  * -
    - 20
    - 20
  * - 1
    - RM11AC0301
    - batch_user

要求電文本文の期待値は、同じグループID・リクエスト\ ID\ で記述する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,45,45

  * - EXPECTED_REQUEST_BODY_MESSAGES[case1]=RM11AC0301
    -
    -
  * - no
    - 会員ID
    - 会員名
  * -
    - 半角
    - 全角
  * -
    - 10
    - 50
  * - 1
    - 1234567890
    - 電文太郎

.. rubric:: YAML形式の場合

テストショット一覧は ``list_maps:``\ の ``id: testShots``\ のエントリに、要求電文の期待値は ``expected_request_header_messages:``\ ・\ ``expected_request_body_messages:``\ のエントリに記述する。\ ``group_id:``\ の値がテストショット一覧の ``expectedMessage``\ カラムに対応する。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          messageRequestId: "RM11AC0301"
          expectedMessage: "case1"

  expected_request_header_messages:
    - group_id: case1
      id: RM11AC0301
      directives:
        text-encoding: ms932
      records:
        - record_type: "no"
          fields:
            - {name: requestId, type: 半角, length: 20}
            - {name: userId,    type: 半角, length: 20}
          rows:
            - ["RM11AC0301", "batch_user"]

  expected_request_body_messages:
    - group_id: case1
      id: RM11AC0301
      records:
        - record_type: "no"
          fields:
            - {name: 会員ID, type: 半角, length: 10}
            - {name: 会員名, type: 全角, length: 50}
          rows:
            - ["1234567890", "電文太郎"]

ステータスコードを省略する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP\ メッセージ送信のテストで、応答電文にステータスコードのカラムを設けない例である。カラムがない場合、実行時にはデフォルト値の ``"200"``\ が使われる。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

応答電文本文の例を示す。\ ``=``\ の右はリクエスト\ ID\ である。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 20,80

  * - RESPONSE_BODY_MESSAGES=REQ001
    -
  * - no
    - body
  * -
    - 半角
  * -
    - 10
  * - 1
    - RESULT_OK

.. rubric:: YAML形式の場合

``response_body_messages:``\ のエントリに、リクエスト\ ID\ （\ ``id:``\ ）と応答電文本文を記述する。

.. code-block:: yaml

  response_body_messages:
    - id: REQ001
      records:
        - record_type: "no"
          fields:
            - {name: body, type: 半角, length: 10}
          rows:
            - ["RESULT_OK"]

.. _testdata_examples-special_notation:

null・空文字・改行など特殊な値を記述する
--------------------------------------------------
特殊記法を使う値の記述例を示す。記法の仕様は\ :ref:`null・空文字・改行など特殊な値を記述する <testdata_notation-special_notation>`\ を参照。

日付・システム日時・NULLを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
スケジュールテーブル（\ ``SCHEDULE``\ ）の期待値に、日付・タイムスタンプ・\ NULL\ ・システム日時を記述する例である。\ ``${systemTime}``\ はシステム日時に、\ ``${updateTime}``\ はその別名として、\ ``${setUpTime}``\ はコンポーネント設定ファイルに記述した固定値に、それぞれ変換される。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. important::

  ``java.sql.Timestamp``\ 型カラムの期待値には、この例の ``CREATED_AT``\ のように末尾へ ``.0``\ を付ける。

.. rubric:: Excel形式の場合

期待値の例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,25,30,35

  * - EXPECTED_TABLE=SCHEDULE
    -
    -
    -
  * - ID
    - EVENT_NAME
    - START_DATE
    - CREATED_AT
  * - 1
    - 会議
    - 2024-01-15
    - 2024-01-01 09:00:00.0
  * - 2
    - NULLテスト
    - NULL
    - NULL
  * - 3
    - システム時刻
    - ${systemTime}
    - ${systemTime}
  * - 4
    - 更新時刻
    - ${updateTime}
    - ${setUpTime}

.. rubric:: YAML形式の場合

NULL\ はアンクォートの ``null``\ で記述する。\ ``${systemTime}``\ などの特殊記法は、他の値と同様にダブルクォートで囲む。

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
        - ID: "4"
          EVENT_NAME: "更新時刻"
          START_DATE: "${updateTime}"
          CREATED_AT: "${setUpTime}"

空文字・改行を記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
備考テーブル（\ ``NOTE``\ ）の期待値に、空文字と改行を含む値を記述する例である。あわせて、可変長ファイルに全フィールドが空文字のレコードを記述する例を示す。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

期待値の例を示す。空文字は空セルで記述する。\ CR\ は ``\r``\ （バックスラッシュと ``r``\ の2文字）と入力する。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 15,25,60

  * - EXPECTED_TABLE=NOTE
    -
    -
  * - ID
    - TITLE
    - BODY
  * - 1
    -
    - 1行目\\r2行目
  * - 2
    - 補足なし
    -

LF\ を表したい場合は、セル内で改行する（\ Alt+Enter\ ）。セル内の改行は表では示せないため、上の例には含めていない。

全フィールドが空文字のレコードは、いずれか1つのフィールドに ``""``\ と記述する。全セルを空にした行は読み飛ばされ、レコードにならないためである。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 25,25,25,25

  * - SETUP_VARIABLE=input/data.csv
    -
    -
    -
  * - field-separator
    - ,
    -
    -
  * - DATA
    - USER_ID
    - USER_NAME
    - AMOUNT
  * -
    - 半角
    - 全角
    - 半角
  * -
    - 001
    - 山田太郎
    - 5000
  * -
    - ``""``
    -
    -

このテストデータから書き出されるファイルは、\ ``001,山田太郎,5000``\ に続けて区切り文字だけが並んだ ``,,``\ の行になり、空行にはならない。何も書かれていない行になるのは、フィールドが1つのファイルの場合だけである。

.. rubric:: YAML形式の場合

空文字は ``""``\ 、\ CR\ は ``"\r"``\ 、\ LF\ は ``"\n"``\ と記述する。\ YAML\ ではパーサがこれらを実際の制御文字に変換するため、\ Excel\ 形式のような2文字表記は使わない。

.. code-block:: yaml

  expected_tables:
    - table: NOTE
      rows:
        - ID: "1"
          TITLE: ""
          BODY: "1行目\r2行目"
        - ID: "2"
          TITLE: "補足なし"
          BODY: ""

Excel\ 形式ではセル内で改行する必要がある\ LF\ も、\ YAML\ 形式では他の値と同じように書ける。

.. code-block:: yaml

  expected_tables:
    - table: NOTE
      rows:
        - ID: "3"
          TITLE: ""
          BODY: "1行目\n2行目"

全フィールドが空文字のレコードは、\ ``rows:``\ の値をすべて ``""``\ とする。\ Excel\ 形式と違い、行が読み飛ばされることはない。

.. code-block:: yaml

  setup_files:
    - path: input/data.csv
      type: variable
      directives:
        field-separator: ","
      records:
        - record_type: DATA
          fields:
            - {name: USER_ID,   type: 半角}
            - {name: USER_NAME, type: 全角}
            - {name: AMOUNT,    type: 半角}
          rows:
            - ["001", "山田太郎", "5000"]
            - ["", "", ""]

書き出されるファイルは\ Excel\ 形式と同じく ``,,``\ の行になる。

スペース・ダブルクォートを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
商品テーブル（\ ``ITEM``\ ）の期待値に、半角スペース1文字とダブルクォート1文字を記述する例である。値が空欄なのか半角スペースなのかを、テストデータ上で区別できるようにする。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

期待値の例を示す。前後をダブルクォートで囲むと、外側の1層だけが除去される。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 20,40,40

  * - EXPECTED_TABLE=ITEM
    -
    -
  * - ID
    - NAME
    - MEMO
  * - 1
    - ``" "``
    - ``"""``

.. rubric:: YAML形式の場合

半角スペース1文字は ``" "``\ 、ダブルクォート1文字は ``"\""``\ または ``'"'``\ と記述する。

.. code-block:: yaml

  expected_tables:
    - table: ITEM
      rows:
        - ID: "1"
          NAME: " "
          MEMO: "\""

バイナリデータを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルテーブル（\ ``FILE_TABLE``\ ）の\ BLOB\ カラムにバイナリデータを記述する例である。値を直接記述する方法と、別のファイルの内容を読み込む方法がある。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 30,70

  * - SETUP_TABLE=FILE_TABLE
    -
  * - FILE_ID
    - FILE_DATA
  * - 001
    - 0xCAFEBABE
  * - 002
    - ${binaryFile:testdata.bin}

``0x``\ を先頭に付けた16進数はバイナリ値として解釈される。\ ``0x``\ がない場合は文字列としてエンコードされる。\ ``${binaryFile:パス}``\ は、テストデータファイルが置かれているディレクトリからの相対パスで指定する。

.. rubric:: YAML形式の場合

``setup_tables:``\ の ``rows:``\ に、\ Excel\ 形式と同じ値をダブルクォートで囲んで記述する。

.. code-block:: yaml

  setup_tables:
    - table: FILE_TABLE
      rows:
        - FILE_ID: "001"
          FILE_DATA: "0xCAFEBABE"
        - FILE_ID: "002"
          FILE_DATA: "${binaryFile:testdata.bin}"

文字列を増幅して記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
会員テーブル（\ ``MEMBER``\ ）の準備データに、桁数の上限いっぱいの値を ``${文字種,文字数}``\ で生成する例である。値そのものに意味がなく桁数だけを満たしたい場合に、実際の文字を並べずに済む。\ ``${半角数字,3}-${半角数字,4}``\ のように、文字列の一部にも使える。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 20,30,25,25

  * - SETUP_TABLE=MEMBER
    -
    -
    -
  * - MEMBER_ID
    - NAME
    - PROFILE
    - ZIP_CODE
  * - 0000000101
    - ${全角漢字,5}
    - ${半角英字,10}
    - ${半角数字,3}-${半角数字,4}

.. rubric:: YAML形式の場合

``setup_tables:``\ の ``rows:``\ に、\ Excel\ 形式と同じ値をダブルクォートで囲んで記述する。

.. code-block:: yaml

  setup_tables:
    - table: MEMBER
      rows:
        - MEMBER_ID: "0000000101"
          NAME: "${全角漢字,5}"
          PROFILE: "${半角英字,10}"
          ZIP_CODE: "${半角数字,3}-${半角数字,4}"

アップロードファイルを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルアップロード画面のリクエスト単体テストで、あらかじめ配置した画像ファイルを ``${attach:ファイルパス}``\ で指定する例である。リクエストパラメータ（\ ``requestParams``\ ）の値に記述する。ファイルパスは、テスト実行時のカレントディレクトリ（プロジェクトルートディレクトリ）からの相対パスで記述する。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

固定長ファイルや\ CSV\ ファイルをアップロードする場合は、ファイルを配置せずファイルの内容をテストデータに記述する方法を採れる。詳しくは :ref:`アップロードファイルを用意する <request_unit_test_web-upload_file>` を参照。

.. rubric:: Excel形式の場合

リクエストパラメータの例を示す。\ ``uploadFile``\ は、画面の ``input``\ タグの ``name``\ 属性である。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 10,25,65

  * - LIST_MAP=requestParams
    -
    -
  * - [no]
    - memberId
    - uploadFile
  * - 1
    - 0000000101
    - ${attach:src/test/resources/upload/member_photo.png}

.. rubric:: YAML形式の場合

``list_maps:``\ の ``id: requestParams``\ のエントリに、\ Excel\ 形式と同じ値をダブルクォートで囲んで記述する。

.. code-block:: yaml

  list_maps:
    - id: requestParams
      rows:
        - "[no]": "1"
          memberId: "0000000101"
          uploadFile: "${attach:src/test/resources/upload/member_photo.png}"

.. _testdata_examples-comment_and_marker:

コメント・マーカーカラム・空エントリを扱う
--------------------------------------------------
テストデータに補足情報を残す記法と、読み込みの対象外になるエントリの記述例を示す。記法の仕様は\ :ref:`コメント・マーカーカラム・空エントリを扱う <testdata_notation-comment_and_marker>`\ を参照。

コメントとマーカーカラムを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータの読み手のために、コメントとマーカーカラムで補足情報を残す例である。いずれも読み込みの対象外になるため、実際のデータには影響しない。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

準備データの例を示す。先頭要素が ``//``\ で始まる行は、行全体が読み飛ばされる。行の先頭以外の要素が ``//``\ で始まる場合は、その要素以降が切り捨てられる。半角角括弧で囲んだ ``[no]``\ ・\ ``[desc]``\ はマーカーカラムであり、データベースへの登録から除外される。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 22,20,15,20,23

  * - SETUP_TABLE=TEST_TABLE
    -
    -
    -
    -
  * - // この行はコメントです
    -
    -
    -
    -
  * - [no]
    - PK_COL1
    - PK_COL2
    - NUMBER_COL
    - [desc]
  * - 1
    - 0000000001
    - AB
    - 100
    - テスト1
  * - // この行もスキップされます
    -
    -
    -
    -
  * - 2
    - 0000000002
    - CD
    - 200
    - テスト2

.. rubric:: YAML形式の場合

コメントは\ YAML\ 標準の ``#``\ で記述する。行頭・行末のどちらにも書ける。マーカーカラムのキーは、\ YAML\ の配列構文との衝突を避けるためダブルクォートで囲む。

.. code-block:: yaml

  setup_tables:
    - table: TEST_TABLE
      rows:
        # この行はコメントです
        - "[no]": "1"
          PK_COL1: "0000000001"
          PK_COL2: "AB"
          NUMBER_COL: "100"  # 数値カラム
          "[desc]": "テスト1"
        - "[no]": "2"
          PK_COL1: "0000000002"
          PK_COL2: "CD"
          NUMBER_COL: "200"
          "[desc]": "テスト2"

空エントリを記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータの見やすさのために空行を挟む例である。全要素が空のエントリは読み飛ばされるため、データの区切りとして空行を入れても結果は変わらない。\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

.. rubric:: Excel形式の場合

準備データの例を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 0
  :widths: 30,70

  * - SETUP_TABLE=USER
    -
  * - USER_ID
    - NAME
  * - 001
    - 山田太郎
  * -
    -
  * - 002
    - 鈴木花子

.. rubric:: YAML形式の場合

YAML\ 形式では ``rows:``\ に空のエントリを書く機会はほとんどない。区切りとして空行を挟んでも、\ YAML\ の構文上は無視される。

.. code-block:: yaml

  setup_tables:
    - table: USER
      rows:
        - USER_ID: "001"
          NAME: "山田太郎"

        - USER_ID: "002"
          NAME: "鈴木花子"
