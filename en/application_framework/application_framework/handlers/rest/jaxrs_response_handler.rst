.. _jaxrs_response_handler:

JAX-RS Response Handler
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

This handler returns the response information from the subsequent handler (resource (action) class or :ref:`body_convert_handler`) to the client.
If an exception and error is thrown by the subsequent handler, constructs the response information corresponding to the error and exception,
and returns it to the client.

This handler performs the following process.

* Generates the response information when an exception and error occur.
  For details, see :ref:`jaxrs_response_handler-error_response`.
* Generates the log output when exception and error occur.
  For details, see :ref:`jaxrs_response_handler-error_log`.
* Returns the response to the client.

The process flow is as follows.

.. image:: ../images/JaxRsResponseHandler/flow.png
  :scale: 75

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.jaxrs.JaxRsResponseHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

Constraints
------------------------------
None.


.. _jaxrs_response_handler-error_response:

Generate responses in response to exceptions and errors
---------------------------------------------------------------------------
Generation of response information based on the exceptions and errors is performed by :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>`
configured in the :java:extdoc:`errorResponseBuilder <nablarch.fw.jaxrs.JaxRsResponseHandler.setErrorResponseBuilder(nablarch.fw.jaxrs.ErrorResponseBuilder)>` property.
However, when the exception class that has occurred is :java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>`,
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` that is returned from
:java:extdoc:`HttpErrorResponse#getResponse() <nablarch.fw.web.HttpErrorResponse.getResponse()>` is returned to the client.

If the setting is omitted, :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>` of the default implementation will be used.
If the default implementation cannot meet the project requirements, inherit the default implementation class.

A configuration example is shown below.

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="errorResponseBuilder">
      <component class="sample.SampleErrorResponseBuilder" />
    </property>
  </component>

.. important::
  ErrorResponseBuilderは例外及びエラーに応じたレスポンス生成を行う役割のため、ErrorResponseBuilderの処理中に例外が発生するとレスポンスが生成されず、クライアントにレスポンスを返せない状態となる。
  そのため、プロジェクトでErrorResponseBuilderをカスタマイズする場合は、ErrorResponseBuilderの処理中に例外が発生しないように実装すること。
  ErrorResponseBuilderの処理中に例外が発生した場合、フレームワークはErrorResponseBuilderの処理中に発生した例外をWARNレベルで
  ログ出力を行い、ステータスコード500のレスポンスを生成し、後続処理を継続する。

.. _jaxrs_response_handler-error_log:

Log output in response to exceptions and errors
--------------------------------------------------
Log output in response to exceptions and errors is performed by :java:extdoc:`JaxRsErrorLogWriter <nablarch.fw.jaxrs.JaxRsErrorLogWriter>`
configured in the property :java:extdoc:`errorLogWriter <nablarch.fw.jaxrs.JaxRsResponseHandler.setErrorLogWriter(nablarch.fw.jaxrs.JaxRsErrorLogWriter)>`.

If the setting is omitted, :java:extdoc:`JaxRsErrorLogWriter <nablarch.fw.jaxrs.JaxRsErrorLogWriter>` of the default implementation
will be used. If the default implementation cannot meet the project requirements, inherit the default implementation class.

A configuration example is shown below.

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="errorLogWriter">
      <component class="sample.SampleJaxRsErrorLogWriter" />
    </property>
  </component>

Expansion example
--------------------------------------------------

.. _jaxrs_response_handler-error_response_body:

Configure a message in response to an error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In some cases, such as a validation error, etc., the error message may have to be configured in the response body and returned.
For such cases, support by creating an inherited class of :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>`.

An implementation example where a JSON format error message is configured in the response is shown below.

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

          // Generation process of error message is omitted

          try {
              response.write(objectMapper.writeValueAsString(errorMessages));
          } catch (JsonProcessingException ignored) {
              return new HttpResponse(500);
          }
          return response;
      }
  }

.. _jaxrs_response_handler-individually_error_response:

Return individually defined error response for specific errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For errors that occur in the subsequent process after this handler,
error response defined with a particular status code or body may have to be returned.

In such cases, create an inherited class from :java:extdoc:`ErrorResponseBuilder <nablarch.fw.jaxrs.ErrorResponseBuilder>`
and implement the response generation process individually corresponding to the exception thrown.

An implementation example is shown below.

.. code-block:: java

  public class SampleErrorResponseBuilder extends ErrorResponseBuilder {

      @Override
      public HttpResponse build(final HttpRequest request,
              final ExecutionContext context, final Throwable throwable) {
          if (throwable instanceof NoDataException) {
              return new HttpResponse(404);
          } else {
              return super.build(request, context, throwable);
          }
      }
  }

.. _jaxrs_response_handler-response_finisher:

クライアントに返すレスポンスに共通処理を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
正常時やエラー発生時を問わず、クライアントに返すレスポンスに対してCORS対応やセキュリティ対応で共通的にレスポンスヘッダを指定したい場合がある。

そのような場合に対応するため、フレームワークはレスポンスを仕上げる :java:extdoc:`ResponseFinisher <nablarch.fw.jaxrs.ResponseFinisher>` インタフェースを提供している。
レスポンスに共通処理を追加したい場合は、ResponseFinisherインタフェースを実装したクラスを作成し、
本ハンドラのresponseFinishersプロパティに指定すればよい。

実装例と設定例を以下に示す。

.. code-block:: java

  public class CustomResponseFinisher implements ResponseFinisher {
      @Override
      public void finish(HttpRequest request, HttpResponse response, ExecutionContext context) {
          // レスポンスヘッダを設定するなど、共通処理を行う。
      }
  }

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="responseFinishers">
      <list>
        <!-- ResponseFinisherを実装したクラスを指定 -->
        <component class="sample.CustomResponseFinisher" />
      </list>
    </property>
  </component>

セキュリティ関連のレスポンスヘッダを設定する :ref:`secure_handler` のような既存のハンドラをResponseFinisherとして利用したい場合がある。
このような場合に対応するため、ハンドラをResponseFinisherに適用する
:java:extdoc:`AdoptHandlerResponseFinisher <nablarch.fw.jaxrs.AdoptHandlerResponseFinisher>` クラスを提供している。

AdoptHandlerResponseFinisherで使用できるハンドラは、自らレスポンスを作成せず、後続ハンドラが返すレスポンスに変更を加えるハンドラに限定される。

AdoptHandlerResponseFinisherの使用例を下記に示す。

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.JaxRsResponseHandler">
    <property name="responseFinishers">
      <list>
        <!-- AdoptHandlerResponseFinisher -->
        <component class="nablarch.fw.jaxrs.AdoptHandlerResponseFinisher">
          <!-- handlerプロパティにハンドラを指定 -->
          <property name="handler" ref="secureHandler" />
        </component>
      </list>
    </property>
  </component>
