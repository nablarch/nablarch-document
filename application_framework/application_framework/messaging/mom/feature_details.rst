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
* :ref:`プロセス終了コード<status_code_convert_handler-rules>`
* :ref:`エラー発生時にエラー応答電文を返す<mom_system_messaging-sync_message_receive>`
* :ref:`メッセージングプロセスを異常終了させる <db_messaging-process_abnormal_end>` (テーブルをキューとして使ったメッセージングと同じ)
* :ref:`処理の並列実行(マルチスレッド化)<multi_thread_execution_handler>`

MOMメッセージング
--------------------------------------------------
* :ref:`mom_system_messaging`
* 標準提供のデータリーダ

  * :java:extdoc:`FwHeaderReader (電文からフレームワーク制御ヘッダの読み込み) <nablarch.fw.messaging.reader.FwHeaderReader>`
  * :java:extdoc:`MessageReader (MQから電文の読み込み)<nablarch.fw.messaging.reader.MessageReader>`

* :ref:`再送制御<message_resend_handler>`
