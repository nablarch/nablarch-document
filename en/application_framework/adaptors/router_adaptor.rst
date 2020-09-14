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
  ==================== =====================
  Business action       URL
  ==================== =====================
  PersonAction#index   /action/person/index
  PersonAction#search  /action/person/search
  LoginAction#index    /action/login/index
  ==================== =====================
