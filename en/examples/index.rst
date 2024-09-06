.. _`example_application`:

=======
Example
=======

Example is an implementation example that demonstrates how to use the features of the Nablarch Application Framework, and is created for each :ref:`runtime platform <runtime_platform>`.
This chapter describes the procedures for building the environment and executing the application, which are necessary for each Example.


  .. tip::
    Example is not intended to be used to create a full-fledged applications by modifying each Example.
    If you want to create a full-fledged application, create it from :ref:`blank_project`.
 
 
How to Run Example
==================

Procedure to build the environment
----------------------------------
Example uses Apache Maven to build and run the application. Refer to the following page to install Apache Maven on the PC and configure the necessary settings.

:ref:`maven`


Procedure to execute
--------------------

For instructions on how to run Example, refer to the README at the top of the GitHub repository for each Example.

Running on Java 11 or higher
----------------------------

Example is assumed to run in Java 8.
If you want to run it on Java 11 or higher, you will need to modify the dependent libraries.
For more information, see the description of the blank project below.

* :ref:`setup_blank_project_for_Java11`
* :ref:`setup_blank_project_for_Java17`
* :ref:`setup_blank_project_for_Java21`


List of Example
===============

Example for each runtime platform is shown below. Explanations of the implementations are also provided, so refer to the “Explanation” links in the following list as necessary.

Web application
---------------

- `Web Application (JSP) <https://github.com/nablarch/nablarch-example-web>`_ (:ref:`Explanation <getting_started>`)
- `Web Application (Thymeleaf) <https://github.com/nablarch/nablarch-example-thymeleaf-web>`_ (:ref:`Explanation <web_thymeleaf_adaptor>`)


Web Service
-----------

- `RESTful Web Service <https://github.com/nablarch/nablarch-example-rest>`_ (:ref:`Explanation <rest_getting_started>`)
- `HTTP Messaging (receiving) <https://github.com/nablarch/nablarch-example-http-messaging>`_ (:ref:`Explanation <http-messaging_getting_started>`)
- `HTTP Messaging (sending) <https://github.com/nablarch/nablarch-example-http-messaging-send>`_ (:ref:`Explanation <http_system_messaging-message_send>`)


Batch Application
-----------------

- `Jakarta Batch-compliant Batch Application <https://github.com/nablarch/nablarch-example-batch-ee>`_ (:ref:`Explanation <jBatch_getting_started>`)
- `Nablarch Batch Application <https://github.com/nablarch/nablarch-example-batch>`_ (:ref:`Explanation <nablarch_Batch_getting_started>`)

  
Messaging
---------

.. _`example_application-mom_system_messaging`:

- Messaging with MOM (:ref:`Explanation <mom_messaging_getting_started>`)
  
  - `Sending asynchronous messages <https://github.com/nablarch/nablarch-example-mom-delayed-send>`_ 
  - `Sending synchronous messages <https://github.com/nablarch/nablarch-example-mom-sync-send-batch>`_
  - `Receiving asynchronous messages <https://github.com/nablarch/nablarch-example-mom-delayed-receive>`_
  - `Receiving synchronous messages <https://github.com/nablarch/nablarch-example-mom-sync-receive>`_

- `Messaging Using Tables as Queues <https://github.com/nablarch/nablarch-example-db-queue>`_ (:ref:`Explanation <db_messaging_getting_started>`)
