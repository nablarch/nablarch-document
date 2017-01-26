.. _`data_format-definition`:

フォーマット定義ファイルの記述ルール
==================================================

.. contents:: 目次
  :depth: 3
  :local:

.. |br| raw:: html

    <br/>

フォーマット定義ファイルの共通の記法
--------------------------------------------------
フォーマット定義ファイルの共通的な記述ルールについて説明する。

文字コード
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フォーマット定義ファイルの文字コードは ``UTF-8`` となる。


リテラル表記
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
設定値にリテラルを記述する場合は、以下のルールに準拠すること。


.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30 70

  * - リテラル型
    - 説明
  * - 文字列
    - Javaの文字リテラルと同じように ``"`` で値を囲んで記述する。

      なお、Unicodeエスケープや8進数エスケープには対応していない。
      
      記述例
       | "Nablarch"
       | "\\r\\n"

  * - 10進整数
    - Javaの数値リテラルと同じように記述する。

      なお、小数には対応していない。

      記述例
        | 123
        | -123

  * - 真偽値
    - ``true`` または、 ``false`` で設定する。(大文字でも可)

コメント
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
行中の ``#`` 以降をコメントとして扱う。

以下に例を示す。

.. code-block:: bash

  #
  # サンプルファイル
  # 
  file-type:     "Fixed"  # 固定長
  text-encoding: "ms932"  # 文字コードはms932
  record-length:  120     # 各業の長さは120バイト




フォーマット定義ファイルの構造
--------------------------------------------------

フォーマット定義ファイルは大きく以下の2つの要素で構成される。

:ディレクティブ宣言部:
  使用するデータ形式(固定長やJSONなど)やエンコーディングなどの共通設定を定義する。

  詳細は、 :ref:`data_format-definition_directive` を参照。

:レコードフォーマット定義部:
  レコードの内容を定義する。

  具体的には、レコード内のフィールド定義やフィールド毎のデータ型やデータ変換ルールの定義を行う。

  詳細は、 :ref:`data_format-definition_record` を参照

.. _data_format-definition_directive:

ディレクティブ宣言部の定義
--------------------------------------------------

共通で使用可能なディレクティブ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
全てのデータ形式で利用するディレクティブ定義は以下のとおり。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - ディレクティブ
    - 説明
  * - file-type ``必須``
    - データ形式を指定する。 

      標準では以下のデータ形式を指定できる。

      * Fixed(固定長)
      * Variable(CSVやTSVなどの可変長)
      * JSON
      * XML

  * - text-encoding ``必須``
    - .. _data_format-directive_text_encoding:

      文字列フィールドの読み書き時に使用するエンコーディングを指定する。

      使用するJVMで利用できる文字エンコーディングのみ指定可能。例えば、 ``UTF-8`` や ``SJIS`` などを指定する。

      `file-type` にJSONを指定した場合は、以下のエンコーディングのみ指定可能

      * UTF-8
      * UTF-16(BE or LE)
      * UTF-32(BE or LE)

      `file-type` にXMLを指定した場合には、本設定値よりもXML宣言部
      に指定されたエンコーディングが優先される。

  * - record-separator ``任意``
    - レコード終端文字(改行文字)を指定する。

      `file-type` にVariable(可変長)を指定した場合は、 ``必須`` となる。

      `file-type` がJSONまたはXMLの場合には、本設定値は使用しない。

Fixed(固定長)形式で指定可能なディレクティブ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fixed(固定長)形式のデータで利用するディレクティブは以下のとおり。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - ディレクティブ
    - 説明
  * -  record-length ``必須``
    - 1レコードのバイト長を指定する。

  * - positive-zone-sign-nibble ``任意``
    - .. _data_format-positive_zone_sign_nibble:

      符号付きゾーン数値のゾーン部に設定する正符号を16進数表記の文字列で指定する。

      デフォルトでは、 :ref:`text-encoding <data_format-directive_text_encoding>` の値に応じて以下の値が使用される。

      :ASCII互換の場合: 0x3      
      :EBCDIC互換の場合: 0xC

  * - negative-zone-sign-nibble ``任意``
    - .. _data_format-negative_zone_sign_nibble:

      符号付きゾーン数値のゾーン部に設定する負符号を16進数表記の文字列で指定する。

      デフォルトでは、 :ref:`text-encoding <data_format-directive_text_encoding>` の値に応じて以下の値が使用される。

      :ASCII互換の場合: 0x7      
      :EBCDIC互換の場合: 0xD

  * - positive-pack-sign-nibble ``任意``
    - .. _data_format-positive_pack_sign_nibble:
      
      符号付きパック数値の符号ビットに設定する正符号を16進数表記の文字列で指定する。

      デフォルトでは、 :ref:`text-encoding <data_format-directive_text_encoding>` の値に応じて以下の値が使用される。

      :ASCII互換の場合: 0x3      
      :EBCDIC互換の場合: 0xC
  
  * - negative-pack-sign-nibble ``任意``
    - .. _data_format-negative_pack_sign_nibble:
      
      符号付きパック数値の符号ビットに設定する負符号を16進数表記の文字列で指定する。

      デフォルトでは、 :ref:`text-encoding <data_format-directive_text_encoding>` の値に応じて以下の値が使用される。

      :ASCII互換の場合: 0x7      
      :EBCDIC互換の場合: 0xD

  * - required-decimal-point ``任意``
    - 符号無し数値及び符号付き数値の小数点の要否を指定する。

      ``true`` を指定すると書き込むデータに小数点が付与される。

      ``false`` を指定すると、書き込むデータに小数点が付与されない。(固定小数点となる)

      デフォルト動作は 小数点付与( ``true`` )となる。

  * - fixed-sign-position ``任意``
    - 符号付き数値の符号位置を固定するかの要否を指定する。

      符号位置を固定( ``true`` )とした場合、符号位置は項目の先頭に固定される。
      符号位置を非固定( ``false`` )とした場合、符号位置はパディング前の数値の先頭に付加される。

      デフォルト動作は固定( ``true`` )となる。

      例
        :符号位置を固定: -000123456
        :符号位置を非固定: 000-123456

  
  * - required-plus-sign ``任意``
    - 符号付き数値の正の符号の要否を指定する。

      ``true`` を指定した場合、読み込むデータには正の符号( ``+`` )が必要で、
      書き込むデータには正の符号( ``+`` )が付加される。

      デフォルトの動作は付加しない( ``false`` )となる。



以下に例を示す。

.. code-block:: bash

  #
  # ディレクティブ定義部
  #
  file-type:                      "Fixed"  # 固定長ファイル
  text-encoding:                  "ms932"  # 文字列型フィールドの文字エンコーディング
  record-length:                  120      # 各レコードbyte長 
  positive-zone-sign-nibble:      "C"      # ゾーン数値の正符号
  negative-zone-sign-nibble:      "D"      # ゾーン数値の負符号
  positive-pack-sign-nibble:      "C"      # パック数値の正符号
  negative-pack-sign-nibbleL      "D"      # パック数値の負符号
  required-decimal-point:         true     # 小数点あり
  fixed-sign-position:            true     # 符号は先頭に
  required-plus-sign:             false    # 正符号は付加しない

.. _data_format-variable_data_directive:

Variable(可変長)形式で指定可能なディレクティブ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Variable(可変長)形式のデータで利用するディレクティブは以下のとおり。

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - ディレクティブ
    - 説明
  * - field-separator ``必須``
    - フィールド(項目)の区切り文字を指定する。

      例えば、CSVであれば ``,`` を、TSVであれば ``\t`` を指定する。

  * - quoting-delimiter ``任意``
    - フィールド(項目)の値をクォートする際に使用する文字を指定する。

      例えば、ダブルクォートを設定する場合には、 ``"`` を、
      シングルクォートを設定する場合には、 ``'`` を設定する。

      値を設定した場合、全てのフィールド(項目)がクォートされる。

      デフォルトでは、クォートされない。

  * - ignore-blank-lines ``任意``
    - データ読み込み時に空行を無視するか否かを設定する。

      ``true`` を設定した場合、空行(改行のみ)のレコードは無視される。

      デフォルトでは、空行は無視される。

  * - requires-title ``任意``
    - .. _data_format-requires-title:
      
      最初のレコードをタイトルとして読み書きするかどうかを設定する。

      ``true`` を設定した場合、最初のレコードをタイトルとして扱う。

      デフォルトでは、最初のレコードをタイトルとして扱わない。

      タイトルレコードのレイアウト定義は、 :ref:`title-record-type-nameディレクティブ <data_format-title_type_name>` を参照。

  * - title-record-type-name ``任意``
    - .. _data_format-title_type_name:
      
      タイトルのレコードタイプ名を設定する。

      指定しなかった場合、タイトルのレコードタイプ名は ``Title`` となる。

      このディレクティブで指定したレコードタイプ名に紐づくレコードフォーマット定義に従い、タイトルレコードが編集される。

      タイトルのレコードタイプを使ったフォーマット定義ファイルのサンプルは、
      :ref:`タイトルレコードのフォーマット定義例 <data_format-variable_title_sample>` を参照。

      レコードタイプやレコード定義の詳細は、 :ref:`data_format-definition_record` を参照。

  * - max-record-length ``任意``
    - 読み込みを許容する1レコードの文字数を指定する。

      レコードの区切り文字が存在しないデータ(壊れているデータ)を読み込んだ場合、
      レコードを全てヒープ上に展開するとヒープ不足によりプロセスが異常終了する可能性がある。

      このため、このディレクティブに設定した値の文字数を読み込んでもレコードの区切り文字が存在しなかった場合には、
      不正なデータとして読み込み処理を中止し例外を送出する。

      デフォルトでは、1,000,000文字となる。

以下に例を示す。

.. code-block:: bash

  #
  # ディレクティブ定義部
  #
  file-type:                  "Variable"  # 可変長ファイル
  text-encoding:              "utf-8"     # 文字列型フィールドの文字エンコーディング
  record-separator:           "\\r\\n"    # 改行

  field-separator:            ","         # CSV
  quoting-delimiter:          "\""        # ダブルクォートで項目を囲む
  ignore-blank-lines:         true        # 空行は無視
  requires-title:             false       # タイトルレコードは無し
  max-record-length:          1000        # このcsvのレコードには最大でも1000文字まで

JSON形式で指定可能なディレクティブ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSONデータ形式固有のディレクティブは存在しない。

以下に例を示す。

.. code-block:: bash

  file-type:      "JSON"      # jsonフォーマット
  text-encoding:  "utf-8"     # 文字列型フィールドの文字エンコーディング


XML形式で指定可能なディレクティブ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XMLデータ形式固有のディレクティブは存在いない。

以下に例を示す。

.. code-block:: bash

  file-type:      "XML"       # xmlフォーマット
  text-encoding:  "utf-8"     # 文字列型フィールドの文字エンコーディング

.. _data_format-definition_record:

レコードフォーマット定義部
--------------------------------------------------
レコードフォーマット定義部には、レコードを構成するフィールド(項目)の定義情報(レコード内での位置やデータ型など)を設定する。

レコードフォーマット定義例を以下に示す。

ポイント
  * レコードを識別するためのレコードタイプ名を ``[`` 、 ``]`` で囲んで定義する。
  * レコードタイプ名は、フォーマット定義ファイル内で一意となっていること。
  * レコードタイプ名は、任意の値を定義する。
  * レコードタイプの次の行から、レコード内のフィールド(項目)を定義する。
  * フィールド(項目)定義は、フィールド数分繰り返し定義する。
  * フィールド定義の書式については、 :ref:`フィールド定義の書式 <data_format-field_definition>` を参照。

.. code-block:: bash

  [data]              # レコードタイプ名:data
  1 name  N(100)      # 名前
  2 age   X9(3)       # 年齢


.. _data_format-field_definition:

フィールド定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フィールド定義は、以下の形式で定義する。

.. code-block:: text
  
  <フィールド開始位置> <フィールド名> <多重度> <フィールドタイプ> <フィールドコンバータ>

フィールド定義の各要素の詳細は以下のとおり。

.. list-table::
  :class: white-space-normal
  :widths: 30 70

  * - フィールド開始位置 ``必須``
    - データ形式毎以下のルールに従いフィールド開始位置を定義する。

      :Fixed(固定長): フィールドの開始バイト数(1起算)を設定する。
      :Variable(可変長: フィールドの項目通番を設定する。
      :JSON: フィールドの要素通番
      :XML: フィールドの要素通番

  * - フィールド名 ``必須``
    - フィールドを識別するための名前を設定する。

      フィールド名は、 本機能の入出力で使用する :java:extdoc:`java.util.Map` のキーとなる。

      フィールド名の先頭に ``?`` を付加した場合、その項目は入力時には :java:extdoc:`java.util.Map` には読み込まれない。
      例えば、ホストでよく扱われる固定長ファイルのfiller項目に使用することで、余計な項目を入力対象除外できる。

      .. important::

        数字のみのフィールド名は定義できないので注意すること。

      XMLデータ形式の場合、フィールド名の先頭に ``@`` を付加することで、その項目を属性値として扱うことが出来る。

      以下に例を示す。
      
      .. code-block:: bash

        [tagName]
        @attr

      上記に対応したXMLは、以下のようになる。

      .. code-block:: xml

        <tagName attr="val">
        ・・・
        </tagName>

  * - 多重度 ``任意``
    - フィールドの定義可能数を指定する。

      この値は、JSON及びXMLデータ形式の場合のみ指定できる。

      記述ルールは以下のとおり。
        * 定義可能数は、 ``[`` 、 ``]`` で囲んで記述する。
        * 下限と上限がある場合は、下限と上限の間に ``..`` を記述する。
        * 上限がない場合は ``*`` を記述する。
        * 省略した場合は、 ``[1]`` となる。

      以下に指定例を示す。

      .. code-block:: bash

        address [1..3]    # 1から3の定義が可能
        address           # 省略しているので1つだけ可能
        address [0..*]    # 条件なし(0から無制限)
        address [*]       # 条件なし(0から無制限)
        address [1..*]    # 1以上

      以下のxmlの場合、 ``address`` フィールドの定義数は ``2`` となる。

      .. code-block:: xml

        <person>
          <address>自宅住所</address>
          <address>勤務先住所</address>
        </person>

      以下のJSONの場合、 ``address`` フィールドの要素数は、``3`` となる。

      .. code-block:: json

        {
          "address" : ["自宅住所", "勤務先住所", "送付先住所"]
        }
      

  * - フィールドタイプ ``必須``
    - フィールドのデータ型を定義する。

      デフォルトで指定可能なフィールドタイプは、 :ref:`data_format-field_type_list` を参照。

  * - フィールドコンバータ ``任意``
    - フィールドタイプに対するオプションの指定やデータ変換などの入出力の事前処理の内容を定義する。

      デフォルトで指定可能なフィールドタイプは、 :ref:`data_format-field_convertor_list` を参照。

      フィールドコンバータは、複数設定することも出来る。


.. _data_format-multi_layout_data:

マルチフォーマット形式のレコードを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
マルチフォーマット形式のデータの場合は、フォーマット定義ファイル上に複数のレコードフォーマットを定義する。

入出力データが、どのレコードフォーマットかは、特定のフィールドの値によって自動的に判定される。
もし、入出力対象のデータが、どのレコードタイプにもマッチしない場合は、不正データ扱いとし処理を異常終了する。

以下にマルチフォーマット形式のフォーマット定義例を示す。

ポイント
  * レコード識別フィールドを定義する。レコードタイプ名は ``Classifier`` とする。
  * 各レコード定義のレコードタイプ名直下に、レコードと判断するための条件を定義する。
  * レコード識別(Classifier)に定義したフィールドは、レコード定義内に存在している必要がある。

.. code-block:: bash

  file-type:        "Fixed" # 固定長
  text-encoding:    "MS932" # 文字列型フィールドの文字エンコーディング
  record-length:    40      # 各レコードの長さ
  record-separator: "\r\n"  # 改行コード(crlf)

  # レコード識別条件の定義
  [Classifier]
  1 dataKbn X(1)      # 先頭1バイトのフィールドを使用してどのレコードかを判定する

  # ヘッダーレコードの定義
  [header]
  dataKbn = "1"         # dataKbnが"1"の場合ヘッダーレコード
  1 dataKbn X(1)
  2 data    X(39)

  # データレコードの定義
  [data]
  dataKbn = "2"        # dataKbnが"2"の場合データレコード
  1 dataKbn X(1)
  2 data    X(39)

マルチフォーマットの定義サンプルは、以下のリンク先を参照。

.. toctree::
  :maxdepth: 1

  multi_format_example

.. tip::

  JSON及びXMLデータ形式には、レコードの概念が存在しないため、
  マルチフォーマット形式のフォーマット定義には対応していない。

.. _data_format-field_type_list:

フィールドタイプ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
標準で提供するデータタイプ定義一覧を以下に示す。

Fixed(固定長)データ形式で利用可能なフィールドタイプ一覧
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - タイプ
      - Java型
      - 説明

    * - .. _data_format-field_type-single_byte_character_string:

        X
      - String
      - シングルバイト文字列(バイト長 = 文字列長)

        デフォルトでは、半角空白による右トリム及びパディングが行われる。

        :引数: バイト長(数値) ``必須``

        出力対象の値が ``null`` の場合、値を空文字に変換してから処理を行う。

        読み込んだ値が空文字列の場合は、 ``null`` に変換する。
        空文字列を ``null`` に変換したくない場合は、
        :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` に ``false`` を設定する。

    * - N
      - String
      - ダブルバイト文字列 (バイト長 = 文字数 ÷ 2)

        デフォルトでは、全角空白による右トリム・パディングを行う。

        :引数: バイト長(数値) ``必須``

        ※バイト長が2の倍数でない場合は構文エラーとなる。

        出力対象の値が ``null`` の場合や、読み込んだ値が空文字列の場合の扱いは、
        :ref:`シングルバイト文字列のフィールドタイプ <data_format-field_type-single_byte_character_string>` と同じ。

    * - XN
      - String
      - マルチバイト文字列

        UTF-8のようにバイト長の異なる文字が混在するフィールドを扱う場合に、このフィールドタイプを指定する。

        また、全角文字列（ダブルバイト文字列）のパディングに半角スペースを使用する場合にも本フィールドタイプを使用する。

        デフォルトでは、半角空白による右トリム・パディングを行う。

        :引数: バイト長(数値) ``必須``

        出力対象の値が ``null`` の場合や、読み込んだ値が空文字列の場合の扱いは、
        :ref:`シングルバイト文字列のフィールドタイプ <data_format-field_type-single_byte_character_string>` と同じ。

    * - .. _data_format-field_type-zoned_decimal:

        Z
      - BigDecimal
      - ゾーン数値(バイト長 = 桁数)

        デフォルトでは、 ``0`` による左トリム・パディングを行う。

        :引数1: バイト長(数値) ``必須``
        :引数2: 小数点以下桁数(数値) ``任意`` デフォルト: ``0``

        出力対象の値が ``null`` の場合、値を ``0`` に変換してから処理を行う。

        読み込んだ値のバイト数が ``0`` の場合は、 ``null`` に変換する。
        バイト数が ``0`` の場合に ``null`` に変換したくない場合は、
        :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` に ``false`` を設定する。

    * - SZ
      - BigDecimal
      - 符号付きゾーン数値 (バイト長 = 桁数)

        デフォルトでは、 ``0`` による左トリム・パディングを行う。

        :引数1: バイト長(数値) ``必須``
        :引数2: 少数点以下桁数(数値) ``任意`` デフォルト: ``0``
        :引数3: ゾーン部に設定する正符号(16進表記の文字列) ``任意``
        :引数4: ゾーン部に設定する負符号(16進表記の文字列) ``任意``

        引数3及び引数4は、 :ref:`符号付きゾーン数値の正符号 <data_format-positive_zone_sign_nibble>` 及び
        :ref:`符号付きゾーン数値の負符号 <data_format-negative_zone_sign_nibble>` を上書きする場合に設定する。

        出力対象の値が ``null`` の場合や、読み込んだ値のバイト数が ``0`` の場合の扱いは、
        :ref:`ゾーン数値のフィールドタイプ <data_format-field_type-zoned_decimal>` と同じ。

    * - P
      - BigDecimal
      - パック数値 (バイト長 = 桁数 ÷ 2 [端数切り上げ])

        デフォルトでは、 ``0`` による左トリム・パディングを行う。

        :引数1: バイト長(数値) ``必須``
        :引数2: 少数点以下桁数(数値) ``任意`` デフォルト: ``0``

        出力対象の値が ``null`` の場合や、読み込んだ値のバイト数が ``0`` の場合の扱いは、
        :ref:`ゾーン数値のフィールドタイプ <data_format-field_type-zoned_decimal>` と同じ。

    * - SP
      - BigDecimal
      - 符号付きパック数値 (バイト長 = (桁数 + 1) ÷ 2 [端数切り上げ])

        デフォルトでは、 ``0`` による左トリム・パディングを行う。

        :引数1: バイト長(数値) ``必須``
        :引数2: 少数点以下桁数(数値) ``任意`` デフォルト: ``0``
        :引数3: 符号ビットに設定する正符号 (16進表記の文字列) ``任意``
        :引数4: 符号ビットに設定する負符号 (16進表記の文字列) ``任意``

        引数3及び引数4は、 :ref:`符号付きパック数値の正符号 <data_format-positive_pack_sign_nibble>` 及び
        :ref:`符号付きパック数値の負符号 <data_format-negative_pack_sign_nibble>` を上書きする場合に設定する。

        出力対象の値が ``null`` の場合や、読み込んだ値のバイト数が ``0`` の場合の扱いは、
        :ref:`ゾーン数値のフィールドタイプ <data_format-field_type-zoned_decimal>` と同じ。

    * - B
      - byte[]
      - バイナリ列

        パディングやトリムは行わない。

        :引数: バイト長(数値) ``必須``

        出力対象の値が ``null`` の場合の変換仕様はアプリケーションごとに様々である。
        そのため、本フィールドタイプではその場合でも値の変換は行わず、
        :java:extdoc:`InvalidDataFormatException <nablarch.core.dataformat.InvalidDataFormatException>`
        を送出する。

        本フィールドタイプを使用する場合、要件に合わせてアプリケーション側で明示的に値を設定すること。

    * - X9
      - BigDecimal
      - 符号無し数値文字列 (バイト長 = 文字数)

        フィールド中のシングルバイト文字列(X)を数値として扱う。

        デフォルトでは、 ``0`` による左トリム・パディングを行う。
        文字列中に小数点記号( ``.`` )を含めることできる。

        :引数1: バイト長(数値) ``必須``
        :引数2: 固定小数点の場合の小数点以下桁数(数値) ``任意`` デフォルト: ``0``

        出力対象の値が ``null`` の場合の扱いは、
        :ref:`ゾーン数値のフィールドタイプ <data_format-field_type-zoned_decimal>` と同じ。

        読み込んだ値が空文字列の場合の扱いは、
        :ref:`シングルバイト文字列のフィールドタイプ <data_format-field_type-single_byte_character_string>` と同じ。


    * - SX9
      - BigDecimal
      - 符号付き数値文字列 (バイト長 = 文字数)

        フィールド中のシングルバイト文字列(X)を符号付き数値として扱う。
        デフォルトでは、 ``0`` による左トリム・パディングを行う。

        :引数1: バイト長(数値) ``必須``
        :引数2: 固定小数点の場合の小数点以下桁数(数値) ``任意`` デフォルト: ``0``

        出力対象の値が ``null`` の場合の扱いは、
        :ref:`ゾーン数値のフィールドタイプ <data_format-field_type-zoned_decimal>` と同じ。

        読み込んだ値が空文字列の場合の扱いは、
        :ref:`シングルバイト文字列のフィールドタイプ <data_format-field_type-single_byte_character_string>` と同じ。

        符号文字(``+`` 、``-``)を変更したい場合は、以下のクラスの実装を参考にプロジェクト固有のフィールドタイプを作成して対応する。

        * :java:extdoc:`SignedNumberStringDecimal <nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal>`

        フィールドタイプの追加については、 :ref:`data_format-field_type_add` を参照。

Variable(可変長)データ形式で利用可能フィールドタイプ一覧
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - タイプ
      - Java型
      - 説明

    * - X |br|
        N |br|
        XN |br|
        X9 |br|
        SX9
      - String
      - 可変長データ形式では、すべてのフィールドを文字列（String）として読み書きする。

        どのタイプ識別子を指定しても動作は変わらない。
        また、フィールド長の概念が無いので、引数は不要である。

        もし、文字列を数値形式(BigDecimal)として読み書きしたい場合は、
        :ref:`numberコンバータ <data_format-number_convertor>`
        または :ref:`signed_numberコンバータ <data_format-signed_number_convertor>` を使用すること。

        出力対象の値が ``null`` の場合、値を空文字に変換してから処理を行う。
        
        読み込んだ値が空文字列の場合は、 ``null`` に変換する。
        空文字列を ``null`` に変換したくない場合は、 :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.VariableLengthConvertorSetting.setConvertEmptyToNull(boolean)>` に ``false`` を設定する。


JSONおよびXMLデータ形式で利用可能なフィールドタイプ一覧
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - タイプ
      - Java型
      - 説明

    * - .. _data_format-field_type-nullable_string:

        X |br|
        N |br|
        XN
      - String
      - 文字列データタイプ

        パディングなどの編集は行わない。

        JSONの場合は、出力時に値がダブルクォート ``"`` で括られる。

        出力対象の値が ``null`` の場合、JSONでは値の変換は行わなず、
        XMLでは空文字に変換する。

    * - X9 |br|
        SX9 |br|
      - String
      - 数値文字列タイプ

        パディングなどのデータ編集は行わない。出力時は値がそのまま出力される。

        もし、文字列を数値形式(BigDecimal)として読み書きしたい場合は、
        :ref:`numberコンバータ <data_format-number_convertor>`
        または :ref:`signed_numberコンバータ <data_format-signed_number_convertor>` 使用すること。

        出力対象の値が ``null`` の場合の扱いは、
        :ref:`文字列データタイプのフィールドタイプ <data_format-field_type-nullable_string>` と同じ。

    * - BL
      - String	
      - 文字列（ ``true`` or ``false`` を文字列で表したもの）

        パディングなどのデータ編集は行わない。出力時は値がそのまま出力される。

        出力対象の値が ``null`` の場合の扱いは、
        :ref:`文字列データタイプのフィールドタイプ <data_format-field_type-nullable_string>` と同じ。

    * - .. _data_format-nest_object:

        OB
      - \-
      - ネストされたレコードタイプを指定する場合に使用する。

        フィールド名に対応した、レコードタイプがネストした要素として入出力される。

        出力対象の値が ``null`` の場合の扱いは、
        :ref:`文字列データタイプのフィールドタイプ <data_format-field_type-nullable_string>` と同じ。

        以下に使用例を示す。

        json
          .. code-block:: json

            {
              "users": [
                {
                  "name"    : "名前",
                  "age"     : 30,
                  "address" : "住所"
                },
                {
                  "name"    : "名前1",
                  "age"     : 31,
                  "address" : "住所1"
                }
              ]
            }

        xml
          .. code-block:: xml
            
            <users>
              <user>
                <name>名前</name>
                <age>30</age>
                <address>住所</address>
              </user>
              <user>
                <name>名前1</name>
                <age>31</age>
                <address>住所1</address>
              </user>
            </users>

        上記のjson及びxmlに対応したフォーマット定義ファイルは以下のとおり。

        .. code-block:: bash

          [users]       # ルート要素
          1 user [1..*] OB

          [user]        # ネストした要素
          1 name    N   # 最下層の要素
          2 age     X9
          3 address N


.. _data_format-field_convertor_list:

フィールドコンバータ一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
標準で提供するデータコンバータ一覧を以下に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 20 30 50

  * - コンバータ名
    - 型変換仕様
    - 説明

  * - pad
    - 型変換無し
    - パディング及びトリムする文字を設定する。

      パディング及びトリム位置は、フィールドタイプ毎に以下のように動作する。

      :X: 右トリム、右パディング
      :N: 右トリム、右パディング
      :XN: 右トリム、右パディング
      :Z: 左トリム・左パディング
      :SZ: 左トリム・左パディング
      :P: 左トリム・左パディング
      :SP: 左トリム・左パディング
      :X9: 左トリム・左パディング
      :SX9: 左トリム・左パディング

      フィールドタイプの詳細は、 :ref:`data_format-field_type_list` を参照。

      :引数: パディング・トリムの対象となる値 ``必須``

  * - encoding
    - 型変換なし
    - 文字列型フィールドの文字エンコーディングを設定する。

      特定フィールドのみ共通設定( :ref:`text-encoding <data_format-directive_text_encoding>` )を上書きする場合に設定する。

      ``X`` 、 ``N`` 、 ``XN`` フィールドのみに使用することが出来る。
      それ以外のフィールドタイプに設定した場合は、無視される。

      :引数: エンコーディング名(文字列) ``必須``


  * - リテラル値
    - 型変換なし
    - 出力時のデフォルト値を設定する。

      出力時に、値が未設定であった場合に、指定されたリテラル値を出力する。

      入力時には、この設定値は使用しない。

  * - .. _data_format-number_convertor:
    
      number
    - String <-> BigDecimal
    - 数字文字列を数値(BigDecimal)に変換する場合に設定する。

      :入力時: 入力された数字文字列が符号なし数値形式であることをチェックし、\
               BigDecimal型に変換する。

      :出力時: 出力する値を文字列に変換し、符号なし数値形式であることをチェック後に出力する。

  * - .. _data_format-signed_number_convertor:
      
      signed_number

    - String <-> BigDecimal

    - 符号付きの数字文字列を数値(BigDecimal)に変換する場合に設定する。

      符号が許可される点以外は、 :ref:`numberコンバータ <data_format-number_convertor>` と同じ仕様となる。

  * - .. _data_format-replacement_convertor:
      
      replacement
    - 型変換なし
    - 入出力とも、置換え対象文字を変換先の文字に置換して返す。

      :引数: 置き換えタイプ名 ``任意``

      詳細は、 :ref:`data_format-replacement` を参照。


項目定義の省略について
--------------------------------------------------
フォーマット定義ファイルの項目定義と実際のデータの項目定義が合わない場合の振る舞いについて説明する。

固定長及び可変長データの場合
  固定長及び可変長データの場合は、実際のデータとフォーマット定義の項目定義は厳密に一致させる必要がある。
  このため、アプリケーションで不要となる項目が存在しているような場合でも、フォーマット定義ファイル上には項目を定義する必要がある。

JSON及びXMLデータの場合
  JSON及びXMLの場合には、フォーマット定義ファイル上に定義されていない項目は、読み取り対象外となる。
  このため、実際のデータ上に存在している項目でも、アプリケーションで不要なのであれば項目定義を行わなくてもよい。
  

