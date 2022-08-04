.. _use_token_interceptor:

UseTokenインターセプタ
=====================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`二重サブミット(同一リクエストの二重送信)防止 <tag-double_submission_server_side>` のためのトークンを発行するインターセプタ。

このインターセプタが使用されることを想定しているのは、主にJSP以外のテンプレートエンジンを採用している場合である。

JSP以外のテンプレートエンジンでは、このインターセプタの使用に加えてテンプレートでトークンを明示的にhiddenへ埋め込む必要がある。
トークンの埋め込み方は後述する。
なお、JSPを使用している場合は :ref:`tag-form_tag` のuseToken属性でトークン生成とhiddenへの埋め込みが行われる。

トークンをチェックするため後続のアクションに対して
:ref:`on_double_submission_interceptor`
を設定する必要がある。

インターセプタクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.UseToken`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

UseTokenを使用する
--------------------------------------------------
:java:extdoc:`UseToken <nablarch.common.web.token.UseToken>` アノテーションを、
アクションのメソッドに対して設定する。

.. code-block:: java

 @UseToken
 public HttpResponse confirm(HttpRequest req, ExecutionContext ctx) {
     // 省略
 }

また、入力フォームへ明示的にトークンを埋め込む必要がある。

Thymeleafでの実装例
 .. code-block:: xml

  <form th:action="@{/path/to/action}" method="post">
    <input type="hidden" name="nablarch_token" th:value="${nablarch_request_token}" />

この例のようにname属性は"nablarch_token"と設定して、value属性はリクエストスコープから"nablarch_request_token"というキーで取得した値を設定する必要がある。
このname属性とリクエストスコープから値を取得するキーは変更できる。
詳しくは :ref:`サーバ側の二重サブミット防止 <tag-double_submission_server_side>` を参照すること。
