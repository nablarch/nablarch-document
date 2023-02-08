.. _web_front_controller:

Webフロントコントローラ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

ウェブアプリケーションにおけるハンドラキューの実行の起点となるクラス。

本クラスを使用することで、クライアントから受け取ったリクエストに対する処理をハンドラキューに委譲できる。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

.. _handlerqueue:

ハンドラキューを設定する
--------------------------------------------------
リクエストに対する処理をハンドラキューに委譲するための手順を示す。

コンポーネント設定ファイルに設定する
  :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` をコンポーネント設定ファイルに設定し、
  :java:extdoc:`handlerQueue <nablarch.fw.HandlerQueueManager.setHandlerQueue(java.util.Collection)>` プロパティに
  アプリケーションで使用するハンドラを順番に追加していく。

  コンポーネント設定ファイルの設定例を以下に示す。

  ポイント
   * コンポーネント名は **webFrontController** とすること。

  .. code-block:: xml

    <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>

          <!-- 省略 -->

        </list>
      </property>
    </component>

サーブレットフィルタを設定する
  :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>`
  をサーブレットフィルタとして `web.xml` に設定する。
  このフィルタによって、クライアントから受け取ったリクエストに対する処理は、先ほどシステムリポジトリに登録したハンドラキューへ委譲される。

  `web.xml` への設定例を以下に示す。

  ポイント
   * システムリポジトリを初期化するため、 :ref:`nablarch_servlet_context_listener` をリスナーとして設定すること。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>entryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>

    <filter-mapping>
      <filter-name>entryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
    </filter-mapping>

移譲するWebフロントコントローラを変更する
--------------------------------------------------

  コントローラ名を `web.xml` に設定する。
  サーブレットフィルタが移譲するコントローラ名のデフォルト値は **webFrontController** であるため、 :ref:`handlerqueue` でコンポーネント名を
  **webFrontController** とした場合、この設定は不要である。
  
  `web.xml` への設定例を以下に示す。

  ポイント
   * controllerNameのパラメータ値としてコントローラ名を設定する。
   * ウェブアプリケーションとウェブサービスを併用するなどの場合に、ハンドラ構成を分けるために使用する。

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>webEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>
    <filter>
      <filter-name>jaxrsEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
      <init-param>
        <param-name>controllerName</param-name>
        <param-value>jaxrsController</param-value>
      </init-param>
    </filter>

    <filter-mapping>
      <filter-name>webEntryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
      <url-pattern>/</url-pattern>
    </filter-mapping>
    <filter-mapping>
      <filter-name>jaxrsEntryPoint</filter-name>
      <url-pattern>/api/*</url-pattern>
    </filter-mapping>

