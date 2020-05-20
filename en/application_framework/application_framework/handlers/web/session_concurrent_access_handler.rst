.. _session_concurrent_access_handler:

セッション並行アクセスハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:


.. important::
  新規プロジェクトにおける本ハンドラの使用は推奨しない。セッション変数保存ハンドラを使用すること。

本ハンドラはセッションごとにリクエスト処理の並行同時アクセスに対して、同時実行に
よって発生するスレッド間の処理不整合を防ぐ機能を提供する。


本ハンドラでは、以下の処理を行う。

* セッションに保持した情報のコピーを作成する
* 処理終了後、他のスレッドによってセッションが更新されていないかチェックし、更新済みであればエラーとする
* 処理終了後、セッション情報のコピーをセッションに反映する


.. image:: ../images/SessionConcurrentAccessHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.SessionConcurrentAccessHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
------------------------------

なし。

