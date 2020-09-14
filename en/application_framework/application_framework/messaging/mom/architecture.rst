Architecture Overview
==============================

.. contents:: Table of contents
  :depth: 3
  :local:

MOM messaging provides a function to execute an action corresponding to the request ID for request messages sent from the outside. 
The message queue used for MOM messaging is referred to as MQ.

MOM messaging is divided into two types:

Synchronous response messaging
 A response message is created for the request message and sent to MQ based on the execution result of business processing. 
 Used when an immediate response is required, such as for permission business.

Asynchronous response messaging
 The response message is not sent, and the request message contents received from MQ are stored in a table in the DB.
 Business process is executed by a subsequent batch using this table as the input.
 For information on batch, see :ref:`db_messaging`.

.. tip::
 Asynchronous response messaging is a very simple process of storing the contents of messages in a table, 
 so the action class provided by the framework can be used without any change. 
 In that case, only the required configuration needs to be configured, and coding is not required.

.. important::

  Only fixed-length data of :ref:`data_format` can be handled by MOM messaging.

MOM messaging uses the MOM messaging function of the library to send and receive messages. 
For details, see :ref:`mom_system_messaging` .

Configure MOM messaging
------------------------------------------------------
The configuration of MOM messaging is exactly the same as :ref:`nablarch_batch`. 
See :ref:`nablarch_batch-structure` .

Specify action and request ID based on the request message
------------------------------------------------------------------
MOM messaging uses a specified field in the request message as the request ID. 
Since the request ID does not include a hierarchical structure unlike request paths of web applications, 
use :ref:`request_path_java_package_mapping` to specify the action class package and class name suffix in the configuration, 
and dispatch it to the class corresponding to the request ID.

The request ID must be included in the framework control header in the request message. 
For details, see  :ref:`framework control header <mom_system_messaging-fw_header>` .

Process flow of MOM messaging
------------------------------------------------------
The process flow of MOM messaging, from receiving a request message to returning a response message, is shown below. 
The only difference with asynchronous response messaging is that no response message is returned.

.. image:: images/mom_messaging-flow.png
  :scale: 80

1. The :ref:`common start-up launcher (Main) <main>` executes the handler queue.
2. The data reader (:java:extdoc:`FwHeaderReader<nablarch.fw.messaging.reader.FwHeaderReader>`
   /
   :java:extdoc:`MessageReader<nablarch.fw.messaging.reader.MessageReader>`) monitors the message queue, reads the received messages, and provides request messages one by one.
3. The :ref:`nablarch_batch-structure` configured in the handler queue specifies the action class to be processed based on the request ID included in the specified field of the request message, and adds it to the end of the handler queue.
4. The action class executes business logic for each request message using a form class and an entity class.
5. The action class returns :java:extdoc:`ResponseMessage <nablarch.fw.messaging.ResponseMessage>` , which represents the response message.  
6. Steps 2 to 5 are repeated until there is a process stop request.
7. :java:extdoc:`status code → process exit code conversion handler (StatusCodeConvertHandler) <nablarch.fw.handler.StatusCodeConvertHandler>`  set in the handler queue converts the status code of the process result into the process exit code,
   and the process exit code is returned as the processing result of MOM messaging.

Handlers used in MOM messaging
------------------------------------------------------
Nablarch provides several handlers as standard, which are required for building MOM messaging. 
Build the handler queue in accordance with the requirements of the project (a custom handler will have to be created for the project depending on the requirements)

For details of each handler, refer to the link.

Handlers that convert request and response
  * :ref:`status_code_convert_handler`
  * :ref:`data_read_handler`

Handlers that control process execution
  * :ref:`duplicate_process_check_handler`
  * :ref:`multi_thread_execution_handler`
  * :ref:`retry_handler`
  * :ref:`request_thread_loop_handler`
  * :ref:`process_stop_handler`
  * :ref:`request_path_java_package_mapping`

Handlers associated with messaging
  * :ref:`messaging_context_handler`
  * :ref:`message_reply_handler`
  * :ref:`message_resend_handler`


Handlers associated with database
  * :ref:`database_connection_management_handler`
  * :ref:`transaction_management_handler`

Error handling handler
  * :ref:`global_error_handler`

Others
  * :ref:`thread_context_handler`
  * :ref:`thread_context_clear_handler`
  * :ref:`ServiceAvailabilityCheckHandler`


.. _mom_messaging-sync_receive_handler_que:

Minimum handler configuration for synchronous response messaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When building a synchronous response messaging, the minimum required handler queue is as below.
With this as the base, add standard handlers of Nablarch or custom handlers created in the project according to the project requirements.

.. list-table:: Minimum handler configuration for synchronous response messaging
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
     - :ref:`global_error_handler`
     - Main
     -
     -
     - Outputs the log for a runtime exception or error.

   * - 3
     - :ref:`multi_thread_execution_handler`
     - Main
     - Creates a sub-thread and executes the process of the subsequent handler in parallel.
     - Waits for normal termination of all threads.
     - Waits for the current thread to complete and rethrows the cause exception.

   * - 4
     - :ref:`retry_handler`
     - Sub
     -
     -
     - Catches a runtime exception that can be retried, and provided that the retry limit has not been reached, re-executes the subsequent handler.

   * - 5
     - :ref:`messaging_context_handler`
     - Sub
     - Acquires MQ connection.
     - Releases the MQ connection.
     -

   * - 6
     - :ref:`database_connection_management_handler`
     - Sub
     - Acquires DB connection.
     - Releases the DB connection.
     -

   * - 7
     - :ref:`request_thread_loop_handler`
     - Sub
     - Executes subsequent handlers repeatedly.
     - Restores the handler queue contents and continues the loop.
     - Stops the loop only when there is a process stop request or a fatal error occurs.

   * - 8
     - :ref:`thread_context_clear_handler`
     - Sub
     - 
     - Deletes all the values configured on the thread local by the :ref:`thread_context_handler` .
     -
     
   * - 9
     - :ref:`thread_context_handler`
     - Sub
     - Initializes thread context variables such as request ID and user ID from command line arguments.
     -
     -

   * - 10
     - :ref:`process_stop_handler`
     - Sub
     - If the process stop flag of the request table is on, a process stop exception (:java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`) is thrown without performing the subsequent handler process.
     -
     -

   * - 11
     - :ref:`message_reply_handler`
     - Sub
     -
     - Creates messages based on the content of response messages returned from the subsequent handlers and sends it to MQ.
     - Creates messages based on the content of the errors and sends it to MQ.

   * - 12
     - :ref:`data_read_handler`
     - Sub
     - Use a data reader to read one request message and pass it as an argument of the subsequent handler. 
       Also, the :ref:`execution ID numbered <log-execution_id>` is numbered.
     -
     - After generating output of the read message as a log, rethrows the original exception.

   * - 13
     - :ref:`request_path_java_package_mapping`
     - Sub
     - Determines the action to call based on the request ID included in request messages.
     -
     -

   * - 14
     - :ref:`transaction_management_handler`
     - Sub
     - Begin a transaction
     - Commits the transaction.
     - Rolls back a transaction.


.. _mom_messaging-async_receive_handler_que:

Minimum handler configuration for asynchronous response messaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When building a asynchronous response messaging, the minimum required handler queue is as below.
With this as the base, add standard handlers of Nablarch or custom handlers created in the project according to the project requirements.

The minimum handler configuration for asynchronous response messaging is the same as synchronous response messaging, except for the following handlers.

* :ref:`message_reply_handler`
* :ref:`message_resend_handler`

.. important::
 An error response cannot be sent if the storage of messages fails in asynchronous response messaging. 
 Hence, the message is returned to the queue temporarily and retried until the predetermined number of times is reached. 
 For this reason, the registration process for the DB and queue operation must be handled as one transaction (two-phase commit control). 
 Specifically, change the configuration of :ref:`transaction_management_handler` and replace with implementation that supports two-phase commit.

 Nablarch provides an adapter for two-phase commit using WebSphere MQ. 
 For details, see :ref:`webspheremq_adaptor` .

.. list-table:: Minimum handler configuration for asynchronous response messaging
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
     - :ref:`global_error_handler`
     - Main
     -
     -
     - Outputs the log for a runtime exception or error.

   * - 3
     - :ref:`multi_thread_execution_handler`
     - Main
     - Creates a sub-thread and executes the process of the subsequent handler in parallel.
     - Waits for normal termination of all threads.
     - Waits for the current thread to complete and rethrows the cause exception.

   * - 4
     - :ref:`retry_handler`
     - Sub
     -
     -
     - Catches a runtime exception that can be retried, and provided that the retry limit has not been reached, re-executes the subsequent handler.

   * - 5
     - :ref:`messaging_context_handler`
     - Sub
     - Acquires MQ connection.
     - Releases the MQ connection.
     -

   * - 6
     - :ref:`database_connection_management_handler`
     - Sub
     - Acquires DB connection.
     - Releases the DB connection.
     -

   * - 7
     - :ref:`request_thread_loop_handler`
     - Sub
     - Executes subsequent handlers repeatedly.
     - Restores the handler queue contents and continues the loop.
     - Stops the loop only when there is a process stop request or a fatal error occurs.

   * - 8
     - :ref:`thread_context_clear_handler`
     - Sub
     - 
     - Deletes all the values configured on the thread local by the :ref:`thread_context_handler` .
     -
     
   * - 9
     - :ref:`thread_context_handler`
     - Sub
     - Initializes thread context variables such as request ID and user ID from command line arguments.
     -
     -

   * - 10
     - :ref:`process_stop_handler`
     - Sub
     - If the process stop flag of the request table is on, a process stop exception (:java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`) is thrown without performing the subsequent handler process.
     -
     -

   * - 11
     - :ref:`transaction_management_handler`
     - Sub
     - Begin a transaction
     - Commits the transaction.
     - Rolls back a transaction.

   * - 12
     - :ref:`data_read_handler`
     - Sub
     - Use a data reader to read one request message and pass it as an argument of the subsequent handler. 
       Also, the :ref:`execution ID numbered <log-execution_id>` is numbered.
     -
     - After generating output of the read message as a log, rethrows the original exception.

   * - 13
     - :ref:`request_path_java_package_mapping`
     - Sub
     - Determines the action to call based on the request ID included in request messages.
     -
     -


.. _mom_messaging-data_reader:

Data readers used in MOM messaging
------------------------------------------------------
Nablarch provides several data readers as standard, which are required for building MOM messaging. 
For details of each data reader, refer to the respective links.

* :java:extdoc:`FwHeaderReader (reads the framework control header from the message) <nablarch.fw.messaging.reader.FwHeaderReader>`
* :java:extdoc:`MessageReader (reads messages from MQ)<nablarch.fw.messaging.reader.MessageReader>`

.. tip::
  If the above data readers cannot meet the project requirements, create a class that implements the :java:extdoc:`DataReader <nablarch.fw.DataReader>` interface in the project.


.. _mom_messaging-action:

Action used in MOM messaging
---------------------------------------------------------------------------------
Nablarch provides several action classes as standard, which are required for building MOM messaging. 
For details of each action class, refer to the respective links.

* :java:extdoc:`MessagingAction (Template class for actions for synchronous response messaging)<nablarch.fw.messaging.action.MessagingAction>`
* :java:extdoc:`AsyncMessageReceiveAction (Template class for actions for asynchronous response messaging)<nablarch.fw.messaging.action.AsyncMessageReceiveAction>`
