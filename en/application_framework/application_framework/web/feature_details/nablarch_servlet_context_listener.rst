.. _nablarch_servlet_context_listener:

Nablarch Servlet Context Initialization Listener
==================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

This class is defined as a servlet context listener,
and performs the following operations when the launching or exiting the web application.

At startup
 * Initialization process for :ref:`repository`
 * Initialization process for :ref:`log`

At completion
 * Termination process for :ref:`log`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-applog</artifactId>
  </dependency>

Initializing the system repository
--------------------------------------------------

To initialize the system repository, the following must be configured.

* This class is registered as a servlet context listener.
* The path of the component configuration file is configured as an initialization parameter of the servlet context.

A configuration example for `web.xml` is shown below.

Point
 * The parameter name of the path of the component configuration file should be  **di.config** .

.. code-block:: xml

  <context-param>
    <param-name>di.config</param-name>
    <param-value>web-boot.xml</param-value>
  </context-param>

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>
  
Get the success or failure of the initialization in the subsequent process
----------------------------------------------------------------------------------------------------

Whether the initialization of this class has succeeded or not 
can be obtained by using :java:extdoc:`NablarchServletContextListener#isInitializationCompleted <nablarch.fw.web.servlet.NablarchServletContextListener.isInitializationCompleted()>`.
If the initialization is successful, the above method returns ``true``.

If the initialization of this class fails, the application will also fail to start, 
but if multiple servlet context listeners have been registered, the processing of 
the servlet context listeners following this class may be executed.
This function makes it possible for the servlet context listener after this class 
to make a branch that continues processing only if the system repository is 
successfully initialized, as follows.

.. code-block:: java

  public class CustomServletContextListener implements ServletContextListener {
      @Override
      public void contextInitialized(ServletContextEvent sce) {
          if(NablarchServletContextListener.isInitializationCompleted()){
            // Processing using the system repository
          }
      }

The order of execution of servlet context listeners is the order described in `web.xml`.
If you register a servlet context listener that uses the system repository, 
you need to describe it in `web.xml` after this class as follows.
Also, the order of execution is not guaranteed when registering servlet context listener 
by ``@WebListener`` annotation, so be sure to define it in `web.xml`.

.. code-block:: xml

  <listener>
    <listener-class>nablarch.fw.web.servlet.NablarchServletContextListener</listener-class>
  </listener>
  <listener>
    <listener-class>please.change.me.CustomServletContextListener</listener-class>
  </listener>

.. tip::

  When multiple servlet context listeners are registered,
  whether to detect an exception in the processing of the previously executed servlet context listener and abort the processing,
  or to ignore the exception and continue the processing of the subsequent servlet context listener
  depends on the implementation of the servlet container.