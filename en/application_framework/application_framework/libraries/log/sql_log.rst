.. _sql_log:

Output of SQL Log
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

The SQL log outputs the execution time of SQL statements and the SQL statements for use in performance tuning.
The log is output in the application by configuring the log output.

Output of SQL log policy
--------------------------------------------------
SQL logs may become very large resulting in disc becoming full or affecting the performance.
It is assumed that the SQL log will be used during development and the output is limited to DEBUG level or lower.

.. list-table:: Output of SQL log policy
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15,70

   * - Log level
     - Logger name
     - Output contents

   * - DEBUG
     - SQL
     - SQL statement, execution time, number of records (number of searches and updates), transaction process result (commit or rollback)

   * - TRACE
     - SQL
     - SQL parameter (bind variable value)

A configuration example of the log output for the above mentioned output policy is shown below.

Configuration example of log.properties
 .. code-block:: properties

  writerNames=appLog

  # Output destination of the application log
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=SQL,ROO

  # Configure the application log
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # Configure the SQL log
  loggers.SQL.nameRegex=SQL
  loggers.SQL.level=TRACE
  loggers.SQL.writerNames=appLog

Configuration example of app-log.properties
 .. code-block:: properties

  # SqlLogFormatter
  #sqlLogFormatter.className=
  # The format of SqlPStatement#retrieve
  sqlLogFormatter.startRetrieveFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tstart_position = [$startPosition$] size = [$size$]\
                                        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]
  # The format of SqlPStatement#execute
  sqlLogFormatter.startExecuteFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$]
  # The format of SqlPStatement#executeQuery
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$]
  # The format of SqlPStatement#executeUpdate
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\
                                              \n\tSQL = [$sql$]\
                                              \n\tadditional_info:\
                                              \n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]
  # The format of SqlStatement#executeBatch
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

How to use
--------------------------------------------------

.. _sql_log-setting:

Configure the SQL log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The SQL log is configured in the property file described in :ref:`log-app_log_setting`.

Description rules
 \

 sqlLogFormatter.className
  Class that implements sqlLogFormatter.className :java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>`.
  Specify to replace.

 sqlLogFormatter.startRetrieveFormat
  Format used at the start of
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :SQL statement: $sql$
   :Acquire start position: $startPosition$
   :Acquisition maximum count: $size$
   :Timeout time: $queryTimeout$
   :Number of rows to fetch: $fetchSize$
   :Additional information: $additionalInfo$

  Default format
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tstart_position = [$startPosition$] size = [$size$]
        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endRetrieveFormat
  Format used at the end of
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :Execution time: $executeTime$
   :Data acquisition time: $retrieveTime$
   :Search count: $count$

  Default format
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]

 sqlLogFormatter.startExecuteFormat
  Format used at the start of
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :SQL statement: $sql$
   :Additional information: $additionalInfo$

  Default format
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteFormat
  Format used at the end of
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :Execution time: $executeTime$

  Default format
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteQueryFormat
  Format used at the start of
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :SQL statement: $sql$
   :Additional information: $additionalInfo$

  Default format
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteQueryFormat
  Format used at the end of
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :Execution time: $executeTime$

  Default format
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteUpdateFormat
  Format used at the start of
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :SQL statement: $sql$
   :Additional information: $additionalInfo$

  Default format
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteUpdateFormat
  Format used at the end of
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :Execution time: $executeTime$
   :Update count: $updateCount$

  Default format
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]

 sqlLogFormatter.startExecuteBatchFormat
  Format used at the start of
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :SQL statement: $sql$
   :Additional information: $additionalInfo$

  Default format
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteBatchFormat
  Format used at the end of
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`.

  Placeholders that can be specified for the format
   :Method name: $methodName$
   :Execution time: $executeTime$
   :Batch count: $batchCount$

  Default format
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

Example of the description
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlLogFormatter
  sqlLogFormatter.startRetrieveFormat=$methodName$\n\tSQL:$sql$\n\tstart:$startPosition$ size:$size$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\n\texe:$executeTime$ms ret:$retrieveTime$ms count:$count$
  sqlLogFormatter.startExecuteFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$

.. _sql_log-json_setting:

Output as a structured log in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Logs can be output in JSON format by using :ref:`log-json_log_setting` setting, but :java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>` outputs each item of the sql log as a string in the message value.

To output each item in the sql log as a JSON value as well, use the :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>`.
You can configure in the property file described in :ref:`log-app_log_setting`.

Description rules
 The properties to be specified when using :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` are as follows.
 
 sqlLogFormatter.className ``required``
  To output logs in JSON format, specify :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>`.

 sqlLogFormatter.startRetrieveTargets
  Items used at the start of :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`.
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :SQL statement: sql
   :Acquire start position: startPosition
   :Acquisition maximum count: size
   :Timeout time: queryTimeout
   :Number of rows to fetch: fetchSize
   :Additional information: additionalInfo
 
  All items are output in default.

 sqlLogFormatter.endRetrieveTargets
  Items used at the end of :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`.
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :Execution time: executeTime
   :Data acquisition time: retrieveTime
   :Search count: count

  All items are output in default.

 sqlLogFormatter.startExecuteTargets
  Items used at the start of  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :SQL statement: sql
   :Additional information: additionalInfo

  All items are output in default.

 sqlLogFormatter.endExecuteTargets
  Items used at the end of :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :Execution time: executeTime

  All items are output in default.

 sqlLogFormatter.startExecuteQueryTargets
  Items used at the start of :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :SQL statement: sql
   :Additional information: additionalInfo

  All items are output in default.

 sqlLogFormatter.endExecuteQueryTargets
  Items used at the end of :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :Execution time: executeTime

  All items are output in default.

 sqlLogFormatter.startExecuteUpdateTargets
  Items used at the start of :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :SQL statement: sql
   :Additional information: additionalInfo

  All items are output in default.

 sqlLogFormatter.endExecuteUpdateTargets
  Items used at the end of :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :Execution time: executeTime
   :Update count: updateCount

  All items are output in default.

 sqlLogFormatter.startExecuteBatchTargets
  Items used at the start of :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :SQL statement: sql
   :Additional information: additionalInfo

  All items are output in default.

 sqlLogFormatter.endExecuteBatchTargets
  Items used at the end of :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  Separated by comma.

  Output items that can be specified
   :Method name: methodName
   :Execution time: executeTime
   :Batch count: batchCount

  All items are output in default.

 sqlLogFormatter.structuredMessagePrefix
  A marker string given at the beginning of a message to identify that the message string after formatting has been formatted into JSON format.
  If this marker is present at the beginning of the message, :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` processes the message as JSON data.
  The default is ``"$JSON$"``.

Example of the description
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlJsonLogFormatter
  sqlLogFormatter.structuredMessagePrefix=$JSON$
  sqlLogFormatter.startRetrieveTargets=methodName,sql,start,startPosition,size,additionalInfo
  sqlLogFormatter.endRetrieveTargets=methodName,executeTime,retrieveTime,count
  sqlLogFormatter.startExecuteTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteTargets=methodName,executeTime
  sqlLogFormatter.startExecuteQueryTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteQueryTargets=methodName,executeTime
  sqlLogFormatter.startExecuteUpdateTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteUpdateTargets=methodName,executeTime,updateCount
  sqlLogFormatter.startExecuteBatchTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteBatchTargets=methodName,executeTime,updateCount
