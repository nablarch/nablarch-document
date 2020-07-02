.. _inject_form_interceptor:

InjectForm Interceptor
============================

.. contents:: Table of contents
  :depth: 3
  :local:

This interceptor validates the input values and sets the generated form object in the request scope.

This interceptor is enabled by configuring :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` for the business action method.

Interceptor class name
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.interceptor.InjectForm`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- Only when BeanValidation is used for input value check -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>

  <!-- Only when NablarchValidation is used for input value check -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

Using InjectForm
--------------------------------------------------
Configure the :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` annotation for the method that processes the business action request.


An implementation example is shown below.

HTML example of input screen
  .. code-block:: html

    <!-- Validation is not covered-->
    <input name="flag" type="hidden" />

    <!-- Validation is covered -->
    <input name="form.userId" type="text" />
    <input name="form.password" type="password" />

Example of business action
  In this example, validation is executed for the request parameters starting from the ``form`` sent from the screen.
  If there are no errors during validation, the object of the class specified by :java:extdoc:`InjectForm#form <nablarch.common.web.interceptor.InjectForm.form()>` is stored in the request scope.

  Variable name used when storing the validated form in the request scope is specified in :java:extdoc:`InjectForm#name <nablarch.common.web.interceptor.InjectForm.name()>`.
  If the variable name is not specified, the ``form`` is stored with the variable name form.

  When a business action is executed, an object can always be acquired from the request scope.

  .. code-block:: java

    @InjectForm(form = UserForm.class, prefix = "form", validate = "register")
    @OnError(type = ApplicationException.class, path = "forward://registerForm.jsp")
    public HttpResponse handle(HttpRequest req, ExecutionContext ctx) {

      // Obtain the validated form from the request scope.
      UserForm form = ctx.getRequestScopedVar("form");

      // Perform the business process based on the form.
    }


.. tip::
  If :ref:`bean_validation` is used for validation, it can be configured such that the objects can be fetched
  from the request scope even during validation errors. For details, see \ :ref:`bean_validation_onerror`\.
    
Specify the transition destination when a validation error occurs
-------------------------------------------------------------------
The transition destination screen when a validation error occurs is configured using the :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` annotation.

Configure for :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` for the business action method to which :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` that has been configured for the business action method.
Note that if :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` is not configured, validation error is handled as a system error.

To acquire data for display on the transition destination screen when a validation error occurs, see :ref:`on_error-forward`.
