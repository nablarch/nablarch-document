.. _router_adaptor:

ルーティングアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

`http-request-router(外部サイト) <https://github.com/kawasima/http-request-router>`_ を使用して、
リクエストURLと業務アクションのマッピングを行うアダプタ。

本アダプタを使用することで、 :ref:`ウェブアプリケーション <web_application>` や :ref:`RESTfulウェブサービス <restful_web_service>` を
構築する際に、URLと業務アクションのマッピングを容易に定義できる。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- ルーティングアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-router-adaptor</artifactId>
  </dependency>

  <!-- http-request-router -->
  <dependency>
    <groupId>net.unit8</groupId>
    <artifactId>http-request-router</artifactId>
  </dependency>

ルーティングアダプタを使用するための設定を行う
--------------------------------------------------
本アダプタを使用するための手順を以下に示す。

ディスパッチハンドラを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ディスパッチハンドラとして、 :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` をハンドラキューの最後に設定する。

設定例を以下に示す。

ポイント
 * コンポーネント名は **packageMapping** とする。
 * basePackage属性には、アクションクラスが格納されているパッケージを設定する。
   (アクションクラスが複数のパッケージに格納されている場合は、共通となる親パッケージを設定する。)
 * :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` を初期化対象のリストに設定する。

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="basePackage" value="sample.web.action" />
  </component>

  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- その他のハンドラは省略 -->
        <component-ref name="packageMapping" />
      </list>
    </property>
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- その他の初期化処理は省略 -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

ルート定義ファイルを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
クラスパス直下に `routes.xml` を作成し、
指定したURLと業務アクションをマッピングする設定を行う。

ルート定義ファイルへの設定方法は、`ライブラリのREADMEドキュメント(外部サイト) <https://github.com/kawasima/sastruts-advanced-routes/blob/master/README.ja.md>`_ を参照。

業務アクションとURLを自動的にマッピングする
--------------------------------------------------------
ルート定義ファイルにて、 `match` タグのpath属性に ``:controller`` や ``:action``
といったパラメータを使用することで業務アクションとURLの自動マッピングを行うことができる。

.. important::

  アプリケーションサーバに `JBoss` や `WildFly` を使用している場合、この機能は使用できない。
  `get` タグ等を使用して個別に業務アクションとURLのマッピングを定義すること。

.. important::

  `get` タグ等を使用したマッピングの個別定義とこの機能の併用は推奨しない。
  併用した場合に、業務アクションとURLがどのようにマッピングされるかが、ルート定義ファイル上から読み取りづらくなる問題があるため。

この機能を有効にするには、クラスパス直下に作成した `net/unit8/http/router` ディレクトリに
`routes.properties` を作成し、以下のとおり値を設定する。

.. code-block:: bash

  router.controllerDetector=nablarch.integration.router.NablarchControllerDetector

ルート定義ファイルへの設定とマッピングの例を以下に示す。

ルート定義ファイル
  .. code-block:: xml

    <routes>
      <match path="/action/:controller/:action" />
    </routes>

業務アクションとマッピングするURLの例
  ==================== =====================
  業務アクション       URL
  ==================== =====================
  PersonAction#index   /action/person/index
  PersonAction#search  /action/person/search
  LoginAction#index    /action/login/index
  ==================== =====================
