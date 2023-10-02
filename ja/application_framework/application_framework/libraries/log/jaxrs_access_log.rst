.. _jaxrs_access_log:

HTTPアクセスログ（RESTfulウェブサービス用）の出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

HTTPアクセスログは、フレームワークが提供するハンドラを使用して出力する。
アプリケーションでは、ハンドラを設定することでHTTPアクセスログを出力する。

HTTPアクセスログの出力に必要となるハンドラは以下のとおり。

 :ref:`jaxrs_access_log_handler`
  リクエスト処理開始時と終了時のログ出力を行う。

リクエストパラメータを含めたリクエスト情報を出力することで、
個別アプリケーションの証跡ログの要件を満たせる場合は、HTTPアクセスログと証跡ログを兼用することも想定している。

HTTPアクセスログ（RESTfulウェブサービス用）の出力方針
------------------------------------------------------
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
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=ACC,ROO

  # アプリケーションログの設定
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # HTTPアクセスログの設定
  loggers.ACC.nameRegex=HTTP_ACCESS
  loggers.ACC.level=INFO
  loggers.ACC.writerNames=appLog

app-log.propertiesの設定例
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

使用方法
--------------------------------------------------

.. _jaxrs_access_log-setting:

HTTPアクセスログ（RESTfulウェブサービス用）の設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTPアクセスログの設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 \

 jaxRsAccessLogFormatter.className
  :java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>` を実装したクラス。
  差し替える場合に指定する。

 .. _jaxrs_access_log-prop_begin_format:

 jaxRsAccessLogFormatter.beginFormat
  リクエスト処理開始時のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :リクエストID: $requestId$
   :ユーザID: $userId$
   :URL: $url$
   :クエリ文字列: $query$
   :ポート番号: $port$
   :HTTPメソッド: $method$
   :HTTPセッションID: $sessionId$
   :セッションストアID: $sessionStoreId$
   :リクエストパラメータ: $parameters$
   :セッションスコープ情報: $sessionScope$
   :クライアント端末IPアドレス: $clientIpAddress$
   :クライアント端末ホスト: $clientHost$
   :HTTPヘッダのUser-Agent: $clientUserAgent$
   :リクエストボディ: $requestBody$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ BEGIN @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$]
        \n\turl         = [$url$]
        \n\tmethod      = [$method$]
        \n\tport        = [$port$]
        \n\tclient_ip   = [$clientIpAddress$]
        \n\tclient_host = [$clientHost$]

  .. tip::
    プレースホルダ ``$parameters$`` で出力されるリクエストパラメータには、リクエストボディは含まれていない。
    リクエストボディを出力する場合は、 ``$requestBody$`` を使用する。

  .. important::
   リクエストIDとユーザIDは、 :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
   が出力する項目と重複するが、HTTPアクセスログのフォーマットの自由度を高めるために設けている。

   リクエストID、ユーザIDを出力する場合は、
   これらの取得元が :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` なので、
   ハンドラ構成に :ref:`thread_context_handler` が含まれている必要がある。
   特にユーザIDについては、 :ref:`thread_context_handler-user_id_attribute_setting` を参照して
   アプリケーションでセッションに値を設定する必要がある。

 .. _jaxrs_access_log-prop_end_format:

 jaxRsAccessLogFormatter.endFormat
  リクエスト処理終了時のログ出力に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :ステータスコード: $statusCode$
   :開始日時: $startTime$
   :終了日時: $endTime$
   :実行時間: $executionTime$
   :最大メモリ量: $maxMemory$
   :空きメモリ量(開始時): $freeMemory$
   :セッションストアID: $sessionStoreId$
   :レスポンスボディ: $responseBody$

  デフォルトのフォーマット
   .. code-block:: bash

    @@@@ END @@@@ rid = [$requestId$] uid = [$userId$] sid = [$sessionId$] url = [$url$] status_code = [$statusCode$]
        \n\tstart_time     = [$startTime$]
        \n\tend_time       = [$endTime$]
        \n\texecution_time = [$executionTime$]
        \n\tmax_memory     = [$maxMemory$]
        \n\tfree_memory    = [$freeMemory$]

 jaxRsAccessLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 jaxRsAccessLogFormatter.maskingPatterns
  マスク対象のパラメータ名又は変数名を正規表現で指定する。
  複数指定する場合はカンマ区切り。
  リクエストパラメータとセッションスコープ情報の両方のマスキングに使用する。
  指定した正規表現は大文字小文字を区別しない。
  例えば、\ ``password``\ と指定した場合、 ``password`` ``newPassword`` ``password2`` 等にマッチする。

 jaxRsAccessLogFormatter.maskingChar
  マスクに使用する文字。デフォルトは ``*`` 。

 jaxRsAccessLogFormatter.bodyLogTargetMatcher
  リクエストボディ及びレスポンスボディを出力するか判定するためのクラス。
  :java:extdoc:`MessageBodyLogTargetMatcher <nablarch.fw.jaxrs.MessageBodyLogTargetMatcher>` を実装するクラス名を指定する。
  デフォルトは :java:extdoc:`JaxRsBodyLogTargetMatcher <nablarch.fw.jaxrs.JaxRsBodyLogTargetMatcher>` 。

 jaxRsAccessLogFormatter.bodyMaskingFilter
  リクエストボディ及びレスポンスボディをマスク処理するためのクラス。
  :java:extdoc:`LogContentMaskingFilter <nablarch.fw.jaxrs.LogContentMaskingFilter>` を実装するクラス名を指定する。
  デフォルトは :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>` 。

  .. important::
   RESTfulウェブサービスで送受信するボディの形式にはいくつかあるが、デフォルトの :java:extdoc:`JaxRsBodyMaskingFilter <nablarch.fw.jaxrs.JaxRsBodyMaskingFilter>` ではJSON形式のみサポートしている。

 jaxRsAccessLogFormatter.bodyMaskingItemNames
  リクエストボディ及びレスポンスボディをマスク処理する場合、マスク対象の項目名を指定する。
  複数指定する場合はカンマ区切り。

 jaxRsAccessLogFormatter.parametersSeparator
  リクエストパラメータのセパレータ。
  デフォルトは ``\n\t\t`` 。

 jaxRsAccessLogFormatter.sessionScopeSeparator
  セッションスコープ情報のセパレータ。
  デフォルトは ``\n\t\t`` 。

 jaxRsAccessLogFormatter.beginOutputEnabled
  リクエスト処理開始時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理開始時に出力しない。

 jaxRsAccessLogFormatter.endOutputEnabled
  リクエスト処理終了時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理終了時に出力しない。

記述例
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

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定によりログをJSON形式で出力できるが、
:java:extdoc:`JaxRsAccessLogFormatter <nablarch.fw.jaxrs.JaxRsAccessLogFormatter>` では
HTTPアクセスログの各項目はmessageの値に文字列として出力される。
HTTPアクセスログの各項目もJSONの値として出力するには、
:java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` を使用する。
設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` を用いる際に
 指定するプロパティは以下の通り。
 
 httpAccessLogFormatter.className ``必須``
  JSON形式でログを出力する場合、
  :java:extdoc:`JaxRsAccessJsonLogFormatter <nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter>` を指定する。

 .. _jaxrs_access_log-prop_begin_targets:

 jaxRsAccessLogFormatter.beginTargets
  リクエスト処理開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :リクエストID: requestId ``デフォルト``
   :ユーザID: userId ``デフォルト``
   :HTTPセッションID: sessionId ``デフォルト``
   :セッションストアID: sessionStoreId
   :URL: url ``デフォルト``
   :ポート番号: port ``デフォルト``
   :HTTPメソッド: method ``デフォルト``
   :クエリ文字列: queryString
   :リクエストパラメータ: parameters
   :セッションスコープ情報: sessionScope
   :クライアント端末IPアドレス: clientIpAddress ``デフォルト``
   :クライアント端末ホスト: clientHost ``デフォルト``
   :HTTPヘッダのUser-Agent: clientUserAgent
   :リクエストボディ: requestBody

  出力項目の詳細は、
  :ref:`リクエスト処理開始時のログ出力に使用するフォーマット <jaxrs_access_log-prop_begin_format>`
  のプレースホルダーと同じため省略。

 jaxRsAccessLogFormatter.endTargets
  リクエスト処理終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目およびデフォルトの出力項目
   :ラベル: label ``デフォルト``
   :リクエストID: requestId ``デフォルト``
   :ユーザID: userId ``デフォルト``
   :HTTPセッションID: sessionId ``デフォルト``
   :セッションストアID: sessionStoreId
   :URL: url ``デフォルト``
   :ステータスコード: statusCode ``デフォルト``
   :開始日時: startTime ``デフォルト``
   :終了日時: endTime ``デフォルト``
   :実行時間: executionTime ``デフォルト``
   :最大メモリ量: maxMemory ``デフォルト``
   :空きメモリ量(開始時): freeMemory ``デフォルト``
   :レスポンスボディ: responseBody

  出力項目の詳細は、
  :ref:`リクエスト処理終了時のログ出力に使用するフォーマット <jaxrs_access_log-prop_end_format>`
  のプレースホルダーと同じため省略。

 jaxRsAccessLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは ``yyyy-MM-dd HH:mm:ss.SSS`` 。

 jaxRsAccessLogFormatter.maskingPatterns
  マスク対象のパラメータ名又は変数名を正規表現で指定する（部分一致）。
  複数指定する場合はカンマ区切り。
  リクエストパラメータとセッションスコープ情報の両方のマスキングに使用する。
  指定した正規表現は大文字小文字を区別しない。
  例えば、\ ``password``\ と指定した場合、 ``password`` ``newPassword`` ``password2`` 等にマッチする。

 jaxRsAccessLogFormatter.maskingChar
  マスクに使用する文字。デフォルトは ``*`` 。

 jaxRsAccessLogFormatter.beginOutputEnabled
  リクエスト処理開始時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理開始時に出力しない。

 jaxRsAccessLogFormatter.endOutputEnabled
  リクエスト処理終了時の出力が有効か否か。
  デフォルトはtrue。
  falseを指定するとリクエスト処理終了時に出力しない。

 jaxRsAccessLogFormatter.beginLabel
  リクエスト処理開始時ログのlabelに出力する値。
  デフォルトは ``"HTTP ACCESS BEGIN"``。

 jaxRsAccessLogFormatter.endLabel
  リクエスト処理終了時ログのlabelに出力する値。
  デフォルトは ``"HTTP ACCESS END"``。

 jaxRsAccessLogFormatter.structuredMessagePrefix
  フォーマット後のメッセージ文字列が JSON 形式に整形されていることを識別できるようにするために、メッセージの先頭に付与するマーカー文字列。
  メッセージの先頭にあるマーカー文字列が :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` に設定しているマーカー文字列と一致する場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。
  変更する場合は、LogWriterの ``structuredMessagePrefix`` プロパティを使用して :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` にも同じ値を設定すること（LogWriterのプロパティについては :ref:`log-basic_setting` を参照）。

記述例
 .. code-block:: properties

  httpAccessLogFormatter.className=nablarch.fw.jaxrs.JaxRsAccessJsonLogFormatter
  httpAccessLogFormatter.structuredMessagePrefix=$JSON$
  httpAccessLogFormatter.beginTargets=sessionId,url,method
  httpAccessLogFormatter.endTargets=sessionId,url,statusCode
  httpAccessLogFormatter.beginLabel=HTTP ACCESS BEGIN
  httpAccessLogFormatter.endLabel=HTTP ACCESS END

.. _jaxrs_access_log-session_store_id:

セッションストアIDについて
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

セッションストアIDを出力に含めた場合、 :ref:`session_store` が発行するセッションを識別するIDが出力される。

この値は :ref:`session_store_handler` の往路で記録されたものが使用される。
したがってセッションストアIDをログに出力する場合、 :ref:`jaxrs_access_log_handler` は :ref:`session_store_handler` より後に配置しなければならない。

セッションストアIDはリクエスト処理開始時の状態で固定されるため、以下のような仕様になる。

* セッションストアIDが発行されていないリクエストでは、途中でIDが発行されたとしても、同一リクエスト内で出力されるセッションストアIDは全て空になる
* 途中で :java:extdoc:`セッションを破棄 <nablarch.common.web.session.SessionUtil.invalidate(nablarch.fw.ExecutionContext)>` したり :java:extdoc:`IDを変更 <nablarch.common.web.session.SessionUtil.changeId(nablarch.fw.ExecutionContext)>` しても、ログに出力される値はリクエスト処理開始時のものから変化しない
