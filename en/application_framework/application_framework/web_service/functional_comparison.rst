.. _`restful_web_service_functional_comparison`:

Function Comparison of JAX-RS Support /JSR339/HTTP Messaging
=============================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

This section shows the comparison of the following functions:

 - :ref:`Nablarch JAX-RS support <restful_web_service>`
 - :ref:`HTTP messaging <http_messaging>`
 - `JSR 339: JAX-RS 2.0: The Java API for RESTful Web Services(external site) <https://jcp.org/en/jsr/detail?id=339>`_

.. tip::

 Only for Nablarch's JAX-RS support and HTTP messaging only, click the mark in the table to jump to the description page of the manual.

.. |br| raw:: html

   <br />

.. list-table:: Function comparison (A: Provided B: Partially provided C: Not provided D: Not applicable)
   :header-rows: 1
   :class: something-special-class

   * - Function
     - JAX-RS |br| support
     - HTTP |br| messaging
     - JSR 339
   * - Request and resource method mapping
     - :ref:`B <rest-action_mapping>`
     - :ref:`A <http_messaging-action_mapping>`
     - A
   * - Mapping of request and resource method
     - :ref:`B <rest-path_query_param>`
     - C [1]_
     - A
   * - Mapping of HTTP method
     - :ref:`B <rest-action_mapping>`
     - C [1]_
     - A
   * - Convert request/response |br| according to the media type
     - :ref:`B <body_convert_handler>`
     - C [1]_
     - A
   * - Entity validation
     - :ref:`A <rest-request_validation>`
     - :ref:`A <http_messaging-request_validation>`
     - A
   * - Injection to resource class (CDI)
     - C [2]_
     - C [2]_
     - A
   * - Filter for request/response
     - C [3]_
     - C [3]_
     - A
   * - Interceptor for reading and writing the body
     - C [4]_
     - C [5]_
     - A
   * - Client API
     - C [6]_
     - :ref:`A <http_system_messaging-message_send>`
     - A
   * - Asynchronous operation
     - C [7]_
     - C [7]_
     - A
   * - Error log output
     - :ref:`A <jaxrs_response_handler-error_log>`
     - :ref:`A <http_messaging_error_handler-error_response_and_log>`
     - D
   * - Checking the maximum capacity of the request body
     - C [8]_
     - :ref:`A <http_messaging_request_parsing_handler-limit_size>`
     - D
   * - Output of the trace log
     - C [9]_
     - :ref:`A <messaging_log>`
     - D
   * - Retransmission control
     - C [9]_
     - :ref:`A <message_resend_handler>`
     - D
   * - Service availability check
     - C [10]_
     - C [10]_
     - D
   * - Transaction control
     - C [11]_
     - C [11]_
     - D
   * - Callback on business process errors
     - C [12]_
     - :java:extdoc:`A <nablarch.fw.messaging.action.MessagingAction>`
     - D

.. [1] HTTP messaging is not designed in consideration of REST. Use JAX-RS support for RESTful web services.
.. [2] CDI is not available because JAX-RS support and HTTP messaging run as Nablarch web applications.
.. [3] Create a handler for creating a request/response filter.
.. [4] Create a BodyConverter with JAX-RS support for creating an interceptor to read and write the body.
.. [5] Use data format of Nablarch to read and write the body. Create a DataRecordFormatter to change the data format.
.. [6] If JAX-RS client is needed, use a JAX-RS implementation (such as Jersey or RESTEasy).
.. [7] It is assumed that asynchronous operation in the server is not required. Support will be considered if there is a request.
.. [8] Use the function to check the request size on the web server or application server.
.. [9] Each application is assumed to have different requirements. Design/implement in the application.
.. [10] If a service availability check in Nablarch matches the application's requirements, use the check. If a check does not match, design/implement the check in the application.
.. [11] Use the transaction management available in Nablarch.
.. [12] Error handling is assumed to be common and JaxRsResponseHandler is assumed to be customized. To handle errors individually in business operations, use try/catch in resource methods.
