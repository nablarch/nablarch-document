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

  # Configure the application log
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

 httpAccessLogFormatter.beginFormat
  Format used for the log output at the start of the request process.

  Placeholders that can be specified for the format
   :Request ID: $requestId$
   :User ID: $userId$
   :URL: $url$
   :Query string: $query$
   :Port number: $port$
   :HTTP method: $method$
   :Session ID: $sessionId$
   :Request parameters: $parameters$
   :Session scope information: $sessionScope$
   :Client terminal IP address: $clientIpAddress$
   :Client terminal host: $clientHost$
   :User-Agent of HTTP header: $clientUserAgent$
   :Request parameters: $parameters$

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

  Default format
   .. code-block:: bash

    @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]

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
  Specify the parameter name and variable name to be masked with a regular expression (partial match).
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

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定を行うことでログをJSON形式で出力できるが、
:java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>` では
障害ログの各項目はmessageの値に文字列として出力される。
障害ログの各項目もJSONの値として出力するには、
:java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` を使用する。
設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` を用いる際に
 指定するプロパティは以下の通り。
 
 httpAccessLogFormatter.className ``必須``
  JSON形式でログを出力する場合、
  :java:extdoc:`HttpAccessJsonLogFormatter <nablarch.fw.web.handler.HttpAccessJsonLogFormatter>` を指定する。

 .. _http_access_log-prop_begin_targets:

 httpAccessLogFormatter.beginTargets
  リクエスト処理開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :リクエストID: requestId ``デフォルト``
   :ユーザID: userId ``デフォルト``
   :セッションID: sessionId ``デフォルト``
   :URL: url ``デフォルト``
   :ポート番号: port ``デフォルト``
   :HTTPメソッド: method ``デフォルト``
   :クエリ文字列: query
   :リクエストパラメータ: parameters
   :セッションスコープ情報: sessionScope
   :クライアント端末IPアドレス: clientIpAddress ``デフォルト``
   :クライアント端末ホスト: clientHost ``デフォルト``
   :HTTPヘッダのUser-Agent: clientUserAgent
   :リクエストパラメータ: parameters

  出力項目の詳細は、
  :ref:`リクエスト処理開始時のログ出力に使用するフォーマット <http_access_log-prop_begin_format>` 
  のプレースホルダーと同じため省略。

 httpAccessLogFormatter.parametersTargets
  hiddenパラメータ復号後のログ出力項目。カンマ区切りで指定する。
  指定可能な出力項目は、
  :ref:`リクエスト処理開始時の出力項目 <http_access_log-prop_begin_targets>` と同じため省略。
  デフォルトの出力項目は ``label,parameters`` となる。
        
 httpAccessLogFormatter.dispatchingClassTargets
  ディスパッチ先クラス決定後のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :セッションID: sessionId
   :ディスパッチ先クラス: dispatchingClass ``デフォルト``

 httpAccessLogFormatter.endTargets
  リクエスト処理終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :リクエストID: requestId ``デフォルト``
   :ユーザID: userId ``デフォルト``
   :セッションID: sessionId ``デフォルト``
   :URL: url ``デフォルト``
   :ディスパッチ先クラス: dispatchingClass
   :ステータスコード(内部): statusCode
   :ステータスコード(クライアント): responseStatusCode
   :コンテンツパス: contentPath ``デフォルト``
   :開始日時: startTime ``デフォルト``
   :終了日時: endTime ``デフォルト``
   :実行時間: executionTime ``デフォルト``
   :最大メモリ量: maxMemory ``デフォルト``
   :空きメモリ量(開始時): freeMemory ``デフォルト``

  出力項目の詳細は、
  :ref:`リクエスト処理終了時のログ出力に使用するフォーマット <http_access_log-prop_end_format>` 
  のプレースホルダーと同じため省略。

 httpAccessLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 httpAccessLogFormatter.maskingPatterns
  マスク対象のパラメータ名又は変数名を正規表現で指定する（部分一致）。
  複数指定する場合はカンマ区切り。
  リクエストパラメータとセッションスコープ情報の両方のマスキングに使用する。
  指定した正規表現は大文字小文字を区別しない。
  例えば、\ ``password``\ と指定した場合、 ``password`` ``newPassword`` ``password2`` 等にマッチする。

 httpAccessLogFormatter.maskingChar
  マスクに使用する文字。デフォルトは ``*`` 。

 httpAccessLogFormatter.beginOutputEnabled
  リクエスト処理開始時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理開始時の出力を行わない。

 httpAccessLogFormatter.parametersOutputEnabled
  hiddenパラメータ復号後の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとhiddenパラメータ復号後の出力を行わない。

 httpAccessLogFormatter.dispatchingClassOutputEnabled
  ディスパッチ先クラス決定後の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとディスパッチ先クラス決定後の出力を行わない。

 httpAccessLogFormatter.endOutputEnabled
  リクエスト処理終了時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理終了時の出力を行わない。

 httpAccessLogFormatter.beginLabel
  リクエスト処理開始時ログのlabelに出力する値。
  デフォルトは ``"HTTP ACCESS BEGIN"``。

 httpAccessLogFormatter.parametersLabel
  hiddenパラメータ復号後ログのlabelに出力する値。
  デフォルトは ``"PARAMETERS"``。

 httpAccessLogFormatter.dispatchingClassLabel
  ディスパッチ先クラス決定後ログのlabelに出力する値。
  デフォルトは ``"DISPATCHING CLASS"``。

 httpAccessLogFormatter.endLabel
  リクエスト処理終了時ログのlabelに出力する値。
  デフォルトは ``"HTTP ACCESS END"``。

 httpAccessLogFormatter.structuredMessagePrefix
  フォーマット後のメッセージ文字列が JSON 形式に整形されていることを識別できるようにするために、メッセージの先頭に付与するマーカー文字列。
  メッセージの先頭にこのマーカーがある場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。

記述例
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
