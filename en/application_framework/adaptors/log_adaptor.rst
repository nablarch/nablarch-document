.. _log_adaptor:

log Adapter
==================================================
Adapter that delegates the log output process of :ref:`log output function <log>` provided by Nablarch to the following log framework.

* `slf4j (external site) <https://www.slf4j.org/>`_ 
* `JBoss Logging (external site) <https://github.com/jboss-logging>`_

Use an adapter to unify loggers according to customer requests and products to be used. 
When an adapter is used, all log output processing using :ref:`the log output function <log>` of Nablarch is delegated to the selected logging framework.

.. important::

  The log4j adapter that was provided up to Nablarch5u15 uses `log4j1.2 (external site) <https://logging.apache.org/log4j/1.x/>`_. log4j 1.2 is EOL.
  Therefore, the log4j adapter has been deprecated as no fix for the `vulnerability <https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-013606.html>`_ has been published. Use slf4j or JBoss Logging.

.. tip::

  For details on how to configure the logging framework, refer to the product manual.
  
Module list
--------------------------------------------------

slf4j
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

  <!-- slf4j adaptor -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-slf4j-adaptor</artifactId>
  </dependency>
  
.. important::

  With nablarch-slf4j-adaptor, FATAL log level is mapped to ERROR log level because FATAL log level is not supported by slf4j.

.. tip::
  
  Tests are conducted using slf4j version 2.0.11. 
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
