.. _testing_framework_introduction:

テスティングフレームワークの導入
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
テスティングフレームワークを使うには、テストの種類によらず次の3つを行う。依存関係の追加、テスト用のコンポーネント設定ファイルの用意、テストデータの投入に使用するトランザクションの登録である。いずれもテストを書く前に済ませておく。テストの種類や処理方式に固有の設定は、以降のページで行う。

使用方法
--------------------------------------------------

テスティングフレームワークを依存関係に追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークは\ ``nablarch-testing``\ として提供される。テストでのみ使用するため、\ ``test``\ スコープで依存関係に追加する。

.. code-block:: xml

  <!-- テスティングフレームワーク -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing</artifactId>
    <scope>test</scope>
  </dependency>

.. tip::

  処理方式によっては、専用のモジュールを使用する。専用のモジュールが\ ``nablarch-testing``\ に依存する場合は、\ ``nablarch-testing``\ を個別に追加しなくてよい。必要なモジュールは、\ :ref:`リクエスト単体テストの設定（RESTfulウェブサービス） <request_unit_test_setting_rest>`\ のように、該当するページに記載している。

.. _testing_framework_introduction-test_component_config:

テスト用のコンポーネント設定ファイルを用意する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークは、テストの実行時にクラスパス直下の\ ``unit-test.xml``\ をコンポーネント設定ファイルとして読み込む。このファイルには、本番用のコンポーネント設定ファイルをimportしたうえで、テストに必要な設定を記述する。本番用と異なる設定にするコンポーネントは、importの後に同じ名前で定義して上書きする（\ :ref:`repository-override_bean`\ ）。以降のページで「テスト用のコンポーネント設定ファイル」と書いている設定は、すべてこのファイルに記述する。

環境設定ファイルは、importした本番用のコンポーネント設定ファイルが読み込むものがそのまま使われる。テストだけで使う設定値と、本番用と異なる値にする設定値は、テスト用の環境設定ファイルに記述し、このファイルからconfig-file要素で読み込む（\ :ref:`repository-user_environment_configuration`\ ）。後から読み込んだ値が優先されるため、config-file要素はimportの後に置く。以降のページで「環境設定ファイルに記述する」と書いている設定値は、このテスト用の環境設定ファイルに記述する。

.. code-block:: xml

  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">

    <!-- 本番用のコンポーネント設定ファイル -->
    <import file="web-component-configuration.xml"/>

    <!-- テスティングフレームワークのデフォルト設定（必要なものを各ページに従って追加する） -->
    <import file="nablarch/test/test-data.xml"/>
    <import file="nablarch/test/test-transaction.xml"/>

    <!-- 本番用の設定の上書き -->
    <component name="..." class="..."/>

    <!-- テスト用の環境設定ファイル -->
    <config-file file="unit-test.properties"/>

  </component-configuration>

.. _testing_framework_introduction-test_transaction:

テストデータの投入に使用するトランザクションを登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークは、データベースの準備データの投入と、テーブルの内容の取得を、テスト対象の処理とは別のトランザクションで行う。このトランザクションには\ ``testTran``\ という名前のコンポーネントを使用する。名前は固定であり、変更できない。登録していない場合は、準備データを投入する時点で例外が発生する。

デフォルト設定\ ``nablarch/test/test-transaction.xml``\ に、この名前で\ :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>`\ が定義されている。テスト用のコンポーネント設定ファイルでこのファイルをimportする。

.. code-block:: xml

  <import file="nablarch/test/test-transaction.xml"/>

この定義は、\ ``connectionFactory``\ ・\ ``transactionFactory``\ という名前のコンポーネントを参照する。本番用のコンポーネント設定ファイルで接続やトランザクションのファクトリを別の名前で登録している場合は、importせずに、同じ内容を自分で定義する。

.. code-block:: xml

  <!-- テストデータの投入・取得に使用するトランザクション -->
  <component name="testTran" class="nablarch.core.db.transaction.SimpleDbTransactionManager">
    <property name="dbTransactionName" value="test"/>
    <property name="connectionFactory" ref="connectionFactory"/>
    <property name="transactionFactory" ref="jdbcTransactionFactory"/>
  </component>
