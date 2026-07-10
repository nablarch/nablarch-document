.. _junit4_to_junit5_migration:

========================================
JUnit 4からJUnit 5への移行手順
========================================

.. contents:: 目次
  :depth: 2
  :local:

本ページでは、JUnit 4で作成された自動テストフレームワークのテストコードを、JUnit 5（ :ref:`ntf_junit5_extension` ）へ移行する手順を説明する。

.. tip::

  既存のテストを一括で移行する必要はない。
  JUnit VintageによりJUnit 4のテストとJUnit 5のテストは同一プロジェクト内で共存できるため（ :ref:`migration_vintage_coexistence` を参照）、
  既存のテストはJUnit 4のまま維持し、新規のテストだけJUnit 5で作成する段階的な移行が可能である。

-----------------------------
移行の全体像
-----------------------------

JUnit 4の自動テストフレームワークのテストは「テストサポートクラスを継承する」モデルで書かれている。
JUnit 5用拡張機能では、これを「合成アノテーション＋フィールドインジェクション」モデルに置き換える。

移行作業は、テストクラスごとに以下の機械的な書き換えで完了することがほとんどである。

#. 継承宣言（ ``extends`` ）を削除し、対応する合成アノテーションをテストクラスに付与する
#. 継承していたテストサポートクラス型のフィールドを宣言する（インスタンスは拡張機能がインジェクションする）
#. 継承メソッドの直接呼び出しを、フィールドを介した呼び出し（ ``support.`` ）に変更する
#. JUnit 4のアノテーション・アサーションのimportをJUnit 5のものへ変更する

-----------------------------
テストサポートクラスの対応表
-----------------------------

継承していたテストサポートクラスに応じて、以下の合成アノテーションを使用する。

.. list-table:: 継承クラスと合成アノテーションの対応
   :header-rows: 1

   * - JUnit 4で継承していたクラス
     - 付与する合成アノテーション
   * - :java:extdoc:`TestSupport <nablarch.test.TestSupport>`
     - :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`
   * - :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`
     - :java:extdoc:`BatchRequestTest <nablarch.test.junit5.extension.batch.BatchRequestTest>`
   * - :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`
     - :java:extdoc:`DbAccessTest <nablarch.test.junit5.extension.db.DbAccessTest>`
   * - :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`
     - :java:extdoc:`EntityTest <nablarch.test.junit5.extension.db.EntityTest>`
   * - :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`
     - :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` （ ``baseUri`` の指定が必要）
   * - :java:extdoc:`HttpRequestTestSupport <nablarch.test.core.http.HttpRequestTestSupport>`
     - :java:extdoc:`HttpRequestTest <nablarch.test.junit5.extension.http.HttpRequestTest>`
   * - :java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>`
     - :java:extdoc:`RestTest <nablarch.test.junit5.extension.http.RestTest>`
   * - :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`
     - :java:extdoc:`SimpleRestTest <nablarch.test.junit5.extension.http.SimpleRestTest>`
   * - :java:extdoc:`IntegrationTestSupport <nablarch.test.core.integration.IntegrationTestSupport>`
     - :java:extdoc:`IntegrationTest <nablarch.test.junit5.extension.integration.IntegrationTest>`
   * - :java:extdoc:`MessagingReceiveTestSupport <nablarch.test.core.messaging.MessagingReceiveTestSupport>`
     - :java:extdoc:`MessagingReceiveTest <nablarch.test.junit5.extension.messaging.MessagingReceiveTest>`
   * - :java:extdoc:`MessagingRequestTestSupport <nablarch.test.core.messaging.MessagingRequestTestSupport>`
     - :java:extdoc:`MessagingRequestTest <nablarch.test.junit5.extension.messaging.MessagingRequestTest>`

-----------------------------
アノテーション・APIの対応表
-----------------------------

JUnit本体のアノテーション・アサーションは以下のように読み替える。

.. list-table:: JUnit 4とJUnit 5の対応
   :header-rows: 1

   * - JUnit 4
     - JUnit 5
   * - ``org.junit.Test``
     - ``org.junit.jupiter.api.Test``
   * - ``org.junit.Before`` / ``org.junit.After``
     - ``org.junit.jupiter.api.BeforeEach`` / ``org.junit.jupiter.api.AfterEach``
   * - ``org.junit.BeforeClass`` / ``org.junit.AfterClass``
     - ``org.junit.jupiter.api.BeforeAll`` / ``org.junit.jupiter.api.AfterAll``
   * - ``org.junit.Ignore``
     - ``org.junit.jupiter.api.Disabled``
   * - ``org.junit.Assert.assertEquals`` など
     - ``org.junit.jupiter.api.Assertions.assertEquals`` など
   * - ``@Test(expected = ...)``
     - ``org.junit.jupiter.api.Assertions.assertThrows``
   * - ``org.junit.Assert.assertThat``
     - ``org.hamcrest.MatcherAssert.assertThat`` （Hamcrestを継続使用する場合）

その他のJUnit本体の機能の対応については、 `公式の移行ガイド(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/#migrating-from-junit4>`_ を参照のこと。

-----------------------------
書き換えレシピ
-----------------------------

以下に、Form/Entity単体テスト（EntityTestSupport）の書き換え例を示す。他のテストサポートクラスでも手順は同じである。

**移行前（JUnit 4）**

.. code-block:: java

  import nablarch.test.core.db.EntityTestSupport;
  import org.junit.Test;

  public class SampleFormTest extends EntityTestSupport {

      private static final Class<?> TARGET_CLASS = SampleForm.class;

      @Test
      public void testCharsetAndLength() {
          // 継承したメソッドを直接呼び出している
          testValidateCharsetAndLength(TARGET_CLASS, "testCharsetAndLength", "charsetAndLength");
      }
  }

**移行後（JUnit 5）**

.. code-block:: java

  import nablarch.test.core.db.EntityTestSupport;
  import nablarch.test.junit5.extension.db.EntityTest;
  import org.junit.jupiter.api.Test;

  @EntityTest  // 1. 継承の代わりに合成アノテーションを付与する
  class SampleFormTest {

      private static final Class<?> TARGET_CLASS = SampleForm.class;

      // 2. テストサポートクラス型のフィールドを宣言する（インジェクションされる）
      EntityTestSupport support;

      @Test
      void testCharsetAndLength() {
          // 3. フィールドを介してメソッドを呼び出す
          support.testValidateCharsetAndLength(TARGET_CLASS, "testCharsetAndLength", "charsetAndLength");
      }
  }

移行時の注意点
==============

* インジェクション対象のフィールドには値を設定しないこと（nullでない場合、拡張機能はエラー終了する）。
* ``BasicHttpRequestTestTemplate`` からの移行では、 ``getBaseUri()`` のオーバーライドを削除し、合成アノテーションの ``baseUri`` にURIの共通部分を指定する。
* テストサポートクラスの ``protected`` メソッドは、インジェクション方式ではテストクラスから呼び出せない。
  public版の代替メソッド（例: ``readTextResource(Class, String)`` ）を使用する。
* 引数なしの ``execute()`` は、JUnit 5でもテストメソッド名からシート名を解決する（従来と同じ動作）。
* テストサポートクラスを継承した独自拡張クラス（JUnit 4の ``TestRule`` を使用している場合を含む）の移行方法は、
  :ref:`ntf_junit5_extension` の「独自の拡張を加える」を参照すること。

.. _migration_vintage_coexistence:

-----------------------------
JUnit Vintageによる共存
-----------------------------

JUnit 5のJUnit Vintageを使用すると、JUnit 4で書かれた既存のテストを修正せずにJUnit 5の上で実行できる。
これにより、既存のテストはJUnit 4のまま維持しつつ、新規のテストだけをJUnit 5で作成する段階的な移行ができる。

依存関係の追加方法などの詳細は、 :ref:`run_ntf_on_junit5_with_vintage_engine` を参照すること。

.. important::

  JUnit Vintageは、あくまでJUnit 4のテストをJUnit 4として動かすものである。
  JUnit 4のテストの中でJUnit 5の機能（パラメータ化テストなど）を使いたい場合は、本ページの手順でJUnit 5へ移行する必要がある。
