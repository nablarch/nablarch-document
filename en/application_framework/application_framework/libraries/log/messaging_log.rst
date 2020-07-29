.. _messaging_log:

Output Messaging Log
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

The messaging log is output when sending and receiving messages in  :ref:`system_messaging` . 
The log is output in the application by configuring the log output.

Output policy for messaging log
--------------------------------------------------
The messaging log is output to an application log that outputs the log of the entire application.

.. list-table:: Output policy for messaging log
   :header-rows: 1
   :class: white-space-normal
   :widths: 50,50

   * - Log level
     - Logger name

   * - INFO
     - MESSAGING

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

  availableLoggersNamesOrder=MESSAGING,ROO

  # Configure application log
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # Configure messaging log
  loggers.MESSAGING.nameRegex=MESSAGING
  loggers.MESSAGING.level=INFO
  loggers.MESSAGING.writerNames=appLog

Configuration example of app-log.properties
 .. code-block:: properties

  # MessagingLogFormatter
  #messagingLogFormatter.className=
  #messagingLogFormatter.maskingChar=
  #messagingLogFormatter.maskingPatterns=
  # Format for MOM messaging
  messagingLogFormatter.sentMessageFormat=@@@@ SENT MESSAGE @@@@\
                                            \n\tthread_name    = [$threadName$]\
                                            \n\tmessage_id     = [$messageId$]\
                                            \n\tdestination    = [$destination$]\
                                            \n\tcorrelation_id = [$correlationId$]\
                                            \n\treply_to       = [$replyTo$]\
                                            \n\ttime_to_live   = [$timeToLive$]\
                                            \n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.receivedMessageFormat=@@@@ RECEIVED MESSAGE @@@@\
                                                \n\tthread_name    = [$threadName$]\
                                                \n\tmessage_id     = [$messageId$]\
                                                \n\tdestination    = [$destination$]\
                                                \n\tcorrelation_id = [$correlationId$]\
                                                \n\treply_to       = [$replyTo$]\
                                                \n\tmessage_body   = [$messageBody$]
  # Format for HTTP messaging
  messagingLogFormatter.httpSentMessageFormat=@@@@ HTTP SENT MESSAGE @@@@\
                                                \n\tthread_name    = [$threadName$]\
                                                \n\tmessage_id     = [$messageId$]\
                                                \n\tdestination    = [$destination$]\
                                                \n\tcorrelation_id = [$correlationId$]\
                                                \n\tmessage_header = [$messageHeader$]\
                                                \n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.httpReceivedMessageFormat=@@@@ HTTP RECEIVED MESSAGE @@@@\
                                                    \n\tthread_name    = [$threadName$]\
                                                    \n\tmessage_id     = [$messageId$]\
                                                    \n\tdestination    = [$destination$]\
                                                    \n\tcorrelation_id = [$correlationId$]\
                                                    \n\tmessage_header = [$messageHeader$]\
                                                    \n\tmessage_body   = [$messageBody$]

How to use
--------------------------------------------------

.. _messaging_log-setting:

Configure the messaging log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The messaging log is configured in the property file described in :ref:`log-app_log_setting` .

Description rules
 \

 messagingLogFormatter.className
  Class that implements messagingLogFormatter.className :java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` . 
  Specify to replace.

 messagingLogFormatter.maskingPatterns
  Specify the character string to be masked in the message body with a regular expression. 
  The first capture part (enclosed in parentheses) specified by the regular expression will be the target for masking.

  For example, if "<password>(.+?)</password>" is specified as the pattern, 
  and "<password>hoge</password>" is included in the message, 
  then the output string will be "<password>****</password>".

  If more than one is specified, separate them with commas. 
  The specified regular expression is not case-sensitive.

 messagingLogFormatter.maskingChar
  Character used for masking. Default is "*".

 messagingLogFormatter.sentMessageFormat
  Format used for the log output of MOM outgoing message.

  Placeholders that can be specified for the format
   :Thread name: $threadName$
   :Message ID: $messageId$
   :Send destination: $destination$
   :Correlation message ID: $correlationId$
   :Reply to: $replyTo$
   :Expiry interval: $timeToLive$
   :Message body content: $messageBody$ [#placeholder]_
   :Hex dump of message body: $messageBodyHex$ [#placeholder]_
   :Message body byte length: $messageBodyLength$

  Default format
   .. code-block:: bash

    @@@@ SENT MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\treply_to       = [$replyTo$]
        \n\ttime_to_live   = [$timeToLive$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.receivedMessageFormat
  Format used for the log output of MOM incoming message.

  Placeholders that can be specified for the format
   :Thread name: $threadName$
   :Message ID: $messageId$
   :Send destination: $destination$
   :Correlation message ID: $correlationId$
   :Reply to: $replyTo$
   :Expiry interval: $timeToLive$
   :Message body content: $messageBody$ [#placeholder]_
   :Hex dump of message body: $messageBodyHex$ [#placeholder]_
   :Message body byte length: $messageBodyLength$

  Default format
   .. code-block:: bash

    @@@@ RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\treply_to       = [$replyTo$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpSentMessageFormat
  Format used for the log output of HTTP outgoing message.

  Placeholders that can be specified for the format
   :Thread name: $threadName$
   :Message ID: $messageId$
   :Sent to: $destination$
   :Correlation message ID: $correlationId$
   :Message body content: $messageBody$ [#placeholder]_
   :Hex dump of message body: $messageBodyHex$ [#placeholder]_
   :Message body byte length: $messageBodyLength$
   :Message header: $messageHeader$

  Default format
   .. code-block:: bash

    @@@@ HTTP SENT MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpReceivedMessageFormat
  Format used for the log output of HTTP incoming message.

  Placeholders that can be specified for the format
   :Thread name: $threadName$
   :Message ID: $messageId$
   :Sent to: $destination$
   :Correlation message ID: $correlationId$
   :Message body content: $messageBody$ [#placeholder]_
   :Hex dump of message body: $messageBodyHex$ [#placeholder]_
   :Message body byte length: $messageBodyLength$
   :Message header: $messageHeader$

  Default format
   .. code-block:: bash

    @@@@ HTTP RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

.. [#placeholder]


  * **$messageBody$:** Outputs the result of encoding the message with ISO-8859-1 fixed.
  * **$messageBodyHex$:** $messageBody$ are output by hexadump.

Example of the description
 .. code-block:: properties

  messagingLogFormatter.className=nablarch.fw.messaging.logging.MessagingLogFormatter
  messagingLogFormatter.maskingChar=#
  messagingLogFormatter.maskingPatterns=<password>(.+?)</password>,<mobilePhoneNumber>(.+?)</mobilePhoneNumber>

  # MOM messaging format
  messagingLogFormatter.sentMessageFormat=@@@@ SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\ttime_to_live   = [$timeToLive$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.receivedMessageFormat=@@@@ RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\tmessage_body   = [$messageBody$]

  # Format for HTTP messaging
  messagingLogFormatter.httpSentMessageFormat=@@@@ HTTP SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.httpReceivedMessageFormat=@@@@ HTTP RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]


