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
* Data reader provided as standard

  * :java:extdoc:`DatabaseTableQueueReader (Reader that handles database tables as queues) <nablarch.fw.reader.DatabaseTableQueueReader>`

Input Value Check
--------------------------------------------------
* :ref:`Input Value Check <validation>`

Exclusive control
--------------------------------------------------
Although 2 types of exclusive control are offered, 
:ref:`universal_dao`  is recommended due to the reasons described inreason :ref:`UniversalDao is recommended <exclusive_control-deprecated>` .

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_pessimistic_lock`

Execution control
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/error_processing

* :ref:`Process exit code <status_code_convert_handler-rules>`
* :ref:`Exclude error data and continue processing <db_messaging-exclude_error_data>`
* :ref:`Abnormally terminate the messaging process <db_messaging-process_abnormal_end>`
* :ref:`Parallel execution of processing (multi-threading) <multi_thread_execution_handler>`

Multi-process
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/multiple_process

* :ref:`db_messaging-multiple_process`


