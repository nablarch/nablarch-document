.. _http_access_log_handler:

HTTPアクセスログハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

:ref:`HTTPアクセスログ <http_access_log>` を出力するハンドラ。

本ハンドラでは、以下の処理を行う。

* リクエスト処理開始時のアクセスログ出力を行う
* リクエスト処理完了時のアクセスログ出力を行う

処理の流れは以下のとおり。

.. image:: ../images/HttpAccessLogHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.handler.HttpAccessLogHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
--------------------------------------------------

:ref:`thread_context_handler` より後ろに配置すること
  このハンドラから呼ばれるログ出力の処理内では、通常 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` に保持する内容が必要となる。
  このため、 :ref:`thread_context_handler` より後ろに配置する必要がある。

:ref:`http_error_handler` より前に配置すること
  また、完了時のログ出力にはエラーコードが必要となるため、 :ref:`http_error_handler` より前に配置する必要がある。


アクセスログ出力内容の切り替え
--------------------------------------------------

アクセスログの出力内容の切り替え方法は、 :ref:`log` および :ref:`http_access_log` を参照すること。
