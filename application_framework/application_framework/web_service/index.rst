.. _`web_service`:

ウェブサービス編
==================================================
本章ではNablarchアプリケーションフレームワークを利用してウェブサービスを開発するために必要となる情報を提供する。

Nablarchでは、以下2種類のRESTfulウェブサービス用のフレームワークを提供している。

.. toctree::
  :maxdepth: 1

  rest/index
  http_messaging/index

.. _web_service-recommended_jaxrs:

:ref:`restful_web_service` では `JSR 339(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=339>`_ で規定されている
一部のアノテーションを使用して容易にウェブサービスを構築することが出来る。

一方、:ref:`http_messaging` の機能も提供しているが、以下の理由により勧めない。

:ref:`http_messaging` はボディ部やHTTPヘッダーに制約があり、柔軟な設計ができない。
特に、既に構築済みの外部システムと連携するようなウェブサービスを構築する際には、この制約により設計及び実装の難易度が高くなる。

また、 :ref:`data_format` 機能に依存しており、フォーマット定義ファイルを作成する必要があるなど、開発コストが高くなるデメリットがある。

なお、:ref:`http_messaging` で出力されるFATALログには、クライアントからのリクエスト処理中にネットワーク障害によって
TCP接続が切れた場合も含まれる。他のエラーと区別できないため、タイムアウトで処理できなかったことのみを検知したい場合には
この方式は適さない。

.. tip::

  :ref:`restful_web_service` と :ref:`http_messaging` で提供している機能の違いは、:ref:`restful_web_service_functional_comparison` を参照。

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison
