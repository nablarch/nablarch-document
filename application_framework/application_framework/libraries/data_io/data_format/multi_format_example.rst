Fixed(固定長)のマルチフォーマット定義のサンプル集
--------------------------------------------------

単一のフィールドでフォーマットを識別する例
  単一フィールドが条件の場合、そのフィールド値が各フォーマットに定義した条件と一致した場合に、そのレコード定義で処理される。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1の場合、headerレコードタイプとなる。
  * dataKbnが2の場合、dataレコードタイプとなる。

  .. code-block:: bash

    file-type:        "Fixed" # 固定長
    text-encoding:    "MS932" # 文字列型フィールドの文字エンコーディング
    record-length:    40      # 各レコードの長さ
    record-separator: "\r\n"  # 改行コード(crlf)

    # レコード識別フィールドの定義
    [Classifier]
    1 dataKbn X(1)

    # ヘッダーレコードの定義
    [header]
    dataKbn = "1"
    1 dataKbn X(1)
    2 data    X(39)

    # データレコードの定義
    [data]
    dataKbn = "2"
    1 dataKbn X(1)
    2 data    X(39)

複数のフィールドでフォーマットを識別する例
  複数のフィールドでレコードを識別する場合、全ての条件を満たした場合に、そのレコード定義で処理される。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1でtypeが01の場合、parentDataレコードタイプとなる。
  * dataKbnが2でtypeが02の場合、childDataレコードタイプとなる。

  .. code-block:: bash

    file-type:        "Fixed" # 固定長
    text-encoding:    "MS932" # 文字列型フィールドの文字エンコーディング
    record-length:    40      # 各レコードの長さ
    record-separator: "\r\n"  # 改行コード(crlf)

    # レコード識別フィールドの定義
    [Classifier]
    1   dataKbn X(1)      # 先頭1バイト
    10  type    X(2)      # 10バイト目から2バイト

    [parentData]
    dataKbn = "1"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [childData]
    dataKbn = "1"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

レコード毎に識別項目が異なる場合の例
  レコード毎に識別に使用する項目が異なる場合、レコード識別フィールドには識別に使用する全てのフィールドを定義する。
  個別のレコードの条件定義部には、そのレコードを識別する条件を定義する。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1の場合、headerレコードタイプとなる。
  * dataKbnが2でtypeが01の場合、data1レコードタイプとなる。
  * dataKbnが2でtypeが02の場合、data2レコードタイプとなる。

  .. code-block:: bash

    file-type:        "Fixed" # 固定長
    text-encoding:    "MS932" # 文字列型フィールドの文字エンコーディング
    record-length:    40      # 各レコードの長さ
    record-separator: "\r\n"  # 改行コード(crlf)

    # レコード識別フィールドの定義
    [Classifier]
    1   dataKbn X(1)      # 先頭1バイト
    10  type    X(2)      # 10バイト目から2バイト

    # ヘッダー
    [header]
    dataKbn = "1"
    1  dataKbn X(1)
    2  ?filler X(39)

    [data1]
    dataKbn = "2"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [data2]
    dataKbn = "2"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

Variable(可変長)でマルチフォーマット定義のサンプル集
------------------------------------------------------------
Variable(可変長)データのマルチフォーマットの定義方法について説明する。

単一のフィールドでフォーマットを識別する例
  単一フィールドが条件の場合、そのフィールド値が各フォーマットに定義した条件と一致した場合に、そのレコード定義で処理される。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1の場合、headerレコードタイプとなる。
  * dataKbnが2の場合、dataレコードタイプとなる。

  .. code-block:: bash

    file-type:        "Variable" # 可変長
    text-encoding:    "MS932"    # 文字列型フィールドの文字エンコーディング
    record-separator: "\r\n"     # 改行コード(crlf)
    field-separator:  ","        # csv


    # レコード識別フィールドの定義
    [Classifier]
    1 dataKbn X

    # ヘッダーレコードの定義
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 data    X

    # データレコードの定義
    [data]
    dataKbn = "2"
    1 dataKbn X
    2 data    X

複数のフィールドでフォーマットを識別する例
  複数のフィールドでレコードを識別する場合、全ての条件を満たした場合に、そのレコード定義で処理される。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1でtypeが01の場合、parentDataレコードタイプとなる。
  * dataKbnが2でtypeが02の場合、childDataレコードタイプとなる。

  .. code-block:: bash

    file-type:        "Variable" # 可変長
    text-encoding:    "MS932"    # 文字列型フィールドの文字エンコーディング
    record-separator: "\r\n"     # 改行コード(crlf)
    field-separator:  ","        # csv

    # レコード識別フィールドの定義
    [Classifier]
    1 dataKbn X
    3 type    X

    [parentData]
    dataKbn = "1"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [childData]
    dataKbn = "1"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X
 
レコード毎に識別項目が異なる場合の例
  レコード毎に識別に使用する項目が異なる場合、レコード識別フィールドには識別に使用する全てのフィールドを定義する。
  個別のレコードの条件定義部には、そのレコードを識別する条件を定義する。

  このサンプルでは、以下のルールでレコードが識別される。

  * dataKbnが1の場合、headerレコードタイプとなる。
  * dataKbnが2でtypeが01の場合、data1レコードタイプとなる。
  * dataKbnが2でtypeが02の場合、data2レコードタイプとなる。

  .. code-block:: bash

    file-type:        "Variable" # 可変長
    text-encoding:    "MS932"    # 文字列型フィールドの文字エンコーディング
    record-separator: "\r\n"     # 改行コード(crlf)
    field-separator:  ","        # csv

    # レコード識別フィールドの定義
    [Classifier]
    1   dataKbn X
    3   type    X

    # ヘッダー
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 ?filler X

    [data1]
    dataKbn = "2"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [data2]
    dataKbn = "2"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

.. _data_format-variable_title_sample:

タイトルレコードを使用した場合の例
  :ref:`タイトルレコードあり <data_format-requires-title>` の可変長ファイルの場合、タイトルレコードに関してはレコード識別条件を定義する必要が無い。

  タイトルレコード以外のフォーマットがシングルフォーマットの場合には、以下の例のようにレコード識別( ``Classifier`` )の定義は不要となる。
  タイトルレコードのレイアウト定義は、レコードタイプ名を ``Title`` として定義する。

  .. code-block:: bash

    # requires-titleがtrueの場合、最初の行をタイトルとして読み書きできる。
    requires-title: true  

    # タイトル固有のレコードタイプ。最初の行はこのレコードタイプで読み書きされる。
    [Title]               
    1   Kubun      N
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

    # データのレコードタイプ。最初の行以降の行はこのレコードタイプで読み書きされる。
    [DataRecord]          
    1   Kubun      X
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

  タイトルレコード以外のフォーマットがマルチフォーマットの場合には、以下の例のようにレコード識別( ``Classifier`` )の定義が必要となる。
  タイトルレコードを示すレコードタイプが ``Title`` のレコード定義については、マルチフォーマット時に必要となる条件定義は必要ない。

  .. code-block:: bash

    file-type:    "Variable"     # 可変長
    text-encoding:     "ms932"   # ファイルエンコーディング
    record-separator:  "\r\n"    # CRLFで改行
    field-separator:   ","       # フィールド区切り文字
    quoting-delimiter: "\""      # 囲み文字
    requires-title: true         # 最初の行をタイトルとして読み書きする


    [Classifier]
    1  Kubun X                   # レコードタイプ識別フィールド（データ区分）
                                 # 1: データ、2: トレイラ

    # タイトル固有のレコードタイプ。マルチフォーマットでもフォーマットの適用条件は不要。
    [Title]                      
    1   Kubun      N  "データ区分"
    2   Name       N  "書籍名"
    3   Publisher  N  "出版社"
    4   Authors    N  "著者"
    5   Price      N  "価格"

    [DataRecord]                 # データのレコードタイプ
      Kubun = "1"                # データのフォーマットの適用条件
    1   Kubun      X             # データ区分
    2   Name       N             # 書籍名
    3   Publisher  N             # 出版社
    4   Authors    N             # 著者
    5   Price      N             # 価格

    [TrailerRecord]              # トレイラのレコードタイプ
      Kubun = "2"                # トレイラのフォーマットの適用条件
    1   Kubun      X             # データ区分
    2   RecordNum  X             # 総件数

  .. tip::
    
    タイトルレコードのレコードタイプ名を ``Title`` から変更したい場合には、 :ref:`data_format-title_type_nameディレクティブ <data_format-title_type_name>` を使用すること。
    その場合には、タイトルレコードを示すレコードタイプ名を ``Title`` ではなく、:ref:`data_format-title_type_nameディレクティブ <data_format-title_type_name>` で設定した値に変更すること。

