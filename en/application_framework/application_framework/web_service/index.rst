.. _`web_service`:

Web Service
==================================================
This chapter provides the information needed to develop web services using the Nablarch application framework.

Nablarch provides the following two frameworks for RESTful web services.

.. toctree::
  :maxdepth: 1

  rest/index
  http_messaging/index

.. _web_service-recommended_jaxrs:

Although web services can be built using either framework,
creating web services using :ref:`restful_web_service` is recommended for the following reasons.

Reason
  In :ref:`restful_web_service`, a web service can be easily built using some annotations defined in `Jakarta RESTful Web Services(external site) <https://jakarta.ee/specifications/restful-ws/>`_ .
  
  On the other hand, :ref:`http_messaging` cannot be flexibly designed and implemented because of the following restrictions on the body, HTTP headers and exception control.

  * Control area for Nablarch is required in the HTTP header and body.

    When building a web service that works with an already built external system, the difficulty of design and implementation is high.

  * Customizing the items in the response header is not easy.

    As described in :ref:`http_messaging_response_building_handler-header`, the handler has to be replaced to change the response header.

  * Depends on the :ref:`data_format` function.
  
    The development cost increases as a format definition file needs to be created.It is also not easy to customize.
    The input and output data have to be handled with a Map object, which can easily cause implementation errors.

  * Detailed exception handling is not possible as all exceptions when parsing a request body are mapped to a single exception class.

    Because all exceptions in parsing are thrown as :java:extdoc:`MessagingException <nablarch.fw.messaging.MessagingException>`, detailed process control based on the root cause cannot be performed.

.. tip::

  Refer to :ref:`restful_web_service_functional_comparison` for differences between the functions provided by :ref:`restful_web_service` and :ref:`http_messaging`.

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison
