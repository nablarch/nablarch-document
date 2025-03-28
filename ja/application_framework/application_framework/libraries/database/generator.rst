.. _generator:

サロゲートキーの採番
====================

.. contents:: 目次
  :depth: 3
  :local:

データベースのサロゲートキー(代理キー)の値を採番するための機能を提供する。

この機能は、 :ref:`universal_dao` でサロゲートキーを採番(単純な連番を採番)する際に使用する。

なお、 :ref:`universal_dao` 以外でも使用できるが、
以下の理由によりアプリケーション側で対応することを推奨する。

理由
  サロゲートキーの採番処理は、 :ref:`universal_dao` が行うためアプリケーション側で直接採番機能を使用する必要が無い。
  それ以外の用途で値を採番する場合には、採番ルールが複雑であったり、採番した値を編集することが想定される。
  このような場合は、単純な連番を採番する本機能を使用できないため、アプリケーション側で設計、実装する必要がある。
  (本機能でも実現可能だが、設計及び実装(設定)が必要となるため、本機能を使うメリットは無い)

  例えば、親キーの中での連番を採番するケースでは、以下の手順にて値を採番できる。

  1. 親キーの毎に連番を採番するための専用テーブルを作成する。
  2. アプリケーションでは、親のキーが登録されたタイミングで専用テーブルにレコードを登録する。
  3. 採番が必要なタイミングで親キーに対応する採番済みの値をインクリメントすることで、親キー内での連番を採番できる。

機能概要
-------------
シーケンスを使った値の採番が出来る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベース上に作成されたシーケンスオブジェクトを使って、一意の値を採番出来る。

なお、シーケンスを使って次の値を取得するためのSQL文は、
データベースアクセス機能のダイアレクトを使用して構築する。

ダイアレクト機能については、 :ref:`ダイアレクト <database-dialect>` を参照。

テーブルを使った値の採番が出来る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テーブルのレコード単位に現在値を管理し、一意の値を採番出来る。

テーブルのレイアウトは以下のものを想定する。

================ ===================================================
採番識別名(PK)   採番対象を識別するための値

現在値           現在の値(採番を行うとこの値に1を加算したものが取得できる)
================ ===================================================

.. important::

  必要なレコードは予めセットアップしておくこと。
  採番実行時に、指定した採番識別名(PK)に対応するレコードが存在しない場合、
  新規にレコードを追加するのではなく、異常終了(例外を送出)する。


.. important::

  テーブルを使った採番は、大量にデータを処理するようなバッチ処理ではボトルネックとなることが多い。
  このため、テーブルを使った採番を使うのではなく、データベース側の採番カラムやシーケンスを用いた採番を使うことを強く推奨する。

  データベースの機能として、採番カラム及びシーケンスオブジェクトが使用できない場合のみ、テーブルを使った採番機能を使用すること。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------

.. _generator_dao_setting:

ユニバーサルDAO用に採番を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`universal_dao` で本機能を使用するためには、 :java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>` に対する設定が必要となる。

この例では、シーケンス採番とテーブル採番の両方を設定しているが、使用しない採番の設定はしなくてよい。
テーブル採番は推奨しないため、サロゲートキーの採番でシーケンス採番を使用する場合に `sequenceIdGenerator` を設定すれば良い。

もし、シーケンス採番を使用せずにデータベース側の採番機能(自動採番カラム)を使う場合には、採番の設定自体が不要となる。

.. code-block:: xml

  <!-- テーブル採番モジュールの設定 -->
  <component name="tableIdGenerator" class="nablarch.common.idgenerator.TableIdGenerator">
    <property name="tableName" value="GENERATOR" />
    <property name="idColumnName" value="ID" />
    <property name="noColumnName" value="NO" />
  </component>

  <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory">
    <!-- シーケンス採番の設定 -->
    <property name="sequenceIdGenerator">
      <component class="nablarch.common.idgenerator.SequenceIdGenerator"/>
    </property>

    <!-- テーブル採番の設定 -->
    <property name="tableIdGenerator" ref="tableIdGenerator" />

    <!-- 採番に関係のない設定は省略 -->
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- TableIdGeneratorは初期化が必要 -->
        <component-ref name="tableIdGenerator" />
      </list>
    </property>
  </component>

拡張例
--------------------------------------------------
テーブル採番やシーケンス採番を置き換える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テーブルやシーケンスを使った採番の実装を新しいものに置き換える場合には、
:java:extdoc:`IdGenerator <nablarch.common.idgenerator.IdGenerator>` を実装したクラスを作成することで対応できる。

作成したクラスは、 `ユニバーサルDAO用に採番を設定する`_ に従いコンポーネント設定ファイルに定義することで使用可能となる。

.. |br| raw:: html

  <br />
