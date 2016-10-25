.. _data_converter:

様々なフォーマットのデータへのアクセス
==================================================
様々なフォーマットのデータを扱う機能を提供する。

Nablarchでは、以下の2種類のデータ入出力機能を提供している。

.. toctree::
  :maxdepth: 1

  データバインド(データとJava Beansオブジェクトをマッピングする機能) <data_io/data_bind>
  汎用データフォーマット(フォーマット定義ファイルを元にデータ入出力を行う機能) <data_io/data_format>

.. _data_converter-data_bind_recommend:

上記のどちらの機能を使用した場合でも、データアクセスを行うことができるが、
以下の理由により :ref:`data_bind` を使用することを推奨する。

* :ref:`data_bind` は、データをJava Beansオブジェクトとして扱えるため、IDEの補完が有効活用でき開発効率が良い。(項目名のタイプミスなどが起こりえないメリットも有る）
* :ref:`data_format` は、フォーマットの定義が複雑で理解し難い。これにより、学習コストやメンテナンスコストが高くなる。

.. important::

  :ref:`data_bind` で扱うことのできないフォーマットについては、 :ref:`data_format` を使用する必要がある。

.. tip::

  :ref:`data_bind` と :ref:`data_format` で提供している機能の違いは、 :ref:`data_io-functional_comparison` を参照。

.. toctree::
  :hidden:

  data_io/functional_comparison


