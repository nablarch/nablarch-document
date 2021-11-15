
======================================
使用するRDBMSの変更手順
======================================

.. contents:: 目次
  :depth: 2
  :local:

Nablarchのアーキタイプを利用して作成したプロジェクトは、 **初期状態ではH2 Database Engine** (以下H2)を使用するように設定されている。

別のRDBMSを使用するように設定変更する手順を記述する。


前提
===========================

以下を前提とする。

* 各アーキタイプから生成した直後のプロジェクトを対象とする。
* RDBMSには、接続に使用するユーザや、スキーマが作成済みであること。また、RDBMS上のユーザには適切な権限が付与済みであること。


.. _customizeDBAddFileMavenRepo:

Mavenリポジトリへのファイル登録
==========================================

---------------------------
JDBCドライバの登録
---------------------------

使用するJDBCドライバについては、以下のいずれかを満たす必要がある。

* Mavenのセントラルリポジトリに登録されている。
* プロジェクトのMavenリポジトリに登録されている。
* ローカルのMavenリポジトリに登録されている。


ここでは、Mavenのセントラルリポジトリに公開されていないJDBCドライバについて、ローカルのMavenリポジトリにJDBCドライバを登録する方法を説明する。手順中のドライバのバージョンについては適宜読み替えること。

.. important::
  * JDBCドライバはCI環境構築までに、プロジェクトのMavenリポジトリに登録することを強く推奨する。
  * 以降でJDBCドライバの入手方法についても説明する。JDBCドライバを入手する際には、ライセンスを確認した上で入手すること。

H2
------

H2の場合、JDBCドライバはMavenのセントラルリポジトリに公開されているため登録は不要である。


Oracle
------

Oracleの場合、JDBCドライバはMavenのセントラルリポジトリに公開されているため登録は不要である。


PostgreSQL
------------------

PostgreSQLの場合、JDBCドライバはMavenのセントラルリポジトリに公開されているため登録は不要である。


DB2
------------------

DB2のJDBCドライバはMavenのセントラルリポジトリに公開されていないため、ローカルのMavenリポジトリに登録する必要がある。

JDBCドライバをWebから取得する場合は、以下のサイトから入手する。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 6,10


  * - 配布サイトの名前
    - URL

  * - IBM DB2 JDBC Driver Versions |br|
      and Downloads - Japan
    - http://www-01.ibm.com/support/docview.wss?uid=swg21363866 (外部サイト、英語)

以下に、入手したJDBCドライバをローカルのMavenリポジトリに登録するコマンドの例を示す。

.. code-block:: bash

    mvn install:install-file -DgroupId=com.ibm -DartifactId=db2jcc4 -Dversion=10.5.0.7 -Dpackaging=jar -Dfile=db2jcc4.jar


SQLServer
------------------

SQLServerの場合、JDBCドライバはMavenのセントラルリポジトリに公開されているため登録は不要である。


.. _customizeDBNotExistPjRepo:

ファイル修正
===========================

---------------------------
propertiesファイルの修正
---------------------------

env.properties内の以下の箇所を修正する。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 5,4,10


  * - プロパティ名 
    - 説明
    - 使用するプロジェクト/モジュール
  * - nablarch.connectionFactory. |br|
      jndiResourceName
    - JNDIでDataSourceを取得する際のリソース名
    - * 各アーキタイプから生成したプロジェクト |br|
        (JNDIからコネクションを取得する環境のpropertiesファイル(後述)に設定)
  * - nablarch.db.jdbcDriver
    - JDBCドライバのクラス名
    - * 各アーキタイプから生成したプロジェクト |br|
        (ローカルにコネクションプールを作成する環境のpropertiesファイル(後述)に設定)
  * - nablarch.db.url
    - データベースの接続URL
    - * 各アーキタイプから生成したプロジェクト |br|
        (ローカルにコネクションプールを作成する環境のpropertiesファイル(後述)に設定)
  * - nablarch.db.user
    - データベースアクセスユーザ名
    - * 各アーキタイプから生成したプロジェクト |br|
        (ローカルにコネクションプールを作成する環境のpropertiesファイル(後述)に設定)
  * - nablarch.db.password
    - データベースアクセスユーザのパスワード
    - * 各アーキタイプから生成したプロジェクト |br|
        (ローカルにコネクションプールを作成する環境のpropertiesファイル(後述)に設定)
  * - nablarch.db.schema
    - 接続するスキーマ名
    - * Nablarchのテスティングフレームワーク



アーキタイプからプロジェクトを生成した直後は、「JNDIからコネクションを取得する環境のpropertiesファイル」に以下が該当する。


.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,6

  * - プロジェクト種別
    - JNDIからコネクションを取得する環境のpropertiesファイル
  * - * ウェブ
      * RESTfulウェブサービス
    - * 本番環境用properties(src/env/prod/resources/env.properties)
  * - * JSR352に準拠したバッチ
      * Nablarchバッチ
      * コンテナ版ウェブ
      * コンテナ版RESTfulウェブサービス
      * コンテナ版Nablarchバッチ
    - なし

アーキタイプからプロジェクトを生成した直後は、「ローカルにコネクションプールを作成する環境のpropertiesファイル」に以下が該当する。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,6

  * - プロジェクト種別
    - ローカルにコネクションプールを作成する環境のpropertiesファイル
  * - * ウェブ
      * RESTfulウェブサービス
    - * 単体試験環境(打鍵テスト)用properties(src/env/dev/resources/env.properties)
  * - * JSR352に準拠したバッチ
      * Nablarchバッチ
    - * 単体試験環境(打鍵テスト)用properties(src/env/dev/resources/env.properties)
      * 本番環境用properties(src/env/prod/resources/env.properties)
  * - * コンテナ版ウェブ
      * コンテナ版RESTfulウェブサービス
      * コンテナ版Nablarchバッチ
    - * src/main/resources/env.properties :ref:`※解説 <container_production_config>`


以下に、ローカルにコネクションプールを作成する環境のpropertiesファイル設定例を示す。

H2の設定例(デフォルト)
----------------------

.. code-block:: text

    nablarch.db.jdbcDriver=org.h2.Driver
    nablarch.db.url=jdbc:h2:./h2/db/SAMPLE
    nablarch.db.user=SAMPLE
    nablarch.db.password=SAMPLE
    nablarch.db.schema=PUBLIC


Oracleの設定例
--------------

.. code-block:: text

    nablarch.db.jdbcDriver=oracle.jdbc.driver.OracleDriver
    # jdbc:oracle:thin:@ホスト名:ポート番号:データベースのSID
    nablarch.db.url=jdbc:oracle:thin:@localhost:1521/xe
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


PostgreSQLの設定例
------------------

.. code-block:: text

    nablarch.db.jdbcDriver=org.postgresql.Driver
    # jdbc:postgresql://ホスト名:ポート番号/データベース名
    nablarch.db.url=jdbc:postgresql://localhost:5432/postgres
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


DB2の設定例
-----------

.. code-block:: text

    nablarch.db.jdbcDriver=com.ibm.db2.jcc.DB2Driver
    # jdbc:db2://ホスト名:ポート番号/データベース名
    nablarch.db.url=jdbc:db2://localhost:50000/SAMPLE
    nablarch.db.user=sample
    nablarch.db.password=sample
    nablarch.db.schema=sample


SQL Serverの設定例
------------------

.. code-block:: text

    nablarch.db.jdbcDriver=com.microsoft.sqlserver.jdbc.SQLServerDriver
    # jdbc:sqlserver://ホスト名:ポート番号;instanceName=インスタンス名
    nablarch.db.url=jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS
    nablarch.db.user=SAMPLE
    nablarch.db.password=SAMPLE
    nablarch.db.schema=SAMPLE


.. important::
  DBによっては、ユーザ名、パスワード、スキーマの大文字小文字を区別する。
  
  DBに設定した通りに、propertiesファイルにも設定すること。
  

.. _container_production_config:

コンテナの本番環境設定
-----------------------

コンテナ用のプロジェクトでは、プロファイルによる環境設定の切り替えは行わない。
代わりに、アプリケーションを動かす環境のOS環境変数を使って、 ``env.properties`` に宣言した設定値を上書きする。

したがって、OS環境変数を設定していない環境では ``src/main/resources/env.properties`` に書かれた設定がそのまま使用される。
本番等のコンテナ環境で動かすときは、OS環境変数を使って ``nablarch.db.url`` などの環境依存値を適切に上書きしなければならない。

OS環境変数で設定を上書きする方法については、 :ref:`repository-overwrite_environment_configuration_by_os_env_var` を参照。

また、プロファイルではなくOS環境変数で設定を切り替えるようにしている理由については、 `The Twelve-Factor App の III. 設定 <https://12factor.net/ja/config>`_ (外部サイト)を参照。

.. _customizeDB_pom_dependencies:

---------------------------
pom.xmlファイルの修正
---------------------------

.. _customizeDBProfiles:

(本番環境でJNDIからコネクションを取得するプロジェクトの場合)profiles要素内
-----------------------------------------------------------------------------------

profiles要素内で、JDBCドライバの依存関係が記述されている箇所を修正する。


.. tip::

  本番環境でJNDIからコネクションを取得するプロジェクトの場合、ローカルでコネクションプールを作るときだけ明示的に依存関係に入れる必要があるので、profiles要素内に記載されている。

  (JNDIからコネクションを取得する場合は、APサーバのクラスローダから、JDBCドライバを取得できるはずである。)


以下、データベース毎の設定例を記述する。

H2の設定例(デフォルト)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- 中略 -->
    <profile>
      <!-- 中略 -->
      <dependencies>
        <!-- 中略 -->
        <dependency>
          <groupId>com.h2database</groupId>
          <artifactId>h2</artifactId>
          <version>1.4.191</version>
          <scope>runtime</scope>
        </dependency>
        <!-- 中略 -->
      </dependencies>
    </profile>


Oracleの設定例
^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- 中略 -->
    <profile>
      <!-- 中略 -->
      <dependencies>
        <!-- 中略 -->
        <dependency>
          <groupId>com.oracle.database.jdbc</groupId>
          <artifactId>ojdbc6</artifactId>
          <version>11.2.0.4</version>
          <scope>runtime</scope>
        </dependency>
        <!-- 中略 -->
      </dependencies>
    </profile>


PostgreSQLの設定例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- 中略 -->
    <profile>
      <!-- 中略 -->
      <dependencies>
        <!-- 中略 -->
        <dependency>
          <groupId>org.postgresql</groupId>
          <artifactId>postgresql</artifactId>
          <version>9.4.1207</version>
          <scope>runtime</scope>
        </dependency>
        <!-- 中略 -->
      </dependencies>
    </profile>


DB2の設定例
^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- 中略 -->
    <profile>
      <!-- 中略 -->
      <dependencies>
        <!-- 中略 -->
        <dependency>
          <groupId>com.ibm</groupId>
          <artifactId>db2jcc4</artifactId>
          <version>10.5.0.7</version>
          <scope>runtime</scope>
        </dependency>
        <!-- 中略 -->
      </dependencies>
    </profile>


SQLServerの設定例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

  <profiles>
    <!-- 中略 -->
    <profile>
      <!-- 中略 -->
      <dependencies>
        <!-- 中略 -->
        <dependency>
          <groupId>com.microsoft.sqlserver</groupId>
          <artifactId>mssql-jdbc</artifactId>
          <version>7.4.1.jre8</version>
          <scope>runtime</scope>
        </dependency>
        <!-- 中略 -->
      </dependencies>
    </profile>


.. _customizeDBDependencyManagement:


(本番環境でローカルにコネクションプールを作成するプロジェクトの場合)dependencies要素内
---------------------------------------------------------------------------------------------

dependencies要素内で、JDBCドライバの依存関係が記述されている箇所を修正する。

デフォルトで記述されているdependency要素の例を示す。


.. code-block:: xml

  <dependencies>
    <!-- TODO: プロジェクトで使用するDB製品にあわせたJDBCドライバに修正してください。 -->
    <!-- 中略 -->
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <version>1.4.191</version>
      <scope>runtime</scope>
    </dependency>
    <!-- 中略 -->
  </dependencies>

dependency要素内の各要素については、:ref:`customizeDBProfiles` と同じ記述を行う。


.. _customizeDBWebComponentConfiguration:

------------------------------------------------------------------------------------------------------------
(本番環境でJNDIからコネクションを取得するプロジェクトの場合)コンポーネント設定ファイル (src/main/resources/)
------------------------------------------------------------------------------------------------------------

本番環境でJNDIからコネクションを取得するプロジェクトの場合、src/main/resourcesに配置しているコンポーネント設定ファイルにプロジェクトが使用するデータベースのDialectクラスが定義されている。
各プロジェクトのコンポーネント設定ファイル名は以下となる。

.. list-table::
   :widths: 10 10
   :header-rows: 1
   
   * - プロジェクト種別
     - コンポーネント設定ファイル名
   * - ウェブ
     - web-component-configuration.xml
   * - RESTfulウェブサービス
     - rest-component-configuration.xml

上記ファイルの以下の設定を変更する。

.. code-block:: xml

    <!-- ダイアレクト設定 -->
    <!-- 使用するDBに合わせてダイアレクトを設定すること -->
    <component name="dialect" class="nablarch.core.db.dialect.H2Dialect" />


Nablarchには以下のDialectクラスが用意されている。使用するデータベースに対応したDialectクラスに修正すること。

.. list-table::
   :widths: 10 10
   :header-rows: 1

   * - データベース
     - Dialectクラス
   * - Oracle 
     - nablarch.core.db.dialect.OracleDialect
   * - PostgreSQL
     - nablarch.core.db.dialect.PostgreSQLDialect
   * - DB2
     - nablarch.core.db.dialect.DB2Dialect
   * - SQL Server
     - nablarch.core.db.dialect.SqlServerDialect



---------------------------------------------------------------------------------------------------------------------
(本番環境でローカルにコネクションプールを作成するプロジェクトの場合)data-source.xml  (src/main/resources/)
---------------------------------------------------------------------------------------------------------------------

本番環境でローカルにコネクションプールを作成するプロジェクトの場合、data-source.xmlにプロジェクトが使用するデータベースのDialectクラスが記述されている。

このDialectクラスを、使用するデータベースに対応したDialectクラスに修正する。

使用するDialectクラスは、:ref:`customizeDBWebComponentConfiguration` と同一である。


-------------------------------------------
unit-test.xml  (src/test/resources)
-------------------------------------------

テスティングフレームワークが使用するデータベースの設定が記述されている。

デフォルトは以下のように汎用のDB設定になっている。

Oracleを使用する場合は、記述を修正する。

.. code-block:: xml
    
  <!-- TODO: 使用するDBに合せて設定してください。 -->
  <!-- Oracle用の設定 -->
  <!--
    <import file="nablarch/test/test-db-info-oracle.xml"/>
  -->
  <!-- 汎用のDB設定 -->
  <component name="dbInfo" class="nablarch.test.core.db.GenericJdbcDbInfo">
    <property name="dataSource" ref="dataSource"/>
    <property name="schema" value="${nablarch.db.schema}"/>
  </component>

Nablarchが使用するテーブル作成とデータの投入
============================================

----------------------------
テーブル作成
----------------------------

各プロジェクトの以下のディレクトリに、RDBMS別にDDLを用意している。
このDDLを実行することで、Nablarchが使用するテーブルの作成ができる。

* db/ddl/


.. tip::

  DB2の場合、create.sqlの先頭に接続先データベースと、使用スキーマが記述されているので書きかえてからDDLを実行する。

  DDLの実行は、「DB2 コマンド・ウィンドウ」上で以下を実行する。

  .. code-block:: text

    db2 -tvf "C:\develop\myapp-web\db\ddl\db2\create.sql"


.. tip::

    gsp-dba-maven-plugin\ [#gsp]_\ 使用時は、以下のコマンドでgsp-dba-maven-pluginを実行すればテーブルが作成される。

    .. code-block:: bash

      mvn -P gsp clean generate-resources


.. [#gsp]

  gsp-dba-maven-pluginを使用するためには、別途設定が必要である。

  設定については :doc:`addin_gsp` を参照。


----------------------------
データの投入
----------------------------

各プロジェクトの以下のディレクトリに、データのInsert文を用意している。
このInsert文を実行することで、Nablarchが使用するデータのInsertができる。

* db/data/

.. tip::

  DB2の場合、data.sqlの先頭に接続先データベースと使用スキーマを記述してから、SQLを実行する。

  以下に接続先データベースと使用スキーマの記述例を示す。

  .. code-block:: text
  
    CONNECT TO SAMPLE2;
    SET SCHEMA sample;

  DDLの実行は、「DB2 コマンド・ウィンドウ」上で以下を実行する。

  .. code-block:: text

    db2 -tvf "C:\develop\myapp-web\db\data\data.sql"


動作確認
==========================================

以下の手順を参照し、動作確認を行う。

* :ref:`ウェブの疎通確認<firstStepWebStartupTest>`
* :ref:`RESTfulウェブサービスの疎通確認<firstStepWebServiceStartupTest>`
* :ref:`JSR352に準拠したバッチの疎通確認<firstStepBatchEEStartupTest>`
* :ref:`Nablarchバッチの疎通確認<firstStepBatchStartupTest>`
* :ref:`コンテナ用ウェブの疎通確認<firstStepContainerWebStartupTest>`
* :ref:`コンテナ用RESTfulウェブサービスの疎通確認<firstStepContainerWebServiceStartupTest>`
* :ref:`コンテナ用Nablarchバッチの疎通確認<firstStepContainerBatchStartupTest>`


.. |br| raw:: html

  <br />