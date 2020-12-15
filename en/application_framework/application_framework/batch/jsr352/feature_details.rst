Details of Function
========================================
.. contents:: Table of contents
  :depth: 3
  :local:

How to launch the batch application
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/run_batch_application

* :ref:`How to launch the JSR352 batch application <jsr352_run_batch_application>`

Initializing the system repository
--------------------------------------------------
* :ref:`Initializing the system repository with the JSR352 batch application <jsr352_run_batch_init_repository>`

How to define a listener for application to batch jobs
--------------------------------------------------------
* :ref:`How to define a listener <jsr352-listener_definition>`

Input value check
--------------------------------------------------
* :ref:`Input value check <validation>`

Database access
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/database_reader

* :ref:`Database access <database_management>`
* :doc:`feature_details/database_reader`



File I/O
--------------------------------------------------
* :ref:`File I/O<data_converter>`

Exclusive control
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/pessimistic_lock

Although 2 types of exclusive control are offered,
:ref:`universal_dao` is recommended
because of the :ref:`reasons for recommending UniversalDao <exclusive_control-deprecated>` .

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :doc:`Pessimistic lock<feature_details/pessimistic_lock>`

How to create xml for job definitions
--------------------------------------------------
* `See JSR352 Specification (external site) <https://jcp.org/en/jsr/detail?id=352>`_

Send MOM message
----------------------------------------
* :ref:`Sending synchronous message<mom_system_messaging-sync_message_send>`

Operation design
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/operation_policy
  feature_details/progress_log
  feature_details/operator_notice_log

* :doc:`feature_details/operation_policy`
* :doc:`feature_details/progress_log`
* :doc:`feature_details/operator_notice_log`

