.. _view_velocity:

Velocityを使用した画面開発
==================================================
`Velocity(外部サイト、英語) <http://velocity.apache.org/>`_ を使用した画面開発について解説する。。

Velocityの導入手順は以下の通り。なお、詳細な手順については、 `Velocityのドキュメント <http://velocity.apache.org/tools/devel/view-servlet.html>`_ を参照。

1. :ref:`velocity-pom`
2. :ref:`velocity-servlet`
3. :ref:`velocity-configuration`
4. :ref:`velocity-create_vm`
5. :ref:`2重サブミットを防止する(必要な場合のみ) <velocity-use_token>`

.. _velocity-pom:

Velocityを依存ライブラリに追加する
--------------------------------------------------
Velocityをプロジェクトで使用可能にするために依存ライブラリに追加する。
Mavenを利用している場合は、POMに以下を追加する。
なお、本解説書は下のdependencyに記載のバージョンにて確認を行っています。

.. code-block:: xml

  <dependency>
    <groupId>org.apache.velocity</groupId>
    <artifactId>velocity-tools</artifactId>
    <version>2.0</version>
    <!-- servlet-apiを除外しないとアプリケーション実行時に例外が送出される場合があるため除外する -->
    <exclusions>
      <exclusion>
        <groupId>javax.servlet</groupId>
        <artifactId>servlet-api</artifactId>
      </exclusion>
    </exclusions>
  </dependency>


.. _velocity-servlet:

VelocityViewServletの設定を行う
--------------------------------------------------
``web.xml`` に ``VelocityViewServlet`` を登録し、 ``*.vm`` に反応するようにする。

.. code-block:: xml

  <servlet>
    <servlet-name>velocity</servlet-name>
    <servlet-class>
      org.apache.velocity.tools.view.VelocityViewServlet
    </servlet-class>

    <!-- velocityの設定ファイルのパスを設定する -->
    <init-param>
      <param-name>org.apache.velocity.properties</param-name>
      <param-value>/WEB-INF/velocity.properties</param-value>
    </init-param>

    <!-- ツールボックスファイルのパスを設定する(必要な場合) -->
    <init-param>
      <param-name>org.apache.velocity.toolbox</param-name>
      <param-value>/WEB-INF/tools.xml</param-value>
    </init-param>

  </servlet>

  <servlet-mapping>
    <servlet-name>velocity</servlet-name>
    <url-pattern>*.vm</url-pattern>
  </servlet-mapping>

.. _velocity-configuration:

Velocityへの設定を行う
--------------------------------------------------
:ref:`velocity-servlet` の ``org.apache.velocity.properties`` パラメータに指定したファイルを作成し、Velocityに対する設定を行う。
:ref:`velocity-servlet` の例では、 ``/WEB-INF/velocity.properties`` を設定しているため、WARルート配下に ``/WEB-INF/velocity.properties`` を作成する。

設定例
  .. code-block:: properties

    # テンプレートファイルと出力する際のエンコーディングを指定
    input.encoding = UTF-8
    output.encoding = UTF-8

    # 上記以外については、ドキュメントを参照し設定すること

.. _velocity-create_vm:

テンプレートファイル(vmファイル)を作成しActionを実装する
-------------------------------------------------------------------
テンプレートファイル(vmファイル)を作成し配置する。(テンプレートの作成方法は、Velocityのドキュメントを参照)
Actionクラスでは、レスポンスとしてテンプレートファイルへのパスを返却する。

例えば、 ``webapp/WEB-INF/template/index.vm`` を使用してhtmlをクライアントに返したい場合は、Actionクラスは以下のようにレスポンスを返却する。
(webappはWARのルートとなるディレクトリ)

.. code-block:: java

  return new HttpResponse("/WEB-INF/template/index.vm");

.. tip::

  Velocityによって生成されたhtmlがクライアントに返却される仕組みは以下の通り。

  1. :ref:`http_response_handler` が ``/WEB-INF/template/index.vm`` に対してServlet forwardを行う。
  2. 拡張子の ``vm`` に反応し ``VelocityViewServlet`` が実行され、テンプレートとリクエストスコープ等のデータを元にhtmlを生成する。
  3. 生成したhtmlをクライアントに返す。

.. _velocity-use_token:

2重サブミットを防止する
--------------------------------------------------
2重サブミットを防止したい場合は、 :ref:`use_token_interceptor` を参照しAction及びテンプレートファイル(vmファイル)を作成すること。

