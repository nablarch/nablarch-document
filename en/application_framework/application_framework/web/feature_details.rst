Details of Function
========================================

.. contents:: Table of Contents
  :depth: 3
  :local:

.. _web_feature_details-nablarch_initialization:

Initialization of Nablarch
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/nablarch_servlet_context_listener
  feature_details/web_front_controller

To initialize Nablarch, :ref:`configuration for loading the system repository <nablarch_servlet_context_listener>`
and :ref:`configuration of handler queue (construction) <web_front_controller>` are required.

Input value check
----------------------------------------
.. toctree::
    :maxdepth: 1
    :hidden:

    feature_details/error_message

* :ref:`Input value check <validation>`
* :doc:`Screen display of error messages <feature_details/error_message>`

Database access
----------------------------------------
* :ref:`Database access <database_management>`

Exclusive control
----------------------------------------
Although 2 types of exclusive control are offered,
:ref:`universal_dao` is recommended based on the description in
:ref:`reason UniversalDao is recommended <exclusive_control-deprecated>`.

* :ref:`exclusive_control`
* :ref:`universal_dao`

  * :ref:`universal_dao_jpa_optimistic_lock`
  * :ref:`universal_dao_jpa_pessimistic_lock`

Upload File
----------------------------------------
* :ref:`multipart_handler-read_upload_file`

File download
----------------------------------------
Although 2 types of file download are offered,
:ref:`data_bind` is recommended based on the description in
:ref:`reason data bind is recommended <data_converter-data_bind_recommend>`.

* :ref:`Downloading files using the data binding function <data_bind-file_download>`
* :ref:`File download using general data format function <data_format-file_download>`

Refer to :ref:`universal_dao-lazy_load` when downloading large amounts of data,
and be careful not to expand the database search results on the heap.

Mapping of URI and action
----------------------------------------
Although the following 2 methods are offered,
:ref:`router_adaptor` is recommended based on the reasons described in :ref:`reason why routing adapter is recommended<http_request_java_package_mapping-router_adaptor>`.

* :ref:`router_adaptor`
* :ref:`http_request_java_package_mapping`

Duplicate form submission prevention
----------------------------------------
* :ref:`Duplicate form submission prevention <tag-double_submission>`

Also see :ref:`use_token_interceptor` if you are using a template engine other than JSP.

Retain input data
----------------------------------------
* :ref:`session_store`

Pagination
----------------------------------------
See :ref:`database_management` for information on how to perform a range-specific search from a database.

Not provided by the framework in the client because the specifications vary depending on the project requirements.

Screen creation
----------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/jsp_session
  feature_details/view/other

* When JSP is used

  * :ref:`Screen development using JSP taglib <tag>`
  * :ref:`jsp_session`

* When using a template engine other than JSP

  * :ref:`Screen development using Thymeleaf <web_thymeleaf_adaptor>`
  * :ref:`view_other`

Internationalization
----------------------------------------
See the following for multilingualization of static resources.

* :ref:`Multilingualization of messages <message-multi_lang>`
* :ref:`Multilingualization of code names <code-use_multilingualization>`

Although the following two methods are provided to switch the language of the text to be displayed on the screen,
the screen layout may be corrupted when using the internationalization support
:ref:`internationalization of message tags <tag-write_message>` in the message tag.
For this reason, use :ref:`internationalization of message tags <tag-write_message>` only when a layout corrupted is acceptable.

* :ref:`Internationalization of message tags <tag-write_message>`
* :ref:`Switch resource path for each language <tag_change_resource_path_of_lang>`

Authentication
----------------------------------------
Authentication is not provided as a flake work because the specifications vary depending on the project requirements.
Implement authentication in the project according to the project requirements.

See below for information on retaining the authentication information.

* :ref:`session_store-authentication_data`

Permission check
----------------------------------------
* :ref:`permission_check`


.. _web_feature_details-status_code:

Status code
--------------------------------------------------
* `Using the status code (external site) <http://qiita.com/kawasima/items/e48180041ace99842779>`_


Screen transitions and status codes in the case of errors
----------------------------------------------------------
.. toctree::
  :maxdepth: 1
  :hidden:

  feature_details/forward_error_page

* :ref:`Configuring the default destination page for the status code <HttpErrorHandler_DefaultPage>`
* :ref:`Transition to the error page for the exception class in the handler <forward_error_page-handler>`
* Specify the transition destination when an action error occurs

  * Define a transition destination corresponding to an exception class (:ref:`on_error_interceptor` , :ref:`on_errors_interceptor`)
  * :ref:`Defining multiple transition destinations for a single exception <forward_error_page-try_catch>`
* `Using the status code (external site) <http://qiita.com/kawasima/items/e48180041ace99842779>`_

Send MOM message
----------------------------------------
* :ref:`Sending synchronous message<mom_system_messaging-sync_message_send>`


Scale-out design for web application
---------------------------------------

* :ref:`stateless_web_app`

CSRF measures
----------------------------------------
* :ref:`CSRF measures <csrf_token_verification_handler>`

Use web applications and RESTful web services together
----------------------------------------------------------------
* :ref:`Change the name of the delegating web front controller <change_web_front_controller_name>`
