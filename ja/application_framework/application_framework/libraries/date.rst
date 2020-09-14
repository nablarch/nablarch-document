日付管理
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

アプリケーションで使用するシステム日時(OS日時)と業務日付を一元的に管理する機能を提供する。

機能概要
--------------------------

システム日時(OS日時)と業務日付の切り替えができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、コンポーネント定義で指定されたクラスを使用して、システム日時(OS日時)や業務日付を取得する。
そのため、コンポーネント定義で指定するクラスを差し替えるだけで、
アプリケーションで使用するシステム日時(OS日時)と業務日付の取得方法を切り替えることができる。
この切り替えは、テストなどで一時的にシステム日時(OS日時)や業務日付を切り替えたい場合に使用できる。

* :ref:`date-system_time_change`
* :ref:`date-business_date_change`

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

  <!-- 業務日付管理機能を使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _date-system_time_settings:

システム日時の管理機能を使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システム日時の管理機能を使うためには、
:java:extdoc:`BasicSystemTimeProvider <nablarch.core.date.BasicSystemTimeProvider>` の設定をコンポーネント定義に追加する。
コンポーネント名には **systemTimeProvider** と指定する。

.. code-block:: xml

 <component name="systemTimeProvider" class="nablarch.core.date.BasicSystemTimeProvider" />

システム日時を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システム日時の取得は、 :java:extdoc:`SystemTimeUtil <nablarch.core.date.SystemTimeUtil>` を使用する。

.. _date-business_date_settings:

業務日付管理機能を使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
業務日付管理機能では、データベースを使用して複数の業務日付を管理する。
テーブルのレイアウトは以下となる。

================ ===================================================
区分(PK)         業務日付を識別するための値。文字列型
日付             業務日付。文字列型で値はyyyyMMdd形式
================ ===================================================

業務日付管理機能を使うためには、
:java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` の設定をコンポーネント定義に追加する。
コンポーネント名には **businessDateProvider** と指定する。

.. code-block:: xml

 <component name="businessDateProvider" class="nablarch.core.date.BasicBusinessDateProvider">
   <!-- テーブル名 -->
   <property name="tableName" value="BUSINESS_DATE" />
   <!-- 区分のカラム名 -->
   <property name="segmentColumnName" value="SEGMENT"/>
   <!-- 日付のカラム名 -->
   <property name="dateColumnName" value="BIZ_DATE"/>
   <!-- 区分を省略して業務日付を取得した場合に使用される区分 -->
   <property name="defaultSegment" value="00"/>
   <!-- データベースアクセスに使用するトランザクションマネージャ -->
   <property name="transactionManager" ref="transactionManager" />
 </component>

業務日付を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
業務日付の取得は、 :java:extdoc:`BusinessDateUtil <nablarch.core.date.BusinessDateUtil>` を使用する。

業務日付を任意の日付に上書く
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バッチ処理で障害時の再実行時に、過去日付をバッチ実行時の業務日付としたい場合がある。
このような場合に、再実行を行うプロセスのみ任意の日付を業務日付として実行することができる。

.. tip::
 ウェブアプリケーションのように、全ての機能が１プロセス内で実行される場合は、
 単純にデータベースで管理されている日付を変更すればよい。

業務日付の上書きは、 :ref:`repository-overwrite_environment_configuration` を使用して行う。
システムプロパティとして、以下の形式で指定を行う。

システムプロパティの形式
 BasicBusinessDateProvider.<区分>=日付

 ※日付はyyyyMMdd形式

システムプロパティの例
 区分が"batch"の日付を"2016/03/17"に上書きしたい場合

 -DBasicBusinessDateProvider.batch=20160317

業務日付を更新する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
業務日付の更新は、 :java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` を使用して行う。

.. code-block:: java

 // システムリポジトリからBasicBusinessDateProviderを取得する
 BusinessDateProvider provider = SystemRepository.get("businessDateProvider");

 // setDateメソッドを呼び出し、更新する
 provider.setDate(segment, date);

拡張例
--------------------------------------------------

.. _date-system_time_change:

システム日時を切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニットテストの実行時など、システム日時を切り替えたい場合は、以下の手順で行う。

1. :java:extdoc:`SystemTimeProvider <nablarch.core.date.SystemTimeProvider>` を実装したクラスを作成する。
2. :ref:`date-system_time_settings` に従い設定を行う。

.. _date-business_date_change:

業務日付を切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニットテストの実行時など、業務日付を切り替えたい場合は、以下の手順で行う。

1. :java:extdoc:`BusinessDateProvider <nablarch.core.date.BusinessDateProvider>` を実装したクラスを作成する。
2. :ref:`date-business_date_settings` に従い設定を行う。
