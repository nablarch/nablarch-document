.. _jaxrs_response_handler:

JAX-RSレスポンスハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラでは、後続のハンドラ(リソース(アクション)クラスや :ref:`body_convert_handler`)
から戻されたレスポンス情報を、クライアントに返却する。
後続のハンドラで例外及びエラーが送出された場合には、エラー及び例外に対応したレスポンス情報を構築しクライアントに返却する。

本ハンドラでは、以下の処理を行う。

* 例外及びエラー発生時のレスポンス情報の生成を行う。
  詳細は、 :ref:`jaxrs_response_handler-error_response` を参照。
* 例外及びエラー発生時のログ出力を行う。
  詳細は、 :ref:`jaxrs_response_handler-error_log` を参照
* クライアントへのレスポンスの返却を行う。

処理の流れは以下のとおり。

.. image:: ../images/JaxRsResponseHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.jaxrs.JaxRsResponseHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

制約
------------------------------
なし。


.. _jaxrs_response_handler-error_response:

例外及びエラーに応じたレスポンスの生成
--------------------------------------------------
例外及びエラーに応じたレスポンス情報の生成は、 :java:extdoc:`errorResponseBuilder <nablarch.fw.jaxrs.JaxRsResponseHandler.setErrorResponseBuilder(nablarch.fw.jaxrs.ErrorResponseBuilder)>` プロパティに設定された
:java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>` により行われる。
ただし、発生した例外クラスが :java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>` の場合は、
:java:extdoc:`HttpErrorResponse#getResponse() <nablarch.fw.web.HttpErrorResponse.getResponse()>` から戻される
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` がクライアントに戻される。

設定を省略した場合は、デフォルト実装の :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>` が使用される。
デフォルト実装では、プロジェクト要件を満たせない場合は、デフォルト実装クラスを継承して対応すること。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="errorResponseBuilder">
      <component class="sample.SampleErrorResponseBuilder" />
    </property>
  </component>


.. _jaxrs_response_handler-error_log:

例外及びエラーに応じたログ出力
--------------------------------------------------
例外及びエラーに応じたログ出力は :java:extdoc:`errorLogWriter <nablarch.fw.jaxrs.JaxRsResponseHandler.setErrorLogWriter(nablarch.fw.jaxrs.JaxRsErrorLogWriter)>` プロパティに設定された
:java:extdoc:`JaxRsErrorLogWriter <nablarch.fw.jaxrs.JaxRsErrorLogWriter>` により行われる。

設定を省略した場合は、デフォルト実装の :java:extdoc:`JaxRsErrorLogWriter <nablarch.fw.jaxrs.JaxRsErrorLogWriter>` が使用される。
デフォルト実装では、プロジェクト要件を満たせない場合は、デフォルト実装クラスを継承して対応すること。

以下に設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="errorLogWriter">
      <component class="sample.SampleJaxRsErrorLogWriter" />
    </property>
  </component>

拡張例
--------------------------------------------------

.. _jaxrs_response_handler-error_response_body:

エラー時のレスポンスにメッセージを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションエラー発生時など、エラーレスポンスのボディにエラーメッセージを設定して返却したい場合がある。
このような場合は、 :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>` の継承クラスを作成して対応する。

以下に、JSON形式のエラーメッセージをレスポンスに設定する場合の実装例を示す。

.. code-block:: java

  public class SampleErrorResponseBuilder extends ErrorResponseBuilder {

      private final ObjectMapper objectMapper = new ObjectMapper();

      @Override
      public HttpResponse build(final HttpRequest request,
              final ExecutionContext context, final Throwable throwable) {
          if (throwable instanceof ApplicationException) {
              return createResponseBody((ApplicationException) throwable);
          } else {
              return super.build(request, context, throwable);
          }
      }

      private HttpResponse createResponseBody(final ApplicationException ae) {
          final HttpResponse response = new HttpResponse(400);
          response.setContentType(MediaType.APPLICATION_JSON);

          // エラーメッセージの生成処理は省略

          try {
              response.write(objectMapper.writeValueAsString(errorMessages));
          } catch (JsonProcessingException ignored) {
              return new HttpResponse(500);
          }
          return response;
      }
  }

.. _jaxrs_response_handler-individually_error_response:

特定のエラーの場合に個別に定義したエラーレスポンスを返却する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本ハンドラの後続の処理で発生したエラーに対し、
個別にステータスコードやボディを定義したエラーレスポンスを返却したい場合がある。

その場合は以下の手順でエラーレスポンスを生成・返却する。

1. リソースクラスでは、プロジェクト側で新規作成した例外クラスを送出する。
2. :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>` の継承クラスを作成し、
   送出された例外がプロジェクト側で新規作成した例外クラスだった場合の処理を実装する。

実装例を以下に示す。

リソースクラス
  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public List<Project> find(HttpRequest request) {

        try {
            // 業務処理は省略
        } catch (ApplicationException e) {
            throw new SampleException(e);
        }
    }

ErrorResponseBuilder継承クラス
  .. code-block:: java

    public class SampleErrorResponseBuilder extends ErrorResponseBuilder {

        @Override
        public HttpResponse build(final HttpRequest request,
                final ExecutionContext context, final Throwable throwable) {
            if (throwable instanceof SampleException) {
                // レスポンスの生成処理は省略
            } else {
                return super.build(request, context, throwable);
            }
        }
    }