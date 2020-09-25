Output of Logs for Operator
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

Contents of output of logs for operator
--------------------------------------------
At least the following contents have to be output in the logs for operator so that the operator can respond based on the log.

* What has occurred?
* How to respond to it?

If these contents are not output, the operator may not be able to determine how to respond to the event that has occurred.

Add the configuration to output the logs for operator to a dedicated log file
---------------------------------------------------------------------------------
Output the logs for operator with the log category name as ``operator`` . 
By using this category name, the log can be output to the logs for operator file.

Shown below is an configuration example of ``log.properties`` when the :ref:`log` is used. 
When using :ref:`log_adaptor` , refer to the manual of the log library corresponding to the adapter to perform the configuration.

.. code-block:: properties

  # operation log file
  writer.operationLog.className=nablarch.core.log.basic.FileLogWriter
  writer.operationLog.filePath=./log/operation.log
  writer.operationLog.encoding=UTF-8
  writer.operationLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.operationLog.formatter.format=$date$ -$logLevel$- $message$

  # logger list
  availableLoggersNamesOrder=SQL,MON,OPERATOR,ROO

  # operation logger setting
  loggers.OPERATOR.nameRegex=operator
  loggers.OPERATOR.level=INFO
  loggers.OPERATOR.writerNames=operationLog

Log output to the operator
--------------------------------------------------

An implementation example for output of the logs for operator is shown below.

Point
  * Output the log using  :java:extdoc:`OperationLogger#write <nablarch.core.log.operation.OperationLogger.write(nablarch.core.log.basic.LogLevel-java.lang.String-java.lang.Throwable)>`.
  * An exception must throw to abnormally end the batch process as well as the log output to the operator.

Implementation examples
  .. code-block:: java

    @Named
    @Dependent
    public class SampleBatchlet extends AbstractBatchlet {

        @Override
        public String process() throws Exception {

            try {
                // Omitted
            } catch (FileNotFoundException e) {
                // Notifies the operator that the input file is not found and throws an exception
                OperationLogger.write(
                        LogLevel.ERROR,
                        "File does not exist. Check that you have received the correct file." ,
                        e);
                throw e;
            }

            // Omitted
        }
    }

Output example
  .. code-block:: bash

    ERROR operator file does not exist. Check that you have received the correct file.

