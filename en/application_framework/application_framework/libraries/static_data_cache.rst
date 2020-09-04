Static Data Cache
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides a cache function to speed up access to static data stored in databases and files.

This function does not work independently.
To cache static data, implement the data load process by referring to :ref:`static_data_cache-load_data`.

.. important::

  This function holds the cached data in the heap.
  When a large quantity of data is to be cached, note that the frequent occurrence of full GC that might adversely affect the performance.

Function overview
--------------------------------------------------
Arbitrary data can be cached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By implementing the interface provided by this function, arbitrary data can be cached easily.

The data cache is controlled by the class provided by this function.
Therefore, when new data is to be cached, it is sufficient to implement only the data loading process.
A significant advantage is that implementation of a synchronization process like in a multi-thread environment is not required.

For details, see :ref:`static_data_cache-load_data`.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _static_data_cache-load_data:

Cache arbitrarily data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following operations are necessary to cache arbitrary static data.

#. Implement the :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` interface and then implement the process to load data.
#. Configure the implementation class of :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` to :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>`.
#. Configure  :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` to the class that uses the cache.

The detailed procedure is shown below.

Create a loader by implementing the StaticDataLoader interface
  Implement :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` and then implement the process that loads the static data from any arbitrary store.

  Although there are many methods of implementation, implementation based on the following rules is recommended.

  :loadAll: Implement while performing batch loading during system startup. In other cases, `return null` can be used.
  :getValue: Load data corresponding to the ID that uniquely identifies the static data.
             This method is called when there is no data in the cache.
  :Method other than the above: Used to manage the static data for each index.
                       As a general rule, this function is not used, as the implementation method is complicated and using it has no advantage.

                       For implementation, `return null` can be used.

Configure the loader in the BasicStaticDataCache class
  Configure the loader implementing :java:extdoc:`StaticDataLoader <nablarch.core.cache.StaticDataLoader>` to :java:extdoc:`BasicStaticDataCache.loader <nablarch.core.cache.BasicStaticDataCache.setLoader(nablarch.core.cache.StaticDataLoader)>`.

  For configuration example, see :ref:`configuration file example of static data cache <static_data_cache-config_sample>`.

  .. important::

    As done even in the implementation example, :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` must be configured in the initialization target.
    For details of initialization, see :ref:`repository-initialize_object`.

Configure BasicStaticDataCache to the class using the cache.
  Cached data can be accessed by configuring :java:extdoc:`BasicStaticDataCache <nablarch.core.cache.BasicStaticDataCache>` which has a loader in the class that uses the cache.


  An example showing the class that uses the cache is given below.

  In this example, the cached data is acquired using the configured :java:extdoc:`StaticDataCache <nablarch.core.cache.StaticDataCache>`.

  For configuration example, see  :ref:`configuration file example of static data cache <static_data_cache-config_sample>`.

  .. code-block:: java

    public class SampleService {

      private StaticDataCache<Integer> sampleCache;

      public int calc(int n) {
          return sampleCache.getValue(n);
      }

      public void setSampleCache(StaticDataCache<Integer> sampleCache) {
          this.sampleCache = sampleCache;
      }
    }

.. _static_data_cache-config_sample:

Configuration file example
  .. code-block:: xml

    <!-- Loader -->
    <component name="sampleLoader" class="sample.SampleLoader" />

    <!-- BasicStaticDataCache that caches the data loaded by the loader -->
    <component name="sampleDataCache" class="nablarch.core.cache.BasicStaticDataCache">
      <property name="loader" ref="sampleLoader" />
    </component>

    <!--
    Class that uses the cache loaded by the loader.
    Access the cache using BasicStaticDataCache configured in this class.
    -->
    <component class="sample.SampleService">
      <property name="sampleCache" ref="sampleDataCache" />
    </component>

    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">

      <property name="initializeList">
        <list>
          <!-- Initialize BasicStaticDataCache -->
          <component-ref name="sampleDataCache" />
        </list>
      </property>

    </component>


.. _static_data_cache-cache_timing:

Control the cache timing of data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The data cache timing can be selected from the following 2 patterns.

* Batch load (all data is cached during startup)
* On-demand load (cached during the first acquisition request)

.. tip::

  As a general rule, there is no problem with batch loading during startup, but if there is a large amount of static data and only a part of it is used, then on-demand loading is a better option.
  For example, on-demand loading is a better option while accessing only a part of the data such as a batch application.


Change the load timing with :java:extdoc:`BasicStaticDataCache.loadOnStartup <nablarch.core.cache.BasicStaticDataCache.setLoadOnStartup(boolean)>` that has configured the loader.
If this property is set to `true`, data is loaded in a batch during startup.

Since `true` is configured in the following example, data is cached in a batch during startup.

.. code-block:: xml

  <component name="sampleLoader" class="sample.SampleLoader" />

  <component name="sampleDataCache" class="nablarch.core.cache.BasicStaticDataCache">
    <property name="loader" ref="sampleLoader" />
    <property name="loadOnStartup" value="true" />
  </component>

