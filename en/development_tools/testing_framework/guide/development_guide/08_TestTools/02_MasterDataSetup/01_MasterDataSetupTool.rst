.. _master_data_setup_tool:

==============================
Master Data Input Tool
==============================

Summary
========


Provide a function to input the master data into the database.


Features
============

* The data can be described in the same format as the test data of an automated test.
* Since the component configuration file of Nablarch Application Framework is used, a separate configuration file is not required to be prepared.
* Data input to backup schema\ [#]_\  can be performed simultaneously.

.. [#]
  The backup schema is the schema used by \ :doc:`../../06_TestFWGuide/04_MasterDataRestore`\ of the automated testing framework. It is necessary to input the same master data as the automated test schema in the backup schema, and this tool can be used to input data to the two schemas simultaneously.

.. important::

  This tool does not support the multi-thread function. 
  Testing of multi-threaded functions performed should be done with tests that do not use the testing framework (such as integration tests).

How to Use
=============

Prerequisites
----------------

See \ :ref:`master_data_setup_prerequisite` of :doc:`02_ConfigMasterDataSetupTool`\ .

How to create data
--------------------

Enter the data to be input in the MASTER_DATA.xlsx file.The method to enter data is the same as the automated test.
For more information on how to enter the data, see "\ :ref:`how_to_write_setup_table`\".

How to execute
----------------

From the Ant view, double-click on the target to be run.


.. image:: ./_image/build_file_in_view.png
   :scale: 100

.. tip::
  For information on how to setup Ant view, see \ :ref:`how_to_setup_ant_view_in_eclipse`\ .


For target details, see the table given below.

 +-----------------------+----------------------------------------------------------------------------+
 | Target name           | Description                                                                |
 +=======================+============================================================================+
 |Data input (main) |br| | Use the configuration file of the main project to input the database.      |
 |データ投入(main)       | Data is input in the schema when running the application                   |
 |                       | on the application server such as subfunction unit test.                   |
 +-----------------------+----------------------------------------------------------------------------+
 |Data input (test) |br| | The database is input using the configuration file of the test project.    |
 |データ投入(test)       | The data is populated in the schema used by the automated test.            |
 |                       | Data is also input to the master data backup scheme simultaneously.        |
 +-----------------------+----------------------------------------------------------------------------+
 |Master data input |br| | Executes the above two targets together.                                   |
 |マスタデータ投入       |                                                                            |
 +-----------------------+----------------------------------------------------------------------------+

..  |br| raw:: html

  <br />