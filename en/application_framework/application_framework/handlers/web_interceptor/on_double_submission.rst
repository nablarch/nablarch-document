.. _on_double_submission_interceptor:

OnDoubleSubmission Interceptor
=====================================

.. contents:: Table of contents
  :depth: 3
  :local:

Interceptor that performs :ref:`double submission (same request sent twice) check <tag-double_submission_server_side>`.

To use this interceptor, 
:ref:`Token configuration using form tag in jsp <tag-double_submission_token_setting>` or :ref:`Token configuration using UseToken interceptor <use_token_interceptor>` are necessary.

Interceptor class name
--------------------------------------------------
* :java:extdoc:`nablarch.common.web.token.OnDoubleSubmission`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

Using OnDoubleSubmission
--------------------------------------------------
Configure the :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>`  annotation for the action method.

.. code-block:: java

 // Specify the transition destination in the path attribute when it is determined as double submission.
 @OnDoubleSubmission(path = "/WEB-INF/view/error/userError.jsp")
 public HttpResponse register(HttpRequest req, ExecutionContext ctx) {
     // Omitted.
 }

Specify the default value of OnDoubleSubmission
--------------------------------------------------
To configure the default value of the :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>`  annotation that is used throughout the application, 
add :java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>` to the component definition with the name ``doubleSubmissionHandler``.

If the annotation attribute is not specified in :java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>`, then the resource path, message ID and status code configured in the own property are used.

Configuration example
 .. code-block:: xml

  <component name="doubleSubmissionHandler"
             class="nablarch.common.web.token.BasicDoubleSubmissionHandler">
    <!-- Resource path of the transition destination when double submission is determined -->
    <property name="path" value="/WEB-INF/view/error/userError.jsp" />
    <!-- Message ID used for the error message displayed on the transition destination screen when double submission is determined -->
    <property name="messageId" value="DOUBLE_SUBMISSION_ERROR" />
    <!-- Response status when double submission is determined.Default is 400 -->
    <property name="statusCode" value="200" />
  </component>

.. important::
 If both :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` and  :java:extdoc:`BasicDoubleSubmissionHandler <nablarch.common.web.token.BasicDoubleSubmissionHandler>` do not specify the path, 
 a system error occurs because the transition destination is not known when a double submission is determined.

 One of the paths must be specified in the application that uses :ref:`Prevention of double submission using token <tag-double_submission_server_side>`.

Change the behavior of OnDoubleSubmission
--------------------------------------------------
The behavior of the :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>`  annotation can be changed by implementing the interface :java:extdoc:`DoubleSubmissionHandler <nablarch.common.web.token.DoubleSubmissionHandler>`. 
Add the implemented class to the component definition with the name ``doubleSubmissionHandler``.
