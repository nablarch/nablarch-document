=========================================================================
Nablarch 5 to 6 Migration Guide
=========================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

This document will explain how to upgrade a project created with Nablarch 5 to Nablarch 6.

Differences between Nablarch 5 and 6
=========================================================================

One of the major differences between Nablarch 6 and Nablarch 5 is that it supports Jakarta EE 10.

Jakarta EE is the name after Java EE was transferred to the Eclipse Foundation and is the successor to Java EE.
Basically, the Java EE specifications have been transferred as they are, but with Jakarta EE 9, there has been a major change in that the namespace has changed from ``javax.*`` to ``jakarta.*``.

Therefore, in order to upgrade a project created with Nablarch 5 to Nablarch 6, it is necessary to do the same for the project.

Prerequisites
=========================================================================

The instructions here assume that you have already upgraded to the latest version of Nablarch 5.

For projects created with an older version, first upgrade to the latest version of Nablarch 5, then upgrade to Nablarch 6.
See `the release notes <https://nablarch.github.io/docs/LATEST/doc/releases/index.html>`_ for details on the modifications required to upgrade to the latest version of Nablarch 5.

Also, Nablarch 6 modules are compiled with Java 17, so they require Java 17 or higher to run.


Overview of migration steps
=========================================================================

To get a Nablarch 5 project up to Nablarch 6, roughly two modifications are required:

* Nablarch version upgrade
* Compatible with Jakarta EE

The first "Nablarch version upgrade" refers to changing the version of Nablarch used in the project from 5 to 6.

The second, "Compatible with Jakarta EE", refers to making the project compatible with Jakarta EE 10.
This includes changes to namespaces introduced in Jakarta EE 9, and changes libraries that depend on Java EE to Jakarta EE-compatible versions.

Each specific procedure will be described below.


Details of migration steps
=========================================================================

In this section will explain in detail each of the migration steps required when upgrading a Nablarch 5 project to Nablarch 6.

In order to make it easier to imagine the specific modifications, here we will use the case of upgrading Nablarch 5's `nablarch-example-web (external site) <https://github.com/nablarch/nablarch-example-web>`_ to Nablarch 6 as an example.
Depending on the project, unnecessary steps may be included, but in that case, select and read as appropriate (for example, :ref:`waitt-to-jetty` and :ref:`update-ntf-jetty` are steps specific to web projects, so there is no problem in skipping them in batch projects).

.. tip::
    The 5 series code of nablarch-example-web can be obtained by switching to the ``5uXX`` tag.
    A list of tags can be found at `here (external site) <https://github.com/nablarch/nablarch-example-web/tags>`_.

--------------------------------------------------------------------
Nablarch version upgrade
--------------------------------------------------------------------

The version of each module that makes up Nablarch is managed by bom, so you can upgrade Nablarch by changing the version of bom.
Change ``<version>`` to 6 in ``pom.xml`` where Nablarch's bom is loaded, as shown below.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.nablarch.profile</groupId>
        <artifactId>nablarch-bom</artifactId>
        <version>6</version> <!-- set bom version to 6-->
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      ...
    </dependencies>
  </dependencyManagement>

--------------------------------------------------------------------
Compatible with Jakarta EE
--------------------------------------------------------------------


Change Java EE dependency to Jakarta EE
-----------------------------------------------------------------

Java EE API dependencies (``dependency``) must be changed to those of Jakarta EE.
For example, a typical example is Java Servlet.

In ``pom.xml`` of nablarch-example-web, the following are Java EE API dependencies.

.. code-block:: xml

  <!-- Java API for RESTful Web Services (JAX-RS) -->
  <dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>2.0</version>
  </dependency>

  <!-- Java Servlet -->
  <dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>3.1.0</version>
    <scope>provided</scope>
  </dependency>

  <!-- JavaServer Pages (JSP) -->
  <dependency>
    <groupId>javax.servlet.jsp</groupId>
    <artifactId>javax.servlet.jsp-api</artifactId>
    <version>2.3.1</version>
    <scope>provided</scope>
  </dependency>

  <!-- JavaServer Pages Standard Tag Library (JSTL) -->
  <dependency>
    <groupId>javax.servlet.jsp.jstl</groupId>
    <artifactId>javax.servlet.jsp.jstl-api</artifactId>
    <version>1.2.1</version>
  </dependency>

  <!-- Java Persistence API (JPA) -->
  <dependency>
    <groupId>org.apache.geronimo.specs</groupId>
    <artifactId>geronimo-jpa_2.0_spec</artifactId>
  </dependency>

Replacing this with the one provided by Jakarta EE gives the following:

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>jakarta.platform</groupId>
        <artifactId>jakarta.jakartaee-bom</artifactId>
        <version>10.0.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <!-- Jakarta RESTful Web Services -->
  <dependency>
    <groupId>jakarta.ws.rs</groupId>
    <artifactId>jakarta.ws.rs-api</artifactId>
  </dependency>

  <!-- Jakarta Servlet -->
  <dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <scope>provided</scope>
  </dependency>

  <!-- Jakarta Server Pages -->
  <dependency>
    <groupId>jakarta.servlet.jsp</groupId>
    <artifactId>jakarta.servlet.jsp-api</artifactId>
    <scope>provided</scope>
  </dependency>

  <!-- Jakarta Standard Tag Library -->
  <dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
  </dependency>

  <!-- Jakarta Persistence -->
  <dependency>
    <groupId>jakarta.persistence</groupId>
    <artifactId>jakarta.persistence-api</artifactId>
  </dependency>

Bom is prepared for Jakarta EE API, so reading this eliminates the need to specify the version for each API.
It is recommended to read bom because it reduces the trouble of checking the version and mistakes in specification, and makes management easier.

The ``dependency`` of Java EE API is different and not unified depending on the jar provider and version.
Therefore, it cannot be determined mechanically from ``groupId``.
Which ``dependency`` is a Java EE API must be determined from ``groupId``, ``artifactId``, classes included in the jar, and so on.

For reference, :ref:`java_ee_jakarta_ee_comparation` is included in the appendix at the end of this page.
What is ``dependency`` in Jakarta EE is described on each specification page, so please check it (for example, `Jakarta Servlet 6.0 specification page (external site) <https: //jakarta.ee/specifications/servlet/6.0/#details>`_ shows ``jakarta.servlet:jakarta.servlet-api:jar:6.0.0`` in "Maven coordinates").


Update runtimes related to the Java EE
-----------------------------------------------------------------

If you have embedded runtimes from the Java EE specification in your application, replace them with those from Jakarta EE.
For example, nablarch-example-web includes Hibernate Validator, a runtime for Bean Validation.

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>5.3.6.Final</version>
  </dependency>

If this is changed to ``dependency`` of Jakarta EE version, it will be as follows.

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>8.0.0.Final</version>
  </dependency>

To find out which ``dependency`` is the Java EE runtime, you need to investigate each ``dependency`` individually.
Also, if it is found to be a Java EE runtime, what the ``dependency`` of the Jakarta EE compliant version of that runtime will be depends on the runtime.
Therefore, it is necessary to check the official site etc. for each runtime used in the project.

For reference, the ``dependencies`` of typical runtimes Java EE and Jakarta EE are listed in :ref:`jakarta_ee_runtime_dependency` in the appendix of this page.
For runtimes of other specifications, compatible implementations are introduced on each Jakarta EE specification page, so please refer to that as well.
(For example, the `Jakarta RESTful Web Services 3.1 specification page (external site) <https://jakarta.ee/specifications/restful-ws/3.1/#compatible-implementations>`_ lists Eclipse Jersey as a compatible implementation. 3.1.0 is introduced)

Update gsp-dba-maven-plugin
-----------------------------------------------------------------

`gsp-dba-maven-plugin (external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_ is preinstalled in nablarch-example-web and other Nablarch projects built from archetypes. 
This plugin provides a function (``generate-entity``) to generate Java entity classes from database table metadata.
Since Java EE annotations such as JPA are set in this entity class, it cannot be used as is in the Jakarta EE environment.

Since gsp-dba-maven-plugin has Jakarta EE support in 5.0.0, modify ``pom.xml`` as follows.

.. code-block:: xml

    <plugin>
      <groupId>jp.co.tis.gsp</groupId>
      <artifactId>gsp-dba-maven-plugin</artifactId>
      <version>5.0.0</version> <!-- Change gsp-dba-maven-plugin version to Jakarta EE compatible version -->
      <configuration>
      ...

Furthermore, in order to use the ``generate-entity`` of the gsp-dba-maven-plugin that supports Jakarta EE, it is necessary to add ``dependency`` and JVM arguments.
See the `gsp-dba-maven-plugin guide (external site) <https://github.com/coastland/gsp-dba-maven-plugin#generate-entity>`_ for details.

As described above, an entity for which Jakarta EE annotations are set will be generated.

.. _waitt-to-jetty:

Change waitt-maven-plugin to jetty-ee10-maven-plugin
-----------------------------------------------------------------

The `waitt-maven-plugin (external site) <https://github.com/kawasima/waitt>`_ is preinstalled in nablarch-example-web and other Nablarch projects built from archetypes. 
This plugin provides the ability to easily deploy and run your project's code on an embedded server (such as Tomcat).
However, this plugin is not compatible with Jakarta EE, so change it to jetty-ee10-maven-plugin which provides similar functionality and also supports Jakarta EE.

Before modification, waitt-maven-plugin is set in ``pom.xml`` in nablarch-example-web as follows.

**Before modification**

.. code-block:: xml

  <plugin>
    <groupId>net.unit8.waitt</groupId>
    <artifactId>waitt-maven-plugin</artifactId>
    <version>1.2.3</version>
    <configuration>
      <servers>
        <server>
          <groupId>net.unit8.waitt.server</groupId>
          <artifactId>waitt-tomcat8</artifactId>
          <version>1.2.3</version>
        </server>
      </servers>
    </configuration>
  </plugin>

Change this to jetty-ee10-maven-plugin as follows.

**After modification**

.. code-block:: xml

  <plugin>
    <groupId>org.eclipse.jetty.ee10</groupId>
    <artifactId>jetty-ee10-maven-plugin</artifactId>
    <version>12.0.0</version>
  </plugin>

Now you can deploy and run your application code on Jetty.

If you want to actually run it, you can start Jetty with the following command.

.. code-block:: batch

  mvn jetty-ee10:run

.. _update-ntf-jetty:

Change nablarch-testing-jetty6 to nablarch-testing-jetty12
-----------------------------------------------------------------

If your web application project uses NTF (Nablarch Testing Framework), use the module ``nablarch-testing-jetty6`` to run the embedded server in your JUnit tests.
Jetty 6 launched with this module does not support Jakarta EE.
Jetty supports Jakarta EE 10 with Jetty 12, so you need to change it to use ``nablarch-testing-jetty12`` which can start Jetty 12.

.. tip::
  Java 11 or higher projects use ``nablarch-testing-jetty9`` to launch Jetty 9, but this is also not compatible with Jakarta EE, so it is necessary to change to ``nablarch-testing-jetty12``.

First, modify ``pom.xml`` as follows.

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-jetty12</artifactId> <!-- Change the artifactId to nablarch-testing-jetty12 -->
    <scope>test</scope>
  </dependency>

Next, modify the part that defines the components of ``HttpServerFactory`` as follows.

**Before modification**

.. code-block:: xml

  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty6"/>

**After modification**

.. code-block:: xml

  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty12"/>

In case of nablarch-example-web, the above settings exist in ``src/test/resources/unit-test.xml``.

With the above, the embedded server that is started when NTF is executed is switched to the version that supports Jakarta EE.

Change javax namespace to jakarta namespace
-----------------------------------------------------------------

The namespace changes that came with Jakarta EE 9 will also be applied to the application code.
The general flow of handling namespace changes is described below.

1. Grep the whole project with ``javax``
2. Judge whether the location found in the search is a Java EE namespace
3. If it is a Java EE namespace, replace ``javax`` with ``jakarta``

Details are described below.

``javax`` descriptions often appear in ``import`` statements in Java source code.
With the modifications made so far, Java EE dependencies have been removed and replaced with Jakarta EE dependencies, so ``import`` in the ``javax`` namespace causes compilation errors.

However, ``javax`` appears not only in ``import`` statements, but also in places where compilation errors do not occur.
For example, the key ``javax.servlet.forward.request_uri`` for obtaining the request URI before forwarding in Java Servlet is specified as a character string, so a compilation error does not occur (This key should be changed to ``jakarta.servlet.forward.request_uri`` for Jakarta Servlet).
In addition, even if it is described in JSP or configuration file, it will not be a compilation error, but it will be subject to correction.

Therefore, to check for the presence of the ``javax`` namespace, you must do a Grep search of the entire project.

Next, for the location hit by ``javax``, determine whether it is really a Java EE namespace.
For example, if you search nablarch-example-web with ``javax``, the following description will be hit.

.. code-block:: java

  import javax.validation.ConstraintValidator;

This is where the Bean Validation class is ``import``, so it can be judged as a Java EE namespace.

On the other hand, the following description also hits.

.. code-block:: java

  import javax.crypto.SecretKeyFactory;

This is not a Java EE namespace because it imports the classes related to cryptographic processing included in the standard library.

In this way, even if ``javax`` is hit, you cannot simply judge that they are all Java EE namespaces.
Namespaces for each specification are listed in the appendix :ref:`java_ee_jakarta_ee_comparation` on this page, so refer to this to determine if the hit ``javax`` is Java EE.

If it can be determined that it is a Java EE namespace, replace ``javax`` with ``jakarta``.
Below is an example of replacing ``import`` with ``jakarta``.

.. code-block:: java

  import jakarta.validation.ConstraintValidator;


With the above modifications, nablarch-example-web can now run on an application server that supports Jakarta EE 10.


Migration procedure of JSR352-compliant Batch Application
=========================================================================

All execution control platforms provided by Nablarch can be upgraded using the migration procedure described in the previous section.

However, for :doc:`../application_framework/application_framework/batch/jsr352/index` only, JBeret, which is used as the runtime of JSR352, and related libraries are complicated to update, so an additional explanation is given here.

When a JSR352-compliant Batch Application is generated from an archetype, ``dependency`` is set in ``pom.xml`` as shown below up to Nablarch 5.

**Before modification**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish</groupId>
      <artifactId>javax.el</artifactId>
      <version>...</version>
    </dependency>

    ...

    <!-- JBeretに最低限必要な依存関係 -->
    <dependency>
      <groupId>org.jboss.spec.javax.batch</groupId>
      <artifactId>jboss-batch-api_1.0_spec</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>javax.inject</groupId>
      <artifactId>javax.inject</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>javax.enterprise</groupId>
      <artifactId>cdi-api</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.spec.javax.transaction</groupId>
      <artifactId>jboss-transaction-api_1.2_spec</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-core</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.marshalling</groupId>
      <artifactId>jboss-marshalling</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld</groupId>
      <artifactId>weld-core</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.wildfly.security</groupId>
      <artifactId>wildfly-security-manager</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>...</version>
    </dependency>

    <!-- JBereteをJavaSEで動作させるための依存関係 -->
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-se</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld.se</groupId>
      <artifactId>weld-se</artifactId>
      <version>...</version>
    </dependency>

When upgrading to Nablarch 6, modify this as follows.

**After modification**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish.expressly</groupId>
      <artifactId>expressly</artifactId>
      <version>5.0.0</version>
    </dependency>

    ...

    <!-- JBeretに最低限必要な依存関係 -->
    <dependency>
      <groupId>jakarta.batch</groupId>
      <artifactId>jakarta.batch-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.inject</groupId>
      <artifactId>jakarta.inject-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.enterprise</groupId>
      <artifactId>jakarta.enterprise.cdi-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.transaction</groupId>
      <artifactId>jakarta.transaction-api</artifactId>
    </dependency>
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-core</artifactId>
      <version>2.1.1.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.marshalling</groupId>
      <artifactId>jboss-marshalling</artifactId>
      <version>2.0.12.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>3.4.3.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld</groupId>
      <artifactId>weld-core-impl</artifactId>
      <version>5.0.0.SP1</version>
    </dependency>
    <dependency>
      <groupId>org.wildfly.security</groupId>
      <artifactId>wildfly-elytron-security-manager</artifactId>
      <version>1.19.0.Final</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>31.1-jre</version>
    </dependency>

    <!-- JBereteをJavaSEで動作させるための依存関係 -->
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-se</artifactId>
      <version>2.1.1.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld.se</groupId>
      <artifactId>weld-se-core</artifactId>
      <version>5.0.0.SP1</version>
    </dependency>

--------------------------------------------------------------------
What to do if an error occurs during execution
--------------------------------------------------------------------

When NoClassDefFoundError occurs
-----------------------------------------------------------------

.. code-block:: text
  
  org.jboss.weld.exceptions.WeldException
      at org.jboss.weld.executor.AbstractExecutorServices.checkForExceptions (AbstractExecutorServices.java:82)
      ...
  Caused by: java.lang.NoClassDefFoundError
      at jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0 (Native Method)
      ...
  Caused by: java.lang.NoClassDefFoundError: Could not initialize class org.jboss.weld.logging.BeanLogger
      at org.jboss.weld.util.Beans.getBeanConstructor (Beans.java:279)

If the above stack trace is output at runtime and an error occurs, the error can be resolved by placing ``slf4j-nablarch-adaptor`` below Logback in ``pom.xml``.

.. code-block:: xml

  <dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.4</version>
  </dependency>

  <!-- Place slf4j-nablarch-adaptor below Logback -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
    <scope>runtime</scope>
  </dependency>


Appendix
=========================================================================

.. _java_ee_jakarta_ee_comparation:

--------------------------------------------------------------------
Correspondence table between Java EE and Jakarta EE specifications
--------------------------------------------------------------------

.. list-table:: Correspondence table between Java EE and Jakarta EE specifications
    :widths: 3, 1, 1, 3
    :header-rows: 1

    * - Java EE
      - Short name
      - Namespace prefix
      - Jakarta EE
    * - Java Servlet
      - 
      - ``javax.servlet``
      - `Jakarta Servlet (external site) <https://jakarta.ee/specifications/servlet/>`_
    * - JavaServer Faces
      - JSF
      - ``javax.faces``
      - `Jakarta Faces (external site) <https://jakarta.ee/specifications/faces/>`_
    * - Java API for WebSocket
      - 
      - ``javax.websocket``
      - `Jakarta WebSocket (external site) <https://jakarta.ee/specifications/websocket/>`_
    * - Concurrency Utilities for Java EE
      - 
      - ``javax.enterprise.concurrent``
      - `Jakarta Concurrency (external site) <https://jakarta.ee/specifications/concurrency/>`_
    * - Interceptors
      - 
      - ``javax.interceptor``
      - `Jakarta Interceptors (external site) <https://jakarta.ee/specifications/interceptors/>`_
    * - Java Authentication SPI for Containers
      - JASPIC
      - ``javax.security.auth.message``
      - `Jakarta Authentication (external site) <https://jakarta.ee/specifications/authentication/>`_
    * - Java Authorization Contract for Containers
      - JACC
      - ``javax.security.jacc``
      - `Jakarta Authorization (external site) <https://jakarta.ee/specifications/authorization/>`_
    * - Java EE Security API
      - 
      - ``javax.security.enterprise``
      - `Jakarta Security (external site) <https://jakarta.ee/specifications/security/>`_
    * - Java Message Service
      - JMS
      - ``javax.jms``
      - `Jakarta Messaging (external site) <https://jakarta.ee/specifications/messaging/>`_
    * - Java Persistence API
      - JPA
      - ``javax.persistence``
      - `Jakarta Persistence (external site) <https://jakarta.ee/specifications/persistence/>`_
    * - Java Transaction API
      - JTA
      - ``javax.transaction``
      - `Jakarta Transactions (external site) <https://jakarta.ee/specifications/transactions/>`_
    * - Batch Application for the Java Platform
      - JBatch
      - ``javax.batch``
      - `Jakarta Batch (external site) <https://jakarta.ee/specifications/batch/>`_
    * - JavaMail
      - 
      - ``javax.mail``
      - `Jakarta Mail (external site) <https://jakarta.ee/specifications/mail/>`_
    * - Java EE Connector Architecture
      - JCA
      - ``javax.resource``
      - `Jakarta Connectors (external site) <https://jakarta.ee/specifications/connectors/>`_
    * - Common Annotations for the Java Platform
      - 
      - ``javax.annotation``
      - `Jakarta Annotations (external site) <https://jakarta.ee/specifications/annotations/>`_
    * - JavaBeans Activation Framework
      - JAF
      - ``javax.activation``
      - `Jakarta Activation (external site) <https://jakarta.ee/specifications/activation/>`_
    * - Bean Validation
      - 
      - ``javax.validation``
      - `Jakarta Bean Validation (external site) <https://jakarta.ee/specifications/bean-validation/>`_
    * - Expression Language
      - EL
      - ``javax.el``
      - `Jakarta Expression Language (external site) <https://jakarta.ee/specifications/expression-language/>`_
    * - Enterprise JavaBeans
      - EJB
      - ``javax.ejb``
      - `Jakarta Enterprise Beans (external site) <https://jakarta.ee/specifications/enterprise-beans/>`_
    * - Java Architecture for XML Binding
      - JAXB
      - ``javax.xml.bind``
      - `Jakarta XML Binding (external site) <https://jakarta.ee/specifications/xml-binding/>`_
    * - Java API for JSON Binding
      - JSON-B
      - ``javax.json.bind``
      - `Jakarta JSON Binding (external site) <https://jakarta.ee/specifications/jsonb/>`_
    * - Java API for JSON Processing
      - JSON-P
      - * ``javax.json``
        * ``javax.json.spi``
        * ``javax.json.stream``
      - `Jakarta JSON Processing (external site) <https://jakarta.ee/specifications/jsonp/>`_
    * - JavaServer Pages
      - JSP
      - ``javax.servlet.jsp``
      - `Jakarta Server Pages (external site) <https://jakarta.ee/specifications/pages/>`_
    * - Java API for XML-Based Web Services
      - JAX-WS
      - ``javax.xml.ws``
      - `Jakarta XML Web Services (external site) <https://jakarta.ee/specifications/xml-web-services/>`_
    * - Java API for RESTful Web Services
      - JAX-RS
      - ``javax.ws.rs``
      - `Jakarta RESTful Web Services (external site) <https://jakarta.ee/specifications/restful-ws/>`_
    * - JavaServer Pages Standard Tag Library
      - JSTL
      - ``javax.servlet.jsp.jstl``
      - `Jakarta Standard Tag Library (external site) <https://jakarta.ee/specifications/tags/>`_
    * - Contexts and Dependency Injection for Java
      - CDI
      - * ``javax.decorator``
        * ``javax.enterprise.context``
        * ``javax.enterprise.event``
        * ``javax.enterprise.inject``
        * ``javax.enterprise.util``
      - `Jakarta Contexts and Dependency Injection (external site) <https://jakarta.ee/specifications/cdi/>`_
    * - Dependency Injection for Java
      - 
      - ``javax.inject``
      - `Jakarta Dependency Injection (external site) <https://jakarta.ee/specifications/dependency-injection/>`_

.. _jakarta_ee_runtime_dependency:

--------------------------------------------------------------------
Dependencies of runtimes of the typical specification
--------------------------------------------------------------------


JAX-RS, Jakarta RESTful Web Services
-----------------------------------------------------------------

Note: Artifacts listed are examples only and may not be required for all projects.

**Java EE**

.. code-block:: xml
    
  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>...</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.core</groupId>
    <artifactId>jersey-client</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.inject</groupId>
    <artifactId>jersey-hk2</artifactId>
  </dependency>


**Jakarta EE 10**

.. code-block:: xml
    
  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>3.1.1</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.core</groupId>
    <artifactId>jersey-client</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.inject</groupId>
    <artifactId>jersey-hk2</artifactId>
  </dependency>


EL, Jakarta Expression Language
-----------------------------------------------------------------

**Java EE**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish</groupId>
    <artifactId>javax.el</artifactId>
    <version>...</version>
  </dependency>

**Jakarta EE 10**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish.expressly</groupId>
    <artifactId>expressly</artifactId>
    <version>5.0.0</version>
  </dependency>


JSTL, Jakarta Standard Tag Library
-----------------------------------------------------------------

**Java EE**

.. code-block:: xml

  <dependency>
    <groupId>taglibs</groupId>
    <artifactId>standard</artifactId>
    <version>...</version>
  </dependency>

**Jakarta EE 10**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
    <version>3.0.0</version>
  </dependency>
