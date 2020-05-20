.. _http_messaging_error_handler:

HTTPメッセージングエラー制御ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラでは後続のハンドラで発生した例外及びエラーを補足し、例外(エラー)に応じたログ出力とレスポンスの生成を行う。
また、後続のハンドラでレスポンスボディが設定されていない場合には、HTTPステータスコードに対応したデフォルトのボディをレスポンスに設定する。

本ハンドラでは、以下の処理を行う。

* 例外(エラー)に応じたログ出力とレスポンスの生成を行う。
  詳細は、 :ref:`http_messaging_error_handler-error_response_and_log` を参照。

* デフォルトのレスポンスボディの設定を行う。
  詳細は、 :ref:`http_messaging_error_handler-default_page` を参照。

処理の流れは以下のとおり。

.. image:: ../images/HttpMessagingErrorHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.messaging.handler.HttpMessagingErrorHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-messaging-http</artifactId>
  </dependency>

制約
------------------------------
:ref:`http_response_handler` より後ろに配置すること
  本ハンドラで生成した :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` を :ref:`http_response_handler` が処理する。
  このため、本ハンドラを :ref:`http_response_handler` より後ろに設定する必要がある。

.. _http_messaging_error_handler-error_response_and_log:

例外の種類に応じたログ出力処理とレスポンスの生成
--------------------------------------------------------------
:java:extdoc:`nablarch.fw.NoMoreHandlerException`
  :ログレベル: INFO
  :レスポンス: 404
  :説明: リクエストを処理すべきハンドラが存在しなかったことを意味するため、証跡ログとして記録する。
         また、処理すべき *action class* が存在しなかったことを意味するため、HTTPステータスコードが *404*  のレスポンスを生成する。

:java:extdoc:`nablarch.fw.web.HttpErrorResponse`
  :ログレベル: ログ出力なし
  :レスポンス: :java:extdoc:`HttpErrorResponse#getResponse() <nablarch.fw.web.HttpErrorResponse.getResponse()>`
  :説明: 後続のハンドラで業務例外(バリデーションなどを行った結果の例外)が発生したことを意味するので、ログ出力は行わない。

:java:extdoc:`nablarch.fw.Result.Error`
  :ログレベル: 設定による
  :レスポンス: :java:extdoc:`Error#getStatusCode() <nablarch.fw.Result.Error.getStatusCode()>`
  :説明: :ref:`http_messaging_error_handler-write_failure_log_pattern` を参照

:java:extdoc:`nablarch.core.message.ApplicationException` と :java:extdoc:`nablarch.fw.messaging.MessagingException`
  :ログレベル: \-
  :レスポンス: 400
  :説明: クライアントからのリクエストが不正であることを示す例外のため、HTTPステータスコードが *400* のレスポンスを生成する。

上記以外の例外及びエラー
  :ログレベル: FATAL
  :レスポンス: 500
  :説明: 上記に該当しない例外及びエラーの場合には、障害扱いとしてログ出力を行う。
         また、予期しない例外やエラーであるため、レスポンスは **500** としている。

.. _http_messaging_error_handler-write_failure_log_pattern:

nablarch.fw.Result.Errorのログ出力について
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
後続のハンドラで発生した例外が、 :java:extdoc:`Error <nablarch.fw.Result.Error>` の場合はログ出力を行うかどうかは、
:java:extdoc:`writeFailureLogPattern <nablarch.fw.web.handler.HttpErrorHandler.setWriteFailureLogPattern(java.lang.String)>` に設定した値によって変わる。
このプロパティには正規表現が設定でき、その正規表現が :java:extdoc:`Error#getStatusCode() <nablarch.fw.Result.Error.getStatusCode()>` とマッチした場合に `FATAL` レベルのログを出力する。

.. _http_messaging_error_handler-default_page:

レスポンスボディが空の場合のデフォルトレスポンスの設定
--------------------------------------------------------
詳細は、 :ref:`HTTPエラー制御ハンドラのデフォルトページの設定 <HttpErrorHandler_DefaultPage>` を参照。
