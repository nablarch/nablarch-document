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
以下の理由により :doc:`nablarch_batch/index` を使用してバッチアプリケーションを作成することを推奨する。

理由
  :doc:`nablarch_batch/index` は、基本となる :ref:`nablarch_architecture` を :doc:`ウェブアプリケーション<../web/index>` 、 :doc:`ウェブサービス<../web_service/index>` 、
  :doc:`メッセージング<../messaging/index>` の実行基盤と共有している。同じアーキテクチャとすることで、別の実行基盤経験者を混乱させることなくバッチアプリケーション開発にアサインすることができる。
  また、JSR352については2020年時点で情報が少なく有識者もアサインしにくいため、:doc:`nablarch_batch/index` を使用してバッチアプリケーションを作成することを推奨する。

.. tip::

  :ref:`jsr352_batch` と :ref:`nablarch_batch` で提供している機能の違いは、 :ref:`batch-functional_comparison` を参照。


.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison

