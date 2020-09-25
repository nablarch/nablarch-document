.. _on_error_interceptor:

OnErrorインターセプター
============================

.. contents:: 目次
  :depth: 3
  :local:

業務アクションでの例外発生時に、指定したレスポンスを返却するインターセプター。

:ref:`inject_form_interceptor` を使用して入力値チェックを行う場合も、
:ref:`inject_form_interceptor` よりも前にこのインターセプターが実行されるように設定することで、
バリデーションエラーに対するレスポンスを指定することができる。

このインターセプターは、業務アクションのメソッドに対して、 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` を設定することで有効となる。

.. tip::

  複数の例外に対するレスポンスを指定したい場合は、 :ref:`on_errors_interceptor` を使用すること。

.. important::

  単一の例外に対して複数のレスポンスを指定することはできない。
  例外に対して複数のレスポンスを指定したい場合は、 :ref:`on_error-multiple` を参照。
  
インターセプタークラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.interceptor.OnError`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

OnErrorを利用する
--------------------------------------------------
:java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` アノテーションを、
業務アクションのリクエストを処理するメソッドに対して設定する。

以下の例では、業務アクションのメソッド内で業務エラー( `ApplicationException` )が発生した場合の遷移先を指定している。

ポイント
 * type属性には、`RuntimeException` 及びそのサブクラスを指定することができる。
 * type属性に指定した例外のサブクラスも処理の対象となる。

.. code-block:: java

  @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // 業務処理は省略
  }

.. _on_error-forward:

エラー時の遷移先画面に表示するデータを取得する
------------------------------------------------------------
プルダウンの選択肢のように、エラー時の遷移先画面に表示するデータをデータベースなどから取得したい場合がある。

この場合は、表示データを取得する業務アクションのメソッドに対して内部フォーワードを行い、
初期表示用のデータをデータベースなどから取得し、リクエストスコープに設定する。

詳細は :ref:`forwarding_handler`  を参照。

バリデーションエラー発生時に初期表示用のメソッドにフォワードする場合の実装例を以下に示す。

ポイント
 * path属性に、内部フォワード用のパスを設定する。

.. code-block:: java

  /**
   * 入力値のチェックを行う業務アクションのメソッド。
   */
  @InjectForm(form = PersonForm.class, prefix = "form")
  @OnError(type = ApplicationException.class, path = "forward://initializeRegisterPage")
  public HttpResponse confirmForRegister(HttpRequest request, ExecutionContext context) {

    PersonForm form = context.getRequestScopedVar("form");

    return new HttpResponse("/WEB-INF/view/person/confirmForRegister.jsp");
  }

  /**
   * 登録画面の初期表示データを取得するメソッド。
   */
  public HttpResponse initializeRegisterPage(HttpRequest request, ExecutionContext context) {
    // 画面表示データをデータベースなどから取得し、リクエストスコープに設定する

    return new HttpResponse("/WEB-INF/view/person/inputForRegister.jsp");
  }

.. _on_error-multiple:

複数のレスポンスを指定する
--------------------------------------------------
本インターセプターでは、単一の例外に対して複数のレスポンスを指定することはできないため、
複数のレスポンスを指定したい場合は、業務アクションのメソッド内に個別に :java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>` を生成する必要がある。

以下に実装例を示す。

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      try {
          // 業務処理は省略
      } catch (ApplicationException e) {
          if (/* 条件式を記述 */) {
              return new HttpErrorResponse("/WEB-INF/view/project/index.jsp");
          } else {
              return new HttpErrorResponse("/WEB-INF/view/error.jsp");
          }
      }
  }