.. _`data_io-functional_comparison`:

データバインドと汎用データフォーマットの比較表
----------------------------------------------------------------------------------------------------
この章では、以下の機能の比較を示す。

* :ref:`data_bind`
* :ref:`data_format`


.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
  :header-rows: 1
  :class: something-special-class

  * - 機能
    - データバインド
    - 汎用データフォーマット

  * - CSVの入出力ができる
    - ○ |br|
      :ref:`解説書へ <data_bind-csv_format>`
    - ○ |br|
      :ref:`解説書へ <data_format-support_type>`

  * - レコード毎にフォーマットの異なる |br| CSVの入出力ができる
    - × [#csv_multi_format]_
    - ○ |br|
      :ref:`解説書へ <data_format-multi_layout_data>`

  * - CSVの定義を設定できる |br|
      (カンマやクォート文字を変更することできる)
    - ○ |br|
      :ref:`解説書へ <data_bind-csv_format>`
    - ○ |br|
      :ref:`解説書へ <data_format-variable_data_directive>`

  * - 固定長データの入出力ができる
    - × [#fixed_layout]_
    - ○ |br|
      :ref:`解説書へ <data_format-support_type>`

  * - レコード毎にフォーマットの異なる |br| 固定長データの入出力ができる
    - × [#fixed_layout]_
    - ○ |br|
      :ref:`解説書へ <data_format-multi_layout_data>`

  * - JSONデータの入出力ができる
    - × [#json_layout]_
    - ○ |br|
      :ref:`解説書へ <data_format-support_type>`

  * - XMLデータの入出力ができる
    - × [#xml_layout]_
    - ○ |br|
      :ref:`解説書へ <data_format-support_type>`

  * - データ入出力時に値の変換ができる |br|
      (trimやパック数値やゾーン数値の変換など)
    - × [#converter]_
    - ○ |br|
      :ref:`解説書へ <data_format-value_convertor>`

  * - データの寄せ字ができる |br|
      システムで許容可能な文字への変換などを指す
    - × [#char_replace]_
    - ○ |br|
      :ref:`解説書へ <data_format-replacement>`

.. [#csv_multi_format] レコード毎に異なるフォーマットのCSVを扱う場合には、 :ref:`data_format` を使用すること。
.. [#fixed_layout] 固定長データの入出力は未実装。固定長データを扱う場合は、 :ref:`data_format` を使用すること。
.. [#json_layout] JSONデータの入出力は未実装。JSONデータを扱う場合は、 :ref:`data_format` やOSSを使用すること。
.. [#xml_layout] XMLデータの入出力は未実装。XMLデータを扱う場合は、 :ref:`data_format` やJAXBを使用すること。
.. [#converter] 出力前及び入力後にデータの形式変換などを行うこと。
.. [#char_replace] 入力データの寄せ字(文字変換)は、文字変換用のハンドラを作成し対応すること

.. |br| raw:: html

  <br />
