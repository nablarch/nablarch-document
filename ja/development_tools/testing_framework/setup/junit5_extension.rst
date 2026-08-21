.. _junit5_extension:

JUnit 5用拡張機能
==================================================

.. contents:: 目次
  :depth: 3
  :local:

JUnit 5用拡張機能を使うと、JUnit 5で書いたテストからテスティングフレームワークの機能を使用できる。パラメータ化テストなど、JUnit 5が提供する機能と組み合わせてテストを書けるようになる。

JUnit 5そのものの導入方法やテストの書き方は、このページでは説明しない。\ `公式のユーザガイド(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/>`_\ を参照。

機能概要
--------------------------------------------------
テスティングフレームワークは、\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ などのテストに必要な機能を実装したクラスを提供している。JUnit 4では、これらのクラスをテストクラスが継承することで、その機能をテストクラスから使用していた。

本拡張機能は、これらのクラスのインスタンスを拡張機能側で生成し、テストクラスのフィールドにインジェクションする。この仕組みには、JUnit 5の\ `Extension(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/#extensions>`_\ を使用している。テストクラスは継承の必要がなくなるため、パラメータ化テストなどJUnit 5の機能をそのまま使える。

インジェクションは、テスティングフレームワークが提供するクラスごとに用意したExtensionクラスが行う。テストクラスには、Extensionクラスを適用するための合成アノテーションを設定する。

.. tip::

  合成アノテーションはJUnit 5が提供する機能で、複数のアノテーションの設定を別の1つのアノテーションにまとめられる。詳しくは\ `公式のユーザガイドの「2.1.1. Meta-Annotations and Composed Annotations」(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/#writing-tests-meta-annotations>`_\ を参照。

Extensionクラスと合成アノテーションの一覧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本拡張機能は、次のExtensionクラスと合成アノテーションを提供している。

.. list-table::
  :header-rows: 1
  :widths: 34,33,33

  * - テスティングフレームワークが提供するクラス
    - Extensionクラス
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

前提事項
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JUnit 5を使用するには、\ ``maven-surefire-plugin``\ が2.22.0以上である必要がある。

使用方法
--------------------------------------------------

依存関係を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本拡張機能は\ ``nablarch-testing-junit5``\ が提供する。テストでのみ使用するため、\ ``test``\ スコープで依存関係に追加する。

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-junit5</artifactId>
    <scope>test</scope>
  </dependency>

.. tip::

  ``nablarch-testing-junit5``\ は\ ``nablarch-testing``\ に依存する。これを追加することで、\ :ref:`テスティングフレームワーク <testing_framework_about>`\ が提供するAPIも使用できる。

  ただし、\ :java:extdoc:`RestTestExtension <nablarch.test.junit5.extension.http.RestTestExtension>`\ と\ :java:extdoc:`SimpleRestTestExtension <nablarch.test.junit5.extension.http.SimpleRestTestExtension>`\ が必要とする\ ``nablarch-testing-rest``\ は\ ``optional``\ 指定のため推移的に解決されない。これらを使用する場合は、\ :ref:`リクエスト単体テストの設定（RESTfulウェブサービス） <request_unit_test_setting_rest>`\ を参照して依存関係を別途追加する。

.. _junit5_extension-inject:

テストクラスに合成アノテーションを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用するクラスに対応する合成アノテーションをテストクラスに設定し、そのクラス型のインスタンスフィールドを宣言する。\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ を使用する場合の実装例を示す。

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

合成アノテーション\ :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`\ をテストクラスに設定すると、\ :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`\ がテストクラスに適用される。Extensionクラスは、テストの実行前に\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ のインスタンスを生成し、テストクラスのフィールドにインジェクションする。

インジェクションの対象になるのは、生成したインスタンスを代入できる型で宣言されたフィールドすべてである。フィールドの可視性は何でもよく、スーパクラスで宣言されたフィールドも対象になる。該当するフィールドが複数ある場合は、そのすべてに同じインスタンスが代入される。1つもない場合は、何もインジェクションされない。

.. important::

  インジェクションの対象になるフィールドに、あらかじめ値を設定しておいてはならない。値が設定されている場合、Extensionクラスは\ ``IllegalStateException``\ を送出し、そのテストは失敗する。\ ``Object``\ 型のフィールドも代入できる型に該当するため、初期値を設定した\ ``Object``\ 型のフィールドを宣言していると、意図せずこの例外が発生する。

テストデータのシート名とIDの対応は、\ :ref:`テストクラスとテストデータの対応 <testdata_notation-file_structure>`\ を参照。

BasicHttpRequestTestTemplateを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`\ を使用する場合だけは、合成アノテーション\ :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`\ に\ ``baseUri``\ を指定する。\ ``baseUri``\ の指定以外の手順は、\ :ref:`テストクラスに合成アノテーションを設定する <junit5_extension-inject>`\ と同じである。

.. code-block:: java

  // 1. BasicHttpRequestTest の baseUri を指定する
  @BasicHttpRequestTest(baseUri = "/test/")
  class YourTest {
      // 2. BasicHttpRequestTestTemplate のインジェクション方法は、他と変わらない
      BasicHttpRequestTestTemplate support;

      @Test
      void test() {
          support.execute();
      }
  }

指定した値は、\ :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`\ の\ ``getBaseUri()``\ メソッドが返す値になる。

RegisterExtensionでExtensionクラスを適用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本拡張機能が提供するExtensionクラスは、合成アノテーションを使わず、JUnit 5の\ ``RegisterExtension``\ で適用することもできる。ただし\ :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>`\ は、\ ``baseUri``\ を合成アノテーション\ :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`\ から読み取るため、この方法では適用できない。

.. code-block:: java

  class YourTest {
      // 1. static フィールドで RegisterExtension を使用する
      @RegisterExtension
      static TestSupportExtension extension = new TestSupportExtension();

      // 2. テスティングフレームワークが提供するクラスのインスタンスフィールドを宣言する
      TestSupport support;

      @Test
      void test() {
          // 3. support をテストで使用する
          ...
      }
  }

.. important::

  ``RegisterExtension``\ を使う場合は、必ず\ ``static``\ フィールドで宣言する。インスタンスフィールドで宣言すると\ ``beforeAll``\ や\ ``afterAll``\ などの処理が実行されず、Extensionクラスが正しく動作しない。

.. tip::

  ``RegisterExtension``\ については、\ `公式のユーザガイドの「5.2.2. Programmatic Extension Registration」(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/#extensions-registration-programmatic>`_\ を参照。

.. _junit5_extension-vintage:

JUnit 4で書いたテストをJUnit 5上で実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本拡張機能を導入しても、JUnit 4で書いた既存のテストを修正する必要はない。JUnit 5にはJUnit Vintageというプロジェクトがあり、これを使うとJUnit 4で書いたテストをJUnit 5上で実行できる。既存のテストはJUnit 4のまま残し、新しく書くテストだけをJUnit 5で書ける。

JUnit VintageはJUnit 5が提供するプロジェクトであり、本拡張機能の一部ではない。次の2つのアーティファクトを依存関係に追加すると有効になる。バージョンを揃えるため、\ ``org.junit:junit-bom``\ を\ ``dependencyManagement``\ に読み込む。

* ``org.junit.jupiter:junit-jupiter``
* ``org.junit.vintage:junit-vintage-engine``

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      ...

      <!-- バージョンを揃えるため、JUnitが提供しているbomを読み込む -->
      <dependency>
        <groupId>org.junit</groupId>
        <artifactId>junit-bom</artifactId>
        <version>5.8.2</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    ...

    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.vintage</groupId>
      <artifactId>junit-vintage-engine</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

.. important::

  JUnit Vintageは、JUnit 4のテストをJUnit 4として実行しているにすぎない。JUnit 4で書いたテストの中でJUnit 5の機能が使えるようになるわけではない。JUnit 4からJUnit 5へ段階的に移行するための補助として使う。移行の手順は\ `公式の移行ガイド(外部サイト、英語) <https://junit.org/junit5/docs/5.11.0/user-guide/#migrating-from-junit4>`_\ を参照。

拡張例
--------------------------------------------------
テスティングフレームワークが提供するクラスを継承して独自の拡張を加える場合は、次の3つを行う。JUnit 4で書いた既存の独自拡張クラスを本拡張機能で使う場合も同じである。

#. テスティングフレームワークが提供するクラスを継承し、独自拡張クラスを作成する
#. 継承元のクラスに対応するExtensionクラスを継承し、独自拡張クラスのインスタンスを生成するExtensionクラスを作成する
#. ``ExtendWith``\ アノテーションで、作成したExtensionクラスをテストクラスに適用する

このほか、\ ``baseUri``\ を渡す合成アノテーションの作成、事前処理・事後処理の実装、JUnit 4の\ ``TestRule``\ の再現についても、独自拡張用のExtensionクラスで対応できる。

独自拡張クラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークが提供するクラスを継承する。\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ を拡張する場合の実装例を示す。

.. code-block:: java

  public class CustomTestSupport extends TestSupport {
      // テストクラスの Class オブジェクトを TestSupport のコンストラクタに渡せるように実装する
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }

      // 独自の拡張メソッドを実装する
  }

テスティングフレームワークが提供するクラスは、基本的にインスタンスの生成時にテストクラスの\ ``Class``\ オブジェクトを受け取る。したがって、独自拡張クラスにも\ ``Class``\ オブジェクトを受け取るコンストラクタを定義する。

.. tip::

  :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`\ は、テストクラスの\ ``Class``\ オブジェクトをコンストラクタで渡さなくても使用できる。

独自拡張用のExtensionクラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
継承元のクラスに対応するExtensionクラスを継承する。前項の例では\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ を継承しているので、対応するExtensionクラスは\ :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`\ である。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {

      // createSupport() をオーバーライドし、独自拡張クラスのインスタンスを返すように実装する
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  }

``createSupport()``\ メソッドをオーバーライドし、独自拡張クラスのインスタンスを返すように実装する。このメソッドが返したインスタンスは、すべてのExtensionクラスのスーパクラスである\ :java:extdoc:`TestEventDispatcherExtension <nablarch.test.junit5.extension.event.TestEventDispatcherExtension>`\ に定義された\ ``support``\ という\ :java:extdoc:`TestEventDispatcher <nablarch.test.event.TestEventDispatcher>`\ 型のインスタンスフィールドに保存される。このフィールドは\ ``protected``\ なので、サブクラスから参照できる。

.. tip::

  :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`\ を直接継承した独自拡張クラスでは、対応するExtensionクラスとして\ :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>`\ を使用できる。

ExtendWithでテストクラスに適用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
作成した独自拡張用のExtensionクラスは、\ ``ExtendWith``\ アノテーションでテストクラスに適用する。

.. code-block:: java

  ...
  import org.junit.jupiter.api.extension.ExtendWith;

  // 1. ExtendWith で独自拡張用のExtensionクラスをテストクラスに適用する
  @ExtendWith(CustomTestSupportExtension.class)
  class YourTest {
      // 2. 独自拡張クラスをインスタンスフィールドで宣言する
      CustomTestSupport support;

      @Test
      void test() {
          // 3. テスト内で独自拡張クラスを使用する
          support.customMethod();
      }
  }

baseUriを渡す合成アノテーションを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`\ または\ :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`\ を拡張する場合は、\ ``baseUri``\ を独自拡張クラスのインスタンスに渡す必要がある。\ ``ExtendWith``\ ではパラメータを渡せないため、合成アノテーションも独自に作成する。

まず、コンストラクタでテストクラスと\ ``baseUri``\ を受け取る独自拡張クラスを作成する。

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

次に、\ ``baseUri``\ を渡せる合成アノテーションを作成する。

.. code-block:: java

  import org.junit.jupiter.api.extension.ExtendWith;

  import java.lang.annotation.ElementType;
  import java.lang.annotation.Retention;
  import java.lang.annotation.RetentionPolicy;
  import java.lang.annotation.Target;

  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.TYPE)
  // この後作成する独自拡張用のExtensionクラスを指定する
  @ExtendWith(CustomHttpRequestTestExtension.class)
  public @interface CustomHttpRequestTest {
      // baseUri を渡せるように宣言する
      String baseUri();
  }

続いて、\ ``ExtendWith``\ に指定する独自拡張用のExtensionクラスを作成する。

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

``findAnnotation(Object, Class)``\ を使うと、テストクラスに設定されたアノテーションの情報を取得できる。これを使用して、独自拡張クラスに\ ``baseUri``\ の値を渡す。取得できるのはテストクラスに直接設定されたアノテーションだけで、スーパクラスに設定されたアノテーションや、他のアノテーションを介して間接的に設定されたアノテーションは取得できない。

最後に、作成した合成アノテーションをテストクラスに設定する。

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
独自拡張用のExtensionクラスでは、\ ``beforeAll``\ ・\ ``afterAll``\ ・\ ``beforeEach``\ ・\ ``afterEach``\ の4つのメソッドをオーバーライドして、テストの事前処理・事後処理を実装できる。\ ``beforeAll``\ と\ ``afterAll``\ はテストクラス全体に対して、\ ``beforeEach``\ と\ ``afterEach``\ はテストメソッドごとに実行される。

.. code-block:: java

  @Override
  public void beforeAll(ExtensionContext context) {
      // 必ず最初にスーパクラスのメソッドを実行する
      super.beforeAll(context);

      // 独自の事前処理を実装する
      ...
  }

.. important::

  オーバーライドするときは、必ずスーパクラスの同じメソッドを実行する。実行しないと、スーパクラスで定義された事前処理・事後処理が呼ばれなくなる。

.. TODO(NTF-MOD-03-1): resolveTestRules() に登録したTimeoutがテスト本体に効かない。
   不具合と判定済みで、nablarch-testing-junit5 側で修正予定・未着手。
   依頼書 .rn/20260724-ntf-yaml-support/ntf-mod-03-nablarch-testing-junit5.md §2。
   修正後に本文へ反映する。

JUnit 4のTestRuleを再現する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
独自拡張クラスの中でJUnit 4の\ ``org.junit.rules.TestRule``\ を使用している場合は、本拡張機能でもそれを再現できる。例えば、次のような独自拡張クラスがあるとする。

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

この場合、独自拡張用のExtensionクラスで\ ``resolveTestRules()``\ メソッドをオーバーライドし、再現したい\ ``TestRule``\ のリストを返すように実装する。

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {

      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }

      // 1. resolveTestRules メソッドをオーバーライドする
      @Override
      protected List<TestRule> resolveTestRules() {
          // 2. スーパクラスの resolveTestRules() の結果をベースにしてリストを生成する
          List<TestRule> rules = new ArrayList<>(super.resolveTestRules());
          // 3. 独自拡張クラスで定義しているTestRuleをリストに追加する
          rules.add(((CustomTestSupport) support).timeout);
          // 4. 生成したリストを返す
          return rules;
      }
  }

.. important::

  ``resolveTestRules()``\ をオーバーライドするときは、必ずスーパクラスの\ ``resolveTestRules()``\ が返すリストをベースにする。ベースにしないと、スーパクラスで登録している\ ``TestRule``\ が再現されなくなる。
