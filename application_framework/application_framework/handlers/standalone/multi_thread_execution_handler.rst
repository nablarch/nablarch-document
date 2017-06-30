.. _multi_thread_execution_handler:

マルチスレッド実行制御ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラは、サブスレッドを作成し、ハンドラキュー上の後続ハンドラの処理を各サブスレッド上で並行実行する。
このハンドラでの処理結果は、各サブスレッドでの実行結果を集約したオブジェクト(:java:extdoc:`MultiStatus <nablarch.fw.Result.MultiStatus>`)となる。

本ハンドラでは、以下の処理を行う。

* :ref:`サブスレッド起動前のコールバック処理 <multi_thread_execution_handler-callback>`
* :ref:`サブスレッドの起動 <multi_thread_execution_handler-thread_count>`
* サブスレッドでの後続ハンドラの実行
* :ref:`サブスレッドで例外及びエラー発生時のコールバック処理 <multi_thread_execution_handler-callback>`
* :ref:`サブスレッドでの処理終了後のコールバック処理 <multi_thread_execution_handler-callback>`

処理の流れは以下のとおり。

.. image:: ../images/MultiThreadExecutionHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.MultiThreadExecutionHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

制約
------------------------------
特に無し

.. _multi_thread_execution_handler-thread_count:

スレッド数を指定する
--------------------------------------------------
本ハンドラはデフォルトでは、後続のサブスレッドを1つだけ起動し、ハンドラを実行する。

後続の処理（例えばバッチアクションの処理）を並列化することで、パフォーマンス向上が見込まれる場合には、設定値を変更することで後続のハンドラの処理を多重化出来る。

以下に例を示す。

.. code-block:: xml

  <component class = "nablarch.fw.handler.MultiThreadExecutionHandler">
    <!-- 後続ハンドラを8多重で実行する -->
    <property name="concurrentNumber" value="8" />
  </component>

.. important::

  本ハンドラ以降の処理を複数スレッドで実行する場合、後続のハンドラやバッチアクションなどはスレッドセーフな実装となっている必要がある。
  スレッドセーフとなっている保証のない処理を安易に複数スレッドで実行すると、予期せぬ例外が発生したり、データ不整合の原因となるので注意すること。

.. _multi_thread_execution_handler-callback:

スレッド起動前後で任意の処理を実行したい
--------------------------------------------------
このハンドラは、サブスレッド起動前及び終了後にコールバック処理を行う。

コールバック処理は以下の3つのポイントで実行される。

* サブスレッド起動前
* サブスレッドで例外発生後の全スレッド終了後
* 全サブスレッド終了後(サブスレッドで例外が発生した場合でも実行される)

コールバックされる処理は、このハンドラより後続に設定されたハンドラの中で、 :java:extdoc:`ExecutionHandlerCallback <nablarch.fw.handler.ExecutionHandlerCallback>` を実装しているものとなる。
もし、複数のハンドラが  :java:extdoc:`ExecutionHandlerCallback <nablarch.fw.handler.ExecutionHandlerCallback>` を実装している場合は、より手前に設定されているハンドラから順次コールバック処理を実行する。

.. important::

  複数のハンドラがコールバック処理を実装していた場合で、コールバック処理中にエラーや例外が発生した場合は、 残りのハンドラに対するコールバック処理は実行しないため注意すること。

.. important::

  コールバック処理で行ったデータベース処理は、親スレッド側のハンドラキューに設定されたデータベース接続とトランザクションが使用される。
  このため、これらの処理で行った更新処理は本ハンドラ終了後に、親スレッド側に設定された :ref:`transaction_management_handler` で確定(コミット)される。

  もし、コールバック処理内で行った処理を即確定する必要がある場合には、親スレッド側に設定されたデータベース接続ではなく、個別のトランザクションを使用して処理を行うこと。

  詳細は、以下を参照。

  * :ref:`ユニバーサルDAOで個別トランザクションを使用する <universal_dao-transaction>`
  * :ref:`データベースアクセス機能で個別トランザクションを使用する <database-new_transaction>`

以下にコールバック処理の実装例を示す。

.. code-block:: java

  public class SampleHandler implements Handler<Object, Result>, ExecutionHandlerCallback<Object, Result> {

    @Override
    public Result handle(Object input, ExecutionContext context) {
      // ハンドラの処理を実装する。
      return context.handleNext(input);
    }

    @Override
    public void preExecution(Object input, ExecutionContext context) {
      // サブスレッド起動前のコールバック処理を実装する
    }

    @Override
    public void errorInExecution(Throwable error, ExecutionContext context) {
      // サブスレッドでエラーが発生した場合のコールバック処理を実装する
    }

    @Override
    public void postExecution(Result result, ExecutionContext context) {
      // サブスレッド終了後のコールバック処理を実装する
      // サブスレッド側の処理が正常に終了したかどうかは、引数のResultから判定できる。
      if (result.isSuccess()) {
          // サブスレッドが正常終了
      } else {
          // サブスレッドが異常終了
      }
    }
  }

データベース接続に関する設定について
--------------------------------------------------
親スレッド側の処理でデータベース接続が必要となる場合には、本ハンドラ以前に :ref:`database_connection_management_handler` の設定が必要になる。
サブスレッド側でデータベースに対するアクセスが必要な場合には、本ハンドラ以降のサブスレッドで実行されるハンドラ構成に :ref:`database_connection_management_handler` の設定が必要となる。
(親スレッド、サブスレッドともに、データベース接続とセットでトランザクション制御を行うハンドラも必要となる)

このため、親スレッド及びサブスレッドの両方でデータベースアクセスを行うハンドラ構成の場合、最低でも2つのデータベース接続が使用される。
サブスレッドが複数となる場合には、スレッド数分のデータベース接続が必要となる。例えば、サブスレッド数が10の場合、合計11個のデータベース接続が必要となる。

  

