.. _legacy_junit4_request_deal_test:

======================================================
リクエスト単体テスト・取引単体テスト（JUnit 4）
======================================================

.. important::

  本ページはJUnit 4で作成された既存のテスト資産を保守するプロジェクト向けである。
  新規にテストを作成する場合は、JUnit 5版の :ref:`requestUnitTest` および各実行基盤のリクエスト単体テストのページを参照すること。

JUnit 4では、テスティングフレームワークが提供するテストサポートクラスをテストクラスが継承して使用する。
テストデータの書き方・検証方法はJUnit 5版の各ページと共通であり、本ページではテストクラスの書き方の差分（継承モデル）のみを示す。
JUnit 5版のコード例を読み替える場合は、テストクラスの宣言を以下の形に置き換えた上で、 ``support.`` を介したメソッド呼び出しを継承メソッドの直接呼び出しにすればよい。

ウェブアプリケーション
======================

``nablarch.test.core.http.BasicHttpRequestTestTemplate`` を継承し、 ``getBaseUri()`` をオーバーライドする。

.. code-block:: java

  package nablarch.sample.management.user;

  // ～中略～

  public class UserSearchActionRequestTest extends BasicHttpRequestTestTemplate {

      /** URIの共通部分を返却する。 */
      @Override
      protected String getBaseUri() {
          return "/action/management/user/UserSearchAction/";
      }

      @Test
      public void testUsers00101Normal() {
          execute();
      }
  }

RESTfulウェブサービス
=====================

``nablarch.test.core.http.RestTestSupport`` （テストデータの投入とデータベースのアサートが不要な場合は ``nablarch.test.core.http.SimpleRestTestSupport`` ）を継承する。

.. code-block:: java

  public class SampleTest extends RestTestSupport {

      @Test
      public void プロジェクト一覧が取得できること() {
          String message = "プロジェクト一覧取得";

          RestMockHttpRequest request = get("/projects");
          HttpResponse response = sendRequest(request);
          assertStatusCode(message, HttpResponse.Status.OK, response);
      }
  }

バッチ処理（応答不要メッセージ送信処理を含む）
==============================================

``nablarch.test.core.batch.BatchRequestTestSupport`` を継承する。

.. code-block:: java

  package nablarch.sample.ss21AA;

  // ～中略～

  public class RM21AA001ActionRequestTest extends BatchRequestTestSupport {

      @Test
      public void testRegisterUser() {
          execute();
      }
  }

同期応答メッセージ受信処理
==========================

``nablarch.test.core.messaging.MessagingRequestTestSupport`` を継承する。

.. code-block:: java

  package nablarch.sample.ss21AA;

  // ～中略～

  public class RM21AA001ActionRequestTest extends MessagingRequestTestSupport {

      @Test
      public void testRegisterUser() {
          execute();
      }
  }

応答不要メッセージ受信処理
==========================

``nablarch.test.core.messaging.MessagingReceiveTestSupport`` を継承する。

.. code-block:: java

  package nablarch.sample.ss21AA;

  // ～中略～

  public class RM21AA100RequestTest extends MessagingReceiveTestSupport {

      @Test
      public void testRegisterUser() {
          execute();
      }
  }

取引単体テスト
==============

リクエスト単体テストと同じテストサポートクラス（バッチは ``BatchRequestTestSupport`` 、メッセージングは ``MessagingRequestTestSupport`` ）を継承する。

.. code-block:: java

  package nablarch.sample.ss21AC01

  import nablarch.test.core.batch.BatchRequestTestSupport;

  // 中略

  public class B21AC01Test extends BatchRequestTestSupport {

      /** 正常終了するケース */
      @Test
      public void testSuccess() {
          execute();
      }
  }
