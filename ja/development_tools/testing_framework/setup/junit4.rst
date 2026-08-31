.. _junit4_support:

JUnit 4で使用する
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
テスティングフレームワークは、JUnit 4でも使用できる。JUnit 4では、\ :java:extdoc:`TestSupport <nablarch.test.TestSupport>`\ などのサポートクラスをテストクラスが継承することで、その機能をテストクラスから使用する。

既にJUnit 4で書いたテスト資産があるプロジェクトは、この方法でテストを書き続けられる。新しくテストを書く場合は、\ :ref:`標準の使い方 <standard_usage>`\ に従ってJUnit 5で書く。

使用方法
--------------------------------------------------

依存関係
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
依存関係の追加は不要である。\ ``nablarch-testing``\ が\ ``junit:junit``\ の4.13.1を\ ``compile``\ スコープで依存関係に持つため、テスティングフレームワークを使用していればJUnit 4も推移的に解決される。

テストクラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用するサポートクラスを、テストクラスで継承する。\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ を使用する場合の実装例を示す。

.. code-block:: java

  import nablarch.test.core.db.DbAccessTestSupport;

  import org.junit.Test;

  public class UserComponentTest extends DbAccessTestSupport {

      @Test
      public void test() {
          // 継承したサポートクラスのメソッドをそのまま呼び出す
          setUpDb("test");
          // 中略
      }
  }

:ref:`テスティングフレームワークによるテスト実装 <testing_framework_implementation>`\ の実装例は、いずれもJUnit 5で書いている。JUnit 4で書く場合は、テストクラスに設定した合成アノテーションとフィールドの宣言を、対応するサポートクラスの継承に読み替える。また、\ ``support``\ を介した呼び出しは、継承したメソッドの直接の呼び出しに読み替える。合成アノテーションとサポートクラスの対応は、\ :ref:`標準の使い方 <standard_usage>`\ の一覧表を参照。

.. _junit4_support-common_process:

テストの実行前後に共通処理を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスト実行前後の共通処理は、\ JUnit\ のアノテーション（\ ``@Before``\ ・\ ``@After``\ ・\ ``@BeforeClass``\ ・\ ``@AfterClass``\ ）で実装する。

.. important::

  ``@BeforeClass``\ ・\ ``@AfterClass``\ を使用する場合、サブクラスにスーパクラスと同名で同じアノテーションを付けたメソッドを作成しない。同名のメソッドに同種のアノテーションを付けると、スーパクラスのメソッドが起動されなくなる。次の例で\ ``TestSub``\ を実行すると、\ ``TestSuper#setUpBeforeClass``\ は呼び出されない。

  .. code-block:: java

    public class TestSuper {
        @BeforeClass
        public static void setUpBeforeClass() {
            System.out.println("super");   // 呼び出されない
        }
    }

    public class TestSub extends TestSuper {
        @BeforeClass
        public static void setUpBeforeClass() {
            // スーパクラスのメソッドを上書きしている
        }
    }

.. _junit4_support-no_inheritance:

テスティングフレームワークのクラスを継承せずに使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JUnit 4ではテストクラスが1つのクラスしか継承できない。別のクラスを継承しなければならないなどの理由でサポートクラスを継承できない場合は、サポートクラスをインスタンス化して処理を委譲する。コンストラクタにはテストクラス自身の\ ``Class``\ オブジェクトを渡す。この場合はトランザクションの開始・終了が自動では行われないため、前処理・後処理から明示的に呼び出す。

.. code-block:: java

  public class SampleTest extends AnotherSuperClass {

      private DbAccessTestSupport dbSupport = new DbAccessTestSupport(getClass());

      @Before
      public void setUp() {
          dbSupport.beginTransactions();   // トランザクションを開始する
      }

      @After
      public void tearDown() {
          dbSupport.endTransactions();     // トランザクションを終了する
      }

      @Test
      public void test() {
          dbSupport.setUpDb("test");
          // 中略（テスト対象メソッドを起動し、戻り値をactualに受け取る）
          dbSupport.assertSqlResultSetEquals("従業員検索", "test", "expected", actual);
      }
  }

.. _junit4_support-vintage:

JUnit 4で書いたテストをJUnit 5上で実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JUnit 5へ移行する場合も、JUnit 4で書いた既存のテストを修正する必要はない。JUnit 5にはJUnit Vintageというプロジェクトがあり、これを使うとJUnit 4で書いたテストをJUnit 5上で実行できる。既存のテストはJUnit 4のまま残し、新しく書くテストだけをJUnit 5で書ける。

JUnit VintageはJUnit 5が提供するプロジェクトであり、テスティングフレームワークの一部ではない。次の2つのアーティファクトを依存関係に追加すると有効になる。バージョンを揃えるため、\ ``org.junit:junit-bom``\ を\ ``dependencyManagement``\ に読み込む。

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
        <version>5.11.0</version>
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
