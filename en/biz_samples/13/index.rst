
=====================================================
Sample Request/Response Log Output Using Logbook
=====================================================

`Source code <https://github.com/nablarch/nablarch-biz-sample-all/tree/main/nablarch-logbook>`_

--------------
Summary
--------------

This sample uses `Logbook <https://github.com/zalando/logbook>`_ to log HTTP requests and responses.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scope of this sample
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although Logbook supports a variety of message formats and output methods, this sample deals with the following implementation.

* Use Nablarch's log output function for Logbook log output
  
  * The linkage with Nablarch is achieved using :ref:`slf4j_adaptor`
  * Logs are output to standard output

* Use JAX-RS client for sending requests and JSON for message format

  * Use Jersey as a JAX-RS client implementation

* Use `JsonPath <https://github.com/json-path/JsonPath>`_ to mask specific items in JSON format

--------------
How to Use
--------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Adding Dependent Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the use of Logbook, Jersey, and SLF4J Adapter, add the following dependencies to the project's dependency settings.
Logbook has several modules available for the environment in which the system is used, so these should be added as well.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.zalando</groupId>
        <artifactId>logbook-bom</artifactId>
        <version>3.9.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>3.1.1</version>
        <type>pom</type>
        </dependency>
    </dependencies>
  </dependencyManagement>
  <dependencies>
    ...
    <!-- SLF4J Adapter -->
    <dependency>
      <groupId>com.nablarch.integration</groupId>
      <artifactId>slf4j-nablarch-adaptor</artifactId>
      <scope>runtime</scope>
    </dependency>

    <!-- Logbook -->
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-core</artifactId>
    </dependency>
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-jaxrs</artifactId>
    </dependency>
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-json</artifactId>
    </dependency>

    <!-- Jersey -->
    <dependency>
      <groupId>org.glassfish.jersey.core</groupId>
      <artifactId>jersey-client</artifactId>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.media</groupId>
      <artifactId>jersey-media-json-jackson</artifactId>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.inject</groupId>
      <artifactId>jersey-hk2</artifactId>
    </dependency>
    ...
  </dependencies>

.. tip::

  For the version to be specified for the dependency, set the appropriate version for the execution environment.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration of log.properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To output Logbook logs with Nablarch's log output function, make the following settings in **log.properties**.
It is recommended to define a logger for Logbook, as Logbook requires the log level to be set to TRACE.

* Set the log level to TRACE, as Logbook logs output at the TRACE level.
* Set the log output destination

In this sample, the output destination is set to :java:extdoc:`StandardOutputLogWriter (output to standard output) <nablarch.core.log.basic.StandardOutputLogWriter>`

.. code-block:: properties

  ...
  # Standard Output
  writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter
  writer.stdout.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.stdout.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$
  ...
  # Available logger name order
  availableLoggersNamesOrder=DEV,PER,SQL,MON,ACC,LOGBOOK,ROO
  ...
  # Configuration of Logbook
  loggers.LOGBOOK.nameRegex=org\\.zalando\\.logbook\\..*
  loggers.LOGBOOK.level=TRACE
  loggers.LOGBOOK.writerNames=stdout
  ...


See :ref:`log-basic_setting` for Nablarch's log output settings.

.. _logbook_settings:

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration of Logbook
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use Logbook, create an instance of the Logbook class with the necessary settings.

The default setting outputs information including all request and response bodies.

.. code-block:: java

  // Generate Logbook (default setting)
  Logbook logbook = Logbook.builder().build();

Logbook has various settings, such as ``condition`` to set output conditions and ``Filtering`` to set mask processing.
For example, to perform body masking, use the ``BodyFilter`` method to set a filter to replace the value.

.. code-block:: java

  // Generate Logbook (set to mask the id item in the body)
  Logbook logbook = Logbook.builder()
          .bodyFilter(jsonPath("$.id").replace("*****"))
          .build();

.. code-block:: java

  // Generate Logbook (set to mask id and username items in the array in the body)
  Logbook logbook = Logbook.builder()
          .bodyFilter(JsonPathBodyFilters.jsonPath("$[*].id").replace("*****"))
          .bodyFilter(JsonPathBodyFilters.jsonPath("$[*].username").replace("*****"))
          .build();

See `Logbook's README <https://github.com/zalando/logbook/blob/main/README.md>`_ for details on various settings.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Register Logbook in JAX-RS client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The generated Logbook instance can be used by registering it with the client to be used.

Logbook provides classes for registering with various clients,
In this sample, the ``LogbookClientFilter`` class is used because the JAX-RS client is used.

.. code-block:: java

  // Register Logbook in JAX-RS client
  Client client = ClientBuilder.newClient()
                    .register(new LogbookClientFilter(logbook));

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Output request/response logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a request is sent and a response is received by a JAX-RS client that has registered a Logbook, a log is output.

.. code-block:: java

  Response response = client.target("http://localhost:3000")
                        .path("/users")
                        .request()
                        .get();

In this sample, the output destination is set to standard output, so the following log is output to standard output.
The log is output in the format set in Nablarch's log output function, and only the message part is output in the format set in Logbook.
In the default format of Logbook, the type of message (request sent or response received), headers, and body are output.

* Request log

.. code-block:: text

  2023-05-11 09:38:06.438 -TRACE- org.zalando.logbook.Logbook [202305110938060580001] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get] usr_id = [guest] Outgoing Request: bb068bcf35bc5226
  Remote: localhost
  GET http://localhost:3000/users HTTP/1.1

* Response log

.. code-block:: text

  2023-05-11 09:38:06.496 -TRACE- org.zalando.logbook.Logbook [202305110938060580001] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get] usr_id = [guest] Incoming Response: bb068bcf35bc5226
  Duration: 57 ms
  HTTP/1.1 200 OK
  Connection: keep-alive
  Content-Length: 213
  Content-Type: application/json; charset=utf-8
  Date: Thu, 11 May 2023 00:38:06 GMT
  Keep-Alive: timeout=5

  [{"id":"81b8b153-5ed5-4d42-be13-346f257b368d","username":"Chasity91"},{"id":"6b1e7b91-6a1f-4424-be3c-4e3d28dd59c0","username":"Felton_Rohan"},{"id":"622677a4-04e3-4b70-85dd-a0b7f7161678","username":"Bella_Purdy"}]

If the masking process described in :ref:`logbook_settings` above is set, the body in the log above is converted and output as follows.
(Here, we have set the id and username items in the array in the body to be masked.)

.. code-block:: text

  2023-05-11 09:48:37.513 -TRACE- org.zalando.logbook.Logbook [202305110948374650002] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get/mask] usr_id = [guest] Incoming Response: e1ba3d95197a4539
  Duration: 9 ms
  HTTP/1.1 200 OK
  Connection: keep-alive
  Content-Length: 213
  Content-Type: application/json; charset=utf-8
  Date: Thu, 11 May 2023 00:48:37 GMT
  Keep-Alive: timeout=5

  [{"id":"*****","username":"*****"},{"id":"*****","username":"*****"},{"id":"*****","username":"*****"}]
