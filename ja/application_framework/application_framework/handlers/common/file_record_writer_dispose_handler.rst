.. _file_record_writer_dispose_handler:

出力ファイル開放ハンドラ
========================================

.. contents:: 目次
  :depth: 3
  :local:

業務アクションやハンドラで開いた出力ファイルを閉じる(リソースの解放)ハンドラ。

.. important::

  このハンドラで解放対象となるのは、 :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` を使用して開いた出力ファイルとなる。
  それ以外のAPI(例えば、 `java.io` パッケージ)を使って開いたリソースについては、個別にクローズ処理を行うこと。

処理の流れは以下のとおり。

.. image:: ../images/FileRecordWriterDisposeHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.io.FileRecordWriterDisposeHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- 汎用データフォーマット -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-dataformat</artifactId>
  </dependency>

制約
------------------------------
なし。

ハンドラキューへの設定について
--------------------------------------------------
このハンドラは、ハンドラキュー上に設定するだけで、後続のハンドラや業務アクションで開いた出力ファイルを自動的にクローズする。
このため、ファイル出力を行う全てのハンドラより手前に設定する必要がある。



