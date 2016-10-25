.. _http_messaging_response_building_handler:

HTTPメッセージングレスポンス変換ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラでは、後続のハンドラが作成した応答電文オブジェクトをHTTPレスポンスオブジェクトに変換する。
また、応答電文オブジェクト内のプロトコルヘッダーの値を、対応するHTTPヘッダーに設定及びXMLやJSONなどの形式への直列化を行う。


本ハンドラでは、以下の処理を行う。

* 応答電文オブジェクトの内容をHTTPレスポンスオブジェクトに変換する。

処理の流れは以下のとおり。

.. image:: ../images/HttpMessagingResponseBuildingHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.messaging.handler.HttpMessagingResponseBuildingHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-messaging-http</artifactId>
  </dependency>

制約
------------------------------

:ref:`http_response_handler` よりも後ろに設定すること
  このハンドラで生成した :java:extdoc:`HTTPレスポンスオブジェクト <nablarch.fw.web.HttpResponse>` を
  :ref:`http_response_handler` がクライアントに返却するため。

レスポンスヘッダーに設定される値
--------------------------------------------------
後続のハンドラで作成された応答電文オブジェクトを元に以下のレスポンスヘッダを設定する。

:Status-Code:
  応答電文オブジェクトのステータスコードを設定する。

:Content-Type:
  応答電文オブジェクトの持つフォーマッタ(:java:extdoc:`InterSystemMessage.getFormatter() <nablarch.fw.messaging.InterSystemMessage.getFormatter()>`)から以下の値を取得し設定する。

  * MIME(:java:extdoc:`DataRecordFormatterSupport#getMimeType() <nablarch.core.dataformat.DataRecordFormatterSupport.getMimeType()>`
  * cherset(:java:extdoc:`DataRecordFormatterSupport#getDefaultEncoding() <nablarch.core.dataformat.DataRecordFormatterSupport.getDefaultEncoding()>`

  MIMEが ``application/json`` でcharsetが ``utf-8`` の場合、Content-Typeは以下の値となる。

  **application/json;charset=utf-8**

:関連メッセージID: レスポンスヘッダーの ``X-Correlation-Id`` に、応答電文オブジェクトのヘッダーに設定された ``CorrelationId`` の値を設定する。

.. important::
  このハンドラでは、上記に記載のないレスポンスヘッダーを設定することはできない。

  上記外のレスポンスヘッダーを使用したい場合は、プロジェクトでハンドラを作成し対応すること。

フレームワーク制御ヘッダのレイアウトを変更する
--------------------------------------------------
応答電文内のフレームワーク制御ヘッダの定義を変更する場合には、プロジェクトで拡張したフレームワーク制御ヘッダの定義を設定する必要がある。
設定を行わない場合は、デフォルトの :java:extdoc:`StructuredFwHeaderDefinition <nablarch.fw.messaging.reader.StructuredFwHeaderDefinition>` が使用される。

フレームワーク制御ヘッダの詳細は、 :ref:`フレームワーク制御ヘッダ <http_system_messaging-fw_header>` を参照。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.messaging.handler.HttpMessagingResponseBuildingHandler">
    <!-- フレームワーク制御ヘッダの設定 -->
    <property name="fwHeaderDefinition">
      <component class="sample.SampleFwHeaderDefinition" />
    </property>
  </component> 

.. |br| raw:: html

  <br/>
