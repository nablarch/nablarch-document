.. _`batch-functional_comparison`:

JSRに準拠したバッチアプリケーションとNablarchバッチアプリケーションとの機能比較
----------------------------------------------------------------------------------------------------
この章では、以下の機能の比較を示す。

* :doc:`jsr352/index`
* :doc:`nablarch_batch/index`

.. list-table:: 機能比較（JSR：JSRの仕様で定義されている　○：提供あり　△：一部提供あり　×：提供なし　－：対象外）
  :header-rows: 1
  :class: something-special-class
  :widths: 30 35 35

  * - 機能
    - JSR352に準拠 [#jsr]_
    - Nablarchバッチ

  * - 起動時に任意のパラメータを設定できる
    - JSR
    - ○ |br| :ref:`解説書へ <main-option_parameter>`

  * - 同一バッチアプリケーションの同時実行を防止できる
    - ○ |br| :java:extdoc:`Javadocへ <nablarch.fw.batch.ee.listener.job.DuplicateJobRunningCheckListener>`
    - ○ |br| :ref:`解説書へ <duplicate_process_check_handler>`

  * - 実行中のバッチアプリケーションを |br| 外部から安全に停止することができる
    - JSR
    - ○ |br| :ref:`解説書へ <process_stop_handler>`

  * - 1回の実行で処理する最大の件数を指定できる
    - × |br| [#jsr_max]_
    - ○ |br| :ref:`解説書へ <data_read_handler-max_count>`

  * - 一定件数単位のコミットができる
    - JSR
    - ○ |br| :ref:`解説書へ <loop_handler-commit_interval>`

  * - 障害発生ポイントから再実行ができる
    - JSR
    - △ |br| [#resumable]_

  * - 業務処理を複数スレッドで並列実行できる
    - JSR
    - ○ |br| :ref:`解説書へ <multi_thread_execution_handler>`

  * - 特定の例外を無視して処理を継続することができる |br|
      (ロールバック後に処理を継続できる)
    - JSR
    - × |br| [#skip_exception]_

  * - 特定の例外発生時に処理をリトライできる
    - JSR
    - △ |br| [#retry_exception]_

  * - バッチアプリケーションの結果を元に |br| 次に実行する処理を切り替えられる
    - JSR
    - × |br| [#branch_batch]_

  * - 入力データソースを一定間隔で監視し |br| バッチを実行出来る
    - × [#resident_batch]_
    - ○ |br| :ref:`解説書へ <nablarch_batch-resident_batch>`


.. [#jsr]
  JSRの箇所は、JSR352で規定されている仕様に従う。
  詳細は、 `JSR352(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=352>`_ のSpecificationを参照すること。

.. [#jsr_max]
  :java:extdoc:`ItemReader <javax.batch.api.chunk.ItemReader>` の実装クラスに、1回の実行で読み込む最大件数を指定できるプロパティを持たせるなどで対応可能。

.. [#resumable]
  :java:extdoc:`ResumeDataReader (レジューム機能付き読み込み)<nablarch.fw.reader.ResumeDataReader>` を使用することで障害発生ポイントからの再実行が可能。
  ただし、この機能はファイルを入力としている場合にのみ利用できる。それ以外のデータを入力とする場合には、アプリケーション側で設計及び実装が必要となる。

.. [#skip_exception]
  特定例外を無視して処理を継続したい場合は、ハンドラを追加して対応すること。

.. [#retry_exception]
  :ref:`retry_handler` でリトライ可能例外の場合にリトライすることはできるが、JSR352のように例外が発生したデータの単純なリトライを行うことはできない。
  :ref:`retry_handler` では、リトライ対象の例外を柔軟に指定することができない。

  :ref:`retry_handler` で要件を満たすことができない(例外が発生したデータの単純なリトライや柔軟に例外を指定したい)場合は、ハンドラを追加して対応すること。

.. [#branch_batch]
  ジョブスケジューラなどで対応すること。例えば、終了コードを元に次に実行するジョブを切り替える等の対応が必要になる。

.. [#resident_batch]
  JSR352に準拠したバッチアプリケーションでは、一定間隔で入力データソースを監視するようなバッチ処理を実現することができない。
  このため、このようなバッチアプリケーションが必要となった場合は、 :ref:`Nablarchバッチアプリケーションの常駐バッチ  <nablarch_batch-resident_batch>` を使用して実現すること。

.. |br| raw:: html

  <br />

