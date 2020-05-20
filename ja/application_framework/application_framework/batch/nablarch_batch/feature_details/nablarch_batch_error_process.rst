.. _nablarch_batch_error_process:

Nablarchバッチアプリケーションのエラー処理
============================================================
.. contents:: 目次
  :depth: 3
  :local:

.. _nablarch_batch_error_process-rerun:

バッチ処理をリランできるようにする
--------------------------------------------------
Nablarchバッチアプリケーションでは、ファイル入力を除き、
バッチ処理をリランできるようにする機能を提供していない。

そのため、処理対象レコードにステータスを持たせ、
処理成功や失敗時にステータスを変更するといった、
アプリケーションでの設計と実装が必要となる。
処理成功や失敗時のステータス変更の実装方法については、
:ref:`loop_handler-callback` を参照。

ファイル入力については、
:java:extdoc:`ResumeDataReader (レジューム機能付き読み込み)<nablarch.fw.reader.ResumeDataReader>`
を使用することで、障害発生ポイントからの再実行ができる。

.. _nablarch_batch_error_process-continue:

バッチ処理でエラー発生時に処理を継続する
--------------------------------------------------
エラー発生時の処理継続は、 :ref:`常駐バッチ<nablarch_batch-resident_batch>` のみ対応している。
:ref:`都度起動バッチ<nablarch_batch-each_time_batch>` は対応していない。

:ref:`常駐バッチ<nablarch_batch-resident_batch>` では、
:java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
を送出すると、 :ref:`retry_handler` により処理が継続される。
ただし、 :ref:`nablarch_batch_error_process-rerun` に記載した内容で、
バッチ処理がリランできるようになっている必要がある。

.. tip::
 :ref:`都度起動バッチ<nablarch_batch-each_time_batch>` で
 :java:extdoc:`TransactionAbnormalEnd<nablarch.fw.results.TransactionAbnormalEnd>`
 が送出されると、バッチ処理が異常終了となる。

.. _nablarch_batch_error_process-abnormal_end:

バッチ処理を異常終了にする
--------------------------------------------------
アプリケーションでエラーを検知した場合に、
処理を継続せずにバッチ処理を異常終了させたい場合がある。

Nablarchバッチアプリケーションでは、
:java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`
を送出すると、バッチ処理を異常終了にできる。
:java:extdoc:`ProcessAbnormalEnd<nablarch.fw.launcher.ProcessAbnormalEnd>`
が送出された場合、プロセス終了コードはこのクラスに指定された値となる。

