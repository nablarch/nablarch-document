.. _slf4j_adaptor:

SLF4J Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

A lot of Java OSS modules use `SLF4J(external site) <https://www.slf4j.org/>`_  for logging, and if you use these modules, you may want to aggregate the log output into Nablarch's :ref:`Log Output function<log>`.
To address this case, provide an adapter to log output in Nablarch's log output function via the SLF4J API.

Module list
--------------------------------------------------

.. code-block:: xml

  <!-- SLF4J Adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
  </dependency>

.. tip::

  Tested with SLF4J 2.0.11.
  If you change the version, the project should be tested on the project side to make sure it is working.
  Note that the search method for logging implementation has changed since version 2.0.0 of SLF4J. For example, if an incompatible version 1.7 series is used, the following logs will be output, and no further log output will be performed.

  .. code-block:: none

    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.  

Using SLF4J Adapter
--------------------------------------------------
This adapter can be used simply by adding the SLF4J adapter to the project's dependent modules, as SLF4J automatically detects the classes needed at runtime.
See Nablarch's :ref:`Log Output function <log>` for log output settings.

.. code-block:: xml

  <!-- SLF4J Adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
    <scope>runtime</scope>
  </dependency>
