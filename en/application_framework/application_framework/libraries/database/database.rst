.. _database:

Database Access (JDBC Wrapper)
=========================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides a function to execute the SQL statement for the database using JDBC.

.. tip::
  As described in :ref:`database_management` , the use of :ref:`universal_dao` is recommended for executing SQL.

  Since :ref:`universal_dao` internally uses the API of this function to access the database, the configuration to use this function is always required.

.. important::

  Since this function depends on JDBC 3.0, the JDBC driver used must implement JDBC 3.0 or higher.


Function overview
----------------------

.. _database-dialect:

Can be used without sensing the database dialect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By configuring :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` corresponding to the database product used, the application can be implemented without sensing the dialect.

:java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` provides the following functions:

* A method that returns whether the identity column can be used (:java:extdoc:`supportsIdentity <nablarch.core.db.dialect.Dialect.supportsIdentity()>` )
* A method that returns whether batch insert can be performed on a table that has an identity (automatic numbered) column (:java:extdoc:`supportsIdentityWithBatchInsert <nablarch.core.db.dialect.Dialect.supportsIdentityWithBatchInsert()>`)
* A method that returns whether the sequence object can be used (:java:extdoc:`supportsSequence <nablarch.core.db.dialect.Dialect.supportsSequence()>` )
* A method that returns whether offset (or a function equivalent to offset) can be used in the specified range of search query (:java:extdoc:`supportsOffset <nablarch.core.db.dialect.Dialect.supportsOffset()>` )
* A method to determine whether :java:extdoc:`SQLException <java.sql.SQLException>` that indicates a unique constraint violation has occurred (:java:extdoc:`isDuplicateException <nablarch.core.db.dialect.Dialect.isDuplicateException(java.sql.SQLException)>` )
* A method to determine whether :java:extdoc:`SQLException <java.sql.SQLException>` of transaction timeout target has occurred (:java:extdoc:`isTransactionTimeoutError <nablarch.core.db.dialect.Dialect.isTransactionTimeoutError(java.sql.SQLException)>` )
* A method for generating SQL statement to acquire the next value from the sequence object (:java:extdoc:`buildSequenceGeneratorSql <nablarch.core.db.dialect.Dialect.buildSequenceGeneratorSql(java.lang.String)>` )
* A method that returns :java:extdoc:`ResultSetConvertor <nablarch.core.db.statement.ResultSetConvertor>` , which acquires value from :java:extdoc:`ResultSet <java.sql.ResultSet>` (:java:extdoc:`getResultSetConvertor <nablarch.core.db.dialect.Dialect.getResultSetConvertor()>` )
* A method to convert search query to range specification (for paging) SQL (:java:extdoc:`convertPaginationSql <nablarch.core.db.dialect.Dialect.convertPaginationSql(java.lang.String-nablarch.core.db.statement.SelectOption)>` )
* A method for converting search query to the number acquisition SQL (:java:extdoc:`convertCountSql <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String)>` )
* A method that returns SQL to check if :java:extdoc:`Connection <java.sql.Connection>` is connected to the database (:java:extdoc:`getPingSql <nablarch.core.db.dialect.Dialect.getPingSql()>` )

See :ref:`database-use_dialect` for how to configure :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` .

.. _database-sql_file:

Write SQL in SQL file, not logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQL is defined in the SQL file and not in the principle logic.

SQL is not required to be assembled by logic by describing in the SQL file, and since `PreparedStatement` is always used, the vulnerability of SQL injection can be eliminated.

.. tip::

  If defining in the SQL file is not possible, use the provided API, which specifies and executes the SQL directly.
  However, be careful, there is a possibility that SQL injection vulnerability may be embedded.
  It is also assumed testing and review guarantees that there is no SQL injection vulnerability.


For details, see :ref:`database-use_sql_file` .

.. _database-bean:

Bean property values can be embedded in SQL bind variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function to automatically bind the value configured in Bean property to IN parameter of :java:extdoc:`java.sql.PreparedStatement` .

By using this function, it is not necessary to call the method for configuring the value of :java:extdoc:`java.sql.PreparedStatement` multiple times, and it is not necessary to modify the index when the number of IN parameters increases or decreases.

For details, see :ref:`database-input_bean` .

like search can be easily implemented
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function to automatically insert an escape clause and escape processing of wildcard characters in like search.

For details, see :ref:`database-like_condition` .

.. _database-variable_condition:

SQL statements can be dynamically constructed based on the state of the Bean object during execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function to dynamically assemble the SQL statement to be executed based on the state of the Bean object.

For example, dynamic construction of conditions and IN clauses can be performed.

See below for details.

* :ref:`database-use_variable_condition`
* :ref:`database-in_condition`
* :ref:`database-make_order_by`

SQL query results can be cached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function to return search results from the cache without accessing the database when the executed SQL and conditions acquired from an external source (value configured in the bind variable) are equivalent.

For details, see :ref:`database-use_cache` .

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _database-connect:

Connection configuration for the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The connection configuration for the database can be selected from the following two types.

* Creating a database connection using :java:extdoc:`javax.sql.DataSource`
* Creating a database connection using a data source registered on an application server.

To use a connection method other than the above (for example, to use the OSS connection pooling library), refer to :ref:`database-add_connection_factory` and add an implementation that connects to the database.

Connection configuration example
  Generate database connection using :java:extdoc:`javax.sql.DataSource`
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
        <!-- See Javadoc for details of the configuration values -->
      </component>

  Generating a database connection from an application server data source
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForJndi">
        <!-- See Javadoc for details of the configuration values -->
      </component>

  Refer to Javadoc of each class for the configuration values of :java:extdoc:`BasicDbConnectionFactoryForDataSource<nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource>` and :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` .

.. tip::

  Basically, the class configured above is not used directly. If database access is required, use :ref:`database_connection_management_handler` .

  When using a database, transaction management is also required. For transaction management, see :ref:`transaction` .

.. _database-use_dialect:

Use dialects for database products
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The dialect function is enabled by configuring the dialect corresponding to the database product in the component configuration file.

.. tip::
  If it is not configured, :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` is used. In principle, all functions of :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` are disabled, be sure to configure the dialect corresponding to the database product.

  If a dialect that corresponds to the database product is not available, or to use the new functions of the new version, create a new dialect by referring to :ref:`database-add_dialect` .


Component configuration example
  This is a configuration example for the component that acquires the database connection from :java:extdoc:`javax.sql.DataSource` . Even in the case of :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` , configure dialect to the :java:extdoc:`dialect <nablarch.core.db.connection.ConnectionFactorySupport.setDialect(nablarch.core.db.dialect.Dialect)>` property as shown in the following example.

  .. code-block:: xml

    <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
      <!-- Properties that are not related to dialect are omitted -->

      <!--
      Dialect is configured in the dialect property.
      In this example, the dialect for the Oracle database has been configured.
      -->
      <property name="dialect">
        <component class="nablarch.core.db.dialect.OracleDialect" />
      </property>
    </component>


.. _database-use_sql_file:

Manage SQL in files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In this function, SQL is managed in the SQL file as described in :ref:`database-sql_file` . To handle SQL files, it is necessary to configure the component configuration file. For details, see :ref:`Configuration for loading SQL from SQL files <database-load_sql>` .

Create an SQL file according to the following rules.

* Create the SQL under the class path.
* Multiple SQL statements can be described in one SQL file, but SQLID must be unique within the file.
* Insert a blank line between SQLIDs. (Lines with spaces are not considered blank lines)
* Insert ``=`` between SQLID and SQL.
* Describe comments with ``--`` . (Block comments are not supported)
* SQL may be formatted using line breaks and spaces (tabs).


.. important::

  Make sure to create separate SQLs for each function without using same SQL for multiple functions.

  If an SQL is used in multiple functions, unexpected bugs may occur due to unintended usage or changes in SQL. For example, when ``for update`` of exclusive lock is added to the SQL statement used in multiple functions, lock is acquired by a function that does not require exclusive lock causing processing delay.

An example of a SQL file is shown below.

.. code-block:: sql

  -- ＸＸＸＸＸ acquisition SQL
  -- SQL_ID:GET_XXXX_INFO
  GET_XXXX_INFO =
  select
     col1,
     col2
  from
     test_table
  where
     col1 = :col1


  -- ＸＸＸＸＸ update SQL
  -- SQL_ID:UPDATE_XXXX
  update_xxxx =
  update
      test_table
  set
      col2 = :col2
  where
      col1 = :col1

.. _database-load_sql:

Configuration for loading SQL from SQL files
  This section describes the configuration required to load SQL from an SQL file.

  To load SQL, configure :java:extdoc:`BasicSqlLoader <nablarch.core.db.statement.BasicSqlLoader>` in :java:extdoc:`BasicStatementFactory#sqlLoader <nablarch.core.db.statement.BasicStatementFactory.setSqlLoader(nablarch.core.cache.StaticDataLoader)>` .

  In this example, file encoding and extension are configured. When the configuration is omitted, the following values are used.

  :File encoding: utf-8
  :Extension: sql

  The component :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` defined here must be configured in the component that acquires the database connection defined in :ref:`database-connect` .

  Configuration example
    .. code-block:: xml

      <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
        <property name="sqlLoader">
          <component class="nablarch.core.db.statement.BasicSqlLoader">
            <property name="fileEncoding" value="utf-8"/>
            <property name="extension" value="sql"/>
          </component>
        </property>
      </component>

.. _database-execute_sqlid:

Execute SQL by specifying SQLID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To execute SQL based on SQLID, use the database connection obtained from :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` . A database connection has to be registered in :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` using :ref:`database_connection_management_handler` .

The mapping rules between the SQLID and the executed SQL are as follows.

* Up to ``#`` of SQLID is the SQL file name.
* After ``#`` of SQLID is the SQLID in the SQL file


Implementation examples
  In this example, since ``jp.co.tis.sample.action.SampleAction#findUser`` is specified in SQLID, the SQL file is ``jp.co.tis.sample.action.SampleAction.sql`` below the class path. SQLID in the SQL file is ``findUser`` .

  * See Javadoc for how to use :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` and :java:extdoc:`SqlPStatement <nablarch.core.db.statement.SqlPStatement>` .

  .. code-block:: java

    // Get database connection from DbConnectionContext.
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate the statement based on SQLID.
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser");

    // Configure the condition.
    statement.setLong(1, userId);

    // Execute the search process.
    SqlResultSet result = statement.retrieve();

Execute a stored procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Even when executing a stored procedure, basically implement it in the same way as executing a SQL.

.. important::

  :ref:`database-bean` is not supported in the execution of stored procedure. The logic will be scattered between Java and stored procedures and maintainability will be significantly reduced if stored procedures are used. Therefore stored procedures should not be used in principle.

  However, since it is assumed that sometimes stored procedures must be used for existing assets, this function provides a very basic API for executing the stored procedure.

An example is shown below.

* For details on how to use :java:extdoc:`SqlCStatement <nablarch.core.db.statement.SqlCStatement>` , refer to the Javadoc.

.. code-block:: java

  // Generate an execution statement for the stored procedure based on SQLID.
  SqlCStatement statement = connection.prepareCallBySqlId(
      "jp.co.tis.sample.action.SampleAction#execute_sp");

  // Configure the IN and OUT parameters.
  statement.registerOutParameter(1, Types.CHAR);

  // Execute.
  statement.execute();

  // Acquire OUT parameter.
  String result = statement.getString(1);

.. _database-paging:

Execute the SQL by specifying the search scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A specific range of results may be displayed by using a paging function on the search result list screen of a web system. This function provides a function that can specify the range of search results for such applications.

Implementation examples
  When generating a statement from a database connection( `connection` ), specify the search target range. In this example, since the following values are specified, up to 10 records are fetched from the 11th record.

  :Start position: 11
  :Number of records fetched: 10

  .. code-block:: java

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate the statement object by specifying the SQLID and search range.
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser", new SelectOption(11, 10));

    // Execute the search process
    SqlResultSet result = statement.retrieve();

.. tip::
  When the search range is specified, rewrite the search SQL with the SQL specifying the acquisition range and then execute. SQL for specifying the acquisition range is performed by :ref:`dialect <database-dialect>` .

.. _database-input_bean:

Execute SQL with Bean object as input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As described in :ref:`database-bean` , SQL can be executed using the Bean object as an input.

When executing SQL using the Bean object as an input, use a named bind variable for the IN parameter of SQL. In the named parameter, describe the property name of Bean that is received as input after ``:`` .

.. important::

  Note that if the IN parameter is described in JDBC standard ``?`` , execution of the SQL with Bean object as an input will not work.

An implementation example is shown below.

SQL example
  Use named parameters for IN parameters.

  .. code-block:: sql

    insert into user
      (
      id,
      name
      ) values (
      :id,
      :userName
      )

Implementation examples
  Set the required value in the Bean object and call the function to execute SQL using the Bean object as an input.

  * See Javadoc for how to use :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` and :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` .
  * For the relationship between SQLID and the executed SQL, see :ref:`database-execute_sqlid` .

  .. code-block:: java

    // Create a bean and configure a value for the property
    UserEntity entity = new UserEntity();
    entity.setId(1);              // Configure a value to id property
    entity.setUserName("Name"); // Configure a value to userName property

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // Configure the value of bean property to bind variable and execute the SQL
    // Value of id property of bean is configured in :id of the SQL.
    // Value of userName property of bean is configured in :userName of SQL.
    int result = statement.executeUpdateByObject(entity);

.. tip::

  An implementation class of :java:extdoc:`java.util.Map` can be specified instead of Bean. When Map is specified, Map value is configured for IN parameter that matches the key value of Map.

  When Bean is specified, processed after conversion to Map using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` . If a type not supported by :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` is present in the Bean property, the property cannot be used with this function.
  
  To increase the types that can be copied to Map with :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` , prepare referring to :ref:`utility-conversion` .

.. tip::

  Access method to Bean can be changed from property to field. For changing to field access method, add the following configuration to the properties file.

  .. code-block:: properties

     nablarch.dbAccess.isFieldAccess=true

  Field access is not recommended for the following reasons.

  In other functions of this framework (for example, :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`), the method of acquiring values from Bean is unified by property access. If only the database function is changed to field access, the programmer needs to be aware of both field access and property access, which may decrease productivity and cause bugs.


Convert type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Database access (JDBC wrapper) delegates the type conversion of variables used for input to/output from the database to the JDBC driver. Therefore, it is necessary to define the types of variables used for input and output according to the database type and specifications of the JDBC driver that is used.

If an arbitrary type conversion is necessary, the application performs type conversion on the variables used for input to/output from the database.

- When using Bean for input, perform type conversion when setting the value to Bean property. when using a Bean for output, perform type conversion after extracting the value from the property.
- When using Map for input, type conversion is performed when setting the value in Map. When using Map for output, perform type conversion after extracting the value.
- When configuring a bind variable by specifying an index, convert the object to be configured to the bind variable to an appropriate type. When acquiring a value from :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` , perform type conversion after the value has been acquired.


.. _database-common_bean:

Automatically configure a common value when executing SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function to automatically configure the value to be configured each time when registering or updating data, immediately before executing the SQL. For example, this function can be used for items such as registration date and time and update date and time.

This function is enabled only when :ref:`database-input_bean` is used to automatically configure the value based on the annotation configured in the property.

A usage example is shown below.

Component configuration file
  To use this function, configure a class that performs automatic value configuration in the component configuration file.

  As shown in the following example. configure :java:extdoc:`AutoPropertyHandler <nablarch.core.db.statement.AutoPropertyHandler>` implementation class in a list with respect to :java:extdoc:`BasicStatementFactory#updatePreHookObjectHandlerList <nablarch.core.db.statement.BasicStatementFactory.setUpdatePreHookObjectHandlerList(java.util.List)>` . The implementation class provided as standard is placed under the :java:extdoc:`nablarch.core.db.statement.autoproperty` package.

  The component :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` defined here should be configured in the component that acquires the database connection defined in :ref:`database-connect` .

  .. code-block:: xml

    <component name="statementFactory"
        class="nablarch.core.db.statement.BasicStatementFactory">

      <property name="updatePreHookObjectHandlerList">
        <list>
          <!-- Configure the implementation class nablarch.core.db.statement.AutoPropertyHandler in a list-->
        </list>
      </property>
    </component>

Bean object (Entity)
  Configure the annotation to the property for which the value has to be configured automatically. The annotation provided as standard is placed under the :java:extdoc:`nablarch.core.db.statement.autoproperty` package.

  .. code-block:: java

    public class UserEntity {
      // User ID
      private String id;

      // Registration date and time
      // Automatically configured when registering
      @CurrentDateTime
      private Timestamp createdAt;

      // Update date and time
      // Automatically configured during registration/update
      @CurrentDateTime
      private String updatedAt;

      // Access method, etc. are omitted
    }

SQL
  SQL is created in the same way as :ref:`database-input_bean` .

  .. code-block:: sql

    insert into user (
      id,
      createdAt,
      updatedAt
    ) values (
      :id,
      :createdAt,
      :updatedAt
    )

Implementation examples
  Implementation is the same as :ref:`database-input_bean` . For items whose values are automatically configured, there is no need to configure values for Beans with logic. Even if the value is explicitly configured, it is overwritten by the automatic value configuration function immediately before the SQL is executed.

  .. code-block:: java

    // Create a bean and configure a value for the property
    // Values are not required to be configured for createdAt and updatedAt which are automatically configured
    UserEntity entity = new UserEntity();
    entity.setId(1);

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // Call without configuring the value for the automatically configured items.
    // The database function automatically configures the values.
    int result = statement.executeUpdateByObject(entity);

.. _database-like_condition:

Perform a like search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Like search uses :ref:`database-input_bean` , and conditions for like search are described in the SQL according to the following rules.

In the case of prefix match
  Enter ``%`` at the end of the named parameter.

  Example: ``name like :userName%``

In the case of suffix match
  Enter ``%`` at the beginning of the named parameter.

  Example:  ``name like :%userName``

In the case of middle match
  Enter ``%`` before and after the named parameter.

  Example: ``name like :%userName%``

See :ref:`database-def_escape_char` for the definition of escape character and escape target character.

An implementation example is shown below.

SQL
  Define SQL according to the above rules.

  .. code-block:: sql

    select *
      from user
     where name like :userName%

Implementation examples
  Just by executing the SQL in the same way as :ref:`database-input_bean` , value rewriting and escape processing are performed for like conditions. In this case, the actual condition is ``name like 'Na%' escape'\'`` .

  * See Javadoc for how to use :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` and :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` .
  * For the relationship between SQLID and the executed SQL, see :ref:`database-execute_sqlid`

  .. code-block:: java

    // Create a bean and configure a value for the property
    UserEntity entity = new UserEntity();
    entity.setUserName("Na"); // Configure a value to userName property

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUserByName");

    // Configure bean property value to bind variable and execute the SQL
    // In this example, name like 'Na%' is executed
    int result = statement.retrieve(bean);


.. _database-def_escape_char:

Define escape character and escape target characters during like search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Escape character and escape target characters are defined in the component configuration file. Since the escape character is automatically configured, it is not necessary to explicitly configure the escape characters.

When the configuration is omitted, the following values are used.

:Escape character: ``\``
:Escape target characters: ``%`` 、 ``_``

Component configuration example
  In this example, ``\`` is configured as the escape character, and 4 characters ``%`` , ``％`` , ``_`` , ``＿`` are configured as the escape target characters.

  The component :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` defined here should be configured in the component that acquires the database connection defined in :ref:`database-connect` .

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <!-- Escape character definition -->
      <property name="likeEscapeChar" value="\" />

      <!-- Escape target character definition (configured separated with commas) -->
      <property name="likeEscapeTargetCharList" value="%,％,_,＿" />
    </component>

.. _database-use_variable_condition:

Execute SQL with variable conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To execute SQL with variable conditions, use :ref:`database-input_bean` and describe the conditions using the following notation.

Description rules for variable conditions
  Variable condition is described with ``$if(property name){SQL statement condition}`` The condition is excluded by the value of Bean object corresponding to the property name after ``$if`` . Excluded conditions are as follows.

  * For an array or :java:extdoc:`java.util.Collection` , if the property value is null or size is 0
  * For types other than the above, the property value is null or empty string (in case of string object)

  The ``$if`` special syntax has the following restrictions.

  * Only the where clause can be used
  * ``$if`` cannot be used within ``$if``

  .. important::

    This function is used when the search conditions change depending on the input contents of the user, such as the search screen of a web application.
    It is not used to standardize multiple SQLs that differ only in conditions.
    If standardized, since the function may cause unexpected bugs when SQL is changed, be sure to define multiple SQL.


An example is shown below.

SQL
  For this SQL, ``user_name`` and ``user_kbn`` conditions are variables.

  .. code-block:: none

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userName) {user_name like :userName%}
      and $if (userKbn) {user_kbn in ('1', '2')}
      and birthday = :birthday

Implementation examples
  Since the value is set only for `userName` property, ``user_kbn`` defined in the variable condition is excluded from the condition during execution.

  .. code-block:: java

    // Create a bean and configure a value for the property
    UserEntity entity = new UserEntity();
    entity.setUserName("Name");

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    // Specify a Bean object with a condition in the second argument.
    // SQL variable conditions are assembled based on the state of this Bean object.
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser", entity);

    // SQL is executed by configuring the value of the entity property to the bind variable
    SqlResultSet result = statement.retrieve(entity);

.. _database-in_condition:

Executing SQL with variable number of conditions for in clause
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To execute SQL with condition count of the in clause as variable, use :ref:`database-input_bean` and describe the conditions using the following notation.

Description rules of in clause
  Add ``[]`` at the end of the named parameter of the condition. The property type of Bean object corresponding to the named parameter must be an array or :java:extdoc:`java.util.Collection` (including subtype) [#collection]_ .

  .. tip::

    If the property value, that is the condition of the IN clause, is null or size 0, be sure to define the corresponding condition as a variable condition. If the property value is null when the condition is not configured as a variable condition, since the condition will be ``xxxx in (null)`` , the search result may not be acquired correctly.

    \* In the in clause, since the conditional expression (in parentheses) cannot be empty, the conditional expression is specified as ``in (null)`` if an array of size 0 or null is specified.

An example is shown below.

SQL
  In this SQL, the in condition of ``user_kbn`` is dynamically constructed. Since it is used together with ``$if``, if the `userKbn` property is null or the size is 0, it is excluded from the condition.

  .. code-block:: none

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userKbn) {user_kbn in (:userKbn[])}

Execution example
  In this example, since two elements are configured in `userKbn` property, the condition of the executed SQL is ``userKbn in (?, ?)`` .

  Only records with `userKbn` ``1`` and ``3`` are acquired from the database.

  .. code-block:: java

    // Create a bean and configure a value for the property
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserKbn(Arrays.asList("1", "3"));

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    // Specify a Bean object with a condition in the second argument.
    // in clause of SQL is assembled based on the state of this Bean object.
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // SQL is executed by configuring the value of the condition property to the bind variable
    SqlResultSet result = statement.retrieve(condition);
    
.. [#collection] 
    As described in :ref:`database-input_bean` , use the property value after converting it to map with :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` . Therefore, note that if a property is declared with a type that is not supported by :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` , the condition cannot be configured in the in clause.

    For the method of adding the conversion target type with :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` , :ref:`utility-conversion-add-rule` .

.. _database-make_order_by:

Execute SQL by dynamically switching sort items of order by during runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To execute SQL with sort item of order by as variable, use :ref:`database-input_bean` and describe the conditions using the following notation.

Description rules of order by clause
  To make the sort item a variable, use ``$sort`` instead of order by clause and describe as follows.

  .. code-block:: text

     $sort (property name) {(case 1) (case 2) ・ ・ ・ (case n)}

     Property name: Property name that holds the sort ID of Bean object
     Case: Represents the switching candidate for the order by clause.
             Describe the sort ID that uniquely identifies the candidate and string specified in the order by clause (hereinafter referred to as the case body).
             Specify "default" as the sort ID for the default case when no match is found to any candidate.

  * Each case is represented by enclosing the sort ID and case body in single-byte parentheses.
  * Sort ID and case body are separated by a half-width space.
  * Half-width spaces cannot be used for the sort ID.
  * A half-width space can be used for the case body.
  * The first string that appears after the opening parentheses is the sort ID.
  * After the sort ID and before the closing parentheses is the case body.
  * The sort ID and case body are trimmed.


A usage example is shown below.

SQL
  .. code-block:: none

    select
      user_id,
      user_name
    from
      user
    where
      user_name = :userName
    $sort(sortId) {
      (user_id_asc  user_id asc)
      (user_id_desc user_id desc)
      (name_asc     user_name asc)
      (name_desc    user_name desc)
      (default      user_id)

Implementation examples
  In this example, since ``name_asc`` is configured in the sort ID, the order by clause becomes ``order by user_name asc`` .

  .. code-block:: java

    // Create a bean and configure a value for the property
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserName("Name");
    condition.setSortId("name_asc");      // Configure the sort ID

    // Acquire database connection from DbConnectionContext
    AppDbConnection connection = DbConnectionContext.getConnection();

    // Generate a statement based on SQLID
    // Specify a Bean object with a condition in the second argument.
    // order by clause of SQL is assembled based on the state of this Bean object.
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // SQL is executed by configuring the value of the condition property to the bind variable
    SqlResultSet result = statement.retrieve(condition);

.. _database-binary_column:

Accessing columns of binary type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section describes how to access binary type columns such as blob (binary type differs depending on the database product).

Obtain the value of binary type
  When acquiring a binary value, acquire the value as `byte[]` from :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` of the search result object.

  An example is shown below.

  .. code-block:: java

    SqlResultSet rows = statement.retrieve();

    SqlRow row = rows.get(0);

    // Acquire the value of the encrypted column in binary using getBytes
    byte[] encryptedPassword = row.getBytes("password");

  .. important::

    In the case of the above implementation example, all the contents of the column are deployed on the Java heap. Therefore, when data of a very large size is read, it squeezes the heap area, causing failures such as system down.

    Therefore, when reading a large amount of data, use the :java:extdoc:`Blob <java.sql.Blob>` object as shown below to avoid consuming a large amount of heap.

    .. code-block:: java

      SqlResultSet rows = select.retrieve();

      // Acquire the data as Blob
      Blob pdf = (Blob) rows.get(0).get("PDF");

      try (InputStream input = pdf.getBinaryStream()) {
        // Read the data sequentially from InputStream.
        // Note that if read all at once, everything will be loaded into the heap
      }

Register/update binary value
  To register/update a small binary value, use :java:extdoc:`SqlPStatement#setByte <nablarch.core.db.statement.SqlPStatement.setBytes(int-byte:A)>` .

  .. code-block:: java

    SqlPStatement statement = getSqlPStatement("UPDATE_PASSWORD");

    statement.setBytes(1, new byte[] {0x30, 0x31, 0x32});
    int updateCount = statement.executeUpdate();

 When registering and updating a large binary value, use :java:extdoc:`SqlPStatement#setBinaryStream <nablarch.core.db.statement.SqlPStatement.setBinaryStream(int-java.io.InputStream-int)>` , and send values directly to the database from  :java:extdoc:`InputStream <java.io.InputStream>` which represents a file, etc.

 .. code-block:: java

    final Path pdf = Paths.get("input.pdf");
    try (InputStream input = Files.newInputStream(pdf)) {
        statement.setBinaryStream(1, input, (int) Files.size(pdf));
    }


.. _database-clob_column:

Access columns of string type with a large number of digits (e.g. CLOB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section describes how to access a large string type column such as CLOB.

Acquire the value of CLOB type
  When acquiring CLOB type values, acquire the value as string type from :java:extdoc:`search result object <nablarch.core.db.statement.SqlRow>` .

  An example is shown below.

  .. code-block:: java

    SqlResultSet rows = statement.retrieve();
    SqlRow row = rows.get(0);

    // Acquire CLOB value as a string.
    String mailBody = row.getString("mailBody");

  .. important::

    In the case of the above implementation example, all the contents of the column are deployed on the Java heap. Therefore, when data of a very large size is read, it squeezes the heap area, causing failures such as system down.

    Therefore, when reading a large amount of data, use the :java:extdoc:`Clob <java.sql.Clob>` object as shown below to avoid consuming a large amount of heap.

    .. code-block:: java

      SqlResultSet rows = select.retrieve();

      // Acquire the data as Clob
      Clob mailBody = (Clob) rows.get(0).get("mailBody");

      try (Reader reader = mailBody.getCharacterStream()) {
        // Read data sequentially from the Reader.
        // If all the read data is held in the heap, note that the heap will be squeezed.
      }
    
Register (update) the value in CLOB type
  When registering and updating a value with a small size, configure a string type value using :java:extdoc:`SqlPStatement#setString <nablarch.core.db.statement.SqlPStatement.setString(int-java.lang.String)>` .

  An example is shown below.

  .. code-block:: java

    statement.setString(1, "Value");
    statement.executeUpdate();

  When registering or updating a large value, use :java:extdoc:`SqlPStatement#setCharacterStream <nablarch.core.db.statement.SqlPStatement.setCharacterStream(int-java.io.Reader-int)>` , and send values to the database through :java:extdoc:`Reader <java.io.Reader>` that represents a text file, etc.

  An example is shown below.

  .. code-block:: java

    Path path = Paths.get(filePath);
    try (Reader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
      // Register the Reader value using setCharacterStream.
      statement.setCharacterStream(1, reader, (int) Files.size(path));
    }


Exception types that occur when accessing the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exceptions when accessing the database access are broadly divided into the following four types.

Since these exceptions are all unchecked exceptions, there is no need to catch them with ``try-catch`` such as :java:extdoc:`SQLException <java.sql.SQLException>` .

Exception when there is a database access error
  The exception that occurs when accessing the database, and :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` is thrown.

Exception when there is a database connection error
  If the exception during database access indicates a database connection error, :java:extdoc:`DbConnectionException <nablarch.core.db.connection.exception.DbConnectionException>` is thrown. This exception is handled by the :ref:`retry_handler`. (If :ref:`retry_handler` is not applied, it is handled as a runtime exception.)

  :ref:`Dialect <database-dialect>` is used when determining a database connection error.

SQL execution exception
  Exception which occurs when SQL execution fails, and :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` is thrown.

Exception when the SQL execution is a violation of unique constraint
  If the exception during SQL execution is an exception indicating a unique constraint violation, :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` is thrown.

  To handle a unique constraint violation, refer :ref:`database-duplicated_error` .

  :ref:`Dialect <database-dialect>` is used to determine a unique constraint violation.

.. tip::

  Refer to :ref:`database-change_exception` to change the exception when a database access error occurs ( to divide the exception further).

.. _database-duplicated_error:

Process by handling unique constraint violation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If a process has to be performed when a unique constraint is violated, :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` is caught with ``try-catch`` and processed.

:ref:`Dialect <database-dialect>` is used to determine a unique constraint violation.

.. important::

  Note that depending on the database product, if an exception occurs during SQL execution, SQL will no longer be accepted until rollback is performed. In the case of such a product, consider whether it can be substituted by other means.

  For example, to perform the update process when a unique constraint violation occurs during the registration process, this problem can be avoided by using a merge statement instead of performing exception handling.

Processing of long-running transactions is aborted as errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implemented by transaction management. For details, see :ref:`transaction-timeout` .

.. _database-new_transaction:

Execute SQL in a transaction different from the current transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There may be cases database has to be accessed using an individual transaction instead of a transaction started by the database connection management handler and transaction control handler.

For example, to confirm changes to the database even when business processing fails, define a transaction different from the current transaction and access the database.

The following procedures are required to use individual transactions.

#. Configure :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` in the component configuration file.
#. Acquire :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` from the system repository and execute SQL in a new transaction. (Instead of acquiring from the system repository, :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` can be used)

A usage example is shown below.

Component configuration file
  Configure :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` in the component configuration file.

  * Configure implementation class :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` to :java:extdoc:`connectionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>` property.
    For details of implementation class :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>`, see :ref:`database-connect`.

  * Configure implementation class :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` to :java:extdoc:`transactionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>` property.
    For details of implementation :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` , see :ref:`transaction-database` .


  .. code-block:: xml

    <component name="update-login-failed-count-transaction" class="nablarch.core.db.transaction.SimpleDbTransactionManager">
      <!-- Configure ConnectionFactory implementation class in connectionFactory property -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- Configure TransactionFactory implementation class in transactionFactory property -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- Configure a name to identify the transaction -->
      <property name="dbTransactionName" value="update-login-failed-count-transaction" />

    </component>

Implementation examples
  Use :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` to execute SQL. In addition, instead of using :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` directly, use :java:extdoc:`SimpleDbTransactionExecutor<nablarch.core.db.transaction.SimpleDbTransactionExecutor>` to perform transaction control.

  .. code-block:: java

    // Acquire SimpleDbTransactionManager from the system repository
    SimpleDbTransactionManager dbTransactionManager =
        SystemRepository.get("update-login-failed-count-transaction");

    // Execute by specifying SimpleDbTransactionManager in the constructor
    SqlResultSet resultSet = new SimpleDbTransactionExecutor<SqlResultSet>(dbTransactionManager) {
      @Override
      public SqlResultSet execute(AppDbConnection connection) {
        SqlPStatement statement = connection.prepareStatementBySqlId(
            "jp.co.tis.sample.action.SampleAction#findUser");
        statement.setLong(1, userId);
        return statement.retrieve();
      }
    }.doTransaction();

.. _database-use_cache:

Cache search results (handle cached data for the same SQL under the same condition)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the update time is fixed or the data is accessed frequently but the latest data is not required to be returned, the search results can be cached to reduce the load on the database.

This function can be used effectively with the following functions.

* Data that is referenced in large quantities without the need for strict up-to-date results such as sales rankings
* Data that is updated only at night and not updated during the day

Constraints
  LOB type
    When LOB (BLOB type or CLOB type) column is acquired, LOB locator is acquired instead of acquiring the data stored in DB. To acquire the actual value, acquire the value through this LOB locator.

    The expiry interval of the LOB locator depends on the implementation of each RDBMS. Normally, the locator cannot be accessed when :java:extdoc:`java.sql.ResultSet` or :java:extdoc:`java.sql.Connection` is closed. For this reason, BLOB and CLOB types cannot be included in a cache that has a longer lifetime than `ResultSet` or `Connection` .

  Application redundancy
    The component maintaining the cache provided by default retains the cache in the JVM heap. For this reason, when applications have a redundant configuration, the search results are cached for each application.

    For this reason, since the cache timing is different, each application may hold a different cache.

    When application servers are redundant and a round-robin load balancer is used, a different server may be accessed each time. Note that if different caches are maintained for each server, different results may be displayed on the screen for each request.

.. important::

  This function is intended to reduce the system load by omitting database access in the reference system when it is possible and not to speed up the database access (SQL). For this reason, it should not be used to increase the speed of SQL. Perform tuning to increase the SQL speed.   

.. important::

  This function does not update the cache by monitoring update of the database value. For this reason, do not use the function where the latest data is always required to be displayed.

A usage example is shown below.

Component configuration file
  Follow the procedure below to configure for enabling the cache of search results.

  #. Defining the components to cache query results
  #. Search result cache configuration for each SQLID
  #. Definition of SQL execution component that caches the search results

  Defining the components of the query result cache class
    Configure :java:extdoc:`InMemoryResultSetCache <nablarch.core.db.cache.InMemoryResultSetCache>` of the class that caches the query results provided by default.

    .. code-block:: xml

      <component name="resultSetCache" class="nablarch.core.db.cache.InMemoryResultSetCache">
        <property name="cacheSize" value="100"/>
        <property name="systemTimeProvider" ref="systemTimeProvider"/>
      </component>

  Cache configuration for each SQL ID
    Configure the cache for each SQL ID. The cache expiration date can be configured for each SQLID using :java:extdoc:`BasicExpirationSetting <nablarch.core.cache.expirable.BasicExpirationSetting>` provided by default.

    The following units can be used for the expiration date.

    :ms: millisecond
    :sec: Sec
    :min: Minutes
    :h: Hours

    .. code-block:: xml

      <!-- Cache expiration configuration-->
        <component name="expirationSetting"
            class="nablarch.core.cache.expirable.BasicExpirationSetting">

          <property name="expiration">
            <map>
              <!-- Configure SQLID in key and expiration date in value-->
              <entry key="please.change.me.tutorial.ss11AA.W11AA01Action#SELECT" value="100ms"/>
              <entry key="please.change.me.tutorial.ss11AA.W11AA02Action#SELECT" value="30sec"/>
            </map>
          </property>

        </component>

  Definition of SQL execution component that caches the search results
    To cache search results, configure :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` in the generation class of the SQL execution component. Since :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` inherits :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` provided by default, the basic settings are the same as :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` .

    For the :java:extdoc:`expirationSetting <nablarch.core.db.cache.statement.CacheableStatementFactory.setExpirationSetting(nablarch.core.cache.expirable.ExpirationSetting)>` and :java:extdoc:`resultSetCache <nablarch.core.db.cache.statement.CacheableStatementFactory.setResultSetCache(nablarch.core.db.cache.ResultSetCache)>` property, configure the cache component of the query result configured above and the cache configuration component for each SQLID.

    The component :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` defined here should be configured in the component that acquires the database connection defined in :ref:`database-connect` .

    .. code-block:: xml

      <!-- Configure cacheableStatementFactory to generate cacheable statements-->
      <component name="cacheableStatementFactory"
                 class="nablarch.core.db.cache.CacheableStatementFactory">

        <!-- Expiration date setting -->
        <property name="expirationSetting" ref="expirationSetting"/>
        <!-- Cache implementation -->
        <property name="resultSetCache" ref="resultSetCache"/>

      </component>

  Implementation examples
    Database access using SQL does not change depending on the presence of cache. It is implemented as follows.

    * :ref:`database-execute_sqlid`
    * :ref:`database-input_bean`

Process using the `java.sql.Connection`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Handling of JDBC native database connection ( :java:extdoc:`java.sql.Connection` ) may be required. For example, when :java:extdoc:`java.sql.DatabaseMetaData` is required to be used.

This can be supported by acquiring :java:extdoc:`java.sql.Connection` obtained from :java:extdoc:`TransactionManagerConnection <nablarch.core.db.connection.TransactionManagerConnection>` which has been obtained from :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>`.

.. important::

  When :java:extdoc:`java.sql.Connection` is used, exception control needs to be performed by handling :java:extdoc:`java.sql.SQLException` , which is a check exception. If this exception control is implemented incorrectly, problems may occur such as failure not detected or investigation not performed when a failure occurs. For this reason, this feature should not be used unless there is a requirement that cannot be satisfied using :java:extdoc:`java.sql.Connection` .

An example is shown below.

.. code-block:: java

  TransactionManagerConnection managerConnection = DbConnectionContext.getTransactionManagerConnection();
  Connection connection = managerConnection.getConnection();
  return connection.getMetaData();
    

.. _database-replace_schema:
  
Switch the schema in SQL statement for each environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a different schema has to be referenced only for a specific SQL (table), the schema is explicitly specified in the SQL statement (for example: ``SELECT * FROM A_SCHEMA.TABLE1`` ), but there are cases where the schema name to be referred differs depending on the environment (see the example below).

**Reference schema of TABLE1**

====================== ==========
Working environment    Schema
====================== ==========
Production environment A_SCHEMA
Test environment       B_SCHEMA
====================== ==========

In this case, the method of explicitly describing the schema name in the SQL statement cannot be used.

.. code-block:: sql

  -- SELECT by specifying the schema name
  SELECT * FROM A_SCHEMA.TABLE1  -- Works in production environment but not in the test environment

  
For such a case, provide a function to switch the schema in the SQL statement for each environment.

First, describe a placeholder ``#SCHEMA#`` \ [#schema]_\ for replacing the schema in the SQL statement.

.. code-block:: sql
                
  -- SELECT by specifying the schema name
  SELECT * FROM #SCHEMA#.TABLE1


.. [#schema] The text of this placeholder is fixed.


Configure :java:extdoc:`BasicSqlLoader <nablarch.core.db.statement.BasicSqlLoader>` to replace the placeholders, as shown in the following example:

.. code-block:: xml
                
  <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
    <property name="sqlLoader">
      <component name="sqlLoader" class="nablarch.core.db.statement.BasicSqlLoader">
        <property name="sqlLoaderCallback">
          <list>
            <!-- Replace #SCHEMA# in SQL statement with specified value -->
            <component class="nablarch.core.db.statement.sqlloader.SchemaReplacer">
              <property name="schemaName" value="${nablarch.schemaReplacer.schemaName}"/>
            </component>
          </list>
        </property>
      </component>
    </property>
  </component>

Configure the value to replace the placeholder in ``schemaName`` of :java:extdoc:`SchemaReplacer <nablarch.core.db.statement.sqlloader.SchemaReplacer>` . In the above example, the value after replacement is configured in the environment-dependent value ``nablarch.schemaReplacer.schemaName`` . By switching this value for each environment, the schema in the SQL statement can be replaced with the one corresponding to the environment (see :ref:`how_to_switch_env_values` for details of the switching method).


.. tip::
   The schema replacement in the SQL statement by this function is a simple string replacement, and it does not check whether the schema exists or the SQL after the schema replacement is valid (an error occurs when executing the SQL statement).

Expansion example
--------------------------------------------------

.. _database-add_connection_factory:

Add a connection method to the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The procedure for adding a database connection method will be described. For example, this procedure should be followed when using the OSS connection pool library.

#. Inherit :java:extdoc:`ConnectionFactorySupport <nablarch.core.db.connection.ConnectionFactorySupport>` and create a class that generates a database connection.
#. Configure the class that is created in the component configuration file. ( see :ref:`database-connect` )

.. _database-add_dialect:

Add dialects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The procedure to add a dialect will be described.

For example, dialects have to be added when there is no dialect corresponding to the database product to be used, or to switch the availability of a specific function, it is necessary to add a dialect.

#. Inherit :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` and create a dialect corresponding to the database product.
#. Configure the created dialect in the component configuration file (see :ref:`database-use_dialect` )


.. _database-change_exception:

Switching the exception class when accessing the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section describes the procedure to switch the exception class during database access.

For example, to change the exception class of deadlock error, work according to this procedure.

#. Create the implementation class of :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` that generates database access error.
#. Create the implementation class of :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` that generates SQL run-time error.
#. Define the class that is created in the component configuration file.

The detailed procedure is shown below.

Create the implementation class of :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>`
  Create an implementation class of this interface to change :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` that is generated during database connection acquisition and transaction control (commit and rollback).

Create the implementation class of :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>`
  Create an implementation class of this interface to change :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` that occurs when SQL is executed.

Define in the component configuration file
  Implementation class of :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` must be configured in the component that acquires the database connection defined in :ref:`database-connect` .

  .. code-block:: xml

    <component class="sample.SampleDbAccessExceptionFactory" />

  The implementation class of :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` is configured for :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` . :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` must be configured in the component that acquires the database connection defined in :ref:`database-connect` .

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <property name="sqlStatementExceptionFactory">
        <component class="sample.SampleStatementExceptionFactory" />
      </property>
    </component>
