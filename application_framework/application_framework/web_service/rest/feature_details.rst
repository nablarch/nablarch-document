機能詳細
========================================
.. contents:: 目次
  :depth: 3
  :local:

Nablarchの初期化
----------------------------------------
:ref:`ウェブアプリケーションのNablarchの初期化 <web_feature_details-nablarch_initialization>` を参照。

.. _rest-request_validation:
 
入力値のチェック
----------------------------------------
* :ref:`入力値のチェック <validation>`

データベースアクセス
----------------------------------------
* :ref:`データベースアクセス <database_management>`

排他制御
----------------------------------------
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`


.. important::

  :ref:`exclusive_control` 機能は、クライアント(taglib)との連動が前提であるため、
  RESTfulウェブサービスでは使用できない。

.. _rest-action_mapping:

URIとリソース(アクション)クラスのマッピング
------------------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/resource_signature

* :ref:`router_adaptor`
* :ref:`リソースクラスのメソッドのシグネチャ <rest_feature_details-method_signature>`

.. _rest-path_query_param:

パスパラメータやクエリーパラメータ
----------------------------------------------------------------------------------------------------
* :ref:`rest_feature_details-path_param`
* :ref:`rest_feature_details-query_param`

国際化対応
----------------------------------------
静的リソースの多言語化対応については以下を参照。

* :ref:`メッセージの多言語化 <message-multi_lang>`
* :ref:`コード名称の多言語化 <code-use_multilingualization>`

認証
----------------------------------------
認証については、プロジェクト要件により仕様が異なるため、フレークワークとしては提供していない。

認可チェック
----------------------------------------
認可チェックについては、プロジェクト要件により仕様が異なるため、フレークワークとしては提供していない。

エラー時に返却するレスポンス
--------------------------------------------------
* :ref:`jaxrs_response_handler`
