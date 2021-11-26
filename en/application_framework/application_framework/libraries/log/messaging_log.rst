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



.. _messaging_log-json_setting:

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定を行うことでログをJSON形式で出力できるが、
:java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` では
障害ログの各項目はmessageの値に文字列として出力される。
障害ログの各項目もJSONの値として出力するには、
:java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` を使用する。
設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` を用いる際に
 指定するプロパティは以下の通り。
 
 messagingLogFormatter.className ``必須``
  JSON形式でログを出力する場合、
  :java:extdoc:`MessagingJsonLogFormatter <nablarch.fw.messaging.logging.MessagingJsonLogFormatter>` を指定する。

 messagingLogFormatter.maskingPatterns
  メッセージ本文のマスク対象文字列を正規表現で指定する。
  正規表現で指定された最初のキャプチャ部分(括弧で囲まれた部分)がマスク対象となる。

  例えばパターンとして「<password>(.+?)</password>」と指定し、
  実電文に「<password>hoge</password>」が含まれる場合、
  出力される文字列は「<password>****</password>」となる。

  複数指定する場合はカンマ区切り。
  指定した正規表現は大文字小文字を区別しない。

 messagingLogFormatter.maskingChar
  マスクに使用する文字。デフォルトは’*’。

 messagingLogFormatter.sentMessageTargets
  MOM送信メッセージログの出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :スレッド名: threadName ``デフォルト``
   :メッセージID: messageId ``デフォルト``
   :送信宛先: destination ``デフォルト``
   :関連メッセージID: correlationId ``デフォルト``
   :応答宛先: replyTo ``デフォルト``
   :有効期間: timeToLive ``デフォルト``
   :メッセージボディの内容: messageBody [#placeholder_json]_ ``デフォルト``
   :メッセージボディのヘキサダンプ: messageBodyHex [#placeholder_json]_
   :メッセージボディのバイト長: messageBodyLength

 messagingLogFormatter.receivedMessageTargets
  MOM受信メッセージログの出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :スレッド名: threadName ``デフォルト``
   :メッセージID: messageId ``デフォルト``
   :送信宛先: destination ``デフォルト``
   :関連メッセージID: correlationId ``デフォルト``
   :応答宛先: replyTo ``デフォルト``
   :有効期間: timeToLive
   :メッセージボディの内容: messageBody [#placeholder_json]_ ``デフォルト``
   :メッセージボディのヘキサダンプ: messageBodyHex [#placeholder_json]_
   :メッセージボディのバイト長: messageBodyLength

 messagingLogFormatter.httpSentMessageTargets
  HTTP送信メッセージログの出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :スレッド名: threadName ``デフォルト``
   :メッセージID: messageId ``デフォルト``
   :送信先: destination ``デフォルト``
   :関連メッセージID: correlationId ``デフォルト``
   :メッセージボディの内容: messageBody [#placeholder_json]_ ``デフォルト``
   :メッセージボディのヘキサダンプ: messageBodyHex [#placeholder_json]_
   :メッセージボディのバイト長: messageBodyLength
   :メッセージのヘッダ: messageHeader ``デフォルト``

 messagingLogFormatter.httpReceivedMessageTargets
  HTTP受信メッセージログの出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :スレッド名: threadName ``デフォルト``
   :メッセージID: messageId ``デフォルト``
   :送信先: destination ``デフォルト``
   :関連メッセージID: correlationId ``デフォルト``
   :メッセージボディの内容: messageBody [#placeholder_json]_ ``デフォルト``
   :メッセージボディのヘキサダンプ: messageBodyHex [#placeholder_json]_
   :メッセージボディのバイト長: messageBodyLength
   :メッセージのヘッダ: messageHeader ``デフォルト``

 messagingLogFormatter.sentMessageLabel
  MOM送信メッセージログのlabelに出力する値。
  デフォルトは ``"SENT MESSAGE"``。

 messagingLogFormatter.receivedMessageLabel
  MOM受信メッセージログのlabelに出力する値。
  デフォルトは ``"RECEIVED MESSAGE"``。

 messagingLogFormatter.httpSentMessageLabel
  HTTP送信メッセージログのlabelに出力する値。
  デフォルトは ``"HTTP SENT MESSAGE"``。

 messagingLogFormatter.httpReceivedMessageLabel
  HTTP受信メッセージログのlabelに出力する値。
  デフォルトは ``"HTTP RECEIVED MESSAGE"``。

 messagingLogFormatter.structuredMessagePrefix
  フォーマット後のメッセージ文字列が JSON 形式に整形されていることを識別できるようにするために、メッセージの先頭に付与するマーカー文字列。
  メッセージの先頭にこのマーカーがある場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。

.. [#placeholder_json]

  * **messageBody:** 電文をISO-8859-1固定でエンコードした結果を出力する。
  * **messageBodyHex:** messageBodyの内容をヘキサダンプして出力する。

記述例
 .. code-block:: properties

  messagingLogFormatter.className=nablarch.fw.messaging.logging.MessagingJsonLogFormatter
  messagingLogFormatter.structuredMessagePrefix=$JSON$

  # MOMメッセージング用フォーマット
  messagingLogFormatter.sentMessageTargets=threadName,messageId,destination,correlationId,replyTo,timeToLive,messageBody
  messagingLogFormatter.receivedMessageTargets=threadName,messageId,destination,correlationId,replyTo,messageBody

  # HTTPメッセージング用フォーマット
  messagingLogFormatter.httpSentMessageTargets=threadName,messageId,destination,correlationId,messageHeader,messageBody
  messagingLogFormatter.httpReceivedMessageTargets=threadName,messageId,destination,correlationId,messageHeader,messageBody


