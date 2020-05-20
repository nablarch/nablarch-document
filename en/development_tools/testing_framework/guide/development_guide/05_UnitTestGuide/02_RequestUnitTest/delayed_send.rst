====================================================================
リクエスト単体テストの実施方法（応答不要メッセージ送信処理）
====================================================================

--------------------
概要
--------------------
応答不要メッセージ送信処理用のアクションクラスは、Nablarchの一部として提供される。
このため、リクエスト単体テストではこのアクションクラスを使用して、以下の\ `テスト対象の成果物`_\ の確認を行う。

**※他の処理のようなアクションクラスに対する条件網羅や、限界値テストなどは実施不要である。**

テスト対象の成果物
===================
* 電文のレイアウトを定義したフォーマット定義ファイル
* 下記3種類のSQL文

  * 電文送信テーブルからステータスが未送信のデータを取得するためのSELECT文
  * 電文送信後に、該当データのステータスを処理済みに更新するためのUPDATE文
  * 電文送信に失敗した場合に、該当データのステータスを送信失敗(エラー)に更新するためのUPDATE文


--------------------
テストクラスの書き方
--------------------

テストクラスは以下の条件を満たすように作成する。

* テストクラスのパッケージは、テスト対象機能のパッケージとする。
* <電文のリクエストID>RequestTestというクラス名でテストクラスを作成する。
* \ ``nablarch.test.core.batch.BatchRequestTestSupport``\ を継承する。

例えば、テスト対象機能のパッケージがnablarch.sample.ss21AA、電文のリクエストIDがRM11AC0301だとすると、テストクラスは以下のようになる。

.. code-block:: java

  package nablarch.sample.ss21AA;
  
  // ～中略～

  public class RM11AC0301RequestTest extends BatchRequestTestSupport {


------------------------------
データシートの書き方
------------------------------
`テスト対象の成果物`_ のテストを行うために必要なデータシートの記述方法を説明する。

データシートの記述方法は、\ :ref:`message_sendSyncMessage_test`\ を参照すること。
本項では、\ :ref:`message_sendSyncMessage_test`\ と記述方法が異なる箇所の解説を行う。


正常系ケースの準備
=======================

 | 電文が正しく送信されるケースの確認を実施する。
 | このケースでは、送信された電文の確認及び該当データのステータス更新の確認を行う。
 |
 | 応答不要メッセージ送信処理用のアクションクラスは、起動パラメータとしてメッセージのリクエストIDを要求する。
 | このため、「testShots」の定義に下記画像のように「KEY=messageRequestId」、「VALUE=メッセージのリクエストID」を追加する必要がある。

 .. image:: _image/delayed_send.png
    :scale: 50

 .. tip::

  データシートには、下記設定が不要となる。

  * testShotsの定義

    * responseMessage

  * 期待値及び準備データの定義

    * RESPONSE_HEADER_MESSAGES
    * RESPONSE_BODY_MESSAGES

異常系ケースの準備
=======================
  
 | 異常系のテストは、メッセージの送信に失敗した場合に該当データのステータスをエラーに更新するUPDATE文を確認するために必要である。
 | 異常系テストケースを実施するには、「testShots」の定義に下記画像のように「KEY=errorCase」、「VALUE=true」と設定すれば良い。
 | なお、異常系ケースでは電文が送信されないため送信電文の期待値を設定する必要はない。

 .. image:: _image/delayed_send_error.png
    :scale: 70

 .. tip:: 
   異常系テストケースを実施する場合には、応答不要メッセージ送信処理用共通アクションをテスト用アクションに切り替える必要がある。
   以下にその設定例を示す。

   * 本番用設定例

     .. code-block:: xml

      <!--ディスパッチ用ハンドラ-->
      <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
        <!-- 応答不要メッセージ送信処理用共通アクションを設定する。 -->
        <property name="basePackage" value="nablarch.fw.messaging.action.AsyncMessageSendAction" />
        <property name="immediate" value="false" />
      </component>

   * テスト用設定

     上記本番環境用設定をテスト用のアクションクラスで上書きを行う。

     .. code-block:: xml

      <!--ディスパッチ用ハンドラ-->
      <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
        <property name="basePackage" value="nablarch.test.core.messaging.AsyncMessageSendActionForUt" />
        <property name="immediate" value="false" />
      </component>

