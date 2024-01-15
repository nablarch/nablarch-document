.. _slf4j_adaptor:

SLF4Jアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

JavaのOSSは `SLF4J(外部サイト、英語) <https://www.slf4j.org/>`_ を使用してログ出力しているモジュールが多く、
これらのモジュールを使用した場合にNablarchの :ref:`ログ出力機能 <log>` にログ出力を集約したい場合がある。
このケースに対応するため、SLF4JのAPIを経由してNablarchのログ出力機能でログ出力を行うアダプタを提供する。

モジュール一覧
--------------------------------------------------

.. code-block:: xml

  <!-- SLF4Jアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
  </dependency>

.. tip::

  SLF4Jのバージョン2.0.11を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。
  なお、SLF4Jのバージョン2.0.0以降はロギング実装の検索方法が変わっている。例えば互換性のない1.7系のバージョンが使用された場合、以下のログが出力され、以降のログ出力が行われないため注意すること。

  .. code-block:: none

    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.  

SLF4Jアダプタを使用する
--------------------------------------------------
SLF4Jが実行時に必要なクラスを自動で検出するため、本アダプタはSLF4Jアダプタをプロジェクトの依存モジュールに追加するだけで使用できる。
ログ出力の設定はNablarchの :ref:`ログ出力機能 <log>` を参照すること。

.. code-block:: xml

  <!-- SLF4Jアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
    <scope>runtime</scope>
  </dependency>
