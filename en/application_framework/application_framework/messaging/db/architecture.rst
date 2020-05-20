アーキテクチャ概要
==============================
.. contents:: 目次
  :depth: 3
  :local:

データベースをキューとして扱うタイプのメッセージング処理では、
定期的にデータベース上のテーブルを監視し未処理のレコードを順次処理するための機能を提供している。

.. important::

  未処理のレコードの判定は、テーブルのレコード上で表す必要がある。
  このため、処理が終わったレコードの状態を処理済みへ変更する処理が必要となる。

構成
--------------------------------------------------
Nablarchバッチアプリケーションと同じ構成となる。
詳細は、 :ref:`Nablarchバッチアプリケーションの構成 <nablarch_batch-structure>` を参照。


リクエストパスによるアクションとリクエストIDの指定
--------------------------------------------------
データベースをキューとして扱うメッセージング処理では、Nablarchバッチアプリケーションと同じように
コマンドライン引数で実行するアクションとリクエストIDを指定する。

詳細は、 :ref:`NablarchバッチアプリケーションのアクションとリクエストIDの指定 <nablarch_batch-resolve_action>` を参照。

処理の流れ
------------------------------------------------------
Nablarchバッチアプリケーションと同じ処理の流れとなる。詳細は、 :ref:`nablarch_batch-process_flow` を参照。

使用するハンドラ
--------------------------------------------------------------------------
Nablarchでは、データベースをキューとして扱うメッセージング処理で必要なハンドラを標準で幾つか提供している。
プロジェクトの要件に従い、ハンドラキューを構築すること。(要件によっては、プロジェクトカスタムなハンドラを作成することになる)

各ハンドラの詳細は、リンク先を参照すること。

リクエストやレスポンスの変換を行うハンドラ
  * :ref:`status_code_convert_handler`
  * :ref:`data_read_handler`

実行制御を行うハンドラ
  * :ref:`duplicate_process_check_handler`
  * :ref:`request_path_java_package_mapping`
  * :ref:`multi_thread_execution_handler`
  * :ref:`retry_handler`
  * :ref:`process_stop_handler`
  * :ref:`request_thread_loop_handler`

データベースに関連するハンドラ
  * :ref:`database_connection_management_handler`
  * :ref:`transaction_management_handler`

エラー処理に関するハンドラ
  * :ref:`global_error_handler`

その他
  * :ref:`thread_context_handler`
  * :ref:`thread_context_clear_handler`
  * :ref:`ServiceAvailabilityCheckHandler`
  * :ref:`file_record_writer_dispose_handler`

ハンドラの最小構成
--------------------------------------------------
データベースをキューとして扱うメッセージング処理の必要最小限のハンドラキューを以下に示す。
これをベースに、プロジェクト要件に従ってNablarchの標準ハンドラやプロジェクトで作成したカスタムハンドラの追加を行う。

.. list-table:: 最小ハンドラ構成
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,22,12,22,22,22

  * - No.
    - ハンドラ
    - スレッド
    - 往路処理
    - 復路処理
    - 例外処理

  * - 1
    - :ref:`status_code_convert_handler`
    - メイン
    -
    - ステータスコードをプロセス終了コードに変換する。
    -
    
  * - 2
    - :ref:`thread_context_clear_handler`
    - メイン
    - 
    - :ref:`thread_context_handler` でスレッドローカル上に設定した値を全て削除する。
    -

  * - 3
    - :ref:`global_error_handler`
    - メイン
    -
    -
    - 実行時例外、またはエラーの場合、ログ出力を行う。

  * - 4
    - :ref:`thread_context_handler`
    - メイン
    - コマンドライン引数からリクエストID、ユーザID等のスレッドコンテキスト変数を初期化する。
    -
    -

  * - 5
    - :ref:`retry_handler`
    - メイン
    -
    -
    - リトライ可能な実行時例外を捕捉し、かつリトライ上限に達していなければ後続のハンドラを再実行する。

  * - 6
    - :ref:`database_connection_management_handler`
      (初期処理/終了処理用)
    - メイン
    - DB接続を取得する。
    - DB接続を解放する。
    -

  * - 7
    - :ref:`transaction_management_handler`
      (初期処理/終了処理用)
    - メイン
    - トランザクションを開始する。
    - トランザクションをコミットする。
    - トランザクションをロールバックする。

  * - 8
    - :ref:`request_path_java_package_mapping`
    - メイン
    - コマンドライン引数をもとに呼び出すアクションを決定する。
    -
    -

  * - 9
    - :ref:`multi_thread_execution_handler`
    - メイン
    - サブスレッドを作成し、後続ハンドラの処理を並行実行する。
    - 全スレッドの正常終了まで待機する。
    - 処理中のスレッドが完了するまで待機し起因例外を再送出する。

  * - 10
    - :ref:`database_connection_management_handler`
      (業務処理用)
    - サブ
    - DB接続を取得する。
    - DB接続を解放する。
    -

  * - 11
    - :ref:`request_thread_loop_handler`
    - サブ
    -
    - 再度後続のハンドラに処理を委譲する。
    - 例外/エラーに応じたログ出処理と再送出を行う。

  * - 12
    - :ref:`process_stop_handler`
    - サブ
    - リクエストテーブル上の処理停止フラグがオンであった場合は、後続ハンドラの処理は行なわずにプロセス停止例外(
      :java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`
      )を送出する。
    -
    -

  * - 13
    - :ref:`data_read_handler`
    - サブ
    - データリーダを使用してレコードを1件読み込み、後続ハンドラの引数として渡す。
      また :ref:`実行時ID<log-execution_id>` を採番する。
    -
    - 読み込んだレコードをログ出力した後、元例外を再送出する。

  * - 14
    - :ref:`transaction_management_handler`
      (業務処理用)
    - サブ
    - トランザクションを開始する。
    - トランザクションをコミットする。
    - トランザクションをロールバックする。

.. _db_messaging_architecture-reader:

使用するデータリーダ
----------------------------------------------------------------------------------------------------
データベースをキューとして扱う場合には、以下のデータリーダを使用する。
:java:extdoc:`バッチ用のDatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>` を使用した場合、
繰り返しテーブルを監視することができないので注意すること。

* :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>`

.. important::

  上記のリーダで要件を満たすことができず、プロジェクトでリーダを作成する場合は以下の点に注意して実装を行うこと。

  * 対象データがなくなった場合でも、継続して対象データを監視できるようにすること
  * マルチススレッド環境下で使われる場合に、同一データを複数のスレッドで処理することがないようにすること

  なお、 :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>` は、上記を満たすために以下の実装となっている

  * テーブルに未処理のデータが無くなった場合、再度検索用SQLを実行し未処理データを抽出する
  * 複数スレッドで同一データを処理することがないように、現在処理中のデータの識別子(主キーの値)を保持し、処理されていないデータを読み込んでいる


使用するアクションのテンプレートクラス
---------------------------------------------------------------------------------
データベースをキューとして扱う場合は、以下のテンプレートクラスを使用する。

* :java:extdoc:`BatchAction (汎用的なバッチアクション)<nablarch.fw.action.BatchAction>`

