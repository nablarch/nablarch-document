.. _view_other:

Screen Development Using Other Template Engines
==================================================
This section describes how to use template engines other than :ref:`web_thymeleaf_adaptor`.

If the template engine to be used provides a Servlet for returning a response to the client using Servlet forward,
it can be handled by registering the Servlet in ``web.xml``.

In the case of a template engine that does not provide Servlet,
like :ref:`web_thymeleaf_adaptor`, it can be handled by creating an implementation class of :java:extdoc:`CustomResponseWriter <nablarch.fw.web.handler.responsewriter.CustomResponseWriter>`.

Refer to the following manuals and source codes for details on the implementation and configuration methods.

* :ref:`web_thymeleaf_adaptor` 
* `Source code for the web application Thymeleaf adapter <https://github.com/nablarch/nablarch-web-thymeleaf-adaptor>`_
