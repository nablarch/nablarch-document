.. _setup_blank_project_for_Java21:

----------------------------------------------------------
How to Setup When Using With Java21
----------------------------------------------------------

When using blank projects in Java 21, perform the following procedure before communication confirmation of each blank project.

* Change the standard encoding（if you want the standard encoding to be the same execution environment as Java 17 or earlier）
* Change of Java Version

Change the standard encoding（If you want to make the standard encoding dependent on the execution environment as before Java 17）
----------------------------------------------------------------------------------------------------------------------------------------------------------

Since Java 18, the standard encoding is UTF-8, making it environment independent. If you want to make the standard encoding dependent on the execution environment as before Java 17, specify the system property as a runtime option for the Java command as shown below.

* ``-Dfile.encoding=COMPAT``

.. tip::
  When running from Maven, the environment variable `MAVEN_OPTS (external site) <https://maven.apache.org/configure.html#maven_opts-environment-variable>`_ can be used to set the JVM options. However, ``Picked up MAVEN_OPTS: -Dfile.encoding=COMPAT`` is displayed in the log.
  Please note that the settings for JVM options may differ depending on Maven plugin.(For example, in maven-surefire-plugin that runs the test, it needs to be specified in ``argLine`` in plugin settings in pom.xml)

.. important::
  The ``-Dfile.encoding=COMPAT`` option is not valid until Java 17, so be careful not to apply this JVM option to previous execution environments.

Change of Java Version
------------------------------

In a blank project, Java 17 is set as the Java version
that the source and class files conform to, so change the file as below.

* pom.xml

.. code-block:: xml

    <!-- Change Java version as follows -->
    <java.version>21</java.version>
