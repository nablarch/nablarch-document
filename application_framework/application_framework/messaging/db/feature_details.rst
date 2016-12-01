機能詳細
========================================
.. contents:: 目次
  :depth: 3
  :local:

アプリケーションの起動方法
--------------------------------------------------
* :ref:`アプリケーションの起動方法<main-run_application>`

システムリポジトリの初期化
--------------------------------------------------
システムリポジトリの初期化は、アプリケーション起動時にシステムリポジトリの設定ファイルのパスを指定することで行う。
詳細は、:ref:`アプリケーションの起動方法<main-run_application>` を参照。

データベースアクセス
--------------------------------------------------
* :ref:`データベースアクセス <database_management>`
* 標準提供のデータリーダ

  * :java:extdoc:`DatabaseTableQueueReader (データベースのテーブルをキューとして扱うリーダ) <nablarch.fw.reader.DatabaseTableQueueReader>`

入力値のチェック
--------------------------------------------------
* :ref:`入力値のチェック <validation>`

排他制御
--------------------------------------------------
排他制御は、以下の2種類の方法を提供しているが、
:ref:`UniversalDaoを推奨する理由 <exclusive_control-deprecated>` に記載がある通り、
:ref:`universal_dao` の使用を推奨する。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_pessimistic_lock`

実行制御
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/error_processing

* :ref:`プロセス終了コード<status_code_convert_handler-rules>`
* :ref:`エラー発生データを除外して処理を継続する <db_messaging-exclude_error_data>`
* :ref:`メッセージングプロセスを異常終了させる <db_messaging-process_abnormal_end>`
* :ref:`処理の並列実行(マルチスレッド化)<multi_thread_execution_handler>`

マルチプロセス化
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/multiple_process

* :ref:`db_messaging-multiple_process`


