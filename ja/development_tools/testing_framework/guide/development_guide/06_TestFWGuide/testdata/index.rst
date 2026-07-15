.. _ntf_testdata:

============================
テストデータの記述方法
============================

テストデータは Excel または YAML ファイルで記述できる。

.. _ntf_testdata_overview:

テストデータの全体像
====================

テストコード（Java）がテストデータファイルを読み込み、DB へのデータ投入・入力ファイルの配置・期待値との比較を行う。テストデータには **テストケース**・**セットアップ**・**検証** の3用途のデータを記述し、いずれも **データブロック** 単位で管理する。

全体像
------

各用途とデータブロックの対応を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - 用途
     - 内容
     - 主なデータブロック
   * - テストケース
     - 1エントリ1ケースの実行条件（ウェブ:「ユーザ ID・期待ステータスコード・期待フォワード先 URI」、バッチ:「リクエストパス・ユーザ ID・DI コンフィグ・期待ステータスコード」など）
     - ``LIST_MAP=testShots``
   * - セットアップ
     - テスト前に投入するデータ（DB INSERT、固定長・可変長ファイルの入力）
     - ``SETUP_TABLE`` / ``SETUP_FIXED`` / ``SETUP_VARIABLE``
   * - 検証
     - テスト後の期待値（DB・出力ファイル・電文・ログ・検索結果）
     - ``EXPECTED_*`` / ``RESPONSE_*``

データの格納階層
----------------

データの格納階層は次のとおりである。テストクラス1つ分のデータが読み込み単位（Excel は1シート／YAML は1ファイル）に分かれ、その中に複数のデータブロックが共存する。

.. code-block:: text

    テストクラス（Excel:1ブック / YAML:1ディレクトリ）
    └── 読み込み単位（Excel:1シート / YAML:1ファイル）
         └── データブロック（種別 + 識別子）
              └── レコード定義 / フィールド / データ

データブロックは種別（ ``SETUP_TABLE`` など14種）と識別子の値（テーブル名・ファイルパス・ID など）の組み合わせで区別する。詳細は :ref:`ntf_testdata_data_blocks` を参照。

記述例
------

バッチ処理のリクエスト単体テストの例を以下に示す。1ファイルにテストケース・セットアップ・検証が共存する。

Excelの場合
~~~~~~~~~~~

各データブロックはシート先頭のラベルで種別が決まる。

.. code-block:: text

    LIST_MAP=testShots
    | no | description         | expectedStatusCode | setUpTable | expectedTable | diConfig                                 | requestPath       | userId | expectedLog |
    | 1  | 正しく更新されます  | 0                  | default    | default       | nablarch/test/core/batch/BatchSample.xml | DBtoDBBatchSample | test   | expectedLog |

    SETUP_TABLE=ORDER_HEADER
    | ORDER_ID | ITEM_COUNT | REMARKS    |
    | 10001    | 10         | 通常注文   |
    | 10002    | 20         | まとめ買い |

    EXPECTED_TABLE=ORDER_HEADER
    | ORDER_ID | ITEM_COUNT | REMARKS    | UPDATE_DATE           |
    | 10001    | 11         | 通常注文   | 2010-09-13 12:34:56.0 |
    | 10002    | 21         | まとめ買い | 2010-09-13 12:34:56.0 |

    LIST_MAP=expectedLog
    | message       | logLevel |
    | 注文ID[10001] | INFO     |
    | 注文ID[10002] | INFO     |

YAMLの場合
~~~~~~~~~~

各データブロックはトップレベルキーで種別が決まる。

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正しく更新されます"
            expectedStatusCode: "0"
            setUpTable: "default"
            expectedTable: "default"
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

- 種別はトップレベルキーで決まる: ``list_maps:`` の ``id: testShots`` がテストケース定義、 ``setup_tables:`` がセットアップ、 ``expected_tables:`` が検証である。
- ``id: expectedLog`` のような任意 ID の ``list_maps:`` エントリも同一ファイルに共存できる。
- 同一の ``list_maps:`` キーに複数エントリをリストとして並べる（YAML はトップレベルキーの重複不可のため）。

テストデータの基本構造
----------------------

テストデータはテストクラスと1対1で対応する。

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * - 形式
     - テストクラス対応
     - 読み込み単位
   * - Excel
     - 同名の1ブック（``.xls``）
     - 1シート
   * - YAML
     - 同名のディレクトリ
     - 1ファイル（Excel の1シートに相当）

ディレクトリ構成の例を以下に示す。

.. code-block:: text

    【Excel】                              【YAML】
    src/test/java/com/example/            src/test/java/com/example/
      FooTest.xls                           FooTest/
        ├── case01  ← シート                  ├── case01.yaml  ← ファイル
        └── case02  ← シート                  └── case02.yaml  ← ファイル

1読み込み単位の中に、テストケース・セットアップ・検証の複数データブロックを共存させて記述する。

YAML ファイルは **YAML 1.2** に準拠する。YAML 1.1 との主な違いとして、 ``yes`` / ``no`` / ``on`` / ``off`` は真偽値ではなく文字列として扱われる。

ファイルの読み込みルール
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 35 45

   * - 項目
     - Excel
     - YAML
   * - ファイルなし時
     - エラー
     - ファイルが存在しない、またはパース失敗時はエラー
   * - 空ファイル時
     - 空シートは存在しないシート扱い
     - 空ファイル（0バイト）は空データ扱い（エラーにならない）
   * - 値の書き方
     - セルは必ず **文字列書式** で記述する。数値・日付書式の動作は保証しない
     - 値は必ず **ダブルクォートで囲む**

.. _ntf_testdata_data_blocks:

データブロック
==============

各データブロックは **データブロック種別** と **識別子の値** の2要素で識別される。

識別の構成要素
--------------

データブロックの識別方法を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 形式
     - 記述方法
   * - Excel
     - データブロック先頭セルに ``データブロック種別=識別子の値`` と記述する。種別名で始まれば合致（前方一致）。例: ``SETUP_TABLE=USER_MASTER``
   * - YAML
     - 種別ごとの専用トップレベルキーを使用する。完全一致のため前方一致は発生しない

YAML のトップレベルキーとデータブロック種別の対応を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - データブロック種別
     - YAML キー
   * - ``SETUP_TABLE``
     - ``setup_tables``
   * - ``EXPECTED_TABLE``
     - ``expected_tables``
   * - ``EXPECTED_COMPLETE_TABLE``
     - ``expected_complete_tables``
   * - ``LIST_MAP``
     - ``list_maps``
   * - ``SETUP_FIXED`` / ``SETUP_VARIABLE``
     - ``setup_files``
   * - ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE``
     - ``expected_files``
   * - ``MESSAGE``
     - ``messages``
   * - ``EXPECTED_REQUEST_HEADER_MESSAGES``
     - ``expected_request_header_messages``
   * - ``EXPECTED_REQUEST_BODY_MESSAGES``
     - ``expected_request_body_messages``
   * - ``RESPONSE_HEADER_MESSAGES``
     - ``response_header_messages``
   * - ``RESPONSE_BODY_MESSAGES``
     - ``response_body_messages``

記述例を以下に示す。

Excelの場合
~~~~~~~~~~~

データブロック先頭セルに ``種別=識別子`` の形式で記述する。

.. code-block:: text

    SETUP_TABLE=USER_MASTER
    | USER_ID | USER_NAME |
    | 001     | 山田太郎  |

    EXPECTED_TABLE=USER_MASTER
    | USER_ID | USER_NAME |
    | 001     | 山田太郎  |

    LIST_MAP=testShots
    | no | description  |
    | 1  | 正常ケース   |

YAMLの場合
~~~~~~~~~~

種別ごとの専用トップレベルキーを使用する。

.. code-block:: yaml

    setup_tables:
      - table: USER_MASTER
        rows:
          - USER_ID: "001"
            USER_NAME: "山田太郎"

    expected_tables:
      - table: USER_MASTER
        rows:
          - USER_ID: "001"
            USER_NAME: "山田太郎"

    list_maps:
      - id: testShots
        rows:
          - no: "1"
            description: "正常ケース"

同種データブロックの記述ルール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **YAML**: 同一ファイル内のトップレベルキーの重複は禁止である。同種データは同一キーにリストとして並べる（重複時はエラー）。
- **Excel**: 同一シート内に同種データブロックを複数記述できる。DataType により全件収集または先着一致で収集される（下記 :ref:`ntf_testdata_data_blocks_notes` 参照）。

データブロック種別の一覧
------------------------

使用できる種別は以下の14種である。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - データブロック種別
     - 用途
     - 同一 ID が複数ある場合
   * - ``SETUP_TABLE``
     - INSERT 用テーブルデータ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_TABLE``
     - 比較用テーブルデータ（省略カラムは比較対象外）
     - 同じグループのものをすべて収集
   * - ``EXPECTED_COMPLETE_TABLE``
     - 比較用テーブルデータ（省略カラムにデフォルト値補完）
     - 同じグループのものをすべて収集
   * - ``LIST_MAP``
     - キーバリュー形式の汎用データ（テストケース定義・期待値等）
     - 最初の1件のみ有効（2件目以降は無視）
   * - ``SETUP_FIXED``
     - 固定長ファイルの入力データ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_FIXED``
     - 固定長ファイルの期待値データ
     - 同じグループのものをすべて収集
   * - ``SETUP_VARIABLE``
     - 可変長ファイルの入力データ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_VARIABLE``
     - 可変長ファイルの期待値データ
     - 同じグループのものをすべて収集
   * - ``MESSAGE``
     - メッセージング電文データ
     - 最初の1件のみ有効（2件目以降は無視）
   * - ``EXPECTED_REQUEST_HEADER_MESSAGES``
     - 要求電文ヘッダの期待値
     - グループID 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``EXPECTED_REQUEST_BODY_MESSAGES``
     - 要求電文ボディの期待値
     - グループID 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``RESPONSE_HEADER_MESSAGES``
     - 応答電文ヘッダデータ
     - グループID 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``RESPONSE_BODY_MESSAGES``
     - 応答電文ボディデータ
     - グループID 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``DEFAULT``
     - フレームワーク内部用（通常使用しない）
     - —

.. _ntf_testdata_data_blocks_notes:

同一ファイル（シート）内に複数のデータブロックを書く場合の注意
--------------------------------------------------------------

- **複数テーブルの INSERT**: ``setup_tables`` などの全件収集タイプは同一 グループID のものをすべて収集する。複数テーブルデータを並べて記述できる。
- **データタイプの混在順序（YAML）**: YAML はトップレベルのセクションキー（ ``expected_tables`` / ``expected_complete_tables`` 等）ごとに独立して取得する。記述順序や異なるセクションの交互記述に関わらず正しく読み込まれる。
- **``LIST_MAP`` / ``MESSAGE`` の重複 ID**: 同一 ID が複数ある場合は最初の1件のみ有効。2件目以降は無視される。

.. note::

  **Excel との違い**: Excel（旧形式）は行を順に読む方式のため、同一シート内で別のデータタイプを挟むと後半が読み込まれない制約があった。YAML はセクションキーで構造化されるためこの制約はなく、移行時にデータタイプごとにまとめ直す必要はない。

グループの指定方法（グループID）は :ref:`ntf_testdata_testshots` を参照。

.. _ntf_testdata_testshots:

テストケース定義
================

``testShots`` はテストケース定義の予約 ID である。フレームワークがこの ID を自動的に読み込み、各エントリを1テストケースとして実行する。

testShots
---------

``testShots`` の仕様を以下に記載する。

- テスト実行には ``testShots`` に1件以上のエントリが必要である（0件はエラー）。
- 旧称 ``testCases`` も動作するが、新規作成では ``testShots`` を使うこと。
- **Excel**: ``LIST_MAP=testShots`` データブロックに記述する。
- **YAML**: ``list_maps:`` 下の ``id: testShots`` エントリに記述する。

記述例は :ref:`ntf_examples_testshots_overview` を参照。

``testShots`` の1行が1テストケースとなる。カラムには値を直接書くものと、別データブロック（ ``LIST_MAP`` や各種テーブル／ファイル／電文ブロック）の グループID・名前を指す参照型がある。処理方式ごとに必須カラムとオプションカラムが定まる。

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
~~~~~~~~~~

ウェブ・バッチ・メッセージングで共通の必須カラムを以下に示す。エンティティバリデーションは別体系である（後述の :ref:`ntf_testshots_entity` を参照）。

記述例は :ref:`ntf_examples_testshots_common` を参照。

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

ウェブアプリケーション（HttpRequestTestSupport）
-------------------------------------------------

必須カラム
~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

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
     - この値と同じ グループID を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ グループID を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``expectedSearch``
     - 検索結果期待値の グループID（対応する ``LIST_MAP`` セクションを収集）
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
     - この値と同じ グループID を持つ要求電文セクション（ ``EXPECTED_REQUEST_HEADER/BODY_MESSAGES`` ）で検証
     - スキップ
   * - ``responseMessage``
     - この値と同じ グループID を持つ応答電文セクション（ ``RESPONSE_HEADER/BODY_MESSAGES`` ）をレスポンスとして返す
     - スキップ
   * - ``expectedMessageByClient``
     - HTTP 同期応答メッセージ送信の要求電文グループ ID
     - スキップ
   * - ``responseMessageByClient``
     - HTTP 同期応答メッセージ送信の応答電文グループ ID
     - スキップ

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    LIST_MAP=testShots
    | no | description | isValidToken | expectedStatusCode | forwardUri | context    |
    | 1  | 正常ケース  | 0            | 200                | /success   | context001 |
    | 2  | 認証エラー  | 0            | 400                | /error     | context002 |

    LIST_MAP=context001
    | REQUEST_ID | USER_ID | HTTP_METHOD |
    | REQ_001    | user001 | POST        |

YAMLの場合
^^^^^^^^^^

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
--------------------------------------

必須カラム
~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

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
     - この値と同じ グループID を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ グループID を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``setUpFile``
     - この値と同じ グループID を持つ ``SETUP_FIXED`` / ``SETUP_VARIABLE`` セクションを入力ファイルとして配置
     - スキップ
   * - ``expectedFile``
     - この値と同じ グループID を持つ ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE`` セクションで出力ファイルを検証
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
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    LIST_MAP=testShots
    | no | description        | expectedStatusCode | diConfig                                 | requestPath       | userId | setUpFile |
    | 1  | 正しく更新されます | 0                  | nablarch/test/core/batch/BatchSample.xml | DBtoDBBatchSample | test   |           |
    | 2  | 入力ファイルあり   | 0                  | nablarch/test/core/batch/BatchSample.xml | FileToFileBatch   | test   | case2     |

YAMLの場合
^^^^^^^^^^

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
----------------------------------------------

必須カラム
~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

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
     - この値と同じ グループID を持つ ``SETUP_TABLE`` セクションを収集して INSERT
     - スキップ
   * - ``expectedTable``
     - この値と同じ グループID を持つ ``EXPECTED_TABLE`` / ``EXPECTED_COMPLETE_TABLE`` セクションで DB を検証
     - スキップ
   * - ``expectedMessage``
     - この値と同じ グループID を持つ要求電文セクション（ ``EXPECTED_REQUEST_HEADER/BODY_MESSAGES`` ）で検証
     - スキップ
   * - ``responseMessage``
     - この値と同じ グループID を持つ応答電文セクション（ ``RESPONSE_HEADER/BODY_MESSAGES`` ）をレスポンスとして返す
     - スキップ
   * - ``expectedLog``
     - 期待ログの ``LIST_MAP`` 名。指定した LIST_MAP が空の場合はエラー
     - スキップ

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    LIST_MAP=testShots
    | no | description      | expectedStatusCode | diConfig                              | requestPath | userId     | expectedMessage | responseMessage |
    | 1  | 電文送受信テスト | 0                  | batch-test-component-configuration.xml | BM21AA0106  | batch_user | case1           | res_case1       |

YAMLの場合
^^^^^^^^^^

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

エンティティバリデーション（EntityTestSupport）
------------------------------------------------

共通カラムとは別体系である。 ``no`` / ``description`` / ``expectedStatusCode`` は使用しない。

必須カラム
~~~~~~~~~~

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
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 予約 ID
     - 説明
   * - ``params``
     - 入力パラメータ定義。 ``testShots`` の行数と一致が必須

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    LIST_MAP=testShots
    | title    | expectedMessageId1 | propertyName1 |
    | 必須チェック | errors.required  | userName      |

YAMLの場合
^^^^^^^^^^

.. code-block:: yaml

    list_maps:
      - id: testShots
        rows:
          - title: "必須チェック"
            expectedMessageId1: "errors.required"
            propertyName1: "userName"

データブロックのグループ化
--------------------------

複数のテストケースで異なるセットアップデータや期待値を使い分けたい場合、データブロックに **グループID** を付加してグループ化する。 ``testShots`` の各カラム（ ``setUpTable`` / ``expectedTable`` / ``setUpFile`` / ``expectedFile`` 等）に グループID の値を指定すると、そのテストケースでは対応する グループID を持つデータブロックだけが収集される。

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
~~~~

- ``testShots`` の各カラムで グループID を省略すると、グループID なしのデータブロック（デフォルトグループ）が収集される。
- バッチ固有の動作として グループID に ``"default"`` を指定すると グループID なし扱いと同等になる（HTTP テスト・メッセージングテストでは適用されない）。

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

グループID はデータブロック種別ラベルの ``[...]`` で指定する。

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
^^^^^^^^^^

グループID は各エントリの ``group_id:`` フィールドで指定する。

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

記述例は :ref:`ntf_examples_testshots` を参照。

.. _ntf_testdata_table_data:

テーブルデータ
==============

各エントリはカラム名と値の組み合わせで記述する。省略したカラムには INSERT 時にデフォルト値が補完される。

テーブルデータの形式
--------------------

Excelの場合
~~~~~~~~~~~

1行目にカラム名、2行目以降にデータを記述する。

.. code-block:: text

    SETUP_TABLE=テーブル名
    | カラム1 | カラム2 | カラム3 |
    | 値1     | 値2     | 値3     |

YAMLの場合
~~~~~~~~~~

``rows:`` 配列に各行をオブジェクトで記述する。

.. code-block:: yaml

    setup_tables:
      - table: テーブル名
        rows:
          - カラム1: "値1"
            カラム2: "値2"
            カラム3: "値3"

``setup_tables`` / ``expected_tables`` / ``expected_complete_tables`` の各エントリには ``table`` キーが必須である（省略時はエラー）。

SETUP_TABLE
-----------

DB への INSERT 用データである。

- 各エントリのカラム名と値を記述する。
- 主キーカラムは省略しないこと。省略すると型に応じたデフォルト値（数値型は ``"0"`` 、文字型はスペース等）が INSERT される。
- FK が設定された数値カラムも省略しないこと。省略すると ``"0"`` が INSERT され、参照先に ID=0 の行が存在しない場合は FK 違反になる。NULL を意図する場合は省略せず明示的に ``null`` を記述すること（省略 ≠ NULL）。

null 値・空文字の動作を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - 値の指定
     - Excel
     - YAML
   * - null（Java null）
     - セルに ``null`` （大文字小文字不問）
     - アンクォートの ``null`` （ ``"null"`` でも同結果）
   * - 空文字
     - セルを空にする
     - ``""``
   * - 日付型カラムの空文字
     - セルを空にする → ``null`` 扱い
     - ``""`` → ``null`` 扱い

.. important::

  ``SETUP_TABLE`` （ ``setUpDb`` / ``setUpTable`` ）は対象テーブルへ INSERT する前にそのテーブルを **全件 DELETE** してから INSERT する。NTF はテスト後に後始末をしない（INSERT した行はコミットされたままになる）。そのため、あるテストが子テーブルに行を残した状態で別のテストが親テーブルを DELETE しようとすると、残存した子テーブル行が FK 違反を起こして DELETE に失敗する。

  FK のある親テーブルをセットアップ（= clear）するテストでは、 **子テーブルも** ``SETUP_TABLE`` **に列挙して一緒に clear すること。** NTF は親子関係に従い子→親の順で削除する。子テーブルのデータを書き換えないテストであっても、親を clear するなら子の clear 指定が必要である。

記述例を以下に示す。

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    SETUP_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | RATE | PROFILE          | PHOTO                          |
    | 0000000101 | 山田太郎 | 1    | 85000 | 1.5  | ゴールド会員です | ${binaryFile:testdata.txt}     |
    | 0000000102 | 鈴木花子 | 2    | Null  | 2.25 | シルバー会員     | ${binaryFile:member_photo.jpg} |

YAMLの場合
~~~~~~~~~~

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

- 値は文字列で記述する（ ``"0000000101"`` のようにクォート）。
- NULL 値はアンクォートの ``null`` で記述する（ ``"null"`` とクォートしても同じく Java null になる）。
- ``${binaryFile:パス}`` はファイル内容をバイナリ読み込みして HexString に変換する。

EXPECTED_TABLE
--------------

テスト後の DB 状態と比較するデータである。省略したカラムは比較対象外となる。検証したいカラムだけを列挙できる。

行照合の動作は以下の通り。

- 期待行と DB の行は **DB の主キー** で対応付けられる。主キーカラムは省略しないこと。
- 対象テーブルに存在する DB 行は **全件を列挙する** 必要がある。期待側に存在しない DB 行があると「余分な行がある」旨のエラーになる（部分検証はできない）。

.. note::

  主キーが自動採番（IDENTITY / シーケンス等）の場合、テスト実行時に払い出される値が不定になるため期待側に主キー値を書けず、複数行の検証が成立しない。テスト時に主キー値を既知にできる設計（業務キーの複合主キー等）にしておく必要がある。

記述例を以下に示す。

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    EXPECTED_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | UPDATED_DATE          |
    | 0000000101 | 山田太郎 | 1    | 87500 | 2024-04-01 09:00:00.0 |
    | 0000000102 | 鈴木花子 | 2    | 42000 | 2024-04-01 09:00:00.0 |

YAMLの場合
~~~~~~~~~~

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

EXPECTED_COMPLETE_TABLE
-----------------------

省略カラムにデフォルト値を補完してから比較するデータである。

各カラム型のデフォルト値を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - カラム型
     - デフォルト値
   * - 数値型
     - ``"0"``
   * - 固定長文字列型（CHAR, NCHAR）
     - 半角スペース × カラム長
   * - 可変長文字列型（VARCHAR 等）
     - ``" "`` （半角スペース1文字）
   * - 日付型
     - epoch 起点（JVM タイムゾーン依存。JST 環境では ``"1970-01-01 09:00:00.0"`` ）
   * - バイナリ型
     - 10バイトのゼロバイト列の HexString
   * - Boolean 型
     - ``"false"``

.. note::

  DATE カラムのデフォルト値は JVM のタイムゾーン設定に依存する。JST 環境と UTC 環境では値が異なる。

省略カラムの扱いを以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - キーワード
     - 省略カラムの扱い
     - YAML での省略
   * - ``EXPECTED_TABLE`` / ``expected_tables:``
     - 比較対象外。検証したいカラムだけ列挙できる
     - キーを書かない
   * - ``EXPECTED_COMPLETE_TABLE`` / ``expected_complete_tables:``
     - ``BasicDefaultValues`` のデフォルト値を補完してから比較
     - キーを書かない

混在制約は以下の通り。

- **Excel は混在禁止**: 同一シート内で ``EXPECTED_TABLE`` と ``EXPECTED_COMPLETE_TABLE`` を混在させると後半のデータが読み込まれない。同じ種別をまとめて記述すること。
- **YAML は混在可**: ``expected_tables:`` と ``expected_complete_tables:`` は別キーのため混在できる。

記述例を以下に示す。

Excelの場合
~~~~~~~~~~~

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
~~~~~~~~~~

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
            # UPDATE_DATE を省略 → BasicDefaultValues のデフォルト値で補完されて比較

LIST_MAP
--------

キーバリュー形式の汎用データである。テストケース定義（ ``testShots`` ）・リクエストパラメータ・期待値オブジェクト・期待ログなど様々な用途で使う。

- ID は完全一致で検索される。
- 同一ファイル内で同一 ID の重複エントリは先着一致で、2件目以降は無視される。
- 指定 ID のエントリが存在しない場合は空データ扱い（エラーにならない）。

主な予約 ID は :ref:`ntf_testdata_testshots` を参照。

記述例を以下に示す。

Excelの場合
~~~~~~~~~~~

リクエストパラメータ（マーカーカラム付き）の例を以下に示す。

.. code-block:: text

    LIST_MAP=searchParams
    | [no] | memberId   | orderStatus | fromDate   | toDate     | [desc]      |
    | 1    | 0000000101 | 1           | 2024-04-01 | 2024-04-30 | 4月注文検索 |
    | 2    | 0000000102 |             | 2024-01-01 |            | 全件検索    |

    LIST_MAP=expectedLog
    | message                                  | logLevel |
    | 会員ID[0000000101]の注文を処理しました   | INFO     |
    | 会員ID[0000000102]の注文を処理しました   | INFO     |

YAMLの場合
~~~~~~~~~~

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

マーカーカラムについては以下の通り。

- 角括弧で囲んだカラム（ ``[no]`` ・ ``[desc]`` ）はマーカーカラムである。DB 操作から除外される（Excel 上の見やすさのために使うことが多い）。
- YAML ではダブルクォートで囲む（ ``"[no]"`` ）。YAML の角括弧構文との衝突を避けるためである。

記述例は :ref:`ntf_examples_table_data` を参照。DB アサート固有の挙動（順序不問・主キー突合・デフォルト値補完）の記述例は :ref:`ntf_examples_db_assert` を参照。

.. _ntf_testdata_file_data:

ファイルデータ
==============

セットアップ用ファイルデータ（ ``SETUP_FIXED`` / ``SETUP_VARIABLE`` ）は固定長・可変長の区別なくまとめて収集される。期待値ファイル（ ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE`` ）も同様である。固定長か可変長かはデータブロック内の記述で区別される。

``setup_files`` / ``expected_files`` の各エントリには ``path`` キーが必須である（省略時はエラー）。

ファイルデータブロックの構造
----------------------------

ファイルデータブロックは次の順序で記述する。

.. code-block:: text

    1. ディレクティブ（0件以上）: エンコーディング等のファイル属性
    2. レコード種別 + フィールド名称: 先頭要素=レコード種別、以降=フィールド名称
    3. データ型: 各フィールドの型名称
    4. フィールド長（固定長のみ）: 各フィールドのバイト長
    5. データ（1件以上）

Excel 固有の制約として、データの先頭要素は必ず空（null または空文字）にする。YAML にこの制約はない。

各形式の中核要素の対応を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Excel
     - YAML
   * - ``SETUP_FIXED=パス`` / 区切り行
     - ``path`` / ``type`` / ``group_id``
   * - レコード種別+フィールド名称行
     - ``record_type``
   * - データ型行 / フィールド長行
     - ``fields: name/type/length``
   * - データ行（先頭セル空）
     - ``rows: 値配列``

YAML での記述規則は以下の通り。

- ``fields:`` の各要素は ``{name: フィールド名, type: データ型, length: バイト長}`` の形式で記述する。
- ``type`` は日本語型名称（ ``半角`` , ``全角`` , ``数値`` 等）で記述する（詳細は :ref:`ntf_testdata_values_typemap` を参照）。
- ``length`` は整数（ ``length: 10`` ）または文字列（ ``length: "10"`` ）どちらでも有効である。
- ``rows:`` の各行は配列形式で、 ``fields:`` と同じ順序・同じ件数で値を並べる。
- ``rows:`` 内の値はダブルクォートで囲む。

固定長ファイル
--------------

注文データのバッチ処理テスト。固定長の入力ファイルを読み込んで処理し、結果を固定長の出力ファイルに書き出すことを確認するケースを以下に示す。

Excelの場合
~~~~~~~~~~~

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
~~~~~~~~~~

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

エンコーディング指定付き固定長ファイル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MS932 エンコーディングで顧客データファイルを読み込むケースを以下に示す。

Excelの場合
^^^^^^^^^^^

ディレクティブ行はレコード定義より前に「キー | 値」の2セルで記述する。

.. code-block:: text

    SETUP_FIXED=input/data.dat
    | text-encoding | MS932    |           |        |
    | DATA          | USER_ID  | USER_NAME | AMOUNT |
    |               | X        | N         | Z      |
    |               | 10       | 20        | 10     |
    |               | 001      | 山田太郎  | 5000   |
    |               | 002      | 鈴木花子  | 3000   |

YAMLの場合
^^^^^^^^^^

ディレクティブは ``directives:`` オブジェクトの ``key: value`` 形式で記述する。

.. code-block:: yaml

    setup_files:
      - path: input/data.dat
        type: fixed
        directives:
          text-encoding: MS932
        records:
          - record_type: DATA
            fields:
              - {name: USER_ID,   type: 半角, length: 10}
              - {name: USER_NAME, type: 全角, length: 20}
              - {name: AMOUNT,    type: 数値, length: 10}
            rows:
              - ["001", "山田太郎", "5000"]
              - ["002", "鈴木花子", "3000"]

固定長ファイル固有の仕様は以下の通り。

- フィールド名称・データ型・フィールド長の3リストが同サイズで必須である。
- 1ファイルデータブロック内の全レコード定義は同一レコード長でなければならない（違反時はエラー）。
- フィールド値がフィールド長を超えた場合はエラーとなる。

可変長ファイル
--------------

可変長ファイルではフィールド長（ ``length`` ）の記述が不要である。CSV 形式の顧客データファイルを入力として使うケースを以下に示す。

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    SETUP_VARIABLE=input/data.csv
    | field-separator | ,       |           |        |
    | DATA            | USER_ID | USER_NAME | AMOUNT |
    |                 | X       | N         | X      |
    |                 | 001     | 山田太郎  | 5000   |
    |                 | 002     | 鈴木花子  | 3000   |

YAMLの場合
~~~~~~~~~~

可変長では ``fields:`` の各要素から ``length`` を省略する。

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

可変長ファイル固有の仕様は以下の通り。

- フィールド名称・データ型の2リストが同サイズで必須である。フィールド長は不要。
- 空エントリの動作: ファイルデータの空エントリ（先頭フィールドが空の行）はデータ行として扱われる。可変長は全フィールドが ``""`` のレコードとして保持され、固定長はスペースパディングされた定長レコードとして書き出される（テーブルデータの空行スキップとは異なる）。

グループID 付きファイル
-----------------------

テストケースごとに異なる入力ファイルを使い分けるケースを以下に示す。

Excelの場合
~~~~~~~~~~~

グループID はデータブロック種別ラベルの ``[...]`` で指定する。

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
~~~~~~~~~~

グループID は ``group_id:`` フィールドで指定する。省略するとグループ ID なし（デフォルトグループ）扱いである。

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
----------------------

1ファイルデータブロック内に複数のレコードレイアウトを連続して記述できる。データの後ろに新たなレコード種別とフィールド名称を書くと、新しいレコードレイアウトとして扱われる。

1ファイルに HEADER レコードと DATA レコードが混在する振込依頼ファイルを扱うケースを以下に示す。

Excelの場合
~~~~~~~~~~~

同一セクション内でレコード種別+フィールド名称行を続けて書くと、複数レコードレイアウトとなる。

.. code-block:: text

    SETUP_FIXED=input/multi.dat
    | HEADER | SEQ  | TYPE |      |
    |        | X    | X    |      |
    |        | 4    | 2    |      |
    |        | H001 | 01   |      |
    | DATA   | USER_ID | AMOUNT | NOTE |
    |        | X       | Z      | N    |
    |        | 10      | 10     | 20   |
    |        | 001     | 5000   | 備考 |

YAMLの場合
~~~~~~~~~~

``records:`` 配列に複数のレコードレイアウトを並べる。

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

空ファイル
----------

0バイトの空ファイルを表現するには、ディレクティブのみを記述してレコード定義を省略する。出力ファイルがゼロ件のときに空ファイルを生成することを確認するケースを以下に示す。

Excelの場合
~~~~~~~~~~~

ディレクティブ行のみ記述してレコード定義以降を省略する。

.. code-block:: text

    SETUP_FIXED=input/empty.dat
    | text-encoding | MS932 |

YAMLの場合
~~~~~~~~~~

レコードは ``records: []`` と空配列で記述する。

.. code-block:: yaml

    setup_files:
      - path: input/empty.dat
        type: fixed
        directives:
          text-encoding: MS932
        records: []

その他の仕様
------------

``"-"`` 長フィールド
~~~~~~~~~~~~~~~~~~~~

フィールド長に ``"-"`` を指定すると、追加された全レコードの最大バイト長に自動拡張される。値は改行コードと前後空白が除去される。

エラーになるケース
~~~~~~~~~~~~~~~~~~

以下の場合にエラーとなる。

- 同一レコード種別内でフィールド名称が重複している
- フィールド名称リストまたはデータ型リストが未指定または空
- フィールド名称・データ型・フィールド長リストのサイズが一致していない
- 存在しないフィールド名称を指定している
- データ要素数が不正
- ディレクティブまたはレコード種別/フィールド名称定義の要素数が2未満
- ファイルの読み込みに失敗した（IO エラー）
- 日付型カラムの値が日付として解析できない

記述例は :ref:`ntf_examples_file_data` を参照。

.. _ntf_testdata_messaging:

メッセージングテストデータ
==========================

メッセージングテストデータは ``MESSAGE`` / ``EXPECTED_REQUEST_*_MESSAGES`` / ``RESPONSE_*_MESSAGES`` の各データブロックで記述する。

sendSyncTestData の配置規則
---------------------------

テストデータファイルは ``sendSyncTestData/{requestId}/message`` というパスに配置する（末尾の ``message`` は固定のパスセグメント）。

- **Excel**: ``MESSAGE=sendSyncTestData/{requestId}/message`` をデータブロック識別子として記述する。
- **YAML**: ``messages:`` の ``id:`` に ``sendSyncTestData/{requestId}/message`` を指定する。

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    MESSAGE=sendSyncTestData/REQ001/message
    | no | errorMode | field1 | field2 |
    |    | 半角      | 半角   | 半角   |
    |    | 10        | 10     | 10     |
    | 1  |           | value1 | value2 |
    | 2  |           | value3 | value4 |

YAMLの場合
^^^^^^^^^^

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

FW 制御ヘッダフィールド
-----------------------

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
----------------------------

受信電文と応答電文を定義するケースを以下に示す。

Excelの場合
~~~~~~~~~~~

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
~~~~~~~~~~

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

HEADER / BODY MESSAGES の構造と件数制約
----------------------------------------

``EXPECTED_REQUEST_HEADER_MESSAGES`` と ``EXPECTED_REQUEST_BODY_MESSAGES`` のエントリ数（rows 合計）は一致が必須である（不一致時はエラー）。

HTTP 同期応答メッセージ（ ``response_body_messages`` ）の各データエントリは文字列長が同一である必要がある。

記述例（要求電文・応答電文の期待値）
-------------------------------------

バッチリクエスト単体テストで電文の送受信をテストするケースを以下に示す。

Excelの場合
~~~~~~~~~~~

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
~~~~~~~~~~

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

- ``expectedMessage`` カラムには要求電文の グループID、 ``responseMessage`` カラムには応答電文の グループID を指定する。
- YAML では ``expected_request_header_messages:`` の ``group_id:`` が ``testShots`` の ``expectedMessage`` カラムに対応する。
- ``id:`` はリクエスト ID（フォーマット定義ファイルの解決に使われる）。

ステータスコード
----------------

ステータスコードカラムがない場合はデフォルト値 ``"200"`` が使用される。Excel・YAML 両方で共通である。

記述例
~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    RESPONSE_BODY_MESSAGES=REQ001
    | no | body    |
    |    | 半角    |
    |    | 10      |
    | 1  | RESULT_OK |

YAMLの場合
^^^^^^^^^^

.. code-block:: yaml

    response_body_messages:
      - id: REQ001
        records:
          - record_type: DATA
            fields:
              - {name: body, type: 半角, length: 10}
            rows:
              - ["RESULT_OK"]

その他の仕様
------------

no 行（フィールド名称行）と errorMode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**電文の行構造**: ディレクティブ群・FW 制御ヘッダの後、 ``no`` で始まる行がフィールド名称行である。以降、データ型行・フィールド長行・データ行が続く。

- **Excel**: フィールド名称行の先頭セルに ``no`` を記述する。データ行の先頭セル（ ``no`` カラム）はフレームワークが除去しデータとして保存しない。
- **YAML**: フィールド名称は ``fields:`` 、データは ``rows:`` に記述する（ ``no`` カラム自体は YAML の構造に現れない）。

**errorMode（RESPONSE 系・MockMessaging 経路のみ）**:

- ``response_header_messages`` / ``response_body_messages`` で、データ行の先頭値が ``errorMode:timeout`` または ``errorMode:msgException`` の場合、そのエントリは送受信エラーをシミュレートするマーカーとして扱われる。
- errorMode 行は ``fw_header:`` の分離とは独立した別の仕組みである。
- ``RequestTestingSendSyncSupport`` 経路（GroupMessageParser）では errorMode は使用されない。

複数回送信
~~~~~~~~~~

N 回送信する場合は、ヘッダ件数とボディ件数をともに N 件ずつ記述する。同一リクエスト ID で複数回送信する場合は ``no`` 値を変えて連続記述し、送信順序と ``no`` 値を一致させる。

フォーマット定義ファイルの命名規則
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 応答電文: ``{requestId}_RECEIVE``
- 要求電文: ``{requestId}_SEND``

アサート方式の切り替え
~~~~~~~~~~~~~~~~~~~~~~

``SystemRepository`` の ``messaging.assertAsMapFileType`` キーの設定値に応じてアサート方式が切り替わる。未設定時のデフォルトは ``"Fixed"`` 形式（項目単位アサート）。

記述例は :ref:`ntf_examples_messaging` を参照。

.. _ntf_testdata_values:

値・ディレクティブ・コメント
============================

テストデータの値の書き方、インタープリタ、ディレクティブ、コメントおよびヘッダについて説明する。

値の書き方
----------

値の種類と記法
~~~~~~~~~~~~~~

各値の種類と Excel / YAML での記述方法を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - 値の種類
     - Excel での記述
     - YAML での記述
     - 備考
   * - 通常の文字列
     - ``abc``
     - ``"abc"``
     - YAML はクォート必須（型変換防止）
   * - null（DB に null を格納）
     - ``null`` （大文字小文字不問）
     - ``null`` （クォートなし）
     - YAML の ``"null"`` （クォートあり）も同結果
   * - 空文字
     - 空セル
     - ``""``
     -
   * - 先頭ゼロ付き数値
     - ``001``
     - ``"001"``
     - YAML でクォートなしだと ``1`` に型変換される
   * - ``true`` / ``false`` （文字列）
     - ``true``
     - ``"true"``
     - YAML でクォートなしだと真偽値に型変換される
   * - 半角スペース1文字
     - ``" "`` （セルに ``"`` スペース ``"`` と入力）
     - ``" "``
     - 外側クォートが除去されてスペースになる
   * - ダブルクォート1文字
     - ``"""`` （セルに ``"`` ``"`` ``"`` と入力）
     - ``'"'`` （YAML シングルクォート）
     -
   * - 日時プレースホルダ
     - ``${systemTime}``
     - ``"${systemTime}"``
     - 完全一致のみ変換
   * - バイナリファイル参照
     - ``${binaryFile:path}``
     - ``"${binaryFile:path}"``
     - パスはデータファイルのディレクトリ基準
   * - 文字種生成
     - ``${半角英字,10}``
     - ``"${半角英字,10}"``
     -
   * - 改行文字（CR）
     - ``\\r``
     - ``"\\r"``
     - LineSeparatorInterpreter が変換（デフォルト設定は CR のみ）

YAML のクォートルール
~~~~~~~~~~~~~~~~~~~~~

- ``rows:`` 内のすべてのデータ値は **必ずダブルクォートで囲む**。クォートなしだと SnakeYAML が数値・真偽値に型変換する。
- ``null`` のみクォートなしで記述する（ ``"null"`` でも同じく Java null になる）。
- ``type:`` , ``record_type:`` , ``path:`` 等のスキーマ構造値はクォート不要である。

**Excel のセル書式**: セルは必ず **文字列書式** で記述する。数値・日付書式の動作は保証されない。

日付型・Timestamp・特殊値の例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``EXPECTED_TABLE`` で日付・タイムスタンプ・NULL・システム日時を使うケースを以下に示す。

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    EXPECTED_TABLE=SCHEDULE
    | ID | EVENT_NAME   | START_DATE     | CREATED_AT            |
    | 1  | 会議         | 2024-01-15     | 2024-01-01 09:00:00.0 |
    | 2  | NULLテスト   | NULL           | NULL                  |
    | 3  | システム時刻 | ${systemTime}  | ${systemTime}         |
    | 4  | 更新時刻     | ${updateTime}  | ${setUpTime}          |

YAMLの場合
^^^^^^^^^^

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

- ``NULL`` 文字列は ``NullInterpreter`` が Java null に変換する。大文字小文字不問（ ``null`` ・ ``Null`` も同様）。YAML ではアンクォートの ``null`` で記述する（ ``"null"`` とクォートしても同じく Java null になる）。
- ``${systemTime}`` は完全一致のみ変換される。文字列中に埋め込むには ``CompositeInterpreter`` との組み合わせが必要。
- ``java.sql.Timestamp`` 型カラムの期待値は末尾 ``.0`` が必須（ ``"2024-01-01 09:00:00.0"`` ）。末尾 ``.0`` がないとアサートが失敗する。

QuotationTrimmer によるスペース値明示記法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

空白値やダブルクォート文字を明示して記述するケースを以下に示す。

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    EXPECTED_TABLE=ITEM
    | ID | NAME | MEMO |
    | 1  | " "  | """  |

YAMLの場合
^^^^^^^^^^

.. code-block:: yaml

    expected_tables:
      - table: ITEM
        rows:
          - ID: "1"
            NAME: " "
            MEMO: "\""

- Excel: ``" "`` → 半角スペース1文字、 ``"""`` → ダブルクォート1文字。半角または全角ダブルクォートで前後が囲まれた場合のみ外側1層を除去する。
- YAML: ``" "`` でスペース1文字。ダブルクォート文字は ``"\""`` または ``'"'`` で記述する。

バイナリデータ
~~~~~~~~~~~~~~

BLOB カラムにバイナリデータを記述するケースを以下に示す。

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    SETUP_TABLE=FILE_TABLE
    | FILE_ID | FILE_DATA                    |
    | 001     | 0xCAFEBABE                   |
    | 002     | ${binaryFile:testdata.bin}   |

YAMLの場合
^^^^^^^^^^

.. code-block:: yaml

    setup_tables:
      - table: FILE_TABLE
        rows:
          - FILE_ID: "001"
            FILE_DATA: "0xCAFEBABE"
          - FILE_ID: "002"
            FILE_DATA: "${binaryFile:testdata.bin}"

- ``0x`` プレフィクス付き16進数でバイナリ値を記述する。 ``0x`` がない場合は文字列としてエンコードされる。
- ``${binaryFile:パス}`` でファイル内容をバイナリ読み込みして HexString に変換する。

インタープリタチェーンの仕組み
------------------------------

テストデータの値はパース時にインタープリタチェーンを通過して変換される。DI 設定で注入されたインタープリタが順番に適用される。

インタープリタ一覧
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - インタープリタ
     - 変換内容
   * - ``NullInterpreter``
     - ``null`` / ``NULL`` / ``Null`` （大文字小文字不問）→ Java null
   * - ``QuotationTrimmer``
     - 半角または全角ダブルクォートで前後が囲まれた場合のみ外側1層を除去
   * - ``DateTimeInterpreter``
     - ``${systemTime}`` / ``${updateTime}`` / ``${setUpTime}`` の完全一致のみ変換
   * - ``LineSeparatorInterpreter``
     - ``\\r`` → CR（0x0D）に変換（デフォルト設定）。 ``setMatchPattern`` / ``setLineSeparator`` で変換対象・変換後の改行コードを変更可能
   * - ``BinaryFileInterpreter``
     - ``${binaryFile:パス}`` でファイル内容をバイナリ読み込みし HexString に変換。パスはデータファイル（Excel / YAML）のディレクトリからの相対パス
   * - ``BasicJapaneseCharacterInterpreter``
     - ``${文字種,文字数}`` 形式で文字列生成
   * - ``CompositeInterpreter``
     - 文字列中の ``${...}`` 要素を個別解釈して置換

ダブルクォート文字やスペースそのものを値として記述する場合、外側1層が除去されることを踏まえた記法が必要である。

- Excel: ``"""`` → ダブルクォート1文字 ／ ``" "`` → 半角スペース1文字
- YAML: ``"\""`` または ``'"'`` → ダブルクォート1文字 ／ ``" "`` → 半角スペース1文字

記述例は :ref:`ntf_examples_quotation` を参照。

DateTimeInterpreter の完全一致制約
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``DateTimeInterpreter`` は完全一致のみ変換する。部分文字列は変換されない。文字列中の ``${...}`` を置換するには ``CompositeInterpreter`` との組み合わせが必要である。

文字種生成の有効文字種
~~~~~~~~~~~~~~~~~~~~~~

14種類の文字種が使用できる: 半角英字 / 半角数字 / 半角記号 / 半角カナ / 全角英字 / 全角数字 / 全角ひらがな / 全角カタカナ / 全角漢字 / 全角記号その他 / 中国語 / サロゲートペア / 改行 / 外字。

上記以外の文字種を指定するとエラーになる。

BinaryFileInterpreter のパス基準
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``${binaryFile:パス}`` のパスはテストデータファイルのディレクトリからの相対パスである。Excel・YAML 両方で同じ動作。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 形式
     - 基準ディレクトリ
   * - Excel
     - Excel ファイル（ ``.xls`` / ``.xlsx`` ）が置かれているディレクトリ
   * - YAML
     - YAML ファイル（ ``.yaml`` ）が置かれているディレクトリ

日付型カラムの記述形式と境界値
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有効な記述形式は以下の通り。

- ``yyyyMMddHHmmssSSS`` （17文字）
- 後置0埋め短縮形
- JDBC タイムスタンプエスケープ形式（5文字目が ``-`` ）

``java.sql.Timestamp`` 型カラムの期待値は末尾 ``.0`` が必須である（例: ``"2010-01-01 12:34:56.0"`` ）。末尾 ``.0`` がないとアサートが失敗する。

X9/SX9 型フィールドの記述
~~~~~~~~~~~~~~~~~~~~~~~~~~

パディング文字・符号を含めた実際のバイト列表現（固定長フォーマットの実値）をそのまま記述する。

.. _ntf_testdata_values_typemap:

データ型マッピング
~~~~~~~~~~~~~~~~~~

フィールドのデータ型は以下の日本語型名称で指定する。使用できない型名称を指定するとエラーになる。

.. list-table::
   :header-rows: 1
   :widths: 55 15 30

   * - 型名称
     - 型記号
     - 用途
   * - ``半角英字`` / ``半角数字`` / ``半角記号`` / ``半角カナ`` / ``半角英数字`` / ``半角英数字記号`` / ``半角``
     - ``X``
     - 半角文字
   * - ``全角英字`` / ``全角数字`` / ``全角ひらがな`` / ``全角カタカナ`` / ``全角漢字`` / ``全角``
     - ``N``
     - 全角文字
   * - ``全半角``
     - ``XN``
     - 全角・半角混在
   * - ``数値`` / ``符号無ゾーン10進数``
     - ``Z``
     - ゾーン10進数（符号なし）
   * - ``符号付ゾーン10進数``
     - ``SZ``
     - ゾーン10進数（符号あり）
   * - ``符号無パック10進数``
     - ``P``
     - パック10進数（符号なし）
   * - ``符号付パック10進数``
     - ``SP``
     - パック10進数（符号あり）
   * - ``符号無数値``
     - ``X9``
     - バイナリ表現の数値（符号なし）
   * - ``符号付数値``
     - ``SX9``
     - バイナリ表現の数値（符号あり）
   * - ``バイナリ``
     - ``B``
     - バイナリデータ

``TEST_{型名称}`` という名前のデータ型を定義すると、同名の基底型より優先して使用される（テスト専用の型定義に使う）。

ディレクティブ
--------------

ディレクティブの構成
~~~~~~~~~~~~~~~~~~~~

ディレクティブは「キー名・値」の2要素で記述する（最低2要素必要）。

- **Excel**: ファイルデータブロックの先頭（レコード定義より前）に ``| キー名 | 値 |`` の形で記述する。
- **YAML**: ``directives:`` オブジェクトに ``key: value`` 形式で記述する。

固定長ファイルのディレクティブ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有効なキーは以下に限定される。無効なキーを指定するとエラーになる。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ディレクティブキー
     - 説明
   * - ``file-type``
     - 自動設定（ ``"Fixed"`` ）。通常は記述不要
   * - ``text-encoding``
     - ファイルの文字エンコーディング
   * - ``record-length``
     - フィールド長合計から自動計算。通常は記述不要
   * - ``record-separator``
     - レコード区切り文字
   * - ``positive-zone-sign-nibble``
     - ゾーン10進数の正符号ニブル
   * - ``negative-zone-sign-nibble``
     - ゾーン10進数の負符号ニブル
   * - ``positive-pack-sign-nibble``
     - パック10進数の正符号ニブル
   * - ``negative-pack-sign-nibble``
     - パック10進数の負符号ニブル
   * - ``required-decimal-point``
     - 小数点を必須とするか（ ``true`` / ``false`` ）
   * - ``fixed-sign-position``
     - 符号を固定位置に置くか（ ``true`` / ``false`` ）
   * - ``required-plus-sign``
     - 正符号を出力するか（ ``true`` / ``false`` ）

固定長ディレクティブの記述例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

エンコーディングとゾーン10進数の符号ニブルを指定するケースを以下に示す。

Excelの場合
"""""""""""

.. code-block:: text

    SETUP_FIXED=input/data.dat
    | text-encoding              | MS932 |
    | positive-zone-sign-nibble  | C     |
    | DATA | USER_ID | AMOUNT |
    |      | X       | Z      |
    |      | 10      | 10     |
    |      | 001     | 5000   |

YAMLの場合
""""""""""

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
              - {name: USER_ID, type: 半角, length: 10}
              - {name: AMOUNT,  type: 数値, length: 10}
            rows:
              - ["001", "5000"]

可変長ファイルのディレクティブ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有効なキーは以下に限定される。無効なキーを指定するとエラーになる。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ディレクティブキー
     - 説明
   * - ``file-type``
     - 自動設定（ ``"Variable"`` ）。通常は記述不要
   * - ``text-encoding``
     - ファイルの文字エンコーディング
   * - ``record-separator``
     - レコード区切り。 ``NONE`` / ``CR`` / ``LF`` / ``CRLF`` または任意リテラル文字列が有効
   * - ``field-separator``
     - フィールド区切り文字。デフォルトは ``","`` 。 ``"\\t"`` 指定でタブ文字。 **1文字のみ有効** （2文字以上はエラー）
   * - ``quoting-delimiter``
     - クォート文字
   * - ``ignore-blank-lines``
     - 空行を無視するか
   * - ``requires-title``
     - タイトル行の有無
   * - ``max-record-length``
     - レコードの最大長
   * - ``title-record-type-name``
     - タイトルレコードの種別名

可変長ディレクティブの記述例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

タブ区切り・CRLF 改行のファイルを扱うケースを以下に示す。

Excelの場合
"""""""""""

.. code-block:: text

    SETUP_VARIABLE=input/data.tsv
    | field-separator  | \t    |
    | record-separator | CRLF  |
    | DATA | FIELD1 | FIELD2 |
    |      | X      | X      |
    |      | value1 | value2 |

YAMLの場合
""""""""""

タブ文字の記法が形式で異なる点に注意すること。Excel セルには ``\t`` （バックスラッシュ + t の2文字）を入力し、フレームワークがタブ文字（0x09）に変換する。YAML は ``"\\t"`` と記述する（YAML の ``\t`` は実際のタブ文字になるためバックスラッシュをエスケープする）。

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

デフォルトディレクティブの DI 設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``SystemRepository`` への DI 設定で、全ファイル共通または種別専用のデフォルトディレクティブを一括設定できる。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - DI キー
     - 適用対象
   * - ``defaultDirectives``
     - 全ファイル共通のデフォルト
   * - ``fixedLengthDirectives``
     - 固定長ファイル専用。 ``defaultDirectives`` より後に上書き適用される
   * - ``variableLengthDirectives``
     - 可変長ファイル専用

ヘッダ・コメント・空エントリ
-----------------------------

ヘッダの構造
~~~~~~~~~~~~

ヘッダにはカラム名を列挙する。

- ヘッダ末尾の空カラムは除去される（末尾カラムの省略が可能）。
- データエントリがヘッダより少ない場合、不足分は空文字 ``""`` で補完される。

マーカーカラム
~~~~~~~~~~~~~~

カラム名が ``[カラム名]`` 形式（角括弧で囲まれた名前）のカラムはマーカーカラムとして扱われ、DB 操作から除外される。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 形式
     - 除外対象
   * - Excel
     - ``SETUP_TABLE`` / ``EXPECTED_TABLE`` / ``LIST_MAP`` すべて
   * - YAML
     - ``setup_tables`` / ``expected_tables`` / ``list_maps`` すべて

エントリ単位のコメント
~~~~~~~~~~~~~~~~~~~~~~

エントリをコメントとしてマークすると、そのエントリ全体がスキップされる。

- **Excel**: 先頭要素が ``//`` で始まる行はスキップされる。
- **YAML**: ``#`` がコメント記号（行頭・行末どちらにも使える）。

要素途中からのコメント
~~~~~~~~~~~~~~~~~~~~~~

- **Excel**: 先頭以外の要素が ``//`` で始まる場合、その要素以降が切り捨てられる。
- **YAML**: ``#`` を行末に書いて同等の記述ができる（例: ``NUMBER_COL: "100"  # 数値カラム`` ）。

記述例（コメントとマーカーカラム）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Excelの場合
^^^^^^^^^^^

.. code-block:: text

    SETUP_TABLE=TEST_TABLE
    | // この行はコメントです  |            |         |            |        |
    | [no]                     | PK_COL1    | PK_COL2 | NUMBER_COL | [desc] |
    | 1                        | 0000000001 | AB      | 100        | テスト1 |
    | // この行もスキップされます |          |         |            |        |
    | 2                        | 0000000002 | CD      | 200        | テスト2 |

YAMLの場合
^^^^^^^^^^

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

空エントリのスキップ
~~~~~~~~~~~~~~~~~~~~

全要素が null または空文字のエントリは読み飛ばされる。

- **Excel**: 行の全セルが空の場合にスキップされる。
- **YAML**: ``rows:`` 内の要素が空マッピング（ ``{}`` ）またはすべての値が空文字の場合にスキップされる。

記述例
^^^^^^

Excelの場合
"""""""""""

.. code-block:: text

    SETUP_TABLE=USER
    | USER_ID | NAME     |
    | 001     | 山田太郎 |
    |         |          |
    | 002     | 鈴木花子 |

YAMLの場合
""""""""""

.. code-block:: yaml

    setup_tables:
      - table: USER
        rows:
          - USER_ID: "001"
            NAME: "山田太郎"
          # 空行はここには書かない（YAML にはそもそも空エントリの概念がない）
          - USER_ID: "002"
            NAME: "鈴木花子"

記述例は :ref:`ntf_examples_values` を参照。
