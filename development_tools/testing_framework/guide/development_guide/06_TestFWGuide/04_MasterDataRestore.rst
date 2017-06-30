.. _`master_data_backup`:

======================
 マスタデータ復旧機能
======================

.. contents:: 目次
  :depth: 2
  :local:

概要
====

通常の場合、テスト行う際にマスタデータを書き換えることはない。
しかし、マスタメンテナンス機能等のテストでは、マスタデータを変更しないと
実施できないテストケースが存在する。例えば、存在するはずのデータが存在しなかった場合のような
異常系テストケースでは、マスタデータからレコードを削除する必要がある。

テスト中にマスタデータの変更を行った場合、それ以降のテストクラスのテストでは、
マスタデータが意図しない状態になっている為にテストが失敗することがある。


このような、マスタデータ変更による意図しないテスト失敗を防止するため、
自動テスト中にマスタデータが更新された場合、そのテストメソッドが終了した時点で、
マスタデータを元の状態に復旧する機能を提供する。


特徴
====

* テストの実行順序に依存せずに、常に正しい状態のマスタデータでテストできる。
* マスタデータ復旧は自動で行われるので、各テストクラスで復旧処理、復旧用データを用意する必要ない。
* バックアップ用スキーマからテーブル毎に一括で復旧するので、1件ずつINSERTする場合に比べて高速に復旧できる。


必要となるスキーマ
==================

本機能を使用するにあたり、以下の二つのスキーマが必要となる。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 2,6


  * - スキーマ
    - 説明

  * - 自動テスト用スキーマ
    - 自動テストに使用するスキーマ。

  * - バックアップ用スキーマ
    - 復旧に使用するためのマスタデータを保存しておくためのスキーマ。


動作イメージ
============

自動テストフレームワークはコンポーネント設定ファイルより、監視対象テーブル名一覧を取得する。
テスト実行中、自動テストフレームワークはSQLログを監視することにより、\
監視対象テーブルを変更するSQL文が発行されたかどうかを検出する。


.. image:: _images/modification_detected.png

監視対象テーブルを変更するSQL文が発行された場合、テストメソッド終了後に変更があったテーブルを復旧する。
テーブルを復旧する際、いったんテーブル内のレコードを全件削除する。
その後、バックアップ用スキーマのテーブルからレコードを全件挿入する。

.. image:: _images/copy_from_backup.png

.. _`master_data_backup_settings`:

環境構築
========

以下の環境構築を実施し、自動テストフレームワークのマスタデータ復旧機能を有効にする。



バックアップ用スキーマの作成、データ投入
----------------------------------------

マスタデータ復旧用スキーマを作成する。
マスタデータ復旧用スキーマに自動テスト用のスキーマと同じテーブルを作成し復旧用のデータを投入しておく。

.. tip::
  マスタデータ復旧用スキーマには全てのテーブルを作成する必要はない。
  マスタデータ復旧対象とするテーブルのみ存在すればよい（復旧対象以外のテーブルがあっても問題ない）。



コンポーネント設定ファイルに監視対象テーブルを記載
-----------------------------------------------------------

自動テスト用のコンポーネント設定ファイルに、監視対象テーブルを列挙する。


設定項目一覧
~~~~~~~~~~~~

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 3,7,2


  * - 設定項目名
    - 説明
    - デフォルト値

  * - backupSchema
    - マスタデータ復旧用スキーマ名を記載する。
    - なし

  * - tablesTobeWatched
    - 監視対象とするテーブル名をリスト形式で列挙する。
    - なし

  * - testEventListeners
    - テストイベントリスナーの一覧。
      ここにマスタデータ復旧クラス(nablarch.test.core.db.MasterDataRestorer)を登録することで、
      テストメソッド終了時にマスタデータが行われるようになる。
    - なし


設定例
~~~~~~

.. code-block:: xml

  <!-- マスタデータ復旧クラス -->
  <component name="masterDataRestorer"
             class="nablarch.test.core.db.MasterDataRestorer">
    <!-- バックアップスキーマ -->
    <property name="backupSchema" value="nablarch_test_master"/>
    <!-- 監視対象テーブル一覧 -->
    <property name="tablesTobeWatched">
      <list>
        <value>MESSAGE</value>
        <value>ID_GENERATE</value>
        <value>BUSINESS_DATE</value>
        <value>PERMISSION_UNIT</value>
        <value>REQUEST</value>
        <value>PERMISSION_UNIT_REQUEST</value>
      </list>
    </property>
  </component>


ログ出力設定
------------

本機能ではSQLログを監視することにより、マスタデータへの変更を検出する。\
よって、そのためのログ出力が必要である。


app-log.properties
~~~~~~~~~~~~~~~~~~

`sqlLogFormatter`\ のクラス名に、本機能の提供クラスを指定する。

.. code-block:: none

 sqlLogFormatter.className=nablarch.test.core.db.MasterDataRestorer$SqlLogWatchingFormatter


log.properties
~~~~~~~~~~~~~~

log.propertiesにSQLログをデバッグレベル以上で出力する設定をする。
以下の例では、SQLログを標準出力に表示させないよう専用のロガー（何もしないロガー）を
設定している

.. code-block:: none

 # ロガーファクトリ実装クラス								 
 loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory			 
 											 
 # ログライター名									 
 writerNames=stdout,nop									 
 											 
 #デバッグ用の標準出力									 
 writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter			 
 writer.nop.className=nablarch.test.core.log.NopLogWriter   # 【説明】何もしないロガー	 
 											 
 # 利用可能なロガー名順序								 
 availableLoggersNamesOrder=sql,root							 
 											 
 #全てのロガー取得を対象に、DEBUGレベル以上を標準出力に出力する。			 
 loggers.root.nameRegex=.*								 
 loggers.root.level=DEBUG								 
 loggers.root.writerNames=stdout								 
 											 
 #ロガー名に"SQL"を指定したロガー取得を対象に、DEBUGレベル以上を出力する。		 
 loggers.sql.nameRegex=SQL								 
 loggers.sql.level=DEBUG      # 【説明】DEBUGレベル以上に設定すること			 
 loggers.sql.writerNames=nop                                                              
