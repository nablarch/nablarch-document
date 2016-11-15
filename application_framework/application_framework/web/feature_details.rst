機能詳細
========================================

.. contents:: 目次
  :depth: 3
  :local:

.. _web_feature_details-nablarch_initialization:

Nablarchの初期化
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_servlet_context_listener
  feature_details/web_front_controller

Nablarchの初期化を行うためには、 :ref:`システムリポジトリのロードの為の設定 <nablarch_servlet_context_listener>`
及び :ref:`ハンドラキューの設定(構築) <web_front_controller>` が必要となる。

入力値のチェック
----------------------------------------
* :ref:`入力値のチェック <validation>`

データベースアクセス
----------------------------------------
* :ref:`データベースアクセス <database_management>`

排他制御
----------------------------------------
排他制御は、以下の2種類の方法を提供しているが、
:ref:`UniversalDaoを推奨する理由 <exclusive_control-deprecated>` に記載がある通り、
:ref:`universal_dao` の使用を推奨する。

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`

ファイルアップロード
----------------------------------------
* :ref:`multipart_handler-read_upload_file`

ファイルダウンロード
----------------------------------------
ファイルダウンロードは、以下の2種類の方法を提供しているが、
:ref:`データバインドを推奨する理由 <data_converter-data_bind_recommend>` に記載がある通り、
:ref:`data_bind` の使用を推奨する。

* :ref:`データバインド機能を使用したファイルダウンロード <data_bind-file_download>`
* :ref:`汎用データフォーマット機能を使用したファイルダウンロード <data_format-file_download>`

大量データのダウンロード時には、 :ref:`universal_dao-lazy_load` を参照し、
データベースの検索結果をヒープ上に展開しないように注意すること。

URIとアクションクラスのマッピング
----------------------------------------
以下の2種類の方法を提供しているが、
:ref:`ルーティングアダプタが推奨である理由<http_request_java_package_mapping-router_adaptor>` に記載がある通り、 :ref:`router_adaptor` の使用を推奨する。

* :ref:`router_adaptor`
* :ref:`http_request_java_package_mapping`

2重サブミット防止
----------------------------------------
* :ref:`2重サブミット防止 <tag-double_submission>`

入力データの保持
----------------------------------------
* :ref:`session_store`

ページネーション
----------------------------------------
データベースから範囲を指定して検索を行う方法は、 :ref:`database_management` を参照。

クライアントサイドについては、プロジェクト要件により仕様が異なるため、フレークワークとしては提供していない。

JSPによる画面の作成
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/jsp_session
  
* :ref:`tag`
* :ref:`jsp_session`

国際化対応
----------------------------------------
静的リソースの多言語化対応については以下を参照。

* :ref:`メッセージの多言語化 <message-multi_lang>`
* :ref:`コード名称の多言語化 <code-use_multilingualization>`

画面表示する文言の言語を切り替えるには、以下の2通りの方法を提供しているが、
:ref:`メッセージタグでの国際化対応 <tag-write_message>` を使用した場合、
画面レイアウトが崩れる可能性がある。
そのため、レイアウト崩れを許容できる場合のみ、 :ref:`メッセージタグでの国際化対応 <tag-write_message>` を使用すること。

* :ref:`メッセージタグでの国際化対応 <tag-write_message>`
* :ref:`言語ごとにリソースのパスを切り替える <tag_change_resource_path_of_lang>`

認証
----------------------------------------
認証については、プロジェクト要件により仕様が異なるため、フレークワークとしては提供していない。
:ref:`authentication` を参考に、プロジェクト要件に合わせてPJで実装する。

認証情報の保持については、以下を参照。

* :ref:`session_store-authentication_data`

認可チェック
----------------------------------------
* :ref:`permission_check`

エラー時の画面遷移とステータスコード
--------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/forward_error_page

* :ref:`ステータスコードに対応したデフォルトの遷移先ページを設定する <HttpErrorHandler_DefaultPage>`
* :ref:`ハンドラで例外クラスに対応したエラーページに遷移させる <forward_error_page-handler>`
* アクションでエラー時の遷移先を指定する

  * 例外クラスに対応した遷移先を定義する (:ref:`on_error_interceptor` 、 :ref:`on_errors_interceptor`)
  * :ref:`1つの例外に対して複数の遷移先を定義する <forward_error_page-try_catch>`
* `ステータスコードの使い分け(外部サイト) <http://qiita.com/kawasima/items/e48180041ace99842779>`_

MOMメッセージ送信
----------------------------------------
* :ref:`同期応答メッセージ送信<mom_system_messaging-sync_message_send>`