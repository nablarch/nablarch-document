.. _`database-functional_comparison_jdbc_wrapper`:

Functional Comparison Between Universal DAO and JDBC Wrapper
----------------------------------------------------------------------------------------------------
This section compares the following functions:

* :ref:`Universal DAO <universal_dao>`
* :ref:`JDBC wrapper <database>`

Universal DAO is a simple O/R mapper that accesses the database by using the :ref:`JDBC wrapper <database>` internally.
Therefore, as described in :ref:`database_management`, execute SQL with Universal DAO in principle,
and use the :ref:`JDBC wrapper <database>` only when it cannot be realized with Universal DAO.

When to use the JDBC wrapper
  Typical situations that cannot be realized with Universal DAO and require the JDBC wrapper are as follows:

  * To execute an arbitrary update SQL (UPDATE, INSERT, DELETE or MERGE), for example, update or delete with conditions other than the primary key
  * To execute a stored procedure
  * To register, update or acquire binary data or text data with a large data size (BLOB or CLOB) as a stream without loading it into memory
  * To automatically configure the values of common items such as registration date and time or update date and time when executing SQL
  * To cache search results
  * To switch the schema in SQL statements for each environment for the SQL automatically generated from Entity
  * To pass a statement for search to the data reader of a batch process or a messaging process
  * To execute SQL by specifying the SQL statement directly, when the SQL cannot be defined in an SQL file

.. list-table:: Function comparison (A: Provided B: Partially provided C: Not provided D: Not applicable)
  :header-rows: 1
  :class: something-special-class

  * - Function
    - Universal DAO
    - JDBC wrapper

  * - CRUD can be executed based on Entity |br|
      CRUD SQL can be executed without writing SQL
    - A |br| :ref:`To the manual <universal_dao-execute_crud_sql>`
    - C [#crud]_

  * - Can search with an arbitrary SQL written in an SQL file
    - A |br| :ref:`To the manual <universal_dao-sql_file>`
    - A |br| :ref:`To the manual <database-execute_sqlid>`

  * - An arbitrary update SQL (UPDATE, INSERT, DELETE or MERGE) can be executed |br|
      (update or delete with conditions other than the primary key, etc.)
    - C [#update]_
    - A |br| :ref:`To the manual <database-input_bean>`

  * - SQL can be executed by specifying the SQL statement directly
    - C
    - A [#direct_sql]_ |br| :ref:`To the manual <database-sql_file>`

  * - A stored procedure can be executed
    - C
    - A |br| :ref:`To the manual <database-stored_procedure>`

  * - Bean property values can be set to SQL bind variables
    - A |br| :ref:`To the manual <universal_dao-search_with_condition>`
    - A |br| :ref:`To the manual <database-input_bean>`

  * - SQL can be dynamically assembled
    - A [#criteria]_ |br| :ref:`To the manual <universal_dao-sql_file>`
    - A |br| :ref:`To the manual <database-variable_condition>`

  * - Search results can be acquired as Java Beans objects
    - A |br| :ref:`To the manual <universal_dao-bean_mapping>`
    - C [#sqlrow]_

  * - Allows deferred loading when fetching large amounts of data |br|
      (can process large amounts of data without squeezing the heap)
    - A |br| :ref:`To the manual <universal_dao-lazy_load>`
    - A [#iterator]_

  * - Can search using range for paging
    - A |br| :ref:`To the manual <universal_dao-paging>`
    - A |br| :ref:`To the manual <database-paging>`

  * - Search results can be cached
    - C [#cache]_
    - A |br| :ref:`To the manual <database-use_cache>`

  * - Can be executed in a batch (batch registration, update and deletion)
    - A |br| :ref:`To the manual <universal_dao-batch_execute>`
    - A [#batch]_

  * - Optimistic locking is possible
    - A |br| :ref:`To the manual <universal_dao_jpa_optimistic_lock>`
    - C [#optimistic_lock]_

  * - Pessimistic locking is possible
    - D [#pessimistic_lock]_ |br| :ref:`To the manual <universal_dao_jpa_pessimistic_lock>`
    - D [#pessimistic_lock]_

  * - Values of common items (registration date and time, update date and time, etc.) |br| can be configured automatically
    - C [#common_property]_
    - A |br| :ref:`To the manual <database-common_bean>`

  * - Binary data or text data with a large data size (BLOB or CLOB) |br|
      can be registered, updated and acquired as a stream
    - C [#lob]_
    - A |br| :ref:`To the manual (binary type) <database-binary_column>` |br| :ref:`To the manual (CLOB type) <database-clob_column>`

  * - Can number surrogate key values
    - A |br| :ref:`To the manual <universal_dao-generate_surrogate_key>`
    - C [#generator]_

  * - Can be executed in a transaction different from the current transaction
    - A |br| :ref:`To the manual <universal_dao-transaction>`
    - A |br| :ref:`To the manual <database-new_transaction>`

  * - The schema in SQL statements can be switched for each environment
    - B [#schema]_ |br| :ref:`To the manual <universal_dao-execute_crud_sql>`
    - A |br| :ref:`To the manual <database-replace_schema>`

  * - A statement for search can be passed to the data reader |br| of a batch process or a messaging process
    - C
    - A |br| :ref:`To the manual (batch) <nablarch_batch-data_reader>` |br| :ref:`To the manual (messaging) <db_messaging_architecture-reader>`

.. [#crud] In the JDBC wrapper, CRUD SQL is also written in an SQL file and executed.
.. [#update] In Universal DAO, SQL written in an SQL file can be used only for search. Update and delete are limited to the SQL automatically generated from Entity (update and delete with the primary key as the condition).
.. [#direct_sql] In principle, write SQL in an SQL file, and use the API that specifies the SQL statement directly only when the SQL cannot be defined in an SQL file. For details, see :ref:`database-sql_file`.
.. [#criteria] Universal DAO can perform dynamic assembly only for conditions and sort items written in an SQL file. For details, see :ref:`SQL dynamic assembly <database-variable_condition>`.
.. [#sqlrow] In the JDBC wrapper, search results are acquired as :java:extdoc:`SqlResultSet <nablarch.core.db.statement.SqlResultSet>` (a list of :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>`).
.. [#iterator] In the JDBC wrapper, search results are processed one record at a time by using :java:extdoc:`ResultSetIterator <nablarch.core.db.statement.ResultSetIterator>` acquired with :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`.
.. [#cache] The configuration of :ref:`database-use_cache` is not applied to the search executed with Universal DAO.
.. [#batch] In the JDBC wrapper, add SQL to the batch with :java:extdoc:`SqlPStatement#addBatch <nablarch.core.db.statement.SqlPStatement.addBatch()>` or :java:extdoc:`ParameterizedSqlPStatement#addBatchObject <nablarch.core.db.statement.ParameterizedSqlPStatement.addBatchObject(java.lang.Object)>`, and execute them at once with :java:extdoc:`SqlPStatement#executeBatch <nablarch.core.db.statement.SqlPStatement.executeBatch()>`.
.. [#optimistic_lock] In the JDBC wrapper, optimistic locking is realized by writing the comparison and update of the version number in SQL.
.. [#pessimistic_lock] In both functions, pessimistic locking is realized by writing the row lock of the database ( ``select for update`` ) in SQL.
.. [#common_property] To automatically configure the values of common items, apply :ref:`doma_adaptor`, or configure the values explicitly in the application before calling Universal DAO.
.. [#lob] In Universal DAO, registration (update) cannot be performed unless all data is loaded into memory.
.. [#generator] To use a numbered value in the JDBC wrapper, number the value in the application as described in :ref:`generator`.
.. [#schema] In Universal DAO, :ref:`database-replace_schema` cannot be used for the SQL automatically generated from Entity. In this case, specify the schema with the ``@Table`` annotation.

.. |br| raw:: html

  <br />
