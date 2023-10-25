.. _`restful_web_service_functional_comparison`:

Jakarta RESTful Web Servicesサポート/Jakarta RESTful Web Services/HTTPメッセージングの機能比較
=================================================================================================

.. contents:: 目次
  :depth: 3
  :local:

ここでは、以下の機能比較を示す。

 - :ref:`NablarchのJakarta RESTful Web Servicesサポート <restful_web_service>`
 - :ref:`HTTPメッセージング <http_messaging>`
 - `Jakarta RESTful Web Services(外部サイト、英語) <https://jakarta.ee/specifications/restful-ws/>`_

.. tip::

 NablarchのJakarta RESTful Web ServicesサポートとHTTPメッセージングのみ、表内のマークをクリックすると、解説書の説明ページに遷移する。

.. |br| raw:: html

   <br />

.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
   :header-rows: 1
   :class: something-special-class

   * - 機能
     - Jakarta RESTful |br| Web Services |br| サポート
     - HTTP |br| メッセージング
     - Jakarta RESTful |br| Web Services
   * - リクエストとリソースメソッドのマッピング
     - :ref:`△ <rest-action_mapping>`
     - :ref:`○ <http_messaging-action_mapping>`
     - ○
   * - リクエストとパラメータのマッピング
     - :ref:`△ <rest-path_query_param>`
     - × [1]_
     - ○
   * - HTTPメソッドのマッチング
     - :ref:`△ <rest-action_mapping>`
     - × [1]_
     - ○
   * - メディアタイプに応じた |br| リクエスト/レスポンスの変換
     - :ref:`△ <body_convert_handler>`
     - × [1]_
     - ○
   * - エンティティのバリデーション
     - :ref:`○ <rest-request_validation>`
     - :ref:`○ <http_messaging-request_validation>`
     - ○
   * - リソースクラスへのインジェクション |br| (Jakarta Contexts and Dependency Injection)
     - × [2]_
     - × [2]_
     - ○
   * - リクエスト/レスポンスに対するフィルタ
     - × [3]_
     - × [3]_
     - ○
   * - ボディの読み書きに対するインターセプタ
     - × [4]_
     - × [5]_
     - ○
   * - クライアントAPI
     - × [6]_
     - :ref:`○ <http_system_messaging-message_send>`
     - ○
   * - 非同期処理
     - × [7]_
     - × [7]_
     - ○
   * - エラー時ログ出力
     - :ref:`○ <jaxrs_response_handler-error_log>`
     - :ref:`○ <http_messaging_error_handler-error_response_and_log>`
     - －
   * - リクエストボディの最大容量チェック
     - × [8]_
     - :ref:`○ <http_messaging_request_parsing_handler-limit_size>`
     - －
   * - 証跡ログの出力
     - × [9]_
     - :ref:`○ <messaging_log>`
     - －
   * - 再送制御
     - × [9]_
     - :ref:`○ <message_resend_handler>`
     - －
   * - サービス提供の可否チェック
     - × [10]_
     - × [10]_
     - －
   * - トランザクション制御
     - × [11]_
     - × [11]_
     - －
   * - 業務処理エラー時のコールバック
     - × [12]_
     - :java:extdoc:`○ <nablarch.fw.messaging.action.MessagingAction>`
     - －

.. [1] HTTPメッセージングはRESTを考慮した作りになっていない。RESTfulウェブサービスには、Jakarta RESTful Web Servicesサポートを使用する。
.. [2] Jakarta RESTful Web ServicesサポートとHTTPメッセージングは、Nablarchのウェブアプリケーションとして動作するため、Jakarta Contexts and Dependency Injectionは使用できない。
.. [3] リクエスト/レスポンスに対するフィルタを作りたい場合は、ハンドラを作成する。
.. [4] ボディの読み書きに対するインターセプタを作りたい場合は、Jakarta RESTful Web ServicesサポートのBodyConverterを作成する。
.. [5] ボディの読み書きにはNablarchのデータフォーマットを使用している。変更したい場合は、データフォーマットのDataRecordFormatterを作成する。
.. [6] Jakarta RESTful Web Servicesクライアントが必要な場合は、Jakarta RESTful Web Servicesの実装(JerseyやRESTEasyなど)を使用する。
.. [7] サーバサイドで非同期処理が必要になる要件がないと想定している。要望があれば対応を検討する。
.. [8] ウェブサーバやアプリケーションサーバにあるリクエストサイズをチェックする機能を使用する。
.. [9] アプリケーションごとに要件が異なると想定している。アプリケーションで設計/実装する。
.. [10] Nablarchにあるサービス提供可否チェックがアプリケーションの要件にマッチする場合はそれを使用する。マッチしない場合は、アプリケーションで設計/実装する。
.. [11] Nablarchにあるトランザクション管理を使用する。
.. [12] エラー処理は共通化し、JaxRsResponseHandlerをカスタマイズすることを想定している。業務処理で個別にエラー処理をしたい場合は、リソースメソッドにてtry/catchを使用する。
