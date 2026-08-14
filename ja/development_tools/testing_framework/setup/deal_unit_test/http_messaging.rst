.. _deal_unit_test_setting_http_messaging:

取引単体テストの設定（HTTPメッセージング）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

HTTPメッセージングの取引単体テストでは、HTTPメッセージ送信を伴うテストで使用するモックアップクラスを登録する。

使用方法
--------------------------------------------------

.. tip::

  以下の設定はアーキテクトが行う。テストを実装するアプリケーション開発者が設定する必要はない。

モックアップクラスを登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTPメッセージ送信を伴う取引単体テストでは、テスティングフレームワークが提供するモックアップクラス\ :java:extdoc:`MockMessagingClient <nablarch.test.core.messaging.MockMessagingClient>`\ を使用する。このクラスを使用すると、メッセージの送信は行われず、テストデータに記述した内容から応答電文が生成されて返される。コンポーネント設定ファイルに、次のとおり登録する。

.. code-block:: xml

  <!-- HTTP通信用クライアント -->
  <component name="defaultMessageSenderClient"
             class="nablarch.test.core.messaging.MockMessagingClient">
    <property name="charset" value="Shift-JIS"/>
  </component>

コンポーネント名の指定方法は\ :ref:`リクエスト単体テストの設定（HTTPメッセージング） <request_unit_test_setting_http_messaging>`\ と同じである。

``charset``\ には、メッセージングログに出力する電文の文字コード名を指定する。この項目は省略でき、省略した場合は\ ``UTF-8``\ が使用される。

応答電文のテストデータは、ベースディレクトリとテストデータを解析するコンポーネントをあわせて設定しないと読み込まれない。\ :ref:`同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する <testing_framework_common-send_sync_test_data>`\ を参照。

電文のフォーマットとデータの記述方法は\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。
