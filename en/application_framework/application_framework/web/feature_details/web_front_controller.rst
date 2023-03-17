.. _web_front_controller:

Web Front Controller
==================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

The class from which the handler queue is executed in the web application.

This class can delegate the processing of the request received from the client to the handler queue.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

Configure a handler queue
--------------------------------------------------
This section describes the procedure for delegating the processing of a request to the handler queue.

Configure in the component configuration file
  Configure :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` in the component configuration file,
  add the handlers used by the application to :java:extdoc:`handlerQueue <nablarch.fw.HandlerQueueManager.setHandlerQueue(java.util.Collection)>`
  property in order.

  The configuration example of the component configuration file is shown below.

  Point
   * The component name should be **webFrontController** .

  .. code-block:: xml

    <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>

          <!-- Omitted -->

        </list>
      </property>
    </component>

Configure servlet filters
  Configure :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>`
  to `web.xml` as a servlet filter.
  This filter delegates the processing of the request received from the client to the handler queue that is registered earlier in the system repository.

  A configuration example for `web.xml` is shown below.

  Point
   * To initialize the system repository, configure :ref:`nablarch_servlet_context_listener` as a listener.

  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>entryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>

    <filter-mapping>
      <filter-name>entryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
    </filter-mapping>

.. _change_web_front_controller_name:

Change the name of the delegating web front controller
--------------------------------------------------------------

  For example, if you want to process some requests as RESTful web services in a web application-based application.
  There may be a case where you want to use a web application and a web service together.
  In such a case, it is necessary to define multiple web front controllers with different handler configurations.
  :java:extdoc:`RepositoryBasedWebFrontController <nablarch.fw.web.servlet.RepositoryBasedWebFrontController>` is by default
  Get the web front controller transferred from the system repository with the name ``webFrontController``.
  You can change the name of the web front controller retrieved from the system repository by setting initialization parameters in `web.xml`.

  An example web front controller configuration with two handler configurations, one for web applications and one for RESTful web services, is shown below.

  First, in the component definition, set the web front controller with a handler configuration for a web application named ``webFrontController`` 
  and the web front controller with a handler configuration for a RESTful web service named a component name different from ``webFrontController``.

  .. code-block:: xml

    <component name="webFrontController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- Handler configuration for web applications -->
        </list>
      </property>
    </component>

    <component name="jaxrsController"
              class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <!-- Handler configuration for RESTful web services -->
        </list>
      </property>
    </component>

  Next, set up a servlet filter in `web.xml` to use the web front controller set up above.

  Point
   * Use ``<init-param>`` to set the parameter ``controllerName`` to the name of the controller to retrieve from the system repository.
   * Set the URL pattern to be processed by each web front controller in ``<filter-mapping>``.
  
  .. code-block:: xml

    <context-param>
      <param-name>di.config</param-name>
      <param-value>web-boot.xml</param-value>
    </context-param>

    <listener>
      <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
    </listener>

    <filter>
      <filter-name>webEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
    </filter>
    <filter>
      <filter-name>jaxrsEntryPoint</filter-name>
      <filter-class>nablarch.fw.web.servlet.RepositoryBasedWebFrontController</filter-class>
      <init-param>
        <param-name>controllerName</param-name>
        <param-value>jaxrsController</param-value>
      </init-param>
    </filter>

    <filter-mapping>
      <filter-name>webEntryPoint</filter-name>
      <url-pattern>/action/*</url-pattern>
      <url-pattern>/</url-pattern>
    </filter-mapping>
    <filter-mapping>
      <filter-name>jaxrsEntryPoint</filter-name>
      <url-pattern>/api/*</url-pattern>
    </filter-mapping>

