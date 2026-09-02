.. _request_unit_test_setting_http_messaging:

リクエスト単体テストの設定（HTTPメッセージング）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
HTTPメッセージングのリクエスト単体テストは、通信先を用意せずに実施する。HTTPメッセージ送信を伴うテストでは、電文を実際に送る代わりに、テストデータにもとづいて要求電文の検証と応答電文の返却を行うモックアップクラスを登録する。HTTPメッセージ受信のテストで設定が要るのは、フレームワーク制御ヘッダのフィールド名をデフォルトから変更している場合だけである。テストの実装方法は\ :ref:`リクエスト単体テスト（HTTPメッセージング） <request_unit_test_http_messaging>`\ を参照。

使用方法
--------------------------------------------------

モックアップクラスを登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTPメッセージ送信を伴うリクエスト単体テストでは、テスティングフレームワークが提供するモックアップクラス\ :java:extdoc:`RequestTestingMessagingClient <nablarch.test.core.messaging.RequestTestingMessagingClient>`\ を使用する。ウェブアプリケーションやNablarchバッチアプリケーションのリクエスト単体テストで、テスト対象がHTTPメッセージ送信を行う場合も同じである。このクラスを使用すると、電文の送信は行われず、要求電文のアサートと応答電文の返却がテストデータの内容にもとづいて行われる。コンポーネント設定ファイルに、次のとおり登録する。

.. code-block:: xml

  <!-- HTTP通信用クライアント -->
  <component name="defaultMessageSenderClient"
             class="nablarch.test.core.messaging.RequestTestingMessagingClient">
    <property name="charset" value="Shift-JIS"/>
  </component>

コンポーネント名には、環境設定ファイルの\ ``messageSender.<リクエストID>.messageSenderClient``\ に指定した名前を使用する。この名前で参照されていないコンポーネントは、モックアップクラスとして使用されない。

``charset``\ には、\ :ref:`メッセージングログ <messaging_log>`\ に出力する電文の文字コード名を指定する。この項目は省略でき、省略した場合は\ ``UTF-8``\ が使用される。

.. _request_unit_test_setting_http_messaging-fw_header:

フレームワーク制御ヘッダのフィールド名を指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージ受信のテストで、\ :ref:`フレームワーク制御ヘッダのフィールド名 <testdata_notation-messaging_data>`\ をデフォルトから変更している場合は、環境設定ファイルに\ ``reader.fwHeaderfields``\ を設定し、フィールド名をカンマ区切りで指定する。この設定は、HTTPメッセージングと\ :ref:`MOMによるメッセージング <request_unit_test_setting_mom>`\ で共通である。指定した名前はデフォルトのフィールド名に追加されるのではなく、デフォルトのフィールド名をすべて置き換える。名前を変更していないフィールドも含めて、使用するフィールド名をすべて列挙する。値に空白を含めると、空白も含めてフィールド名として扱われるため、カンマの前後に空白を入れない。

.. code-block:: properties

  # 使用するフレームワーク制御ヘッダのフィールド名を、すべてカンマ区切りで列挙する。
  reader.fwHeaderfields=requestId,addHeader

.. important::

  この設定が必要なのは、\ Excel\ 形式のテストデータの場合である。\ YAML\ 形式では\ ``fw_header:``\ に記載したキーがすべてフレームワーク制御ヘッダとして扱われるため、この設定は使用されない。メッセージ送信のテストでも、この設定は使用されない。
