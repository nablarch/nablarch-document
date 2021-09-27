
=======================================================
Procedure for Changing the RDBMS used
=======================================================

.. contents:: Table of contents
  :depth: 2
  :local:

Projects created using the Nablarch archetype are configured to use **the H2 Database Engine (hereinafter H2) by default**.

The procedure to change the configuration to use a different RDBMS is described.


Prerequisites
===========================

The following is assumed.

* The project immediately after generation from each archetype is the target.
* The user and schema used for connecting have been created in the RDBMS. Users of the RDBMS must have been granted appropriate permissions.


.. _customizeDBAddFileMavenRepo:

File registration to the Maven repository
================================================================

---------------------------
Register the JDBC driver
---------------------------

One of the following must be satisfied for the JDBC driver to be used.

* The driver should be registered in the central repository of Maven.
* The driver should be registered in the Maven repository of the project.
* The driver should be registered in the local Maven repository.


This section describes how to register a JDBC driver that is not published in the Maven central repository to the local Maven repository. Replace the driver version in the procedure as appropriate.

.. important::
  * It is highly recommended that the JDBC driver be registered in the Maven repository of the project before building the CI environment.
  * How to obtain the JDBC driver is also explained below.Confirm the license before obtaining the JDBC driver.

H2
------

In the case of H2, registration is not required because the JDBC driver is published in the Maven central repository.

Oracle
------

Since the Oracle JDBC driver is not published in the Maven central repository, it is necessary to register it in the local Maven repository.

The JDBC driver can be downloaded from the following site on the Internet.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 6,10


  * - Distribution site name
    - URL

  * - JDBC, SQLJ, Oracle JPublisher and Universal Connection Pool (UCP)
    - http://www.oracle.com/technetwork/jp/database/features/jdbc/index-099275-ja.html (External site)

An example of the command to register the downloaded JDBC driver to the local Maven repository is shown below.

.. code-block:: bash

    mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.4.0 -Dpackaging=jar -Dfile=ojdbc6.jar

.. tip::

  `maven-install-plugin(external site) <https://maven.apache.org/plugins/maven-install-plugin/install-file-mojo.html>`_ is used for registration to the local Maven repository.

PostgreSQL
------------------

In the case of PostgreSQL, registration is not required because the JDBC driver is published in the Maven central repository.


DB2
------------------

Since DB2 JDBC driver is not published in the Maven central repository, it is necessary to register it in the local Maven repository.

The JDBC driver can be downloaded from the following site on the Internet.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 6,10


  * - Distribution site name
    - URL

  * - IBM DB2 JDBC Driver Versions |br|
      and Downloads - Japan
    - http://www-01.ibm.com/support/docview.wss?uid=swg21363866 (External site)

An example of the command to register the downloaded JDBC driver to the local Maven repository is shown below.

.. code-block:: bash

    mvn install:install-file -DgroupId=com.ibm -DartifactId=db2jcc4 -Dversion=10.5.0.7 -Dpackaging=jar -Dfile=db2jcc4.jar


SQLServer
------------------

In the case of SQLServer, you don't need to register the JDBC driver because it is available in Maven's central repository


.. _customizeDBNotExistPjRepo:

File modification
===========================

---------------------------------------------
Modification of the properties file
---------------------------------------------

Modify the following location in env.properties.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 5,4,10


  * - Property name
    - Description
    - Project/Module used
  * - nablarch.connectionFactory. |br|
      jndiResourceName
    - Resource name when acquiring the DataSource with JNDI
    - * Projects generated from each archetype
        (configure in the properties file (described below) of environment that acquires connections from JNDI)
  * - nablarch.db.jdbcDriver
    - JDBC driver class name
    - * Projects generated from each archetype
        (configure in the properties file (described below) of environments that create local connection pools)
  * - nablarch.db.url
    - Database connection URL
    - * Projects generated from each archetype
        (configure in the properties file (described below) of environments that create local connection pools)
  * - nablarch.db.user
    - Database access user name
    - * Projects generated from each archetype
        (configure in the properties file (described below) of environments that create local connection pools)
  * - nablarch.db.password
    - Database access user password
    - * Projects generated from each archetype
        (configure in the properties file (described below) of environments that create local connection pools)
  * - nablarch.db.schema
    - Connection schema name
    - * Nablarch testing framework



Immediately after a project is generated from an archetype, the following applies to the "properties file of the environment that acquires connections from JNDI".

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,6

  * - Project type
    - Config file of the environment that acquires connections from JNDI
  * - * Web
      * RESTful web service
    - * Production environment properties(src/env/prod/resources/env.properties)
  * - * JSR352-compliant batch
      * Nablarch batch
      * Web for container
      * RESTful web service for container
      * Nablarch batch for container
    - No

Immediately after creating a project from an archetype, the following applies to the "properties file of environments that create local connection pools".

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,6

  * - Project type
    - properties file of environments that create local connection pools
  * - * Web
      * RESTful web service
    - * Unit test environment (manual test) properties (src/env/dev/resources/env.properties)
  * - * JSR352-compliant batch
      * Nablarch batch
    - * Unit test environment (manual test) properties (src/env/dev/resources/env.properties)
      * Production environment properties(src/env/prod/resources/env.properties)
  * - * Web for container
      * RESTful web service for container
      * Nablarch batch for container
    - * src/main/resources/env.properties - :ref:`commentary <container_production_config>`

The configuration example for a properties file of the environment that creates local connection pools is shown below.

H2 configuration example (default)
----------------------------------------

.. code-block:: text

    nablarch.db.jdbcDriver=org.h2.Driver
    nablarch.db.url=jdbc:h2:./h2/db/SAMPLE
    nablarch.db.user=SAMPLE
    nablarch.db.password=SAMPLE
    nablarch.db.schema=PUBLIC


Oracle configuration example
--------------------------------

.. code-block:: text

    nablarch.db.jdbcDriver=oracle.jdbc.driver.OracleDriver
    # jdbc:oracle:thin: @Host name:port number:database SID
    nablarch.db.url=jdbc:oracle:thin:@localhost:1521/xe
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


PostgreSQL configuration example
------------------------------------

.. code-block:: text

    nablarch.db.jdbcDriver=org.postgresql.Driver
    # jdbc:postgresql://Host name:Port number/database name
    nablarch.db.url=jdbc:postgresql://localhost:5432/postgres
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


DB2 configuration example
-----------------------------

.. code-block:: text

    nablarch.db.jdbcDriver=com.ibm.db2.jcc.DB2Driver
    # jdbc:db2://Host name:Port number/database name
    nablarch.db.url=jdbc:db2://localhost:50000/SAMPLE
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


SQL Server configuration example
------------------------------------

.. code-block:: text

    nablarch.db.jdbcDriver=com.microsoft.sqlserver.jdbc.SQLServerDriver
    # jdbc:sqlserver://Host name:Port number;instanceName=Instance name
    nablarch.db.url=jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS
    nablarch.db.user=SAMPLE
    nablarch.db.password=SAMPLE
    nablarch.db.schema=SAMPLE


.. important::
  Depending on the DB, user names, passwords and schemas are case-sensitive.

  Should be configured even in the properties file as configured in the DB.

.. _container_production_config:

Production configuration of containers
----------------------------------------------

In projects for containers, do not switch the preferences by profile.
Instead, it uses the OS environment variable of the environment in which the application will run to override the configuration values declared in ``env.properties``.

Thus, the configuration in ``src/main/resources/env.properties`` is used in the environment where OS environment variables are not set.
When running in a production container environment, the OS environment variables must be used to properly override environment-dependent values such as ``nablarch.db.url``.

See :ref:`repository-overwrite_environment_configuration` for how to overwrite the configuration in OS environment variables.

See `The Twelve-Factor App's III. Configuration <https://12factor.net/ja/config>`_ (external site) for the reason why it switches settings by OS environment variables instead of profiles.

.. _customizeDB_pom_dependencies:

------------------------------------------------------
Modification of the pom.xml file
------------------------------------------------------

.. _customizeDBProfiles:

In the profiles element (for projects that acquire a connection from JNDI in the production environment)
--------------------------------------------------------------------------------------------------------------

Modify the location where the dependency of the JDBC driver is described in the profiles element.


.. tip::

  In the case of a project that acquires a connection from JNDI in a production environment, since the connection has to be explicitly included in the dependency only when creating a local connection pool, it is described in the profiles element.

  (When acquiring a connection from JNDI, it should be possible to acquire the JDBC driver from the class loader of AP server.)


Hereinafter, configuration examples will be described for each type of database.

H2 configuration example (default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- Omitted -->
    <profile>
      <!-- Omitted -->
      <dependencies>
        <!-- Omitted -->
        <dependency>
          <groupId>com.h2database</groupId>
          <artifactId>h2</artifactId>
          <version>1.4.191</version>
          <scope>runtime</scope>
        </dependency>
        <!-- Omitted -->
      </dependencies>
    </profile>


Oracle configuration example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- Omitted -->
    <profile>
      <!-- Omitted -->
      <dependencies>
        <!-- Omitted -->
        <dependency>
          <groupId>com.oracle</groupId>
          <artifactId>ojdbc6</artifactId>
          <version>11.2.0.4.0</version>
          <scope>runtime</scope>
        </dependency>
        <!-- Omitted -->
      </dependencies>
    </profile>


PostgreSQL configuration example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- Omitted -->
    <profile>
      <!-- Omitted -->
      <dependencies>
        <!-- Omitted -->
        <dependency>
          <groupId>org.postgresql</groupId>
          <artifactId>postgresql</artifactId>
          <version>9.4.1207</version>
          <scope>runtime</scope>
        </dependency>
        <!-- Omitted -->
      </dependencies>
    </profile>


DB2 configuration example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- Omitted -->
    <profile>
      <!-- Omitted -->
      <dependencies>
        <!-- Omitted -->
        <dependency>
          <groupId>com.ibm</groupId>
          <artifactId>db2jcc4</artifactId>
          <version>10.5.0.7</version>
          <scope>runtime</scope>
        </dependency>
        <!-- Omitted -->
      </dependencies>
    </profile>


SQLServer configuration example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- Omitted -->
    <profile>
      <!-- Omitted -->
      <dependencies>
        <!-- Omitted -->
        <dependency>
          <groupId>com.microsoft.sqlserver</groupId>
          <artifactId>mssql-jdbc</artifactId>
          <version>7.4.1.jre8</version>
          <scope>runtime</scope>
        </dependency>
        <!-- Omitted -->
      </dependencies>
    </profile>


.. _customizeDBDependencyManagement:


In the dependencies element (for projects that create a local connection pool in the production environment)
---------------------------------------------------------------------------------------------------------------------------

Modify the location where the dependency of the JDBC driver is described in the dependencies element.

An example of the dependency element described by default is shown.


.. code-block:: xml

  <dependencies>
    <!-- TODO: プロジェクトで使用するDB製品にあわせたJDBCドライバに修正してください。(Modify the JDBC driver according to the DB product used in the project.) -->
    <!-- Omitted -->
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <version>1.4.191</version>
      <scope>runtime</scope>
    </dependency>
    <!-- Omitted -->
  </dependencies>

For each element in the dependency element, enter the same description as :ref:`customizeDBProfiles`.


.. _customizeDBWebComponentConfiguration:

---------------------------------------------------------------------------------------------------------------------------------------------------
(for projects that acquire a connection from JNDI in the production environment) component configuration file (src/main/resources/)
---------------------------------------------------------------------------------------------------------------------------------------------------

In the case of a project that fetches a connection from JNDI in a production environment,
the dialect class of the database that is used by the project, is defined in the component configuration file located in src/main/resources.
The component configuration file name of each project is as follows.

.. list-table::
   :widths: 10 10
   :header-rows: 1

   * - Project type
     - Component configuration file name
   * - Web
     - web-component-configuration.xml
   * - RESTful web service
     - rest-component-configuration.xml

Change the following configuration in the above file.

.. code-block:: xml

    <!-- ダイアレクト設定(Dialect configuration.) -->
    <!-- TODO:使用するDBに合わせてダイアレクトを設定すること(Configure dialect according to the DB to be used.) -->
    <component name="dialect" class="nablarch.core.db.dialect.H2Dialect" />


The following dialect classes are available in Nablarch. Modify the dialect class corresponding to the database to be used.

.. list-table::
   :widths: 10 10
   :header-rows: 1

   * - Database
     - Dialect class
   * - Oracle
     - nablarch.core.db.dialect.OracleDialect
   * - PostgreSQL
     - nablarch.core.db.dialect.PostgreSQLDialect
   * - DB2
     - nablarch.core.db.dialect.DB2Dialect
   * - SQL Server
     - nablarch.core.db.dialect.SqlServerDialect



-----------------------------------------------------------------------------------------------------------------------------------
(for projects that create a local connection pool in the production environment) data-source.xml (src/main/resources/)
-----------------------------------------------------------------------------------------------------------------------------------

In the case of a project that creates a local connection pool in the production environment, the dialect class of the database used by the project is described in data-source.xml.

Modify this dialect class to the one that corresponds to the database to be used.

The Dialect class to be used is the same as :ref:`customizeDBWebComponentConfiguration`.


-------------------------------------------
unit-test.xml  (src/test/resources)
-------------------------------------------

Describes the database configuration used by the testing framework.

The default is a general-purpose DB configuration as shown below.

When using Oracle, modify the description.

.. code-block:: xml

  <!-- TODO: 使用するDBに合せて設定してください。(configure it for project DB.) -->
  <!-- Oracle用の設定(Configuration for Oracle) -->
  <!--
    <import file="nablarch/test/test-db-info-oracle.xml"/>
  -->
  <!-- General purpose DB configuration -->
  <component name="dbInfo" class="nablarch.test.core.db.GenericJdbcDbInfo">
    <property name="dataSource" ref="dataSource"/>
    <property name="schema" value="${nablarch.db.schema}"/>
  </component>

Create tables and populate data used by Nablarch
=========================================================

----------------------------
Create table
----------------------------

DDL is prepared for each RDBMS in the following directory of each project.
By executing this DDL, tables used by Nablarch can be created.

* db/ddl/


.. tip::

  In the case of DB2, since the connected database and schema to be used are described at the top of create.sql, edit this information before executing DDL.

  To execute DDL, execute the following in the "DB2 Command Window".

  .. code-block:: text

    db2 -tvf "C:\develop\myapp-web\db\ddl\db2\create.sql"


.. tip::

    When using gsp-dba-maven-plugin \ [#gsp]_\, create a table by executing gsp-dba-maven-plugin with the following command.

    .. code-block:: bash

      mvn -P gsp clean generate-resources


.. [#gsp]

  Separate configuration is required to use gsp-dba-maven-plugin.

  See :doc:`addin_gsp` for configuration.


----------------------------
Data input
----------------------------

Insert statements of data are available in the following directory of each project.
By executing the insert statement, data that is used by Nablarch can be inserted.

* db/data/

.. tip::

  In the case of DB2, describe the connected database and schema used at the top of data.sql and then execute the SQL.

  A description example of the connected database and schema used is shown below.

  .. code-block:: text

    CONNECT TO SAMPLE2;
    SET SCHEMA sample;

  To execute DDL, execute the following in the "DB2 Command Window".

  .. code-block:: text

    db2 -tvf "C:\develop\myapp-web\db\data\data.sql"


Communication confirmation
==========================================

Refer to the following procedure and confirm communications.

* :ref:`Communication confirmation of Web<firstStepWebStartupTest>`
* :ref:`Communication confirmation of RESTful Web service<firstStepWebServiceStartupTest>`
* :ref:`Communication confirmation of JSR352-compliant batch<firstStepBatchEEStartupTest>`
* :ref:`Communication confirmation of Nablarch batch<firstStepBatchStartupTest>`
* :ref:`Communication confirmation of Web for container<firstStepContainerWebStartupTest>`
* :ref:`Communication confirmation of RESTful Web service for container<firstStepContainerWebServiceStartupTest>`
* :ref:`Communication confirmation of Nablarch batch for container<firstStepContainerBatchStartupTest>`

.. |br| raw:: html

  <br />
