.. _entityUnitTest:

=============================
Form/Entityのクラス単体テスト
=============================
本項では、FormおよびFormの一種であるEntityのクラス単体テスト(以下Form単体テストまたはEntity単体テスト)について説明する。
両者はほぼ同じように単体テストを行えるため、共通する内容についてはEntity単体テストをベースに説明し、特有の処理については個別に説明する。

.. tip::
   Entityとは、テーブルのカラムと1対1に対応するプロパティを持つFormのことである。

-----------------------------
Form/Entity単体テストの書き方
-----------------------------
本項で例として使用したテストクラスとテストデータは以下のとおり(右クリック->保存でダウンロード)。

* :download:`テストクラス(SystemAccountEntityTest.java)<./_download/SystemAccountEntityTest.java>`
* :download:`テストデータ(SystemAccountEntityTest.xlsx)<./_download/SystemAccountEntityTest.xlsx>`
* :download:`テスト対象クラス(SystemAccountEntity.java)<./_download/SystemAccountEntity.java>`  

テストデータの作成
==================
テストデータを記載したExcelファイルそのものの作成方法を説明する。テストデータを記載したExcelファイルは、テストソースコードと同じディレクトリに同じ名前で格納する(拡張子のみ異なる)。\
なお、後述する\
\ :ref:`精査のテストケース<entityUnitTest_ValidationCase>`\ 、\
\ :ref:`コンストラクタのテストケース<entityUnitTest_ConstructorCase>`\ 、\
\ :ref:`setter、getterに対するテストケース<entityUnitTest_SetterGetterCase>`\ 
のそれぞれが、1シートずつ使用する前提である。

テストデータの記述方法詳細については、\ :doc:`../../06_TestFWGuide/01_Abstract`\ 、\ :doc:`../../06_TestFWGuide/02_DbAccessTest`\ を参照。

なお、メッセージデータやコードマスタなどの、データベースに格納する静的マスタデータは、プロジェクトで管理されたデータがあらかじめ投入されている\
(これらのデータを個別のテストデータとして作成しない)前提である。

テストクラスの作成
==================
Form/Entity単体テストのテストクラスは、以下の条件を満たすように作成する。

* テストクラスのパッケージは、テスト対象のForm/Entityと同じとする。
* <Form/Entityクラス名>Testというクラス名でテストクラスを作成する。
* nablarch.test.core.db.EntityTestSupportを継承する。

.. code-block:: java

   package nablarch.sample.management.user; // 【説明】パッケージはSystemAccountEntityと同じ

   import java.util.HashMap;
   import java.util.Map;

   import org.junit.Test;

   import nablarch.test.core.db.EntityTestSupport;

   import static org.junit.Assert.assertArrayEquals;
   import static org.junit.Assert.assertEquals;

   /**
    * SystemAccountEntityクラスに対するテストを実行するクラス。<br/>
    * テスト内容はエクセルシート参照のこと。
    *
    * @author Miki Habu
    * @since 1.0
    */
   public class SystemAccountEntityTest extends EntityTestSupport {
   // 【説明】クラス名はSystemAccountEntityTestで、EntityTestSupportを継承する
   

   // ～後略～


テストメソッドの記述方法は本項以降に記載されているコード例を参照。

.. _entityUnitTest_ValidationCase:

文字種と文字列長の単項目精査テストケース
========================================

単項目精査に関するテストケースは、入力される文字種および文字列長に関するものがほとんどである。\
例えば、以下のようなプロパティがあるとする。

* プロパティ名「フリガナ」
* 最大文字列長は50文字
* 必須項目
* 全角カタカナのみを許容する

この場合、以下のようなテストケースを作成することになる。

 =============================================== =========================
 ケース                                           観点			 
 =============================================== =========================
 全角カタカナ50文字を入力し精査が成功する。        最大文字列長、文字種の確認	 
 全角カタカナ51文字を入力し精査が失敗する。        最大文字列長の確認		 
 全角カタカナ1文字を入力し精査が成功する。         最小文字列長、文字種の確認	 
 空文字を入力し、精査が失敗する。                  必須精査の確認		 
 半角カタカナを入力し精査が失敗する。              文字種の確認\ [#]_\		 
 =============================================== =========================

\ 
 
 .. [#] 同様に、半角英字、全角ひらがな、漢字...等が入力され精査が失敗するケースが必要である。

このように、単項目精査のテストケースは、ケース数が多くなりデータ作成の労力がかかる。\
そこで、単項目精査テスト専用のテスト方法を提供する。これにより以下の効果が見込まれる。

* 単項目精査のテストケース作成を容易になる。
* 保守性の高いテストデータが作成でき、レビューやメンテナンスが容易になる。


.. tip::
   本テスト方法は、プロパティとして別のFormを保持するFormに対しては使用できない。その場合、独自に精査処理のテストを実装すること。
   プロパティとして別のFormを保持するFormとは、以下の形式でプロパティにアクセスする親Formのこと。
   
   .. code-block:: none
   
      <親Form>.<子Form>.<子フォームのプロパティ名>


テストケース表の作成方法
------------------------

以下のカラムを用意する。

+-----------------------------+--------------------------------------------------+
| カラム名                    | 記載内容                                         |
+=============================+==================================================+
|propertyName                 |テスト対象のプロパティ名                          |
+-----------------------------+--------------------------------------------------+
|allowEmpty                   |そのプロパティが未入力を許容するか                |
+-----------------------------+--------------------------------------------------+
|         min                 |そのプロパティが入力値として許容する最小文字列長（|
|                             |省略可）                                          |
+-----------------------------+--------------------------------------------------+
|         max                 |そのプロパティが入力値として許容する最大文字列長  |
+-----------------------------+--------------------------------------------------+
|messageIdWhenNotApplicable   |文字種不適合時に期待するメッセージID              |
+-----------------------------+--------------------------------------------------+
|半角英字                     |半角英字を許容するか                              |
+-----------------------------+--------------------------------------------------+
|半角数字                     |半角数字を許容するか                              |
+-----------------------------+--------------------------------------------------+
|半角記号                     |半角記号を許容するか                              |
+-----------------------------+--------------------------------------------------+
|半角カナ                     |半角カナを許容するか                              |
+-----------------------------+--------------------------------------------------+
|全角英字                     |全角英字を許容するか                              |
+-----------------------------+--------------------------------------------------+
|全角数字                     |全角数字を許容するか                              |
+-----------------------------+--------------------------------------------------+
|全角ひらがな                 |全角ひらがなを許容するか                          |
+-----------------------------+--------------------------------------------------+
|全角カタカナ                 |全角カタカナを許容するか                          |
+-----------------------------+--------------------------------------------------+
|全角漢字                     |全角漢字を許容するか                              |
+-----------------------------+--------------------------------------------------+
|全角記号その他               |全角記号その他を許容するか                        |
+-----------------------------+--------------------------------------------------+
|外字                         |外字を許容するか                                  |
+-----------------------------+--------------------------------------------------+

許容するかどうかを記入するカラムには、以下の値を設定する。

 ========== ======= ========================
 設定内容    設定値    備考
 ========== ======= ========================
 許容する     o      半角英小文字のオー
 許容しない   x      半角英小文字のエックス
 ========== ======= ========================

具体例を以下に示す。

.. image:: ./_image/entityUnitTest_CharsetAndLengthExample.png



テストメソッドの作成方法
------------------------

 
スーパクラスの以下のメソッドを起動する。

.. code-block:: java

   void testValidateCharsetAndLength(Class entityClass, String sheetName, String id)


\ 

.. code-block:: java

   // 【説明】～前略～

  public class SystemAccountEntityTest extends EntityTestSupport {
    
       /** テスト対象エンティティクラス */
       private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;


       /**
        * 文字種および文字列長のテストケース
        */
       @Test
       public void testCharsetAndLength() {
            // 【説明】テストデータを記載したシート名
            String sheetName = "testCharsetAndLength";        

            // 【説明】テストデータのID
            String id = "charsetAndLength";

            // 【説明】テスト実行
            testValidateCharsetAndLength(ENTITY_CLASS, sheetName, id);
       }


       // 【説明】～後略～



このメソッドを実行すると、テストデータの各行毎に以下の観点でテストが実行される。

+---------------+-----------------------------+---------------------------------------------------+
| 観点          |入力値                       | 備考                                              |
+===============+=============================+===================================================+
| 文字種        |半角英字                     | max(最大文字列長)欄に記載した長さの文字列で構成さ |
+---------------+-----------------------------+ れる。                                            |
| 文字種        |半角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |半角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |半角記号                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |半角カナ                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角英字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角数字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角ひらがな                 |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角カタカナ                 |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角漢字                     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |全角記号その他               |                                                   |
+---------------+-----------------------------+                                                   |
| 文字種        |外字                         |                                                   |
+---------------+-----------------------------+---------------------------------------------------+
| 未入力        |空文字                       |長さ0の文字列                                      |
+---------------+-----------------------------+---------------------------------------------------+
| 最小文字列    |最小文字列長の文字列         |入力値は、o印を付けた文字種で構成される            |
+---------------+-----------------------------+                                                   |
| 最長文字列    |最長文字列長の文字列         |                                                   |
+---------------+-----------------------------+                                                   |
| 文字列長不足  |最小文字列長－１の文字列     |                                                   |
+---------------+-----------------------------+                                                   |
| 文字列長超過  |最大文字列長＋１の文字列     |                                                   |
+---------------+-----------------------------+---------------------------------------------------+



その他の単項目精査のテストケース
================================

前述の、文字種と文字列長の単項目精査テストケースを使用すれば\
大部分の単項目精査がテストできるが、一部の精査についてはカバーできないものもある。
例えば、数値入力項目の範囲精査が挙げられる。


このような単項目精査のテストについても、簡易にテストできる仕組みを用意している。
各プロパティについて、１つの入力値と期待するメッセージIDのペアを記述することで、
任意の値で単項目精査のテストができる。


.. tip::
   本テスト方法は、プロパティとして別のFormを保持するFormに対しては使用できない。その場合は、独自に精査処理のテストを実装すること。
   プロパティとして別のFormを保持するFormとは、以下の形式でプロパティにアクセスする親Formのこと。
   
   .. code-block:: none
   
      <親Form>.<子Form>.<子フォームのプロパティ名>


テストケース表の作成方法
------------------------

以下のカラムを用意する。

+-----------------------------+--------------------------------------------------+
| カラム名                    | 記載内容                                         |
+=============================+==================================================+
|propertyName                 |テスト対象のプロパティ名                          |
+-----------------------------+--------------------------------------------------+
|case                         |テストケースの簡単な説明                          |
+-----------------------------+--------------------------------------------------+
|input1\ [#]_                 |入力値 [#]_                                       |
+-----------------------------+--------------------------------------------------+
|messageId                    |上記入力値で単項目精査した場合に、発生すると期待す|
|                             |るメッセージID（精査エラーにならないことを期待する|
|                             |場合は空欄）                                      |
+-----------------------------+--------------------------------------------------+


.. [#] ひとつのキーに対して複数のパラメータを指定する場合は、input2, input3 というようにカラムを増やす。

\

.. [#] \ :ref:`special_notation_in_cell`\ の記法を使用することで、効率的に入力値を作成できる。

具体例を以下に示す。

.. image:: ./_image/entityUnitTest_singleValidationDataExample.png


テストメソッドの作成方法
------------------------

 
スーパクラスの以下のメソッドを起動する。

.. code-block:: java

   void testSingleValidation(Class entityClass, String sheetName, String id)




.. code-block:: java

 // 【説明】～前略～

 public class SystemAccountEntityTest extends EntityTestSupport {
    
      /** テスト対象エンティティクラス */
      private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

      /**
       * 文字種および文字列長の単項目精査テストケース
       */
      // 【説明】～中略～

      /**							  
       * 単項目精査のテストケース（上記以外）		  
       */							  
      @Test						  
      public void testSingleValidation() {		  
          String sheetName = "testSingleValidation";	  
          String id = "singleValidation";			  
          testSingleValidation(ENTITY_CLASS, sheetName, id);
      }                                                     


       // 【説明】～後略～


バリデーションメソッドのテストケース
====================================

上記までの単項目精査のテストでは、エンティティのセッターメソッドに付与されたアノテーションが\
正しいかテストされ、エンティティに実装したバリデーションメソッド\ [#]_\ は実行されていない。

その為、独自のバリデーションメソッドをエンティティに実装した場合は、
別途テストを作成する必要がある。



.. [#] ``@ValidateFor``\ アノテーションを付与したstaticメソッドのこと


テストケース表の作成
--------------------

* IDは"testShots"固定とする。
* 以下のカラムを用意する。

 +---------------------------+-----------------------------------------------+
 | カラム名                  | 記載内容                                      |
 +===========================+===============================================+
 | title                     | テストケースのタイトル                        |
 +---------------------------+-----------------------------------------------+
 | description               | テストケースの簡単な説明                      |
 +---------------------------+-----------------------------------------------+
 |  expectedMessageId\ *ｎ*  | 期待するメッセージ（\ *ｎ*\ は1からの連番 ）  |
 +---------------------------+-----------------------------------------------+
 | propertyName\ *ｎ*        | 期待するプロパティ（\ *ｎ*\ は1からの連番 ）  |
 +---------------------------+-----------------------------------------------+

 複数のメッセージを期待する場合、expectedMessageId2, propertyName2というように数値を増やして右側に追加していく。

* 入力パラメータ表の作成

  * IDは"params"固定とする。
  * 上記のテストケース表に対応する、入力パラメータ\ [#]_ \を1行ずつ記載する。

\

    .. [#] \ :ref:`special_notation_in_cell`\ の記法を使用することで、効率的に入力値を作成できる。

\

    具体例を以下に示す。

    .. image:: ./_image/entityUnitTest_validationTestData.png
      :scale: 70

    ※Entityの保有するプロパティ名のExcelへの記述手順は、 :ref:`property-name-copy-label` を参照。



テストケース、テストデータの作成
--------------------------------


.. _entityUnitTest_ValidationMethodSpecifyNormal:


精査対象確認
~~~~~~~~~~~~

精査対象のプロパティを指定(\ :ref:`nablarch_validation`\ 参照)した場合、\
その指定が正しいかどうか確認するケースを作成する。


全てのプロパティに対して、おのおの単項目精査でエラーとなるデータを用意する。\
精査対象プロパティの指定が正しければ、精査対象のプロパティだけが単項目精査になるはずである。\
よって、期待値として、全精査対象プロパティ名と、各プロパティ単項目精査エラー時のメッセージIDを記載する。\


.. tip::
 精査対象プロパティが誤って精査対象から漏れていた場合、\
 期待したメッセージが出力されない為、メッセージIDのアサートが失敗する。\
 また、精査対象でないプロパティが誤って精査対象となっていた場合は、\
 入力値が不正により単項目精査が失敗し、予期しないメッセージが出力される。\
 これにより、精査対象の誤りを検知することができる。


テストケース表には、全精査対象プロパティのプロパティ名と、\
そのプロパティ単項目精査エラーメッセージIDを記載する。

.. image:: ./_image/entityUnitTest_ValidationPropTestCases.png
 :scale: 70


入力パラメータ表には、全てのプロパティに対してそれぞれ単項目精査エラーとなる値を記載する。


.. image:: ./_image/entityUnitTest_ValidationPropParams.png
 :scale: 68


.. tip::

   Form単体テストのテストケースやテストデータを作成する際、\
   **プロパティに保持している別のFormのプロパティ** を指定したいことがある。\
   この場合、次のように指定できる。
   
   * Formのコード例
   
   .. code-block:: java
   
     public class SampleForm {

         /** システムユーザ */
         private SystemUserEntity systemUser;

         /** 電話番号配列 */
         private UserTelEntity[] userTelArray;
     
         // 【説明】プロパティ以外は省略
     
     }

   * 保持しているFormのプロパティを指定する方法(SystemUserEntity.userIdを指定する場合)
   
   .. code-block:: none
   
      sampleForm.systemUser.userId

   * Form配列の要素のプロパティを指定する方法(UserTelEntity配列の先頭要素のプロパティを指定する場合)
   
   .. code-block:: none
   
      sampleForm.userTelArray[0].telNoArea



項目間精査など
~~~~~~~~~~~~~~

項目間精査など、バリデーションメソッドの\ :ref:`entityUnitTest_ValidationMethodSpecifyNormal`\ 
で行った精査対象指定以外の動作確認を行うケースを作成する。

下図では、"newPasswordとconfirmPasswordが等しいこと"というバリデーションメソッドに対する正常系のケースを作成している。

.. image:: ./_image/entityUnitTest_RelationalValidation.png
 :scale: 100


テストメソッドの作成方法
------------------------

これまでに作成したテストケース、データを使用するテストメソッドを以下に示す。\
下記コードの変数内容を変更するだけで、異なるEntityの精査のテストに対応できる。

.. code-block:: java

    // ～前略～

    /** テスト対象エンティティクラス */
    private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

    // ～中略～
    /**
     * {@link SystemAccountEntity#validateForRegisterUser(nablarch.core.validation.ValidationContext)} のテスト。
     */
    @Test
    public void testValidateForRegisterUser() {
        // 精査実行
        String sheetName = "testValidateForRegisterUser";
        String validateFor = "registerUser";
        testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
    }

   // ～後略～



.. _entityUnitTest_ConstructorCase:

コンストラクタに対するテストケース
==================================

コンストラクタに対するテストでは、引数に指定した値が、正しくプロパティに設定されているかを確認するケースを作成する。\
このとき対象となるプロパティは、Entityにに定義されている全てのプロパティである。\
テストデータには、プロパティ名とそれに設定するデータと期待値(getterで取得した値と比較するデータ)を用意する。

下図では、以下のように各プロパティに値を指定している。
テストでは、コンストラクタにこれらの値の組み合わせを与えたとき、各プロパティに指定した値が設定されているか(getterを呼び出して、想定通りの値が取得できるか)確認している。

実際のテストコードでは、コンストラクタへの値の設定及び値の確認は、自動テストフレームワークで提供されるメソッド内で行われる。
詳細は、 :ref:`テストコード<test-constructor-java-label>` を参照すること。


.. tip::
   
   Entityは自動生成されるため、アプリケーションで使用されないコンストラクタが生成される可能性がある。\
   その場合リクエスト単体テストではテストできないため、Entity単体テストでコンストラクタに対するテストを必ず行うこと。
   
   一方、一般的なFormの場合、アプリケーションで使用するコンストラクタのみを作成する。\
   したがって、リクエスト単体テストでコンストラクタのテストを行うことができる。\
   そのため、一般的なFormについては、クラス単体テストでコンストラクタのテストを行う必要はない。

Excelへの定義
-------------
.. image:: ./_image/entityUnitTest_Constructor.png
    :scale: 80

※Entityの保有するプロパティ名のExcelへの記述手順は、 :ref:`property-name-copy-label` を参照。

上記設定値のテスト内容(抜粋)

=============== =========================== ================================
プロパティ      コンストラクタに設定する値  期待値(getterから取得される値
=============== =========================== ================================
userId          userid                      userid
loginId         loginid                     loginid
password        password                    password
=============== =========================== ================================

.. _test-constructor-java-label:

このデータを使用するテストメソッドを以下に示す。

.. code-block:: java

   // 【説明】～前略～

   public class SystemAccountEntityTest extends EntityTestSupport {

        /** コンストラクタのテスト */
        @Test
        public void testConstructor() {
            Class<?> entityClass = SystemAccountEntity.class;
            String sheetName = "testAccessor";
            String id = "testConstructor";
            testConstructorAndGetter(entityClass, sheetName, id);
        }

   }


.. _testConstructorAndGetter-note-label:

.. tip::

  testConstructorAndGetterでテスト可能なプロパティの型(クラス)には制限がある。
  下記型(クラス)に該当しない場合には、各テストクラスにてコンストラクタとgetterを明示的に呼び出してテストする必要がある。


  * String及び、String配列
  * BigDecimal及び、BigDecimal配列
  * valueOf(String)メソッドを持つクラス及び、その配列クラス(例えばIntegerやLong、java.sql.Dateやjava.sql.Timestampなど)

  以下に、個別のテスト実施方法の例を示す。


    * Excelへのデータ記述例

      .. image:: _image/entityUnitTest_ConstructorOther.png
        :scale: 80

    

    * テストコード例

      .. code-block:: java

       /** コンストラクタのテスト */
       @Test
       public void testConstructor() {
           // 【説明】
           // 共通にテストが実施出来る項目は、testConstructorAndGetterを使用してテストを実施する。
           Class<?> entityClass = SystemAccountEntity.class;
           String sheetName = "testAccessor";
           String id = "testConstructor";
           testConstructorAndGetter(entityClass, sheetName, id);

           // 【説明】
           // 共通にテストが実施出来ない項目は、個別にテストを実施する。

           // 【説明】
           // getParamMapを呼び出し、個別にテストを行うプロパティのテストデータを取得する。
           // (テスト対象のプロパティが複数ある場合は、getListParamMapを使用する。)
           Map<String, String[]> data = getParamMap(sheetName, "testConstructorOther");

           // 【説明】Map<String, String[]>から、Entityのコンストラクタの引数であるMap<String, Object>へ変換する
           Map<String, Object> params = new HashMap<String, Object>();
           params.put("users", Arrays.asList(data.get("set")));

           // 【説明】上記で生成したMap<String, Object>を引数にEntityを生成する。
           SystemAccountEntity entity = new SystemAccountEntity(params);

           // 【説明】getterを呼び出し、期待値通りの値が返却されることを確認する。
           assertEquals(entity.getUsers(), Arrays.asList(data.get("get")));

       }




.. _entityUnitTest_SetterGetterCase:

setter、getterに対するテストケース
==================================

setter、getterに対するテストでは、setterで設定した値とgetterで取得した値が、期待通りになっているか確認するケースを作成する。\
このとき対象となるプロパティは、Entityに定義されている全てのプロパティである。

各プロパティに対して、setterに渡すためのデータと期待値(getterで取得した値と比較するデータ)を用意する。
テストメソッドでは、前述のsetterに渡すためのデータを引数にsetterを呼び出し、直後にgetterで取得した値と期待値が\
等しいことを確認している。

実際のテストコードでは、setterへの値の設定及び値の確認(期待値との比較)は、
自動テストフレームワークで提供されるメソッド内で行われる。 詳細は、 テストコード を参照すること。


.. tip::
   
   Entityは自動生成されるため、アプリケーションで使用されないsetter/getterが生成される可能性がある。\
   その場合リクエスト単体テストではテストできないため、Entity単体テストでsetter/getterに対するテストを必ず行うこと。
   
   一方、一般的なFormの場合、アプリケーションで使用するsetter/getterのみを作成する。\
   したがって、リクエスト単体テストでsetter/getterのテストを行うことができる。\
   そのため、一般的なFormについては、クラス単体テストでsetter/getterのテストを行う必要はない。


Excelへの定義
-------------
.. image:: ./_image/entityUnitTest_SetterAndGetter.png
    :scale: 90

※Entityの保有するプロパティ名のExcelへの記述手順は、 :ref:`property-name-copy-label` を参照。

このデータを使用するテストメソッドを以下に示す。

.. code-block:: java

   // 【説明】～前略～

   public class SystemAccountEntityTest extends EntityTestSupport {

       /**
        * setter、getterのテスト
        */
       @Test
       public void testSetterAndGetter() {
           Class<?> entityClass = SystemAccountEntity.class;
           String sheetName = "testAccessor";
           String id = "testGetterAndSetter";
           testSetterAndGetter(entityClass, sheetName, id);
       }

       // 【説明】～後略～

.. tip::

  testGetterAndSetterでテスト可能なプロパティの型(クラス)には制限がある。
  制限内容の詳細は、 :ref:`entityUnitTest_ConstructorCase` を参照すること。

.. tip::

  setterやgetterにロジックを記述した場合(例えば、setterは郵便番号上3桁と下4桁に別れているが、getterはまとめて7桁取得する場合など)は、
  そのロジックを確認するテストケースを作成すること。

  上記のテストをExcelに定義する場合には、下記画像のように定義する。::

    郵便番号に下記を設定した場合に、正しく7桁の郵便番号(0010001)が取得することを確認する例
      郵便番号上3桁:001
      郵便番号下4桁:0001

  .. image:: ./_image/entityUnitTest_SetterAndGetter_PostNo.png
    :scale: 80


.. _property-name-copy-label:

プロパティ名の一覧を簡易的に取得する手順
========================================
①Eclipseでテスト対象のEntityクラスをオープンし、Outline(アウトライン)を表示する。

  .. image:: ./_image/entityUnitTest_PropertyWrite1.png
    :scale: 85

②コピーしたいプロパティを選択する。

  .. image:: ./_image/entityUnitTest_PropertyWrite2.png

③マウスの右クリックで表示されるメニューからCopy Qualified Name(修飾名のコピー)を選択する。

  .. image:: ./_image/entityUnitTest_PropertyWrite3.png

④コピーしたプロパティ名のリストをエクセルに貼り付ける。

 貼りつけた値には、下記画像のように「クラス名 + プロパティ名」の完全修飾名の形式になっている。
 このため、Excelの置き換え機能を使用して不要なクラス名を削除する。

 Entityクラスが、「nablarch.sample.management.user.SystemAccountEntity」の場合の置き換え例::
 
  検索する文字列：nablarch.sample.management.user.SystemAccountEntity.
  置き換え後の文字列：(空のまま)

 .. image:: ./_image/entityUnitTest_PropertyWrite4.png

\

自動テストフレームワーク設定値
==============================

:ref:`entityUnitTest_ValidationCase`\ を実施する際に必要な初期値設定について説明する。


設定項目一覧
------------

``nablarch.test.core.entity.EntityTestConfiguration``\ クラスを使用し、\
以下の値をコンポーネント設定ファイルで設定する（全項目必須）。

+--------------------+----------------------------------------------+
|     設定項目名     |説明                                          |
+====================+==============================================+
|maxMessageId        |最大文字列長超過時のメッセージID              |
+--------------------+----------------------------------------------+
|maxAndMinMessageId  |最長最小文字列長範囲外のメッセージID(可変長)  |
+--------------------+----------------------------------------------+
|fixLengthMessageId  |最長最小文字列長範囲外のメッセージID(固定長)  |
+--------------------+----------------------------------------------+
|underLimitMessageId |文字列長不足時のメッセージID                  |
+--------------------+----------------------------------------------+
|emptyInputMessageId |未入力時のメッセージID                        |
+--------------------+----------------------------------------------+
|characterGenerator  |文字列生成クラス \ [#]_\                      |
+--------------------+----------------------------------------------+

\

.. [#]
 ``nablarch.test.core.util.generator.CharacterGenerator``\ の実装クラスを指定する。
 このクラスがテスト用の入力値を生成する。
 通常は、\ ``nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator``\ を使用すれば良い。


設定するメッセージIDは、バリデータの設定値と合致させる。

（以下の記述例を参照）


コンポーネント設定ファイルの記述例
------------------------------------

以下の設定値を使用する場合のコンポーネント設定ファイル記述例を示す。

**【精査クラスのコンポーネント設定ファイル】**

.. code-block:: xml

    <property name="validators">
      <list>
        <component class="nablarch.core.validation.validator.RequiredValidator">
          <property name="messageId" value="MSG00010"/>
        </component>
        <component class="nablarch.core.validation.validator.LengthValidator">
          <property name="maxMessageId" value="MSG00011"/>
          <property name="maxAndMinMessageId" value="MSG00011"/>
          <property name="fixLengthMessageId" value="MSG00023"/>
        </component>
        <!-- 中略 -->
    </property>


**【テストのコンポーネント設定ファイル】**

.. code-block:: xml
 
  <!-- エンティティテスト設定 -->
  <component name="entityTestConfiguration" class="nablarch.test.core.entity.EntityTestConfiguration">
    <property name="maxMessageId"        value="MSG00011"/>
    <property name="maxAndMinMessageId"  value="MSG00011"/>
    <property name="fixLengthMessageId"  value="MSG00023"/>
    <property name="underLimitMessageId" value="MSG00011"/>
    <property name="emptyInputMessageId" value="MSG00010"/>
    <property name="characterGenerator">
      <component name="characterGenerator"
                 class="nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator"/>
    </property>
  </component>
