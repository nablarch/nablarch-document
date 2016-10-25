=========================================================
gsp-dba-maven-plugin(DBA作業支援ツール)の初期設定方法
=========================================================

.. contents:: 目次
  :depth: 2
  :local:

概要
====================================================

`gsp-dba-maven-plugin(外部サイト) <https://github.com/coastland/gsp-dba-maven-plugin>`_ は、Apache License Version 2.0 ライセンスで提供されるオープンソースのツールである。

gsp-dba-maven-pluginは、利用開始前にRDBMSにあわせた設定を行う必要がある。

本手順では、アーキタイプから生成したプロジェクトで、gsp-dba-maven-pluginを使用するための設定方法を示す。

前提
====================================================

以下のプロジェクトを対象とする。

* アーキタイプから生成後、:doc:`CustomizeDB` の手順を実施した各種プロジェクト。

Mavenの設定
===============

gsp-dba-maven-pluginを使用するにあたって、3rd Party Repositoryの設定が必要である。

設定は、<ホームディレクトリ>/.m2/settings.xmlに行う。

.. code-block:: xml

  <settings>
    <!-- 中略 -->
    <profiles>
      <profile>
        <id>my-repository</id>
        <repository>
          <id>maven.seasar.org</id>
          <name>The Seasar Foundation Maven Repository</name>
          <url>http://maven.seasar.org/maven2</url>
          <snapshots>
            <enabled>false</enabled>
          </snapshots>
        </repository>
        <repository>
          <id>maven-snapshot.seasar.org</id>
          <name>The Seasar Foundation Maven Snapshot Repository</name>
          <url>http://maven.seasar.org/maven2-snapshot</url>
          <releases>
            <enabled>false</enabled>
          </releases>
          <snapshots>
            <enabled>true</enabled>
            <updatePolicy>always</updatePolicy>
          </snapshots>
        </repository>
      </profile>
    </profiles>
    <!-- 中略 -->
  </settings>

.. tip::

  gsp-dba-maven-pluginはデフォルトでH2 Database Engine(以下H2)を使うように設定されている。

  H2を使用する場合は、以降の手順は不要である。 :ref:`confirm_gsp` だけ行うこと。


ファイル修正
===========================


pom.xmlファイルの修正
---------------------------

properties要素内
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pom.xmlのpropertiesタグ内の以下の箇所を修正する。

=============================================== ===========================================
プロパティ名                                    説明                                       
=============================================== ===========================================
nablarch.db.jdbcDriver                          JDBCドライバのクラス名
nablarch.db.url                                 データベースの接続URL
nablarch.db.adminUser                           管理者ユーザー名                           
nablarch.db.adminPassword                       管理者ユーザーのパスワード                 
nablarch.db.user                                データベースアクセスユーザ名
nablarch.db.password                            データベースアクセスユーザのパスワード
nablarch.db.schema                              接続するスキーマ名
=============================================== ===========================================

以下に記述例を示す。

**Oracleの設定例**


.. code-block:: xml

    <nablarch.db.jdbcDriver>oracle.jdbc.driver.OracleDriver</nablarch.db.jdbcDriver>
    <!-- jdbc:oracle:thin:@ホスト名:ポート番号:データベースのSID -->
    <nablarch.db.url>jdbc:oracle:thin:@localhost:1521/xe</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>
    

**PostgreSQLの設定例**

.. code-block:: xml

    <nablarch.db.jdbcDriver>org.postgresql.Driver</nablarch.db.jdbcDriver>
    <!-- jdbc:postgresql://ホスト名:ポート番号/データベース名 -->
    <nablarch.db.url>jdbc:postgresql://localhost:5432/postgres</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


**DB2の設定例**

.. code-block:: xml

    <nablarch.db.jdbcDriver>com.ibm.db2.jcc.DB2Driver</nablarch.db.jdbcDriver>
    <!-- jdbc:db2://ホスト名:ポート番号/データベース名 -->
    <nablarch.db.url>jdbc:db2://localhost:50000/SAMPLE</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>
    

**SQLServerの設定例**


.. code-block:: xml

    <nablarch.db.jdbcDriver>com.microsoft.sqlserver.jdbc.SQLServerDriver</nablarch.db.jdbcDriver>
    <!-- jdbc:sqlserver://ホスト名:ポート番号;instanceName=インスタンス名 -->
    <nablarch.db.url>jdbc:sqlserver://localhost:1433;instanceName=SQLEXPRESS</nablarch.db.url>
    <nablarch.db.adminUser>SAMPLE</nablarch.db.adminUser>
    <nablarch.db.adminPassword>SAMPLE</nablarch.db.adminPassword>
    <nablarch.db.user>sample</nablarch.db.user>
    <nablarch.db.password>sample</nablarch.db.password>
    <nablarch.db.schema>sample</nablarch.db.schema>


build要素内
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

gsp-dba-maven-plugin使用時は、gsp-dba-maven-pluginで使用するJDBCドライバの設定を追加する。

以下に記述例を示す。


Oracleの設定例
^^^^^^^^^^^^^^

.. code-block:: xml

    <build>
      <plugins>
        <!-- 中略 -->
        <plugin>
          <groupId>jp.co.tis.gsp</groupId>
          <artifactId>gsp-dba-maven-plugin</artifactId>
          <dependencies>
            <dependency>
              <groupId>com.oracle</groupId>
              <artifactId>ojdbc6</artifactId>
              <version>11.2.0.2.0</version>
            </dependency>
          </dependencies>
        </plugin>
        <!-- 中略 -->
      </plugins>
    </build>


PostgreSQLの設定例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

    <build>
      <plugins>
        <!-- 中略 -->
        <plugin>
          <groupId>jp.co.tis.gsp</groupId>
          <artifactId>gsp-dba-maven-plugin</artifactId>
          <dependencies>
            <dependency>
              <groupId>org.postgresql</groupId>
              <artifactId>postgresql</artifactId>
              <version>9.4.1207</version>
            </dependency>
          </dependencies>
        </plugin>
        <!-- 中略 -->
      </plugins>
    </build>


DB2の設定例
^^^^^^^^^^^^^^

.. code-block:: xml

    <build>
      <plugins>
        <!-- 中略 -->
        <plugin>
          <groupId>jp.co.tis.gsp</groupId>
          <artifactId>gsp-dba-maven-plugin</artifactId>
          <dependencies>
            <dependency>
              <groupId>com.ibm</groupId>
              <artifactId>db2jcc4</artifactId>
              <version>10.5.0.7</version>
            </dependency>
          </dependencies>
        </plugin>
        <!-- 中略 -->
      </plugins>
    </build>


SQLServerの設定例
^^^^^^^^^^^^^^^^^

.. code-block:: xml

    <build>
      <plugins>
        <!-- 中略 -->
        <plugin>
          <groupId>jp.co.tis.gsp</groupId>
          <artifactId>gsp-dba-maven-plugin</artifactId>
          <dependencies>
            <dependency>
              <groupId>com.microsoft</groupId>
              <artifactId>sqljdbc4</artifactId>
              <version>4.0</version>
            </dependency>
          </dependencies>
        </plugin>
        <!-- 中略 -->
      </plugins>
    </build>


data-model.edm  (src/main/resources/entity)の準備
-------------------------------------------------

src/main/resources/entity以下にRDBMS毎にedmファイルが存在するので、使用するRDBMSに対応するファイルを「data-model.edm」にリネームする。

.. _confirm_gsp:

動作確認
===========================

.. important::

  DBのデータが削除されるため、必要であれば現在DBに格納されているデータを退避しておくこと。


**1.以下のコマンドを実行して、DDLの生成からダンプファイル作成までを行う。**

.. code-block:: bash

  mvn -P gsp clean generate-resources

.. tip ::

  以下のゴールが実行されるように、各アーキタイプから生成したプロジェクトのpom.xmlに記述されている。

  * generate-ddl
  * execute-ddl
  * load-data
  * export-schema


成功すると以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] --- gsp-dba-maven-plugin:3.2.0:export-schema (default-cli) @ myapp-web ---
  [INFO] PUBLICスキーマのExportを開始します。:C:\develop\myapp\myapp-web\gsp-target\output\PUBLIC.dmp
  [INFO] Building jar: C:\develop\myapp-web\gsp-target\output\myapp-web-testdata-0.1.0.jar
  [INFO] PUBLICスキーマのExport完了
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 5.415 s
  [INFO] Finished at: 2016-05-11T21:17:03+09:00
  [INFO] Final Memory: 13M/31M
  [INFO] ------------------------------------------------------------------------


また、 ``gsp-target/output/`` ディレクトリにダンプファイルが格納されたjarファイルが生成される。

.. tip::

  実行に失敗する場合は、RDBMS固有の制限事項に抵触していないか確認する。
  
  RDBMS固有の制限事項については、https://github.com/coastland/gsp-dba-maven-plugin (外部サイト)の「ゴール共通のパラメータ」を参照。


**2.以下のコマンドを実行して、ダンプファイルをローカルリポジトリへインストールする。**

.. code-block:: bash

  mvn -P gsp install:install-file


成功すると以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] --- maven-install-plugin:2.5.2:install-file (default-cli) @ myapp-web ---
  [INFO] pom.xml not found in myapp-web-testdata-0.1.0.jar
  [INFO] Installing C:\develop\myapp-web\gsp-target\output\myapp-web-testdata-0.1.0.jar to C:\Users\TISxxxxxx\.m2\repository\com\example\myapp-web-testdata\0.1.0\myapp-web-testdata-0.1.0.jar
  [INFO] Installing C:\Users\TISxxx~1\AppData\Local\Temp\mvninstall7441010390688212345.pom to C:\Users\TISxxxxxx\.m2\repository\com\example\myapp-web-testdata\0.1.0\myapp-web-testdata-0.1.0.pom
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 1.077 s
  [INFO] Finished at: 2016-05-12T14:37:39+09:00
  [INFO] Final Memory: 8M/20M
  [INFO] ------------------------------------------------------------------------



**3.以下のコマンドを実行して、ダンプファイルをインポートする。**

.. code-block:: bash

  mvn -P gsp gsp-dba:import-schema


成功すると以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] スキーマのインポートを開始します。:C:\develop\myapp-web\gsp-target\output\PUBLIC.dmp
  [INFO] スキーマのインポートを終了しました
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  [INFO] Total time: 2.584 s
  [INFO] Finished at: 2016-05-12T14:49:58+09:00
  [INFO] Final Memory: 9M/23M
  [INFO] ------------------------------------------------------------------------
