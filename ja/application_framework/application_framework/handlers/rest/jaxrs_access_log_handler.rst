.. _jaxrs_access_log_handler:

HTTPアクセスログ（RESTfulウェブサービス用）ハンドラ
======================================================
.. contents:: 目次
  :depth: 3
  :local:

:ref:`HTTPアクセスログ（RESTfulウェブサービス用） <jaxrs_access_log>` を出力するハンドラ。

本ハンドラでは、以下の処理を行う。

* リクエスト処理開始時のアクセスログを出力する
* リクエスト処理完了時のアクセスログを出力する

処理の流れは以下のとおり。

.. image:: ../images/HttpAccessLogHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.jaxrs.JaxRsAccessLogHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

制約
--------------------------------------------------

:ref:`thread_context_handler` より後ろに配置すること
  このハンドラから呼ばれるログ出力の処理内では、通常 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` に保持する内容が必要となる。
  このため、 :ref:`thread_context_handler` より後ろに配置する必要がある。

:ref:`http_error_handler` より前に配置すること
  また、完了時のログ出力にはエラーコードが必要となるため、 :ref:`http_error_handler` より前に配置する必要がある。

セッションストアIDを出力する場合は :ref:`session_store_handler` より後ろに配置すること
  詳細は :ref:`jaxrs_access_log-session_store_id` を参照。

アクセスログ出力内容の切り替え
--------------------------------------------------

アクセスログの出力内容の切り替え方法は、 :ref:`log` および :ref:`jaxrs_access_log` を参照すること。
