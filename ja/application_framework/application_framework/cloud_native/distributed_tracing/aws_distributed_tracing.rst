AWSにおける分散トレーシング
=========================================

.. contents:: 目次
  :depth: 3
  :local:

AWSでは `AWS X-Ray(外部サイト)`_ という分散トレーシングを実現するためのサービスが用意されている。
Javaアプリケーションの分散トレーシングは以下2つの方法で実現できる。

* AWS X-Ray SDK for Java
* AWS X-Ray Java 用 自動計測エージェント

`自動計測エージェント(外部サイト)`_ を使用するとアプリケーションのランタイムにコードを追加することなく計測が可能だが、
Nablarchはフレームワークの構造上、自動計測エージェントが使用できない。そのため本手順ではAWS X-Ray SDK for Javaをアプリケーションに組み込む方法について説明する。
以下で触れない詳細な設定方法については `AWS X-Ray SDK for Java(外部サイト)`_ を参照。

.. important::

  2020年10月に第3の方法として `AWS Distro for OpenTelemetry(外部サイト、英語)`_ が発表された。
  しかし、2021年3月現在production-readyとなっているが、正式リリースはされていない。
  そのため今後 AWS Distro for OpenTelemetry がリリースされ、Nablarchでの動作確認がとれた場合は、本章は AWS Distro for OpenTelemetry を使用した手順に差し替える可能性がある。

以下にコンテナ用アーキタイプを使用した場合の例を示す。
:ref:`xray_configuration_incoming_request` の設定だけでサービス間の関連はトレースできる。
:ref:`xray_configuration_outgoing_http_calls` と :ref:`xray_configuration_sql_queries` はアプリケーションの要件に応じて設定する必要がある。

依存関係の追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS X-Ray SDKのサブモジュールから必要なものを依存関係に追加する。
使用できるサブモジュールは以下参照。

* `Submodules(外部サイト)`_

``pom.xml`` に以下を追記する。

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <!--  中略  -->
      <dependency>
        <groupId>com.amazonaws</groupId>
        <artifactId>aws-xray-recorder-sdk-bom</artifactId>
        <version>2.4.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <!--  中略  -->
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-xray-recorder-sdk-core</artifactId>
    </dependency>
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-xray-recorder-sdk-apache-http</artifactId>
    </dependency>
    <dependency>
      <groupId>com.amazonaws</groupId>
      <artifactId>aws-xray-recorder-sdk-sql</artifactId>
    </dependency>
  </dependencies>

.. tip::

  `AWS X-Ray SDK for Java(外部サイト)`_ ではSQLクエリのトレースには
  ``aws-xray-recorder-sdk-sql-postgres`` または ``aws-xray-recorder-sdk-sql-mysql`` を使用すると記載されている。
  本手順では任意のJDBCデータソースをトレース可能な `aws-xray-sdk-java(外部サイト、英語)`_ に含まれる ``aws-xray-recorder-sdk-sql`` を使用する。

.. _xray_configuration_incoming_request:

受信HTTPリクエスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `X-Ray SDK for Java を使用して受信リクエストをトレースする(外部サイト)`_

受信HTTPリクエストをトレースするためX-Ray サーブレットフィルタをアプリケーションに追加する。
``src/main/webapp/WEB-INF/web.xml`` に以下を追記。

.. code-block:: xml

  <filter>
    <filter-name>AWSXRayServletFilter</filter-name>
    <filter-class>com.amazonaws.xray.javax.servlet.AWSXRayServletFilter</filter-class>
    <init-param>
      <param-name>fixedName</param-name>
      <!-- サービスマップでアプリケーションを識別する名前を指定する -->
      <param-value>example-app</param-value>
    </init-param>
  </filter>

  <filter-mapping>
    <filter-name>AWSXRayServletFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <!-- ↑既存のfilter-mappingより上に記載する -->
  <filter-mapping>
    <filter-name>entryPoint</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>

.. _xray_configuration_outgoing_http_calls:

送信HTTP呼び出し
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `X-Ray SDK for Java を使用してダウンストリーム HTTP ウェブサービスの呼び出しをトレースする(外部サイト)`_

他のサービスへのHTTPリクエストをトレースするための設定を追加する。

X-Ray SDK for Javaには、送信HTTP呼び出しを計測するためのAPIとして `Apache HttpComponents(外部サイト、英語)`_ のインタフェースで使用できるクラスが用意されている。

Apache HttpComponentsを直接使うと処理が煩雑になるため、本手順ではJAX-RSクライアントの実装である `Jersey(外部サイト、英語)`_ 経由で使用する。
Jerseyは、デフォルトではHTTP通信に ``java.net.HttpURLConnection`` を使用するため、Apache HttpComponentsを利用するためには設定が必要となる。
``org.glassfish.jersey.client.spi.ConnectorProvider`` というインタフェースが用意されているので、
その実装クラスをJerseyクライアントに登録することで ``java.net.HttpURLConnection`` 以外の方法でHTTP通信が可能となる。

* `Client Transport Connectors(外部サイト、英語)`_

Apache HttpComponentsを使用するための ``org.glassfish.jersey.client.spi.ConnectorProvider`` の実装として 
``org.glassfish.jersey.apache.connector.ApacheConnectorProvider`` が用意されている。

まず依存にJerseyを加える。

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <!--  中略  -->
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>2.32</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <!--  中略  -->
    <!-- Jerseyクライアント -->
    <dependency>
      <groupId>org.glassfish.jersey.core</groupId>
      <artifactId>jersey-client</artifactId>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.connectors</groupId>
      <artifactId>jersey-apache-connector</artifactId>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.media</groupId>
      <artifactId>jersey-media-json-jackson</artifactId>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.inject</groupId>
      <artifactId>jersey-hk2</artifactId>
    </dependency>
  </dependencies>

Jerseyには ``org.glassfish.jersey.apache.connector.ApacheHttpClientBuilderConfigurator`` インタフェースが用意されている。
このインタフェースを使用することで、 ``HttpClientBuilder`` への追加設定や、 ``HttpClientBuilder`` そのものを差し替えるといった処理が可能となる。
下記では ``HttpClientBuilder`` をAWS SDKの ``com.amazonaws.xray.proxies.apache.http.HttpClientBuilder`` に差し替えている。

.. code-block:: java

  package com.example;

  import com.amazonaws.xray.proxies.apache.http.HttpClientBuilder;
  import nablarch.core.repository.di.ComponentFactory;
  import org.glassfish.jersey.apache.connector.ApacheConnectorProvider;
  import org.glassfish.jersey.apache.connector.ApacheHttpClientBuilderConfigurator;
  import org.glassfish.jersey.client.ClientConfig;

  import javax.ws.rs.client.Client;
  import javax.ws.rs.client.ClientBuilder;
  import javax.ws.rs.core.Configuration;
  import java.util.function.UnaryOperator;

  public class JerseyHttpClientWithAWSXRayFactory implements ComponentFactory<Client> {
      @Override
      public Client createObject() {
          ApacheHttpClientBuilderConfigurator clientBuilderConfigurator 
                  = (httpClientBuilder) -> HttpClientBuilder.create();

          Configuration config = new ClientConfig()
                  .register(clientBuilderConfigurator)
                  .connectorProvider(new ApacheConnectorProvider());
          return ClientBuilder.newClient(config);
      }
  }

``ComponentFactory`` を ``src/main/resources/rest-component-configuration.xml`` に記述し、HTTPクライアントをシステムリポジトリに登録する。

.. code-block:: xml

  <!-- HTTPクライアントの設定 -->
  <component name="httpClient" class="com.example.system.httpclient.JerseyHttpClientWithAWSXRayFactory" />

システムリポジトリに登録したHTTPクライアントを使用するクラスの例を以下に示す。
このクラスは ``@SystemRepositoryComponent`` のアノテーションを付与することでDIコンテナの構築対象となり、コンストラクタインジェクションでHTTPクライアントが登録される。

.. code-block:: java

  package com.example;

  import nablarch.core.repository.di.config.externalize.annotation.ComponentRef;
  import nablarch.core.repository.di.config.externalize.annotation.ConfigValue;
  import nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent;
  import javax.ws.rs.client.Client;

  @SystemRepositoryComponent
  public class HttpProductRepository {

      private final Client httpClient;
      private final String productAPI;

      public HttpProductRepository(@ComponentRef("httpClient") Client httpClient,
                                  @ConfigValue("${api.product.url}") String productAPI) {
          this.httpClient = httpClient;
          this.productAPI = productAPI;
      }

      public ProductList findAll() {
          WebTarget target = httpClient.target(productAPI).path("/products");
          return target.request().get(ProductList.class);
      }

      //以下省略
  }

また、システムリポジトリから直接HTTPクライアントを取得して使用することも可能。

.. code-block:: java

  Client httpClient = SystemRepository.get("httpclient");
  WebTarget target = httpClient.target(productAPI).path("/products");
  ProductResponse products = target.request().get(ProductResponse.class);


.. _xray_configuration_sql_queries:

SQLクエリ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `X-Ray SDK for Java を使用して、SQL クエリをトレースする(外部サイト)`_

SQLクエリを計測対象とするための設定を加える。

以下に記載のように、データソースを ``com.amazonaws.xray.sql.TracingDataSource`` でデコレートすることでSQLクエリの計測が可能となる。

* `Intercept JDBC-Based SQL Queries(外部サイト、英語)`_

デコレートされたデータソースを作成するファクトリクラスを作成する。

.. code-block:: java

  package com.example;

  import com.amazonaws.xray.sql.TracingDataSource;
  import nablarch.core.log.Logger;
  import nablarch.core.log.LoggerManager;
  import nablarch.core.repository.di.ComponentFactory;

  import javax.sql.DataSource;

  public class TracingDataSourceFactory implements ComponentFactory<DataSource> {
      /** ロガー */
      private static final Logger LOGGER = LoggerManager.get(TracingDataSourceFactory.class);
      /** データソース */
      private DataSource dataSource;

      @Override
      public DataSource createObject() {
          LOGGER.logInfo("Wrap " + dataSource + " in " + TracingDataSource.class.getName());
          return TracingDataSource.decorate(dataSource);
      }

      /**
      * データソースを設定する。
      *
      * @param dataSource データソース
      */
      public void setDataSource(DataSource dataSource) {
          this.dataSource = dataSource;
      }
  }

アーキタイプから生成したプロジェクトではデータソースの設定が ``src/main/resources/data-source.xml`` に記述されている。
これを以下のように編集する。

* ``dataSource`` という名前で ``com.zaxxer.hikari.HikariDataSource`` が定義されているので、 ``rawDataSource`` という名前に変更する。
* 代わりに上記で作成した ``TracingDataSourceFactory`` を ``dataSource`` という名前で定義する。
* ``TracingDataSourceFactory`` には元になるデータソースをプロパティとして設定する必要がある。元になるデータソースには、 ``rawDataSource`` を設定する。

Nablarchは ``dataSource`` という名前でデータソースコンポーネントを取得する。
このように編集することでX-Ray SDK for Java JDBCインターセプタがデータソース設定に追加され、SQLクエリが計測されるようになる。

.. code-block:: xml

  <component name="rawDataSource"
             class="com.zaxxer.hikari.HikariDataSource" autowireType="None">
    <property name="driverClassName" value="${nablarch.db.jdbcDriver}"/>
    <property name="jdbcUrl" value="${nablarch.db.url}"/>
    <property name="username" value="${nablarch.db.user}"/>
    <property name="password" value="${nablarch.db.password}"/>
    <property name="maximumPoolSize" value="${nablarch.db.maxPoolSize}"/>
    <property name="minimumIdle" value="${nablarch.db.minimumIdle}"/>
    <property name="connectionTimeout" value="${nablarch.db.connectionTimeout}"/>
    <property name="idleTimeout" value="${nablarch.db.idleTimeout}"/>
    <property name="maxLifetime" value="${nablarch.db.maxLifetime}"/>
    <property name="validationTimeout" value="${nablarch.db.validationTimeout}"/>
  </component>
  <component name="dataSource" class="com.example.system.awsxray.TracingDataSourceFactory">
    <property name="dataSource" ref="rawDataSource" />
  </component>

.. _AWS X-Ray(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/aws-xray.html
.. _自動計測エージェント(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/aws-x-ray-auto-instrumentation-agent-for-java.html
.. _AWS X-Ray SDK for Java(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java.html
.. _AWS Distro for OpenTelemetry(外部サイト、英語): https://aws.amazon.com/jp/otel/?otel-blogs.sort-by=item.additionalFields.createdDate&otel-blogs.sort-order=desc
.. _Submodules(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java.html#xray-sdk-java-submodules
.. _aws-xray-sdk-java(外部サイト、英語): https://github.com/aws/aws-xray-sdk-java
.. _X-Ray SDK for Java を使用して受信リクエストをトレースする(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java-filters.html
.. _X-Ray SDK for Java を使用してダウンストリーム HTTP ウェブサービスの呼び出しをトレースする(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java-httpclients.html
.. _Apache HttpComponents(外部サイト、英語): https://hc.apache.org/
.. _Jersey(外部サイト、英語): https://eclipse-ee4j.github.io/jersey/
.. _Client Transport Connectors(外部サイト、英語): https://eclipse-ee4j.github.io/jersey.github.io/documentation/latest/client.html#d0e5082
.. _X-Ray SDK for Java を使用して、SQL クエリをトレースする(外部サイト): https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java-sqlclients.html
.. _Intercept JDBC-Based SQL Queries(外部サイト、英語): https://github.com/aws/aws-xray-sdk-java#intercept-jdbc-based-sql-queries