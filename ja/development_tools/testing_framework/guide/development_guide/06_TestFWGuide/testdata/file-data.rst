.. _ntf_testdata_file_data:

================
ファイルデータ
================

テストデータは Excel または YAML ファイルで記述できる。

セットアップ用ファイルデータ（ ``SETUP_FIXED`` / ``SETUP_VARIABLE`` ）は固定長・可変長の区別なくまとめて収集される。期待値ファイル（ ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE`` ）も同様である。固定長か可変長かはデータブロック内の記述で区別される。

``setup_files`` / ``expected_files`` の各エントリには ``path`` キーが必須である（省略時はエラー）。

ファイルデータブロックの構造
============================

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
==============

注文データのバッチ処理テスト。固定長の入力ファイルを読み込んで処理し、結果を固定長の出力ファイルに書き出すことを確認するケースを以下に示す。

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

エンコーディング指定付き固定長ファイル
======================================

MS932 エンコーディングで顧客データファイルを読み込むケースを以下に示す。

Excelの場合
-----------

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
----------

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
==============

可変長ファイルではフィールド長（ ``length`` ）の記述が不要である。CSV 形式の顧客データファイルを入力として使うケースを以下に示す。

Excelの場合
-----------

.. code-block:: text

    SETUP_VARIABLE=input/data.csv
    | field-separator | ,       |           |        |
    | DATA            | USER_ID | USER_NAME | AMOUNT |
    |                 | X       | N         | X      |
    |                 | 001     | 山田太郎  | 5000   |
    |                 | 002     | 鈴木花子  | 3000   |

YAMLの場合
----------

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

groupId 付きファイル
====================

テストケースごとに異なる入力ファイルを使い分けるケースを以下に示す。

Excelの場合
-----------

groupId はデータブロック種別ラベルの ``[...]`` で指定する。

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

groupId は ``group_id:`` フィールドで指定する。省略するとグループ ID なし（デフォルトグループ）扱いである。

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

1ファイルデータブロック内に複数のレコードレイアウトを連続して記述できる。データの後ろに新たなレコード種別とフィールド名称を書くと、新しいレコードレイアウトとして扱われる。

1ファイルに HEADER レコードと DATA レコードが混在する振込依頼ファイルを扱うケースを以下に示す。

Excelの場合
-----------

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
----------

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
==========

0バイトの空ファイルを表現するには、ディレクティブのみを記述してレコード定義を省略する。出力ファイルがゼロ件のときに空ファイルを生成することを確認するケースを以下に示す。

Excelの場合
-----------

ディレクティブ行のみ記述してレコード定義以降を省略する。

.. code-block:: text

    SETUP_FIXED=input/empty.dat
    | text-encoding | MS932 |

YAMLの場合
----------

レコードは ``records: []`` と空配列で記述する。

.. code-block:: yaml

    setup_files:
      - path: input/empty.dat
        type: fixed
        directives:
          text-encoding: MS932
        records: []

その他の仕様
============

``"-"`` 長フィールド
--------------------

フィールド長に ``"-"`` を指定すると、追加された全レコードの最大バイト長に自動拡張される。値は改行コードと前後空白が除去される。

エラーになるケース
------------------

以下の場合にエラーとなる。

- 同一レコード種別内でフィールド名称が重複している
- フィールド名称リストまたはデータ型リストが未指定または空
- フィールド名称・データ型・フィールド長リストのサイズが一致していない
- 存在しないフィールド名称を指定している
- データ要素数が不正
- ディレクティブまたはレコード種別/フィールド名称定義の要素数が2未満
- ファイルの読み込みに失敗した（IO エラー）
- 日付型カラムの値が日付として解析できない
