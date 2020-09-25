.. _`batch-functional_comparison`:

Function Comparison Between JSR-compliant Batch Application and Nablarch Batch Application
----------------------------------------------------------------------------------------------------
This section compares the following features:

* :doc:`jsr352/index`
* :doc:`nablarch_batch/index`

.. list-table:: Function comparison (JSR: Defined in JSR specifications A: Provided B: Partially provided C: Not provided D: Not applicable)
  :header-rows: 1
  :class: white-space-normal
  :widths: 30 35 35

  * - Function
    - Compliant with JSR352 [#jsr]_
    - Nablarch batch

  * - Arbitrary parameters can be configured at startup
    - JSR
    - A |br| :ref:`To the manual <main-option_parameter>`

  * - Simultaneous execution of the same batch applications can be prevented
    - A |br| :java:extdoc:`To Javadoc <nablarch.fw.batch.ee.listener.job.DuplicateJobRunningCheckListener>`
    - A |br| :ref:`To the manual <duplicate_process_check_handler>`

  * - Batch applications that are running, can be safely stopped from the outside
    - JSR
    - A |br| :ref:`To the manual <process_stop_handler>`

  * - The maximum number of records to be processed in one execution can be specified.
    - C |br| [#jsr_max]_
    - A |br| :ref:`To the manual <data_read_handler-max_count>`

  * - A fixed number of record units can be committed
    - JSR
    - A |br| :ref:`To the manual <loop_handler-commit_interval>`

  * - Can re-run from the point of failure
    - JSR
    - B |br| [#resumable]_

  * - Business processes can be executed in parallel by multiple threads
    - JSR
    - A |br| :ref:`To the manual <multi_thread_execution_handler>`

  * - Processing can be continued ignoring specific exceptions (processing can be continued after rollback)
    - JSR
    - C |br| [#skip_exception]_

  * - Processing can be retried when a specific exception occurs
    - JSR
    - B |br| [#retry_exception]_

  * - The process to be executed next can be switched based on the batch application result
    - JSR
    - C |br| [#branch_batch]_

  * - Batches can be executed by monitoring input data sources at regular intervals
    - C [#resident_batch]_
    - A |br| :ref:`To the manual <nablarch_batch-resident_batch>`


.. [#jsr]
  JSR parts are in accordance with the specifications defined in JSR352.
  For details, refer to the specification of `JSR352 (external site) <https://jcp.org/en/jsr/detail?id=352>`_.

.. [#jsr_max]
  The property to specify the maximum number to read in a single run
  can be included in the implementation class :java:extdoc:`ItemReader <javax.batch.api.chunk.ItemReader>`.

.. [#resumable]
  Re-execution from the point of failure is possible by using
  :java:extdoc:`ResumeDataReader (read with resume function)<nablarch.fw.reader.ResumeDataReader>`.
  However, this feature is available only when a file is input.
  When other data is input, design and implementation are required in the application.

.. [#skip_exception]
  Add a handler to continue processing ignoring specific exceptions.

.. [#retry_exception]
  :ref:`retry_handler` retries for exceptions that can be retried,
  but a simple retry cannot be performed for data where an exception has occurred,
  as in JSR352. Exceptions to be retried cannot be specified flexibly with :ref:`retry_handler`.

  If the requirements cannot be met with the :ref:`retry_handler`
  (simple retry of the data where the exception occurred or to specify the exception flexibly),
  provide support by adding a handler.

.. [#branch_batch]
  Use a job scheduler, etc. For example, taking measures such as switching the job
  to be executed next based on the exit code will be necessary.

.. [#resident_batch]
  In JSR352-compliant batch applications, it is not possible to realize a batch process
  for monitoring an input data source at regular intervals.
  For this reason, if such a batch application is necessary,
  realize using  :ref:`the resident batch of Nablarch batch application <nablarch_batch-resident_batch>`.

.. |br| raw:: html

  <br />

