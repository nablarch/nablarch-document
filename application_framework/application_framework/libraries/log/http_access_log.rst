.. _http_access_log:

HTTPアクセスログの出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

HTTPアクセスログは、フレームワークが提供するハンドラを使用して出力する。
アプリケーションでは、ハンドラの設定を行うことでHTTPアクセスログを出力する。

HTTPアクセスログの出力に必要となるハンドラは以下のとおり。

 :ref:`http_access_log_handler`
  リクエスト処理開始時と終了時のログ出力を行う。

 :ref:`nablarch_tag_handler`
  hiddenパラメータ復号後のログ出力を行う。
  hiddenパラメータについては、 :ref:`hidden暗号化<tag-hidden_encryption>` を参照。

 :ref:`http_request_java_package_mapping`
  ディスパッチ先クラス決定後のログ出力を行う。

リクエストパラメータを含めたリクエスト情報を出力することで、
個別アプリケーションの証跡ログの要件を満たせる場合は、HTTPアクセスログと証跡ログを兼用することも想定している。

HTTPアクセスログの出力方針
--------------------------------------------------
HTTPアクセスログは、アプリケーション全体のログ出力を行うアプリケーションログに出力する。

.. list-table:: HTTPアクセスログの出力方針
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - ログレベル
     - ロガー名

   * - INFO
     - HTTP_ACCESS

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

  availableLoggersNamesOrder=ACC,ROO

  # アプリケーションログの設定
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # HTTPアクセスログの設定
  loggers.ACC.nameRegex=HTTP_ACCESS
  loggers.ACC.level=INFO
  loggers.ACC.writerNames=appLog

使用方法
--------------------------------------------------

.. _http_access_log-setting:

HTTPアクセスログの設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTPアクセスログの設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 \

 httpAccessLogFormatter.className
  :java:extdoc:`HttpAccessLogFormatter <nablarch.fw.web.handler.HttpAccessLogFormatter>` を実装したクラス。
  差し替える場合に指定する。

 httpAccessLogFormatter.beginFormat
  リクエスト処理開始時のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :リクエストID: $requestId$
   :ユーザID: $userId$
   :URL: $url$
   :ポート番号: $port$
   :HTTPメソッド: $method$
   :セッションID: $sessionId$
   :リクエストパラメータ: $parameters$
   :セッションスコープ情報: $sessionScope$
   :クライアント端末IPアドレス: $clientIpAddress$
   :クライアント端末ホスト: $clientHost$
   :HTTPヘッダのUser-Agent: $clientUserAgent$
   :リクエストパラメータ: $parameters$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]
        \n\tparameters  = [$parameters$]

  .. tip::
   リクエストパラメータは、 :ref:`hidden暗号化<tag-hidden_encryption>` の復号前の状態となる。

  .. important::
   リクエストIDとユーザIDは、 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
   が出力する項目と重複するが、HTTPアクセスログのフォーマットの自由度を高めるために設けている。

   リクエストID、ユーザIDを出力する場合は、
   これらの取得元が :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` なので、
   ハンドラ構成に :ref:`thread_context_handler` が含まれている必要がある。

 httpAccessLogFormatter.parametersFormat
  hiddenパラメータ復号後のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   「リクエスト処理開始時のログ出力に使用するフォーマット」と同じため省略。

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ PARAMETERS @@@@
        \n\tparameters  = [$parameters$]

 httpAccessLogFormatter.dispatchingClassFormat
  ディスパッチ先クラス決定後のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :ディスパッチ先クラス: $dispatchingClass$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]

 httpAccessLogFormatter.endFormat
  リクエスト処理終了時のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :ディスパッチ先クラス: $dispatchingClass$
   :ステータスコード(内部): $statusCode$
   :ステータスコード(クライアント): $responseStatusCode$
   :コンテンツパス: $contentPath$
   :開始日時: $startTime$
   :終了日時: $endTime$
   :実行時間: $executionTime$
   :最大メモリ量: $maxMemory$
   :空きメモリ量(開始時): $freeMemory$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

  .. tip::

    ステータスコード(内部)は、 :ref:`http_access_log_handler` の復路時点でのステータスコードのことを指す。
    ステータスコード(クライアント)は、 :ref:`http_response_handler` で、クライアントに返却するステータスコードのことを指す。

    ステータスコード(クライアント)は、本ログ出力時点では確定していないが、 :ref:`http_response_handler` と同じ機能を使い、
    ステータスコード(クライアント)を導出しログ出力を行う。

    ステータスコードの変換ルールは、 :ref:`http_response_handler-convert_status_code` を参照。

  .. important::
   ``ステータスコード(クライアント)`` の値は、 HTTPアクセスログハンドラの処理の後にJSPのエラーなどシステムエラーが発生した場合、
   実際の内部コードと異なることがある。この場合、システムエラーとして別途障害監視ログが出力されるため、
   障害監視ログが発生した際にはこの値が正しくない可能性があることを考慮してログを検証すること。

 httpAccessLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 httpAccessLogFormatter.maskingPatterns
  マスク対象のパラメータ名又は変数名を正規表現で指定する。
  複数指定する場合はカンマ区切り。
  リクエストパラメータとセッションスコープ情報の両方のマスキングに使用する。
  指定した正規表現は大文字小文字を区別しない。

 httpAccessLogFormatter.maskingChar
  マスクに使用する文字。デフォルトは ``*`` 。

 httpAccessLogFormatter.parametersSeparator
  リクエストパラメータのセパレータ。
  デフォルトは ``\n\t\t`` 。

 httpAccessLogFormatter.sessionScopeSeparator
  セッションスコープ情報のセパレータ。
  デフォルトは ``\n\t\t`` 。

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

記述例
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.web.handler.HttpAccessLogFormatter
  httpAccessLogFormatter.beginFormat=> sid = [$sessionId$] @@@@ BEGIN @@@@\n\turl = [$url$]\n\tmethod = [$method$]
  httpAccessLogFormatter.parametersFormat=> sid = [$sessionId$] @@@@ PARAMETERS @@@@\n\tparameters  = [$parameters$]
  httpAccessLogFormatter.dispatchingClassFormat=> sid = [$sessionId$] @@@@ DISPATCHING CLASS @@@@ class = [$dispatchingClass$]
  httpAccessLogFormatter.endFormat=< sid = [$sessionId$] @@@@ END @@@@ url = [$url$] status_code = [$statusCode$] content_path = [$contentPath$]
  httpAccessLogFormatter.datePattern="yyyy-MM-dd HH:mm:ss.SSS"
  httpAccessLogFormatter.maskingChar=#
  httpAccessLogFormatter.maskingPatterns=\\.*password\\.*,\\.*mobilePhoneNumber\\.*
  httpAccessLogFormatter.parametersSeparator=,
  httpAccessLogFormatter.sessionScopeSeparator=,
  httpAccessLogFormatter.beginOutputEnabled=true
  httpAccessLogFormatter.parametersOutputEnabled=true
  httpAccessLogFormatter.dispatchingClassOutputEnabled=true
  httpAccessLogFormatter.endOutputEnabled=true
