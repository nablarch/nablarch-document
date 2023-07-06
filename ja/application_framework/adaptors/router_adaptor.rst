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

.. tip::
  
  http-request-routerのバージョン0.1.1を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

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
指定したURLと業務アクションのマッピングを設定する。

ルート定義ファイルへの設定方法は、`ライブラリのREADMEドキュメント(外部サイト) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ を参照。

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
  ========================== ===========================
  業務アクション              URL
  ========================== ===========================
  PersonAction#index         /action/person/index
  PersonAction#search        /action/person/search
  LoginAction#index          /action/login/index
  ProjectUploadAction#index  /action/projectUpload/index
  ========================== ===========================

.. _router_adaptor_path_annotation:

Jakarta RESTful Web ServicesのPathアノテーションでマッピングする
--------------------------------------------------------------------
本アダプタのバージョン1.2.0から、Jakarta RESTful Web Servicesの ``jakarta.ws.rs.Path`` アノテーション（以下 ``Path`` アノテーションと表記）を使ったルーティングのマッピングができるようになった。

ここでは、既存の :ref:`RESTfulウェブサービス <restful_web_service>` に対して ``Path`` アノテーションを使ったルーティングを有効にする方法と、各種設定の詳細について説明する。

.. important::

  本機能は、クラスパス配下のリソースを独自のファイルシステムで管理している一部のウェブアプリケーションサーバでは使用できない。

  例えば、JbossやWildflyでは、vfsと呼ばれるバーチャルファイルシステムで
  クラスパス配下のリソースが管理されるため、 ``Path`` アノテーションで注釈されたクラスの検索ができない。

  そのようなウェブアプリケーションサーバを使用する場合は、従来通りXMLを用いたルーティングの定義を使用すること。

ディスパッチハンドラを変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XMLのマッピング定義を使用する場合は、ディスパッチハンドラの実装として :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` を使用していた。
一方、 ``Path`` アノテーションによるマッピング定義を用いる場合は、 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` をディスパッチハンドラとして設定する必要がある。

.. code-block:: xml

  <!-- Pathアノテーションによるルーティング定義を有効にする場合の設定例 -->
  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="pathOptionsProvider">
      <component class="nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider">
        <property name="applicationPath" value="${nablarch.webApi.applicationPath}" />
        <property name="basePackage" value="${nablarch.commonProperty.basePackage}" />
      </component>
    </property>

    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>
  </component>

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- 省略 -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

| ``Path`` アノテーションによるルーティングを使用するには、 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` の ``pathOptionsProvider`` プロパティに :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>` を設定する。
| （``methodBinderFactory`` プロパティの設定については :ref:`jaxrs_adaptor` を参照）

さらに、この :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>` には、次の２つのプロパティを設定する必要がある。

**applicationPath**

  | マッピングするパスに共通するプレフィックスを設定する。
  | Jakarta RESTful Web Services の ``jakarta.ws.rs.ApplicationPath`` アノテーションで設定する値と同じものを意味する。

**basePackage**

  | ``Path`` アノテーションが設定されたクラスを検索する、ルートとなるパッケージ名を設定する。


定義した :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` のコンポーネントは初期化が必要なので、初期化対象のリストに追加する。

.. code-block:: xml

  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="packageMapping" />
        <!-- 省略 -->
      </list>
    </property>
  </component>

以上の設定により、 ``Path`` アノテーションによるルーティングの登録機能が使用できるようになる。

マッピングの実装方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``Path`` アノテーションを使ってマッピングを定義した実装例を以下に示す。

.. code-block:: java

    @Path("/sample")
    public class SampleAction {

        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public List<Person> findAll() {
            // 省略
        }

        @POST
        @Produces(MediaType.APPLICATION_JSON)
        public int register(HttpRequest request) {
            // 省略
        }
    }

| アクションクラスを ``Path`` アノテーションで注釈することで、 ``Path`` アノテーションの ``value`` で設定したパスとアクションクラスを紐づけることができる。
| さらに、 ``jakarta.ws.rs.GET`` などのHTTPメソッドを表すアノテーションでアクションクラスのメソッドを注釈することで、HTTPメソッドとアクションクラスのメソッドを紐づけることができる。

上記の実装例では、次のように HTTP リクエストがディスパッチされる。


============ ============== ============================
パス          HTTPメソッド    ディスパッチされるメソッド
============ ============== ============================
``/sample``   ``GET``        ``SampleAction#findAll()``
``/sample``   ``POST``       ``SampleAction#register(HttpRequest)``
============ ============== ============================

.. tip::
 HTTPメソッドを紐づけるアノテーションは、標準で以下のものが用意されている。

  * ``jakarta.ws.rs.DELETE``
  * ``jakarta.ws.rs.GET``
  * ``jakarta.ws.rs.HEAD``
  * ``jakarta.ws.rs.OPTIONS``
  * ``jakarta.ws.rs.PATCH``
  * ``jakarta.ws.rs.POST``
  * ``jakarta.ws.rs.PUT``

さらに、以下のようにメソッドを ``Path`` アノテーションで注釈することで、サブパスのマッピングも定義できる。

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo() {
            // 省略
        }

        @GET
        @Path("/bar")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar() {
            // 省略
        }
    }

この場合、HTTPリクエストのディスパッチは次のようになる。

================ ============== ============================
パス              HTTPメソッド    ディスパッチされるメソッド
================ ============== ============================
``/sample/foo``   ``GET``       ``SampleAction#findAll()``
``/sample/bar``   ``GET``       ``SampleAction#register(HttpRequest)``
================ ============== ============================

パスパラメータの定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
次のように、パスにパラメータを含めることもできる。

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo/{param}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo(HttpRequest request) {
            String param = request.getParam("param")[0];
            // 省略
        }

        @GET
        @Path("/bar/{id : \\d+}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar(HttpRequest request) {
            int id = Integer.parseInt(request.getParam("id")[0]);
            // 省略
        }
    }

| パスパラメータはhttp-request-routerの記法ではなく、Jakarta RESTful Web Servicesの仕様に従った形で記述する。
| これは、本機能（``Path`` アノテーションによるルーティング定義）がJakarta RESTful Web Servicesの仕様に準拠しているためである。

| パスの一部を ``{パラメータ名}`` と記述することで、その部分をパラメータとして定義できる。
| ここで定義したパラメータ名を :java:extdoc:`HttpRequest#getParam(String) <nablarch.fw.web.HttpRequest.getParam(java.lang.String)>` に渡すことで、パスパラメータの値を取得できる。

| さらに、 ``{パラメータ名 : 正規表現}`` と記述することで、そのパスパラメータの書式を正規表現で定義できる。
| 上記実装例では ``\\d+`` と正規表現を指定しているので、パスの値が数値のときのみメソッドがディスパッチされるようになる。

HTTPリクエストのディスパッチの例は次のようになる。

===================== ============== ============================
パス                   HTTPメソッド    ディスパッチされるメソッド
===================== ============== ============================
``/sample/foo/hello`` ``GET``        ``SampleAction#foo(HttpRequest)``
``/sample/foo/world`` ``GET``        ``SampleAction#foo(HttpRequest)``
``/sample/bar/123``   ``GET``        ``SampleAction#bar(HttpRequest)``
``/sample/bar/987``   ``GET``        ``SampleAction#bar(HttpRequest)``
===================== ============== ============================

ルーティング定義を一覧で確認する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` によって読み込まれたルーティング定義は、初期化時にデバッグレベルでログに出力される。

デフォルトでは、次のようにしてルーティングの一覧がログに出力される。

.. code-block:: text

    2020-07-20 13:35:53.092 -DEBUG- nablarch.integration.router.PathOptionsProviderRoutesMapping [null] boot_proc = [] proc_sys = [jaxrs] req_id = [null] usr_id = [null] GET /api/bar => com.example.BarAction#findAll
    GET /api/bar/fizz => com.example.BarAction#fizz
    GET /api/foo => com.example.FooAction#findAll
    POST /api/foo => com.example.FooAction#register
    DELETE /api/foo/(:id) => com.example.FooAction#delete
    GET /api/foo/(:id) => com.example.FooAction#find
    POST /api/foo/(:id) => com.example.FooAction#update

ログのフォーマットを変更したい場合は、 :java:extdoc:`PathOptionsFormatter <nablarch.integration.router.PathOptionsFormatter>` を実装したクラスを作り、 :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` の ``pathOptionsFormatter`` プロパティに設定する。

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="methodBinderFactory">
      <!-- 省略 -->
    </property>
    <property name="pathOptionsProvider">
      <!-- 省略 -->
    </property>

    <property name="pathOptionsFormatter">
      <!-- 自作のフォーマットクラスを設定する -->
      <component class="com.example.CustomPathOptionsFormatter" />
    </property>
  </component>
