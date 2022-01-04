.. _setup_blank_project_for_Java17:

----------------------------------------------------------
How to Setup When Using With Java17
----------------------------------------------------------

When using blank projects in Java 17, perform the following procedure before communication confirmation of each blank project.

* Add dependent module
* Configure gsp-dba-maven-plugin to work with Java 17
* Change of Jetty module used in automatic test (only for web projects or RESTful web service projects)
* Add --add-opens options (only for JSR352-compliant batch project)

Add dependent module
-------------------------------------------------------------

Add the following modules to the created blank project POM.

There are two differences from the :ref:`Add dependent module in Java 11 <setup_blank_project_for_Java11_add_dependencies>`.

* Specify ``jaxb-impl`` version as ``2.3.5``.
* Remove the ``jaxb-api`` artifact.

  * Because ``2.3.5`` of ``jaxb-impl`` transitively uses another artifact called ``jakarta.xml.bind-api``.

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
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-core</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-impl</artifactId>
      <version>2.3.5</version>
    </dependency>
    <dependency>
      <groupId>javax.annotation</groupId>
      <artifactId>javax.annotation-api</artifactId>
      <version>1.3.2</version>
    </dependency>
  </dependencies>


Configure gsp-dba-maven-plugin to work with Java 17
----------------------------------------------------------

Configure by referring to the following.

`Configuration in Java17 <https://github.com/coastland/gsp-dba-maven-plugin#java17%E3%81%A7%E3%81%AE%E8%A8%AD%E5%AE%9A>`_ (external site)

.. _setup_java17_jetty9:

Change of Jetty module used in automatic test (only for web projects or RESTful web service projects)
------------------------------------------------------------------------------------------------------------------

The Jetty version which is configured by default in the blank project does not support Java17.
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


Add --add-opens options (only for JSR352-compliant batch project)
------------------------------------------------------------------------------------------------------------------

When running a JSR352-compliant batch project, the following JVM options need to be set.

* ``--add-opens java.base/java.lang=ALL-UNNAMED``
* ``--add-opens java.base/java.security=ALL-UNNAMED``

The following is an example of a command with the options specified.

.. code-block:: batch

  > java --add-opens java.base/java.lang=ALL-UNNAMED ^
         --add-opens java.base/java.security=ALL-UNNAMED ^
         -jar target\myapp-batch-ee-0.1.0\myapp-batch-ee-0.1.0.jar ^
         sample-batchlet

.. tip::
  When running from Maven, the environment variable `MAVEN_OPTS (external site) <https://maven.apache.org/configure.html#maven_opts-environment-variable>`_ can be used to set the JVM options.
