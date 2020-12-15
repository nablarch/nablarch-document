.. _redishealthchecker_lettuce_adaptor:

Redis Health Checker (Lettus) adapter
================================================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides adapters that enable `Redis(External sites) <https://redis.io/>`_ health checks.
See :ref:`health_check_endpoint_handler` for health checks.

You can add health checks by creating a class that inherits from :java:extdoc:`HealthChecker <nablarch.fw.web.handler.health.HealthChecker>` , described in :ref:`health_check_endpoint_handler-add_health_checker` .
The adapter offers :java:extdoc:`RedisHealthChecker <nablarch.integration.health.RedisHealthChecker>` , a successor to HealthChecker.

.. _redishealthchecker_lettuce_adaptor_settings:

Perform a redis health check
-----------------------------------------------------------------------------------------------
Redis health checks can be implemented by specifying RedisHealthChecker in the healthCheckers property of the HealthCheckEndpointHandler.

An example configuration is shown below.

.. code-block:: xml

    <!-- Health Check Endpoint Handler -->
    <component class="nablarch.fw.web.handler.HealthCheckEndpointHandler">
      <!-- The healthCheckers property is specified in a list -->
      <property name="healthCheckers">
        <list>
          <!-- Redis Health Check -->
          <component class="nablarch.integration.health.RedisHealthChecker">
            <!-- Specifies the Redis client (LettuceRedisClient) -->
            <property name="client" ref="lettuceRedisClient" />
          </component>
        </list>
      </property>
    </component>

The RedisHealthChecker uses the :java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` to check for the existence of the key and judge the health check to be successful if no exception is thrown.
The key need not exist.
For LettuceRedisClient, refer to the :ref:`redisstore_redis_client_config_client_classes` .
If want to change the key, specify it in the key property of RedisHealthChecker.


.. code-block:: xml

    <!-- Redis Health Check -->
    <component class="nablarch.integration.health.RedisHealthChecker">
      <!-- Specifies the Redis client (LettuceRedisClient) -->
      <property name="client" ref="lettuceRedisClient" />
      <!-- Specify Key -->
      <property name="key" ref="pingtest" />
    </component>
