アーキテクチャ概要
==============================

.. contents:: 目次
  :depth: 3
  :local:

MOMメッセージングでは、外部から送信される要求電文に対し、
電文中のリクエストIDに対応するアクションを実行する機能を提供する。
なお、ここでは、MOMメッセージングに使うメッセージキューのことをMQと称す。

MOMメッセージングは、以下の2つに分かれる。

同期応答メッセージング
 業務処理の実行結果をもとに、要求電文に対する応答電文を作成してMQに送信する。
 オーソリ業務のような即時応答を必要とする場合に使用する。

応答不要メッセージング
 応答電文の送信は行わず、MQから受信した要求電文の内容をDB上のテーブルに格納する。
 業務処理は、このテーブルを入力とする後続バッチによって実行する。
 バッチについては、 :ref:`db_messaging` を参照すること。

.. tip::
 応答不要メッセージングは、電文の内容をテーブルに格納するという、極めて単純な処理となるため、
 フレームワークが提供するアクションクラスをそのまま使用することができる。
 その場合、必要な設定を行うだけでよく、コーディングは不要である。

MOMメッセージングでは、メッセージの送受信にライブラリのMOMメッセージング機能を使用している。
詳細は :ref:`mom_system_messaging` を参照。

MOMメッセージングの構成
------------------------------------------------------
MOMメッセージングの構成は、 :ref:`nablarch_batch` とまったく同じである。
:ref:`nablarch_batch-structure` を参照。

要求電文によるアクションとリクエストIDの指定
------------------------------------------------------
MOMメッセージングでは、要求電文中の特定のフィールドをリクエストIDとして使用する。
この場合、ウェブアプリケーションなどのリクエストパスとは異なり、リクエストIDには階層構造が含まれないので、
:ref:`request_path_java_package_mapping` を使用し、アクションクラスのパッケージやクラス名のサフィックスを設定で指定し、
リクエストIDに対応するクラスにディスパッチを行う。

リクエストIDは要求電文中のフレームワーク制御ヘッダ部に含める必要がある。
詳細は、  :ref:`フレームワーク制御ヘッダ <mom_system_messaging-fw_header>` を参照。

MOMメッセージングの処理の流れ
------------------------------------------------------
MOMメッセージングが要求電文を受信し、応答電文を返却するまでの処理の流れを以下に示す。
応答不要メッセージングでは、応答電文を返却しない点のみ異なる。

.. image:: images/mom_messaging-flow.png
  :scale: 80

1. :ref:`共通起動ランチャ(Main) <main>` がハンドラキュー(handler queue)を実行する。
2. データリーダ(
   :java:extdoc:`FwHeaderReader<nablarch.fw.messaging.reader.FwHeaderReader>`
   /
   :java:extdoc:`MessageReader<nablarch.fw.messaging.reader.MessageReader>`
   )がメッセージキューを監視し、受信した電文を読み込み、要求電文を1件ずつ提供する。
3. ハンドラキューに設定された
   :ref:`nablarch_batch-structure` が、
   要求電文の特定フィールドに含まれるリクエストIDを元に処理すべきアクションクラス(action class)を特定し、
   ハンドラキューの末尾に追加する。
4. アクションクラス(action class)は、フォームクラス(form class)やエンティティクラス(entity class)を使用して、
   要求電文1件ごとの業務ロジック(business logic) を実行する。
5. アクションクラス(action class)は、応答電文を表す
   :java:extdoc:`ResponseMessage <nablarch.fw.messaging.ResponseMessage>` を返却する。
6. プロセス停止要求があるまで2～5を繰り返す。
7. ハンドラキューに設定された
   :java:extdoc:`ステータスコード→プロセス終了コード変換ハンドラ(StatusCodeConvertHandler) <nablarch.fw.handler.StatusCodeConvertHandler>` が、
   処理結果のステータスコードをプロセス終了コードに変換し、
   MOMメッセージングの処理結果としてプロセス終了コードが返される。


MOMメッセージングで使用するハンドラ
------------------------------------------------------
Nablarchでは、MOMメッセージングを構築するために必要なハンドラを標準で幾つか提供している。
プロジェクトの要件に従い、ハンドラキューを構築すること。
(要件によっては、プロジェクトカスタムなハンドラを作成することになる)

各ハンドラの詳細は、リンク先を参照すること。

リクエストやレスポンスの変換を行うハンドラ
  * :ref:`status_code_convert_handler`
  * :ref:`data_read_handler`

プロセスの実行制御を行うハンドラ
  * :ref:`duplicate_process_check_handler`
  * :ref:`multi_thread_execution_handler`
  * :ref:`retry_handler`
  * :ref:`request_thread_loop_handler`
  * :ref:`process_stop_handler`
  * :ref:`request_path_java_package_mapping`

メッセージングに関連するハンドラ
  * :ref:`messaging_context_handler`
  * :ref:`message_reply_handler`
  * :ref:`message_resend_handler`


データベースに関連するハンドラ
  * :ref:`database_connection_management_handler`
  * :ref:`transaction_management_handler`

エラー処理に関するハンドラ
  * :ref:`global_error_handler`

その他
  * :ref:`thread_context_handler`
  * :ref:`thread_context_clear_handler`
  * :ref:`ServiceAvailabilityCheckHandler`


.. _mom_messaging-sync_receive_handler_que:

同期応答メッセージングの最小ハンドラ構成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
同期応答メッセージングを構築する際の、必要最小限のハンドラキューを以下に示す。
これをベースに、プロジェクト要件に従ってNablarchの標準ハンドラやプロジェクトで作成したカスタムハンドラの追加を行う。

.. list-table:: 同期応答メッセージングの最小ハンドラ構成
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
     - :ref:`global_error_handler`
     - メイン
     -
     -
     - 実行時例外、またはエラーの場合、ログ出力を行う。

   * - 3
     - :ref:`multi_thread_execution_handler`
     - メイン
     - サブスレッドを作成し、後続ハンドラの処理を並行実行する。
     - 全スレッドの正常終了まで待機する。
     - 処理中のスレッドが完了するまで待機し起因例外を再送出する。

   * - 4
     - :ref:`retry_handler`
     - サブ
     -
     -
     - リトライ可能な実行時例外を捕捉し、かつリトライ上限に達していなければ後続のハンドラを再実行する。

   * - 5
     - :ref:`messaging_context_handler`
     - サブ
     - MQ接続を取得する。
     - MQ接続を解放する。
     -

   * - 6
     - :ref:`database_connection_management_handler`
     - サブ
     - DB接続を取得する。
     - DB接続を解放する。
     -

   * - 7
     - :ref:`request_thread_loop_handler`
     - サブ
     - 後続のハンドラを繰り返し実行する。
     - ハンドラキューの内容を復旧しループを継続する。
     - プロセス停止要求か致命的なエラーが発生した場合のみループを停止する。

   * - 8
     - :ref:`thread_context_clear_handler`
     - サブ
     - 
     - :ref:`thread_context_handler` でスレッドローカル上に設定した値を全て削除する。
     -
     
   * - 9
     - :ref:`thread_context_handler`
     - サブ
     - コマンドライン引数からリクエストID、ユーザID等のスレッドコンテキスト変数を初期化する。
     -
     -

   * - 10
     - :ref:`process_stop_handler`
     - サブ
     - リクエストテーブル上の処理停止フラグがオンであった場合は、後続ハンドラの処理は行なわずにプロセス停止例外(
       :java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`
       )を送出する。
     -
     -

   * - 11
     - :ref:`message_reply_handler`
     - サブ
     -
     - 後続ハンドラから返される応答電文の内容をもとに電文を作成してMQに送信する。
     - エラーの内容をもとに電文を作成してMQに送信する。

   * - 12
     - :ref:`data_read_handler`
     - サブ
     - データリーダを使用して要求電文を1件読み込み、後続ハンドラの引数として渡す。
       また :ref:`実行時ID<log-execution_id>` を採番する。
     -
     - 読み込んだ電文をログ出力した後、元例外を再送出する。

   * - 13
     - :ref:`request_path_java_package_mapping`
     - サブ
     - 要求電文に含まれるリクエストIDをもとに呼び出すアクションを決定する。
     -
     -

   * - 14
     - :ref:`transaction_management_handler`
     - サブ
     - トランザクションを開始する。
     - トランザクションをコミットする。
     - トランザクションをロールバックする。


.. _mom_messaging-async_receive_handler_que:

応答不要メッセージングの最小ハンドラ構成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
応答不要メッセージングを構築する際の、必要最小限のハンドラキューを以下に示す。
これをベースに、プロジェクト要件に従ってNablarchの標準ハンドラやプロジェクトで作成したカスタムハンドラの追加を行う。

応答不要メッセージングの最小ハンドラ構成は、以下のハンドラを除けば同期応答メッセージングと同じである。

* :ref:`message_reply_handler`
* :ref:`message_resend_handler`

.. important::
 応答不要メッセージングでは、電文の保存に失敗した場合にエラー応答を送信することができないので、
 取得した電文を一旦キューに戻した後で既定回数に達するまでリトライする。
 このため、DBに対する登録処理とキューに対する操作を1つのトランザクションとして扱う必要がある(2相コミット制御)。
 具体的には、 :ref:`transaction_management_handler` の設定を変更し、2相コミットに対応した実装に差し替える必要がある。

 Nablarchでは、WebSphere MQ を使用した2相コミット用のアダプタを予め提供している。
 詳細は、 :ref:`webspheremq_adaptor` を参照。

.. list-table:: 応答不要メッセージングの最小ハンドラ構成
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
     - :ref:`global_error_handler`
     - メイン
     -
     -
     - 実行時例外、またはエラーの場合、ログ出力を行う。

   * - 3
     - :ref:`multi_thread_execution_handler`
     - メイン
     - サブスレッドを作成し、後続ハンドラの処理を並行実行する。
     - 全スレッドの正常終了まで待機する。
     - 処理中のスレッドが完了するまで待機し起因例外を再送出する。

   * - 4
     - :ref:`retry_handler`
     - サブ
     -
     -
     - リトライ可能な実行時例外を捕捉し、かつリトライ上限に達していなければ後続のハンドラを再実行する。

   * - 5
     - :ref:`messaging_context_handler`
     - サブ
     - MQ接続を取得する。
     - MQ接続を解放する。
     -

   * - 6
     - :ref:`database_connection_management_handler`
     - サブ
     - DB接続を取得する。
     - DB接続を解放する。
     -

   * - 7
     - :ref:`request_thread_loop_handler`
     - サブ
     - 後続のハンドラを繰り返し実行する。
     - ハンドラキューの内容を復旧しループを継続する。
     - プロセス停止要求か致命的なエラーが発生した場合のみループを停止する。

   * - 8
     - :ref:`thread_context_clear_handler`
     - サブ
     - 
     - :ref:`thread_context_handler` でスレッドローカル上に設定した値を全て削除する。
     -
     
   * - 9
     - :ref:`thread_context_handler`
     - サブ
     - コマンドライン引数からリクエストID、ユーザID等のスレッドコンテキスト変数を初期化する。
     -
     -

   * - 10
     - :ref:`process_stop_handler`
     - サブ
     - リクエストテーブル上の処理停止フラグがオンであった場合は、後続ハンドラの処理は行なわずにプロセス停止例外(
       :java:extdoc:`ProcessStop <nablarch.fw.handler.ProcessStopHandler.ProcessStop>`
       )を送出する。
     -
     -

   * - 11
     - :ref:`transaction_management_handler`
     - サブ
     - トランザクションを開始する。
     - トランザクションをコミットする。
     - トランザクションをロールバックする。

   * - 12
     - :ref:`data_read_handler`
     - サブ
     - データリーダを使用して要求電文を1件読み込み、後続ハンドラの引数として渡す。
       また :ref:`実行時ID<log-execution_id>` を採番する。
     -
     - 読み込んだ電文をログ出力した後、元例外を再送出する。

   * - 13
     - :ref:`request_path_java_package_mapping`
     - サブ
     - 要求電文に含まれるリクエストIDをもとに呼び出すアクションを決定する。
     -
     -


.. _mom_messaging-data_reader:

MOMメッセージングで使用するデータリーダ
------------------------------------------------------
Nablarchでは、MOMメッセージングを構築するために必要なデータリーダを標準で幾つか提供している。
各データリーダの詳細は、リンク先を参照すること。

* :java:extdoc:`FwHeaderReader (電文からフレームワーク制御ヘッダの読み込み) <nablarch.fw.messaging.reader.FwHeaderReader>`
* :java:extdoc:`MessageReader (MQから電文の読み込み)<nablarch.fw.messaging.reader.MessageReader>`

.. tip::
 上記のデータリーダでプロジェクトの要件を満たせない場合は、
 :java:extdoc:`DataReader <nablarch.fw.DataReader>` インタフェースを実装したクラスを
 プロジェクトで作成して対応する。

.. _mom_messaging-action:

MOMメッセージングで使用するアクション
---------------------------------------------------------------------------------
Nablarchでは、MOMメッセージングを構築するために必要なアクションクラスを標準で幾つか提供している。
各アクションクラスの詳細は、リンク先を参照すること。

* :java:extdoc:`MessagingAction (同期応答メッセージング用アクションのテンプレートクラス)<nablarch.fw.messaging.action.MessagingAction>`
* :java:extdoc:`AsyncMessageReceiveAction (応答不要メッセージングのアクションクラス)<nablarch.fw.messaging.action.AsyncMessageReceiveAction>`
