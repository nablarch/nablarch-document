.. _legacy_junit4_tips:

==========================================
目的別API使用方法（JUnit 4）
==========================================

.. important::

  本ページはJUnit 4で作成された既存のテスト資産を保守するプロジェクト向けである。
  新規にテストを作成する場合は、JUnit 5版の :doc:`../03_Tips` を参照すること。

.. _legacy_junit4_using_junit_annotation:

------------------------------------
テスト実行前後に共通処理を行いたい。
------------------------------------

JUnit4で用意されたアノテーション(@Before, @After, @BeforeClass, @AfterClass)を使用することで、
テスト実行前後に共通処理を実行させることができる。

注意事項
========

上記のアノテーションを使用する際は、以下の点に注意すること。

@BeforeClass, @AfterClass使用時の注意点
---------------------------------------

 * サブクラスにて、スーパークラスと同名の名前、同じアノテーションを付与のメソッドを作成しないこと。
   同名のメソッドに同種のアノテーションを付与した場合、スーパークラスのメソッドは起動されなくなる。

 .. code-block:: java

    public class TestSuper {
        @BeforeClass
        public static void setUpBeforeClass() {
            System.out.println("super");   // 表示されない。
        }
    }

    public class TestSub extends TestSuper {

        @BeforeClass
        public static void setUpBeforeClass() {
            // スーパークラスのメソッドを上書き
        }

        @Test
        public void test() {
            System.out.println("test");
        }
    }


上記のTestSubを実行した場合、「test」と表示される。

.. _legacy_junit4_using_other_class:

--------------------------------------------------------
本フレームワークのクラスを継承せずに使用したい
--------------------------------------------------------

通常、JUnit 4でのテストクラス作成時は本フレームワークで用意されているスーパークラスを継承すればよいが、
別のクラスを継承しなければならない等の理由で、本フレームワークのスーパークラスを継承できない場合がある。この場合、本フレームワークのスーパークラスをインスタンス化し、処理を委譲することで代替可能である。

委譲を使用する場合、コンストラクタにテストクラス自身のClassインスタンスを渡す必要がある。
また、前処理(@Before)メソッド、後処理(@After)メソッドについては、明示的に呼び出す必要がある。

テストソースコード実装例
========================

 .. code-block:: java

    public class SampleTest extends AnotherSuperClass {

        /** DbAccessテストサポート */
        private DbAccessTestSupport dbSupport
              = new DbAccessTestSupport(getClass());

        /** 前処理 */
        @Before
        public void setUp() {
            // DbSupportの前処理を起動
            dbSupport.beginTransactions();
        }

        /** 後処理 */
        @After
        public void tearDown() {
            // DbSupportの後処理を起動
            dbSupport.endTransactions();
        }

        @Test
        public void test() {
            // データベースに準備データ投入
            dbSupport.setUpDb("test");

            // ＜中略＞
            dbSupport.assertSqlResultSetEquals("test", "id", actual);
        }
    }

上記以外の目的別API使用方法は、JUnit 5版の :doc:`../03_Tips` と共通である。
JUnit 5版のコード例における ``support.`` を介したメソッド呼び出しを、継承したメソッドの直接呼び出しに読み替えること。
