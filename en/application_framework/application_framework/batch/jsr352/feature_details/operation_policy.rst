Operation Policy
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

In JSR352-compliant batch applications, fault monitoring and a log output policy in accordance with the following policies is recommended.

* Perform :ref:`jsr352-failure_monitoring` with the batch exit status.
* Outputs logs for operators for recovery when an expected failure occurs, such as when the imported file does not exist.
* Outputs all logs for investigation when an unexpected failure occurs, such as application failures. 
  For log output when an exception occurs, see :ref:`jsr352-batch_error_flow` .
* Outputs a progress log to predict the end time when the batch process is delayed.

The following advantages are obtained by following these policies.
In other words, it increases the possibility that operators alone can respond to failures and customer inquiries, and can be expected to reduce the operational burden on developers.

* If the recovery procedure is output to the log for the operators when a failure occurs, the operator can perform the recovery.
* Output of the progress log eliminates the need for the developer to check the progress status by other means, and the operator can reply to the customer about the expected end time by referring to the progress log.

.. important::

  Batch designers should design batches by identifying expected failures and their measures, and output them to the log for the :doc:`Logs for operator<operator_notice_log>` .

Reference image for log when a failure is detected
  .. image:: ../images/operation-image.png

Reference image for log when the batch process is delayed
  .. image:: ../images/progress-image.png

.. _jsr352-failure_monitoring:

Fault monitoring
-----------------------------
Performs fault monitoring based on the batch exit status. 
Refer to the log for detailed information.

Normal complete
  Indicates that the batch process has been completed normally.

Abnormal end
  Indicates that the batch completed abnormally for some reason, and subsequent jobs cannot be executed. 
  Operators should refer to the log and take appropriate action.

End with warning
  Indicates that a problem has occurred during batch execution, but subsequent jobs can be executed. 
  Operators should refer to the log and check the details of the problem that occurred.
  
For details on the exit status of the batch application (return code returned from the Java operation), see :java:extdoc:`JobExecutor <nablarch.fw.batch.ee.JobExecutor>` and :java:extdoc:`Main <nablarch.fw.batch.ee.Main>` .

.. tip::

  To classify the exit code in more detail than mentioned above, create a launch class (Main).

Log output policy
-------------------------------

Logs for operator
  Outputs a message describing the failure that has occurred and the measures.
  The operator responds to the failure based on the information output to this log.
  Detailed information (stack trace) is not output because this information is not required by the operator.
  For details, see  :doc:`operator_notice_log` .

Progress log
  Outputs the state of progress for the batch process.
  If the batch process is delayed, estimates the end of the current operation based on this log and determine whether to continue or end the process.
  For details, see :doc:`progress_log` .

All logs
  Outputs all logs except for ``the Progress log`` . 
  Detailed information (stack trace) on ``Logs for operator`` is also output to this log.


