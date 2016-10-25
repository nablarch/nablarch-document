.. _on_double_submission_interceptor:

OnDoubleSubmissionインターセプター
=====================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`二重サブミット(同一リクエストの二重送信)のチェック <tag-double_submission_server_side>` を行うインターセプター。

このインターセプターを使用するためには、
:ref:`jspでのformタグによるトークン設定 <tag-double_submission_token_setting>`
が必要である。

インターセプタークラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.OnDoubleSubmission`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

OnDoubleSubmissionを利用する
--------------------------------------------------
:java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` アノテーションを、
アクションのメソッドに対して設定する。

.. code-block:: java

 // 二重サブミットと判定した場合の遷移先をpath属性に指定する。
 @OnDoubleSubmission(path = "/WEB-INF/view/error/userError.jsp")
 public HttpResponse register(HttpRequest req, ExecutionContext ctx) {
     // 省略。
 }

OnDoubleSubmissionのデフォルト値を指定する
--------------------------------------------------
アプリケーション全体で使用する
:java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` アノテーションのデフォルト値を設定する場合は、
:java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>`
をコンポーネント定義に ``doubleSubmissionHandler`` という名前で追加する。

:java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>`
では、アノテーションの属性が指定されなかった場合に、自身のプロパティに設定されたリソースパス、メッセージID、ステータスコードを使用する。

設定例
 .. code-block:: xml

  <component name="doubleSubmissionHandler"
             class="nablarch.common.web.token.BasicDoubleSubmissionHandler">
    <!-- 二重サブミットと判定した場合の遷移先のリソースパス -->
    <property name="path" value="/WEB-INF/view/error/userError.jsp" />
    <!-- 二重サブミットと判定した場合の遷移先画面に表示するエラーメッセージに使用するメッセージID -->
    <property name="messageId" value="DOUBLE_SUBMISSION_ERROR" />
    <!-- 二重サブミットと判定した場合のレスポンスステータス。デフォルトは400 -->
    <property name="statusCode" value="200" />
  </component>

.. important::
 :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>`
 と :java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>` の
 どちらもpathの指定がない場合は、二重サブミットと判定した場合に遷移先が不明なため、システムエラーとなる。

 このため、 :ref:`トークンを使用した二重サブミットの防止 <tag-double_submission_server_side>`
 を使用するアプリケーションでは、必ずどちらかのpathを指定すること。

OnDoubleSubmissionの振る舞いを変更する
--------------------------------------------------
:java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` アノテーションの振る舞いは、
:java:extdoc:`DoubleSubmissionHandler <nablarch.common.web.token.DoubleSubmissionHandler>`
インタフェースを実装することで変更できる。実装したクラスをコンポーネント定義に ``doubleSubmissionHandler`` という名前で追加する。

