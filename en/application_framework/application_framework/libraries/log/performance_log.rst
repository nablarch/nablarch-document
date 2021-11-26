.. _performance_log:

Output of Performance Log
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Performance log outputs the execution time and memory usage corresponding to an arbitrary process range and is used for performance tuning during development. 
The application calls the API provided by the framework in the source code and tracks the output after specifying the process range for measurement.

Output policy of performance log
--------------------------------------------------
Performance logs can affect performance such as acquiring the heap size, etc. 
It is assumed that the performance log will be used during development and output is limited to the DEBUG level.

.. list-table:: Output policy of performance log
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - Log level
     - Logger name

   * - DEBUG
     - PERFORMANCE

A configuration example of the log output for the above mentioned output policy is shown below

Configuration example of log.properties
 .. code-block:: properties

  writerNames=appLog

  # Output destination of application log
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=PER,ROO

  # Configure application log
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # Configure performance log
  loggers.PER.nameRegex=PERFORMANCE
  loggers.PER.level=DEBUG
  loggers.PER.writerNames=appLog

Configuration example of app-log.properties
 .. code-block:: properties

  # PerformanceLogFormatter
  #performanceLogFormatter.className=
  #performanceLogFormatter.targetPoints=
  #performanceLogFormatter.datePattern=
  performanceLogFormatter.format=\n\tpoint = [$point$] result = [$result$]\
                                 \n\tstart_time = [$startTime$] end_time = [$endTime$]\
                                 \n\texecution_time = [$executionTime$]\
                                 \n\tmax_memory = [$maxMemory$]\
                                 \n\tstart_free_memory = [$startFreeMemory$] start_used_memory = [$startUsedMemory$]\
                                 \n\tend_free_memory = [$endFreeMemory$] end_used_memory = [$endUsedMemory$]


How to use
--------------------------------------------------

.. _performance_log-logging:

Output performance log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Performance log is output using  :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` . 
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>`  provides :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>` which is called at the start of the process and  :java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String-java.lang.String-java.lang.Object...)>` which is called at the end of the process. 
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>`  will output the log together with the date and time and memory usage acquired by  :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>` when :java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String-java.lang.String-java.lang.Object...)>` is called.

Usage example of :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>`  is shown below.

.. code-block:: java

 // Specify the point that identifies the measurement target in the start method.
 // log is not output if this point name is not defined in the configuration file
 // to prevent unwanted output because of incorrect configuration.
 String point = "UserSearchAction#doUSERS00101";
 PerformanceLogUtil.start(point);

 // Search execution
 UserSearchService searchService = new UserSearchService();
 SqlResultSet searchResult = searchService.selectByCondition(condition);

 // In the end method, point, string indicating the process result and optional information of log output can be specified.
 // Optional information of the log output is not specified in the following.
 PerformanceLogUtil.end(point, String.valueOf(searchResult.size()));

.. important::
  :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` uniquely identifies the measurement target with the :ref:`execution ID <log-execution_id>`  + point name.
  Therefore, note that if  :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` is used during a recursive call, measurement cannot be performed.

.. _performance_log-setting:

Configure performance log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The performance log is configured in the property file described in :ref:`log-app_log_setting` .

Description rules
 \

 performanceLogFormatter.className
  Class that implements performanceLogFormatter.className :java:extdoc:`PerformanceLogFormatter <nablarch.core.log.app.PerformanceLogFormatter>` . 
  Specify to replace.

 performanceLogFormatter.format
  Format of individual items in the performance log.

  Placeholders that can be specified for the format
   :Measurement target identification ID: $point$
   :Character string that represents the process result.: $result$
   :Start date and time of process: $startTime$
   :End date and time of process: $endTime$
   :Execution time of the process (End date and time – Start date and time ): $executionTime$
   :Heap size at the start of the process: $maxMemory$
   :Free heap size at the start of the process: $startFreeMemory$
   :Used heap size used at the start of the process: $startUsedMemory$
   :Free heap size at the end of the process: $endFreeMemory$
   :Used heap size at the end of the process: $endUsedMemory$

  Default format
   .. code-block:: bash

    \n\tpoint = [$point$] result = [$result$]
    \n\tstart_time = [$startTime$] end_time = [$endTime$]
    \n\texecution_time = [$executionTime$]
    \n\tmax_memory = [$maxMemory$]
    \n\tstart_free_memory = [$startFreeMemory$] start_used_memory = [$startUsedMemory$]
    \n\tend_free_memory = [$endFreeMemory$] end_used_memory = [$endUsedMemory$]

 performanceLogFormatter.datePattern
  Date and time pattern to use for date and time of the start and end.
  For the pattern, specify the syntax specified by  :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` . 
  Default is "yyyy-MM-dd HH:mm:ss.SSS".

 performanceLogFormatter.targetPoints
  Point name to be output.
  If more than one is specified, separate them with commas.
  The performance log is output based on this configuration to prevent unwanted output because of incorrect configuration.

Example of the description
 .. code-block:: properties

  performanceLogFormatter.className=nablarch.core.log.app.PerformanceLogFormatter
  performanceLogFormatter.targetPoints=UserSearchAction#doUSERS00101
  performanceLogFormatter.datePattern=yyyy-MM-dd HH:mm:ss.SSS
  performanceLogFormatter.format=point:$point$ result:$result$ exe_time:$executionTime$ms

.. _performance_log-json_setting:

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定を行うことでログをJSON形式で出力できるが、
:java:extdoc:`PerformanceLogFormatter <nablarch.core.log.app.PerformanceLogFormatter>` では
障害ログの各項目はmessageの値に文字列として出力される。
障害ログの各項目もJSONの値として出力するには、
:java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` を使用する。
設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` を用いる際に
 指定するプロパティは以下の通り。
 
 performanceLogFormatter.className ``必須``
  JSON形式でログを出力する場合、
  :java:extdoc:`PerformanceJsonLogFormatter <nablarch.core.log.app.PerformanceJsonLogFormatter>` を指定する。

 performanceLogFormatter.targets
  パフォーマンスログの出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :測定対象を識別するID: point
   :処理結果を表す文字列: result
   :処理の開始日時: startTime
   :処理の終了日時: endTime
   :処理の実行時間(終了日時 - 開始日時): executionTime
   :処理の開始時点のヒープサイズ: maxMemory
   :処理の開始時点の空きヒープサイズ: startFreeMemory
   :処理の開始時点の使用ヒープサイズ: startUsedMemory
   :処理の終了時点の空きヒープサイズ: endFreeMemory
   :処理の終了時点の使用ヒープサイズ: endUsedMemory

  デフォルトは全ての出力項目が対象となる。

 performanceLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは”yyyy-MM-dd HH:mm:ss.SSS”。

 performanceLogFormatter.targetPoints
  出力対象とするポイント名。
  複数指定する場合はカンマ区切り。
  パフォーマンスログは、誤設定による無駄な出力を防ぐため、この設定に基づき出力する。

 performanceLogFormatter.structuredMessagePrefix
  フォーマット後のメッセージ文字列が JSON 形式に整形されていることを識別できるようにするために、メッセージの先頭に付与するマーカー文字列。
  メッセージの先頭にこのマーカーがある場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。

記述例
 .. code-block:: properties

  performanceLogFormatter.className=nablarch.core.log.app.PerformanceJsonLogFormatter
  performanceLogFormatter.structuredMessagePrefix=$JSON$
  performanceLogFormatter.targetPoints=UserSearchAction#doUSERS00101
  performanceLogFormatter.datePattern=yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
  performanceLogFormatter.targets=point,result,executionTime
