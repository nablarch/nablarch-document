.. _db_messaging-error_processing:

Error Handling for Messaging Which Uses Database as Queue
===========================================================

.. _db_messaging-exclude_error_data:

Exclude error data and continue processing
--------------------------------------------------
The exclusion of error data is done by the callback method (:java:extdoc:`transactionFailure <nablarch.fw.action.BatchActionBase.transactionFailure(D-nablarch.fw.ExecutionContext)>`) when an exception occurs.

.. important::
  If the error data is not excluded, the data containing errors gets extracted again and exceptions reoccur.
  (basically, the result will be the same for the same data processed with the same conditions.)
  The error data is repeatedly processed if it is not excluded and other data is not processed causing failures (delay failure for example).

An implementation example is shown below.

.. code-block:: java

    @Override
    protected void transactionFailure(SqlRow inputData, ExecutionContext context) {
      // Since inputData is the data that is input when an error occurrs,
      // Using this information, the corresponding record is updated to a non-processing target
      // (for example, a processing failure status, etc.).
    }

.. _db_messaging-process_abnormal_end:

Terminate the process abnormally
--------------------------------------------------
To terminate the process abnormally, throws :java:extdoc:`ProcessAbnormalEnd <nablarch.fw.launcher.ProcessAbnormalEnd>`.

.. important::
  Since the monitoring process of the table queue is terminated when the process is abnormally terminated, it causes unprocessed data to pile on, delaying capture of data.
  Continuation of the process using :ref:`exclude error data <db_messaging-exclude_error_data>` is recommended to avoid this problem instead of terminating the process abnormally.

An implementation example is shown below.

.. code-block:: java

  @Override
  public Result handle(SqlRow inputData, ExecutionContext ctx) {

    if (isAbnormalEnd(inputData)) {
      // In the case of abnormal termination, throws ProcessAbnormalEnd.
      throw new ProcessAbnormalEnd(100, "sample_process_failure");
    }

    return new Result.Success();
  }
