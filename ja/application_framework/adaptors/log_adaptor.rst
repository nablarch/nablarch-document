.. _log_adaptor:

logアダプタ
==================================================
Nablarchの提供する :ref:`ログ出力機能 <log>` のログ出力処理を以下のログフレームワークに委譲するアダプタ。

* `slf4j(外部サイト、英語) <https://www.slf4j.org/>`_ 
* `JBoss Logging(外部サイト、英語) <https://github.com/jboss-logging>`_

顧客からの要求や使用する製品などにあわせてロガーを統一したい場合に、アダプタを使用する。
アダプタを使用した場合、 Nablarchの :ref:`ログ出力機能 <log>` を使用したログ出力処理は全て選択したロギングフレームワークに委譲される。

.. important::

  Nablarch5u15まで提供されていたlog4jアダプタは、EOLを迎えた `log4j1.2(外部サイト、英語) <https://logging.apache.org/log4j/1.x/>`_ を使用しており
  `脆弱性 <https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-013606.html>`_ への修正が公開されないため廃止します。
  slf4jまたはJBoss Loggingを使用してください。

.. tip::

  ロギングフレームワークの設定方法などは、製品のマニュアルなどを参照すること。
  
モジュール一覧
--------------------------------------------------

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- slf4jアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-slf4j-adaptor</artifactId>
  </dependency>

.. important::

  slf4jにはFATALレベルが存在しないため、nablarch-slf4j-adaptorはFATALレベルでログ出力しようとした場合は全てERRORレベルで出力する仕様となっている。

.. tip::
  
  slf4jのバージョン2.0.11を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。


JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- JBoss Loggingアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jboss-logging-adaptor</artifactId>
  </dependency>
  
.. tip::
  
  JBoss Loggingのバージョン3.3.0.Finalを使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。
  
ロギングフレームワークを使用するための設定を行う
--------------------------------------------------
:ref:`ログ出力機能 <log>` の設定ファイル(\ **log.properties**\ )にファクトリを設定する。
この設定によりログ出力処理が、ロギングフレームワークに委譲される。

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # slf4jを使用するためのファクトリの設定
  loggerFactory.className=nablarch.integration.log.slf4j.Slf4JLoggerFactory
  
JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # JBoss Loggingを使用するためのファクトリの設定
  loggerFactory.className=nablarch.integration.log.jbosslogging.JbossLoggingLoggerFactory
