.. _transaction_management_handler:

トランザクション制御ハンドラ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

データベースやメッセージキューなどのトランザクションに対応したリソースを使用し、後続処理における透過的トランザクションを実現するハンドラ。

トランザクション機能の詳細は、 :ref:`transaction` を参照。

本ハンドラでは、以下の処理を行う。

* トランザクションの開始
* トランザクションの終了(コミットやロールバック)
* トランザクションの終了時のコールバック

処理の流れは以下のとおり。

.. image:: ../images/TransactionManagementHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.TransactionManagementHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-transaction</artifactId>
  </dependency>

  <!-- データベースに対するトランザクションを制御する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

  <!-- トランザクション終了時に任意の処理を実行する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

制約
------------------------------
:ref:`database_connection_management_handler` より後ろに配置すること
  データベースに対するトランザクションを制御する場合には、トランザクション管理対象のデータベース接続がスレッド上に存在している必要がある。
  このため、本ハンドラは :ref:`database_connection_management_handler` より後ろに配置する必要がある。

トランザクション制御対象の設定を行う
--------------------------------------------------
このハンドラは、 :java:extdoc:`transactionFactory <nablarch.common.handler.TransactionManagementHandler.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>`
プロパティに設定されたファクトリクラス( :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 実装クラス)を使用してトランザクションの制御対象を取得しスレッド上で管理する。

スレッド上で管理する際には、トランザクションを識別するための名前を設定する。
デフォルトでは、 ``transaction`` が使用されるが、任意の名前を使用する場合は、 :java:extdoc:`transactionName <nablarch.common.handler.TransactionManagementHandler.setTransactionName(java.lang.String)>` プロパティに設定すること。
:ref:`複数のトランザクションを使用する場合 <transaction_management_handler-multi_transaction>` は、  :java:extdoc:`transactionName <nablarch.common.handler.TransactionManagementHandler.setTransactionName(java.lang.String)>`  プロパティへの値の設定が必須となる。

.. tip::

  :ref:`database_connection_management_handler` で設定したデータベースに対するトランザクション制御を行う場合は、
  :java:extdoc:`DbConnectionManagementHandler#connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` に設定した値と同じ値を
  :java:extdoc:`transactionName <nablarch.common.handler.TransactionManagementHandler.setTransactionName(java.lang.String)>` プロパティに設定すること。

  なお、 :java:extdoc:`DbConnectionManagementHandler#connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` に値を設定していない場合は、
  :java:extdoc:`transactionName <nablarch.common.handler.TransactionManagementHandler.setTransactionName(java.lang.String)>` への設定は省略して良い。

以下の設定ファイル例を参考にし、このハンドラの設定を行うこと。

.. code-block:: xml

  <!-- トランザクション制御ハンドラ -->
  <component class="nablarch.common.handler.TransactionManagementHandler">
    <property name="transactionFactory" ref="databaseTransactionFactory" />
    <property name="transactionName" value="name" />
  </component>

  <!-- データベースに対するトランザクション制御を行う場合には、JdbcTransactionFactoryを設定する -->
  <component name="databaseTransactionFactory"
      class="nablarch.core.db.transaction.JdbcTransactionFactory">
    <!-- プロパティの設定は省略 -->
  </component>

特定の例外の場合にトランザクションをコミットさせる
----------------------------------------------------------------------------------------------------
このハンドラのデフォルト動作では、全てのエラー及び例外がロールバック対象となるが、
発生した例外の内容によってはトランザクションをコミットしたい場合がある。

この場合は、 :java:extdoc:`transactionCommitExceptions <nablarch.common.handler.TransactionManagementHandler.setTransactionCommitExceptions(java.util.List)>` プロパティに対して、
コミット対象の例外クラスを設定することで対応する。
なお、設定した例外クラスのサブクラスもコミット対象となる。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.common.handler.TransactionManagementHandler">
    <!-- transactionCommitExceptionsプロパティにコミット対象の例外クラスをFQCNで設定する。 -->
    <property name="transactionCommitExceptions">
      <list>
        <!-- example.TransactionCommitExceptionをコミット対象とする -->
        <value>example.TransactionCommitException</value>
      </list>
    </property>
  </component>

トランザクション終了時に任意の処理を実行したい
--------------------------------------------------
このハンドラでは、トランザクション終了(コミットやロールバック)時に、コールバック処理を行う。

コールバックされる処理は、このハンドラより後続に設定されたハンドラの中で、 :java:extdoc:`TransactionEventCallback <nablarch.fw.TransactionEventCallback>` を実装しているものとなる。
もし、複数のハンドラが  :java:extdoc:`TransactionEventCallback <nablarch.fw.TransactionEventCallback>` を実装している場合は、より手前に設定されているハンドラから順次コールバック処理を実行する。

なお、トランザクションをロールバックする場合には、ロールバック後にコールバック処理を実行する。
このため、コールバック処理は新しいトランザクションで実行され、コールバックが正常に終了するとコミットされる。

.. important::

  複数のハンドラがコールバック処理を実装していた場合で、コールバック処理中にエラーや例外が発生した場合は、
  残りのハンドラに対するコールバック処理は実行しないため注意すること。


以下に例を示す。

コールバック処理を行うハンドラの作成
  以下実装例のように、  :java:extdoc:`TransactionEventCallback <nablarch.fw.TransactionEventCallback>` を実装したハンドラを作成する。

  :java:extdoc:`transactionNormalEnd <nablarch.fw.TransactionEventCallback.transactionNormalEnd(TData,%20nablarch.fw.ExecutionContext)>` にトランザクションコミット時のコールバック処理を実装し、
  :java:extdoc:`transactionAbnormalEnd <nablarch.fw.TransactionEventCallback.transactionAbnormalEnd(java.lang.Throwable,%20TData,%20nablarch.fw.ExecutionContext)>` にトランザクションロールバック時のコールバック処理を実装する。

  .. code-block:: java

    public static class SampleHandler
        implements Handler<Object, Object>, TransactionEventCallback<Object> {

      @Override
      public Object handle(Object o, ExecutionContext context) {
        // ハンドラの処理を実装する
        return context.handleNext(o);
      }

      @Override
      public void transactionNormalEnd(Object o, ExecutionContext ctx) {
        // トランザクションコミット時のコールバック処理を実装する
      }

      @Override
      public void transactionAbnormalEnd(Throwable e, Object o, ExecutionContext ctx) {
        // トランザクションロールバック時のコールバック処理を実装する
      }
    }

ハンドラキューを構築する
  以下のように、このハンドラの後続ハンドラにコールバック処理を実装したハンドラを設定する。

  .. code-block:: xml

    <list name="handlerQueue">
      <!-- トランザクション制御ハンドラ -->
      <component class="nablarch.common.handler.TransactionManagementHandler">
        <!-- プロパティへの設定は省略 -->
      </component>

      <!-- コールバック処理を実装したハンドラ -->
      <component class="sample.SampleHandler" />
    </list>

.. _transaction_management_handler-multi_transaction:

アプリケーションで複数のトランザクションを使用する
----------------------------------------------------------------------------------------------------
1つのアプリケーションで複数のトランザクション制御が必要となるケースが考えられる。
この場合は、このハンドラをハンドラキュー上に複数設定することで対応する。

以下に複数のデータベース接続に対するトランザクションを制御するための設定例を示す。

.. code-block:: xml

  <!-- デフォルトのデータベース接続を設定 -->
  <component name="defaultDatabaseHandler"
      class="nablarch.common.handler.DbConnectionManagementHandler">

    <property name="connectionFactory" ref="connectionFactory" />

  </component>

  <!-- userAccessLogという名前でデータベース接続を登録 -->
  <component name="userAccessLogDatabaseHandler"
      class="nablarch.common.handler.DbConnectionManagementHandler">

    <property name="connectionFactory" ref="userAccessLogConnectionFactory" />
    <property name="connectionName" value="userAccessLog" />

  </component>

  <!-- デフォルトのデータベース接続に対するトランザクション制御の設定 -->
  <component name="defaultTransactionHandler"
      class="nablarch.common.handler.TransactionManagementHandler">

    <property name="transactionFactory" ref="databaseTransactionFactory" />

  </component>

  <!-- userAccessLogというデータベース接続に対するトランザクション制御の設定 -->
  <component name="userAccessLogTransactionHandler"
      class="nablarch.common.handler.TransactionManagementHandler">

    <property name="transactionFactory" ref="databaseTransactionFactory" />
    <property name="transactionName" value="userAccessLog" />

  </component>

上記のハンドラをハンドラキューに設定した場合の例を示す。

.. code-block:: xml

  <!-- データベースとトランザクション制御以外のハンドラは省略 -->

  <list name="handlerQueue">
    <!-- デフォルトのデータベースに対する接続とトランザクション制御 -->
    <component-ref name="defaultDatabaseHandler" />
    <component-ref name="defaultTransactionHandler" />

    <!-- userAccessLogのデータベースに対する接続とトランザクション制御 -->
    <component-ref name="userAccessLogDatabaseHandler" />
    <component-ref name="userAccessLogTransactionHandler" />
  </list>

