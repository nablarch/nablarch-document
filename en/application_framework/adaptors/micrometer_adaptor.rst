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

  Tests are conducted using Micrometer version 1.13.0.
  If you change the version, the project  should be tested to make sure it is working.

Setting up to use the Micrometer adapter
--------------------------------------------------
In order to collect metrics in Micrometer, need to create a class called `Registry (external site) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html>`_ .
This adapter provides a :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` to register this registry in the System Repository.

In this section,  describe how to set up :java:extdoc:`LoggingMeterRegistryFactory<nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>` as an example, registering `LoggingMeterRegistry (external site)`_ as a component.

.. tip::

  `LoggingMeterRegistry (external site)`_ provides the feature to log metrics using SLF4J or Java Util Logging.
  When no specific configuration is made, metrics are output to standard output using Java Util Logging, which is useful for a quick behavior check.

  Other registries require a lot of work to prepare the services to be federated and to create an implementation to output the collected metrics.
  For this reason, we have used `LoggingMeterRegistry (external site)`_ , which is the easiest to behavior check.

In this example, use `Web application Example (external site) <https://github.com/nablarch/nablarch-example-web>`_ as the base application.

.. _micrometer_adaptor_declare_default_meter_binder_list_provider_as_component:

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

  # Output metrics every 5 seconds (1 minute in default)
  nablarch.micrometer.logging.step=5s
  # Configuring to output log at disposal process
  # even if the application is terminated earlier than the time specified in step.
  nablarch.micrometer.logging.logInactive=true

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
  * - `OtlpMeterRegistry(external site)`_
    - :java:extdoc:`OtlpMeterRegistryFactory <nablarch.integration.micrometer.otlp.OtlpMeterRegistry>`
    - ``1.3.0`` or higher


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
``OtlpMeterRegistryFactory``        ``otlp``
=================================== ================

``<key>`` should be the same name as the method defined in `configuration class (external site) <https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/config/MeterRegistryConfig.html>`_  that Micrometer provides per registry.

For example, there is a configuration class named `DatadogConfig (external site)`_ for `DatadogMeterRegistry (external site)`_ .
And in this configuration class, a method named `apiKey (external site) <https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html#apiKey()>`_ is defined.

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
    - Last minute system load average （Reference: `OperatingSystemMXBean(external site) <https://docs.oracle.com/en/java/javase/17/docs/api/java.management/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage()>`_ ）
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
  * - ``jvm.threads.started``
    - The total number of application threads started in the JVM
  * - ``process.cpu.time``
    - The "cpu time" used by the Java Virtual Machine process

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

#. Add a Micrometer module prepared for each monitoring service and linking method to the dependencies.
#. Define a registry factory to be used as a component.
#. Configuring other proprietary settings for each monitoring service.

This section describes how to work with each of the monitoring services.


Working with Datadog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding Dependencies
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-datadog</artifactId>
      <version>1.13.0</version>
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

  The API key can be set in ``nablarch.micrometer.datadog.apiKey`` .

Configuring the site URL
  .. code-block:: text

    nablarch.micrometer.datadog.uri=<SITE_URL>

  The site URL can be set in ``nablarch.micrometer.datadog.uri`` .

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
      <version>1.13.0</version>
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

  * `Java codeless application monitoring Azure Monitor Application Insights(external site) <https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  The Java 3.0 agent automatically collects metrics output to Micrometer's `Global Registry(external site) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html#_global_registry>`_, and sends to Azure.

  * `Send custom telemetry from your application(external site) <https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  .. important::
    The Java 3.0 agent loads a large number of jar files during the initialization process.
    This may cause frequent GC during the initialization process of the Java 3.0 agent.

    Therefore, note that the performance may temporarily deteriorate due to GC for a while after the application is launched.

    Also, under heavy load, the overhead caused by the processing of the Java 3.0 agent may affect the performance.
    Therefore, you should confirm the performance in the performance test with the Java 3.0 agent as in production.

  For information on how to set up a Java 3.0 agent, see :ref:`Distributed Tracing in Azure <azure_distributed_tracing>` .

How to configure Micrometer adaptor
  You need to configure following settings to send metrics to Azure with Micrometer adaptor.

  * Add the Java 3.0 agent to your application's JVM args
  * Define a ``MeterRegistry`` component using the Global Registry

  See the `Azure documentation(external site) <https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=java#modify-your-application>`_ for how to set JVM args.

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

  For more information, see `Configuration Options(external site) <https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-standalone-config>`_.

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
      <version>1.13.0</version>
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

Using OpenTelemetry Protocol (OTLP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many monitoring services support `OpenTelemetry (external site) <https://opentelemetry.io/>`_ and can collect metrics using the OpenTelemetry Protocol (hereafter OTLP) as the communication protocol.
The ``micrometer-registry-otlp`` module allows OTLP to work with various monitoring services.

  .. important::
    When collecting metrics with OpenTelemetry, check the information on the monitoring service to be used, as the appropriate (and available) linking method depends on the monitoring service.
    As an example, information on some monitoring services is shown below.

     * `Datadog's OpenTelemetry (external site) <https://docs.datadoghq.com/opentelemetry/>`_
     * `Introduction to OpenTelemetry by New Relic (external site) <https://docs.newrelic.com/docs/opentelemetry/opentelemetry-introduction/>`_
     * `Prometheus | HTTP API | OTLP Receiver(external site) <https://prometheus.io/docs/prometheus/latest/querying/api/#otlp-receiver>`_

In this section, we will use the case of OTLP linking to Prometheus running on port 9090 of localhost as an example.

Adding Dependencies
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-otlp</artifactId>
      <version>1.13.0</version>
    </dependency>

Declare the Registry Factory
  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.otlp.OtlpMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

Write a configuration file
  .. code-block:: text

    # Change Destination
    nablarch.micrometer.otlp.url=http://localhost:9090/api/v1/otlp/v1/metrics

Configuring headers
  .. code-block:: text

    nablarch.micrometer.otlp.headers=key1=value1,key2=value2

  If you need header information such as API keys for authentication, you can set it with ``nablarch.micrometer.otlp.headers``.

Disable the registry
  .. code-block:: text

    nablarch.micrometer.otlp.enabled=false

  You can disable the registry by setting ``nablarch.micrometer.otlp.enabled`` to ``false`` in ``micrometer.properties``.
  You can override this configuration by environment variable.
  Therefor, you can enable the registry by setting ``true`` with environment variable only at production.

Examples of metrics for each application type.
---------------------------------------------------------

In this section, we will explain what metrics should be collected for each application type (web and batch).

Examples of metrics for web applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Processing time for HTTP requests
  By measuring the processing time for each HTTP request, you can do the following.

  * You can check how much traffic each URL
  * You can check how long it takes to process the request

  By measuring percentiles, you can also check how long it takes to process most of the requests.

  See the following guide for more informations on how to collect these metrics.

  * :ref:`micrometer_timer_metrics_handler`
  * :ref:`micrometer_timer_metrics_handler_percentiles`

Processing time for SQL
  By measuring the SQL processing time, you can do the following.

  * You can check how long it takes for each SQL to be processed
  * You can check for SQLs that are taking longer than expected

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_sql_time`

Output count per log level
  By measuring the count of outputs per log level, you can do the following.

  * You can check if the warning log is output an abnormal number of times (attack detection)
  * You can detect error logs

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_log_count`

Status of resources provided by application servers and libraries
  By collecting metrics on the status of resources provided by application servers and libraries (thread pools, DB connection pools, etc.), you can use it as a source of information to identify the cause of system failures.

  Many application servers expose the status of their resources through MBean in JMX.
  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_mbean_metrics`

Examples of metrics for batch applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Processing time for batch
  By measuring the processing time of batches in normally, you can know the processing time under normal conditions.
  Therefore, you can quickly detect abnormalities when processing time deviates from normal.

  You can get processing time of batch by ``process.uptime`` described in :ref:`micrometer_default_metrics`.

Processing time per transaction
  By measuring the processing time per transaction, you can check whether each threads are distributed evenly in the multi-thread batch.

  As with processing time for batch, you can quickly detect abnormalities when processing time deviates from normal.

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_adaptor_batch_transaction_time`

Processed count with batch
  By measuring the count that was processed by batch, you can do the following.

  * You can check the progress of the batch
  * You can check that the batch process is proceeding at the expected speed
  * You can check that the count processed with batch is expected

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_batch_processed_count`

Processing time for SQL
  By measuring the SQL processing time, you can do the following.

  * You can check how long it takes for each SQL to be processed
  * You can check for SQLs that are taking longer than expected

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_sql_time`

Output count per log level
  By measuring the count of outputs per log level, you can detect warning logs and error logs.

  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_log_count`

Status of resources provided by libraries
  By collecting metrics on the status of resources provided by  libraries (DB connection pools, etc.), you can use it as a source of information to identify the cause of system failures.

  Some libraries expose the status of the resource through MBean in JMX.
  See the following guide for more informations on how to collect metrics.

  * :ref:`micrometer_mbean_metrics`


.. _micrometer_timer_metrics_handler:

Handler to measure processing time
--------------------------------------------------

By setting :java:extdoc:`TimerMetricsHandler <nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler>` to the handler queue, you can measure processing time of subsequent handlers as metrics.
You can monitor the average and maximum processing times in handler queue.

``TimerMetricsHandler`` needs an instance of a class that implements the :java:extdoc:`HandlerMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder>` interface.
The ``HandlerMetrcisMetaDataBuilder`` provides a function to build the following meta data for setting to collected metrics.

* Name of metrics
* Description of metrics
* Tag list of metrics

The following is an example for implementation of ``HandlerMetricsMetaDataBuilder``.

.. code-block:: java

  import io.micrometer.core.instrument.Tag;
  import nablarch.fw.ExecutionContext;
  import nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder;

  import java.util.Arrays;
  import java.util.List;

  public class CustomHandlerMetricsMetaDataBuilder<TData, TResult>
      implements HandlerMetricsMetaDataBuilder<TData, TResult> {
    
      @Override
      public String getMetricsName() {
          return "metrics.name";
      }

      @Override
      public String getMetricsDescription() {
          return "Description of this metrics.";
      }

      @Override
      public List<Tag> buildTagList(TData param, ExecutionContext executionContext, TResult tResult, Throwable thrownThrowable) {
          return Arrays.asList(Tag.of("foo", "FOO"), Tag.of("bar", "BAR"));
      }
  }

You need implement methods ``getMetricsName()`` and ``getMetricsDescription()`` that return name and description of the metrics.

``buildTagList()`` is passed the parameters passed to the handler, the execution result of the subsequent handler, and any exceptions thrown by the subsequent handler (or ``null`` if no exceptions were thrown).
You need implement this method that returns list of tags for the metrics.

The following is an example for setting ``TimerMetricsHandler`` to the handler queue.

.. code-block:: xml

  <!-- Handler queue -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- ... -->

        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <property name="meterRegistry" ref="meterRegistry" />

          <property name="handlerMetricsMetaDataBuilder">
            <component class="xxx.CustomHandlerMetricsMetaDataBuilder" />
          </property>
        </component>

        <!-- ... -->
      </list>
    </property>
  </component>

Add ``TimerMetricsHandler`` to the handler queue and set the ``HandlerMetricsMetaDataBuilder`` component  to ``handlerMetricsMetaDataBuilder`` property.

Then, set the `MeterRegistry (external site)`_ created by registry factory to ``meterRegistry`` property.

Now the ``TimerMetricsHandler`` can collect the processing time of subsequent handlers as metrics.

Nablarch provides a class that implements ``HandlerMetricsMetaDataBuilder`` to provide the following function.
For more information, please refer to the linked explanation.

* :ref:`micrometer_adaptor_http_request_process_time_metrics`

.. _micrometer_timer_metrics_handler_percentiles:

Collect the percentiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TimerMetricsHandler`` has the following properties to send percentiles to the monitoring services.

.. list-table::

  * - Property
    - Description
  * - ``percentiles``
    - A list of percentile values to be collected.
      If you want to collect the 95th percentile, specify ``0.95``.
  * - ``enablePercentileHistogram``
    - A flag whether the bucket of collected histograms should be sent to the monitoring service.
      If the monitoring service does not support a mechanism to calculate percentile values from histograms, this property will be ignored.
  * - ``serviceLevelObjectives``
    - A list of bucket values to be added to the histogram.
      The unit is milliseconds.
      This value is set based on the SLO (Service Level Objective).
  * - ``minimumExpectedValue``
    - A minimum value of the histogram bucket to be collected.
      The unit is milliseconds.
  * - ``maximumExpectedValue``
    - A maximum value of the histogram bucket to be collected.
      The unit is milliseconds.

These properties are used as values to be set in `Timer(external site)`_ provided by Micrometer.
For more details, see the `Micrometer documentation (external site) <https://docs.micrometer.io/micrometer/reference/concepts/histogram-quantiles.html>`_.

These properties are unset by default. Therefore, no percentile information is collected.
You must configure these properties explicitly if you want collect percentiles.
The following is an example for configuration.

.. code-block:: xml

  <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
    <property name="meterRegistry" ref="meterRegistry" />
    <property name="handlerMetricsMetaDataBuilder">
      <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
    </property>

    <!-- Collect 98th, 90th, 50th percentiles -->
    <property name="percentiles">
      <list>
        <value>0.98</value>
        <value>0.90</value>
        <value>0.50</value>
      </list>
    </property>

    <!-- Send the histogram backets to the monitoring service  -->
    <property name="enablePercentileHistogram" value="true" />

    <!-- Set 1000ms and 1500ms as SLO -->
    <property name="serviceLevelObjectives">
      <list>
        <value>1000</value>
        <value>1500</value>
      </list>
    </property>
    
    <!-- Set the minimum bucket value to 500ms -->
    <property name="minimumExpectedValue" value="500" />
    <!-- Set the maximum bucket value to 3000ms -->
    <property name="maximumExpectedValue" value="3000" />
  </component>

If you use the ``MeterRegistry`` that supports histogram buckets, the above configuration will allow you to collect the following metrics.

.. code-block:: text

  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.98",} 1.475346432
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.9",} 1.408237568
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.5",} 0.737148928
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.5",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.536870911",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.626349396",} 12.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.715827881",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.805306366",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.894784851",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.984263336",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.0",} 18.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.073741824",} 20.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.431655765",} 29.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.5",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.789569706",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.147483647",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.505397588",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.863311529",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="3.0",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="+Inf",} 32.0

.. tip::
  
  In the ``MeterRegistry`` provided by this adapter, only the ``OtlpMeterRegistry`` supports histogram buckets.

  The example uses `PrometheusMeterRegistry(external site)`_ to show a concrete example of a histogram bucket (``http_server_requests_seconds_bucket``) (`Prometheus(external site) <https://prometheus.io/>`_ supports computing percentiles by histogram).
  However, this adaptor does not provide ``MeterRegistryFactory`` of ``PrometheusMeterRegistry``.
  If you want to try the ``PrometheusMeterRegistry``, you should create the following class.

  .. code-block:: java

    package example.micrometer.prometheus;

    import io.micrometer.prometheusmetrics.PrometheusConfig;
    import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
    import nablarch.core.repository.di.DiContainer;
    import nablarch.integration.micrometer.MeterRegistryFactory;
    import nablarch.integration.micrometer.MicrometerConfiguration;
    import nablarch.integration.micrometer.NablarchMeterRegistryConfig;

    public class PrometheusMeterRegistryFactory extends MeterRegistryFactory<PrometheusMeterRegistry> {

        @Override
        protected PrometheusMeterRegistry createMeterRegistry(MicrometerConfiguration micrometerConfiguration) {
            return new PrometheusMeterRegistry(new Config(prefix, micrometerConfiguration));
        }

        @Override
        public PrometheusMeterRegistry createObject() {
            return doCreateObject();
        }

        static class Config extends NablarchMeterRegistryConfig implements PrometheusConfig {

            public Config(String prefix, DiContainer diContainer) {
                super(prefix, diContainer);
            }

            @Override
            protected String subPrefix() {
                return "prometheus";
            }
        }
    }

The provided HandlerMetricsMetaDataBuilder implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section, we explain the implementation class of ``HandlerMetricsMetaDataBuilder``, which is provided by Nablarch.

.. _micrometer_adaptor_http_request_process_time_metrics:

Collect the processing time of HTTP requests
*********************************************************************

The :java:extdoc:`HttpRequestTimeMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder>` builds meta data of metrics for measuring processing time of HTTP requrest.

This class uses ``http.server.requirements`` as the name of the metrics.

This class set the following tags to metrics.

.. list-table::

  * - Tag name
    - Description
  * - ``class``
    - The name of the action class that handled the request (``Class.getName()``).
      If it cannot be obtained, it will be ``UNKNOWN``.
  * - ``method``
    - A string consisting of the method name of the action class that handled the request and the type name of the argument (``Class.getCanonicalName()``), joined by an underscore (``_``).
      If it cannot be obtained, it will be ``UNKNOWN``.
  * - ``httpMethod``
    - A HTTP method.
  * - ``status``
    - A HTTP status code.
  * - ``outcome``
    - A string indicating the status code type (1XX: ``INFORMATION``, 2XX: ``SUCCESS``, 3XX: ``REDIRECTION``, 4XX: ``CLIENT_ERROR``, 5XX: ``SERVER_ERROR``, Others: ``UNKNOWN``).
  * - ``exception``
    - A simple name of the exception thrown during request processing (or ``None`` if no exception was thrown).

The following is an example using this class.

.. code-block:: xml

  <!-- Handler queue -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- Handler to collect metrics of processing time of HTTP requests -->
        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <!-- Set the MeterRegistry created by the registry factory to meterRegistry property -->
          <property name="meterRegistry" ref="meterRegistry" />

          <!-- Set the HttpRequestTimeMetricsMetaDataBuilder to handlerMetricsMetaDataBuilder property -->
          <property name="handlerMetricsMetaDataBuilder">
            <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
          </property>
        </component>

        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>

        <!-- ... -->
     </list>
    </property>
  </component>

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=POST,method=login_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=REDIRECTION,status=303} throughput=0.2/s mean=0.4617585s max=0.4617585s
  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.IndustryAction,exception=None,httpMethod=GET,method=find,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.103277s max=0.103277s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=4.7409146s max=4.7409146s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.ProjectAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.5329547s max=0.5329547s

.. _micrometer_adaptor_batch_transaction_time:

Measure the processing time per transaction of a batch
-----------------------------------------------------------------------

You can measure the processing time per transaction of the :ref:`nablarch_batch` as metrics with :java:extdoc:`BatchTransactionTimeMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger>`.
This will allow you to monitor the average and maximum processing time per transaction.

The ``BatchTransactionTimeMetricsLogger`` collects metrics with `Timer(external site)`_.
Metrics name is ``batch.transaction.time``.

You can change the name with :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger.setMetricsName(java.lang.String)>`.

Metrics have the following tag.

.. list-table::

  * - Tag name
    - Description
  * - ``class``
    - The name of action class (This value is obtained from :ref:`-requestPath <nablarch_batch-resolve_action>`).

The following is an example to use ``BatchTransactionTimeMetricsLogger``.

.. code-block:: xml

  <!-- Combining multiple CommitLoggers -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- Configure the default CommitLogger -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- Measuring the processing time per transaction -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

First, define the :java:extdoc:`CompositeCommitLogger <nablarch.core.log.app.CompositeCommitLogger>` component with the name ``commitLogger``.

Then, set  :java:extdoc:`BasicCommitLogger <nablarch.core.log.app.BasicCommitLogger>` and ``BatchTransactionTimeMetricsLogger`` components to the ``commitLoggerList`` property.

Now you can measure time per transaction units.
In the following, we explain how it works.

The Nablarch batch controls the transaction commit interval by the :ref:`loop_handler`.
This handler provides a mechanism to call the ``increment(long)`` method of the :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` when a transaction is committed.
This ``CommitLogger`` entity can be overridden by defining a component named ``commitLogger``.

The ``BatchTransactionTimeMetricsLogger`` implements the ``CommitLogger`` interface.
Then, the ``BatchTransactionTimeMetricsLogger`` measures the time per transaction by measuring the interval between calls to ``increment(long)``.
Therefore, you can measure time per transaction by defining the ``BatchTransactionTimeMetricsLogger`` component that is named ``commitLogger``.

However, if you define ``BatchTransactionTimeMetricsLogger`` as ``commitLogger``, the default component of ``CommitLogger``, ``BasicCommitLogger``, will not work.
Therefore, the above configuration example uses the ``CompositeCommitLogger``, which can combine multiple CommitLoggers, to use the ``BasicCommitLogger`` and ``BatchTransactionTimeMetricsLogger``.

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  Feb 18, 2021 11:51:54 AM io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$5
  INFO: batch.transaction.time{class=MetricsTestAction} throughput=0.8/s mean=2.394144925s max=4.692886s

.. _micrometer_batch_processed_count:

Measure the count that was processed by batch
--------------------------------------------------

You can measure the count of input data processed by the :ref:`nablarch_batch` with the :java:extdoc:`BatchProcessedRecordCountMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger>`.
This will allow you to monitor the progress of the batch and changes in processing speed.

The ``BatchProcessedRecordCountMetricsLogger`` collects metrics with `Counter(external site)`_.
Metrics name is ``batch.processed.record.count``.

You can change the name with :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger.setMetricsName(java.lang.String)>`.

Metrics have the following tag.

.. list-table::

  * - Tag name
    - Description
  * - ``class``
    - The name of action class (This value is obtained from :ref:`-requestPath <nablarch_batch-resolve_action>`).

The following is an example to use ``BatchProcessedRecordCountMetricsLogger``.

.. code-block:: xml

  <!-- Combining multiple CommitLoggers -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- Configure the default CommitLogger -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- Measure the processed count -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

The ``BatchProcessedRecordCountMetricsLogger`` uses the :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` mechanism to measure the processed count, just as in "Measure the processing time per transaction of a batch".

For more information on how ``CommitLogger`` works and how to use it, please refer to :ref:`micrometer_adaptor_batch_transaction_time`.

Now you can use ``BatchProcessedRecordCountMetricsLogger``.

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  Feb 18, 2021 11:51:44 AM io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  INFO: batch.processed.record.count{class=MetricsTestAction} throughput=4/s
  Feb 18, 2021 11:51:49 AM io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  INFO: batch.processed.record.count{class=MetricsTestAction} throughput=10/s
  Feb 18, 2021 11:51:54 AM io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  INFO: batch.processed.record.count{class=MetricsTestAction} throughput=8/s

.. _micrometer_log_count:

Measure the output count per log level
--------------------------------------------------

You can measure the output count per log level with the :java:extdoc:`LogCountMetrics <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics>`.
This will allow you to monitor the frequency of output at specific log levels, monitor error logs.

The ``LogCountMetrics`` collects metrics with `Counter(external site)`_.
Metrics name is ``log.count``.
You can change the name with the :java:extdoc:`constructor <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics.<init>(nablarch.integration.micrometer.instrument.binder.MetricsMetaData)>` that receives the :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>`.

Metrics have the following tags.

.. list-table::

  * - Tag name
    - Description
  * - ``level``
    - The log level.
  * - ``logger``
    - The name used to get the logger from the :java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>`.

Configure LogPublisher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` uses the :java:extdoc:`LogPublisher <nablarch.core.log.basic.LogPublisher>` mechanism to detect log output events.

Therefore, you need to configure ``LogPublisher`` at first to use ``LogCountMetrics``.
For ``LogPublisher`` settings, see :ref:`log-publisher_usage`.

Create a custom DefaultMeterBinderListProvider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` is provided as an implementation class of `MeterBinder (external site)`_.
Therefore, you need create a class that inherits from :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` and implement it to return a list of MeterBinders that contains ``LogCountMetrics``.

.. tip::

  For a description of the ``DefaultMeterBinderListProvider``, see :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component`.

The following is an example for a custom ``DefaultMeterBinderListProvider``.

.. code-block:: java

  package example.micrometer.log;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // Add LogCountMetrics to the default MeterBinder list.
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics());
          return meterBinderList;
      }
  }

Finally, set the custom ``DefaultMeterBinderListProvider`` that you created to the ``meterBinderListProvider`` property of the ``MeterRegistryFactory`` component.
Now you can use the ``LogCountMetrics``.

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  2020-12-22 14:25:36.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=WARN,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=0.4/s
  2020-12-22 14:25:41.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=ERROR,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=1.4/s

Log level to be aggregated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, only log outputs above the warning log will be counted.

``LogCountMetrics`` has a constructor that receives a :java:extdoc:`LogLevel <nablarch.core.log.basic.LogLevel>`.
You can change the threshold of the log level to be aggregated with the constructor.
In the following implementation example, the threshold value is changed to INFO.

.. code-block:: java

  // ...
  import nablarch.core.log.basic.LogLevel;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics(LogLevel.INFO)); // Specify the threshold of log level.
          return meterBinderList;
      }
  }

.. important::

  If you lower the log level threshold too much, a large amount of metrics may be collected depending on the application.
  Depending on the fee structure of the monitoring service to be used, the usage fee may increase, so it should be set with care.

.. _micrometer_sql_time:

Measure SQL processing time
--------------------------------------------------

By using :java:extdoc:`SqlTimeMetricsDaoContext <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContext>`, you can measure the processing time of SQL executed using the :ref:`universal_dao`.
This will allow you to monitor the average and maximum processing time for each SQL.

The ``SqlTimeMetricsDaoContext`` collects metrics with `Timer(external site)`_.
Metrics name is ``sql.process.time``.
You can change the name with :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory.setMetricsName(java.lang.String)>` of the :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` that is a factory class for ``SqlTimeMetricsDaoContext``.

Metrics have the following tags.

.. list-table::

  * - Tag name
    - Description
  * - ``sql.id``
    - The SQLID passed in the method argument of ``DaoContext`` (``"None"`` if there is no SQLID)
  * - ``entity``
    - The name of the entity class (``Class.getName()``)
  * - ``method``
    - The method name of the executed ``DaoContext``.

The following is an example of the configuration for using ``SqlTimeMetricsDaoContext``.

.. code-block:: xml

  <!-- Define SqlTimeMetricsDaoContextFactory as daoContextFactory. -->
  <component name="daoContextFactory"
             class="nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory">
    <!-- Set the factory of the DaoContext to be transferred to the delegate. -->
    <property name="delegate">
      <component class="nablarch.common.dao.BasicDaoContextFactory">
        <property name="sequenceIdGenerator">
          <component class="nablarch.common.idgenerator.SequenceIdGenerator" />
        </property>
      </component>
    </property>

    <!-- Set the meterRegistry generated by the registry factory to the meterRegistry property. -->
    <property name="meterRegistry" ref="meterRegistry" />
  </component>

``SqlTimeMetricsDaoContext`` measures the processing time of each database access method by wrapping :java:extdoc:`DaoContext <nablarch.common.dao.DaoContext>`.
Then, :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` is a factory class that generates a ``SqlTimeMetricsDaoContext`` that wraps a ``DaoContext``.

Define this ``SqlTimeMetricsDaoContextFactory`` as a component with the name ``daoContextFactory``.
This will replace the ``DaoContext`` used by :ref:`universal_dao` with ``SqlTimeMetricsDaoContext``.

Now you can use ``SqlTimeMetricsDaoContext``.

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=delete,sql.id=None} throughput=0.2/s mean=0.0005717s max=0.0005717s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=findAllBySqlFile,sql.id=SEARCH_PROJECT} throughput=0.6/s mean=0.003364233s max=0.0043483s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.web.dto.ProjectDto,method=findBySqlFile,sql.id=FIND_BY_PROJECT} throughput=0.2/s mean=0.000475s max=0.0060838s
  2020-12-23 15:00:25.162 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Industry,method=findAll,sql.id=None} throughput=0.8/s mean=0.00058155s max=0.0013081s

.. _micrometer_mbean_metrics:

Measure the value obtained from any MBean as a metric
-------------------------------------------------------------

:java:extdoc:`JmxGaugeMetrics <nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics>` allows you to measure the values obtained from any MBean as metrics.
This will allow you to measure the various status of the application server or libraries provided by MBean and monitor them.

.. tip::

  MBean is a Java object defined in Java Management Extensions (JMX), which provides APIs for accessing information on managed resources.
  Many application servers, such as Tomcat, expose the server status (thread pool status, etc.) in MBean.
  By accessing these MBeans from the application, you can get the status of the server.

  For more information about JMX, see the `Java Management Extensions Guide (external site) <https://docs.oracle.com/en/java/javase/17/jmx/java-management-extensions-jmx-user-guide.html>`_.

The ``JmxGaugeMetrics`` measure values obtained from MBean with `Gauge(external site)`_.

This section explains how to use ``JmxGaugeMetrics``.

First, as an example of referring to the MBean provided by the application server, we show an example of obtaining the status of the Tomcat thread pool.
Next, as an example of referring to the MBean provided by the library embedded in the application, we show an example of obtaining the status of the HikariCP connection pool.

Obtain the status of the Tomcat thread pool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``JmxGaugeMetrics`` implements `MeterBinder (external site)`_.
Therefore, you need create a class that inherits from :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` and implement it to return a list of MeterBinders that contains ``JmxGaugeMetrics``.

.. tip::

  For a description of the ``DefaultMeterBinderListProvider``, see :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component`.

The following is an example for a custom ``DefaultMeterBinderListProvider``.

.. code-block:: java

  package example.micrometer;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new JmxGaugeMetrics(
              // Name and description of metrics.
              new MetricsMetaData("thread.count.current", "Current thread count."),
              // The conditions to specify the attribute of MBean.
              new MBeanAttributeCondition("Catalina:type=ThreadPool,name=\"http-nio-8080\"", "currentThreadCount")
          ));
          return meterBinderList;
      }
  }

You must pass following classes to the constructor of ``JmxGaugeMetrics``.

* :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>`
    * Specify meta data such as the name, description, and tags of the metrics.
* :java:extdoc:`MBeanAttributeCondition <nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition>`
    * Specify the object name and attribute name to identify the MBean.

``JmxGaugeMetrics`` gets the MBean based on the information specified in ``MBeanAttributeCondition``.
Then, the ``JmxGaugeMetrics`` constructs metrics with the information specified in ``MetricsMetaData``.

.. tip::

  You can check the object and attribute names of the MBean created by Tomcat with JConsole tool that comes with the JDK.
  When you connect to the JVM running Tomcat with JConsole and open the "MBeans" tab, you get the list of MBeans in the connected JVM.

  For more details about JConsole, refer to the `Monitoring and Management Guide (external site) <https://docs.oracle.com/en/java/javase/17/management/using-jconsole.html#GUID-A2AE31B2-6C50-47B4-B854-5212C5AE4955>`_.

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  18-Feb-2021 13:17:38.168 INFO [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 thread.count.current{} value=10

Obtain the status of the HikariCP connection pool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`HikariCP (external site) <https://github.com/brettwooldridge/HikariCP>`_ has a function to get status of the connection pool by MBean.

* `MBean (JMX) Monitoring and Management (external site) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management>`_

This function will allow ``JmxGaugeMetrics`` to collect connection pool status.

First, enable the function to publish status by MBean.
You must set ``true`` to ``registerMbeans`` property of ``com.zaxxer.hikari.HikariDataSource``.

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">
    <!-- ... -->

    <!-- Datasource configuration -->
    <component name="dataSource"
              class="com.zaxxer.hikari.HikariDataSource" autowireType="None">
      <property name="driverClassName" value="${nablarch.db.jdbcDriver}"/>
      <property name="jdbcUrl"         value="${nablarch.db.url}"/>
      <property name="username"        value="${nablarch.db.user}"/>
      <property name="password"        value="${nablarch.db.password}"/>
      <property name="maximumPoolSize" value="${nablarch.db.maxPoolSize}"/>
      <!-- Enable MBean to publish status. -->
      <property name="registerMbeans"  value="true"/>
    </component>

  </component-configuration>

In the above configuration, we set true to the ``registerMbeans`` property in the component definition of ``HikariDataSource``.

Next, configure the ``JmxGaugeMetrics`` with the object name and attribute name that you want to measure.
The specifications of object names and attribute names are described in the `HikariCP document mentioned above (external site) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management#programmatic-access>`_.

The following is an example implementation of ``JmxGaugeMetrics`` for measuring the maximum count of connection pools and the count of active connections.

.. code-block:: java

  package com.nablarch.example.app.metrics;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          // The maximum count.
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.total", "Total DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "TotalConnections")
          ));
          // The active count.
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.active", "Active DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "ActiveConnections")
          ));
          return meterBinderList;
      }
  }

If you use ``LoggingMeterRegistry``, you will get like the following metrics.

.. code-block:: text

  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.active{} value=0
  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.total{} value=5

About the warning log output when the server is started
*********************************************************************

There are two main ways for Micrometer to send metrics to the monitoring service.

* Applications send metrics to the monitoring service at regular intervals (Client pushes)
    * Datadog, CloudWatch, etc
* The monitoring service queries to the application for metrics at regular intervals (Server polls)
    * Prometheus, etc

In the former case (Client pushes), ``MeterRegistry`` will start sending metrics at regular intervals after component creation.
On the other hand, HikariCP's connection pool is designed to be created the first time when the first database access is made.

Therefore, ``JmxGaugeMetrics`` will refer to a connection pool that does not exist if it sends metrics before the first database access occurs.
At this time, the Micrometer will output the following warning log.

.. code-block:: text

  18-Feb-2021 13:17:37.953 WARNING [logging-metrics-publisher] io.micrometer.core.util.internal.logging.WarnThenDebugLogger.log Failed to apply the value function for the gauge 'db.pool.active'. Note that subsequent logs will be logged at debug level.
          java.lang.RuntimeException: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:59)
                  at io.micrometer.core.instrument.Gauge.lambda$builder$0(Gauge.java:58)
                  at io.micrometer.core.instrument.StrongReferenceGaugeFunction.applyAsDouble(StrongReferenceGaugeFunction.java:47)
                  at io.micrometer.core.instrument.internal.DefaultGauge.value(DefaultGauge.java:54)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3(LoggingMeterRegistry.java:98)
                  at io.micrometer.core.instrument.Meter.use(Meter.java:158)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$12(LoggingMeterRegistry.java:97)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:183)
                  at java.util.stream.SortedOps$SizedRefSortingSink.end(SortedOps.java:357)
                  at java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:483)
                  at java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:472)
                  at java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:150)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:173)
                  at java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:234)
                  at java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:485)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.publish(LoggingMeterRegistry.java:95)
                  at io.micrometer.core.instrument.push.PushMeterRegistry.publishSafely(PushMeterRegistry.java:52)
                  at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
                  at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
                  at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
                  at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
                  at java.lang.Thread.run(Thread.java:748)
          Caused by: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getMBean(DefaultMBeanServerInterceptor.java:1095)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getAttribute(DefaultMBeanServerInterceptor.java:643)
                  at com.sun.jmx.mbeanserver.JmxMBeanServer.getAttribute(JmxMBeanServer.java:678)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:52)
                  ... 23 more

The value of the metrics will be NaN while the connection pool is not created.

.. code-block:: text

  18-Feb-2021 13:18:32.933 INFO [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.active{} value=NaN
  18-Feb-2021 13:18:32.933 INFO [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.total{} value=NaN

The Micrometer outputs this warning log only the first time, and it suppresses after the second time.
The connection pool values will be collected correctly after connection pool is created.

This means that this warning log may be output even when the application is normal, depending on the timing.
However, there is no harm.
You can ignore this warning log.

If you really want to suppress the warning log, you can avoid it to some extent by implementing the following.

.. code-block:: java

  package example.micrometer;

  // ...
  import nablarch.core.log.Logger;
  import nablarch.core.log.LoggerManager;
  import nablarch.core.repository.initialization.Initializable;
  import java.sql.SQLException;
  import javax.sql.DataSource;
  import java.sql.Connection;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider implements Initializable {
      private static final Logger LOGGER = LoggerManager.get(CustomMeterBinderListProvider.class);

      private DataSource dataSource;

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // ...
      }

      public void setDataSource(DataSource dataSource) {
          this.dataSource = dataSource;
      }

      @Override
      public void initialize() {
          try (Connection con = dataSource.getConnection()) {
              // Preventing the warning log by establishing a connection during initialization.
          } catch (SQLException e) {
              LOGGER.logWarn("Failed initial connection.", e);
          }
      }
  }

Implement a custom ``DefaultMeterBinderListProvider`` with :java:extdoc:`Initializable <nablarch.core.repository.initialization.Initializable>`.
Next, implement to accept ``java.sql.DataSource`` as a property.
Finally, implement the ``initialize()`` method that connects to the database.

In the component definition, set the ``DataSource`` to the property.
Then, add this custom class to the list of components that need initialization.

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="example.micrometer.CustomMeterBinderListProvider">
    <!-- Set the DataSource -->
    <property name="dataSource" ref="dataSource" />
  </component>

  <!-- The components that need initialization. -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- ... -->

        <!-- Add CustomMeterBinderListProvider for initialization. -->
        <component-ref name="meterBinderListProvider" />
      </list>
    </property>
  </component>

With the above modifications, the database connection will be made when the system repository is initialized.
The default interval for sending metrics is 1 minute, so in most cases the connection pool will be created before the metrics are sent.
This will cause no warning log to be output.

Note, however, that if the interval for sending metrics is set to a very short time, the metrics may be sent before the system repository is initialized and a warning log may be output.

.. _MeterBinder (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/MeterBinder.html
.. _Counter(external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Counter.html
.. _Gauge(external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Gauge.html
.. _DatadogConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html
.. _CloudWatchConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchConfig.html
.. _StatsdConfig (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdConfig.html
.. _OtlpConfig(external site): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.9.17/io/micrometer/registry/otlp/OtlpConfig.html
.. _MeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/MeterRegistry.html
.. _DatadogMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _StatsdMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdMeterRegistry.html
.. _OtlpMeterRegistry(external site): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.9.17/io/micrometer/registry/otlp/OtlpMeterRegistry.html
.. _DatadogMeterRegistry (external site: https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _CloudWatchMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchMeterRegistry.html
.. _LoggingMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/logging/LoggingMeterRegistry.html
.. _SimpleMeterRegistry (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/simple/SimpleMeterRegistry.html
.. _JvmMemoryMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmMemoryMetrics.html
.. _ProcessorMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/ProcessorMetrics.html
.. _JvmGcMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmGcMetrics.html
.. _JvmThreadMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmThreadMetrics.html
.. _ClassLoaderMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/ClassLoaderMetrics.html
.. _FileDescriptorMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/FileDescriptorMetrics.html
.. _UptimeMetrics (external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/UptimeMetrics.html
.. _Timer(external site): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Timer.html
.. _PrometheusMeterRegistry(external site): https://javadoc.io/doc/io.micrometer/micrometer-registry-prometheus/1.13.0/io/micrometer/prometheusmetrics/PrometheusMeterRegistry.html