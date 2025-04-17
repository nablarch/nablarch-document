.. _setup_blank_project_for_Java17:

----------------------------------------------------------
How to Setup When Using With Java17
----------------------------------------------------------

When using blank projects in Java 17, perform the following procedure before communication confirmation of each blank project.

* Add dependent module
* Configure gsp-dba-maven-plugin to work with Java 17
* Change of Jetty module used in automatic test (only for web projects or RESTful web service projects)
* Add --add-opens options (only for JSR352-compliant batch project)
* Change of Java Version

.. _setup_blank_project_for_Java17_add_dependencies:

Add dependent module
-------------------------------------------------------------

With Java 11, some modules, such as JAXB, have been removed from the standard library.
Removed modules need to be explicitly added to dependencies.
Therefore, add the following modules to the created blank project POM.

There are two differences from the :ref:`Add dependent module in Java 11 <setup_blank_project_for_Java11_add_dependencies>`.

* Specify ``jaxb-impl`` version as ``2.3.5``.

  * This version includes support for Java 17 enhanced encapsulation.

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

.. _setup_blank_project_for_Java17_gsp_dba_maven_plugin:

Configure gsp-dba-maven-plugin to work with Java 17
----------------------------------------------------------

Configure by referring to the following.

`Configuration in Java17 <https://github.com/coastland/gsp-dba-maven-plugin/tree/4.x.x-main/en#java17-configuration>`_ (external site)

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

.. _setup_blank_project_for_Java17_add_JVMoption:

Add --add-opens options (only for JSR352-compliant batch project)
------------------------------------------------------------------------------------------------------------------

Encapsulation has been enhanced in Java 17, and internal APIs such as the standard API are no longer available for reflection by default.
The canonical fix for this change would be to migrate to an alternate API. However, jBeret, the JSR352 implementation used in JSR352-compliant batch project, does not include this fix.

Therefore, in order to run JSR352-compliant batch project in Java 17 as well, the following JVM options must be set so that the internal API can be used in reflection.

* ``--add-opens java.base/java.lang=ALL-UNNAMED``
* ``--add-opens java.base/java.security=ALL-UNNAMED``

.. tip::
  Specifying this JVM option is also the method used by WildFly, which includes jBeret.
  
  * `Running WildFly with SE 17 (external site) <https://www.wildfly.org/news/2021/12/16/WildFly26-Final-Released/#running-wildfly-with-se-17>`_

The following is an example of a command with the options specified.

.. code-block:: batch

  > java --add-opens java.base/java.lang=ALL-UNNAMED ^
         --add-opens java.base/java.security=ALL-UNNAMED ^
         -jar target\myapp-batch-ee-0.1.0\myapp-batch-ee-0.1.0.jar ^
         sample-batchlet

.. tip::
  When running from Maven, the environment variable `MAVEN_OPTS (external site) <https://maven.apache.org/configure.html#MAVEN_OPTS_environment_variable.3A>`_ can be used to set the JVM options.

Change of Java Version
------------------------------

In a blank project, Java 8 is set as the Java version 
that the source and class files conform to, so change the file as below.

* pom.xml

.. code-block:: xml

    <!-- Change Java version as follows -->
    <java.version>17</java.version>

