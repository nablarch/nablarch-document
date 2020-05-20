.. _batch_application:

バッチアプリケーション編
==================================================
本章ではNablarchアプリケーションフレームワークを利用してバッチアプリケーションを開発するために必要となる情報を提供する。

Nablarchのバッチアプリケーションでは、以下2種類のバッチアプリケーションのフレームワークを提供している。

.. toctree::
  :maxdepth: 1

  jsr352/index
  nablarch_batch/index

どちらのフレームワークを使用してもバッチアプリケーションを構築することができるが、
以下の理由により :doc:`jsr352/index` を使用してバッチアプリケーションを作成することを推奨する。

理由
  :doc:`nablarch_batch/index` は、 `JSR352(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=352>`_ や `Spring Batch(外部サイト、英語) <http://projects.spring.io/spring-batch/>`_ [#spring_batch]_ に似ているが、異なる部分が数多く存在している。
  このため、 :doc:`nablarch_batch/index` を使用した場合、多くを学ぶ必要があり学習コストが高くなるデメリットがある。
  また、似て非なる部分が開発者の混乱の元となり、開発生産性を下げるデメリットがある。

.. tip::

  :ref:`jsr352_batch` と :ref:`nablarch_batch` で提供している機能の違いは、 :ref:`batch-functional_comparison` を参照。


.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison


.. [#spring_batch] JSR352は、Spring Batchから多くの機能を引き継いで標準化されている。このため、Spring Batchの経験者は多くを学ぶことなくJSR352を使用したバッチアプリケーションの開発が行える。
