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