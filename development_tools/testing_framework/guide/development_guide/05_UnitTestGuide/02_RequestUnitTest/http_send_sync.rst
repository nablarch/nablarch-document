.. _`message_httpSendSyncMessage_test`:

=============================================================================
リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)
=============================================================================

リクエスト単体テスト実施方法は、\ :ref:`message_sendSyncMessage_test`\ を参照すること。

ただし、「送信キュー」「受信キュー」を「通信先」と読み替えること。

本項では、\ :ref:`message_sendSyncMessage_test`\ と異なる箇所の解説を行う。


----------------------
テストケースの記述単位
----------------------

HTTP同期応答メッセージ送信処理については、1シート、1ケースで記述することを **強く** 推奨する。

同一シート内では、同一リクエストIDのメッセージの電文の長さを統一する必要があるためである。


.. _`http_send_sync_request_write_test_data`:

--------------------
テストデータの書き方
--------------------

以下に、実際にExcelで書かれたテストデータを示す。


.. image:: ./_image/http_send_sync.png
    :scale: 80


.. important::
 リクエスト単体テストの対象が複数回メッセージ送信を行う際は、以下の点に注意すること。

 * 異なるリクエストIDのメッセージを送信する際、同一データタイプ( ``RESPONSE_HEADER_MESSAGES`` 等)を複数回記述する必要がある。この場合、同一データタイプは連続で記述すること。データタイプ自体の説明は、\ :ref:`structure_in_excel_sheet`\ を参照。
 * 同一リクエストIDメッセージを一つのテストケースで複数回送信する際は、noの値を変えてまとめて記述すること。
 * 同一リクエストIDメッセージを一つのテストケースで複数回送信する際は、同じ種類の電文は同じ長さにすること。テストケース上、同一の長さにできない場合は、手動でテストを行うこと。

 以下に複数回メッセージ送信を行う際の、応答電文の記述例を示す。

 .. image:: ./_image/http_send_sync_ok_pattern_response.png

 以下に複数回メッセージ送信を行う際の、要求電文の記述例を示す。

 .. image:: ./_image/http_send_sync_ok_pattern_expected.png


また、異なる種類のメッセージを送信する際、送信順のテストは不可能である。
上記の例の場合、 ``ProjectSaveMessage`` より先に、 ``ProjectSaveMessage2`` が送信された場合であってもテストは成功となる。

-----------

モックアップを使用する場合、testShotsに"expectedMessageByClient"および"responseMessageByClient"にグループIDを設定する。
グループIDの関連については\ :ref:`message_sendSyncMessage_test`\ における"expectedMessage"および"responseMessage"の場合と同様であるため割愛する。

.. image:: ./_image/http_send_sync_shot.png



| 同一アクション内でMOMによる同期応答メッセージ送信処理とHTTP同期応答メッセージ送信処理が同時に行われる場合、
| "expectedMessage"、"responseMessage"にMOMによる同期応答メッセージ送信処理で使用するグループIDを、
| "expectedMessageByClient"、"responseMessageByClient"にHTTP同期応答メッセージ送信処理で使用するグループIDを
| それぞれ個別に指定する。

.. image:: ./_image/http_mom_send_sync_shot.png


.. tip::


  グループIDはMOMによる同期応答メッセージ送信処理とHTTP同期応答メッセージ送信処理でそれぞれ別の値を設定する必要がある。
  同一のグループIDを指定した場合、正しく結果検証が行われないため、注意すること。


-----------

テストデータのディレクティブ行に設定されたfile-typeの値により、要求電文のアサート方法が変化する。

設定方法やアサート内容についての詳細は :ref:`real_request_test` のレスポンスメッセージの項を参照すること。

------------------------------------
フレームワークで使用するクラスの設定
------------------------------------

通常、これらの設定はアーキテクトが行うものでありアプリケーションプログラマが設定する必要はない。


モックアップクラスの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンポーネント設定ファイルに、リクエスト単体テストで使用するモックアップクラスを設定する。

 .. code-block:: xml
  
      <!-- HTTP通信用クライアント -->
      <component name="defaultMessageSenderClient" 
                 class="nablarch.test.core.messaging.RequestTestingMessagingClient">
        <property name="charset" value="Shift-JIS"/>
      </component>

なお、\ ``charset``\ に、文字コード名を指定することでログに出力する文字コードを変更することができる。
通常は省略可能で、省略した場合はUTF-8が使用される。



