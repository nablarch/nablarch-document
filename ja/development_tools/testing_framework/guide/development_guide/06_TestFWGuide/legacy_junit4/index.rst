.. _legacy_junit4_testfw_guide:

==============================================================
自動テストフレームワークをJUnit 4で使用する（既存資産向け）
==============================================================

本セクションは、JUnit 4をベースに作成された既存のテスト資産を保守するプロジェクト向けのガイドである。

自動テストフレームワークはJUnit 4の上でも使用できる。
JUnit 4で作成された既存のテストコードは修正せずにそのまま使用でき、JUnit Vintageを併用することでJUnit 5の上でも実行できる（ :ref:`run_ntf_on_junit5_with_vintage_engine` を参照）。

.. important::

  新規にテストを作成する場合は、JUnit 5（ :ref:`ntf_junit5_extension` ）の使用を推奨する。

.. _legacy_junit4_how_to_write:

--------------------------------
JUnit 4でのテストクラスの書き方
--------------------------------

JUnit 4で自動テストフレームワークを使用する場合、テストに必要な機能を実装したクラス（ :java:extdoc:`TestSupport <nablarch.test.TestSupport>` など）をテストクラスが継承することで、それらのクラスが持つ機能をテストクラスから使用する。

.. code-block:: java

  import org.junit.Test;

  import nablarch.test.core.db.DbAccessTestSupport;

  // 自動テストフレームワークが提供するクラスを継承する
  public class SampleTest extends DbAccessTestSupport {

      // テストメソッドには org.junit.Test を付与する
      @Test
      public void testSomething() {
          // 継承したメソッドを直接呼び出せる
          setUpDb("testSomething");
          // テスト処理
      }
  }

テストの種類ごとに継承するクラスは以下の通り。

.. list-table:: テストの種類と継承するクラスの対応
   :header-rows: 1

   * - テストの種類
     - 継承するクラス
   * - 汎用（Excelからのテストデータ読み込みなど）
     - :java:extdoc:`TestSupport <nablarch.test.TestSupport>`
   * - クラス単体テスト（データベースアクセスあり）
     - :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`
   * - Form/Entityのクラス単体テスト
     - :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`
   * - リクエスト単体テスト（ウェブアプリケーション）
     - :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`
   * - リクエスト単体テスト（RESTfulウェブサービス）
     - :java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>` または :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`
   * - リクエスト単体テスト（バッチ）
     - :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`
   * - リクエスト単体テスト（同期応答メッセージ受信）
     - :java:extdoc:`MessagingRequestTestSupport <nablarch.test.core.messaging.MessagingRequestTestSupport>`
   * - リクエスト単体テスト（応答不要メッセージ受信）
     - :java:extdoc:`MessagingReceiveTestSupport <nablarch.test.core.messaging.MessagingReceiveTestSupport>`
   * - 結合テスト
     - :java:extdoc:`IntegrationTestSupport <nablarch.test.core.integration.IntegrationTestSupport>`

各テストの実施方法（テストデータの書き方や検証方法）は、 :ref:`unitTestGuide` および :ref:`testFWGuide` の各ページと共通である。
各ページのJUnit 5のコード例を、本ページの継承モデル（継承したメソッドを直接呼び出す形）に読み替えること。
JUnit 4版のコード例が提供されているページについては、 :ref:`legacy_junit4_unittest_guide` を参照すること。

.. toctree::
   :maxdepth: 1

   01_tips_junit4
