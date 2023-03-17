
Messaging Platform Test Simulator Sample
================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

`Source code <https://github.com/nablarch/nablarch-messaging-simulator>`_

This sample provides a sample implementation to simulate a destination system for testing applications using the Nablarch application framework  :ref:`mom_system_messaging` and :ref:`http_system_messaging`.

It is assumed to be used as a connection destination for applications in communication confirmation and application coupling tests after a test environment is built.

The operation image of the simulator is shown below.

When the simulator receives a message
  .. image:: ./_images/behavior_illustration01.png
    :scale: 70

When the simulator sends a message
  .. image:: ./_images/behavior_illustration02.png
    :scale: 70

Uses
----------

Communication confirmation test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It can be used as a destination system for simple communication in the communication test to confirm the configuration of Nablarch application framework, middleware, hardware, etc. after building the test environment.

Combined test
~~~~~~~~~~~~~~~~

It can be used as a pseudo counterpart system for inter-system communication confirmation during application integration test.
By using the simulator to set the data to be used as the request message/response message, the test using the scenario can be performed.

While testing using scenarios is possible in a subfunction unit test, 
testing using a simulator is different in that it is possible to confirm the operation of the OS and middleware.

Load test
~~~~~~~~~~~

It is possible to send and receive a large number of messages to apply a load when performing an application load test.

Features
----------

Test data can be created in the same way as subfunction unit testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The test data used in this simulator can be created in the same way as the subfunction unit test. 
Therefore, no extra learning cost is incurred when using this simulator.

Supports special and complex test cases by customizing (message reception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By modifying the source code of the provided simulator, 
the following tests can be performed for special and complex test cases.

* Perform a test that needs to dynamically change the content of the response message according to the content of the request message.
* Perform an abnormal pattern test by intentionally delaying the response time to cause a timeout.


Capable of sending request messages in multiple threads (message sending)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The multi-thread execution control handler of Nablarch application framework is used inside the simulator. 
By sending a request message with multi-thread, it is possible to perform a load test that sends a large number of messages.

Request
------------

When the simulator receives a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* It is possible to send response messages on receiving HTTP messages and MOM receiving synchronous message.
* It is possible to output a log of the request message.
* Can return any HTTP status code.
* It is possible to send response messages according to the order of requests to the simulator (similarly to the unit test, the contents described in the Excel file are returned in order from the top).

When the simulator sends a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Request messages for sending HTTP messages, MOM sending synchronous message, and MOM sending asynchronous message can be sent.
* Send the same message a specified number of times.
* The response message log can be output.
* The contents described in the Excel file can be sent sequentially.


How to use
------------------------

Create a simulator execution module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In this sample, it is assumed that the user will customize the Java file etc. 
in order to carry out the intended test, so the source code and configuration file are provided as samples.

Therefore, in order to use the simulator, it is necessary to execute a build and create an execution module according to the following procedure.

Getting a simulator
  Execute the following command to get the source code of the simulator.

  .. code-block:: bash

    git clone https://github.com/nablarch/nablarch-messaging-simulator.git

  The following libraries must be installed in the local repository to run the simulator.

    * Jar file provided with WebSphere MQ

Creating an execution module
  Execute the following command to create an execution module under ``src/main/build``.

  .. code-block:: bat

    gradlew setupBuild

  The created execution module is placed in the environment where the simulator is to be executed.

Start the simulator
~~~~~~~~~~~~~~~~~~~~~~~~~

The simulator is started by executing the following bat file included in the execution module.

:HTTP receive messages: http-incoming-startup.bat
:Send HTTP message: http-outgoing-startup.bat
:MOM receive messages: mom-incoming-startup.bat
:Send MOM message: mom-outgoing-startup.bat

Expansion example
---------------------------

Specify the number of times to send a request when sending a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the requests for the line count described in the send list file (CSV) are sent, 
and the request send count can be specified with the ``sendCount`` option to send the same data repeatedly.

An example for specifying options is shown below.

.. code-block:: bat

  java <omitted> nablarch.fw.launcher.Main <omitted> -sendCount 10000

Switch the response according to the type of request when receiving a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To switch responses based on the request type, modify the ``getRequestId`` method of the action class.

Implementation example when switching the response by request URI when receiving HTTP message is shown below.

.. code-block:: java

  public class HttpIncomingSimulateAction implements Handler<HttpRequest, HttpResponse> {

      // Omitted

      protected String getRequestId(HttpRequest request) {
          // Switch the request ID of the response based on the request URI.
          return request.getRequestUri().endsWith("RM11AC0101") ? "RM11AC0201" : "RM11AC0202";
      }
  }

.. tip::

  To switch responses when receiving an MOM message, modify the ``getRequestId`` method of the action class in the same way as when receiving an HTTP message.

Intentionally delay the response when receiving a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To delay the response intentionally when receiving a message, 
implement the delay process directly in the ``handle`` method of action class as follows.

.. code-block:: java

  public class HttpIncomingSimulateAction implements Handler<HttpRequest, HttpResponse> {

    public HttpResponse handle(HttpRequest request, ExecutionContext context) {

        try {
            // Delay for 10 seconds
            TimeUnit.SECONDS.sleep(10);
        } catch (InterruptedException e) {
            // Exception handling
        }

        // Omitted
    }
  }
