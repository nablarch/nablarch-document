.. _http_error_handler:

HTTPエラー制御ハンドラ
============================

.. contents:: 目次
  :depth: 3
  :local:

後続のハンドラで発生した例外に対するログ出力やレスポンスへの変換を行うハンドラ。

本ハンドラでは、以下の処理を行う。

* :ref:`例外の種類に応じたログ出力 <HttpErrorHandler_ErrorHandling>`
* :ref:`例外の種類に応じたエラー用HttpResponseの生成と返却 <HttpErrorHandler_ErrorHandling>`
* :ref:`デフォルトページの設定 <HttpErrorHandler_DefaultPage>`


処理の流れは以下のとおり。

.. image:: ../images/HttpErrorHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.HttpErrorHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
------------------------------

:ref:`http_response_handler` より後ろに配置すること
  本ハンドラで生成した :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` をHTTPレスポンスハンドラが処理するため、
  本ハンドラは :ref:`http_response_handler` より後ろに配置する必要がある。

:ref:`http_access_log_handler` より後ろに配置すること
  本ハンドラで生成したエラー用 :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` を元にログ出力を行うため、
  :ref:`http_access_log_handler` より後ろに配置する必要がある。

.. _HttpErrorHandler_ErrorHandling:

例外の種類に応じたログ出力処理とレスポンスの生成
--------------------------------------------------------------

:java:extdoc:`nablarch.fw.NoMoreHandlerException`
  :ログレベル: INFO
  :レスポンス: 404
  :説明: リクエストを処理すべきハンドラが存在しなかったことを意味するため、証跡ログとして記録する。
         また、処理すべき *action class* が存在しなかったことを意味するため、レスポンスは *404*  としている。

:java:extdoc:`nablarch.fw.web.HttpErrorResponse`
  :ログレベル: ログ出力なし
  :レスポンス: :java:extdoc:`HttpErrorResponse#getResponse() <nablarch.fw.web.HttpErrorResponse.getResponse()>`
  :説明: 後続のハンドラで業務例外(バリデーションなどを行った結果のエラーレスポンス送出)を送出したことを意味するのでログ出力は行わない。

:java:extdoc:`nablarch.fw.Result.Error`
  :ログレベル: 設定による
  :レスポンス: :java:extdoc:`Error#getStatusCode() <nablarch.fw.Result.Error.getStatusCode()>`
  :説明: `nablarch.fw.Result.Errorのログ出力について`_ を参照

:java:extdoc:`java.lang.StackOverflowError`
  :ログレベル: FATAL
  :レスポンス: 500
  :説明: データや実装バグに起因する可能性があるため、障害として通知する。
         また予期しないエラーであるため、レスポンスは **500** としている。

:java:extdoc:`java.lang.ThreadDeath` と :java:extdoc:`java.lang.VirtualMachineError` ( :java:extdoc:`java.lang.StackOverflowError` 以外)
  :ログレベル: \-
  :レスポンス: \-
  :説明: 本ハンドラでは何もせず上位のハンドラに処理を任せる。(エラーを再送出する)

上記以外の例外及びエラー
  :ログレベル: FATAL
  :レスポンス: 500
  :説明: 上記に該当しない例外及びエラーの場合には、障害扱いとしてログ出力を行う。
         また、予期しない例外やエラーであるため、レスポンスは **500** としている。

nablarch.fw.Result.Errorのログ出力について
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
後続のハンドラで発生した例外が、 :java:extdoc:`Error <nablarch.fw.Result.Error>` の場合はログ出力を行うかどうかは、
:java:extdoc:`writeFailureLogPattern <nablarch.fw.web.handler.HttpErrorHandler.setWriteFailureLogPattern(java.lang.String)>` に設定した値によって変わる。
このプロパティには正規表現が設定でき、その正規表現が :java:extdoc:`Error#getStatusCode() <nablarch.fw.Result.Error.getStatusCode()>` とマッチした場合に `FATAL` レベルのログを出力する。

.. _HttpErrorHandler_DefaultPage:

デフォルトページの設定
---------------------------
後続のハンドラや本ハンドラのエラー処理で作成した :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` に対して、デフォルトページを適用する。
この機能では、 :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` が設定されていなかった場合、
:java:extdoc:`defaultPage <nablarch.fw.web.handler.HttpErrorHandler.setDefaultPage(java.lang.String,%20java.lang.String)>` や
:java:extdoc:`defaultPages <nablarch.fw.web.handler.HttpErrorHandler.setDefaultPages(java.util.Map)>` で設定されたデフォルトのページを適用する。

以下に設定例を示す。

.. code-block:: xml

 <component class="nablarch.fw.web.handler.HttpErrorHandler">
   <property name="defaultPages">
     <map>
       <entry key="4.." value="/USER_ERROR.jsp" />
       <entry key="404" value="/NOT_FOUND.jsp" />
       <entry key="5.." value="/ERROR.jsp" />
       <entry key="503" value="/NOT_IN_SERVICE.jsp" />
     </map>
   </property>
 </component>

.. important::

  この機能を使用した場合、Servlet APIで規定されている `web.xml` へのエラーページ設定( `error-page` 要素)と重複してJSPの設定が必要となる。
  `web.xml` への設定を行わなかった場合、エラーの発生場所によっては、ウェブサーバのデフォルトのエラーページが表示される。

  このため、本機能を使用するのではなく、デフォルトのエラーページの設定は、 `web.xml` へ行うことを推奨する。


