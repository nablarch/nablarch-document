.. _ntf_junit5_extension:

========================================
 JUnit 5用拡張機能
========================================

.. contents:: 目次
  :depth: 3
  :local:

-----
概要
-----

ここでは、JUnit 5で書かれたテストの中で自動テストフレームワークを使用するための拡張機能について説明する。
本拡張機能を利用することで、パラメータ化テストなどのJUnit 5が提供する便利な機能と自動テストフレームワークを組み合わせて使用できるようになる。

.. tip::
  本拡張機能を導入しても、JUnit 4で書かれた既存の自動テストフレームワークのテストを修正する必要はない。
  JUnit 4で書かれたテストは、JUnit Vintageを使うことで引き続きJUnit 5上で実行できる（JUnit Vintageを使って自動テストフレームワークを動作させる方法については :ref:`run_ntf_on_junit5_with_vintage_engine` を参照）。
  したがって、既存のテストはJUnit 4のコードのままにしておき、新規テストだけJUnit 5を使ったコードにすることができる。

----------
前提条件
----------

JUnit 5を利用するには、以下の条件を満たしている必要がある。

* Java 8 以上
* maven-surefire-plugin の 2.22.0 以上

また本ページは、JUnit 5の導入方法やテストケースの作成方法などの基本的な知識を有していることを前提としているため、それらの手順については記載していない。
JUnit 5 自体についての情報は、 `公式のユーザーガイド（外部サイト、英語） <https://junit.org/junit5/docs/5.8.2/user-guide/>`_ を参照のこと。

---------------
モジュール一覧
---------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-junit5</artifactId>
    <scope>test</scope>
  </dependency>

.. _ntf_junit5_extension_standard_usages:

---------------
基本的な使い方
---------------

自動テストフレームワークは、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` などのテストに必要な機能を実装したクラスを提供している。
従来のJUnit 4では、これらの自動テストフレームワークが提供するクラスをテストクラスが継承することで、提供するクラスが持つ機能をテストクラスから利用できるようにしていた。

本拡張機能は、自動テストフレームワークが提供するクラスのインスタンスを拡張機能側で生成し、テストクラスにインジェクションする仕組みを提供する。
この仕組みには、JUnit 5の `Extension (外部サイト、英語) <https://junit.org/junit5/docs/5.8.2/user-guide/#extensions>`_ を利用している。

本拡張機能では、自動テストフレームワークが提供するクラスごとに **Extension クラス** と **合成アノテーション** を用意している。
例えば、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` には :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` と :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>` が用意されている。

.. tip::
  合成アノテーションはJUnit 5が提供する機能で、複数のアノテーションの設定を別の１つのアノテーションにまとめることができる。
  詳しくは `公式ガイドの「2.1.1. Meta-Annotations and Composed Annotations」(外部サイト、英語) <https://junit.org/junit5/docs/5.8.2/user-guide/#writing-tests-meta-annotations>`_ を参照のこと。


これらのクラスを使って以下のように実装することで、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` をテストで使用できるようになる。

.. code-block:: java

  // 1. 対応する合成アノテーションをテストクラスに設定する
  @NablarchTest
  class YourTest {
      // 2. 使用するクラスをテストクラスのフィールドとして宣言する
      TestSupport support;

      @Test
      void test() {
          ...
          // 3. テスト内で使用する
          Map<String, String> map = support.getMap(sheetName, id);
          ...
      }
  }

:java:extdoc:`TestSupport <nablarch.test.TestSupport>` をテストクラスで使用する場合は、まず対応する合成アノテーション(:java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`)をテストクラスに設定する。
これにより、 :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` がテストクラスに対して適用される。

次に、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` 型のインスタンスフィールドをテストクラスに宣言する。
このとき、インスタンスフィールドの可視性は何でも構わない。

拡張機能は、テスト実行前に対応するクラス（ここでは :java:extdoc:`TestSupport <nablarch.test.TestSupport>`）のインスタンスを生成する。
そして、テストクラスに代入可能なフィールドを見つけると、自動的にインスタンスをインジェクションする。

.. warning::

  インジェクション対象となるフィールドがnullでない場合、拡張機能はエラー終了するので値は設定しないこと。

---------------------------------------------
Extension クラスと合成アノテーションの一覧
---------------------------------------------

本拡張機能では、以下のExtensionクラスと合成アノテーションを提供している。


.. list-table:: 拡張機能が提供するExtensionクラスと合成アノテーションの一覧
   :header-rows: 1

   * - 自動テストフレームワークが提供するクラス
     - Extension クラス
     - 合成アノテーション
   * - :java:extdoc:`TestSupport <nablarch.test.TestSupport>`
     - :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`
     - :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`
   * - :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`
     - :java:extdoc:`BatchRequestTestExtension <nablarch.test.junit5.extension.batch.BatchRequestTestExtension>`
     - :java:extdoc:`BatchRequestTest <nablarch.test.junit5.extension.batch.BatchRequestTest>`
   * - :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`
     - :java:extdoc:`DbAccessTestExtension <nablarch.test.junit5.extension.db.DbAccessTestExtension>`
     - :java:extdoc:`DbAccessTest <nablarch.test.junit5.extension.db.DbAccessTest>`
   * - :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`
     - :java:extdoc:`EntityTestExtension <nablarch.test.junit5.extension.db.EntityTestExtension>`
     - :java:extdoc:`EntityTest <nablarch.test.junit5.extension.db.EntityTest>`
   * - :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`
     - :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>`
     - :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`
   * - :java:extdoc:`HttpRequestTestSupport <nablarch.test.core.http.HttpRequestTestSupport>`
     - :java:extdoc:`HttpRequestTestExtension <nablarch.test.junit5.extension.http.HttpRequestTestExtension>`
     - :java:extdoc:`HttpRequestTest <nablarch.test.junit5.extension.http.HttpRequestTest>`
   * - :java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>`
     - :java:extdoc:`RestTestExtension <nablarch.test.junit5.extension.http.RestTestExtension>`
     - :java:extdoc:`RestTest <nablarch.test.junit5.extension.http.RestTest>`
   * - :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`
     - :java:extdoc:`SimpleRestTestExtension <nablarch.test.junit5.extension.http.SimpleRestTestExtension>`
     - :java:extdoc:`SimpleRestTest <nablarch.test.junit5.extension.http.SimpleRestTest>`
   * - :java:extdoc:`IntegrationTestSupport <nablarch.test.core.integration.IntegrationTestSupport>`
     - :java:extdoc:`IntegrationTestExtension <nablarch.test.junit5.extension.integration.IntegrationTestExtension>`
     - :java:extdoc:`IntegrationTest <nablarch.test.junit5.extension.integration.IntegrationTest>`
   * - :java:extdoc:`MessagingReceiveTestSupport <nablarch.test.core.messaging.MessagingReceiveTestSupport>`
     - :java:extdoc:`MessagingReceiveTestExtension <nablarch.test.junit5.extension.messaging.MessagingReceiveTestExtension>`
     - :java:extdoc:`MessagingReceiveTest <nablarch.test.junit5.extension.messaging.MessagingReceiveTest>`
   * - :java:extdoc:`MessagingRequestTestSupport <nablarch.test.core.messaging.MessagingRequestTestSupport>`
     - :java:extdoc:`MessagingRequestTestExtension <nablarch.test.junit5.extension.messaging.MessagingRequestTestExtension>`
     - :java:extdoc:`MessagingRequestTest <nablarch.test.junit5.extension.messaging.MessagingRequestTest>`

BasicHttpRequestTest の使い方の補足
====================================

:java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` 以外は、 :ref:`ntf_junit5_extension_standard_usages` で説明した方法で使用できる。

:java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` のみ、合成アノテーションである :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` を使用するときにパラメータを指定する必要があるので、その点について補足する。

.. code-block:: java

  // 1. BasicHttpRequestTest の baseUri を指定する
  @BasicHttpRequestTest(baseUri = "/test/")
  class YourTestClass {
      // 2. BasicHttpRequestTestTemplate のインジェクション方法は、他と変わらない
      BasicHttpRequestTestTemplate support;

      @Test
      void test() {
          support.execute();
      }
  }

:java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` アノテーションには ``baseUri`` を指定する必要がある。
この値は、 :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` の ``getBaseUri()`` メソッドが返却する値に対応する。

-------------------
独自の拡張を加える
-------------------

自動テストフレームワークが提供するクラスを継承し、独自の拡張を加える場合の対応方法について説明する。

.. tip::
  ここで説明する手順は、JUnit 4で書かれた既存の独自拡張クラスを本拡張機能用に利用する場合にも適用できる。

独自拡張クラスを作成する場合は、大きく次のようにして対応する。

#. 自動テストフレームワークが提供するクラスを継承し、独自拡張クラスを作成する
#. 継承元のクラスに対応するExtensionクラスを継承した独自拡張用のExtensionを作成し、独自拡張クラスのインスタンスを生成するように実装する
#. ``ExtendWith`` アノテーションを使って独自Extensionクラスをテストクラスに適用する

独自拡張クラスを作成する
========================

ここでは、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` を拡張したクラスを作成する場合を例にして説明する。

まず、 :java:extdoc:`TestSupport <nablarch.test.TestSupport>` を継承した独自拡張クラスを作成する。

.. code-block:: java

  public class CustomTestSupport extends TestSupport {
      // テストクラスの Class インスタンスを TestSupport のコンストラクタに渡せるように実装する
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }

      // 独自の拡張メソッドを実装する
  }

基本的に、自動テストフレームワークが提供するクラスは、インスタンス生成時にテストクラスの ``Class`` オブジェクトを渡す必要がある。
したがって、独自拡張クラスにはテストクラスの ``Class`` オブジェクトを受け取れるようにコンストラクタを定義する必要がある。

.. tip::
  :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>` は、テストクラスの ``Class`` オブジェクトをコンストラクタで渡さなくても使用できる。

独自拡張用のExtensionを作成する
====================================

次に、拡張元のクラスに対応するExtensionクラスを継承し、独自拡張用のExtensionを作成する。
例では :java:extdoc:`TestSupport <nablarch.test.TestSupport>` を継承しているので、対応するExtensionクラスは :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` になる。

.. tip::
  :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` を直接継承した独自拡張クラスを使用する場合、対応するExtensionとしては :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>` が使用できる。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      // createSupport() をオーバーライドし、独自拡張クラスのインスタンスを返すように実装する
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  }

独自拡張用のExtensionでは、 ``createSupport()`` メソッドをオーバーライドする。
そして、先ほど作成した独自拡張クラスのインスタンスを返却するように実装する。

なお、 ``createSupport()`` メソッドで生成した独自拡張クラスのインスタンスは、親クラスの :java:extdoc:`TestEventDispatcherExtension <nablarch.test.junit5.extension.event.TestEventDispatcherExtension>` に定義された ``support`` という :java:extdoc:`TestEventDispatcher <nablarch.test.event.TestEventDispatcher>` 型のインスタンスフィールドに保存される。
このフィールドは ``protected`` なので、サブクラスから参照できる。


ExtendWithでテストクラスに適用する
====================================

作成した独自拡張用のExtensionは、 ``ExtendWith`` アノテーションを使ってテストクラスに適用できる。
以下に実装例を示す。

.. code-block:: java

  ..
  import org.junit.jupiter.api.extension.ExtendWith;
  
  // 1. ExtendWith で独自拡張用のExtensionをテストクラスに適用する
  @ExtendWith(CustomTestSupportExtension.class)
  class YourTest {
      // 2. 独自拡張クラスをインスタンス変数で宣言する
      CustomTestSupport support;

      @Test
      void test() {
          // 3. テスト内で独自拡張クラスを使用する
          support.customMethod();
      }
  }

BasicHttpRequestTestTemplateを拡張する場合はアノテーションも作成する
====================================================================

:java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` または :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>` を拡張する場合は、 ``baseUri`` を独自拡張クラスのインスタンスに連携する必要がある。
``ExtendWith`` ではパラメータの連携ができないので、アノテーションも独自に作成する必要がある。

以下に、 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` での実装例を示す。

.. code-block:: java

  public class CustomHttpRequestTestSupport extends BasicHttpRequestTestTemplate {
      private final String baseUri;
     
      // baseUri を外部から連携できるように実装しておく
      public CustomHttpRequestTestSupport(Class<?> testClass, String baseUri) {
          super(testClass);
          this.baseUri = baseUri;
      }
  
      @Override
      protected String getBaseUri() {
          return baseUri;
      }
  }

まず、 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` を継承して独自拡張クラスを作成する。
このとき、コンストラクタではテストクラスと ``baseUri`` を渡せるようにしておく。

次に、独自拡張クラス用の合成アノテーションを作成する。

.. code-block:: java

  import org.junit.jupiter.api.extension.ExtendWith;
  
  import java.lang.annotation.ElementType;
  import java.lang.annotation.Retention;
  import java.lang.annotation.RetentionPolicy;
  import java.lang.annotation.Target;
  
  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.TYPE)
  // この後作成する独自拡張用のExtensionを指定する
  @ExtendWith(CustomHttpRequestTestExtension.class)
  public @interface CustomHttpRequestTest {
      // baseUri を渡せるように宣言する
      String baseUri();
  }

合成アノテーションでは、 ``baseUri`` を渡せるように宣言する。
``ExtendWith`` で指定する独自拡張用のExtensionは、以下のようにして実装する。

.. code-block:: java

  public class CustomHttpRequestTestExtension extends BasicHttpRequestTestExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          // テストクラスからアノテーションの情報を取得する
          CustomHttpRequestTest annotation = findAnnotation(testInstance, CustomHttpRequestTest.class);
          // 独自拡張クラスのコンストラクタに baseUri の情報を連携する
          return new CustomHttpRequestTestSupport(testInstance.getClass(), annotation.baseUri());
      }
  }

``findAnnotation(Object, Class)`` を使用すると、テストクラスに設定されたアノテーションの情報を取得できる。
これを利用することで、独自拡張クラスに ``baseUri`` の値を連携できる。

最後に、独自の合成アノテーションを使って次のように実装することで、 :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` を継承した独自拡張クラスを使用できるようになる。

.. code-block:: java

  // 独自の合成アノテーションをテストクラスに設定する(baseUri も設定する)
  @CustomHttpRequestTest(baseUri = "/custom/")
  class YourTest {
      // 独自拡張クラスをフィールドで宣言する
      CustomHttpRequestTestSupport support;
  
      @Test
      void test() {
          // 独自拡張クラスをテストで使用する
          support.customMethod();
      }
  }

事前処理・事後処理を実装する
=============================

独自拡張用のExtensionでは、以下のメソッドをオーバーライドすることによってテストの事前処理・事後処理を実装できる。

* beforeAll
* beforeEach
* afterAll
* afterEach

``beforeAll`` と ``afterAll`` では、テストクラス全体での事前・事後処理を実装できる。
そして、 ``beforeEach`` と ``afterEach`` では、テストメソッドごとの事前・事後処理を実装できる。

それぞれのメソッドをオーバーライドするときは、必ず以下のようにして親クラスの同メソッドを実行する必要がある。
そうしない場合、親クラスで定義された事前・事後処理が呼ばれなくなる。

.. code-block:: java

  @Override
  public void beforeAll(ExtensionContext context) {
      // 必ず最初に親のメソッドを実行する
      super.beforeAll(context);

      // 独自の事前処理を実装する
      ...
  }

JUnit 4のTestRuleを再現する
=============================

既存プロジェクトなどで作成した独自拡張クラスがあり、その中でJUnit 4の ``TestRule`` を使用している場合に、本拡張機能に移植する方法を説明する。

例えば、以下のような独自拡張クラスが存在したとする。

.. code-block:: java

  import org.junit.Rule;
  import org.junit.rules.Timeout;
  import java.util.concurrent.TimeUnit;
  
  public class CustomTestSupport extends TestSupport {
      // JUnit 4のTestRuleを使用している
      @Rule
      public Timeout timeout = new Timeout(1000, TimeUnit.MILLISECONDS);
  
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }
  }

これを本拡張機能に移植する場合は、独自拡張用のExtensionクラスを次のようにして実装する。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  
      // 1. resolveTestRules メソッドをオーバーライドする
      @Override
      protected List<TestRule> resolveTestRules() {
          // 2. 親クラスの resolveTestRules() の結果をベースにしてリストを生成する
          List<TestRule> rules = new ArrayList<>(super.resolveTestRules());
          // 3. 独自拡張クラスで定義しているTestRuleをリストに追加する
          rules.add(((CustomTestSupport) support).timeout);
          // 4. 生成したリストを返却する
          return rules;
      }
  }

独自拡張用のExtensionでは、 ``resolveTestRules()`` というメソッドをオーバーライドできる。
このメソッドで、再現させたいJUnit 4の ``TestRule`` をリストにして返却するように実装する。
これにより、JUnit 5のテスト上でもJUnit 4の ``TestRule`` を再現できるようになる。

なお、 ``resolveTestRules()`` をオーバーライドするときは、必ず親クラスの ``resolveTestRules()`` が返すリストをベースにすること。
そうしない場合、親クラスで登録している ``TestRule`` が再現されなくなる。


-------------------------------
RegisterExtensionで使用する
-------------------------------

JUnit 5では、Extensionのインスタンスを手続き的に生成してテストクラスに適用するためにRegisterExtensionという仕組みが用意されている。

.. tip::
  RegisterExtensionの説明については、 `公式ガイドの「5.2.2. Programmatic Extension Registration」(外部サイト、英語) <https://junit.org/junit5/docs/5.8.2/user-guide/#extensions-registration-programmatic>`_ を参照のこと。

本拡張機能が提供するExtensionは、RegisterExtensionを使って利用することもできる。
ただし、その場合は必ずstaticフィールドで使用すること。
インスタンスフィールドで使用した場合、 ``beforeAll`` や ``afterAll`` などの処理が実行されないため、Extensionが正常に動作しなくなる。

以下に、実装例を示す。

.. code-block:: java

  class YourTest {
      // 1. static フィールドで RegisterExtension を使用する
      @RegisterExtension
      static TestSupportExtension extension = new TestSupportExtension();
  
      // 2. 自動テストフレームワークが提供するクラスのインスタンスフィールドを宣言する
      TestSupport support;
  
      @Test
      void test() {
          // 3. support をテストで使用する
          ...
      }
  }

