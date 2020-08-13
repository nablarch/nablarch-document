.. _`restful_web_service_functional_comparison`:

Function Comparison of JAX-RS Support /JSR339/HTTP Messaging
=============================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

This section shows the comparison of the following functions:

 - :ref:`Nablarch JAX-RS support <restful_web_service>`
 - :ref:`HTTP messaging <http_messaging>`
 - `JSR 339: JAX-RS 2.0: The Java API for RESTful Web Services(external site, English) <https://jcp.org/en/jsr/detail?id=339>`_

.. tip::

 Only for Nablarch's JAX-RS support and HTTP messaging only, click the mark in the table to jump to the description page of the manual.

.. |br| raw:: html

   <br />

.. list-table:: Function comparison (✓: Provided △: Partially provided ×: Not provided -: Not applicable)
   :header-rows: 1
   :class: something-special-class

   * - Function
     - JAX-RS |br| support
     - HTTP |br| messaging
     - JSR 339
   * - Request and resource method mapping
     - :ref:`△ <rest-action_mapping>`
     - :ref:`✓ <http_messaging-action_mapping>`
     - ✓
   * - Mapping of request and resource method
     - :ref:`△ <rest-path_query_param>`
     - × [1]_
     - ✓
   * - Mapping of HTTP method
     - :ref:`△ <rest-action_mapping>`
     - × [1]_
     - ✓
   * - Convert request/response |br| according to the media type
     - :ref:`△ <body_convert_handler>`
     - × [1]_
     - ✓
   * - Entity validation
     - :ref:`✓ <rest-request_validation>`
     - :ref:`✓ <http_messaging-request_validation>`
     - ✓
   * - Injection to resource class (CDI)
     - × [2]_
     - × [2]_
     - ✓
   * - Filter for request/response
     - × [3]_
     - × [3]_
     - ✓
   * - Interceptor for reading and writing the body
     - × [4]_
     - × [5]_
     - ✓
   * - Client API
     - × [6]_
     - :ref:`✓ <http_system_messaging-message_send>`
     - ✓
   * - Asynchronous operation
     - × [7]_
     - × [7]_
     - ✓
   * - Error log output
     - :ref:`✓ <jaxrs_response_handler-error_log>`
     - :ref:`✓ <http_messaging_error_handler-error_response_and_log>`
     - －
   * - Checking the maximum capacity of the request body
     - × [8]_
     - :ref:`✓ <http_messaging_request_parsing_handler-limit_size>`
     - －
   * - Output of the trail log
     - × [9]_
     - :ref:`✓ <messaging_log>`
     - －
   * - Retransmission control
     - × [9]_
     - :ref:`✓ <message_resend_handler>`
     - －
   * - Service availability check
     - × [10]_
     - × [10]_
     - －
   * - Transaction control
     - × [11]_
     - × [11]_
     - －
   * - Callback on business process errors
     - × [12]_
     - :java:extdoc:`✓ <nablarch.fw.messaging.action.MessagingAction>`
     - －

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
