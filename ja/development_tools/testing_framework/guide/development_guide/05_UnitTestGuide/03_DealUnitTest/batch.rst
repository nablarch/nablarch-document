==================================
取引単体テストの実施方法（バッチ）
==================================

バッチ処理の取引単体テストは、自動テストフレームワークを使用してテストを行う。
リクエスト単体テストを連続実行することにより、取引単位でのテストを行う。

テストクラスは以下の条件を満たすように作成する。

* テストクラスのパッケージはテスト対象取引のパッケージとする。
* <取引ID>Testというクラス名でテストクラスを作成する。

例えば、テスト対象取引の取引IDがB21AC01だとすると、テストクラスは以下のようになる。

.. code-block:: java

 package nablarch.sample.ss21AC01

 import nablarch.test.core.batch.BatchRequestTestSupport;
 import nablarch.test.junit5.extension.batch.BatchRequestTest;

 // 中略

 @BatchRequestTest
 class B21AC01Test {

     BatchRequestTestSupport support;
 

テストケース分割方針
====================

基本的には、\ **1シートにつき1テストケース**\ とする。
以下、例外事項を示す。


複雑なテストケースの場合
------------------------

テストデータが大量であったり、1取引に含まれる処理が多い場合に、\
１つのシートに全てのテストデータを詰め込むと、シート内にデータが多くなり過ぎて、\
テストデータの可読性が落ちる場合がある。\
このような場合は、1ケースを複数シートに分割して記述しても良い。


非常に簡単なテストケースの場合
------------------------------

非常に簡単なテストケースで、テストデータ量が少ない場合、
1シートに全テストケースを含めてもよい。


基本的な記述方法
================

基本的には、1テストケースを1シートにまとめて記述する。\
1シート内に複数のバッチ実行を記述することにより、取引単位のテストとなる。

以下の例では、３つのバッチ(ファイル入力バッチ、ユーザ削除バッチ、ファイル出力バッチ)\
で構成される取引を処理している。

.. code-block:: java

 /** 正常終了するケース */
 @Test
 void testSuccess() {
     support.execute();
 }


**【testSuccessシート】**

LIST_MAP=testShots

=== ============= ==================  ========== ========= ============== ============ ===============
no  description   expectedStatusCode  setUpTable setUpFile expectedTable  expectedFile   requestPath    
=== ============= ==================  ========== ========= ============== ============ ===============
 1  ファイル入力                 100  default    default   default                     fileInputBatch 
 2  ユーザ削除                   100  default              default                     userDeleteBatch
 3  ファイル出力                 100  default              fileInputBatch default      fileOutputBatch          
=== ============= ==================  ========== ========= ============== ============ ===============


1テストケースを複数シートを分割する場合
=======================================

                                           
例えば、前項(\ `基本的な記述方法`_\ )で例示したテストケースは、以下のように分割して記述可能である。


.. code-block:: java

 package nablarch.sample.ss21AA01

 import org.junit.jupiter.api.Test;
 import nablarch.test.core.batch.BatchRequestTestSupport;
 import nablarch.test.junit5.extension.batch.BatchRequestTest;

 // 中略

 @BatchRequestTest
 class B21AA01Test {

     BatchRequestTestSupport support;

     @Test
     void testSuccess() {

         // 入力ファイルをテンポラリテーブルに登録
         support.execute("testSuccess_fileInput");

         // テンポラリテーブルの情報をユーザ関連テーブルを削除
         support.execute("testSuccess_userDelete");

         // 結果をファイル出力
         support.execute("testSuccess_fileOutput");
     }

\

**【testSuccess_fileInputシート】**

LIST_MAP=testShots

==== ============= ==================  ========== ========= ===============
 no  case          expectedStatusCode  setUpTable setUpFile    requestPath    
==== ============= ==================  ========== ========= ===============
  1  ファイル入力                 100  default    default   fileInputBatch 
==== ============= ==================  ========== ========= ===============

\

**【testSuccess_userDeleteシート】**

LIST_MAP=testShots

==== ============= ==================  ========== ============= ===============
 no  case          expectedStatusCode  setUpTable expectedTable requestPath    
==== ============= ==================  ========== ============= ===============
  1  ユーザ削除                   100  default    default       userDeleteBatch
==== ============= ==================  ========== ============= ===============


**【testSuccess_fileOutputシート】**

LIST_MAP=testShots

==== ============= ==================  ========== ========= ===============
 no  case          expectedStatusCode  setUpTable outFile    requestPath    
==== ============= ==================  ========== ========= ===============
  1  ファイル出力                 100  default    default   fileOutputBatch 
==== ============= ==================  ========== ========= ===============


1シートに複数ケースを含める場合
===============================

非常に簡単なテストケースの場合は、複数にまとめてもよい。

以下の例では、２つのテストケース（通常のケースと入力データが0件のケース）を\
１つのシートで記述している

.. code-block:: java

 /** 正常終了するケース */
 @Test
 void testSuccess() {
     support.execute();
 }


**【testSuccessシート】**

LIST_MAP=testShots

=== ==================== ==================  ========== ========= ============== ============ ===============
 no  description         expectedStatusCode  setUpTable setUpFile expectedTable  expectedFile   requestPath    
=== ==================== ==================  ========== ========= ============== ============ ===============
1-1  ファイル入力                    100      shot1      shot1                                fileInputBatch 
1-2  ユーザ削除                      100                           shot1                      userDeleteBatch
2-1  ファイル入力（0件）             100      shot2      shot2                                fileInputBatch 
2-2  ユーザ削除（0件）               100                           shot2                      userDeleteBatch
=== ==================== ==================  ========== ========= ============== ============ ===============

\

.. tip::
 グループIDを使用することで1シートに複数ケースのテストデータを記述できる。
 詳細は、『\ :ref:`tips_groupId`\ 』の項を参照。


