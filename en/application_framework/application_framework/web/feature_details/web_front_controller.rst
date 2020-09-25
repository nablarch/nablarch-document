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
