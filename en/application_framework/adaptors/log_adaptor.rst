.. _log_adaptor:

log Adapter
==================================================
Adapter that delegates the log output process of :ref:`log output function <log>` provided by Nablarch to the following log framework.

* `log4j (external site, English) <http://logging.apache.org/log4j/1.2/>`_ 
* `slf4j (external site, English) <https://www.slf4j.org/>`_ 
* `JBoss Logging (external site, English) <https://github.com/jboss-logging>`_

Use an adapter to unify loggers according to customer requests and products to be used. 
When an adapter is used, all log output processing using :ref:`the log output function <log>` of Nablarch is delegated to the selected logging framework.

.. tip::

  For details on how to configure the logging framework, refer to the product manual.
  
Module list
--------------------------------------------------

log4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- log4j adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-log4j-adaptor</artifactId>
  </dependency>
  
.. tip::
  
  Tests are conducted using log4j version 1.2.16. 
  When changing the version, test in the project to confirm that there are no problems.
  
slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- slf4j adaptor -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-slf4j-adaptor</artifactId>
  </dependency>
  
.. tip::
  
  Tests are conducted using slf4j version 1.7.22. 
  When changing the version, test in the project to confirm that there are no problems.


JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- JBoss Logging adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jboss-logging-adaptor</artifactId>
  </dependency>
  
.. tip::
  
  Tests are conducted using JBoss Logging version 3.3.0 Final. 
  When changing the version, test in the project to confirm that there are no problems.
  
Configuration settings for using the logging framework
----------------------------------------------------------
Configure the following in the configuration file (\ **log.properties**\ ) of :ref:`log output function <log>`. 
With this configuration, the log output process is delegated to the logging framework.

log4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # configure factory to use log4j
  loggerFactory.className=nablarch.integration.log.log4j.Log4JLoggerFactory

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # configure factory to use slf4j
  loggerFactory.className=nablarch.integration.log.slf4j.Slf4JLoggerFactory
  
JBoss Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: properties

  # configure factory to use JBoss Logging
  loggerFactory.className=nablarch.integration.log.jbosslogging.JbossLoggingLoggerFactory
