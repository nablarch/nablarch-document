.. _`nablarch_Batch_getting_started`:

Getting Started
==========================================
本章を通読することで、Nablarchバッチアプリケーション方式のバッチの開発イメージを掴むことができる。

前提条件
  本章は :ref:`example_application` をベースに解説を行う。
  Exampleアプリケーションの動作環境を事前に構築しておくこと。

  .. tip::
    Exampleアプリケーションに関する以下の事項は、本章では解説しない。
    以下の事項については、 :ref:`example_application` を参照すること。

    - Exampleアプリケーションの環境構築および実行
    - Exampleアプリケーションの設定
    - 使用しているOSSプラグインについて

.. toctree::
  :maxdepth: 1

  nablarch_batch/index

.. tip::
 Nablarchバッチアプリケーションでは、 :ref:`都度起動バッチ<nablarch_batch-each_time_batch>` と
 :ref:`常駐バッチ<nablarch_batch-resident_batch>` でアプリケーションの実装方法に違いがないため、
 別々にGetting Startedを用意していない。
 :ref:`都度起動バッチ<nablarch_batch-each_time_batch>` と
 :ref:`常駐バッチ<nablarch_batch-resident_batch>` で異なるのは、ハンドラ構成のみである。
