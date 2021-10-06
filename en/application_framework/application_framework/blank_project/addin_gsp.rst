.. _gsp-maven-plugin:

==================================================================================================================
Initial Configuration Method of gsp-dba-maven-plugin (DBA Work Support Tool)
==================================================================================================================

.. contents:: Table of contents
  :depth: 2
  :local:

Summary
====================================================

`gsp-dba-maven-plugin(external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_ is an open source tool provided under the Apache License Version 2.0 license.

gsp-dba-maven-plugin needs to be configured according to the RDBMS before starting the use.

This procedure shows the configuration method to use the gsp-dba-maven-plugin in the project generated from archetype.

Prerequisites
====================================================

The following projects are covered.

* Various projects that have implemented :doc:`CustomizeDB` procedures after generation from archetypes.

Configuration of Maven
=============================================

Configuration of third party repository is required to use gsp-dba-maven-plugin.

Configured in >/.m2/settings.xml.

.. code-block:: xml

  <settings>
    <!-- Omitted -->
    <profiles>
      <profile>
        <id>my-repository</id>
        <pluginRepositories>
          <pluginRepository>
            <id>maven.seasar.org</id>
            <name>The Seasar Foundation Maven Repository</name>
            <url>https://maven.seasar.org/maven2</url>
            <snapshots>
              <enabled>false</enabled>
            </snapshots>
          </pluginRepository>
          <pluginRepository>
            <id>maven-snapshot.seasar.org</id>
            <name>The Seasar Foundation Maven Snapshot Repository</name>
            <url>https://maven.seasar.org/maven2-snapshot</url>
            <releases>
              <enabled>false</enabled>
            </releases>
            <snapshots>
              <enabled>true</enabled>
              <updatePolicy>always</updatePolicy>
            </snapshots>
          </pluginRepository>
        </pluginRepositories>
      </profile>
    </profiles>
    <!-- Omitted -->
  </settings>

.. tip::

  gsp-dba-maven-plugin is configured to use H2 Database Engine (hereinafter H2) by default.

  The following steps are not required if H2 is used. Perform only :ref:`confirm_gsp`.


File modification
===========================


Modification of the pom.xml file
------------------------------------------------------

In the properties element
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Modify the following locations in the properties tag of pom.xml.

=============================================== ===========================================
Property name                                    Description
=============================================== ===========================================
nablarch.db.jdbcDriver                          JDBC driver class name
nablarch.db.url                                 Database connection URL
nablarch.db.adminUser                           Administrator user name
nablarch.db.adminPassword                       Administrator user password
nablarch.db.user                                Database access user name
nablarch.db.password                            Database access user password
nablarch.db.schema                              Connection schema name
=============================================== ===========================================

A description example is shown below.

**Oracle configuration example**


.. code-block:: xml

    <nablarch.db.jdbcDriver>oracle.jdbc.driver.OracleDriver</nablarch.db.jdbcDriver>
    <!-- jdbc:oracle:thin:@Host name:Port number:Database SID-->
    <nablarch.db.url>jdbc:oracle:thin:@localhost:1521/xe</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


**PostgreSQL configuration example**

.. code-block:: xml

    <nablarch.db.jdbcDriver>org.postgresql.Driver</nablarch.db.jdbcDriver>
    <!-- jdbc:postgresql://Host name:Port number/Database name -->
    <nablarch.db.url>jdbc:postgresql://localhost:5432/postgres</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


**DB2 configuration example**

.. code-block:: xml

    <nablarch.db.jdbcDriver>com.ibm.db2.jcc.DB2Driver</nablarch.db.jdbcDriver>
    <!-- jdbc:db2://Host name:Port number/Database name -->
    <nablarch.db.url>jdbc:db2://localhost:50000/SAMPLE</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


**SQLServer configuration example**


.. code-block:: xml

    <nablarch.db.jdbcDriver>com.microsoft.sqlserver.jdbc.SQLServerDriver</nablarch.db.jdbcDriver>
    <!-- jdbc:sqlserver://Host name:Port number;instanceName=Instance name -->
    <nablarch.db.url>jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


In the build element
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modify the dependency on gsp-dba-maven-plugin to the one that matches the RDBMS used from the H2 JDBC driver.

For POM configuration example, see :ref:`customizeDB_pom_dependencies`.
For example, when using PostgreSQL, configure as follows.

.. code-block:: xml

  <build>
    <plugins>
      <plugin>
        <groupId>jp.co.tis.gsp</groupId>
        <artifactId>gsp-dba-maven-plugin</artifactId>
        <dependencies>
          <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <!-- Replace the version as appropriate. -->
            <version>42.1.4</version>
          </dependency>
        </dependencies>
      </plugin>
    </plugins>
  </build>

Preparation of data-model.edm (src/main/resources/entity)
------------------------------------------------------------------------

Since an edm file is present for each RDBMS under src/main/resources/entity, rename the file corresponding to the RDBMS to be used to "data-model.edm".

.. _confirm_gsp:

Communication confirmation
===========================

.. important::

  Since data in the DB will be deleted, backup the current data if necessary.


**1. Execute the following command to execute steps from DDL generation to dump file creation.**

.. code-block:: bash

  mvn -P gsp clean generate-resources

.. tip ::

  The project's pom.xml generated from each archetype so that the following goals are executed It is described in.

  * generate-ddl
  * execute-ddl
  * load-data
  * export-schema


If successful, the log given below will be output to the console.

.. code-block:: text

  (omitted)
  [INFO] --- gsp-dba-maven-plugin:3.2.0:export-schema (default-cli) @ myapp-web ---
  [INFO] PUBLICスキーマのExportを開始します。:C:\develop\myapp\myapp-web\gsp-target\output\PUBLIC.dmp
  [INFO] Building jar: C:\develop\myapp-web\gsp-target\output\myapp-web-testdata-0.1.0.jar
  [INFO] PUBLICスキーマのExport完了
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 5.415 s
  [INFO] Finished at: 2016-05-11T21:17:03+09:00
  [INFO] Final Memory: 13M/31M
  [INFO] ------------------------------------------------------------------------


Also, a jar file containing the dump file is generated in the ``gsp-target/output/`` directory.

.. tip::

  If the execution fails, check if any restrictions specific to the RDBMS are violated.

  For restrictions specific to the RDBMS, refer to "Common Goal Parameters" at https://github.com/coastland/gsp-dba-maven-plugin (external site).


**2. Install the dump file to the local repository by executing the following command.**

.. code-block:: bash

  mvn -P gsp install:install-file


If successful, the log given below will be output to the console.

.. code-block:: text

  (omitted)
  [INFO] --- maven-install-plugin:2.5.2:install-file (default-cli) @ myapp-web ---
  [INFO] pom.xml not found in myapp-web-testdata-0.1.0.jar
  [INFO] Installing C:\develop\myapp-web\gsp-target\output\myapp-web-testdata-0.1.0.jar to C:\Users\TISxxxxxx\.m2\repository\com\example\myapp-web-testdata\0.1.0\myapp-web-testdata-0.1.0.jar
  [INFO] Installing C:\Users\TISxxx~1\AppData\Local\Temp\mvninstall7441010390688212345.pom to C:\Users\TISxxxxxx\.m2\repository\com\example\myapp-web-testdata\0.1.0\myapp-web-testdata-0.1.0.pom
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 1.077 s
  [INFO] Finished at: 2016-05-12T14:37:39+09:00
  [INFO] Final Memory: 8M/20M
  [INFO] ------------------------------------------------------------------------



**3. Import the dump file by executing the following command.**

.. code-block:: bash

  mvn -P gsp gsp-dba:import-schema


If successful, the log given below will be output to the console.

.. code-block:: text

  (omitted)
  [INFO] スキーマのインポートを開始します。:C:\develop\myapp-web\gsp-target\output\PUBLIC.dmp
  [INFO] スキーマのインポートを終了しました
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 2.584 s
  [INFO] Finished at: 2016-05-12T14:49:58+09:00
  [INFO] Final Memory: 9M/23M
  [INFO] ------------------------------------------------------------------------
