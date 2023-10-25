.. _web_thymeleaf_adaptor:

Web Application Thymeleaf Adapter
========================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter to use `Thymeleaf (external site) <http://www.thymeleaf.org>`_ for the template engine of web application.

Module list
--------------

.. code-block:: xml

  <!-- web application Thymeleaf adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-web-thymeleaf-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using Thymeleaf version 3.1.1 RELEASE. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the web application Thymeleaf adapter
------------------------------------------------------------------

To use this adapter, configure :java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` to :java:extdoc:`HttpResponseHandler<nablarch.fw.web.handler.HttpResponseHandler>`  in the component configuration file.

``TemplateEngine``  provided by Thymeleaf has to be configured in ``ThymeleafResponseWriter``.

The configuration example of the component configuration file is shown below.

.. code-block:: xml

  <component name="templateEngine" class="org.thymeleaf.TemplateEngine" autowireType="None">
    <property name="templateResolver">
      <component class="org.thymeleaf.templateresolver.ClassLoaderTemplateResolver">
        <property name="prefix" value="template/"/>
      </component>
    </property>
  </component>

  <component name="thymeleafResponseWriter"
             class="nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter"
             autowireType="None">
    <property name="templateEngine" ref="templateEngine" />
  </component>

  <component name="httpResponseHandler"
             class="nablarch.fw.web.handler.HttpResponseHandler">
    <property name="customResponseWriter" ref="thymeleafResponseWriter"/>
    <!-- Other settings are omitted -->
  </component>


.. tip::

  Though ``org.thymeleaf.templateresolver.ServletContextTemplateResolver``  is present in the implementation class of ``ITemplateResolver`` , it cannot be registered to the :ref:`repository` for the following reasons:

  * ``jakarta.servlet.ServletContext`` is required as a constructor argument (it has no default constructor).
  * ``jakarta.servlet.ServletContext`` cannot be accessed when building a system repository and objects cannot be created by :ref:`factory <repository-factory_injection>`.

  For this reason, use another implementation class such as ``ClassLoaderTemplateResolver``  and not ``ServletContextTemplateResolver`` .

Determine processing target 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
:java:extdoc:`ThymeleafResponseWriter<nablarch.fw.web.handler.responsewriter.thymeleaf.ThymeleafResponseWriter>` determines whether to output a response using the template engine based on the content path of :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` . 
If the content path ends with ``.html`` by default, it is determined to be a target for processing and output by the template engine.

For example, suppose ``HttpResponse`` is returned in the action class as follows.

.. code-block:: java

  return new HttpResponse("template/index.html");

In this case, since the content path (\ ``template/index.html``\ ) ends with ``.html`` , it is determined to be an output target of the template engine.

If it is not determined to be a target for processing, template engine does not output and servlet forward is executed. 
For example, in the following example, the servlet forward is executed because the content path does not end with ``.html`` .

.. code-block:: java

  return new HttpResponse("/path/to/anotherServlet");

  
The configuration of the determination condition for target of processing can be changed.
A regular expression used for judgment can be configured in property pathPattern (default value is * \.html).
If the content path matches the regular expression, it is determined to be a target for processing by the template engine.

.. important::

  Though Thymeleaf allows the suffix to be omitted when resolving the template path, do not omit the suffix when using this adapter.

  * OK: ``return new HttpResponse("index.html");``
  * NG: ``return new HttpResponse("index");``

  If the suffix is omitted, transfer is not performed from the session store to the request scope, and the template can no longer reference values from session store.

Using a template engine
------------------------------

To use the template engine, a template file needs to be created and placed.

Where to place the template file depends on the ``TemplateEngine`` configuration.
In the configuration example shown in the previous section, the template file is loaded from the class path.
Since  ``prefix``  such as  ``template/`` is configured in the property prefix of  ``ClassLoaderTemplateResolver`` , place the template file under the  ``template``  directory of the class path.

To output a response using the placed template, return ``HttpResponse`` , which specifies the path to the template file, as the return value of the action class.

For example, assume that a template file ``index.html``  is placed in  ``src/main/resources/template`` . 
In this case, the template file will be located in ``template/index.html`` of the class path, and the action class returns the ``HttpResponse`` with this path.

If the prefix is specified as in the previous configuration example, then specify the path without the prefix.

.. code-block:: java

  return new HttpResponse("index.html");


If a prefix is not specified, specify the without omitting the path.

.. code-block:: java

  return new HttpResponse("template/index.html");


With this, a response is output using the template file that has been placed.