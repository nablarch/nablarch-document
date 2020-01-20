=========================================
 Webアプリケーションをステートレスにする
=========================================


基本的な考え方
==============

サーブレットAPIが提供するHttpSessionはAPサーバで状態を持ってしまうため、そのままではスケールアウトができない。
通常、APサーバをスケールアウトを行うには以下のような以下のような対処が必要となる。

1. ロードバランサーでスティッキーセッションを有効にする
2. APサーバのセッションレプリケーション機能を使用する
3. APサーバのHttpSession保存先をNoSQLにする

1, 2は12 Factor Appで言うところの廃棄容易性の点で劣り、2, 3はAPサーバ依存となる。

Nablarchが使用する機能では、HttpSessionに依存しているものがあるが、
これらの機能をHttpSession非依存のものに切り替えることで、
APサーバをステートレスにすることができる。

※ローカルファイルシステムへの依存なども考慮しないと


HttpSessionに依存している機能
=============================

以下の機能は、デフォルトではHttpSessionに依存している。

* :ref:`session_store`
* :ref:`2重サブミット防止<tag-double_submission>`
* :ref:`thread_context_handler`
  
  * :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`
  * :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`
  * :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`
* :ref:`http_rewrite_handler`
* :ref:`hidden暗号化<tag-hidden_encryption>`


HttpSession非依存機能の導入方法
===============================


セッションストア
~~~~~~~~~~~~~~~~

2重サブミット防止
~~~~~~~~~~~~~~~~~

スレッドコンテキスト変数管理ハンドラ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTTPリライトハンドラ
~~~~~~~~~~~~~~~~~~~~


hidden暗号化
~~~~~~~~~~~~

