.. _transaction:

Transaction Management
============================
.. contents:: Table of contents
  :depth: 3
  :local:

Provides a transaction management function for resources (database and message queue) that require transaction control.

Function overview
--------------------------
Transaction control is possible for various resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Transaction management is possible for resources such as databases and message queues that require transaction control.

Refer to the following for details of transaction control of database.

* :ref:`transaction-database`
* :ref:`transaction-timeout`

If there is a requirement for transaction control for a new resource, the control can be easily realized by implementing the interface defined by this function.
For details, see :ref:`transaction_addResource`.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-transaction</artifactId>
  </dependency>

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _transaction-database:

Perform transaction control for the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Database transaction control can be realized by adding transaction control using JDBC to the component definition file.
It is assumed that the connection has been configured to the database.

For details on how to connect to the database, see :ref:`database-connect`.

To use a small transaction such as 1 SQL unit, configure and implement referring to :ref:`database-new_transaction`.

Example of component definition
  Define the factory class ( :java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>` ), which generates transaction class for JDBC, in the component configuration file.

  .. code-block:: xml

    <!-- Configure JdbcTransactionFactory as a component -->
    <component class="nablarch.core.db.transaction.JdbcTransactionFactory">

      <!-- Isolation level -->
      <property name="isolationLevel" value="READ_COMMITTED" />

      <!-- Transaction timeout in seconds -->
      <property name="transactionTimeoutSec" value="15" />

    </component>

.. tip::

  Basically, the class configured above is not used directly.
  If transaction control is required, use :ref:`transaction_management_handler`.

.. _transaction-timeout:

Apply transaction timeout for the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The transaction timeout function is enabled by configuring the transaction timeout seconds for :java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>`.
If the transaction timeout seconds is 0 or less, the transaction timeout function is disabled.

.. tip::

  For functions such as batch applications that process large amounts of data in bulk,
  the processing delays are handled by monitoring the end delay of the job scheduler instead of using the transaction timeout function.

  This is because in batch applications, it is sufficient if the overall processing time is within the expected range, and there is no problem even if delays occur in individual transactions.
  For example, even if a particular transaction takes 1 minute due to a lack of resources in the database, it is determined that there is no problem if the entire process is finished within the expected time.


Start check timing of transaction timeout
  ( :java:extdoc:`Transaction#begin() <nablarch.core.transaction.Transaction.begin()>` ) starts checking at the start of the transaction.

  Checks for timeouts for each transaction if multiple transactions are used
  (for example, if another transaction is executed in a transaction).

Check timing of transaction timeout
  Checks if the transaction timeout seconds are exceeded at the following timing.

  Before executing the SQL
    Throws :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` if transaction timeout seconds are exceeded before executing the SQL.

    Checks before SQL execution because access to the database will result in unnecessary consumption of resources
    if the transaction timeout seconds have already passed.

  After executing the SQL
    Throws :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` if transaction timeout seconds are exceeded after executing SQL.

    Since the transaction timeout seconds may be exceeded during SQL execution or result set conversion,
    a check is performed even if SQL execution is completed normally.

  When a query timeout exception occurs
    Throws :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` if an exception that indicates a query timeout occurs and transaction timeout number of seconds has been exceeded.
    Whether it is a query timeout exception is determined using the :ref:`dialect <database-dialect>` of the database function.

    Control might not come back from the database if a SQL statement with a long processing time (simple slow SQL or SQL waiting for lock release) is executed.
    Therefore, the number of seconds remaining in the transaction timeout is configured to `java.sql.Statement#setQueryTimeout`
    and the execution is forced to be canceled when the transaction timeout seconds is exceeded.

    If the query timeout time is configured when executing the SQL,
    overwrites the configured query timeout time with the remaining transaction timeout seconds
    when the remaining transaction timeout seconds is smaller than the configured query timeout time.

    An example of handling query timeout is shown below.

    Pattern 1
      | Configured query timeout time: 10 seconds
      | Transaction timeout remaining seconds: 15 seconds
      | Query timeout time configured when executing the SQL: 10 seconds
      | Transaction timeout does not occur when query timeout occurs and SQL runtime exception is thrown

    Pattern 2
      | Configured query timeout time: 10 seconds
      | Transaction timeout remaining seconds: 5 seconds
      | Query timeout time configured when executing the SQL: 5 seconds
      | Transaction timeout occurs when query timeout occurs and :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` is thrown.

  .. tip::

    Since this function checks for transaction timeout when accessing a database,
    it does not cause a transaction timeout when processing delay occurs in a logic that does not access the database.

    For example, if an infinite loop occurs in the logic that does not access the database, this function cannot detect the transaction timeout.
    In such a case, delayed application threads are handled using the application server timeout function, etc.

Reset timing of transaction timeout time
  The transaction timeout period is reset when a transaction is explicitly started ( when :java:extdoc:`Transaction#begin <nablarch.core.transaction.Transaction.begin()>` is called).
  Note that at the end of the transaction ( :java:extdoc:`Transaction#commit <nablarch.core.transaction.Transaction.commit()>` and  :java:extdoc:`Transaction#rollback <nablarch.core.transaction.Transaction.rollback()>` ),
  the remaining time of transaction timeout is not reset.

Expansion example
--------------------------------------------------

.. _transaction_addResource:

Add transaction target resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following steps are required to add transaction target resource.

For example, this applies when performing transaction control using IBM WebSphere MQ as a transaction manager for distributed transactions.

#. Add transaction implementation
#. Add a factory implementation to generate a transaction
#. Realize transaction control using :ref:`transaction_management_handler`

The detailed procedure is shown below.

Add transaction implementation
  Transaction implements the :java:extdoc:`Transaction <nablarch.core.transaction.Transaction>` interface and implements
  transaction begin/end process for the transaction target resource.

  .. code-block:: java

    public class SampleTransaction implements Transaction {

      private final String resourceName;

      // Receive the resource name for identifying
      // the transaction control target resource.
      // During transaction control, the resource for transaction control must be acquired
      // from this resource name.
      public SampleTransaction(String resourceName) {
        this.resourceName = resourceName;
      }

      @Override
      public void begin() {
        // Implement the transaction start process for the transaction target resource
      }

      @Override
      public void commit() {
        // Implement the transaction confirmation process for the transaction target resource
      }

      @Override
      public void rollback() {
        // Implement the transaction discard process for the transaction target resource
      }
    }

Add a factory implementation to generate a transaction
  Create a factory class to generate a transaction.
  Implement :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` for the factory class.

  This example is a factory class that generates the `SampleTransaction` created above.

  .. code-block:: java

    public class SampleTransactionFactory implements TransactionFactory {

      @Override
      public Transaction getTransaction(String resourceName) {
        // Hold a resource name to identify the transaction target
        // Create and return a transaction object.
        SampleTransaction transaction = new SampleTransaction(resourceName);
        return transaction;
      }
    }

Realize transaction control using :ref:`transaction_management_handler`
  Transaction control can be achieved by using the transaction control handler included in the standard handler of Nablarch.

  Configure the added factory class to the transaction control handler, as in the following example.

  .. code-block:: xml

    <!-- Transaction control handler -->
    <component class="nablarch.common.handler.TransactionManagementHandler">

      <!-- Transaction factory -->
      <property name="transactionFactory">
        <component class="sample.SampleTransactionFactory" />
      </property>

   </component>

