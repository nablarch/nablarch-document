.. _messaging_log:

メッセージングログの出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

メッセージングログは、 :ref:`system_messaging` の中でメッセージ送受信時に出力する。
アプリケーションでは、ログ出力の設定を行うことにより出力する。

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
  writer.appLog.formatter.format=<アプリケーションログ用のフォーマット>

  availableLoggersNamesOrder=MESSAGING,ROO

  # アプリケーションログの設定
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # メッセージングログの設定
  loggers.MESSAGING.nameRegex=MESSAGING
  loggers.MESSAGING.level=INFO
  loggers.MESSAGING.writerNames=appLog

使用方法
--------------------------------------------------

.. _messaging_log-setting:

メッセージングログの設定を行う
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
   :メッセージボディの内容: $messageBody$
   :メッセージボディのヘキサダンプ: $messageBodyHex$
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
   :メッセージボディの内容: $messageBody$
   :メッセージボディのヘキサダンプ: $messageBodyHex$
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
   :メッセージボディの内容: $messageBody$
   :メッセージボディのヘキサダンプ: $messageBodyHex$
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
   :メッセージボディの内容: $messageBody$
   :メッセージボディのヘキサダンプ: $messageBodyHex$
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


