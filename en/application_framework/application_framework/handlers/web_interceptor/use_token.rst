.. _use_token_interceptor:

UseToken Interceptor
=====================================

.. contents:: Table of contents
  :depth: 3
  :local:

Interceptor that issues token for :ref:`double submission (same request sent twice) prevention <tag-double_submission_server_side>` .

This interceptor is expected to be used mainly when a template engine other than JSP is adopted.

In template engines other than JSP, in addition to using this interceptor, it is necessary that the token is explicitly embedded in hidden of the template.
How to embed the token will be described later.
If JSP is used, useToken attribute of  :ref:`tag-form_tag`  is used to generate the token and embed in hidden.

To check tokens, :ref:`on_double_submission_interceptor` has to be configured for subsequent actions.

Interceptor class name
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.UseToken`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

Using UseToken
--------------------------------------------------
Configure the :java:extdoc:`UseToken <nablarch.common.web.token.UseToken>`  annotation for the action method.

.. code-block:: java

 @UseToken
 public HttpResponse confirm(HttpRequest req, ExecutionContext ctx) {
     // Omitted
 }

Tokens must be explicitly embedded in the input form.

Implementation example in Thymeleaf
 .. code-block:: xml

  <form th:action="@{/path/to/action}" method="post">
    <input type="hidden" name="nablarch_token" th:value="${nablarch_request_token}" />

As in this example, it is necessary to configure "nablarch_token" as the name attribute and the value obtained from the request scope with the key "nablarch_request_token" as the value attribute.
The name attribute and the key to acquire the value from the request scope can be changed.
For details, see  :ref:`prevention of double submission in the server <tag-double_submission_server_side>` .

