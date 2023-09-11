.. _universal_dao:

Universal DAO
=====================================================================

.. contents:: Table of contents
   :depth: 3
   :local:

Universal DAO provides a simple O/R mapper that
uses `JPA2.0(JSR317) (external site) <https://jcp.org/en/jsr/detail?id=317>`_ annotations.

Since Universal DAO uses a :ref:`database`,
the :ref:`database` must be configured to use Universal DAO.

.. tip::
 Universal DAO is positioned as a simple O/R mapper
 and is not intended to realize all database access.
 Perform :ref:`database` operations directly if it cannot be realized with Universal DAO.

 For example, in Universal DAO, update/delete with conditions other than the primary key cannot be performed,
 so :ref:`database` operations must be performed directly.

.. tip::

  Universal DAO does not provide an automatic configuration function for common items (insert users, update users, etc. defined in all tables).
  To automatically configure values for common items, apply :ref:`doma_adaptor` and use Doma entity listener function.

  To use Universal DAO in any case, configure the common items explicitly in the application before using the functions of Universal DAO.

.. _universal_dao-spec:

Function overview
---------------------------------------------------------------------

.. _universal_dao-execute_crud_sql:

Simple CRUD without writing SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Just by adding JPA annotation to Entity, a simple CRUD can be created without writing SQL.
SQL statements are constructed at runtime based on JPA annotations.

* Registration/Batch registration
* Update/Batch update by specifying the primary key
* Delete/Batch delete by specifying the primary key
* Search by specifying the primary key

For JPA annotations that can be used in Entity, see :ref:`universal_dao_jpa_annotations`.


.. tip::
   In the above CRUD function of Universal DAO, schema can be specified using \ ``@Table``\ annotation \
   (see :ref:`universal_dao_jpa_annotations`).
   However, :ref:`database-replace_schema` function of :ref:`database` cannot be used with the above CRUD function of Universal DAO. \
   Use the :ref:`database` directly instead of Universal DAO for switching the schema for each environment.
   
.. _universal_dao-bean_mapping:

Search results can be mapped to Bean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In search, as with :ref:`database`, you can create an SQL file and perform a search by specifying the SQL ID.
In Universal DAO, search results can be obtained by mapping them to Bean (Entity, Form, DTO).
Map the items whose Bean property name matches the SELECT clause name.

For data types that can be used for Bean, see :ref:`universal_dao_bean_data_types`.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-dao</artifactId>
  </dependency>

How to use
---------------------------------------------------------------------

.. important::
 See :java:extdoc:`nablarch.common.dao.UniversalDao <nablarch.common.dao.UniversalDao>` for the basic usage of Universal DAO.

Configure settings to use Universal DAO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use universal DAO, add :java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>` configuration
to component definition in addition to :ref:`database` configuration.

.. code-block:: xml

 <!-- Configure the component name in "daoContextFactory". -->
 <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory" />

.. _universal_dao-sql_file:

Search with any SQL (SQL file)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To search using SQL, create an SQL file and search by specifying the SQL ID,
similar to :ref:`database-use_sql_file` of database access.

.. code-block:: java

 UniversalDao.findAllBySqlFile(User.class, "FIND_BY_NAME");

SQL file is derived from Bean that maps the search results.
When User.class in the above example is sample.entity.User,
the path of the SQL file is sample/entity/User.sql under the class path.

If "#" is included in the SQL ID, it is interpreted as "SQL file path#SQL ID".
In the example below, the SQL file path is sample/entity/Member.sql under the class path,
and the SQL ID is FIND_BY_NAME.

.. code-block:: java

 UniversalDao.findAllBySqlFile(GoldUser.class, "sample.entity.Member#FIND_BY_NAME");

.. tip::
 The specification including "#" can be used when SQL is to be aggregated in function units (action handler units).
 However, since there is a disadvantage that the specification becomes complicated, basically use the specification without "#".

.. _universal_dao-join:

Obtain search results using JOIN of tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes the result of JOIN of multiple tables in list search is required to be acquired.
Since it is inefficient in such cases, create **a Bean that maps the SQL that can be searched once and JOIN results**,
without individually searching the JOIN target data.

.. _universal_dao-lazy_load:

Deferred loading of search results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The memory becomes insufficient in processes that handle large amounts of search results, and all search results cannot be expanded in the memory.
Some of the cases are as follows.

* Download large amounts of data on the Web
* Process large amounts of data in batch

In such cases, use deferred loading of Universal DAO.
When deferred loading is used, Universal DAO loads the records one by one,
but the amount of memory used changes depending on the JDBC fetch size.
For details of the fetch size, refer to the manual provided by the database vendor.

Deferred loading can be used by just calling the :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` method first during search.
since server cursor is used internally,
:java:extdoc:`DeferredEntityList#close <nablarch.common.dao.DeferredEntityList.close()>` method must be called.

.. code-block:: java

 // Call close using try-with-resources.
 // Get DeferredEntityList by downcast.
 try (DeferredEntityList<User> users
         = (DeferredEntityList<User>) UniversalDao.defer()
                                         .findAllBySqlFile(User.class, "FIND_BY_NAME")) {
     for (User user : users) {
         // Process using the user
     }
 }

.. important::
   Depending on the RDBMS used, if transaction control is performed while a cursor is open, the cursor will be closed.
   Note that this may result in an error when transaction control is performed during processing of large amounts of data using lazy loading, as it may refer to a cursor that has already been closed.
   Avoid this by adjusting the cursor behavior according to the manual provided by the database vendor, or by :ref:`paging <universal_dao-paging>` to avoid handling large amounts of data.

.. _universal_dao-search_with_condition:

Searching by specifying the conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Like the search screen, Universal DAO also provides a search with specified conditions.

.. code-block:: java

 // Get the search conditions
 ProjectSearchForm condition = context.getRequestScopedVar("form");

 // Search by specifying the conditions
 List<Project> projects = UniversalDao.findAllBySqlFile(
     Project.class, "SEARCH_PROJECT", condition);

.. important::
  For the search condition, specify a dedicated Bean that has the search condition instead of Entity.
  However, Entity may be specified when accessing only one table.


Convert type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Universal DAO, :ref:`@Temporal <universal_dao_jpa_temporal>` can be used to specify how to map ``java.util.Date`` and ``java.util.Calendar`` type values to the database.
Since arbitrary mapping is not possible for other types, Entity properties must be defined according to the database type and specifications of the JDBC driver to be used.

Though Universal DAO uses JPA annotation information when sending automatically generated SQL to the DB, JPA annotation information is not used when sending arbitrary SQL to the DB.
Therefore, the type conversion is as follows.

:ref:`When executing SQL automatically generated from the Entity <universal_dao-execute_crud_sql>`
  During output to a database
    * For properties configured with :ref:`@Temporal <universal_dao_jpa_temporal>`, converts to the type specified in @Temporal.
    * For other than above, conversion is performed by delegating the process to the :ref:`database`.

  When fetching from database
    * For properties configured with :ref:`@Temporal <universal_dao_jpa_temporal>`, converts from the type specified in @Temporal.
    * For other than the above, values are converted based on Entity information.

:ref:`When searching with an arbitrary SQL <universal_dao-sql_file>`
  During output to a database
    * Conversion is performed by delegating the process to the :ref:`database`.

  When fetching from database
    * Perform the same process as when executing SQL automatically generated from the Entity.


.. important::
  If the database type and property type do not match, a type conversion error may occur during runtime.
  In addition, implicit type conversion is performed during SQL execution, which may cause performance degradation (caused as index is not used).

  To map between database and Java data type,
  refer to the JDBC driver manual as it depends on the product used.

  For example, if the DB is a date type, the property type is :java:extdoc:`java.sql.Date` in many databases.
  If the DB is a numeric type (integer, bigint, number), the property type will be
  `int` (:java:extdoc:`java.lang.Integer`) or `long` (:java:extdoc:`java.lang.Long`).


.. _universal_dao-paging:

Paging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal DAO Search supports paging.
First call the :java:extdoc:`UniversalDao#per <nablarch.common.dao.UniversalDao.per(long)>` method and :java:extdoc:`UniversalDao#page <nablarch.common.dao.UniversalDao.page(long)>` method for paging at the time of search.

.. code-block:: java

 EntityList<User> users = UniversalDao.per(3).page(1)
                             .findAllBySqlFile(User.class, "FIND_ALL_USERS");

Information such as the number of search results required for displaying the paging screen is stored in :java:extdoc:`Pagination <nablarch.common.dao.Pagination>`.
:java:extdoc:`Pagination <nablarch.common.dao.Pagination>` can be obtained from :java:extdoc:`EntityList <nablarch.common.dao.EntityList>`.

.. code-block:: java

 Pagination pagination = users.getPagination();

.. tip::
  Search process for paging is performed using :ref:`range specified search function of database access (JDBC wrapper) <database-paging>`.

.. _universal_dao-generate_surrogate_key:

Numbering the surrogate keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. toctree::
  :maxdepth: 1
  :hidden:

  generator

When numbering the surrogate keys, use the following annotations.

* :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
* :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
* :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

Universal DAO supports all strategies of :java:extdoc:`javax.persistence.GenerationType`.

GenerationType.AUTO
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.AUTO)
  public Long getId() {
      return id;
  }

 - Select the numbering method based on :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` configured in the database function.
   The priority is in the order IDENTITY → SEQUENCE → TABLE.
 - If SEQUENCE is selected, the sequence object name will be "<table name>_<column name to be numbered>".
 - To specify the sequence object name, use :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`.

GenerationType.IDENTITY
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  public Long getId() {
      return id;
  }

GenerationType.SEQUENCE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "seq")
  @SequenceGenerator(name = "seq", sequenceName = "USER_ID_SEQ")
  public Long getId() {
      return id;
  }

 - Specify the sequence object name with :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`.
 - If the sequenceName attribute is omitted, it will be "<table name>_<column name to be numbered>".

GenerationType.TABLE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.TABLE, generator = "table")
  @TableGenerator(name = "table", pkColumnValue = "USER_ID")
  public Long getId() {
      return id;
  }

 - Specify the value that identifies a record with :ref:`@TableGenerator <universal_dao_jpa_table_generator>`.
 - If the pkColumnValue attribute is omitted, it will be "<table name>_<column name to be numbered>".

.. tip::

  Numbering process of surrogate key using sequence and table is performed using :ref:`generator`.
  Refer to the link destination for configuring the value (configuring the table and column names when using a table).

.. _universal_dao-batch_execute:

Perform batch execution (batch registration, update and deletion)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal DAO allows batch execution when registering, updating, or deleting large amounts of data.
By performing batch execution, the number of round trips between the application server and database server can be reduced, and improvement in performance can be expected.

Batch execution uses the following methods.

* :java:extdoc:`batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`
* :java:extdoc:`batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>`
* :java:extdoc:`batchDelete <nablarch.common.dao.UniversalDao.batchDelete(java.util.List)>`

.. important::

  Exclusive control processing is not performed in the batch update processing that uses `batchUpdate`.
  If the version of the Entity to be updated and the version in the database do not match, the process ends normally without updating the record.

  If the update processing requires exclusive control, call the update process for each record instead of batch update.

.. _`universal_dao_jpa_optimistic_lock`:

Optimistic locking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal DAO automatically performs optimistic locking
when an Entity with :ref:`@Version <universal_dao_jpa_version>` is updated.
Throws :java:extdoc:`javax.persistence.OptimisticLockException` if an exclusive error occurs in optimistic locking.

.. important::
 :ref:`@Version <universal_dao_jpa_version>` can be specified only for numeric type properties.
 It does not work properly with string type properties.

Screen transition during an exclusive error is performed using :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>`.

.. code-block:: java

 // Specify the target exception in the type attribute and transition destination path
 // in the path attribute.
 @OnError(type = OptimisticLockException.class,
          path = "/WEB-INF/view/common/errorPages/userError.jsp")
 public HttpResponse update(HttpRequest request, ExecutionContext context) {

     UniversalDao.update(user); // Before and after processing is omitted.

 }

.. important::
  Note that optimistic locking cannot be used in batch update process (`batchUpdate`)
  as described in :ref:`universal_dao-batch_execute`.

.. _`universal_dao_jpa_pessimistic_lock`:

Pessimistic locking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal DAO does not particularly provide the pessimistic locking function.

Pessimistic locking is done by using the database row locking (select for update).
SQL with the row lock (select for update) executes using
the :java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class-java.lang.String-java.lang.Object)>` method.

Concept of exclusive control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is necessary to decide from a business perspective the table in which the version column used for exclusive control has to be defined.

Tables with version numbers are defined for each unit of exclusive control and the largest unit in which conflicts are allowed.
For example, if business allows locking in a large unit called "user", a version number is defined in the user table.
However, note that the possibility of conflict increases if the unit is increased, and update failure (in the case of optimistic locking) and processing delay (in the case of pessimistic locking) will occur.


Register (update) binary data with a large data size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You may want to register (update) binary data with a large data size, such as BLOB of Oracle.
In the case of Universal DAO, since registration (update) cannot be performed unless all data is loaded into memory,
use the functions provided by the database to register (update) directly from a file.

For details, see :ref:`database-binary_column`.

Registration (update) of text data with a large data size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You may want to register (update) text data with a large data size, such as CLOB of Oracle.
In the case of Universal DAO, since registration (update) cannot be performed unless all data is loaded into memory,
use the functions provided by the database to register (update) directly from a file.

For details, see :ref:`database-clob_column`.

.. _universal_dao-transaction:

Execute in a transaction different from the current transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section explains how to perform the same process as :ref:`database-new_transaction` of :ref:`database`  with universal DAO.

The following procedures are required to use individual transactions.

#. Define :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` in the component configuration file.
#. Use :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` to execute Universal DAO in a new transaction.

An usage example is shown below.

Component configuration file
  Define :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` in the component configuration file.

  * Configure implementation class of :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>`
    to :java:extdoc:`connectionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>` property.
    For details of implementation class of :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>`, see :ref:`database-connect`.

  * Configure implementation class of :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>`
    to :java:extdoc:`transactionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>` property.
    For details of implementation of :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>`, see :ref:`transaction-database`.

  .. code-block:: xml

    <component name="find-persons-transaction"
        class="nablarch.core.db.transaction.SimpleDbTransactionManager">

      <!-- Configure ConnectionFactory implementation class in the connectionFactory property -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- Configure TransactionFactory implementation class in the transactionFactory property -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- Configure a name to identify the transaction -->
      <property name="dbTransactionName" value="update-login-failed-count-transaction" />

    </component>

Implementation examples
  Use :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` configured in the component configuration file and execute universal DAO.
  In addition, instead of using :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` directly,
  use :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` to perform transaction control.

  First, create a class that inherits :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>`.

  .. code-block:: java

    private static final class FindPersonsTransaction extends UniversalDao.Transaction {

        // Prepare a container to receive the result.
        private EntityList<Person> persons;

        FindPersonsTransaction() {
            // Specify SimpleDbTransactionManager as super ().
            // The name specified in the component definition or the SimpleDbTransactionManager object can be specified.
            // In this example, the name mentioned in the component definition is specified.
            super("find-persons-transaction");
        }

        //This method is automatically executed in another transaction.
        // If the process is completed successfully, the transaction is committed.
        // If an exception or error is thrown, the transaction is rolled back.
        @Override
        protected void execute() {
            // Implement the process using UniversalDao in the execute method.
            persons = UniversalDao.findAllBySqlFile(Person.class, "FIND_PERSONS");
        }

        // Prepare getter that returns the result.
        public EntityList<Person> getPersons() {
            return persons;
        }
    }

  Then, call the class that inherits :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>`.

  .. code-block:: java

    // Executed in a different transaction after generation.
    FindPersonsTransaction findPersonsTransaction = new FindPersonsTransaction();

    // Acquire the result.
    EntityList<Person> persons = findPersonsTransaction.getPersons();


Expansion example
---------------------------------------------------------------------

Support when information cannot be obtained from DatabaseMetaData
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Depending on the database, the primary key information cannot be acquired
from :java:extdoc:`java.sql.DatabaseMetaData` due to the use of synonyms or permission problems.
If the primary key information cannot be acquired, the search that specifies the primary key does not work properly.
For such cases, support by creating an inherited class of :java:extdoc:`DatabaseMetaDataExtractor <nablarch.common.dao.DatabaseMetaDataExtractor>`.
Refer to the product manual as the method to acquire the primary key information depends on the database.

Configuration is required to use the created class.

.. code-block:: xml

 <!--
 Configuration example when sample.dao.CustomDatabaseMetaDataExtractor is created
 Configure the component name as "databaseMetaDataExtractor".
 -->
 <component name="databaseMetaDataExtractor" class="sample.dao.CustomDatabaseMetaDataExtractor" />

.. _`universal_dao_jpa_annotations`:

JPA annotation that can be used for Entity
---------------------------------------------------------------------
JPA annotations that can be used for entity are as follows.

* Annotation configured in class

  * :ref:`@Entity <universal_dao_jpa_entity>`
  * :ref:`@Table <universal_dao_jpa_table>`
  * :ref:`@Access <universal_dao_jpa_access>`
* Annotation configured in getter or field

  * :ref:`@Column <universal_dao_jpa_column>`
  * :ref:`@Id <universal_dao_jpa_id>`
  * :ref:`@Version <universal_dao_jpa_version>`
  * :ref:`@Temporal <universal_dao_jpa_temporal>`
  * :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
  * :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
  * :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

.. important::
 Using annotations and attributes that are not described here will not work.

When configuring in a field, specify explicitly with @Access. Refers to the field annotation only when explicitly specified with @Access.

Even when configuring an annotation in a field, since acquiring and configuring values are performed through properties in UniversalDao, getters and setters must be created.

Since the field and property are linked by name, if the names are different, the annotation of the field cannot be referenced by the property.
Therefore, be sure to use the same field and property names (getXX, setXX).

.. tip::
 For example, when using a library that generates boilerplate code such as Lombok,
 take full advantage of the library as configuring the annotation on the field
 eliminates the need to create a getter.

.. _`universal_dao_jpa_entity`:

*javax.persistence.Entity*
 This annotation is configured in the Entity class corresponding to the database table.

 When this annotation is configured, the table name is derived from the class name.
 The table name is the value obtained by converting the class name (Pascal case) into the snake case (all uppercase).

 .. code-block:: bash

  Book class        -> BOOK
  BookAuthor class  -> BOOK_AUTHOR

 .. tip::
  If the table name cannot be derived from the class name,
  specify the table name explicitly using :ref:`@Table <universal_dao_jpa_table>` that is described later.

.. _`universal_dao_jpa_table`:

*javax.persistence.Table*
 This annotation is used to specify the table name.

 If a value is specified in the name attribute, that value will be used as the table name.
 If a value is specified in schema attribute, access the table by specifying the specified schema name as a qualifier.
 For example, when work is specified in the schema attribute and the table name is users_work, work.users_work is accessed.

.. _`universal_dao_jpa_access`:

*javax.persistence.Access*
 This annotation is used to specify the location to configure the annotation.

 Refers to the field annotation only when explicitly specified in the field.

.. _`universal_dao_jpa_column`:

*javax.persistence.Column*
 This annotation is used to specify the column name.

 If a value is specified in the name attribute, that value will be used as the column name.

 .. tip::
  If this annotation is not set, the column name is derived from the property name.
  The derivation method is the same as the derivation method used for the table name.
  For details, see :ref:`@Entity <universal_dao_jpa_entity>`.

.. _`universal_dao_jpa_id`:

*javax.persistence.Id*
 This annotation is configured in the primary key.

 In the case of a compound primary key, configure this annotation to multiple getters or fields.

.. _`universal_dao_jpa_version`:

*javax.persistence.Version*
 This annotation is configured in the version column used for exclusive control.

 This annotation can be specified only for numeric type properties.
 It does not work properly with string type properties.

 When this annotation is set,
 the version column is automatically added to the condition during update processing, and optimistic locking is performed.

 .. tip::
  Only one annotation can be specified in the Entity.

.. _`universal_dao_jpa_temporal`:

*javax.persistence.Temporal*
 This annotation specifies how to map the values of
 *java.util.Date* and *java.util.Calendar* types to the database.

 Converts the value of the Java object to the database type specified in value attribute and registers it in the database.

.. _`universal_dao_jpa_generated_value`:

*javax.persistence.GeneratedValue*
 This annotation indicates that the automatically numbered value is registered.

 Configures the numbering method to the strategy attribute.
 When AUTO is configured, the numbering method is selected according to the following rules.

 * If there is a Generator configuration corresponding to the generator attribute, performs the numbering process using that Generator.
 * If generator is not configured or there is no corresponding Generator configuration,
   select the numbering method based on :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` configured in the database function.
   The priority is in the order IDENTITY → SEQUENCE → TABLE.

 Configure an arbitrary name in the generator attribute.

 .. tip::
  If :ref:`@GeneratedValue <universal_dao_jpa_generated_value>` cannot be used to
  acquire the sequence object name for sequence numbering or the value
  that identifies the record for table numbering,
  derive each value from the table name and column name to be automatically numbered.

  .. code-block:: bash

   Table name "USER", Column name to be numbered "ID" -> USER_ID

.. _`universal_dao_jpa_sequence_generator`:

*javax.persistence.SequenceGenerator*
 This annotation has to be configured when using sequence numbering.

 In the name attribute, configure the same value as the generator attribute of
 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`.

 Configure the sequence object name created in the database to the sequenceName attribute.

 .. tip::
  The numbering function is used to perform sequence numbering.
  For this reason, :ref:`numbering configuration <generator_dao_setting>` must be performed separately.

.. _`universal_dao_jpa_table_generator`:

*javax.persistence.TableGenerator*
 This annotation is configured when using table numbering.

 In the name attribute, configure the same value as the generator attribute of
 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`.

 In the pkColumnValue attribute, configure a value to identify the record in the numbering table.

 .. tip::
  The numbering function is used to perform table numbering.
  For this reason, :ref:`numbering configuration <generator_dao_setting>` must be performed separately.

.. _`universal_dao_bean_data_types`:

Data types that can be used for Bean
---------------------------------------------------------------------
Data types that can be used in Bean, which maps search results, are as follows.

.. important::
 Search results cannot be mapped to data types not listed here (runtime exception is thrown).

*java.lang.String*
 \

*java.lang.Short*
 Primitive types can also be specified. For primitive types, ``null`` is handled as ``0``.

*java.lang.Integer*
 Primitive types can also be specified. For primitive types, ``null`` is handled as ``0``.

*java.lang.Long*
 Primitive types can also be specified. For primitive types, ``null`` is handled as ``0``.

*java.math.BigDecimal*
 \

*java.lang.Boolean*
 Primitive types can also be specified. For primitive types, ``null`` is handled as ``false``.
 In the case of wrapper type (Boolean), the read method name must start with get.
 In the case of a primitive type, the read method name may start with 'is'.

*java.util.Date*
 The data type has to be specified in the database
 with :ref:`@Temporal <universal_dao_jpa_temporal>` of JPA.


*java.sql.Date*
 \

*java.sql.Timestamp*
 \

*byte[]*
  Be careful not to expand the data in the heap by using this function
  for the value of data type of very large size such as BLOB.
  When handling very large binary data,
  use database access directly and refer to the data through Stream.

  For details, see :ref:`database-binary_column`.
