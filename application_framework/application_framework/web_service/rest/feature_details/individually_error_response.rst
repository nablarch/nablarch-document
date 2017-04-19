.. _rest_feature_details-individually_error_response:

個別に生成したエラーレスポンスを返却する
==================================================

リソースクラス内で業務エラーが発生した場合に、リソースクラスごとに個別に生成したエラーレスポンスを返却したい場合がある。

その場合、エラーレスポンスの生成を :ref:`jaxrs_response_handler` で行うのではなく、
リソースクラス内で直接 :java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>` を送出して対応する。

以下に、JSON形式のエラーメッセージを設定したエラーレスポンスを返却する際の実装例を示す。

.. code-block:: java

  @Produces(MediaType.APPLICATION_JSON)
  public List<Project> find(HttpRequest request) {

      try {
          // 業務処理は省略
      } catch (ApplicationException e) {
          final HttpResponse response = new HttpResponse(400);
          response.setContentType(MediaType.APPLICATION_JSON);

          // エラーメッセージの生成処理は省略

          try {
              response.write(objectMapper.writeValueAsString(errorMessages));
          } catch (JsonProcessingException ignored) {
              throw new HttpErrorResponse(new HttpResponse(500));
          }
          throw new HttpErrorResponse(response);
      }
  }