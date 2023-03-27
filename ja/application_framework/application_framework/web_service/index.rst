.. _`web_service`:

ウェブサービス編
==================================================
本章ではNablarchアプリケーションフレームワークを使用してウェブサービスを開発するために必要となる情報を提供する。

Nablarchでは、以下2種類のRESTfulウェブサービス用のフレームワークを提供している。

.. toctree::
  :maxdepth: 1

  rest/index
  http_messaging/index

.. _web_service-recommended_jaxrs:

これらのどちらのフレームワークを使用してもウェブサービスを構築できるが、
以下の理由により :ref:`restful_web_service` を使用してウェブサービスを作成することを推奨する。

理由
  :ref:`restful_web_service` では、 `JSR 339(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=339>`_ で規定されている一部のアノテーションを使用して容易にウェブサービスを構築できる。
  
  一方、 :ref:`http_messaging` はボディ部やHTTPヘッダ、例外制御に以下の制約があり柔軟な設計及び実装ができない。

  * Nablarchの制御用領域がHTTPヘッダやボディ部に必要となる。

    既に構築済みの外部システムと連携するようなウェブサービスを構築する場合に設計及び実装の難易度が高くなる。

  * レスポンスヘッダに設定する項目を容易にカスタマイズ出来ない。

    :ref:`http_messaging_response_building_handler-header` に記載がある通り、レスポンスヘッダの変更したい場合はハンドラ自体を差し替える必要がある。

  * :ref:`data_format` 機能に依存している。
  
    フォーマット定義ファイルを作成する必要があり、開発コストが高くなる。
    また、カスタマイズが容易でなく、入出力データをMapオブジェクトで扱う必要があり、実装ミスを起こしやすい。

  * リクエストボディのパース時の例外が全て単一の例外クラスにマッピングされるため細かく例外ハンドリングできない。

    パース中の例外は全て :java:extdoc:`MessagingException <nablarch.fw.messaging.MessagingException>` として送出されるため、根本原因を元に細かな処理制御を行うことが出来ない。

.. tip::

  :ref:`restful_web_service` と :ref:`http_messaging` で提供している機能の違いは、:ref:`restful_web_service_functional_comparison` を参照。

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison
