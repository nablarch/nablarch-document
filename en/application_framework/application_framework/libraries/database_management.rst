.. _database_management:

Database Access
==================================================
Provides the function to connect to database and execute SQL.

Nablarch provides the following two types of database access functions:

.. toctree::
  :maxdepth: 1

  database/database
  database/universal_dao

Although SQL can be executed by using either of the above functions, 
use of  :ref:`universal DAO <universal_dao>`  is recommended for the following reasons.

* SQL statement of CRUD can be automatically generated from Entity, and the SQL can be executed.
* Since the search results can be obtained as a Bean object, complementary functions of IDE can be effectively used and development efficiency is good.

.. important::

  Even if :ref:`universal DAO <universal_dao>`  is used, 
  :ref:`JDBC wrapper function <database>`  is used to connect to the database and execute SQL. 
  Therefore, configuration for using :ref:`JDBC wrapper function <database>`  are required.

.. tip::
 For comparison of functions between :ref:`universal_dao` and Jakarta Persistence, refer to  :ref:`database-functional_comparison` .

.. toctree::
  :hidden:

  database/functional_comparison