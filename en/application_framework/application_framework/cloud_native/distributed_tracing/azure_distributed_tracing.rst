Distributed Tracing in Azure
=========================================

This chapter describes how to perform distributed tracing on Azure.

.. _how_to_enable_distributed_tracing:

How to perform distributed tracing on Azure
--------------------------------------------------------------------------------------------------

  In Azure, distributed tracing is done using ``Azure Application Insights``.

  * `Distributed tracing in Azure Application Insights (external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing>`_

  A mechanism for enabling distributed tracing from Java applications is provided by using a Java agent (**Java 3.0 agent**).

  * `Azure Monitor Application Insights monitoring Java code-free applications (external site) <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in- process-agent>`_

  .. important::
    The Java 3.0 agent loads a large number of jar files during the initialization process.
    This may cause frequent GC during the initialization process of the Java 3.0 agent.

    Therefore, note that the performance may temporarily deteriorate due to GC for a while after the application is launched.

    Also, under heavy load, the overhead caused by the processing of the Java 3.0 agent may affect the performance.
    Therefore, you should confirm the performance in the performance test with the Java 3.0 agent as in production.

  The following is an example of using the archetype for containers.

  First, download the agent from the official website of `Azure <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in-process-agent#quickstart>`_.
  Then, create an arbitrary directory under ``src/main/jib`` and store the agent.

  Next, place ``applicationinsights.json`` in the directory where you have just stored the agent.
  The ``connectionString`` is a connection string containing the instrumentation key that will be issued after the Azure Application Insights resource is created.
  For other configuration options, see the `Guide <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-standalone-config>`_.

  * applicationinsights.json

  .. code-block:: json

    {
      "connectionString": "InstrumentationKey=XXXXX"
    }


  Finally, add the environment variable ``CATALINA_OPTS`` to ``jib-maven-plugin`` in ``pom.xml``.
  (In the example, we specify ``applicationinsights-agent-3.0.2.jar``, which is located directly under the ``applicationInsights`` directory.

  * pom.xml

  .. code-block:: xml

    <! -- Docker containerization -->
    <plugin>
        <groupId>com.google.cloud.tools</groupId>
        <artifactId>jib-maven-plugin</artifactId>
        <configuration>
            <container>
                <appRoot>/usr/local/tomcat/webapps/ROOT</appRoot>
                <ports>
                    <port>8080</port>
                </ports>
                <environment>
                    <CATALINA_OPTS>-javaagent:/applicationInsights/applicationinsights-agent-3.0.2.jar</CATALINA_OPTS>
                </environment>
            </container>
        </configuration>
    </plugin>


Now you can use ``Azure Application Insights`` for distributed tracing by building with Jib.

For detailed configuration instructions, see the `Azure documentation <https://docs.microsoft.com/en-us/azure/azure-monitor/app/java-in-process-agent#quickstart>`_.
