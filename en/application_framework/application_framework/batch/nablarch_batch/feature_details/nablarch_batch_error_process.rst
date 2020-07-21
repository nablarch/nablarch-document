.. _nablarch_batch_error_process:

Error Handling of Nablarch Batch Applications
============================================================
.. contents:: Table of contents
  :depth: 3
  :local:

.. _nablarch_batch_error_process-rerun:

Enables rerun of batch processing
--------------------------------------------------
Nablarch batch application does not provide a function to re-run the batch process
except for file input.

Design and implementation is necessary in applications that allow the status to be held
in a record for process target and modify the status when a process is successful or fails.
See :ref:`loop_handler-callback` for the implementation method to modify the status
during success or failure of the process.

For file input, re-execution from the point of failure is possible by using
:java:extdoc:`ResumeDataReader (read with resume function)<nablarch.fw.reader.ResumeDataReader>`.

.. _nablarch_batch_error_process-continue:

Continue the process even when there is an error in the batch process.
----------------------------------------------------------------------------------------------------
Continuation of the process even when there an error,
is supported only for :ref:`resident batch<nablarch_batch-resident_batch>`.
:ref:`On-demand batch<nablarch_batch-on-demand_batch>` is not supported.

If :java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
is thrown in :ref:`resident batch<nablarch_batch-resident_batch>`,
the process is continued by retry_handler.
However, it is necessary to be able to re-run the batch process with the contents
described in :ref:`nablarch_batch_error_process-rerun`.

.. tip::
 If :java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
 is thrown in :ref:`on-demand batch<nablarch_batch-on-demand_batch>`,
 the batch process is terminated abnormally.

.. _nablarch_batch_error_process-abnormal_end:

Abnormal termination of batch process
--------------------------------------------------
When an error detected in the application, it might be necessary to stop continuing
the batch process and abnormally terminate the process.

In Nablarch batch application, the batch process can be abnormally terminated by throwing
:java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`.
When :java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`
is thrown, the process exit code value is as specified by this class.


