.. _fixed_time_and_id:

システム日時と採番の固定
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
システム日時とシーケンスオブジェクトによる採番は、実行のたびに値が変わるため、そのままでは期待値を書けない。テスティングフレームワークは、システム日時を固定値にする機能と、シーケンス採番をテーブル採番に置き換える機能を提供する。どちらもテストの種類によらず使える。登録日時・更新日時や採番したIDをテーブルの期待値に書くテストがあるなら、このページの設定を行う。

使用方法
--------------------------------------------------

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
