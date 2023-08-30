.. _http_access_log:

Output of HTTP Access Log
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

The HTTP access log is output using the handler provided by the framework.
The HTTP access log is output in the application by configuring the handler.

The handlers required to output the HTTP access log are as follows.

 :ref:`http_access_log_handler`
  Outputs the log at the start and end of the request process.

 :ref:`nablarch_tag_handler`
  Outputs the log after decrypting the hidden parameters.
  For hidden parameters, see :ref:`hidden encryption <tag-hidden_encryption>`.

 :ref:`http_request_java_package_mapping`
  Outputs the log after the dispatch class is determined.

If the requirements of the trace log of the individual application can be met by output of the request information including the request parameters,
then the HTTP access and trace logs can be used together.

Output policy of HTTP access log
--------------------------------------------------
The HTTP access log is output to an application log that outputs the log of the entire application.

.. list-table:: Output policy of HTTP access log
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - Log level
     - Logger name

   * - INFO
     - HTTP_ACCESS

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

  availableLoggersNamesOrder=ACC,ROO

  # Configuration of the application log
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # Configuration of HTTP access log
  loggers.ACC.nameRegex=HTTP_ACCESS
  loggers.ACC.level=INFO
  loggers.ACC.writerNames=appLog

Configuration example of app-log.properties
 .. code-block:: properties

  # HttpAccessLogFormatter
  #httpAccessLogFormatter.className=
  #httpAccessLogFormatter.datePattern=
  #httpAccessLogFormatter.maskingChar=
  #httpAccessLogFormatter.maskingPatterns=
  #httpAccessLogFormatter.parametersSeparator=
  #httpAccessLogFormatter.sessionScopeSeparator=
  #httpAccessLogFormatter.beginOutputEnabled=
  #httpAccessLogFormatter.parametersOutputEnabled=
  #httpAccessLogFormatter.dispatchingClassOutputEnabled=
  #httpAccessLogFormatter.endOutputEnabled=
  httpAccessLogFormatter.beginFormat=@@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]\
                                        \n\turl          = [$url$$query$]\
                                        \n\tmethod      = [$method$]\
                                        \n\tport        = [$port$]\
                                        \n\tclient_ip   = [$clientIpAddress$]\
                                        \n\tclient_host = [$clientHost$]
  httpAccessLogFormatter.parametersFormat=@@@@ PARAMETERS @@@@\n\tparameters  = [$parameters$]
  httpAccessLogFormatter.dispatchingClassFormat=@@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]
  httpAccessLogFormatter.endFormat=@@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$$query$] method = [$method$] status_code = [$statusCode$] content_path = [$contentPath$]\
                                      \n\tstart_time     = [$startTime$]\
                                      \n\tend_time       = [$endTime$]\
                                      \n\texecution_time = [$executionTime$]\
                                      \n\tmax_memory     = [$maxMemory$]\
                                      \n\tfree_memory    = [$freeMemory$]

How to use
--------------------------------------------------

.. _http_access_log-setting:

Configure the HTTP access log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The http access log is configured in the property file described in :ref:`log-app_log_setting`.

Description rules
 \

 httpAccessLogFormatter.className
  Class that implements :java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>`.
  Specify to replace.

 .. _http_access_log-prop_begin_format:

 httpAccessLogFormatter.beginFormat
  Format used for the log output at the start of the request process.

  Placeholders that can be specified for the format
   :Request ID: $requestId$
   :User ID: $userId$
   :URL: $url$
   :Query string: $query$
   :Port number: $port$
   :HTTP method: $method$
   :HTTP Session ID: $sessionId$
   :Session Store ID: $sessionStoreId$
   :Request parameters: $parameters$
   :Session scope information: $sessionScope$
   :Client terminal IP address: $clientIpAddress$
   :Client terminal host: $clientHost$
   :User-Agent of HTTP header: $clientUserAgent$

  Default format
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]

  .. tip::
   Request parameters are in the state before decryption of :ref:`hidden encryption <tag-hidden_encryption>`.

  .. important::
   Although request ID and user ID might overlap with the output items of  :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`,
   they have been provided to increase the flexibility of the HTTP access log format.

   When the request ID and user ID are output,
   :ref:`thread_context_handler` must be included in the handler configuration as they are acquired
   from :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>`.
   In particular, for user IDs, you need to set a value for the session in your application
   by referring to the :ref:`thread_context_handler-user_id_attribute_setting`.

 httpAccessLogFormatter.parametersFormat
  Format used for the log output after decryption of hidden parameters.

  Placeholders that can be specified for the format
   Omitted as it is the same as "format used for the log output at the start of the request process".

  Default format
   .. code-block:: bash

    @@@@ PARAMETERS @@@@
        \n\tparameters  = [$parameters$]

 httpAccessLogFormatter.dispatchingClassFormat
  Format used for the output log after the dispatch class has been determined.

  Placeholders that can be specified for the format
   :Dispatch destination class: $dispatchingClass$
   :Session Store ID: $sessionStoreId$

  Default format
   .. code-block:: bash

    @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]

 .. _http_access_log-prop_end_format:

 httpAccessLogFormatter.endFormat
  Format used for the log output at the end of the request process.

  Placeholders that can be specified for the format
   :Dispatch destination class: $dispatchingClass$
   :Status code (internal): $statusCode$
   :Status code (client): $responseStatusCode$
   :Content path: $contentPath$
   :Start date and time: $startTime$
   :End date and time: $endTime$
   :Execution time: $executionTime$
   :Maximum memory: $maxMemory$
   :Free memory (at start): $freeMemory$
   :Session Store ID: $sessionStoreId$

  Default format
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

  .. tip::

    The status code (internal) indicates the status code when :ref:`http_access_log_handler` is returned.
    Status code (client) is :ref:`http_response_handler` and indicates the status code returned to the client.

    Although the status code (client) is not finalized when this log is output,
    the log is output by deriving the status code (client) using the same function as :ref:`http_response_handler`.

    For status code conversion rules, see :ref:`http_response_handler-convert_status_code`.

  .. important::
   Value of the ``status code (client)`` may be different form the internal code when system errors such as JSP error occur after the HTTP access log handler is processed.
   Since a separate failure monitoring log is output as system error in such cases,
   consider the possibility that this value may be incorrect whenever a failure monitoring log is generated and verify the log.

 httpAccessLogFormatter.datePattern
  Date and time pattern to use for date and time of the start and end.
  For the pattern, specify the syntax specified by :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`.
  Default is ``yyyy-MM-dd HH:mm:ss.SSS``.

 httpAccessLogFormatter.maskingPatterns
  Specify the parameter name and variable name to be masked with a regular expression.
  If more than one is specified, separate them with commas.
  Used for masking both the request parameters and session scope information.
  The specified regular expression is not case-sensitive.
  For example, if specified as \ ``password``\, matches with ``password``, ``newPassword`` and ``password2``, etc.

 httpAccessLogFormatter.maskingChar
  Character used for masking. Default is ``*``.

 httpAccessLogFormatter.parametersSeparator
  Request parameter separator.
  Default is ``\n\t\t`` .

 httpAccessLogFormatter.sessionScopeSeparator
  Separator for session scope information.
  Default is ``\n\t\t`` .

 httpAccessLogFormatter.beginOutputEnabled
  Whether output at the start of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the start of the request process.

 httpAccessLogFormatter.parametersOutputEnabled
  Whether output after hidden parameter decryption is enabled.
  Default is true.
  If specified as false, it is not output after decryption of the hidden parameter.

 httpAccessLogFormatter.dispatchingClassOutputEnabled
  Whether output after determining the dispatch class is enabled.
  Default is true.
  If specified as false, it is not output after determining the dispatch class.

 httpAccessLogFormatter.endOutputEnabled
  Whether output at the end of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the end of the request process.

Example of the description
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.web.handler.HttpAccessLogFormatter
  httpAccessLogFormatter.beginFormat=> sid = [$sessionId$] @@@@ BEGIN @@@@\n\turl = [$url$]\n\tmethod = [$method$]
  httpAccessLogFormatter.parametersFormat=> sid = [$sessionId$] @@@@ PARAMETERS @@@@\n\tparameters  = [$parameters$]
  httpAccessLogFormatter.dispatchingClassFormat=> sid = [$sessionId$] @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]
  httpAccessLogFormatter.endFormat=< sid = [$sessionId$] @@@@ END @@@@ url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
  httpAccessLogFormatter.datePattern="yyyy-MM-dd HH:mm:ss.SSS"
  httpAccessLogFormatter.maskingChar=#
  httpAccessLogFormatter.maskingPatterns=password,mobilePhoneNumber
  httpAccessLogFormatter.parametersSeparator=,
  httpAccessLogFormatter.sessionScopeSeparator=,
  httpAccessLogFormatter.beginOutputEnabled=true
  httpAccessLogFormatter.parametersOutputEnabled=true
  httpAccessLogFormatter.dispatchingClassOutputEnabled=true
  httpAccessLogFormatter.endOutputEnabled=true

.. _http_access_log-json_setting:

Output as a structured log in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logs can be output in JSON format by using :ref:`log-json_log_setting` setting, but :java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>` outputs each item of the http access log as a string in the message value.

To output each item in the http access log as a JSON value as well, use the :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>`.

You can configure in the property file described in :ref:`log-app_log_setting`.

Description rules
 The properties to be specified when using :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` are as follows.
 
 httpAccessLogFormatter.className ``required``
  To output logs in JSON format, specify :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>`.

 .. _http_access_log-prop_begin_targets:

 httpAccessLogFormatter.beginTargets
  Items for the log output at the start of the request process. Separated by comma.

  Output items that can be specified and default output items
   :Label: label ``default``
   :Request ID: requestId ``default``
   :Usre ID: userId ``default``
   :HTTP Session ID: sessionId ``default``
   :Session Store ID: sessionStoreId
   :URL: url ``default``
   :Port number: port ``default``
   :HTTP method: method ``default``
   :Query string: queryString
   :Request parameters: parameters
   :Session scope information: sessionScope
   :Client terminal IP address: clientIpAddress ``default``
   :Client terminal host: clientHost ``default``
   :User-Agent of HTTP header: clientUserAgent

  The details of the output items are omitted because they are the same as the placeholders for :ref:`the format used to output the log at the start of the request process <http_access_log-prop_begin_format>`.

 httpAccessLogFormatter.parametersTargets
  Items used for the log output after decryption of hidden parameters. Separated by comma.
  Omitted as it is the same as :ref:`format used for the log output at the start of the request process <http_access_log-prop_begin_targets>`.
  The default output item is ``label,parameters``.
 
 httpAccessLogFormatter.dispatchingClassTargets
  Items used for the output log after the dispatch class has been determined. Separated by comma.

  Output items that can be specified and default output items
   :Label: label ``default``
   :HTTP Session ID: sessionId
   :Session Store ID: sessionStoreId
   :Dispatch destination class: dispatchingClass ``default``

 httpAccessLogFormatter.endTargets
  Items used for the log output at the end of the request process. Separated by comma.

  Output items that can be specified and default output items
   :Label: label ``default``
   :Request ID: requestId ``default``
   :User ID: userId ``default``
   :HTTP Session ID: sessionId ``default``
   :Session Store ID: sessionStoreId
   :URL: url ``default``
   :Dispatch destination class: dispatchingClass
   :Status code (internal): statusCode ``default``
   :Status code (client): responseStatusCode
   :Content path: contentPath ``default``
   :Start date and time: startTime ``default``
   :End date and time: endTime ``default``
   :Executuion time: executionTime ``default``
   :Maximum memory: maxMemory ``default``
   :Free memory(at start): freeMemory ``default``

  Omitted as it is the same as :ref:`format used for the log output at the end of the request process <http_access_log-prop_end_format>`.

 httpAccessLogFormatter.datePattern
  Date and time pattern to use for date and time of the start and end.
  For the pattern, specify the syntax specified by :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`.
  Default is ``yyyy-MM-dd HH:mm:ss.SSS``.

 httpAccessLogFormatter.maskingPatterns
  Specify the parameter name and variable name to be masked with a regular expression (partial match).
  If more than one is specified, separate them with commas.
  Used for masking both the request parameters and session scope information.
  The specified regular expression is not case-sensitive.
  For example, if specified as \ ``password``\, matches with ``password``, ``newPassword`` and ``password2``, etc.

 httpAccessLogFormatter.maskingChar
  Character used for masking. Default is ``*``.

 httpAccessLogFormatter.beginOutputEnabled
  Whether output at the start of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the start of the request process.

 httpAccessLogFormatter.parametersOutputEnabled
  Whether output after hidden parameter decryption is enabled.
  Default is true.
  If specified as false, it is not output after decryption of the hidden parameter.

 httpAccessLogFormatter.dispatchingClassOutputEnabled
  Whether output after determining the dispatch class is enabled.
  Default is true.
  If specified as false, it is not output after determining the dispatch class.

 httpAccessLogFormatter.endOutputEnabled
  Whether output at the end of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the end of the request process.

 httpAccessLogFormatter.beginLabel
  Value to be output to the label in the log at the start of the request process.
  Default is ``"HTTP ACCESS BEGIN"``。

 httpAccessLogFormatter.parametersLabel
  Value to be output to the label in the log after hidden parameter decryption.
  Default is ``"PARAMETERS"``。

 httpAccessLogFormatter.dispatchingClassLabel
  Value to be output to the label in the log after determining the dispatch class.
  Default is ``"DISPATCHING CLASS"``。

 httpAccessLogFormatter.endLabel
  Value to be output to the label in the log at the end of the request process.
  Default is ``"HTTP ACCESS END"``。

 httpAccessLogFormatter.structuredMessagePrefix
  A marker string given at the beginning of a message to identify that the message string after formatting has been formatted into JSON format.
  If the marker string at the beginning of the message matches the marker string set in :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>`, :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` processes the message as JSON data.
  The default is ``"$JSON$"``.
  If you change it, set the same value in :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` using LogWriter's ``structuredMessagePrefix`` property (see :ref:`log-basic_setting` for LogWriter properties).

Example of the description
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.web.handler.HttpAccessJsonLogFormatter
  httpAccessLogFormatter.structuredMessagePrefix=$JSON$
  httpAccessLogFormatter.beginTargets=sessionId,url,method
  httpAccessLogFormatter.parametersTargets=sessionId,parameters
  httpAccessLogFormatter.dispatchingClassTargets=sessionId,dispatchingClass
  httpAccessLogFormatter.endTargets=sessionId,url,statusCode,contentPath
  httpAccessLogFormatter.beginLabel=HTTP ACCESS BEGIN
  httpAccessLogFormatter.parametersLabel=PARAMETERS
  httpAccessLogFormatter.dispatchingClassLabel=DISPATCHING CLASS
  httpAccessLogFormatter.endLabel=HTTP ACCESS END


.. _http_access_log-session_store_id:

About Session Store ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the session store ID is included in the output, the ID identifying the session issued by :ref:`session_store` is output.

The value saved in the request process of the :ref:`session_store_handler` is used for this value.
Therefore, if the session store ID is to be logged, the :ref:`http_access_log_handler` must be placed after the :ref:`session_store_handler`.

Since the session store ID is fixed in the state at the start of request processing, the specification is as follows.

* For requests that do not have a session store ID, all session store IDs output within the same request are empty, even if an ID is issued in the middle.
* If the :java:extdoc:`session is destroyed <nablarch.common.web.session.SessionUtil.invalidate(nablarch.fw.ExecutionContext)>` or the :java:extdoc:`ID is changed <nablarch.common.web.session.SessionUtil.changeId(nablarch.fw.ExecutionContext)>`, the value in the log does not change from the value at the start of the request processing.
