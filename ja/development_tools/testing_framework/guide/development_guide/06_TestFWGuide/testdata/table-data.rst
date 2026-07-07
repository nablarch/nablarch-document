.. _ntf_testdata_table_data:

================
テーブルデータ
================

テストデータは Excel または YAML ファイルで記述できる。

各エントリはカラム名と値の組み合わせで記述する。省略したカラムには INSERT 時にデフォルト値が補完される。

テーブルデータの形式
====================

Excelの場合
-----------

1行目にカラム名、2行目以降にデータを記述する。

.. code-block:: text

    SETUP_TABLE=テーブル名
    | カラム1 | カラム2 | カラム3 |
    | 値1     | 値2     | 値3     |

YAMLの場合
----------

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
===========

DB への INSERT 用データである。

- 各エントリのカラム名と値を記述する。
- 主キーカラムは省略しないこと。省略すると型に応じたデフォルト値（数値型は ``"0"`` 、文字型はスペース等）が INSERT される。

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

記述例を以下に示す。

Excelの場合
-----------

.. code-block:: text

    SETUP_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | RATE | PROFILE          | PHOTO                          |
    | 0000000101 | 山田太郎 | 1    | 85000 | 1.5  | ゴールド会員です | ${binaryFile:testdata.txt}     |
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

- 値は文字列で記述する（ ``"0000000101"`` のようにクォート）。
- NULL 値はアンクォートの ``null`` で記述する（ ``"null"`` とクォートしても同じく Java null になる）。
- ``${binaryFile:パス}`` はファイル内容をバイナリ読み込みして HexString に変換する。

EXPECTED_TABLE
==============

テスト後の DB 状態と比較するデータである。省略したカラムは比較対象外となる。検証したいカラムだけを列挙できる。

記述例を以下に示す。

Excelの場合
-----------

.. code-block:: text

    EXPECTED_TABLE=MEMBER
    | MEMBER_ID  | NAME     | RANK | SCORE | UPDATED_DATE          |
    | 0000000101 | 山田太郎 | 1    | 87500 | 2024-04-01 09:00:00.0 |
    | 0000000102 | 鈴木花子 | 2    | 42000 | 2024-04-01 09:00:00.0 |

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

EXPECTED_COMPLETE_TABLE
=======================

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
            # UPDATE_DATE を省略 → BasicDefaultValues のデフォルト値で補完されて比較

LIST_MAP
========

キーバリュー形式の汎用データである。テストケース定義（ ``testShots`` ）・リクエストパラメータ・期待値オブジェクト・期待ログなど様々な用途で使う。

- ID は完全一致で検索される。
- 同一ファイル内で同一 ID の重複エントリは先着一致で、2件目以降は無視される。
- 指定 ID のエントリが存在しない場合は空データ扱い（エラーにならない）。

主な予約 ID は :ref:`ntf_testdata_testshots` を参照。

記述例を以下に示す。

Excelの場合
-----------

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

マーカーカラムについては以下の通り。

- 角括弧で囲んだカラム（ ``[no]`` ・ ``[desc]`` ）はマーカーカラムである。DB 操作から除外される（Excel 上の見やすさのために使うことが多い）。
- YAML ではダブルクォートで囲む（ ``"[no]"`` ）。YAML の角括弧構文との衝突を避けるためである。
