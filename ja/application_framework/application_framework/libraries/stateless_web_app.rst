.. _`stateless_web_app`:

Webアプリケーションをステートレスにする
=====================================================================

.. contents:: 目次
  :depth: 3

基本的な考え方
--------------------------------------------------

サーブレットAPIが提供するHTTPセッションはAPサーバで状態を持ってしまうため、そのままではスケールアウトができない。
通常、APサーバのスケールアウトを行うには以下のような対処が必要となる。

1. ロードバランサーでスティッキーセッションを有効にする
2. APサーバのセッションレプリケーション機能を使用する
3. APサーバのHTTPセッション保存先をNoSQLにする

1, 2は `Twelve-Factor App <https://12factor.net/ja/>`_ で言うところの廃棄容易性の点で劣り、2, 3はAPサーバ依存となる。

Nablarchが使用する機能では、HTTPセッションに依存しているものがあるが、
これらの機能をHTTPセッション非依存のものに切り替えることで、
APサーバをステートレスにできる。

.. _http-session-dependence:

HTTPセッションに依存している機能
--------------------------------------------------

以下の機能は、デフォルトではHTTPセッションに依存している。

* :ref:`session_store`
* :ref:`2重サブミット防止<tag-double_submission>`
* :ref:`thread_context_handler`
* :ref:`http_rewrite_handler`
* :ref:`hidden暗号化<tag-hidden_encryption>`

HTTPセッション非依存機能の導入方法
--------------------------------------------------

:ref:`http-session-dependence` の各機能について以下の通り設定することでHTTPセッションへの依存をなくすことができる。

セッションストア
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_managed_expiration`

2重サブミット防止
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_double_submit` 

スレッドコンテキスト変数管理ハンドラ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`スレッドコンテキストの初期化<thread_context_handler-initialization>` に以下の部品を使用しない。

* :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`
* :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`
* :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`


それぞれ、HTTPセッションを使用しない実装として以下の部品で代替できる。

* :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
* :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
* :java:extdoc:`UserIdAttributeInSessionStore <nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore>`

HTTPリライトハンドラ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`http_rewrite_handler` を使用しない。
使用する場合にはセッションスコープにアクセスしないよう設定する。

hidden暗号化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nablarchでは :ref:`hidden暗号化<tag-hidden_encryption>` の機能を提供している。
この機能はHTTPセッションに依存しているため、使用しないよう :ref:`useHiddenEncryption <tag-use_hidden_encryption>` に ``false`` を設定する。

ローカルファイルシステムの使用
--------------------------------------------------
アップロードしたファイルなどをAPサーバのローカルに保存してしまうと、ステートを持つことになってしまう。
このような場合は、共有のストレージを用意するなどして、APサーバがローカルにファイルを持たないようにする必要がある。

HTTPセッションの誤生成を検知する
--------------------------------------------------
設定漏れや実装ミスによって誤ってHTTPセッションを生成してしまうことを防ぐために、HTTPセッションの生成を検知する機能を提供している。
この機能を有効にすると、HTTPセッションを生成しようとしたときに例外が送出されるようになる。

この機能は、 :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` の ``preventSessionCreation`` プロパティに ``true`` を設定することで有効にできる（デフォルトは ``false`` で無効になっている）。

具体的には、 :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` のコンポーネントを定義した設定ファイルで、次のように記述することで検知機能を有効にできる。

.. code-block:: xml

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">

    <!-- HTTPセッションの誤生成を検知する -->
    <property name="preventSessionCreation" value="true" />
