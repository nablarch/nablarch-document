.. _nablarch_servlet_context_listener:

Nablarchサーブレットコンテキスト初期化リスナー
==================================================

.. contents:: 目次
  :depth: 3
  :local:

本クラスはサーブレットコンテキストリスナーとして定義されており、
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

システムリポジトリの初期化を行うには、以下のとおり設定する必要がある。

* サーブレットコンテキストリスナーとして、本クラスを登録する。
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

初期化の成否を後続処理で取得する
--------------------------------------------------

本クラスの初期化に成功したか否かは、:java:extdoc:`NablarchServletContextListener#isInitializationCompleted <nablarch.fw.web.servlet.NablarchServletContextListener.isInitializationCompleted()>` を使用して取得できる。
初期化に成功した場合は上記メソッドは ``true`` を返却する。

本クラスの初期化に失敗するとアプリケーションの起動も失敗するが、サーブレットコンテキストリスナーを複数登録していた場合は、
本クラスの後続のサーブレットコンテキストリスナーの処理が実行されることがある。
この機能を使用することで本クラスの後続のサーブレットコンテキストリスナーにおいて、
以下のようにシステムリポジトリの初期化に成功した場合だけ処理を続行するといった分岐が可能となる。

.. code-block:: java

  public class CustomServletContextListener implements ServletContextListener {
      @Override
      public void contextInitialized(ServletContextEvent sce) {
          if(NablarchServletContextListener.isInitializationCompleted()){
            // システムリポジトリを使用した処理
          }
      }

なお、サーブレットコンテキストリスナーの実行順は `web.xml` に記載した順序となる。
システムリポジトリを使用するサーブレットコンテキストリスナーを登録する場合は、
以下のように本クラスより後に `web.xml` に記載する必要がある。
また、 ``@WebListener`` アノテーションによるサーブレットコンテキストリスナーの登録では実行順序は保証されないため、
必ず `web.xml` で定義すること。

.. code-block:: xml

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>
  <listener>
    <listener-class>please.change.me.CustomServletContextListener</listener-class>
  </listener>

.. tip::

  複数のサーブレットコンテキストリスナーが登録されている場合に、先に実行されたサーブレットコンテキストリスナーの処理の例外を検知して処理を中止するか、
  例外を無視して後続のサーブレットコンテキストリスナーの処理を継続するかはサーブレットコンテナの実装に依存する。