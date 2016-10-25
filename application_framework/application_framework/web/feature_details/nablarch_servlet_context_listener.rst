.. _nablarch_servlet_context_listener:

Nablarchサーブレットコンテキスト初期化リスナ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

本クラスはサーブレットコンテキストリスナとして定義されており、
ウェブアプリケーションの起動時、終了時に以下の処理を行う。

起動時
 * :ref:`repository` の初期化処理
 * :ref:`log` の初期化処理

終了時
 * :ref:`log` の終了処理

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-applog</artifactId>
  </dependency>

システムリポジトリを初期化する
--------------------------------------------------

システムリポジトリの初期化を行うには、以下の設定を行う必要がある。

* サーブレットコンテキストリスナとして、本クラスを登録する。
* サーブレットコンテキストの初期化パラメータとして、コンポーネント設定ファイルのパスを設定する。

`web.xml` への設定例を以下に示す。

ポイント
 * コンポーネント設定ファイルのパスのパラメータ名は **di.config** とすること。

.. code-block:: xml

  <context-param>
    <param-name>di.config</param-name>
    <param-value>web-boot.xml</param-value>
  </context-param>

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>