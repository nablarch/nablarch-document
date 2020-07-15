Nablarch SQL Executor
=====================

.. contents:: Table of Contents
  :depth: 2
  :local:

Nablarch SQL Executor is a tool for interactively executing SQL files containing Nablarch special syntax.

Prerequisites
----------------

Prerequisites are shown below.

* Firefox or Chrome must be installed.
* Nablarch development environment must be set up.
* When using an RDBMS that does not have a JDBC driver in Maven Central Repository, a JDBC driver must be registered in Project Local Repository or Local Repository. 
  For more information on the registration method, see :ref:`customizeDBAddFileMavenRepo`.
 
Limitations
-------------
This tool has the following limitations: 
Therefore, if you want to run these SQL, instead of this tool use the SQL execution environment attached to the database to be used.

* Conditions cannot be set for the in clause
* SQL that starts with a with clause cannot be executed

.. tip::

  Nablarch provides an :ref:`adapter <doma_adaptor>` for `Doma (external site) <http://doma.readthedocs.io/ja/stable/>`_  that can describe SQL as 2-way SQL.
  
  When using Doma, the SQL defined for the production environment can be easily test executed without setting up complicated tools such as this one. 
  (Even when constructing a dynamic condition, it can be executed without rewriting SQL)
  
  For this reason, it is recommended to consider the use of Doma.

How to install
----------------

Clone the repository published on the following site.

https://github.com/nablarch/sql-executor (external site)


DB configuration change
------------------------------

Change the settings according to the RDBMS being used.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Change the basic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modification of src/main/resources/db.config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modify the src/main/resources/db.config if you want to change the connection URL, user, or password.

A configuration example is shown below.


**H2 configuration example (default)**

.. code-block:: text

  db.url=jdbc:h2:./h2/db/SAMPLE
  db.user=SAMPLE
  db.password=SAMPLE


**Oracle configuration example**

.. code-block:: text

  # jdbc:oracle:thin:@Host name: port number: database SID
  db.url=jdbc:oracle:thin:@localhost:1521/xe
  db.user=sample
  db.password=sample


**PostgreSQL configuration example**

.. code-block:: text

  # jdbc:postgresql://Host name: Port number/database name
  db.url=jdbc:postgresql://localhost:5432/postgres
  db.user=sample
  db.password=sample


**DB2 configuration example**

.. code-block:: text

  # jdbc:db2://Host name: Port number/database name
  db.url=jdbc:db2://localhost:50000/SAMPLE
  db.user=sample
  db.password=sample


**SQL Server configuration example**

.. code-block:: text

  # jdbc:sqlserver://Host name: Port number;instanceName= Instance name
  db.url=jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS
  db.user=SAMPLE
  db.password=SAMPLE


~~~~~~~~~~~~~~~~~~~~~~~~
Change the JDBC driver
~~~~~~~~~~~~~~~~~~~~~~~~

To change the JDBC driver, modify the following file:


pom.xml
~~~~~~~~~~~~~~~~~~~~~~~~~

"Please update the dependency of the following JDBC driver according to the RDBMS to be used (使用するRDBMSにあわせて、下記JDBCドライバの dependency を更新してください。)" in pom.xml. Correct where there is a comment.

Hereinafter, configuration examples will be described for each type of database.

**H2 configuration example (default)**

.. code-block:: xml

    <dependencies>
      <!-- Middle is omitted -->

      <!--使用するRDBMSにあわせて、下記JDBCドライバの dependency を更新してください。 -->
      <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <version>1.3.176</version>
        <scope>runtime</scope>
      </dependency>
    </dependencies>


**Oracle configuration example**

.. code-block:: xml

    <dependencies>
      <!-- Middle is omitted -->

      <!--使用するRDBMSにあわせて、下記JDBCドライバの dependency を更新してください。 -->
      <dependency>
        <groupId>com.oracle</groupId>
        <artifactId>ojdbc6</artifactId>
        <version>11.2.0.2.0</version>
        <scope>runtime</scope>
      </dependency>
    </dependencies>


**PostgreSQL configuration example**

.. code-block:: xml

    <dependencies>
      <!-- Middle is omitted -->

      <!--使用するRDBMSにあわせて、下記JDBCドライバの dependency を更新してください。 -->
      <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>9.4.1207</version>
        <scope>runtime</scope>
      </dependency>
    </dependencies>


**DB2 configuration example**

.. code-block:: xml

    <dependencies>
      <!-- Middle is omitted -->

      <!--使用するRDBMSにあわせて、下記JDBCドライバの dependency を更新してください。 -->
      <dependency>
        <groupId>com.ibm</groupId>
        <artifactId>db2jcc4</artifactId>
        <version>10.5.0.7</version>
        <scope>runtime</scope>
      </dependency>
    </dependencies>


src/main/resources/db.xml
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Correct the class name of the JDBC driver and the class name of the dialect. 
Set the driver class name in driverClassName property of dataSource component.

The relevant parts are shown below.

.. code-block:: xml

  <!-- データソース設定 -->
  <component name="dataSource" class="org.apache.commons.dbcp.BasicDataSource">
    <!-- JDBC driver class name設定 -->
    <!-- TODO: Database接続情報を変更する場合、ここを修正します -->
    <property name="driverClassName"
              value="org.h2.Driver" />
    <!-- Middle is omitted -->
  </component>

  <!-- Database接続用設定 -->
  <component name="connectionFactory"
      class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
    <!-- Middle is omitted -->
    <property name="dialect">
      <!-- Dialect class name設定 -->
      <!-- TODO: Databaseを変更する場合、ここを修正します。-->
      <component class="nablarch.core.db.dialect.H2Dialect"/>
    </property>
  </component>


An example of the configuration value is shown below.

.. list-table::
   :widths: 5 8 10
   :header-rows: 1

   * - Database
     - JDBC driver class name
     - Dialect class name
   * - H2
     - org.h2.Driver
     - nablarch.core.db.dialect.H2Dialect
   * - Oracle
     - oracle.jdbc.driver.OracleDriver
     - nablarch.core.db.dialect.OracleDialect
   * - PostgreSQL
     - org.postgresql.Driver
     - nablarch.core.db.dialect.PostgreSQLDialect
   * - DB2
     - com.ibm.db2.jcc.DB2Driver
     - nablarch.core.db.dialect.DB2Dialect
   * - SQL Server
     - com.microsoft.sqlserver.jdbc. |br| SQLServerDriver
     - nablarch.core.db.dialect.SqlServerDialect


How to launch
------------------

**For Unix systems**

Execute the following command.

.. code-block:: text

  mvn compile exec:java


Then launch the browser and display http://localhost:7979/index.html.


**For Windows**

Execute the batch file located directly under the directory. 
Double-click the file or start it from the command prompt.

.. code-block:: bat

  nse-web.bat


When the command is executed, the browser starts automatically.

.. tip::

  * The browser may time out if it takes longer to start, for example when starting for the first time. 
    In such a case, reload the browser after startup is complete.
  * This tool does not work properly on Internet Explorer. If Internet Explorer starts, copy the URL and paste it in the address field of Firefox or Chrome.


How to operate
----------------

The first time it is launched, the list of SQL files under the current directory will be displayed, 
but if it does not exist, the following screen is displayed.

.. figure:: ./_images/initial_screen.png
   :alt: Initial screen

   Initial screen

Specify the path to the local folder in the lower right input column and click **[Search again (再検索)]** as shown below to display the list of SQL files and the statements described in each file under that search.


.. figure:: ./_images/setting_search_root_path.png
   :alt: Search path configuration

   Search path configuration

Click each statement name to display its contents and operation buttons.

.. figure:: ./_images/browsing_sql_scripts.png
   :alt: SQL statement list

   SQL statement list

The embedded variable in the statement is an input field, 
and the statement can be executed by editing the contents and clicking on **[Run]**.

Click **[Fill]** to restore the contents of the input field from the previous execution.

.. figure:: ./_images/running_sql_scripts.png
   :alt: SQL execution result (Query)

   SQL execution result (Query)

.. figure:: ./_images/running_dml_scripts.png
   :alt: SQL execution result (DML)

   SQL execution result (DML)

Associated files
-----------------

The following log files are output during execution:

* sql.log → Runtime log of SQL statements
* app.log → All execution logs

FAQ
---

**Q1** :How to set the value of the DATE/DATETIME/TIMESTAMP field?

**A1** :Use the same format as DATE/DATETIME literals of SQL92. 
An example is shown below.

::

  12/11/1970


::

  12/11/1970 12:01:20

The current time is set by specifying the keyword ``SYSDATE``.

--------------

**Q2** :What is the solution if the program terminates abnormally without any output even after execution?

**A2** :Some errors, such as DB connection errors during launch, are output to the execution log file instead of standard error output. 
Since the execution log is output directly as ``app.log`` under the current directory, check the contents and take appropriate action.

.. |br| raw:: html

  <br />
