.. _jaxrs_access_log:

Output of HTTP Access Log (for RESTful Web Service)
=====================================================

.. contents:: Table of contents
  :depth: 3
  :local:

The HTTP access log is output using the handler provided by the framework.
The HTTP access log is output in the application by configuring the handler.

The handlers required to output the HTTP access log are as follows.

:ref:`jaxrs_access_log_handler`
  Outputs the log at the start and end of the request process.

If the requirements of the trace log of the individual application can be met by output of the request information including the request parameters,
then the HTTP access and trace logs can be used together.

Output policy of HTTP access log
------------------------------------------------------
The HTTP access log is output to an application log that outputs the log of the entire application.

.. list-table:: Output policy of HTTP access log for RESTful web service
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - Log Level
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

  # JaxRsAccessLogFormatter
  #jaxRsAccessLogFormatter.className=
  #jaxRsAccessLogFormatter.datePattern=
  #jaxRsAccessLogFormatter.maskingChar=
  #jaxRsAccessLogFormatter.maskingPatterns=
  #jaxRsAccessLogFormatter.bodyLogTargetMatcher=
  #jaxRsAccessLogFormatter.bodyMaskingFilter=
  #jaxRsAccessLogFormatter.bodyMaskingItemNames=
  #jaxRsAccessLogFormatter.parametersSeparator=
  #jaxRsAccessLogFormatter.sessionScopeSeparator=
  #jaxRsAccessLogFormatter.beginOutputEnabled=
  #jaxRsAccessLogFormatter.endOutputEnabled=
  jaxRsAccessLogFormatter.beginFormat=@@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]\
                                        \n\turl         = [$url$$query$]\
                                        \n\tmethod      = [$method$]\
                                        \n\tport        = [$port$]\
                                        \n\tclient_ip   = [$clientIpAddress$]\
                                        \n\tclient_host = [$clientHost$]
  jaxRsAccessLogFormatter.endFormat=@@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$$query$] method = [$method$] status_code = [$statusCode$]\
                                      \n\tstart_time     = [$startTime$]\
                                      \n\tend_time       = [$endTime$]\
                                      \n\texecution_time = [$executionTime$]\
                                      \n\tmax_memory     = [$maxMemory$]\
                                      \n\tfree_memory    = [$freeMemory$]

How to use
--------------------------------------------------

.. _jaxrs_access_log-setting:

Configure the HTTP access log (for RESTful Web Service)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The http access log is configured in the property file described in :ref:`log-app_log_setting`.

Description rules
 \

 jaxRsAccessLogFormatter.className
  Class that implements :java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>`.
  Specify to replace.

 .. _jaxrs_access_log-prop_begin_format:

 jaxRsAccessLogFormatter.beginFormat
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
   :Request Body: $requestBody$

  Default format
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]

  .. tip::
   Request parameters output with the placeholder ``$parameters$`` do not include the request body.
   Use ``$requestBody$`` to output the request body.

  .. important::
   Although request ID and user ID might overlap with the output items of  :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`,
   they have been provided to increase the flexibility of the HTTP access log format.

   When the request ID and user ID are output,
   :ref:`thread_context_handler` must be included in the handler configuration as they are acquired
   from :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>`.
   In particular, for user IDs, you need to set a value for the session in your application
   by referring to the :ref:`thread_context_handler-user_id_attribute_setting`.

 .. _jaxrs_access_log-prop_end_format:

 jaxRsAccessLogFormatter.endFormat
  Format used for the log output at the end of the request process.

  Placeholders that can be specified for the format
   :Status code: $statusCode$
   :Start date and time: $startTime$
   :End date and time: $endTime$
   :Execution time: $executionTime$
   :Maximum memory: $maxMemory$
   :Free memory (at start): $freeMemory$
   :Session Store ID: $sessionStoreId$
   :Response body: $responseBody$

  Default format
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

 jaxRsAccessLogFormatter.datePattern
  Date and time pattern to use for date and time of the start and end.
  For the pattern, specify the syntax specified by :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`.
  Default is ``yyyy-MM-dd HH:mm:ss.SSS``.

 jaxRsAccessLogFormatter.maskingPatterns
  Specify the parameter name and variable name to be masked with a regular expression.
  If more than one is specified, separate them with commas.
  Used for masking both the request parameters and session scope information.
  The specified regular expression is not case-sensitive.
  For example, if specified as \ ``password``\, matches with ``password``, ``newPassword`` and ``password2``, etc.

 jaxRsAccessLogFormatter.maskingChar
  Character used for masking. Default is ``*``.

 jaxRsAccessLogFormatter.bodyLogTargetMatcher
  Class for determining whether to output the request body and the response body.
  Specify the class name that implements :java:extdoc:`MessageBodyLogTargetMatcher <nablarch.fw.jaxrs.MessageBodyLogTargetMatcher>`.
  Default is :java:extdoc:`JaxRsBodyLogTargetMatcher <nablarch.fw.jaxrs.JaxRsBodyLogTargetMatcher>`.

 jaxRsAccessLogFormatter.bodyMaskingFilter
  Class for mask processing of the request body and the response body.
  Specify the class name that implements :java:extdoc:`LogContentMaskingFilter <nablarch.fw.jaxrs.LogContentMaskingFilter>`.
  Default is :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>`.

  .. important::
   There are several body formats that can be sent and received by RESTful web services, but the default :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>` supports only the JSON format.  

 jaxRsAccessLogFormatter.bodyMaskingItemNames
  When masking the request body and the response body, specify the names of items to be masked.
  If multiple items are specified, they are separated by commas.
 
 jaxRsAccessLogFormatter.parametersSeparator
  Request parameter separator.
  Default is ``\n\t\t`` .

 jaxRsAccessLogFormatter.sessionScopeSeparator
  Separator for session scope information.
  Default is ``\n\t\t`` .

 jaxRsAccessLogFormatter.beginOutputEnabled
  Whether output at the start of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the start of the request process.

 jaxRsAccessLogFormatter.endOutputEnabled
  Whether output at the end of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the end of the request process.

Example of the description
 .. code-block:: properties

  jaxRsAccessLogFormatter.className=nablarch.fw.jaxrs.JaxRsAccessLogFormatter
  jaxRsAccessLogFormatter.beginFormat=> sid = [$sessionId$] @@@@ BEGIN @@@@\n\turl = [$url$]\n\tmethod = [$method$]
  jaxRsAccessLogFormatter.endFormat=< sid = [$sessionId$] @@@@ END @@@@ url = [$url$] status_code = [$statusCode$]
  jaxRsAccessLogFormatter.datePattern="yyyy-MM-dd HH:mm:ss.SSS"
  jaxRsAccessLogFormatter.maskingChar=#
  jaxRsAccessLogFormatter.maskingPatterns=password,mobilePhoneNumber
  jaxRsAccessLogFormatter.bodyLogTargetMatcher=nablarch.fw.jaxrs.JaxRsBodyLogTargetMatcher
  jaxRsAccessLogFormatter.bodyMaskingFilter=nablarch.fw.jaxrs.JaxRsBodyMaskingFilter
  jaxRsAccessLogFormatter.bodyMaskingItemNames=password,mobilePhoneNumber
  jaxRsAccessLogFormatter.parametersSeparator=,
  jaxRsAccessLogFormatter.sessionScopeSeparator=,
  jaxRsAccessLogFormatter.beginOutputEnabled=true
  jaxRsAccessLogFormatter.endOutputEnabled=true

.. _jaxrs_access_log-json_setting:

Output as a structured log in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Logs can be output in JSON format by using :ref:`log-json_log_setting` setting, but :java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>` outputs each item of the http access log as a string in the message value.

To output each item in the http access log as a JSON value as well, use the :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>`.

You can configure in the property file described in :ref:`log-app_log_setting`.

Description rules
 The properties to be specified when using :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` are as follows.
 
 httpAccessLogFormatter.className ``required``
  To output logs in JSON format, specify :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>`.

 .. _jaxrs_access_log-prop_begin_targets:

 jaxRsAccessLogFormatter.beginTargets
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
   :Request body: requestBody

  The details of the output items are omitted because they are the same as the placeholders for :ref:`the format used to output the log at the start of the request process  <jaxrs_access_log-prop_begin_format>`.

 jaxRsAccessLogFormatter.endTargets
  Items used for the log output at the end of the request process. Separated by comma.

  Output items that can be specified and default output items
   :Label: label ``default``
   :Request ID: requestId ``default``
   :User ID: userId ``default``
   :HTTP Session ID: sessionId ``default``
   :Session Store ID: sessionStoreId
   :URL: url ``default``
   :Status code: statusCode ``default``
   :Start date and time: startTime ``default``
   :End date and time: endTime ``default``
   :Executuion time: executionTime ``default``
   :Maximum memory: maxMemory ``default``
   :Free memory(at start): freeMemory ``default``
   :Response body: responseBody

  Omitted as it is the same as :ref:`format used for the log output at the end of the request process <jaxrs_access_log-prop_end_format>`.

 jaxRsAccessLogFormatter.datePattern
  Date and time pattern to use for date and time of the start and end.
  For the pattern, specify the syntax specified by :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`.
  Default is ``yyyy-MM-dd HH:mm:ss.SSS``.

 jaxRsAccessLogFormatter.maskingPatterns
  Specify the parameter name and variable name to be masked with a regular expression (partial match).
  If more than one is specified, separate them with commas.
  Used for masking both the request parameters and session scope information.
  The specified regular expression is not case-sensitive.
  For example, if specified as \ ``password``\, matches with ``password``, ``newPassword`` and ``password2``, etc.

 jaxRsAccessLogFormatter.maskingChar
  Character used for masking. Default is ``*``.

 jaxRsAccessLogFormatter.beginOutputEnabled
  Whether output at the start of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the start of the request process.

 jaxRsAccessLogFormatter.endOutputEnabled
  Whether output at the end of the request process is enabled.
  Default is true.
  If specified as false, it is not output at the end of the request process.

 jaxRsAccessLogFormatter.beginLabel
  Value to be output to the label in the log at the start of the request process.
  Default is ``"HTTP ACCESS BEGIN"``。

 jaxRsAccessLogFormatter.endLabel
  Value to be output to the label in the log at the end of the request process.
  Default is ``"HTTP ACCESS END"``。

 jaxRsAccessLogFormatter.structuredMessagePrefix
  A marker string given at the beginning of a message to identify that the message string after formatting has been formatted into JSON format.
  If the marker string at the beginning of the message matches the marker string set in :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>`, :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` processes the message as JSON data.
  The default is ``"$JSON$"``.
  If you change it, set the same value in :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` using LogWriter's ``structuredMessagePrefix`` property (see :ref:`log-basic_setting` for LogWriter properties).

Example of the description
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter
  httpAccessLogFormatter.structuredMessagePrefix=$JSON$
  httpAccessLogFormatter.beginTargets=sessionId,url,method
  httpAccessLogFormatter.endTargets=sessionId,url,statusCode
  httpAccessLogFormatter.beginLabel=HTTP ACCESS BEGIN
  httpAccessLogFormatter.endLabel=HTTP ACCESS END

.. _jaxrs_access_log-session_store_id:

About Session Store ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the session store ID is included in the output, the ID identifying the session issued by :ref:`session_store` is output.

The value saved in the request process of the :ref:`session_store_handler` is used for this value.
Therefore, if the session store ID is to be logged, the :ref:`jaxrs_access_log_handler` must be placed after the :ref:`session_store_handler`.

Since the session store ID is fixed in the state at the start of request processing, the specification is as follows.

* For requests that do not have a session store ID, all session store IDs output within the same request are empty, even if an ID is issued in the middle.
* If the :java:extdoc:`session is destroyed <nablarch.common.web.session.SessionUtil.invalidate(nablarch.fw.ExecutionContext)>` or the :java:extdoc:`ID is changed <nablarch.common.web.session.SessionUtil.changeId(nablarch.fw.ExecutionContext)>`, the value in the log does not change from the value at the start of the request processing.
