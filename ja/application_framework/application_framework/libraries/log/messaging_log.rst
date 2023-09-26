.. _messaging_log:

メッセージングログの出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

メッセージングログは、 :ref:`system_messaging` の中でメッセージ送受信時に出力する。
アプリケーションでは、ログ出力を設定することにより出力する。

メッセージングログの出力方針
--------------------------------------------------
メッセージングログは、アプリケーション全体のログ出力を行うアプリケーションログに出力する。

.. list-table:: メッセージングログの出力方針
   :header-rows: 1
   :class: white-space-normal
   :widths: 50,50

   * - ログレベル
     - ロガー名

   * - INFO
     - MESSAGING

上記出力方針に対するログ出力の設定例を下記に示す。

log.propertiesの設定例
 .. code-block:: properties

  writerNames=appLog

  # アプリケーションログの出力先
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=MESSAGING,ROO

  # アプリケーションログの設定
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # メッセージングログの設定
  loggers.MESSAGING.nameRegex=MESSAGING
  loggers.MESSAGING.level=INFO
  loggers.MESSAGING.writerNames=appLog

app-log.propertiesの設定例
 .. code-block:: properties

  # MessagingLogFormatter
  #messagingLogFormatter.className=
  #messagingLogFormatter.maskingChar=
  #messagingLogFormatter.maskingPatterns=
  # MOMメッセージング用フォーマット
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
  # HTTPメッセージング用フォーマット
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

使用方法
--------------------------------------------------

.. _messaging_log-setting:

メッセージングログの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージングログの設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 \

 messagingLogFormatter.className
  :java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` を実装したクラス。
  差し替える場合に指定する。

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

 messagingLogFormatter.sentMessageFormat
  MOM送信メッセージのログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :スレッド名: $threadName$
   :メッセージID: $messageId$
   :送信宛先: $destination$
   :関連メッセージID: $correlationId$
   :応答宛先: $replyTo$
   :有効期間: $timeToLive$
   :メッセージボディの内容: $messageBody$ [#placeholder]_
   :メッセージボディのヘキサダンプ: $messageBodyHex$ [#placeholder]_
   :メッセージボディのバイト長: $messageBodyLength$

  デフォルトのフォーマット
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
  MOM受信メッセージのログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :スレッド名: $threadName$
   :メッセージID: $messageId$
   :送信宛先: $destination$
   :関連メッセージID: $correlationId$
   :応答宛先: $replyTo$
   :有効期間: $timeToLive$
   :メッセージボディの内容: $messageBody$ [#placeholder]_
   :メッセージボディのヘキサダンプ: $messageBodyHex$ [#placeholder]_
   :メッセージボディのバイト長: $messageBodyLength$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\treply_to       = [$replyTo$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpSentMessageFormat
  HTTP送信メッセージのログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :スレッド名: $threadName$
   :メッセージID: $messageId$
   :送信先: $destination$
   :関連メッセージID: $correlationId$
   :メッセージボディの内容: $messageBody$ [#placeholder]_
   :メッセージボディのヘキサダンプ: $messageBodyHex$ [#placeholder]_
   :メッセージボディのバイト長: $messageBodyLength$
   :メッセージのヘッダ: $messageHeader$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ HTTP SENT MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

 messagingLogFormatter.httpReceivedMessageFormat
  HTTP受信メッセージのログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :スレッド名: $threadName$
   :メッセージID: $messageId$
   :送信先: $destination$
   :関連メッセージID: $correlationId$
   :メッセージボディの内容: $messageBody$ [#placeholder]_
   :メッセージボディのヘキサダンプ: $messageBodyHex$ [#placeholder]_
   :メッセージボディのバイト長: $messageBodyLength$
   :メッセージのヘッダ: $messageHeader$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ HTTP RECEIVED MESSAGE @@@@
        \n\tthread_name    = [$threadName$]
        \n\tmessage_id     = [$messageId$]
        \n\tdestination    = [$destination$]
        \n\tcorrelation_id = [$correlationId$]
        \n\tmessage_header = [$messageHeader$]
        \n\tmessage_body   = [$messageBody$]

.. [#placeholder]


  * **$messageBody$:** 電文をISO-8859-1固定でエンコードした結果を出力する。
  * **$messageBodyHex$:** $messageBody$の内容をヘキサダンプして出力する。

記述例
 .. code-block:: properties

  messagingLogFormatter.className=nablarch.fw.messaging.logging.MessagingLogFormatter
  messagingLogFormatter.maskingChar=#
  messagingLogFormatter.maskingPatterns=<password>(.+?)</password>,<mobilePhoneNumber>(.+?)</mobilePhoneNumber>

  # MOMメッセージング用フォーマット
  messagingLogFormatter.sentMessageFormat=@@@@ SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\ttime_to_live   = [$timeToLive$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.receivedMessageFormat=@@@@ RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\treply_to       = [$replyTo$]\n\tmessage_body   = [$messageBody$]

  # HTTPメッセージング用フォーマット
  messagingLogFormatter.httpSentMessageFormat=@@@@ HTTP SENT MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]
  messagingLogFormatter.httpReceivedMessageFormat=@@@@ HTTP RECEIVED MESSAGE @@@@\n\tthread_name    = [$threadName$]\n\tmessage_id     = [$messageId$]\n\tdestination    = [$destination$]\n\tcorrelation_id = [$correlationId$]\n\tmessage_header = [$messageHeader$]\n\tmessage_body   = [$messageBody$]

.. _messaging_log-json_setting:

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定によりログをJSON形式で出力できるが、
:java:extdoc:`MessagingLogFormatter <nablarch.fw.messaging.logging.MessagingLogFormatter>` では
メッセージングログの各項目はmessageの値に文字列として出力される。
メッセージングログの各項目もJSONの値として出力するには、
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
  メッセージの先頭にあるマーカー文字列が :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` に設定しているマーカー文字列と一致する場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。
  変更する場合は、LogWriterの ``structuredMessagePrefix`` プロパティを使用して :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` にも同じ値を設定すること（LogWriterのプロパティについては :ref:`log-basic_setting` を参照）。

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
