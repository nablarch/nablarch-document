.. _loop_handler:

トランザクションループ制御ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラは、データリーダ上に処理対象のデータが存在する間、後続ハンドラの処理を繰り返し実行するとともに、トランザクション制御を行ない、一定の繰り返し回数ごとにトランザクションをコミットする。
トランザクションのコミット間隔を大きくすることで、バッチ処理のスループットを向上させることができる。

* トランザクションの開始
* トランザクションの終了(コミットやロールバック)
* トランザクションの終了時のコールバック

処理の流れは以下のとおり。

.. image:: ../images/LoopHandler/flow.png
  :scale: 80

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.LoopHandler`

モジュール一覧
--------------------------------------------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-transaction</artifactId>
  </dependency>

  <!-- データベースに対するトランザクションを制御する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

制約
------------------------------
:ref:`database_connection_management_handler` より後ろに設定すること
  データベースに対するトランザクションを制御する場合には、トランザクション管理対象のデータベース接続がスレッド上に存在している必要がある。

トランザクション制御対象の設定を行う
--------------------------------------------------
このハンドラは、 :java:extdoc:`transactionFactory <nablarch.fw.handler.LoopHandler.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>`
プロパティに設定されたファクトリクラス( :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` の実装クラス)を使用してトランザクションの制御対象を取得しスレッド上で管理する。

スレッド上で管理する際には、トランザクションを識別するための名前を設定する。
デフォルトでは、 ``transaction`` が使用されるが、任意の名前を使用する場合は、 :java:extdoc:`transactionName <nablarch.fw.handler.LoopHandler.setTransactionName(java.lang.String)>` プロパティに設定すること。

.. tip::

  :ref:`database_connection_management_handler` で設定したデータベースに対するトランザクション制御を行う場合は、
  :java:extdoc:`DbConnectionManagementHandler#connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` に設定した値と同じ値を
  :java:extdoc:`transactionName <nablarch.fw.handler.LoopHandler.setTransactionName(java.lang.String)>` プロパティに設定すること。

  なお、 :java:extdoc:`DbConnectionManagementHandler#connectionName <nablarch.common.handler.DbConnectionManagementHandler.setConnectionName(java.lang.String)>` に値を設定していない場合は、
  :java:extdoc:`transactionName <nablarch.fw.handler.LoopHandler.setTransactionName(java.lang.String)>` への設定は省略して良い。

以下の設定ファイル例を参考にし、このハンドラの設定を行うこと。

.. code-block:: xml

  <!-- トランザクション制御ハンドラ -->
  <component class="nablarch.fw.handler.LoopHandler">
    <property name="transactionFactory" ref="databaseTransactionFactory" />
    <property name="transactionName" value="name" />
  </component>

  <!-- データベースに対するトランザクション制御を行う場合には、JdbcTransactionFactoryを設定する -->
  <component name="databaseTransactionFactory"
      class="nablarch.core.db.transaction.JdbcTransactionFactory">
    <!-- プロパティの設定は省略 -->
  </component>

.. _loop_handler-commit_interval:

コミット間隔を指定する
--------------------------------------------------
バッチ処理のコミット間隔は、 :java:extdoc:`commitInterval <nablarch.fw.handler.LoopHandler.setCommitInterval(int)>` プロパティに設定する。
概要で述べたように、コミット間隔を調整することで、バッチ処理のスループットを向上させることができる。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.handler.LoopHandler">
    <!-- コミット間隔に1000を指定 -->
    <property name="commitInterval" value="1000" />
  </component>

.. _loop_handler-callback:

トランザクション終了時に任意の処理を実行したい
--------------------------------------------------
このハンドラでは、後続のハンドラの処理実行後にコールバック処理を行う。

コールバックされる処理は、このハンドラより後続に設定されたハンドラの中で、 :java:extdoc:`TransactionEventCallback <nablarch.fw.TransactionEventCallback>` を実装しているものとなる。
もし、複数のハンドラが  :java:extdoc:`TransactionEventCallback <nablarch.fw.TransactionEventCallback>` を実装している場合は、より手前に設定されているハンドラから順次コールバック処理を実行する。

後続ハンドラが正常に処理を終えた場合のコールバック処理は、後続ハンドラと同一のトランザクションで実行される。
コールバック処理で行った処理は、次回のコミットタイミングで一括コミットされる。

後続のハンドラで例外及びエラーが発生し、トランザクションをロールバックする場合には、ロールバック後にコールバック処理を実行する。
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
        // 後続ハンドラが正常終了した場合のコールバック処理を実装する
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
      <component class="nablarch.fw.handler.LoopHandler">
        <!-- プロパティへの設定は省略 -->
      </component>

      <!-- コールバック処理を実装したハンドラ -->
      <component class="sample.SampleHandler" />
    </list>
