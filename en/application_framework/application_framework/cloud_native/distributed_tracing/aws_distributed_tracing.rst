Distributed Tracing in AWS
=========================================

.. contents:: Table of contents
  :depth: 3
  :local:

AWS provides a service called `AWS X-Ray (external site)`_ to realize distributed tracing.
Distributed tracing of Java applications can be realized in the following two ways.

* AWS X-Ray SDK for Java
* AWS X-Ray Java auto-instrumentation agent for Java

You can use `auto-instrumentation agent (external site)`_ to measure without adding code to the application runtime, 
but Nablarch cannot use the agent due to the structure of the framework. 
Therefore, this procedure describes how to incorporate the AWS X-Ray SDK for Java into your application.
See `AWS X-Ray SDK for Java (external site)`_ for detailed configuration methods not mentioned below.

.. important::

  In October 2020, `AWS Distro for OpenTelemetry (external site)`_ was announced as the third method.
  However, although it is production-ready as of March 2021, it has not been officially released.
  Therefore, if AWS Distro for OpenTelemetry is released in the future and its operation is confirmed on Nablarch, this chapter may be replaced with the procedure using AWS Distro for OpenTelemetry.

The following is an example of using the archetype for containers.
:ref:`xray_configuration_incoming_request` setting is enough to trace the relationship between services.
:ref:`xray_configuration_outgoing_http_calls` and :ref:`xray_configuration_sql_queries` should be set according to your application requirements.

Dependency management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the required ones from the sub-modules of AWS X-Ray SDK to the dependencies.
See below for available submodules.

* `Submodules(external site)`_

Add the SDK as a dependency in your ``pom.xml`` file.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <!--  Omitted  -->
      <dependency>
        <groupId>com.amazonaws</groupId>
        <artifactId>aws-xray-recorder-sdk-bom</artifactId>
        <version>2.15.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <!--  Omitted  -->
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

  The `AWS X-Ray SDK for Java (external site)`_ states that you should use ``aws-xray-recorder-sdk-sql-postgres`` or 
  ``aws-xray-recorder-sdk-sql-mysql`` for tracing SQL queries.
  This procedure uses ``aws-xray-recorder-sdk-sql`` included in `aws-xray-sdk-java(external site)`_ which can trace any JDBC data source.

.. _xray_configuration_incoming_request:

Incoming requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Tracing incoming requests with the X-Ray SDK for Java(external site)`_

Add an X-Ray servlet filter to your application to trace incoming HTTP requests.
Add the following to ``src/main/webapp/WEB-INF/web.xml``.

.. code-block:: xml

  <filter>
    <filter-name>AWSXRayServletFilter</filter-name>
    <filter-class>com.amazonaws.xray.jakarta.servlet.AWSXRayServletFilter</filter-class>
    <init-param>
      <param-name>fixedName</param-name>
      <!-- Specify a name to identify the application in the service map -->
      <param-value>example-app</param-value>
    </init-param>
  </filter>

  <filter-mapping>
    <filter-name>AWSXRayServletFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <!-- Put it above the existing filter-mapping. -->
  <filter-mapping>
    <filter-name>entryPoint</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>

.. _xray_configuration_outgoing_http_calls:

Outgoing HTTP calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Tracing calls to downstream HTTP web services with the X-Ray SDK for Java(external site)`_

Add a setting to trace HTTP requests to other services.

X-Ray SDK for Java provides a class that can be used in the interface of `Apache HttpComponents(external site)`_ as an API for measuring outgoing HTTP calls.

Since using Apache HttpComponents directly is complicated, this procedure uses it via `Jersey(external site)`_, which is an implementation of Jakarta RESTful Web Services client.
Jersey uses ``java.net.HttpURLConnection`` for HTTP communication by default, so it needs to be configured to use Apache HttpComponents.
Jersey provides the interface ``org.glassfish.jersey.client.spi.ConnectorProvider``. 
By registering your own ``ConnectorProvider`` implementation to the Jersey client, HTTP communication can be performed by a method other than ``java.net.HttpURLConnection``.

* `Client Transport Connectors(external site)`_

``org.glassfish.jersey.apache.connector.ApacheConnectorProvider`` is provided as an implementation of ``org.glassfish.jersey.client.spi.ConnectorProvider``
for using Apache HttpComponents.

First, add Jersey to the dependency.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <!--  Omitted  -->
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>3.1.1</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <!--  Omitted  -->
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

Jersey provides the ``org.glassfish.jersey.apache.connector.ApacheHttpClientBuilderConfigurator`` interface.
Using this interface, it is possible to configure additional settings in the ``HttpClientBuilder`` or replace the ``HttpClientBuilder`` itself.
In the following, we replace the ``HttpClientBuilder`` with the AWS SDK ``com.amazonaws.xray.proxies.apache.http.HttpClientBuilder``.

.. code-block:: java

  package com.example;

  import com.amazonaws.xray.proxies.apache.http.HttpClientBuilder;
  import nablarch.core.repository.di.ComponentFactory;
  import org.glassfish.jersey.apache.connector.ApacheConnectorProvider;
  import org.glassfish.jersey.apache.connector.ApacheHttpClientBuilderConfigurator;
  import org.glassfish.jersey.client.ClientConfig;

  import jakarta.ws.rs.client.Client;
  import jakarta.ws.rs.client.ClientBuilder;
  import jakarta.ws.rs.core.Configuration;

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

Describe the ``ComponentFactory`` in ``src/main/resources/rest-component-configuration.xml`` and register the HTTP client in the system repository.

.. code-block:: xml

  <component name="httpClient" class="com.example.system.httpclient.JerseyHttpClientWithAWSXRayFactory" />

An example of a class that uses an HTTP client registered in the system repository is shown below.
By annotating this class with ``@SystemRepositoryComponent``, it becomes a target of the DI container construction, and the HTTP client is registered by constructor injection.

.. code-block:: java

  package com.example;

  import nablarch.core.repository.di.config.externalize.annotation.ComponentRef;
  import nablarch.core.repository.di.config.externalize.annotation.ConfigValue;
  import nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent;
  import jakarta.ws.rs.client.Client;

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

It is also possible to obtain and use HTTP clients directly from the system repository.

.. code-block:: java

  Client httpClient = SystemRepository.get("httpclient");
  WebTarget target = httpClient.target(productAPI).path("/products");
  ProductResponse products = target.request().get(ProductResponse.class);


.. _xray_configuration_sql_queries:

SQL queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Tracing SQL queries with the X-Ray SDK for Java(external site)`_

Add settings to measure SQL queries.

You can instrument SQL queries by decorating the data source with ``com.amazonaws.xray.sql.TracingDataSource``, as described below.

* `Intercept JDBC-Based SQL Queries(external site)`_

Implement a factory class that creates a decorated data source.

.. code-block:: java

  package com.example;

  import com.amazonaws.xray.sql.TracingDataSource;
  import nablarch.core.log.Logger;
  import nablarch.core.log.LoggerManager;
  import nablarch.core.repository.di.ComponentFactory;

  import javax.sql.DataSource;

  public class TracingDataSourceFactory implements ComponentFactory<DataSource> {
      private static final Logger LOGGER = LoggerManager.get(TracingDataSourceFactory.class);
      private DataSource dataSource;

      @Override
      public DataSource createObject() {
          LOGGER.logInfo("Wrap " + dataSource + " in " + TracingDataSource.class.getName());
          return TracingDataSource.decorate(dataSource);
      }

      /**
      * Set the data source.
      *
      * @param dataSource the dataSource to trace
      */
      public void setDataSource(DataSource dataSource) {
          this.dataSource = dataSource;
      }
  }

In the project generated from the archetype, the data source settings are described in ``src/main/resources/data-source.xml``.
Edit it as follows.

* Since ``com.zaxxer.hikari.HikariDataSource`` is defined as ``dataSource``, rename it to ``rawDataSource``.
* Instead, define the ``TracingDataSourceFactory`` created above with the name ``dataSource``.
* The ``TracingDataSourceFactory`` needs to be set with the original data source as a property. Set ``rawDataSource`` as the original data source.

Nablarch will get a data source component named ``dataSource``.
By editing it like this, X-Ray SDK for Java JDBC interceptor will be added to the data source configuration and SQL queries will be instrumented.

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

.. _AWS X-Ray (external site): https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html
.. _auto-instrumentation agent (external site): https://docs.aws.amazon.com/xray/latest/devguide/aws-x-ray-auto-instrumentation-agent-for-java.html
.. _AWS X-Ray SDK for Java (external site): https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java.html
.. _AWS Distro for OpenTelemetry (external site): https://aws.amazon.com/jp/otel/?otel-blogs.sort-by=item.additionalFields.createdDate&otel-blogs.sort-order=desc
.. _Submodules(external site): https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java.html#xray-sdk-java-submodules
.. _aws-xray-sdk-java(external site): https://github.com/aws/aws-xray-sdk-java
.. _Tracing incoming requests with the X-Ray SDK for Java(external site): https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java-filters.html
.. _Tracing calls to downstream HTTP web services with the X-Ray SDK for Java(external site): https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java-httpclients.html
.. _Apache HttpComponents(external site): https://hc.apache.org/
.. _Jersey(external site): https://eclipse-ee4j.github.io/jersey/
.. _Client Transport Connectors(external site): https://eclipse-ee4j.github.io/jersey.github.io/documentation/latest/client.html#d0e5043
.. _Tracing SQL queries with the X-Ray SDK for Java(external site): https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java-sqlclients.html
.. _Intercept JDBC-Based SQL Queries(external site): https://github.com/aws/aws-xray-sdk-java#intercept-jdbc-based-sql-queries