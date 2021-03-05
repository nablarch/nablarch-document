AWSにおける分散トレーシング
=========================================

本章では、AWS上で分散トレーシングを行う方法について説明する。

AWSでは[AWS X-Ray](https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/aws-xray.html)というサービスが用意されており、アプリケーションにAWS X-Ray SDKを組み込むことで分散トレーシングが可能となります。
詳細な設定方法は[AWS X-Ray SDK for Java](https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java.html)を参照してください。

以下はアーキタイプから作成されたコンテナ用RESTfulウェブサービスプロジェクトに、分散トレーシングを設定する例です。

AWS X-Ray SDKを使用するため、[Submodules](https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java.html#xray-sdk-java-submodules)のうち必要なものを依存関係に追加します。
※上記SubmodulesではSQLクエリのトレースには`aws-xray-recorder-sdk-sql-postgres`または`aws-xray-recorder-sdk-sql-mysql`を使用するとなっていますが、本記事では任意のJDBCデータソースをトレース可能な[aws-xray-sdk-java](https://github.com/aws/aws-xray-sdk-java)に含まれる`aws-xray-recorder-sdk-sql`を使用します。

`pom.xml`に以下を追記します。

```xml
  <dependencyManagement>
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
```

依存を追加したら受信HTTPリクエストのトレースするためX-Ray サーブレットフィルタをアプリケーションに追加します。
`src/main/webapp/WEB-INF/web.xml`に以下を追記します。

```xml
  <filter>
    <filter-name>AWSXRayServletFilter</filter-name>
    <filter-class>com.amazonaws.xray.javax.servlet.AWSXRayServletFilter</filter-class>
    <init-param>
      <param-name>fixedName</param-name>
      <param-value>gateway</param-value>
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
```

続いて他のサービスへのHTTPリクエストをトレースするための設定を追加します。

X-Ray SDK for Javaには、送信HTTP呼び出しを計測するためのAPIとして[Apache HttpComponents](https://hc.apache.org/)のインタフェースで[使用できるクラス](https://docs.aws.amazon.com/ja_jp/xray/latest/devguide/xray-sdk-java-httpclients.html)が用意されています。
Apache HttpComponentsを直接使うと処理が煩雑になるため、今回はJAX-RSクライアントの実装である[Jersey](https://eclipse-ee4j.github.io/jersey/)経由で利用します。
Jerseyは、デフォルトでは`java.net.HttpURLConnection`をトランスポート層に利用します。JerseyクライアントにConnectorSPIを実装する`HttpUrlConnectorProvider`を登録することで[トランスポート層の置き換えが可能](https://eclipse-ee4j.github.io/jersey.github.io/documentation/latest/client.html#d0e4974)です。
Apache HttpComponentsを利用するため、`org.glassfish.jersey.apache.connector.ApacheConnectorProvider`を使用します。

まず依存にJerseyを加えます。

```xml
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
```

Jerseyには`org.glassfish.jersey.apache.connector.ApacheHttpClientBuilderConfigurator`インタフェースが用意されています。このインタフェースを使用することで、`HttpClientBuilder`に追加の設定をしたり、`HttpClientBuilder`そのものを差し替えたりといった処理が可能になります。
下記では`HttpClientBuilder`をAWS SDKの`com.amazonaws.xray.proxies.apache.http.HttpClientBuilder`に差し替えています。

```java
package com.example.system.httpclient;

import nablarch.core.repository.di.ComponentFactory;
import org.apache.http.impl.client.HttpClientBuilder;
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
```

`ComponentFactory`を`src/main/resources/rest-component-configuration.xml`に記述し、HTTPクライアントをシステムリポジトリに登録します。

```xml
  <!-- HTTPクライアントの設定 -->
  <component name="httpClient" class="com.example.system.httpclient.JerseyHttpClientWithAWSXRayFactory" />
```

以下はシステムリポジトリに登録したHTTPクライアントを利用するクラスの例です。
このクラスは`@SystemRepositoryComponent`のアノテーションを付与することで[DIコンテナの構築対象となり](https://nablarch.github.io/docs/LATEST/doc/application_framework/application_framework/libraries/repository.html#repository-inject-annotation-component)コンストラクタインジェクションでHTTPクライアントが登録されます。

```java
package com.example.recommendation.infrastracture;

import com.example.recommendation.domain.model.Product;
import com.example.recommendation.domain.model.ProductId;
import com.example.recommendation.domain.model.ProductImage;
import com.example.recommendation.domain.model.ProductName;
import com.example.recommendation.domain.model.ProductPrice;
import com.example.recommendation.domain.model.Products;
import com.example.recommendation.domain.repository.ProductRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import nablarch.core.repository.di.config.externalize.annotation.ComponentRef;
import nablarch.core.repository.di.config.externalize.annotation.ConfigValue;
import nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.GenericType;
import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@SystemRepositoryComponent
public class HttpProductRepository implements ProductRepository {

    private final Client httpClient;
    private final String productAPI;

    public HttpProductRepository(@ComponentRef("httpClient") Client httpClient,
                                 @ConfigValue("${api.product.url}") String productAPI) {
        this.httpClient = httpClient;
        this.productAPI = productAPI;
    }

    @Override
    public Products findAll() {
        WebTarget target = httpClient.target(productAPI).path("/products");
        List<ProductResponse> products = target.request().get(new GenericType<>() {});
        return new Products(products.stream().map(ProductResponse::toProduct).collect(Collectors.toList()));
    }

    public static class ProductResponse {
        public String id;
        public String name;
        public BigDecimal price;
        public String image;

        public Product toProduct() {
            return new Product(new ProductId(id), new ProductName(name), new ProductPrice(price), new ProductImage(image));
        }
    }
}
```

次にSQLクエリも計測対象とするための設定を加えます。

aws-xray-sdk-javaの[Intercept JDBC-Based SQL Queries](https://github.com/aws/aws-xray-sdk-java#intercept-jdbc-based-sql-queries)に記載のようにデータソースを`com.amazonaws.xray.sql.TracingDataSource`でデコレートすることでSQLクエリの計測が可能となります。
デコレートされたデータソースを作成する`TracingDataSourceFactory`を作成します。

```java
package com.example.system.awsxray;

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
```

アーキタイプから生成したプロジェクトではデータソースの設定が`src/main/resources/data-source.xml`に記述されています。これを以下のように編集します。
`dataSource`という名前で`com.zaxxer.hikari.HikariDataSource`が定義されているので、`rawDataSource`という名前に変更します。代わりに上記で作成した`TracingDataSourceFactory`を`dataSource`という名前で定義します。`TracingDataSourceFactory`には元になるデータソースをプロパティとして設定します。元になるデータソースには、`rawDataSource`を設定します。
Nablarchは`dataSource`という名前でデータソースコンポーネントを取得します。このように編集することでX-Ray SDK for Java JDBCインターセプターがデータソース設定に追加され、SQLクエリが計測されるようになります。

```xml
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
```

以上でAWS X-Rayでの分散トレーシング設定は完了です。
