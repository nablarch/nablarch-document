.. _database_connection_management_handler:

データベース接続管理ハンドラ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

後続のハンドラ及びライブラリで使用するためのデータベース接続を、スレッド上で管理するハンドラ。

データベースアクセスの詳細は、 :ref:`database` を参照。

.. important::

  このハンドラを使用する場合は、 :ref:`transaction_management_handler` をセットで設定すること。
  トランザクション制御ハンドラが設定されていない場合、トランザクション制御が実施されないため後続で行ったデータベースへの変更は全て破棄される。

本ハンドラでは、以下の処理を行う。

* データベース接続の取得
* データベース接続の解放

処理の流れは以下のとおり。

.. image:: ../images/DbConnectionManagementHandler/DbConnectionManagementHandler_flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.DbConnectionManagementHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

制約
------------------------------
なし。

データベースの接続先の設定を行う
--------------------------------------------------
このハンドラは、 :java:extdoc:`connectionFactory <nablarch.common.handler.DbConnectionManagementHandler.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>`
プロパティに設定されたファクトリクラス( :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 実装クラス )を使用してデータベース接続を取得する。

以下の設定ファイル例を参考にし、  :java:extdoc:`connectionFactory <nablarch.common.handler.DbConnectionManagementHandler.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>`
プロパティにファクトリクラスを設定すること。

.. code-block:: xml

  <!-- データベース接続管理ハンドラ -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <property name="connectionFactory" ref="connectionFactory" />
  </component>

  <!-- データベース接続オブジェクトを取得するファクトリクラスの設定 -->
  <component name="connectionFactory"
      class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
    <!-- プロパティの設定は省略 -->
  </component>

.. important::

  データベース接続オブジェクトを取得するためのファクトリクラスの詳細は、 :ref:`database-connect` を参照。

アプリケーションで複数のデータベース接続（トランザクション）を使用する
----------------------------------------------------------------------------------------------------
1つのアプリケーションで複数のデータベース接続が必要となるケースが考えられる。
この場合は、このハンドラをハンドラキュー上に複数設定することで対応する。

このハンドラは、データベース接続オブジェクトをスレッド上で管理する際に、データベース接続名をつけて管理している。
データベース接続名は、スレッド内で一意とする必要がある。

データベース接続名は、このハンドラの :java:extdoc:`connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` プロパティに設定する。
:java:extdoc:`connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` への設定を省略した場合、その接続はデフォルトのデータベース接続となり簡易的に利用できる。
このため、最もよく使うデータベース接続をデフォルトとし、それ以外のデータベース接続に対して任意の名前をつけると良い。

以下にデータベース接続名の設定例を示す。

.. code-block:: xml

  <!-- データベース接続を取得するファクトリの設定は省略 -->

  <!-- デフォルトのデータベース接続を設定 -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <property name="connectionFactory" ref="connectionFactory" />
  </component>

  <!-- userAccessLogという名前でデータベース接続を登録 -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <property name="connectionFactory" ref="userAccessLogConnectionFactory" />
    <property name="connectionName" value="userAccessLog" />
  </component>

上記のハンドラ設定の場合の、アプリケーションからのデータベースアクセス例を以下に示す。
なお、データベースアクセス部品の詳細な使用方法は、 :ref:`database` を参照。

デフォルトのデータベース接続を使用する
  :java:extdoc:`DbConnection#getConnection <nablarch.core.db.connection.DbConnectionContext.getConnection()>` 呼び出し時に引数を指定する必要が無い。
  引数を指定しないと、自動的にデフォルトのデータベース接続が戻される。

  .. code-block:: java

    AppDbConnection connection = DbConnectionContext.getConnection();

userAccessLogデータベース接続を使用する
  :java:extdoc:`DbConnection#getConnection(String) <nablarch.core.db.connection.DbConnectionContext.getConnection(java.lang.String)>` を使用し、引数にデータベース接続名を指定する。
  データベース接続名は :java:extdoc:`connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` プロパティに設定した値と一致させる必要がある。

  .. code-block:: java

    AppDbConnection connection = DbConnectionContext.getConnection("userAccessLog");
