.. _log_adaptor:

logアダプタ
==================================================
Nablarchの提供する :ref:`ログ出力機能 <log>` のログ出力処理を以下のログフレームワークに委譲するアダプタ。

* `log4j(外部サイト、英語) <http://logging.apache.org/log4j/1.2/>`_ 
* `slf4j(外部サイト、英語) <https://www.slf4j.org/>`_ 
* `JBoss Logging(外部サイト、英語) <https://github.com/jboss-logging>`_

顧客からの要求や使用する製品などにあわせてロガーを統一したい場合に、アダプタを使用する。
アダプタを使用した場合、 Nablarchの :ref:`ログ出力機能 <log>` を使用したログ出力処理は全て選択したロギングフレームワークに委譲される。

.. tip::

  ロギングフレームワークの設定方法などは、製品のマニュアルなどを参照すること。
  
モジュール一覧
--------------------------------------------------

log4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
  
slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- slf4jアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-slf4j-adaptor</artifactId>
  </dependency>

  <!-- slf4j -->
  <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
  </dependency>

JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- JBoss Loggingアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jboss-logging-adaptor</artifactId>
  </dependency>

  <!-- JBoss Logging -->
  <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
  </dependency>
  
  
ロギングフレームワークを使用するための設定を行う
--------------------------------------------------
:ref:`ログ出力機能 <log>` の設定ファイル(\ **log.properties**\ )に以下の設定を行う。
この設定によりログ出力処理が、ロギングフレームワークに委譲される。

log4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # log4jを使用するためのファクトリの設定
  loggerFactory.className=nablarch.integration.log.log4j.Log4JLoggerFactory

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
