.. _micrometer_adaptor:

Micrometer Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter to perform metrics collection using `Micrometer (external site) <https://micrometer.io/>`_ .

This adapter can be used to do the following. This provides the advantage of easier operational monitoring of the application.

* Can collect application metrics such as JVM memory usage and CPU usage.
* The collected metrics can be linked to monitoring services such as `Datadog (external site) <https://www.datadoghq.com/>`_ and `CloudWatch (external site) <https://aws.amazon.com/cloudwatch/>`_ .


Module list
--------------------------------------------------
.. code-block:: xml

  <!-- Micrometer adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-micrometer-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using Micrometer version 1.5.4.
  If you change the version, the project  should be tested to make sure it is working.

Setting up to use the Micrometer adapter
--------------------------------------------------
In order to collect metrics in Micrometer, need to create a class called `Registry (external site) <https://micrometer.io/docs/concepts#_registry>`_ .
This adapter provides a :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` to register this registry in the System Repository.

In this section,  describe how to set up :java:extdoc:`LoggingMeterRegistryFactory<nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>` as an example, registering `LoggingMeterRegistry (external site)`_ as a component.

.. tip::

  `LoggingMeterRegistry (external site)`_ provides the feature to log metrics using SLF4J or Java Util Logging.
  When no specific configuration is made, metrics are output to standard output using Java Util Logging, which is useful for a quick behavior check.

  Other registries require a lot of work to prepare the services to be federated and to create an implementation to output the collected metrics.
  For this reason, we have used `LoggingMeterRegistry (external site)`_ , which is the easiest to behavior check.

In this example, use `Web application Example (external site) <https://github.com/nablarch/nablarch-example-web>`_ as the base application.


Declare the DefaultsMeterBinderListProvider as a component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Micrometer has an interface called `MeterBinder (external site)`_  .

The collection of frequently used metrics, such as JVM memory usage and CPU usage, is provided in advance as a class that implements this interface.
(e.g., `JvmMemoryMetrics (external site)`_ for JVM memory usage and `ProcessorMetrics (external site)`_ for CPU usage)

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` is a class that provides this `MeterBinder (external site)`_ list , which can be used to collect metrics such as JVM memory usage and CPU usage.

First, add this :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` declaration to ``src/main/resources/web-component-configuration.xml`` .

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="nablarch.integration.micrometer.DefaultMeterBinderListProvider" />


For a specific description of the metrics that are collected, see :ref:`micrometer_default_metrics` .


Target the DefaultsMeterBinderListProvider for disposal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Because the :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` is a component that needs to be disposed of, declare it for disposal as follows.

.. code-block:: xml
  
  <component name="disposer"
      class="nablarch.core.repository.disposal.BasicApplicationDisposer">

    <property name="disposableList">
      <list>
        <component-ref name="meterBinderListProvider"/>
      </list>
    </property>

  </component>


For the object disposal process, see :ref:`repository-dispose_object` .


Declare the registry's factory class as a component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <component class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />
  </component>

Next, declare the factory class as a component, which is provided for each registry to be used.

In doing so, configure two properties, ``meterBinderListProvider`` and ``applicationDisposer`` .
For each property, configure :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` and :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` as declared above.

The factory classes provided by this adapter are listed in :ref:`micrometer_registry_factory` .


Creating a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, create a text file named ``micrometer.properties`` under ``src/main/resources`` .

Describe the contents as follows.

.. code-block:: properties

  # Output metrics every 5 seconds
  nablarch.micrometer.logging.step=5s

.. important::

  ``micrometer.properties`` must be placed even if the content is empty.


.. _micrometer_metrics_output_example:

Execution Result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Now you can collect metrics using the ``LoggingMeterRegistry`` .

Launching the application, can see that the collected metrics are output to standard output as follows

.. code-block:: text

  2020-09-04 15:33:40.689 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS Scavenge} throughput=2.6/s
  2020-09-04 15:33:40.690 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS MarkSweep} throughput=0.4/s
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=mapped} value=0 buffers
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=direct} value=2 buffers
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=direct} value=124 KiB
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=direct} value=124 KiB
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.classes.loaded{} value=9932 classes
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.live.data.size{} value=0 B
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.max.data.size{} value=2.65918 GiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Old Gen} value=182.5 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Eden Space} value=197 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Code Cache} value=29.125 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Compressed Class Space} value=6.796875 MiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Metaspace} value=55.789062 MiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Old Gen} value=2.65918 GiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Code Cache} value=240 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Metaspace} value=-1 B
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Eden Space} value=1.243652 GiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Compressed Class Space} value=1 GiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Code Cache} value=28.618713 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Compressed Class Space} value=6.270714 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Metaspace} value=54.118324 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Old Gen} value=69.320663 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Survivor Space} value=7.926674 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Eden Space} value=171.750542 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.daemon{} value=28 threads
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.live{} value=29 threads
  2020-09-04 15:33:40.699 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.peak{} value=31 threads
  2020-09-04 15:33:40.702 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=blocked} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=runnable} value=9 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=new} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=timed-waiting} value=3 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=terminated} value=0 threads
  2020-09-04 15:33:40.704 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=waiting} value=17 threads
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.cpu.usage{} value=0.111672
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{} value=444222h 33m 14.544s
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{} value=26.729s
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{} value=8
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{} value=0.394545



.. _micrometer_registry_factory:

Registry factory
--------------------------------------------------
This adapter provides the following registry factory classes.

.. list-table::

  * - Registry
    - Factory class
    - The version of the adapter being provided
  * - `SimpleMeterRegistry (external site)`_
    - :java:extdoc:`SimpleMeterRegistryFactory <nablarch.integration.micrometer.simple.SimpleMeterRegistryFactory>`
    - ``1.0.0`` or higher
  * - `LoggingMeterRegistry (external site)`_
    - :java:extdoc:`LoggingMeterRegistryFactory <nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>`
    - ``1.0.0`` or higher
  * - `CloudWatchMeterRegistry (external site)`_
    - :java:extdoc:`CloudWatchMeterRegistryFactory <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory>`
    - ``1.0.0`` or higher
  * - `DatadogMeterRegistry (external site)`_
    - :java:extdoc:`DatadogMeterRegistryFactory <nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory>`
    - ``1.0.0`` or higher
  * - `StatsdMeterRegistry (external site)`_
    - :java:extdoc:`StatsdMeterRegistryFactory <nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory>`
    - ``1.0.0`` or higher



.. _micrometer_configuration:

Configuration File
--------------------------------------------------

Placement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a configuration file for this adapter to be placed directly under the classpath with the name ``micrometer.properties`` .

Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Describe it in the following format

.. code-block:: text

  nablarch.micrometer.<subPrefix>.<key>=<value>

The value specified for ``<subPrefix>`` is different for each registry factory used.

For each registry factory, the following table lists the values to specify for ``<subPrefix>``.

=================================== ================
Registry factory                    subPrefix
=================================== ================
``SimpleMeterRegistryFactory``      ``simple``
``LoggingMeterRegistryFactory``     ``logging``
``CloudWatchMeterRegistryFactory``  ``cloudwatch``
``DatadogMeterRegistryFactory``     ``datadog``
``StatsdMeterRegistryFactory``      ``statsd``
=================================== ================

``<key>`` should be the same name as the method defined in `configuration class (external site) <https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/config/MeterRegistryConfig.html>`_  that Micrometer provides per registry.

For example, there is a configuration class named `DatadogConfig (external site)`_ for `DatadogMeterRegistry (external site)`_ .
And in this configuration class, a method named `apyKey (external site) <https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogConfig.html#apiKey()>`_ is defined.

Therefore, can configure your ``apiKey`` by writing in your ``micrometer.properties`` like this.

.. code-block:: text

  nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXXXXXX

Override with OS environment variables or system properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The configuration values in ``micrometer.properties`` can be overridden by OS environment variables or system properties.

The configuration values are adopted in the following order of priority.

#. The value specified in system properties
#. Value specified in OS environment variables
#. Configuration values for ``micrometer.properties``

For example, suppose you have the following conditions set.

micrometer.properties

  .. code-block:: text

    nablarch.micrometer.example.one=PROPERTIES
    nablarch.micrometer.example.two=PROPERTIES
    nablarch.micrometer.example.three=PROPERTIES

OS environment variables

  .. code-block:: text

    $ export NABLARCH_MICROMETER_EXAMPLE_TWO=OS_ENV

    $ export NABLARCH_MICROMETER_EXAMPLE_THREE=OS_ENV

system properties

  .. code-block:: text

    -Dnablarch.micrometer.example.three=SYSTEM_PROP

In this case, each set value will eventually adopt the following values

========== ================
Key        Value adopted
========== ================
``one``    ``PROPERTIES``
``two``    ``OS_ENV``
``three``  ``SYSTEM_PROP``
========== ================

For rules on naming when overwriting with OS environment variables, see :ref:`About the names of OS environment variables <repository-overwrite_environment_configuration_by_os_env_var_naming_rule>` .


Changing the configuration prefix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration prefix (``nablarch.micrometer.<subPrefix>``) can be changed by specifying the :java:extdoc:`prefix <nablarch.integration.micrometer.MeterRegistryFactory.setPrefix(java.lang.String)>` property for each registry factory.

Below is an example of changing the prefix.

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- Configuring the prefix property with an arbitrary prefix -->
    <property name="prefix" value="sample.prefix" />
  </component>

In this case, the ``micrometer.properties`` can be configured as follows

.. code-block:: text

  sample.prefix.step=10s

Changing the place of the configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The place of the configuration file (``micrometer.properties``) can be changed in the following ways.

First, specify the path of the XML file to load the configuration file in :java:extdoc:`xmlConfigPath <nablarch.integration.micrometer.MeterRegistryFactory.setXmlConfigPath(java.lang.String)>` property of the registry factory.

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- Specify the path of the XML file to load the configuration file -->
    <property name="xmlConfigPath" value="config/metrics.xml" />
  </component>


And, place the XML file to load the configuration file at the place specified in the ``xmlConfigPath`` property.
In the following configuration, ``config/metrics.properties`` in the classpath will be loaded as a configuration file.

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">

    <!-- Load Micrometer adapter Configuration -->
    <config-file file="config/metrics.properties" />

  </component-configuration>

.. tip::

  This XML file can be written in the same format as the component configuration file.

  However, even if you define a component in this file, you will not be able to get a reference from the System Repository.


.. _micrometer_default_metrics:

Metrics collected by the DefaultMeterBinderListProvider
-------------------------------------------------------

`MeterBinder (external site)`_ list generated by the :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` contains the following classes.


* `JvmMemoryMetrics (external site)`_
* `JvmGcMetrics (external site)`_
* `JvmThreadMetrics (external site)`_
* `ClassLoaderMetrics (external site)`_
* `ProcessorMetrics (external site)`_
* `FileDescriptorMetrics (external site)`_
* `UptimeMetrics (external site)`_
* :java:extdoc:`NablarchGcCountMetrics <nablarch.integration.micrometer.instrument.binder.jvm.NablarchGcCountMetrics>`



This will enable the following metrics to be collected.

.. list-table::

  * - Metrics Name
    - Description
  * - ``jvm.buffer.count``
    - The number of buffers in the buffer pool
  * - ``jvm.buffer.memory.used``
    - Buffer pool usage
  * - ``jvm.buffer.total.capacity``
    - Total capacity of the buffer pool
  * - ``jvm.memory.used``
    - Memory pool memory usage
  * - ``jvm.memory.committed``
    - The committed amount of memory in the memory pool
  * - ``jvm.memory.max``
    - The maximum amount of memory in the memory pool
  * - ``jvm.gc.max.data.size``
    - The maximum amount of memory in the OLD space
  * - ``jvm.gc.live.data.size``
    - Memory usage in the OLD space after Full GC
  * - ``jvm.gc.memory.promoted``
    - Incremental memory usage in the OLD space, increased before and after GC
  * - ``jvm.gc.memory.allocated``
    - Incremental memory usage in the young space from the previous GC to the current GC
  * - ``jvm.gc.concurrent.phase.time``
    - Concurrent phase processing time
  * - ``jvm.gc.pause``
    - Time spent on GC pause
  * - ``jvm.threads.peak``
    - Peak number of threads
  * - ``jvm.threads.daemon``
    - The number of current daemon threads
  * - ``jvm.threads.live``
    - The number of current non-demon threads
  * - ``jvm.threads.states``
    - The number of current threads per state
  * - ``jvm.classes.loaded``
    - The number of classes currently loaded
  * - ``jvm.classes.unloaded``
    - The number of classes that have been unloaded since the JVM was started
  * - ``system.cpu.count``
    - The number of processors available in the JVM
  * - ``system.load.average.1m``
    - Last minute system load average （Reference: `OperatingSystemMXBean(external site) <https://docs.oracle.com/javase/jp/11/docs/api/java.management/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage()>`_ ）
  * - ``system.cpu.usage``
    - Recent system-wide CPU usage
  * - ``process.cpu.usage``
    - The JVM's recent CPU usage
  * - ``process.files.open``
    - The number of open file descriptors
  * - ``process.files.max``
    - Maximum number of file descriptors
  * - ``process.uptime``
    - JVM uptime
  * - ``process.start.time``
    - JVM startup time (UNIX time)
  * - ``jvm.gc.count``
    - Number of GC

See :ref:`micrometer_metrics_output_example` for an example of the actual metrics to be collected.


Configuring Common Tags
--------------------------------------------------

The :java:extdoc:`tags <nablarch.integration.micrometer.MeterRegistryFactory.setTags(java.util.Map)>` property of the registry factory allows you to configure tags that are common to all metrics.

This feature can be used, for example, to set information that can identify the host, instance, region, etc. on which an application is running.

Describe how to set it up below.

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- Configure common tags in the tags property -->
    <property name="tags">
      <map>
        <entry key="foo" value="FOO" />
        <entry key="bar" value="BAR" />
      </map>
    </property>
  </component>

The ``tags`` property is of type ``Map<String, String>``  and can be configured using a ``<map>`` tag.
In addition, the map key is mapped to the name of the tag and the map value is mapped to the tag value.

In the case of the above setup, the metrics to be collected are as follows.

.. code-block:: text

  （Omitted）
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{bar=BAR,foo=FOO} value=444224h 29m 38.875000064s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{bar=BAR,foo=FOO} value=27.849s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{bar=BAR,foo=FOO} value=8
  2020-09-04 17:30:06.657 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{bar=BAR,foo=FOO} value=0.475654

Can see that all metrics are set with the tags ``foo=FOO``, ``bar=BAR`` .

Working with monitoring services
--------------------------------------------------

In order to work with monitoring services, the following settings need to be made, broadly categorized.

#. Add a Micrometer module for each monitoring service to the dependencies.
#. Define a registry factory for the monitoring service as a component.
#. Configuring other proprietary settings for each monitoring service.

This section describes how to work with each of the monitoring services.


Working with Datadog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding Dependencies
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-datadog</artifactId>
      <version>1.5.4</version>
    </dependency>

Declare the Registry Factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

Configuring the API key
  .. code-block:: text

    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  The API key can be set in ``nablarch.micrometer.datadog.apyKey`` .

  See `DatadogConfig (external site)`_ for other configuration.

Disable the registry
  .. code-block:: text

    nablarch.micrometer.datadog.enabled=false
    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  You can disable the registry by setting ``nablarch.micrometer.datadog.enabled`` to ``false`` in ``micrometer.properties``.
  You can override this configuration by environment variable.
  Therefor, you can enable the registry by setting ``true`` with environment variable only at production.

  .. important::
    Even if you disable the registry, you still need to set some value for ``nablarch.micrometer.datadog.apiKey``.
    You can set dummy value to the ``apiKey``.

Working with CloudWatch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding Dependencies
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-cloudwatch2</artifactId>
      <version>1.5.4</version>
    </dependency>

Declare the Registry Factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

Configure the region, access keys, etc
  .. code-block:: bash
    
    $ export AWS_REGION=ap-northeast-1

    $ export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX

    $ export AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYYYYY

  The ``micrometer-registry-cloudwatch2`` module uses the AWS SDK.
  Therefore, the configuration of the region, access keys, etc. follows the AWS SDK ways.

  The above describes an example of how to set up an OS environment variable in Linux.
  For more information, see the `AWS documentation (external site) <https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html>`_ .

Configuring the namespace
  .. code-block:: text

    nablarch.micrometer.cloudwatch.namespace=test

  Custom metrics namespaces can be configured in ``nablarch.micrometer.cloudwatch.namespace`` .

  See `CloudWatchConfig (external site)`_ for more configuration information.


More detailed configuration
  If want more detailed configuration that cannot be specified in the OS environment variables and configuration files, you can write a custom provider that implements :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` .

  .. code-block:: java

      package example.micrometer.cloudwatch;

      import nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider;
      import software.amazon.awssdk.services.cloudwatch.CloudWatchAsyncClient;

      public class CustomCloudWatchAsyncClientProvider implements CloudWatchAsyncClientProvider {
          @Override
          public CloudWatchAsyncClient provide() {
              return CloudWatchAsyncClient
                      .builder()
                      .asyncConfiguration(...) // Do your own configuration
                      .build();
          }
      }

  :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` has a ``provide()`` method that provides the ``CloudWatchAsyncClient`` .
  A custom provider implements the ``provide()`` method to build and return the ``CloudWatchAsyncClient`` with your desired configuration.

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />

      <!-- Configure a custom provider for the cloudWatchAsyncClientProvider property -->
      <property name="cloudWatchAsyncClientProvider">
        <component class="example.micrometer.cloudwatch.CustomCloudWatchAsyncClientProvider" />
      </property>
    </component>

  The custom provider you write will be configured in the :java:extdoc:`cloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory.setCloudWatchAsyncClientProvider(nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider)>` property of the ``CloudWatchMeterRegistryFactory`` .

  This enables the ``CloudWatchAsyncClient`` generated by the custom provider to be used in the cooperation of the metrics.


  .. tip::

    By default, the instance created by `CloudWatchAsyncClient.create() (external site) <https://javadoc.io/static/software.amazon.awssdk/cloudwatch/2.13.4/software/amazon/awssdk/services/cloudwatch/CloudWatchAsyncClient.html#create-->`_ is used.

Disable the registry
  .. code-block:: text

    nablarch.micrometer.cloudwatch.enabled=false
    nablarch.micrometer.cloudwatch.namespace=test

  You can disable the registry by setting ``nablarch.micrometer.cloudwatch.enabled`` to ``false`` in ``micrometer.properties``.
  You can override this configuration by environment variable.
  Therefor, you can enable the registry by setting ``true`` with environment variable only at production.

  .. important::
    Even if you disable the registry, you still need to set some value for ``nablarch.micrometer.cloudwatch.namespace``.
    You also need to set the environment variable ``AWS_REGION``.

    You can set dummy values to the ``namespace`` and ``AWS_REGION``.

Working with Azure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How to send metrics to Azure with Micrometer
  Azure provides the library using the Java agent (**Java 3.0 agent**) for sending metrics from Java applications to Azure.

  * `Java codeless application monitoring Azure Monitor Application Insights(external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in-process-agent>`_

  The Java 3.0 agent automatically collects metrics output to Micrometer's `Global Registry(external site) <https://micrometer.io/docs/concepts#_global_registry>`_, and sends to Azure.

  * `Send custom telemetry from your application(external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in-process-agent#send-custom-telemetry-from-your-application>`_

How to configure Micrometer adaptor
  You need to configure following settings to send metrics to Azure with Micrometer adaptor.

  * Add the Java 3.0 agent to your application's JVM args
  * Define a ``MeterRegistry`` component using the Global Registry

  See the `Azure documentation(external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in-process-agent#quickstart>`_ for how to set JVM args.

  This adaptor provides :java:extdoc:`GlobalMeterRegistryFactory <nablarch.integration.micrometer.GlobalMeterRegistryFactory>` for factory of Global Registry component.
  The following is an example of a component definition for this factory class.

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.GlobalMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

  This configuration makes the Global Registry to collect metrics.
  The Java 3.0 agent sends metrics collected by the Global Registry to Azure.

  .. tip::
    ``MeterRegistry`` is not used in this approach using Java 3.0 agent.
    Therefore, you can send metrics without additional dependent modules for Azure.

Configuration
  The metrics are sent by the Java 3.0 agent provided by Azure.
  Therefore, you must use configuration options provided by the Java 3.0 agent.

  For more information, see `Configuration Options(external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-standalone-config>`_.

  .. important::
    The configuration file for this adapter, ``micrometer.properties``, is not used.
    However, you must place the ``micrometer.properties`` file (the content can be empty).

Disable the registry
  You can disable to send metrics by launching application without the Java 3.0 agent.

Working with Datadog using StatsD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Datadog supports `DogStatsD (external site) <https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent>`_, which is a cooperation using the `StatsD (external site) <https://github.com/statsd/statsd>`_ protocol. 

Therefore, Can use ``micrometer-registry-statsd`` module to connect to Datadog with StatsD.

In this section, we will use the case of cooperation with Datadog using the StatsD protocol as an example.
For more information on how to install DogStatsD, refer to `Datadog's site (external site) <https://docs.datadoghq.com/agent/>`_ .


Adding Dependencies
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-statsd</artifactId>
      <version>1.5.4</version>
    </dependency>

Declare the Registry Factory
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

Write a configuration file if necessary
  The configuration for working with the StatsD daemon has been adjusted so that the default values match those of DogStatsD installed in its default configuration.
  
  Therefore, if DogStatsD is installed in the default configuration, the cooperation by DogStatsD will work without any explicit settings.

  If you have installed a non-default configuration, refer to `StatsdConfig (external site)`_ to configure it for actual environment.

  .. code-block:: text

    # Change Port
    nablarch.micrometer.statsd.port=9999

Disable the registry
  .. code-block:: text

    nablarch.micrometer.statsd.enabled=false

  You can disable the registry by setting ``nablarch.micrometer.statsd.enabled`` to ``false`` in ``micrometer.properties``.
  You can override this configuration by environment variable.
  Therefor, you can enable the registry by setting ``true`` with environment variable only at production.

.. _MeterBinder (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/MeterBinder.html
.. _DatadogConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogConfig.html
.. _CloudWatchConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.5.4/io/micrometer/cloudwatch2/CloudWatchConfig.html
.. _StatsdConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.5.4/io/micrometer/statsd/StatsdConfig.html
.. _MeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/MeterRegistry.html
.. _DatadogMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogMeterRegistry.html
.. _StatsdMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.5.4/io/micrometer/statsd/StatsdMeterRegistry.html
.. _DatadogMeterRegistry (external site: https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogMeterRegistry.html
.. _CloudWatchMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.5.4/io/micrometer/cloudwatch2/CloudWatchMeterRegistry.html
.. _LoggingMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/logging/LoggingMeterRegistry.html
.. _SimpleMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/simple/SimpleMeterRegistry.html
.. _JvmMemoryMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmMemoryMetrics.html
.. _ProcessorMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/ProcessorMetrics.html
.. _JvmGcMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmGcMetrics.html
.. _JvmThreadMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmThreadMetrics.html
.. _ClassLoaderMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/ClassLoaderMetrics.html
.. _FileDescriptorMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/FileDescriptorMetrics.html
.. _UptimeMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/UptimeMetrics.html
