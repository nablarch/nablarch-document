.. _router_adaptor:

Routing Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Adapter that performs mapping between request URL and business action using `http-request-router (external site) <https://github.com/kawasima/http-request-router>`_ .
By using this adapter, mapping of URL and business action can be easily defined when building :ref:`Web application <web_application>` or :ref:`RESTful web service <restful_web_service>`.

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- Routing adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-router-adaptor</artifactId>
  </dependency>

.. tip::
  
  Tests are conducted using http-request-router version 0.1.1. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the routing adapter
--------------------------------------------------
The procedure for using this adapter is shown below.

Configure the dispatch handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configure :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` as the dispatch handler at the end of the handler queue.

The configuration example shown below.

Point
 * The component name should be **packageMapping** .
 * Configure the package in which the action class is stored in basePackage attribute. (If the action class is stored in multiple packages, configure a common parent package.)
 * Configure :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` in the initialization list.

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="basePackage" value="sample.web.action" />
  </component>

  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- Other handlers are omitted -->
        <component-ref name="packageMapping" />
      </list>
    </property>
  </component>

  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- Other initialization processes are omitted -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

Create a route definition file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creates `routes.xml` directly under the class path and configures the configurations to map the specified URL and business action.

For the configuration method to the route definition file, see `Library README document (external site) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ .

Automatically map business actions and URLs
--------------------------------------------------------
Business action and URL can be automatically mapped by using parameters such as ``:controller`` and ``:action`` in the path attribute of `match` tag in the route definition file.

.. important::

  This feature is not available when using `JBoss` or `WildFly` as the application server. 
  Define the mapping between business action and URL individually using `get` tag, etc.
  
.. important::

  Using this function together with individual definition of mapping using `get` tag, etc. is not recommended. 
  This is because of the difficultly in reading how the business action and URL are mapped from the route definition file when used together.

To enable this function, create `routes.properties` in the router directory `net/unit8/http/router` created directly under the class path, and configure the values as follows.

.. code-block:: bash

  router.controllerDetector=nablarch.integration.router.NablarchControllerDetector

An example of setting and mapping to the route definition file is shown below.

Route definition file
  .. code-block:: xml

    <routes>
      <match path="/action/:controller/:action" />
    </routes>

Example of mapping URL to business action
  ========================== ===========================
  Business action            URL
  ========================== ===========================
  PersonAction#index         /action/person/index
  PersonAction#search        /action/person/search
  LoginAction#index          /action/login/index
  ProjectUploadAction#index  /action/projectUpload/index
  ========================== ===========================

.. _router_adaptor_path_annotation:

Mapping in Jakarta RESTful Web Services Path Annotation
-------------------------------------------------------------
Since version 1.2.0 of this adapter, it is possible to map routing using the ``jakarta.ws.rs.Path`` annotation (hereafter referred to as ``Path`` annotation) in Jakarta RESTful Web Services.

This section describes how to enable routing with ``Path`` annotations for existing :ref:`RESTful Web Service <restful_web_service>` and details of the various configurations.


.. important::

  This feature is not available on some web application servers where resources under the classpath are managed by the web application server's unique file system.

  For example, in Jboss and Wildfly, the resources under the classpath are managed by a virtual file system called vfs, which makes it impossible to search for classes annotated with ``Path`` annotations.

  If use such a web application server, use the existing XML-based routing definition.

Changing the dispatch handlers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When using XML mapping definitions, :java:extdoc:`RoutesMapping <nablarch.integration.router.RoutesMapping>` is used as the dispatcher's implementation.
On the other hand, when using mapping definitions with Path annotations, :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` needs to be set up as a dispatcher handler.

.. code-block:: xml

  <!-- Configuration example for enabling routing definitions with Path annotation -->
  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="pathOptionsProvider">
      <component class="nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider">
        <property name="applicationPath" value="${nablarch.webApi.applicationPath}" />
        <property name="basePackage" value="${nablarch.commonProperty.basePackage}" />
      </component>
    </property>

    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>
  </component>

  <!-- Handler queue configuration -->
  <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- Omitted -->
        <component-ref name="packageMapping"/>
      </list>
    </property>
  </component>

| To use routing with ``Path`` annotations, configure ``pathOptionsProvider`` property of :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` to be :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>` .
| (See :ref:`jaxrs_adaptor` for information on setting ``methodBinderFactory`` property.

In addition, this :java:extdoc:`JaxRsPathOptionsProvider <nablarch.integration.router.jaxrs.JaxRsPathOptionsProvider>`  needs to be set to two properties.

**applicationPath**

  | Specify a common prefix for the path to be mapped.
  | This means the same value as in ``jakarta.ws.rs.ApplicationPath`` annotation in Jakarta RESTful Web Services.

**basePackage**

  | Specify the name of the package to be the root in searching for classes with the ``Path`` annotation.

:java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` component defined needs to be initialized and added to the list of objects to be initialized.

.. code-block:: xml

  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="packageMapping" />
        <!-- Omitted -->
      </list>
    </property>
  </component>

The above configuration enables the ability to register the routing by ``Path`` annotation.

How to implement the mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following is an example implementation that defines the mapping using the ``Path`` annotation.

.. code-block:: java

    @Path("/sample")
    public class SampleAction {

        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public List<Person> findAll() {
            // Omitted
        }

        @POST
        @Produces(MediaType.APPLICATION_JSON)
        public int register(HttpRequest request) {
            // Omitted
        }
    }

| By annotating the action class with a ``Path`` annotation, we can associate the path set in the ``value`` of the ``Path`` annotation with the action class.
| In addition, can map a HTTP method to methods in the action class by annotating methods in the action class with a corresponding annotation of HTTP method such as ``jakarta.ws.rs.GET`` .

In the above example implementation, the HTTP request will be dispatched as follows


============ ============== =============================
Path         HTTP method    Method of dispatching target
============ ============== =============================
``/sample``   ``GET``        ``SampleAction#findAll()``
``/sample``   ``POST``       ``SampleAction#register(HttpRequest)``
============ ============== =============================

.. tip::
 The following annotations mapping the HTTP method are provided by default.

  * ``jakarta.ws.rs.DELETE``
  * ``jakarta.ws.rs.GET``
  * ``jakarta.ws.rs.HEAD``
  * ``jakarta.ws.rs.OPTIONS``
  * ``jakarta.ws.rs.PATCH``
  * ``jakarta.ws.rs.POST``
  * ``jakarta.ws.rs.PUT``

In addition, you can also define a subpath mapping by annotating the method with a ``Path`` annotation as follows.

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo() {
            // Omitted
        }

        @GET
        @Path("/bar")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar() {
            // Omitted
        }
    }

In this case, the dispatch of the HTTP request would be as follows.

================ ============== =============================
Path             HTTP method    Method of dispatching target
================ ============== =============================
``/sample/foo``   ``GET``       ``SampleAction#findAll()``
``/sample/bar``   ``GET``       ``SampleAction#register(HttpRequest)``
================ ============== =============================

Definition of path parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Can also include parameters in the path, as follows

.. code-block:: java

    @Path("/sample")
    public class TestAction {

        @GET
        @Path("/foo/{param}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person foo(HttpRequest request) {
            String param = request.getParam("param")[0];
            // Omitted
        }

        @GET
        @Path("/bar/{id : \\d+}")
        @Produces(MediaType.APPLICATION_JSON)
        public Person bar(HttpRequest request) {
            int id = Integer.parseInt(request.getParam("id")[0]);
            // Omitted
        }
    }

| The path parameter should be written in accordance with the Jakarta RESTful Web Services specification, not in the http-request-router syntax.
| This is because this feature (routing definition with ``Path`` annotations) follows the Jakarta RESTful Web Services specification.

| By describing a part of the path as ``{parameter name}``, can define that part of the path as a parameter.
| Can get the value of the path parameter by passing the parameter name defined here to :java:extdoc:`HttpRequest#getParam(String) <nablarch.fw.web.HttpRequest.getParam(java.lang.String)>` .

| In addition, can define the format of the path parameter in a regular expression by describing it as ``{parameter name: regular expression}``.
| In the example implementation above, set the regular expression to ``\\d+``, so the method will be dispatched only if the path value is a number.

An example of HTTP request dispatch would be as follows.

===================== ============== =============================
Path                  HTTP method    Method of dispatching target
===================== ============== =============================
``/sample/foo/hello`` ``GET``        ``SampleAction#foo(HttpRequest)``
``/sample/foo/world`` ``GET``        ``SampleAction#foo(HttpRequest)``
``/sample/bar/123``   ``GET``        ``SampleAction#bar(HttpRequest)``
``/sample/bar/987``   ``GET``        ``SampleAction#bar(HttpRequest)``
===================== ============== =============================

See the list of routing definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Routing definitions loaded by :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` are logged at the debug level during initialization.

By default, the routing list is output to the log as follows.

.. code-block:: text

    2020-07-20 13:35:53.092 -DEBUG- nablarch.integration.router.PathOptionsProviderRoutesMapping [null] boot_proc = [] proc_sys = [jaxrs] req_id = [null] usr_id = [null] GET /api/bar => com.example.BarAction#findAll
    GET /api/bar/fizz => com.example.BarAction#fizz
    GET /api/foo => com.example.FooAction#findAll
    POST /api/foo => com.example.FooAction#register
    DELETE /api/foo/(:id) => com.example.FooAction#delete
    GET /api/foo/(:id) => com.example.FooAction#find
    POST /api/foo/(:id) => com.example.FooAction#update

If want to change the format of the log, write a class that implements :java:extdoc:`PathOptionsFormatter <nablarch.integration.router.PathOptionsFormatter>` and configure the ``PathOptionsFormatter`` property of :java:extdoc:`PathOptionsProviderRoutesMapping <nablarch.integration.router.PathOptionsProviderRoutesMapping>` .

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.PathOptionsProviderRoutesMapping">
    <property name="methodBinderFactory">
      <!-- Omitted -->
    </property>
    <property name="pathOptionsProvider">
      <!-- Omitted -->
    </property>

    <property name="pathOptionsFormatter">
      <!-- Configure your custom formatting class -->
      <component class="com.example.CustomPathOptionsFormatter" />
    </property>
  </component>
