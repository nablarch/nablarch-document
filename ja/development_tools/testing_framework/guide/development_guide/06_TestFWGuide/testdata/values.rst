.. _ntf_testdata_values:

================================
値・ディレクティブ・コメント
================================

テストデータは Excel または YAML ファイルで記述できる。

本節ではテストデータの値の書き方、インタープリタ、ディレクティブ、コメントおよびヘッダの仕様を説明する。

--------------
値の書き方
--------------

値の種類と記法
==============

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
=====================

- ``rows:`` 内のすべてのデータ値は **必ずダブルクォートで囲む**。クォートなしだと SnakeYAML が数値・真偽値に型変換する。
- ``null`` のみクォートなしで記述する（ ``"null"`` でも同じく Java null になる）。
- ``type:`` , ``record_type:`` , ``path:`` 等のスキーマ構造値はクォート不要である。

**Excel のセル書式**: セルは必ず **文字列書式** で記述する。数値・日付書式の動作は保証されない。

日付型・Timestamp・特殊値の例
==============================

``EXPECTED_TABLE`` で日付・タイムスタンプ・NULL・システム日時を使うケースを以下に示す。

Excelの場合
-----------

.. code-block:: text

    EXPECTED_TABLE=SCHEDULE
    | ID | EVENT_NAME   | START_DATE     | CREATED_AT            |
    | 1  | 会議         | 2024-01-15     | 2024-01-01 09:00:00.0 |
    | 2  | NULLテスト   | NULL           | NULL                  |
    | 3  | システム時刻 | ${systemTime}  | ${systemTime}         |
    | 4  | 更新時刻     | ${updateTime}  | ${setUpTime}          |

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
          - ID: "4"
            EVENT_NAME: "更新時刻"
            START_DATE: "${updateTime}"
            CREATED_AT: "${setUpTime}"

- ``NULL`` 文字列は ``NullInterpreter`` が Java null に変換する。大文字小文字不問（ ``null`` ・ ``Null`` も同様）。YAML ではアンクォートの ``null`` で記述し、 ``"null"`` とクォートすると文字列として格納される。
- ``${systemTime}`` は完全一致のみ変換される。文字列中に埋め込むには ``CompositeInterpreter`` との組み合わせが必要。
- ``java.sql.Timestamp`` 型カラムの期待値は末尾 ``.0`` が必須（ ``"2024-01-01 09:00:00.0"`` ）。末尾 ``.0`` がないとアサートが失敗する。

QuotationTrimmer によるスペース値明示記法
=========================================

空白値やダブルクォート文字を明示して記述するケースを以下に示す。

Excelの場合
-----------

.. code-block:: text

    EXPECTED_TABLE=ITEM
    | ID | NAME | MEMO |
    | 1  | " "  | """  |

YAMLの場合
----------

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
==============

BLOB カラムにバイナリデータを記述するケースを以下に示す。

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

- ``0x`` プレフィクス付き16進数でバイナリ値を記述する。 ``0x`` がない場合は文字列としてエンコードされる。
- ``${binaryFile:パス}`` でファイル内容をバイナリ読み込みして HexString に変換する。

--------------------------------
インタープリタチェーンの仕組み
--------------------------------

テストデータの値はパース時にインタープリタチェーンを通過して変換される。DI 設定で注入されたインタープリタが順番に適用される。

インタープリタ一覧
==================

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

DateTimeInterpreter の完全一致制約
===================================

``DateTimeInterpreter`` は完全一致のみ変換する。部分文字列は変換されない。文字列中の ``${...}`` を置換するには ``CompositeInterpreter`` との組み合わせが必要である。

文字種生成の有効文字種
======================

14種類の文字種が使用できる: 半角英字 / 半角数字 / 半角記号 / 半角カナ / 全角英字 / 全角数字 / 全角ひらがな / 全角カタカナ / 全角漢字 / 全角記号その他 / 中国語 / サロゲートペア / 改行 / 外字。

上記以外の文字種を指定するとエラーになる。

BinaryFileInterpreter のパス基準
=================================

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
================================

有効な記述形式は以下の通り。

- ``yyyyMMddHHmmssSSS`` （17文字）
- 後置0埋め短縮形
- JDBC タイムスタンプエスケープ形式（5文字目が ``-`` ）

``java.sql.Timestamp`` 型カラムの期待値は末尾 ``.0`` が必須である（例: ``"2010-01-01 12:34:56.0"`` ）。末尾 ``.0`` がないとアサートが失敗する。

X9/SX9 型フィールドの記述
==========================

パディング文字・符号を含めた実際のバイト列表現（固定長フォーマットの実値）をそのまま記述する。

.. _ntf_testdata_values_typemap:

データ型マッピング
==================

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

---------------
ディレクティブ
---------------

ディレクティブの構成
====================

ディレクティブは「キー名・値」の2要素で記述する（最低2要素必要）。

- **Excel**: ファイルデータブロックの先頭（レコード定義より前）に ``| キー名 | 値 |`` の形で記述する。
- **YAML**: ``directives:`` オブジェクトに ``key: value`` 形式で記述する。

固定長ファイルのディレクティブ
================================

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
------------------------------

エンコーディングとゾーン10進数の符号ニブルを指定するケースを以下に示す。

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    SETUP_FIXED=input/data.dat
    | text-encoding              | MS932 |
    | positive-zone-sign-nibble  | C     |
    | DATA | USER_ID | AMOUNT |
    |      | X       | Z      |
    |      | 10      | 10     |
    |      | 001     | 5000   |

YAMLの場合
~~~~~~~~~~

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

可変長ファイルのディレクティブ
================================

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
------------------------------

タブ区切り・CRLF 改行のファイルを扱うケースを以下に示す。

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    SETUP_VARIABLE=input/data.tsv
    | field-separator  | \t    |
    | record-separator | CRLF  |
    | DATA | FIELD1 | FIELD2 |
    |      | X      | X      |
    |      | value1 | value2 |

YAMLの場合
~~~~~~~~~~

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
              - {name: FIELD1, type: X}
              - {name: FIELD2, type: X}
            rows:
              - ["value1", "value2"]

デフォルトディレクティブの DI 設定
====================================

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

------------------------------
ヘッダ・コメント・空エントリ
------------------------------

ヘッダの構造
============

ヘッダにはカラム名を列挙する。

- ヘッダ末尾の空カラムは除去される（末尾カラムの省略が可能）。
- データエントリがヘッダより少ない場合、不足分は空文字 ``""`` で補完される。

マーカーカラム
==============

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
======================

エントリをコメントとしてマークすると、そのエントリ全体がスキップされる。

- **Excel**: 先頭要素が ``//`` で始まる行はスキップされる。
- **YAML**: ``#`` がコメント記号（行頭・行末どちらにも使える）。

要素途中からのコメント
======================

- **Excel**: 先頭以外の要素が ``//`` で始まる場合、その要素以降が切り捨てられる。
- **YAML**: ``#`` を行末に書いて同等の記述ができる（例: ``NUMBER_COL: "100"  # 数値カラム`` ）。

記述例（コメントとマーカーカラム）
====================================

Excelの場合
-----------

.. code-block:: text

    SETUP_TABLE=TEST_TABLE
    | // この行はコメントです  |            |         |            |        |
    | [no]                     | PK_COL1    | PK_COL2 | NUMBER_COL | [desc] |
    | 1                        | 0000000001 | AB      | 100        | テスト1 |
    | // この行もスキップされます |          |         |            |        |
    | 2                        | 0000000002 | CD      | 200        | テスト2 |

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

空エントリのスキップ
====================

全要素が null または空文字のエントリは読み飛ばされる。

- **Excel**: 行の全セルが空の場合にスキップされる。
- **YAML**: ``rows:`` 内の要素が空マッピング（ ``{}`` ）またはすべての値が空文字の場合にスキップされる。

記述例
------

Excelの場合
~~~~~~~~~~~

.. code-block:: text

    SETUP_TABLE=USER
    | USER_ID | NAME     |
    | 001     | 山田太郎 |
    |         |          |
    | 002     | 鈴木花子 |

YAMLの場合
~~~~~~~~~~

.. code-block:: yaml

    setup_tables:
      - table: USER
        rows:
          - USER_ID: "001"
            NAME: "山田太郎"
          # 空行はここには書かない（YAML にはそもそも空エントリの概念がない）
          - USER_ID: "002"
            NAME: "鈴木花子"
