機能詳細
========================================
.. contents:: 目次
  :depth: 3
  :local:

バッチアプリケーションの起動方法
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/run_batch_application

* :ref:`JSR352バッチアプリケーションの起動方法 <jsr352_run_batch_application>`

システムリポジトリの初期化
--------------------------------------------------
* :ref:`JSR352バッチアプリケーションでシステムリポジトリの初期化 <jsr352_run_batch_init_repository>`

バッチジョブに適用するリスナーの定義方法
--------------------------------------------------
* :ref:`リスナーの定義方法 <jsr352-listener_definition>`

入力値のチェック
--------------------------------------------------
* :ref:`入力値のチェック <validation>`

データベースアクセス
--------------------------------------------------
* :ref:`データベースアクセス <database_management>`

ファイル入出力
--------------------------------------------------
* :ref:`ファイル入出力<data_converter>`

排他制御
--------------------------------------------------
排他制御は、以下の2種類の方法を提供しているが、
:ref:`UniversalDaoを推奨する理由 <exclusive_control-deprecated>` に記載がある通り、
:ref:`universal_dao` の使用を推奨する。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_pessimistic_lock`

ジョブ定義のxmlの作成方法
--------------------------------------------------
* `JSR352 Specificationを参照(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=352>`_

MOMメッセージ送信
----------------------------------------
* :ref:`同期応答メッセージ送信<mom_system_messaging-sync_message_send>`

運用設計
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/operation_policy
  feature_details/progress_log
  feature_details/operator_notice_log

* :doc:`feature_details/operation_policy`
* :doc:`feature_details/progress_log`
* :doc:`feature_details/operator_notice_log`

