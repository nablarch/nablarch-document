.. _use_token_interceptor:

UseTokenインターセプター
=====================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`二重サブミット(同一リクエストの二重送信)防止 <tag-double_submission_server_side>` のためのトークン発行を行うインターセプター。

このインターセプターが使用されることを想定しているのは、主にJSP以外のテンプレートエンジンを採用している場合である。
JSPを使用している場合は :ref:`tag-form_tag` のuseToken属性で同様の効果を得られる。

インターセプタークラス名
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
