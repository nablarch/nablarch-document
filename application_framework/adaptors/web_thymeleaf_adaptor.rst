.. _web_thymeleaf_adaptor:

ウェブアプリケーション Thymeleafアダプタ
========================================

.. contents:: 目次
  :depth: 3
  :local:

ウェブアプリケーションで、テンプレートエンジンに `Thymeleaf(外部サイト) <http://www.thymeleaf.org>`_
を使用するためのアダプタを提供する。

モジュール一覧
--------------

.. code-block:: xml

  <!-- ウェブアプリケーション Thymeleafアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-web-thymeleaf-adaptor</artifactId>
  </dependency>
  
.. tip::

  Thymeleafのバージョン3.0.9.RELEASEを使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。


ウェブアプリケーション Thymeleafアダプタを使用するための設定を行う
------------------------------------------------------------------


本アダプタを使用するためには、コンポーネント設定ファイルで
:java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` を\
:java:extdoc:`HttpResponseHandler<nablarch.fw.web.handler.HttpResponseHandler>` へ設定する。

``ThymeleafResponseWriter`` にはThymeleafが提供する ``TemplateEngine`` を設定する必要がある。

コンポーネント設定ファイルの設定例を以下に示す。

.. code-block:: xml

  <component name="templateEngine" class="org.thymeleaf.TemplateEngine" autowireType="None">
    <property name="templateResolver">
      <component class="org.thymeleaf.templateresolver.ClassLoaderTemplateResolver">
        <property name="prefix" value="/template/"/>
      </component>
    </property>
  </component>

  <component name="thymeleafResponseWriter"
             class="nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter"
             autowireType="None">
    <property name="templateEngine" ref="templateEngine" />
  </component>

  <component name="httpResponseHandler"
             class="nablarch.fw.web.handler.HttpResponseHandler">
    <property name="customResponseWriter" ref="thymeleafResponseWriter"/>
    <!-- その他の設定は省略 -->
  </component>


.. tip::

  ``ITemplateResolver`` インタフェースの実装クラスに、
  ``org.thymeleaf.templateresolver.ServletContextTemplateResolver`` が存在するが、
  このクラスは、コンストラクタ引数に ``javax.servlet.ServletContext`` が必須であるため、
  :ref:`repository` にコンポーネントとして登録できない。

  本クラスではなく、 ``ClassLoaderTemplateResolver`` 等の別の実装クラスを使用すること。
  

処理対象判定について
~~~~~~~~~~~~~~~~~~~~
  
:java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` は\
:java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` のコンテンツパスの内容によって、
テンプレートエンジンを使用してレスポンス出力を行うか否かを判断する。
デフォルトではコンテンツパスが ``.html`` で終了している場合、処理対象と判定しテンプレートエンジンによる出力を行う。

例えば、アクションクラスで以下のように ``HttpResponse`` を返却したとする。

.. code-block:: java

  return new HttpResponse("/template/index.html");

この場合、コンテンツパス(\ ``/template/index.html``\ )は ``.html`` で終了しているため、
テンプレートエンジンの出力対象と判定される。


処理対象と判定されなかった場合は、テンプレートエンジンによる出力は行われず、\
サーブレットフォワードが実行される。
例えば、以下の例では、コンテンツパスが ``.html`` で終了していないため、サーブレットフォワードが実行される。

.. code-block:: java

  return new HttpResponse("/path/to/anotherServlet");

  
この処理対象判定条件は設定変更が可能である。プロパティ\ ``pathPattern`` に、\
判定に使用する正規表現が設定できる(デフォルト値は ``.*\.html`` )。\
この正規表現にコンテンツパスがマッチした場合、テンプレートエンジンの処理対象と判定される。


.. important::

  Thymeleafでは、テンプレートのパスを解決する際、サフィックスを省略する設定ができるが、
  本クラスを使用する場合はサフィックスの省略は行わないこと。
  
  * OK: ``return new HttpResponse("/template/index.html");``
  * NG: ``return new HttpResponse("/template/index");``
  
  サフィックスを省略した場合、セッションストアからリクエストスコープへの移送が行われなくなる。   


テンプレートを作成する
----------------------

テンプレートファイルを配置する場所は ``TemplateEngine`` の設定によって異なる。
例えば、前節で示した設定例だとテンプレートファイルはクラスパスからロードされる。
また、 ``ClassLoaderTemplateResolver`` のプロパティ ``prefix`` に ``/template/`` と設定されているので、
クラスパス上の ``/template/`` ディレクトリにテンプレートファイルを配置することになる。


テンプレートエンジンを使用する
------------------------------

アクションクラスで、テンプレートへのパスを指定した ``HttpResponse`` を返却する。

.. code-block:: java

  return new HttpResponse("/template/index.html");
