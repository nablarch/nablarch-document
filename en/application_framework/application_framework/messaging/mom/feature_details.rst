Details of Function
========================================
.. contents:: Table of contents
  :depth: 3
  :local:

How to launch an application
--------------------------------------------------
* :ref:`How to launch an application<main-run_application>`

Initializing the system repository
--------------------------------------------------
The system repository is initialized by specifying the path of the system repository configuration file when the application starts. 
For more information, see :ref:`How to launch an application<main-run_application>` 

Database Access
--------------------------------------------------
* :ref:`Database Access <database_management>`

Input value check
--------------------------------------------------
* :ref:`Input value check <validation>`

Exclusive control
--------------------------------------------------
Although 2 types of exclusive control are offered, :ref:`universal_dao` is recommended due to the reasons described inreason :ref:`UniversalDao is recommended <exclusive_control-deprecated>` .

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_pessimistic_lock`

Execution control
--------------------------------------------------
* :ref:`Process exit code<status_code_convert_handler-rules>`
* :ref:`Returns an error response message when an error occurs <mom_system_messaging-sync_message_receive>`
* :ref:`Terminate the messaging process abnormally <db_messaging-process_abnormal_end>` (same as messaging using tables as queues)
* :ref:`Parallel execution of processing (multi-threading)<multi_thread_execution_handler>`

MOM messaging
--------------------------------------------------
* :ref:`mom_system_messaging`
* Data reader provided as standard

  * :java:extdoc:`FwHeaderReader (reads the framework control header from the message) <nablarch.fw.messaging.reader.FwHeaderReader>`
  * :java:extdoc:`MessageReader (reads messages from MQ)<nablarch.fw.messaging.reader.MessageReader>`

* :ref:`Resend control<message_resend_handler>`

.. _data_format-messaging-formatter:

Format the display format of the output data
--------------------------------------------------
When generating the output data, display format such as date and number of the data can be formatted by using :ref:`format` . 
For details, see :ref:`format` .
