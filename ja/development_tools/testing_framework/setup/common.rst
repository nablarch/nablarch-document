.. _testing_framework_common:

共通設定
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
共通設定は、テストの種類によらず、テスティングフレームワークを使うすべてのプロジェクトで行う設定である。依存関係の追加とテスト用のコンポーネント設定ファイルの用意は必須で、テストを書く前に済ませておく。そのほかに、システム日時の固定やテストデータの読み込み先の変更など、テストを安定して繰り返すための設定をここでまとめて行う。

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

.. _testing_framework_common-test_component_config:

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

    <!-- 本番用の設定の上書き -->
    <component name="..." class="..."/>

    <!-- テスト用の環境設定ファイル -->
    <config-file file="unit-test.properties"/>

  </component-configuration>

.. _testing_framework_common-yaml_testdata:

テストデータの形式をYAMLに変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータは、デフォルトでは\ Excel\ 形式で読み込まれる。\ Excel\ 形式で記述する場合、設定は不要である。

YAML\ 形式で記述する場合は、\ ``nablarch-testing-yaml``\ を依存関係に追加する。\ YAML\ 形式のテストデータを解析するクラスは、このモジュールが提供する。

.. code-block:: xml

  <!-- YAML形式のテストデータ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-yaml</artifactId>
    <scope>test</scope>
  </dependency>

あわせて、テストデータを解析するコンポーネント\ ``testDataParser``\ を\ :java:extdoc:`YamlTestDataParser <nablarch.test.core.reader.YamlTestDataParser>`\ に差し替える。特殊記法を解釈するクラス（Interpreter）は、importした\ ``nablarch/test/test-data.xml``\ が\ Excel\ 形式用に定義している5つのうち、次の2つだけを\ ``interpreters``\ に指定する。

- ``dateTimeInterpreter``\ … ``${systemTime}``\ ・\ ``${updateTime}``\ ・\ ``${setUpTime}``\ を日時に変換する
- ``compositeInterpreter``\ … ``${文字種,文字数}``\ を、その文字種の文字列に変換する

残りの3つ（\ ``nullInterpreter``\ ・\ ``quotationTrimmer``\ ・\ ``lineSeparatorInterpreter``\ ）は、null・ダブルクォート・改行を\ Excel\ のセル値から読み取るためのもので、\ YAML\ では構文がその役割を担うため指定しない。

.. code-block:: xml

  <!-- テストデータを解析するコンポーネント -->
  <component name="testDataParser" class="nablarch.test.core.reader.YamlTestDataParser">
    <property name="dbInfo" ref="dbInfo"/>
    <property name="interpreters">
      <list>
        <component-ref name="dateTimeInterpreter"/>
        <component-ref name="compositeInterpreter"/>
      </list>
    </property>
  </component>

``testDataReader``\ は指定しない。\ :java:extdoc:`YamlTestDataParser <nablarch.test.core.reader.YamlTestDataParser>`\ は\ YAML\ ファイルを直接読み込むため、この設定を使用しない。

テストデータの読み込み先を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータは、デフォルトでは\ ``src/test/java``\ 配下から読み込まれる。プロジェクトのディレクトリ構成に合わせて読み込み先を変更する場合は、環境設定ファイルに\ ``nablarch.test.resource-root``\ を設定する。値には、テスト実行時のカレントディレクトリからの相対パスを指定する。

.. code-block:: properties

  nablarch.test.resource-root=path/to/test-data-dir

読み込み先は、セミコロン（\ ``;``\ ）で区切って複数指定できる。

.. code-block:: properties

  nablarch.test.resource-root=test/online;test/batch

.. important::

  同名のテストデータが複数のディレクトリに存在する場合、最初に見つかったものが読み込まれる。

システム日時を固定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
登録日時や更新日時のようにシステム日時を設定する項目は、そのままテストを実行すると実行日によって値が変わるため、設定値が正しいことを自動テストで確認できない。テスティングフレームワークは、システム日時として固定値を返す機能を提供する。この機能を使うと、システム日時を設定する項目についても、期待値と比較して設定値が正しいことを確認できる。

Nablarch Application Frameworkでは、\ :java:extdoc:`SystemTimeProvider <nablarch.core.date.SystemTimeProvider>`\ インタフェースの実装クラスがシステム日時を提供する。テストでは、コンポーネント設定ファイルでこの実装クラスを指定している箇所を、固定値を返す\ :java:extdoc:`FixedSystemTimeProvider <nablarch.test.FixedSystemTimeProvider>`\ に差し替え、\ ``fixedDate``\ プロパティに固定したい日時を指定する。システム日時を2010年9月14日12時34分56秒に固定する場合の例を示す。

.. code-block:: xml

  <component name="systemTimeProvider"
      class="nablarch.test.FixedSystemTimeProvider">
    <property name="fixedDate" value="20100914123456" />
  </component>

``fixedDate``\ には、\ ``yyyyMMddHHmmss``\ （14桁）または\ ``yyyyMMddHHmmssSSS``\ （17桁）のいずれかの形式に合致する文字列を指定する。この設定を行うと、テスト対象のアプリケーションが\ ``SystemTimeProvider``\ を通じて取得するシステム日時は、指定した日時に固定される。

シーケンス採番をテーブル採番に置き換える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
シーケンスオブジェクトを使用して採番する処理は、次に採番される値を事前に予測できないため、期待値を設定できない。テスティングフレームワークは、シーケンスオブジェクトを使用した採番処理を、コンポーネント設定ファイルの変更だけでテーブル採番に置き換える機能を提供する。テーブル採番に置き換えたうえで、採番用テーブルに準備データを投入し、投入した値を元に期待値を設定することで、採番処理が正しく行われていることを確認できる。

本番用のコンポーネント設定ファイルに、次のようなシーケンスオブジェクトを使用した採番の設定があるとする。

.. code-block:: xml

  <!-- シーケンスオブジェクトを使用した採番設定 -->
  <component name="idGenerator" class="com.example.common.idgenerator.OracleSequenceIdGenerator">
    <property name="idTable">
      <map>
        <entry key="1101" value="SEQ_1"/> <!-- ID1採番用 -->
        <entry key="1102" value="SEQ_2"/> <!-- ID2採番用 -->
        <entry key="1103" value="SEQ_3"/> <!-- ID3採番用 -->
        <entry key="1104" value="SEQ_4"/> <!-- ID4採番用 -->
      </map>
    </property>
  </component>

テスト用のコンポーネント設定ファイルでは、この設定をテーブル採番の設定で上書きする。

.. code-block:: xml

  <!-- シーケンスオブジェクトの採番設定をテーブルを使用した採番設定に置き換える -->
  <component name="idGenerator" class="nablarch.common.idgenerator.FastTableIdGenerator">
    <property name="tableName" value="TEST_SBN_TBL"/>
    <property name="idColumnName" value="ID_COL"/>
    <property name="noColumnName" value="NO_COL"/>
    <property name="dbTransactionManager" ref="dbTransactionManager"/>
  </component>

各プロパティの意味は、\ :java:extdoc:`FastTableIdGenerator <nablarch.common.idgenerator.FastTableIdGenerator>`\ を参照。

採番用テーブルの準備データと期待値の記述例は、\ :ref:`テーブルのデータを記述する <testdata_examples-table_data>`\ を参照。
