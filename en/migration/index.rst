=========================================================================
Nablarch 5 to 6 Migration Guide
=========================================================================

.. contents:: Table of contents
  :depth: 4
  :local:

This document will explain how to migration a project created with Nablarch 5 to Nablarch 6.

.. important::
  Nablarch 6 version 6/6u1 is a pre-release version, and 6u2 will be the first version after the official release.
  Therefore, the procedures described here assume that you are upgrading from the latest version of Nablarch 5 to Nablarch 6u2.
  When upgrading to 6u3 or later, additional steps may be required in addition to those explained here.
  Be sure to check the upgrade procedure by referring to the release notes for 6u3 or later in order.

Major differences between Nablarch 5 and 6
=========================================================================

--------------------------------------------------------------------
Supports Jakarta EE 10
--------------------------------------------------------------------

Nablarch 6 supports Jakarta EE 10.

Jakarta EE is the name after Java EE was transferred to the Eclipse Foundation and is the successor to Java EE.
Basically, the Java EE specifications have been transferred as they are, but with Jakarta EE 9, there has been a major change in that the namespace has changed from ``javax.*`` to ``jakarta.*``.

Therefore, in order to migrate a project created with Nablarch 5 to Nablarch 6, it is necessary not only to upgrade Nablarch but also to make project compatible with Jakarta EE 10.

Also, backward compatibility cannot be maintained due to namespace changes, etc., so an application server compatible with Jakarta EE 10 is required to run on application server.

--------------------------------------------------------------------
Changed  required Java version to 17
--------------------------------------------------------------------

Nablarch 6 modules are compiled with Java 17, so you will need Java 17 or higher to work.

Prerequisites
=========================================================================

The instructions here assume that you have already upgraded to the latest version of Nablarch 5.

For projects created with an older version, first upgrade to the latest version of Nablarch 5, then migrate to Nablarch 6.
See `Nablarch 5 release notes <https://nablarch.github.io/docs/5-LATEST/doc/releases/index.html>`_ for details on the modifications required to upgrade to the latest version of Nablarch 5.

Additionally, in order to operate, an application server that supports Java 17 or higher and Jakarta EE 10 is required, so it must be operated in an environment that supports these.

.. tip::
  In addition to upgrade to the latest version of Nablarch 5, it will also need to be supported for use with Java 17 or higher.
  See `Nablarch 5 setup procedure <https://nablarch.github.io/docs/5-LATEST/doc/en/application_framework/application_framework/blank_project/FirstStep.html>`_ for instructions on how to respond.


Overview of migration steps
=========================================================================

To get a Nablarch 5 project migrate to Nablarch 6, roughly two modifications are required:

* Nablarch version upgrade
* Compatible with Jakarta EE

The first "Nablarch version upgrade" refers to changing the version of Nablarch used in the project from 5 to 6.

The second, "Compatible with Jakarta EE", refers to making the project compatible with Jakarta EE 10.
This includes changes to namespaces introduced in Jakarta EE 9, and changes libraries that depend on Java EE to Jakarta EE-compatible versions.

Each specific procedure will be described below.


Details of migration steps
=========================================================================

In this section will explain in detail each of the migration steps required when migration a Nablarch 5 project to Nablarch 6.

Depending on the project, unnecessary steps may be included, but in that case, select and read as appropriate (for example, :ref:`waitt-to-jetty` and :ref:`update-ntf-jetty` are steps specific to web projects, so there is no problem in skipping them in batch projects).

--------------------------------------------------------------------
Nablarch version upgrade
--------------------------------------------------------------------

The version of each module that makes up Nablarch is managed by BOM, so you can upgrade Nablarch by changing the version of BOM.
Change ``<version>`` in ``pom.xml`` where Nablarch's BOM is loaded, as shown below.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.nablarch.profile</groupId>
        <artifactId>nablarch-bom</artifactId>
        <version>6u2</version>
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

The ``dependency`` of Java EE API is different and not unified depending on the jar provider and version.
Therefore, it cannot be determined mechanically from ``groupId``.
Which ``dependency`` is a Java EE API must be determined from ``groupId``, ``artifactId``, classes included in the jar, and so on.

For your reference, archetypes and examples provided by Nablarch changes listed below.

In addition, in example applications, by reading the BOM provided by Jakarta EE, it is possible to avoid specifying the version individually.
It is recommended to read BOM because it reduces the trouble of checking the version and mistakes in specification, and makes management easier.

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

Additionally, :ref:`java_ee_jakarta_ee_comparation` is listed as an appendix at the end of this page as a reference for changing dependencies that are not listed in the modification examples.
What is ``dependency`` in Jakarta EE is described on each specification page, so please check it (for example, `Jakarta Servlet 6.0 specification page (external site) <https: //jakarta.ee/specifications/servlet/6.0/#details>`_ shows ``jakarta.servlet:jakarta.servlet-api:jar:6.0.0`` in "Maven coordinates").

Java Servlet → Jakarta Servlet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>...</version>
    <scope>provided</scope>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <scope>provided</scope>
  </dependency>


JSP → Jakarta Server Pages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>javax.servlet.jsp</groupId>
    <artifactId>javax.servlet.jsp-api</artifactId>
    <version>...</version>
    <scope>provided</scope>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.servlet.jsp</groupId>
    <artifactId>jakarta.servlet.jsp-api</artifactId>
    <scope>provided</scope>
  </dependency>

JSTL → Jakarta Standard Tag Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>javax.servlet.jsp.jstl</groupId>
    <artifactId>javax.servlet.jsp.jstl-api</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
  </dependency>

JPA → Jakarta Persistence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>org.apache.geronimo.specs</groupId>
    <artifactId>geronimo-jpa_2.0_spec</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.persistence</groupId>
    <artifactId>jakarta.persistence-api</artifactId>
  </dependency>

JAX-RS → Jakarta RESTful Web Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.ws.rs</groupId>
    <artifactId>jakarta.ws.rs-api</artifactId>
  </dependency>

Common Annotations for the Java Platform → Jakarta Annotations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>javax.annotation</groupId>
    <artifactId>javax.annotation-api</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>jakarta.annotation</groupId>
    <artifactId>jakarta.annotation-api</artifactId>
  </dependency>


Update Java EE specification implementation library
-----------------------------------------------------------------

If you have embedded Java EE specification implementation library in your application, replace them with those from Jakarta EE.

To find out which ``dependency`` is Java EE specification implementation library, you need to investigate each ``dependency`` individually.
Also, if it is found to be a Java EE specification implementation library, what the ``dependency`` of the Jakarta EE compliant version of that implementation library will be depends on the implementation library.
Therefore, it is necessary to check the official site etc. for each implementation library used in the project.

For your reference, archetypes and examples provided by Nablarch changes listed below.

Compatible implementations are also introduced on each Jakarta EE specification page, so please refer to those as well.
(For example, the `Jakarta RESTful Web Services 3.1 specification page (external site) <https://jakarta.ee/specifications/restful-ws/3.1/#compatible-implementations>`_ lists Eclipse Jersey as a compatible implementation. 3.1.0 is introduced)

Bean Validation → Jakarta Bean Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>5.3.6.Final</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>8.0.0.Final</version>
  </dependency>

JSTL → Jakarta Standard Tag Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>taglibs</groupId>
    <artifactId>standard</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
    <version>3.0.0</version>
  </dependency>

JAX-RS → Jakarta RESTful Web Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

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

**After modification**

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>3.1.8</version>
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

JMS → Jakarta Messaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Before modification**

.. code-block:: xml

  <dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>activemq-all</artifactId>
    <version>...</version>
  </dependency>

**After modification**

.. code-block:: xml

  <dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>artemis-server</artifactId>
    <version>2.37.0</version>
  </dependency>
  <dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>artemis-jakarta-server</artifactId>
    <version>2.37.0</version>
  </dependency>
  <dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>artemis-jakarta-client</artifactId>
    <version>2.37.0</version>
  </dependency>


Update gsp-dba-maven-plugin
-----------------------------------------------------------------

`gsp-dba-maven-plugin (external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_ is preinstalled in nablarch-example-web and other projects built from archetypes.
This plugin provides a function (``generate-entity``) to generate Java entity classes from database table metadata.
Since Java EE annotations such as JPA are set in this entity class, it cannot be used as is in the Jakarta EE environment.

Since gsp-dba-maven-plugin is compatible with Jakarta EE in 5.0.0, change ``<version>`` of gsp-dba-maven-plugin in ``pom.xml``.

.. code-block:: xml

    <plugin>
      <groupId>jp.co.tis.gsp</groupId>
      <artifactId>gsp-dba-maven-plugin</artifactId>
      <version>5.1.0</version>
      <configuration>
      ...

Furthermore, in order to use the ``generate-entity`` of the gsp-dba-maven-plugin that supports Jakarta EE, it is necessary to add ``dependency`` and JVM arguments.
See the `gsp-dba-maven-plugin guide (external site) <https://github.com/coastland/gsp-dba-maven-plugin?tab=readme-ov-file#generate-entity>`_ for details.

As described above, an entity for which Jakarta EE annotations are set will be generated.

.. _waitt-to-jetty:

Change waitt-maven-plugin to jetty-ee10-maven-plugin
-----------------------------------------------------------------

The `waitt-maven-plugin (external site) <https://github.com/kawasima/waitt>`_ is preinstalled in nablarch-example-web and other web application projects built from archetypes.
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
    <version>12.0.12</version>
  </plugin>

Now you can deploy and run your application code on Jetty.

If you want to actually run it, you can start Jetty with the following command.

.. code-block:: batch

  mvn jetty:run

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

1. Code that is ``import`` in ``javax`` namespace causes a compilation error, so change to ``jakarta`` namespace.
1. Grep the whole project with ``javax`` and find out where there are no compilation errors.
2. Judge whether the location found in the search is a Java EE namespace
3. If it is a Java EE namespace, replace ``javax`` with ``jakarta``

Details are described below.

``javax`` descriptions often appear in ``import`` statements in Java source code.
With the modifications made so far, Java EE dependencies have been removed and replaced with Jakarta EE dependencies, so ``import`` in the ``javax`` namespace causes compilation errors.
Therefore, first check where the compilation error occurs and change to ``jakarta`` namespace.

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


Change XML schema specification to Jakarta EE 10 schema
-----------------------------------------------------------------

XML files such as ``web.xml`` specify an XML schema, but change this to a schema compatible with Jakarta EE 10.
Schemas provided in Jakarta EE 10 can be found at `Jakarta EE XML Schemas (external site) <https://jakarta.ee/xml/ns/jakartaee/#10>`_ .

**Before modification**

.. code-block:: xml

  <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
           http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
           version="3.1">

**After modification**

.. code-block:: xml

  <web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee
                               web-app_6_0.xsd"
           version="6.0">


Change tag library namespace to Jakarta EE 10 namespace
-----------------------------------------------------------------------------

In the JSP file, the tag library namespace is specified using the taglib directive, but change this to a namespace compatible with Jakarta EE 10.
You can check the namespaces provided in Jakarta EE 10 at `Jakarta Standard Tag Library 3.0 (external site) <https://jakarta.ee/specifications/tags/3.0/>`_ .

**Before modification**

.. code-block:: jsp

  <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

**After modification**

.. code-block:: jsp

  <%@ taglib prefix="c" uri="jakarta.tags.core" %>


Migration procedure of JSR352-compliant Batch Application
=========================================================================

All execution control platforms provided by Nablarch can be migrate using the procedure described in the previous section.

However, for :doc:`../application_framework/application_framework/batch/jsr352/index` only, JBeret, which is used as implementation compliant with JSR352, and related libraries are complicated to update, so an additional explanation is given here.

When a JSR352-compliant Batch Application is generated from an archetype, ``dependency`` is set in ``pom.xml`` as shown below up to Nablarch 5.

**Before modification**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish</groupId>
      <artifactId>javax.el</artifactId>
      <version>...</version>
    </dependency>

    ...

    <!-- Minimum required dependencies for JBeret -->
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

    <!-- Dependencies for JBeret to work with Java SE -->
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

    <!-- Dependencies when outputting logs with Logback -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>...</version>
    </dependency>

When migrate to Nablarch 6, modify this as follows.

**After modification**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish.expressly</groupId>
      <artifactId>expressly</artifactId>
      <version>5.0.0</version>
    </dependency>

    ...

    <!-- Minimum required dependencies for JBeret -->
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
      <version>2.1.4.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.marshalling</groupId>
      <artifactId>jboss-marshalling</artifactId>
      <version>2.1.3.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>3.5.3.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld</groupId>
      <artifactId>weld-core-impl</artifactId>
      <version>5.0.1.Final</version>
    </dependency>
    <dependency>
      <groupId>org.wildfly.security</groupId>
      <artifactId>wildfly-elytron-security-manager</artifactId>
      <version>2.2.2.Final</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>32.1.1-jre</version>
    </dependency>

    <!-- Dependencies for JBeret to work with Java SE -->
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-se</artifactId>
      <version>2.1.4.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld.se</groupId>
      <artifactId>weld-se-core</artifactId>
      <version>5.0.1.Final</version>
    </dependency>

    <!-- Dependencies when outputting logs with Logback -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.11</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.5.6</version>
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
  Caused by: java.lang.NoClassDefFoundError:Could not initialize class org.jboss.weld.logging.BeanLogger
      at org.jboss.weld.util.Beans.getBeanConstructor (Beans.java:279)


If a stack trace like the one above is output during execution and an error occurs, you can resolve the error by placing ``slf4j-nablarch-adaptor`` after Logback in the classpath order.
When running with Maven, you can change the classpath order by placing ``slf4j-nablarch-adaptor`` in ``pom.xml`` below Logback.

.. code-block:: xml

  <dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>...</version>
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
      - jBatch
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
