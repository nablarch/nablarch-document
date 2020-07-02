.. _on_errors_interceptor:

OnErrors Interceptor
============================

.. contents:: Table of contents
  :depth: 3
  :local:

Interceptor that returns a specified response when an exception occurs in a business action.
Responses can be specified for multiple exceptions.

This interceptor is enabled by configuring :java:extdoc:`OnErrors <nablarch.fw.web.interceptor.OnErrors>` to the business action method.

Interceptor class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.interceptor.OnErrors`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

Using OnErrors
--------------------------------------------------
:java:extdoc:`OnErrors <nablarch.fw.web.interceptor.OnErrors>` annotation is configured
for the method that processes the request in the business action.

:java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` is used to specify the response to each exception.

An implementation example in which the following exceptions are thrown in the business action method is shown.

* `ApplicationException` (Business error)
* `AuthenticationException` (Authentication error)
* `UserLockedException` (Account locked error. Subclass of `AuthenticationException`)

.. code-block:: java

  @OnErrors({
          @OnError(type = UserLockedException.class, path = "/WEB-INF/view/login/locked.jsp"),
          @OnError(type = AuthenticationException.class, path = "/WEB-INF/view/login/index.jsp"),
          @OnError(type = ApplicationException.class, path = "/WEB-INF/view/login/index.jsp")
  })
  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // Business process is omitted
  }

.. important::

  Since the exceptions are processed in the order defined by :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>`,
  the exceptions of subclasses must be defined first when defining exceptions that have an inheritance relationship.

