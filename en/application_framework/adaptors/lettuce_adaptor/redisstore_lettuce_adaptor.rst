.. _redisstore_lettuce_adaptor:

Redis Store (Lettus) Adapter
================================================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provide an adapter that allows `Redis (External sites) <https://redis.io/>`_ to be used for the session store.

Using Redis as a session store provides the following advantages over choosing a DB store.

* No need to prepare a table in advance to store session information
* No need to make a batch to remove expired session information

.. _redisstore_minimum_settings:

Running in a minimal configuration
-----------------------------------------------------------------------------------------------
This section describes how to configure it, with the example of connecting to a single Redis instance running on port ``6379`` of the ``localhost`` .

.. tip::
  If want to try it locally, can use Docker to build a Redis instance by executing the following command.
  
  .. code-block:: shell

    > docker run --name redis -d -p 6379:6379 redis:5.0.9
  
  To stop, execute the command as follows.

  .. code-block:: shell

    > docker stop redis


.. _redisstore_minimum_settings_content:

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start using the Redis store with minimal configuration, need to modify the component definitions and configuration values of the application.

.. _redisstore_minimum_settings_how_modify_component_definition:

Modify the component definition file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Describes how to modify the component definition file.

.. code-block:: xml

  <!-- Omitted -->
  <config-file file="nablarch/webui/redisstore-lettuce.config" />
  <config-file file="common.properties" />
  <config-file file="env.properties" />
  
  <!-- Omitted -->
  <import file="nablarch/webui/redisstore-lettuce.xml" />


First, load the following two configuration files, which are provided by the default configuration.

* ``nablarch/webui/redisstore-lettuce.config``
* ``nablarch/webui/redisstore-lettuce.xml``

``redisstore-lettuce.config`` has already declared the default values for the placeholders used in ``redisstore-lettuce.xml`` .

If your application has a configuration file (such as ``env.properties`` ), ``redisstore-lettuce.config`` should be loaded before it.
This way, can override the default placeholder values with the application's configuration file, if necessary.

In addition, by using the methods described in Overriding Environment Dependencies with :ref:`repository-overwrite_environment_configuration_by_os_env_var` , it is possible to switch the destination Redis for each execution environment.

.. tip::

  By default, it is configured to connect to a single Redis instance running on port ``6379`` of the ``localhost`` .


``redisstore-lettuce.xml`` defines the components that are needed to use the Redis store.

If use ``redisstore-lettuce.xml`` , ``nablarch/webui/session-store.xml`` is no longer needed.
If you are generating a project with :ref:`web archetype <firstStepGenerateWebBlankProject>` , you are configured to use ``session-store.xml`` by default, so remove the import of ``session-store.xml`` and import ``redisstore-lettuce.xml`` instead Modify as.


.. code-block:: xml

  <!-- Components that need to be initialized -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- Omitted -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>


Next, add a component of the :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` to the ``initializeList`` of the :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` .

The ``LettuceRedisClientProvider`` component is defined in ``redisstore-lettuce.xml`` under the name ``lettuceRedisClientProvider`` so that it can be configured using name references.

For an explanation of this configuration, see :ref:`redisstore_initialize_client` .

.. code-block:: xml

  <!-- Components that need to be discarded -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- Omitted -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>


In addition, add a component of the :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` to the :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` 's ``disposableList`` .

For an explanation of this configuration, see :ref:`repository-dispose_object` .

.. _redisstore_minimum_settings_how_modify_env_config:

Modify the environment settings values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Describe how to modify the environment setting values.

.. code-block:: properties

  # The default session store name
  nablarch.sessionManager.defaultStoreName=redis


In the project's configuration file, define a configuration item named ``nablarch.sessionManager.defaultStoreName`` and set the value to ``redis`` .

.. tip::

  If you are creating a project with :ref:`web archetype <firstStepGenerateWebBlankProject>` , ``nablarch.sessionManager.defaultStoreName`` is declared in ``src/main/resources/common.properties`` .


Now can use Redis running on port ``6379`` of the ``localhost`` as a session store.

.. _redisstore_redis_client_config:

Configure it for Redis composition
-----------------------------------------------------------------------------------------------
:ref:`redisstore_minimum_settings` showed an example of connecting to a single Redis instance that starts locally.

However, when actually use Redis in production environment, you need to be able to connect to Redis with the following composition.

* Master-Replica composition with Sentinel
* Cluster Composition

This section describes how to change the configuration depending on the Redis composition of the destination.

.. _redisstore_redis_client_config_client_classes:

Client classes prepared per composition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This adapter provides a dedicated client class (a class that implements :java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` ) for each Redis composition to connect to.

:java:extdoc:`LettuceSimpleRedisClient<nablarch.integration.redisstore.lettuce.LettuceSimpleRedisClient>`
  Class used to connect directly to a single Redis instance.

:java:extdoc:`LettuceMasterReplicaRedisClient<nablarch.integration.redisstore.lettuce.LettuceMasterReplicaRedisClient>`
  Class to use when connecting to a Redis instance of Master-Replica composition.
  Use this class to connect through Sentinel.

:java:extdoc:`LettuceClusterRedisClient<nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient>`
  Class used to connect to a Redis instance in a Cluster composition.

Need to configure the client classes to be used from among these according to the Redis composition used by the application.

.. tip::

  These client class components are defined in ``redisstore-lettuce.xml`` and do not need to be defined by the user.

.. _redisstore_redis_client_config_how_select_client:

Configure the client class to be used
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Which client class is used is configurable by the environment setting key ``nablarch.lettuce.clientType`` .

The relationship between the values and the adopted client class is shown in the table below.

================= ======================================
Value             Client class
================= ======================================
``simple``        ``LettuceSimpleRedisClient``
``masterReplica`` ``LettuceMasterReplicaRedisClient``
``cluster``       ``LettuceClusterRedisClient``
================= ======================================

Therefore, can connect to Redis in a Cluster composition by configuring application's configuration file as follows.

.. code-block:: properties

  nablarch.lettuce.clientType=cluster

.. tip::

  The default value for ``nablarch.lettuce.clientType`` is configured to be ``simple`` in ``redisstore-lettuce.config`` .

.. _redisstore_redis_client_config_uri:

Configure the connection URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The information of Redis to connect to is specified by URI.

URI can be configured for each Redis composition with the following environment setting values.
URI can be configured for each Redis composition with the following environment settings keys.

=============== ====================================== ========================================================================================================
Composition     Key                                    The default value (configured in redisstore-lettuce.config)
=============== ====================================== ========================================================================================================
Single          ``nablarch.lettuce.simple.uri``        ``redis://localhost:6379``
Master-Replica  ``nablarch.lettuce.masterReplica.uri`` ``redis-sentinel://localhost:26379,localhost:26380,localhost:26381?sentinelMasterId=masterGroupName``
Cluster         ``nablarch.lettuce.cluster.uriList``   ``redis://localhost:6379,redis://localhost:6380,redis://localhost:6381``
=============== ====================================== ========================================================================================================

The Cluster configuration value is a comma-separated list of URIs to connect to each node.
For more information on the format of individual URIs, see `Lettuce documentation(URI syntax) (external site) <https://redis.github.io/lettuce/user-guide/connecting-redis/#uri-syntax>`_ .

.. _redisstore_redis_client_config_advanced:

Do more advanced configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Only the client class type and URI can be specified in the environment settings values.
If want to do more advanced configuration, need to create a custom client class that inherits from each client class.

In each client class, there is a ``protected`` method to create a Lettuce instance.
The ``protected`` methods provided in each client class are listed in the following table.

=================================== ======================================== ================================================================================================================================================================================================================
Client class                        Method                                   Return value type
=================================== ======================================== ================================================================================================================================================================================================================
``LettuceSimpleRedisClient``        ``createClient()``                       `RedisClient(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisConnection<byte[], byte[]>(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/api/StatefulRedisConnection.html>`_
``LettuceMasterReplicaRedisClient`` ``createClient()``                       `RedisClient(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisMasterReplicaConnection<byte[], byte[]>(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/masterreplica/StatefulRedisMasterReplicaConnection.html>`_
``LettuceClusterRedisClient``       ``createClient()``                       `RedisClusterClient(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/RedisClusterClient.html>`_
\                                   ``createConnection(RedisClusterClient)`` `StatefulRedisClusterConnection<byte[], byte[]>(external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/api/StatefulRedisClusterConnection.html>`_
=================================== ======================================== ================================================================================================================================================================================================================

By overriding these methods in a custom client class and implementing them to return an instance of Lettuce with your own settings, you can make any settings you want.

Can then replace components of the client class by defining components of the custom client class with the same names as the original components.

The component names of each client class are shown in the table below.

=================================== ====================================
Client class                        Component name
=================================== ====================================
``LettuceSimpleRedisClient``        ``lettuceSimpleRedisClient``
``LettuceMasterReplicaRedisClient`` ``lettuceMasterReplicaRedisClient``
``LettuceClusterRedisClient``       ``lettuceClusterRedisClient``
=================================== ====================================

.. _redisstore_redis_client_config_advanced_topology_refresh_example:

Examples: Enable monitoring of Cluster topology updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To describe the implementation and configuration of a custom client class, with an example setting to enable monitoring of the Cluster topology updates.

First, create a custom client class (``CustomClusterRedisClient``) that inherits from the ``LettuceClusterRedisClient`` client class for cluster composition.

.. code-block:: java
  
  package com.nablarch.example.redisstore;
  
  import io.lettuce.core.RedisURI;
  import io.lettuce.core.cluster.ClusterClientOptions;
  import io.lettuce.core.cluster.ClusterTopologyRefreshOptions;
  import io.lettuce.core.cluster.RedisClusterClient;
  import nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient;
  
  import java.time.Duration;
  import java.util.List;
  import java.util.stream.Collectors;
  
  public class CustomClusterRedisClient extends LettuceClusterRedisClient {
  
      @Override
      protected RedisClusterClient createClient() {
          List<RedisURI> redisUriList = uriList.stream().map(RedisURI::create).collect(Collectors.toList());
          RedisClusterClient client = RedisClusterClient.create(redisUriList);
  
          ClusterTopologyRefreshOptions clusterTopologyRefreshOptions = ClusterTopologyRefreshOptions.builder()
                  .enableAllAdaptiveRefreshTriggers()
                  .enablePeriodicRefresh(Duration.ofSeconds(10))
                  .build();
  
          ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
                  .topologyRefreshOptions(clusterTopologyRefreshOptions)
                  .build();
  
          client.setOptions(clusterClientOptions);
  
          return client;
      }
  }


To enable Lettuce to monitor cluster topology updates, you need to set `ClusterTopologyRefreshOptions (external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/ClusterTopologyRefreshOptions.html>`_  to `RedisClusterClient (external site) <https://www.javadoc.io/static/io.lettuce/lettuce-core/5.3.0.RELEASE/io/lettuce/core/cluster/RedisClusterClient.html>`_ with the necessary settings.

Therefore, implement the ``CustomClusterRedisClient`` by overriding ``createClient()`` , which creates a ``RedisClusterClient`` , to return an instance of the ``RedisClusterClient`` with the necessary settings.

.. tip::

  For more information on settings of Lettuce, see `Lettuce documentation(Cluster-specific options) (external site) <https://redis.github.io/lettuce/advanced-usage/#cluster-specific-options>`_ .


Next, define this custom client class as the component.

.. code-block:: xml

  <import file="nablarch/webui/redisstore-lettuce.xml" />

  <component name="lettuceClusterRedisClient" class="com.nablarch.example.redisstore.CustomClusterRedisClient">
    <property name="uriList" ref="redisClusterUriListFactory" />
  </component>


Since the original client class of ``CustomClusterRedisClient`` is ``LettuceClusterRedisClient`` , can override the component by defining it by the name ``lettuceClusterRedisClient`` .

The configuration of the ``uriList`` property is the same as in the original ``redisstore-lettuce.xml`` .
If you create a class that extends another client class, the property settings should be the same as in ``redisstore-lettuce.xml`` .

Now it is possible to monitor the topology updates.

.. _redisstore_mechanism_to_decide_client:

Mechanism for determining the client class to use
-----------------------------------------------------------------------------------------------
In the section :ref:`redisstore_redis_client_config_how_select_client` , we described how the client class to be used can be set using the Environment settings key ``nablarch.lettuce.clientType`` .
In this section, will describe how the client class is determined and the details of the mechanism.

Which of the components of the three client classes is actually used is determined by :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` .

``LettuceRedisClientProvider`` is defined in ``redisstore-lettuce.xml`` as follows.

.. code-block:: xml

  <component name="lettuceRedisClientProvider" class="nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider">
      <property name="clientType" value="${nablarch.lettuce.clientType}" />
      <property name="clientList">
          <list>
              <component-ref name="lettuceSimpleRedisClient" />
              <component-ref name="lettuceMasterReplicaRedisClient" />
              <component-ref name="lettuceClusterRedisClient" />
          </list>
      </property>
  </component>


This class has two properties: ``clientList`` and ``clientType`` .

The ``clientList`` is set to a list of candidate client class components.
And in ``clientType`` , the identifier of the client class to be used is set.

Each client class has a method called ``getType()`` that returns its own identifier.
``LettuceRedisClientProvider`` compares the value set in the ``clientType`` property with the value in ``getType()`` returned by each component set in the ``clientList`` property.
The component whose value matches is then determined to be the actual component to use.

``LettuceRedisClientProvider`` implements :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` and the ``createObject()`` method is implemented to return components of the determined client class ( :java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` ).

.. _redisstore_initialize_client:

Initialize client classes
-----------------------------------------------------------------------------------------------
All three client classes provided by this adapter require initialization to establish a connection to Redis.

Each client class implements :java:extdoc:`Initializable<nablarch.core.repository.initialization.Initializable>` , and a connection to Redis is established by executing the ``initialize()`` method.
Therefore, the component of the client class to be used must be configured for the ``initializeList`` property of :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` .

The actual configuration of the initializeList is achieved by using the function of ``LettuceRedisClientProvider`` component described in :ref:`redisstore_mechanism_to_decide_client` as shown below.

.. code-block:: xml

  <!-- Components that need to be initialized -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- Omitted -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>


In this way, initialize the components of a determined client class without changing the description of the component definition.

Disposal of client classes
-----------------------------------------------------------------------------------------------

Each client class implements :java:extdoc:`Disposable<nablarch.core.repository.disposal.Disposable>` , and its connection to Redis is closed by executing the ``dispose()`` method.
Therefore, by configuring the ``disposableList`` property of the :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` with the components of the client class to be used, the connection to Redis can be closed when the application exits.

.. code-block:: xml

  <!-- Components that need to be disposal -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- Omitted  -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>


Same way as the ``initializeList`` in the ``BasicApplicationInitializer`` , specify ``LettuceRedisClientProvider`` component in the ``disposableList`` property. This will perform the disposal process for the actual client class being used.

.. _redisstore_session_persistence:

How to store session information
-----------------------------------------------------------------------------------------------
Session information stored in Redis is stored with the key ``nablarch.session.<session ID>`` .

The following shows the display of the keys stored in the ``redis-cli`` .

.. code-block:: shell

  127.0.0.1:6379> keys *
  1) "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"


The session information (the list of :java:extdoc:`SessionEntry<nablarch.common.web.session.SessionEntry>`) is stored in binary format, encoded by default with :java:extdoc:`JavaSerializeStateEncoder<nablarch.common.web.session.encoder.JavaSerializeStateEncoder>` .

The encoder used can be changed by defining encoder component named ``serializeEncoder`` .

.. _redisstore_expiration:

How to manage the expiration period
-----------------------------------------------------------------------------------------------
Redis provides a mechanism to set an expiration period for stored keys.
Expired keys are automatically deleted.

This adapter uses the Redis expiration mechanism to manage the expiration of a session.
Therefore, since expired session information is automatically deleted, there is no need to prepare a batch to delete the session information that remains as garbage.

The following shows the expiration period of the session information being checked with the `pttl command (external site) <https://redis.io/docs/latest/commands/pttl/>`_ .

.. code-block:: shell

  127.0.0.1:6379> pttl "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"
  (integer) 879774

