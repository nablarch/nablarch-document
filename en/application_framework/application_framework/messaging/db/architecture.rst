Architecture Overview
==============================
.. contents:: Table of contents
  :depth: 3
  :local:

The type of messaging process that treats a database as a queue provides the function to monitor tables on a database periodically and sequentially process records that are yet to be processed.

.. important::

  Determination of the record that are not processed should be displayed on the table record. For that reason, 
  it is necessary to perform the process of changing the status of the record for which processing is completed to processed

Configuration
--------------------------------------------------
It has the same structure as the Nablarch batch application. 
For details, see structure of :ref:`Nablarch batch application <nablarch_batch-structure>` 


Specify action and request ID based on request path
----------------------------------------------------------
For messaging process that treats the databases as a queues, 
specify the actions and request IDs to be executed using command line arguments as in the Nablarch batch application.

For details, see :ref:`specify nablarch batch application action and request id <nablarch_batch-resolve_action>` .

Process flow
------------------------------------------------------
The process flow is the same as the Nablarch batch application. For details, see :ref:`nablarch_batch-process_flow` .

Handler used
--------------------------------------------------------------------------
Nablarch provides several handlers as standard that are required for the messaging process that treats databases as a queues. 
Build the handler queue in accordance with the requirements of the project (a custom handler will have to be created for the project depending on the requirements)

For details of each handler, refer to the link.

Handlers that convert request and response
  * :ref:`status_code_convert_handler`
  * :ref:`data_read_handler`

Handlers that control execution
  * :ref:`duplicate_process_check_handler`
  * :ref:`request_path_java_package_mapping`
  * :ref:`multi_thread_execution_handler`
  * :ref:`retry_handler`
  * :ref:`process_stop_handler`
  * :ref:`request_thread_loop_handler`

Handlers associated with database
  * :ref:`database_connection_management_handler`
  * :ref:`transaction_management_handler`

Error handling handler
  * :ref:`global_error_handler`

Others
  * :ref:`thread_context_handler`
  * :ref:`thread_context_clear_handler`
  * :ref:`ServiceAvailabilityCheckHandler`
  * :ref:`file_record_writer_dispose_handler`

Minimum configuration of handler
--------------------------------------------------
The following shows the minimum required handler queue for messaging process that handles databases as queues. 
With this as the base, add standard handlers of Nablarch or custom handlers created in the project according to the project requirements.

.. list-table:: Minimum handler configuration
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,22,12,22,22,22

  * - No.
    - Handler
    - Thread
    - Request process
    - Response process
    - Exception handling

  * - 1
    - :ref:`status_code_convert_handler`
    - Main
    -
    - Converts the status code to process exit code.
    -
    
  * - 2
    - :ref:`thread_context_clear_handler`
    - Main
    - 
    - Deletes all the values configured on the thread local by the :ref:`thread_context_handler` .
    -

  * - 3
    - :ref:`global_error_handler`
    - Main
    -
    -
    - Outputs the log for a runtime exception or error.

  * - 4
    - :ref:`thread_context_handler`
    - Main
    - Initializes thread context variables such as request ID and user ID from command line arguments.
    -
    -

  * - 5
    - :ref:`retry_handler`
    - Main
    -
    -
    - Catches a runtime exception that can be retried, and provided that the retry limit has not been reached, re-executes the subsequent handler.

  * - 6
    - :ref:`database_connection_management_handler`
      (For initial processing/end processing)
    - Main
    - Acquires DB connection.
    - Releases the DB connection.
    -

  * - 7
    - :ref:`transaction_management_handler`
      (For initial processing/end processing)
    - Main
    - Begin a transaction
    - Commits the transaction.
    - Rolls back a transaction.

  * - 8
    - :ref:`request_path_java_package_mapping`
    - Main
    - Determine the action to call based on the command line arguments.
    -
    -

  * - 9
    - :ref:`multi_thread_execution_handler`
    - Main
    - Creates a sub-thread and executes the process of the subsequent handler in parallel.
    - Waits for normal termination of all threads.
    - Waits for the current thread to complete and rethrows the cause exception.

  * - 10
    - :ref:`database_connection_management_handler`
      (For business processing)
    - Sub
    - Acquires DB connection.
    - Releases the DB connection.
    -

  * - 11
    - :ref:`request_thread_loop_handler`
    - Sub
    -
    - Delegates the process to the subsequent handler again.
    - Performs the log output process and resend according to the exception/error.

  * - 12
    - :ref:`process_stop_handler`
    - Sub
    - If the process stop flag of the request table is on, a process stop exception (:java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`) is thrown without performing the subsequent handler process.
    -
    -

  * - 13
    - :ref:`data_read_handler`
    - Sub
    - Use a data reader to read records one by one and pass it as an argument of the subsequent handler. 
      Also, the :ref:`execution ID numbered <log-execution_id>`  is numbered.
    -
    - After generating output of the read record as a log, rethrows the original exception.

  * - 14
    - :ref:`transaction_management_handler`
      (for business processing)
    - Sub
    - Begin a transaction
    - Commits the transaction.
    - Rolls back a transaction.

.. _db_messaging_architecture-reader:

Data reader used
----------------------------------------------------------------------------------------------------
Use the following data reader to handle a database as a queue. 
Note that the the table cannot be monitored repeatedly if :java:extdoc:`batch DatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>` is used.

* :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>`

.. important::

  If the requirements cannot be satisfied with the above mentioned reader, then the reader has to be created in the project based on the following points.

  * Even if the target data disappears, the reader should be able to continuously monitor the target data.
  * When used in a multithreaded environment, prevent the same data from being processed by multiple threads.

   :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>`  is implemented as given below to satisfy the above criteria

  * When there is no unprocessed data in the table, executes the search SQL again to extract the unprocessed data.
  * To ensure that multiple threads are not processing the same data, holds the identifier (primary key value) of the data currently being processed and reads data that has not been processed.


Template class of the action to use
---------------------------------------------------------------------------------
Use the following template class to handle a database as a queue.

* :java:extdoc:`BatchAction (generic batch action)<nablarch.fw.action.BatchAction>`

