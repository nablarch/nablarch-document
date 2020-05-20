.. _thread_context_clear_handler:

スレッドコンテキスト変数削除ハンドラ
=======================================

.. contents:: 目次
  :depth: 3
  :local:
  
:ref:`thread_context_handler` で設定したスレッドローカル上の変数を削除するハンドラ。

本ハンドラでは、以下の処理を行う。

* :ref:`thread_context_clear_handler-clear`

処理の流れは以下のとおり。

.. image:: ../images/ThreadContextClearHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.threadcontext.ThreadContextClearHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw</artifactId>
  </dependency>

制約
---------------------------------------
本ハンドラは極力手前側に配置すること。
なぜなら往路処理では、本ハンドラより手前のハンドラではスレッドコンテキストにアクセスできなくなるため。

.. _thread_context_clear_handler-clear:

スレッドコンテキストの削除処理
-----------------------------------------------------------
:ref:`thread_context_handler` でスレッドローカル上に設定した値を全て削除する。

