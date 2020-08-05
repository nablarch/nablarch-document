.. _aws_xray_adaptor:

AWS X-Ray アダプタ
================================================================================================

.. contents:: 目次
  :depth: 1
  :local:

分散トレーシングを実現するため、 `AWS X-Ray(外部サイト) <https://docs.aws.amazon.com/ja_jp/xray/index.html>`_ を使用できるようにするアダプタを提供する。


.. _aws_xray_adaptor_module_list:

モジュール一覧
-----------------------------------------------------------------------------------------------

.. code-block:: xml

  <!-- AWS X-Ray アダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-aws-xray-adaptor</artifactId>
  </dependency>

.. _aws_xray_settings:

AWS X-Ray アダプタを使用するための設定を行う
-----------------------------------------------------------------------------------------------
本アダプタを使用するためには、コンポーネント設定ファイルでハンドラキューに
:java:extdoc:`AWSXRayServletFilterAdaptorHandler<nablarch.integration.amazonaws.xray.AWSXRayServletFilterAdaptorHandler>` を設定する必要がある。

上記ハンドラを設定することでX-Rayのセグメントが作成されトレースが可能となる。
``fixedSegmentName`` プロパティにはセグメントの名前として任意の値を設定する。
``fixedSegmentName`` または ``AWSXRayServletFilter`` のいずれかのプロパティを必ず設定する必要がある。

.. code-block:: xml

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
        <component class="nablarch.fw.handler.GlobalErrorHandler"/>
        <!-- AWS X-Ray サーブレットフィルターアダプタハンドラ -->
        <component class="nablarch.integration.amazonaws.xray.AWSXRayServletFilterAdaptorHandler">
          <property name="fixedSegmentName" value="example"/>
        </component>

.. tip::
  `ローカルで X-Ray デーモンを実行する(外部サイト) <https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-daemon-local.html>`_ ことで
  ローカルで実行したアプリケーションのトレースを行うことができる。

.. _aws_xray_setting_switch_enabled:

環境によってAWS X-Rayの有効無効を切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ローカルではAWS X-Rayを無効にし、本番環境では有効にしたい場合、以下の設定で実現できる。

コンポーネント定義
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ハンドラキューに ``AWSXRayServletFilterAdaptorHandler`` を直接定義するのではなく
:java:extdoc:`AWSXRayServletFilterAdaptorHandlerFactory<nablarch.integration.amazonaws.xray.AWSXRayServletFilterAdaptorHandlerFactory>`  を定義することで
X-Rayの設定によりトレース可否を切り替えることができる。

.. code-block:: xml

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
        <component class="nablarch.fw.handler.GlobalErrorHandler"/>
        <!-- X-Rayの設定によりハンドラを切り替えるファクトリ -->
        <component class="nablarch.integration.amazonaws.xray.AWSXRayServletFilterAdaptorHandlerFactory">
          <property name="fixedSegmentName" value="example"/>
          <property name="enabledXRay" value="${aws.xray.enabled}"/>
        </component>

上記のように :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` を実装した ``AWSXRayServletFilterAdaptorHandlerFactory`` をコンポーネントに定義し
``aws.xray.enabled`` の :ref:`設定値を環境ごとに変える <repository-environment_configuration>` ことでトレース可否を切り替えることができる。

``AWSXRayServletFilterAdaptorHandlerFactory`` は ``enabledXRay`` が ``true`` の場合、 ``fixedSegmentName`` に設定した名前でセグメントを作成する
``AWSXRayServletFilterAdaptorHandler`` を生成し、 ``enabledXRay`` が ``false`` の場合、何もしない :java:extdoc:`PassThroughHandler<nablarch.fw.web.handler.PassThroughHandler>` を生成する。

.. _aws_xray_http_client:

HTTP呼び出しの計測
-----------------------------------------------------------------------------------------------
アプリケーションがマイクロサービスまたはパブリックHTTP APIに呼び出しを実行する場合、 X-Ray SDK for Java の ``HttpClient`` を使用して呼び出しを計測することができる。
本アダプタでは、X-Rayの有効な環境ではX-Ray SDK for Java の ``HttpClient`` を、無効な環境ではApache.orgの ``HttpClient`` を生成する :java:extdoc:`AWSXRayHttpClientFactory<nablarch.integration.amazonaws.xray.AWSXRayHttpClientFactory>` を提供する。

コンポーネント定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システムリポジトリに上記ファクトリで生成される  ``HttpClient`` を登録しておき、HTTP呼び出しのクライアントとして使用することでトレースが可能となる。

.. code-block:: xml

  <component name="httpClient" class="nablarch.integration.amazonaws.xray.AWSXRayHttpClientFactory">
    <property name="enabledXRay" value="${aws.xray.enabled}"/>
  </component>

:ref:`ハンドラの設定<aws_xray_setting_switch_enabled>` 同様、 ``aws.xray.enabled`` の設定値を変えることでトレース可否を切り替えることができる。

HttpClientの設定を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``AWSXRayHttpClientFactory`` はデフォルトでは `com.amazonaws.xray.proxies.apache.http.HttpClientBuilder#create <https://docs.aws.amazon.com/xray-sdk-for-java/latest/javadoc/com/amazonaws/xray/proxies/apache/http/HttpClientBuilder.html#create-->`_ 
(X-Rayが無効な環境では `org.apache.http.impl.client.HttpClientBuilder#create <https://www.javadoc.io/static/org.apache.httpcomponents/httpclient/4.5.2/org/apache/http/impl/client/HttpClientBuilder.html#create()>`_ )メソッドで
生成される ``HttpClientBuilder`` から ``HttpClient`` を生成する。

``HttpClient`` に対して設定を追加したい場合は、　``AWSXRayHttpClientFactory`` の ``customizer`` フィールドに ``UnaryOperator<HttpClientBuilder>`` の実装クラスを設定する。

以下の例ではプロキシとユーザーエージェントを追加する場合の実装例を示す。

.. code-block:: java

    public class ExampleCustomizer implements UnaryOperator<HttpClientBuilder> {
        private String proxyHost;
        private int proxyPort;
        private String userAgent;

        @Override
        public HttpClientBuilder apply(HttpClientBuilder builder) {
            // HttpClientBuilderに追加で実行したい設定を実装する
            return builder
                    .setProxy(new HttpHost(proxyHost, proxyPort))
                    .setUserAgent(userAgent);
        }

        // setterは省略
    }

.. code-block:: xml

  <component name="customizer" class="nablarch.integration.amazonaws.xray.ExampleCustomizer">
    <property name="proxyHost" value="example.com"/>
    <property name="proxyPort" value="8080"/>
    <property name="userAgent" value="user-agent"/>
  </component>

  <component class="nablarch.integration.amazonaws.xray.AWSXRayHttpClientFactory">
    <property name="enabledXRay" value="${aws.xray.enabled}"/>
    <!-- customizerフィールドに設定された関数がHttpClientBuilder#build()前に実行される -->
    <property name="customizer" ref="customizer"/>
  </component>

.. _aws_xray_sql_datasource:

SQLクエリの計測
-----------------------------------------------------------------------------------------------
:java:extdoc:`TracingDataSourceFactory<nablarch.integration.amazonaws.xray.TracingDataSourceFactory>` を使用してデータソースを生成することで
SQLクエリの計測が可能となる。

コンポーネント定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`javax.sql.DataSource` を使った :ref:`データベース接続 <database-connect>` が使用できるよう
``dataSource`` という名前で ``TracingDataSourceFactory`` から生成したデータソースを登録する。
``TracingDataSourceFactory`` の ``dataSource`` には各アプリケーションで使用するデータソースを設定する。

以下では ``HikariDataSource`` を使用した ``TracingDataSourceFactory`` の設定例を示す。

.. code-block:: xml

  <import file="nablarch/core/db-base.xml"/>
 
  <!-- DataSourceを使った接続設定 -->
  <import file="nablarch/core/db/connection-factory-datasource.xml"/>

  <!-- 接続に使用するDataSourceを設定する -->
  <component name="rawDataSource" class="com.zaxxer.hikari.HikariDataSource" autowireType="None">
    <property name="driverClassName" value="${nablarch.db.jdbcDriver}"/>
    <property name="jdbcUrl" value="${nablarch.db.url}"/>
    <property name="username" value="${nablarch.db.user}"/>
    <property name="password" value="${nablarch.db.password}"/>
    <property name="maximumPoolSize" value="${nablarch.db.maxPoolSize}"/>
  </component>
 
  <!-- dataSourceという名前でコンポーネントを登録する -->
  <component name="dataSource" class="nablarch.integration.amazonaws.xray.TracingDataSourceFactory">
    <property name="enabledXRay" value="${aws.xray.enabled}"/>
    <!-- このフィールドに設定したDataSourceをラッピングしてトレース可能とする -->
    <property name="dataSource" ref="rawDataSource"/>
  </component>

:ref:`ハンドラの設定<aws_xray_setting_switch_enabled>` 同様、 ``aws.xray.enabled`` の設定値を変えることでトレース可否を切り替えることができる。
