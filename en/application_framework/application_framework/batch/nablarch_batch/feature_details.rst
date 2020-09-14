Details of Function
========================================
.. contents:: Table of contents
  :depth: 3
  :local:

How to launch the batch application
--------------------------------------------------
* :ref:`How to launch a Nablarch batch application<main-run_application>`

Initializing the system repository
--------------------------------------------------
The system repository is initialized by specifying the path of the system repository configuration file
when the application starts. For more information, see :ref:`How to launch a Nablarch batch application<main-run_application>`.

Input value check
--------------------------------------------------
* :ref:`Input value check <validation>`

Database access
--------------------------------------------------
* :ref:`Database access <database_management>`
* Data reader provided as standard

  * :java:extdoc:`DatabaseRecordReader (read database) <nablarch.fw.reader.DatabaseRecordReader>`

File I/O
--------------------------------------------------
* :ref:`File I/O<data_converter>`

* Data reader provided as standard

  * :java:extdoc:`FileDataReader (read file)<nablarch.fw.reader.FileDataReader>`
  * :java:extdoc:`ValidatableFileDataReader (read files with validation function)<nablarch.fw.reader.ValidatableFileDataReader>`
  * :java:extdoc:`ResumeDataReader (read with resume function)<nablarch.fw.reader.ResumeDataReader>`

Exclusive control
--------------------------------------------------
.. toctree::
    :maxdepth: 1
    :hidden:

    feature_details/nablarch_batch_pessimistic_lock

Although 2 types of exclusive control are offered,
:ref:`universal_dao` is recommended due to the reasons described in
:ref:`Why UniversalDao is recommended<exclusive_control-deprecated>`.

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`Pessimistic lock<nablarch_batch_pessimistic_lock>`

Execution control of batch process
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_error_process
  feature_details/nablarch_batch_retention_state

* :ref:`Process exit code of batch process<status_code_convert_handler-rules>`
* :ref:`Error handling of batch process<nablarch_batch_error_process>`
* :ref:`Parallel execution of batch process (multi-threading)<multi_thread_execution_handler>`
* :ref:`Controlling the commit interval for batch process<loop_handler-commit_interval>`
* :ref:`Limit the number of processes in one batch process<data_read_handler-max_count>`
  |br| (For example, when the batch process for processing large amounts of data is split into several days and processed)

Send MOM message
----------------------------------------
* :ref:`Sending synchronous message<mom_system_messaging-sync_message_send>`
* :ref:`Sending asynchronous message<mom_system_messaging-async_message_send>`

Maintain state during batch execution
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_retention_state

* :ref:`nablarch_batch_retention_state`

Multi-processing of resident batch
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_multiple_process
  
* :ref:`nablarch_batch_multiple_process`

.. |br| raw:: html

  <br />
