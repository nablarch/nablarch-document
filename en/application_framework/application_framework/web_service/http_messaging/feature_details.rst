Details of Function
========================================
.. contents:: Table of Contents
  :depth: 3
  :local:

Initialization of Nablarch
----------------------------------------
See :ref:`initializing Nablarch for web application <web_feature_details-nablarch_initialization>` .

.. _http_messaging-request_validation:

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

  The :ref:`exclusive_control` function cannot be used in HTTP messaging because it is assumed to work with the client (taglib).

.. _http_messaging-action_mapping:

Mapping of URI and action
----------------------------------------
* :ref:`http_request_java_package_mapping`

.. tip::
 :ref:`router_adaptor` cannot be used for HTTP messaging. 
 As HTTP messaging creates an action class with :java:extdoc:`MessagingAction<nablarch.fw.messaging.action.MessagingAction>` provided by :ref:`mom_system_messaging` , 
 there is no assumption that the methods of the action class are called separately according to the URI.

Internationalization
----------------------------------------
See the following for multilingualization of static resources.

* :ref:`Multilingualization of messages <message-multi_lang>`
* :ref:`Multilingualization of code names <code-use_multilingualization>`

Authentication
----------------------------------------
Authentication is not provided as a flake work because the specifications vary according depending on the project requirements.

Permission check
----------------------------------------
* :ref:`permission_check`

Response to be returned on error
--------------------------------------------------
* :ref:`http_messaging_error_handler`
