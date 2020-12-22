.. _lettuce_adaptor:

Lettuce Adapter
================================================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides adapters to use `Redis(external site) <https://redis.io/>`_ for the following features provided by Nablarch.

- :ref:`session_store`
- :ref:`health_check_endpoint_handler`

This adapter uses `Lettuce (external site) <https://lettuce.io/>`_ as a client library for Redis.

.. _lettuce_adaptor_module_list:

Module List
-----------------------------------------------------------------------------------------------

.. code-block:: xml

  <!-- RedisStore Lettuce Adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-lettuce-adaptor</artifactId>
  </dependency>

  <!-- Default configuration -->
  <dependency>
    <groupId>com.nablarch.configuration</groupId>
    <artifactId>nablarch-main-default-configuration</artifactId>
  </dependency>

.. tip::

  Tested with Redis 5.0.9 and Lettuce 5.3.0.RELEASE.
  If you change the version, the project  should be tested to make sure it is working.

See below for a description of the adapters that support each feature.

.. toctree::
  :maxdepth: 1

  lettuce_adaptor/redisstore_lettuce_adaptor
  lettuce_adaptor/redishealthchecker_lettuce_adaptor
