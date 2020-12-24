.. _`database-functional_comparison`:

Functional Comparison Between Universal DAO and JSR317 (JPA2.0)
----------------------------------------------------------------------------------------------------
This section compares the following functions:

* :ref:`Universal DAO <universal_dao>`
* |JSR317|

.. important::

  Universal DAO supports only those annotations listed in  :ref:`universal_dao_jpa_annotations`  among the annotations defined in JPA. 
  Functions related to annotations not described here cannot be used.


.. list-table:: Function comparison (A: Provided B: Partially provided C: Not provided D: Not applicable)
  :header-rows: 1
  :class: something-special-class

  * - Function
    - Universal DAO
    - JSR317

  * - Supports relationship |br|
    - C [#relation]_
    - A

  * - CRUD can be executed based on Entity |br|
      CRUD SQL can be executed without writing SQL
    - A |br| :ref:`To the manual <universal_dao-execute_crud_sql>`
    - A

  * - Search results can be acquired as Java Beans objects
    - A |br| :ref:`To the manual <universal_dao-bean_mapping>`
    - A

  * - An arbitrary SQL statement can be executed
    - A |br| :ref:`To the manual <universal_dao-sql_file>`
    - A

  * - SQL can be dynamically assembled
    - B [#criteria]_ |br| :ref:`To the manual <universal_dao-sql_file>`
    - A

  * - Can be executed in a batch
    - A |br| :ref:`To the manual <universal_dao-batch_execute>`
    - C

  * - Allows deferred loading  |br| when fetching large amounts of data |br|
      (can process large amounts |br| of data without squeezing the heap)
    - A |br| :ref:`To the manual <universal_dao-lazy_load>`
    - C

  * - Can search using range for paging.
    - A |br| :ref:`To the manual <universal_dao-paging>`
    - A

  * - Can number surrogate key values
    - A |br| :ref:`To the manual <universal_dao-generate_surrogate_key>`
    - A

  * - Can execute Bean Validation |br| when the Entity status is incorporated in the database
    - C [#validaiton]_
    - A

  * - Can execute arbitrary processing (callback call) |br| before and after database access
    - C [#callback]_
    - A

  * - Exclusive control is possible
    - B [#lock]_ |br| :ref:`To the manual(optimistic lock) <universal_dao_jpa_optimistic_lock>` |br| :ref:`To the manual(pessimistic lock) <universal_dao_jpa_pessimistic_lock>`
    - A

.. [#relation] Searching for tables with relationships can be supported by creating SQL. Registration, update and deletion are handled by calling the necessary function for each table. 
.. [#criteria] Universal DAO can perform dynamic processing only for conditions and sort items. For details, see :ref:`SQL dynamic assembly <database-variable_condition>` 
.. [#validaiton] Nablarch performs validation when data is received from the outside, and converts to Entity and saves to database only when there is no validation error.
.. [#callback] If an arbitrary process is required, it is handled by the process that calls the universal DAO.
.. [#lock] Universal DAO only supports optimistic locking. Pessimistic lock or lock mode specification at the time of search defined in JSR are not supported. (Pessimistic lock can be realized by using  ``select for update`` .) 

.. |jsr317| raw:: html

   <a href="https://jcp.org/en/jsr/detail?id=317" target="_blank">JSR317(External site)</a>

.. |br| raw:: html

  <br />
