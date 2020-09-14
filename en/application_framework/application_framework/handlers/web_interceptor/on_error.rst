.. _on_error_interceptor:

OnError Interceptor
============================

.. contents:: Table of contents
  :depth: 3
  :local:

Interceptor that returns a specified response when an exception occurs in a business action.

Even when performing the input value check using :ref:`inject_form_interceptor` , 
by configuring such that the interceptor is executed before the :ref:`inject_form_interceptor` , 
the response for the validation error can be specified.

This interceptor is enabled by configuring  :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>`  to the business action method.

.. tip::

  Use  :ref:`on_errors_interceptor`  to specify the response for multiple exceptions.

.. important::

  Multiple responses cannot be specified for a single exception. 
  To specify multiple responses for exceptions, see  :ref:`on_error-multiple` .
  
Interceptor class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.interceptor.OnError`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

Using OnError
--------------------------------------------------
The :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>`  annotation is configured for the method that processes the business action request.

In the following example, the transition destination when a business error ( `ApplicationException` ) occurs in the business action method is specified.

Point
 * `RuntimeException` and its subclass can be specified in the type attribute.
 * The subclass of the exception specified in the type attribute is also processed.

.. code-block:: java

  @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // Business process is omitted
  }

.. _on_error-forward:

Acquire the data to be displayed on the transition destination screen when an error occurs
--------------------------------------------------------------------------------------------------
Users may want to obtain the data to be displayed on the transition destination screen from a database using options such as pull-down when an error occurs.

In this case, data for initial display is acquired from the database by performing internal forward for the business action method that acquires the display data, etc. and configured in the request scope.

For details, see :ref:`forwarding_handler`  .

An implementation example for forwarding to the initial display method when a validation error occurs is shown below.

Point
 * Configure the internal forward path in the path attribute.

.. code-block:: java

  / **
   * Business action method to check the input value.
   */
  @InjectForm(form = PersonForm.class, prefix = "form")
  @OnError(type = ApplicationException.class, path = "forward://initializeRegisterPage")
  public HttpResponse confirmForRegister(HttpRequest request, ExecutionContext context) {

    PersonForm form = context.getRequestScopedVar("form");

    return new HttpResponse("/WEB-INF/view/person/confirmForRegister.jsp");
  }

  / **
   * Method to acquire the initial display data of registration screen.
   */
  public HttpResponse initializeRegisterPage(HttpRequest request, ExecutionContext context) {
    // Obtain the screen display data from the database, etc. and configure in the request scope

    return new HttpResponse("/WEB-INF/view/person/inputForRegister.jsp");
  }

.. _on_error-multiple:

Specify multiple responses
--------------------------------------------------
Since this interceptor cannot specify multiple responses for a single exception, 
:java:extdoc:`HttpErrorResponse <nablarch.fw.web.HttpErrorResponse>`  has to be separately generated in the business action method to specify multiple responses.

An implementation example is shown below.

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      try {
          // Business process is omitted
      } catch (ApplicationException e) {
          if (/* Write conditional expression */) {
              return new HttpErrorResponse("/WEB-INF/view/project/index.jsp");
          } else {
              return new HttpErrorResponse("/WEB-INF/view/error.jsp");
          }
      }
  }