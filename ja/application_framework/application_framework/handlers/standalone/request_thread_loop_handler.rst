.. _request_thread_loop_handler:

リクエストスレッド内ループ制御ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

プロセスの停止要求があるまで、後続のハンドラを繰り返し実行するハンドラ。
このハンドラは、メッセージキューやデータベース上のテーブルなどを監視し、未処理のデータを随時処理するプロセスで使用する。

.. tip::

  メッセージキューやデータベース上のテーブルを監視して処理するプロセスでは、個々のリクエスト(データ)は独立して扱われる。
  1つのリクエスト処理がエラーとなっても他のリクエスト処理はそのまま継続しなければならない。
  このため、このハンドラで捕捉した例外は、プロセス正常停止要求や致命的な一部の例外を除き処理を継続する。

  詳細は、 :ref:`request_thread_loop_handler-error_handling` を参照。

本ハンドラでは、以下の処理を行う。

* 後続ハンドラを繰り返し実行
* プロテス停止要求例外発生時の後続ハンドラ実行の停止 |br|
  詳細は、 :ref:`request_thread_loop_handler-stop` を参照
* 後続ハンドラで発生した例外(エラー)に応じた処理(ログ出力等) |br|
  詳細は、 :ref:`request_thread_loop_handler-error_handling` を参照

処理の流れは以下のとおり。

.. image:: ../images/RequestThreadLoopHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.RequestThreadLoopHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

制約
------------------------------
:ref:`retry_handler` より後ろに配置すること
  このハンドラでは、処理が継続可能な例外の場合に :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。
  このため、リトライ可能例外を処理する :ref:`retry_handler` よりも後ろにこのハンドラを設定する必要がある。

.. _request_thread_loop_handler-interval:

サービス閉塞中の待機時間を設定する
--------------------------------------------------
後続のハンドラからサービス閉塞中を示す例外(:java:extdoc:`ServiceUnavailable <nablarch.fw.results.ServiceUnavailable>`)が発生した場合の待機時間を設定することが出来る。
この時間を設定することで、サービスが開局されたかどうかのチェックタイミングを調整することが出来る。

待機時間を長くし過ぎると、サービスが開局中に変更されても、即処理が開始されない問題があるので、要件にあわせて値を設定すること。
なお、設定を省略した場合は、1秒待機後に後続ハンドラを再実行する。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.handler.RequestThreadLoopHandler">
    <!-- 待機時間に5秒を設定 -->
    <property name="serviceUnavailabilityRetryInterval" value="5000" />
  </component>

.. tip::
  後続ハンドラに :ref:`ServiceAvailabilityCheckHandler` を設定しない場合には、本設定値は設定する必要が無い。
  (設定したとしても、この値が使われることはない。)

.. _request_thread_loop_handler-stop:

本ハンドラの停止方法
--------------------------------------------------
このハンドラは、プロセスの停止要求を示す例外が発生するまで、繰り返し後続のハンドラに対して処理を委譲する。
このため、メンテナンスなどでプロセスを停止する必要がある場合には、本ハンドラより後続に :ref:`process_stop_handler` を設定し、
外部からプロセスを停止できるようにする必要がある。

プロセス停止要求を示す例外が発生した場合の処理内容は、 :ref:`request_thread_loop_handler-error_handling` を参照。

.. _request_thread_loop_handler-error_handling:

後続ハンドラで発生した例外(エラー)に応じた処理内容
------------------------------------------------------------
このハンドラで行う後続ハンドラで発生した例外(エラー)に応じた処理内容について解説する。

サービス閉塞中例外(:java:extdoc:`ServiceUnavailable <nablarch.fw.results.ServiceUnavailable>`)
  一定時間待機後に、再度後続ハンドラに処理を委譲する。
  待機時間の設定方法は、 :ref:`request_thread_loop_handler-interval` を参照。

プロセス停止要求を示す例外(:java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`)
  プロセス停止要求を示す例外であるため、本ハンドラの処理を終了する。

プロセスの異常終了を示す例外(:java:extdoc:`ProcessAbnormalEnd <nablarch.fw.launcher.ProcessAbnormalEnd>`)
  プロセスの異常終了を示す例外のため、捕捉した例外を再送出する。

処理を継続することができなかったことを示すサービスエラー(:java:extdoc:`ServiceError <nablarch.fw.results.ServiceError>`)
  補足した例外クラスにログ出力処理を委譲し、 :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。

ハンドラの処理が異常終了したことを示す例外(:java:extdoc:`Result.Error <nablarch.fw.Result.Error>`)
  ``FATAL`` レベルのログを出力し、 :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。

実行時例外(:java:extdoc:`RuntimeException <java.lang.RuntimeException>`)
  ``FATAL`` レベルのログを出力し、 :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。
 
スレッドの停止を示す例外(:java:extdoc:`ThreadDeath <java.lang.ThreadDeath>`)
  ``INFO`` レベルのログを出力し、補足した例外(ThreadDeath)を再送出する。

スタックオーバーフローエラー(:java:extdoc:`StackOverflowError <java.lang.StackOverflowError>`)
  ``FATAL`` レベルのログを出力し、 :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。

ヒープ不足のエラー(:java:extdoc:`OutOfMemoryError <java.lang.OutOfMemoryError>`)
  標準エラー出力にヒープ不足が発生したことを示すメッセージを出力し、 ``FATAL`` レベルのログ出力を行う。
  (ログ出力時に再度ヒープ不足が発生する可能性があるため、標準エラー出力にメッセージ出力後にログを出力する。)

  ヒープ不足の原因不足となったオブジェクトへの参照が切れ、処理継続可能な場合があるため :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。
  
JVMの異常を示すエラー(:java:extdoc:`VirtualMachineError <java.lang.VirtualMachineError>`)
  発生した例外を再送出する

上記以外のエラー
  ``FATAL`` レベルのログを出力し、 :java:extdoc:`リトライ可能例外(Retryable) <nablarch.fw.handler.retry.Retryable>` を送出する。

.. |br| raw:: html

  <br/>
