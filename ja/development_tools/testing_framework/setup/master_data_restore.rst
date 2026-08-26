.. _master_data_restore:

マスタデータ復旧機能
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
マスタデータ復旧機能を使うと、テストの実行中に変更されたマスタデータを、テストメソッドの終了時に元の状態へ自動的に戻せる。マスタデータを変更するテストがあっても、後続のテストがその変更に影響されなくなる。

通常、テストを行う際にマスタデータを書き換えることはない。しかし、マスタメンテナンス機能等のテストでは、マスタデータを変更しないと実施できないテストがある。例えば、存在するはずのデータが存在しなかった場合のような異常系のテストでは、マスタデータからレコードを削除する必要がある。

テスト中にマスタデータを変更した場合、それ以降のテストクラスのテストでは、マスタデータが意図しない状態になっているためにテストが失敗することがある。マスタデータ復旧機能は、このような意図しないテスト失敗を防止するために、テスト中にマスタデータが更新された場合、そのテストメソッドが終了した時点でマスタデータを元の状態に復旧する。

マスタデータ復旧機能には次の特徴がある。

* テストの実行順序に依存せずに、常に正しい状態のマスタデータでテストできる。
* 復旧は自動で行われるので、テストクラスごとに復旧処理や復旧用のデータを用意する必要がない。
* バックアップ用スキーマからテーブル単位で一括してコピーするので、1件ずつ挿入する場合に比べて高速である。

マスタデータを復旧する流れ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークは、コンポーネント設定ファイルから監視対象テーブル名一覧を取得する。テストの実行中は、SQLログを監視することにより、監視対象テーブルを変更するSQL文が発行されたかどうかを検出する。

.. image:: images/master_data_restore/modification_detected.png

監視対象テーブルを変更するSQL文が発行された場合、テストメソッドの終了後に、変更があったテーブルを復旧する。復旧では、変更があったテーブルのレコードをすべて削除したうえで、あらかじめ用意しておいたバックアップ用スキーマの同じテーブルからレコードをすべて挿入する。

.. image:: images/master_data_restore/copy_from_backup.png

必要となるスキーマ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
マスタデータ復旧機能を使用するにあたり、次の2つのスキーマが必要となる。

.. list-table::
  :header-rows: 1
  :widths: 30,70

  * - スキーマ
    - 説明
  * - 自動テスト用スキーマ
    - 自動テストに使用するスキーマ
  * - バックアップ用スキーマ
    - 復旧に使用するためのマスタデータを保存しておくスキーマ

使用方法
--------------------------------------------------
マスタデータ復旧機能は、バックアップ用スキーマの作成・監視対象テーブルの登録・SQLログの出力設定の3つをすべて行うと有効になる。テーブルの依存関係の解析の抑止は、必要な場合にだけ行う。

.. _master_data_restore-backup_schema:

バックアップ用スキーマを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バックアップ用スキーマを作成する。自動テスト用スキーマと同じテーブルをバックアップ用スキーマにも作成し、復旧用のデータを投入しておく。

.. tip::

  バックアップ用スキーマには、すべてのテーブルを作成する必要はない。監視対象テーブルとして登録するテーブルのみ存在すればよい（それ以外のテーブルがあっても問題ない）。ただし\ :ref:`マスタデータ投入ツール <master_data_tool>`\ でバックアップ用スキーマにも投入する場合は、投入するマスタデータファイルに記述したすべてのテーブルがバックアップ用スキーマに必要である。このツールは、マスタデータファイルに記述されたテーブルをすべてバックアップ用スキーマへコピーするためである。

.. _master_data_restore-watched_tables:

監視対象テーブルを登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
自動テスト用のコンポーネント設定ファイルに、マスタデータ復旧クラス\ :java:extdoc:`MasterDataRestorer <nablarch.test.core.db.MasterDataRestorer>`\ を登録し、監視対象テーブルを列挙する。主な設定項目は次のとおりである。

.. list-table::
  :header-rows: 1
  :widths: 25,60,15

  * - 設定項目名
    - 説明
    - デフォルト値
  * - ``backupSchema``
    - バックアップ用スキーマ名
    - 該当なし
  * - ``tablesTobeWatched``
    - 監視対象とするテーブル名。リスト形式で列挙する
    - 該当なし

あわせて、登録したマスタデータ復旧クラスを、テストイベントリスナーの一覧（\ ``testEventListeners``\ ）にも追加する。テストメソッドの終了は、この一覧に登録されたクラスにだけ通知されるためである。記述例を示す。

.. code-block:: xml

  <!-- マスタデータ復旧クラス -->
  <component name="masterDataRestorer"
             class="nablarch.test.core.db.MasterDataRestorer">
    <!-- バックアップ用スキーマ -->
    <property name="backupSchema" value="NABLARCH_TEST_MASTER"/>
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

  <!-- テストイベントリスナー一覧 -->
  <list name="testEventListeners">
    <component class="nablarch.test.RepositoryInitializer"/>
    <component-ref name="masterDataRestorer"/>
  </list>

.. important::

  ``testEventListeners``\ への登録を省略すると、マスタデータ復旧クラスを定義していてもマスタデータの復旧は行われない。

  記述例に含めた\ :java:extdoc:`RepositoryInitializer <nablarch.test.RepositoryInitializer>`\ は、テストクラスの終了時にリポジトリを復元するクラスである。これもこの一覧に登録しないと復元が行われないため、マスタデータ復旧クラスとあわせて登録する。

SQLログを出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
マスタデータ復旧機能はSQLログを監視することにより、マスタデータへの変更を検出する。よって、そのためのログ出力が必要である。

``app-log.properties``\ には、\ ``sqlLogFormatter``\ のクラス名として、マスタデータ復旧機能が提供する\ ``SqlLogWatchingFormatter``\ を指定する。

.. code-block:: properties

  sqlLogFormatter.className=nablarch.test.core.db.MasterDataRestorer$SqlLogWatchingFormatter

``log.properties``\ には、SQLログをデバッグレベルで出力する設定をする。次の例では、SQLログを標準出力に表示させないよう、何も出力しないログライター\ :java:extdoc:`NopLogWriter <nablarch.test.core.log.NopLogWriter>`\ を設定している。

.. code-block:: properties

  # ロガーファクトリ実装クラス
  loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory

  # ログライター名
  writerNames=stdout,nop

  # デバッグ用の標準出力
  writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter
  # 何も出力しないログライター
  writer.nop.className=nablarch.test.core.log.NopLogWriter

  # 利用可能なロガー名順序
  availableLoggersNamesOrder=sql,root

  # すべてのロガー取得を対象に、DEBUGレベル以上を標準出力に出力する。
  loggers.root.nameRegex=.*
  loggers.root.level=DEBUG
  loggers.root.writerNames=stdout

  # ロガー名に"SQL"を指定したロガー取得を対象に、DEBUGレベル以上を出力する。
  loggers.sql.nameRegex=SQL
  loggers.sql.level=DEBUG
  loggers.sql.writerNames=nop

.. important::

  ``loggers.sql.level``\ には\ ``DEBUG``\ を指定する。\ ``INFO``\ 以上を指定するとSQLログが出力されず、マスタデータの変更を検出できない。

.. _master_data_restore-suppress_table_sort:

テーブルの依存関係の解析を抑止する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
外部キーが設定されたテーブルに対してデータを復旧する場合には、親子関係を意識して復旧処理を行う必要がある。このため、デフォルトでは、JDBCの機能を用いてテーブルの依存関係を解析し、削除処理は子テーブルから、挿入処理は親テーブルから順に行う。

しかし、テーブル数が膨大なプロジェクトの場合、依存関係の解析にかかる時間のためにテストの実行時間が長くなることがある。これを避けるために、依存関係の解析を行わず、\ :ref:`監視対象テーブルを登録する <master_data_restore-watched_tables>`\ で列挙した記述順をもとにテーブルの削除・挿入処理を行う動作も提供している。記述順をもとにマスタデータを復旧させたい場合には、環境設定ファイルに次の設定を追加する。

.. code-block:: properties

  nablarch.suppress-table-sort=true

.. important::

  この設定を行った場合、テーブルは\ ``tablesTobeWatched``\ に列挙した順に挿入され、その逆順に削除される。外部キーが設定されたテーブルを復旧するときは、親テーブルが子テーブルより先に来るように列挙する。

  この設定は、テスティングフレームワークが行うテーブルの依存関係の解析すべてに適用される。マスタデータの復旧だけでなく、準備データの投入や\ :ref:`master_data_tool`\ による投入の順序も、テーブルの記述順をもとに決まるようになる。
