.. _view_freemarker:

FreeMarkerを使用した画面開発
==================================================
`FreeMarker(外部サイト、英語) <https://freemarker.apache.org/>`_ を使用した画面開発について解説する。

FreeMarkerの導入手順は以下の通り。なお、詳細な手順については、 `FreeMarkerのドキュメント <https://freemarker.apache.org/docs/pgui_misc_servlet.html>`_ を参照。

1. :ref:`freemarker-pom`
2. :ref:`freemarker-servlet`
3. :ref:`freemarker-create_ftl`
4. :ref:`2重サブミットを防止する(必要な場合のみ) <freemarker-use_token>`

.. _freemarker-pom:

FreeMarkerを依存ライブラリに追加する
--------------------------------------------------
FreeMarkerをプロジェクトで使用可能にするために依存ライブラリに追加する。
Mavenを使用している場合は、POMに以下を追加する。
なお、本解説書は下のdependencyに記載のバージョンにて動作確認している。

.. code-block:: xml

  <dependency>
    <groupId>org.freemarker</groupId>
    <artifactId>freemarker-gae</artifactId>
    <version>2.3.27-incubating</version>
  </dependency>

.. _freemarker-servlet:

FreeMarkerServletの設定を行う
--------------------------------------------------
``web.xml`` に ``FreeMarkerServlet`` を登録し、 ``*.ftl`` に反応するようにする。

web.xmlの例
  .. code-block:: xml

    <servlet>
      <servlet-name>freemarker</servlet-name>
      <servlet-class>freemarker.ext.servlet.FreemarkerServlet</servlet-class>
    </servlet>

    <servlet-mapping>
      <servlet-name>freemarker</servlet-name>
      <url-pattern>*.ftl</url-pattern>

      <init-param>
        <!--
        テンプレートファイル(ftl)の配置ディレクトリを指定する。
        「/」を指定した場合は、warのルートディレクトリが配置ディレクトリとなる。
        -->
        <param-name>TemplatePath</param-name>
        <param-value>/</param-value>

        <!-- 上記以外については、ドキュメントを参照し必要なパラメータを設定すること -->
      </init-param>
    </servlet-mapping>

.. _freemarker-create_ftl:

テンプレートファイル(ftlファイル)を作成しActionを実装する
-------------------------------------------------------------------
テンプレートファイル(ftlファイル)を作成し配置する。(テンプレートの作成方法は、FreeMarkerのドキュメントを参照)
Actionクラスでは、レスポンスとしてテンプレートファイルへのパスを返却する。

例えば、 ``webapp/WEB-INF/template/index.ftl`` を使用してhtmlをクライアントに返したい場合は、Actionクラスは以下のようにレスポンスを返却する。
(webappはWARのルートとなるディレクトリ)

.. code-block:: java

  return new HttpResponse("/WEB-INF/template/index.ftl");

.. tip::

  FreeMarkerによって生成されたhtmlがクライアントに返却される仕組みは以下の通り。

  1. :ref:`http_response_handler` が ``/WEB-INF/template/index.ftl`` に対してServlet forwardを行う。
  2. 拡張子の ``ftl`` に反応し ``FreeMarkerServlet`` が実行され、テンプレートとリクエストスコープ等のデータを元にhtmlを生成する。
  3. 生成したhtmlをクライアントに返す。

.. _freemarker-use_token:

2重サブミットを防止する
--------------------------------------------------
2重サブミットを防止したい場合は、 :ref:`use_token_interceptor` を参照しAction及びテンプレートファイル(ftlファイル)を作成すること。

