.. _request_unit_test_setting_rest:

リクエスト単体テストの設定（RESTfulウェブサービス）
===================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------

RESTfulウェブサービスのリクエスト単体テストには、専用のモジュールとデフォルト設定の追加が必要である。内蔵サーバに配備するルートディレクトリと、内蔵サーバで実行するハンドラキューは、コンポーネント設定ファイルで変更できる。テストの実装方法は\ :ref:`リクエスト単体テスト（RESTfulウェブサービス） <request_unit_test_rest>`\ を参照。

使用方法
--------------------------------------------------

必要なモジュールとコンポーネント設定を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
RESTfulウェブサービスのリクエスト単体テストには、次の3つのモジュールが必要である。いずれもテストでのみ使用するため、\ ``test``\ スコープで依存関係に追加する。

.. code-block:: xml

  <!-- RESTfulウェブサービス用のテスティングフレームワーク -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-rest</artifactId>
    <scope>test</scope>
  </dependency>
  <!-- テスティングフレームワークのデフォルト設定 -->
  <dependency>
    <groupId>com.nablarch.configuration</groupId>
    <artifactId>nablarch-testing-default-configuration</artifactId>
    <scope>test</scope>
  </dependency>
  <!-- 内蔵サーバの実装 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-jetty12</artifactId>
    <scope>test</scope>
  </dependency>

.. tip::

  ``nablarch-testing-rest``\ は\ ``nablarch-testing``\ に依存する。上記の3つを追加することで、\ :ref:`テスティングフレームワーク <testing_framework_about>`\ が提供するAPIも使用できる。

テスティングフレームワークの設定は、テスト用のコンポーネント設定ファイルに記述する。ブランクプロジェクトでは\ ``src/test/resources/unit-test.xml``\ が該当する。RESTfulウェブサービスのリクエスト単体テストを実行するには、デフォルト設定として提供されている設定ファイルの読み込みと、内蔵サーバを生成するファクトリの登録を記述する。

.. code-block:: xml

  <import file="nablarch/test/rest-request-test.xml"/>
  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty12"/>

.. important::

  ``nablarch-testing-jetty12``\ が提供するのは、内蔵サーバと\ :ref:`リクエスト単体データ作成ツール <request_data_tool>`\ のクラスだけである。コンポーネントの登録は行わないため、\ ``httpServerFactory``\ を登録していないと、内蔵サーバの生成時に例外が発生する。

.. tip::

  アーキタイプから\ :doc:`RESTfulウェブサービスプロジェクト <../../../../application_framework/application_framework/blank_project/setup_blankProject/setup_WebService>`\ を作成した場合は、上記の依存関係と設定が既に記述されている。\ :doc:`ウェブプロジェクト <../../../../application_framework/application_framework/blank_project/setup_blankProject/setup_Web>`\ や\ :doc:`Nablarchバッチプロジェクト <../../../../application_framework/application_framework/blank_project/setup_blankProject/setup_NablarchBatch>`\ から作成した場合は、不足している記述を追加する。

:java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>`\ を使用するテストクラスでデータベースを扱う場合は、テストデータを解析する\ ``testDataParser``\ のコンポーネントも登録する。記述例は\ :ref:`省略したテーブルのカラムのデフォルト値を変更する <class_unit_test_setting-column_default_values>`\ を参照。

コンポーネント設定ファイルで設定値を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
デフォルト設定を読み込むと、\ :java:extdoc:`RestTestConfiguration <nablarch.test.core.http.RestTestConfiguration>`\ が\ ``restTestConfiguration``\ というコンポーネント名で登録される。実行環境に依存する設定値は、このコンポーネントを同じ名前で上書きして変更する。上書きの記述は、デフォルト設定の読み込みより後に置く。主な設定項目は次のとおりである。デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 25,50,25

  * - 設定項目名
    - 説明
    - デフォルト値
  * - ``webBaseDir``
    - 内蔵サーバに配備するウェブアプリケーションのルートディレクトリ
    - ``src/main/webapp``
  * - ``webFrontControllerKey``
    - 内蔵サーバで実行するハンドラキューの取得元となる\ :ref:`Webフロントコントローラ <web_front_controller>`\ のコンポーネント名
    - ``webFrontController``

ルートディレクトリが複数に分かれている場合は、\ ``webBaseDir``\ にカンマ区切りで指定する。プロジェクト共通のウェブモジュールを別に持つ構成が該当する。内蔵サーバは、指定された順にディレクトリを探索し、最初に見つかったリソースを使用する。

.. code-block:: xml

  <component name="restTestConfiguration" class="nablarch.test.core.http.RestTestConfiguration">
    <property name="webBaseDir" value="/path/to/web-a/,/path/to/web-common"/>
  </component>

``webFrontControllerKey``\ は、\ :ref:`Webフロントコントローラ <web_front_controller>`\ を\ ``webFrontController``\ 以外のコンポーネント名で登録している場合に指定する。ウェブアプリケーションとRESTfulウェブサービスを併用し、ハンドラ構成の異なるWebフロントコントローラを複数定義する構成が該当する。コンポーネント定義の例は\ :ref:`委譲するWebフロントコントローラの名前を変更する <change_web_front_controller_name>`\ を参照。この項目を指定しないと、ウェブアプリケーション用のハンドラキューが内蔵サーバで実行される。

.. code-block:: xml

  <component name="restTestConfiguration" class="nablarch.test.core.http.RestTestConfiguration">
    <property name="webFrontControllerKey" value="jaxrsController"/>
  </component>
