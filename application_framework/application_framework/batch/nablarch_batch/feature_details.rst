機能詳細
========================================
.. contents:: 目次
  :depth: 3
  :local:

バッチアプリケーションの起動方法
--------------------------------------------------
* :ref:`Nablarchバッチアプリケーションの起動方法<main-run_application>`

システムリポジトリの初期化
--------------------------------------------------
システムリポジトリの初期化は、アプリケーション起動時にシステムリポジトリの設定ファイルのパスを指定することで行う。
詳細は、:ref:`Nablarchバッチアプリケーションの起動方法<main-run_application>` を参照。

入力値のチェック
--------------------------------------------------
* :ref:`入力値のチェック <validation>`

データベースアクセス
--------------------------------------------------
* :ref:`データベースアクセス <database_management>`
* 標準提供のデータリーダ

  * :java:extdoc:`DatabaseRecordReader (データベース読み込み) <nablarch.fw.reader.DatabaseRecordReader>`

ファイル入出力
--------------------------------------------------
* :ref:`ファイル入出力<data_converter>`

* 標準提供のデータリーダ

  * :java:extdoc:`FileDataReader (ファイル読み込み)<nablarch.fw.reader.FileDataReader>`
  * :java:extdoc:`ValidatableFileDataReader (バリデージョン機能付きファイル読み込み)<nablarch.fw.reader.ValidatableFileDataReader>`
  * :java:extdoc:`ResumeDataReader (レジューム機能付き読み込み)<nablarch.fw.reader.ResumeDataReader>`

排他制御
--------------------------------------------------
排他制御は、以下の2種類の方法を提供しているが、
:ref:`UniversalDaoを推奨する理由 <exclusive_control-deprecated>` に記載がある通り、
:ref:`universal_dao` の使用を推奨する。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_pessimistic_lock`

バッチ処理の実行制御
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_error_process
  feature_details/nablarch_batch_retention_state

* :ref:`バッチ処理のプロセス終了コード<status_code_convert_handler-rules>`
* :ref:`バッチ処理のエラー処理<nablarch_batch_error_process>`
* :ref:`バッチ処理の並列実行(マルチスレッド化)<multi_thread_execution_handler>`
* :ref:`バッチ処理のコミット間隔の制御 <loop_handler-commit_interval>`
* :ref:`1回のバッチ処理の処理件数制限 <data_read_handler-max_count>`
  |br| (大量データを処理するバッチ処理を数日に分けて処理させる場合など)

MOMメッセージ送信
----------------------------------------
* :ref:`同期応答メッセージ送信<mom_system_messaging-sync_message_send>`
* :ref:`応答不要メッセージ送信<mom_system_messaging-async_message_send>`

バッチ実行中の状態の保持
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_retention_state

* :ref:`nablarch_batch_retention_state`

常駐バッチのマルチプロセス化
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_batch_multiple_process
  
* :ref:`nablarch_batch_multiple_process`

.. |br| raw:: html

  <br />
