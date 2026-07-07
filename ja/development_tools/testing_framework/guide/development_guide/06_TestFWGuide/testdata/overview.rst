.. _ntf_testdata_overview:

====================
テストデータの全体像
====================

テストデータは Excel または YAML ファイルで記述できる。

テストコード（Java）がテストデータファイルを読み込み、DB へのデータ投入・入力ファイルの配置・期待値との比較を行う。テストデータには **テストケース**・**セットアップ**・**検証** の3用途のデータを記述し、いずれも **データブロック** 単位で管理する。

------
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
================

データの格納階層は次のとおりである。テストクラス1つ分のデータが読み込み単位（Excel は1シート／YAML は1ファイル）に分かれ、その中に複数のデータブロックが共存する。

.. code-block:: text

    テストクラス（Excel:1ブック / YAML:1ディレクトリ）
    └── 読み込み単位（Excel:1シート / YAML:1ファイル）
         └── データブロック（種別 + 識別子）
              └── レコード定義 / フィールド / データ

データブロックは種別（ ``SETUP_TABLE`` など14種）と識別子の値（テーブル名・ファイルパス・ID など）の組み合わせで区別する。詳細は :ref:`ntf_testdata_data_blocks` を参照。

記述例
======

バッチ処理のリクエスト単体テストの例を以下に示す。1ファイルにテストケース・セットアップ・検証が共存する。

Excelの場合
-----------

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
----------

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

--------------------------
テストデータの基本構造
--------------------------

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
========================

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
