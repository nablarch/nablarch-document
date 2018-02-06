=====================================
データフォーマッタの拡張
=====================================

本サンプルで提供するフォーマッタ機能の仕様を解説する。

フォーマッタ機能の概要、基本となる汎用データフォーマット機能に関する詳細は、Nablarch Application Framework解説書の汎用データフォーマット機能に関する解説を参照すること。

----------------------------
概要
----------------------------

Nablarchが用意しているフォーマッタ（例えば、Json形式やXml形式）とは別のフォーマッタを利用したい場合、
データフォーマッタを追加することで対応できる。

本サンプルでは、HTTPのPOSTパラメータのように、
Key項目=Value項目を&で結合するようなデータ形式(application/x-www-form-urlencoded)に対応したフォーマッタを作成する場合を想定している。



提供パッケージ
--------------------------------------------------------------------

本機能は、下記のパッケージで提供される。

  *please.change.me.* **core.dataformat**

  *please.change.me.* **core.dataformat.convertor**

  *please.change.me.* **test.core.file**

.. _ExtendedFormatter_FormUrlEncodedFormatter:



FormUrlEncodedデータフォーマッタの構成
--------------------------------------------------------------------

FormUrlEncodedデータフォーマッタはapplication/x-www-form-urlencodedで使用されるデータを取り扱う。
このデータはname1=value1&name2=value2のように、名前と値の組を等号でつなげたものをアンド記号で結んで表現される。
同一のキーで複数の値を扱うこともできる。

値についてURLエンコードを行う。
キーについては汎用データフォーマットのフォーマット定義書式に従いURLエンコードは行わず、特殊文字をキー文字列に使用することはできない。

以下に本機能で使用するクラス一覧を記す。

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - パッケージ名
     - クラス名
     - 概要
   * - *please.change.me.* **core.dataformat**
     - FormUrlEncodedDataFormatterFactory
     - | フォーマッタファクトリクラス。
       | サンプル実装ではcreateFormatter(String fileType, String formatFilePath)メソッドをオーバーライドし、FormUrlEncodedDataRecordFormatterのインスタンス生成を可能としている。
   * - *please.change.me.* **core.dataformat**
     - FormUrlEncodedDataRecordFormatter
     - | フォーマッタクラス。
       | application/x-www-form-urlencodedで使用されるデータを解析、構築する。
       | サンプル実装では読み込み時はパラメータの出現順を意識せず、書き込み時はフォーマット定義順でパラメータを出力する。
   * - *please.change.me.* **core.dataformat.convertor**
     - FormUrlEncodedDataConvertorFactory
     - | データコンバータのファクトリクラス。
       | デフォルトのコンバータ名とコンバータ実装クラスの対応表を保持する。
   * - *please.change.me.* **core.dataformat.convertor**
     - FormUrlEncodedDataConvertorSetting
     - | コンバータの設定情報を保持するクラス。
       | コンバータ名とコンバータ実装クラスの対応表を、DIコンテナから設定する。
   * - *please.change.me.* **test.core.file**
     - FormUrlEncodedTestDataConverter
     - | テストデータコンバータクラス。
       | サンプル実装ではテストデータとして項目ごとにKey=Value形式を設定されたデータを解析し、Value部の値に対し動的にURLエンコーディングを行う。


----------------------------
使用方法
----------------------------

FormUrlEncodedデータフォーマッタの使用方法
--------------------------------------------------------------------
  業務アプリケーションで作成したフォーマッタファクトリクラスを使用する場合、以下の設定を行う必要がある。

  .. code-block:: xml

    <component name="formatterFactory" class="please.change.me.core.dataformat.FormUrlEncodedDataFormatterFactory"/>


フォーマット定義ファイルの記述例
--------------------------------------------------------------------
  サンプルのソースコードに対応するフォーマット定義ファイルの記述例を以下に示す。

  .. code-block:: bash

    #
    # ディレクティブ定義部
    #
    file-type:     "FormUrlEncoded"  # フォームURLエンコード形式ファイル
    text-encoding: "UTF-8"  # 文字列型フィールドの文字エンコーディング

    #
    # データレコード定義部
    #
    [data]
    1    key1   X      # 項目1
    2    key2   X      # 項目2


フィールドタイプ・フィールドコンバータ定義一覧
--------------------------------------------------------------------
  FormUrlEncodedデータフォーマッタで使用されるフィールドタイプ・フィールドコンバータについて解説する。

  **フィールドタイプ**

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - タイプ識別子
     - Java型
     - 内容

   * - X、N、XN、X9、SX9
     - String
     - | FormUrlEncodedデータフォーマッタでは、すべてのフィールドを文字列（String）として読み書きする。
       | よって、どのタイプ識別子を指定しても動作は変わらない。
       | また、フィールド長の概念が無いので、引数は不要である。
       | もしNumber型（BigDecimalなど）のデータを読み書きしたい場合は、後述のnumber/signed_numberコンバータを使用すること。

  いずれのタイプ識別子もフィールド長の概念が無いので、引数は不要である。

  **フィールドコンバータ**

  .. list-table::
   :widths: 70 100 350
   :header-rows: 1

   * - コンバータ名
     - Java型(変換前後)
     - 内容

   * - リテラル値
     - Object <-> Object
     - | **入力時:** (なにもしない)
       | **出力時:** 出力する値が未設定であった場合に指定されたリテラル値を出力する。
       | **デフォルト実装クラス:** nablarch.core.dataformat.convertor.value.DefaultValue
       | **引数:** なし

   * - number
     - String <-> BigDecimal
     - | **入力時:** 入力された値が符号なし数値であることを形式チェックした上でBigDecimal型に変換して、返却する。
       |         もし入力された値がnullまたは空文字の場合、nullを返却する。
       | **出力時:** 出力する値を文字列に変換し、符号なし数値であることを形式チェックした上で出力する。
       |         もし出力する値がnullの場合、空文字を出力する。
       | **デフォルト実装クラス:** nablarch.core.dataformat.convertor.value.NumberString
       | **引数:** なし

   * - signed_number
     - String <-> BigDecimal
     - | 符号が許可される点以外は **number** コンバータと同じ仕様。
       | **デフォルト実装クラス:** nablarch.core.dataformat.convertor.value.SignedNumberString
       | **引数:** なし


同一キーで複数の値を取り扱う場合
--------------------------------------------------------------------
  同一キーで複数の値を取り扱う場合、データはString配列形式で保持される。
  また、フォーマット定義ファイルにて多重度を設定する必要がある。
  定義方法についてはNablarch Application Framework解説書の汎用データフォーマット機能を参照すること。


テストデータの記述方法
--------------------------------------------------------------------

  FormUrlEncodedデータフォーマッタを使用した場合、入力データをURLエンコーディングする必要がある。
  しかし、URLエンコーディングされたデータをExcelファイルに直接記述することは、可読性や保守性、作業効率といった面で現実的ではない。
  そのため、以下の例のようにテストデータコンバータを指定する。

  テストデータコンバータについてはプログラミング・単体テストガイドの自動テストフレームワークの使用方法を参照すること。

  **コンポーネント設定ファイル**

    テスト側のコンポーネント設定ファイルに以下の設定を追記する。

    .. code-block:: xml

      <!-- テストデータコンバータ定義 -->
      <component name="TestDataConverter_FormUrlEncoded"
                 class="please.change.me.test.core.file.FormUrlEncodedTestDataConverter"/>

  **Excelファイル**

    以下のようにfile-typeに"FormUrlEncoded"を指定し、テストデータとして項目ごとにKey-Value形式となるように記述する。

    .. image:: ./_images/test_data_example.png

    この場合、テストデータ読み込み時にテストフレームワークによりFormUrlEncodedTestDataConverterが呼び出され、
    結果的にFormUrlEncodedデータフォーマッタには以下のデータが入力される。

    .. code-block:: text

      kanjiName=%E6%BC%A2%E5%AD%97%E6%B0%8F%E5%90%8D&kanaName=%E3%82%AB%E3%83%8A%E3%82%B7%E3%83%A1%E3%82%A4&mailAddr=test%40anydomain.com



