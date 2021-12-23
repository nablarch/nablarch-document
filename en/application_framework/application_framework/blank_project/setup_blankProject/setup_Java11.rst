.. _setup_blank_project_for_Java11:

----------------------------------------------------------
How to Setup When Using With Java11
----------------------------------------------------------

When using blank projects in Java 11, perform the following procedure before communication confirmation of each blank project.

* Add dependent module
* Add dependent module used by gsp-dba-maven-plugin
* Change of Jetty module used in automatic test (only for web projects or RESTful web service projects)

.. tip::
   The blank project for containers assumes Java 11, and the modifications described in this chapter have been applied beforehand.
   Therefore, in a blank project for containers the procedures of this chapter are not necessary.

.. _setup_blank_project_for_Java11_add_dependencies:

Add dependent module
-------------------------------------------------------------

Add the following modules to the created blank project POM.

.. code-block:: xml

  <dependencies>
    <!-- Omitted -->
    <!-- Add the following. -->
    <dependency>
      <groupId>com.sun.activation</groupId>
      <artifactId>javax.activation</artifactId>
      <version>1.2.0</version>
    </dependency>
    <dependency>
      <groupId>javax.xml.bind</groupId>
      <artifactId>jaxb-api</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-core</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-impl</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>javax.annotation</groupId>
      <artifactId>javax.annotation-api</artifactId>
      <version>1.3.2</version>
    </dependency>
  </dependencies>


Add dependent module used by gsp-dba-maven-plugin
----------------------------------------------------------

Configure by referring to the following.

`Configuration in Java11 <https://github.com/coastland/gsp-dba-maven-plugin#java11%E3%81%A7%E3%81%AE%E8%A8%AD%E5%AE%9A>`_ (external site)

.. _setup_java11_jetty9:

Change of Jetty module used in automatic test (only for web projects or RESTful web service projects)
------------------------------------------------------------------------------------------------------------------

The Jetty version which is configured by default in the blank project does not support Java11.
Therefore, make changes to 2 files as given below.

* pom.xml

.. code-block:: xml

  <!-- Change the location of nablarch-testing-jetty6 as follows -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-jetty9</artifactId>
    <scope>test</scope>
  </dependency>


* src/test/resources/unit-test.xml

.. code-block:: xml

  <!-- Change the location of HttpServerFactoryJetty6 as follows -->
  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty9"/>

