.. _log4j_adaptor:

log4jアダプタ
==================================================
Nablarchの提供する :ref:`ログ出力機能 <log>` のログ出力処理をlog4jに委譲するアダプタ。

顧客からの要求などで、log4jを使用しなければならない場合にこのアダプタを使用する。
このアダプタを使用した場合、Nablarchの :ref:`ログ出力機能 <log>` を使用したログ出力処理は全てlog4jに委譲される。

.. tip::

  log4jの使用、設定方法などは、 `log4jの公式サイト(外部サイト、英語) <http://logging.apache.org/log4j/1.2/>`_ を参照すること。

.. _log4j:

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- log4jアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-log4j-adaptor</artifactId>
  </dependency>

  <!-- log4j(1.2系の最新版) -->
  <dependency>
  <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
      <version>1.2.17</version>
  </dependency>

log4jでログ出力するための設定を行う
--------------------------------------------------
:ref:`ログ出力機能 <log>` の設定ファイル(\ **log.properties**\ )に以下の設定を行う。
この設定により、ログ出力処理がlog4jに委譲される。

.. code-block:: properties

  # log4jを使用するためのファクトリの設定
  loggerFactory.className=nablarch.core.log.log4j.Log4JLoggerFactory

.. tip::

  ログレベルなどの設定は、log4jの設定ファイルに行う必要がある。
  詳細は、log4jのマニュアルを参照すること。

