.. _deal_unit_test_batch:

取引単体テスト（Nablarchバッチアプリケーション）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

Nablarchバッチアプリケーションの取引単体テストは、1つの取引を構成する複数のバッチ処理を1つのテストメソッドの中で順に動かし、取引全体が想定どおりに処理されることを検証する。

機能概要
--------------------------------------------------

テスティングフレームワークは、リクエスト単体テストと同じ仕組みでバッチを起動する機能を提供している。この機能を1つのテストメソッドの中で連続して呼び出すことで、取引単位のテストになる。

使用方法
--------------------------------------------------

テストの実行方法は\ :ref:`リクエスト単体テスト（Nablarchバッチアプリケーション） <request_unit_test_batch>`\ と同じである。テストデータの格納場所と記述方法は\ :ref:`テストデータの書き方 <testdata_notation>`\ に従う。コンポーネント設定は\ :ref:`リクエスト単体テストの設定（Nablarchバッチアプリケーション） <request_unit_test_setting_batch>`\ に従ってあらかじめ済ませておく。ここでは、テストクラスの作り方、テストメソッドの作り方、テストデータの作り方を順に説明する。

テストクラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストクラスは、次の条件を満たすように作成する。

* パッケージは、テスト対象の取引のパッケージとする。
* クラス名は\ ``<取引ID>Test``\ とする。
* :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ を継承する。

取引\ ID\ が\ ``B21AC01``\ の場合、テストクラスは次のようになる。

.. code-block:: java

  package nablarch.sample.ss21AC01;

  import nablarch.test.core.batch.BatchRequestTestSupport;

  // 中略

  public class B21AC01Test extends BatchRequestTestSupport {
  }

テストメソッドを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1つの取引は、1つのテストメソッドの中で実行する。テストメソッドから\ ``execute``\ を呼ぶと、読み込み単位に記述したテストショットが上から順に実行される。

.. code-block:: java

  /** 正常終了するテスト */
  @Test
  public void testSuccess() {
      execute();
  }

引数なしの\ ``execute``\ は、テストメソッド名と同じ名前の読み込み単位を読み込む。読み込み単位を複数に分ける場合は、読み込み単位の名前を引数に渡した\ ``execute``\ を、読み込み単位の数だけ呼ぶ。

.. code-block:: java

  package nablarch.sample.ss21AA01;

  import org.junit.Test;
  import nablarch.test.core.batch.BatchRequestTestSupport;

  // 中略

  public class B21AA01Test extends BatchRequestTestSupport {

      @Test
      public void testSuccess() {
          // 入力ファイルをテンポラリテーブルに登録
          execute("testSuccess_fileInput");

          // テンポラリテーブルの情報をもとにユーザ関連テーブルを削除
          execute("testSuccess_userDelete");

          // 結果をファイル出力
          execute("testSuccess_fileOutput");
      }
  }

テストデータを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1つの読み込み単位（\ Excel\ 形式では1シート、\ YAML\ 形式では1ファイル）につき1つのテストを記述することを原則とする。1つの取引を構成する複数のバッチ処理は、その読み込み単位のテストショット一覧に上から順に並べる。テストショット一覧に記述できるカラムの仕様は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ を、処理方式ごとの一般的な記述例は\ :ref:`テストデータの記載例 <testdata_examples>`\ を参照。ここでは、取引単体テストに固有の書き方だけを示す。

原則に対する例外は2つある。テストデータが大量である場合や、1つの取引に含まれる処理が多い場合は、すべてのテストデータを1つの読み込み単位に詰め込むと読みにくくなる。このときは、1つのテストを複数の読み込み単位に分割してよい。逆に、非常に簡単なテストでデータ量が少ない場合は、1つの読み込み単位に複数のテストを含めてよい。

以降では、次の3つの書き方を\ Excel\ 形式・\ YAML\ 形式のそれぞれについて示す。

* **1つの読み込み単位にまとめる**\ 。原則どおりの書き方である。ファイル入力・ユーザ削除・ファイル出力の3つの処理で構成される取引（取引\ ID\ は\ ``B21AC01``\ ）を、3件のテストショットとして1つの読み込み単位に記述する。テストメソッドは引数なしの\ ``execute``\ を1回呼ぶだけであり、読み込み単位の名前はテストメソッド名と同じ\ ``testSuccess``\ になる
* **複数の読み込み単位に分割する**\ 。1つ目の例外である。同じ構成の取引（取引\ ID\ は\ ``B21AA01``\ ）を、処理ごとに\ ``testSuccess_fileInput``\ ・\ ``testSuccess_userDelete``\ ・\ ``testSuccess_fileOutput``\ の3つの読み込み単位に分ける。テストメソッドからは、それぞれの名前を引数に渡して\ ``execute``\ を呼ぶ
* **1つの読み込み単位に複数のテストを含める**\ 。2つ目の例外である。通常の入力と入力データが0件の場合という2つのテストを、1つの読み込み単位に記述する。テストショット番号は\ ``1-1``\ ・\ ``1-2``\ ・\ ``2-1``\ ・\ ``2-2``\ のように「テストの番号 - 取引内での順序」の形で付ける

``setUpTable``\ ・\ ``setUpFile``\ ・\ ``expectedTable``\ ・\ ``expectedFile``\ の各カラムに書く値は、同じ読み込み単位にあるデータブロックのグループIDである。\ ``default``\ は、グループIDを持たないデータブロックを指す。グループIDの記述方法は\ :ref:`グループIDによる使い分け <testdata_notation-group_id>`\ を参照。

``setUpTable``\ ・\ ``setUpFile``\ に値を書いたテストショットでは、そのテストショットを実行する直前に準備データが投入される。取引を構成する複数の処理を1つの読み込み単位に並べた場合も、投入はテストショットごとに行われる。

``expectedTable``\ ・\ ``expectedFile``\ を空欄にしたテストショットでは、テーブル・ファイルの検証を行わない。以降に示す3つの書き方で期待値のカラムの有無が異なるのは、それぞれの処理で検証する対象だけを記述しているためである。

Excel形式の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**1つの読み込み単位にまとめる**

シート名は\ ``testSuccess``\ である。カラム数が多いため、前半・後半に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :header-rows: 0
  :widths: 6,20,20,30,24

  * - LIST_MAP=testShots
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
    - requestPath
  * - 1
    - ファイル入力
    - 0
    - ss21AC01/B21AC01.xml
    - fileInputBatch
  * - 2
    - ユーザ削除
    - 0
    - ss21AC01/B21AC01.xml
    - userDeleteBatch
  * - 3
    - ファイル出力
    - 0
    - ss21AC01/B21AC01.xml
    - fileOutputBatch

.. list-table::
  :header-rows: 0
  :widths: 6,12,18,16,26,22

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
  * - no
    - userId
    - setUpTable
    - setUpFile
    - expectedTable
    - expectedFile
  * - 1
    - test
    - default
    - default
    - default
    -
  * - 2
    - test
    - default
    -
    - default
    -
  * - 3
    - test
    - default
    -
    -
    - default

**複数の読み込み単位に分割する**

3つのシートに分けて記述する。各シートが持つ準備データと期待値のカラムは、その処理に必要なものだけになる。必須カラムである\ ``no``\ ・\ ``description``\ ・\ ``expectedStatusCode``\ ・\ ``diConfig``\ ・\ ``requestPath``\ ・\ ``userId``\ は、どのシートにも記述する。

.. list-table::
  :header-rows: 0
  :widths: 6,14,16,20,17,7,10,10

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
    - requestPath
    - userId
    - setUpTable
    - setUpFile
  * - 1
    - ファイル入力
    - 0
    - ss21AA01/B21AA01.xml
    - fileInputBatch
    - test
    - default
    - default

.. list-table::
  :header-rows: 0
  :widths: 6,14,16,20,16,7,10,11

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
    - requestPath
    - userId
    - setUpTable
    - expectedTable
  * - 1
    - ユーザ削除
    - 0
    - ss21AA01/B21AA01.xml
    - userDeleteBatch
    - test
    - default
    - default

.. list-table::
  :header-rows: 0
  :widths: 6,14,16,20,16,7,10,11

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
    - requestPath
    - userId
    - setUpTable
    - expectedFile
  * - 1
    - ファイル出力
    - 0
    - ss21AA01/B21AA01.xml
    - fileOutputBatch
    - test
    - default
    - default

**1つの読み込み単位に複数のテストを含める**

シート名は\ ``testSuccess``\ である。カラム数が多いため、前半・後半に分けて示す（実際のシートでは1行に続けて記述する）。

.. list-table::
  :header-rows: 0
  :widths: 8,24,18,28,22

  * - LIST_MAP=testShots
    -
    -
    -
    -
  * - no
    - description
    - expectedStatusCode
    - diConfig
    - requestPath
  * - 1-1
    - ファイル入力
    - 0
    - ss21AC01/B21AC01.xml
    - fileInputBatch
  * - 1-2
    - ユーザ削除
    - 0
    - ss21AC01/B21AC01.xml
    - userDeleteBatch
  * - 2-1
    - ファイル入力（0件）
    - 0
    - ss21AC01/B21AC01.xml
    - fileInputBatch
  * - 2-2
    - ユーザ削除（0件）
    - 0
    - ss21AC01/B21AC01.xml
    - userDeleteBatch

.. list-table::
  :header-rows: 0
  :widths: 8,12,18,16,24,22

  * - LIST_MAP=testShots
    -
    -
    -
    -
    -
  * - no
    - userId
    - setUpTable
    - setUpFile
    - expectedTable
    - expectedFile
  * - 1-1
    - test
    - shot1
    - shot1
    -
    -
  * - 1-2
    - test
    -
    -
    - shot1
    -
  * - 2-1
    - test
    - shot2
    - shot2
    -
    -
  * - 2-2
    - test
    -
    -
    - shot2
    -

YAML形式の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**1つの読み込み単位にまとめる**

テストクラスと同じ名前のディレクトリに置いた\ ``testSuccess.yaml``\ に記述する。ファイル名はテストメソッド名と同じである。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "ファイル入力"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "fileInputBatch"
          userId: "test"
          setUpTable: "default"
          setUpFile: "default"
          expectedTable: "default"
          expectedFile: ""
        - no: "2"
          description: "ユーザ削除"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "userDeleteBatch"
          userId: "test"
          setUpTable: "default"
          setUpFile: ""
          expectedTable: "default"
          expectedFile: ""
        - no: "3"
          description: "ファイル出力"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "fileOutputBatch"
          userId: "test"
          setUpTable: "default"
          setUpFile: ""
          expectedTable: ""
          expectedFile: "default"

**複数の読み込み単位に分割する**

同じディレクトリに、読み込み単位ごとのファイルを置く。

.. code-block:: text

  src/test/java/nablarch/sample/ss21AA01/
    B21AA01Test/
      ├── testSuccess_fileInput.yaml
      ├── testSuccess_userDelete.yaml
      └── testSuccess_fileOutput.yaml

``testSuccess_fileInput.yaml``\ の内容を示す。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "ファイル入力"
          expectedStatusCode: "0"
          diConfig: "ss21AA01/B21AA01.xml"
          requestPath: "fileInputBatch"
          userId: "test"
          setUpTable: "default"
          setUpFile: "default"

``testSuccess_userDelete.yaml``\ の内容を示す。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "ユーザ削除"
          expectedStatusCode: "0"
          diConfig: "ss21AA01/B21AA01.xml"
          requestPath: "userDeleteBatch"
          userId: "test"
          setUpTable: "default"
          expectedTable: "default"

``testSuccess_fileOutput.yaml``\ の内容を示す。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1"
          description: "ファイル出力"
          expectedStatusCode: "0"
          diConfig: "ss21AA01/B21AA01.xml"
          requestPath: "fileOutputBatch"
          userId: "test"
          setUpTable: "default"
          expectedFile: "default"

**1つの読み込み単位に複数のテストを含める**

準備データと期待値はグループID（\ ``shot1``\ ・\ ``shot2``\ ）で使い分ける。

.. code-block:: yaml

  list_maps:
    - id: testShots
      rows:
        - no: "1-1"
          description: "ファイル入力"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "fileInputBatch"
          userId: "test"
          setUpTable: "shot1"
          setUpFile: "shot1"
          expectedTable: ""
          expectedFile: ""
        - no: "1-2"
          description: "ユーザ削除"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "userDeleteBatch"
          userId: "test"
          setUpTable: ""
          setUpFile: ""
          expectedTable: "shot1"
          expectedFile: ""
        - no: "2-1"
          description: "ファイル入力（0件）"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "fileInputBatch"
          userId: "test"
          setUpTable: "shot2"
          setUpFile: "shot2"
          expectedTable: ""
          expectedFile: ""
        - no: "2-2"
          description: "ユーザ削除（0件）"
          expectedStatusCode: "0"
          diConfig: "ss21AC01/B21AC01.xml"
          requestPath: "userDeleteBatch"
          userId: "test"
          setUpTable: ""
          setUpFile: ""
          expectedTable: "shot2"
          expectedFile: ""
