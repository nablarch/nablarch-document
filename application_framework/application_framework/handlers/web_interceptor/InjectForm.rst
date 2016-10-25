.. _inject_form_interceptor:

InjectForm インターセプター
============================

.. contents:: 目次
  :depth: 3
  :local:

入力値に対するバリデーションを行い、生成したフォームオブジェクトをリクエストスコープに設定するインターセプター。

このインターセプターは、業務アクションのメソッドに対して、 :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` を設定することで有効となる。

インターセプタークラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.interceptor.InjectForm`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- 入力値チェックにBeanValidationを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>

  <!-- 入力値チェックにNablarchValidationを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

InjectFormを利用する
--------------------------------------------------
:java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` アノテーションを、業務アクションのリクエストを処理するメソッドに対して設定する。


以下に実装例を示す。

入力画面のhtml例
  .. code-block:: html

    <!-- バリデーション対象外-->
    <input name="flag" type="hidden" />

    <!-- バリデーション対象 -->
    <input name="form.userId" type="text" />
    <input name="form.password" type="password" />

業務アクションの例
  この例では、画面から送信された ``form`` から始まるリクエストパラメータに対してバリデーションが実行される。
  バリーションでエラーが発生しなかった場合は、リクエストスコープに :java:extdoc:`InjectForm#form <nablarch.common.web.interceptor.InjectForm.form()>` で指定したクラスのオブジェクトが格納される。

  リクエストスコープにバリデーション済みのフォームを格納する際に使用する変数名は、 :java:extdoc:`InjectForm#name <nablarch.common.web.interceptor.InjectForm.name()>` に指定する。
  指定しなかった場合は、 ``form`` という変数名でフォームが格納される。

  業務アクションが実行された場合には、必ずリクエストスコープからオブジェクトが取得できる。

  .. code-block:: java

    @InjectForm(form = UserForm.class, prefix = "form", validate = "register")
    @OnError(type = ApplicationException.class, path = "forward://registerForm.jsp")
    public HttpResponse handle(HttpRequest req, ExecutionContext ctx) {

      // リクエストスコープからバリデーション済みのフォームを取得する。
      UserForm form = ctx.getRequestScopedVar("form");

      // formを元に業務処理を行う。
    }


バリデーションエラー時の遷移先を指定する
-------------------------------------------------
バリデーションエラー発生時の遷移先画面は、 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` アノテーションを使用して設定する。

:java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` アノテーションは、:java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` を設定した業務アクションのメソッドに対して設定する。
:java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` が設定されていない場合、バリデーションエラーがシステムエラー扱いとなるため注意すること。

バリデーションエラー発生時に、遷移先画面で表示するデータを取得したい場合は、:ref:`on_error-forward` を参照。
