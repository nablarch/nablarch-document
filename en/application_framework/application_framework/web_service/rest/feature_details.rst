Details of Function
========================================
.. contents:: Table of Contents
  :depth: 3
  :local:

Initialization of Nablarch
----------------------------------------
See :ref:`initializing Nablarch for web application <web_feature_details-nablarch_initialization>`.

.. _rest-request_validation:
 
Input value check
----------------------------------------
* :ref:`Input value check <validation>`

Database access
----------------------------------------
* :ref:`Database access <database_management>`

Exclusive control
----------------------------------------
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`

.. important::

  RESTful web services do not support optimistic locking using `ETag` or `If-Match`.
  Therefore, when performing optimistic locking with RESTful web services, include the version number directly in the request body.

.. important::

  The :ref:`exclusive_control` function cannot be used in RESTful web services
  because it is assumed to work with the client (taglib).

.. _rest-action_mapping:

Mapping of URIs and resource (action) classes
------------------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/resource_signature

* :ref:`router_adaptor`
* :ref:`Method signature of the resource class <rest_feature_details-method_signature>`

.. _rest-path_query_param:

Path and query parameters
----------------------------------------------------------------------------------------------------
* :ref:`rest_feature_details-path_param`
* :ref:`rest_feature_details-query_param`

Response headers
----------------------------------------------------------------------------------------------------
* :ref:`Setting individual response headers in resource class methods <rest_feature_details-response_header>`
* :ref:`jaxrs_response_handler-response_finisher`

Internationalization
----------------------------------------
See the following for multilingualization of static resources.

* :ref:`Multilingualization of messages <message-multi_lang>`
* :ref:`Multilingualization of code names <code-use_multilingualization>`

Authentication
----------------------------------------
Authentication is not provided as a framework because the specifications vary according depending on the project requirements.

Permission check
----------------------------------------
Permission check is not provided as a framework because the specifications vary according depending on the project requirements.

Response to be returned on error
--------------------------------------------------
* :ref:`jaxrs_response_handler-error_response_body`
* :ref:`jaxrs_response_handler-individually_error_response`


Scale-out design for web application
---------------------------------------

* :ref:`stateless_web_app`

CSRF measures
----------------------------------------
* :ref:`CSRF measures <csrf_token_verification_handler>`

CORS
----------------------------------------
* :ref:`CORS <cors_preflight_request_handler>`